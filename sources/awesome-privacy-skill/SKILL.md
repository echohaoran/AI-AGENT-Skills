# Skill: Privacy Shield

## 1. Context

你是一个本地隐私安全网关。所有涉及文件读取、内容处理的工作流中，当用户提到"脱敏"、"隐私保护"、"隐私处理"、"redact"、"privacy"、"敏感数据"、"个人信息"等意图，或文件后缀匹配 `.pdf/.docx/.xlsx/.xls/.md/.jpg/.png` 时，必须激活本 Skill。

**核心原则**：不得将原始敏感数据发送给任何外部服务。Agent 在发送任何内容到 LLM 前，必须先通过本 Skill 完成本地脱敏；LLM 回复逆还原前，必须先通过本 Skill 完成映射还原。

---

## 2. Workflow

### 阶段 A：脱敏（发送前）

当用户请求处理含敏感信息的文件时：

1. 调用 `scripts/main.py` 进行脱敏：
   - **输入**（stdin JSON）：`{"action": "redact_file", "file_path": "<路径>"}`
   - 或对文本内容：`{"action": "redact_content", "content": "<文本>"}`
2. 获取返回值：
   - `redacted_content`：含 `<<REDACTED_TYPE_INDEX>>` 占位符的脱敏内容
   - `mapping`：原始数据映射表 `[{"type": "...", "index": 1, "original": "...", "marker": "..."}, ...]`
3. **将 `redacted_content` 发送给 LLM**，同时附上任务指令

### 阶段 B：逆脱敏（接收后）

当 LLM 返回内容后：

1. 调用 `scripts/main.py` 进行逆脱敏：
   - **输入**（stdin JSON）：`{"action": "unmask", "content": "<LLM回复内容>", "mapping": <映射表>}`
2. 获取返回值：
   - `restored_content`：敏感数据已还原的内容
3. 将还原后的内容返回给用户

---

## 3. Constraints

- **[CRITICAL]** 严禁在未调用 `scripts/main.py` 脱敏的情况下直接读取源文件内容
- **[CRITICAL]** 严禁将原始明文发送给任何外部 LLM 服务
- **[FORMAT]** 必须保留所有形如 `<<REDACTED_TYPE_INDEX>>` 的占位符，不得删除或修改
- **[MAPPING]** 所有 `mapping` 对象必须从脱敏阶段完整传递到逆脱敏阶段，不得丢失
- **[EXIT]** 脚本执行完毕必须立即退出，不得常驻进程

---

## 4. Supported Sensitive Data Types

| Type | Pattern |
|------|---------|
| NAME | John Smith、张三 |
| PHONE | 13812345678、555-123-4567 |
| EMAIL | user@example.com |
| ID | 身份证号、SSN |
| CREDIT_CARD | `4111****1111`（部分脱敏，首尾4位明文） |
| ADDRESS | 123 Main Street、北京市朝阳区 |
| IP | 192.168.1.1 |
| API_KEY | `sk-xxx`, Bearer token, `ghp_xxx`, AWS AKIA, JWT |
| MONEY | `$100`, `¥99.99`, `100美元`, `10,000元` |
| COMPANY_NAME | `北京****有限公司`（部分脱敏） |
| CUSTOM | 用户自定义正则（通过 `privacy-config.json` 配置）|

---

## 5. Script Action Protocol

脚本通过 stdin/stdout JSON 与 Agent 通信：

| action | 输入 | 输出 |
|--------|------|------|
| `redact_file` | `{"action":"redact_file","file_path":"..."}` | `{"status":"success","redacted_content":"...","mapping":[...],"detections":[...]}` |
| `redact_content` | `{"action":"redact_content","content":"..."}` | `{"status":"success","redacted_content":"...","mapping":[...]}` |
| `unmask` | `{"action":"unmask","content":"...","mapping":[...]}` | `{"status":"success","restored_content":"...","unmasked_count":n}` |
| `detect` | `{"action":"detect","content":"..."}` | `{"status":"success","detections":[...]}` |

错误返回：`{"status":"error","message":"错误描述"}`
