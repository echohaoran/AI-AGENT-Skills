#!/bin/bash
# Quick OCR Script for Local Tesseract
# Usage: ./quick_ocr.sh <image_path> [-l language] [--psm mode]

set -e

IMAGE_PATH="${1:-}"
LANGUAGE="${2:-chi_sim+eng}"
PSM="${3:-6}"

usage() {
    echo "Usage: $0 <image_path> [language] [psm_mode]"
    echo ""
    echo "Arguments:"
    echo "  image_path   Path to image file (required)"
    echo "  language     Language code (default: chi_sim+eng)"
    echo "               Options: chi_sim, chi_tra, eng, jpn, kor"
    echo "  psm_mode     Page segmentation mode (default: 6)"
    echo "               6=single text block, 3=full page analysis"
    echo ""
    echo "Examples:"
    echo "  $0 screenshot.png"
    echo "  $0 document.jpg eng"
    echo "  $0 invoice.png chi_sim 3"
}

check_tesseract() {
    if ! command -v tesseract &> /dev/null; then
        echo "❌ Error: Tesseract not found"
        echo ""
        echo "Install Tesseract on macOS:"
        echo "  brew install tesseract"
        echo "  brew install tesseract-ocr/tessdata_*  # Language packs"
        exit 1
    fi
}

if [ "$IMAGE_PATH" = "-h" ] || [ "$IMAGE_PATH" = "--help" ] || [ -z "$IMAGE_PATH" ]; then
    usage
    exit 0
fi

if [ ! -f "$IMAGE_PATH" ]; then
    echo "❌ Error: Image file not found: $IMAGE_PATH"
    exit 1
fi

echo "🔍 Recognizing text from: $IMAGE_PATH"
echo "📚 Language: $LANGUAGE"
echo "🎯 PSM Mode: $PSM"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

tesseract "$IMAGE_PATH" stdout -l "$LANGUAGE" --psm "$PSM"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Recognition complete"
