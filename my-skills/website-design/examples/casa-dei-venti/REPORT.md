# Casa dei Venti: run report

A full run of the website-design skill on one brief, kept as a worked example. The hotel, its story,
prices, times and people are invented; the photographs were generated for this example.

## The run

| Stage | What happened |
|---|---|
| Kickoff | Book a room; one long page in English; quiet luxury; the story of a 1928 lemon merchant's house with twelve rooms named for the winds. Client confirmed. |
| Look | Taste skill draw, sector hospitality, tone luxury, `--have photography`, three options. Chosen: **The place carries it** (seed 2065965846). Type Archivo, olive on bone, film-title hero. No redraws. |
| Motion and scene | Cinematic plan. Scene: the estate walkthrough, rebuilt in the look's own type and buttons (its mono captions, room counter and glass card do not survive the taste house rules). |
| Pictures | Ten photographs from Figma's `generate_image` (gpt-image-2.5-flare), generated straight into the mockup file with one shared style line and one sentence per shot. Downloaded at 1536 × 864 (16:9), 960 × 1280 (3:4) and 1024 × 1024, then WebP at 640, 1024 and native width, plus a 1200 × 630 share picture. |
| Mockup | Figma, computer and phone width, real words and the generated pictures. Approved first time. |
| Build | Static HTML, self-hosted Archivo (Fontsource, OFL), no libraries. |
| Gate | `lint.mjs` 0 FAIL; `inspect.mjs` 0 FAIL, 2 WARN defended (below), after five rounds of fixes. |
| Critique | Two rounds with `references/critique.md`. |
| Checks | `tools/check-page.mjs`: nothing to fix. `impeccable detect`: 0 findings (one rule scoped off with measured evidence). |

## Idea and live thing

- Idea: the twelve winds the rooms are named after become a wind rose that leads to each room. The rose
  is true to the compass: tower suites north, sunrise rooms east, rock suites south, lemon rooms
  south-west, sunset rooms west to north-west, where the summer sun sets.
- Live thing: choose the light you want to wake up to; the rose lights the rooms that face it and links
  to them. The booking card quotes the price as dates, room and guests change, and says when a room
  sleeps fewer guests than chosen.

## Scores

Design rubric (`references/critique.md`, a juror's view; real Sites of the Day land at 7.5 to 8.0):

| Round | Design | Usability | Creativity | Content | Overall |
|---|---|---|---|---|---|
| 1 | 8.0 | 8.0 | 8.0 | 8.5 | 8.1 |
| 2 | 8.5 | 8.5 | 8.5 | 8.5 | 8.5 |

Developer Award criteria, measured (the nine studied winners' jury averages in brackets):

| Criterion | Score | Evidence |
|---|---|---|
| Animations | 8.5 (8.3) | Slow push-in on the first picture; staggered entrances in every section; rooms cross-fade with a push-in and a card that never overlaps the next; rose petals and wind buttons respond; press, hover and focus on every control; reduced motion keeps every state. No transitions between pages (one page) and no film. |
| Performance | 9.5 (7.8) | Main content in 0.12 s locally, layout shift 0, blocking 0 ms, 16 requests, about 1 MB on first view (all pictures WebP with srcset, lazy below the fold, fonts self-hosted and preloaded). |
| Responsive | 9.0 (7.3) | No sideways scroll at 320, 390, 768, 1024 × 600 and 1920; phone layouts composed (two-line name, docked room cards, focal point per room photo, scaled rose); every target 44 px or more. |
| Semantics / SEO | 9.0 (7.3) | One h1, clean outline (h2 per section, h3 inside), header, nav, main and footer, 563 words readable without JavaScript, descriptive alt text, Hotel JSON-LD. |
| Markup / meta | 8.5 (7.2) | Title, description, canonical, Open Graph with sized share picture and alt, Twitter card, theme colour, JSON-LD. Held under 9 only because the address is example.com until launch (`check-page --launch` fails until it changes). |
| Accessibility | 9.0 (7.0) | Skip link; 42 keyboard stops, each with a visible focus ring; the rose works with arrow keys; no unnamed control or image; form labels and live quote; reduced motion; contrast of the opening sentence measured on the photograph with the letters hidden: at least 5.18 behind 90% of it. Not yet tried with a screen reader. |

## Defended warnings

- No footage: nothing honest to show without a video model (Weave was not linked). The first picture
  moves instead.
- Room cards over pictures: the cards are opaque panels, as the direction's blueprint specifies; no
  text sits on the photograph.

## What still holds it under 9 on the design rubric

1. Generated stills, not a film. A slow camera move through the house would lift design and creativity.
2. Archivo is sound but common. A drawn wordmark for the name would give the first and last screens
   something no other hotel has.
3. The signature motion is good rather than unforgettable: a wind that visibly moves the page (the rose
   turning to the chosen wind, the light in the first picture shifting with it) is the next step.

## Sample content to confirm before launch

Prices, room sizes, times, the dinner menu, the address, the telephone number, the email address,
Marta at the desk, the 75-minute airport transfer, the ramp to Garbino.
