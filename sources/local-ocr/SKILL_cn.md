---
title: 本地 OCR 识图转文
excerpt: 基于 Tesseract 的本地化图像文字识别，无需网络 API，支持中英简繁四语，保护隐私同时离线可用。
date: 2026-04-17
---

SKILL.md
# 本地 OCR 识图转文技能

## 何时使用

✅ **使用此技能的场景：**

- 用户要求"截图转文字"、"图片提取文本"
- 需要识别纸质文件照片中的文字
- 对隐私敏感的文件（合同、身份证、发票等）
- 离线环境下的文字识别需求
- 批量处理图片中的文字提取

❌ **不要使用的场景：**

- 复杂手写体（建议使用专业扫描 App）
- 严重倾斜/模糊/低质量的图片（先预处理）
- 需要极高准确率的专业场景（人工校对）

## 快速开始

### 前置检查

```bash
# 确认 Tesseract 已安装（macOS Homebrew）
which tesseract
tesseract --version

# 确认语言包（应包含 chi_sim, chi_tra, eng）
tesseract --list-langs | grep -E "chi|eng"
```

### 基础用法

```bash
# 单张图片识别（输出到 stdout）
tesseract image.png stdout --psm 6 -l chi_sim+eng

# 识别并保存结果文件
tesseract invoice.jpg invoice_txt --psm 3 -l chi_sim

# 指定输出格式（HOCR 带坐标信息）
tesseract image.png output.hocr --psm 6 -l chi_sim -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789
```

### Python 自动化脚本

```python
import subprocess
import sys

def ocr_image(image_path, lang='chi_sim', psm=6):
    """
    使用 Tesseract 识别图片文字
    
    Args:
        image_path: 图片文件路径
        lang: 语言码（chi_sim/chi_tra/eng/jpn...）
        psm: 页面分割模式（6=单一文本块，3=完整页面分析）
    
    Returns:
        str: 识别出的文本内容
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
            return f"错误：{result.stderr}"
    except subprocess.TimeoutExpired:
        return "超时：识别时间超过 30 秒"
    except FileNotFoundError:
        return "未找到 tesseract 命令，请先安装"

# 使用示例
if __name__ == '__main__':
    image = sys.argv[1] if len(sys.argv) > 1 else 'test.png'
    text = ocr_image(image)
    print("=" * 50)
    print(text)
    print("=" * 50)
```

## PSM 模式选择指南

| PSM | 说明 | 适用场景 |
|-----|------|---------|
| 0 | 完全自动，不带 OSD | 通用场景 |
| 3 | 完整页面分析（默认） | 复杂布局文档 |
| 4 | 单个单词 | 单词卡片 |
| 6 | 假设单一文本块 | 截图文本框 ⭐ |
| 7 | 假设一行文本 | 标题行识别 |
| 11 | 单一列文本 | 纵向排版 |
| 13 | 单一字符 | 验证码识别 |

## 语言包管理

### 查看已安装语言

```bash
tesseract --list-langs
```

### 安装新语言包（macOS）

```bash
# 查看可用语言列表
ls /opt/homebrew/share/tessdata/*.traineddata

# 安装日文（如未存在）
brew install tesseract-lang/tesseract
```

### 常用语言代码

| 语言 | 代码 | 备注 |
|------|------|------|
| 简体中文 | `chi_sim` | |
| 繁体中文 | `chi_tra` | 竖排：`chi_tra_vert` |
| 英文 | `eng` | |
| 日文 | `jpn` | |
| 韩文 | `kor` | |
| 法文 | `fra` | |
| 德文 | `deu` | |

## 性能优化技巧

### 1. 图片预处理提升准确率

```python
from PIL import Image, ImageEnhance, ImageFilter

def preprocess_image(input_path, output_path):
    """增强图片以提高 OCR 准确率"""
    img = Image.open(input_path)
    
    # 转换为灰度
    img = img.convert('L')
    
    # 锐化
    img = ImageEnhance.Sharpness(img).enhance(1.5)
    
    # 二值化（阈值 128）
    threshold = 128
    img = img.point(lambda x: 255 if x > threshold else 0)
    
    img.save(output_path)
    return output_path
```

### 2. 批量化处理

```bash
#!/bin/bash
# batch_ocr.sh - 批量 OCR 处理

INPUT_DIR="${1:=./images}"
OUTPUT_DIR="${2:=./output}"
LANG="${3:=chi_sim}"

mkdir -p "$OUTPUT_DIR"

for img in "$INPUT_DIR"/*.{jpg,png,pdf,JPEG,PNG}; do
    [ -f "$img" ] || continue
    basename=$(basename "$img")
    echo "正在处理：$basename"
    tesseract "$img" "$OUTPUT_DIR/$basename" --psm 6 -l "$LANG"
done

echo "✅ 批量处理完成"
```

## 常见问题

### Q1: 识别率低怎么办？

1. **提高图片质量**：确保分辨率 ≥ 300 DPI
2. **调整 PSM 模式**：尝试不同数值
3. **添加字符白名单**：限制输出字符集
   ```bash
   tesseract img.png out --psm 6 -l eng -c tessedit_char_whitelist=0123456789ABCDEF
   ```
4. **预处理图片**：去噪、二值化、锐化

### Q2: 中英文混排怎么识别？

```bash
# 同时加载多个语言
tesseract image.png stdout -l chi_sim+eng --psm 6
```

### Q3: 表格如何识别？

```bash
# 启用表格检测
tesseract table.png stdout --psm 6 -l eng --oem 1 --psm 6 --userpatterns ./table.traineddata
```

## 与 PaddleOCR 对比

| 特性 | Tesseract | PaddleOCR |
|------|-----------|-----------|
| 中文准确率 | 中等 | **优秀** ⭐ |
| 安装复杂度 | 低（系统命令） | 高（Python 环境） |
| 模型大小 | ~20MB/语言 | ~200MB |
| 速度 | 快 | 较快 |
| 离线支持 | ✅ | ✅ |
| 手写识别 | ❌ | ⭕ 有限支持 |

**建议**：
- 简单任务用 Tesseract（已在您系统中）
- 追求中文准确率 → PaddleOCR

---

## 参考资源

- [Tesseract 官方文档](https://tesseract-ocr.github.io/)
- [PaddleOCR GitHub](https://github.com/PaddlePaddle/PaddleOCR)
- [Supported Languages](https://github.com/tesseract-ocr/tessdata)
