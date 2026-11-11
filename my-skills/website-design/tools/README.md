# website-design tools

Four small tools the skill runs. The three `.mjs` tools need Playwright once per machine:
`npm i -D playwright && npx playwright install chromium`. `frames.sh` needs ffmpeg.

| Tool | Run | What you get |
|---|---|---|
| `check-page.mjs` | `node check-page.mjs <folder or url> [out-dir]` | Screenshots on a computer (top, 40%, 75%), a phone, reduced motion and JavaScript off, plus a must-fix list: script errors, failed requests, sideways scroll on phones, text invisible without JavaScript, h1 count, meta description. Exit code 1 while anything must be fixed. |
| `scroll-preview.mjs` | `node scroll-preview.mjs <url> preview.jpg [--phone] [--frames 6]` | One image of the whole scroll at 2x, made of real viewports, so sticky and scroll-driven scenes show as visitors see them. For sending to the client. |
| `study-site.mjs` | `node study-site.mjs <url> [out-dir]` | `report.md` on a site the user admires: libraries, canvases and WebGL settings, videos, fonts, colours, type scale, sticky elements, weight, plus eight scroll frames. Evidence for understanding, never for copying. |
| `frames.sh` | `./frames.sh film.mp4 public/film [fps] [width]` | Landscape and 4:5 portrait WebP frame sets and a poster from any film, with the `SequencePlayer` settings to paste. |

Flags: `check-page.mjs --query "?fog=false"` adds dials to the address; `--libs <node_modules>` serves
jsDelivr libraries from a local folder when the machine is offline.
