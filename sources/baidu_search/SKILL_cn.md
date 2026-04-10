---
title: 百度搜索
excerpt: 使用百度搜索引擎进行网络搜索，便于发现中文互联网内容。
date: 2026-04-09
---

SKILL.md
百度搜索

使用百度搜索引擎进行网络搜索，便于发现中文互联网内容。

何时使用

✅ 使用此技能的场景：

    "用百度搜索 [主题]"
    "查找中文网页结果"
    "搜索中文新闻"
    "获取中国市场数据"
    "研究中文资料"

何时不使用

❌ 不要使用此技能的场景：

    需要全球搜索结果（使用 tavily-search 或 web-search）
    需要图片/视频搜索（使用百度媒体 API）
    需要实时股票数据（使用金融数据 API）
    学术论文（使用知网或专用学术搜索）

快速开始

# 基本搜索
baidu search "人工智能发展趋势"

# 带语言过滤器
baidu search "科技新闻" --lang zh

# 获取前 10 条结果
baidu search "Python 教程" --num 10 --format json

核心命令

搜索

baidu search "查询词"                    # 基本搜索
baidu search "查询词" --num 20            # 自定义结果数量
baidu search "查询词" --format json       # JSON 输出
baidu search "查询词" --lang zh           # 仅中文结果

新闻

baidu news "话题"                       # 最新新闻
baidu news "话题" --days 7              # 最近 7 天
baidu news "话题" --category tech       # 按类别

图片

baidu image "查询词"                      # 图片搜索
baidu image "查询词" --num 20             # 自定义数量
baidu image "查询词" --size large         # 按尺寸

高级搜索

baidu search "查询词" --site example.com  # 站内搜索
baidu search "查询词" --filetype pdf      # 文件类型筛选
baidu search "查询词" --exclude "关键词" # 排除词

输出格式

JSON

{
  "query": "搜索词",
  "results": [
    {
      "title": "结果标题",
      "url": "https://example.com",
      "snippet": "描述...",
      "source": "网站名称",
      "date": "2024-01-15"
    }
  ],
  "total": 1000,
  "page": 1
}

Markdown

**结果标题**
链接: https://example.com
来源: 网站名称 | 日期: 2024-01-15

结果的描述...

配置

export BAIDU_API_KEY="your_api_key"
export BAIDU_SEARCH_ENDPOINT="https://api.baidu.com/search"

速率限制

    免费版：100 次搜索/天
    付费版：1000 次搜索/分钟
    图片搜索：500 次搜索/天

最佳实践

    使用中文关键词以获得更好的结果
    结合翻译技能进行跨语言研究
    缓存频繁搜索以减少 API 使用
    使用 site: 操作符进行站内搜索

故障排除

常见问题

    无结果 - 尝试更广泛的关键词或移除过滤器
    速率限制 - 等待并使用指数退避重试
    API 密钥无效 - 检查配置

相关技能

    tavily-search - 全球网络搜索
    translate - 语言翻译
    web-research - 研究自动化
