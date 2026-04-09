SKILL.md
钉钉 (DingTalk) 集成

与钉钉集成，实现企业通讯、考勤、审批工作流和团队管理。

何时使用

✅ 使用此技能的场景：

    "发送钉钉消息"
    "创建钉钉审批"
    "查看考勤报表"
    "管理钉钉组织用户"
    "自动化钉钉机器人"

何时不使用

❌ 不要使用此技能的场景：

    偏好使用飞书（使用 feishu 技能）
    偏好使用企业微信（使用 wecom 技能）
    仅视频会议（使用钉钉原生应用）
    复杂的 HR 系统（使用专用钉钉 HR API）

快速开始

# 发送消息
dingtalk send --to "user-id" "你好，来自钉钉机器人的消息！"

# 创建审批
dingtalk approval create --template_id "template-123" --form_data '{"reason": "请假申请"}'

# 获取考勤
dingtalk attendance report --date 2024-01-15

核心命令

消息发送

dingtalk send --to "user-id" "消息"
dingtalk send --conversation "chat-id" "消息"
dingtalk send --all "公告消息"

机器人

dingtalk bot send --robot_code "robot_code" --secret "robot_secret" "消息"
dingtalk bot card --card_id "card_id" --data '{"key": "value"}'

审批

dingtalk approval list --status pending
dingtalk approval create --template_id "xxx" --form_data '{}'
dingtalk approval approve --approval_id "xxx" --comment "已批准"
dingtalk approval reject --approval_id "xxx" --comment "已拒绝"

考勤

dingtalk attendance user --user_id "user-id" --date 2024-01-15
dingtalk attendance group --dept_id 1 --date 2024-01-15
dingtalk attendance export --date_from 2024-01-01 --date_to 2024-01-31

组织管理

dingtalk org user list --dept_id 1
dingtalk org user info --user_id "user-id"
dingtalk org department list

配置

export DINGTALK_APP_KEY="your_app_key"
export DINGTALK_APP_SECRET="your_app_secret"
export DINGTALK_AGENT_ID="your_agent_id"

OAuth 设置

1. 在 open.dingtalk.com 创建应用
2. 设置所需的作用域
3. 配置回调 URL
4. 实现 OAuth 握手

所需权限

    消息：qyapi_write_message
    审批：approval_write
    考勤：attendance_read
    用户信息：oapi_user_list_by_page

最佳实践

    使用审批模板保持工作流一致
    缓存用户信息以减少 API 调用
    实现网络失败重试逻辑
    使用异步 webhooks 获取实时更新

故障排除

常见错误

    40014 INVALID_ACCESS_TOKEN - 刷新令牌
    40078 APPLICATION_NOT_FOUND - 检查应用配置
    40300 PERMISSION_DENIED - 请求所需的作用域

速率限制

    API 调用：每个应用 1000次/小时
    消息：每个机器人 100条/分钟
    审批：无限制

相关技能

    feishu - 飞书集成
    wecom - 企业微信集成
    approval-workflow - 通用审批自动化
