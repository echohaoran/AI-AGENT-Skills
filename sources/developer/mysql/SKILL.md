---
name: mysql
description: Execute MySQL/SQL queries, analyze database schemas, export data to CSV/JSON, and perform migrations. Works with local or remote MySQL/PostgreSQL databases.
date: 2026-04-17
source: planetscale/database-skills@mysql
installs: 2720
allowed-tools:
  - Bash
  - Read
---

SKILL.md

# MySQL Database Skill

> **Source:** planetscale/database-skills@mysql  
> **Installs:** 2,720+ | **API Required:** ❌ No (needs local MySQL) | **License:** MIT

## When to Use

✅ **Use this skill when:**

- Analyzing database schema and relationships
- Exporting query results to CSV/JSON
- Writing and optimizing SQL queries
- Understanding table structure and indexes
- Database migrations between environments

## Quick Start

```bash
# Connect to local MySQL
mysql -u root -p

# List databases
mysql> SHOW DATABASES;

# Select database
mysql> USE mydb;

# Show tables
mysql> SHOW TABLES;

# Describe table
mysql> DESCRIBE users;
```

## Query Examples

### Basic Queries

```sql
-- Select with conditions
SELECT * FROM users WHERE status = 'active' ORDER BY created_at DESC LIMIT 10;

-- Join multiple tables
SELECT u.name, o.total, o.created_at
FROM users u
JOIN orders o ON u.id = o.user_id
WHERE o.total > 100;

-- Aggregate with group by
SELECT category, COUNT(*) as count, AVG(price) as avg_price
FROM products
GROUP BY category
HAVING count > 5;
```

### Export Data

```bash
# Export to CSV
mysql -u root -p mydb -e "SELECT * FROM users" | csvkit > users.csv

# Export to JSON
mysql -u root -p mydb -e "SELECT * FROM users" -B | mysql2json > users.json

# Export specific columns
mysql -u root -p mydb -e "SELECT id, name, email FROM users" | column -t -s $'\t' > users.tsv
```

## Scripts Reference

### `scripts/query.sh`

```bash
#!/bin/bash
# Execute SQL query with optional export
DB="${DB_NAME:-mydb}"
QUERY="$1"
FORMAT="${2:-table}"  # table, csv, json

mysql -u root -p "$DB" -e "$QUERY" -B 2>/dev/null | \
  case "$FORMAT" in
    csv)  mlr --icsv --opprint cat ;;
    json) mlr --itsv --ojson cat ;;
    *)    cat ;;
  esac
```

## See Also

- [Document XLSX Skill](../document-xlsx/) — Export to spreadsheets
- [File Organizer](../file-organizer/) — Organize export files
