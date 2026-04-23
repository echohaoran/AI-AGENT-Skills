---
name: miaoda-skillhub
title: 技能市场
excerpt: 搜索和安装火山引擎 Skillhub 技能
date: 2026-04-20
来源: 飞书机器人技能库
授权工具: [命令行工具]
---

# 技能市场

> **来源：** 飞书机器人技能库  
> **API 依赖：** 是 | **协议：** MIT

## 何时使用

✅ **使用此技能的场景：**

- 需要搜索技能
- 需要安装技能
- 需要管理已安装的技能
- 用户问"有没有XX技能"
- 用户提到"技能市场"、"技能安装"、"技能搜索"

❌ **不要使用的场景：**

- 已有现成工具可用
- 用户有明确需求要直接执行

## 核心能力

| 能力 | 说明 |
|------|------|
| Skills 广场 | GitHub 开源 Skills 国内镜像 + 二方 Skills |
| Skills 检索 | 自然语言模糊检索 |
| Skills 展示 | 元信息和 SKILL.md 内容 |
| Skills 安全 | 恶意 Skill 扫描与审核 |
| Skills 安装 | 支持 zip 下载、API & SDK |

## 门户地址

- **findskill.cn** | **findskill.com**

## CLI 命令

### 搜索技能

```bash
SKILLS_API_URL=https://skills.volces.com/v1 npx -y skills find <关键词>
```

### 安装技能

```bash
SKILLS_API_URL=https://skills.volces.com/v1 npx -y skills add <URL> -s <skill> -a openclaw -y --copy
```

## 使用决策

```
安装技能的方式？
├─ CLI（推荐）→ SKILLS_API_URL=npx -y skills find/add
├─ 门户 → 访问 findskill.cn
└─ 手动 → 放到 skills/<skill-name>/
```

## 多 Agent 场景

技能安装后：
- 所有 Agent 共用 → 保留在默认 skills/ 目录
- 仅特定 Agent → 移动到该 Agent 的 workspace 目录

```bash
cp -r skills/<skill-name> <agent-workspace>/skills/<skill-name>
```

## 相关技能

- [查找技能](../find-skills/)
- [技能创建](../skill-creator/)
