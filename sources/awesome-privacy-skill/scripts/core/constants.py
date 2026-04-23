"""
Sensitive data detection patterns and constants.

Key design decisions:
- \b word boundaries are NOT used for Chinese/ASCII mixed text.
  Python's \b fails at Chinese→ASCII transitions (e.g. "卡6222..." fails \b).
  Instead, (?<!\d)(?!\d) lookarounds are used for numeric patterns.
- Rules are sorted by length (longest first) during replacement to prevent
  short patterns from consuming parts of longer sensitive keywords.
- SPECIFICITY: higher value wins when patterns overlap.
"""

import re

# ─────────────────────────────────────────────
# NAME patterns (English + common Chinese)
# ─────────────────────────────────────────────
NAME_PATTERNS = [
    # English names: "John Smith"
    r'\b[A-Z][a-z]+ [A-Z][a-z]+\b',
    # English names with middle initial: "John A. Smith"
    r'\b[A-Z][a-z]+ [A-Z]\. [A-Z][a-z]+\b',
    # Chinese pinyin names: "Zhang Wei"
    r'\b[A-Z][a-z]{2,10} [A-Z][a-z]{2,10}\b',
]

# ─────────────────────────────────────────────
# PHONE patterns (global coverage)
# ─────────────────────────────────────────────
PHONE_PATTERNS = [
    # China mobile: 1[3-9]xxxxxxxxx
    r'1[3-9]\d{9}',
    # China mobile with separators
    r'1[3-9][-\s]?\d{4}[-\s]?\d{4}',
    # US/Canada: (xxx) xxx-xxxx or xxx-xxx-xxxx
    r'\(\d{3}\)\s*\d{3}[-.]?\d{4}',
    r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
    # International: +xx xxx xxxx
    r'\+\d{1,3}[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}',
]

# ─────────────────────────────────────────────
# EMAIL pattern
# ─────────────────────────────────────────────
EMAIL_PATTERN = r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'

# ─────────────────────────────────────────────
# ID patterns (China + SSN)
# ─────────────────────────────────────────────
# China ID: 18 digits, born 1900-2099, with optional X
# Note: no \b — use (?<!\d)(?!\d) for Chinese context compatibility
CHINESE_ID_PATTERN = r'[1-9]\d{5}(?:19|20)\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])\d{3}[\dXx]'
# US SSN: requires separator to avoid matching phone numbers
SSN_PATTERN = r'\d{3}[-\s]\d{2}[-\s]\d{4}'

# ─────────────────────────────────────────────
# CREDIT CARD patterns
# Uses (?<!\d)(?!\d) instead of \b for Chinese context compatibility.
# Supports 13-19 digit cards (international + Chinese UnionPay).
# ─────────────────────────────────────────────
CREDIT_CARD_PATTERNS = [
    # Visa: 4xxx xxxx xxxx xxxx
    r'(?<!\d)4\d{3}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}(?!\d)',
    # Mastercard: 51-55xx or 2221-2720
    r'(?<!\d)5[1-5]\d{2}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}(?!\d)',
    # Amex: 34xx or 37xx
    r'(?<!\d)3[47]\d{2}[-\s]?\d{6}[-\s]?\d{5}(?!\d)',
    # Discover: 6011 or 65xx
    r'(?<!\d)6(?:011|5\d{2})[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}(?!\d)',
    # China UnionPay (62xxx, 13-19 digits)
    r'(?<!\d)62\d{12,19}(?!\d)',
    # Generic 6xxx cards (13-19 digits)
    r'(?<!\d)6\d{12,19}(?!\d)',
]

# ─────────────────────────────────────────────
# IP ADDRESS patterns
# ─────────────────────────────────────────────
IP_PATTERN = r'(?<!\d)(?:(?:25[0-5]|2[0-4]\d|1?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|1?\d\d?)(?!\d)'

# ─────────────────────────────────────────────
# COMPANY NAME patterns
# Company name is lower specificity (25) to allow more specific types
# (ID, EMAIL, PHONE) to take priority when they co-occur.
# ─────────────────────────────────────────────
COMPANY_NAME_PATTERNS = [
    # Chinese company suffixes (60+ common types — v1.2 新增12种)
    r'[\u4e00-\u9fa5]{2,30}(?:有限公司|股份有限公司|集团有限公司|科技有限公司|信息技术有限公司|网络科技有限公司|电子科技有限公司|实业有限公司|投资有限公司|商贸有限公司|贸易有限公司|进出口有限公司|房地产开发有限公司|建设工程有限公司|装饰工程有限公司|咨询有限公司|管理咨询有限公司|保险代理有限公司|金融服务有限公司|基金管理有限公司|资产管理有限公司|租赁有限公司|运输有限公司|物流有限公司|仓储有限公司|包装有限公司|印刷有限公司|服装有限公司|纺织有限公司|建材有限公司|化工有限公司|医药有限公司|医疗器械有限公司|食品有限公司|饮料有限公司|酒店管理有限公司|物业管理有限公司|园林工程有限公司|广告有限公司|传媒有限公司|文化传播有限公司|教育咨询有限公司|培训有限公司|律师事务所|会计师事务所|税务师事务所|评估有限公司|认证服务有限公司|检测有限公司|研究院|研究中心|研究所|实验室|检测中心|技术中心|研发中心|设计院|规划院|工程院|数字科技有限公司|科技咨询有限公司|软件技术有限公司)',
    # English company suffixes
    r'\b[A-Z][A-Za-z0-9\s&.,]*(?:Ltd\.|LLC|Inc\.|Corp\.|Corporation|Company|Co\.|Group|Holdings|International|Technologies|Technology|Systems|Solutions|Consulting|Services|Limited)\b',
    # Well-known Chinese organizations
    r'(?:腾讯|阿里巴巴|字节跳动|百度|京东|美团|滴滴|网易|华为|小米|OPPO|VIVO|海尔|格力|比亚迪|蔚来|理想|小鹏|拼多多|快手|哔哩哔哩|知乎|小红书|微博|抖音|今日头条|钉钉|飞书|企业微信|招商银行|工商银行|建设银行|农业银行|中国银行|交通银行|平安保险|中国人寿|太平洋保险|浙江大学|清华大学|北京大学)',
]

# ─────────────────────────────────────────────
# API KEY / SECRET / TOKEN patterns
# ─────────────────────────────────────────────
API_KEY_PATTERNS = [
    # Generic: api_key: "value" or api_key = value
    r'(?:api[_-]?key|apikey|api[_-]?secret|api[_-]?token)\s*[:=]\s*["\']?[\w\-\.]{8,64}["\']?',
    # Common prefixes: sk-, ak-, key-, token-
    r'(?:sk|ak|api|key|token|secret|password|passwd|pwd)[-_][\w\-\.]{8,64}',
    # Bearer tokens
    r'[Bb]earer\s+[A-Za-z0-9\-\._~\+\/]{16,}',
    # Authorization header
    r'[Aa]uthorization\s*:\s*(?:Bearer|Basic|Digest)\s+[\w\-\.]{16,}',
    # JWT tokens
    r'eyJ[A-Za-z0-9_\-]+\.eyJ[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+',
    # AWS access keys
    r'(?:AKIA|A3T|AGPA|AIDA|AROA|AIPA|ANPA|ANVA|ASIA)[A-Z0-9]{16}',
    # GitHub tokens: ghp_, gho_, ghu_, ghs_, ghr_
    r'(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9_]{10,}',
    # OpenAI / generic sk- keys
    r'\bsk[-_][\w]{16,64}',
    # Stripe keys
    r'(?:sk|pk|rk)_(?:test|live)_[A-Za-z0-9]{24,}',
    # Slack tokens
    r'xox[baprs]-[0-9]{10,13}-[0-9]{10,13}-[A-Za-z0-9]{24,}',
    # Firebase / Google service account
    r'[A-Za-z0-9\-_]+\.iam\.gserviceaccount\.com',
    # Private key blocks
    r'-----BEGIN (?:RSA |EC |DSA |OPENSSH |PGP )?PRIVATE KEY-----',
    # Password fields in config/database contexts
    r'(?:password|passwd|pwd|secret|credential)\s*[:=]\s*["\']?[A-Za-z0-9\/\+=@#$%^&*!.\-]{6,64}["\']?',
]

# ─────────────────────────────────────────────
# MONEY / CURRENCY patterns
# ─────────────────────────────────────────────
MONEY_PATTERNS = [
    # Currency symbols + amount: $1,000 / ¥1000 / €500
    r'[\$¥€£₹₽₩]\s*\d+(?:[,，]?\d{3})*(?:\.\d{1,2})?',
    # Amount + currency symbol: 1000$ / 1000¥
    r'\d+(?:[,，]?\d{3})*(?:\.\d{1,2})?\s*[\$¥€£₹₽₩]',
    # Amount + Chinese currency: 1000元 / 1000美元 / 1000人民币
    r'\d+(?:[,，]?\d{3})*(?:\.\d{1,2})?\s*(?:元|美元|欧元|英镑|日元|韩元|澳元|加元|港币|人民币)',
    # Chinese currency + amount: 一千元 / 一万元 (handled separately)
    # Financial keywords + amount
    r'(?:价格|金额|付款|支付|收款|转账|余额|费用|工资|薪资|收入|支出|利润|亏损|成本|报价|账单|预算|报销)\s*[:：]?\s*[\$¥€£₹₽₩]?\s*\d+(?:[,，]?\d{3})*(?:\.\d{1,2})?',
    # Pure numeric amounts ≥12 digits (bounded — excludes 11-digit phones)
    r'(?<![0-9,　])\d{12,}(?![0-9])',
    # Large number with Chinese magnitude units: 1亿, 100万
    r'\d+(?:[,，]\d{3})*(?:\.\d{1,2})?\s*(?:万|亿|万亿)元?',
]

# ─────────────────────────────────────────────
# ADDRESS patterns
# Uses (?<!\w)(?!\w) instead of \b for Chinese context.
# Lower specificity (20) — high-specificity types take priority.

# v1.2 新增：护照、通行证、驾照编号模式（实测发现）
PASSPORT_PATTERNS = [
    # 中国普通护照: E + 8位字母数字
    r'(?<!\d)E\d{8}(?!\d)',
    # 往来港澳通行证: W + 8位
    r'(?<!\d)W\d{8}(?!\d)',
    # 往来台湾通行证: S + 8位
    r'(?<!\d)S\d{8}(?!\d)',
    # 中国驾驶证编号: 12位数字（含省份代码）
    r'(?<!\d)\d{12}(?!\d)',
]


# ─────────────────────────────────────────────
# 实战补充：长数字串模式（v1.2 新增）
# 用于检测 PDF/OCR 中被拆分的长编号
# ─────────────────────────────────────────────
FRAGMENT_PATTERNS = [
    # 10-11位手机号（可能被OCR拆分）
    r'(?<!\d)\d{10,11}(?!\d)',
    # 15-19位银行卡/账号（可能被OCR拆分）
    r'(?<!\d)\d{15,19}(?!\d)',
    # 18位身份证（可能被OCR拆分）
    r'(?<!\d)\d{17}[\dXx](?!\d)',
    # 6位短码（密码、验证码等）
    r'(?<!\d)\d{6}(?!\d)',
]

# ─────────────────────────────────────────────
# 实战补充：通用账号/用户名模式（v1.2 新增）
# ─────────────────────────────────────────────
USERNAME_PATTERNS = [
    # 社交媒体账号: @username 或纯英文用户名
    r'@[\w\-]{3,20}',
    # OA/内部系统账号: 纯小写字母+数字组合
    r'\b[a-z][a-z0-9]{2,15}\b',
    # 微信号: wxid_开头
    r'wxid_[\w]{8,}',
]
# ─────────────────────────────────────────────
ADDRESS_PATTERNS = [
    # English: 123 Main Street, 456 Oak Ave
    r'\b\d+\s+[\w\s]+(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Lane|Ln|Drive|Dr|Court|Ct|Circle|Cir)\.?\b',
    # Chinese province-city-district: 浙江省杭州市西湖区...
    r'[\u4e00-\u9fa5]{2,6}(?:省|市|自治区|特别行政区)?[\u4e00-\u9fa5]{2,10}(?:市|区|县)?[\u4e00-\u9fa5]{2,20}',
    # Chinese detailed address: ...路/街...号...栋/楼/室
    r'[\u4e00-\u9fa5]+(?:省|市|区|县|街|路|巷|道|号|弄|栋|楼|层|单元|室)[^\n]{3,80}',
]

# ─────────────────────────────────────────────
# URL pattern
# ─────────────────────────────────────────────
URL_PATTERN = r'https?://[^\s<>"{}|\\^`\[\]]+'

# ─────────────────────────────────────────────
# Specificity ranking (higher wins on overlap)
# ─────────────────────────────────────────────
SPECIFICITY = {
    "CREDIT_CARD": 80,
    "ID": 70,
    "API_KEY": 65,
    "EMAIL": 60,
    "MONEY": 55,
    "PHONE": 50,
    "IP": 40,
    "PASSPORT": 45,       # v1.2 新增：护照/通行证/驾照
    "FRAGMENT": 35,       # v1.2 新增：长数字串（可能被拆分）
    "USERNAME": 30,       # v1.2 新增：通用账号/微信号
    "ADDRESS": 10,        # Low — too broad, avoid matching company names
    "NAME": 20,
    "URL": 10,
    "CUSTOM": 25,
    "COMPANY_NAME": 30,   # 高于 ADDRESS，防止公司名被误判为地址
}

# ─────────────────────────────────────────────
# All patterns compiled for detection
# ─────────────────────────────────────────────
SENSITIVE_PATTERNS = {
    "NAME": [re.compile(p) for p in NAME_PATTERNS],
    "PHONE": [re.compile(p) for p in PHONE_PATTERNS],
    "EMAIL": [re.compile(EMAIL_PATTERN)],
    "ID": [re.compile(CHINESE_ID_PATTERN), re.compile(SSN_PATTERN)],
    "CREDIT_CARD": [re.compile(p) for p in CREDIT_CARD_PATTERNS],
    "IP": [re.compile(IP_PATTERN)],
    "PASSPORT": [re.compile(p) for p in PASSPORT_PATTERNS],      # v1.2
    "FRAGMENT": [re.compile(p) for p in FRAGMENT_PATTERNS],       # v1.2
    "USERNAME": [re.compile(p) for p in USERNAME_PATTERNS],       # v1.2
    "ADDRESS": [re.compile(p, re.MULTILINE) for p in ADDRESS_PATTERNS],
    "URL": [re.compile(URL_PATTERN)],
    "API_KEY": [re.compile(p, re.IGNORECASE) for p in API_KEY_PATTERNS],
    "MONEY": [re.compile(p) for p in MONEY_PATTERNS],
    "COMPANY_NAME": [re.compile(p) for p in COMPANY_NAME_PATTERNS],
}

# ─────────────────────────────────────────────
# Partial mask: show first+last chars with **** in middle
# ─────────────────────────────────────────────
PARTIAL_MASK_TYPES = {"CREDIT_CARD", "COMPANY_NAME"}

# ─────────────────────────────────────────────
# Redaction marker format
# ─────────────────────────────────────────────
REDACTION_MARKER = "<<REDACTED_{type}_{index}>>"
