---
name: feishu-bitable
title: 飞书多维表格
excerpt: 飞书多维表格（Bitable）的创建、查询、编辑和管理工具
date: 2026-04-20
来源: 飞书机器人技能库
授权工具: [feishu_bitable_app, feishu_bitable_app_table, feishu_bitable_app_table_field, feishu_bitable_app_table_record, feishu_bitable_app_table_view]
---

# 飞书多维表格

> **来源：** 飞书机器人技能库  
> **API 依赖：** 是 | **协议：** MIT

## 何时使用

✅ **使用此技能的场景：**

- 需要创建或管理飞书多维表格应用
- 需要在多维表格中新增、查询、修改、删除记录
- 需要管理字段（列）、视图、数据表
- 用户提到"多维表格"、"bitable"、"数据表"、"记录"
- 需要批量导入或更新数据

❌ **不要使用的场景：**

- 需要实时数据同步（从其他数据源同步的多维表格不支持增删改）
- 需要修改公式字段或查看引用字段（只读）

## 核心功能

| 功能 | 工具 | 说明 |
|------|------|------|
| 创建多维表格 | feishu_bitable_app | 创建新的多维表格应用 |
| 创建数据表 | feishu_bitable_app_table | 在应用内创建数据表 |
| 管理字段 | feishu_bitable_app_table_field | 新增、查询字段 |
| 管理记录 | feishu_bitable_app_table_record | 增删改查记录（行数据） |
| 管理视图 | feishu_bitable_app_table_view | 创建不同视图 |

## 重要约束

### 字段值格式

| 字段类型 | 正确格式 | 常见错误 |
|----------|----------|----------|
| 人员 | `[{id: "ou_xxx"}]` | 传字符串或包含name |
| 日期 | 毫秒时间戳 `1674206443000` | 传秒级时间戳或字符串 |
| 单选 | `"选项名"` | 传数组 |
| 多选 | `["选项1", "选项2"]` | 传字符串 |
| 超链接 | `{link: "URL", text: "显示"}` | 只传URL字符串 |
| 附件 | `[{file_token: "xxx"}]` | 传外部URL |

### 操作限制

- **批量上限**：单次最多500条记录
- **并发写**：同一数据表不支持并发写，需串行调用
- **默认表空行**：创建应用后自带空行，插入数据前建议先删除

## 使用示例

### 查询字段类型

```json
{
  "action": "list",
  "app_token": "S404b...",
  "table_id": "tbl..."
}
```

### 批量导入客户数据

```json
{
  "action": "batch_create",
  "app_token": "S404b...",
  "table_id": "tbl...",
  "records": [
    {
      "fields": {
        "客户名称": "Bytedance",
        "负责人": [{"id": "ou_xxx"}],
        "签约日期": 1674206443000,
        "状态": "进行中"
      }
    }
  ]
}
```

### 筛选查询

```json
{
  "action": "list",
  "filter": {
    "conjunction": "and",
    "conditions": [
      {"field_name": "状态", "operator": "is", "value": ["进行中"]}
    ]
  }
}
```

## 相关技能

- [飞书文档创建](../feishu-create-doc/)
- [飞书文档更新](../feishu-update-doc/)
- [飞书任务管理](../feishu-task/)
