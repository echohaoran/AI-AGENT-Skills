---
name: video-frames
title: 视频帧提取
excerpt: 使用 ffmpeg 从视频中提取帧或创建缩略图
date: 2026-04-20
来源: 飞书机器人技能库
授权工具: [ffmpeg]
---

# 视频帧提取

> **来源：** 飞书机器人技能库  
> **API 依赖：** 是（需要 ffmpeg） | **协议：** MIT

## 何时使用

✅ **使用此技能的场景：**

- 需要从视频中提取单帧
- 需要创建视频缩略图
- 需要分析视频特定时间点的内容
- 用户提到"提取视频帧"、"视频截图"

❌ **不要使用的场景：**

- 需要处理大量视频帧
- 需要视频格式转换（使用 ffmpeg 本身）
- 需要提取音频

## 核心命令

### 提取第一帧

```bash
{baseDir}/scripts/frame.sh /path/to/video.mp4 --out /tmp/frame.jpg
```

### 提取指定时间帧

```bash
{baseDir}/scripts/frame.sh /path/to/video.mp4 --time 00:00:10 --out /tmp/frame-10s.jpg
```

## 参数说明

| 参数 | 说明 |
|------|------|
| --time | 时间戳，用于"这个时间点发生了什么" |
| --out | 输出路径 |

## 格式选择

| 格式 | 用途 |
|------|------|
| .jpg | 快速分享 |
| .png | 清晰 UI 帧 |

## 使用场景

| 场景 | 用法 |
|------|------|
| 分析视频内容 | 指定 --time 提取关键帧 |
| 创建缩略图 | 不指定时间提取首帧 |
| 查看某时刻 | 指定具体时间点 |

## 相关技能

- [图片理解](../miaoda-image-understanding/)
- [语音转文字](../miaoda-speech-to-text/)
