// Procedural stand-in pictures for the demos, so every template runs with no binary assets.
// In a real build, replace them with the client's footage, renders, or generated frames.

export function rng(seed = 1) {
  let s = seed >>> 0;
  return () => {
    s = (s + 0x6d2b79f5) >>> 0;
    let t = s;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

/** Smooth 1D value noise. */
export function noise1(seed = 7) {
  const r = rng(seed);
  const pts = Array.from({ length: 512 }, () => r());
  return (x) => {
    const i = Math.floor(x);
    const f = x - i;
    const a = pts[((i % 512) + 512) % 512];
    const b = pts[(((i + 1) % 512) + 512) % 512];
    const u = f * f * (3 - 2 * f);
    return a + (b - a) * u;
  };
}

const mix = (a, b, t) => a + (b - a) * t;
const rgb = (c) => `rgb(${c[0] | 0},${c[1] | 0},${c[2] | 0})`;
const mixc = (a, b, t) => [mix(a[0], b[0], t), mix(a[1], b[1], t), mix(a[2], b[2], t)];

/**
 * A dawn-to-day mountain journey: layered ridges with haze, a sun that rises, and a camera that moves
 * forward through the ranges as t goes from 0 to 1.
 */
export function ridges(ctx, w, h, t, palette = {}) {
  const skyTop = palette.skyTop || mixc([24, 22, 40], [64, 104, 150], t);
  const skyLow = palette.skyLow || mixc([232, 146, 102], [236, 206, 170], t);
  const haze = palette.haze || mixc([196, 120, 104], [176, 190, 200], t);
  const ink = palette.ink || [16, 18, 26];
  const g = ctx.createLinearGradient(0, 0, 0, h);
  g.addColorStop(0, rgb(skyTop));
  g.addColorStop(0.62, rgb(skyLow));
  g.addColorStop(1, rgb(haze));
  ctx.fillStyle = g;
  ctx.fillRect(0, 0, w, h);
  // sun
  const sy = h * mix(0.62, 0.22, t);
  const sun = ctx.createRadialGradient(w * 0.62, sy, 0, w * 0.62, sy, h * 0.42);
  sun.addColorStop(0, 'rgba(255,236,200,0.95)');
  sun.addColorStop(0.08, 'rgba(255,214,160,0.75)');
  sun.addColorStop(1, 'rgba(255,200,150,0)');
  ctx.fillStyle = sun;
  ctx.fillRect(0, 0, w, h);
  // ridges, far to near; the camera moves forward with t, so near ridges grow and slide down
  const layers = 6;
  const span = Math.max(w, h * 1.6); // phones see a crop of the range instead of squeezed peaks
  for (let l = 0; l < layers; l++) {
    const depth = l / (layers - 1);
    const n = noise1(11 + l * 7);
    const zoom = 1 + t * (0.3 + depth * 1.6);
    const base = h * (0.5 + depth * 0.32) + t * depth * h * 0.18;
    const amp = h * (0.08 + depth * 0.12) * zoom;
    const freq = (2.2 + l * 0.9) / span;
    const shift = t * (40 + l * 30);
    ctx.beginPath();
    ctx.moveTo(0, h);
    for (let x = 0; x <= w; x += Math.max(2, w / 360)) {
      const xx = (x - w / 2) / zoom + w / 2;
      const y = base - amp * (n(xx * freq + shift) * 0.75 + n(xx * freq * 3.1 + shift * 2) * 0.25);
      ctx.lineTo(x, y);
    }
    ctx.lineTo(w, h);
    ctx.closePath();
    ctx.fillStyle = rgb(mixc(haze, ink, Math.pow(depth, 0.8) * 0.92));
    ctx.fill();
    // mist band in front of each layer
    const mist = ctx.createLinearGradient(0, base - amp, 0, base + h * 0.06);
    mist.addColorStop(0, 'rgba(255,255,255,0)');
    mist.addColorStop(1, `rgba(${haze[0]},${haze[1]},${haze[2]},${0.18 * (1 - depth)})`);
    ctx.fillStyle = mist;
    ctx.fillRect(0, base - amp, w, h * 0.2);
  }
}

/**
 * A one-point-perspective interior with a window, a warm light pool and a camera moving forward.
 * room = 0..n picks the palette and window; t = 0..1 is the dolly within the room.
 */
export function room(ctx, w, h, roomIndex, t) {
  const palettes = [
    { wall: [214, 202, 186], floor: [150, 112, 82], sky: [[236, 160, 110], [72, 92, 140]], light: [255, 214, 160] },
    { wall: [196, 190, 182], floor: [118, 96, 78], sky: [[250, 200, 150], [110, 150, 190]], light: [255, 226, 186] },
    { wall: [226, 220, 210], floor: [176, 150, 120], sky: [[200, 220, 236], [120, 170, 210]], light: [255, 240, 214] },
    { wall: [180, 170, 160], floor: [96, 76, 62], sky: [[240, 140, 100], [40, 50, 90]], light: [255, 190, 140] },
    { wall: [208, 214, 216], floor: [140, 140, 136], sky: [[255, 210, 160], [90, 140, 200]], light: [255, 232, 200] },
  ];
  const p = palettes[roomIndex % palettes.length];
  const z = 1 + t * 0.55;
  const cx = w / 2;
  const cy = h * 0.46;
  const bw = (w * 0.42) * z;
  const bh = (h * 0.46) * z;
  const L = cx - bw / 2;
  const R = cx + bw / 2;
  const T = cy - bh / 2;
  const B = cy + bh / 2;
  // walls
  ctx.fillStyle = rgb(mixc(p.wall, [0, 0, 0], 0.18));
  ctx.fillRect(0, 0, w, h);
  ctx.fillStyle = rgb(p.wall);
  ctx.fillRect(L, T, bw, bh);
  // floor
  ctx.beginPath(); ctx.moveTo(0, h); ctx.lineTo(L, B); ctx.lineTo(R, B); ctx.lineTo(w, h); ctx.closePath();
  ctx.fillStyle = rgb(p.floor); ctx.fill();
  // ceiling
  ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(L, T); ctx.lineTo(R, T); ctx.lineTo(w, 0); ctx.closePath();
  ctx.fillStyle = rgb(mixc(p.wall, [255, 255, 255], 0.25)); ctx.fill();
  // side walls
  ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(L, T); ctx.lineTo(L, B); ctx.lineTo(0, h); ctx.closePath();
  ctx.fillStyle = rgb(mixc(p.wall, [0, 0, 0], 0.1)); ctx.fill();
  ctx.beginPath(); ctx.moveTo(w, 0); ctx.lineTo(R, T); ctx.lineTo(R, B); ctx.lineTo(w, h); ctx.closePath();
  ctx.fillStyle = rgb(mixc(p.wall, [0, 0, 0], 0.22)); ctx.fill();
  // floor planks
  ctx.strokeStyle = 'rgba(0,0,0,0.12)';
  ctx.lineWidth = Math.max(1, w / 900);
  for (let i = -8; i <= 8; i++) {
    ctx.beginPath(); ctx.moveTo(cx + i * bw / 8, B); ctx.lineTo(cx + i * w / 4, h); ctx.stroke();
  }
  // window with sky
  const ww = bw * 0.62;
  const wh = bh * 0.58;
  const wx = cx - ww / 2;
  const wy = T + bh * 0.14;
  const sky = ctx.createLinearGradient(0, wy, 0, wy + wh);
  sky.addColorStop(0, rgb(p.sky[1]));
  sky.addColorStop(1, rgb(p.sky[0]));
  ctx.fillStyle = sky;
  ctx.fillRect(wx, wy, ww, wh);
  ctx.fillStyle = 'rgba(30,40,60,0.55)';
  ctx.fillRect(wx, wy + wh * 0.78, ww, wh * 0.22);
  ctx.strokeStyle = rgb(mixc(p.wall, [0, 0, 0], 0.5));
  ctx.lineWidth = Math.max(2, bw / 160);
  ctx.strokeRect(wx, wy, ww, wh);
  ctx.beginPath(); ctx.moveTo(cx, wy); ctx.lineTo(cx, wy + wh); ctx.stroke();
  // light pool on the floor
  const pool = ctx.createRadialGradient(cx, B + (h - B) * 0.35, 0, cx, B + (h - B) * 0.35, w * 0.45);
  pool.addColorStop(0, `rgba(${p.light[0]},${p.light[1]},${p.light[2]},0.45)`);
  pool.addColorStop(1, 'rgba(0,0,0,0)');
  ctx.fillStyle = pool;
  ctx.fillRect(0, 0, w, h);
  // vignette
  const v = ctx.createRadialGradient(cx, cy, Math.min(w, h) * 0.3, cx, cy, Math.max(w, h) * 0.75);
  v.addColorStop(0, 'rgba(0,0,0,0)');
  v.addColorStop(1, 'rgba(0,0,0,0.45)');
  ctx.fillStyle = v;
  ctx.fillRect(0, 0, w, h);
}

/** An abstract artwork for gallery demos, seeded so each card differs. Returns a canvas. */
export function artwork(seed, size = 512, ratio = 1.25) {
  const c = document.createElement('canvas');
  c.width = size;
  c.height = Math.round(size * ratio);
  const ctx = c.getContext('2d');
  const r = rng(seed * 97 + 3);
  const palettes = [
    ['#e9e3d6', '#1f2a44', '#c8553d', '#f2a65a'],
    ['#101418', '#e6e1d3', '#4f7cac', '#c0d6df'],
    ['#f3efe6', '#2d3a2e', '#8a9a5b', '#d9a441'],
    ['#1b1b1f', '#e94f37', '#f6f7eb', '#393e41'],
    ['#ece4db', '#5b4e77', '#b388eb', '#2b2d42'],
    ['#0f1b2d', '#f0ebd8', '#d4a373', '#457b9d'],
  ];
  const pal = palettes[seed % palettes.length];
  ctx.fillStyle = pal[0];
  ctx.fillRect(0, 0, c.width, c.height);
  const kind = seed % 3;
  if (kind === 0) {
    for (let i = 0; i < 4; i++) {
      ctx.fillStyle = pal[1 + (i % 3)];
      ctx.beginPath();
      ctx.arc(c.width * r(), c.height * r(), size * (0.12 + r() * 0.34), 0, Math.PI * 2);
      ctx.fill();
    }
  } else if (kind === 1) {
    const bands = 5 + Math.floor(r() * 6);
    for (let i = 0; i < bands; i++) {
      ctx.fillStyle = pal[1 + (i % 3)];
      ctx.fillRect(0, (i / bands) * c.height, c.width, c.height / bands * (0.3 + r() * 0.6));
    }
  } else {
    ctx.fillStyle = pal[1];
    ctx.fillRect(c.width * 0.12, c.height * 0.1, c.width * 0.76, c.height * 0.8);
    ctx.fillStyle = pal[2];
    ctx.beginPath();
    ctx.moveTo(c.width * 0.12, c.height * 0.9);
    ctx.lineTo(c.width * 0.5, c.height * (0.25 + r() * 0.2));
    ctx.lineTo(c.width * 0.88, c.height * 0.9);
    ctx.fill();
    ctx.fillStyle = pal[3];
    ctx.beginPath();
    ctx.arc(c.width * 0.68, c.height * 0.3, size * 0.09, 0, Math.PI * 2);
    ctx.fill();
  }
  // paper grain
  const img = ctx.getImageData(0, 0, c.width, c.height);
  for (let i = 0; i < img.data.length; i += 4) {
    const n = (r() - 0.5) * 18;
    img.data[i] += n; img.data[i + 1] += n; img.data[i + 2] += n;
  }
  ctx.putImageData(img, 0, 0);
  return c;
}
