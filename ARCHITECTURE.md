# Architecture

## Overview
neural-codex is a Codex-native harness with file-based state, repo-local prompts and skills, lifecycle hooks, GPT-5.6 profile overlays, and test-gated automation loops.

## Key Components
- `.codex/hooks.json` and `.codex/hooks/` lifecycle guardrails
- `.codex/profiles/` source templates for global Codex profiles
- `.codex/prompts/`, `.codex/templates/`, and `.codex/config.toml`
- `.agents/skills/` skills library
- `plans/` task state and progress logs
- `scripts/` automation utilities

## Deep Dives
- `docs/design-docs/README.md`
- `docs/AGENT-HARNESS.md`
- `docs/HOOKS.md`
- `docs/VERIFICATION.md`
