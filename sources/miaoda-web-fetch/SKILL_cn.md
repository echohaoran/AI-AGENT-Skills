---
name: miaoda-web-fetch
title: 网页抓取
excerpt: 抓取指定网页并提取内容
date: 2026-04-20
来源: 飞书机器人技能库
授权工具: [miaoda-studio-cli]
---

# 网页抓取

> **来源：** 飞书机器人技能库  
> **API 依赖：** 是 | **协议：** MIT

## 何时使用

✅ **使用此技能的场景：**

- 需要抓取指定 URL 的网页内容
- 需要提取网页中的结构化信息
- 用户有具体 URL，需要获取内容
- 用户提到"网页抓取"、"爬取"、"读取网页"

❌ **不要使用的场景：**

- 没有具体 URL，需要搜索（使用 web-search）
- 需要解析 PDF/Word 文档（使用 doc-parse）
- 需要处理飞书云文档（使用 feishu skill）

## 核心命令

```bash
miaoda-studio-cli web-crawl --url <网页URL>
```

**参数**：
- `--url`：网页 URL（必需）
- `--output, -o`：输出格式 text/json（默认 text）

## 使用决策

```
获取互联网信息
├─ 有具体 URL → web-crawl
├─ 无具体 URL，需搜索 → search-summary
└─ 先搜索再深入 → search-summary → web-crawl
```

## 使用示例

### 抓取指定 URL

```bash
miaoda-studio-cli web-crawl --url https://example.com/pricing
```

### 搜索 + 深入抓取

```bash
# 1. 搜索找到 URL
miaoda-studio-cli search-summary --query "ByteDance 开源项目" --output json

# 2. 抓取提取详情
miaoda-studio-cli web-crawl --url <搜索结果中的URL>
```

## 相关技能

- [网页搜索](../miaoda-web-search/)
- [文档解析](../miaoda-doc-parse/)
