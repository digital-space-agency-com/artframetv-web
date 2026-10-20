/* Art Frame TV — landing page behaviour.
   The presets, mat colours and mouldings below are transcribed from the app so the
   page demonstrates the real product:
     app/src/main/java/team/dsa/artframetv/model/FrameSettings.kt
     app/src/main/java/team/dsa/artframetv/model/MatteColor.kt
     app/src/main/java/team/dsa/artframetv/model/FrameMoulding.kt
   Keep them in step when the app's defaults change. */

const W = (dp) => (dp / 960 * 100).toFixed(2) + '%';   // dp on a 960dp-wide TV panel → % of screen width

const MOULDINGS = {
  MODERN_BLACK:  { name: 'Pitch Black (OLED)',        a: '#000000', b: '#070707' },
  DARK_WALNUT:   { name: 'Dark Walnut',               a: '#14100e', b: '#221a16' },
  NATURAL_OAK:   { name: 'Natural White Oak',         a: '#c7a77e', b: '#dec39e' },
  GALLERY_WHITE: { name: 'Gallery White Wood',        a: '#e5e2da', b: '#f3f1ec' },
  ANTIQUE_BRASS: { name: 'Brushed Brass & Gold',      a: '#a58348', b: '#d4b168', metallic: true },
  NONE:          { name: 'Frameless (Edge-to-Edge)',  a: 'transparent', b: 'transparent' },
};

const MATTES = {
  WARM_COTTON:     { name: 'Warm Cotton White',      hex: '#f5f2ea' },
  MUSEUM_EGGSHELL: { name: 'Museum Eggshell',        hex: '#efece6' },
  ANTIQUE_CREAM:   { name: 'Antique Cream',          hex: '#efebd9' },
  GALLERY_BLACK:   { name: 'Charcoal Black',         hex: '#1c1b1a' },
  SAGE_GREEN:      { name: 'Museum Sage',            hex: '#4a5348' },
  FRENCH_BLUE:     { name: 'Heritage French Blue',   hex: '#3c4752' },
  NONE:            { name: 'No Matte',               hex: 'transparent' },
};

const BEVELS = {
  WHITE_CORE: { hi: '#ffffff', sh: '#d6d0c3' },
  CREAM_CORE: { hi: '#faf7ee', sh: '#cbc4b2' },
  BLACK_CORE: { hi: '#4a4a4a', sh: '#141414' },
};

/* The app's own one-press presets. */
const PRESETS = [
  { id: 'museum',    label: 'Museum Classic',   moulding: 'DARK_WALNUT',   frameWidthDp: 44, matte: 'WARM_COTTON',     matteMarginDp: 64, bottomWeighted: true,  fill: false, bevel: 'WHITE_CORE', depth: 0.35, glaze: true  },
  { id: 'minimal',   label: 'Pitch Black OLED', moulding: 'MODERN_BLACK',  frameWidthDp: 24, matte: 'NONE',            matteMarginDp: 0,  bottomWeighted: false, fill: true,  bevel: null,         depth: 0.12, glaze: false },
  { id: 'nordic',    label: 'Nordic Oak',       moulding: 'NATURAL_OAK',   frameWidthDp: 36, matte: 'ANTIQUE_CREAM',   matteMarginDp: 20, bottomWeighted: false, fill: true,  bevel: 'CREAM_CORE', depth: 0.25, glaze: true  },
  { id: 'gilded',    label: 'Gilded Gold',      moulding: 'ANTIQUE_BRASS', frameWidthDp: 48, matte: 'NONE',            matteMarginDp: 0,  bottomWeighted: false, fill: true,  bevel: null,         depth: 0.14, glaze: true  },
  { id: 'slim',      label: 'Ultra-Slim Matte', moulding: 'DARK_WALNUT',   frameWidthDp: 36, matte: 'WARM_COTTON',     matteMarginDp: 16, bottomWeighted: false, fill: true,  bevel: 'WHITE_CORE', depth: 0.25, glaze: true  },
  { id: 'fullframe', label: 'Full Frame',       moulding: 'DARK_WALNUT',   frameWidthDp: 36, matte: 'NONE',            matteMarginDp: 0,  bottomWeighted: false, fill: true,  bevel: null,         depth: 0.1,  glaze: true  },
];

/* What the app actually bundles, from ArtworkRepository.kt: 7 public-domain
   masterworks (Wikimedia), 3 landscape photographs and 20 minimalist/geometric
   photographs (both Unsplash, all 3:2) — 30 images in total.

   The site shows LANDSCAPE work only. A television is a landscape panel, and a
   portrait print on it is honest but unrepresentative of how the app is used,
   so the Vermeer, the Friedrich and the square Klimt are left to the app. */
const ART = [
  { title: 'The Starry Night',            artist: 'Vincent van Gogh',   year: '1889', ar: 1.258, url: 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/ea/Van_Gogh_-_Starry_Night_-_Google_Art_Project.jpg/1280px-Van_Gogh_-_Starry_Night_-_Google_Art_Project.jpg' },
  { title: 'The Great Wave off Kanagawa', artist: 'Katsushika Hokusai', year: '1831', ar: 1.488, url: 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Tsunami_by_hokusai_19th_century.jpg/1280px-Tsunami_by_hokusai_19th_century.jpg' },
  { title: 'A Sunday on La Grande Jatte', artist: 'Georges Seurat',     year: '1884', ar: 1.516, url: 'https://upload.wikimedia.org/wikipedia/commons/thumb/7/7d/A_Sunday_on_La_Grande_Jatte%2C_Georges_Seurat%2C_1884.jpg/1280px-A_Sunday_on_La_Grande_Jatte%2C_Georges_Seurat%2C_1884.jpg' },
  { title: 'Water Lilies',                artist: 'Claude Monet',       year: '1916', ar: 1.065, url: 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/14/Claude_Monet_-_Water_Lilies_-_Google_Art_Project.jpg/1280px-Claude_Monet_-_Water_Lilies_-_Google_Art_Project.jpg' },
];

/* The minimalist set — six of the twenty in `geometricPatterns`
   (ArtworkRepository.kt). Ids and titles are copied verbatim so a caption here
   always names the photograph the app would show. All 3:2. */
const MINIMAL = [
  { id: 'geo_6',  title: 'Symmetrical black and white architectural pattern with sky', photo: 'photo-1758781538402-ce262e43719f' },
  { id: 'geo_15', title: 'Abstract orange lines on a dark background',                  photo: 'photo-1758637612224-82540ceeb007' },
  { id: 'geo_18', title: 'Spiral staircase with warm lighting and dark background',     photo: 'photo-1758801305948-adbc9fc7966b' },
  { id: 'geo_9',  title: 'Looking up at modern skyscrapers against a clear sky',        photo: 'photo-1759496435064-c81eddcb9b95' },
  { id: 'geo_8',  title: 'A black and white facade of many windows',                    photo: 'photo-1758528851112-0d2dae1870c4' },
  { id: 'geo_17', title: 'Sunlight streams across brick wall and staircase',            photo: 'photo-1759516176657-69df2e4856cf' },
].map((p) => ({ ...p, ar: 1.5, year: '', artist: 'Unsplash', url: `https://images.unsplash.com/${p.photo}?w=1280&q=80` }));

const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;

/* ------------------------------------------------------------- the frame */

const frame   = document.getElementById('frame');
const screenEl = document.getElementById('screen');
const layers  = [document.getElementById('artA'), document.getElementById('artB')];
const pTitle  = document.getElementById('pTitle');
const pMeta   = document.getElementById('pMeta');
const rail    = document.getElementById('rail');

let artIndex = 0;
let front = 0;
let preset = PRESETS[0];
let timer = null;

function applyPreset(p) {
  preset = p;
  const m = MOULDINGS[p.moulding];
  const mat = MATTES[p.matte];
  const bev = p.bevel ? BEVELS[p.bevel] : null;

  frame.style.setProperty('--moulding-w', p.moulding === 'NONE' ? '0%' : W(p.frameWidthDp));
  frame.style.setProperty('--moulding-a', m.a);
  frame.style.setProperty('--moulding-b', m.b);
  frame.style.setProperty('--matte-c', mat.hex);
  frame.style.setProperty('--matte-m', W(p.matteMarginDp));
  frame.style.setProperty('--bw', p.bottomWeighted ? 1.18 : 1);
  frame.style.setProperty('--bevel-on', bev ? 1 : 0);
  frame.style.setProperty('--bevel-hi', bev ? bev.hi : 'transparent');
  frame.style.setProperty('--bevel-sh', bev ? bev.sh : 'transparent');
  frame.style.setProperty('--depth', p.depth);
  frame.dataset.metallic = String(Boolean(m.metallic));
  screenEl.style.setProperty('--glaze-on', p.glaze ? 1 : 0);

  frame.dataset.fit = p.fill ? 'cover' : 'contain';
  frame.style.setProperty('--ar', ART[artIndex].ar);

  rail.querySelectorAll('.chip').forEach((c) => {
    c.setAttribute('aria-pressed', String(c.dataset.id === p.id));
  });
}

let seq = 0;
let misses = 0;

/* Crossfade to artwork `i`. The incoming picture is preloaded first, so the
   layer never swaps to a half-painted image, and a sequence token makes a
   slow load that has since been superseded a no-op instead of a blank frame. */
function show(i) {
  const n = (i + ART.length) % ART.length;
  const a = ART[n];
  const token = ++seq;
  const cur = front;
  const nxt = 1 - front;
  const back = layers[nxt];

  const pre = new Image();
  pre.decoding = 'async';

  pre.onload = async () => {
    if (token !== seq) return;
    misses = 0;
    back.src = a.url;
    back.alt = `${a.title} by ${a.artist}, ${a.year}`;

    /* Wait for the layer itself to be decodable before anything visible moves,
       or the placard names the next picture while the frame still shows the last. */
    try { await back.decode(); } catch { /* fine: fall through and swap anyway */ }
    if (token !== seq) return;

    back.classList.add('is-on');
    layers[cur].classList.remove('is-on');
    front = nxt;
    artIndex = n;
    frame.style.setProperty('--ar', a.ar);
    pTitle.textContent = a.title;
    pMeta.textContent = `${a.artist} · ${a.year}`;
  };

  /* Skip past an image that will not load rather than stalling on it. */
  pre.onerror = () => {
    if (token !== seq) return;
    if (++misses < ART.length) show(n + 1);
  };

  pre.src = a.url;
}

function startSlideshow() {
  if (reduced) return;
  clearInterval(timer);
  timer = setInterval(() => show(artIndex + 1), 7000);
}

/* Build the preset rail. */
rail.innerHTML = PRESETS.map((p) => {
  const m = MOULDINGS[p.moulding];
  const sw = p.moulding === 'NONE'
    ? MATTES[p.matte].hex
    : `linear-gradient(135deg, ${m.b}, ${m.a})`;
  return `<button class="chip" type="button" data-id="${p.id}" aria-pressed="false">
            <span class="chip-swatch" style="background:${sw}"></span>${p.label}
          </button>`;
}).join('');

rail.addEventListener('click', (e) => {
  const chip = e.target.closest('.chip');
  if (!chip) return;
  const p = PRESETS.find((x) => x.id === chip.dataset.id);
  if (p) { applyPreset(p); startSlideshow(); }
});

applyPreset(PRESETS[0]);
layers[0].src = ART[0].url;
layers[0].alt = `${ART[0].title} by ${ART[0].artist}, ${ART[0].year}`;
startSlideshow();

/* Pause while the hero is off screen — no point burning bandwidth or CPU. */
if ('IntersectionObserver' in window) {
  new IntersectionObserver((entries) => {
    for (const en of entries) {
      if (en.isIntersecting) startSlideshow();
      else clearInterval(timer);
    }
  }, { threshold: 0.12 }).observe(screenEl);
}

/* --------------------------------------------------------- material lists */

const swatchRow = (name, hex, wood) => `
  <li>
    <span class="sw" style="background:${hex}"${wood ? ' data-wood="true"' : ''}></span>
    <span>${name}</span>
    <span class="hex">${hex.toUpperCase()}</span>
  </li>`;

document.getElementById('matList').innerHTML = Object.values(MATTES)
  .filter((m) => m.hex !== 'transparent')
  .map((m) => swatchRow(m.name, m.hex))
  .join('');

document.getElementById('mouldList').innerHTML = Object.entries(MOULDINGS)
  .filter(([k]) => k !== 'NONE')
  .map(([, m]) => `
    <li>
      <span class="sw" data-wood="true" style="background:linear-gradient(135deg, ${m.b}, ${m.a})"></span>
      <span>${m.name}</span>
      <span class="hex">${m.a.toUpperCase()}</span>
    </li>`)
  .join('') + `
    <li>
      <span class="sw" data-wood="true" style="background:repeating-linear-gradient(45deg,#2a2724 0 4px,#1a1917 4px 8px)"></span>
      <span>Frameless (Edge-to-Edge)</span>
      <span class="hex">—</span>
    </li>`;

/* Both scales are on the remote: TvSettingsOverlay.kt, "Matte Thickness / Margin"
   and "Frame Width". dp values are against a 960dp-wide panel. */
const MAT_THICKNESS = [
  { label: 'Ultra-Slim', dp: 8 },
  { label: 'Slim', dp: 16 },
  { label: 'Medium', dp: 32 },
  { label: 'Classic', dp: 64 },
  { label: 'Deep', dp: 96 },
];
const FRAME_WIDTH = [
  { label: 'Slim', dp: 18 },
  { label: 'Classic', dp: 32 },
  { label: 'Bold', dp: 48 },
  { label: 'Deep', dp: 68 },
];

const gaugeRow = (rows, tone) => {
  const max = Math.max(...rows.map((r) => r.dp));
  return rows.map((r) => `
    <li>
      <span class="gauge" style="--fill:${(r.dp / max * 100).toFixed(1)}%;--tone:${tone}"></span>
      <span>${r.label}</span>
      <span class="hex">${r.dp}dp</span>
    </li>`).join('');
};

document.getElementById('thicknessList').innerHTML =
  gaugeRow(MAT_THICKNESS, 'var(--mat-paper)');
document.getElementById('widthList').innerHTML =
  gaugeRow(FRAME_WIDTH, 'var(--bronze-lt)');

/* ----------------------------------------------------------- gallery strip */

const plate = (a) => `
  <figure class="plate" style="margin:0">
    <div class="plate-img">
      <div class="plate-mat">
        <img src="${a.url}" alt="${a.title}${a.artist ? ', ' + a.artist : ''}" loading="lazy" decoding="async">
      </div>
    </div>
    <figcaption class="plate-cap"><b>${a.title}</b><span>${[a.artist, a.year].filter(Boolean).join(' · ')}</span></figcaption>
  </figure>`;

document.getElementById('strip').innerHTML = ART.map(plate).join('');
const minStrip = document.getElementById('stripMinimal');
if (minStrip) minStrip.innerHTML = MINIMAL.map(plate).join('');

/* ------------------------------------------------------------------ chrome */

const nav = document.getElementById('nav');
const onScroll = () => { nav.dataset.stuck = String(window.scrollY > 12); };
onScroll();
addEventListener('scroll', onScroll, { passive: true });

document.getElementById('year').textContent = new Date().getFullYear();
