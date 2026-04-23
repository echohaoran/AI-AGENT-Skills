[**中文**](./README.md) | English

---

# Privacy Shield

Local sensitive data redaction and unmasking tool. Communicates with Agent via OpenClaw Skill protocol, compatible with all Agent runtimes.

## Features

- **Sensitive Data Detection**: Automatically identifies names, phones, emails, IDs, credit cards, addresses, IPs
- **Reversible Redaction**: Replaces with markers, fully restored after LLM processing
- **Multi-format Support**: PDF, Excel, Word, Markdown, Images (OCR)
- **Zero API Calls**: All processing is local, no raw data is uploaded

## Installation

### One-Click Install (Recommended)

Copy the link below and give it to OpenClaw or your Agent — it will auto-clone and deploy:

```
hCheck out this repository: https://github.com/echohaoran/awesome-privacy-skill, and install this skill according to the repository instructions.
```

### Manual Install

```bash
# Clone the repo
git clone https://github.com/echohaoran/awesome-privacy-skill
cd awesome-privacy-skill

# Install Python dependencies
pip install -r requirements.txt

# OCR for images
brew install tesseract          # macOS
apt-get install tesseract-ocr    # Ubuntu/Debian
```

### Dependency List

| Package | Purpose |
|---------|---------|
| pypdf | PDF text extraction |
| openpyxl | Excel cell reading |
| python-docx | Word document reading |
| Pillow | Image processing |
| pytesseract | OCR text recognition |

Optional OCR engines (install one):
- `paddleocr` — Fast, great Chinese/English support
- `rapidocr-onnxruntime` — Cross-platform, no extra dependencies

## How to Use

### As an OpenClaw Skill

1. Clone this repo locally
2. Install dependencies: `pip install -r requirements.txt`
3. Register this Skill in your Agent environment
4. Agent will automatically recognize triggers and invoke it

### Agent Workflow

```
Phase A: Redact
  Agent → scripts/main.py (redact_file / redact_content)
        → get redacted_content + mapping

Phase B: LLM Processing
  Agent → send redacted_content to LLM
        → get LLM response

Phase C: Unmask
  Agent → scripts/main.py (unmask)
        → get restored content
```

### Script Protocol

Call `scripts/main.py` via stdin/stdout JSON:

```bash
# Redact file
echo '{"action":"redact_file","file_path":"doc.pdf"}' | python scripts/main.py

# Redact content
echo '{"action":"redact_content","content":"John 13812345678 user@example.com"}' | python scripts/main.py

# Unmask
echo '{"action":"unmask","content":"<<REDACTED_PHONE_1>>","mapping":[{"type":"PHONE","index":1,"original":"13812345678","marker":"<<REDACTED_PHONE_1>>"}]}' | python scripts/main.py

# Detect only
echo '{"action":"detect","content":"..."}' | python scripts/main.py
```

### Response Format

**Redaction success:**
```json
{
  "status": "success",
  "redacted_content": "John <<REDACTED_PHONE_1>>",
  "mapping": [
    {"type": "PHONE", "index": 1, "original": "13812345678", "marker": "<<REDACTED_PHONE_1>>"}
  ]
}
```

**Unmask success:**
```json
{
  "status": "success",
  "restored_content": "John 13812345678",
  "unmasked_count": 1
}
```

## How It Works

```
Original → Detect → Redact (markers + mapping)
        → Send to LLM → LLM processes
        → Receive response → Unmask (mapping restore) → Final content
```

1. **Detect**: Scan content with regex patterns to identify sensitive data types
2. **Redact**: Replace sensitive data with `<<REDACTED_TYPE_INDEX>>` markers, generate mapping
3. **LLM**: Agent sends redacted content to LLM, all markers remain unchanged
4. **Unmask**: Restore all markers to original data using the mapping

## Sensitive Data Types

| Type | Example |
|------|---------|
| NAME | John Smith |
| PHONE | 13812345678、555-123-4567 |
| EMAIL | user@example.com |
| ID | Chinese ID, SSN |
| CREDIT_CARD | `4111****1111` (partial redaction) |
| ADDRESS | 123 Main Street、Beijing Chaoyang District |
| IP | 192.168.1.1 |
| API_KEY | `sk-xxx`, Bearer token, JWT |
| MONEY | `$100`, `10,000 CNY` |
| COMPANY_NAME | `Beijing**** Co., Ltd.` (partial redaction) |
| CUSTOM | User-defined via config |

## Configuration

Create `privacy-config.json` to customize behavior:

```json
{
  "sensitive_types": {
    "NAME": true,
    "PHONE": true,
    "EMAIL": true
  },
  "custom_patterns": [
    {"type": "CUSTOM", "pattern": "\\b[A-Z]{2}\\d{6}\\b"}
  ]
}
```

## Project Structure

```
awesome-privacy-skill/
├── skill.json              # OpenClaw registry manifest
├── SKILL.md               # Agent instruction logic
├── package.json           # npm distribution config
├── assets/               # Static resources
├── scripts/
│   ├── main.py           # Action protocol entry
│   ├── core/             # Detection, redaction, unmasking
│   ├── handlers/         # File format handlers
│   └── config/           # Configuration
└── requirements.txt
```

## Demo

### Original
> The following content is for illustrative purposes only
![alt text](assets/原文.png)

### Redaction Mapping
![alt text](assets/映射表.png)

### Redacted Result
![alt text](assets/结果.png)

---

## Issues & Feedback

Found a bug or have a feature request? Submit an [Issue](https://github.com/echohaoran/awesome-privacy-skill/issues).

## License

MIT
