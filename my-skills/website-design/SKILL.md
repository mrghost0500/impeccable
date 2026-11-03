---
name: website-design
description: "Start here for any website or interface design work: a new site or landing page, a redesign, an app screen or dashboard, making existing UI look or feel better, motion, mobile feel, and design reviews. This is the master skill over the installed design skills (impeccable, design-taste-frontend, and Emil Kowalski's emil-design-eng, animate, break-ui, mobile-native, apple-design and the rest) and Matt Pocock's engineering skills for the work around the design (sharpening the brief, planning a large site, testing logic, fixing bugs, shipping). It picks one lead skill for the job, runs the stages in order, and calls each specialist at the right stage so they never run competing processes. Use it instead of calling those skills directly, unless the user names one."
argument-hint: "[what to design or improve]"
---

# Website design

One entry point for design work. You do not design from this file. You pick the job, hand each stage
to the skill built for it, and keep the stages in order.

## How to call a skill

- Invoke a skill with the Skill tool by name and pass the task as its argument, so it starts on the
  task instead of greeting. `impeccable` takes its command first: `audit the pricing section`.
- Some skills can only be started by the user, so the Skill tool refuses them: `prototype`,
  `review-animations`, `pick-ui-library`, and most of Matt Pocock's planning skills (`grill-me`,
  `to-questionnaire`, `to-spec`, `to-tickets`, `implement`, `wayfinder`, `handoff`, `retro`). Read
  `~/.claude/skills/<name>/SKILL.md` and follow it instead.
- Each skill's files and scripts sit in its own folder under `~/.claude/skills/`. The folder that
  `design-taste-frontend` calls `<skill>` is `~/.claude/skills/design-taste-frontend`.
- If the user names a skill ("use taste", "run impeccable audit"), use that one and skip the routing.

## 1. Pick the job

| The request | Lead | Then |
|---|---|---|
| A new public page or site, or a full redesign of one: landing page, marketing or product site, portfolio, event, restaurant, one-pager | `design-taste-frontend`, its page run | The stages in section 2 |
| A new app screen or docs: dashboard, admin, settings, editor, tool, help pages | `impeccable` as general design work (it routes to new-work) | The stages in section 3 |
| A change to existing UI: bolder, quieter, simpler, type, spacing, colour, copy, responsive, speed, first-run, personality | The matching `impeccable` command: `bolder`, `quieter`, `distill`, `typeset`, `layout`, `colorize`, `clarify`, `adapt`, `optimize`, `onboard`, `delight`, `overdrive` | `impeccable polish` on what changed |
| A review, no changes yet | `impeccable critique`, then `impeccable audit` | `emil-design-eng` for its Before/After table on the interactive parts; `review-animations` when there is motion |
| Polish before shipping | `impeccable polish` | `emil-design-eng` detail pass on the interactive parts |
| Motion | `animate` to build a move; `improve-animations` to audit a codebase; `find-animation-opportunities` for where motion belongs; `animation-performance` for jank; `apple-design` for gestures, sheets and springs | `review-animations` |
| Stress-test a component | `break-ui` | |
| Feels wrong on a phone | `mobile-native` | `impeccable adapt` |
| See options before choosing | `prototype` for one component; `impeccable generate` or `impeccable live` for variants in the running page | |
| A quick question | `animation-vocabulary` (what an effect is called), `pick-ui-library` (which library), `ask-sonner` (toasts) | |
| A native app | `impeccable` with the platform recorded in PRODUCT.md (`ios`, `android` or `adaptive`); `animate-expo` for React Native motion; `write-swift` for Swift code | |

If two rows fit, the earlier row wins. If you cannot tell a page from an app screen: a page is read
and scrolled, an app screen is worked in. A product site that shows its app is a page.

## 2. New public page

1. **Brief and direction.** `design-taste-frontend` steps 1 to 4: brief, argument, draw, idea. If the
   project has PRODUCT.md or DESIGN.md, read them first and treat them as part of the brief. If a
   fact only the client knows is missing, see section 4. The direction chosen here is the direction
   for the whole job.
2. **Build.** Its steps 5 to 8: words, build, gate, look.
3. **Motion.** Its step 9. Build each move with `emil-design-eng`: its Animation Decision Framework
   (should it animate, purpose, easing, duration) and its component rules (press feedback, never from
   `scale(0)`, popovers that grow from their trigger). Use `apple-design` for drag, swipe and sheets.
4. **Hardening.** `break-ui` on every component fed by data: cards, pricing, lists, testimonials,
   forms. `mobile-native` for the phone pass. `impeccable harden` when there are forms or error states.
5. **Review.** `impeccable critique`, then `impeccable audit` (it owns accessibility). Fix what they
   find. Then `review-animations` on the motion.
6. **Polish.** `impeccable polish`. Then run the taste gate again (`lint.mjs`, `inspect.mjs`, and
   `scenes.mjs` if the page has scroll scenes), because the later stages changed the page. It must
   still show 0 FAIL at every width.
7. **Report.** The taste skill's step 10 report, plus one line per stage: which skill ran and what it
   changed. Then ship it as section 4 describes.

## 3. New app screen or docs

1. **Brief, direction and build.** `impeccable`: its Setup, then new-work. Operate and Read screens
   are built straight in code.
2. **Interaction detail.** `emil-design-eng` on buttons, menus, popovers, tooltips, tabs and
   transitions. `animate` for any new motion. Logic behind the screen (filters, validation,
   calculations, state) is built test-first with `tdd`.
3. **Hardening.** `break-ui` on every table, list, card and form; app screens break on real data more
   than anything else. `mobile-native` if it ships to phones as web. `impeccable harden`.
4. **Review.** `impeccable critique`, `impeccable audit`, and `review-animations` when there is motion.
5. **Polish.** `impeccable polish`.
6. **Report.** One line per stage: which skill ran and what it changed, then what still falls short.
   Then ship it as section 4 describes.

## 4. Engineering around the design (Matt Pocock)

The design skills decide how it looks and feels. These decide how the work is scoped, planned, tested
and shipped. Use one only when its moment comes up.

| Moment | Skill |
|---|---|
| The idea is vague and the user wants to think it through, or asks to be grilled | `grilling` (or `grill-me` when the user calls it) |
| A fact only the client knows blocks the brief: name, offer, prices, real photos, claims | `to-questionnaire`, so the user can send the questions on |
| Facts about the subject, a library or an API need checking | `research` |
| A site of several pages, or more work than one session holds | `to-spec`, then `to-tickets`; `wayfinder` when even the route is unclear. Set the direction once for the whole site in stage 1 and write it into the spec, so every ticket follows it. Then build each ticket through the stages above, or with `implement` |
| Interactive logic: forms, booking, pricing calculators, filters, carts | `tdd` |
| How components and modules are split | `codebase-design` |
| Something throws, fails or is broken | `diagnosing-bugs` (slow animation goes to `animation-performance`, slow pages to `impeccable optimize`) |
| Steps only the user can do: domain, DNS, hosting, accounts, API keys | `wizard` |
| Writing the pull request | `pr` |
| The session is getting long, or another agent will continue | `handoff` |
| The user wants a look back at how it went | `retro` |

`to-spec`, `to-tickets` and `wayfinder` publish to the issue tracker that `/setup-matt-pocock-skills`
sets up once per repo. If it has not run, ask the user to run it, or keep the spec and tickets as
local markdown files.

## Rules for combining

- **One lead, one direction.** Never run impeccable's new-work and the taste skill's draw on the same
  surface. Every later stage refines the lead's direction; none of them replaces it, and no planning
  or engineering skill changes it.
- **The brief wins, then the lead.** When two skills disagree, follow the user's brief, then the lead
  skill's house rules for that surface.
- **Refine, do not restart.** Stages after the build work on what exists. When `impeccable` runs on a
  page the taste skill built, it is refining an existing page: do not start its init interview unless
  the user wants PRODUCT.md written.
- **Skip stages with nothing to do.** No data-fed components, no `break-ui`. No motion, no
  `review-animations`. Name the skipped stages and the reason in the report.
- **Check with the user only where a skill says to,** or before replacing their content or claims.
- **Small requests stay small.** A one-line fix gets its one skill from the table, not the pipeline.
