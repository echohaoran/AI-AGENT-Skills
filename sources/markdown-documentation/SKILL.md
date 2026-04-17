---
name: markdown-documentation
description: Write, format, and organize Markdown documentation with automatic style enforcement, link validation, and multi-format export (HTML/PDF/Word).
date: 2026-04-17
source: aj-geddes/useful-ai-prompts@markdown-documentation
installs: 709
allowed-tools:
  - Bash
  - Read
  - Write
---

SKILL.md

# Markdown Documentation Skill

> **Source:** aj-geddes/useful-ai-prompts@markdown-documentation  
> **Installs:** 709+ | **API Required:** ❌ No | **License:** MIT

## When to Use

✅ **Use this skill when:**

- User wants to write or organize project documentation
- Need to convert Markdown to other formats
- Checking documentation completeness and style
- Validating internal links
- "Write documentation for this project"
- "Convert this README to standard format"

## Quick Start

```bash
# Check documentation style
mdoc check README.md

# Format and beautify
mdoc format README.md

# Validate all links
mdoc validate-links ./docs/

# Convert to HTML
mdoc export README.md --to html --output dist/

# Convert to PDF
mdoc export README.md --to pdf --output dist/
```

## Documentation Templates

### Standard README Structure

```markdown
# Project Name

Brief description (1-2 sentences).

## Installation

```bash
npm install project-name
```

## Usage

```javascript
import { feature } from 'project-name';
feature();
```

## API Reference

### `functionName(params)`

Description of what this function does.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)

## License

MIT
```

## Scripts Reference

### `scripts/check-links.sh`

```bash
#!/bin/bash
# Check all Markdown links
find . -name "*.md" -exec grep -h '\[.*\](.*)' {} \; | \
  sed 's/.*\[//;s/\].*//' | \
  while read -r link; do
    if [[ "$link" == http* ]]; then
      curl -s -o /dev/null -w "%{http_code}" "$link" | \
        grep -q "200" || echo "❌ Broken: $link"
    fi
  done
```

## See Also

- [Marp Skill](../marp/) — Create presentations from Markdown
- [PDF Generator](../pdf-generator/) — Export to PDF
