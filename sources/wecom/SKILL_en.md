---
title: wecom
excerpt: A skill for integrating WeCom (Enterprise WeChat) with OpenClaw AI Agent, enabling message sending and receiving, encryption, token management, and access control.
date: 2026-04-09
---

# OpenClaw WeCom Channel Plugin

WeCom (Enterprise WeChat/WxWork) channel plugin that lets an OpenClaw AI Agent send and receive messages via WeCom, alongside Telegram, Discord, Signal, etc.

## Features

- Receive messages — Users send text in WeCom, the Agent replies automatically
- Proactive push — Agent sends messages via WeCom APIs
- Message encryption — Full AES‑256‑CBC (WXBizMsgCrypt) encrypt/decrypt
- Token management — access_token caching with early refresh
- Access control — open / pairing / allowlist strategies
- Smart reply — respond within 5s, degrade to proactive push if timeout

## Prerequisites

- OpenClaw installed and running
- WeCom admin privileges (create a custom app)
- Publicly reachable callback URL (Cloudflare Tunnel recommended)

## Quick Start

### 1) Install the plugin
```bash
git clone https://github.com/darrryZ/openclaw-wecom-channel.git ~/.openclaw/extensions/wecom
```

### 2) Configure OpenClaw
Edit `~/.openclaw/openclaw.json`:
```json
{
  "channels": {
    "wecom": {
      "enabled": true,
      "corpId": "your_corp_id",
      "agentId": 1000003,
      "secret": "app_secret",
      "token": "callback_token",
      "encodingAESKey": "callback_encoding_aes_key",
      "port": 18800,
      "dmPolicy": "open"
    }
  },
  "plugins": {
    "entries": { "wecom": { "enabled": true } }
  }
}
```

### 3) Expose callback via Cloudflare Tunnel
```bash
cloudflared tunnel create wecom-tunnel
cloudflared tunnel route dns wecom-tunnel wecom.yourdomain.com
cloudflared tunnel run --edge-ip-version 4 --url http://localhost:18800 wecom-tunnel
```
Set the WeCom callback URL to: `https://wecom.yourdomain.com/wecom/callback`

### 4) Restart gateway
```bash
openclaw gateway restart
```

## Links

- GitHub: https://github.com/darrryZ/openclaw-wecom-channel
- OpenClaw: https://github.com/openclaw/openclaw
- WeCom Developer Docs: https://developer.work.weixin.qq.com/document/
