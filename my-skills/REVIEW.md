# Skill review

A review of every skill installed for website work, done before rebuilding `website-design`
(2026-11-03). What each one is for, where they overlap or clash, and what the master skill does about
it.

## What is installed, by job

| Job | Skills |
|---|---|
| Lead a new public page | `design-taste-frontend` |
| Lead app screens, docs and changes to existing UI | `impeccable` (24 commands) |
| Look things up: font pairings, usability rules, rules per framework, charts | `ui-ux-pro-max` |
| How motion and interaction feel | `emil-design-eng`, `animate`, `apple-design`, `improve-animations`, `find-animation-opportunities`, `animation-performance`, `animation-vocabulary` |
| Stress-testing | `break-ui`, `mobile-native`, `impeccable harden` / `adapt` |
| Reviewing | `impeccable critique` / `audit`, `web-design-guidelines`, `review-animations` |
| Testing in a real browser | `webapp-testing`, plus the taste skill's own inspector |
| Launch: titles, share previews, search engines | `fixing-metadata`, `seo` and 25 `seo-*` skills with 19 helper agents |
| Showing options | `prototype`, `impeccable generate` / `live` |
| Planning, testing logic, shipping (Matt Pocock) | `grilling`, `to-questionnaire`, `research`, `to-spec`, `to-tickets`, `wayfinder`, `implement`, `tdd`, `codebase-design`, `diagnosing-bugs`, `wizard`, `pr`, `handoff`, `retro` |
| Installed, outside the pipeline | `ask-sonner`, `pick-ui-library`, `animate-expo`, `write-swift`, and Matt's repo tools (`triage`, `domain-modeling`, `teach`, `writing-for-agents` and others) |

## Findings and what the master skill does

1. **Too many skills answer "design my website".** `impeccable`, `design-taste-frontend`,
   `ui-ux-pro-max` and `web-design-guidelines` all claim the same requests, so which one starts was
   down to chance. The setup script now marks those four as start-by-name-only, so `website-design` is
   the one automatic entry point and calls them itself. Typing `/impeccable` and the others still
   works. Set `ONLY_VIA_MASTER=0` in `setup-skills.sh` to undo it.
2. **Two complete design processes.** impeccable and the taste skill each pick a look and build
   from it. Running both on one page gives two looks fighting. One lead per page; everything after
   refines that lead's look.
3. **`ui-ux-pro-max` picks generic looks.** Asked for a warm coffee roastery site, its design-system
   search returned the stock sequence (big banner, three features, call to action) in a stock blue.
   That is what the taste skill exists to prevent. It is used for lookups only and never saves its
   own design system.
4. **The taste skill is told not to ask questions.** It decides and states its reading of a vague
   brief. The master asks the user first and hands the answers over as the brief, and the three looks
   the taste skill deals become a choice the user makes.
5. **Accessibility timing.** `ui-ux-pro-max` puts accessibility first while designing; impeccable
   keeps it for its audit on purpose, because reminders at design time make timid designs. Checks
   happen at the review stage.
6. **How much motion.** The taste skill requires at least eight moving elements on a page; Emil's
   rules question every animation. On public pages the taste count stands and Emil's rules decide how
   each move feels. On app screens Emil's restraint wins.
7. **Five reviewers.** impeccable critique, impeccable audit, `web-design-guidelines`,
   `review-animations` and Emil's table overlap. They run in a fixed order and the user gets one
   merged list in plain words.
8. **Records of the look in several places.** impeccable keeps PRODUCT.md and DESIGN.md, the taste
   skill keeps `.taste-skill/`, `ui-ux-pro-max` can write a `design-system/` folder. After a
   taste-led build, `impeccable document` writes DESIGN.md so later changes keep the same look.
9. **`webapp-testing` expects Python's Playwright,** which cloud sessions do not have. They do have
   Node's, so the same scripts are written in JavaScript there.
10. **`claude-seo` needs a one-time setup** (`/seo setup`, which only the user can start; it
    downloads about 20 Python packages and a browser) and most of its checks need the site to be
    live. Before launch, `fixing-metadata` covers titles and share previews; the full search check is
    offered once the site has an address.
11. **Some SEO skills need paid accounts:** `seo-dataforseo`, `seo-google`, `seo-maps` and
    `seo-image-gen`. They are installed but only used when the user has those accounts. The ten
    add-ons for other paid services (Ahrefs, Bing, Matomo and more) were left out.
12. **Built-in skills on this account overlap:** `web-art-direction`, `cinematic-website-builder`
    and `scroll-motion-engineering` also build whole sites. They cannot be switched off from here, so
    the master skill uses them only when the user names one.

## Connected tools (checked 2026-11-04)

| Tool | Helpful? | How the master skill uses it |
|---|---|---|
| Figma | Yes | Mockups of public pages for the user to approve before the build, and builds from the user's own Figma designs. Tested: this account can create files and draw in them. On the Starter plan with a View seat Figma allows about 20 reads a month (screenshots, reading designs back) and does not limit writing, so the skill takes screenshots inside its drawing calls and never reads back its own mockups. Figma's tools that turn a web page straight into a design are not offered on this plan, so mockups are drawn layer by layer. |
| Wonder | Yes, as a second choice | A canvas made of real code, for mockups when the user prefers it or Figma is missing. |
| Playwright | Already there | Not a connector: the library and Chromium are installed in cloud sessions, and the taste skill's inspector and `webapp-testing` use them. |
| Firecrawl | Yes | Reads colours, fonts and logo from the user's current site, and checks facts about the subject. |
| Higgsfield | Yes, when there are no photos | Generated images and short videos, after the user agrees to the credits. |
| Google Drive | Yes, once connected | The user's photos, logo and documents. Not connected yet. |
| Stripe | Only for sites that sell | Payment links or checkout. Connection not finished. |
| Ahrefs | After launch | Keyword ideas and search checks; paid account. Connection not finished. |
| Zillow, Dubai Real Estate Data, Yardi Matrix | Only for property sites | Real figures, credited. |
| Apollo, Adspirer, Supermetrics | No | Sales and marketing tools; no part in designing a site. |

## Gaps that remain

- Putting the site online. `wizard` walks the user through steps only they can do; there is no
  deploy skill. Vercel's `deploy-to-vercel` (in `vercel-labs/agent-skills`) would fill it.
- Pictures when the user has none. The taste skill finds free photos in open collections with
  credits; generated images need an image tool, which usually costs credits.
- Legal pages (privacy, cookies), analytics, and form handling are not covered by any skill.
