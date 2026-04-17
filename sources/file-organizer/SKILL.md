---
name: file-organizer
description: Intelligently organize, classify, and manage files on your computer. Supports batch renaming, duplicate detection, smart categorization, and automatic archiving. No API required — pure local processing.
date: 2026-04-17
source: sickn33/antigravity-awesome-skills@file-organizer
installs: 582
allowed-tools:
  - Bash
  - Read
  - Write
---

SKILL.md

# File Organizer Skill

> **Source:** sickn33/antigravity-awesome-skills@file-organizer  
> **Installs:** 582+ | **API Required:** ❌ No | **License:** MIT

## When to Use

✅ **Use this skill when:**

- User wants to organize messy Downloads or Documents folder
- Need to batch rename files following naming conventions
- Finding and removing duplicate files
- Auto-categorizing files by type/date/size
- Archiving old files automatically
- "I have 500 photos to rename"
- "Clean up my Downloads folder"

❌ **Do NOT use this skill when:**

- System files that shouldn't be moved (leave them alone)
- Files currently open by other applications
- Encrypted or permission-protected files

## Core Features

```infographic
infographic sequence-steps-simple
data
  title 文件整理五步法
  items
    - label 扫描
      desc 遍历目录，建立文件索引
    - label 分类
      desc 按类型/日期/大小智能分组
    - label 分析
      desc 检测重复，计算统计信息
    - label 执行
      desc 移动/重命名/归档操作
    - label 验证
      desc 确认操作结果，生成报告
```

## Quick Start

### Organize a Folder

```bash
# Basic organization by file type
file-organizer organize ~/Downloads/

# Organize by date (YYYY/MM/)
file-organizer organize ~/Downloads/ --by date

# Organize by type and size
file-organizer organize ~/Downloads/ --by type --min-size 10MB

# Preview mode (don't actually move files)
file-organizer organize ~/Downloads/ --dry-run
```

### Find Duplicates

```bash
# Find duplicate files by content hash
file-organizer find-duplicates ~/Documents/

# Find duplicates larger than 1MB
file-organizer find-duplicates ~/Pictures/ --min-size 1M

# Find and auto-remove (keeps newest)
file-organizer find-duplicates ~/Downloads/ --auto-remove
```

### Batch Rename

```bash
# Rename photos by date
file-organizer rename ~/Photos/*.jpg \
  --template "{date}_IMG_{counter:04d}"

# Rename with prefix and sequence
file-organizer rename *.pdf \
  --template "Doc_{counter:03d}_{original}"

# Find and replace in filenames
file-organizer rename ~/Documents/ \
  --replace "旧名称" "新名称" \
  --pattern "*.txt"
```

## File Classification Rules

### Built-in Categories

| Category | Extensions | Example |
|----------|-----------|---------|
| **Images** | jpg, jpeg, png, gif, webp, svg, bmp | Photos, screenshots |
| **Documents** | pdf, doc, docx, txt, rtf, odt | Reports, notes |
| **Spreadsheets** | xls, xlsx, csv, numbers | Data, tables |
| **Videos** | mp4, mkv, mov, avi, webm | Recordings, clips |
| **Audio** | mp3, wav, flac, aac, ogg | Music, podcasts |
| **Archives** | zip, rar, 7z, tar, gz | Compressed files |
| **Code** | py, js, ts, java, cpp, go | Source files |
| **Executables** | app, dmg, exe, deb, rpm | Installers |

### Custom Rules

```yaml
# file-organizer-rules.yaml
rules:
  - name: Screenshots
    pattern: "Screenshot*.png"
    destination: ~/Pictures/Screenshots/

  - name: Downloads-By-Type
    by: type
    destination:
      images: ~/Pictures/Downloads/
      documents: ~/Documents/Downloads/
      archives: ~/Archives/Downloads/

  - name: Project-Files
    pattern: "project-*.{json,yaml,md}"
    destination: ~/Projects/

  - name: Large-Files
    min_size: 100MB
    action: archive
    destination: ~/Archives/Large/
```

## Scripts Reference

### `scripts/organize.sh` — Main Organizer

```bash
#!/bin/bash
# Usage: organize.sh <directory> [options]

DIR="${1:-.}"
DRY_RUN="${2:-false}"

if [ "$DRY_RUN" = "true" ]; then
  echo "🔍 Dry run mode - no files will be moved"
fi

# Scan directory
echo "📂 Scanning: $DIR"
find "$DIR" -maxdepth 1 -type f | while read -r file; do
  ext="${file##*.}"
  date_taken=$(GetFileInfo -d "$file" 2>/dev/null | cut -d' ' -f1)
  
  # Categorize and move
  case "$ext" in
    jpg|JPG|jpeg|png|gif)
      dest="$HOME/Pictures/$(date +%Y)/$(date +%m)/"
      ;;
    pdf|doc|docx|txt)
      dest="$HOME/Documents/$(date +%Y)/$(date +%m)/"
      ;;
    mp4|mov|avi|mkv)
      dest="$HOME/Videos/$(date +%Y)/"
      ;;
    zip|tar|gz|rar|7z)
      dest="$HOME/Archives/$(date +%Y)/"
      ;;
    *)
      dest="$HOME/Others/"
      ;;
  esac
  
  mkdir -p "$dest"
  
  if [ "$DRY_RUN" = "false" ]; then
    mv -n "$file" "$dest"
    echo "📦 $file → $dest"
  else
    echo "✅ [DRY] $file → $dest"
  fi
done
```

### `scripts/find-duplicates.sh` — Duplicate Finder

```bash
#!/bin/bash
# Usage: find-duplicates.sh <directory> [min_size]

DIR="${1:-.}"
MIN_SIZE="${2:-1k}"

echo "🔍 Finding duplicates in: $DIR"

# Find files by size (potential duplicates have same size)
find "$DIR" -type f -size +"$MIN_SIZE" -exec stat -f%z {} \; | \
  sort | uniq -c | sort -rn | head -20

# Use MD5/SHA256 for exact match
find "$DIR" -type f -size +"$MIN_SIZE" -exec shasum -a 256 {} \; | \
  sort | uniq -cw1 --check-chars=64 | grep -v "^ *1 "
```

### `scripts/batch-rename.sh` — Batch Renamer

```bash
#!/bin/bash
# Usage: batch-rename.sh <directory> <template> [pattern]

DIR="${1:-.}"
TEMPLATE="${2:-{original}}"
PATTERN="${3:-*}"

counter=1
for file in "$DIR"/$PATTERN; do
  [ -f "$file" ] || continue
  
  original=$(basename "$file")
  ext="${original##*.}"
  name="${original%.*}"
  
  # Generate new name from template
  new_name=$(echo "$TEMPLATE" | sed \
    -e "s/{original}/$name/g" \
    -e "s/{counter}/$(printf '%03d' $counter)/g" \
    -e "s/{date}/$(date +%Y%m%d)/g" \
    -e "s/{ext}/$ext/g")
  
  # Add extension if not present
  if [[ "$new_name" != *.* ]]; then
    new_name="$new_name.$ext"
  fi
  
  echo "📝 $original → $new_name"
  mv "$file" "$DIR/$new_name"
  ((counter++))
done
```

## Automation Templates

### Template: Daily Downloads Cleanup

```yaml
name: daily-downloads-cleanup
schedule: "0 18 * * *"  # Every day at 6pm

actions:
  - scan: ~/Downloads/
  - classify:
      images: ~/Pictures/Downloads/
      documents: ~/Documents/Downloads/
      archives: ~/Archives/Downloads/
      code: ~/Projects/downloads/
  - remove_empty: true
  - report: ~/Documents/downloads-cleanup-report.txt
```

### Template: Photo Organization

```yaml
name: organize-photos
input: ~/Downloads/photos/
output: ~/Pictures/Organized/

rules:
  - by: exif-date
    template: "{year}/{month}/{day}/{original}"
  - skip-duplicates: true
  - create-album-folders: true
```

## Configuration

```yaml
# file-organizer-config.yaml
general:
  dry_run: false
  create_dirs: true
  overwrite: false
  follow_symlinks: false
  verbose: true

classify:
  by: [type, date, size]
  case_sensitive: false

rename:
  template: "{original}"
  counter_padding: 3
  safe_chars_only: true
  preserve_extension: true

duplicate:
  hash_algorithm: sha256  # md5, sha1, sha256
  min_size: 1k
  keep_newest: true
  dry_run: true

archive:
  compression: zip
  delete_original: false
  keep_structure: true
```

## Performance Tips

1. **Use `--dry-run` first** — Always preview before actual moves
2. **Batch by type** — Organizing 1000 files at once is faster than 1000 individual moves
3. **Use hard links for duplicates** — `ln` instead of `cp` to save space
4. **Exclude directories** — `--exclude '*.tmp'` for temporary files
5. **Use `rsync`** — For large moves, `rsync -av --remove-source-files` is more reliable

## Safety Checks

```bash
# Safety: Never move system files
file-organizer organize / --exclude '/System/*' --exclude '/Library/*'

# Safety: Check file is not open
lsof "$file" && echo "File is in use!" || echo "Safe to move"

# Safety: Verify target directory exists
[ -d "$dest" ] || mkdir -p "$dest"

# Safety: Check available disk space
df -h "$dest"
```

## See Also

- [Alma File Manager Skill](sources/alma-bundled/file-manager/) — File search and management
- [Alma Screenshot Skill](sources/alma-bundled/screenshot/) — Screenshot organization
- [Workflow Automation](sources/workflow-automation/) — Automated cleanup workflows
