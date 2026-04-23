---
name: xiaohongshu-cli
description: "Use for ANY Xiaohongshu / 小红书 / Rednote / Little Red Book task: login, account status, search notes/users/topics, read note details/comments, browse feed and hot lists, like/favorite/comment/reply, follow/unfollow, check favorites/notifications/my-notes, post image notes, and delete your own notes."
license: Apache-2.0
allowed-tools:
  - Bash
---

# Xiaohongshu CLI Skill

This bundled skill wraps the upstream `xiaohongshu-cli` project by `jackwener`.
Source reviewed from `https://github.com/jackwener/xiaohongshu-cli` at commit `95b21d2062c72357fde4fd760c40f250de2d1551` (`2026-03-11`, version `0.5.0`).

## Runtime

Use `scripts/xhs` for every invocation.

- It prefers a locally installed `xhs`.
- If `xhs` is missing, it falls back to `uvx --from xiaohongshu-cli xhs`.
- If only `uv` exists, it falls back to `uv tool run --from xiaohongshu-cli xhs`.

Examples:

```bash
scripts/xhs --help
scripts/xhs status --yaml
scripts/xhs search "美食" --json
```

For heavy or repeated usage, install once:

```bash
uv tool install xiaohongshu-cli
uv tool upgrade xiaohongshu-cli
```

## Operating Rules

- Do not parallelize `xhs` requests. The upstream client adds jitter, captcha cooldowns, and retry logic for account safety.
- Prefer `--json` or `--yaml` when the result will be parsed. Non-TTY stdout already defaults to YAML.
- Prefer a full Xiaohongshu URL over a bare note ID when the user has one. `read` and `comments` can extract and cache the `xsec_token` from the URL.
- Treat cookies as secrets. Never ask the user to paste raw cookies into chat.

## Authentication Workflow

Always check auth before any write action, and before longer read workflows:

```bash
scripts/xhs status --yaml
```

If authentication is missing or expired:

```bash
# Browser cookie extraction
scripts/xhs login

# Optional: choose a browser explicitly
scripts/xhs login --cookie-source arc

# QR login if browser cookie extraction is unavailable
scripts/xhs login --qrcode
```

Verify after login:

```bash
scripts/xhs whoami --yaml
```

Common recovery paths:

- `not_authenticated`: rerun `scripts/xhs login`
- `verification_required`: ask the user to complete the captcha in a browser, then retry
- `ip_blocked`: suggest changing network, hotspot, or VPN

## Command Guide

### Read and Discover

```bash
scripts/xhs search "美食" --sort popular --type video --json
scripts/xhs read "<note_url_or_id>" --json
scripts/xhs comments "<note_url_or_id>" --all --json
scripts/xhs sub-comments <note_id> <comment_id> --json
scripts/xhs user <user_id> --json
scripts/xhs user-posts <user_id> --json
scripts/xhs topics "旅行" --json
scripts/xhs search-user "摄影" --json
scripts/xhs feed --json
scripts/xhs hot -c food --json
```

`hot` categories: `fashion`, `food`, `cosmetics`, `movie`, `career`, `love`, `home`, `gaming`, `travel`, `fitness`

### Interactions and Social

```bash
scripts/xhs like <note_id_or_url>
scripts/xhs like <note_id_or_url> --undo
scripts/xhs favorite <note_id_or_url>
scripts/xhs unfavorite <note_id_or_url>
scripts/xhs comment <note_id_or_url> -c "好看"
scripts/xhs reply <note_id_or_url> --comment-id <comment_id> -c "谢谢"
scripts/xhs delete-comment <note_id> <comment_id>
scripts/xhs follow <user_id>
scripts/xhs unfollow <user_id>
scripts/xhs favorites --json
scripts/xhs favorites <user_id> --json
```

### Creator and Inbox

```bash
scripts/xhs my-notes --json
scripts/xhs post --title "标题" --body "正文" --images /path/to/a.jpg /path/to/b.jpg
scripts/xhs delete <note_id> -y
```

**Newlines in post body**: Bash single-quoted strings do NOT interpret `\n`.
Use `printf` to produce real newlines:

```bash
BODY=$(printf '第一段落\n\n第二段落\n\n第三段落')
scripts/xhs post --title "标题" --body "$BODY" --images /path/to/img.jpg
scripts/xhs unread --json
scripts/xhs notifications --type mentions --json
scripts/xhs notifications --type likes --json
scripts/xhs notifications --type connections --json
```

## Structured Output

Machine-readable output uses this envelope:

```yaml
ok: true
schema_version: "1"
data: ...
```

Errors use:

```yaml
ok: false
schema_version: "1"
error:
  code: not_authenticated
  message: ...
```

Common `error.code` values:

- `not_authenticated`
- `verification_required`
- `ip_blocked`
- `signature_error`
- `unsupported_operation`
- `api_error`

## Recommended Flows

Search, inspect, then act:

```bash
NOTE_ID=$(scripts/xhs search "露营" --json | jq -r '.data.items[0].id')
scripts/xhs read "$NOTE_ID" --json
scripts/xhs like "$NOTE_ID"
```

Use pasted URLs for richer analysis:

```bash
scripts/xhs read "https://www.xiaohongshu.com/explore/xxx?xsec_token=yyy" --json
scripts/xhs comments "https://www.xiaohongshu.com/explore/xxx?xsec_token=yyy" --all --json
```

## Limitations

- No DM support
- No live-stream features
- No following/followers list API
- No media download support in the upstream CLI
- One account session at a time
- Posting support is centered on image notes
