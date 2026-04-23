---
name: skill-creator
title: 技能创建
excerpt: 创建、编辑、改进或审核 Agent Skills
date: 2026-04-20
来源: 飞书机器人技能库
授权工具: [命令行工具, init_skill.py, package_skill.py]
---

# 技能创建

> **来源：** 飞书机器人技能库  
> **API 依赖：** 是 | **协议：** MIT

## 何时使用

✅ **使用此技能的场景：**

- 需要从零创建新技能
- 需要改进现有技能
- 需要审核、整理技能文件
- 用户提到"创建技能"、"制作技能"、"改进技能"

❌ **不要使用的场景：**

- 只需要使用现有技能
- 非技能开发相关需求

## 核心原则

### 简洁为王

- 上下文窗口是公共资源
- 只添加模型确实需要的内容
- 简洁示例优于冗长解释

### 适当自由度

| 自由度 | 适用场景 |
|--------|----------|
| 高（文本指令） | 多种方案有效、需上下文判断 |
| 中（伪代码/脚本） | 有偏好模式、可接受变化 |
| 低（具体脚本） | 操作脆弱、需要一致性 |

## 技能结构

```
skill-name/
├── SKILL.md (必需)
│   ├── YAML frontmatter (name + description)
│   └── Markdown 说明
└── 资源文件 (可选)
    ├── scripts/      # 可执行脚本
    ├── references/   # 参考文档
    └── assets/       # 资源文件
```

## 创建流程

### 1. 理解需求

通过具体示例理解技能用途

### 2. 规划内容

分析需要哪些脚本、参考文档、资源文件

### 3. 初始化技能

```bash
scripts/init_skill.py <skill-name> --path <输出目录> [--resources scripts,references,assets]
```

### 4. 编辑技能

- 编写 SKILL.md（frontmatter + 说明）
- 添加资源文件
- 测试脚本

### 5. 打包技能

```bash
scripts/package_skill.py <path/to/skill-folder>
```

打包会自动验证：
- YAML frontmatter 格式
- 命名规范和目录结构
- 描述完整性和质量

## Frontmatter 格式

```yaml
---
name: skill-name
description: |
  技能描述（触发词 + 功能说明）
---
```

## 渐进式披露设计

保持 SKILL.md 精简（<500 行），详细信息放到 references/ 目录：

```
skill-name/
├── SKILL.md
└── references/
    ├── patterns.md    # 模式参考
    └── examples.md    # 示例参考
```

## 相关技能

- [查找技能](../find-skills/)
- [技能市场](../miaoda-skillhub/)
