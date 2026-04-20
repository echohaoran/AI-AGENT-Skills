#!/usr/bin/env python3
"""
OCR Test Script for Local Tesseract Installation

Usage:
    python ocr_test.py [image_path]
    
If no image path provided, creates a test image and recognizes it.
"""

import subprocess
import sys
from PIL import Image, ImageDraw, ImageFont

def check_tesseract():
    """Check if Tesseract is installed and get version info"""
    try:
        result = subprocess.run(
            ['tesseract', '--version'],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            print(f"✅ {lines[0]}")
            return True
    except FileNotFoundError:
        print("❌ Tesseract not found. Install with: brew install tesseract")
    except Exception as e:
        print(f"❌ Error checking Tesseract: {e}")
    return False

def list_languages():
    """List available language packs"""
    try:
        result = subprocess.run(
            ['tesseract', '--list-langs'],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            langs = [l.strip() for l in result.stdout.strip().split('\n')[1:]]
            relevant = [l for l in langs if any(x in l.lower() for x in ['chi', 'eng', 'jpn', 'kor'])]
            print(f"\n📚 Available languages (relevant):")
            for lang in sorted(relevant):
                print(f"   • {lang}")
            return langs
    except Exception as e:
        print(f"❌ Error listing languages: {e}")
    return []

def create_test_image(path='ocr_test_sample.png'):
    """Create a test image with Chinese and English text"""
    width, height = 600, 200
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)
    
    # Draw text (using default font since we may not have CJK fonts)
    texts = [
        ("Hello World", (50, 30)),
        ("Test OCR Recognition", (50, 70)),
        ("Testing 123 ABC xyz", (50, 110)),
        ("Numbers: 1+2=3, 3.14, %50%", (50, 150)),
    ]
    
    for text, position in texts:
        draw.text(position, text, fill='black')
    
    img.save(path)
    print(f"\n📸 Created test image: {path}")
    return path

def recognize_image(image_path, lang='eng', psm=6):
    """
    Recognize text from image using Tesseract
    
    Args:
        image_path: Path to image file
        lang: Language code
        psm: Page segmentation mode
    
    Returns:
        str: Recognized text
    """
    try:
        result = subprocess.run(
            ['tesseract', image_path, 'stdout', '-l', lang, '--psm', str(psm)],
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.stdout if result.returncode == 0 else f"Error: {result.stderr}"
    except subprocess.TimeoutExpired:
        return "Timeout: Recognition exceeded 30 seconds"
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    print("=" * 60)
    print("Local OCR Test Suite")
    print("=" * 60)
    
    # Check installation
    if not check_tesseract():
        sys.exit(1)
    
    # List languages
    langs = list_languages()
    if not ('eng' in langs or 'chi_sim' in langs):
        print("\n⚠️  Warning: English or Simplified Chinese language pack missing!")
        print("Install with: brew install tesseract-ocr/tessdata_eng")
    
    # Process image
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        print(f"\n🖼️  Processing: {image_path}")
        
        # Auto-detect language based on filename or use default
        lang = 'chi_sim' if 'chi' in image_path.lower() else 'eng'
        print(f"🔤 Using language: {lang}")
    else:
        print("\n🎨 Creating test image...")
        image_path = create_test_image()
        lang = 'eng'
        print(f"🔤 Using language: {lang}")
    
    # Perform OCR
    print("\n🔍 Performing OCR recognition...")
    recognized_text = recognize_image(image_path, lang)
    
    # Display results
    print("\n" + "=" * 60)
    print("Recognition Result:")
    print("=" * 60)
    print(recognized_text)
    print("=" * 60)

if __name__ == '__main__':
    try:
        # Check Pillow dependency
        import PIL
    except ImportError:
        print("Installing Pillow...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'pillow'])
        import PIL
    
    main()
