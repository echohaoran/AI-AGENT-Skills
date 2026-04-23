---
name: web-search
description: Search the web for information using the built-in WebSearch tool. Use when users ask questions requiring up-to-date information, research, or fact-checking.
allowed-tools:
  - Bash
  - WebSearch
  - WebFetch
---

# Web Search Skill

Search the web using the **built-in WebSearch tool**. It uses Electron's BrowserWindow to perform searches, handling JavaScript-rendered search results and bypassing basic anti-bot measures. This is NOT a simple HTTP request — it opens the page in a real browser window, performs the search, and extracts results from the rendered page.

## WebSearch Tool (Primary)

```
WebSearch(query="your search query", max_results=5)
```

- Supports multiple search engines (Google, Bing, DuckDuckGo, etc.)
- Handles JavaScript-rendered pages
- Returns structured results with title, URL, snippet, and markdown content
- Automatic CAPTCHA detection and user notification

## Fetching Page Content

After finding URLs from search, use the **WebFetch** tool to get the actual page content:

```
WebFetch(url="https://example.com/article", prompt="Extract the main content")
```

- Renders pages in a real browser with full JavaScript execution
- Handles SPAs, dynamic content, and anti-bot protections
- Returns clean markdown

## Browser Skill (Fallback)

If WebSearch or WebFetch fail (e.g., page requires login, CAPTCHA, or multi-step navigation), fall back to the Browser Skill:

```bash
# Open URL in a real Chrome browser tab
alma browser open "https://example.com"

# Read the page content as markdown
alma browser read <tabId>
```

The Browser Skill uses Chrome Relay to control the user's real Chrome browser with existing sessions, cookies, and logins.

## Tips

- For complex queries, try multiple search approaches
- Always summarize findings for the user rather than dumping raw results
- For freshness queries (`today`, `latest`, `今天`, `最新`), use the **current year** from runtime context instead of hardcoding a fixed year
- Use `max_results` to control the number of search results returned

## Examples

**"Latest AI news":**
```
WebSearch(query="latest AI news <current_year>", max_results=5)
```

**"Python 3.13 new features":**
```
WebSearch(query="python 3.13 new features", max_results=5)
```

**Fetch a specific article after search:**
```
WebFetch(url="https://docs.python.org/3.13/whatsnew/3.13.html", prompt="Summarize the new features")
```
