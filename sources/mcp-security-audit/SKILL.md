---
name: mcp-security-audit
description: Audit Model Context Protocol (MCP) plugins for security vulnerabilities, permission analysis, and compliance. No API required — pure static analysis.
date: 2026-04-17
source: github/awesome-copilot@mcp-security-audit
installs: 495
allowed-tools:
  - Bash
  - Read
---

SKILL.md

# MCP Security Audit Skill

> **Source:** github/awesome-copilot@mcp-security-audit  
> **Installs:** 495+ | **API Required:** ❌ No | **License:** MIT

## When to Use

✅ **Use this skill when:**

- Auditing installed MCP plugins before use
- Checking plugin permission requests
- Identifying known vulnerability patterns
- Generating security compliance reports
- "Audit my MCP plugins"
- "Is this plugin safe to install?"

## Quick Start

```bash
# Audit all installed MCP plugins
mcp-audit scan --all

# Audit specific plugin
mcp-audit scan --plugin my-plugin

# Generate report
mcp-audit report --format json --output security-report.json

# Check for known CVEs
mcp-audit check-cves --plugin my-plugin
```

## Audit Categories

| Category | Checks |
|----------|--------|
| **Permissions** | Overreaching permissions requested |
| **Network** | Unnecessary network access |
| **Storage** | Excessive file system access |
| **Secrets** | Hardcoded credentials |
| **Dependencies** | Known vulnerabilities in dependencies |

## Report Output

```json
{
  "plugin": "my-plugin",
  "overall_risk": "LOW",
  "findings": [
    {
      "severity": "INFO",
      "rule": "permission-minimal",
      "message": "Plugin requests 3 permissions"
    },
    {
      "severity": "WARN",
      "rule": "network-excessive",
      "message": "Full network access requested"
    }
  ]
}
```

## See Also

- [Firebase Security Auditor](../firestore-security-audit/) — Database security rules
- [Code Review Quality](../code-review-quality/) — General security checks
- [Privacy Skill](../awesome-privacy-skill/) — Data privacy protection
