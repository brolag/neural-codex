---
name: skill-installer
description: Install external skills from URLs, repos, or known registries. Use when adding community or third-party skills.
metadata:
  short-description: Install external Codex skills
  category: meta
  source: neural-codex
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Skill Installer

Install skills from external sources into your project or global skill directory.

## When to Use
- Adding a community skill from a git repository
- Installing skills from a URL
- Cloning skill templates for customization

## Usage
```
$skill-installer <source> [--global] [--name <custom-name>]
```

## Usage Examples
Install from a GitHub repo:
```
$skill-installer "github.com/user/codex-skills/my-skill"
```

Install a known skill:
```
$skill-installer linear
```

Install globally:
```
$skill-installer "https://example.com/skill.zip" --global
```

## Supported Sources
- **GitHub URLs**: `github.com/user/repo/path/to/skill`
- **Direct URLs**: `.zip` or `.tar.gz` archives
- **Known skills**: Short names from the neural-codex registry

## Known Skills Registry
The following skills can be installed by name:
- `linear` - Linear issue integration
- `notion-spec` - Notion specification reader
- `github-pr` - GitHub PR workflows

## Steps
1) Parse the source URL or skill name
2) Determine target directory (local or global)
3) Download/clone the skill content
4) Validate SKILL.md exists and is well-formed
5) Copy to target directory
6) Print installation confirmation

## Validation
After install, verify with:
```
ls .codex/skills/<skill-name>/
cat .codex/skills/<skill-name>/SKILL.md
```

## Safety
- Review SKILL.md before using unknown skills
- Check allowed-tools for risky permissions
- Prefer skills from trusted sources
- Installed scripts run with your permissions
