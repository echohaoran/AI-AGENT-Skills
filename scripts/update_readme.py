#!/usr/bin/env python3
"""
Update README.md and README_cn.md based on SKILL_*.md files in sources/.
Run this script after adding new skills to sources/.

Usage: python scripts/update_readme.py
"""

import os
import re
import glob

SOURCES_DIR = "sources"
README_EN = "README.md"
README_CN = "README_cn.md"

def get_skills():
    """Scan sources/ for skill folders and extract metadata from SKILL_en.md and SKILL_cn.md."""
    skills = {}
    for folder in sorted(os.listdir(SOURCES_DIR)):
        skill_dir = os.path.join(SOURCES_DIR, folder)
        if not os.path.isdir(skill_dir):
            continue

        en_file = os.path.join(skill_dir, "SKILL_en.md")
        cn_file = os.path.join(skill_dir, "SKILL_cn.md")

        en_excerpt = ""
        en_title = folder

        if os.path.exists(en_file):
            with open(en_file, "r", encoding="utf-8") as f:
                content = f.read()
            # Extract excerpt from frontmatter
            m = re.search(r'^---\s*\ntitle:\s*(.+?)\s*\nexcerpt:\s*(.+?)\s*\n', content, re.MULTILINE)
            if m:
                en_title = m.group(1).strip()
                en_excerpt = m.group(2).strip()

        cn_excerpt = ""

        if os.path.exists(cn_file):
            with open(cn_file, "r", encoding="utf-8") as f:
                content = f.read()
            # Extract excerpt from frontmatter
            m = re.search(r'^---\s*\ntitle:\s*(.+?)\s*\nexcerpt:\s*(.+?)\s*\n', content, re.MULTILINE)
            if m:
                cn_excerpt = m.group(2).strip()

        skills[folder] = {
            "title": en_title,
            "en_excerpt": en_excerpt,
            "cn_excerpt": cn_excerpt,
        }

    return skills


def get_zip_name(skill_dir, folder):
    """Try to find the zip file in the skill directory."""
    if os.path.exists(skill_dir):
        for f in os.listdir(skill_dir):
            if f.endswith(".zip"):
                return f
    return f"{folder}-1.0.0.zip"


def build_readme_en(skills):
    """Build English README content."""
    lines = []
    lines.append("[English](README.md) | [中文](README_cn.md)")
    lines.append("")
    lines.append("# Commonly Used Skills")
    lines.append("")
    lines.append("> Click the name to enter the corresponding page for details")
    lines.append("")
    lines.append("## Skills Catalog")
    lines.append("")
    lines.append("| Skill | Description |")
    lines.append("|-------|-------------|")

    for folder, info in skills.items():
        link = f"[{folder}](sources/{folder}/SKILL_en.md)"
        desc = info["en_excerpt"] or info["cn_excerpt"] or ""
        lines.append(f"| {link} | {desc} |")

    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Skill Details")
    lines.append("")

    for folder, info in skills.items():
        lines.append(f"### [{folder}](sources/{folder}/SKILL_en.md)")
        excerpt = info["en_excerpt"] or info["cn_excerpt"] or ""
        lines.append(excerpt)
        lines.append("")
        lines.append(f"[View Details](sources/{folder}/SKILL_en.md)")
        lines.append("")

        skill_dir = os.path.join(SOURCES_DIR, folder)
        zip_name = get_zip_name(skill_dir, folder)
        # Convert folder name to skill name
        # Specific mappings first, then generic underscore->hyphen
        skill_name = folder
        if skill_name == "Agent_Browser":
            skill_name = "agent-browser"
        elif skill_name == "self_improving_agent":
            skill_name = "self-improving-agent"
        elif skill_name == "Find_Skills_Skill":
            skill_name = "find-skills-skill"
        elif skill_name == "Skill_Vetter":
            skill_name = "skill-vetter"
        else:
            skill_name = skill_name.replace("_", "-")

        url = f"https://gitee.com/echohaoran/ai-agent-commonly-used---kills/raw/master/sources/{folder}/{zip_name}"
        install_path = f"~/.openclaw/skills/{skill_name}"
        lines.append("```")
        lines.append(f"Download the {folder.replace('_', '-')} skill from {url} and install it to {install_path}")
        lines.append("```")
        lines.append("")
        lines.append("---")
        lines.append("")

    return "\n".join(lines)


def build_readme_cn(skills):
    """Build Chinese README content."""
    lines = []
    lines.append("[English](README.md) | [中文](README_cn.md)")
    lines.append("")
    lines.append("# 常用的 Skills")
    lines.append("")
    lines.append("> 点击名称可进入对应页面查看详情")
    lines.append("")
    lines.append("## 技能目录")
    lines.append("")
    lines.append("| 技能 | 描述 |")
    lines.append("|-------|-------------|")

    for folder, info in skills.items():
        link = f"[{folder}](sources/{folder}/SKILL_cn.md)"
        desc = info["cn_excerpt"] or info["en_excerpt"] or ""
        lines.append(f"| {link} | {desc} |")

    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 技能详情")
    lines.append("")

    for folder, info in skills.items():
        lines.append(f"### [{folder}](sources/{folder}/SKILL_cn.md)")
        excerpt = info["cn_excerpt"] or info["en_excerpt"] or ""
        lines.append(excerpt)
        lines.append("")
        lines.append(f"[查看详情](sources/{folder}/SKILL_cn.md)")
        lines.append("")

        skill_dir = os.path.join(SOURCES_DIR, folder)
        zip_name = get_zip_name(skill_dir, folder)
        # Convert folder name to skill name
        skill_name = folder
        if skill_name == "Agent_Browser":
            skill_name = "agent-browser"
        elif skill_name == "self_improving_agent":
            skill_name = "self-improving-agent"
        elif skill_name == "Find_Skills_Skill":
            skill_name = "find-skills-skill"
        elif skill_name == "Skill_Vetter":
            skill_name = "skill-vetter"
        else:
            skill_name = skill_name.replace("_", "-")

        url = f"https://gitee.com/echohaoran/ai-agent-commonly-used---kills/raw/master/sources/{folder}/{zip_name}"
        install_path = f"~/.openclaw/skills/{skill_name}"
        lines.append("```")
        lines.append(f"从 {url} 下载 {skill_name} 技能并安装到 {install_path}")
        lines.append("```")
        lines.append("")
        lines.append("---")
        lines.append("")

    return "\n".join(lines)


def main():
    print("Scanning skills in sources/...")
    skills = get_skills()
    print(f"Found {len(skills)} skills: {', '.join(skills.keys())}")

    print(f"\nUpdating {README_EN}...")
    en_content = build_readme_en(skills)
    with open(README_EN, "w", encoding="utf-8") as f:
        f.write(en_content)
    print("Done.")

    print(f"\nUpdating {README_CN}...")
    cn_content = build_readme_cn(skills)
    with open(README_CN, "w", encoding="utf-8") as f:
        f.write(cn_content)
    print("Done.")

    print("\nAll READMEs updated successfully.")


if __name__ == "__main__":
    main()
