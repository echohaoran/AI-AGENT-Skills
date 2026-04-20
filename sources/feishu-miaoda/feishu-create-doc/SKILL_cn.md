---
name: feishu-create-doc
title: 创建飞书云文档
excerpt: 从 Markdown 内容创建飞书云文档，支持飞书扩展语法、高亮块、表格、画板等
date: 2026-04-20
来源: 飞书机器人技能库
授权工具: [feishu_mcp_create_doc]
---

# 创建飞书云文档

> **来源：** 飞书机器人技能库  
> **API 依赖：** 是 | **协议：** MIT

## 何时使用

✅ **使用此技能的场景：**

- 需要创建新的飞书云文档
- 需要在指定文件夹或知识库创建文档
- 用户提到"创建文档"、"新建文档"、"写个文档"

❌ **不要使用的场景：**

- 需要更新现有文档（使用 update-doc）
- 需要读取文档内容（使用 fetch-doc）

## 核心功能

- 从 Markdown 创建飞书云文档
- 支持指定创建位置（文件夹/知识库/知识空间）
- 支持飞书扩展语法（高亮块、表格、画板等）

## 参数说明

| 参数 | 说明 | 必需 |
|------|------|------|
| markdown | 文档内容（飞书 Markdown 格式） | 是 |
| title | 文档标题 | 否 |
| folder_token | 父文件夹 token | 否 |
| wiki_node | 知识库节点 token | 否 |
| wiki_space | 知识空间 ID（`my_library` 为个人知识库） | 否 |

**参数优先级**：wiki_node > wiki_space > folder_token

## 飞书扩展语法

### 高亮块（Callout）

```html
<callout emoji="💡" background-color="light-blue">
重要提示内容
</callout>
```

### 表格

```markdown
| 列1 | 列2 |
|------|------|
| 内容1 | 内容2 |
```

### 画板（Mermaid）

````markdown
```mermaid
graph TD
    A[开始] --> B{判断}
```
````

### 图片

```html
<image url="https://example.com/image.png" width="800" height="600"/>
```

## 使用示例

### 创建简单文档

```json
{
  "title": "项目计划",
  "markdown": "# 项目概述\n\n这是一个新项目。"
}
```

### 创建到指定文件夹

```json
{
  "title": "会议纪要",
  "folder_token": "fldcnXXXX",
  "markdown": "# 周会 2025-01-15"
}
```

### 使用飞书扩展语法

```json
{
  "title": "产品需求",
  "markdown": "<callout emoji=\"💡\" background-color=\"light-blue\">\n重要需求说明\n</callout>\n\n## 功能列表\n\n| 功能 | 优先级 |\n|------|--------|\n| 登录 | P0 |\n"
}
```

## 注意事项

- **禁止重复标题**：markdown 开头不要写与 title 相同的一级标题
- **目录自动生成**：飞书会自动生成目录，无需手动添加
- **创建长文档**：建议配合 update-doc 的 append 模式分段创建，提高成功率

## 相关技能

- [飞书文档更新](../feishu-update-doc/)
- [飞书文档读取](../feishu-fetch-doc/)
- [飞书多维表格](../feishu-bitable/)
