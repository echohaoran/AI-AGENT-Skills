---
title: Agent 浏览器
excerpt: 使用 accessibility tree snapshots 和 refs 实现快速浏览器自动化，实现确定性元素选择。
date: 2026-04-09
---

SKILL.md
Agent Browser Skill

使用 accessibility tree snapshots 和 refs 实现快速浏览器自动化，实现确定性元素选择。

为什么使用这个而不是内置浏览器工具

适用场景：
    自动化多步骤工作流
    需要确定性元素选择
    性能要求高
    处理复杂的单页应用（SPA）
    需要会话隔离

适用内置浏览器工具的场景：
    需要截图/PDF 用于分析
    需要视觉检查
    需要浏览器扩展集成

核心工作流程

# 1. 导航并获取快照
agent-browser open https://example.com
agent-browser snapshot -i --json

# 2. 从 JSON 解析 refs，然后进行交互
agent-browser click @e2
agent-browser fill @e3 "text"

# 3. 页面变化后重新获取快照
agent-browser snapshot -i --json

核心命令
导航

agent-browser open <url>
agent-browser back | forward | reload | close

快照（始终使用 -i --json）

agent-browser snapshot -i --json          # 交互元素，JSON 输出
agent-browser snapshot -i -c -d 5 --json  # + 紧凑模式，深度限制
agent-browser snapshot -s "#main" -i      # 限定选择器范围

交互（基于 Ref）

agent-browser click @e2
agent-browser fill @e3 "text"
agent-browser type @e3 "text"
agent-browser hover @e4
agent-browser check @e5 | uncheck @e5
agent-browser select @e6 "value"
agent-browser press "Enter"
agent-browser scroll down 500
agent-browser drag @e7 @e8

获取信息

agent-browser get text @e1 --json
agent-browser get html @e2 --json
agent-browser get value @e3 --json
agent-browser get attr @e4 "href" --json
agent-browser get title --json
agent-browser get url --json
agent-browser get count ".item" --json

检查状态

agent-browser is visible @e2 --json
agent-browser is enabled @e3 --json
agent-browser is checked @e4 --json

等待

agent-browser wait @e2                    # 等待元素出现
agent-browser wait 1000                   # 等待毫秒
agent-browser wait --text "Welcome"       # 等待文本出现
agent-browser wait --url "**/dashboard"   # 等待 URL 匹配
agent-browser wait --load networkidle     # 等待网络空闲
agent-browser wait --fn "window.ready === true"

会话（隔离浏览器）

agent-browser --session admin open site.com
agent-browser --session user open site.com
agent-browser session list
# 或通过环境变量：AGENT_BROWSER_SESSION=admin agent-browser ...

状态持久化

agent-browser state save auth.json        # 保存 cookies/storage
agent-browser state load auth.json        # 加载（跳过登录）

截图与 PDF

agent-browser screenshot page.png
agent-browser screenshot --full page.png
agent-browser pdf page.pdf

网络控制

agent-browser network route "**/ads/*" --abort           # 屏蔽
agent-browser network route "**/api/*" --body '{"x":1}'  # 模拟
agent-browser network requests --filter api              # 查看

Cookies 与存储

agent-browser cookies                     # 获取所有
agent-browser cookies set name value
agent-browser storage local key           # 获取 localStorage
agent-browser storage local set key val

标签页与框架

agent-browser tab new https://example.com
agent-browser tab 2                       # 切换到标签页
agent-browser frame @e5                   # 切换到 iframe
agent-browser frame main                  # 返回主框架

快照输出格式

{
  "success": true,
  "data": {
    "snapshot": "...",
    "refs": {
      "e1": {"role": "heading", "name": "Example Domain"},
      "e2": {"role": "button", "name": "Submit"},
      "e3": {"role": "textbox", "name": "Email"}
    }
  }
}

最佳实践

    始终使用 -i 标志 - 聚焦于交互元素
    始终使用 --json - 更易于解析
    等待稳定 - agent-browser wait --load networkidle
    保存认证状态 - 使用 state save/load 跳过登录流程
    使用会话 - 隔离不同的浏览器上下文
    使用 --headed 进行调试 - 查看正在发生什么

示例：搜索并提取

agent-browser open https://www.google.com
agent-browser snapshot -i --json
# AI 识别搜索框 @e1
agent-browser fill @e1 "AI agents"
agent-browser press Enter
agent-browser wait --load networkidle
agent-browser snapshot -i --json
# AI 识别结果 refs
agent-browser get text @e3 --json
agent-browser get attr @e4 "href" --json

示例：多会话测试

# Admin 会话
agent-browser --session admin open app.com
agent-browser --session admin state load admin-auth.json
agent-browser --session admin snapshot -i --json

# User 会话（同时）
agent-browser --session user open app.com
agent-browser --session user state load user-auth.json
agent-browser --session user snapshot -i --json

安装

npm install -g agent-browser
agent-browser install                     # 下载 Chromium
agent-browser install --with-deps         # Linux: + 系统依赖
