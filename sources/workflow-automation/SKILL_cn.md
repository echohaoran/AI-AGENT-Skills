---
name: workflow-automation
title: 工作流自动化
excerpt: 将复杂多步骤任务编排为自动化工作流，支持定时调度、文件监听、跨工具联动，无需 API 即可本地运行。
date: 2026-04-17
来源: sickn33/antigravity-awesome-skills@workflow-automation
安装量: 810+
授权工具:
  - Bash
  - Read
  - Write
---

# 工作流自动化技能

> **来源：** sickn33/antigravity-awesome-skills  
> **安装量：** 810+ | **API 依赖：** ❌ 无 | **协议：** MIT

## 何时使用

✅ **使用此技能的场景：**

- 用户希望自动化重复性多步骤任务
- 需要定时调度或触发式任务
- 将多个工具/脚本连接为自动化流水线
- 批量处理跨应用文件
- "每天早上 9 点自动执行 X"
- "当文件 A 变化时，自动执行 B、C、D"

❌ **不要使用的场景：**

- 简单的单步任务（直接执行即可）
- 需要复杂决策树（使用专用编排器）
- 实时流处理（使用事件驱动架构）

## 核心概念

### 工作流类型

| 类型 | 触发方式 | 示例 |
|------|---------|------|
| **定时调度** | Cron/时间驱动 | 每天 9 点生成报告 |
| **事件驱动** | 文件/监听触发 | 新文件 → 自动处理 |
| **链条式** | 手动触发 | 任务 A → B → C → D |
| **条件分支** | If/else 逻辑 | 满足条件则执行 |

### 工作流组件

```
┌─────────────────────────────────────────────────────┐
│                    WORKFLOW                          │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐         │
│  │ 触发器  │───▶│ 动作 A  │───▶│ 动作 B  │───▶ 完成 │
│  └─────────┘    └─────────┘    └─────────┘         │
│       │              │              │                 │
│  ┌────▼────┐    ┌────▼────┐    ┌────▼────┐         │
│  │ 条件判断│    │ 通知提醒│    │ 回滚机制│         │
│  └─────────┘    └─────────┘    └─────────┘         │
└─────────────────────────────────────────────────────┘
```

## 快速开始

### 1. 定义简单工作流

```yaml
# .workflows/daily-report.yaml
name: daily-report
trigger:
  type: schedule
  cron: "0 9 * * *"  # 每天早上9点

steps:
  - name: collect-data
    action: run
    command: python scripts/收集数据.py

  - name: generate-report
    action: run
    command: python scripts/生成报告.py
    depends_on: collect-data

  - name: send-email
    action: notify
    channel: email
    depends_on: generate-report
```

### 2. 运行工作流

```bash
# 运行工作流文件
workflow-cli run .workflows/daily-report.yaml

# 列出所有工作流
workflow-cli list

# 查看状态
workflow-cli status daily-report
```

## 工作流模板

### 模板一：文件处理流水线

```yaml
name: 文件处理流水线
watch: ~/下载/*.pdf
steps:
  - action: 读取元数据
  - action: 分类
  - action: 移动
    dest: "~/文档/{分类}/{日期}/"
  - action: 记录日志
```

### 模板二：通知链

```yaml
name: 告警通知链
trigger:
  type: webhook
  port: 8080

steps:
  - action: 验证输入
  - action: 处理数据
  - action: 飞书通知
  - action: 邮件通知
  - action: 写入数据库
```

### 模板三：定时备份

```yaml
name: 定时备份
trigger:
  type: schedule
  cron: "0 2 * * *"  # 每天凌晨2点

steps:
  - action: 备份文件
    source: ~/项目/
    dest: ~/备份/项目-{日期}.zip
  - action: 备份数据库
    command: pg_dump mydb | gzip > 备份.sql.gz
  - action: 验证备份
  - action: 清理旧文件
    keep: 7  # 保留最近7个备份
```

## 参考：可用动作

| 动作 | 描述 | 参数 |
|------|------|------|
| `run` | 执行 shell 命令 | `command`, `timeout`, `env` |
| `notify` | 发送通知 | `channel`, `message`, `template` |
| `move` | 移动/复制文件 | `source`, `dest`, `overwrite` |
| `read-metadata` | 提取文件元数据 | `file`, `fields` |
| `classify` | 内容分类 | `input`, `rules` |
| `log` | 记录日志 | `message`, `level`, `destination` |
| `validate` | 验证输入 | `schema`, `data` |
| `transform` | 数据转换 | `input`, `template` |
| `http` | 发起 HTTP 请求 | `url`, `method`, `headers`, `body` |
| `email` | 发送邮件 | `to`, `subject`, `body`, `attachments` |

## 高级：条件逻辑

```yaml
name: 条件工作流
steps:
  - name: 检查大小
    action: run
    command: stat -f%z {file}
    register: file_size

  - name: 大文件处理
    if: "{file_size} > 10000000"  # > 10MB
    steps:
      - action: 压缩
      - action: 通知
        message: "大文件已压缩"

  - name: 小文件处理
    if: "{file_size} <= 10000000"
    steps:
      - action: 直接上传
```

## 脚本参考

### `scripts/scheduler.sh` — Cron 任务管理器

```bash
#!/bin/bash
# 添加工作流到 cron
./scheduler.sh add daily-report "0 9 * * *" ./run-workflow.sh daily-report

# 列出已调度任务
./scheduler.sh list

# 移除任务
./scheduler.sh remove daily-report
```

### `scripts/watcher.sh` — 文件监听守护进程

```bash
#!/bin/bash
# 监听目录变化
./watcher.sh start --path ~/下载 --pattern "*.pdf"

# 带过滤器监听
./watcher.sh start --path ~/项目 --pattern "*.js" --ignore "node_modules"
```

## 配置

```yaml
# workflow-config.yaml
global:
  timeout: 3600          # 最大运行时长（秒）
  retry: 3               # 失败重试次数
  retry_delay: 60        # 重试间隔
  log_level: info        # debug|info|warn|error
  notification:
    default_channel: feishu
    on_failure: always
    on_success: never

paths:
  workflows: .workflows/
  scripts: scripts/
  logs: logs/
  temp: /tmp/workflows/
```

## 错误处理与重试

```yaml
steps:
  - name: unreliable-api
    action: http
    url: https://api.example.com/data
    retry:
      max_attempts: 3
      backoff: exponential
      initial_delay: 1
      max_delay: 30
    on_failure:
      action: use-cache
      fallback: "echo 'API不可用，使用缓存'"
```

## 日志与监控

```bash
# 查看工作流执行日志
workflow-cli logs daily-report --follow

# JSON 格式输出（用于监控）
workflow-cli logs daily-report --format json

# 指标端点（Prometheus/Grafana）
workflow-cli metrics --port 9090
```

## 完整示例：每日办公自动化

```yaml
# .workflows/每日办公工作流.yaml
name: daily-office-workflow
description: 早晨例程 - 检查日程、备份文件、生成简报

trigger:
  type: schedule
  cron: "0 8 * * 1-5"  # 工作日早上8点

steps:
  - name: 检查日程
    action: run
    command: alma calendar events --today --json
    register: calendar_events

  - name: 备份昨日文件
    action: run
    command: |
      tar -czf ~/backups/work-$(date -v-1d +%Y%m%d).tar.gz \
        ~/Documents/projects/
    on_failure: log-warn

  - name: 生成每日简报
    action: run
    command: |
      echo "今日日程:" && \
      echo "{calendar_events}" && \
      echo "备份已完成。"

  - name: 发送飞书通知
    action: notify
    channel: feishu
    message: "☀️ 早间简报已就绪"
```

## 故障排除

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| 工作流不启动 | Cron 语法错误 | 使用 crontab.guru 验证 |
| 步骤卡住 | 命令超时 | 增加 config 中的 `timeout` |
| 通知未发送 | 通道配置错误 | 检查 `workflow-config.yaml` |
| 文件监听漏报 | 防抖太快 | 调整 `debounce_ms` 设置 |

## 与其他技能协同

- **scheduler**（Alma 内置）→ 智能调度组合
- **self_improving_agent** → 记录失败日志持续改进
- **feishu** → 发送工作流通知
- **file-manager** → 工作流前后文件操作

## 相关技能

- [Alma Scheduler 技能](../alma-bundled/scheduler/) — 周期性任务调度
- [文件整理器技能](../file-organizer/) — 智能文件处理
- [API 集成专家](../api-integration-specialist/) — 连接外部服务
