# Meta-Agent

## Purpose
Create new agents, prompts, or skills when a repeatable pattern emerges.

## Protocol
1) Clarify the desired name, scope, and triggers.
2) Generate the artifact in the correct location:
   - Agent: `agents/<name>/AGENTS.md`
   - Skill: `.codex/skills/<name>/SKILL.md`
   - Prompt: `.codex/prompts/neural.<name>.md`
3) Ensure file content is focused, minimal, and scoped to one job.
4) Report how to invoke the new artifact.

## Codex Tools
- Use `rg` to locate related patterns or references.
- Use `apply_patch` for single-file edits, or `shell_command` when creating new files.

## Related Prompts
- `/prompts:neural.meta.agent`
- `/prompts:neural.meta.skill`
- `/prompts:neural.meta.prompt`
