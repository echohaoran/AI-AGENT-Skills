# AI Agent 技能仓库 / AI Agent Skills

> 精选 AI Agent 技能合集 | 支持 Alma Desktop AI

[English](README.md) | [中文](README_cn.md)

---

## 📦 技能包总览

| 技能包 | 路径 | 技能数 | 描述 |
|--------|------|--------|------|
| **productivity/** | [📂 查看](sources/productivity/README_cn.md) | 7 项 | 办公效率套件（Office、WPS、PPT、图表、PDF、Excel） |
| **developer/** | [📂 查看](sources/developer/README_cn.md) | 8 项 | 开发者工具（Docker、Git、MySQL、代码审查、API） |
| **ai-tools/** | [📂 查看](sources/ai-tools/README_cn.md) | 4 项 | AI 智能工具（浏览器自动化、技能搜索、安全审查） |
| **privacy-security/** | [📂 查看](sources/privacy-security/README_cn.md) | 2 项 | 隐私安全（隐私脱敏、MCP 审计） |
| **web-tools/** | [📂 查看](sources/web-tools/README_cn.md) | 3 项 | 网页工具（百度搜索、天气、OCR） |
| **feishu-miaoda/** | [📂 查看](sources/feishu-miaoda/README_cn.md) | 27 项 | 飞书妙搭技能包（文档、多维表格、日历、任务等） |
| **alma-bundled/** | [📂 查看](sources/alma-bundled/README_cn.md) | 30 项 | Alma 内置技能包（系统内置功能） |
| **feishu/** | [📂 查看](sources/feishu/SKILL_cn.md) | 1 项 | 飞书基础集成 |

---

## 📊 技能总数统计

| 分类 | 数量 |
|------|------|
| 办公效率套件 (productivity) | 7 |
| 开发者工具 (developer) | 8 |
| AI 智能工具 (ai-tools) | 4 |
| 隐私安全 (privacy-security) | 2 |
| 网页工具 (web-tools) | 3 |
| 飞书妙搭技能包 (feishu-miaoda) | 27 |
| Alma 内置技能包 (alma-bundled) | 30 |
| 飞书基础集成 (feishu) | 1 |
| **总计** | **~82** 项 |

---

## 📁 目录结构

```
sources/
├── productivity/          # 📊 办公效率套件 (7项)
│   ├── office/           # Microsoft 365, Google Workspace
│   ├── wps/             # WPS Office 中文办公
│   ├── marp/            # Markdown PPT 演示
│   ├── mermaid/         # SVG 图表生成器
│   ├── pdf-generator/   # PDF 程序化生成
│   ├── document-xlsx/    # Excel 读写生成
│   └── Nano_Pdf/         # PDF 编辑
│
├── developer/            # 🛠️ 开发者工具 (8项)
│   ├── docker/           # Docker 容器化
│   ├── git-workflow/     # Git 工作流
│   ├── mysql/            # MySQL 数据库
│   ├── code-review-quality/ # 代码审查
│   ├── markdown-documentation/ # Markdown 文档
│   ├── api-integration-specialist/ # API 集成
│   ├── workflow-automation/ # 工作流自动化
│   └── file-organizer/   # 文件智能整理
│
├── ai-tools/             # 🤖 AI 智能工具 (4项)
│   ├── Agent_Browser/    # 浏览器自动化
│   ├── Find_Skills_Skill/ # 技能搜索
│   ├── Skill_Vetter/     # 安全审查
│   └── self_improving_agent/ # 自我改进
│
├── privacy-security/     # 🔒 隐私安全 (2项)
│   ├── awesome-privacy-skill/ # 隐私脱敏
│   └── mcp-security-audit/    # MCP 审计
│
├── web-tools/            # 🌐 网页工具 (3项)
│   ├── baidu_search/     # 百度搜索
│   ├── weather/          # 天气查询
│   └── local-ocr/        # 本地 OCR
│
├── feishu-miaoda/       # 📱 飞书妙搭 (27项)
│   ├── feishu-bitable/      # 多维表格
│   ├── feishu-calendar/     # 日历管理
│   ├── feishu-create-doc/   # 创建文档
│   ├── feishu-fetch-doc/    # 读取文档
│   ├── feishu-im-read/      # 消息读取
│   ├── feishu-task/        # 任务管理
│   ├── miaoda-coding/       # 代码开发
│   ├── miaoda-database/     # 数据库
│   ├── miaoda-doc-parse/    # 文档解析
│   ├── miaoda-image-understanding/ # 图片理解
│   ├── miaoda-speech-to-text/ # 语音转文字
│   ├── miaoda-text-gen-image/  # 文生图
│   ├── miaoda-web-fetch/    # 网页抓取
│   ├── miaoda-web-search/   # 网页搜索
│   ├── taobao-shop-price/   # 全网比价
│   ├── video-frames/        # 视频帧提取
│   └── ...
│
├── alma-bundled/        # 🔧 Alma 内置 (30项)
│   ├── browser/          # 浏览器自动化
│   ├── screenshot/      # 屏幕截图
│   ├── system-info/     # 系统信息
│   ├── memory-management/ # 记忆管理
│   ├── voice/           # 语音生成
│   ├── telegram/        # Telegram 机器人
│   ├── discord/         # Discord 集成
│   └── ...
│
└── feishu/              # 📱 飞书基础集成
```

---

## 🔗 相关链接

- **Gitee 仓库**：https://gitee.com/echohaoran/ai-agent-skills
- **Alma 官网**：https://almachat.com

---

## 更新日志

| 日期 | 内容 |
|------|------|
| 2026-04-20 | 新增子目录结构（productivity、developer、ai-tools、privacy-security、web-tools） |
| 2026-04-20 | 新增飞书妙搭技能包（27 项） |
| 2026-04-17 | 新增 10 项无 API 技能（workflow-automation、docker、mysql 等） |
| 2026-04-17 | 新增 alma-bundled 技能包（30 项） |

---

*更新时间：2026-04-20*
