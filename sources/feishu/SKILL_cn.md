SKILL.md
飞书 (Feishu/Lark) 集成

与飞书（Lark）集成，实现工作沟通、协作和自动化。

何时使用

✅ 使用此技能的场景：

    "发送飞书消息"
    "创建飞书群"
    "安排飞书会议"
    "读取飞书联系人"
    "自动化飞书工作流"

何时不使用

❌ 不要使用此技能的场景：

    直接调用 API 更快（简单的单次消息）
    飞书 API 在您所在的地区不可用
    需要实时流（webhook 是异步的）

快速开始

# 发送消息
feishu send --channel "general" "你好团队！"

# 创建群组
feishu group create "项目Alpha"

# 安排会议
feishu meeting schedule --title "站会" --participants @user1 @user2

核心命令

消息发送

feishu send --channel "channel-name" "消息内容"
feishu send --user "email@example.com" "消息内容"
feishu send --group "group-id" "消息内容"

群组与频道

feishu group list
feishu group create "群组名称"
feishu group add-member "group-id" @用户名

会议

feishu meeting schedule --title "会议标题" --duration 30
feishu meeting list --upcoming
feishu meeting cancel "meeting-id"

联系人

feishu contact list --department "工程部"
feishu contact info @用户名

自动化

feishu webhook trigger --event "build_complete" --data '{"build_id": "123"}'
feishu bot send "来自 CI流水线的自动化消息"

配置

设置您的飞书 API 凭据：

export FEISHU_APP_ID="your_app_id"
export FEISHU_APP_SECRET="your_app_secret"
export FEISHU_WEBHOOK_URL="your_webhook_url"

所需权限

    发送消息：chat:write
    读取消息：chat:read
    管理群组：group:admin
    安排会议：calendar:write
    读取联系人：contact:read

最佳实践

    使用 webhooks 实现事件驱动自动化
    缓存联系人查询以加快常用用户访问
    设置 API 速率限制的错误处理
    使用话题回复保持对话有序

故障排除

速率限制

    默认：100 请求/分钟
    超出限制：等待 60 秒后重试
    尽可能使用批量操作

常见错误

    10003 INVALID_ACCESS_TOKEN - 刷新您的访问令牌
    99991663 CHANNEL_NOT_FOUND - 检查频道名称/群组 ID
    230001 PERMISSION_DENIED - 请求所需的作用域

相关技能

    wecom - 企业微信集成
    dingtalk - 钉钉集成
    webhook - 通用 webhook 自动化
