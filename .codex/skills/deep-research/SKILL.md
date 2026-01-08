---
name: deep-research
description: Conduct comprehensive multi-source research with systematic analysis. Use for thorough investigation of complex topics.
metadata:
  short-description: Multi-source deep research
  category: utilities
  source: neural-codex
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Deep Research

Conduct comprehensive research across multiple sources with systematic documentation.

## When to Use
- Investigating a new technology or library
- Understanding complex systems or APIs
- Comparing solutions before implementation
- Building knowledge for architectural decisions

## Usage
```
$deep-research "<topic>" [--sources <count>] [--output <file>]
```

## Usage Examples
Research a library:
```
$deep-research "Zod validation library best practices"
```

Compare frameworks:
```
$deep-research "Next.js vs Remix for API routes" --sources 5
```

Save findings:
```
$deep-research "OAuth 2.0 PKCE flow" --output plans/research/oauth.md
```

## Research Process

### 1. Scope Definition
- Clarify the research question
- Identify key areas to investigate
- Set success criteria

### 2. Source Gathering
- Official documentation
- GitHub issues and discussions
- Stack Overflow threads
- Blog posts and tutorials
- Academic papers (if relevant)

### 3. Analysis
- Extract key facts and patterns
- Identify trade-offs and risks
- Note conflicting information
- Highlight best practices

### 4. Synthesis
- Summarize findings
- Provide recommendations
- List actionable next steps
- Document sources

## Output Format
```markdown
# Research: <Topic>

## Summary
<Key findings in 2-3 sentences>

## Key Facts
- <Fact 1>
- <Fact 2>

## Trade-offs
| Option | Pros | Cons |
|--------|------|------|
| A | ... | ... |
| B | ... | ... |

## Recommendations
1. <Recommendation>
2. <Recommendation>

## Sources
- [Source 1](url)
- [Source 2](url)

## Next Steps
- [ ] <Action item>
```

## Integration with Memory
Save important findings:
```
$memory-system remember "Research: <topic> - <key insight>"
```

## Safety
- Verify information from multiple sources
- Note publication dates for time-sensitive topics
- Distinguish facts from opinions
- Cite sources for traceability
