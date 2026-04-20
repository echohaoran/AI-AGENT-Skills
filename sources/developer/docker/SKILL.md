---
name: docker
description: Containerize applications and execute code in secure sandboxes using Docker. Eliminate "works on my machine" problems, enable reproducible environments, and safely run untrusted code. No API required.
date: 2026-04-17
source: bobmatnyc/claude-mpm-skills@docker
installs: 705
allowed-tools:
  - Bash
  - Read
  - Write
---

SKILL.md

# Docker Containerization Skill

> **Source:** bobmatnyc/claude-mpm-skills@docker  
> **Installs:** 705+ | **API Required:** ❌ No | **License:** MIT

## When to Use

✅ **Use this skill when:**

- User wants to run code in a reproducible environment
- Need to execute untrusted or user-submitted code safely
- "Works on my machine" issues need to be resolved
- Multi-language projects need consistent environments
- Building CI/CD pipelines with containerized steps
- Testing across different OS environments (Linux, Windows, macOS)

❌ **Do NOT use this skill when:**

- Simple one-off scripts (run directly is faster)
- Already in a containerized environment (skip Docker layer)
- Resource-constrained environments (Docker overhead is significant)
- Real-time audio/video processing (native is lower latency)

## Core Capabilities

```infographic
infographic hierarchy-tree-curved-line-rounded-rect-node
data
  title Docker Skill 核心能力
  items
    - label Container Management
      children
        - label Build images from Dockerfile
        - label Run containers
        - label Compose multi-container
        - label Prune/cleanup
    - label Secure Execution
      children
        - label Sandboxed code runs
        - label Resource limits
        - label Network isolation
    - label Environment Control
      children
        - label Python/Node/Go/Rust
        - label Specific package versions
        - label Custom base images
```

## Quick Start

### 1. Build an Image

```bash
# Build from Dockerfile
docker build -t my-project:latest .

# Build with build args
docker build --build-arg VERSION=1.0 -t my-project:1.0 .

# Build using buildx for multi-platform
docker buildx build --platform linux/amd64,linux/arm64 -t my-project:latest .
```

### 2. Run a Container

```bash
# Basic run
docker run my-project:latest

# With volume mount
docker run -v $(pwd):/app my-project:latest python app.py

# With resource limits
docker run --memory=512m --cpus=0.5 my-project:latest

# Interactive with shell
docker run -it my-project:latest /bin/bash

# Detached (background)
docker run -d --name my-container my-project:latest
```

### 3. Use Docker Compose

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

## Secure Code Execution

### Run Untrusted Code Safely

```bash
# Very restricted execution
docker run \
  --rm \
  --network=none \           # No network access
  --memory=128m \           # Max 128MB RAM
  --cpus=0.25 \             # Max 25% CPU
  --pids-limit=50 \         # Max 50 processes
  --read-only \             # Read-only filesystem
  -v $(mktemp -d):/tmp \
  python:3.11-slim \
  python /tmp/script.py
```

### Resource-Limited Execution

```bash
#!/bin/bash
# Execute user code in sandbox
CONTAINER_ID=$(docker run -d \
  --network=none \
  --memory=256m \
  --cpus=0.5 \
  --pids-limit=20 \
  --read-only \
  --user=nonroot \
  -v user_code:/code:ro \
  python:3.11-slim \
  python /code/main.py)

# Wait with timeout
docker wait $CONTAINER_ID
RESULT=$(docker logs $CONTAINER_ID)
docker rm $CONTAINER_ID > /dev/null

echo "$RESULT"
```

## Multi-Language Environment Templates

### Python Environment

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "main.py"]
```

### Node.js Environment

```dockerfile
FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
CMD ["node", "main.js"]
```

### Go Environment

```dockerfile
FROM golang:1.22-alpine AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o main .

FROM alpine:latest
RUN apk --no-cache add ca-certificates
WORKDIR /root/
COPY --from=builder /app/main .
CMD ["./main"]
```

## Docker Compose Templates

### Full-Stack Development

```yaml
version: '3.8'
services:
  frontend:
    build: ./frontend
    ports: ["3000:3000"]
    environment:
      - API_URL=http://backend:8000
    volumes:
      - ./frontend:/app
      - /app/node_modules

  backend:
    build: ./backend
    ports: ["8000:8000"]
    environment:
      - DATABASE_URL=postgresql://postgres:secret@db:5432/app
      - REDIS_URL=redis://redis:6379
    depends_on: [db, redis]

  db:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: secret
    volumes:
      - pgdata:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine

  nginx:
    image: nginx:alpine
    ports: ["80:80"]
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on: [frontend, backend]

volumes:
  pgdata:
```

## Scripts Reference

### `scripts/build.sh` — Build Wrapper

```bash
#!/bin/bash
# Build with caching and progress
docker build \
  --progress=plain \
  --no-cache="${NO_CACHE:-false}" \
  -t "${IMAGE_NAME:-app}:${VERSION:-latest}" \
  -f "${DOCKERFILE:-Dockerfile}" \
  .

echo "✅ Built: ${IMAGE_NAME:-app}:${VERSION:-latest}"
```

### `scripts/run-sandbox.sh` — Safe Code Execution

```bash
#!/bin/bash
# Execute user code in heavily restricted container
EXEC_DIR=$(mktemp -d)
chmod 755 $EXEC_DIR

# Copy user code
cp "$1" $EXEC_DIR/

# Run with restrictions
docker run --rm \
  --network=none \
  --memory=128m \
  --cpus=0.25 \
  --pids-limit=10 \
  --read-only \
  --user=1000:1000 \
  -v $EXEC_DIR:/code:ro \
  -w /code \
  python:3.11-slim \
  python /code/$(basename "$1")

rm -rf $EXEC_DIR
```

### `scripts/prune.sh` — Cleanup

```bash
#!/bin/bash
# Clean up Docker resources
docker system prune -f
docker image prune -f
docker container prune -f
echo "✅ Docker cleanup complete"
```

## Use Cases

### Use Case 1: Consistent Dev Environment

```bash
# Instead of "it works on my machine"
docker run -it --rm \
  -v $(pwd):/workspace \
  -w /workspace \
  my-org/dev-env:latest \
  bash
```

### Use Case 2: Safe Plugin Execution

```bash
# Execute a user-uploaded plugin safely
docker run --rm \
  --network=none \
  --memory=64m \
  --cpus=0.1 \
  --read-only \
  --user=nobody \
  -v plugin_code:/plugin:ro \
  -v /tmp/plugin_output:/output \
  --security-opt=no-new-privileges \
  python:3.11-slim \
  python /plugin/run.py

# Output is in /tmp/plugin_output
```

### Use Case 3: Multi-Version Testing

```bash
# Test against Python 3.8, 3.9, 3.10, 3.11
for version in 3.8 3.9 3.10 3.11; do
  docker run --rm \
    python:${version}-slim \
    python -m pytest tests/
done
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `docker: command not found` | Install Docker Desktop or `brew install docker` |
| `permission denied` | Add user to docker group: `sudo usermod -aG docker $USER` |
| Build slow | Use BuildKit: `DOCKER_BUILDKIT=1 docker build ...` |
| Container exits immediately | Check logs: `docker logs <container>` |
| Port already in use | Change port mapping or stop conflicting service |

## Best Practices

1. **Use slim images** — `python:3.11-slim` over `python:3.11`
2. **Multi-stage builds** — Keep final image small, builder stage can be large
3. **Don't run as root** — Use `--user` flag in production
4. **Set resource limits** — Always set `--memory` and `--cpus`
5. **Network isolation** — Use `--network=none` for untrusted code
6. **Read-only root** — Use `--read-only` when possible
7. **Clean up** — Run `docker system prune` regularly

## Integration with Other Skills

- **workflow-automation** → Containerize workflow steps
- **code-review-quality** → Run tests in containers
- **git-workflow** → Build and push on commits
- **file-organizer** → Build Dockerfiles from project files

## See Also

- [Docker Official Docs](https://docs.docker.com/)
- [Dockerfile Best Practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [Play with Docker](https://labs.play-with-docker.com/) — Free online Docker playground
