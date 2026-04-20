---
name: weather
title: 天气查询
excerpt: 获取当前天气和天气预报
date: 2026-04-20
来源: 飞书机器人技能库
授权工具: [curl]
---

# 天气查询

> **来源：** 飞书机器人技能库  
> **API 依赖：** 是（wttr.in） | **协议：** MIT

## 何时使用

✅ **使用此技能的场景：**

- 用户问天气
- 需要查询温度
- 需要天气预报
- 旅行规划天气检查
- 用户提到"天气"、"温度"、"下雨吗"

❌ **不要使用的场景：**

- 需要历史天气数据
- 需要专业气象分析
- 需要气象预警（查询官方渠道）
- 需要航空/航海气象

## 核心命令

### 当前天气（一行）

```bash
curl "wttr.in/London?format=3"
```

### 详细当前天气

```bash
curl "wttr.in/London?0"
```

### 3 天预报

```bash
curl "wttr.in/London"
```

### 周预报

```bash
curl "wttr.in/London?format=v2"
```

### 指定日期（0=今天，1=明天，2=后天）

```bash
curl "wttr.in/London?1"
```

## 格式选项

### 一行摘要

```bash
curl "wttr.in/London?format=%l:+%c+%t+%w"
```

### JSON 输出

```bash
curl "wttr.in/London?format=j1"
```

### PNG 图片

```bash
curl "wttr.in/London.png"
```

## 格式代码

| 代码 | 含义 |
|------|------|
| %c | 天气状况表情 |
| %t | 温度 |
| %f | 体感温度 |
| %w | 风速 |
| %h | 湿度 |
| %p | 降水 |
| %l | 地点 |

## 快速响应示例

### "天气怎么样？"

```bash
curl -s "wttr.in/London?format=%l:+%c+%t+(feels+like+%f),+%w+wind,+%h+humidity"
```

### "会下雨吗？"

```bash
curl -s "wttr.in/London?format=%l:+%c+%p"
```

### "周末天气预报"

```bash
curl "wttr.in/London?format=v2"
```

## 注意事项

- 无需 API key
- 有请求频率限制
- 支持全球大多数城市
- 支持机场代码：`curl wttr.in/ORD`

## 相关技能

- [网页搜索](../miaoda-web-search/)
