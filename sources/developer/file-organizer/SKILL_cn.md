---
name: file-organizer
title: 文件整理器
excerpt: 智能整理、分类和管理计算机上的文件。支持批量重命名、重复文件检测、智能分类、自动归档。无需 API — 纯本地处理。
date: 2026-04-17
来源: sickn33/antigravity-awesome-skills@file-organizer
安装量: 582+
授权工具:
  - Bash
  - Read
  - Write
---

# 文件整理器技能

> **来源：** sickn33/antigravity-awesome-skills@file-organizer  
> **安装量：** 582+ | **API 依赖：** ❌ 无 | **协议：** MIT

## 何时使用

✅ **使用此技能的场景：**

- 用户想要整理杂乱的下载或文档文件夹
- 需要按命名规范批量重命名文件
- 查找并删除重复文件
- 按类型/日期/大小自动分类文件
- 自动归档旧文件
- "我有 500 张照片需要重命名"
- "清理我的下载文件夹"

❌ **不要使用的场景：**

- 不应移动的系统文件
- 其他应用程序正在打开的文件
- 加密或受权限保护的文件

## 核心功能

```infographic
infographic sequence-steps-simple
data
  title 文件整理五步法
  items
    - label 扫描
      desc 遍历目录，建立文件索引
    - label 分类
      desc 按类型/日期/大小智能分组
    - label 分析
      desc 检测重复，计算统计信息
    - label 执行
      desc 移动/重命名/归档操作
    - label 验证
      desc 确认操作结果，生成报告
```

## 快速开始

### 整理文件夹

```bash
# 按文件类型基本整理
file-organizer organize ~/下载/

# 按日期整理 (YYYY/MM/)
file-organizer organize ~/下载/ --by date

# 按类型和大小整理
file-organizer organize ~/下载/ --by type --min-size 10MB

# 预览模式（不实际移动文件）
file-organizer organize ~/下载/ --dry-run
```

### 查找重复文件

```bash
# 按内容哈希查找重复
file-organizer find-duplicates ~/文档/

# 查找大于 1MB 的重复
file-organizer find-duplicates ~/图片/ --min-size 1M

# 自动删除（保留最新）
file-organizer find-duplicates ~/下载/ --auto-remove
```

### 批量重命名

```bash
# 按日期重命名照片
file-organizer rename ~/照片/*.jpg \
  --template "{日期}_照片_{序号:04d}"

# 带前缀和序号的批量重命名
file-organizer rename *.pdf \
  --template "文档_{序号:03d}_{原名}"

# 查找替换文件名
file-organizer rename ~/文档/ \
  --replace "旧名称" "新名称" \
  --pattern "*.txt"
```

## 内置分类

| 类别 | 扩展名 | 示例 |
|------|--------|------|
| **图片** | jpg, jpeg, png, gif, webp, svg | 照片、截图 |
| **文档** | pdf, doc, docx, txt, rtf | 报告、笔记 |
| **表格** | xls, xlsx, csv, numbers | 数据、表格 |
| **视频** | mp4, mkv, mov, avi | 录像、剪辑 |
| **音频** | mp3, wav, flac, aac | 音乐、播客 |
| **归档** | zip, rar, 7z, tar, gz | 压缩文件 |
| **代码** | py, js, ts, java, cpp | 源代码 |
| **安装包** | app, dmg, exe, deb | 安装程序 |

## 相关技能

- [Alma 文件管理器技能](../alma-bundled/file-manager/) — 文件搜索和管理
- [Alma 截图技能](../alma-bundled/screenshot/) — 截图整理
- [工作流自动化](../workflow-automation/) — 自动清理工作流
