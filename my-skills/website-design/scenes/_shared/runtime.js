// Small helpers shared by the scene templates. No dependencies.

const reducedQuery = matchMedia('(prefers-reduced-motion: reduce)');
export const isReduced = () => reducedQuery.matches;
export const onReducedChange = (fn) => reducedQuery.addEventListener('change', () => fn(reducedQuery.matches));

/** Marks the document so CSS can tell "script ran" and "motion allowed" apart from the no-script page. */
export function boot() {
  const root = document.documentElement;
  root.classList.add('js');
  const set = () => root.classList.toggle('motion-ok', !isReduced());
  set();
  onReducedChange(set);
}

export function webglAvailable() {
  try {
    const c = document.createElement('canvas');
    return Boolean(c.getContext('webgl2') || c.getContext('webgl'));
  } catch {
    return false;
  }
}

/** Shows the poster instead of the canvas when WebGL is missing or fails. */
export function fallbackToPoster(reason) {
  document.documentElement.classList.add('no-webgl');
  if (reason) console.info('[scene] showing the poster:', reason);
}

export const pixelRatio = (max = 2) => Math.min(window.devicePixelRatio || 1, max);

/**
 * A requestAnimationFrame loop that stops when the tab is hidden or the target leaves the viewport,
 * so a scene never burns battery off screen. fn(timeSeconds, deltaSeconds).
 */
export function loop(fn, { target } = {}) {
  let raf = 0;
  let running = false;
  let inView = true;
  let last = performance.now();
  const tick = (now) => {
    raf = requestAnimationFrame(tick);
    const dt = Math.min(0.05, (now - last) / 1000);
    last = now;
    fn(now / 1000, dt);
  };
  const start = () => {
    if (running || !inView || document.hidden) return;
    running = true;
    last = performance.now();
    raf = requestAnimationFrame(tick);
  };
  const stop = () => {
    if (!running) return;
    cancelAnimationFrame(raf);
    running = false;
  };
  document.addEventListener('visibilitychange', () => (document.hidden ? stop() : start()));
  if (target) {
    new IntersectionObserver(([entry]) => {
      inView = entry.isIntersecting;
      inView ? start() : stop();
    }).observe(target);
  }
  start();
  return { start, stop };
}

/** Pointer position in pixels and in -1..1 space, smoothed toward the latest value with ease(). */
export function pointer() {
  const p = { x: innerWidth / 2, y: innerHeight / 2, nx: 0, ny: 0, sx: 0, sy: 0, active: false };
  addEventListener('pointermove', (e) => {
    p.x = e.clientX;
    p.y = e.clientY;
    p.nx = (e.clientX / innerWidth) * 2 - 1;
    p.ny = -((e.clientY / innerHeight) * 2 - 1);
    p.active = true;
  }, { passive: true });
  p.ease = (k = 0.08) => {
    p.sx += (p.nx - p.sx) * k;
    p.sy += (p.ny - p.sy) * k;
  };
  return p;
}

/** Adds .is-in to .reveal elements once they enter the viewport. Content stays visible without script. */
export function reveals(selector = '.reveal') {
  const els = document.querySelectorAll(selector);
  if (isReduced() || !('IntersectionObserver' in window)) {
    els.forEach((el) => el.classList.add('is-in'));
    return;
  }
  const io = new IntersectionObserver((entries) => {
    for (const e of entries) {
      if (e.isIntersecting) {
        e.target.classList.add('is-in');
        io.unobserve(e.target);
      }
    }
  }, { rootMargin: '0px 0px -12% 0px' });
  els.forEach((el) => io.observe(el));
}

/** Progress 0..1 of the page scroll through a tall section (the sticky-stage pattern). */
export function sectionProgress(section) {
  const r = section.getBoundingClientRect();
  const span = r.height - innerHeight;
  if (span <= 0) return 0;
  return Math.min(1, Math.max(0, -r.top / span));
}

export const clamp = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v));
export const lerp = (a, b, t) => a + (b - a) * t;
export const smoothstep = (a, b, v) => {
  const t = clamp((v - a) / (b - a));
  return t * t * (3 - 2 * t);
};
