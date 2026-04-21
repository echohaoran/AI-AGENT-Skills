---
name: markitdown
title: 文档转 Markdown 工具
excerpt: 微软开发的文档格式转换工具，将 DOCX、XLSX、PPTX、PDF、图片、EPUB、HTML 等格式转换为干净的 Markdown。
date: 2026-04-21
来源: microsoft/markitdown
安装量: 4500+
授权工具:
  - Bash
  - Read
  - Write
---

# markitdown - 文档转 Markdown 工具

> **来源：** microsoft/markitdown  
> **类型：** CLI 文档转换器  
> **协议：** MIT | **平台：** macOS, Linux, Windows

## 概览

markitdown 是微软开发的 CLI 工具，可将各种文档格式转换为干净、可读的 Markdown 格式。支持 DOCX、XLSX、PPTX、PDF、图片（带 OCR）、EPUB、HTML 等格式。

**核心特点：**
- ✅ 批量转换多个文件
- ✅ 保留格式（表格、标题、列表）
- ✅ 图片和扫描 PDF 的 OCR 识别
- ✅ 跨平台（macOS、Linux、Windows）
- ✅ 无需 API 密钥 — 本地运行

## 安装

### 方式一：npm（macOS/Linux 推荐）

```bash
npm install -g @microsoft/markitdown
```

### 方式二：dotnet tool

```bash
dotnet tool install -g markitdown
```

### 方式三：下载二进制

```bash
# macOS
curl -fsSL https://github.com/microsoft/markitdown/releases/latest/download/markitdown-macos-x64.tar.gz | tar -xz
sudo mv markitdown /usr/local/bin/

# Linux
curl -fsSL https://github.com/microsoft/markitdown/releases/latest/download/markitdown-linux-x64.tar.gz | tar -xz
sudo mv markitdown /usr/local/bin/
```

### 验证安装

```bash
markitdown --version
```

## 支持的格式

| 格式 | 扩展名 | 说明 |
|------|--------|------|
| Word | .docx | ✅ 完全支持 |
| Excel | .xlsx | ✅ 表格保留 |
| PowerPoint | .pptx | ✅ 包含备注 |
| PDF | .pdf | ✅ 文本提取 |
| 图片 | .png, .jpg | 🅾️ 需 OCR |
| EPUB | .epub | ✅ 完全支持 |
| HTML | .html | ✅ 完全支持 |
| Markdown | .md | ✅ 直通 |

## 快速开始

### 基本用法

```bash
# 转换单个文件
markitdown 文档.docx -o 输出.md

# 输出到标准输出
markitdown 文档.docx

# 转换多个文件
markitdown 文件1.docx 文件2.xlsx 文件3.pdf

# 转换整个目录
markitdown ./文档/

# 输出到指定目录
markitdown ./文档/ -o ./markdown/
```

### 高级选项

```bash
# 启用图片 OCR
markitdown 图片.png --ocr -o 输出.md

# 跳过不支持的文件
markitdown ./文档/ --skip

# 详细输出
markitdown 文档.docx -v

# 提取图片到目录
markitdown 文档.docx --extract-images ./图片/

# 保留原文件名
markitdown ./文档/ --preserve-filenames -o ./输出/
```

## 使用场景

### 场景一：批量转换 Office 文档

```bash
# 将所有 Office 文件转换为 Markdown
for f in *.docx *.xlsx *.pptx; do
    markitdown "$f" -o "./md/${f%.*}.md"
done
```

### 场景二：OCR 处理扫描 PDF

```bash
# 启用 OCR 处理扫描文档
markitdown 扫描件.pdf --ocr -o 输出.md
```

### 场景三：提取电子书内容

```bash
# 将电子书转换为 Markdown 用于分析
markitdown 电子书.epub -o 电子书.md
```

### 场景四：网页存档

```bash
# 将网页保存为 Markdown
markitdown https://example.com/article -o 文章.md
```

## 脚本参考

### `scripts/batch-convert.sh` — 批量转换

```bash
#!/bin/bash
# 批量转换目录中的所有支持文件

输入目录="${1:-.}"
输出目录="${2:-./markitdown-output}"

mkdir -p "$输出目录"

find "$输入目录" -type f \( \
    -name "*.docx" -o \
    -name "*.xlsx" -o \
    -name "*.pptx" -o \
    -name "*.pdf" -o \
    -name "*.epub" -o \
    -name "*.html" \
\) | while read -r file; do
    basename=$(basename "$file")
    filename="${basename%.*}"
    output="$输出目录/$filename.md"
    
    echo "📄 转换中: $basename"
    markitdown "$file" -o "$output" 2>/dev/null
    
    if [ $? -eq 0 ]; then
        echo "  ✅ → $output"
    else
        echo "  ❌ 失败"
    fi
done

echo ""
echo "📊 转换完成！"
echo "输出目录: $输出目录"
```

### `scripts/ocr-pipeline.sh` — OCR 处理

```bash
#!/bin/bash
# 使用 OCR 处理图片和扫描 PDF

输入="$1"
输出="${2:-output.md}"

echo "🔍 OCR 处理中: $输入"
markitdown "$输入" --ocr -o "$输出"

if [ $? -eq 0 ]; then
    echo "✅ OCR 完成: $输出"
    echo "字数统计: $(wc -w < "$输出")"
else
    echo "❌ OCR 失败"
fi
```

## 与其他工具对比

| 功能 | markitdown | pandoc | docx2txt |
|------|------------|--------|----------|
| DOCX | ✅ | ✅ | ✅ |
| XLSX | ✅ | ✅ | ❌ |
| PPTX | ✅ | ✅ | ❌ |
| PDF | ✅ | ✅ | ❌ |
| 图片 OCR | ✅ | ❌ | ❌ |
| EPUB | ✅ | ✅ | ❌ |
| 无依赖 | ✅ | ❌ | ✅ |
| 跨平台 | ✅ | ✅ | ✅ |

## 故障排除

| 问题 | 解决方案 |
|------|---------|
| "command not found" | 使用 `npm install -g @microsoft/markitdown` 安装 |
| "提取失败" | 文件可能损坏或受密码保护 |
| OCR 不工作 | 安装 Tesseract：`brew install tesseract` |
| 转换慢 | 使用 `--skip` 跳过问题文件 |

## 与其他技能协同

- **pdf-generator** → 链式：markitdown → pdf-generator 格式转换
- **mermaid** → 提取内容 → 生成图表
- **markdown-documentation** → 转换文档 → 生成文档
- **file-organizer** → 批量整理转换后的文件

## 相关链接

- [GitHub 仓库](https://github.com/microsoft/markitdown)
- [npm 包](https://www.npmjs.com/package/@microsoft/markitdown)
- [微软开发者博客](https://devblogs.microsoft.com/)
