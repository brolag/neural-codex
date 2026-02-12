---
name: kpi
description: Track agentic KPIs (plan velocity, review velocity, autonomy duration, loop state).
metadata:
  short-description: Agentic KPI tracker
  category: productivity
  source: neural-claude-code-plugin
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# KPI Tracking

Track four core metrics of agentic coding performance.

## KPIs
- Plan Velocity (minutes to produce a spec)
- Review Velocity (minutes per review cycle)
- Autonomy Duration (minutes without human input)
- Loop State (in-loop, out-loop, zte)

## Data Location
Store daily logs in `plans/metrics/kpi-YYYY-MM-DD.json`.
Targets in `plans/metrics/kpi-targets.json`.

## Usage
```
$kpi dashboard
$kpi plan <minutes> "<task>"
$kpi review <minutes> "<task>"
$kpi autonomy <minutes> "<task>"
$kpi state <in-loop|out-loop|zte> "<task>"
$kpi report
$kpi target <metric> <value>
```

## Notes
- If files are missing, create them.
- Summaries should include totals, averages, and trends.
