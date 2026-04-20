---
name: api-integration-specialist
title: API 集成专家技能
excerpt: 集成任何 REST API — 处理认证（OAuth/API Key/Bearer）、实现重试逻辑、管理 Webhook 回调。本技能本身不调用外部 API。
date: 2026-04-17
来源: davila7/claude-code-templates@api-integration-specialist
安装量: 441+
授权工具:
  - Bash
  - Read
  - Write
---

# API 集成专家技能

> **来源：** davila7/claude-code-templates@api-integration-specialist  
> **安装量：** 441+ | **API 依赖：** ❌ 无（您提供自己的 API）| **协议：** MIT

## 何时使用

✅ **使用此技能的场景：**

- 用户需要集成 REST API
- 实现 OAuth 流程或 API Key 认证
- 构建 Webhook 处理器
- "调用 GitHub API"
- "集成 Stripe 支付"

## 认证模式

### API Key

```bash
# Header 认证
curl -H "X-API-Key: YOUR_API_KEY" https://api.example.com/data

# 查询参数
curl "https://api.example.com/data?api_key=YOUR_API_KEY"
```

### Bearer Token

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" https://api.example.com/user
```

## 重试逻辑

```bash
#!/bin/bash
# 指数退避重试
retry_request() {
  local url="$1"
  local max_attempts=3
  local delay=1
  
  for i in $(seq 1 $max_attempts); do
    response=$(curl -s -w "\n%{http_code}" "$url")
    code=$(echo "$response" | tail -1)
    
    if [ "$code" -eq 200 ]; then
      echo "$response" | head -n -1
      return 0
    fi
    
    if [ $i -lt $max_attempts ]; then
      echo "第 $i 次失败，${delay}s 后重试..." >&2
      sleep $delay
      delay=$((delay * 2))
    fi
  done
  
  echo "❌ 所有 $max_attempts 次尝试均失败" >&2
  return 1
}
```

## 相关技能

- [工作流自动化](../workflow-automation/) — API 调用链
- [飞书技能](../feishu/) — 通过飞书发送通知
- [天气技能](../weather/) — 调用天气 API
