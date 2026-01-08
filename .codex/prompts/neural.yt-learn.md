---
description: Learn from a YouTube video transcript
argument-hint: URL="<youtube url>"
---

Goal: pull transcript and summarize key takeaways.

Steps:
1) Fetch transcript (use `scripts/youtube-transcript.py` or `scripts/neural-codex/youtube-transcript.py`; or use MCP search if available). If tooling absent, instruct how to install or ask for transcript.
2) Summarize: main ideas, steps, code snippets, risks/limitations.
3) Emit a short actionable checklist relevant to neural-codex work.
4) If fetch fails, return a clear failure note and next steps.
