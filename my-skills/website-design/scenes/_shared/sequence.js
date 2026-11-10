// Image-sequence player: the technique behind cinematic scroll films (a rendered or filmed journey
// exported as frames and drawn to a canvas by scroll position). Frame-exact, works on phones.
//
// Production: pass frameCount and src(i) for numbered WebP or JPEG frames, and optionally
// portraitSrc(i) for a 9:16 or 4:5 set. Demos: pass painter(ctx, w, h, t) and no frames.

import { pixelRatio } from './runtime.js';

export class SequencePlayer {
  constructor({ canvas, frameCount = 0, src = null, portraitSrc = null, painter = null, fit = 'cover' }) {
    this.canvas = canvas;
    this.ctx = canvas.getContext('2d', { alpha: false });
    this.frameCount = frameCount;
    this.painter = painter;
    this.fit = fit;
    this.progress = 0;
    this.portraitQuery = matchMedia('(orientation: portrait) and (max-width: 900px)');
    this.sources = { landscape: src, portrait: portraitSrc || src };
    this.cache = new Map();
    this.resize = this.resize.bind(this);
    addEventListener('resize', this.resize, { passive: true });
    this.portraitQuery.addEventListener('change', () => this.reload());
    this.resize();
    if (this.frameCount && src) this.reload();
  }

  get set() {
    return this.portraitQuery.matches ? 'portrait' : 'landscape';
  }

  /** Loads frames coarse to fine (every 16th, then 8th, 4th, 2nd, all), so scrubbing works early. */
  reload() {
    this.cache.clear();
    const make = this.sources[this.set];
    if (!make) return;
    const order = [];
    const seen = new Set();
    for (const step of [16, 8, 4, 2, 1]) {
      for (let i = 0; i < this.frameCount; i += step) {
        if (!seen.has(i)) { seen.add(i); order.push(i); }
      }
    }
    let cursor = 0;
    const lane = () => {
      if (cursor >= order.length) return;
      const i = order[cursor++];
      const img = new Image();
      img.decoding = 'async';
      img.src = make(i);
      img.decode().then(() => {
        this.cache.set(i, img);
        if (Math.abs(i - this.targetIndex()) < 3) this.draw();
      }).catch(() => {}).finally(lane);
    };
    for (let k = 0; k < 6; k++) lane();
  }

  targetIndex() {
    return Math.round(this.progress * (this.frameCount - 1));
  }

  nearestLoaded(i) {
    for (let d = 0; d < this.frameCount; d++) {
      if (this.cache.has(i - d)) return this.cache.get(i - d);
      if (this.cache.has(i + d)) return this.cache.get(i + d);
    }
    return null;
  }

  resize() {
    const r = this.canvas.getBoundingClientRect();
    const k = pixelRatio(2);
    this.canvas.width = Math.max(1, Math.round(r.width * k));
    this.canvas.height = Math.max(1, Math.round(r.height * k));
    this.draw();
  }

  setProgress(p) {
    if (p === this.progress) return;
    this.progress = p;
    this.draw();
  }

  draw() {
    const { ctx, canvas } = this;
    const w = canvas.width;
    const h = canvas.height;
    if (this.painter && !this.frameCount) {
      this.painter(ctx, w, h, this.progress);
      return;
    }
    const img = this.nearestLoaded(this.targetIndex());
    if (!img) return;
    const s = this.fit === 'cover'
      ? Math.max(w / img.naturalWidth, h / img.naturalHeight)
      : Math.min(w / img.naturalWidth, h / img.naturalHeight);
    const dw = img.naturalWidth * s;
    const dh = img.naturalHeight * s;
    ctx.drawImage(img, (w - dw) / 2, (h - dh) / 2, dw, dh);
  }
}

/**
 * Ties a player to a tall section with a sticky stage. Chapters are [{ at: 0..1, id }]; the callback
 * receives the active chapter. Under reduced motion the film does not scrub: it jumps to each chapter's
 * own frame as that chapter's text arrives, so every state is a finished still.
 */
export function scrollFilm({ player, section, chapters = [], onChapter = () => {}, reduced = false }) {
  let active = -1;
  const update = () => {
    const r = section.getBoundingClientRect();
    const span = r.height - innerHeight;
    const p = span > 0 ? Math.min(1, Math.max(0, -r.top / span)) : 0;
    let idx = 0;
    chapters.forEach((c, i) => { if (p >= c.at) idx = i; });
    if (idx !== active) {
      active = idx;
      onChapter(chapters[idx], idx);
    }
    if (reduced) {
      const c = chapters[idx];
      player.setProgress(c ? (c.still ?? c.at) : p);
    } else {
      player.setProgress(p);
    }
  };
  addEventListener('scroll', update, { passive: true });
  addEventListener('resize', update, { passive: true });
  update();
  return update;
}
