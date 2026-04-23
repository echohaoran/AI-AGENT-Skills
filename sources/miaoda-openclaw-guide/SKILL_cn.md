---
name: miaoda-openclaw-guide
title: OpenClaw 运行时指南
excerpt: OpenClaw Agent 运行环境说明、沙箱安全配置、可用技能和工具限制
date: 2026-04-20
来源: 飞书机器人技能库
授权工具: [无]
---

# OpenClaw 运行时指南

> **来源：** 飞书机器人技能库  
> **API 依赖：** 否 | **协议：** MIT

## 何时使用

✅ **使用此技能的场景：**

- 需要了解运行环境约束
- 遇到"没有权限"、"无法安装"、"sudo"问题
- 需要了解可用技能和工具
- 用户提到"环境限制"、"安全配置"

❌ **不要使用的场景：**

- 正常功能使用场景

## 运行环境约束

| 约束 | 说明 | 替代方案 |
|------|------|----------|
| 无 sudo/root | 沙箱安全策略 | npm/pip 用户级安装 |
| 无固定公网 IP | 平台限制 | 后续平台提供 |
| 无法安装系统服务 | 无 root 权限 | 用户级安装或脚本替代 |
| Chrome Browser Relay 不可用 | 无法连接本地 Chrome | miaoda-web-fetch + browser 工具 |
| Browser Replay 不可用 | 环境限制 | 使用 browser 工具 |

## 内置技能速查

| 技能 | 命令 | 注意 |
|------|------|------|
| 网页搜索 | miaoda-studio-cli search-summary | 替代原生 web_search |
| 网页抓取 | miaoda-studio-cli web-crawl | 替代原生 web_fetch |
| 文档解析 | miaoda-studio-cli doc-parse | |
| 图片理解 | miaoda-studio-cli image-understanding | 无需浏览器 |
| 语音转文字 | miaoda-studio-cli speech-to-text | |
| 文生图 | miaoda-studio-cli text-to-image | |

## 常见请求路由

```
用户请求分类
├─ 看图/分析截图 → miaoda-image-understanding
├─ 搜索 → miaoda-web-search
├─ 抓取网页 → miaoda-web-fetch
├─ 网页交互 → browser 工具
├─ 安装软件 → npm/pip 用户级安装
├─ 没有 sudo → 说明限制，引导用户级安装
└─ 配置问题 → 引导通过妙搭平台操作
```

## 禁止事项

- 尝试 sudo 或提权
- 修改 `.agents/skills/` 下内置 skill
- 修改 `openclaw.json` 的 secrets.providers
- 执行交互式 CLI 命令
- 尝试连接 Chrome Browser Relay

## Workspace 文件说明

| 文件 | 用途 |
|------|------|
| IDENTITY.md | Agent 身份与人格 |
| SOUL.md | 核心价值观与行为准则 |
| AGENTS.md | 角色与能力声明 |
| TOOLS.md | 工具使用指南 |

## 相关技能

- [节点连接诊断](../node-connect/)
- [主机安全加固](../healthcheck/)
