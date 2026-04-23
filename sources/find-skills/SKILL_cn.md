---
name: find-skills
title: 查找技能
excerpt: 在开放技能市场中搜索和安装 Agent 技能
date: 2026-04-20
来源: 飞书机器人技能库
授权工具: [命令行工具]
---

# 查找技能

> **来源：** 飞书机器人技能库  
> **API 依赖：** 是（Skills CLI） | **协议：** MIT

## 何时使用

✅ **使用此技能的场景：**

- 用户问"有没有能做XX的技能"
- 用户问"怎么实现XX功能"
- 用户想扩展 Agent 能力
- 用户想搜索工具、模板或工作流
- 用户提到"找技能"、"安装技能"

❌ **不要使用的场景：**

- 用户已经有明确需求要直接执行
- 已有现成工具可用

## 核心命令

### 搜索技能

```bash
npx skills find [关键词]
```

### 安装技能

```bash
npx skills add <owner/repo@skill> -g -y
```

### 检查更新

```bash
npx skills check
npx skills update
```

## 使用流程

1. **理解需求**：确定用户的领域、具体任务
2. **先查排行榜**：访问 https://skills.sh/ 查看热门技能
3. **搜索技能**：`npx skills find [关键词]`
4. **验证质量**：
   - 安装数（优先 1K+）
   - 来源信誉（官方 > 不知名）
   - GitHub stars
5. **呈现选项**：技能名、功能、安装数、安装命令
6. **安装技能**：如用户同意

## 常见技能分类

| 分类 | 示例关键词 |
|------|-----------|
| Web 开发 | react, nextjs, typescript |
| 测试 | testing, jest, playwright |
| DevOps | deploy, docker, kubernetes |
| 文档 | docs, readme, changelog |
| 代码质量 | review, lint, refactor |
| 设计 | ui, ux, design-system |

## 热门来源

- `vercel-labs/agent-skills` — React, Next.js
- `anthropics/skills` — 前端设计、文档处理
- `microsoft/skills` — 各类工具

## 相关技能

- [技能市场](../miaoda-skillhub/)
- [技能创建](../skill-creator/)
