SKILL.md
Find Skills Skill

从各种来源搜索和发现 OpenClaw 技能。

何时使用

✅ 使用此技能的场景：

    "查找用于 [任务] 的技能"
    "搜索 OpenClaw 技能"
    "有哪些可用的技能？"
    "发现新技能"
    "按类别查找技能"

何时不使用

❌ 不要使用此技能的场景：

    安装技能 → 使用 clawhub install
    管理已安装的技能 → 使用 openclaw skills list
    创建新技能 → 使用 skill-creator 技能

查找技能的资源
1. ClawHub（主要来源）

# 搜索技能
npx clawhub search "keyword"

# 浏览类别
npx clawhub browse

2. OpenClaw 目录

    网站：https://www.openclawdirectory.dev/skills
    按类别、人气或搜索浏览

3. LobeHub 技能市场

    网站：https://lobehub.com/skills
    社区贡献的技能

4. GitHub

    搜索：openclaw skill 或 agent-skill
    查找包含 SKILL.md 文件的仓库

5. 社区论坛

    SitePoint：https://www.sitepoint.com/community/
    Discord：https://discord.com/invite/clawd

搜索策略
按功能搜索

# 网络搜索技能
npx clawhub search "web search"

# 天气技能
npx clawhub search "weather"

# 文档技能
npx clawhub search "document"

按提供商搜索

# Tavily 技能
npx clawhub search "tavily"

# GitHub 技能
npx clawhub search "github"

# 日历技能
npx clawhub search "calendar"

按人气搜索

# 安装最多的技能
npx clawhub search --sort installs

# 星标最多的技能
npx clawhub search --sort stars

安装提示

    安装前检查系统要求
    阅读 SKILL.md 了解使用说明
    在隔离环境中测试后再用于生产
    定期检查更新

常见技能类别
核心技能

    weather - 天气预报
    skill-creator - 创建新技能
    healthcheck - 安全审计

集成技能

    github - GitHub 操作
    feishu - 飞书集成
    notion - Notion API

搜索技能

    tavily-search - 通过 Tavily 进行网络搜索
    web-search-plus - 增强型网络搜索

代理技能

    proactive-agent - 主动自动化
    coding-agent - 代码生成

故障排除
速率限制

如果遇到 clawhub 速率限制：

    重试前等待 1 小时
    使用替代来源（网站）
    在 GitHub 上手动搜索

安装问题

    检查技能系统要求
    验证网络连接
    检查 OpenClaw 版本兼容性

最佳实践

    创建前先搜索 - 不要重复造轮子
    阅读文档 - 了解技能能力
    从简单开始 - 一次安装一个技能
    彻底测试 - 验证技能是否按预期工作
    提供反馈 - 帮助改进技能

相关技能

    clawhub - ClawHub CLI 工具
    skill-creator - 创建新技能
    healthcheck - 系统健康检查
