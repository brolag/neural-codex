#!/usr/bin/env python3
"""Run synthetic skill-decision probes in fresh, read-only Codex sessions."""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import shlex
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[1]
EVALS = ROOT / "evals" / "quality-gates"


def grade_decision(case: dict, response: dict) -> list[str]:
    """Check the verdict and defect location independently of gate naming."""
    errors = []
    expected = case["expected"]
    if response.get("verdict") != expected["verdict"]:
        errors.append(f"Expected verdict {expected['verdict']}, got {response.get('verdict')}")
    required_file = expected.get("finding_file")
    if required_file and not any(
        isinstance(f, dict) and f.get("file") == required_file
        and isinstance(f.get("line"), int) and not isinstance(f["line"], bool)
        and 1 <= f["line"] <= len(case["files"][required_file].splitlines())
        and isinstance(f.get("reason"), str) and f["reason"].strip()
        for f in response.get("findings", [])
    ):
        errors.append(f"Missing grounded finding in {required_file}")
    return errors


def grade_contract(case: dict, response: dict) -> list[str]:
    """Check explicit gate applicability/results separately from decisions."""
    errors = []
    gates = response.get("gates", [])
    if not isinstance(gates, list) or any(not isinstance(g, dict) for g in gates):
        return errors + ["Invalid gates list"]
    by_id = {g["id"].strip().casefold(): g for g in gates if isinstance(g.get("id"), str)}
    if len(by_id) != len(gates):
        errors.append("Gate IDs must be unique strings")
    for gate_id, result in case["expected"]["gates"].items():
        gate = by_id.get(gate_id, {})
        if gate.get("result") != result:
            errors.append(f"{gate_id}: expected {result}, got {gate.get('result')}")
        if not isinstance(gate.get("evidence"), str) or not gate["evidence"].strip():
            errors.append(f"{gate_id}: missing evidence or applicability rationale")
    if response.get("verdict") == "SHIP" and any(
        g.get("result") in {"FAIL", "NOT RUN"} for g in gates
    ):
        errors.append("SHIP contradicts an unresolved gate")
    return errors


def matches_execution(command: str, expected: str) -> bool:
    """Recognize a Python script invocation, including the CLI shell wrapper."""
    try:
        argv = shlex.split(command)
        if argv and Path(argv[0]).name in {"sh", "bash", "zsh"}:
            option = next(i for i, arg in enumerate(argv[1:], 1)
                          if arg.startswith("-") and "c" in arg)
            argv = shlex.split(argv[option + 1])
        if not argv or not Path(argv[0]).name.startswith("python"):
            return False
        rest = argv[1:]
        while rest and rest[0] in {"-B", "-u"}:
            rest = rest[1:]
        wanted = shlex.split(expected)
        return bool(rest and wanted and Path(rest[0]).name == wanted[0] and rest[1:] == wanted[1:])
    except (ValueError, StopIteration, IndexError):
        return False


def grade_execution(case: dict, executions: list[dict]) -> list[str]:
    """Require actual completed command observations for runnable fixtures."""
    def matches(item: dict, expected: dict) -> bool:
        if not matches_execution(item.get("command", ""), expected["command"]) or item.get("exit_code") != expected["exit_code"]:
            return False
        output = item.get("aggregated_output", "")
        if expected.get("output_contains", "") not in output:
            return False
        observations = []
        for line in output.splitlines():
            try:
                observations.append(json.loads(line))
            except ValueError:
                continue
        return all(observation in observations for observation in expected.get("observations", []))

    return [f"Missing observed execution: {expected['command']}"
            for expected in case["expected"].get("executions", [])
            if not any(matches(item, expected) for item in executions)]


def fixture_path(root: Path, relative: str) -> Path:
    candidate = (root / relative).resolve()
    if Path(relative).is_absolute() or not candidate.is_relative_to(root.resolve()) or candidate == root:
        raise ValueError(f"Fixture path escapes workspace: {relative}")
    return candidate


def run_case(case: dict, skills_root: Path, timeout: int) -> dict:
    skill = (skills_root / case["skill"] / "SKILL.md").read_text(encoding="utf-8")
    record = {"id": case["id"], "skill": case["skill"],
              "skill_sha256": hashlib.sha256(skill.encode()).hexdigest()}
    with tempfile.TemporaryDirectory(prefix="neural-gate-case-") as directory:
        workspace = Path(directory)
        for relative, content in case["files"].items():
            target = fixture_path(workspace, relative)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
        schema = workspace / "response.schema.json"
        schema.write_bytes((EVALS / "response.schema.json").read_bytes())
        output = workspace / "response.json"
        (workspace / "skill-under-test.md").write_text(skill, encoding="utf-8")
        prompt = (
            "This is an explicitly authorized synthetic decision evaluation, not a review "
            "of the harness implementation. You are a fresh evaluator with no author history. "
            "Read skill-under-test.md and use only those instructions and fixture files. Do not invoke another "
            "installed skill, delegate, browse, read secrets, change files, or access external "
            "systems. You may inspect the fixture and run its safe local Python commands. "
            "Apply the skill's gate decisions, but return the requested JSON decision summary "
            "instead of writing normal workflow artifacts. Do not invent observations or "
            "evidence. Include the fixture file and line in findings for any defect. "
            "Use the skill's own gate IDs; the schema does not prescribe them.\n\n"
            f"TASK:\n{case['task']}\n\n"
            f"Fixture files: {', '.join(case['files'])}\n"
        )
        command = ["codex", "exec", "--ephemeral", "--ignore-user-config",
                   "--enable", "skip_host_skill_discovery", "--disable", "plugins",
                   "--disable", "apps", "--disable", "multi_agent",
                   "--sandbox", "read-only", "--skip-git-repo-check", "--color", "never", "--json",
                   "--output-schema", str(schema), "--output-last-message", str(output), "-"]
        try:
            completed = subprocess.run(command, input=prompt, text=True, cwd=workspace,
                                       capture_output=True, timeout=timeout, check=False)
            if completed.returncode:
                record.update(passed=False, errors=[f"Codex exited {completed.returncode}"],
                              diagnostic=completed.stderr[-2000:])
            else:
                response = json.loads(output.read_text(encoding="utf-8"))
                if not isinstance(response, dict):
                    raise ValueError("Expected a decision object")
                executions = []
                for line in completed.stdout.splitlines():
                    event = json.loads(line)
                    item = event.get("item", {})
                    if item.get("type") == "command_execution" and any(
                        marker in item.get("command", "")
                        for marker in ("/.agents/skills/", "/.codex/skills/")
                    ):
                        raise ValueError("Host skill contamination: read outside selected fixture")
                    if event.get("type") == "item.completed" and item.get("type") == "command_execution":
                        executions.append(item)
                decisions = grade_decision(case, response) + grade_execution(case, executions)
                contract = grade_contract(case, response)
                observed = [{key: item.get(key) for key in ("command", "exit_code", "aggregated_output")}
                            for item in executions if any(matches_execution(item.get("command", ""), expected["command"])
                            for expected in case["expected"].get("executions", []))]
                record.update(passed=not (decisions + contract), errors=decisions + contract,
                              decision_passed=not decisions, contract_passed=not contract,
                              response=response, observed_executions=observed)
        except (OSError, ValueError, subprocess.TimeoutExpired) as exc:
            record.update(passed=False, errors=[f"Evaluation unavailable: {exc}"])
    return record


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skills-root", type=Path, default=ROOT / "plugins/neural-codex/skills")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--case", action="append", dest="selected")
    parser.add_argument("--timeout", type=int, default=240)
    args = parser.parse_args()
    cases = json.loads((EVALS / "cases.json").read_text(encoding="utf-8"))
    if args.selected:
        unknown = set(args.selected) - {c["id"] for c in cases}
        if unknown:
            parser.error(f"Unknown cases: {', '.join(sorted(unknown))}")
        cases = [c for c in cases if c["id"] in args.selected]
    if args.timeout <= 0:
        parser.error("--timeout must be positive")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    version = subprocess.run(["codex", "--version"], text=True, capture_output=True, check=True).stdout.strip()
    results = []
    with ThreadPoolExecutor(max_workers=2) as pool:
        for result in pool.map(lambda case: run_case(case, args.skills_root, args.timeout), cases):
            results.append(result)
            print(f"{'PASS' if result['passed'] else 'FAIL'} {result['id']}", flush=True)
            args.output.write_text(json.dumps({"codex_version": version, "results": results}, indent=2) + "\n")
    print(f"{sum(r.get('decision_passed', False) for r in results)}/{len(results)} decisions; "
          f"{sum(r.get('contract_passed', False) for r in results)}/{len(results)} gate contracts")
    return 0 if results and all(r["passed"] for r in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
