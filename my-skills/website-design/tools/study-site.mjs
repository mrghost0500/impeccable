#!/usr/bin/env node
// study-site: gather evidence about how a site the user admires is built, so we can explain what makes
// it work and build our own version. Evidence only: it does not download the site's code or assets for
// reuse. Read the site's terms; never copy paid or licensed work.
//
//   node study-site.mjs <url> [out-dir]
//
// Writes report.md (libraries, canvases and WebGL, videos, fonts, colours, type scale, sticky and
// pinned elements, weight by type, page length) and eight scroll frames.
// Needs Playwright: npm i -D playwright && npx playwright install chromium
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
// Playwright from the project being checked first, then from next to this tool.
let chromium;
for (const from of [path.join(process.cwd(), 'x.js'), import.meta.url]) {
  try { ({ chromium } = createRequire(from)('playwright')); break; } catch {}
}
if (!chromium) {
  console.error('Playwright is not installed. In the project: npm i -D playwright && npx playwright install chromium');
  process.exit(2);
}
const [url, outDir = 'site-study'] = process.argv.slice(2);
if (!url) { console.error('Usage: node study-site.mjs <url> [out-dir]'); process.exit(2); }
fs.mkdirSync(outDir, { recursive: true });

const browser = await chromium.launch({ args: ['--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1 });
// Record every canvas context a page asks for, before any of its scripts run.
await ctx.addInitScript(() => {
  window.__study = { contexts: [] };
  const orig = HTMLCanvasElement.prototype.getContext;
  HTMLCanvasElement.prototype.getContext = function (type, attrs) {
    window.__study.contexts.push({ type, attrs: attrs ? JSON.stringify(attrs) : '', w: this.width, h: this.height });
    return orig.call(this, type, attrs);
  };
});
const page = await ctx.newPage();
const byType = {};
const hosts = new Set();
page.on('response', (r) => {
  const t = r.request().resourceType();
  const len = Number(r.headers()['content-length'] || 0);
  byType[t] = byType[t] || { n: 0, kb: 0 }; byType[t].n++; byType[t].kb += len / 1024;
  try { hosts.add(new URL(r.url()).host); } catch {}
});
await page.goto(url, { waitUntil: 'load', timeout: 90000 });
await page.waitForTimeout(4000);
const span = await page.evaluate(() => document.documentElement.scrollHeight - innerHeight);
for (let i = 0; i < 8; i++) {
  await page.evaluate((y) => scrollTo(0, y), Math.round((span * i) / 7));
  await page.waitForTimeout(1500);
  await page.screenshot({ path: path.join(outDir, `frame-${i}.jpg`), type: 'jpeg', quality: 80 });
}
const facts = await page.evaluate(() => {
  const g = window;
  const libs = [];
  if (g.THREE?.REVISION) libs.push(`three.js r${g.THREE.REVISION}`);
  if (g.gsap?.version) libs.push(`GSAP ${g.gsap.version}`);
  if (g.ScrollTrigger) libs.push('ScrollTrigger');
  if (g.Lenis || document.documentElement.classList.contains('lenis')) libs.push('Lenis');
  if (g.__NEXT_DATA__ || document.getElementById('__next')) libs.push('Next.js');
  if (g.__NUXT__) libs.push('Nuxt');
  if (document.querySelector('[data-framer-name], [data-framer-component-type]')) libs.push('Framer');
  if (document.documentElement.dataset.wfPage) libs.push('Webflow');
  if (g.Swiper) libs.push('Swiper');
  if (g.PIXI) libs.push('PixiJS');
  if (g.BABYLON) libs.push('Babylon.js');
  if (document.querySelector('spline-viewer, canvas[data-engine*="spline"]')) libs.push('Spline');
  const scripts = [...document.scripts].map((s) => s.src).filter(Boolean);
  for (const s of scripts) for (const [re, name] of [[/three/i, 'three (script)'], [/gsap/i, 'GSAP (script)'], [/lenis/i, 'Lenis (script)'], [/lottie/i, 'Lottie'], [/rive/i, 'Rive'], [/barba/i, 'Barba'], [/swup/i, 'Swup']]) if (re.test(s) && !libs.includes(name)) libs.push(name);
  const count = (sel) => document.querySelectorAll(sel).length;
  const all = [...document.querySelectorAll('body *')];
  const sticky = all.filter((e) => ['sticky', 'fixed'].includes(getComputedStyle(e).position)).length;
  const tally = (prop) => { const m = new Map(); all.slice(0, 4000).forEach((e) => { const v = getComputedStyle(e)[prop]; if (v && v !== 'rgba(0, 0, 0, 0)') m.set(v, (m.get(v) || 0) + 1); }); return [...m].sort((a, b) => b[1] - a[1]).slice(0, 8).map(([v, n]) => `${v} (${n})`); };
  const type = [...document.querySelectorAll('h1, h2, h3, p, a, button')].slice(0, 400).map((e) => { const s = getComputedStyle(e); return `${e.tagName.toLowerCase()} ${s.fontSize} ${s.fontWeight} ${s.fontFamily.split(',')[0]}`; });
  const typeCounts = [...type.reduce((m, t) => m.set(t, (m.get(t) || 0) + 1), new Map())].sort((a, b) => parseFloat(b[0].split(' ')[1]) - parseFloat(a[0].split(' ')[1])).slice(0, 12).map(([t, n]) => `${t} ×${n}`);
  return {
    title: document.title,
    screens: (document.documentElement.scrollHeight / innerHeight).toFixed(1),
    libs, contexts: g.__study?.contexts || [],
    canvases: count('canvas'), videos: [...document.querySelectorAll('video')].map((v) => `${v.currentSrc || v.querySelector('source')?.src || '(no src)'} ${v.videoWidth}x${v.videoHeight}`),
    images: count('img'), svgs: count('svg'), sticky,
    fonts: [...document.fonts].filter((f) => f.status === 'loaded').map((f) => `${f.family} ${f.weight} ${f.style}`).filter((v, i, a) => a.indexOf(v) === i),
    colours: tally('color'), backgrounds: tally('backgroundColor'), typeScale: typeCounts,
    headings: [...document.querySelectorAll('h1, h2')].slice(0, 12).map((h) => h.textContent.trim().replace(/\s+/g, ' ').slice(0, 90)),
    reducedMotionRules: [...document.styleSheets].some((s) => { try { return [...s.cssRules].some((r) => r.media && /reduced-motion/.test(r.media.mediaText)); } catch { return false; } }),
  };
});
await browser.close();
const md = `# Site study: ${facts.title}

URL: ${url}
Page length: ${facts.screens} screens. Sticky or fixed elements: ${facts.sticky}. Honours reduced motion in CSS: ${facts.reducedMotionRules ? 'yes' : 'no rules found'}.

## Built with
${facts.libs.length ? facts.libs.map((l) => `- ${l}`).join('\n') : '- Nothing recognisable (plain code, or bundled beyond recognition)'}

## Drawing surfaces
- Canvases on the page: ${facts.canvases}
${[...facts.contexts.reduce((m, c) => { const k = `${c.type} ${c.w}x${c.h} ${c.attrs}`; return m.set(k, (m.get(k) || 0) + 1); }, new Map())].map(([k, n]) => `- ${k}${n > 1 ? ` (×${n})` : ''}`).join('\n') || '- No canvas contexts requested'}
- Videos: ${facts.videos.length} on the page${facts.videos.some((v) => v.startsWith('blob:')) ? ' (some streamed through blob URLs, so adaptive streaming)' : ''}; with a direct file: ${facts.videos.filter((v) => /^https?:/.test(v)).slice(0, 6).join('; ') || 'none'}
- Images: ${facts.images}, inline SVGs: ${facts.svgs}

## Type
Fonts loaded: ${facts.fonts.join(', ') || 'system fonts only'}

Largest styles in use (tag, size, weight, family, count):
${facts.typeScale.map((t) => `- ${t}`).join('\n')}

## Colour
Text: ${facts.colours.join(', ')}

Backgrounds: ${facts.backgrounds.join(', ')}

## Headings
${facts.headings.map((h) => `- ${h}`).join('\n')}

## Weight
${Object.entries(byType).map(([t, v]) => `- ${t}: ${v.n} requests, about ${Math.round(v.kb)} KB (from content-length; streamed files may show 0)`).join('\n')}

Hosts contacted: ${[...hosts].join(', ')}

## Frames
frame-0.jpg to frame-7.jpg, evenly spaced from top to bottom.

## Next
Write down, in plain words, the three to five things that make this site work (one world, how the story is told, where the type sits, the small interface, what responds to the visitor, how it degrades). Build those ideas with our own content. Do not copy its code, images, names or wording.
`;
fs.writeFileSync(path.join(outDir, 'report.md'), md);
console.log(md);
