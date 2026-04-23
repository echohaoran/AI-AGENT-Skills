"""
Sensitive data detection patterns and constants.
"""

import re

NAME_PATTERNS = [
    r'\b[A-Z][a-z]+ [A-Z][a-z]+\b',
    r'\b[A-Z][a-z]+ [A-Z]\. [A-Z][a-z]+\b',
    r'\b[A-Z][a-z]+·[A-Z][a-z]+ [A-Z][a-z]+\b',
]

PHONE_PATTERNS = [
    r'1[3-9]\d{9}',
    r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
    r'\+\d{1,3}[-.\s]?\d{1,14}',
    r'\(\d{3}\)\s*\d{3}[-.]?\d{4}',
]

# Note: no \b boundary — Python \b fails at Chinese/ASCII transitions
EMAIL_PATTERN = r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'

# Note: no \b boundary — Python \b fails at Chinese/ASCII transitions
CHINESE_ID_PATTERN = r'[1-9]\d{5}(?:19|20)\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])\d{3}[\dXx]'
# Require separator for SSN to avoid false positives (e.g. phone numbers)
SSN_PATTERN = r'\d{3}[-\s]\d{2}[-\s]\d{4}'

CREDIT_CARD_PATTERNS = [
    r'\b4\d{3}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b',
    r'\b5[1-5]\d{2}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b',
    r'\b3[47]\d{2}[-\s]?\d{6}[-\s]?\d{5}\b',
    r'\b6(?:011|5\d{2})[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b',
]

IP_PATTERN = r'\b(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\b'

# Company name patterns — common suffixes and multi-word organization names
COMPANY_NAME_PATTERNS = [
    # Chinese company suffixes
    r'[\u4e00-\u9fa5]{4,}(?:有限公司|股份有限公司|集团有限公司|科技有限公司|信息技术有限公司|网络科技有限公司|电子科技有限公司|实业有限公司|投资有限公司|商贸有限公司|贸易有限公司|进出口有限公司|房地产开发有限公司|建设工程有限公司|装饰工程有限公司|咨询有限公司|管理咨询有限公司|保险代理有限公司|金融服务有限公司|基金管理有限公司|资产管理有限公司|租赁有限公司|运输有限公司|物流有限公司|仓储有限公司|包装有限公司|印刷有限公司|服装有限公司|纺织有限公司|建材有限公司|化工有限公司|医药有限公司|医疗器械有限公司|食品有限公司|饮料有限公司|酒店管理有限公司|物业管理有限公司|园林工程有限公司|广告有限公司|传媒有限公司|文化传播有限公司|教育咨询有限公司|培训有限公司|律师事务所|会计师事务所|税务师事务所|评估有限公司|认证服务有限公司|检测有限公司|研究院|研究中心|研究所|实验室|检测中心|技术中心|研发中心|设计院|规划院|工程院)',
    # English company suffixes
    r'\b[A-Z][A-Za-z0-9\s&.,]+(?:Ltd\.|LLC|Inc\.|Corp\.|Corporation|Company|Co\.|Group|Holdings|International|Technologies|Technology|Systems|Solutions|Consulting|Services|Limited)\b',
    # Common short organization patterns (Chinese)
    r'(?:腾讯|阿里巴巴|字节跳动|百度|京东|美团|滴滴|网易|华为|小米|OPPO|VIVO|海尔|格力|比亚迪|蔚来|理想|小鹏|拼多多|快手|哔哩哔哩|知乎|小红书|微博|抖音|今日头条|钉钉|飞书|企业微信|招商银行|工商银行|建设银行|农业银行|中国银行|交通银行|平安保险|中国人寿|太平洋保险)',
]

API_KEY_PATTERNS = [
    # Generic API key formats
    r'\b(?:api[_-]?key|apikey|api[_-]?secret|api[_-]?token)\s*[:=]\s*["\']?[\w\-\.]{16,64}["\']?',
    # Common prefixed API keys
    r'\b(?:sk|ak|api|key|token|secret|password|passwd|pwd)\s*[-_]\s*[\w\-\.]{16,64}\b',
    # Bearer tokens
    r'\b[Bb]earer\s+[A-Za-z0-9\-\._~\+\/]{20,}\b',
    # Auth tokens in Authorization header style
    r'\b[Aa]uthorization\s*:\s*(?:Bearer|Basic|Digest)\s+[\w\-\.]{16,}\b',
    # Long alphanumeric tokens (likely JWT, access tokens)
    r'\beyJ[A-Za-z0-9_\-]+\.eyJ[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+\b',
    # AWS keys
    r'\b(?:AKIA|A3T|AGPA|AIDA|AROA|AIPA|ANPA|ANVA|ASIA)[A-Z0-9]{16}\b',
    # GitHub tokens
    r'\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9_]{36,}\b',
    # OpenAI / generic sk- prefixed keys
    r'\bsk[-_\w]{20,64}\b',
    # Stripe keys
    r'\b(?:sk|pk|rk)_(?:test|live)_[A-Za-z0-9]{24,}\b',
    # Slack tokens
    r'\bxox[baprs]-[0-9]{10,13}-[0-9]{10,13}-[A-Za-z0-9]{24,}\b',
    # Firebase / Google service account
    r'\b[A-Za-z0-9\-_]+\.iam\.gserviceaccount\.com\b',
    # Private key blocks
    r'-----BEGIN (?:RSA |EC |DSA |OPENSSH |PGP )?PRIVATE KEY-----',
    # Generic long secret strings (≥24 chars, high entropy indicator)
    r'(?i)(?:secret|password|token|credential)\s*[:=]\s*["\']?[A-Za-z0-9\/\+=]{24,64}["\']?',
]

# Money / currency patterns
MONEY_PATTERNS = [
    # Currency symbols + amount (with or without comma separators)
    r'[\$¥€£₹₽₩¥]\s*\d+(?:[,，]\d{3})*(?:\.\d{1,2})?',
    # Amount + currency symbols (ASCII)
    r'\d+(?:[,，]\d{3})*(?:\.\d{1,2})?\s*[\$¥€£₹₽₩]',
    # Amount + Chinese currency unit (use \d+ to correctly match large numbers)
    r'\d+(?:[,，]\d{3})*(?:\.\d{1,2})?\s*(?:人民币|美元|欧元|英镑|日元|韩元|澳元|加元|元|块|刀)',
    # Chinese currency name + amount
    r'(?:人民币|美元|欧元|英镑|日元|韩元|澳元|加元|元)\s*\d+(?:[,，]\d{3})*(?:\.\d{1,2})?',
    # Financial keywords + amount (symbol optional, use \d+ for large numbers)
    r'(?:价格|金额|付款|支付|收款|转账|余额|费用|工资|薪资|收入|支出|利润|亏损|成本|报价|账单)\s*[:：]?\s*[\$¥€£₹₽₩]?\s*\d+(?:[,，]\d{3})*(?:\.\d{1,2})?',
    # Symbol + amount + Chinese unit
    r'[\$¥€£₹₽₩¥]?\s*\d+(?:[,，]\d{3})*(?:\.\d{1,2})?\s*(?:元|美元|欧元|英镑|人民币|日元|韩元|万|亿)',
    # Pure numeric amounts (≥12 digits, bounded — 11-digit phone numbers excluded)
    r'(?<![0-9,，])\d{12,}(?![0-9])',
    # Numbers followed by Chinese magnitude units: 1亿, 100万 (use \d+ for large numbers)
    r'\d+(?:[,，]\d{3})*(?:\.\d{1,2})?\s*(?:万|亿|万亿)元?',
]

ADDRESS_PATTERNS = [
    r'\b\d+\s+[\w\s]+(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Lane|Ln|Drive|Dr)\.?\b',
    r'[\u4e00-\u9fa5]+(?:省|市|区|县|街|路|巷|号|弄|栋|楼|单元)[^\n]{5,50}',
]

URL_PATTERN = r'https?://[^\s<>"{}|\\^`\[\]]+'

# Specificity: higher value wins when patterns overlap
# CREDIT_CARD > ID > EMAIL > PHONE > IP > ADDRESS > NAME > URL
SPECIFICITY = {
    "CREDIT_CARD": 80,
    "ID": 70,
    "EMAIL": 60,
    "PHONE": 50,
    "IP": 40,
    "ADDRESS": 30,
    "NAME": 20,
    "URL": 10,
    "CUSTOM": 25,
    "API_KEY": 65,
    "MONEY": 55,
    "COMPANY_NAME": 25,
}

SENSITIVE_PATTERNS = {
    "NAME": [re.compile(p) for p in NAME_PATTERNS],
    "PHONE": [re.compile(p) for p in PHONE_PATTERNS],
    "EMAIL": [re.compile(EMAIL_PATTERN)],
    "ID": [re.compile(CHINESE_ID_PATTERN), re.compile(SSN_PATTERN)],
    "CREDIT_CARD": [re.compile(p) for p in CREDIT_CARD_PATTERNS],
    "IP": [re.compile(IP_PATTERN)],
    "ADDRESS": [re.compile(p, re.MULTILINE) for p in ADDRESS_PATTERNS],
    "URL": [re.compile(URL_PATTERN)],
    "API_KEY": [re.compile(p, re.IGNORECASE) for p in API_KEY_PATTERNS],
    "MONEY": [re.compile(p) for p in MONEY_PATTERNS],
    "COMPANY_NAME": [re.compile(p) for p in COMPANY_NAME_PATTERNS],
}

# Types that use partial masking (show first+last chars with **** in middle)
# Original value is still preserved in mapping for full reversibility
PARTIAL_MASK_TYPES = {"CREDIT_CARD", "COMPANY_NAME"}

REDACTION_MARKER = "<<REDACTED_{type}_{index}>>"
