---
name: markitdown
description: Convert various document formats (DOCX, XLSX, PPTX, PDF, images, EPUB, HTML) to clean Markdown using Microsoft's markitdown CLI tool.
date: 2026-04-21
source: microsoft/markitdown
installs: 4500+
license: MIT
allowed-tools:
  - Bash
  - Read
  - Write
---

# markitdown

> **Source:** microsoft/markitdown  
> **Type:** CLI Document Converter  
> **License:** MIT | **Platform:** macOS, Linux, Windows

## Overview

markitdown is a Microsoft-developed CLI tool that converts various document formats into clean, readable Markdown. It supports DOCX, XLSX, PPTX, PDF, images (with OCR), EPUB, HTML, and more.

**Key Features:**
- ✅ Batch conversion of multiple files
- ✅ Preserves formatting (tables, headings, lists)
- ✅ OCR for images and scanned PDFs
- ✅ Cross-platform (macOS, Linux, Windows)
- ✅ No API key required — runs locally

## Installation

### Option 1: npm (Recommended for macOS/Linux)

```bash
npm install -g @microsoft/markitdown
```

### Option 2: dotnet tool

```bash
dotnet tool install -g markitdown
```

### Option 3: Download Binary

```bash
# macOS
curl -fsSL https://github.com/microsoft/markitdown/releases/latest/download/markitdown-macos-x64.tar.gz | tar -xz
sudo mv markitdown /usr/local/bin/

# Linux
curl -fsSL https://github.com/microsoft/markitdown/releases/latest/download/markitdown-linux-x64.tar.gz | tar -xz
sudo mv markitdown /usr/local/bin/
```

### Verify Installation

```bash
markitdown --version
```

## Supported Formats

| Format | Extension | Notes |
|--------|-----------|-------|
| Word | .docx | ✅ Full support |
| Excel | .xlsx | ✅ Tables preserved |
| PowerPoint | .pptx | ✅ Notes included |
| PDF | .pdf | ✅ Text extraction |
| Images | .png, .jpg | 🅾️ OCR required |
| EPUB | .epub | ✅ Full support |
| HTML | .html | ✅ Full support |
| Markdown | .md | ✅ Pass-through |

## Quick Start

### Basic Usage

```bash
# Convert single file
markitdown document.docx -o output.md

# Convert to stdout
markitdown document.docx

# Convert multiple files
markitdown file1.docx file2.xlsx file3.pdf

# Convert entire directory
markitdown ./documents/

# Output to specific directory
markitdown ./documents/ -o ./markdown/
```

### Advanced Options

```bash
# Enable OCR for images
markitdown image.png --ocr -o output.md

# Skip unsupported files (don't error)
markitdown ./documents/ --skip

# Verbose output
markitdown document.docx -v

# Extract images to directory
markitdown document.docx --extract-images ./images/

# Preserve original filenames
markitdown ./documents/ --preserve-filenames -o ./output/
```

## Output Formats

### Markdown Output

```markdown
# Document Title

## Section 1

Content with **bold** and *italic* text.

### Table

| Column 1 | Column 2 |
|----------|----------|
| Cell 1   | Cell 2   |

## Section 2

- List item 1
- List item 2
```

### Image Handling

Images are downloaded and referenced locally:

```markdown
![Image](./images/image1.png)

![Chart](./images/chart1.png)
```

## Use Cases

### Use Case 1: Batch Convert Office Documents

```bash
# Convert all Office files to Markdown
for f in *.docx *.xlsx *.pptx; do
    markitdown "$f" -o "./md/$(basename "$f" .${f##*.}).md"
done
```

### Use Case 2: Process Scanned PDFs with OCR

```bash
# Enable OCR for scanned documents
markitdown scanned.pdf --ocr -o output.md
```

### Use Case 3: Extract Content from EPUB

```bash
# Convert ebook to Markdown for analysis
markitdown book.epub -o book.md
```

### Use Case 4: Web Page Archival

```bash
# Save web page as Markdown
markitdown https://example.com/article -o article.md
```

## Scripts Reference

### `scripts/batch-convert.sh`

```bash
#!/bin/bash
# Batch convert all supported files in directory

INPUT_DIR="${1:-.}"
OUTPUT_DIR="${2:-./markitdown-output}"

mkdir -p "$OUTPUT_DIR"

find "$INPUT_DIR" -type f \( \
    -name "*.docx" -o \
    -name "*.xlsx" -o \
    -name "*.pptx" -o \
    -name "*.pdf" -o \
    -name "*.epub" -o \
    -name "*.html" \
\) | while read -r file; do
    basename=$(basename "$file")
    extension="${basename##*.}"
    filename="${basename%.*}"
    output="$OUTPUT_DIR/$filename.md"
    
    echo "📄 Converting: $basename"
    markitdown "$file" -o "$output" 2>/dev/null
    
    if [ $? -eq 0 ]; then
        echo "  ✅ → $output"
    else
        echo "  ❌ Failed"
    fi
done

echo ""
echo "📊 Conversion complete!"
echo "Output directory: $OUTPUT_DIR"
```

### `scripts/ocr-pipeline.sh`

```bash
#!/bin/bash
# Process images and scanned PDFs with OCR

INPUT="$1"
OUTPUT="${2:-output.md}"

echo "🔍 Running OCR on: $INPUT"
markitdown "$INPUT" --ocr -o "$OUTPUT"

if [ $? -eq 0 ]; then
    echo "✅ OCR complete: $OUTPUT"
    echo "Word count: $(wc -w < "$OUTPUT")"
else
    echo "❌ OCR failed"
fi
```

## Configuration

### Global Config

```yaml
# ~/.markitdown.yaml
output_format: markdown
preserve_filenames: true
extract_images: true
images_dir: ./images
ocr_enabled: false
skip_unsupported: true
```

## Comparison with Other Tools

| Feature | markitdown | pandoc | docx2txt |
|---------|------------|--------|----------|
| DOCX | ✅ | ✅ | ✅ |
| XLSX | ✅ | ✅ | ❌ |
| PPTX | ✅ | ✅ | ❌ |
| PDF | ✅ | ✅ | ❌ |
| Images OCR | ✅ | ❌ | ❌ |
| EPUB | ✅ | ✅ | ❌ |
| No Dependencies | ✅ | ❌ | ✅ |
| Cross-platform | ✅ | ✅ | ✅ |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "command not found" | Install via `npm install -g @microsoft/markitdown` |
| "Failed to extract" | File may be corrupted or password-protected |
| OCR not working | Install Tesseract: `brew install tesseract` |
| Slow conversion | Use `--skip` to skip problematic files |

## Integration with Other Skills

- **pdf-generator** → Chain: markitdown → pdf-generator for format conversion
- **mermaid** → Extract content → Generate diagrams
- **markdown-documentation** → Convert documents → Generate docs
- **file-organizer** → Batch organize converted files

## See Also

- [GitHub Repository](https://github.com/microsoft/markitdown)
- [npm Package](https://www.npmjs.com/package/@microsoft/markitdown)
- [Microsoft Blog Post](https://devblogs.microsoft.com/)
