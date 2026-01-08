from __future__ import annotations

from pathlib import Path

OUTPUT_STYLE_PROMPT = "neural.output-style"
REQUIRED_STYLES = [
    "default",
    "concise",
    "table",
    "yaml",
    "html",
    "genui",
]


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _prompt_path(name: str) -> Path:
    return _repo_root() / ".codex" / "prompts" / f"{name}.md"


def _read_text(path: Path) -> str:
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


def test_output_style_prompt_exists() -> None:
    path = _prompt_path(OUTPUT_STYLE_PROMPT)
    assert path.exists(), f"Missing prompt: {path}"


def test_output_style_prompt_lists_required_styles() -> None:
    front = _front_matter(_read_text(_prompt_path(OUTPUT_STYLE_PROMPT)))
    hint = front.get("argument-hint", "").lower()
    for style in REQUIRED_STYLES:
        assert style in hint, f"Missing style '{style}' in argument-hint"


def test_output_style_prompt_avoids_tts() -> None:
    text = _read_text(_prompt_path(OUTPUT_STYLE_PROMPT)).lower()
    assert "tts" not in text, "Output style prompt should not mention TTS"


def test_readmes_document_output_styles() -> None:
    for readme in ["README.md", "README-neural-codex.md"]:
        text = _read_text(_repo_root() / readme).lower()
        assert "neural.output-style" in text, f"Missing output style line in {readme}"
        for style in REQUIRED_STYLES:
            assert style in text, f"Missing style '{style}' in {readme}"
