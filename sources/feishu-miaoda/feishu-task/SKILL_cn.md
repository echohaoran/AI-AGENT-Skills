---
name: feishu-task
title: 飞书任务管理
excerpt: 飞书任务管理工具，用于创建、查询、更新任务和清单
date: 2026-04-20
来源: 飞书机器人技能库
授权工具: [feishu_task_task, feishu_task_tasklist]
---

# 飞书任务管理

> **来源：** 飞书机器人技能库  
> **API 依赖：** 是 | **协议：** MIT

## 何时使用

✅ **使用此技能的场景：**

- 需要创建、查询、更新任务
- 需要创建和管理任务清单
- 需要查看任务列表或清单内的任务
- 用户提到"任务"、"待办"、"to-do"、"清单"
- 需要设置任务负责人、关注人、截止时间

❌ **不要使用的场景：**

- 需要日历功能（使用 feishu-calendar）
- 需要管理多维表格数据（使用 feishu-bitable）

## 核心功能

| 用户意图 | 工具 | action | 必填参数 |
|----------|------|--------|----------|
| 新建待办 | feishu_task_task | create | summary |
| 查未完成任务 | feishu_task_task | list | - |
| 获取任务详情 | feishu_task_task | get | task_guid |
| 完成任务 | feishu_task_task | patch | task_guid, completed_at |
| 反完成任务 | feishu_task_task | patch | task_guid, completed_at="0" |
| 创建清单 | feishu_task_tasklist | create | name |
| 查看清单任务 | feishu_task_tasklist | tasks | tasklist_guid |

## 重要约束

### 时间格式
- 使用 ISO 8601 / RFC 3339 格式
- 例如：`2026-02-28T17:00:00+08:00`

### current_user_id 强烈建议
传入当前用户 ID（从 SenderId 获取），工具会自动添加为 follower，确保创建者可以编辑任务。

### 任务成员角色
- **assignee（负责人）**：负责完成任务，可以编辑
- **follower（关注人）**：关注进展，接收通知

### completed_at 用法

| 用法 | 值 |
|------|---|
| 完成任务 | `"2026-02-26T15:30:00+08:00"` |
| 反完成（恢复） | `"0"` |

## 使用示例

### 创建任务并分配负责人

```json
{
  "action": "create",
  "summary": "准备周会材料",
  "description": "整理本周工作进展",
  "current_user_id": "ou_发送者",
  "due": {
    "timestamp": "2026-02-28T17:00:00+08:00",
    "is_all_day": false
  },
  "members": [
    {"id": "ou_协作者", "role": "assignee"}
  ]
}
```

### 查询未完成任务

```json
{
  "action": "list",
  "completed": false,
  "page_size": 20
}
```

### 完成任务

```json
{
  "action": "patch",
  "task_guid": "xxx",
  "completed_at": "2026-02-26T15:30:00+08:00"
}
```

### 反完成任务

```json
{
  "action": "patch",
  "task_guid": "xxx",
  "completed_at": "0"
}
```

### 创建清单并添加成员

```json
{
  "action": "create",
  "name": "产品迭代 v2.0",
  "members": [
    {"id": "ou_xxx", "role": "editor"},
    {"id": "ou_yyy", "role": "viewer"}
  ]
}
```

## 相关技能

- [飞书日历管理](../feishu-calendar/)
- [飞书消息读取](../feishu-im-read/)
