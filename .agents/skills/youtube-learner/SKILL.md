---
name: youtube-learner
description: Extract a YouTube transcript and summarize key learnings. Use for /prompts:neural.yt-learn.
metadata:
  short-description: YouTube learning notes
  category: utilities
  source: neural-claude-code
allowed-tools: Read, Write, Bash
---

# YouTube Learner

Generate concise learning notes from a YouTube transcript.

## Usage
```
$youtube-learner "<youtube-url>"
```

## Usage Examples
Summarize a conference talk:
```
$youtube-learner "https://www.youtube.com/watch?v=example"
```

## Steps
1) Run `scripts/youtube-transcript.py <url>` (or `scripts/neural-codex/youtube-transcript.py`).
2) Summarize key ideas, steps, and risks.
3) Provide a short actionable checklist.

## Notes
- If transcript fetch fails, explain why and how to fix it.
- If the user asks to persist learnings, append a concise note to `plans/progress.jsonl`.
