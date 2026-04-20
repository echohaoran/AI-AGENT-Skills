---
name: code-review-quality
description: Automated code quality review — enforce style guides, catch bugs, identify security vulnerabilities, and ensure best practices. No API required — local static analysis.
date: 2026-04-17
source: proffesor-for-testing/agentic-qe@code-review-quality
installs: 1024
allowed-tools:
  - Bash
  - Read
---

SKILL.md

# Code Review Quality Skill

> **Source:** proffesor-for-testing/agentic-qe@code-review-quality  
> **Installs:** 1,024+ | **API Required:** ❌ No | **License:** MIT

## When to Use

✅ **Use this skill when:**

- User wants automated code review before merging
- Checking code for security vulnerabilities
- Enforcing team coding standards
- Finding bugs, performance issues, code smells
- "Review this PR"
- "Check this code for issues"

## Quick Start

```bash
# Review a file
code-review review path/to/file.py

# Review entire directory
code-review review ./src/

# Review with security focus
code-review review ./src/ --focus security

# Output as JSON for CI/CD
code-review review ./src/ --format json --output report.json
```

## Quality Gates

| Check | Severity | Auto-fix |
|-------|----------|----------|
| **Security** | Critical | ❌ |
| **Code Smell** | Warning | ✅ |
| **Style** | Info | ✅ |
| **Performance** | Warning | ❌ |
| **Test Coverage** | Warning | ❌ |

## Security Checks

```bash
# SQL Injection detection
code-review check security --rules sqli ./src/

# XSS vulnerability scan
code-review check security --rules xss ./src/

# Hardcoded credentials
code-review check security --rules secrets ./src/

# Dependency vulnerabilities
code-review check security --rules dependencies ./package.json
```

## Style Checks

```bash
# Python style (PEP8)
code-review check style --lang python ./src/

# JavaScript style (ESLint)
code-review check style --lang javascript ./src/

# Auto-fix style issues
code-review fix --lang python ./src/
```

## Scripts Reference

### `scripts/review.sh`

```bash
#!/bin/bash
# Usage: review.sh <path> [options]

PATH="${1:-.}"
FORMAT="${2:-text}"

echo "🔍 Running code review on: $PATH"
echo "================================"

# Security scan
echo "🔒 Security Check..."
code-review check security "$PATH"

# Style check
echo ""
echo "🎨 Style Check..."
code-review check style "$PATH"

# Complexity check
echo ""
echo "📊 Complexity Check..."
code-review check complexity "$PATH"

# Generate summary
echo ""
echo "📋 Summary"
code-review summary "$PATH" --format "$FORMAT"
```

## Integration

- Works with **Git hooks** for pre-commit checks
- Output can be **CI/CD** integration (GitHub Actions, GitLab CI)
- Configurable **quality gates** for pass/fail decisions

## See Also

- [Alma Skill Vetter](../Skill_Vetter/) — Skill security vetting
- [Docker](../docker/) — Run in containers for isolation
- [Git Workflow](../git-workflow/) — Version control integration
