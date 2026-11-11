# DIRECTION SHEET: The place carries it
seed 2065965846 · drawn 2026-11-11 · sector hospitality · tone luxury
Brief: Casa dei Venti: a 12-room clifftop hotel in a 1928 lemon merchant's house on an Amalfi-style coast; each room named after a Mediterranean wind; 214 steps to a private swimming rock; boat to town at 8:00 and 19:00; open April to October

| | |
| --- | --- |
| Direction | The place carries it |
| Hero | Film title, bottom edge |
| Type | Archivo |
| Colour | Olive on bone |
| Sections | intro (Right-half paragraph, lone photo) → showcase (Close-up with column card) → list (The printed menu sheet) → faq (Questions beside a tall photograph) → contact (Visit card on a photograph) → footer (The back of the card) |
| Motion | Slow crossfade |
| Photographs | the "Coast" set, as atmosphere |

This is the direction for this build. Adopt it. Do not blend it with the layout you would have made anyway,
and do not redraw because it is unfamiliar: unfamiliar is the point. Redraw a slot only when it conflicts
with a stated brand constraint or needs an asset that does not exist, and say why in your report.

The parts of this sheet were written separately and will disagree in small ways. Settle every disagreement in this order:
**house rules** (including type no smaller than 13px and body text of 16px or more) → **the direction** (the idea, the composition habits, where the
one accent goes) → **the type system and the palette** (which face does which job, the five size steps, which colour is the ground and where the
accent goes) → **the hero blueprint** → **the section blueprints**. Under each blueprint below, "Adjusted for this page" lists where it disagrees.
In practice: take geometry from blueprints (columns, proportions, what sits where) and take everything else from above them. Map every size a
blueprint names onto one of your five type steps instead of adding a sixth. Use one button shape, one corner radius and one pair of page margins on
the whole page, whatever individual blueprints say. If a blueprint names a kind of typeface (a light serif, a heavy grotesk), use the dealt face.

## 1. The idea
For a place, the photograph is the argument. One full-bleed image of where you would be standing fills the first screen, and the design steps back: the name sits along the bottom edge like a film title, or small in a corner, and nothing else interrupts the view. The page that follows keeps that restraint: few words, large pictures, long pauses. The designer's work here is editing: choosing the one frame that makes someone want to be there, and then not covering it.

Before anything else, write one sentence in your notes: "On this page, <the subject's own material> becomes <the device>."
Fill the first blank from your inventory of what only this client has (its name and what it means, its street, its numbers, its
constraint), then put the nearest competitor in the sentence: if it still works, the idea is the category's, not the client's.
Then name the one live thing the visitor can do on the page (SKILL.md step 4).

## 2. Composition
First screen: a single photograph at 100vw by 100svh, focal point kept clear of text. The name is set either very large (14–20vw) hugging the bottom edge with 16–24px of margin, or small (20–28px) top-left with a one-line description bottom-left. Navigation is two to four words in the top corners in the same small size. If text sits on the image, a soft neutral scrim under the text area only. Below, sections alternate between a short centred or left-set paragraph in a narrow column (max 52ch) with wide empty margins, and photographs shown large: one full-bleed, then a pair at different sizes, then one portrait offset to the right. Practical information (hours, address, rates, booking) is gathered once near the end in a plain two-column block.

## 3. Type: Archivo
A sturdy grotesque kept at regular weight even at 88px, so the page reads as composed rather than loud. Suits finance, infrastructure and research pages that need to look sober and current.
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;600&display=swap" rel="stylesheet">
```
- Display: **Archivo**: weight 400 · tracking -0.02em · leading 1.0 · sentence case; never bold, inactive items fade to grey
- Text: **Archivo**: 400 for body, 600 for buttons and short emphasis · leading 1.5 · tracking 0
```css
:root {
  --step-small: clamp(0.8125rem, 0.79rem + 0.1vw, 0.875rem);
  --step-body: clamp(1.0625rem, 1rem + 0.25vw, 1.1875rem);
  --step-lead: clamp(1.25rem, 1.1rem + 0.7vw, 1.625rem);
  --step-head: clamp(2rem, 1.3rem + 3.2vw, 4rem);
}
```
A face with some grace for the name; small, calm, well-spaced text everywhere else. Sentence case. Body 17–19px with leading around 1.55.
The direction decides sizes and how many of them; the type system decides how this face is set. Where the two give different tracking or leading, use the values of the type system: they are tuned to this face.
The display size itself comes from the hero blueprint below.

## 4. Colour: Olive on bone
```css
:root {
  --bg: #ecebe7;
  --surface: #e1dfd9;
  --ink: #38450f;
  --muted: #5d683a;
  --accent: #38450f;
  --accent-ink: #ecebe7;
  --field-1: #38450f;  --field-1-ink: #ecebe7;
}
```
A bone page with every word, large or small, in one olive green; the footer inverts to a solid olive field with bone text. Photography supplies all other colour, and the button is the same olive, filled.
Neutral paper or deep neutral ground chosen to flatter the photographs; text ink drawn from the darkest tone in the imagery. Colour lives in the pictures.

## 5. Imagery
**Use the images that belong to the project in every picture slot.** For slots they cannot fill, real pictures of the subject's world from the open collections come next (start with `node /root/.claude/skills/design-taste-frontend/scripts/assets.mjs "clifftop hotel"`, then queries from your inventory (its street, its materials, its trade's tools and history); credit them on the page), then the dealt photographs.

The dealt set is the palette. Choose four to six photographs with the same light. The hero image must have a calm area for the name. Full-bleed or large with square corners; never thumbnails, never a carousel of ten.

**Floor (the inspector checks it):** at least four real pictures on the page, usually six to twelve; SVG drawings do not count. One moving picture where an honest clip exists: `node <skill>/scripts/assets.mjs --video "<query>"`, used as a muted loop with a poster frame. Whatever this direction says about pictures, it is carried out with real ones.

Photographs dealt for this build, from the "Coast" set (sea, shoreline, cliffs, piers and beaches)
Order of preference for imagery: (1) the project's own photographs and product shots; (2) images you generate, if an image tool is
available; (3) real pictures of the subject's world found in the open collections (assets.mjs, downloaded and credited on the page);
(4) drawings of the subject in code; (5) these. They are real photographs (Unsplash licence, served by picsum.photos) of places, light and
texture. They are atmosphere, never a stand-in for a specific product, dish, person or interface. List the ones you use in your report so
they can be replaced.
Treatment: Leave photographs ungraded. If text overlays one, darken only the area behind the text with a neutral scrim.
- `https://picsum.photos/id/626/1600/1000`: Red and white lighthouse in turquoise sea below a chalk cliff · light tone · turquoise, white, grass green · calm area: left · native landscape · photo: Nick Diamantidis
- `https://picsum.photos/id/162/1600/1000`: Aerial view of a coastline with turquoise sea and patchwork fields · mid tone · turquoise, sand brown, deep blue · calm area: bottom · native landscape · photo: Dillon McIntosh
- `https://picsum.photos/id/440/1600/1000`: Rugged coastal headlands in soft backlit haze at sunset · mid tone · pale gold, warm brown, cream · calm area: left · native landscape · photo: Artur Pokusin
- `https://picsum.photos/id/851/1600/1000`: Aerial view of turquoise sea meeting a curved reddish coastline · mid tone · turquoise, teal, rust brown · calm area: left · native landscape · photo: Tiago Aguiar
- `https://picsum.photos/id/374/1600/1000`: Coastline with green headlands, a curving beach and turquoise sea · mid tone · turquoise, deep green, sky blue · calm area: top · native landscape · photo: Ma. Alejandra
- `https://picsum.photos/id/640/1600/1000`: Aerial view of turquoise surf breaking onto golden sand · mid tone · sand, turquoise, white · calm area: bottom · native landscape · photo: Sarah Bürvenich
- `https://picsum.photos/id/1049/1600/1000`: Rock island reflected on a wet beach under a pale sky · light tone · pale grey, soft white, dark green · calm area: top · native landscape · photo: Rosan Harmens
- `https://picsum.photos/id/77/1600/1000`: Wooden jetty leading to a small pavilion over calm sea · mid tone · warm tan, pale teal, soft grey · calm area: top · native landscape · photo: May Pamintuan
The last two path numbers are width and height: request the exact crop you render (`/1200/1500` for a 4:5 portrait, `/2400/1350` for a hero) and
add `?grayscale` to desaturate. Use three to six of them, not all eight. Always set `width`, `height`, `alt` and `loading="lazy"` (not on the hero image).
Other sets that fit this brief: interior-and-table, fog-and-quiet, mountain, architecture: `node draw.mjs --photos <set>` prints one in full; `--photos list` shows all sets. Taking photographs from another set is your call and is not a redraw; keep them to one light and one treatment.

## 6. Hero: Film title, bottom edge
One photograph fills the viewport at 100vw by 100svh, `object-fit: cover`, with its subject in the upper two-thirds and a calmer, darker zone along the bottom. The name is one condensed uppercase word, or a short name in a high-contrast serif, set at clamp(150px, 17.5vw, 290px) and sized to span the full width between 32px margins. It is centred and anchored so its baseline sits 34px above the bottom edge, covering roughly the lowest quarter of the frame. A soft neutral dark scrim lies under that bottom band only, about 40% of the height; the rest of the image is untouched. Directly above the name's left end, on the same margin, sits the supporting sentence at 16px on two short lines. Directly above its right end, right-aligned, sits the single action as a small paper-coloured rectangular button. The top edge carries a small emblem or wordmark at the left margin and up to five text links at 15px grouped at the right, all in white. The central half of the screen belongs to the view.

On a phone: The photograph is re-cropped to portrait with `object-position` on its subject and fills 100svh. The name stays on the bottom edge at 22vw on one line, or two lines at 20vw beyond eight characters, 20px above the edge. The supporting sentence sits above the name's left end at 15px. The action button moves to the top-right corner and the links collapse to a menu word beside the emblem.
Headline: The name of the place: one word of up to about 12 characters at 17.5vw, or two words stacked on a phone.

Adjusted for this page:
- It names a kind of typeface: use the dealt faces (display Archivo, text Archivo) and their settings; capitals only where the type system sets them.
- It names colours (white): map them onto this palette's roles (ground `--bg`, panels `--surface` and the fields, text `--ink`/`--muted`, the accent `--accent` on the primary action only).

## 7. Sections, in order
Each is a composition to rebuild with this project's content. Keep the geometry; change the subject. Re-order or drop a
section when the argument of the page needs it (see references/copy.md), never to fall back to a card grid.

### 1. intro: Right-half paragraph, lone photo (split)
No heading. On a 12-column grid with 5vw margins, one statement paragraph of 45–70 words occupies columns 7–12 only, set at clamp(24px, 2.2vw, 34px) with leading 1.25 and a first-line indent of 3em. Its top edge sits 18vh below the section top. Columns 1–6 stay empty except for a single square photograph, 20vw wide, in columns 1–3, placed so its top aligns with the paragraph's last line and it hangs below the text by most of its height. A five-line note at 14px, 180px wide, sits in columns 1–2, 96px beneath the photograph. Section padding is 160px top and bottom. Nothing is centred: the paragraph's left edge is the midpoint of the page, and later text blocks on the page may reuse that line. Holds one paragraph, one photograph and one note.
On a phone: The paragraph comes first at 22px, full width with 20px margins and no indent. The photograph follows at 62% width, pushed to the right margin, in a 4:5 crop instead of square. The small note sits to its left, bottom-aligned with the photograph, in the remaining 30% of the width.

### 2. showcase: Close-up with column card (full-bleed)
A full-bleed close-up photograph, 100vw by 100svh, with nothing over most of it. A four-column grid lies on top. One solid card in the ink colour, exactly one grid column wide (about 22vw) and 52svh tall, sits in the second column, vertically centred. Inside it, centred: the item's name at 30–36px, a variant line at 17px, the price or key fact at 17px, a small 3:2 photograph of the whole object (the card shows the whole, the background shows the detail), and at the foot a square-cornered action filling the card's width. The card is opaque, radius 0–6px, with no blur. When the section presents two or three items, each gets its own full-bleed frame and its card moves one column to the right each time, so position carries the sequence. The first card's name is the section heading.
On a phone: The photograph fills 100svh, cropped to its most detailed area. The card becomes a full-width block docked to the bottom, 46svh tall, left-aligned inside with 20px padding; the small whole-object photograph sits to the right of the name at 96px wide.

### 3. list: The printed menu sheet (band)
The list is one tall sheet of paper. A filled paper-colour panel 640px wide sits centred, or offset to columns 7–12, on a contrasting flat ground or a full-bleed photograph, with square corners and its top and bottom edges cut into shallow scallops by `clip-path` or an SVG `mask`. Inside, 64px padding and a centred, symmetrical setting like a printed card: the venue or section name at 40–48px, a one-line note at 15px, then three or four groups 56px apart. Each group opens with its name at 22px, centred. Items follow at 17px with 16px between them: the dish or service at the left of a 420px measure, the price at the right with tabular figures, and a one-line description at 14px in the soft ink under the name. Alignment alone links name and price; there are no leaders. The sheet ends with the opening hours as two centred lines. Holds 12–24 items.
On a phone: The sheet spans the screen with 10px of ground showing at each side and 28px padding; the scalloped edges stay at top and bottom. The measure is the full inner width and prices stay right-aligned. Group names at 20px, items at 16px.

### 4. faq: Questions beside a tall photograph (split)
One field in a deep or pale flat tone, split 5 to 7. Left, columns 1–5: a heading of two to four words at 36–44px; under it the three or four practical facts people ask first (address, times, how to arrive) as plain lines at 18px; then five or six questions as an accordion with no lines between rows, only 28px of space. Each question is a `<summary>` at 20px with a small chevron drawn from two 2px strokes at its right; the open answer sits beneath at 17px in the softer ink, on the same left edge. One filled button and one text link close the column. Right, columns 7–12: a tall photograph (3:4) that bleeds off the top edge of the section and stops 80px short of the bottom, with a second, square photograph a third of its width overlapping its lower-left corner by 40px.
On a phone: The tall photograph leads at full width, 4:5, with the square one overlapping its bottom-right corner at 38% width. Heading at 30px, facts at 17px, then the accordion at full width with 24px between questions and 44px touch targets. Button full width at the end.

### 5. contact: Visit card on a photograph (full-bleed)
A full-bleed photograph of the place, 100vw by 100svh, carries one solid card and nothing else. The card is a filled panel in the paper colour, fully opaque, 380px wide with 8px corners and 32px padding, placed in the upper-right corner 60px from the top and right edges (or the upper-left: pick the corner where the photograph is calmest). It holds, top to bottom: a two- or three-word title at 28px in a light weight; the address on two lines at 16px; the opening hours as three rows with days at the left and times right-aligned in tabular figures; the phone number; then, flush with the card's bottom edge and spanning its width, a solid booking button 52px tall. The card may be `position: sticky; top: 60px` inside a taller section so it holds while the photograph scrolls beneath it. The photograph's focal point must stay clear of the card. No heading outside the card.
On a phone: The photograph is 100vw by 70svh. The card leaves the corner: it spans the width with 16px margins and overlaps the photograph's bottom edge by 80px, so image and card interlock. The booking button is full width, 56px tall, at the card's bottom.

### 6. footer: The back of the card (stack)
The footer is the reverse side of the page's artefact, laid out as the back of a postcard. A paper-coloured panel spans columns 2–11 on the contrasting ground, about 420px tall, its top edge cut into a row of twelve semicircular scallops (an inline SVG path or `clip-path`, each scallop about 100px wide). The panel is divided by space into two halves. Left half: a short sign-off of two to four words at 32px, then two or three lines at 16px, written like a message. Right half: the address block, four left-aligned lines at 18px with 12px between them, each line a link (email, telephone, street, social); above it in the top-right corner, a stamp: one small photograph, 3:4 and 88px wide, with a 6px paper-coloured margin. Along the panel's bottom edge, a single centred line at 12px gives the copyright like a printer's imprint.
On a phone: The panel runs full width with six scallops across its top edge. The stamp sits top-right at 64px wide; the sign-off and message come first, then the address lines at 17px beneath them, then the imprint line centred at 12px.

Adjusted for this page:
- It sets text at 12px: use your small step (13px or more) instead.

## 8. Motion: Slow crossfade
The principal photograph quietly changes: three or four images of the same framing crossfade over about 1.6 seconds, holding five to six seconds each, or the fixed image changes when its matching section arrives. It should feel like light shifting in a room. Pause when the tab is hidden; under reduced motion show only the first image.
This is the signature move, the one loud moment. Around it the page still needs the rest of the motion layer (SKILL.md step 9): an entrance for the parts of every section, feedback on every control, and one moving picture. The inspector fails a page that barely moves. Recipes: references/motion.md.

## 10. Where the richness comes from
The photographs, at full size, uninterrupted. Empty paper around short text makes the next image land harder.

## 11. How this direction goes wrong
A weak hero photograph cannot be fixed by typography; pick again. Do not stack a headline, a paragraph and two buttons on the image. Do not use a booking bar that covers the bottom of the view; one small action is enough.

## 12. Real references
Studied sites that work this way. Take the principle, never the specifics: no names, copy, images or signature assets of theirs.
- **Eagle’s Nest** (One Page Love, studied score 7.5) `opl-eagles-nest`
  Idea: Let the lake view do the selling: full-bleed footage of the volcano horizon with the name set as a monumental cream serif along the bottom edge.
  Hero: Full-bleed video of a silhouetted figure meditating before a lake and volcanoes, with no scrim. The name is set in a high-contrast cream serif, uppercase, about 15vw, spanning the full width between 34px margins and sitting on the bottom edge so it covers the lower fifth of the frame. Directly above its left and right ends sit two pairs of small white labels (what it is, where it is). Top row: a round emblem far left, eight plain text links grouped right of centre and an outlined pill button far right. A small black vertical awards tab hangs on the right edge.
  Worth taking: Anchor the name at full width on the bottom edge of a full-bleed video and tuck two tiny descriptor pairs above its left and right ends.
- **Seasats** (Awwwards Site of the Day, studied score 8.4) `aww-seasats`
  Idea: Calm, dusk-lit seascapes sell autonomous boats as serene instruments, and the navigation is a column of stacked colour swatches taken from that sea-and-sand palette.
  Hero: A 10px white frame surrounds everything. The left 84% is one rounded media panel: a dusk scene of a low, solar-decked vessel centred on mirror-flat water, with two larger hulls cropped by the panel's left and right edges. The headline is centred in the panel's upper third, two lines of white light-weight flared serif at 124px (8.6vw). A wordmark in custom wide techno lettering sits top-left; a white rounded button with mono caps and a dark-green square arrow sits bottom-centre. The right 14% is the menu: a full-height column of stacked flat colour blocks (blush, sage, then four darkening olives), each holding left-aligned 15px links, sub-items numbered 01 to 04.
  Worth taking: Build the menu as a full-height column of stacked flat colour blocks sampled from the imagery, grouping links by block colour instead of by rules or headings.
- **Kereliott** (One Page Love, studied score 7.3) `opl-kereliott`
  Idea: A quiet house gets a quiet page: one dark field, one typeface, the name set as wide as the screen and photographs left to drift in generous darkness.
  Hero: Very dark green-black field with cream type. A two-line introductory sentence at about 30px sits top-left inside 30px margins; a small cream rectangular button sits top-right. The upper half is otherwise empty. The house name fills the full content width in a flared humanist sans, mixed case, with capitals about 19vw tall, its baseline at roughly 87% of the viewport height. Immediately beneath, separated by a gap of a few pixels, the top sliver of a full-width landscape photograph enters from the bottom edge.
  Worth taking: Size the wordmark to fill the content width exactly and let the first photograph tuck directly under its baseline.
Full notes on any of them: `node draw.mjs --site <id>`.

## Always
Headlines two lines or fewer at every width. No eyebrow labels, no monospace, no 01/02/03, no thin rules, no gradients, no shadows at rest,
no cream-and-terracotta, no violet. The frame: one h1 on the first screen that says what this is, equal outer margins, no
section huddled on one side with the other half empty, no blank stretch over half a screen, a heading on every section.
`inspect.mjs` measures all of it.

Saved to /home/user/impeccable/my-skills/website-design/examples/casa-dei-venti/.taste-skill/direction.json · reprint with `node draw.mjs --show`
