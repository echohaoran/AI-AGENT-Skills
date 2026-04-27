---
name: awesome-privacy-skill
description: >
  本地敏感数据脱敏与可逆还原工具 v1.3。当用户提到任何与"脱敏"、"隐私保护"、"敏感数据处理"、"个人信息保护"相关的内容时，必须激活本技能。
  支持 PDF 图像级遮盖脱敏、OCR 脱敏、Word/Markdown/Excel 精准替换脱敏。
  自动检测 17 种敏感数据类型（姓名、手机号、身份证、银行卡、邮箱、密码、API Key、地址、IP、护照、公司名等）。
  多格式全管道输出：OCR脱敏文本 + 脱敏版PDF + 脱敏版DOCX + 脱敏版MD + 汇总映射表 + 反脱敏指南。
  
  触发关键词：脱敏、隐私、敏感数据、个人信息、加隐私、redact、redaction、mask、privacy、personal data、PII、个人信息保护、数据脱敏、隐私处理、隐去、掩盖、打码、保护隐私、去隐私、遮盖、擦除、替换敏感信息。
  
  支持文件格式：.pdf, .docx, .xlsx, .xls, .md, .markdown, .jpg, .jpeg, .png
  
  处理流程：OCR识别 → 关键词脱敏 → PDF遮盖 → 格式转换脱敏 → 输出多格式结果。
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
---

# Skill: Privacy Shield v1.3

## 1. Context

你是一个本地隐私安全网关。所有涉及文件读取、内容处理的工作流中，当用户提到"脱敏"、"隐私保护"、"隐私处理"、"redact"、"privacy"、"敏感数据"、"个人信息"等意图，或文件后缀匹配 `.pdf/.docx/.xlsx/.xls/.md/.jpg/.png` 时，必须激活本 Skill。

**核心原则**：不得将原始敏感数据发送给任何外部服务。Agent 在发送任何内容到 LLM 前，必须先通过本 Skill 完成本地脱敏；LLM 回复逆还原前，必须先通过本 Skill 完成映射还原。

**v1.3 新增能力**：
- **多格式全管道脱敏**（`redact_multi_format`）：PDF/图片 → OCR 脱敏 + PDF 图像遮盖 + DOCX 转换脱敏 + MD 转换脱敏 + 汇总映射表 + 反脱敏指南

**v1.2 新增能力**：
- **PDF 图像级脱敏**（核心创新）：PyMuPDF 精准坐标定位 + 高清渲染 + OCR 验证，全自动
- 新增 `PASSPORT` / `FRAGMENT` / `USERNAME` 类型检测
- 新增 `pdf_handler.redact_image_level()` — PDF 图像级脱敏专用方法
- 新增 `pdf_handler.verify_redaction()` — OCR 验证脱敏效果

---

## 2. Workflow

### 阶段 A：脱敏（发送前）

```bash
# Word/Excel/Markdown：正则模式（自动检测未知敏感数据）
echo '{"action":"redact_file","file_path":"report.docx"}' | python3 scripts/main.py

# Word/Excel/Markdown：关键词规则表（最高精度）
echo '{"action":"redact_file","file_path":"report.docx","keyword_rules":[
  {"keyword":"张雅琪","placeholder":"████姓名A"},
  {"keyword":"13867925618","placeholder":"████手机A"}
]}' | python3 scripts/main.py

# PDF（图形化文本，推荐图像级脱敏）
echo '{"action":"redact_file","file_path":"report.pdf","keyword_rules":[
  {"keyword":"张雅琪","placeholder":"████姓名A"},
  {"keyword":"13867925618","placeholder":"████手机A"}
],"redact_mode":"image"}' | python3 scripts/main.py
```

获取返回值：`redacted_content`、`mapping`、`output_path`、`detections`

**将 `redacted_content` 发送给 LLM**，同时附上任务指令。

### 阶段 B：验证（推荐）

```bash
echo '{"action":"validate","redacted_content":"..."}' | python3 scripts/main.py
# 返回 {"clean": true/false, "remaining": [...]} — 若 clean=false，需补充规则
```

### 阶段 C：逆脱敏（接收后）

```bash
echo '{"action":"unmask","content":"<LLM回复内容>","mapping":[...]}' | python3 scripts/main.py
```

---

## 3. Constraints

- **[CRITICAL]** 严禁在未调用 `scripts/main.py` 脱敏的情况下直接读取源文件内容
- **[CRITICAL]** 严禁将原始明文发送给任何外部 LLM 服务
- **[FORMAT]** 必须保留所有形如 `<<REDACTED_TYPE_INDEX>>` 或 `[████TYPE_1]` 的占位符
- **[MAPPING]** 所有 `mapping` 对象必须从脱敏阶段完整传递到逆脱敏阶段，不得丢失
- **[VALIDATE]** 脱敏完成后，强烈建议调用 `validate` 确认无残留
- **[KEYWORD]** 关键词规则按长度降序排列，防止短词吞长词
- **[PDF]** 对于图形化 PDF，优先使用 `redact_image_level()` 方法（图像级遮盖）
- **[EXIT]** 脚本执行完毕必须立即退出，不得常驻进程

---

## 4. Supported Sensitive Data Types (v1.2)

| Type | Pattern | Specificity |
|------|---------|-------------|
| CREDIT_CARD | Visa/MC/Amex/UnionPay 13-19位，`(?<!\d)(?!\d)` 边界 | 80 |
| ID | 中国身份证18位 / US SSN（含分隔符） | 70 |
| API_KEY | GitHub Token、AWS Key、OpenAI Key、JWT、Bearer Token 等 | 65 |
| EMAIL | 标准邮箱格式 | 60 |
| MONEY | 货币符号+金额、金融关键词+金额 | 55 |
| PHONE | 中国手机号、US电话、国际电话 | 50 |
| PASSPORT | 中国护照(E+8位)、港澳通行证(W+8位)、驾照(12位) | 45 |
| IP | IPv4 地址 | 40 |
| FRAGMENT | 10-19位数字串（捕获 OCR 碎片化长编号） | 35 |
| USERNAME | 微信号(wxid_)、OA账号、社交媒体用户名 | 30 |
| COMPANY_NAME | 公司名（中英文后缀匹配，**部分脱敏**） | 30 |
| NAME | English Name、Chinese Pinyin Name | 20 |
| ADDRESS | 英文街道地址、中文省市区详细地址 | 10 |
| CUSTOM | 用户自定义正则（`privacy-config.json` 配置） | 25 |

---

## 5. Script Action Protocol (v1.2)

| action | 输入 | 输出 |
|--------|------|------|
| `redact_file` | `{"action":"redact_file","file_path":"...","keyword_rules":[...],"redact_mode":"image"}` | `{"status":"success","redacted_content":"...","mapping":[...],"output_path":"...","detections":[...]}` |
| `redact_content` | `{"action":"redact_content","content":"...","keyword_rules":[...]}` | `{"status":"success","redacted_content":"...","mapping":[...],"detections":[...]}` |
| `unmask` | `{"action":"unmask","content":"...","mapping":[...]}` | `{"status":"success","restored_content":"...","unmasked_count":n}` |
| `detect` | `{"action":"detect","content":"..."}` | `{"status":"success","detections":[...]}` |
| `validate` | `{"action":"validate","redacted_content":"..."}` | `{"status":"success","clean":bool,"remaining":[...]}` |

---

## 6. PDF 图像级脱敏详解（v1.2 核心创新）

### 适用场景
- 图形化 PDF（文字由字体渲染，PyMuPDF 文本提取不完整）
- OCR 难以精准识别的复杂布局
- 需要视觉级遮盖而非文本替换

### 技术原理

```
PDF原始页面
    ↓ [PyMuPDF text_dict 提取]
精确文本坐标 (x0, y0, x1, y1)
    ↓ [Scale × zoom 倍]
图像像素坐标
    ↓ [PIL 绘制全行黑条]
高清遮盖图像
    ↓ [fitz.insert_image]
新 PDF（敏感内容被黑块完全覆盖）
    ↓ [pytesseract OCR 验证]
确认零残留
```

### 关键参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `zoom` | 4 | 渲染分辨率（4×=288 DPI，越高越精准但文件越大） |
| `keyword_rules` | 必填 | 精准关键词表（推荐先用 `detect` 提取） |
| `output_path` | 必填 | 输出 PDF 路径 |

### 代码示例

```python
from scripts.handlers.pdf_handler import PDFHandler

handler = PDFHandler(settings)
result = handler.redact_image_level(
    input_path="原始.pdf",
    output_path="脱敏版.pdf",
    keyword_rules=[
        {"keyword": "张雅琪", "placeholder": "████姓名A"},
        {"keyword": "13867925618", "placeholder": "████手机A"},
    ],
    zoom=4,
)
print(result["total_rects"], "处已遮盖")
```

### 注意事项

1. **关键词空格**：PyMuPDF 提取文本可能不保留空格，如 `"税前 18600 元"` 实际为 `"税前18600 元"`。建议同时添加有空格和无空格两个版本。
2. **全行遮盖**：使用整行宽度黑条，而非仅覆盖文本 bbox，防止字体字形超界导致的白缝。
3. **合并相邻行**：相邻的敏感行合并为一个遮盖区域，减少黑块数量。
4. **验证必须**：脱敏后必须运行 OCR 验证，防止遗漏。

---

## 7. keyword_rules 使用指南

```python
keyword_rules = [
    # 长词在前，短词在后（防止短词吞长词）
    {"keyword": "杭州市滨江区长河街道奥体壹号小区7栋2单元1902", "placeholder": "████现居地址A"},
    {"keyword": "奥体壹号小区", "placeholder": "████小区A"},
    {"keyword": "张雅琪", "placeholder": "████姓名A"},
    {"keyword": "13867925618", "placeholder": "████手机A"},
    # PDF 关键词建议同时添加空格/无空格版本
    {"keyword": "税前18600 元", "placeholder": "████薪资A"},
    {"keyword": "税前 18600 元", "placeholder": "████薪资A"},
]
```

**优势**：
- 零误差：精确字符串匹配，不依赖正则
- 防碎片化：不会被文本分块/OCR 拆分影响
- 快速：单次遍历，O(n) 复杂度

---

## 8. Configuration (`privacy-config.json`)

```json
{
  "privacy": {
    "redaction_marker": "<<REDACTED_{type}_{index}>>",
    "marker_style": "angle"
  },
  "sensitive_types": {
    "NAME": true, "PHONE": true, "EMAIL": true,
    "ID": true, "CREDIT_CARD": true,
    "PASSPORT": true, "FRAGMENT": true, "USERNAME": true,
    "ADDRESS": true, "IP": true,
    "API_KEY": true, "MONEY": true, "COMPANY_NAME": true,
    "CUSTOM": true
  },
  "keyword_rules": [
    {"keyword": "张雅琪", "placeholder": "████姓名A"}
  ],
  "custom_patterns": [
    {"type": "CUSTOM", "pattern": "\\bsecret\\d+\\b"}
  ],
  "output": {
    "save_file": true,
    "suffix": "_redacted"
  }
}
```

---

## 9. 文件处理说明

| 格式 | 方法 | 说明 |
|------|------|------|
| `.docx` | `write_with_mapping()` | 关键词精准替换，保留段落/表格结构 |
| `.pdf` | `redact_image_level()` | 图像级遮盖，OCR 验证，零残留 |
| `.xlsx` | 正则模式 | 正则替换，保留 Excel 格式 |
| `.md` | 直接替换 | 文本替换，直接保存 |
| `.jpg/.png` | `pytesseract` | OCR 识别文字区域 + 像素级遮盖 |

---

## 10. `redact_multi_format` 全格式脱敏管道（v1.3 新增）

### 适用场景
PDF 或图片文件需要**多格式输出**时使用。一条命令产出 6 种形式的结果：

| # | 输出 | 格式 | 说明 |
|---|------|------|------|
| 1 | `OCR脱敏.txt` | TXT | OCR 识别原文 → 脱敏，覆盖图形化文本 |
| 2 | `脱敏版.pdf` | PDF | 图像级黑框遮盖，视觉零残留 |
| 3 | `脱敏版.docx` | DOCX | PDF → Word 转换 → 脱敏，可编辑 |
| 4 | `脱敏版.md` | MD | PDF → Markdown 转换 → 脱敏，可编辑 |
| 5 | `汇总映射表.json` | JSON | 所有脱敏项的完整映射（用于还原） |
| 6 | `反脱敏指南.txt` | TXT | 含还原命令的实操文档 |

### 调用方式

```bash
echo '{"action":"redact_multi_format","file_path":"报告.pdf","keyword_rules":[
  {"keyword":"张雅琪","placeholder":"████姓名A"},
  {"keyword":"13867925618","placeholder":"████手机A"}
]}' | python3 scripts/main.py
```

### 完整流程图

```
用户请求
    │
    ▼
┌─────────────────────────────────┐
│      redact_multi_format        │
│  ┌──────────────────────────┐   │
│  │ Step 1: OCR → 脱敏       │   │
│  │   PDF渲染为高清图片       │   │
│  │   pytesseract OCR 提取文本│   │
│  │   redact_hybrid() 脱敏    │   │
│  │   输出: OCR脱敏.txt       │   │
│  └──────────────────────────┘   │
│  ┌──────────────────────────┐   │
│  │ Step 2: PDF 图像级遮盖   │   │
│  │   PyMuPDF 坐标提取       │   │
│  │   PIL 全行黑条遮盖       │   │
│  │   fitz 嵌入回 PDF        │   │
│  │   输出: 脱敏版.pdf        │   │
│  └──────────────────────────┘   │
│  ┌──────────────────────────┐   │
│  │ Step 3: PDF → DOCX 脱敏  │   │
│  │   pdf2docx 转换格式      │   │
│  │   write_with_mapping()   │   │
│  │   输出: 脱敏版.docx       │   │
│  └──────────────────────────┘   │
│  ┌──────────────────────────┐   │
│  │ Step 4: PDF → MD 脱敏    │   │
│  │   PyMuPDF 文本提取       │   │
│  │   redact_hybrid() 脱敏    │   │
│  │   输出: 脱敏版.md         │   │
│  └──────────────────────────┘   │
│  ┌──────────────────────────┐   │
│  │ Step 5: 汇总输出         │   │
│  │   汇总映射表.json         │   │
│  │   反脱敏指南.txt          │   │
│  └──────────────────────────┘   │
└─────────────────────────────────┘
```

### 注意事项

1. **OCR 为第一道防线**：PDF 的文字层可能不完整（字体缺失、坐标偏差），OCR 提供首选文本来源
2. **各格式独立脱敏**：每个格式都独立应用 `redact_hybrid()`，确保没有遗漏
3. **非致命失败**：DOCX 转换（pdf2docx）可能因复杂布局失败，不影响其他格式输出
4. **映射表去重**：跨格式的相同敏感词只保留一条映射记录
5. **反脱敏指南**：包含完整 `unmask` 命令，粘贴即可用
