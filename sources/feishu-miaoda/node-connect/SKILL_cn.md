---
name: node-connect
title: 节点连接诊断
excerpt: 诊断 OpenClaw 节点连接和配对失败问题
date: 2026-04-20
来源: 飞书机器人技能库
授权工具: [命令行工具]
---

# 节点连接诊断

> **来源：** 飞书机器人技能库  
> **API 依赖：** 是 | **协议：** MIT

## 何时使用

✅ **使用此技能的场景：**

- QR/设置码/手动连接失败
- 本地 Wi-Fi 可用但 VPS/tailnet 不可用
- 报错提示"pairing required"、"unauthorized"、"bootstrap token invalid"
- 涉及 gateway.bind、gateway.remote.url、Tailscale 配置问题
- 用户提到"连接失败"、"配对"、"节点"

❌ **不要使用的场景：**

- 正常功能使用
- 非 OpenClaw 相关问题

## 诊断流程

### 1. 确定拓扑类型

| 类型 | 说明 |
|------|------|
| 同机器/模拟器/USB | 同一设备 |
| 同局域网/Wi-Fi | 本地网络 |
| 同 Tailscale tailnet | Tailscale 网络 |
| 公网 URL/反向代理 | 远程访问 |

### 2. 收集信息

如果情况不明确，先问清楚：
- 打算用什么连接方式
- 用 QR 码还是手动输入
- 具体的错误信息

### 3. 运行诊断命令

```bash
openclaw config get gateway.mode
openclaw config get gateway.bind
openclaw config get gateway.tailscale.mode
openclaw config get gateway.remote.url
openclaw config get plugins.entries.device-pair.config.publicUrl
openclaw qr --json
openclaw devices list
openclaw nodes status
```

### 4. 解读 QR 结果

`openclaw qr --json` 返回：
- `gatewayUrl`：实际端点
- `urlSource`：配置来源

### 5. 常见问题

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| 循环地址 | 网关只绑定本地 | 改用 LAN/Tailnet/公网 |
| tailnet 无 IP | 主机未加入 Tailscale | 加入 Tailscale |
| pairing required | 需要批准配对 | openclaw devices approve --latest |
| token invalid | setup code 过期 | 生成新的 setup code |

## 相关技能

- [主机安全加固](../healthcheck/)
- [OpenClaw 运行时指南](../miaoda-openclaw-guide/)
