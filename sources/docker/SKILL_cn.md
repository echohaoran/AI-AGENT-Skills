---
name: docker
title: Docker 容器化技能
excerpt: 使用 Docker 将应用程序容器化，在安全沙箱中执行代码。消除"在我机器上能跑"的问题，实现可复现环境，安全运行不受信任的代码。无需 API。
date: 2026-04-17
来源: bobmatnyc/claude-mpm-skills@docker
安装量: 705+
授权工具:
  - Bash
  - Read
  - Write
---

# Docker 容器化技能

> **来源：** bobmatnyc/claude-mpm-skills@docker  
> **安装量：** 705+ | **API 依赖：** ❌ 无 | **协议：** MIT

## 何时使用

✅ **使用此技能的场景：**

- 需要在可复现环境中运行代码
- 需要安全地执行不受信任的代码
- 解决"在我机器上能跑"的问题
- 多语言项目需要一致的环境
- 构建容器化的 CI/CD 流水线
- 跨不同操作系统测试（Linux、Windows、macOS）

❌ **不要使用的场景：**

- 简单的一次性脚本（直接运行更快）
- 已在容器化环境中（跳过 Docker 层）
- 资源受限的环境（Docker 开销较大）
- 实时音视频处理（原生方式延迟更低）

## 核心能力

```infographic
infographic hierarchy-tree-curved-line-rounded-rect-node
data
  title Docker 技能核心能力
  items
    - label 容器管理
      children
        - label 从 Dockerfile 构建镜像
        - label 运行容器
        - label Compose 多容器编排
        - label 清理资源
    - label 安全执行
      children
        - label 沙箱代码运行
        - label 资源限制
        - label 网络隔离
    - label 环境控制
      children
        - label Python/Node/Go/Rust
        - label 指定包版本
        - label 自定义基础镜像
```

## 快速开始

### 1. 构建镜像

```bash
# 从 Dockerfile 构建
docker build -t my-project:latest .

# 带构建参数
docker build --build-arg VERSION=1.0 -t my-project:1.0 .

# 多平台构建
docker buildx build --platform linux/amd64,linux/arm64 -t my-project:latest .
```

### 2. 运行容器

```bash
# 基本运行
docker run my-project:latest

# 挂载卷
docker run -v $(pwd):/app my-project:latest python app.py

# 资源限制
docker run --memory=512m --cpus=0.5 my-project:latest

# 交互式 Shell
docker run -it my-project:latest /bin/bash

# 后台运行
docker run -d --name my-container my-project:latest
```

### 3. 使用 Docker Compose

```yaml
# docker-compose.yaml
version: '3.8'

services:
  app:
    build: .
    volumes:
      - ./data:/app/data
    environment:
      - NODE_ENV=production
    depends_on:
      - db
      - redis

  db:
    image: postgres:15
    volumes:
      - db-data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine

volumes:
  db-data:
```

## 安全代码执行

### 安全运行不受信任的代码

```bash
# 高度受限的执行
docker run \
  --rm \
  --network=none \           # 无网络访问
  --memory=128m \           # 最多 128MB 内存
  --cpus=0.25 \             # 最多 25% CPU
  --pids-limit=50 \         # 最多 50 个进程
  --read-only \             # 只读文件系统
  -v $(mktemp -d):/tmp \
  python:3.11-slim \
  python /tmp/script.py
```

## 多语言环境模板

### Python 环境

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "main.py"]
```

### Node.js 环境

```dockerfile
FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
CMD ["node", "main.js"]
```

## 故障排除

| 问题 | 解决方案 |
|------|---------|
| `docker: command not found` | 安装 Docker Desktop 或 `brew install docker` |
| `permission denied` | 将用户加入 docker 组：`sudo usermod -aG docker $USER` |
| 构建太慢 | 启用 BuildKit：`DOCKER_BUILDKIT=1 docker build ...` |
| 容器立即退出 | 检查日志：`docker logs <container>` |
| 端口已被占用 | 更换端口映射或停止冲突服务 |

## 与其他技能协同

- **workflow-automation** → 容器化工作流步骤
- **code-review-quality** → 在容器中运行测试
- **git-workflow** → 提交时自动构建和推送
- **file-organizer** → 从项目文件构建 Dockerfile

## 相关资源

- [Docker 官方文档](https://docs.docker.com/)
- [Dockerfile 最佳实践](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [Play with Docker](https://labs.play-with-docker.com/) — 免费在线 Docker 练习场
