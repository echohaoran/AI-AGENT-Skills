---
name: twitter-media
description: "Extract content from Twitter/X links — text, images, videos, and thumbnails. Use when users share any twitter.com or x.com URL, or when you need to fetch media from a tweet. Triggers: any URL containing twitter.com or x.com, 'what did they post', 'what's in this tweet', 'show me that tweet'."
allowed-tools:
  - Bash
  - WebFetch
---

# Twitter Media Skill

Extract text, images, and video from Twitter/X posts using the **fxtwitter API** (no auth required).

## How It Works

Twitter/X blocks direct scraping. Use the free **fxtwitter API** to get structured JSON:

```
https://api.fxtwitter.com/{username}/status/{tweet_id}
```

## Extract Tweet ID from URL

Twitter URLs come in many forms. Extract the status ID:

```bash
# From: https://x.com/username/status/123456789?s=20
# Or:   https://twitter.com/username/status/123456789
# Extract: username and tweet_id

URL="https://x.com/YRyokan51928/status/2026565956206817573?s=20"
# Remove query params and trailing slashes
CLEAN=$(echo "$URL" | sed 's/[?#].*//' | sed 's:/*$::')
USERNAME=$(echo "$CLEAN" | grep -oP '(?:twitter\.com|x\.com)/\K[^/]+')
TWEET_ID=$(echo "$CLEAN" | grep -oP 'status/\K[0-9]+')
```

## Fetch Tweet Data

```bash
# Get full tweet JSON
curl -s "https://api.fxtwitter.com/${USERNAME}/status/${TWEET_ID}" | python3 -m json.tool

# Quick extract: text + media URLs
curl -s "https://api.fxtwitter.com/${USERNAME}/status/${TWEET_ID}" | python3 -c "
import sys, json
data = json.load(sys.stdin)
tweet = data.get('tweet', {})
print('Author:', tweet.get('author', {}).get('name', 'unknown'))
print('Text:', tweet.get('text', '(no text)'))
media = tweet.get('media', {})
for item in media.get('all', []):
    mtype = item.get('type', 'unknown')
    if mtype == 'photo':
        print(f'Photo: {item[\"url\"]}')
    elif mtype == 'video':
        print(f'Video: {item[\"url\"]}')
        print(f'Thumbnail: {item[\"thumbnail_url\"]}')
    elif mtype == 'gif':
        print(f'GIF: {item[\"url\"]}')
        print(f'Thumbnail: {item[\"thumbnail_url\"]}')
"
```

## Download Media

```bash
# Download photo
curl -sL -o /tmp/tweet_photo.jpg "PHOTO_URL"

# Download video thumbnail (for analysis)
curl -sL -o /tmp/tweet_thumb.jpg "THUMBNAIL_URL"

# Download video (best quality — pick highest bitrate mp4)
curl -sL -o /tmp/tweet_video.mp4 "VIDEO_URL"
```

## Analyze Image Content

After downloading an image or thumbnail, use your vision capabilities to describe the content:

```bash
# Download then analyze
curl -sL -o /tmp/tweet_media.jpg "IMAGE_OR_THUMBNAIL_URL"
# Then use the image tool or describe in your response
```

## Common Patterns

### User shares a tweet link → Summarize

1. Extract username + tweet_id from URL
2. Fetch via fxtwitter API
3. Return: author, text, and describe any media

### User says "wear this outfit" with a tweet link

1. Fetch tweet → get image/thumbnail URL
2. Download the image
3. Analyze with vision to describe the outfit in detail
4. Use the description as a prompt for image generation

### User wants to see the video

1. Fetch tweet → get video URL (pick highest bitrate mp4 from `formats`)
2. Download with curl
3. Send with `alma send video`

## Tips

- **fxtwitter API is free and needs no auth** — it's a public embed-fix service
- For videos, the API returns multiple quality variants — pick the highest `bitrate`
- Thumbnails are JPEG and good enough for outfit/scene analysis
- If fxtwitter is down, try `api.vxtwitter.com` as fallback (same API format)
- The API returns `possibly_sensitive: true` for NSFW tweets — content is still accessible
