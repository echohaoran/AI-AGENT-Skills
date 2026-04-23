---
name: miaoda-text-gen-image
title: 文生图
excerpt: 根据文字描述生成 AI 图片
date: 2026-04-20
来源: 飞书机器人技能库
授权工具: [miaoda-studio-cli]
---

# 文生图

> **来源：** 飞书机器人技能库  
> **API 依赖：** 是 | **协议：** MIT

## 何时使用

✅ **使用此技能的场景：**

- 需要生成配图
- 需要生成封面图
- 需要生成插图
- 用户提到"生成图片"、"画图"、"AI 画图"

❌ **不要使用的场景：**

- 需要真实人物或品牌图片（版权问题）
- 需要精确的产品图
- 需要复杂编辑（使用图片理解+编辑工具）

## 核心命令

```bash
miaoda-studio-cli text-to-image --prompt "<描述>"
```

**参数**：
- `--prompt`：图片描述（必需，越详细效果越好）
- `--ratio`：宽高比（默认 1:1）
- `--watermark`：添加 AI 水印（默认 false）
- `--output, -o`：输出格式 text/json（默认 text）

## 宽高比选择

| 用途 | ratio | 说明 |
|------|-------|------|
| 头像、图标 | 1:1 | 正方形，默认 |
| 文章配图 | 4:3 或 3:2 | 通用横向 |
| 演示封面 | 16:9 | 宽屏横向 |
| 手机壁纸 | 9:16 | 竖屏 |
| 社交竖版 | 3:4 | 略竖 |
| 超宽横幅 | 21:9 | 超宽屏 |

## 使用示例

### 基础用法

```bash
miaoda-studio-cli text-to-image --prompt "一只可爱的橘猫在阳光下打盹，暖色调"
```

### 指定宽高比 + 水印

```bash
miaoda-studio-cli text-to-image --prompt "科技感数据仪表盘" --ratio 16:9 --watermark
```

### 获取 JSON 输出（含 URL）

```bash
miaoda-studio-cli text-to-image --prompt "极简山水画" --ratio 3:2 --output json
```

## 常见错误

| 错误 | 正确做法 |
|------|----------|
| prompt 过于简短 | 描述主体+场景+风格+色调 |
| 用途不符 | 根据场景选择合适 ratio |
| 版权内容 | 避免品牌名、真实人物 |

## 相关技能

- [图片理解](../miaoda-image-understanding/)
- [妙搭应用开发](../miaoda-coding/)
