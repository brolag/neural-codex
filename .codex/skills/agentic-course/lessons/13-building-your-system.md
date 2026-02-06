# Lesson 13: Building Your System

## Objective

Create your personalized agentic coding workflow.

## Congratulations!

You've learned all the pieces. Now let's put them together.

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│   ✅ The 70% Problem - Realistic expectations                  │
│   ✅ CRAFT Framework - Structured prompts                      │
│   ✅ 6 Core Areas - Complete specifications                    │
│   ✅ 3-Tier Boundaries - Safety guardrails                     │
│   ✅ Loop Fundamentals - Autonomous iteration                  │
│   ✅ Circuit Breakers - Safety mechanisms                      │
│   ✅ State Management - Progress persistence                   │
│   ✅ Multi-Agent - Parallel execution                          │
│   ✅ Context Engineering - Optimal resource usage              │
│   ✅ Compute Advantage - Leverage measurement                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Your Personal Workflow

Design a workflow that fits YOUR style:

### 1. Choose Your Mode

```
EXPLORER                        PLANNER
─────────────────────────────────────────────────────────
Vibe coding                     Spec-Driven Development
Quick iterations                Upfront planning
Good for: prototypes            Good for: production
```

### 2. Set Your Boundaries

Create `plans/rules/my-boundaries.md`:

```markdown
## My Boundaries

### ✅ Always
- [Your safe actions]

### ⚠️ Ask First
- [Your risky actions]

### 🚫 Never
- [Your forbidden actions]
```

### 3. Create Your Templates

Save CRAFT templates for common tasks:

```
.codex/templates/
├── feature.yaml     # New feature template
├── bugfix.yaml      # Bug fix template
├── refactor.yaml    # Refactoring template
└── test.yaml        # Test writing template
```

### 4. Set Default Limits

In your CLAUDE.md:

```yaml
defaults:
  loop_max: 10
  timeout: 30m
  regression_abort: true
```

## Daily Workflow Example

```
MORNING
├── /daily              # Check priorities
├── /todo-check         # Review active tasks
└── /recall yesterday   # Remember context

WORKING
├── /craft "task"       # Generate spec for complex work
├── /loop "task" --max 10  # Execute autonomously
├── /todo-check         # Monitor progress
└── /remember "key decision"  # Save insights

END OF DAY
├── git commit          # Checkpoint work
├── /todo-check         # Status update
└── Handover file       # Context for tomorrow
```

## Scaling Up

As you get comfortable:

```
LEVEL 1: Single Loops
/loop "Fix tests" --max 5

LEVEL 2: CRAFT Loops
/craft "Feature" → Review → /loop --craft

LEVEL 3: Parallel Agents
/squad:init → /squad:task "Backend" → /squad:task "Frontend"

LEVEL 4: Overnight Work
/loop "Refactor entire module" --max 30 --timeout 4h
# Go to sleep, check results in morning
```

## Common Patterns

### Pattern 1: Test-Driven Loop

```bash
/loop "Implement UserService with full test coverage" --type tdd --max 15
```

### Pattern 2: Lint Then Ship

```bash
/loop "Fix all linting errors" --type lint --max 10
git add . && git commit -m "chore: fix linting"
```

### Pattern 3: Parallel Research

```bash
/pv-mesh "Best architecture for real-time features?"
# Get multiple perspectives, then decide
```

### Pattern 4: Plan-Execute

```bash
/plan-execute "Implement OAuth2 authentication"
# Opus plans, Gemini executes (cheaper)
```

## Your Capstone Project

Design and implement your first fully autonomous task:

```bash
# 1. Create a CRAFT spec
/craft "Add a /status command that shows system health"

# 2. Review and adjust the spec

# 3. Execute with loop
/loop --craft --max 10

# 4. Check result
/todo-check

# 5. Calculate your CA
/ca
```

## What's Next?

You're now an agentic coding practitioner. Keep improving:

```
1. PRACTICE
   Run loops daily. Build muscle memory.

2. MEASURE
   Track CA over time. Look for patterns.

3. REFINE
   Improve your templates. Sharpen boundaries.

4. SHARE
   Teach others. Best way to solidify knowledge.
```

## Quick Reference

| Task | Command |
|------|---------|
| Start course | `/course` |
| Check progress | `/course progress` |
| Quick reference | `/course ref <topic>` |
| Get help | `/mentor` |
| Track KPIs | `/kpi` |
| Calculate CA | `/ca` |
| Run loop | `/loop "task" --max N` |
| Create CRAFT | `/craft "task"` |

## Course Complete!

```
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║   🎉 CONGRATULATIONS!                                            ║
║                                                                   ║
║   You've completed the Agentic Coding Mastery Course             ║
║                                                                   ║
║   You now know:                                                   ║
║   • How to set realistic expectations                             ║
║   • How to structure prompts for autonomy                         ║
║   • How to keep AI safe with boundaries                           ║
║   • How to run autonomous loops                                   ║
║   • How to manage state and context                               ║
║   • How to measure your leverage                                  ║
║                                                                   ║
║   Go build something amazing!                                     ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
```

---

*Neural Claude Code - Self-improving AI development*
*Course complete. Time to create.*
