from __future__ import annotations

from pathlib import Path

META_PROMPT_NAMES = [
    "neural.meta.agent",
    "neural.meta.skill",
    "neural.meta.prompt",
    "neural.meta.improve",
    "neural.meta.eval",
    "neural.meta.brain",
]

BANNED_TERMS = [
    "claude",
    ".claude",
    "statusline",
    "tts",
]


def _prompt_path(name: str) -> Path:
    repo_root = Path(__file__).resolve().parents[1]
    return repo_root / ".codex" / "prompts" / f"{name}.md"


def _read_prompt(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _front_matter(text: str) -> dict[str, str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise AssertionError("Prompt is missing YAML front matter start")

    front_lines: list[str] = []
    for line in lines[1:]:
        if line.strip() == "---":
            break
        front_lines.append(line)
    else:
        raise AssertionError("Prompt is missing YAML front matter end")

    data: dict[str, str] = {}
    for line in front_lines:
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip()
    return data


def test_meta_prompts_exist() -> None:
    for name in META_PROMPT_NAMES:
        path = _prompt_path(name)
        assert path.exists(), f"Missing prompt: {path}"


def test_meta_prompts_have_descriptions() -> None:
    for name in META_PROMPT_NAMES:
        front = _front_matter(_read_prompt(_prompt_path(name)))
        assert front.get("description"), f"Missing description in {name}"


def test_meta_prompts_avoid_claude_specific_terms() -> None:
    for name in META_PROMPT_NAMES:
        text = _read_prompt(_prompt_path(name)).lower()
        for term in BANNED_TERMS:
            assert term not in text, f"Found banned term '{term}' in {name}"


def test_route_prompt_mentions_meta_prompts() -> None:
    route_text = _read_prompt(_prompt_path("neural.route")).lower()
    assert "neural.meta." in route_text, "neural.route should mention meta prompts"
