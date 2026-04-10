---
title: 自我改进代理
excerpt: 将学习成果和错误记录到 markdown 文件中以实现持续改进。编码代理稍后可以将这些处理成修复方案，重要的学习内容会被提升到项目内存中。
date: 2026-04-09
---

SKILL.md
Self-Improvement Skill

将学习成果和错误记录到 markdown 文件中以实现持续改进。编码代理稍后可以将这些处理成修复方案，重要的学习内容会被提升到项目内存中。

快速参考
情况	操作
命令/操作失败	记录到 .learnings/ERRORS.md
用户纠正你	使用类别 correction 记录到 .learnings/LEARNINGS.md
用户需要缺失的功能	记录到 .learnings/FEATURE_REQUESTS.md
API/外部工具失败	使用集成详细信息记录到 .learnings/ERRORS.md
知识已过时	使用类别 knowledge_gap 记录到 .learnings/LEARNINGS.md
找到更好的方法	使用类别 best_practice 记录到 .learnings/LEARNINGS.md
简化/强化重复模式	使用来源：simplify-and-harden 和稳定的 Pattern-Key 更新/记录到 .learnings/LEARNINGS.md
与现有条目相似	使用 **See Also** 链接，考虑提升优先级
广泛适用的学习内容	提升到 CLAUDE.md、AGENTS.md 和/或 .github/copilot-instructions.md
工作流改进	提升到 AGENTS.md（OpenClaw 工作区）
工具注意事项	提升到 TOOLS.md（OpenClaw 工作区）
行为模式	提升到 SOUL.md（OpenClaw 工作区）

OpenClaw 设置（推荐）

OpenClaw 是此技能的主要平台。它使用基于工作区的提示注入和自动技能加载。

安装

通过 ClawdHub（推荐）：

clawdhub install self-improving-agent

手动安装：

git clone https://github.com/peterskoett/self-improving-agent.git ~/.openclaw/skills/self-improving-agent

为 openclaw 重制自原始仓库：https://github.com/pskoett/pskoett-ai-skills - https://github.com/pskoett/pskoett-ai-skills/tree/main/skills/self-improvement

工作区结构

OpenClaw 将这些文件注入每个会话：

~/.openclaw/workspace/
├── AGENTS.md          # 多代理工作流、委托模式
├── SOUL.md            # 行为准则、个性、原则
├── TOOLS.md           # 工具能力、集成注意事项
├── MEMORY.md          # 长期内存（仅主会话）
├── memory/            # 每日内存文件
│   └── YYYY-MM-DD.md
└── .learnings/        # 此技能的日志文件
    ├── LEARNINGS.md
    ├── ERRORS.md
    └── FEATURE_REQUESTS.md

创建学习文件

mkdir -p ~/.openclaw/workspace/.learnings

然后创建日志文件（或从 assets/ 复制）：

    LEARNINGS.md — 纠正、知识差距、最佳实践
    ERRORS.md — 命令失败、异常
    FEATURE_REQUESTS.md — 用户请求的功能

提升目标

当学习成果被证明具有广泛适用性时，将其提升到工作区文件：
学习类型	提升到	示例
行为模式	SOUL.md	"保持简洁，避免免责声明"
工作流改进	AGENTS.md	"为长任务生成子代理"
工具注意事项	TOOLS.md	"Git push 需要先配置认证"
会话间通信

OpenClaw 提供跨会话共享学习成果的工具：

    sessions_list — 查看活动/最近的会话
    sessions_history — 读取另一个会话的记录
    sessions_send — 向另一个会话发送学习内容
    sessions_spawn — 生成子代理进行后台工作

可选：启用钩子

对于会话开始时自动提醒：

# 将钩子复制到 OpenClaw 钩子目录
cp -r hooks/openclaw ~/.openclaw/hooks/self-improvement

# 启用它
openclaw hooks enable self-improvement

有关完整详情，请参阅 references/openclaw-integration.md。

通用设置（其他代理）

对于 Claude Code、Codex、Copilot 或其他代理，在项目中创建 .learnings/：

mkdir -p .learnings

从 assets/ 复制模板或创建带有标题的文件。
在代理文件 AGENTS.md、CLAUDE.md 或 .github/copilot-instructions.md 中添加参考以提醒自己记录学习成果。（这是基于钩子提醒的替代方案）

自我改进工作流

当发生错误或纠正时：

    记录到 .learnings/ERRORS.md、LEARNINGS.md 或 FEATURE_REQUESTS.md
    审查并将广泛适用的学习成果提升到：
        CLAUDE.md - 项目事实和约定
        AGENTS.md - 工作流和自动化
        .github/copilot-instructions.md - Copilot 上下文

日志格式
学习条目

追加到 .learnings/LEARNINGS.md：

## [LRN-YYYYMMDD-XXX] 类别

**记录时间**：ISO-8601 时间戳
**优先级**：低 | 中 | 高 | 关键
**状态**：待处理
**领域**：前端 | 后端 | 基础设施 | 测试 | 文档 | 配置

### 摘要
所学内容的单行描述

### 详情
完整上下文：发生了什么、什么是错误的、正确的是什么

### 建议操作
具体修复或改进

### 元数据
- 来源：对话 | 错误 | 用户反馈
- 相关文件：path/to/file.ext
- 标签：tag1, tag2
- 另请参阅：LRN-20250110-001（如果与现有条目相关）
- Pattern-Key：simplify.dead_code | harden.input_validation（可选，用于重复模式跟踪）
- Recurrence-Count：1（可选）
- First-Seen：2025-01-15（可选）
- Last-Seen：2025-01-15（可选）

---

错误条目

追加到 .learnings/ERRORS.md：

## [ERR-YYYYMMDD-XXX] skill_or_command_name

**记录时间**：ISO-8601 时间戳
**优先级**：高
**状态**：待处理
**领域**：前端 | 后端 | 基础设施 | 测试 | 文档 | 配置

### 摘要
失败的简要描述

### 错误

实际错误消息或输出

### 上下文
- 尝试的命令/操作
- 使用的输入或参数
- 相关环境详情

### 建议修复
如果可以识别，可能解决此问题的方法

### 元数据
- 可重现：是 | 否 | 未知
- 相关文件：path/to/file.ext
- 另请参阅：ERR-20250110-001（如果重复）

---

功能请求条目

追加到 .learnings/FEATURE_REQUESTS.md：

## [FEAT-YYYYMMDD-XXX] capability_name

**记录时间**：ISO-8601 时间戳
**优先级**：中
**状态**：待处理
**领域**：前端 | 后端 | 基础设施 | 测试 | 文档 | 配置

### 请求的功能
用户想要做什么

### 用户上下文
为什么需要它，他们要解决什么问题

### 复杂度估计
简单 | 中等 | 复杂

### 建议实现方式
如何构建，可以扩展什么

### 元数据
- 频率：首次 | 重复
- 相关功能：existing_feature_name

---

ID 生成

格式：TYPE-YYYYMMDD-XXX

    TYPE：LRN（学习）、ERR（错误）、FEAT（功能）
    YYYYMMDD：当前日期
    XXX：序列号或随机 3 个字符（例如 001、A7B）

示例：LRN-20250115-001、ERR-20250115-A3F、FEAT-20250115-002

解决条目

当问题被修复时，更新条目：

    将 **状态**：待处理 → **状态**：已解决
    在元数据后添加解决块：

### 解决
- **解决时间**：2025-01-16T09:00:00Z
- **提交/PR**：abc123 或 #42
- **备注**：所做工作的简要描述

其他状态值：

    进行中 - 正在积极处理
    不修复 - 决定不处理（在解决备注中添加原因）
    已提升 - 提升到 CLAUDE.md、AGENTS.md 或 .github/copilot-instructions.md

提升到项目内存

当学习内容具有广泛适用性（不是一次性修复）时，将其提升到永久项目内存。

何时提升

    学习内容适用于多个文件/功能
    任何贡献者（人类或 AI）都应该知道的知识
    防止重复犯错
    记录项目特定的约定

提升目标
目标	属于那里内容
CLAUDE.md	所有 Claude 交互的项目事实、约定、注意事项
AGENTS.md	代理特定的工作流、工具使用模式、自动化规则
.github/copilot-instructions.md	GitHub Copilot 的项目上下文和约定
SOUL.md	行为准则、沟通风格、原则（OpenClaw 工作区）
TOOLS.md	工具能力、使用模式、集成注意事项（OpenClaw 工作区）

如何提升

    将学习内容提炼成简洁的规则或事实
    添加到目标文件的适当部分（如需要则创建文件）
    更新原始条目：
        将 **状态**：待处理 → **状态**：已提升
        添加 **已提升到**：CLAUDE.md、AGENTS.md 或 .github/copilot-instructions.md

提升示例

学习内容（详细）：

    项目使用 pnpm workspaces。尝试 npm install 但失败。锁文件是 pnpm-lock.yaml。必须使用 pnpm install。

在 CLAUDE.md 中（简洁）：

## 构建与依赖
- 包管理器：pnpm（不是 npm）- 使用 `pnpm install`

学习内容（详细）：

    修改 API 端点时，必须重新生成 TypeScript 客户端。忘记这一点会导致运行时类型不匹配。

在 AGENTS.md 中（可操作）：

## API 更改后
1. 重新生成客户端：`pnpm run generate:api`
2. 检查类型错误：`pnpm tsc --noEmit`

重复模式检测

如果记录的内容与现有条目相似：

    首先搜索：grep -r "keyword" .learnings/
    链接条目：在元数据中添加 **另请参阅**：ERR-20250110-001
    如果问题持续出现则提升优先级
    考虑系统性修复：重复问题通常表示：
        缺少文档（→ 提升到 CLAUDE.md 或 .github/copilot-instructions.md）
        缺少自动化（→ 添加到 AGENTS.md）
        架构问题（→ 创建技术债务工单）

简化和强化提要

使用此工作流从 simplify-and-harden 技能中获取重复模式，并将其转化为持久的提示指导。

摄取工作流

    从任务摘要中读取 simplify_and_harden.learning_loop.candidates
    对于每个候选项，使用 pattern_key 作为稳定的去重键
    在 .learnings/LEARNINGS.md 中搜索具有该键的现有条目：
        grep -n "Pattern-Key: <pattern_key>" .learnings/LEARNINGS.md
    如果找到：
        增加 Recurrence-Count
        更新 Last-Seen
        添加相关条目/任务的另请参阅链接
    如果未找到：
        创建新的 LRN-... 条目
        设置来源：simplify-and-harden
        设置 Pattern-Key、Recurrence-Count: 1 和 First-Seen/Last-Seen

提升规则（系统提示反馈）

当以下条件全部满足时，将重复模式提升到代理上下文/系统提示文件：

    Recurrence-Count >= 3
    跨至少 2 个不同任务看到
    在 30 天窗口内发生

提升目标：

    CLAUDE.md
    AGENTS.md
    .github/copilot-instructions.md
    SOUL.md / TOOLS.md（适用于 OpenClaw 工作区级指导）

将提升的规则编写为简短的预防规则（在编码之前/期间做什么），而不是长的事故报告。

定期审查

在自然断点处审查 .learnings/：

何时审查

    开始新的主要任务之前
    完成一个功能之后
    在有过去学习内容的领域工作时
    活跃开发期间每周

快速状态检查

# 统计待处理项目数
grep -h "Status**：待处理" .learnings/*.md | wc -l

# 列出待处理的高优先级项目
grep -B5 "Priority**：高" .learnings/*.md | grep "^## \["

# 查找特定领域的学习内容
grep -l "Area**：后端" .learnings/*.md

审查操作

    解决已修复的项目
    提升适用的学习内容
    链接相关条目
    升级重复问题

检测触发器

当你注意到以下情况时自动记录：

纠正（→ 类别为 correction 的学习）：

    "不，那不对..."
    "实际上，应该是..."
    "你关于...是错的"
    "那个已经过时了..."

功能请求（→ 功能请求）：

    "你也可以..."
    "我希望你能..."
    "有办法...吗"
    "为什么你不能..."

知识差距（→ 类别为 knowledge_gap 的学习）：

    用户提供了你不知道的信息
    你参考的文档已过时
    API 行为与你的理解不同

错误（→ 错误条目）：

    命令返回非零退出码
    异常或堆栈跟踪
    意外输出或行为
    超时或连接失败

优先级指南
优先级	何时使用
关键	阻塞核心功能、数据丢失风险、安全问题
高	重大影响、影响常见工作流、重复问题
中	中等影响、存在变通方案
低	轻微不便、边缘情况、可有可无

领域标签

用于按代码库区域过滤学习内容：
领域	范围
前端	UI、组件、客户端代码
后端	API、服务、服务器端代码
基础设施	CI/CD、部署、Docker、云
测试	测试文件、测试工具、覆盖率
文档	文档、注释、README
配置	配置文件、环境、设置

最佳实践

    立即记录 - 上下文在问题发生后最清晰
    要具体 - 未来的代理需要快速理解
    包括重现步骤 - 特别是对于错误
    链接相关文件 - 使修复更容易
    建议具体修复 - 而不仅仅是"调查"
    使用一致的类别 - 便于过滤
    积极提升 - 如果有疑问，添加到 CLAUDE.md 或 .github/copilot-instructions.md
    定期审查 - 过时的学习内容会失去价值

Gitignore 选项

保留学习内容在本地（按开发者）：

.learnings/

在仓库中跟踪学习内容（团队范围）：不要添加到 .gitignore - 学习内容成为共享知识。

混合（跟踪模板，忽略条目）：

.learnings/*.md
!.learnings/.gitkeep

钩子集成

通过代理钩子启用自动提醒。这是可选的 - 你必须明确配置钩子。

快速设置（Claude Code / Codex）

在项目中创建 .claude/settings.json：

{
  "hooks": {
    "UserPromptSubmit": [{
      "matcher": "",
      "hooks": [{
        "type": "command",
        "command": "./skills/self-improvement/scripts/activator.sh"
      }]
    }]
  }
}

这在每个提示之后注入学习评估提醒（约 50-100 token 开销）。

完整设置（带错误检测）

{
  "hooks": {
    "UserPromptSubmit": [{
      "matcher": "",
      "hooks": [{
        "type": "command",
        "command": "./skills/self-improvement/scripts/activator.sh"
      }]
    }],
    "PostToolUse": [{
      "matcher": "Bash",
      "hooks": [{
        "type": "command",
        "command": "./skills/self-improvement/scripts/error-detector.sh"
      }]
    }]
  }
}

可用的钩子脚本
脚本	钩子类型	目的
scripts/activator.sh	UserPromptSubmit	任务后提醒评估学习内容
scripts/error-detector.sh	PostToolUse (Bash)	命令错误时触发

有关详细配置和故障排除，请参阅 references/hooks-setup.md。

自动技能提取

当学习内容足够有价值可以成为可重用技能时，使用提供的辅助工具进行提取。

技能提取标准

当满足以下任何条件时，学习内容符合技能提取条件：
标准	描述
重复	有 2+ 个相似问题的另请参阅链接
已验证	状态为已解决并有有效的修复
非显而易见	需要实际调试/调查才能发现
广泛适用	不是特定于项目的；跨代码库有用
用户标记	用户说"保存为技能"或类似的话

提取工作流

    识别候选项：学习内容符合提取条件
    运行辅助工具（或手动创建）：

    ./skills/self-improvement/scripts/extract-skill.sh skill-name --dry-run
    ./skills/self-improvement/scripts/extract-skill.sh skill-name

    自定义 SKILL.md：用学习内容填充模板
    更新学习内容：将状态设置为 promoted_to_skill，添加 Skill-Path
    验证：在新会话中阅读技能以确保它是独立的

手动提取

如果你更喜欢手动创建：

    创建 skills/<skill-name>/SKILL.md
    使用 assets/SKILL-TEMPLATE.md 中的模板
    遵循代理技能规范：
        带 name 和 description 的 YAML 前页脚
        名称必须与文件夹名称匹配
        技能文件夹内没有 README.md

提取检测触发器

注意以下表示学习内容应该成为技能的信号：

在对话中：

    "保存为技能"
    "我一直在遇到这个问题"
    "这对其他项目也有用"
    "记住这个模式"

在学习条目中：

    多个另请参阅链接（重复问题）
    高优先级 + 已解决状态
    类别：best_practice 具有广泛适用性
    用户反馈赞扬解决方案

技能质量门

提取前，验证：

    解决方案经过测试并有效
    描述清晰，无需原始上下文
    代码示例是独立的
    没有特定于项目的硬编码值
    遵循技能命名约定（小写、连字符）

多代理支持

此技能可跨不同的 AI 编码代理工作，具有特定于代理的激活。

Claude Code

激活：钩子（UserPromptSubmit、PostToolUse）设置：带有钩子配置的 .claude/settings.json 检测：通过钩子脚本自动检测

Codex CLI

激活：钩子（与 Claude Code 相同的模式）设置：带有钩子配置的 .codex/settings.json 检测：通过钩子脚本自动检测

GitHub Copilot

激活：手动（无钩子支持）设置：添加到 .github/copilot-instructions.md：

## 自我改进

解决非显而易见的问题后，考虑记录到 `.learnings/`：
1. 使用自我改进技能格式
2. 使用另请参阅链接相关条目
3. 将高价值学习内容提升为技能

在聊天中询问："我应该将其记录为学习内容吗？"

检测：会话结束时的手动审查

OpenClaw

激活：工作区注入 + 代理间消息设置：见上面的"OpenClaw 设置"部分检测：通过会话工具和工作区文件

与代理无关的指导

无论使用何种代理，当你发现以下情况时应用自我改进：

    发现非显而易见的东西 - 解决方案不是立即的
    纠正自己 - 最初的方法是错误的
    学习项目约定 - 发现未记录的模式
    遇到意外错误 - 特别是诊断困难的情况下
    找到更好的方法 - 改进了原始解决方案

Copilot Chat 集成

对于 Copilot 用户，在相关时将此添加到提示中：

    完成此任务后，评估是否有任何学习内容应该使用自我改进技能格式记录到 .learnings/。

或使用快速提示：

    "将此记录到学习内容"
    "从中创建技能"
    "检查 .learnings/ 中的相关问题"
