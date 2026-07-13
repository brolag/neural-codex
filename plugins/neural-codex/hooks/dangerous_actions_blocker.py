#!/usr/bin/env python3
"""PreToolUse hook that blocks high-confidence destructive Bash commands."""

from __future__ import annotations

import os
import posixpath
import re
import shlex
from glob import has_magic

from hook_utils import block, command_from, emit, read_event


BLOCKED_SUBSTRINGS = (
    "dd if=",
    "mkfs",
    ":(){:|:&};:",
    "> /dev/sda",
    "chmod -R 777 /",
    "--no-preserve-root",
    "DROP DATABASE",
    "DROP TABLE",
)

SHELL_OPERATORS = {";", "&&", "||", "|", "&"}
SHELL_EXECUTABLES = {"bash", "dash", "ksh", "sh", "zsh"}
SUDO_OPTIONS_WITH_VALUE = {
    "-C",
    "-D",
    "-R",
    "-T",
    "-g",
    "-h",
    "-p",
    "-u",
    "--chdir",
    "--chroot",
    "--command-timeout",
    "--group",
    "--host",
    "--prompt",
    "--role",
    "--type",
    "--user",
}
ENV_OPTIONS_WITH_VALUE = {"-C", "-S", "-u", "--chdir", "--split-string", "--unset"}
ASSIGNMENT_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*=")


def shell_tokens(command: str) -> list[str]:
    try:
        lexer = shlex.shlex(command, posix=True, punctuation_chars=";&|")
        lexer.whitespace_split = True
        lexer.commenters = ""
        return list(lexer)
    except ValueError:
        return []


def is_recursive_option(token: str) -> bool:
    if token == "--recursive":
        return True
    return token.startswith("-") and not token.startswith("--") and any(flag in token[1:] for flag in ("r", "R"))


def normalize_target(token: str) -> str:
    home = os.path.expanduser("~")
    for prefix in ("${HOME}", "$HOME"):
        if token == prefix or token.startswith(prefix + "/"):
            token = home + token[len(prefix) :]
            break
    if token == "~" or token.startswith("~/"):
        token = os.path.expanduser(token)
    normalized = posixpath.normpath(token)
    if normalized.startswith("//"):
        normalized = "/" + normalized.lstrip("/")
    return normalized


def command_segments(tokens: list[str]) -> list[list[str]]:
    segments: list[list[str]] = []
    current: list[str] = []
    for token in tokens:
        if token in SHELL_OPERATORS:
            if current:
                segments.append(current)
                current = []
            continue
        current.append(token)
    if current:
        segments.append(current)
    return segments


def skip_options(tokens: list[str], index: int, options_with_value: set[str]) -> int:
    while index < len(tokens):
        token = tokens[index]
        if token == "--":
            return index + 1
        option_name = token.split("=", 1)[0]
        if option_name in options_with_value and "=" not in token:
            index += 2
            continue
        if token.startswith("-"):
            index += 1
            continue
        break
    return index


def executable_index(tokens: list[str]) -> int | None:
    index = 0
    while index < len(tokens):
        while index < len(tokens) and ASSIGNMENT_RE.match(tokens[index]):
            index += 1
        if index >= len(tokens):
            return None

        executable = posixpath.basename(tokens[index])
        if executable == "sudo":
            index = skip_options(tokens, index + 1, SUDO_OPTIONS_WITH_VALUE)
            continue
        if executable == "env":
            index = skip_options(tokens, index + 1, ENV_OPTIONS_WITH_VALUE)
            while index < len(tokens) and ASSIGNMENT_RE.match(tokens[index]):
                index += 1
            continue
        if executable in {"command", "nohup"}:
            index = skip_options(tokens, index + 1, set())
            continue
        return index
    return None


def shell_command_argument(arguments: list[str]) -> str | None:
    for index, argument in enumerate(arguments):
        if argument == "--":
            continue
        if argument == "--command" or (argument.startswith("-") and not argument.startswith("--") and "c" in argument[1:]):
            if index + 1 < len(arguments):
                return arguments[index + 1]
            return None
    return None


def destructive_rm_arguments(arguments: list[str]) -> bool:
    recursive = False
    targets: list[str] = []
    options_done = False
    for argument in arguments:
        if argument == "--":
            options_done = True
            continue
        if not options_done and argument.startswith("-"):
            recursive = recursive or is_recursive_option(argument)
            continue
        targets.append(normalize_target(argument))

    protected_targets = {"/", posixpath.normpath(os.path.expanduser("~"))}
    if not recursive:
        return False
    return any(
        target in protected_targets
        or (has_magic(target) and posixpath.dirname(target) in protected_targets)
        for target in targets
    )


def contains_destructive_rm(command: str, *, depth: int = 0) -> bool:
    if depth > 4:
        return False

    for segment in command_segments(shell_tokens(command)):
        index = executable_index(segment)
        if index is None:
            continue

        executable = posixpath.basename(segment[index])
        arguments = segment[index + 1 :]
        if executable == "rm" and destructive_rm_arguments(arguments):
            return True

        if executable in SHELL_EXECUTABLES:
            nested_command = shell_command_argument(arguments)
            if nested_command is not None and contains_destructive_rm(nested_command, depth=depth + 1):
                return True
    return False


def main() -> int:
    event = read_event()
    if event.get("tool_name") != "Bash":
        return 0

    command = command_from(event)
    if contains_destructive_rm(command):
        return block("BLOCKED: Recursive deletion of a root or home directory")

    for pattern in BLOCKED_SUBSTRINGS:
        if pattern in command:
            return block(f"BLOCKED: Destructive command detected: {pattern!r}")

    if re.search(r"git\s+push\b", command) and re.search(r"(?:\s-f\b|--force(?:-with-lease)?\b)", command) and re.search(r"\b(?:main|master)\b", command):
        return block("BLOCKED: Force push to main/master")

    if re.search(r"(?:^|[;&|]\s*)(?:npm|pnpm|yarn)\s+publish\b", command):
        return block("BLOCKED: Package publication requires manual confirmation")

    if re.search(r"(?:^|\s)(?:rm\s+-r\b|rmdir\b)", command):
        emit({"systemMessage": "Warning: File deletion detected. Verify that it is intentional."})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
