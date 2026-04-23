---
name: miaoda-text-gen-image
description: "Use when user needs to generate images from text descriptions. Provides necessary command usage instructions for generating images from text. Supports various aspect ratios and AI watermark. 触发词：生成图片, 画图, 图片生成, text to image, 文字生成图片, AI 画图, 生成配图, 生成封面, 生成插图, generate image, 画一张, 做一张图"
---

# Image Generation

通过 `miaoda-studio-cli text-to-image` 根据文字描述生成 AI 图片，返回图片的URL。

## Quick Reference

| 参数 | 说明 | 必需 | 默认值 |
|------|------|------|--------|
| `--prompt` | 图片描述（越详细效果越好） | 是 | - |
| `--ratio` | 宽高比 | 否 | 1:1 |
| `--watermark` | 添加 AI 水印 | 否 | false |
| `--output, -o` | 输出格式: text/json | 否 | text |

## 宽高比选择

| 用途 | 推荐 ratio | 说明 |
|------|-----------|------|
| 头像、图标、Logo | `1:1` | 正方形，默认值 |
| 文章配图、横幅 | `4:3` 或 `3:2` | 通用横向 |
| 演示文稿、视频封面 | `16:9` | 宽屏横向 |
| 手机壁纸、竖版海报 | `9:16` | 竖屏 |
| 社交媒体竖版 | `3:4` | 略竖 |
| 超宽横幅 | `21:9` | 超宽屏 |
| 竖版内容 | `2:3` | 竖版 |

## 使用示例

```bash
# 基础用法
miaoda-studio-cli text-to-image --prompt "一只可爱的橘猫在阳光下打盹，暖色调，柔和光线"

# 指定宽高比 + 水印
miaoda-studio-cli text-to-image --prompt "科技感十足的数据可视化仪表盘，深蓝色背景" --ratio 16:9 --watermark

# 获取 JSON 输出（含图片 URL）
miaoda-studio-cli text-to-image --prompt "极简风格的山水画" --ratio 3:2 --output json
```

## Common Mistakes

| 错误 | 正确做法 |
|------|----------|
| prompt 过于简短（如"猫"） | 描述主体 + 场景 + 风格 + 色调，越详细效果越好 |
| 不指定 `--ratio`，横屏场景用了默认 1:1 | 根据实际用途选择合适的宽高比 |
| prompt 中包含品牌名、真实人物 | 避免版权内容，用描述性语言替代 |
| 需要图片 URL 但未加 `--output json` | 需要获取图片 URL 时加 `--output json` |
| 命令失败后不重试 | 退出码 `1` 表示失败，简化 prompt 后重试 |
