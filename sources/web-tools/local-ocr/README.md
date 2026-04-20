# Local OCR Skill for Tesseract

A ready-to-use local OCR (Optical Character Recognition) skill based on Tesseract, enabling offline image-to-text conversion without external API calls.

**Features:**
- ✅ Fully offline operation (no network required)
- ✅ Privacy-friendly (all processing happens locally)
- ✅ Supports Simplified/Traditional Chinese, English, Japanese, Korean, and 80+ languages
- ✅ Batch processing support
- ✅ Python and Bash automation scripts included

## Quick Start

### Check Your Environment

```bash
# Verify Tesseract installation
tesseract --version

# List available language packs
tesseract --list-langs | grep -E "chi|eng|jpn|kor"
```

If not installed:
```bash
# macOS (Homebrew)
brew install tesseract
brew install tesseract-ocr/tessdata_chi_sim
brew install tesseract-ocr/tessdata_eng

# Ubuntu/Debian
sudo apt-get install tesseract-ocr tesseract-ocr-chi-sim tesseract-ocr-eng
```

### Test the Skill

```bash
# Method 1: Use the test script (auto-creates sample image)
cd sources/local-ocr
python3 ocr_test.py

# Method 2: Use quick bash script
./quick_ocr.sh your_image.png chi_sim

# Method 3: Direct Tesseract command
tesseract invoice.jpg output_txt -l chi_sim --psm 6
```

## Supported Languages

| Language | Code | Note |
|----------|------|------|
| Simplified Chinese | `chi_sim` | Default for Chinese |
| Traditional Chinese | `chi_tra` | For traditional characters |
| English | `eng` | Most accurate language |
| Japanese | `jpn` | Includes Kanji |
| Korean | `kor` | Hangul support |

For full list: https://github.com/tesseract-ocr/tessdata

## PSM Modes

Page Segmentation Mode controls how Tesseract analyzes the image layout:

| Mode | Description | Best For |
|------|-------------|----------|
| 3 | Fully automatic page segmentation | Documents with complex layouts |
| 6 | Assume single uniform block of text | Screenshots, text boxes ⭐ |
| 7 | Treat as a single text line | Titles, headers |
| 11 | Sparse text, don't sort | Vertical text |
| 13 | Sparse text, single character | CAPTCHA codes |

## Performance Tips

1. **Image Quality**: Ensure resolution ≥ 300 DPI
2. **Preprocessing**: Convert to grayscale, apply thresholding
3. **PSM Selection**: Try different modes for best results
4. **Character Whitelist**: Restrict output to expected characters

```bash
# Example: Extract only numbers and letters
tesseract img.png out -l eng -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789
```

## Comparison with Alternatives

| Feature | Tesseract | PaddleOCR | Cloud APIs |
|---------|-----------|-----------|------------|
| Offline | ✅ Yes | ✅ Yes | ❌ No |
| Free | ✅ Yes | ✅ Yes | 💰 Paid |
| Privacy | ✅ Local | ✅ Local | ❌ External |
| Chinese Accuracy | Medium | Excellent ⭐ | Excellent ⭐ |
| Setup Complexity | Low | Medium | Lowest |

**Recommendation:**
- Use **Tesseract** for general tasks and privacy-sensitive work
- Use **PaddleOCR** when highest Chinese accuracy is needed
- Use **Cloud APIs** only for maximum convenience with public data

## License

MIT License - see SKILL_en.md for details
