# GLM 图片生成技能

使用 **PPIO（派欧云）** 平台的 GLM Image 文生图 API 生成高质量图像。

## ⚠️ 需要手动配置

本技能需要你自行申请 PPIO API Key，不支持免配置开箱即用。

### 获取 API Key

1. 前往 [PPIO 派欧云官网](https://ppio.com) 注册账号
2. 在控制台创建 API Key
3. 将 Key 填入配置

### 配置方式

将 `.env.example` 复制为 `.env`，填入你的 API Key：

```bash
cp .env.example .env
# 编辑 .env 文件，填入 PPIO_API_KEY
```

或设置环境变量：

```bash
export PPIO_API_KEY=your_api_key_here
```

## 能力

- 文生图（GLM Image 模型）
- 支持多种尺寸（1280x1280、1568x1056、1056x1568 等）
- 异步任务模式，支持轮询结果
- 支持 curl / Python / Alma CLI 三种调用方式

## 接口说明

| 端点 | 方法 | 说明 |
|------|------|------|
| `/v1/images/generations:glm-image` | POST | 提交图片生成任务 |
| `/v1/tasks/{task_id}` | GET | 查询任务结果 |

详情见 [SKILL.md](SKILL.md)
