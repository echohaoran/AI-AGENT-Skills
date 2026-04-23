---
name: music-gen
description: "Generate original songs with lyrics and vocals. Use when users ask to sing, create a song, make music, compose, or generate audio. Supports style prompts, custom lyrics, duration control, and instrumental mode."
allowed-tools:
  - Bash
---

# Music Generation Skill

Generate original songs using **ACE-Step 1.5** on remote 3090 GPU. Produces full songs with vocals, instruments, and lyrics in ~40 seconds.

## When to Use

- User says "sing me a song", "make a song", "create music"
- User provides lyrics and asks for a song
- User describes a music style they want to hear
- User says "generate a song about..."

## Command

```bash
alma sing generate "style description" [--lyrics "lyrics text"] [--duration 60] [--instrumental]
```

### Parameters

| Flag | Default | Description |
|------|---------|-------------|
| `"style description"` | required | Music style/genre prompt (e.g. "dreamy lo-fi chill hop, female vocal") |
| `--lyrics "..."` | empty | Song lyrics with structure tags like `[verse]`, `[chorus]`, `[bridge]` |
| `--duration N` | 60 | Duration in seconds (10-600) |
| `--instrumental` | false | Generate without vocals |

### Output

Prints the saved MP3 file path to stdout. Send it with:
```bash
alma send file <chatId> <path>
```

## Examples

### Simple song
```bash
alma sing generate "upbeat pop rock, male vocal, energetic drums"
```

### Song with custom lyrics
```bash
alma sing generate "dreamy lo-fi chill hop, female vocal, warm piano" --lyrics "[verse]\nMidnight glow on my screen\nCoffee steam like a dream\n\n[chorus]\nLet the music carry me\nThrough the night so peacefully"
```

### Instrumental track
```bash
alma sing generate "epic orchestral cinematic, strings and brass" --duration 120 --instrumental
```

### Short jingle
```bash
alma sing generate "cute happy ukulele jingle" --duration 15
```

## Style Prompt Tips

- Include **genre** (pop, rock, jazz, lo-fi, classical, EDM, hip hop...)
- Include **vocal type** (female vocal, male vocal, choir...)
- Include **instruments** (piano, guitar, drums, synth, strings, brass...)
- Include **mood** (dreamy, energetic, melancholic, upbeat, dark, romantic...)
- Example: `"melancholic acoustic folk, female vocal, fingerpicked guitar, autumn evening vibe"`

## Lyrics Format

Use structure tags for song sections:
```
[verse]
First verse lyrics here
Line two of verse

[chorus]
Chorus lyrics here
Repeated refrain

[bridge]
Bridge section
Something different

[outro]
Ending lyrics
```

## Supported Languages

50+ languages for lyrics including English, Chinese, Japanese, Korean, Spanish, French, etc.

## Technical Notes

- Backend: ACE-Step 1.5 on NVIDIA RTX 3090 (24GB VRAM)
- LM: 0.6B parameter model with PyTorch backend
- Generation time: ~35-40s for 60s audio
- Audio format: MP3
- The API server auto-starts if not running (first call takes ~90s extra for model loading)
- ACE-Step and ComfyUI share the same GPU — ComfyUI will be stopped when music generation starts
- Output saved to `~/.config/alma/music/`

## Troubleshooting

If generation fails:
1. Check if the 3090 is reachable: `ssh yetone@10.0.0.207 'echo ok'`
2. Check ACE-Step logs: `ssh yetone@10.0.0.207 'tail -30 /tmp/acestep.log'`
3. Check VRAM: `ssh yetone@10.0.0.207 '/usr/lib/wsl/lib/nvidia-smi'`
4. If VRAM is full, kill other processes: `ssh yetone@10.0.0.207 'pkill -f comfyui; pkill -f acestep'`
