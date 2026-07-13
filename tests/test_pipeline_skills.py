from __future__ import annotations

from pathlib import Path


PIPELINE_SKILLS = ["discover", "spec", "craft", "vet", "exercise"]


def _root() -> Path:
    return Path(__file__).resolve().parents[1]


def _skill_dir(name: str) -> Path:
    return _root() / "plugins" / "neural-codex" / "skills" / name


def _skill_text(name: str) -> str:
    return (_skill_dir(name) / "SKILL.md").read_text(encoding="utf-8")


def _frontmatter_keys(text: str) -> set[str]:
    lines = text.splitlines()
    assert lines and lines[0] == "---"
    end = lines.index("---", 1)
    return {
        line.split(":", 1)[0].strip()
        for line in lines[1:end]
        if line and not line.startswith((" ", "\t")) and ":" in line
    }


def test_pipeline_skills_have_current_codex_shape() -> None:
    for name in PIPELINE_SKILLS:
        skill_dir = _skill_dir(name)
        assert (skill_dir / "SKILL.md").is_file()
        assert (skill_dir / "agents" / "openai.yaml").is_file()
        text = _skill_text(name)
        assert _frontmatter_keys(text) == {"name", "description"}
        assert f"name: {name}" in text
        assert "## Usage Examples" in text
        metadata = (skill_dir / "agents" / "openai.yaml").read_text(encoding="utf-8")
        assert f"${name}" in metadata


def test_discover_hands_a_grounded_map_to_spec() -> None:
    text = _skill_text("discover")
    for term in (
        "blindspot pass",
        "Known knowns",
        "Known unknowns",
        "Unknown knowns",
        "Unknown unknowns",
        "unknowns-map.md",
        "$spec",
        "Do not modify application code",
    ):
        assert term in text
    reference = _skill_dir("discover") / "references" / "unknowns-framework.md"
    assert "status: ready-for-spec | blocked" in reference.read_text(encoding="utf-8")


def test_spec_stops_for_approval_with_executable_contract() -> None:
    text = _skill_text("spec")
    for term in (
        "unknowns-map.md",
        "plan.md",
        "status: draft",
        "[needs: S1, S2]",
        "[tier:]",
        "Security invariants",
        "when",
        "requires",
        "ensures",
        "STOP for approval",
    ):
        assert term in text
    assert "Do not generate HTML" in text


def test_craft_requires_approval_and_independent_gates() -> None:
    text = _skill_text("craft")
    for term in (
        "status: approved",
        "baseline.md",
        "[needs:]",
        "$vet --spec",
        "$exercise --spec",
        "before -> after",
        "Do not commit, push, open or merge",
    ):
        assert term in text


def test_vet_and_exercise_are_separate_evidence_gates() -> None:
    vet = _skill_text("vet")
    exercise = _skill_text("exercise")
    for term in ("neutral review bundle", "fresh-reviewer", "SHIP", "HOLD", "active"):
        assert term in vet
    for term in ("real user behavior", "evidence", "PASS", "FAIL", "Do not infer behavior solely"):
        assert term in exercise


def test_plan_artifacts_reject_paths_outside_repository_plans() -> None:
    for name in ("spec", "craft", "exercise"):
        text = _skill_text(name)
        for term in (
            "os.path.commonpath",
            "../../outside/plan.md",
            "plans/../outside/plan.md",
            "/tmp/external-plan.md",
            "symlink",
        ):
            assert term in text, f"Missing path-containment contract {term!r} in {name}"


def test_vet_bundle_accounts_for_untracked_content() -> None:
    text = _skill_text("vet")
    for term in (
        "git ls-files --others --exclude-standard -z",
        "untracked-manifest.txt",
        "untracked/",
        "without following symlinks",
        "unexplained missing path prevents `SHIP`",
    ):
        assert term in text


def test_skills_do_not_reference_removed_harness_surfaces() -> None:
    banned = (
        ".claude/skills/",
        ".codex/prompts",
        "/prompts:",
        "AskUserQuestion",
        "Agent(",
        "Skill(",
        "Task(",
    )
    for name in PIPELINE_SKILLS:
        text = _skill_text(name)
        for term in banned:
            assert term not in text, f"Unsupported contract {term!r} in {name}"
