# Scene craft

How to build the cinematic and lively tier: pages where the visitor stands inside one world instead of
scrolling past boxes. Distilled from a study of HorizonX (19 template films measured frame by frame,
20 template write-ups, their docs) and the Awwwards GSAP winners in `award-patterns.md`. Read it when
the motion plan is Lively or Cinematic, or when the user shows a site like this and asks for the same
level.

Why it works, in HorizonX's own words: ask a model for a website from nothing and you get the average of
everything it has seen. A finished starting point, with the motion, depth and atmosphere already worked
out, is what lifts the result. That is what `scenes/` is for.

## 1. The ten rules

1. **One world per page.** The page is one place (a sea at dusk, a mesa, a city block, a lit room), not
   a stack of sections with their own backgrounds. 16 of the 19 films were one continuous take: the camera
   moves, the world never cuts.
2. **The camera tells the story, in chapters.** Three to five chapters, each a camera position with one
   short headline and one or two lines. A chapter list (rail, pills, counter) shows where the visitor is.
3. **The story ends at the conversion.** The last chapter is the booking, the bag, the viewing request or
   the access form, inside the world (a showroom, a booking card on the sea), not a footer link.
4. **Type lives in the scene.** Split the headline to opposite edges and leave the middle to the world;
   put the wordmark between photo layers; keep text where the picture is darkest. Giant display type
   against tiny interface type (11 to 12 px mono labels) is the signature contrast.
5. **Small, precise interface floats over the world.** Listing card with chips and price, count pills,
   a booking widget, a mini dashboard. Real data, real controls, glass or solid panels, never decoration.
6. **The world answers the visitor.** A wake on the water, particles that scatter and drift back, fish
   that flee, a fog pane they wipe clear, a product they turn. One response per page, felt within 100 ms.
7. **Choices change the world.** Picking a finish recolours the sky and ground, not just the product;
   typing makes the scene lean; a state change (thinking, answering) shows in the orb.
8. **Scenes change by dissolve, never by cut.** Pixel or dither dissolve, points flying apart, a fog
   that clears, a crossfade between rooms. Snap to the nearest chapter when scrolling stops, or move one
   room per wheel turn, so every resting state is a composed frame.
9. **An entrance moment, once.** A ruler that ticks and folds into the mark, fogged glass to wipe, a
   headline that unscrambles or rises out of a blur, a dashboard that lifts into place. Under 1.6 s,
   skippable, never for reduced motion, and the content is already underneath.
10. **It degrades to something finished.** Every scene has a still for reduced motion, a poster without
    WebGL, all text without JavaScript, a pause button when things move on their own (remembered per
    visitor), solid panels when transparency is reduced, lower pixel density and fewer particles on
    weaker devices, and a pause when the tab is hidden or the scene is off screen.

## 2. Craft details that separate the tiers

- **Frame sequences beat video** for scroll-driven films: frame-exact, scrubbable both ways, separate
  landscape and portrait sets, loaded coarse to fine (every 16th frame first). 150 to 421 frames in the
  studied templates. `tools/frames.sh` makes them from any film.
- **Procedural beats downloads** where it can: sea, sky, aurora, fire and particles drawn by shaders
  weigh kilobytes and stay sharp at any size. HorizonX's sea hero loads no images at all.
- **Settings in one place.** Speed, spread, colours and strength are named dials at the top of the
  script, readable from the address bar (`?palette=moss&spin=0.3`), so a client can see options live.
- **Pages tuned for four shapes:** phone, short phone, short laptop (under 640 px tall) and wide screen.
  Short screens tighten the hero instead of clipping it.
- **Lenis runs on the GSAP ticker** (`gsap.ticker.add(t => lenis.raf(t * 1000))`, `lagSmoothing(0)`)
  so pinned scenes and smooth scroll never drift. No Lenis under reduced motion.
- **Shaders write display colour.** A custom `ShaderMaterial` must end with
  `#include <colorspace_fragment>` (or author colours as display values and skip gamma), or everything
  comes out too dark or washed out.
- **Contrast is measured on the picture, not the page colour.** Place text over the darkest part of the
  world or darken the sky there; a gradient's brightest stop is what fails.
- **Decorative WebGL asks to fail fast.** HorizonX's own background effect creates its context with
  `failIfMajorPerformanceCaveat: true` and `powerPreference: 'low-power'`, so a device that would
  render it in software gets the still instead of a crawling page. Do the same for anything that is
  atmosphere rather than content; keep `high-performance` for the scene the page is about.
- **Preview films stream.** Long or many videos go through adaptive streaming (HLS), not one large
  MP4; short loops stay as small MP4 or WebM with a poster.
- **One fluid unit** (a `clamp()` scale tied to the window) keeps proportions identical from phone to
  wide screen.
- **Ship notes for the next person**: what to replace, where the dials are, how it degrades. HorizonX
  ships an AGENTS.md with every template; ours is `scenes/catalog.json` plus this file.

## 3. Getting the pictures

The templates bring the motion, the layout and the fallbacks. What made the studied pages look
expensive was the picture inside them, so settle where it comes from at kickoff (Ask), in this order:

1. **The client's own material.** A drone or phone film walked slowly through the place becomes a scroll
   film or a walkthrough with `tools/frames.sh`; one strong photograph becomes a layered hero (a
   background plate plus a cut-out of the foreground; cut-outs from an image tool or a photo editor).
2. **Made in code.** Sea, sky, aurora, fire, particles, point clouds, terrain and simple products are
   procedural in these scenes and cost nothing to load. Prefer this whenever the subject allows.
3. **Generated (costs credits, ask first).** A still in the chosen look from an image tool, then a short
   camera move from a video tool (Higgsfield when connected), then `tools/frames.sh`. Keep one camera
   move per chapter, slow and level, 4 to 8 seconds; generate the portrait version separately rather
   than cropping when the subject is wide. Check every frame for warped hands, text and logos.
4. **3D models.** A glTF of the product from the client's maker, or `img2threejs` for a simple object
   from a photo. Compress with Draco or Meshopt; keep the hero model under 2 MB.

Never ship the painted stand-ins from `_shared/painters.js`, and never use pictures from the reference
sites or paid libraries that were studied.

## 4. Using the scene library

`scenes/catalog.json` lists 15 scenes with what each suits, its dials, what to replace for a client and
how it degrades. `scenes/README.md` is the same list for people, with previews.

1. **Shortlist.** From the kickoff (kind of business, mode, motion plan), pick the two or three scenes
   whose `bestFor` and `motion` fit. Never offer a Cinematic scene to a business that chose Calm.
2. **Let the user choose (Ask).** Show each scene's `preview.jpg` with one line on what visitors will
   do there, your pick first. "None of these" is an option; then build from the rules above without a
   template.
3. **Tune live.** Open the scene with dials in the address bar to try colours and strength with the user
   before writing code. Then copy the scene into the project and set the dials as defaults.
4. **Replace every stand-in.** Brand, words (through `humanizer`), pictures, frames, models, prices. The
   painted stand-ins in `_shared/painters.js` must not survive into a client site. Keep the fallbacks.
5. **Check it.** `node tools/check-page.mjs <folder or url>`: desktop, scroll positions, phone, reduced
   motion and JavaScript off, with errors, sideways scroll, invisible text, missing title or
   description. 0 must-fix items before the user sees it. Then `tools/scroll-preview.mjs` for the image
   you send them.

## 5. Studying a site the user loves

When the user points at a site and says "like this":

1. `node tools/study-site.mjs <url>`: libraries, canvases and WebGL, videos, fonts, colours, type scale,
   sticky elements, weight, eight scroll frames. Firecrawl's `branding` format adds the palette and
   logo. If the site shows films (product previews, showreels), take frames with ffmpeg and look at
   them in sequence: pacing and transitions show there.
2. If REA (the reverse-engineering MCP) is installed and the user has allowed it, its browser
   observation tools (`inspect_web_page`, `analyze_web_bundle`, `capture_browser_scenario`) give
   deeper evidence: script modules, network timeline, scenario screenshots.
3. Write three to five plain sentences on what makes it work, mapped to the ten rules above, and show
   them to the user. Build those ideas with our own content and code.
4. Never copy code, images, names, copy or 3D models from a paid or licensed library, even when they
   are reachable. Evidence is for understanding; the build is ours.
