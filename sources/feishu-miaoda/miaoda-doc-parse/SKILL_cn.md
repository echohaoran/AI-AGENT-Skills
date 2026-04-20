---
name: miaoda-doc-parse
title: 文档解析
excerpt: 将 PDF、Word、Excel、PPT 等文档转换为 Markdown
date: 2026-04-20
来源: 飞书机器人技能库
授权工具: [miaoda-studio-cli]
---

# 文档解析

> **来源：** 飞书机器人技能库  
> **API 依赖：** 是 | **协议：** MIT

## 何时使用

✅ **使用此技能的场景：**

- 需要解析 PDF 文件
- 需要读取 Word 文档
- 需要提取 Excel 表格数据
- 需要解析 PPT 演示文稿
- 用户提到"文档解析"、"PDF转文本"、"读取文档"

❌ **不要使用的场景：**

- 文档是飞书云文档（使用 feishu skill）
- 文档是网页（使用 web-fetch）
- 需要抓取网页内容

## 支持格式

| 格式 | 扩展名 |
|------|--------|
| PDF | .pdf |
| Word | .doc, .docx |
| PowerPoint | .pptx |
| Excel | .xlsx |
| CSV | .csv |
| 纯文本 | .txt, .md |
| 网页 | .html |

## 核心命令

```bash
miaoda-studio-cli doc-parse --file <文件路径或URL>
```

**参数**：
- `--file`：文档路径或 URL（必需）
- `--output, -o`：输出格式 text/json（默认 text）

## 使用示例

### 解析本地 PDF

```bash
miaoda-studio-cli doc-parse --file report.pdf
```

### 解析远程文档

```bash
miaoda-studio-cli doc-parse --file https://example.com/document.docx
```

### 输出 JSON

```bash
miaoda-studio-cli doc-parse --file data.xlsx --output json
```

## 使用决策

```
需要获取文档内容
├─ 本地文件或可下载 URL → miaoda-studio-cli doc-parse
├─ 文档是网页 → miaoda-studio-cli web-crawl
└─ 文档是飞书云文档 → feishu skill
```

## 相关技能

- [网页抓取](../miaoda-web-fetch/)
- [妙搭应用开发](../miaoda-coding/)
