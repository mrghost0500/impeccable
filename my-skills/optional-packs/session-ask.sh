#!/usr/bin/env bash
# SessionStart hook (startup and /clear): tells Claude to ask the user whether to turn on the
# optional packs for this session. Only these few lines enter the context; a pack's own text is
# read only after the user picks it. Shell built-ins only, because startup hooks can run with an
# empty PATH.

PACKS="$HOME/.claude/optional-packs"
[ -f "$PACKS/karpathy/LOAD.md" ] || [ -f "$PACKS/superpowers/LOAD.md" ] || exit 0

printf '%s\n' '{"hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":"Optional packs are installed for this session but not loaded: Karpathy coding guidelines, and Superpowers (a skills framework for planning, test-first work, debugging and code review). Before your first reply, ask the user once with the AskUserQuestion tool (header \"Packs\", multiSelect): \"Turn on any optional packs for this session?\" Options: \"Karpathy guidelines\" (think before coding, keep it simple, change only what was asked), \"Superpowers\" (structured planning, test-first, debugging and review workflows; adds process to every task), \"Neither\". Then deal with their message as usual. For each pack they choose, read ~/.claude/optional-packs/karpathy/LOAD.md or ~/.claude/optional-packs/superpowers/LOAD.md and follow it for the rest of the session. If a schedule, a trigger or another agent started this session rather than a person, load neither and do not ask. After a resume or a compaction, do not ask again."}}'
