SKILL.md
企业微信 (WeCom) 集成

与企业微信（WeCom）集成，实现企业消息、CRM 自动化和工作流。

何时使用

✅ 使用此技能的场景：

    "发送企业微信消息"
    "自动化企业微信群消息"
    "连接企业微信到外部系统"
    "处理企业微信 webhooks"
    "管理企业微信联系人"

何时不使用

❌ 不要使用此技能的场景：

    需要个人微信集成（使用微信公众平台 API）
    高频实时消息（考虑原生 API）
    需要语音/视频通话（企业微信有内置功能）

快速开始

# 发送消息
wecom send --to "user-id" "你好，来自企业微信机器人的消息！"

# 发送群消息
wecom send --group "group-chat-id" "团队通知"

# 接收 webhooks
wecom webhook listen --port 3000

核心命令

消息发送

wecom send --to "user-id" "消息"
wecom send --party "party-id" "消息"
wecom send --tag "tag-id" "消息"

媒体消息

wecom send.image --to "user-id" --path "image.png"
wecom send.file --to "user-id" --path "document.pdf"
wecom send.markdown --to "user-id" --content "**粗体** 文本"

群组管理

wecom group create "项目团队"
wecom group add "group-id" --members @user1,@user2
wecom group remove "group-id" --members @user3

联系人

wecom contact list --department 1
wecom contact user "user-id"
wecom contact search --name "张三"

Webhooks

wecom webhook receive --handler "./handler.js"
wecom webhook send --url "webhook-url" --data '{"key": "value"}'

配置

export WECOM_CORP_ID="your_corp_id"
export WECOM_AGENT_ID="your_agent_id"
export WECOM_SECRET="your_secret"
export WECOM_WEBHOOK_URL="your_webhook_url"

所需权限

    发送消息：agent:send_msg
    读取联系人：contact:read
    管理群组：group:manage
    Webhook 访问：webhook:custom

最佳实践

    使用 markdown 格式化消息
    对发送失败实施重试逻辑
    缓存联系人信息以减少 API 调用
    使用批量操作处理大群组

故障排除

常见错误

    40014 INVALID_ACCESS_TOKEN - 重新生成令牌
    40078 APPLICATION_NOT_FOUND - 检查 agent_id
    41006 MISSING_AGENT - 设置默认 agent

速率限制

    消息：每个 agent 100条/分钟
    API 调用：每个企业 1000次/小时
    Webhooks：接收无限制

相关技能

    feishu - 飞书集成
    dingtalk - 钉钉集成
    crm - 通用 CRM 集成
