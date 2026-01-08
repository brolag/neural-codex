from __future__ import annotations

from pathlib import Path

PROMPT_NAMES = [
    "neural.loop-cancel",
    "neural.plan-execute",
    "neural.question",
    "neural.pv",
    "neural.sync",
    "neural.changelog-architect",
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


def test_required_prompts_exist() -> None:
    for name in PROMPT_NAMES:
        path = _prompt_path(name)
        assert path.exists(), f"Missing prompt: {path}"


def test_required_prompts_have_description_and_argument_hint() -> None:
    for name in PROMPT_NAMES:
        path = _prompt_path(name)
        front = _front_matter(_read_prompt(path))
        assert front.get("description"), f"Missing description in {path}"
        assert front.get("argument-hint"), f"Missing argument-hint in {path}"


def test_required_prompts_avoid_claude_specific_terms() -> None:
    for name in PROMPT_NAMES:
        text = _read_prompt(_prompt_path(name)).lower()
        for term in BANNED_TERMS:
            assert term not in text, f"Found banned term '{term}' in {name}"
