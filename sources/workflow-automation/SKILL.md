---
name: workflow-automation
description: Automate complex multi-step tasks by orchestrating workflows, scheduling periodic jobs, and connecting multiple tools into automation chains. No API required — runs locally.
date: 2026-04-17
source: sickn33/antigravity-awesome-skills@workflow-automation
installs: 810
allowed-tools:
  - Bash
  - Read
  - Write
---

SKILL.md

# Workflow Automation Skill

> **Source:** sickn33/antigravity-awesome-skills  
> **Installs:** 810+ | **API Required:** ❌ No | **License:** MIT

## When to Use

✅ **Use this skill when:**

- User wants to automate repetitive multi-step tasks
- Need to schedule periodic or trigger-based jobs
- Connecting multiple tools/scripts into automation pipelines
- Batch processing files across different applications
- "Every morning at 9am do X"
- "When file A changes, automatically do B, C, and D"

❌ **Do NOT use this skill when:**

- Simple one-step task (just do it directly)
- Requires complex decision trees (use a dedicated orchestrator)
- Real-time streaming (use event-driven architecture instead)

## Core Concepts

### Workflow Types

| Type | Trigger | Example |
|------|---------|---------|
| **Scheduled** | Cron/time-based | Daily report at 9am |
| **Event-driven** | File/watch trigger | New file → process it |
| **Chain** | Manual trigger | Task A → B → C → D |
| **Conditional** | If/else logic | If X then Y else Z |

### Workflow Components

```
┌─────────────────────────────────────────────────────┐
│                    WORKFLOW                          │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐         │
│  │ TRIGGER │───▶│ ACTION  │───▶│ ACTION  │───▶ DONE│
│  └─────────┘    └─────────┘    └─────────┘         │
│       │              │              │              │
│  ┌────▼────┐    ┌────▼────┐    ┌────▼────┐         │
│  │CONDITION│    │NOTIFY  │    │ROLLBACK │         │
│  └─────────┘    └─────────┘    └─────────┘         │
└─────────────────────────────────────────────────────┘
```

## Quick Start

### 1. Define a Simple Workflow

```yaml
# .workflows/daily-report.yaml
name: daily-report
trigger:
  type: schedule
  cron: "0 9 * * *"  # Every day at 9am

steps:
  - name: collect-data
    action: run
    command: python scripts/collect_metrics.py

  - name: generate-report
    action: run
    command: python scripts/generate_report.py
    depends_on: collect-data

  - name: send-email
    action: notify
    channel: email
    depends_on: generate-report
```

### 2. Run the Workflow

```bash
# Run a workflow file
workflow-cli run .workflows/daily-report.yaml

# List all workflows
workflow-cli list

# Check status
workflow-cli status daily-report
```

## Workflow Templates

### Template 1: File Processing Pipeline

```yaml
name: file-processor
watch: ~/Downloads/*.pdf
steps:
  - action: read-metadata
  - action: classify
  - action: move
    dest: "~/Documents/{category}/{date}/"
  - action: log
```

### Template 2: Notification Chain

```yaml
name: alert-chain
trigger:
  type: webhook
  port: 8080

steps:
  - action: validate-input
  - action: process-data
  - action: notify-slack
  - action: notify-email
  - action: log-to-db
```

### Template 3: Scheduled Backup

```yaml
name: scheduled-backup
trigger:
  type: schedule
  cron: "0 2 * * *"  # 2am daily

steps:
  - action: backup-files
    source: ~/projects/
    dest: ~/backups/projects-{date}.zip
  - action: backup-db
    command: pg_dump mydb | gzip > backup.sql.gz
  - action: verify-backup
  - action: cleanup-old
    keep: 7  # Keep last 7 backups
```

## Reference: Available Actions

| Action | Description | Parameters |
|--------|-------------|------------|
| `run` | Execute shell command | `command`, `timeout`, `env` |
| `notify` | Send notification | `channel`, `message`, `template` |
| `move` | Move/copy files | `source`, `dest`, `overwrite` |
| `read-metadata` | Extract file metadata | `file`, `fields` |
| `classify` | Categorize content | `input`, `rules` |
| `log` | Log to file/DB | `message`, `level`, `destination` |
| `validate` | Validate input | `schema`, `data` |
| `transform` | Transform data | `input`, `template` |
| `http` | Make HTTP request | `url`, `method`, `headers`, `body` |
| `email` | Send email | `to`, `subject`, `body`, `attachments` |

## Advanced: Conditional Logic

```yaml
name: conditional-workflow
steps:
  - name: check-size
    action: run
    command: stat -f%z {file}
    register: file_size

  - name: large-file
    if: "{file_size} > 10000000"
    steps:
      - action: compress
      - action: notify
        message: "Large file compressed"

  - name: small-file
    if: "{file_size} <= 10000000"
    steps:
      - action: direct-upload
```

## Scripts Reference

### `scripts/scheduler.sh` — Cron Job Manager

```bash
#!/bin/bash
# Add a workflow to cron
./scheduler.sh add daily-report "0 9 * * *" ./run-workflow.sh daily-report

# List scheduled jobs
./scheduler.sh list

# Remove a job
./scheduler.sh remove daily-report
```

### `scripts/watcher.sh` — File Watch Daemon

```bash
#!/bin/bash
# Watch a directory for changes
./watcher.sh start --path ~/Downloads --pattern "*.pdf"

# Watch with filter
./watcher.sh start --path ~/Projects --pattern "*.js" --ignore "node_modules"
```

## Configuration

```yaml
# workflow-config.yaml
global:
  timeout: 3600          # Max workflow runtime (seconds)
  retry: 3               # Retry failed steps
  retry_delay: 60         # Delay between retries
  log_level: info         # debug|info|warn|error
  notification:
    default_channel: slack
    on_failure: always
    on_success: never

paths:
  workflows: .workflows/
  scripts: scripts/
  logs: logs/
  temp: /tmp/workflows/

environments:
  dev:
    dry_run: true
  prod:
    dry_run: false
    require_approval: true
```

## Error Handling & Retry

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
      fallback: "echo 'API unavailable, using cache'"
```

## Logging & Monitoring

```bash
# View workflow execution logs
workflow-cli logs daily-report --follow

# View in JSON format for monitoring
workflow-cli logs daily-report --format json

# Metrics endpoint (for Prometheus/Grafana)
workflow-cli metrics --port 9090
```

## Example: Complete Daily Automation

```yaml
# .workflows/daily-office-workflow.yaml
name: daily-office-workflow
description: Morning routine - check schedule, backup files, generate report

trigger:
  type: schedule
  cron: "0 8 * * 1-5"  # Weekdays at 8am

steps:
  - name: check-calendar
    action: run
    command: alma calendar events --today --json
    register: calendar_events

  - name: backup-yesterday
    action: run
    command: |
      tar -czf ~/backups/work-$(date -v-1d +%Y%m%d).tar.gz \
        ~/Documents/projects/
    on_failure: log-warn

  - name: generate-daily-brief
    action: run
    command: |
      echo "Today's Schedule:" && \
      echo "{calendar_events}" && \
      echo "Backups completed."

  - name: send-to-feishu
    action: notify
    channel: feishu
    message: "☀️ Morning brief ready"
```

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Workflow never starts | Cron syntax wrong | Use `crontab.guru` to validate |
| Step hangs | Command timeout | Increase `timeout` in config |
| Notifications not sent | Channel misconfigured | Check `workflow-config.yaml` |
| File watcher misses events | Debounce too fast | Adjust `debounce_ms` setting |

## Integration with Other Skills

- **scheduler** (Alma built-in) → Combine for smart scheduling
- **self_improving_agent** → Log failures for continuous improvement
- **feishu** → Send workflow notifications
- **file-manager** → Pre/post workflow file operations

## See Also

- [Alma Scheduler Skill](sources/alma-bundled/scheduler/) — Periodic task scheduling
- [File Organizer Skill](sources/file-organizer/) — Intelligent file processing
- [API Integration Specialist](sources/api-integration-specialist/) — Connect external services
