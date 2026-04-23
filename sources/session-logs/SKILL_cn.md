---
name: session-logs
title: 会话日志搜索
excerpt: 搜索和分析历史会话记录
date: 2026-04-20
来源: 飞书机器人技能库
授权工具: [命令行工具, jq, ripgrep]
---

# 会话日志搜索

> **来源：** 飞书机器人技能库  
> **API 依赖：** 是 | **协议：** MIT

## 何时使用

✅ **使用此技能的场景：**

- 用户提到之前的对话
- 需要查找历史上下文
- 需要回顾之前的讨论内容
- 用户问"之前说过什么"、"上次聊了什么"

❌ **不要使用的场景：**

- 新对话
- 只需要当前会话内容

## 日志位置

```
~/.openclaw/agents/<agentId>/sessions/
```

文件：
- `sessions.json` — 会话索引
- `<session-id>.jsonl` — 完整对话记录

## 日志结构

每条消息包含：
- `type`："session"（元数据）或 "message"
- `timestamp`：ISO 时间戳
- `message.role`："user"、"assistant" 或 "toolResult"
- `message.content[]`：文本、思考或工具调用
- `message.usage.cost.total`：响应成本

## 常用查询

### 列出所有会话

```bash
for f in ~/.openclaw/agents/<agentId>/sessions/*.jsonl; do
  date=$(head -1 "$f" | jq -r '.timestamp' | cut -dT -f1)
  size=$(ls -lh "$f" | awk '{print $5}')
  echo "$date $size $(basename $f)"
done | sort -r
```

### 查找特定日期的会话

```bash
for f in ~/.openclaw/agents/<agentId>/sessions/*.jsonl; do
  head -1 "$f" | jq -r '.timestamp' | grep -q "2026-01-06" && echo "$f"
done
```

### 提取用户消息

```bash
jq -r 'select(.message.role == "user") | .message.content[]? | select(.type == "text") | .text' <session>.jsonl
```

### 搜索关键词

```bash
jq -r 'select(.message.role == "assistant") | .message.content[]? | select(.type == "text") | .text' <session>.jsonl | rg -i "关键词"
```

### 统计成本

```bash
jq -s '[.[] | .message.usage.cost.total // 0] | add' <session>.jsonl
```

### 搜索所有会话

```bash
rg -l "关键词" ~/.openclaw/agents/<agentId>/sessions/*.jsonl
```

## 相关技能

- [主机安全加固](../healthcheck/)
