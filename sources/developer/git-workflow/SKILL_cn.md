---
name: git-workflow
title: Git 工作流技能
excerpt: 精通 Git 版本控制工作流 — 分支策略、提交规范、冲突解决、历史分析。无需 API — 兼容所有 Git 仓库。
date: 2026-04-17
来源: bobmatnyc/claude-mpm-skills@git-workflow
安装量: 348+
授权工具:
  - Bash
  - Read
---

# Git 工作流技能

> **来源：** bobmatnyc/claude-mpm-skills@git-workflow  
> **安装量：** 348+ | **API 依赖：** ❌ 无 | **协议：** MIT

## 何时使用

✅ **使用此技能的场景：**

- 用户需要 Git 分支策略指导
- 需要解决合并或变基冲突
- 编写规范的提交信息（Conventional Commits）
- 分析 Git 历史和 blame
- 创建或管理 Git 钩子

## 分支策略

### Git Flow

```
main ────●──────────────●────────────────── (生产版本)
         │              │
         └─●──●──●──●──┘                   (开发分支)
             │  │  │  │
             ●  ●  ●  ●                     (功能分支)
```

## Conventional Commits 规范

### 格式

```
<类型>(<范围>): <主题>

[可选正文]

[可选脚注]
```

### 类型

| 类型 | 用于 |
|------|------|
| `feat` | 新功能 |
| `fix` | 错误修复 |
| `docs` | 仅文档 |
| `style` | 格式调整，无代码变化 |
| `refactor` | 重构（不修复也不新增） |
| `perf` | 性能改进 |
| `test` | 添加测试 |
| `chore` | 维护任务 |

## 相关技能

- [代码审查质量](../code-review-quality/) — PR 自动检查
- [Skill Vetter](../Skill_Vetter/) — 技能版本控制
- [自我改进代理](../self_improving_agent/) — 追踪变化和学习
