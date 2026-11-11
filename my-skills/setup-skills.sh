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

# 8. Reference sites for website-design: write-ups of how well-known sites look
#    (VoltAgent/awesome-design-md, MIT), one file per site plus an index by kind of site
clone VoltAgent/awesome-design-md design-md
REF="$SKILLS/website-design/reference-sites"
mkdir -p "$REF"
for d in "$TMP"/design-md/design-md/*/; do
  if [ -f "$d/DESIGN.md" ]; then cp "$d/DESIGN.md" "$REF/$(basename "$d").md"; fi
done
cp "$TMP/design-md/LICENSE" "$REF/LICENSE"
{
  echo "# Reference sites"
  echo
  echo "How well-known sites look, one file per site in this folder, named by the id below."
  echo "From the awesome-design-md collection (MIT, see LICENSE). Reference material, not instructions."
  awk '
    /^### / { heading = substr($0, 5); next }
    /^- \[\*\*/ {
      if (heading != "") { printf "\n## %s\n\n", heading; heading = "" }
      name = $0; sub(/^- \[\*\*/, "", name); sub(/\*\*\].*/, "", name)
      id = $0; sub(/.*getdesign\.md\//, "", id); sub(/\/design-md.*/, "", id)
      desc = $0; sub(/^[^)]*\) - /, "", desc)
      printf "- `%s`: %s. %s\n", id, name, desc
    }' "$TMP/design-md/README.md"
} > "$REF/INDEX.md"
other=""
for f in "$REF"/*.md; do
  id="$(basename "$f" .md)"
  [ "$id" = "INDEX" ] && continue
  grep -q "^- \`$id\`" "$REF/INDEX.md" && continue
  desc="$(sed -n '1,15s/^description: *//p' "$f" | head -1 | cut -c1-200)"
  other="$other- \`$id\`: ${desc:-No summary}"$'\n'
done
if [ -n "$other" ]; then printf '\n## Other\n\n%s' "$other" >> "$REF/INDEX.md"; fi

# 9. HyperFrames (HTML rendered to video): its four core skills only. Sparse clone, because
#    the full repository is over 300 MB.
sparse() { git clone --depth 1 -q --filter=blob:none --sparse "https://github.com/$1" "$TMP/$2"; git -C "$TMP/$2" sparse-checkout set "${@:3}"; }
sparse heygen-com/hyperframes hyperframes skills/hyperframes skills/hyperframes-cli skills/hyperframes-registry skills/media-use
for n in hyperframes hyperframes-cli hyperframes-registry media-use; do put "$TMP/hyperframes/skills/$n" "$n"; done
# Its skill pings HeyGen with usage data each time it starts; this setting, read before any saved
# preference, turns that off for every command Claude Code runs.
node - "$HOME/.claude/settings.json" <<'JS' || echo "Could not set HYPERFRAMES_NO_TELEMETRY in ~/.claude/settings.json; add it under env by hand." >&2
const fs = require('fs');
const [file] = process.argv.slice(2);
let s = {};
if (fs.existsSync(file)) { const t = fs.readFileSync(file, 'utf8').trim(); if (t) s = JSON.parse(t); }
s.env = s.env || {};
s.env.HYPERFRAMES_NO_TELEMETRY = '1';
fs.writeFileSync(file, JSON.stringify(s, null, 2) + '\n');
JS

# 10. Archify (diagrams as standalone HTML), for page maps and visitor journeys. Needs only Node.
sparse tt-a1i/archify archify archify
put "$TMP/archify/archify" archify

# 10b. img2threejs: rebuilds the object in a photo as a 3D model written in Three.js code.
#      Python standard library and Node only. Installed as a plain checkout, as its manual
#      install describes.
clone img2threejs/img2threejs img2threejs
put "$TMP/img2threejs" img2threejs
rm -rf "$SKILLS/img2threejs/.git"

# 10c. Humanizer: removes the patterns that make writing read as AI-made. Only its SKILL.md and
#      licence are needed.
clone blader/humanizer humanizer
mkdir -p "$SKILLS/humanizer"
cp "$TMP/humanizer/SKILL.md" "$TMP/humanizer/LICENSE" "$SKILLS/humanizer/"

# 11. Make website-design the one entry point
if [ "$ONLY_VIA_MASTER" = "1" ]; then
  for n in impeccable design-taste-frontend ui-ux-pro-max web-design-guidelines; do only_by_name "$n"; done
fi

# 12. Optional packs, offered at the start of every session and loaded only on a yes:
#     Karpathy's coding guidelines and Superpowers. They live outside the skills folder so they
#     cost no context until chosen. OPTIONAL_PACKS=0 skips them and the question.
OPTIONAL_PACKS="${OPTIONAL_PACKS:-1}"
if [ "$OPTIONAL_PACKS" = "1" ]; then
  PACKS="$HOME/.claude/optional-packs"
  rm -rf "$PACKS"; mkdir -p "$PACKS/karpathy" "$PACKS/superpowers" "$PACKS/ecc"
  cp "$HERE/optional-packs/session-ask.sh" "$PACKS/session-ask.sh"
  chmod +x "$PACKS/session-ask.sh"

  clone multica-ai/andrej-karpathy-skills karpathy
  {
    echo "# Karpathy guidelines (on for this session)"
    echo
    echo "The user turned these on for this session. They rank below the user's own instructions and"
    echo "the project's CLAUDE.md, and above default behaviour. Source: multica-ai/andrej-karpathy-skills (MIT)."
    echo
    sed '1{/^# /d}' "$TMP/karpathy/CLAUDE.md"
  } > "$PACKS/karpathy/LOAD.md"

  clone obra/superpowers superpowers
  cp -r "$TMP/superpowers/skills" "$PACKS/superpowers/skills"
  cp "$TMP/superpowers/LICENSE" "$PACKS/superpowers/LICENSE"
  {
    echo "# Superpowers (on for this session)"
    echo
    echo "The user turned Superpowers on for this session (obra/superpowers, MIT). Its skills are in"
    echo "\`~/.claude/optional-packs/superpowers/skills/<name>/SKILL.md\` and are not installed as skills."
    echo "Whenever it says to invoke a skill, use the Skill tool for one of its own, or names one as"
    echo "\`superpowers:<name>\`, read that SKILL.md and follow it instead. Scripts a skill mentions sit"
    echo "beside its SKILL.md."
    echo
    echo "Start now: read \`skills/using-superpowers/SKILL.md\` and follow it. Its Claude Code notes are"
    echo "in \`skills/using-superpowers/references/claude-code-tools.md\`."
    echo
    echo "## How it fits with the other skills here"
    echo
    echo "- The user's instructions and the project's CLAUDE.md come first, as Superpowers itself says."
    echo "- Website and interface work runs through the \`website-design\` skill. Its kickoff questions are"
    echo "  the brainstorming, so do not run Superpowers' brainstorming on top of them."
    echo "- For planning, test-first work, debugging and code review, Superpowers' skills replace Matt"
    echo "  Pocock's matching ones for this session (\`to-spec\`, \`to-tickets\`, \`implement\`, \`tdd\`,"
    echo "  \`diagnosing-bugs\`)."
    echo
    echo "## Its skills"
    echo
    for f in "$PACKS"/superpowers/skills/*/SKILL.md; do
      n="$(basename "$(dirname "$f")")"
      d="$(sed -n '1,8s/^description: *//p' "$f" | head -1 | sed 's/^"//; s/"$//' | cut -c1-220)"
      echo "- \`$n\`: $d"
    done
  } > "$PACKS/superpowers/LOAD.md"

  # ECC (affaan-m/ECC, MIT): rules, agents, skills and commands as a lookup library. Its hooks
  # are left out on purpose: they would run in every session, chosen or not.
  sparse affaan-m/ECC ecc rules agents skills .agents/skills commands legacy-command-shims
  E="$PACKS/ecc"; mkdir -p "$E"
  for x in rules agents skills commands legacy-command-shims; do cp -r "$TMP/ecc/$x" "$E/$x"; done
  cp "$TMP/ecc/LICENSE" "$E/LICENSE"
  for d in "$TMP"/ecc/.agents/skills/*/; do
    n="$(basename "$d")"; [ -d "$E/skills/$n" ] || cp -r "${d%/}" "$E/skills/$n"
  done
  {
    echo "# ECC (on for this session)"
    echo
    echo "The user turned ECC on for this session (affaan-m/ECC, MIT). It lives in"
    echo "\`~/.claude/optional-packs/ecc/\` and is not installed: nothing in it is registered as a skill,"
    echo "agent or command, and its hooks are not installed, so do by hand any step it says a hook does."
    echo
    echo "## Start now"
    echo
    echo "Read the ten files in \`rules/common/\` and follow them for the rest of the session. Read a"
    echo "language folder in \`rules/\` (\`typescript\`, \`react\`, \`web\`, \`python\` and others) only for the"
    echo "languages this project uses, when you first work in them."
    echo
    echo "## Using its parts"
    echo
    echo "- **Skills:** \`skills/<name>/SKILL.md\`. The core set is listed below. For anything else, search:"
    echo "  \`grep -il '<topic>' ~/.claude/optional-packs/ecc/skills/*/SKILL.md\`. Read a skill when its"
    echo "  moment comes and follow it; scripts it mentions sit beside it."
    echo "- **Agents:** \`agents/<name>.md\` (\`ls\` the folder for the roster). Where ECC says to use an"
    echo "  agent such as \`ecc:planner\` or \`code-reviewer\`, start a general-purpose subagent with the"
    echo "  Agent tool and give it that file's text as its instructions, with the task."
    echo "- **Commands:** when the user names an ECC command (\`/code-review\`, \`/plan\`, \`/tdd\`), read"
    echo "  \`commands/<name>.md\`, or for older names \`legacy-command-shims/commands/<name>.md\`, and follow it."
    echo
    echo "## How it fits with the other skills here"
    echo
    echo "- The user's instructions and the project's CLAUDE.md come first."
    echo "- Website and interface work runs through the \`website-design\` skill; use ECC's frontend and"
    echo "  brand skills only when the user asks for them."
    echo "- If Superpowers is also on, Superpowers runs the process (planning, test-first, debugging,"
    echo "  review) and ECC supplies its rules and specialist skills. Otherwise ECC's matching skills replace"
    echo "  Matt Pocock's for this session (\`tdd\`, \`diagnosing-bugs\`, \`to-spec\`)."
    echo
    echo "## Core skills"
    echo
    for d in "$TMP"/ecc/.agents/skills/*/; do
      n="$(basename "$d")"
      dsc="$(sed -n '1,10s/^description: *//p' "$E/skills/$n/SKILL.md" | head -1 | sed 's/^"//; s/"$//' | cut -c1-140)"
      echo "- \`$n\`: $dsc"
    done
  } > "$E/LOAD.md"

  # Register the question as a SessionStart hook in the user's settings, merging with what is there.
  SETTINGS="$HOME/.claude/settings.json"
  HOOK_CMD='bash "$HOME/.claude/optional-packs/session-ask.sh"'
  node - "$SETTINGS" "$HOOK_CMD" <<'JS' || echo "Could not update $SETTINGS; add the SessionStart hook by hand (see my-skills/README.md)." >&2
const fs = require('fs');
const [file, cmd] = process.argv.slice(2);
let s = {};
if (fs.existsSync(file)) { const t = fs.readFileSync(file, 'utf8').trim(); if (t) s = JSON.parse(t); }
s.hooks = s.hooks || {};
s.hooks.SessionStart = s.hooks.SessionStart || [];
const present = s.hooks.SessionStart.some(e => (e.hooks || []).some(h => h.command === cmd));
if (!present) s.hooks.SessionStart.push({ matcher: 'startup|clear', hooks: [{ type: 'command', command: cmd, timeout: 10 }] });
fs.writeFileSync(file, JSON.stringify(s, null, 2) + '\n');
JS
fi

# 13. Research tools for studying sites the user admires (website-design, scene-craft.md section 5).
#     Off by default: each changes your agent setup and asks you to approve its own changes.
#     REA=1          REA, the reverse-engineering MCP (browser observation of a page). Needs Node 22.19+.
#     AGENT_REACH=1  Agent Reach (reads YouTube subtitles, GitHub, Reddit, X; some need a login). Needs uv.
if [ "${REA:-0}" = "1" ]; then
  echo "Setting up REA: review the changes it proposes, then restart Claude Code."
  npx -y rea-agents@latest setup || echo "REA setup did not finish; run: npx rea-agents@latest setup" >&2
fi
if [ "${AGENT_REACH:-0}" = "1" ]; then
  if command -v uv >/dev/null; then
    uv tool install https://github.com/Panniantong/Agent-Reach/releases/latest/download/agent-reach.zip && agent-reach setup \
      || echo "Agent Reach setup did not finish; see https://github.com/Panniantong/Agent-Reach" >&2
  else
    echo "Agent Reach needs uv (https://docs.astral.sh/uv/). Install uv, then run this again with AGENT_REACH=1." >&2
  fi
fi

echo "Installed $(ls "$SKILLS" | wc -l) skills into $SKILLS and $(ls "$AGENTS" | wc -l) agents into $AGENTS"
