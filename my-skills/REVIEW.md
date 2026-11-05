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
| Agreeing on the feel with reference sites | `website-design/reference-sites/` (84 write-ups from awesome-design-md) |
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

13. **Reference sites (added 2026-11-05).** `VoltAgent/awesome-design-md` holds write-ups of how 84
    well-known sites look: colours, type, spacing, components, do's and don'ts. Useful for a user who
    is not a designer, who can name a site they like more easily than describe a feel. Two risks:
    each file is another company's identity, and taking one as the look goes against the taste
    skill's rule that the idea comes from the subject. They are installed inside `website-design`
    and used at kickoff for qualities only (how dense, how big the type, how colour and photos are
    used), never for logos, colours, typefaces, motifs or words. A few files contain brand rules
    worded as orders and mention install commands; the skill treats them as reference material.

14. **Effect libraries (checked 2026-11-05).** Four repos were weighed for the skill:

    | Repo | Verdict | Why |
    |---|---|---|
    | `pmndrs/react-three-fiber` (33.5k stars, MIT, active) | Yes, for real 3D only | The standard way to put a 3D object in a React site; fits a page whose one live thing is a product to turn round or configure. Used through `impeccable overdrive`, with drei. |
    | `dashersw/liquid-glass-js` (1.7k, MIT, last change June 2025) | No | Glass panels are banned by the taste skill and impeccable; it also screenshots the whole page with html2canvas to fake the refraction, which is slow and breaks on many pages. |
    | `ruucm/shadergradient` (3.1k, MIT) | No | Moving gradient backgrounds are the commonest sign of a generated page, and both design skills ban gradients used this way. |
    | `paper-design/liquid-logo` (1.4k, PolyForm Shield) | No, use Paper Shaders instead | A demo app under a license that is not open source, pinned to an old `@paper-design/shaders-react`. The maintained library, `paper-design/shaders` (Apache-2.0), has the same liquid-metal effect and about 30 others. |

15. **More repos (checked 2026-11-05).**

    | Repo | Verdict | Why |
    |---|---|---|
    | `heygen-com/hyperframes` (79k stars, Apache-2.0) | Yes, its 4 core skills | Renders HTML to video, so a looping clip for a page or a launch film can be made from the site's own look. Needs Node 22 and ffmpeg, both present. Its HeyGen features cost money. Its skill sends a usage ping to HeyGen each time it starts, so the setup script sets `HYPERFRAMES_NO_TELEMETRY=1` in `~/.claude/settings.json`, which the CLI checks before anything else. The other five skills (slideshows, copying videos, porting from Remotion) are not website work. |
    | `tt-a1i/archify` (94k, Apache-2.0) | Yes | Diagrams as standalone HTML. A page map and a visitor journey help a user who is not technical check a multi-page site before the build. Needs only Node. |
    | `mrghost0500/ui-ux-pro-max-skill`, its other six skills | No | `ui-ux-pro-max` is already installed. `brand`, `design-system` and `ui-styling` repeat what the taste skill, impeccable and the master skill do; `slides` is not website work; `banner-design` is marketing; `design` needs a paid Gemini key. |
    | `multica-ai/andrej-karpathy-skills` (230k, MIT per README) | Yes, per session | A 2.4 KB set of coding guidelines. Kept out of the skills folder and offered at the start of each session. |
    | `obra/superpowers` (313k, MIT) | Yes, per session | A skills framework for planning, test-first work, debugging and review. Installed as a plugin it injects its 3 KB guide into every session and lists 14 skills; here it is offered at the start of each session instead. Its guide insists on brainstorming before any build, which would duplicate `website-design`'s kickoff, and its process skills overlap Matt Pocock's; its load note settles both. |

16. **ECC and img2threejs (checked 2026-11-05).**

    | Repo | Verdict | Why |
    |---|---|---|
    | `affaan-m/ECC` (298k stars, MIT) | Yes, per session | 71 agents, 314 skills, 98 commands, rules and hooks. Registered as skills, its descriptions alone (about 37 KB) would go far past Claude Code's allowance for the skill list, which then shortens every skill's description, the design skills' included. So it is offered at the start of each session and used by lookup: on a yes Claude reads its ten common rules (19 KB) and a short index of its 47 core skills, and finds the rest by searching. Its hooks are left out, because they would run in every session. It overlaps Superpowers; when both are on, Superpowers runs the process. |
    | `img2threejs/img2threejs` (20k, Apache-2.0) | Yes, for the 3D route | Rebuilds the object in a photo as a Three.js model written in code: free, small and easy to recolour, which suits product configurators. Python standard library and Node only. It reports when a photo cannot reach the fidelity wanted. Used through `impeccable overdrive`, like React Three Fiber. |

17. **21st MCP, formerly Magic MCP (checked 2026-11-05): not added.** `21st-dev/magic-mcp` (6.4k
    stars, ISC) is now a proxy for the hosted 21st MCP: a catalog of 10,000+ React and Tailwind
    components, brand-logo lookup, and AI UI generation, behind a 21st.dev API key (free tier: search
    and 2 component installs a day; AI generation and some components are paid). Its bundled skill
    says to prefer catalog components over writing UI and starts on the same requests as
    `website-design` (a pricing section, a hero, a navbar). Stock components are the template look the
    design skills exist to avoid, many in the catalog use the animated gradients and glass they ban,
    and its generator would be a second process choosing the look. The useful parts are narrow: logos
    of other companies as SVG for an integrations or payments row, and the odd complex widget for an
    app screen. If it is ever added, take the MCP server alone, without its `21st-ui` skill, with the
    key saved as an environment secret.

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
