---
name: skill-search
description: Search and install new skills to extend your capabilities. Use when you encounter a task beyond your current skills.
allowed-tools:
  - Bash
---

# Skill Search

When you encounter a task you can't handle with your current skills, search for and install new ones.

## Search Priority

Always search in this order:

1. **Check <available_skills> first** — skills are already auto-selected and listed in your system prompt. If a matching skill exists there, just use the Skill tool directly. Do NOT search for skills you already have.

2. **Local second** — if nothing in <available_skills> fits, check all installed skills:
   ```bash
   alma skill list
   ```
   A skill you need may already be installed but not selected for this conversation.

3. **Remote last** — search the skills.sh ecosystem for new skills:
   ```bash
   alma skill search <query>
   ```

## Install a Skill

```bash
alma skill install <user/repo>
```

## When to Use

- You're asked to do something beyond your current capabilities
- A task fails because you lack a specialized skill
- The user asks to find or add new capabilities
