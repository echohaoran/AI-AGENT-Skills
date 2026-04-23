# AI Agent 技能仓库 / AI Agent Skills

> 精选 AI Agent 技能合集 | 支持 Alma Desktop AI

[English](README.md) | [中文](README_cn.md)

---

## 📦 技能目录

| 技能 | 描述 |
|------|------|
| [office](sources/office/SKILL_cn.md) | Office 办公技能（Microsoft 365、Google Workspace） |
| [wps](sources/wps/SKILL_cn.md) | 面向中文办公场景的 WPS 技能 |
| [Nano_Pdf](sources/Nano_Pdf/SKILL_cn.md) | 使用自然语言指令编辑 PDF 特定页面 |
| [self_improving_agent](sources/self_improving_agent/SKILL_cn.md) | 学习成果和错误记录，持续改进 |
| [Find_Skills_Skill](sources/Find_Skills_Skill/SKILL_cn.md) | 搜索和发现 OpenClaw 技能 |
| [Agent_Browser](sources/Agent_Browser/SKILL_cn.md) | 浏览器自动化，快速元素选择 |
| [Skill_Vetter](sources/Skill_Vetter/SKILL_cn.md) | AI 代理技能安全审查协议 |
| [feishu](sources/feishu/SKILL_cn.md) | 飞书基础集成 |
| [baidu_search](sources/baidu_search/SKILL_cn.md) | 百度搜索引擎，中文互联网内容 |
| [awesome-privacy-skill](sources/awesome-privacy-skill/README.md) | 🔒 隐私脱敏，防止 LLM 泄露用户隐私 |
| [document-xlsx](sources/document-xlsx/frameworks/shared-skills/skills/document-xlsx/SKILL.md) | 📊 Excel 完整读写与生成，图表公式 |
| [marp](sources/marp/README.md) | 🎤 Markdown 编写 PPT，导出 PPTX/PDF/HTML |
| [mermaid](sources/mermaid/README.zh-CN.md) | 📈 SVG 图表生成器，31 种图表类型 |
| [pdf-generator](sources/pdf-generator/skills/general/document-processing/pdf/pdf-generator/SKILL.md) | 📄 PDF 程序化创建与模板填充 |
| [local-ocr](sources/local-ocr/SKILL_cn.md) | 🔍 本地 OCR 识图转文，离线可用 |
| [weather](sources/weather/SKILL.md) | ☔ 天气查询，无需 API 密钥 |
| [workflow-automation](sources/workflow-automation/SKILL_cn.md) | ⚙️ 工作流自动化，定时调度 |
| [docker](sources/docker/SKILL_cn.md) | 🐳 Docker 容器化，安全沙箱 |
| [file-organizer](sources/file-organizer/SKILL_cn.md) | 📁 文件智能整理，批量重命名 |
| [git-workflow](sources/git-workflow/SKILL_cn.md) | 🔀 Git 分支策略，提交规范 |
| [code-review-quality](sources/code-review-quality/SKILL_cn.md) | ✅ 自动化代码审查，风格检查 |
| [mysql](sources/mysql/SKILL_cn.md) | 🗄️ MySQL 数据库查询，数据导出 |
| [markdown-documentation](sources/markdown-documentation/SKILL_cn.md) | 📝 Markdown 文档，风格检查 |
| [mcp-security-audit](sources/mcp-security-audit/SKILL_cn.md) | 🔒 MCP 安全审计，权限分析 |
| [api-integration-specialist](sources/api-integration-specialist/SKILL_cn.md) | 🌐 REST API 集成，OAuth，重试逻辑 |
| [markitdown](sources/markitdown/SKILL_cn.md) | 📄 微软文档转 Markdown，支持 DOCX/Excel/PPTX/PDF/图片 OCR |

---

## 📦 技能包（打包合集）

| 技能包 | 路径 | 描述 |
|--------|------|------|
| **feishu-miaoda/** | [📂 查看](sources/feishu-miaoda/README_cn.md) | 🤖 飞书妙搭技能包（27 项） |
| **alma-bundled/** | [📂 查看](sources/alma-bundled/README_cn.md) | 🔧 Alma 内置技能包（30 项） |

---

## 📊 技能总数

| 分类 | 数量 |
|------|------|
| 独立技能 | 25 项 |
| 飞书妙搭技能包 | 27 项 |
| Alma 内置技能包 | 30 项 |
| **总计** | **~82 项** |

---

## 📁 目录结构

```
sources/
├── office/                  # Office 办公
├── wps/                    # WPS 办公
├── Nano_Pdf/              # PDF 编辑
├── self_improving_agent/  # 自我改进
├── Find_Skills_Skill/     # 技能搜索
├── Agent_Browser/         # 浏览器自动化
├── Skill_Vetter/          # 安全审查
├── feishu/                # 飞书基础
├── baidu_search/          # 百度搜索
├── weather/               # 天气查询
├── local-ocr/             # 本地 OCR
├── workflow-automation/   # 工作流自动化
├── docker/                # Docker 容器化
├── file-organizer/        # 文件整理
├── git-workflow/          # Git 工作流
├── code-review-quality/   # 代码审查
├── mysql/                 # MySQL 数据库
├── markdown-documentation/ # Markdown 文档
├── mcp-security-audit/   # MCP 安全审计
├── api-integration-specialist/ # API 集成
│
├── feishu-miaoda/         # 📦 飞书妙搭技能包（27项）
│   ├── feishu-bitable/
│   ├── feishu-calendar/
│   ├── feishu-create-doc/
│   ├── feishu-fetch-doc/
│   ├── feishu-im-read/
│   ├── feishu-task/
│   ├── feishu-troubleshoot/
│   ├── feishu-update-doc/
│   ├── miaoda-coding/
│   ├── miaoda-database-skill/
│   ├── miaoda-doc-parse/
│   ├── miaoda-image-understanding/
│   ├── miaoda-openclaw-guide/
│   ├── miaoda-skillhub/
│   ├── miaoda-speech-to-text/
│   ├── miaoda-text-gen-image/
│   ├── miaoda-web-fetch/
│   ├── miaoda-web-search/
│   ├── taobao-shop-price/
│   ├── video-frames/
│   └── ...
│
├── alma-bundled/          # 📦 Alma 内置技能包（30项）
│   ├── browser/
│   ├── screenshot/
│   ├── system-info/
│   ├── memory-management/
│   ├── voice/
│   ├── telegram/
│   ├── discord/
│   └── ...
│
├── awesome-privacy-skill/ # 隐私脱敏（独立仓库）
├── marp/                  # Markdown PPT（独立仓库）
├── mermaid/               # SVG 图表（独立仓库）
├── pdf-generator/         # PDF 生成（独立仓库）
└── document-xlsx/          # Excel（独立仓库）
```

---

## 🔗 相关链接

- **Gitee 仓库**：https://gitee.com/echohaoran/ai-agent-skills
- **Alma 官网**：https://almachat.com

---

## 更新日志

| 日期 | 内容 |
|------|------|
| 2026-04-20 | 整理目录结构，独立技能保持扁平，feishu/alma 打包为子目录 |
| 2026-04-20 | 新增飞书妙搭技能包（27 项） |
| 2026-04-17 | 新增 10 项无 API 技能 |
| 2026-04-17 | 新增 alma-bundled 技能包（30 项） |

---

*更新时间：2026-04-20*
