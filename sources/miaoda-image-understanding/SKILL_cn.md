---
name: miaoda-image-understanding
title: 图片理解
excerpt: AI 理解、分析和描述图片内容，支持截图、照片、图表
date: 2026-04-20
来源: 飞书机器人技能库
授权工具: [miaoda-studio-cli]
---

# 图片理解

> **来源：** 飞书机器人技能库  
> **API 依赖：** 是 | **协议：** MIT

## 何时使用

✅ **使用此技能的场景：**

- 用户需要看图、理解图片内容
- 需要分析截图、照片、图表
- 需要识别图中信息
- 用户提到"看看这张图"、"图片理解"、"图片分析"

❌ **不要使用的场景：**

- 需要处理 PDF/Word 文档（使用 doc-parse）
- 图片需要进一步处理（编辑、裁剪）

## 核心命令

```bash
miaoda-studio-cli image-understanding --image <本地图片路径>
```

**参数**：
- `--image, -i`：本地图片路径（必需）
- `--prompt, -p`：关于图片的问题（默认：描述图片内容）
- `--output, -o`：输出格式 text/json（默认 text）

## 使用示例

### 描述图片内容

```bash
miaoda-studio-cli image-understanding --image ./photo.png
```

### 针对图片提问

```bash
miaoda-studio-cli image-understanding --image ./photo.png --prompt "这张图片中有什么"
```

### 提取图片文字

```bash
miaoda-studio-cli image-understanding --image ./screenshot.png --prompt "提取图片中的文字"
```

### 分析图片风格

```bash
miaoda-studio-cli image-understanding -i ./photo.jpg -p "分析图片的色彩风格"
```

## 使用决策

```
需要理解图片内容
├─ 描述整体 → 不指定 prompt
├─ 针对提问 → 用 --prompt
├─ 提取文字 → --prompt "提取图片中的文字"
└─ 分析风格 → --prompt 描述分析需求
```

## 相关技能

- [文生图](../miaoda-text-gen-image/)
- [视频帧提取](../video-frames/)
