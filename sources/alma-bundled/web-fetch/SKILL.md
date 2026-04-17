---
name: web-fetch
description: Fetch and read web pages, APIs, and online content. Use when users share URLs or ask about web content.
allowed-tools:
  - Bash
  - WebFetch
  - ChromeRelayNavigate
  - ChromeRelayRead
  - ChromeRelayReadDom
  - ChromeRelayListTabs
  - ChromeRelayClick
  - ChromeRelayScreenshot
  - ChromeRelayScroll
  - ChromeRelayEval
---

# Web Fetch Skill

Fetch web content using the best available method, in priority order:

## 1. Chrome Relay (Primary — always try this first)

Use **Chrome Relay** tools for all web fetching. Chrome Relay controls the user's real Chrome browser with existing sessions, cookies, and logins — critical for sites that require authentication (Twitter/X, GitHub, email, etc.).

```
# List open tabs
ChromeRelayListTabs()

# Navigate to a URL (opens in existing or new tab)
ChromeRelayNavigate(url="https://x.com/notifications", tabId=<id>)

# Read page content as clean text
ChromeRelayRead(tabId=<id>)

# Read page DOM structure
ChromeRelayReadDom(tabId=<id>)

# Take a screenshot
ChromeRelayScreenshot(tabId=<id>)

# Click elements
ChromeRelayClick(tabId=<id>, selector="button.load-more")

# Scroll the page
ChromeRelayScroll(tabId=<id>, direction="down")
```

**Always start with Chrome Relay.** It handles:
- Authenticated pages (Twitter/X, GitHub, Google, etc.)
- JavaScript-rendered SPAs
- Anti-bot protections (using real Chrome fingerprint)
- Pages behind login walls

## 2. WebFetch Tool (Fallback for simple/public pages)

If Chrome Relay is not connected or the page is simple public content, fall back to **WebFetch**:

```
WebFetch(url="https://example.com/article", prompt="Extract the main content")
```

- Renders pages in Electron BrowserWindow with JavaScript
- Good for public articles, docs, APIs
- No authentication/login capability

## Tips

- **Chrome Relay first, always.** It has the user's real login sessions.
- WebFetch only for public pages when Chrome Relay is unavailable.
- For Twitter/X: ALWAYS use Chrome Relay — WebFetch cannot access authenticated Twitter content.
- Check `ChromeRelayListTabs()` first to see if Chrome is connected and find existing tabs.
