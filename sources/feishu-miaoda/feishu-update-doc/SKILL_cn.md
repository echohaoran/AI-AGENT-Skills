---
name: feishu-update-doc
title: 更新飞书云文档
excerpt: 更新飞书云文档，支持7种更新模式：追加、覆盖、定位替换、全文替换、前/后插入、删除
date: 2026-04-20
来源: 飞书机器人技能库
授权工具: [feishu__update_doc]
---

# 更新飞书云文档

> **来源：** 飞书机器人技能库  
> **API 依赖：** 是 | **协议：** MIT

## 何时使用

✅ **使用此技能的场景：**

- 需要更新现有飞书文档内容
- 需要追加新内容到文档
- 需要替换文档中的特定内容
- 需要删除文档中的某些内容

❌ **不要使用的场景：**

- 需要读取文档内容（使用 fetch-doc）
- 需要创建新文档（使用 create-doc）

## 7种更新模式

| 模式 | 说明 | 需要 markdown |
|------|------|---------------|
| append | 追加到末尾 | 是 |
| overwrite | 完全覆盖 | 是 |
| replace_range | 定位替换 | 是 |
| replace_all | 全文替换（多处） | 是 |
| insert_before | 前插入 | 是 |
| insert_after | 后插入 | 是 |
| delete_range | 删除内容 | 否 |

## 定位方式

### selection_with_ellipsis - 内容定位

- **范围匹配**：`开头内容...结尾内容`
- **精确匹配**：`完整内容`（不含 `...`）

### selection_by_title - 标题定位

格式：`## 章节标题`（可带或不带 # 前缀）

自动定位整个章节（到下一个同级或更高级标题之前）。

## 使用示例

### append - 追加到末尾

```json
{
  "doc_id": "文档ID或URL",
  "mode": "append",
  "markdown": "## 新章节\n\n追加的内容..."
}
```

### replace_range - 定位替换

```json
{
  "doc_id": "文档ID或URL",
  "mode": "replace_range",
  "selection_with_ellipsis": "## 旧章节标题...旧章节结尾",
  "markdown": "## 新章节标题\n\n新的内容..."
}
```

### replace_all - 全文替换

```json
{
  "doc_id": "文档ID或URL",
  "mode": "replace_all",
  "selection_with_ellipsis": "张三",
  "markdown": "李四"
}
```

### delete_range - 删除内容

```json
{
  "doc_id": "文档ID或URL",
  "mode": "delete_range",
  "selection_with_ellipsis": "## 废弃章节...不再需要的内容"
}
```

## 最佳实践

### 小粒度精确替换
定位范围越小越安全，尤其是表格、分栏等嵌套块。

### 保护不可重建内容
图片、画板、电子表格等以 token 形式存储，替换时避开这些区域。

### 分步更新优于整体覆盖
多次小范围替换，逐步修改，保留原有媒体和评论。

## 相关技能

- [飞书文档创建](../feishu-create-doc/)
- [飞书文档读取](../feishu-fetch-doc/)
