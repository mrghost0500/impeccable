# Casa dei Venti: design record

The look as built, for later changes. Direction: The place carries it (taste skill, seed 2065965846).

## Colour
| Role | Value | Use |
|---|---|---|
| Ground | #ecebe7 bone | Page, cards, the printed sheet |
| Surface | #e1dfd9 | The rose and the questions sections |
| Ink | #38450f olive | All text, the primary button, the olive fields |
| Muted | #4f5a2c | Notes and secondary lines only |
| Field | #38450f with bone text | Rooms cards, the day section, the footer |

Colour lives in the photographs. One neutral scrim only, under the opening sentence and name.

## Type
Archivo (self-hosted, OFL), weights 400, 500 and 600. Five sizes only:
small 13 to 14 px, body 17 to 19 px, lead 22 to 32 px, head 32 to 64 px, display 68 px to 12.78vw.
Display tracking -0.035em, leading 0.86; body leading 1.45 to 1.55. Sentence case throughout.

## Layout
One 12-column grid, margins 16 to 32 px, section padding 52 px on phones and 72 to 116 px on computers.
Square corners on photographs and buttons; 8 px on the booking card and the postcard.

## Components
- Button: square, olive fill with bone text, or bone fill on photographs; 48 px tall (44 in the top bar).
- Light choices: filled pills (bone, olive when chosen), never outlined.
- Room card: olive panel 22vw wide in one column, moving one column right per room; full width and
  docked to the bottom on phones.
- The printed sheet and the postcard: bone panels with scalloped edges drawn as repeating SVG.

## Motion
- First picture: slow push-in over 24 s.
- Entrances: rise 24 px and fade, 640 ms, 70 ms stagger, starting just before the part enters the screen.
- Rooms: one sticky stage; each room's photograph pushes in and cross-fades; its card fades only after
  the photograph is mostly in, so two cards never overlap.
- Reduced motion: every room is a still frame in sequence, nothing travels, nothing hides.
