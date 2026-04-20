---
name: miaoda-database-skill
title: 数据库操作
excerpt: 创建数据库、建表、执行 SQL、查询数据
date: 2026-04-20
来源: 飞书机器人技能库
授权工具: [命令行工具]
---

# 数据库操作

> **来源：** 飞书机器人技能库  
> **API 依赖：** 是 | **协议：** MIT

## 何时使用

✅ **使用此技能的场景：**

- 需要创建数据库和数据表
- 需要执行 SQL 语句（DDL/DML/SELECT）
- 需要查看表结构
- 用户提到"数据库"、"SQL"、"建表"

❌ **不要使用的场景：**

- 需要复杂事务处理
- 需要数据库管理（用户直接操作）

## 核心命令

### db init - 初始化数据库

```bash
npx -y @lark-apaas/miaoda-data-cli db init
```

### db sql - 执行 SQL

```bash
npx -y @lark-apaas/miaoda-data-cli db sql "SELECT * FROM users"
```

**参数**：
- `--json`：输出结构化 JSON

### db schema - 查看表结构

```bash
npx -y @lark-apaas/miaoda-data-cli db schema <table_name>
```

**参数**：
- `--json`：输出结构化 JSON

## 使用示例

### 初始化并建表

```bash
# 1. 初始化
npx -y @lark-apaas/miaoda-data-cli db init

# 2. 建表
npx -y @lark-apaas/miaoda-data-cli db sql "CREATE TABLE note (id UUID PRIMARY KEY DEFAULT gen_random_uuid(), title VARCHAR(255) NOT NULL)"

# 3. 查看结构
npx -y @lark-apaas/miaoda-data-cli db schema note
```

### 查询数据

```bash
npx -y @lark-apaas/miaoda-data-cli db sql "SELECT title, content FROM note LIMIT 10"
```

### 插入数据

```bash
npx -y @lark-apaas/miaoda-data-cli db sql "INSERT INTO note (title, content) VALUES ('hello', 'world')"
```

## 错误处理

| statusCode | 含义 | 处理 |
|------------|------|------|
| 1 | 语法/参数错误 | 检查语法 |
| 2 | 执行失败 | 检查错误信息 |
| 3 | 服务异常 | 重试一次 |

## 相关技能

- [妙搭应用开发](../miaoda-coding/)
- [文档解析](../miaoda-doc-parse/)
