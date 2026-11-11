#!/usr/bin/env node
// check-page: look at a page the way visitors will meet it, and report what is wrong.
//
//   node check-page.mjs <url | folder> [out-dir] [--query "?fog=false"] [--libs <node_modules>] [--launch]
//
// A folder is served on a local port (its index.html, or <folder>/<sub>/ for a sub page).
// Captures, at 1x: desktop top, desktop at 40% and 75% scroll, phone, reduced motion, JavaScript off
// (full page). Reports console and page errors, failed requests, sideways overflow on phones, page
// length in screens, words readable without JavaScript, headings hidden without JavaScript, and the
// weight of what loaded, layout shift and main-thread blocking (Google's limits: 0.1 and 200 ms),
// sideways scroll at 320 px, the nav landmark, and share tags. --launch also fails on share tags that
// are missing or still point at example.com. Exit code 1 when something must be fixed.
//
// Needs Playwright: npm i -D playwright && npx playwright install chromium
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';

// Playwright from the project being checked first, then from next to this tool.
let chromium;
for (const from of [path.join(process.cwd(), 'x.js'), import.meta.url]) {
  try { ({ chromium } = createRequire(from)('playwright')); break; } catch {}
}
if (!chromium) {
  console.error('Playwright is not installed. In the project: npm i -D playwright && npx playwright install chromium');
  process.exit(2);
}

const args = process.argv.slice(2);
const flag = (n) => { const i = args.indexOf(n); if (i < 0) return null; const v = args[i + 1]; args.splice(i, 2); return v; };
const query = flag('--query') || '';
const libs = flag('--libs');
const launch = args.includes('--launch'); if (launch) args.splice(args.indexOf('--launch'), 1);
const [target, outDir = 'page-check'] = args;
if (!target) { console.error('Usage: node check-page.mjs <url | folder> [out-dir] [--query "?x=1"] [--libs <node_modules>]'); process.exit(2); }
fs.mkdirSync(outDir, { recursive: true });

let server = null;
let url = target;
if (!/^https?:/.test(target)) {
  const root = path.resolve(target);
  const types = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript', '.mjs': 'text/javascript', '.css': 'text/css', '.json': 'application/json',
    '.svg': 'image/svg+xml', '.png': 'image/png', '.jpg': 'image/jpeg', '.webp': 'image/webp', '.avif': 'image/avif', '.woff2': 'font/woff2', '.mp4': 'video/mp4' };
  // Serve the parent so pages can reach sibling folders such as ../_shared.
  const base = path.dirname(root);
  server = http.createServer((req, res) => {
    const p = path.join(base, decodeURIComponent(new URL(req.url, 'http://x').pathname));
    if (!p.startsWith(base)) { res.writeHead(403); return res.end(); }
    const f = fs.existsSync(p) && fs.statSync(p).isDirectory() ? path.join(p, 'index.html') : p;
    if (!fs.existsSync(f)) { res.writeHead(404); return res.end('not found'); }
    res.writeHead(200, { 'content-type': types[path.extname(f)] || 'application/octet-stream' });
    fs.createReadStream(f).pipe(res);
  });
  await new Promise((r) => server.listen(0, '127.0.0.1', r));
  url = `http://127.0.0.1:${server.address().port}/${path.basename(root)}/`;
}
url += query;

const browser = await chromium.launch({ args: ['--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
const report = { url, errors: [], failedRequests: [], shots: [] };

async function open(opts = {}) {
  const ctx = await browser.newContext({ viewport: opts.viewport || { width: 1440, height: 900 }, deviceScaleFactor: 1,
    reducedMotion: opts.reduced ? 'reduce' : 'no-preference', javaScriptEnabled: opts.js !== false, isMobile: !!opts.mobile, hasTouch: !!opts.mobile });
  if (libs) {
    await ctx.route(/https:\/\/cdn\.jsdelivr\.net\/npm\/([^@/]+)@[^/]+\/(.*)/, (route) => {
      const m = route.request().url().match(/npm\/([^@/]+)@[^/]+\/([^?]*)/);
      const f = path.join(libs, m[1], m[2]);
      return fs.existsSync(f) ? route.fulfill({ status: 200, contentType: 'text/javascript', body: fs.readFileSync(f) }) : route.continue();
    });
  }
  const page = await ctx.newPage();
  await page.addInitScript(() => {
    window.__vitals = { cls: 0, tbt: 0 };
    try {
      new PerformanceObserver((l) => { for (const e of l.getEntries()) if (!e.hadRecentInput) window.__vitals.cls += e.value; }).observe({ type: 'layout-shift', buffered: true });
      new PerformanceObserver((l) => { for (const e of l.getEntries()) window.__vitals.tbt += Math.max(0, e.duration - 50); }).observe({ type: 'longtask', buffered: true });
    } catch {}
  });
  const log = { errors: [], failed: [], bytes: 0, requests: 0 };
  page.on('pageerror', (e) => log.errors.push(`page error: ${e.message}`));
  page.on('console', (m) => { if (m.type() === 'error') log.errors.push(`console: ${m.text()}`); });
  page.on('requestfailed', (r) => log.failed.push(`${r.failure()?.errorText} ${r.url()}`));
  page.on('response', async (r) => { log.requests++; const len = Number(r.headers()['content-length'] || 0); log.bytes += len; if (r.status() >= 400) log.failed.push(`${r.status()} ${r.url()}`); });
  await page.goto(url, { waitUntil: 'load', timeout: 60000 });
  await page.waitForTimeout(opts.wait ?? 2500);
  return { ctx, page, log };
}
const shot = async (page, name, full = false) => { const f = path.join(outDir, `${name}.png`); await page.screenshot({ path: f, fullPage: full }); report.shots.push(f); };

{ // Desktop
  const { ctx, page, log } = await open();
  await shot(page, 'desktop');
  const span = await page.evaluate(() => document.documentElement.scrollHeight - innerHeight);
  report.screens = Number((await page.evaluate(() => document.documentElement.scrollHeight / innerHeight)).toFixed(1));
  for (const f of [0.4, 0.75]) if (span > 50) { await page.evaluate((y) => scrollTo(0, y), Math.round(span * f)); await page.waitForTimeout(1300); await shot(page, `desktop-${f * 100}`); }
  report.errors.push(...log.errors); report.failedRequests.push(...log.failed);
  report.requests = log.requests; report.kilobytes = Math.round(log.bytes / 1024);
  Object.assign(report, await page.evaluate(() => ({ layoutShift: +window.__vitals.cls.toFixed(3), blockingMs: Math.round(window.__vitals.tbt) })));
  Object.assign(report, await page.evaluate(() => {
    const m = (sel, attr = 'content') => document.querySelector(sel)?.getAttribute(attr) || '';
    return { nav: !!document.querySelector('nav, [role=navigation]'), shareImage: m('meta[property="og:image"]'), canonical: m('link[rel=canonical]', 'href'),
      structuredData: !!document.querySelector('script[type="application/ld+json"]'), lang: !!document.documentElement.lang };
  }));
  await ctx.close();
}
{ // Phone
  const { ctx, page, log } = await open({ viewport: { width: 390, height: 844 }, mobile: true });
  await shot(page, 'phone');
  report.phoneOverflow = await page.evaluate(() => document.documentElement.scrollWidth > innerWidth + 1);
  report.smallTapTargets = await page.evaluate(() => [...document.querySelectorAll('a, button, input, select, textarea')].filter((e) => {
    const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0 && (r.height < 32 || r.width < 32) && getComputedStyle(e).visibility !== 'hidden';
  }).length);
  report.errors.push(...log.errors.map((e) => `phone ${e}`));
  await ctx.close();
}
{ // The smallest phones still in use
  const { ctx, page } = await open({ viewport: { width: 320, height: 640 }, mobile: true, wait: 1200 });
  report.overflowAt320 = await page.evaluate(() => document.documentElement.scrollWidth > innerWidth + 1);
  await ctx.close();
}
{ // Reduced motion
  const { ctx, page, log } = await open({ reduced: true, wait: 1500 });
  await shot(page, 'reduced-motion');
  report.errors.push(...log.errors.map((e) => `reduced ${e}`));
  await ctx.close();
}
{ // JavaScript off: what search engines, link previews and slow phones see
  const { ctx, page } = await open({ js: false, wait: 400 });
  await shot(page, 'no-javascript', true);
  report.wordsWithoutJs = await page.evaluate(() => (document.body.innerText || '').split(/\s+/).filter((w) => /\p{L}{2,}/u.test(w)).length);
  report.hiddenWithoutJs = await page.evaluate(() => [...document.querySelectorAll('h1, h2, h3, p, li')].filter((e) => {
    const s = getComputedStyle(e); return e.textContent.trim() && (s.opacity === '0' || s.visibility === 'hidden');
  }).map((e) => e.textContent.trim().slice(0, 60)));
  report.title = await page.title();
  report.h1 = await page.evaluate(() => document.querySelectorAll('h1').length);
  report.metaDescription = await page.evaluate(() => Boolean(document.querySelector('meta[name="description"]')?.content));
  await ctx.close();
}
await browser.close();
server?.close();

const must = [];
if (report.errors.length) must.push(`${report.errors.length} script or console errors`);
if (report.failedRequests.length) must.push(`${report.failedRequests.length} failed requests`);
if (report.phoneOverflow) must.push('the page scrolls sideways on a phone');
if (report.hiddenWithoutJs.length) must.push(`${report.hiddenWithoutJs.length} headings or paragraphs are invisible without JavaScript`);
if (report.h1 !== 1) must.push(`${report.h1} h1 headings (want exactly 1)`);
if (!report.metaDescription) must.push('no meta description');
if (report.overflowAt320) must.push('the page scrolls sideways on a 320 px phone');
if (report.layoutShift > 0.1) must.push(`layout shift ${report.layoutShift} (Google's limit is 0.1)`);
if (report.blockingMs > 200) must.push(`main thread blocked ${report.blockingMs} ms at start (aim under 200)`);
if (!report.lang) must.push('no lang attribute on <html>');
const hasMenu = await Promise.resolve(report.nav);
if (!hasMenu) report.warnings = [...(report.warnings || []), 'no <nav> landmark (fine for a one-screen tool, not for a site)'];
if (launch) {
  if (!report.shareImage || /example\.com/.test(report.shareImage)) must.push('share image (og:image) missing or still example.com');
  if (!report.canonical || /example\.com/.test(report.canonical)) must.push('canonical address missing or still example.com');
  if (!report.structuredData) must.push('no structured data (JSON-LD)');
}
report.mustFix = must;
fs.writeFileSync(path.join(outDir, 'report.json'), JSON.stringify(report, null, 2));
console.log(JSON.stringify({ url: report.url, mustFix: must, warnings: report.warnings || [], layoutShift: report.layoutShift, blockingMs: report.blockingMs, screens: report.screens, requests: report.requests, kilobytes: report.kilobytes, smallTapTargets: report.smallTapTargets, wordsWithoutJs: report.wordsWithoutJs, out: outDir }, null, 2));
process.exit(must.length ? 1 : 0);
