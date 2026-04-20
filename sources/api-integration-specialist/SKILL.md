---
name: api-integration-specialist
description: Integrate with any REST API — handle authentication (OAuth/API Key/Bearer), implement retry logic, and manage webhook callbacks. No external API calls from this skill itself.
date: 2026-04-17
source: davila7/claude-code-templates@api-integration-specialist
installs: 441
allowed-tools:
  - Bash
  - Read
  - Write
---

SKILL.md

# API Integration Specialist Skill

> **Source:** davila7/claude-code-templates@api-integration-specialist  
> **Installs:** 441+ | **API Required:** ❌ No (you provide your own API) | **License:** MIT

## When to Use

✅ **Use this skill when:**

- User needs to integrate with a REST API
- Implementing OAuth flow or API key authentication
- Building webhook handlers
- "Call GitHub API"
- "Integrate with Stripe payment"
- "Set up webhook endpoint"

## Authentication Patterns

### API Key

```bash
# Header authentication
curl -H "X-API-Key: YOUR_API_KEY" https://api.example.com/data

# Query parameter
curl "https://api.example.com/data?api_key=YOUR_API_KEY"
```

### Bearer Token

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" https://api.example.com/user
```

### OAuth 2.0

```bash
# 1. Get authorization URL
echo "Visit: https://auth.example.com/oauth/authorize?client_id=ID&redirect_uri=URI&scope=read"

# 2. Exchange code for token
curl -X POST https://auth.example.com/oauth/token \
  -d "grant_type=authorization_code" \
  -d "code=AUTH_CODE" \
  -d "client_id=ID" \
  -d "client_secret=SECRET"
```

## Retry Logic

```bash
#!/bin/bash
# Retry with exponential backoff
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
      echo "Attempt $i failed, retrying in ${delay}s..." >&2
      sleep $delay
      delay=$((delay * 2))
    fi
  done
  
  echo "❌ All $max_attempts attempts failed" >&2
  return 1
}
```

## Webhook Handler

```bash
#!/bin/bash
# Simple webhook receiver
PAYLOAD=$(cat)
EVENT_TYPE="$HTTP_X_GITHUB_EVENT"
SIGNATURE="$HTTP_X_HUB_SIGNATURE_256"

# Verify signature
SECRET="your-webhook-secret"
EXPECTED=$(echo -n "sha256=${SECRET}" | openssl dgst -sha256 -hmac "$SECRET" -hex | cut -d' ' -f2)

if [ "$SIGNATURE" != "$EXPECTED" ]; then
  echo "❌ Invalid signature"
  exit 1
fi

# Process event
case "$EVENT_TYPE" in
  push)
    echo "📦 New push received"
    # Run deployment
    ;;
  pull_request)
    echo "🔀 PR event received"
    ;;
  *)
    echo "📬 Event: $EVENT_TYPE"
    ;;
esac

echo "✅ Webhook processed"
```

## Scripts Reference

### `scripts/api-client.sh`

```bash
#!/bin/bash
# Generic API client with auth and retry

API_BASE="${API_BASE_URL:-https://api.example.com}"
API_KEY="${MY_API_KEY}"

api_get() {
  local endpoint="$1"
  curl -s -H "Authorization: Bearer $API_KEY" \
       -H "Accept: application/json" \
       "$API_BASE$endpoint"
}

api_post() {
  local endpoint="$1"
  local data="$2"
  curl -s -X POST \
       -H "Authorization: Bearer $API_KEY" \
       -H "Content-Type: application/json" \
       -d "$data" \
       "$API_BASE$endpoint"
}
```

## Integration Examples

### GitHub API

```bash
# Get user info
curl -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/user

# Create issue
curl -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Bug found","body":"Description"}' \
  https://api.github.com/repos/user/repo/issues
```

## See Also

- [Workflow Automation](../workflow-automation/) — Chain API calls
- [Feishu Skill](../feishu/) — Send notifications via Feishu
- [Weather Skill](../weather/) — Call weather APIs
