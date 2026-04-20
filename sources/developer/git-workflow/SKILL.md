---
name: git-workflow
description: Master Git version control workflows — branching strategies, commit conventions, conflict resolution, and history analysis. No API required — works with any Git repository.
date: 2026-04-17
source: bobmatnyc/claude-mpm-skills@git-workflow
installs: 348
allowed-tools:
  - Bash
  - Read
---

SKILL.md

# Git Workflow Skill

> **Source:** bobmatnyc/claude-mpm-skills@git-workflow  
> **Installs:** 348+ | **API Required:** ❌ No | **License:** MIT

## When to Use

✅ **Use this skill when:**

- User needs help with Git branching strategy
- Merge or rebase conflicts need resolution
- Writing proper commit messages (Conventional Commits)
- Analyzing Git history and blame
- Creating or managing Git hooks
- "What changed in this file?"
- "Help me resolve this merge conflict"

## Branching Strategies

### Git Flow

```
main ────●──────────────●────────────────── (production releases)
         │              │
         └─●──●──●──●──┘                   (develop)
             │  │  │  │
             ●  ●  ●  ●                     (feature branches)
```

### GitHub Flow

```
main ────●──●──●──●──●──●──●──●  (always deployable)
         │     │
         └───●──┘                    (feature branches, PRs)
```

## Quick Reference

### Essential Commands

```bash
# Create and switch branch
git checkout -b feature/new-feature
git switch -c feature/new-feature   # Modern syntax

# Stage and commit
git add .
git commit -m "feat: add user authentication"

# Push and create PR
git push -u origin feature/new-feature

# Sync with main
git fetch origin
git rebase origin/main

# Resolve conflict
git mergetool
git add .
git commit
```

## Conventional Commits

### Format

```
<type>(<scope>): <subject>

[optional body]

[optional footer]
```

### Types

| Type | Use For |
|------|---------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `style` | Formatting, no code change |
| `refactor` | Code change that neither fixes nor adds |
| `perf` | Performance improvement |
| `test` | Adding tests |
| `chore` | Maintenance tasks |

### Examples

```bash
git commit -m "feat(auth): add OAuth2 login support"
git commit -m "fix(api): resolve null pointer in user endpoint"
git commit -m "docs: update README with installation steps"
git commit -m "refactor(db): extract connection pooling"
git commit -m "perf(ui): lazy load images below fold"
```

## Conflict Resolution

### Step by Step

```bash
# 1. Switch to target branch
git checkout main

# 2. Pull latest
git pull

# 3. Merge feature branch
git merge feature/my-feature

# 4. If conflict, edit conflicted files
# Find conflicts: git status

# 5. Mark resolved
git add <resolved-file>

# 6. Complete merge
git commit

# Alternative: use rebase
git checkout feature/my-feature
git rebase main
# Resolve conflicts during rebase
git rebase --continue
```

### Conflict Markers

```diff
<<<<<<< HEAD
const x = 1;
const y = 2;
=======
const x = 1;
const z = 3;
>>>>>>> feature/my-feature
```

Choose one or combine:

```diff
<<<<<<< HEAD
const x = 1;
const y = 2;
const z = 3;  # Keep both changes
=======
const x = 1;
const z = 3;
>>>>>>> feature/my-feature
```

## History Analysis

```bash
# Show recent commits
git log --oneline -10

# Show file history
git log --oneline --follow -- path/to/file

# Show who changed each line
git blame path/to/file

# Show diff stats
git diff main..feature --stat

# Show commit graph
git log --graph --oneline --all

# Find commits by message
git log --grep="fix bug" --oneline

# Show files changed in last week
git diff --name-status @{"7 days ago"}..HEAD
```

## Scripts Reference

### `scripts/conventional-check.sh`

```bash
#!/bin/bash
# Validate commit message follows Conventional Commits
COMMIT_MSG=$(cat "$1")

if ! echo "$COMMIT_MSG" | grep -qE "^(feat|fix|docs|style|refactor|perf|test|chore)(\(.+\))?: .+"; then
  echo "❌ Commit message doesn't follow Conventional Commits"
  echo "Format: <type>(<scope>): <subject>"
  exit 1
fi
echo "✅ Commit message is valid"
```

### `scripts/sync-branch.sh`

```bash
#!/bin/bash
# Sync feature branch with main
CURRENT=$(git branch --show-current)
TARGET="${1:-main}"

echo "🔄 Syncing $CURRENT with $TARGET..."

git fetch origin
git checkout "$TARGET"
git pull
git checkout "$CURRENT"
git rebase "$TARGET"

if [ $? -eq 0 ]; then
  echo "✅ Synced successfully"
else
  echo "⚠️  Conflicts detected. Resolve manually."
fi
```

## Git Hooks

### Pre-commit Hook (prevent bad commits)

```bash
#!/bin/bash
# .git/hooks/pre-commit

# Run linters
npm run lint
if [ $? -ne 0 ]; then
  echo "❌ Linting failed"
  exit 1
fi

# Check for console.log
if git diff --cached | grep -q 'console\.log'; then
  echo "⚠️  console.log found in staged changes"
fi

# Run tests
npm test
if [ $? -ne 0 ]; then
  echo "❌ Tests failed"
  exit 1
fi

echo "✅ Pre-commit checks passed"
```

### Commit-msg Hook (enforce conventions)

```bash
#!/bin/bash
# .git/hooks/commit-msg
COMMIT_MSG=$(cat "$1")

if ! echo "$COMMIT_MSG" | grep -qE "^(feat|fix|docs|style|refactor|perf|test|chore)(\(.+\))?: .+"; then
  echo "❌ Commit message must follow Conventional Commits"
  echo "Format: <type>(<scope>): <subject>"
  echo "Types: feat, fix, docs, style, refactor, perf, test, chore"
  exit 1
fi
```

## Integration with Other Skills

- **code-review-quality** → Auto-check commits in PR
- **Skill_Vetter** → Version control for skill development
- **self_improving_agent** → Track changes and learnings

## See Also

- [Conventional Commits](https://www.conventionalcommits.org/)
- [Git Flow](https://nvie.com/posts/a-successful-git-branching-model/)
- [GitHub Flow](https://guides.github.com/introduction/flow/)
