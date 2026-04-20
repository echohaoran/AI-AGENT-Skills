---
name: feishu-im-read
title: 飞书消息读取
excerpt: 读取群聊/单聊历史消息、话题回复，支持跨会话搜索和资源下载
date: 2026-04-20
来源: 飞书机器人技能库
授权工具: [feishu_im_user_get_messages, feishu_im_user_get_thread_messages, feishu_im_user_search_messages, feishu_im_user_fetch_resource]
---

# 飞书消息读取

> **来源：** 飞书机器人技能库  
> **API 依赖：** 是 | **协议：** MIT

## 何时使用

✅ **使用此技能的场景：**

- 需要获取群聊或单聊的历史消息
- 需要读取话题（thread）内的回复消息
- 需要跨会话搜索消息（关键词、发送者、时间）
- 消息中包含图片、文件需要下载
- 用户提到"聊天记录"、"消息"、"群里说了什么"

❌ **不要使用的场景：**

- 需要发送消息（使用其他飞书消息工具）
- 用户没有权限查看的会话

## 核心功能

| 用户意图 | 工具 | 必填参数 |
|----------|------|----------|
| 获取历史消息 | feishu_im_user_get_messages | chat_id 或 open_id |
| 获取话题回复 | feishu_im_user_get_thread_messages | thread_id |
| 跨会话搜索 | feishu_im_user_search_messages | 至少一个过滤条件 |
| 下载图片 | feishu_im_user_fetch_resource | message_id, file_key, type="image" |
| 下载文件 | feishu_im_user_fetch_resource | message_id, file_key, type="file" |

## 时间过滤

| 方式 | 参数 | 示例 |
|------|------|------|
| 相对时间 | relative_time | today, yesterday, this_week |
| 精确时间 | start_time + end_time | 2026-02-27T00:00:00+08:00 |

**注意**：relative_time 和 start_time/end_time 互斥，不能同时使用

## 话题消息处理

发现 thread_id 时，建议主动获取话题最新 10 条回复：

```json
{
  "thread_id": "omt_xxx",
  "page_size": 10,
  "sort_rule": "create_time_desc"
}
```

## 资源下载

| 资源类型 | 内容标记 | 参数 |
|----------|----------|------|
| 图片 | `![image](img_xxx)` | type="image" |
| 文件 | `<file key="file_xxx"/>` | type="file" |
| 音频 | `<audio key="file_xxx"/>` | type="file" |
| 视频 | `<video key="file_xxx"/>` | type="file" |

## 使用示例

### 获取群聊消息并展开话题

步骤1：获取群聊消息
```json
{"chat_id": "oc_xxx"}
```

步骤2：展开话题最新回复
```json
{"thread_id": "omt_xxx", "page_size": 10, "sort_rule": "create_time_desc"}
```

### 跨会话搜索消息

```json
{"query": "项目进度", "chat_id": "oc_xxx"}
```

### 下载消息中的图片

```json
{"message_id": "om_xxx", "file_key": "img_v3_xxx", "type": "image"}
```

## 相关技能

- [飞书日历管理](../feishu-calendar/)
- [飞书任务管理](../feishu-task/)
