---
name: miaoda-speech-to-text
title: 语音转文字
excerpt: 将音频文件转换为文字，支持多语言
date: 2026-04-20
来源: 飞书机器人技能库
授权工具: [miaoda-studio-cli]
---

# 语音转文字

> **来源：** 飞书机器人技能库  
> **API 依赖：** 是 | **协议：** MIT

## 何时使用

✅ **使用此技能的场景：**

- 需要将会议录音转为文字
- 需要转录语音记录
- 需要将音频内容提取为文本
- 用户提到"语音转文字"、"音频转文字"、"转录"、"录音转文字"

❌ **不要使用的场景：**

- 音频超过 10 分钟（需要拆分）
- 需要实时语音识别

## 核心命令

```bash
miaoda-studio-cli speech-to-text --file <音频文件路径>
```

**参数**：
- `--file`：音频文件路径（必需）
- `--lang`：语言代码（默认 zh）
- `--output, -o`：输出格式 text/json（默认 text）

## 支持语言

| 代码 | 语言 |
|------|------|
| zh | 中文（默认） |
| en | 英语 |
| ja | 日语 |
| ko | 韩语 |
| fr | 法语 |
| es | 西班牙语 |
| pt | 葡萄牙语 |
| ru | 俄语 |
| id | 印尼语 |
| ms | 马来语 |

## 使用示例

### 中文音频转文字

```bash
miaoda-studio-cli speech-to-text --file meeting.mp3
```

### 英文音频转文字

```bash
miaoda-studio-cli speech-to-text --file interview.wav --lang en
```

### 输出 JSON

```bash
miaoda-studio-cli speech-to-text --file recording.mp3 --lang zh --output json
```

## 使用场景

| 场景 | 用法 |
|------|------|
| 会议录音 | speech-to-text + search-summary 搜索关键内容 |
| 外语音频 | 指定对应语言代码 |

## 相关技能

- [网页搜索](../miaoda-web-search/)
- [文档解析](../miaoda-doc-parse/)
