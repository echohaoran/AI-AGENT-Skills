#!/bin/bash
# ============================================================
# AI Agent 技能包 — 一键安装脚本（通用版）
# 适用于：Claude CLI / OpenCode / Cursor / Windsurf / 任何 AI Agent
# 来源：https://gitee.com/echohaoran/ai-agent-skills
# 技能总数：74 项独立技能 + 2 个工具包
#
# 使用方式（任选其一）：
#   bash -c "$(curl -fsSL https://gitee.com/echohaoran/ai-agent-skills/raw/master/install.sh)"
#   或
#   curl -fsSL https://gitee.com/echohaoran/ai-agent-skills/raw/master/install.sh -o install.sh
#   chmod +x install.sh && ./install.sh
# ============================================================

REPO_URL="https://gitee.com/echohaoran/ai-agent-skills.git"
INSTALL_DIR="${HOME}/.ai-skills"
REGISTRY="${INSTALL_DIR}/REGISTRY.md"

# ── 颜色 ──
R='\033[0;31m'; G='\033[0;32m'; Y='\033[1;33m'; B='\033[0;34m'; N='\033[0m'

echo ""
echo -e "${B}╔══════════════════════════════════════════════╗${N}"
echo -e "${B}║   🤖 AI Agent 技能包 — 一键安装              ║${N}"
echo -e "${B}║   通用版 · 不限平台                           ║${N}"
echo -e "${B}╚══════════════════════════════════════════════╝${N}"
echo ""

# ════════════════════════════════════════════════
# Step 1: 克隆仓库
# ════════════════════════════════════════════════
echo -e "${Y}[1/5] 克隆技能仓库...${N}"
if [ -d "${INSTALL_DIR}/.git" ]; then
    echo "  → 仓库已存在，更新中..."
    cd "${INSTALL_DIR}" && git pull --depth 1 2>/dev/null || true
    echo -e "  ${G}✅ 已更新${N}"
else
    mkdir -p "${INSTALL_DIR}"
    git clone --depth 1 "${REPO_URL}" "${INSTALL_DIR}" 2>&1 | tail -1
    echo -e "  ${G}✅ 已克隆${N}"
fi

SKILLS_DIR="${INSTALL_DIR}/sources"

# ════════════════════════════════════════════════
# Step 2: 生成技能注册表
# ════════════════════════════════════════════════
echo ""
echo -e "${Y}[2/5] 生成技能注册表...${N}"

cat > "${REGISTRY}" << REGEOF
# 🤖 AI Agent 技能注册表
# 自动生成于 $(date '+%Y-%m-%d %H:%M')
# 路径：\${AI_SKILLS}/<技能名>/SKILL.md
#
# 在 prompt 中引用技能：
#   cat \${AI_SKILLS}/markitdown/SKILL.md

REGEOF

# 遍历所有技能目录
count=0
for skill_dir in "${SKILLS_DIR}"/*/; do
    name=$(basename "${skill_dir}")
    [ "${name}" = "alma-bundled" ] && continue
    [ "${name}" = "feishu-miaoda" ] && continue

    # 尝试读取 SKILL.md 的 description（从 YAML frontmatter）
    desc=""
    if [ -f "${skill_dir}SKILL.md" ]; then
        desc=$(grep -E "^description:" "${skill_dir}SKILL.md" 2>/dev/null | sed 's/^description: *//' | sed 's/^"//;s/"$//' | head -1)
    fi
    if [ -z "${desc}" ] && [ -f "${skill_dir}SKILL_cn.md" ]; then
        desc=$(grep -E "^description:" "${skill_dir}SKILL_cn.md" 2>/dev/null | sed 's/^description: *//' | sed 's/^"//;s/"$//' | head -1)
    fi
    if [ -z "${desc}" ]; then
        desc="（无描述）"
    fi

    echo "- **${name}** — ${desc}" >> "${REGISTRY}"
    count=$((count + 1))
done

echo -e "  ${G}✅ 已注册 ${count} 个技能 → ${REGISTRY}${N}"

# ════════════════════════════════════════════════
# Step 3: 设置环境变量
# ════════════════════════════════════════════════
echo ""
echo -e "${Y}[3/5] 配置环境变量...${N}"

# 检测 shell 配置文件
SHELL_RC="${HOME}/.bashrc"
if [ -n "${ZSH_VERSION}" ] || [ "${SHELL##*/}" = "zsh" ]; then
    SHELL_RC="${HOME}/.zshrc"
elif [ "${SHELL##*/}" = "fish" ]; then
    SHELL_RC="${HOME}/.config/fish/config.fish"
fi

if ! grep -q "AI_SKILLS" "${SHELL_RC}" 2>/dev/null; then
    {
        echo ""
        echo "# AI Agent Skills — https://gitee.com/echohaoran/ai-agent-skills"
        echo "export AI_SKILLS=\"${SKILLS_DIR}\""
        echo "alias skill-list='cat ${REGISTRY}'"
        echo "alias skill-view='f() { cat \"\${AI_SKILLS}/\$1/SKILL.md\" 2>/dev/null || cat \"\${AI_SKILLS}/\$1/SKILL_cn.md\" 2>/dev/null || echo \"未找到技能: \$1\"; }; f'"
    } >> "${SHELL_RC}"
    echo -e "  ${G}✅ 已添加至 ${SHELL_RC}${N}"
else
    echo -e "  ${Y}⏭️  AI_SKILLS 已配置${N}"
fi

# 当前 shell 也可用
export AI_SKILLS="${SKILLS_DIR}"
echo -e "  ${G}✅ AI_SKILLS=${AI_SKILLS}${N}"

# ════════════════════════════════════════════════
# Step 4: 配置 Claude CLI
# ════════════════════════════════════════════════
echo ""
echo -e "${Y}[4/5] 可选：集成 Claude CLI / OpenCode...${N}"

CLAUDE_DIR="${HOME}/.claude"
OPENCODE_DIR="${HOME}/.opencode"

# Claude CLI
if command -v claude &>/dev/null && [ -d "${CLAUDE_DIR}" ]; then
    CLAUDE_MD="${CLAUDE_DIR}/CLAUDE.md"
    if ! grep -q "AI_SKILLS" "${CLAUDE_MD}" 2>/dev/null; then
    cat >> "${CLAUDE_MD}" << CLAUDEEOF

## 🧰 AI 技能库

你拥有以下技能库可用，技能路径为 \`\${AI_SKILLS}/<技能名>/SKILL.md\`：

\`\`\`
$(cat "${REGISTRY}")
\`\`\`

**使用方式**：当用户需求匹配某个技能时，执行以下命令加载技能：
\`\`\`bash
cat \${AI_SKILLS}/<技能名>/SKILL.md
\`\`\`

CLAUDEEOF
        echo -e "  ${G}✅ 已配置 Claude CLI${N}"
    else
        echo -e "  ${Y}⏭️  Claude CLI 已配置${N}"
    fi
else
    echo -e "  ${Y}⏭️  未检测到 Claude CLI${N}"
fi

# OpenCode
if command -v opencode &>/dev/null && [ -d "${OPENCODE_DIR}" ]; then
    OPENCODE_MD="${OPENCODE_DIR}/SETUP.md"
    if [ ! -f "${OPENCODE_MD}" ] || ! grep -q "AI_SKILLS" "${OPENCODE_MD}" 2>/dev/null; then
    cat >> "${OPENCODE_MD}" << OPENCODEEOF

## 🧰 AI 技能库

技能路径：\`${SKILLS_DIR}/<技能名>/SKILL.md\`

主要技能：
$(cat "${REGISTRY}")

OPENCODEEOF
        echo -e "  ${G}✅ 已配置 OpenCode${N}"
    else
        echo -e "  ${Y}⏭️  OpenCode 已配置${N}"
    fi
else
    echo -e "  ${Y}⏭️  未检测到 OpenCode${N}"
fi

# ════════════════════════════════════════════════
# Step 5: 输出使用说明
# ════════════════════════════════════════════════
echo ""
echo -e "${Y}[5/5] 安装完成！${N}"
echo ""
echo -e "${B}╔══════════════════════════════════════════════╗${N}"
echo -e "${B}║   ✅ 安装完成！                               ║${N}"
echo -e "${B}╚══════════════════════════════════════════════╝${N}"
echo ""
echo -e "  📂 技能目录: ${SKILLS_DIR}"
echo -e "  📋 注册表:   ${REGISTRY}"
echo -e "  🔗 仓库:     ${REPO_URL}"
echo ""
echo -e "  ${B}💡 在 prompt 中引用技能：${N}"
echo '     cat ${AI_SKILLS}/awesome-privacy-skill/SKILL.md'
echo '     cat ${AI_SKILLS}/maishou/SKILL.md'
echo '     cat ${AI_SKILLS}/markitdown/SKILL.md'
echo ""
echo -e "  ${B}💡 快捷键（重开终端后）：${N}"
echo '     skill-list              # 列出所有技能'
echo '     skill-view <技能名>     # 查看技能详情'
echo ""
echo -e "  ${B}💡 分类速查：${N}"
echo -e "     📄 文档:     awesome-privacy-skill, pdf-generator, markitdown, marp"
echo -e "     🌐 比价:     maishou, taobao-shop-price, baidu_search"
echo -e "     🔧 开发:     docker, mysql, git-workflow, code-review-quality"
echo -e "     💬 通讯:     feishu, discord, telegram, xiaohongshu-cli"
echo -e "     🤖 Agent:    self_improving_agent, Agent_Browser"
echo -e "     🐦 Miaoda:   miaoca-* (16项), find-skills, skill-creator"
echo -e "     🤖 飞书:     feishu-* (9项, 需飞书 API)"
echo ""
echo -e "  ${Y}💡 跨平台使用：${N}"
echo "     Claude CLI:  已自动配置 ~/.claude/CLAUDE.md"
echo "     OpenCode:    已自动配置 ~/.opencode/SETUP.md"
echo "     其他 Agent:  设置环境变量 AI_SKILLS=${SKILLS_DIR}"
echo "                   即可在 prompt 中引用任意技能"
echo ""
