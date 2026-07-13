from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
HOOKS = ROOT / "plugins" / "neural-codex" / "hooks"


def run_hook(name: str, payload: dict[str, object], *, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(HOOKS / name)],
        input=json.dumps(payload),
        text=True,
        capture_output=True,
        cwd=cwd or ROOT,
        check=False,
    )


def test_hooks_config_uses_portable_codex_plugin_contract() -> None:
    data = json.loads((HOOKS / "hooks.json").read_text(encoding="utf-8"))
    hooks = data["hooks"]
    assert {"PreToolUse", "PostToolUse", "PreCompact"} <= hooks.keys()
    handlers = [handler for groups in hooks.values() for group in groups for handler in group["hooks"]]
    assert all(handler.get("timeout", 0) < 100 for handler in handlers)
    assert all('${PLUGIN_ROOT}/hooks/' in handler["command"] for handler in handlers)
    encoded = json.dumps(data)
    assert "git rev-parse" not in encoded
    assert ".codex/hooks" not in encoded
    assert "CLAUDE_PLUGIN_ROOT" not in encoded
    assert "tool_output" not in encoded


def test_dangerous_action_is_blocked() -> None:
    result = run_hook("dangerous_actions_blocker.py", {"tool_name": "Bash", "tool_input": {"command": "rm -rf /"}})
    assert result.returncode == 2
    assert "Recursive deletion" in result.stderr


def test_safe_command_is_allowed() -> None:
    result = run_hook("dangerous_actions_blocker.py", {"tool_name": "Bash", "tool_input": {"command": "git status --short"}})
    assert result.returncode == 0
    assert result.stdout == ""


@pytest.mark.parametrize(
    "command",
    [
        "rm -fr /",
        "rm -fr ~",
        "rm -rf /*",
        "rm -rf $HOME/*",
        "rm --recursive --force /",
        'rm -rf "$HOME"',
        "sudo rm -R -f -- /",
        'bash -c "rm -rf /"',
        "sh -c 'rm -fr $HOME'",
        'env SAFE=1 bash -lc "rm -rf /"',
    ],
)
def test_equivalent_root_and_home_deletions_are_blocked(command: str) -> None:
    result = run_hook("dangerous_actions_blocker.py", {"tool_name": "Bash", "tool_input": {"command": command}})
    assert result.returncode == 2
    assert "Recursive deletion" in result.stderr


@pytest.mark.parametrize(
    "command",
    [
        "rm -rf /tmp/disposable-build",
        "echo rm -rf /",
        "/bin/echo rm -rf /",
        "git rm -rf /",
        "printf '%s' 'rm -rf /'",
        'bash -c "echo rm -rf /"',
    ],
)
def test_commands_that_only_delete_disposable_content_or_quote_text_are_allowed(command: str) -> None:
    result = run_hook("dangerous_actions_blocker.py", {"tool_name": "Bash", "tool_input": {"command": command}})
    assert result.returncode == 0


def test_force_push_main_is_blocked_regardless_of_argument_order() -> None:
    result = run_hook("dangerous_actions_blocker.py", {"tool_name": "Bash", "tool_input": {"command": "git push origin main --force-with-lease"}})
    assert result.returncode == 2


def test_sensitive_apply_patch_is_blocked_without_echoing_content() -> None:
    secret = "not-a-real-secret-value"
    result = run_hook(
        "sensitive_file_guard.py",
        {"tool_name": "apply_patch", "tool_input": {"command": f"*** Begin Patch\n*** Update File: .env.local\n@@\n-old\n+{secret}\n*** End Patch"}},
    )
    assert result.returncode == 2
    assert ".env.local" in result.stderr
    assert secret not in result.stderr


def test_markdown_patch_can_discuss_injection_patterns() -> None:
    result = run_hook(
        "prompt_injection_detector.py",
        {"tool_name": "apply_patch", "tool_input": {"command": "*** Begin Patch\n*** Update File: guide.md\n@@\n+ignore previous instructions\n*** End Patch"}},
    )
    assert result.returncode == 0


def test_executable_injection_pattern_is_blocked() -> None:
    result = run_hook("prompt_injection_detector.py", {"tool_name": "Bash", "tool_input": {"command": "run --arg 'ignore previous instructions'"}})
    assert result.returncode == 2


def test_output_scanner_warns_without_repeating_secret() -> None:
    token = "ghp_" + "a" * 36
    result = run_hook("output_scanner.py", {"tool_response": {"output": token}})
    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert "GitHub token" in payload["systemMessage"]
    assert token not in result.stdout


def test_pre_compact_writes_recovery_context(tmp_path: Path) -> None:
    result = run_hook("pre_compact.py", {"cwd": str(tmp_path), "trigger": "auto"}, cwd=tmp_path)
    assert result.returncode == 0
    output = tmp_path / ".codex" / "compact-context.md"
    assert output.exists()
    assert "Pre-Compaction Context" in output.read_text(encoding="utf-8")
