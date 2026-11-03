#!/usr/bin/env bash
# Installs the website-design master skill and every skill it calls into ~/.claude/skills.
# Run it from a checkout of this branch; it finds website-design next to itself.
set -euo pipefail

# 1: impeccable, design-taste-frontend, ui-ux-pro-max and web-design-guidelines start only by name
# or through website-design, so it is the one skill that answers "design my website".
# 0: leave them starting on their own as well.
ONLY_VIA_MASTER="${ONLY_VIA_MASTER:-1}"

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS="$HOME/.claude/skills"
AGENTS="$HOME/.claude/agents"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
mkdir -p "$SKILLS" "$AGENTS"

clone() { git clone --depth 1 -q "https://github.com/$1" "$TMP/$2"; }
put() { rm -rf "$SKILLS/$2"; cp -r "$1" "$SKILLS/$2"; }
only_by_name() {
  local f="$SKILLS/$1/SKILL.md"
  grep -q '^disable-model-invocation:' "$f" && return 0
  awk '{ print } !done && /^name:/ { print "disable-model-invocation: true"; done = 1 }' "$f" > "$f.tmp"
  mv "$f.tmp" "$f"
}

# 0. The master skill
put "$HERE/website-design" website-design

# 1. impeccable (its engine downloads itself on first run)
clone mrghost0500/impeccable impeccable
put "$TMP/impeccable/plugin/skills/impeccable" impeccable
chmod +x "$SKILLS/impeccable/scripts/impeccable"

# 2. Taste skill, under its skill name
clone mrghost0500/taste-skill taste-skill
put "$TMP/taste-skill/skills/taste-skill" design-taste-frontend

# 3. Emil Kowalski: all 15 skills
clone mrghost0500/skills-Emil skills-Emil
for d in "$TMP"/skills-Emil/skills/*/; do put "${d%/}" "$(basename "$d")"; done

# 4. Matt Pocock: the 27 skills his plugin ships, minus prototype (Emil's is kept)
#    and code-review (the built-in /code-review is kept)
clone mrghost0500/skills matt
for d in "$TMP"/matt/skills/engineering/*/ "$TMP"/matt/skills/productivity/*/; do
  n="$(basename "$d")"
  case "$n" in prototype|code-review) continue ;; esac
  put "${d%/}" "$n"
done

# 5. UI/UX Pro Max: the main skill, with its search script pointed at this install
clone mrghost0500/ui-ux-pro-max-skill uupm
put "$TMP/uupm/.claude/skills/ui-ux-pro-max" ui-ux-pro-max
find "$SKILLS/ui-ux-pro-max" -name '*.md' -exec \
  sed -i 's#\${CLAUDE_PLUGIN_ROOT}/\.claude/skills/ui-ux-pro-max#$HOME/.claude/skills/ui-ux-pro-max#g' {} +

# 6. Claude SEO: its 26 skills and 19 helper agents, laid out the way its own install.sh does,
#    without the add-ons for paid services. Its Python tools install later, when the user runs
#    /seo setup.
clone mrghost0500/claude-seo seo
R="$TMP/seo"
for d in "$R"/skills/*/; do put "${d%/}" "$(basename "$d")"; done
for x in schema data pdf; do
  if [ -d "$R/$x" ]; then mkdir -p "$SKILLS/seo/$x"; cp -r "$R/$x/." "$SKILLS/seo/$x/"; fi
done
mkdir -p "$SKILLS/seo/scripts"
cp -r "$R/scripts/." "$SKILLS/seo/scripts/"
chmod +x "$SKILLS/seo/scripts/claude-seo"
cp "$R/requirements.txt" "$SKILLS/seo/"
cp "$R/.claude-plugin/plugin.json" "$SKILLS/seo/runtime-plugin.json"
cp "$R"/agents/*.md "$AGENTS/"
root_esc="$(printf '%s' "$SKILLS/" | sed 's/[#&\\]/\\&/g')"
rewrite() {
  sed -i -e "s#\${CLAUDE_PLUGIN_ROOT}/skills/#${root_esc}#g" \
    -e 's#"${CLAUDE_PLUGIN_ROOT}/scripts/claude-seo" \(run\|setup\|doctor\)#"$HOME/.claude/skills/seo/scripts/claude-seo" \1#g' "$1"
}
for d in "$R"/skills/*/; do
  find "$SKILLS/$(basename "$d")" -name '*.md' -print0 | while IFS= read -r -d '' f; do rewrite "$f"; done
done
for f in "$R"/agents/*.md; do rewrite "$AGENTS/$(basename "$f")"; done

# 7. Single skills from upstream repos
clone vercel-labs/agent-skills vercel
put "$TMP/vercel/skills/web-design-guidelines" web-design-guidelines
clone ibelick/ui-skills ibelick
put "$TMP/ibelick/skills/fixing-metadata" fixing-metadata
git clone --depth 1 -q --filter=blob:none --sparse https://github.com/anthropics/skills "$TMP/anthropic"
git -C "$TMP/anthropic" sparse-checkout set skills/webapp-testing
put "$TMP/anthropic/skills/webapp-testing" webapp-testing

# 8. Make website-design the one entry point
if [ "$ONLY_VIA_MASTER" = "1" ]; then
  for n in impeccable design-taste-frontend ui-ux-pro-max web-design-guidelines; do only_by_name "$n"; done
fi

echo "Installed $(ls "$SKILLS" | wc -l) skills into $SKILLS and $(ls "$AGENTS" | wc -l) agents into $AGENTS"
