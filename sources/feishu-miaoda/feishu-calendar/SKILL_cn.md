---
name: feishu-calendar
title: 飞书日历管理
excerpt: 飞书日历与日程管理工具集，包含日历管理、日程管理、参会人管理和忙闲查询
date: 2026-04-20
来源: 飞书机器人技能库
授权工具: [feishu_calendar_event, feishu_calendar_freebusy, feishu_calendar_event_attendee]
---

# 飞书日历管理

> **来源：** 飞书机器人技能库  
> **API 依赖：** 是 | **协议：** MIT

## 何时使用

✅ **使用此技能的场景：**

- 创建会议或日程
- 查询某个时间段的日程安排
- 查看用户的忙闲时间
- 邀请参会人（包括会议室）
- 修改或取消日程
- 搜索日程关键词
- 回复日程邀请

❌ **不要使用的场景：**

- 需要处理日历权限管理（非主日历）
- 需要查看其他用户的所有日历（受权限限制）

## 核心功能

| 用户意图 | 工具 | action |
|----------|------|--------|
| 创建会议 | feishu_calendar_event | create |
| 查询日程 | feishu_calendar_event | list |
| 修改日程 | feishu_calendar_event | patch |
| 搜索日程 | feishu_calendar_event | search |
| 回复邀请 | feishu_calendar_event | reply |
| 查询忙闲 | feishu_calendar_freebusy | list |
| 邀请参会人 | feishu_calendar_event_attendee | create |

## 重要约束

### 时间格式
- 使用 ISO 8601 / RFC 3339 格式
- 例如：`2026-02-25T14:00:00+08:00`
- 时区固定为 Asia/Shanghai（UTC+8）

### user_open_id 必填
创建日程时强烈建议传入 `user_open_id`（从 SenderId 获取），确保：
- 发起人能收到日程通知
- 发起人出现在参会人列表中

### 参会人类型
- `user` + `ou_xxx` — 飞书用户
- `chat` + `oc_xxx` — 群组
- `resource` + `omm_xxx` — 会议室
- `third_party` + `email` — 外部邮箱

### 会议室预约
会议室预约是异步流程，状态会从 `needs_action` 变为 `accept` 或 `decline`。

## 使用示例

### 创建会议并邀请参会人

```json
{
  "action": "create",
  "summary": "项目复盘会议",
  "description": "讨论 Q1 项目进展",
  "start_time": "2026-02-25T14:00:00+08:00",
  "end_time": "2026-02-25T15:30:00+08:00",
  "user_open_id": "ou_aaa",
  "attendees": [
    {"type": "user", "id": "ou_bbb"},
    {"type": "resource", "id": "omm_xxx"}
  ]
}
```

### 查询用户忙闲

```json
{
  "action": "list",
  "time_min": "2026-02-25T09:00:00+08:00",
  "time_max": "2026-02-25T18:00:00+08:00",
  "user_ids": ["ou_aaa", "ou_bbb"]
}
```

### 回复日程邀请

```json
{
  "action": "reply",
  "event_id": "xxx_0",
  "rsvp_status": "accept"
}
```

## 相关技能

- [飞书任务管理](../feishu-task/)
- [飞书消息读取](../feishu-im-read/)
