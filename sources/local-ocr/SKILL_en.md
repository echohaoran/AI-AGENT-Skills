---
title: Local OCR Image-to-Text
excerpt: Tesseract-based local image text recognition without network API, supporting Simplified/Traditional Chinese and English. Privacy-friendly and works offline.
date: 2026-04-17
---

SKILL.md
# Local OCR Image-to-Text Skill

## When to Use

✅ **Use this skill when:**

- User requests "screenshot to text", "extract text from image"
- Need to recognize text from photos of paper documents
- Privacy-sensitive files (contracts, ID cards, invoices)
- Offline text recognition requirements
- Batch processing images for text extraction

❌ **Do NOT use when:**

- Complex handwriting (use professional scanning apps)
- Severely tilted/blurred/low-quality images (preprocess first)
- Professional scenarios requiring extremely high accuracy (manual verification needed)

## Quick Start

### Prerequisites Check

```bash
# Confirm Tesseract is installed (macOS Homebrew)
which tesseract
tesseract --version

# Confirm language packs (should include chi_sim, chi_tra, eng)
tesseract --list-langs | grep -E "chi|eng"
```

### Basic Usage

```bash
# Single image recognition (output to stdout)
tesseract image.png stdout --psm 6 -l chi_sim+eng

# Recognize and save result file
tesseract invoice.jpg invoice_txt --psm 3 -l chi_sim

# Specify output format (HOCR with coordinate information)
tesseract image.png output.hocr --psm 6 -l chi_sim -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789
```

### Python Automation Script

```python
import subprocess
import sys

def ocr_image(image_path, lang='chi_sim', psm=6):
    """
    Use Tesseract to recognize text from image
    
    Args:
        image_path: Image file path
        lang: Language code (chi_sim/chi_tra/eng/jpn...)
        psm: Page segmentation mode (6=single text block, 3=full page analysis)
    
    Returns:
        str: Recognized text content
    """
    try:
        result = subprocess.run(
            ['tesseract', image_path, 'stdout', f'-l{lang}', f'--psm{psm}'],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return f"Error: {result.stderr}"
    except subprocess.TimeoutExpired:
        return "Timeout: Recognition exceeded 30 seconds"
    except FileNotFoundError:
        return "tesseract command not found, please install first"

# Usage example
if __name__ == '__main__':
    image = sys.argv[1] if len(sys.argv) > 1 else 'test.png'
    text = ocr_image(image)
    print("=" * 50)
    print(text)
    print("=" * 50)
```

## PSM Mode Selection Guide

| PSM | Description | Best For |
|-----|-------------|----------|
| 0 | Fully automatic, no OSD | General purpose |
| 3 | Fully automatic page segmentation (default) | Complex layout documents |
| 4 | Assume single uniform block of text | Text boxes in screenshots ⭐ |
| 6 | Assume a single uniform block of text | Most common scenario |
| 7 | Treat the image as a single text line | Title lines |
| 11 | Sparse text, don't sort | Vertical layout |
| 13 | Sparse text, single character | CAPTCHA recognition |

## Language Pack Management

### View Installed Languages

```bash
tesseract --list-langs
```

### Install New Language Packs (macOS)

```bash
# View available language list
ls /opt/homebrew/share/tessdata/*.traineddata

# Install Japanese (if not exists)
brew install tesseract-lang/tesseract
```

### Common Language Codes

| Language | Code | Notes |
|----------|------|-------|
| Simplified Chinese | `chi_sim` | |
| Traditional Chinese | `chi_tra` | Vertical: `chi_tra_vert` |
| English | `eng` | |
| Japanese | `jpn` | |
| Korean | `kor` | |
| French | `fra` | |
| German | `deu` | |

## Performance Optimization Tips

### 1. Image Preprocessing for Better Accuracy

```python
from PIL import Image, ImageEnhance, ImageFilter

def preprocess_image(input_path, output_path):
    """Enhance image to improve OCR accuracy"""
    img = Image.open(input_path)
    
    # Convert to grayscale
    img = img.convert('L')
    
    # Sharpen
    img = ImageEnhance.Sharpness(img).enhance(1.5)
    
    # Binarization (threshold 128)
    threshold = 128
    img = img.point(lambda x: 255 if x > threshold else 0)
    
    img.save(output_path)
    return output_path
```

### 2. Batch Processing

```bash
#!/bin/bash
# batch_ocr.sh - Batch OCR processing

INPUT_DIR="${1:=./images}"
OUTPUT_DIR="${2:=./output}"
LANG="${3:=chi_sim}"

mkdir -p "$OUTPUT_DIR"

for img in "$INPUT_DIR"/*.{jpg,png,pdf,JPEG,PNG}; do
    [ -f "$img" ] || continue
    basename=$(basename "$img")
    echo "Processing: $basename"
    tesseract "$img" "$OUTPUT_DIR/$basename" --psm 6 -l "$LANG"
done

echo "✅ Batch processing complete"
```

## Common Issues

### Q1: Low recognition rate?

1. **Improve image quality**: Ensure resolution ≥ 300 DPI
2. **Adjust PSM mode**: Try different values
3. **Add character whitelist**: Restrict output character set
   ```bash
   tesseract img.png out --psm 6 -l eng -c tessedit_char_whitelist=0123456789ABCDEF
   ```
4. **Preprocess image**: Denoise, binarize, sharpen

### Q2: How to handle mixed Chinese and English?

```bash
# Load multiple languages simultaneously
tesseract image.png stdout -l chi_sim+eng --psm 6
```

### Q3: Table recognition?

```bash
# Enable table detection
tesseract table.png stdout --psm 6 -l eng --oem 1 --psm 6 --userpatterns ./table.traineddata
```

## Comparison with PaddleOCR

| Feature | Tesseract | PaddleOCR |
|---------|-----------|-----------|
| Chinese Accuracy | Medium | **Excellent** ⭐ |
| Installation Complexity | Low (system command) | High (Python environment) |
| Model Size | ~20MB/language | ~200MB |
| Speed | Fast | Faster |
| Offline Support | ✅ | ✅ |
| Handwriting Recognition | ❌ | ⭕ Limited support |

**Recommendation:**
- Use Tesseract for simple tasks (already in your system)
- For higher Chinese accuracy → PaddleOCR

---

## References

- [Tesseract Official Documentation](https://tesseract-ocr.github.io/)
- [PaddleOCR GitHub](https://github.com/PaddlePaddle/PaddleOCR)
- [Supported Languages](https://github.com/tesseract-ocr/tessdata)
