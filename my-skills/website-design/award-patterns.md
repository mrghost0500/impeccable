# Award patterns

What the top GSAP sites on Awwwards do, measured in November 2026, and the house version of each.
It adds to the taste skill's study of 99 Sites of the Day (`design-taste-frontend/references/motion.md`
section 2), which already covers curves, durations, staggers, scroll behaviours and their costs. Read
the section the master skill points to; you do not need the whole file.

**Sample.** Jury records for 9 winners (Lando Norris, Zentry, Terminal Industries, ERA Residence,
Floema, Why Zero, Slosh Seltzer, Agrumea Farm, Justin Jefferson). Six live sites studied in desktop
screenshots, five of them full-page and in their HTML (ERA Residence, Terminal Industries, King River
Wagyu, Floema, Lando Norris; Agrumea Farm by its first screen only), two in phone screenshots, and an
Awwwards juror's reasons for the year's best.

## 1. Motion plans

The kickoff asks how much movement the client wants. Each plan still passes the taste skill's gate.

| Plan | For | What moves | Built with |
|---|---|---|---|
| Calm | Services, clinics, law, local businesses, anything people read carefully | The taste skill's section entrances, feedback on every control, one moving picture. No scroll scenes, no smooth scroll. | The taste skill alone. A calm brief is a stated constraint, so leaving its dealt scenes out is within its rules. |
| Lively (recommended for most) | Brands, products, food, hospitality, studios | The taste skill's full motion layer: two or three scroll scenes, one signature move, page-to-page transitions on a site of several pages. | The taste skill's stage and recipes; `scroll-motion-engineering` for anything pinned or scrubbed. |
| Cinematic | Launches, flagship brands, portfolios, sites where the experience is the product | Lively, plus smooth scroll and one scrubbed journey: a filmed or generated video, an image sequence, or a 3D product. | `scroll-motion-engineering` for the engineering; footage from the client, Higgsfield or a 3D model from `img2threejs`. Ask before anything that costs credits. |

Whatever the plan: no loading screen (the taste study found they hide no slow load and cost
usability), the message readable on the first frame, every scene with a finished still state for
reduced motion, and a phone version that is designed, not stacked.

## 2. What the winners share, and the house version

- **The real thing is the hero.** Agrumea's actual jars, King River's grading boxes, ERA's building,
  Terminal's truck at dusk, Floema's benches in a city square. House: the taste skill's imagery rules
  and its idea taken from the subject.
- **Content is the interface.** The thing the business has many of becomes the navigation: Lando's
  helmet collection, Floema's catalogue as categories with counts ("Urban (51)"), King River's grades
  as data, ERA's floor plans with bedrooms and square metres per unit. House: the taste skill's "one
  live thing", chosen from this inventory.
- **The live thing feeds the main action.** Terminal's "What's your yard costing you?" calculator
  shows an estimated saving and asks for a work email in the same panel. House: when the one live
  thing produces a result, put the main action next to the result.
- **Business ideas by type.** Real estate: units by type with size and price, a location panel, the
  views. Food producer: the product and its origin, grades or varieties as data, where to buy. B2B or
  industrial: a cost or savings calculator, entry points by customer size, logos, a contact promise
  ("same day"). Product maker: the catalogue as categories, the product in use, material choices.
  Personal brand: the collection or record, the store, socials as a designed block.
- **Type at two extremes.** One oversized statement (ERA's headline at 230px) against small
  supporting text, usually in licensed typefaces. House: keep the scale contrast, but keep body text
  at the taste skill's sizes. The winners set body at 11 to 13px on five of six sites, and the type
  pairing should come from the dealt type system, not from copying.
- **One piece, not pages.** Dedicated page-transition libraries on three of five (Barba, Swup, Taxi,
  with Rive animations on Lando's). House: the taste skill's "Page to page" recipe on any site of
  several pages under the Lively and Cinematic plans.
- **Smooth scroll is the norm on these sites.** Lenis on five of six. House: Cinematic only, synced
  with GSAP ScrollTrigger as `scroll-motion-engineering` shows, off for touch and reduced motion.
- **The footer is a finale.** A giant wordmark (King River, Floema), a signature and the hero object
  again (Lando). House: the taste skill's curtain footer.
- **Consent is designed.** The European sites show a cookie banner set in the brand's own type and
  colour (Agrumea, ERA; Lando through a consent service). Floema runs cookie-free analytics
  (Plausible, Umami). See master section 7.
- **Two languages are common** for European businesses (Agrumea in Italian and English, Floema in
  several). Ask at kickoff; `seo-hreflang` checks the language tags.
- **Phones get their own layout on the best of them.** Lando turns the helmet wall into a two-column
  grid and keeps the store button within reach. Terminal stacks its desktop page into about 19 phone
  screens. House: `mobile-native` and the phone pass; aim well under the desktop length.
- **They are long.** Desktop pages ran 11 to 24 screens. House: the taste skill's limits on held
  stages; length has to be paid for with content.

## 3. Where winners lose points

Awwwards' Developer Award judges six criteria. Across the nine winners:

| Criterion | Range | Average | What it checks, and who covers it here |
|---|---|---|---|
| Animations / transitions | 8.0 to 8.8 | 8.33 | Highest on all nine. `review-animations`, the taste gate |
| Performance (WPO) | 7.0 to 8.2 | 7.76 | Load and responsiveness. Budget in `scroll-motion-engineering` section 12; `impeccable optimize` |
| Responsive design | 7.0 to 7.8 | 7.33 | The phone and tablet versions. Taste inspector at 390 and 768, `mobile-native`, `impeccable adapt` |
| Semantics / SEO | 6.6 to 7.8 | 7.29 | Headings, landmarks, search. `impeccable audit`, `seo-page` |
| Markup / meta-data | 6.8 to 7.6 | 7.24 | Titles, descriptions, share cards, structured data. `fixing-metadata`, `seo-schema` |
| Accessibility | 6.6 to 7.6 | 6.98 | Lowest or tied lowest on seven of nine. `impeccable audit`, `web-design-guidelines` |

What the live builds got wrong, in their HTML and screenshots:

- Images without descriptions on three of five: 180 of 198 on Lando's, 35 of 41 on ERA's and on
  Terminal's.
- No `prefers-reduced-motion` rule at all on two of five (ERA, Lando).
- A skip link on one of five. Five `h1` headings on ERA's page. No `nav` element on two of five.
- Content invisible until scrolled on two of five: their full-page captures are mostly blank slabs
  (ERA, Floema), which is what search engines, link previews and slow phones are shown.

**The review rubric.** Score the build out of 10 on each of the six criteria with the evidence
beside each score, fix anything under 8, and treat accessibility as the place to beat the winners.

## 4. The stack they use

GSAP is named on six of the nine winners' entries, loaded from a CDN on the Webflow builds (ERA:
GSAP with ScrollTrigger, SplitText and CustomEase) and bundled into the Nuxt and Next builds. GSAP is free in full since version 3.13,
SplitText and the other former paid plugins included. Lenis for smooth scroll. Three.js where the hero
is a product or a world (Agrumea, Justin Jefferson, Why Zero). Platforms: Webflow (ERA, Lando), Nuxt
(Agrumea, Floema), Vue (Terminal), Next (Justin Jefferson), WordPress (King River). The build skills
choose the stack for the project; nothing here is a reason to switch it.

## 5. An awards submission (optional, at hand-over)

If the client wants to enter the site for an award, prepare the material their entry form asks for
at that time: the title and address, a short description in the client's voice (`humanizer`), the
category and tags, the technologies, the credits, and desktop and phone screenshots of the strongest
screens. Check the form's current requirements first; they change.
