# GLM 图片生成 Skill

使用 PPIO 平台的 GLM Image 文生图 API 生成高质量图像。

## 配置

在 `~/.config/alma/skills/glm-image-generator/.env` 中设置：

```
PPIO_API_KEY=your_api_key_here
```

## API 概览

- **Base URL**: `https://api.ppio.com`
- **鉴权方式**: Bearer Token (`Authorization: Bearer {PPIO_API_KEY}`)
- **Content-Type**: `application/json`

## 流程说明

GLM Image 采用**异步任务模式**：

1. **提交生成任务** — 发送 prompt 等参数，返回 `task_id`
2. **轮询任务结果** — 使用 `task_id` 查询，直到状态变为 `success`
3. **获取图片** — 从结果中的 `images[].image_url` 下载图片

---

## 1. 提交 GLM 图片生成任务

### 请求

**Endpoint**: `POST /v1/images/generations:glm-image`

### 请求体参数

| 参数 | 类型 | 必填 | 默认值 | 描述 |
|------|------|:----:|:------:|------|
| `prompt` | string | ✅ | — | 图像描述。描述场景、主体、风格、细节 |
| `size` | string | ❌ | `"1280x1280"` | 图片尺寸。推荐：1280x1280、1568x1056、1056x1568、1472x1088、1088x1472、1728x960、960x1728。自定义：宽高 1024-2048px，总像素 ≤ 4194304，宽高均为 32 的倍数 |
| `quality` | string | ❌ | `"hd"` | 图像质量。当前仅支持 `"hd"` |
| `watermark_enabled` | boolean | ❌ | `true` | 是否添加 AI 生成水印 |

### 响应

```json
{
  "task_id": "string"
}
```

---

## 2. 查询任务结果

### 请求

**Endpoint**: `GET /v1/tasks/{task_id}`

### 响应

```json
{
  "task": {
    "task_id": "string",
    "status": "string",      // pending | running | success | failed
    "reason": "string",      // 失败原因（仅 status=failed 时）
    "eta": 123,
    "progress_percent": 123
  },
  "images": [
    {
      "image_url": "string",
      "image_url_ttl": 123,   // 图片链接有效期（秒）
      "image_type": "string"  // 图片格式
    }
  ]
}
```

### 状态说明

| 状态 | 说明 |
|------|------|
| `pending` | 任务排队中 |
| `running` | 任务执行中 |
| `success` | 任务完成，可读取 `images` 字段 |
| `failed` | 任务失败，`reason` 字段说明原因 |

建议轮询间隔：首次等待 5 秒，之后每 2 秒查询一次。

---

## 使用示例

### bash 调用

```bash
# 1. 提交任务
TASK_ID=$(curl -s -X POST "https://api.ppio.com/v1/images/generations:glm-image" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $PPIO_API_KEY" \
  -d '{
    "prompt": "一只可爱的橘猫坐在窗台上晒太阳，阳光透过玻璃洒在它身上，油画风格",
    "size": "1280x1280",
    "quality": "hd",
    "watermark_enabled": false
  }' | jq -r '.task_id')

echo "Task ID: $TASK_ID"

# 2. 轮询结果
while true; do
  RESULT=$(curl -s "https://api.ppio.com/v1/tasks/$TASK_ID" \
    -H "Authorization: Bearer $PPIO_API_KEY")
  STATUS=$(echo "$RESULT" | jq -r '.task.status')
  
  if [ "$STATUS" = "success" ]; then
    IMAGE_URL=$(echo "$RESULT" | jq -r '.images[0].image_url')
    echo "图片生成成功！"
    echo "下载链接: $IMAGE_URL"
    # 下载图片
    curl -o "glm_image_${TASK_ID}.png" "$IMAGE_URL"
    break
  elif [ "$STATUS" = "failed" ]; then
    echo "生成失败: $(echo "$RESULT" | jq -r '.task.reason')"
    break
  else
    echo "状态: $STATUS ($(echo "$RESULT" | jq -r '.task.progress_percent')%)"
    sleep 2
  fi
done
```

### Python 示例

```python
import requests
import time
import os

API_KEY = os.getenv("PPIO_API_KEY", "your_api_key_here")
BASE_URL = "https://api.ppio.com"

# 请求头
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

# 1. 提交任务
payload = {
    "prompt": "一只可爱的橘猫坐在窗台上晒太阳，阳光透过玻璃洒在它身上，油画风格",
    "size": "1280x1280",
    "quality": "hd",
    "watermark_enabled": False
}

resp = requests.post(
    f"{BASE_URL}/v1/images/generations:glm-image",
    headers=headers,
    json=payload
)
resp.raise_for_status()
task_id = resp.json()["task_id"]
print(f"任务已提交，Task ID: {task_id}")

# 2. 轮询结果
while True:
    result = requests.get(
        f"{BASE_URL}/v1/tasks/{task_id}",
        headers=headers
    )
    result.raise_for_status()
    data = result.json()
    status = data["task"]["status"]
    
    if status == "success":
        image_url = data["images"][0]["image_url"]
        print(f"图片生成成功！下载链接: {image_url}")
        # 下载图片
        img_resp = requests.get(image_url)
        with open(f"glm_image_{task_id}.png", "wb") as f:
            f.write(img_resp.content)
        print(f"已保存为 glm_image_{task_id}.png")
        break
    elif status == "failed":
        print(f"生成失败: {data['task'].get('reason', '未知错误')}")
        break
    else:
        print(f"状态: {status} ({data['task'].get('progress_percent', 0)}%)")
        time.sleep(2)
```

### Alma CLI 直接调用

```bash
# 提交任务
alma exec curl -s -X POST "https://api.ppio.com/v1/images/generations:glm-image" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $PPIO_API_KEY" \
  -d '{"prompt":"一只可爱的橘猫","size":"1280x1280","quality":"hd","watermark_enabled":false}'

# 查询结果（替换 YOUR_TASK_ID）
alma exec curl -s "https://api.ppio.com/v1/tasks/YOUR_TASK_ID" \
  -H "Authorization: Bearer $PPIO_API_KEY"
```

---

## 配置说明

1. 在 `.env` 文件中设置 `PPIO_API_KEY` 或在环境变量中设置
2. 图片生成是异步的，需要轮询任务结果
3. 建议设置合理的超时时间（默认 120 秒）
4. 生成图片链接有时效性（`image_url_ttl` 字段），请在有效期内下载

## 环境变量

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `PPIO_API_KEY` | PPIO API 密钥 | — |
| `PPIO_BASE_URL` | API 基础地址 | `https://api.ppio.com` |
