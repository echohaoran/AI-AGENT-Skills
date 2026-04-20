---
name: miaoda-web-search
title: 网页搜索
excerpt: 按关键词搜索互联网信息，返回结构化结果
date: 2026-04-20
来源: 飞书机器人技能库
授权工具: [miaoda-studio-cli]
---

# 网页搜索

> **来源：** 飞书机器人技能库  
> **API 依赖：** 是 | **协议：** MIT

## 何时使用

✅ **使用此技能的场景：**

- 需要查找、验证任何互联网信息
- 需要搜索最新资讯
- 没有具体 URL，需要先搜索
- 用户提到"搜索"、"搜一下"、"查一下"

❌ **不要使用的场景：**

- 有具体 URL（直接用 web-fetch）
- 需要历史天气数据
- 需要专业气象分析

## 核心命令

```bash
miaoda-studio-cli search-summary --query "<关键词>"
```

**参数**：
- `--query`：搜索关键词（1-500 字符，必需）
- `--output, -o`：输出格式 text/json（默认 text）

## 使用决策

```
获取互联网信息
├─ 有具体 URL → web-crawl
├─ 无具体 URL → search-summary
└─ 先搜索再深入 → search-summary → web-crawl
```

## 使用示例

### 基础搜索

```bash
miaoda-studio-cli search-summary --query "React 19 新特性"
```

### 搜索并输出 JSON

```bash
miaoda-studio-cli search-summary --query "ByteDance 开源项目" --output json
```

## 常见错误

| 错误 | 正确做法 |
|------|----------|
| 无 URL 用 web-crawl | 用 search-summary |
| 关键词超 500 字符 | 提炼核心关键词 |
| 需要程序处理 | 加 --output json |

## 相关技能

- [网页抓取](../miaoda-web-fetch/)
- [图片理解](../miaoda-image-understanding/)
