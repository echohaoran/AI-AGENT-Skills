---
title: 阿里云
excerpt: 管理阿里云资源，包括 ECS、OSS、RDS 等云服务。
date: 2026-04-09
---

SKILL.md
阿里云 (Aliyun) 操作

管理阿里云资源，包括 ECS、OSS、RDS 等云服务。

何时使用

✅ 使用此技能的场景：

    "列出我的阿里云 ECS 实例"
    "上传文件到 OSS 存储桶"
    "检查 RDS 数据库状态"
    "管理阿里云 RAM 用户"
    "自动化阿里云部署"

何时不使用

❌ 不要使用此技能的场景：

    需要 AWS 特定功能（使用 aws 技能）
    需要 Azure 特定功能（使用 azure 技能）
    复杂的 Kubernetes 部署（使用 aliyun-ack 技能）
    实时大数据处理（使用 dataworks 技能）

快速开始

# 配置凭据
aliyun configure --access-key-id YOUR_KEY --access-key-secret YOUR_SECRET --region cn-hangzhou

# 列出 ECS 实例
aliyun ecs list-instances

# 上传到 OSS
aliyun oss put bucket-name object-key --file ./local-file.txt

核心命令

ECS（计算）

aliyun ecs list-instances                      # 列出所有 ECS
aliyun ecs describe-instance --instance-id i-xxx
aliyun ecs start-instance --instance-id i-xxx
aliyun ecs stop-instance --instance-id i-xxx
aliyun ecs create-snapshot --disk-id d-xxx

OSS（存储）

aliyun oss list-buckets
aliyun oss put bucket/key --file file.txt
aliyun oss get bucket/key --output ./download.txt
aliyun oss list bucket/key
aliyun oss delete bucket/key

RDS（数据库）

aliyun rds list-instances
aliyun rds describe-db --db-instance-id rm-xxx
aliyun rds create-backup --db-instance-id rm-xxx
aliyun rds restore-db --db-instance-id rm-xxx --backup-id b-xxx

RAM（身份管理）

aliyun ram list-users
aliyun ram create-user --name username
aliyun ram attach-policy --user-name username --policy-name AliyunECSReadOnlyAccess

SLB（负载均衡）

aliyun slb list-load-balancers
aliyun slb describe-load-balancer --load-balancer-id lb-xxx
aliyun slb add-backend-servers --load-balancer-id lb-xxx --instance-ids i-xxx,i-yyy

配置

aliyun configure                           # 交互式设置
aliyun configure --mode AK               # 访问密钥模式
aliyun configure --mode StsToken         # STS 令牌模式
aliyun configure --mode EcsRamRole       # ECS RAM 角色模式

环境变量

export ALIYUN_ACCESS_KEY_ID="your_key_id"
export ALIYUN_ACCESS_KEY_SECRET="your_key_secret"
export ALIYUN_DEFAULT_REGION="cn-hangzhou"

常见用例

备份策略

# 为 RDS 创建每日备份
aliyun rds create-backup --db-instance-id rm-xxx --backup-method Full --backup-retention-period 7

# ECS 自动快照轮换
aliyun ecs create-snapshot --disk-id d-xxx
aliyun ecs delete-snapshot --snapshot-id s-xxx --force

通过 OSS 传输文件

# 上传应用构建
aliyun oss put my-app-bucket deploy/v1.2.3.tar.gz --file ./build.tar.gz

# 下载日志
aliyun oss get my-logs-bucket app.log.2024-01-15 --output ./app.log

最佳实践

    使用 RAM 角色实现最小权限
    为关键磁盘启用自动快照策略
    使用 OSS 生命周期规则优化成本
    设置 SLB 健康检查以确保高可用性
    为所有资源添加标签以便成本跟踪

故障排除

常见错误

    InvalidAccessKeyId - 检查您的访问密钥
    NoPermission - 附加所需的 RAM 策略
    InvalidRegionId - 使用正确的区域代码
    ResourceNotFound - 检查资源 ID 是否存在

速率限制

    API 调用因服务而异
    使用指数退避处理限流
    考虑使用 ROS 进行批量操作

相关技能

    aws - AWS 操作
    azure - Azure 操作
    terraform - 基础设施即代码
