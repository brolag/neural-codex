from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "neural-codex"
CORE_SKILLS = {"discover", "spec", "craft", "vet", "exercise"}


def _load(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def test_manifest_has_valid_current_plugin_shape() -> None:
    manifest = _load(PLUGIN / ".codex-plugin" / "plugin.json")
    assert manifest["name"] == "neural-codex"
    assert manifest["version"] == "1.0.0"
    assert manifest["skills"] == "./skills/"
    assert manifest["repository"] == "https://github.com/brolag/neural-codex"
    assert manifest["homepage"] == "https://brolag.github.io/neural-codex/"
    assert manifest["author"] == {
        "name": "Alfredo Bonilla",
        "url": "https://github.com/brolag",
    }
    interface = manifest["interface"]
    assert isinstance(interface, dict)
    assert interface["displayName"] == "Neural Codex"
    assert len(interface["defaultPrompt"]) <= 3

    # Conventional hooks/hooks.json is auto-discovered. Optional components are
    # omitted unless their companion files exist.
    assert "hooks" not in manifest
    assert "apps" not in manifest
    assert "mcpServers" not in manifest
    assert "license" not in manifest


def test_every_manifest_path_stays_inside_plugin() -> None:
    manifest = _load(PLUGIN / ".codex-plugin" / "plugin.json")
    for key in ("skills", "apps", "mcpServers", "hooks"):
        value = manifest.get(key)
        if not isinstance(value, str):
            continue
        assert value.startswith("./")
        resolved = (PLUGIN / value).resolve()
        assert resolved == PLUGIN.resolve() or PLUGIN.resolve() in resolved.parents
        assert resolved.exists()


def test_repo_marketplace_points_to_the_nested_plugin() -> None:
    marketplace = _load(ROOT / ".agents" / "plugins" / "marketplace.json")
    assert marketplace["name"] == "neural-codex"
    assert marketplace["interface"] == {"displayName": "Neural Codex"}
    assert marketplace["plugins"] == [
        {
            "name": "neural-codex",
            "source": {"source": "local", "path": "./plugins/neural-codex"},
            "policy": {
                "installation": "AVAILABLE",
                "authentication": "ON_INSTALL",
            },
            "category": "Developer Tools",
        }
    ]


def test_plugin_contains_exactly_the_reviewed_skills() -> None:
    skills_root = PLUGIN / "skills"
    actual = {path.name for path in skills_root.iterdir() if path.is_dir()}
    assert actual == CORE_SKILLS
    for name in CORE_SKILLS:
        assert (skills_root / name / "SKILL.md").is_file()
        assert (skills_root / name / "agents" / "openai.yaml").is_file()


def test_no_duplicate_or_legacy_distribution_roots_remain() -> None:
    for relative in (
        ".codex",
        "agents",
        ".agents/skills",
        "README-neural-codex.md",
        "scripts/setup-global.sh",
        "scripts/setup-project.sh",
        "scripts/ralph-loop.sh",
        "plans/prd.json",
        "plans/progress.jsonl",
    ):
        assert not (ROOT / relative).exists(), relative

    skill_files = set(ROOT.glob("**/SKILL.md"))
    expected = {PLUGIN / "skills" / name / "SKILL.md" for name in CORE_SKILLS}
    assert skill_files == expected


def test_default_plugin_hook_manifest_exists() -> None:
    assert (PLUGIN / "hooks" / "hooks.json").is_file()
