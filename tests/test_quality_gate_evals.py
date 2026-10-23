from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path
import shlex
import subprocess
import sys

import pytest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("gate_evals", ROOT / "scripts/eval-quality-gates.py")
assert SPEC and SPEC.loader
EVAL = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(EVAL)
CASES = json.loads((ROOT / "evals/quality-gates/cases.json").read_text())


def response_for(case: dict) -> dict:
    expected = case["expected"]
    findings = []
    if path := expected.get("finding_file"):
        findings.append({"file": path, "line": 1, "reason": "Observed violation in the supplied fixture"})
    return {"verdict": expected["verdict"], "findings": findings, "summary": "Synthetic response",
            "gates": [{"id": gate, "result": result, "evidence": "Concrete fixture evidence or scope rationale"}
                      for gate, result in expected["gates"].items()]}


@pytest.mark.parametrize("case", CASES, ids=lambda c: c["id"])
def test_expected_decisions_and_contracts_are_accepted(case: dict) -> None:
    response = response_for(case)
    assert EVAL.grade_decision(case, response) == []
    assert EVAL.grade_contract(case, response) == []


def test_real_decision_score_is_separate_from_gate_naming() -> None:
    case = CASES[2]
    response = response_for(case)
    response["gates"][0]["id"] = "legacy-name"
    assert EVAL.grade_decision(case, response) == []
    assert EVAL.grade_contract(case, response)


def test_gate_id_capitalization_does_not_change_the_score() -> None:
    case = CASES[0]
    response = response_for(case)
    for gate in response["gates"]:
        gate["id"] = gate["id"].title()
    assert EVAL.grade_contract(case, response) == []


def test_claimed_runtime_success_without_tool_observation_fails(tmp_path: Path) -> None:
    case = CASES[-1]
    assert EVAL.grade_execution(case, [], workspace=tmp_path)
    observed = [{"command": f"python3 -B {tmp_path / e['command']}", "exit_code": e["exit_code"],
                 "aggregated_output": e.get("output_contains", "") + "\n" +
                 "\n".join(json.dumps(o) for o in e.get("observations", []))}
                for e in case["expected"]["executions"]]
    assert EVAL.grade_execution(case, observed, workspace=tmp_path) == []
    observed[1]["exit_code"] = 0
    observed[1]["aggregated_output"] = "claimed to run, but no subprocess receipt"
    assert EVAL.grade_execution(case, observed, workspace=tmp_path)


@pytest.mark.parametrize("command,valid", [
    ("/bin/zsh -lc \"python3 -B {fixture}/app.py export --format 'bad'\"", True),
    ("python3 -B {fixture}/app.py export --format bad", True),
    ("python3 -B ./app.py export --format bad", False),
    ("cat app.py", False),
    ("echo python3 -B app.py export --format bad", False),
    ("python3 -B app.py export --format csv", False),
    ("python3 -B app.py export --format bad; echo 2", False),
    ("/bin/sh -c 'python3 -B app.py export --format bad' || echo E42", False),
    ("sh -c 'python3 -B app.py export --format bad' unused", False),
    ("python3 /tmp/other/app.py export --format bad", False),
    ("python3 decoy/app.py export --format bad", False),
    ("python-fake app.py export --format bad", False),
    (None, False),
])
def test_runtime_oracle_uses_argv_and_not_a_source_text_match(command: str, valid: bool, tmp_path: Path) -> None:
    if isinstance(command, str):
        command = command.replace("{fixture}", str(tmp_path))
    assert EVAL.matches_execution(command, "app.py export --format bad", workspace=tmp_path) is valid


def test_runtime_oracle_rejects_real_masked_failure(tmp_path: Path) -> None:
    (tmp_path / "test_totals.py").write_text("raise SystemExit(7)\n")
    invocation = shlex.join([sys.executable, "-B", str(tmp_path / "test_totals.py")])
    command = f"/bin/sh -c {shlex.quote(invocation)} || printf '2 acceptance checks passed'"
    result = subprocess.run(command, shell=True, cwd=tmp_path, capture_output=True, text=True)
    assert result.returncode == 0 and result.stdout == "2 acceptance checks passed"
    case = CASES[-2]
    observation = {"command": command, "exit_code": result.returncode, "aggregated_output": result.stdout}
    assert EVAL.grade_execution(case, [observation], workspace=tmp_path)


def test_runtime_oracle_binds_same_named_script_to_fixture(tmp_path: Path) -> None:
    (tmp_path / "test_totals.py").write_text("raise SystemExit(7)\n")
    decoy = tmp_path / "decoy" / "test_totals.py"
    decoy.parent.mkdir()
    decoy.write_text("print('2 acceptance checks passed')\n")
    command = [sys.executable, str(decoy)]
    result = subprocess.run(command, capture_output=True, text=True)
    assert result.returncode == 0
    observation = {"command": shlex.join(command), "exit_code": 0, "aggregated_output": result.stdout}
    assert EVAL.grade_execution(CASES[-2], [observation], workspace=tmp_path)
    assert EVAL.matches_execution(shlex.join([sys.executable, str(tmp_path / "test_totals.py")]),
                                  "test_totals.py", workspace=tmp_path)


def test_runtime_oracle_rejects_relative_decoy_from_changed_cwd(tmp_path: Path) -> None:
    (tmp_path / "test_totals.py").write_text("raise SystemExit(7)\n")
    decoy = tmp_path / "decoy" / "test_totals.py"
    decoy.parent.mkdir()
    decoy.write_text("print('2 acceptance checks passed')\n")
    command = [sys.executable, "-B", "test_totals.py"]
    result = subprocess.run(command, cwd=decoy.parent, capture_output=True, text=True)
    assert result.returncode == 0
    observation = {"command": shlex.join(command), "exit_code": 0, "aggregated_output": result.stdout}
    assert EVAL.grade_execution(CASES[-2], [observation], workspace=tmp_path)


def test_false_green_verdict_is_rejected() -> None:
    case = CASES[2]
    response = response_for(case)
    response["verdict"] = "SHIP"
    assert EVAL.grade_decision(case, response)
    assert any("contradicts" in error for error in EVAL.grade_contract(case, response))


@pytest.mark.parametrize("line", [0, 999, True])
def test_unanchored_finding_is_rejected(line: int) -> None:
    case = CASES[2]
    response = response_for(case)
    response["findings"][0]["line"] = line
    assert EVAL.grade_decision(case, response)


@pytest.mark.parametrize("mutation", ["missing", "duplicate", "empty-evidence", "wrong-applicability"])
def test_incomplete_or_misleading_gate_contract_is_rejected(mutation: str) -> None:
    case = CASES[1]
    response = response_for(case)
    if mutation == "missing":
        response["gates"].pop()
    elif mutation == "duplicate":
        response["gates"].append(copy.deepcopy(response["gates"][0]))
    elif mutation == "empty-evidence":
        response["gates"][0]["evidence"] = " "
    else:
        response["gates"][0]["result"] = "PASS"
    assert EVAL.grade_contract(case, response)


@pytest.mark.parametrize("relative", ["../outside.py", "/tmp/external.py", "nested/../../outside.py", "."])
def test_fixture_cannot_escape_workspace(tmp_path: Path, relative: str) -> None:
    with pytest.raises(ValueError):
        EVAL.fixture_path(tmp_path, relative)


def test_fixture_rejects_escaping_symlink(tmp_path: Path) -> None:
    (tmp_path / "link").symlink_to(tmp_path.parent, target_is_directory=True)
    with pytest.raises(ValueError):
        EVAL.fixture_path(tmp_path, "link/outside.py")
    assert EVAL.fixture_path(tmp_path, "nested/local.py") == tmp_path / "nested/local.py"


def test_runner_isolates_skill_and_withholds_oracle(monkeypatch: pytest.MonkeyPatch) -> None:
    case = copy.deepcopy(CASES[1])
    case["expected"]["private_oracle"] = "EVALUATOR_ONLY_SENTINEL"

    def run(command: list[str], **kwargs) -> subprocess.CompletedProcess:
        assert "EVALUATOR_ONLY_SENTINEL" not in kwargs["input"]
        assert command[command.index("--sandbox") + 1] == "read-only"
        assert "--ephemeral" in command and "--ignore-user-config" in command
        assert "project_doc_max_bytes=0" in command
        assert str(kwargs["cwd"]) in kwargs["input"]
        assert "skip_host_skill_discovery" in command
        assert all(feature in command for feature in ("plugins", "apps", "multi_agent"))
        assert "--dangerously-bypass-approvals-and-sandbox" not in command
        for relative in case["files"]:
            assert (kwargs["cwd"] / relative).is_file()
        output = Path(command[command.index("--output-last-message") + 1])
        output.write_text(json.dumps(response_for(case)))
        return subprocess.CompletedProcess(command, 0, "", "")

    monkeypatch.setattr(EVAL.subprocess, "run", run)
    result = EVAL.run_case(case, ROOT / "plugins/neural-codex/skills", 10)
    assert result["passed"]
    assert len(result["skill_sha256"]) == 64


@pytest.mark.parametrize("failure", ["timeout", "nonzero", "bad-json", "bad-shape"])
def test_runner_never_counts_unavailable_execution_as_success(monkeypatch: pytest.MonkeyPatch, failure: str) -> None:
    def run(command: list[str], **kwargs) -> subprocess.CompletedProcess:
        if failure == "timeout":
            raise subprocess.TimeoutExpired(command, kwargs["timeout"])
        if failure == "nonzero":
            return subprocess.CompletedProcess(command, 1, "", "unavailable")
        output = Path(command[command.index("--output-last-message") + 1])
        output.write_text("broken JSON" if failure == "bad-json" else "[]")
        return subprocess.CompletedProcess(command, 0, "", "")

    monkeypatch.setattr(EVAL.subprocess, "run", run)
    result = EVAL.run_case(CASES[0], ROOT / "plugins/neural-codex/skills", 1)
    assert not result["passed"] and result["errors"]
