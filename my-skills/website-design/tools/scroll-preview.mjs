#!/usr/bin/env node
// scroll-preview: one image that shows a page from top to bottom the way a visitor scrolls it, for
// sending to a client. Sticky and scroll-driven scenes come out right because every frame is a real
// viewport at a real scroll position (a full-page screenshot flattens them).
//
//   node scroll-preview.mjs <url> <out.jpg> [--phone] [--frames 6] [--query "?fog=false"]
//
// Frames are taken at 2x and joined into one column (desktop) or one row (phone).
// Needs Playwright: npm i -D playwright && npx playwright install chromium
import { createRequire } from 'node:module';
import fs from 'node:fs';
const require = createRequire(import.meta.url);
const { chromium } = require('playwright');

const args = process.argv.slice(2);
const has = (n) => { const i = args.indexOf(n); if (i < 0) return false; args.splice(i, 1); return true; };
const val = (n, d) => { const i = args.indexOf(n); if (i < 0) return d; const v = args[i + 1]; args.splice(i, 2); return v; };
const phone = has('--phone');
const count = Number(val('--frames', 6));
const query = val('--query', '');
const [url, out = 'scroll-preview.jpg'] = args;
if (!url) { console.error('Usage: node scroll-preview.mjs <url> <out.jpg> [--phone] [--frames 6]'); process.exit(2); }

const vp = phone ? { width: 390, height: 844 } : { width: 1440, height: 900 };
const browser = await chromium.launch();
const ctx = await browser.newContext({ viewport: vp, deviceScaleFactor: 2, isMobile: phone, hasTouch: phone });
const page = await ctx.newPage();
await page.goto(url + query, { waitUntil: 'networkidle', timeout: 60000 });
await page.evaluate(() => document.fonts.ready);
await page.waitForTimeout(1200);
const span = await page.evaluate(() => document.documentElement.scrollHeight - innerHeight);
const frames = [];
for (let i = 0; i < count; i++) {
  const y = Math.round((span * i) / Math.max(1, count - 1));
  await page.evaluate((v) => scrollTo(0, v), y);
  await page.waitForTimeout(1300);
  frames.push((await page.screenshot({ type: 'jpeg', quality: 82 })).toString('base64'));
}
// Join the frames by laying them out in a page and photographing that page: no image library needed.
const sheet = await (await browser.newContext({ viewport: phone ? { width: (390 + 12) * count, height: 844 } : { width: 1440, height: 100 }, deviceScaleFactor: 1 })).newPage();
await sheet.setContent(`<body style="margin:0;background:#e8e4dc;display:flex;${phone ? 'flex-direction:row' : 'flex-direction:column'};gap:12px">${frames.map((b) => `<img src="data:image/jpeg;base64,${b}" style="width:${phone ? 390 : 1440}px;display:block">`).join('')}</body>`);
await sheet.waitForTimeout(300);
fs.writeFileSync(out, await sheet.screenshot({ fullPage: true, type: 'jpeg', quality: 84 }));
await browser.close();
console.log(`Wrote ${out} (${count} frames, ${phone ? 'phone' : 'desktop'})`);
