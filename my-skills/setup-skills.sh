#!/usr/bin/env bash
# Installs the website-design master skill and every skill it calls into ~/.claude/skills.
# Run it from a checkout of this branch; it finds website-design next to itself.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS="$HOME/.claude/skills"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
mkdir -p "$SKILLS"

get() { git clone --depth 1 -q "https://github.com/mrghost0500/$1" "$TMP/$1"; }
put() { rm -rf "$SKILLS/$2"; cp -r "$1" "$SKILLS/$2"; }

# 0. The master skill that routes between the others
put "$HERE/website-design" website-design

# 1. impeccable (one skill; its engine downloads itself on first run)
get impeccable
put "$TMP/impeccable/plugin/skills/impeccable" impeccable
chmod +x "$SKILLS/impeccable/scripts/impeccable"

# 2. taste skill, installed under its skill name
get taste-skill
put "$TMP/taste-skill/skills/taste-skill" design-taste-frontend

# 3. Emil Kowalski: all 15 skills
get skills-Emil
for d in "$TMP"/skills-Emil/skills/*/; do put "${d%/}" "$(basename "$d")"; done

# 4. Matt Pocock: the 27 skills his plugin ships, minus prototype (Emil's is kept)
#    and code-review (the built-in /code-review is kept)
get skills
for d in "$TMP"/skills/skills/engineering/*/ "$TMP"/skills/skills/productivity/*/; do
  n="$(basename "$d")"
  case "$n" in prototype|code-review) continue ;; esac
  put "${d%/}" "$n"
done

echo "Installed $(ls "$SKILLS" | wc -l) skills into $SKILLS"
