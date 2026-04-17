# Alma 内置技能库

> 来源：Alma Desktop AI 内置技能包（v2026.04）  
> 路径：`/Applications/Alma.app/Contents/Resources/bundled-skills/`  
> 状态：✅ 已归档至本地仓库

---

## 📦 技能目录（共 30 项）

| 技能名称 | 描述 |
|---------|------|
| [browser](browser/SKILL.md) | 🌐 浏览器自动化，支持 PinchTab 和 Chrome Relay 双引擎 |
| [discord](discord/SKILL.md) | 💬 Discord 机器人交互，发送消息/文件/图片/视频 |
| [file-manager](file-manager/SKILL.md) | 📁 文件管理，按名称/类型/大小搜索文件并整理 |
| [image-gen](image-gen/SKILL.md) | 🖼️ 图像生成，支持本地图像生成模型 |
| [memory-management](memory-management/SKILL.md) | 🧠 长期记忆管理，读取/写入/检索持久化记忆 |
| [music-gen](music-gen/SKILL.md) | 🎵 音乐生成，使用 Suno 生成音乐 |
| [music-listener](music-listener/SKILL.md) | 🎧 音乐播放和控制 |
| [notebook](notebook/SKILL.md) | 📓 多模态笔记系统，支持文本/图片/音频 |
| [plan-mode](plan-mode/SKILL.md) | 📋 计划模式，规划复杂任务和工作流程 |
| [reactions](reactions/SKILL.md) | 👍 消息反应管理 |
| [scheduler](scheduler/SKILL.md) | ⏰ 任务调度，周期性任务和提醒 |
| [screenshot](screenshot/SKILL.md) | 📸 macOS 屏幕截图 |
| [self-management](self-management/SKILL.md) | ⚙️ Alma 系统设置管理 |
| [self-reflection](self-reflection/SKILL.md) | 🔄 每日自我反思与成长记录 |
| [selfie](selfie/SKILL.md) | 📷 自拍照生成，保持一致的面容 |
| [send-file](send-file/SKILL.md) | 📤 发送文件到当前对话 |
| [skill-hub](skill-hub/SKILL.md) | 🛠️ 技能市场，从 skills.sh 搜索安装技能 |
| [skill-search](skill-search/SKILL.md) | 🔍 搜索安装新技能 |
| [system-info](system-info/SKILL.md) | 💻 macOS 系统信息 |
| [tasks](tasks/SKILL.md) | ✅ 结构化任务管理 |
| [telegram](telegram/SKILL.md) | 📱 Telegram Bot API 交互 |
| [thread-management](thread-management/SKILL.md) | 🧵 线程管理，创建/切换/删除对话 |
| [todo](todo/SKILL.md) | 📝 Markdown 任务清单管理 |
| [travel](travel/SKILL.md) | ✈️ 虚拟旅行系统 |
| [twitter-media](twitter-media/SKILL.md) | 🐦 Twitter/X 媒体提取 |
| [video-reader](video-reader/SKILL.md) | 🎬 视频/音频内容理解 |
| [voice](voice/SKILL.md) | 🔊 本地 Qwen3-TTS 语音生成（离线） |
| [web-fetch](web-fetch/SKILL.md) | 🌐 网页内容抓取 |
| [web-search](web-search/SKILL.md) | 🔎 Web 搜索（内置浏览器引擎） |
| [xiaohongshu-cli](xiaohongshu-cli/SKILL.md) | 📕 小红书 CLI 工具 |

---

## 🏷️ 技能分类速查

### 🌐 网络与浏览器
| 技能 | 功能 |
|------|------|
| **browser** | 浏览器自动化（PinchTab + Chrome Relay） |
| **web-search** | 实时网络搜索 |
| **web-fetch** | 网页内容抓取 |
| **discord** | Discord 消息交互 |
| **telegram** | Telegram Bot API |
| **twitter-media** | Twitter/X 媒体提取 |
| **xiaohongshu-cli** | 小红书全功能操作 |

### 🧠 记忆与认知
| 技能 | 功能 |
|------|------|
| **memory-management** | 长期记忆存取 |
| **self-reflection** | 每日反思成长 |
| **notebook** | 多模态笔记 |

### 📁 文件与任务
| 技能 | 功能 |
|------|------|
| **file-manager** | 文件搜索整理 |
| **tasks** | 结构化任务管理 |
| **todo** | Markdown 任务清单 |
| **scheduler** | 周期性任务调度 |

### 🎨 媒体生成
| 技能 | 功能 |
|------|------|
| **image-gen** | 本地图像生成 |
| **music-gen** | Suno 音乐生成 |
| **voice** | Qwen3-TTS 离线语音 |

### ⚙️ 系统与设置
| 技能 | 功能 |
|------|------|
| **self-management** | Alma 系统设置 |
| **system-info** | macOS 系统信息 |
| **screenshot** | 屏幕截图 |
| **thread-management** | 对话线程管理 |

### 🎯 特殊功能
| 技能 | 功能 |
|------|------|
| **travel** | 虚拟旅行探索 |
| **plan-mode** | 复杂任务规划 |
| **reactions** | 消息表情反应 |
| **send-file** | 文件发送 |

---

## 📊 技能状态

| 状态 | 数量 | 说明 |
|------|------|------|
| ✅ 已启用 | 30 | 主公系统全部内置技能 |
| 🔧 内置 | 30 | 来源：Alma Desktop AI |
| 🌐 网络依赖 | 10+ | 部分技能需联网 |
| 🔒 离线可用 | 15+ | 核心功能可离线运行 |

---

## 🔧 使用方式

```bash
# 在 Alma 对话中直接使用
/skill browser    # 激活浏览器自动化
/skill image-gen # 激活图像生成

# 或通过自然语言触发
"帮我截个屏"
"搜索最新的 AI 新闻"
"生成一张图片"
```

---

**归档时间：** 2026-04-17  
**版本：** Alma Desktop AI v2026.04
