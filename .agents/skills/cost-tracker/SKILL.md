---
name: cost-tracker
description: Track AI usage costs for tasks and reports.
metadata:
  short-description: Cost tracker
  category: productivity
  source: neural-claude-code-plugin
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Cost Tracker

Track cost per task/session to feed KPI and compute-advantage reporting.

## Data Location
`plans/metrics/costs.json`

## Usage
```
$cost-tracker dashboard
$cost-tracker log <usd> "<task>" [--model <name>] [--tokens-in <n>] [--tokens-out <n>]
$cost-tracker report
$cost-tracker budget <usd> --weekly|--monthly
$cost-tracker export --format csv
```

## Notes
- Avoid hardcoding model pricing; use current provider dashboards.
- If tokens are unknown, log cost only and note the model.
