---
name: website-design
description: "Start here for any website or interface work: a new site or landing page, a redesign, an app screen or dashboard, a build from the user's own Figma design, changes to how an existing site looks or feels, motion, phones, design reviews, and getting ready to launch (page titles, share previews, search engines). This is the master skill over every installed design skill (impeccable, design-taste-frontend, ui-ux-pro-max, web-design-guidelines, Emil Kowalski's motion and polish skills, webapp-testing, fixing-metadata, the seo skills), Matt Pocock's engineering skills, and the connected design tools (Figma mockups, Wonder, Firecrawl, image generation). It takes the user through a few plain-language checkpoints, so someone who is not technical chooses the look, approves a mockup in Figma and signs off the result, and hands each stage to the right specialist. Use it instead of calling those skills directly, unless the user names one."
argument-hint: "[what to design or improve]"
---

# Website design

You run the job and the specialist skills do the stages. The user is your client and may not be
technical: they decide what the site is for, choose the look, approve a mockup and sign off the
result at a few checkpoints, in plain words. You make every technical decision yourself.

## Working with the user

- **Guided by default.** Stop at the checkpoints marked **(Ask)**. If the user says "just build it",
  "don't ask me", "surprise me" or "you decide", switch to quick mode: skip the checkpoints and the
  mockup, ask only for a fact that blocks the work, and list what you assumed in the final report.
- **Ask with the AskUserQuestion tool** when you have it: up to four questions a round, two to four
  options each, your recommendation first marked "(Recommended)", and one line under each option on
  what it means for their site. They can always type their own answer. Without the tool, ask in chat
  as a short numbered list they can answer with numbers.
- **Only ask what changes the work.** Never ask what the request already says or what you can find
  out yourself (their files, their current site). Never ask a technical question (framework, hosting
  setup, file formats): pick a sensible default and mention it in one line. "I don't know" means you
  pick and say what you picked.
- **Plain words.** Say "the top of the page", not "hero"; "the look", not "direction"; "how it works
  on phones", not "responsive"; "showing up on Google", not "SEO", unless they use the word first.
  When a technical word is unavoidable, explain it in a few words.
- **Show, do not describe.** At every checkpoint about the look, show pictures: the Figma link and a
  screenshot of the mockup, or screenshots of the built page on a computer and a phone. Send or attach
  the image files, or publish a preview page, whichever this environment offers.
- **Keep them posted.** Before a long stretch of work, say in one sentence what happens next and that
  you will come back with something to look at.
- **Two rounds of big changes per checkpoint at most.** After that, suggest moving on and note what
  is left for later.
- **Ask before anything that costs money or goes public:** generated images or video (credits), paid
  data services, payments, publishing the site.

## How to call a skill

- `impeccable`, `design-taste-frontend`, `ui-ux-pro-max` and `web-design-guidelines` are set to start
  only by name or through this skill: read `~/.claude/skills/<name>/SKILL.md` and follow it. In
  impeccable's text, `${CLAUDE_SKILL_DIR}` is `~/.claude/skills/impeccable`; in the taste skill's text,
  `<skill>` is `~/.claude/skills/design-taste-frontend`. Their reference files sit beside SKILL.md.
- Any other skill: invoke it with the Skill tool and pass the task as its argument. If the tool
  refuses because only the user can start it, read its SKILL.md and follow it instead.
- If the user names a skill ("use impeccable", "run the taste skill"), use that one.
- Hand every skill what the user already told you as its brief, and answer its own questions from
  that brief. Pass a question on to the user only when the brief cannot answer it and it blocks the
  work.

## 1. Pick the job

| The request | Lead | Go to |
|---|---|---|
| A new public site or page, or a full redesign of one: business, shop, restaurant, event, portfolio, product, landing page | `design-taste-frontend` | Section 2 |
| Build from a design the user already has in Figma (a figma.com link) | Their Figma design | Section 3 |
| A new app screen or docs: dashboard, admin, settings, editor, tool, help pages | `impeccable` | Section 4 |
| A change to something that exists: more striking, calmer, simpler, easier to read, better on phones, faster, better words | `impeccable` commands | Section 5 |
| A review with no changes yet | `impeccable` critique and audit, `web-design-guidelines` | Section 5 |
| Motion, one component, a quick question | The specialists | Section 6 |
| Page titles, share previews, Google, going live | `fixing-metadata`, the `seo` skills, `wizard` | Section 7 |

If you cannot tell a page from an app screen: a page is read and scrolled, an app screen is worked
in. A product site that shows its app is a page.

## 2. New public site

1. **Kickoff (Ask).** Read what exists first: their files, PRODUCT.md and DESIGN.md, and their
   current site if they have one (Firecrawl's `branding` format gives its colours, fonts and logo).
   Then ask what is still missing, in two rounds at most.
   - Round one, the purpose: what the site is for and who it is for; the one thing a visitor should
     do (call or book, buy, sign up, visit in person, get in touch, read about them); one page or
     several (home, about, menu or services, prices, contact); whether they already have a design in
     Figma (if so, go to section 3).
   - Round two, their material and taste: the feel, offered as the taste skill's tones that suit them
     (warm, bold, quiet, luxury, playful, editorial, technical: three or four of them, plus their own
     words); a logo, colours or fonts they want kept (then pass `--keep palette,type`); the photos they
     have (their own, product photos, screenshots of their app, none; from Google Drive if it is
     connected). With none, ask whether you should find free photos with credits, make images with an
     image tool (it costs credits), or leave marked spaces for their own. Sites they like, optional.
   - In the same rounds, ask for three or four things only they have: where they are, how they make
     it, the story behind the name, a number they are proud of. The taste skill builds the page's
     idea from exactly this. Facts you must not invent (prices, opening hours, address) go in here
     too; if someone else has to answer them, use `to-questionnaire`.
   - Read the brief back in five short lines and ask one question: is this right?
2. **The look (Ask).** `design-taste-frontend` steps 1 to 3 with the kickoff as the brief: inventory,
   argument, then the draw with `--options 3`, passing `--tone`, `--have` and `--keep` from the
   kickoff. Describe each of the three looks in two or three plain sentences (how it feels, its colours
   and type, how the page is arranged) and one line on why it could suit them, your pick first. Ask
   which one, with "show me three different ones" as an option. Deal the chosen one's full sheet, do
   step 4, and tell them the idea in one sentence ("Your page opens on ..., and visitors can ...").
3. **Words and mockup (Ask).** The taste skill's step 5 writes the words. Then, when Figma is
   connected, build a mockup of the home page (and one more key page if there are several) at
   computer width and phone width, following section 8. Show them the Figma link and the screenshot,
   and ask: love it, a few changes, or not right. They can also mark it up in Figma and tell you.
   Changes are made in the mockup and shown again; "not right" goes back to stage 2. Without Figma,
   skip this stage; stage 5 is their first look.
4. **Build.** The taste skill's steps 6 to 8: build, gate, look. Build what the user approved in the
   mockup. Use `ui-ux-pro-max` only to look things up (font pairings, usability rules, framework
   rules), never to choose the look.
5. **First look (Ask).** Screenshots of the real page on a computer and a phone. With a mockup
   approved, ask whether anything looks off compared with it; without one, ask how it feels (love it /
   close, a few changes / not right) and what they would change. "Not right" goes back to stage 2.
6. **Motion.** The taste skill's step 9. Build each move with `emil-design-eng`, its Animation
   Decision Framework and component rules; `apple-design` for drag, swipe and sheets.
7. **Hardening and testing.** `break-ui` on everything fed by real content (cards, prices, lists,
   quotes, forms). `mobile-native` for phones. `webapp-testing` to click every link, button and form
   and read the browser console. `impeccable harden` when there are forms or error states.
8. **Review.** In this order: `impeccable critique`, `impeccable audit` (accessibility lives there),
   `web-design-guidelines`, `review-animations`. Merge the findings into one list and fix them, then
   tell the user the five that mattered most, in plain words. Ask only when a fix would change their
   words or claims.
9. **Launch prep (Ask).** Section 7. Then `impeccable polish`, the taste gate once more (`lint.mjs`,
   `inspect.mjs`, and `scenes.mjs` when there are scroll scenes: 0 FAIL at every width), and
   `impeccable document` so DESIGN.md records the look for later changes.
10. **Hand-over (Ask).** Final screenshots and a short plain report: what was built and why it suits
    them; the Figma mockup link; what is still a placeholder for them to replace; photo credits; what
    you assumed; how to ask for changes later ("/website-design make the prices bigger"). Put the
    taste skill's step 10 report underneath for anyone technical. Ask: done, or more changes?

## 3. Build from the user's Figma design

Their design is the look, so there is no draw and no mockup stage.

1. **Kickoff (Ask),** as in section 2 but shorter: what the site is for, what visitors should do,
   which frames in the file are the pages to build, and anything in the design they already know they
   want changed.
2. **Read the design.** Load Figma's `figma-design-to-code` guide (section 8), then `create_session`
   and `get_design_context` for each page frame. On a limited Figma plan each read counts against the
   monthly allowance, so read each frame once and work from what you saved.
3. **Build.** A public page: the taste skill's steps 5 to 8 with the Figma design as the direction
   sheet; where the design and the house rules disagree, the design wins and you mention the
   difference in the report. An app screen: `impeccable` with the design as the brief.
4. **Then** stages 5 to 10 of section 2 (first look, motion, hardening, review, launch, hand-over).

## 4. New app screen or docs

App screens are designed in code, not in mockups: built screens of this kind come out better than
pictures of them. Make a Figma mockup only if the user asks for one.

1. **Kickoff (Ask).** Who uses it, the main task they come to do, what information it shows, and any
   existing look to match. Read the project first and skip what it answers.
2. **Look and build.** `impeccable`: its Setup, then new-work, with the kickoff as the brief. If
   impeccable offers its own choice of looks, that is the look checkpoint; do not ask twice.
3. **First look (Ask),** as in section 2, stage 5.
4. **Interaction detail.** `emil-design-eng` on buttons, menus, popovers, tooltips, tabs and
   transitions; `animate` for new motion. Logic behind the screen (filters, validation, sums, state)
   is built test-first with `tdd`.
5. **Hardening and testing.** `break-ui` on every table, list, card and form; `mobile-native` if it
   runs in a phone browser; `webapp-testing`; `impeccable harden`.
6. **Review,** as in section 2, stage 8.
7. **Polish and hand-over (Ask).** `impeccable polish`, then the hand-over as in section 2, stage 10.

## 5. Changes to what exists, and reviews

- Look at the current site first. A clear request maps to one `impeccable` command (`bolder`,
  `quieter`, `distill`, `typeset`, `layout`, `colorize`, `clarify`, `adapt`, `optimize`, `onboard`,
  `delight`, `overdrive`), then `impeccable polish` on what changed.
- **A vague request (Ask).** "Make it better" gets one question: what bothers you most? Looks plain
  (`bolder`), too busy (`quieter`), hard to read (`typeset`), cramped or messy (`layout`), bad on
  phones (`adapt` and `mobile-native`), slow (`optimize`), unclear words (`clarify`), or "not sure,
  have a look" (`impeccable critique`, then ask which findings to fix).
- **A review (Ask).** `impeccable critique`, `impeccable audit` and `web-design-guidelines`, merged into
  one plain list with the most important first. Ask which ones to fix.
- **Confirm (Ask).** Show before and after screenshots and ask whether to keep the change. For a big
  change to the look, offer to mock it up in Figma first.

## 6. Specialists

| Need | Skill |
|---|---|
| Build a move | `animate` |
| Where motion belongs | `find-animation-opportunities` |
| Audit all the motion in a codebase | `improve-animations` |
| Janky or stuttering motion | `animation-performance` |
| Gestures, sheets, springs | `apple-design` |
| Review motion | `review-animations` |
| Name an effect | `animation-vocabulary` |
| Polish the details of a component | `emil-design-eng` |
| Stress-test a component | `break-ui` |
| Feels wrong on a phone | `mobile-native`, then `impeccable adapt` |
| See versions before choosing (Ask: show them and let them pick) | `prototype` for one component; `impeccable generate` or `live` in the running page |
| Check the site works in a browser | `webapp-testing` |
| Which library to use; toasts | `pick-ui-library`; `ask-sonner` |
| Native apps | `impeccable` with the platform recorded in PRODUCT.md (`ios`, `android` or `adaptive`); `animate-expo`; `write-swift` |

## 7. Page titles, share previews, Google and going live

- **Before launch (Ask).** `fixing-metadata` needs three things from the user, asked together with
  your suggestions as the first options: the name to show in the browser tab and on Google, one
  sentence describing them for search results and link previews, and the picture shown when someone
  shares the link (make one from the page, use their logo, or skip).
- **Once the site is live (Ask).** Offer a full check of how it shows up on Google and in AI search.
  It needs a one-time setup that only the user can start, `/seo setup`, which takes a few minutes.
  Then `seo-page` for one page, `seo-audit` for the whole site, `seo-local` for a business people
  visit, `seo-schema` for rich results. `seo-google`, `seo-dataforseo`, `seo-maps` and `seo-image-gen`
  need paid accounts, and so does the Ahrefs connector; use them only if the user has one.
- **Selling things (Ask).** For a shop, bookings or donations with the Stripe connector connected,
  offer payment links or checkout. Ask before creating anything in their Stripe account.
- **Going live (Ask).** Ask whether they want help putting it online. Steps only they can do (buying
  a domain, creating a hosting account, pointing the domain at it) go through `wizard`.

## 8. Connected tools

Use a tool only when it is connected in this session; if one is missing, skip its step and say so in
the report.

**Figma, for mockups.**
- Load Figma's own guides before its tools, with `get_figma_skill`: `figma-use` and
  `figma-generate-design` before drawing, `figma-create-new-file` before making a file,
  `figma-design-to-code` before reading a design to build it. Call `create_session` with the file
  before any other file tool.
- Call `whoami` once (it is free). On a Starter plan, or with a View or Collab seat, Figma allows
  about 20 reads a month: `get_screenshot`, `get_metadata`, `get_design_context`, design-system
  searches. Writing with `use_figma` and making files are not limited. So take the mockup's picture
  inside the same `use_figma` call with `node.screenshot()`, never read back a mockup you drew
  yourself (you already know what is in it), and keep reads for designs the user changed. If the
  allowance runs out, carry on without Figma and tell the user plainly.
- Ask for their Figma file link if they have one for this project; otherwise make a file named after
  the project. One page per site, one frame per screen at 1440 and 390 wide, named "Home, computer",
  "Home, phone" and so on. Put the link in the hand-over.
- Draw the mockup from the direction sheet and the words: its fonts (check them with
  `listAvailableFontsAsync`; if a font is missing in Figma, use the closest one and say so), its
  palette and proportions, its sections in order, the real words. Follow the taste skill's house
  rules, so that what the user approves already passes the gate when built.
- Pictures: upload the photos the user gave or the taste skill found with `upload_assets`; otherwise
  grey boxes labelled with what goes there. Figma's `generate_image` uses Figma AI credits; ask first.

**Wonder,** a design canvas built from real code: use it for mockups instead of Figma when the user
prefers it or Figma is not connected. Load its `new-design` skill with `get_skills` first.

**Playwright** is installed as a library, not as a connector: the taste skill's inspector and
`webapp-testing` use it for screenshots and click-through tests. Nothing to connect.

**Firecrawl:** the `branding` format reads colours, fonts and logo from the user's current site or a
site they like; scraping and search check facts about the subject for the taste skill's inventory.

**Higgsfield:** images and short videos when the user has no photos and agreed to generated ones. It
costs credits: say roughly how many before you start. Use the
`anthropic-skills:higgsfield-creative-director` skill for the prompts when it is available.

**Google Drive** (when connected): the user's photos, logo and documents. **Stripe:** section 7.
**Ahrefs:** keyword ideas while writing the words, and search checks after launch (paid account).
**Zillow, Dubai Real Estate Data, Yardi Matrix:** real figures for property sites only, credited.
Apollo, Adspirer and Supermetrics are marketing tools and play no part in designing the site.

## 9. Engineering around the design (Matt Pocock)

The design skills decide how it looks and feels. These decide how the work is scoped, planned,
tested and shipped. Use one only when its moment comes up.

| Moment | Skill |
|---|---|
| The idea is vague and the user wants to think it through, or asks to be grilled | `grilling` (or `grill-me` when the user calls it) |
| A fact only the client knows blocks the brief | `to-questionnaire`, so the user can send the questions on |
| Facts about the subject, a library or an API need checking | `research` |
| A site of several pages, or more work than one session holds | `to-spec`, then `to-tickets`; `wayfinder` when even the route is unclear. Set the look once for the whole site in section 2 and write it into the spec, so every ticket follows it. Then build each ticket through the stages, or with `implement` |
| Interactive logic: forms, booking, price calculators, filters, carts | `tdd` |
| How components and modules are split | `codebase-design` |
| Something throws, fails or is broken | `diagnosing-bugs` (slow motion goes to `animation-performance`, slow pages to `impeccable optimize`) |
| Writing the pull request | `pr` |
| The session is getting long, or another agent will continue | `handoff` |
| The user wants a look back at how it went | `retro` |

`to-spec`, `to-tickets` and `wayfinder` publish to the issue tracker that `/setup-matt-pocock-skills`
sets up once per repo. If it has not run, ask the user to run it, or keep the spec and tickets as
local markdown files.

## Rules for combining

- **One lead, one look.** Never run impeccable's new-work and the taste skill's draw on the same
  surface. Every later stage refines the lead's look; no stage, tool, planning or engineering skill
  replaces it. An approved mockup is that look made concrete: the build follows it.
- **The user's brief wins, then the lead.** When two skills disagree, follow what the user asked for
  or approved, then the lead skill's house rules for that surface.
- **Refine, do not restart.** Stages after the build work on what exists. When `impeccable` runs on a
  page the taste skill built, it is refining an existing page: answer its init questions from the
  kickoff brief rather than starting its interview.
- **`ui-ux-pro-max` is a reference book.** Look things up in it; never take its style, palette or
  section order for a page another skill leads, and never save its design system.
- **Checks at the review stage.** Accessibility and the other rule checks run in the review stage,
  not while designing.
- **Motion.** On public pages the taste skill's motion count stands and Emil's rules decide how each
  move feels. On app screens Emil's restraint wins.
- **One record of the look.** DESIGN.md, written by `impeccable document` at the end. The taste
  skill's `.taste-skill/` working files stay as they are; the Figma file is the user's to keep.
- **Browser tests without Python's Playwright.** If `webapp-testing`'s Python scripts cannot import
  Playwright, write the same scripts in JavaScript with `require('playwright')`.
- **Skip stages with nothing to do,** and name them in the report: no content-fed components, no
  `break-ui`; no motion, no `review-animations`; no Figma, no mockup.
- **Small requests stay small.** A one-line fix gets its one skill, not the whole process.
- **Other whole-site skills on this account** (`web-art-direction`, `cinematic-website-builder`,
  `scroll-motion-engineering`) run only when the user names one.
