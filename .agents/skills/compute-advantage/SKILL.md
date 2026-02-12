---
name: compute-advantage
description: Calculate compute advantage (agentic leverage) and log sessions.
metadata:
  short-description: Compute advantage
  category: productivity
  source: neural-claude-code-plugin
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Compute Advantage

Compute Advantage (CA) measures agentic leverage.

Formula:
```
CA = (compute_scaling * autonomy_min) / (human_time_min + effort + cost_usd)
```

## Data Location
`plans/metrics/ca-sessions.json`

## Usage
```
$compute-advantage calc compute=<n> autonomy=<min> time=<min> effort=<1-5> cost=<usd>
$compute-advantage log "<task>" --compute=<n> --autonomy=<min> --time=<min> --effort=<1-5> --cost=<usd>
$compute-advantage history
$compute-advantage report
```

## Notes
- Use realistic effort (1=trivial, 5=complex).
- If cost is unknown, estimate or leave at 0 with a note.
