#!/usr/bin/env bash
# SessionStart hook (startup and /clear): tells Claude to ask the user whether to turn on the
# optional packs for this session. Only these few lines enter the context; a pack's own text is
# read only after the user picks it. Shell built-ins only, because startup hooks can run with an
# empty PATH.

PACKS="$HOME/.claude/optional-packs"
[ -f "$PACKS/karpathy/LOAD.md" ] || [ -f "$PACKS/superpowers/LOAD.md" ] || [ -f "$PACKS/ecc/LOAD.md" ] || exit 0

printf '%s\n' '{"hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":"Optional packs are installed for this session but not loaded. Before your first reply, ask the user once with the AskUserQuestion tool (header \"Packs\", multiSelect): \"Turn on any optional packs for this session?\" Options: \"Karpathy guidelines\" (think before coding, keep it simple, change only what was asked; light), \"Superpowers\" (structured planning, test-first, debugging and review workflows; adds process to every task), \"ECC\" (a large engineering library: coding rules, about 70 agents and 300 skills looked up as needed; the heaviest, and it overlaps Superpowers), \"Neither\". Then deal with their message as usual. For each pack they choose, read its LOAD.md and follow it for the rest of the session: ~/.claude/optional-packs/karpathy/LOAD.md, ~/.claude/optional-packs/superpowers/LOAD.md or ~/.claude/optional-packs/ecc/LOAD.md. If a schedule, a trigger or another agent started this session rather than a person, load none and do not ask. After a resume or a compaction, do not ask again."}}'
