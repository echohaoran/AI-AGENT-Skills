---
name: feishu-fetch-doc
title: 读取飞书云文档
excerpt: 获取飞书云文档内容，返回 Markdown 格式
date: 2026-04-20
来源: 飞书机器人技能库
授权工具: [feishu_mcp_fetch_doc, feishu_doc_media, feishu_wiki_space_node]
---

# 读取飞书云文档

> **来源：** 飞书机器人技能库  
> **API 依赖：** 是 | **协议：** MIT

## 何时使用

✅ **使用此技能的场景：**

- 需要获取飞书云文档内容
- 用户分享了文档链接，需要读取内容
- 需要分析文档结构和文字内容

❌ **不要使用的场景：**

- 需要下载文档中的图片/文件（使用 feishu_doc_media）
- 需要修改文档（使用 update-doc）

## 核心功能

- 获取飞书云文档的 Markdown 内容
- 支持直接传 URL 或 token
- 支持知识库链接自动解析

## 参数说明

| 参数 | 说明 | 必需 |
|------|------|------|
| doc_id | 文档 URL 或 token | 是 |

**支持的 URL 格式**：
- 云文档：`https://xxx.feishu.cn/docx/Z1Fjxxx`
- 知识库：`https://xxx.feishu.cn/wiki/Z1Fjxxx`

## 媒体文件处理

文档中的图片、文件、画板需要单独下载：

### 图片格式
```html
<image token="Z1Fjxxx" width="1833" height="2491"/>
```

### 文件格式
```html
<view type="1">
  <file token="Z1Fjxxx" name="skills.zip"/>
</view>
```

### 下载步骤
1. 从 HTML 标签提取 `token` 属性
2. 调用 `feishu_doc_media` 下载：
```json
{
  "action": "download",
  "resource_token": "token值",
  "resource_type": "media",
  "output_path": "/path/to/save"
}
```

## 知识库链接处理

知识库链接（`/wiki/TOKEN`）可能指向不同类型文档：

| obj_type | 工具 |
|----------|------|
| docx | feishu_mcp_fetch_doc |
| sheet | feishu_sheet |
| bitable | feishu_bitable_* |

### 处理流程
1. 调用 `feishu_wiki_space_node`（action: get）解析 wiki token
2. 根据返回的 `obj_type` 调用对应工具

## 工具组合

| 需求 | 工具 |
|------|------|
| 获取文档文本 | feishu_mcp_fetch_doc |
| 下载图片/文件/画板 | feishu_doc_media |
| 解析 wiki 类型 | feishu_wiki_space_node |

## 相关技能

- [飞书文档创建](../feishu-create-doc/)
- [飞书文档更新](../feishu-update-doc/)
