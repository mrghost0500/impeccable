# Scene library

Fifteen finished starting points for pages where the visitor stands inside one world. Each is a single
`index.html` with invented demo content, built on the shared files in `_shared/`, checked in a real
browser on a computer and a phone, with motion reduced and with JavaScript off. The rules behind them are
in `../scene-craft.md`; the data the skill searches is `catalog.json`.

## The scenes

| Scene | What visitors do | Suits | Motion | Built with |
|---|---|---|---|---|
| [scroll-film](scroll-film/) | Scroll a dawn journey drawn frame by frame, in chapters, to the departures | Tours, hotels, outdoor brands, launches with a film | Cinematic | Canvas, no libraries |
| [layered-hero](layered-hero/) | See the wordmark sit between sky and trees; layers part with the pointer | Hospitality, venues, fashion | Lively | SVG and CSS |
| [estate-walkthrough](estate-walkthrough/) | Glide room by room, one wheel turn per room, then book a viewing | Real estate, rentals, showrooms | Cinematic | Canvas, scroll snap |
| [world-configurator](world-configurator/) | Wipe the fogged glass, turn the product, pick a finish that recolours the world, add to bag | Single-product shops, colourways | Lively | three.js |
| [horizon-sea](horizon-sea/) | Leave a wake on a live sea; dusk turns to night as they scroll | Coastal hotels, wellness, calm luxury | Cinematic | three.js shader |
| [particle-form](particle-form/) | Scatter 60,000 points that drift back and re-form as the wordmark | AI and data products, labs | Cinematic | three.js points |
| [point-scan](point-scan/) | Watch a ruler fold into the mark, then dive into a point-drawn city | Architecture, engineering, mapping | Cinematic | three.js lines and points |
| [material-orb](material-orb/) | Talk to an assistant whose orb shows listening, thinking, answering | AI assistants, voice products | Lively | three.js shader |
| [world-dashboard](world-dashboard/) | See a working dashboard rise out of an aurora, cut at the fold | SaaS, analytics, fintech | Lively | three.js shader, SVG |
| [picture-tunnel](picture-tunnel/) | Drag a corridor of pictures that fold and split colour at speed | Photographers, studios, galleries | Lively | three.js |
| [zoom-constellation](zoom-constellation/) | Fly through photo tiles from one phrase to the next | Restaurants, retreats, wineries | Lively | CSS 3D only |
| [card-fan](card-fan/) | Watch cards rise, stack and fan; a marquee moves with the scroll | Food and drink, small ranges, subscriptions | Lively | GSAP, ScrollTrigger, Lenis |
| [texture-studio](texture-studio/) | Turn a photo into characters, dither, halftone, two-ink print or dots, export PNG | A tool for making on-brand images | Calm | Canvas |
| [ascii-ambient-app](ascii-ambient-app/) | Write a note over a kelp forest drawn in characters; Ctrl+K finds notes | Calm apps, journaling, AI tools | Lively | Canvas text |
| [world-story](world-story/) | Travel through four stations of one 3D world, settling on each | Tours, places, signature worlds | Cinematic | three.js, Lenis |

Each folder has `preview.jpg` (desktop, first screen). `scroll-film/preview-desktop.jpg` and
`preview-phone.jpg` show a whole scroll.

## Run one

The pages load modules, so open them through a local server, not by double-clicking:

```bash
cd ~/.claude/skills/website-design/scenes
python3 -m http.server 8000      # then open http://localhost:8000/horizon-sea/
```

Libraries come from jsDelivr at pinned versions (three 0.186.1, GSAP 3.15.0, Lenis 1.3.27). For a
client build, install the same versions with npm or vendor the files next to the page.

## Dials

Most scenes declare their settings at the top of the script and read overrides from the address bar:

```
horizon-sea/?waves=1.4&wake=1.5
world-configurator/?palette=tide&fog=false
particle-form/?word=NORTH&hue=2
texture-studio/?look=halftone&cell=10&paper=%23f3eee4&ink=%23111111
```

`catalog.json` lists every dial with its range. Use them to show a client options live, then set the
chosen values as defaults in the copy that goes into the project.

## Adapting one for a client

1. Copy the scene folder and `_shared/` into the project (or port the parts to its framework).
2. Replace everything in the scene's `swap` list in `catalog.json`: brand, words, pictures, frames,
   models, prices. The painted pictures from `_shared/painters.js` are stand-ins only.
3. Keep the fallbacks: the poster, the reduced-motion stills, the text that shows without JavaScript.
4. Run `node ../tools/check-page.mjs <folder>` until it reports nothing to fix.

## Shared files

- `_shared/scene.css`: tokens, header, display type, chips, cards, count pills, chapter rail, glass with
  a solid fallback, pause button, short-screen rules, reduced-motion rules.
- `_shared/runtime.js`: `boot`, `isReduced`, `loop` (pauses off screen and in hidden tabs), `pointer`,
  `reveals`, `sectionProgress`, `config` (dials), `qualityTier`, `motionPause`, `onScrollSettle`,
  `webglAvailable` and `fallbackToPoster`.
- `_shared/sequence.js`: `SequencePlayer` (frame sequences, landscape and portrait, coarse-to-fine
  loading) and `scrollFilm` (chapters, reduced-motion stills).
- `_shared/painters.js`: procedural stand-in pictures for the demos.

All demo brands, people, places and prices are invented.
