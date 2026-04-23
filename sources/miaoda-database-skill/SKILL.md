---
name: miaoda-database-skill
description: 创建数据库、建表、执行 SQL、查询数据、查看表结构。当用户需要数据库、数据表、数据持久化、PostgreSQL 操作时使用。通过 miaoda-data-cli db 子命令（db init / db sql / db schema）完成数据库初始化、DDL/DML/SELECT 执行和表结构查看。
---
# Database Skill

本技能指导 Agent 通过 `miaoda-data-cli db` 命令操作数据库，包括：
- **db sql**：执行 SQL 语句（DDL/SELECT/DML）
- **db schema**：查看数据库表结构（默认 DDL，`--json` 输出结构化 JSON）

### 使用方式

推荐通过 `npx -y` 直接运行，无需预先安装：

```bash
npx -y @lark-apaas/miaoda-data-cli db sql "SELECT 1"
```

## 通用约定

### 错误处理

所有命令失败时退出码为 **1**，错误信息输出到 **stderr**，格式为 JSON：

```json
{"statusCode": 2, "message": "SQL 执行失败", "detail": "[k_dl_1300002] ERROR: relation \"xxx\" does not exist"}
```

| statusCode | 含义 | 是否重试 | 触发场景 |
|------------|------|----------|---------|
| 1 | 语法/参数错误 | 否 | SQL 语法错误、参数缺失、表名不合法 |
| 2 | 执行失败 / 业务错误 | 否 | 表不存在、插入失败、权限不足等 |
| 3 | 服务异常 | 是，最多 1 次 | 网络错误、数据库暂时不可用 |

**处理策略**：
- statusCode 1 → 检查语法，修正后重新执行
- statusCode 2 → 读取 `detail` 字段定位原因，修正后重新执行
  - 若 message 包含"数据库未初始化"，说明尚未执行 `db init`，需先执行 `db init` 初始化数据库后再重试
- statusCode 3 → 重试一次，仍失败则告知用户

### 输出约定

- `db sql`：默认输出表格到 **stdout**，`--json` 输出结构化 JSON
- `db schema`：默认输出 DDL 到 **stdout**，`--json` 输出表结构 JSON

---

## 命令：db init

初始化数据库。**首次使用 `db sql` / `db schema` 前必须执行**。此命令是幂等的，重复执行不会报错。

### 格式

```bash
npx -y @lark-apaas/miaoda-data-cli db init
```

### 输出

```
Database initialized.
```

### 典型工作流

```bash
# 1. 初始化数据库
npx -y @lark-apaas/miaoda-data-cli db init

# 2. 建表（建议添加表注释和字段注释，便于后续理解用途）
npx -y @lark-apaas/miaoda-data-cli db sql "CREATE TABLE note (id UUID PRIMARY KEY DEFAULT gen_random_uuid(), title VARCHAR(255) NOT NULL); COMMENT ON TABLE note IS '笔记表';"

# 3. 查看表结构
npx -y @lark-apaas/miaoda-data-cli db schema note
```

---

## 命令：db sql

执行 SQL 语句并返回结果。

### 格式

```bash
npx -y @lark-apaas/miaoda-data-cli db sql "<SQL 语句>"

# 加 --json 输出结构化 JSON
npx -y @lark-apaas/miaoda-data-cli db sql --json "<SQL 语句>"
```

### 示例

```bash
# DDL
npx -y @lark-apaas/miaoda-data-cli db sql "
CREATE TABLE note (id UUID PRIMARY KEY DEFAULT gen_random_uuid(), title VARCHAR(255) NOT NULL, content TEXT);
COMMENT ON TABLE note IS 'note table';
CREATE INDEX idx_note_title ON note(title);
"

# SELECT
npx -y @lark-apaas/miaoda-data-cli db sql "SELECT title, content FROM note LIMIT 10"

# INSERT
npx -y @lark-apaas/miaoda-data-cli db sql "INSERT INTO note (title, content) VALUES ('hello', 'world')"
```

### 默认输出（表格格式）

**SELECT**：
```
title | content
------+--------
hello | world
(1 row)
```

**DML**：
```
1 row affected
```

**DDL**：
```
DDL executed successfully
```

### --json 输出

**单条语句**：

SELECT — 直接输出查询结果的 JSON 数组：
```json
[
  {"title": "hello", "content": "world"}
]
```

DML — 输出影响行数：
```json
{"affectedRows": 1}
```

DDL — 输出成功标识：
```json
{"status":"ok"}
```

**多条语句**：输出带 index/type 的结构化数组：
```json
[
  {"index": 0, "type": "DDL", "status": "ok"},
  {"index": 1, "type": "DML", "affectedRows": 1},
  {"index": 2, "type": "SELECT", "rows": [{"id": "...", "name": "test"}], "rowCount": 1}
]
```

### 返回值处理

- **DDL**：默认输出确认文本，`--json` 输出 `{"status":"ok"}`，退出码 0 即成功
- **SELECT**：默认输出表格，`--json` 直接输出数据 JSON 数组，可直接解析使用
- **DML**：默认输出影响行数文本，`--json` 输出 `{"affectedRows": N}`

---

## 命令：db schema

查看数据库表结构。默认输出 DDL（CREATE TABLE 语句），`--json` 输出表结构 JSON。支持多表名。

### 格式

```bash
# 所有表 DDL
npx -y @lark-apaas/miaoda-data-cli db schema

# 指定表 DDL
npx -y @lark-apaas/miaoda-data-cli db schema <table_name>

# 多表 DDL
npx -y @lark-apaas/miaoda-data-cli db schema <table1> <table2>

# 表结构 JSON
npx -y @lark-apaas/miaoda-data-cli db schema --json
npx -y @lark-apaas/miaoda-data-cli db schema <table_name> --json
```

### 示例

```bash
# 所有表 DDL
npx -y @lark-apaas/miaoda-data-cli db schema

# 查看 note 表 DDL
npx -y @lark-apaas/miaoda-data-cli db schema note

# 查看 note 表结构 JSON
npx -y @lark-apaas/miaoda-data-cli db schema note --json
```

### 默认输出（DDL）

```sql
CREATE TABLE workspace_xxx.note (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  title character varying(255) NOT NULL,
  content text NULL,
  CONSTRAINT note_pkey PRIMARY KEY (id)
) TABLESPACE pg_default;
COMMENT ON TABLE workspace_xxx.note IS 'note table';
```

多表时空行分隔，不存在的表输出 `-- table "xxx" not found`。

### --json 输出

```json
{
  "tableName": "note",
  "comment": "note table",
  "type": "normal",
  "fields": [
    {
      "fieldName": "id",
      "type": "uuid",
      "isNullable": false,
      "defaultValue": "gen_random_uuid()",
      "isPrimary": true,
      "isUnique": false,
      "isArray": false,
      "isEnum": false
    },
    {
      "fieldName": "title",
      "type": "varchar",
      "isNullable": false,
      "defaultValue": null,
      "isPrimary": false
    }
  ],
  "indexes": [],
  "relationships": []
}
```
