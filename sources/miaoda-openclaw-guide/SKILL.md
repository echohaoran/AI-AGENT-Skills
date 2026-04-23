---
name: miaoda-openclaw-guide
description: "OpenClaw agent runtime guide: sandbox environment, security config, available skills, tool limitations, and common user request handling. 运行环境说明、沙箱安全配置、可用技能、工具限制、常见问题处理。触发词：环境限制, 没有权限, sudo, 无法安装, 安全配置, dangerouslyDisable, no-sandbox, Browser Relay, Browser Replay, 内置技能, 可用工具"
---

# OpenClaw Agent 运行时指南

本指南帮助 OpenClaw agent 了解自身运行环境的约束、可用能力和行为规范。

---

## 运行环境约束

你运行在沙箱环境中，以下限制属于预期行为，非 Bug：

| 约束 | 说明 | 用户问到时的回答 |
|------|------|-----------------|
| 无 sudo/root 权限 | 沙箱安全策略 | 可用 `npm install` / `pip install --user` 安装到用户目录 |
| 无固定公网 IP | 平台限制 | 暂不支持，后续平台会提供方案 |
| 无法安装系统级服务 | 无 root 权限 | 用 npm/pip 用户级安装，或 skill 脚本替代 |
| Chrome Browser Relay 不可用 | 无法连接用户本地 Chrome | 获取网页 → `miaoda-web-fetch`；交互操作 → 内置 `browser` 工具 |
| Browser Replay 不可用 | 环境限制，录制回放功能不支持 | 需要网页交互用内置 `browser` 工具 |
| 不要修改 `.agents/skills/` | 平台管理的内置 skill 目录 | 用户自定义 skill 放 `skills/` 目录 |

> 遇到用户反馈"没有权限"、"无法安装"、"sudo 不行"时，**说明限制原因并提供替代方案，不要尝试绕过**。

---

## 内置技能速查

以下技能可直接调用，原生 `web_search` / `web_fetch` 已被 override，统一使用 `miaoda-studio-cli`：

| 技能 | 功能 | 调用方式 | 注意 |
|------|------|----------|------|
| miaoda-web-search | 网页搜索 | `miaoda-studio-cli search-summary --query "..."` | 替代原生 web_search |
| miaoda-web-fetch | 网页抓取 | `miaoda-studio-cli web-crawl --url "..."` | 替代原生 web_fetch |
| miaoda-doc-parse | 文档解析 | `miaoda-studio-cli doc-parse --file <path>` | 支持 PDF/Word/Excel/PPT |
| miaoda-image-understanding | 图片理解 | `miaoda-studio-cli image-understanding -i <path>` | **无需浏览器**，直接分析本地图片 |
| miaoda-speech-to-text | 音频转文字 | `miaoda-studio-cli speech-to-text --audio <path>` | |
| miaoda-text-gen-image | 文生图 | `miaoda-studio-cli text-to-image --prompt "..."` | |

---

## 常见用户请求路由

```
用户请求分类
├─ "帮我看看这张图" / "分析截图"
│   → miaoda-image-understanding（无需浏览器）
├─ "帮我搜一下 xxx"
│   → miaoda-web-search
├─ "帮我打开这个网页" / "抓取网页内容"
│   → miaoda-web-fetch
├─ "帮我点击网页上的按钮" / 网页交互
│   → 内置 browser 工具
├─ "帮我安装 xxx"
│   → npm install / pip install --user（无 sudo）
├─ "Browser Relay 连不上" / "Browser Replay 不可用"
│   → 说明环境限制，引导替代方案
├─ "没有 sudo 密码" / "无法获取 root"
│   → 说明沙箱策略，引导用户级安装
├─ "费用/限额问题"
│   → 无法处理，引导联系平台管理员或反馈群
└─ "帮我改 openclaw 配置" / 运维类
    → 超出 OpenClaw agent 职责，建议用户通过妙搭平台操作
```

---

## 禁止事项

| 禁止 | 原因 |
|------|------|
| 尝试 `sudo` 或提权操作 | 沙箱策略，会失败 |
| 修改 `.agents/skills/` 下的内置 skill | 平台管理，会被覆盖 |
| 修改 `openclaw.json` 的 `secrets.providers` | 平台自动更新，手动修改会导致严重报错 |
| 执行交互式 CLI 命令（需要 stdin 输入的） | Agent 无法处理交互式 prompt，会卡死 |
| 尝试连接 Chrome Browser Relay | 环境限制，连不上 |
| 尝试使用 Browser Replay | 环境限制，录制回放不支持 |

---

## 沙箱安全配置说明

当前沙箱环境以下配置是合理的，**不要尝试"修复"或加固**：

| 配置 | 理由 |
|------|------|
| `dangerouslyDisableDeviceAuth: true` | 沙箱已有基础设施级访问控制，设备认证是冗余层 |
| `tools.profile: "full"` | 单一可信用户，不需要限制工具权限 |
| `tools.sessions.visibility: "all"` | 所有 session 都是自己的，无隔离需求 |
| 缺少 `tools.exec` / `tools.elevated` / `tools.fs` 限制 | 可信操作者模型下，这些限制反而影响使用体验 |
| `browser --no-sandbox` | 远程容器以 root 运行，容器本身是隔离层，`--no-sandbox` 是常规做法 |

---

## Workspace 文件说明

`workspace/` 下的 Bootstrap 文件定义了你的身份和行为边界：

| 文件 | 用途 |
|------|------|
| `IDENTITY.md` | Agent 身份与人格定义 |
| `SOUL.md` | 核心价值观与行为准则 |
| `AGENTS.md` | 角色与能力声明 |
| `TOOLS.md` | 工具使用指南 |
| `USER.md` | 用户偏好设置 |
| `HEARTBEAT.md` | 心跳检测配置 |

> 这些文件定义了你的行为边界，修改需谨慎。用户要求调整 Agent 行为时，编辑对应文件。

---

## 用户自定义 Skill

用户安装/开发的 Skill 统一放在 `skills/` 目录下：

```
skills/<skill-name>/
└── SKILL.md    # 必需
```

系统通过 glob `skills/**/SKILL.md` 自动发现，无需手动注册。

> 如需搜索或安装社区 Skill，参考 Skillhub 技能市场。
