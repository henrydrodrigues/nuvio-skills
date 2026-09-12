# HTML Build Conventions

Reference patterns extracted from the proven programmatic renderer.
Use these as building blocks — adapt, combine, and extend freely.

---

## 1. Page Shell

Every output must follow this skeleton:

```html
<!DOCTYPE html>
<html lang="[detect from source]" data-theme="[default per style]">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[doc title]</title>
  <!-- Google Fonts (from design style file) — Stage 05 strips these for offline
       compatibility; CSS var() fallbacks (sans-serif, monospace) ensure readability. -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="[fonts_url from design style]" rel="stylesheet">
  <!-- No-JS fallback: force sections visible + show first tab panel -->
  <noscript><style>.js-ready .section{opacity:1!important;transform:none!important;animation:none!important}.tab-panel:first-of-type{display:block!important}</style></noscript>
  <!-- Chart.js (only if any chart widget is used) — Stage 05 replaces this CDN
       tag with the full inlined bundle for offline / iOS Files Quick Look support. -->
  <script defer src="https://cdn.jsdelivr.net/npm/chart.js@4/dist/chart.umd.min.js"></script>
  <style>
    /* Section 2: CSS Foundation */
  </style>
</head>
<body>
  <div class="layout">
    <nav class="sidebar" id="sidebar">
      <div class="sidebar-inner">
        <div class="sidebar-brand">[title]</div>
        <div class="progress-track"><div class="progress-fill" id="progress-fill"></div></div>
        <!-- One nav-link per section -->
        <a class="nav-link" href="#section-id" data-target="section-id">Section Heading</a>
        <!-- Optional: nav-group-label for multi-part docs -->
      </div>
    </nav>
    <div class="main-wrap">
      <div class="topbar" id="topbar">
        <div class="topbar-left">
          <button class="topbar-btn hamburger-btn" id="hamburger" onclick="toggleSidebar()" title="Menu" aria-label="Toggle sidebar">&#9776;</button>
          <span class="topbar-title">[title]</span>
          <!-- Optional: status badge -->
          <span class="status-badge">[status]</span>
        </div>
        <div class="topbar-right">
          <div class="topbar-meta">
            <span>v[version]</span>
            <span>[date]</span>
          </div>
          <button class="topbar-btn" onclick="toggleTheme()" title="Toggle light/dark theme" aria-label="Toggle theme">&#127763;</button>
          <button class="topbar-btn" onclick="window.print()" title="Print" aria-label="Print document">&#128424;</button>
        </div>
      </div>
      <header class="doc-header">
        <h1 class="doc-title">[title]</h1>
        <div class="doc-meta">
          <span><strong>Author:</strong> [author]</span>
          <span><strong>Date:</strong> [date]</span>
        </div>
      </header>
      <main class="content" id="content">
        <!-- One section per top-level heading -->
        <section class="section" id="[kebab-id]">
          <div class="section-num">[01]</div>
          <h2 class="section-heading">[heading]</h2>
          <div class="section-subtitle">[optional subtitle]</div>
          <div class="widget">
            <!-- Widget HTML here -->
          </div>
        </section>
      </main>
      <footer class="doc-footer">
        <span>[org]</span>
        <span>Generated [date] &middot; Source: [slug]</span>
      </footer>
    </div>
  </div>
  <!-- Modal -->
  <div id="modal-backdrop" onclick="closeModal()"></div>
  <div id="detail-modal" role="dialog" aria-modal="true">
    <div class="modal-header">
      <span id="modal-title"></span>
      <button class="modal-close" onclick="closeModal()" aria-label="Close">&#10005;</button>
    </div>
    <div id="modal-body" class="modal-body"></div>
  </div>
  <script>
    /* Section 6: JavaScript */
  </script>
</body>
</html>
```

---

## 2. Design Style Integration

### How to apply a design style

1. Read `style_slug` from `work.json` — never infer.
2. Load `skills/md2html-cognitive/design-styles/design-style-[slug].md`.
3. Extract all `:root` tokens and place them in the CSS `:root {}` block.
4. Extract `[data-theme="..."]` override tokens and place them in the corresponding CSS selector.
5. Set `<html data-theme="[default_theme]">` from the style file's default.

### CSS token injection

```css
:root {
    --bg: #0d1117;
    --surface: #161b22;
    --surface-2: #1c2128;
    --border: #21262d;
    --ink: #e6edf3;
    --ink-55: #8b949e;
    --ink-20: #30363d;
    --accent: #f0a500;
    --accent-2: #ffc947;
    --accent-bg: rgba(240,165,0,.12);
    --ok: #3fb950;
    --ok-bg: rgba(63,185,80,.12);
    --warn: #d29922;
    --warn-bg: rgba(210,153,34,.12);
    --danger: #f85149;
    --danger-bg: rgba(248,81,73,.12);
    --info: #388bfd;
    --info-bg: rgba(56,139,253,.12);
    --radius: 8px;
    --radius-sm: 4px;
    --font-display: 'Space Grotesk', sans-serif;
    --font-body: 'Inter', sans-serif;
    --font-mono: 'JetBrains Mono', monospace;
    --transition: all 0.2s ease;
}
```

### Alternate theme overrides

Each style has an alternate theme. For dark-default styles the alternate is light; for light-default styles the alternate is dark.

```css
[data-theme="light"] {
    --bg: #f6f8fa;
    --surface: #ffffff;
    --surface-2: #f6f8fa;
    --border: #d0d7de;
    --ink: #1f2328;
    --ink-55: #636c76;
    --ink-20: #d0d7de;
    --ok: #0f7f5e;
    --ok-bg: #d8f0e6;
    --warn: #a76800;
    --warn-bg: #fdedce;
    --danger: #b8242e;
    --danger-bg: #fbe2e5;
    --info: #1c63b8;
    --info-bg: #e3eefb;
}
```

### Per-style theme overrides

| Style slug | Default theme | Alternate theme |
|-----------|---------------|-----------------|
| `dark-terminal` | dark | light |
| `editorial-warm` | light | dark |
| `clinical-blue` | light | dark |
| `pastel-soft` | light | dark |
| `brutalist-mono` | light | dark |

**editorial-warm dark overrides:**
`--bg:#1e1a14` `--surface:#2a2520` `--surface-2:#332e28` `--border:rgba(244,240,232,.14)` `--ink:#f4f0e8` `--ink-55:rgba(244,240,232,.55)` `--ink-20:rgba(244,240,232,.14)` `--ok:#3ecfba` `--ok-bg:#0a2e28` `--warn:#e8a82c` `--warn-bg:#2e1e00` `--danger:#e06078` `--danger-bg:#2e0a18` `--info:#5aaaf0` `--info-bg:#092040`

**clinical-blue dark overrides:**
`--bg:#0f1e35` `--surface:#172a47` `--surface-2:#1f3556` `--border:#2c456a` `--ink:#eaf1fb` `--ink-55:#9bb0cc` `--ink-20:#3a527a` `--ok:#3ecfba` `--ok-bg:#0a2e28` `--warn:#e8a82c` `--warn-bg:#2e1e00` `--danger:#e06078` `--danger-bg:#2e0a18` `--info:#5aacf8` `--info-bg:#082040`

**pastel-soft dark overrides:**
`--bg:#1a1a2e` `--surface:#222238` `--surface-2:#2a2a44` `--border:rgba(220,210,255,.14)` `--ink:#e8e4f8` `--ink-55:rgba(232,228,248,.55)` `--ink-20:rgba(232,228,248,.14)` `--ok:#40d4ba` `--ok-bg:#0a3028` `--warn:#e8b030` `--warn-bg:#302000` `--danger:#e06888` `--danger-bg:#300a20` `--info:#70a8f8` `--info-bg:#0a1e44`

**brutalist-mono dark overrides:**
`--bg:#0a0a0a` `--surface:#111111` `--surface-2:#1a1a1a` `--border:rgba(255,255,255,.14)` `--ink:#f0f0f0` `--ink-55:rgba(240,240,240,.55)` `--ink-20:rgba(240,240,240,.14)` `--ok:#30c0a8` `--ok-bg:#0a2820` `--warn:#c09820` `--warn-bg:#281800` `--danger:#c05068` `--danger-bg:#280818` `--info:#4890d8` `--info-bg:#081830`

---

## 3. CSS Foundation

All CSS below uses `var(--token)` references. Never hardcode hex values outside `:root`.

```css
/* ── Reset ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html { scroll-behavior: smooth; }
body {
  background: var(--bg);
  color: var(--ink);
  font-family: var(--font-body, sans-serif);
  font-size: clamp(14px, 2.5vw, 16px);
  font-weight: 300;
  line-height: 1.7;
}

/* ── Custom scrollbar ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--ink-20); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--ink-55); }

/* ── Layout ── */
.layout { display: flex; min-height: 100vh; }
.main-wrap { flex: 1; display: flex; flex-direction: column; min-width: 0; }

/* ── Topbar ── */
.topbar {
  background: var(--surface);
  border-bottom: 2px solid var(--accent);
  position: sticky; top: 0; z-index: 100;
  display: flex; align-items: center; justify-content: space-between;
  padding: 0 1.25rem; height: 52px; gap: 1rem;
}
.topbar-left { display: flex; align-items: center; gap: .75rem; min-width: 0; }
.topbar-title {
  font-family: var(--font-display, sans-serif);
  font-size: clamp(13px, 1.6vw, 16px); font-weight: 700;
  color: var(--ink); white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
.topbar-right { display: flex; align-items: center; gap: .5rem; flex-shrink: 0; }
.topbar-meta { font-size: .75rem; color: var(--ink-55); display: flex; gap: .75rem; flex-wrap: wrap; }
.topbar-meta span { white-space: nowrap; }
.status-badge {
  display: inline-flex; align-items: center;
  padding: .15rem .6rem; border-radius: 100px;
  font-size: .72rem; font-weight: 600; white-space: nowrap;
  background: var(--info-bg, #dce8f4); color: var(--info, #1c63b8);
}
.topbar-btn {
  background: transparent; border: 1px solid var(--border);
  border-radius: var(--radius-sm, 6px); color: var(--ink-55);
  cursor: pointer; font-size: 1rem; line-height: 1;
  padding: .3rem .5rem; transition: var(--transition, all .2s);
}
.topbar-btn:hover { color: var(--accent); border-color: var(--accent); background: var(--surface-2); }
.hamburger-btn { display: none; }

/* ── Sidebar ── */
.sidebar {
  width: 260px; flex-shrink: 0;
  background: var(--surface); border-right: 1px solid var(--border);
  position: sticky; top: 0; height: 100vh;
  overflow-y: auto; transition: transform .3s ease;
}
.sidebar-inner { padding: 1.5rem 0 2.5rem; }
.sidebar-brand {
  font-family: var(--font-display, sans-serif);
  font-size: 0.85rem; font-weight: 700; color: var(--ink-55);
  padding: 0 1.25rem .75rem; border-bottom: 1px solid var(--border);
  margin-bottom: .5rem; word-break: break-word;
}
.progress-track { height: 3px; background: var(--surface-2); margin: 0 0 .75rem; }
.progress-fill { height: 100%; background: var(--accent); width: 0%; transition: width .3s ease; }
.nav-group-label {
  font-size: 0.7rem; font-weight: 700; letter-spacing: .08em;
  text-transform: uppercase; color: var(--ink-20); padding: 0.75rem 1.25rem 0.25rem;
}
.nav-link {
  display: block; padding: 0.35rem 1.25rem;
  color: var(--ink-55); text-decoration: none;
  font-size: 0.875rem; font-weight: 500;
  border-left: 3px solid transparent; transition: var(--transition, color .15s);
}
.nav-link:hover, .nav-link.active {
  color: var(--accent); border-left-color: var(--accent); background: var(--surface-2);
}

/* ── Header ── */
.doc-header {
  background: var(--surface); border-bottom: 1px solid var(--border);
  padding: 2rem 2.5rem 1.5rem;
}
.doc-title {
  font-family: var(--font-display, sans-serif);
  font-size: clamp(36px, 4.8vw, 58px); font-weight: 500;
  letter-spacing: -0.02em; color: var(--ink); line-height: 1.15; margin-bottom: .5rem;
}
.doc-meta { display: flex; flex-wrap: wrap; gap: .5rem 1.5rem; font-size: .8rem; color: var(--ink-55); }

/* ── Content ── */
.content { flex: 1; padding: 2rem 2.5rem; max-width: 960px; margin: 0 auto; width: 100%; }
/* Progressive enhancement: sections visible by default.
   JS adds .js-ready to <html> on load — only then are sections hidden
   and revealed by IntersectionObserver. A CSS-only @keyframes fallback
   forces visibility after 1s even if JS dies mid-execution (iOS Files
   Quick Look, restrictive WebViews). If JS works, .visible cancels
   the animation. */
.section {
  margin-bottom: 4rem; scroll-margin-top: 4rem;
}
.js-ready .section {
  opacity: 0; transform: translateY(16px);
  transition: opacity 0.5s ease, transform 0.5s ease;
  animation: section-fallback 0s 1s forwards;
}
.js-ready .section.visible { opacity: 1; transform: translateY(0); animation: none; }
@keyframes section-fallback { to { opacity: 1; transform: translateY(0); } }
@media (prefers-reduced-motion: reduce) { .js-ready .section { opacity: 1; transform: none; transition: none; animation: none; } }
.section-num {
  font-family: var(--font-mono, monospace); font-size: .7rem; font-weight: 600;
  letter-spacing: .08em; text-transform: uppercase; color: var(--accent); margin-bottom: .3rem;
}
.section-heading {
  font-family: var(--font-display, sans-serif);
  font-size: clamp(1.25rem, 4vw, 1.9rem); font-weight: 500; letter-spacing: -0.02em;
  color: var(--ink); margin-bottom: 1rem; padding-bottom: .5rem;
  border-bottom: 2px solid var(--accent);
}
.section-subtitle { font-size: .9rem; color: var(--ink-55); margin-top: -.5rem; margin-bottom: 1rem; }
.widget { margin-bottom: 1.5rem; }

/* ── Part dividers ── */
.section.part-header { border-top: 2px solid var(--accent); padding-top: 2.5rem; margin-top: 4rem; }
.section.part-header .section-heading {
  font-size: clamp(28px, 3.5vw, 40px); color: var(--accent); border-bottom-color: transparent;
}

/* ── Footer ── */
.doc-footer {
  border-top: 1px solid var(--border); padding: 1rem 2.5rem;
  font-size: .78rem; color: var(--ink-20);
  display: flex; justify-content: space-between; flex-wrap: wrap; gap: .5rem;
}

/* ── Modal ── */
#modal-backdrop {
  position: fixed; inset: 0; background: rgba(0,0,0,.7);
  backdrop-filter: blur(4px); z-index: 200;
  opacity: 0; pointer-events: none; transition: opacity 300ms ease;
}
#modal-backdrop.open { opacity: 1; pointer-events: auto; }
#detail-modal {
  position: fixed; top: 0; right: 0; bottom: 0;
  width: min(480px, 95vw); background: var(--surface);
  border-left: 1px solid var(--border); z-index: 201;
  display: flex; flex-direction: column;
  transform: translateX(100%); transition: transform 300ms ease; overflow: hidden;
}
#detail-modal.open { transform: translateX(0); }
.modal-header {
  display: flex; align-items: center; justify-content: space-between;
  padding: 1rem 1.25rem; border-bottom: 2px solid var(--accent); flex-shrink: 0; gap: .75rem;
}
#modal-title { font-family: var(--font-display, sans-serif); font-weight: 600; font-size: 1rem; color: var(--ink); }
.modal-close {
  background: transparent; border: 1px solid var(--border);
  border-radius: var(--radius-sm, 4px); color: var(--ink-55);
  cursor: pointer; font-size: 1rem; line-height: 1; padding: .25rem .5rem;
  flex-shrink: 0; transition: var(--transition, all .2s);
}
.modal-close:hover { color: var(--danger); border-color: var(--danger); }
.modal-body { padding: 1.25rem; overflow-y: auto; flex: 1; }
.modal-field { margin-bottom: .75rem; }
.modal-field-label {
  font-size: .7rem; font-weight: 600; text-transform: uppercase;
  letter-spacing: .06em; color: var(--ink-55); margin-bottom: .2rem;
}
.modal-field-value { font-size: .87rem; color: var(--ink); }

/* ── Print ── */
@media print {
  .sidebar, .topbar, #modal-backdrop, #detail-modal { display: none !important; }
  .main-wrap { display: block; }
  .content { padding: 1rem; }
  .section { opacity: 1; transform: none; transition: none; break-inside: avoid; }
}

/* ── Responsive ── */

/* Tablet */
@media (max-width: 1024px) {
  .content { padding: 1.5rem 1.75rem; max-width: 100%; }
  .doc-header { padding: 1.5rem 1.75rem 1.25rem; }
  .doc-footer { padding: 1rem 1.75rem; }
  .section { margin-bottom: 3rem; }
  .flow-step { min-width: 80px; padding: .5rem .75rem; font-size: .8rem; }
  .flow-step.decision { width: 60px; height: 60px; }
  .chart-container { max-width: 100%; }
}

/* Mobile */
@media (max-width: 768px) {
  /* Sidebar off-canvas */
  .sidebar {
    position: fixed; z-index: 150; height: 100vh; top: 0;
    transform: translateX(-100%);
  }
  .sidebar.open { transform: translateX(0); box-shadow: 4px 0 24px rgba(0,0,0,.25); }
  .hamburger-btn { display: flex; }
  .content { padding: 1rem; max-width: 100%; }
  .doc-header { padding: 1.25rem 1rem 1rem; }
  .topbar-meta { display: none; }

  /* Touch targets — Apple HIG minimum 44×44 */
  .topbar-btn { min-width: 44px; min-height: 44px; display: flex; align-items: center; justify-content: center; font-size: 1.15rem; }

  /* Typography */
  .doc-title { font-size: clamp(1.75rem, 6vw, 2.5rem); }

  /* Spacing */
  .section { margin-bottom: 2.5rem; scroll-margin-top: 3.5rem; }
  .doc-footer { padding: .75rem 1rem; }

  /* KPI cards → 2 columns */
  .kpi-row { gap: .5rem; }
  .kpi-card { min-width: 0; flex: 1 1 calc(50% - .25rem); }

  /* Cards → 1 column, reduced padding */
  .card-grid { grid-template-columns: 1fr; gap: .75rem; }
  .card-item { padding: 1rem; }
  .prose-card { padding: 1rem 1.25rem; }
  .pull-quote { padding: 1rem 1.25rem; font-size: 1rem; }

  /* Flow diagram → vertical */
  .flow-diagram { flex-direction: column; align-items: stretch; }
  .flow-step { min-width: 0; width: 100%; }
  .flow-step.decision { transform: none; width: 100%; height: auto; border-radius: var(--radius, 8px); padding: .6rem 1rem; }
  .flow-step.decision .flow-label { transform: none; font-size: .8rem; }
  .flow-arrow { transform: rotate(90deg); align-self: center; }

  /* Tables — smaller padding and font */
  .data-table th, .data-table td { padding: .4rem .5rem; font-size: .75rem; }
  .data-table th { font-size: .65rem; }

  /* Tree — reduced indent */
  .tree-node { margin-left: .5rem; }

  /* Checklist — meta wraps to new line */
  .checklist-item { flex-wrap: wrap; }
  .item-meta { margin-left: 0; padding-left: 1.75rem; width: 100%; }

  /* Tabs — horizontal scroll instead of wrap */
  .tabs-nav { overflow-x: auto; flex-wrap: nowrap; -webkit-overflow-scrolling: touch; }
  .tab-btn { white-space: nowrap; flex-shrink: 0; padding: .5rem .75rem; font-size: .8rem; }

  /* Charts — full width on mobile */
  .chart-container,
  .chart-container--doughnut,
  .chart-container--bar,
  .chart-container--scurve,
  .chart-container--bubble,
  .chart-container--gantt,
  .chart-container--risk { max-width: 100%; }

  /* Filter bar — horizontal scroll */
  .filter-bar { overflow-x: auto; flex-wrap: nowrap; padding-bottom: .25rem; }
  .filter-btn { flex-shrink: 0; }

  /* Definition list */
  .def-entry { padding: .75rem 1rem; }

  /* Code block */
  .code-block-wrap pre { padding: .75rem 1rem; font-size: .78rem; }

  /* Figure */
  .figure-wrap { padding: 1rem; }

  /* Modal full-width */
  #detail-modal { width: 100vw; }
}

/* Small phone */
@media (max-width: 480px) {
  /* KPI → 1 column */
  .kpi-card { flex: 1 1 100%; }
  .kpi-card .kpi-label { font-size: .65rem; }

  /* Minimal padding */
  .content { padding: .75rem; max-width: 100%; }
  .doc-header { padding: 1rem .75rem .75rem; }

  /* Compact sections */
  .section { margin-bottom: 2rem; }
  .section-num { font-size: .6rem; }

  /* Compact topbar */
  .topbar { padding: 0 .75rem; height: 44px; }
  .topbar-title { font-size: 12px; }
  .status-badge { font-size: .65rem; padding: .1rem .4rem; }

  /* Minimal tree indent */
  .tree-node { margin-left: .35rem; }
  .tree-node > details > summary { font-size: .8rem; }
  .tree-leaf { font-size: .78rem; padding-left: 1.2rem; }

  /* Smaller checklist ring */
  .progress-ring { width: 48px; height: 48px; }
  .ring-label .ring-pct { font-size: 1rem; }
  .ring-label { font-size: .75rem; }

  /* Vertical footer */
  .doc-footer { flex-direction: column; font-size: .7rem; padding: .5rem .75rem; }
}
```

---

## 4. Widget HTML Patterns

### 4.1 KPI Summary

Summary text + KPI card row.

```html
<div class="kpi-summary-text">[overview text]</div>
<div class="kpi-row">
  <div class="kpi-card kpi-[semantic]">
    <div class="kpi-label">[LABEL]</div>
    <div class="kpi-value" data-countup="[number]">[value]</div>
  </div>
  <!-- more cards -->
</div>
```

CSS for KPI cards:

```css
.kpi-row { display: flex; flex-wrap: wrap; gap: 1rem; }
.kpi-card {
  background: var(--surface); border: 1px solid var(--border);
  border-radius: var(--radius, 8px); padding: 1.125rem 1.25rem;
  min-width: 140px; flex: 1;
  transition: transform .18s ease, box-shadow .18s ease; cursor: default;
}
.kpi-card:hover { transform: scale(1.03); box-shadow: 0 0 0 1px var(--accent), 0 6px 24px rgba(240,165,0,.15); }
.kpi-card .kpi-label {
  font-size: .75rem; font-weight: 600; color: var(--ink-55);
  text-transform: uppercase; letter-spacing: .08em; margin-bottom: .35rem;
}
.kpi-card .kpi-value { font-family: var(--font-mono, monospace); font-size: clamp(1.3rem, 4vw, 2rem); font-weight: 700; color: var(--accent); }
.kpi-card.kpi-ok    { background: var(--ok-bg, #d1f0eb); }
.kpi-card.kpi-warn  { background: var(--warn-bg, #fdf0dc); }
.kpi-card.kpi-danger { background: var(--danger-bg, #fce8ed); }
.kpi-card.kpi-info  { background: var(--info-bg, #dce8f4); }
.kpi-card.kpi-ok    .kpi-value { color: var(--ok); }
.kpi-card.kpi-warn  .kpi-value { color: var(--warn); }
.kpi-card.kpi-danger .kpi-value { color: var(--danger); }
.kpi-card.kpi-info  .kpi-value { color: var(--info); }
.kpi-card.kpi-ok .kpi-label, .kpi-card.kpi-warn .kpi-label,
.kpi-card.kpi-danger .kpi-label, .kpi-card.kpi-info .kpi-label { color: var(--ink); }
.kpi-summary-text { color: var(--ink-55); margin-bottom: 1rem; font-size: .95rem; }
```

Semantic values: `ok`, `warn`, `danger`, `info`. Add `data-countup="[number]"` to animate numeric values on scroll.

### 4.2 KPI Row

Same as KPI Summary but without the summary text.

### 4.3 Highlight List

```html
<ul class="highlight-list">
  <li>[text]<span class="hl-badge">[optional badge]</span></li>
</ul>
```

```css
.highlight-list { list-style: none; display: flex; flex-direction: column; gap: .4rem; }
.highlight-list li {
  display: flex; align-items: flex-start; gap: .6rem;
  padding: .5rem .75rem; background: var(--surface);
  border-radius: var(--radius-sm, 4px); border: 1px solid var(--border);
}
.highlight-list li::before { content: "\203A"; color: var(--accent); font-weight: 700; flex-shrink: 0; }
.hl-badge {
  margin-left: auto; font-size: .7rem; padding: .1rem .45rem;
  border-radius: var(--radius-sm, 4px); background: var(--surface-2); color: var(--ink-55); white-space: nowrap;
}
```

### 4.4 Card Grid

```html
<div class="card-grid">
  <div class="card-item">
    <div class="card-title">[title]<span class="hl-badge">[badge]</span></div>
    <div class="card-body">[body text]</div>
    <div class="card-tags"><span class="card-tag">[tag]</span></div>
  </div>
</div>
```

```css
.card-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(min(220px, 100%), 1fr)); gap: 1rem; }
.card-item {
  background: var(--surface); border: 1px solid var(--border);
  border-radius: var(--radius, 8px); padding: 1.5rem;
  transition: transform .18s ease, box-shadow .18s ease;
}
.card-item:hover { transform: translateY(-2px); box-shadow: 0 8px 28px rgba(30,26,20,.08); }
.card-item .card-title { font-weight: 600; margin-bottom: .4rem; }
.card-item .card-body { font-size: .85rem; color: var(--ink-55); }
.card-tags { margin-top: .5rem; display: flex; flex-wrap: wrap; gap: .25rem; }
.card-tag { font-size: .7rem; padding: .1rem .4rem; background: var(--surface-2); border-radius: var(--radius-sm, 4px); color: var(--ink-55); }
```

### 4.5 Sortable Table

```html
<div class="table-wrap">
  <table class="data-table" id="[uid]">
    <thead><tr>
      <th onclick="sortTable('[uid]',0)">[Column] <span class="sort-icon"></span></th>
    </tr></thead>
    <tbody>
      <tr class="clickable-row" data-row='{"key":"value"}' onclick="openRowModal(this)">
        <td>[value]</td>
        <td class="mono-cell">[numeric value]</td>
      </tr>
    </tbody>
  </table>
</div>
```

```css
.table-wrap { overflow-x: auto; border: 1px solid var(--border); border-radius: var(--radius-sm, 10px); overflow: hidden; }
.data-table { width: 100%; border-collapse: collapse; font-size: .81rem; }
.data-table th, .data-table td { padding: .55rem .8rem; text-align: left; border-bottom: 1px solid var(--border); }
.data-table th {
  background: var(--surface-2); font-size: .72rem; font-weight: 600;
  color: var(--ink-55); text-transform: uppercase; letter-spacing: .05em;
  cursor: pointer; user-select: none; white-space: nowrap;
}
.data-table th:hover { color: var(--accent); }
.data-table th .sort-icon { opacity: .4; margin-left: .25rem; }
.data-table th.asc .sort-icon::after { content: " \25B2"; opacity: 1; }
.data-table th.desc .sort-icon::after { content: " \25BC"; opacity: 1; }
.data-table tr.clickable-row { cursor: pointer; }
.data-table tr.clickable-row:hover td { background: var(--surface-2); }
.mono-cell { font-family: var(--font-mono, monospace); font-size: .8rem; }
```

### 4.6 Status Table

Same structure as sortable table. Status column renders as badges:

```html
<td><span class="status-badge status-[semantic]">[status text]</span></td>
```

```css
.status-ok { background: color-mix(in srgb, var(--ok) 15%, transparent); color: var(--ok); }
.status-warn { background: color-mix(in srgb, var(--warn) 15%, transparent); color: var(--warn); }
.status-danger { background: color-mix(in srgb, var(--danger) 15%, transparent); color: var(--danger); }
.status-info { background: color-mix(in srgb, var(--info) 15%, transparent); color: var(--info); }
.status-muted { background: var(--surface-2); color: var(--ink-20); }
```

### 4.7 Gantt (Chart.js horizontal bar)

```html
<div class="chart-container"><canvas id="chart-[uid]"></canvas></div>
<script>window.__gantt_[uid] = { tasks: [...], month_count: 12, period_label: "Month" };</script>
```

Example: uid = `roadmap` → `<canvas id="chart-roadmap">` + `window.__gantt_roadmap`

Task objects: `{ name, start, end, owner (optional), critical (bool) }`

### 4.8 Doughnut (Chart.js)

```html
<div class="chart-container" style="max-width:340px;">
  <canvas id="chart-[uid]"></canvas>
</div>
<script>window.__doughnut_[uid] = { labels: [...], values: [...], colors: [...], total_label: "Total", currency: "" };</script>
```

Example: uid = `orcamento` → `<canvas id="chart-orcamento">` + `window.__doughnut_orcamento`

### 4.9 S-Curve (Chart.js bar+line combo)

```html
<div class="chart-container"><canvas id="chart-[uid]"></canvas></div>
<script>window.__scurve_[uid] = { labels: [...], monthly: [...], cumulative: [...] };</script>
```

Example: uid = `receita` → `<canvas id="chart-receita">` + `window.__scurve_receita`

### 4.10 Bubble Heatmap (Chart.js scatter)

```html
<div class="chart-container"><canvas id="chart-[uid]"></canvas></div>
<script>window.__bubble_[uid] = { points: [{x, y, r, label}], x_label: "X", y_label: "Y", x_max: 10, y_max: 10 };</script>
```

Example: uid = `verticais` → `<canvas id="chart-verticais">` + `window.__bubble_verticais`

### 4.11 Bar Chart (Chart.js grouped)

```html
<div class="chart-container"><canvas id="chart-[uid]"></canvas></div>
<script>window.__bar_[uid] = { categories: [...], series: [{label, values: [...]}] };</script>
```

Example: uid = `preco` → `<canvas id="chart-preco">` + `window.__bar_preco`

### 4.12 Tree (expand/collapse)

```html
<div class="tree-controls">
  <button class="tree-ctrl-btn" onclick="expandAllTree('[uid]')">Expand All</button>
  <button class="tree-ctrl-btn" onclick="collapseAllTree('[uid]')">Collapse All</button>
</div>
<div class="tree" id="[uid]">
  <div class="tree-node">
    <details open>
      <summary>[parent label]<span class="tree-meta">[optional meta]</span></summary>
      <div class="tree-leaf">[leaf label]<span class="tree-meta">[meta]</span></div>
      <!-- nested tree-node for deeper levels -->
    </details>
  </div>
</div>
```

```css
.tree-controls { display: flex; gap: .5rem; margin-bottom: .6rem; }
.tree-ctrl-btn {
  background: var(--surface); border: 1px solid var(--border);
  border-radius: var(--radius-sm, 4px); color: var(--ink-55);
  cursor: pointer; font-size: .72rem; font-weight: 600;
  padding: .2rem .6rem; transition: var(--transition, all .2s);
}
.tree-ctrl-btn:hover { color: var(--accent); border-color: var(--accent); }
.tree-node { margin-left: clamp(.35rem, 2vw, 1rem); }
.tree-node > details > summary {
  cursor: pointer; padding: .25rem .4rem;
  border-radius: var(--radius-sm, 4px); list-style: none;
  display: flex; align-items: center; gap: .5rem;
  color: var(--ink); font-size: .87rem;
}
.tree-node > details > summary:hover { background: var(--surface); color: var(--accent); }
.tree-node > details > summary::before { content: "\25B6"; font-size: .6rem; color: var(--ink-20); }
.tree-node > details[open] > summary::before { content: "\25BC"; }
.tree-leaf { padding: .25rem .4rem .25rem 1.6rem; font-size: .85rem; color: var(--ink-55); }
.tree-meta { font-size: .75rem; color: var(--ink-20); margin-left: .4rem; }
```

### 4.13 Flow Diagram

```html
<div class="flow-diagram">
  <div class="flow-step start"><div>[Start]</div></div>
  <div class="flow-arrow">&rarr;</div>
  <div class="flow-step"><div>[Step]</div><div class="flow-sublabel">[detail]</div></div>
  <div class="flow-arrow">&rarr;</div>
  <div class="flow-step decision"><span class="flow-label">[Decision?]</span></div>
  <div class="flow-arrow">&rarr;</div>
  <div class="flow-step end"><div>[End]</div></div>
</div>
```

```css
.flow-diagram { display: flex; flex-wrap: wrap; align-items: center; gap: .5rem; overflow-x: auto; }
.flow-step {
  background: var(--surface); border: 1px solid var(--border);
  border-radius: var(--radius, 8px); padding: .6rem 1rem;
  text-align: center; font-size: .85rem; min-width: 100px;
}
.flow-step.start, .flow-step.end {
  background: var(--accent); color: var(--bg); border-color: var(--accent); border-radius: 99px;
}
.flow-step.decision {
  background: var(--surface-2); border-style: dashed; border-radius: 0;
  transform: rotate(45deg); width: 72px; height: 72px;
  display: flex; align-items: center; justify-content: center;
}
.flow-step.decision .flow-label { transform: rotate(-45deg); font-size: .72rem; }
.flow-arrow { color: var(--accent); font-weight: 700; font-size: 1.2rem; }
.flow-sublabel { font-size: .72rem; color: var(--ink-55); }
```

### 4.14 Tabs

```html
<div class="tabs-widget" id="[uid]">
  <div class="tabs-nav">
    <button class="tab-btn active" onclick="switchTab('[uid]','tab0')">
      <span class="tab-star">&#9733;</span>[label]
    </button>
    <button class="tab-btn" onclick="switchTab('[uid]','tab1')">[label]</button>
  </div>
  <div class="tab-panel active" id="[uid]-tab0">
    <div class="kpi-row" style="margin-bottom:.75rem"><!-- optional KPIs --></div>
    <p>[body text]</p>
  </div>
  <div class="tab-panel" id="[uid]-tab1"><p>[body text]</p></div>
</div>
```

```css
.tabs-nav { display: flex; gap: .25rem; border-bottom: 1px solid var(--border); margin-bottom: 1rem; flex-wrap: wrap; }
.tab-btn {
  padding: .5rem 1rem; border: none; background: none;
  color: var(--ink-55); cursor: pointer; font-size: .87rem;
  border-bottom: 2px solid transparent; transition: var(--transition, color .15s);
}
.tab-btn.active { color: var(--accent); border-bottom-color: var(--accent); }
.tab-btn:hover { color: var(--accent); }
.tab-btn .tab-star { color: var(--warn, #d29922); margin-right: .25rem; }
.tab-panel { display: none; }
.tab-panel.active { display: block; }
```

### 4.15 Checklist

```html
<div class="checklist-widget" id="[uid]" data-checklist='{"uid":"[uid]","total":N,"done":0}'>
  <div class="checklist-ring-wrap">
    <svg class="progress-ring" viewBox="0 0 60 60" aria-hidden="true">
      <circle class="ring-track" cx="30" cy="30" r="24"/>
      <circle class="ring-fill" id="[uid]-ring" cx="30" cy="30" r="24"/>
    </svg>
    <div class="ring-label">
      <span class="ring-pct" id="[uid]-pct">0%</span>
      items completed
    </div>
  </div>
  <div class="checklist-group">
    <div class="checklist-group-label" onclick="toggleChecklistGroup(this)">[Group Label]</div>
    <div class="checklist-items">
      <div class="checklist-item" id="ci-[itemId]">
        <label class="checklist-label">
          <input type="checkbox" onchange="updateChecklist('[uid]','[itemId]',this.checked)">
          <span class="item-text">[text]</span>
        </label>
        <span class="item-meta">@[owner] &middot; <span class="overdue-date">[due]</span></span>
      </div>
    </div>
  </div>
</div>
```

```css
.checklist-widget { position: relative; }
.checklist-ring-wrap { display: flex; align-items: center; gap: .75rem; margin-bottom: 1rem; }
.progress-ring { width: 60px; height: 60px; transform: rotate(-90deg); flex-shrink: 0; }
.ring-track { fill: none; stroke: var(--surface-2); stroke-width: 5; }
.ring-fill {
  fill: none; stroke: var(--accent); stroke-width: 5; stroke-linecap: round;
  stroke-dasharray: 150.8; stroke-dashoffset: 150.8; transition: stroke-dashoffset 500ms ease;
}
.ring-label { font-family: var(--font-mono, monospace); font-size: .85rem; font-weight: 600; color: var(--ink-55); line-height: 1.3; }
.ring-label .ring-pct { font-size: 1.25rem; color: var(--accent); display: block; }
.checklist-group { margin-bottom: 1rem; }
.checklist-group-label {
  font-weight: 600; margin-bottom: .5rem; font-size: .9rem; cursor: pointer;
  display: flex; align-items: center; gap: .4rem;
}
.checklist-group-label::before { content: "\25BE"; color: var(--accent); font-size: .75rem; transition: transform .2s; }
.checklist-group.collapsed .checklist-group-label::before { content: "\25B8"; }
.checklist-group.collapsed .checklist-items { display: none; }
.checklist-item {
  display: flex; align-items: flex-start; gap: .75rem;
  padding: .4rem .5rem; border-radius: var(--radius-sm, 4px);
  border-left: 3px solid transparent;
}
.checklist-item:hover { background: var(--surface); }
.checklist-item input[type=checkbox] { margin-top: .2rem; accent-color: var(--accent); }
.checklist-label { display: flex; align-items: flex-start; gap: .75rem; flex: 1; min-width: 0; cursor: pointer; }
.checklist-item.done .item-text { text-decoration: line-through; color: var(--ink-55); }
.checklist-item.overdue { border-left-color: var(--danger); }
.item-meta { margin-left: auto; font-size: .75rem; color: var(--ink-20); white-space: nowrap; }
.item-meta .overdue-date { color: var(--danger); }
```

### 4.16 Definition List

```html
<div class="def-list">
  <div class="def-entry">
    <div class="def-term">[term]</div>
    <div class="def-definition">[definition]</div>
    <div class="def-tags"><span class="card-tag">[tag]</span></div>
  </div>
</div>
```

```css
.def-list { display: flex; flex-direction: column; gap: .6rem; }
.def-entry {
  background: var(--surface); border: 1px solid var(--border);
  border-radius: var(--radius-sm, 10px); padding: 1rem 1.25rem;
  transition: transform .18s ease, box-shadow .18s ease;
}
.def-entry:hover { transform: translateY(-1px); box-shadow: 0 4px 18px rgba(30,26,20,.07); }
.def-term { font-weight: 600; margin-bottom: .25rem; }
.def-definition { font-size: .87rem; color: var(--ink-55); }
.def-tags { margin-top: .4rem; display: flex; flex-wrap: wrap; gap: .25rem; }
```

### 4.17 Risk Heatmap

Combines: filter bar + Chart.js bubble chart + table with status badges.

```html
<div class="filter-bar" id="[uid]-filters">
  <button class="filter-btn active" onclick="filterRisks('[uid]','all')">All ([count])</button>
  <button class="filter-btn" onclick="filterRisks('[uid]','critical')">Critical ([count])</button>
  <!-- more level buttons -->
</div>
<div class="chart-container" style="max-width:460px;margin-bottom:1rem;">
  <canvas id="chart-[uid]"></canvas>
</div>
<script>window.__risk_[uid] = { risks: [{label, probability, impact, level, strategy, owner, detail}] };</script>
<div class="table-wrap">
  <table class="data-table" id="[uid]-table">
    <thead><tr><th>Risk</th><th>Prob.</th><th>Impact</th><th>Level</th><th>Strategy</th><th>Owner</th></tr></thead>
    <tbody>
      <tr class="clickable-row" data-level="[level]" data-row='{...}' onclick="openRowModal(this)">
        <td>[risk label]</td>
        <td style="text-align:center">[prob]</td>
        <td style="text-align:center">[impact]</td>
        <td><span class="status-badge status-[semantic]">[level]</span></td>
        <td>[strategy]</td>
        <td>[owner]</td>
      </tr>
    </tbody>
  </table>
</div>
```

Example: uid = `riscos` → `<canvas id="chart-riscos">` + `window.__risk_riscos`

Level to semantic mapping: `critical` -> `danger`, `high` -> `warn`, `medium` -> `info`, `low` -> `muted`.

```css
.filter-bar { display: flex; flex-wrap: wrap; gap: .4rem; margin-bottom: .75rem; }
.filter-btn {
  background: var(--surface); border: 1px solid var(--border); border-radius: 100px;
  color: var(--ink-55); cursor: pointer; font-size: .72rem; font-weight: 600;
  padding: .25rem .75rem; transition: var(--transition, all .2s); white-space: nowrap;
}
.filter-btn:hover { color: var(--accent); border-color: var(--accent); }
.filter-btn.active { background: var(--accent-bg, rgba(240,165,0,.12)); border-color: var(--accent); color: var(--accent); }
```

### 4.18 RACI Table

```html
<div class="table-wrap">
  <table class="data-table">
    <thead><tr><th>Task</th><th>[Member1]</th><th>[Member2]</th></tr></thead>
    <tbody>
      <tr>
        <td style="font-weight:600">[task label]</td>
        <td class="raci-cell raci-R">R</td>
        <td class="raci-cell raci-A">A</td>
      </tr>
    </tbody>
  </table>
</div>
```

```css
.raci-cell { text-align: center; font-weight: 700; font-size: .8rem; }
.raci-R { color: var(--accent); }
.raci-A { color: var(--danger); }
.raci-C { color: var(--info); }
.raci-I { color: var(--ink-55); }
```

### 4.19 Prose Card

```html
<div class="prose-card">
  <p>[paragraph text]</p>
  <blockquote class="prose-quote">[quote text]</blockquote>
</div>
```

```css
.prose-card {
  background: var(--surface); border: 1px solid var(--border);
  border-radius: var(--radius, 8px); padding: 1.5rem 1.75rem;
  transition: box-shadow .18s ease;
}
.prose-card:hover { box-shadow: 0 4px 18px rgba(30,26,20,.06); }
.prose-card p { margin-bottom: .8rem; line-height: 1.7; font-size: .92rem; }
.prose-card p:last-child { margin-bottom: 0; }
.prose-quote {
  border-left: 3px solid var(--accent); padding-left: 1rem;
  margin: .75rem 0; color: var(--ink-55); font-style: italic; font-size: .9rem;
}
```

### 4.20 Pull Quote

```html
<blockquote class="pull-quote">
  [quote text]
  <span class="attribution">&mdash; [attribution]</span>
</blockquote>
```

```css
.pull-quote {
  background: var(--accent-2, #fdecd8); border: 1px solid rgba(196,92,26,.18);
  border-radius: var(--radius-sm, 10px); padding: 1.25rem 1.5rem;
  font-family: var(--font-display, serif); font-style: italic;
  font-size: 1.125rem; color: var(--accent-deep, #8c3a08); line-height: 1.6;
}
.pull-quote .attribution {
  display: block; margin-top: .6rem; font-style: normal;
  font-family: var(--font-body, sans-serif); font-size: .8rem; color: var(--ink-55);
}
```

### 4.21 Code Block

```html
<div class="code-block-wrap">
  <div class="code-lang-label">[language]</div>
  <pre><code>[escaped code]</code></pre>
</div>
```

```css
.code-block-wrap {
  background: #1e1a14; border: 1px solid var(--border);
  border-radius: var(--radius, 16px); overflow: hidden;
}
.code-lang-label {
  font-size: .7rem; padding: .4rem .75rem;
  background: rgba(255,255,255,.07); color: rgba(244,240,232,.6);
  font-family: var(--font-mono, monospace); letter-spacing: .05em; text-transform: uppercase;
}
.code-block-wrap pre {
  padding: 1rem 1.25rem; overflow-x: auto;
  font-family: var(--font-mono, monospace); font-size: .82rem; line-height: 1.65; color: #f4f0e8;
}
```

### 4.22 Figure

```html
<div class="figure-wrap">
  <img src="[url]" alt="[alt text]">
  <div class="figure-caption">[caption]</div>
</div>
```

```css
.figure-wrap { background: transparent; padding: 2rem; text-align: center; }
.figure-wrap img { max-width: 320px; max-height: 160px; object-fit: contain; }
.figure-caption { font-size: .8rem; color: var(--ink-55); margin-top: .5rem; }
```

### 4.23 Motion Canvas

Animated Canvas 2D widget for cinematic data visualizations and concept animations.
Supports multiple instances per page via distinct `uid` values.

**Rules:**
- `id="mc-[uid]"` on the wrapper — prevents collisions with `<section id="...">` (same convention as `chart-[uid]` for Chart.js canvases).
- `id="canvas-[uid]"` on the `<canvas>` — used by inline animation code.
- Animation code lives entirely inside an IIFE `<script>` block — zero external dependencies.
- For `doc2html-motion`: Stage 04 inserts `/* ANIMATION_CODE_PLACEHOLDER_[uid] */`; Stage 05 injects the code from Stage 03's `animation-code.js`.
- For all other agents (e.g. `project-planner`): write the complete animation code directly inside the `<script>` block.

```html
<!-- uid: short kebab-case identifier, e.g. "motion-main", "risk-sim", "budget-flow" -->
<div class="motion-canvas-widget widget" id="mc-[uid]">
  <canvas id="canvas-[uid]" class="motion-canvas-el"
          width="800" height="450"
          aria-label="[brief description of what the animation visualizes]"></canvas>
  <script>
  (function() {
    'use strict';
    var _canvas = document.getElementById('canvas-[uid]');
    if (!_canvas || !_canvas.getContext) return;  /* graceful no-canvas fallback */
    var _ctx = _canvas.getContext('2d');

    /* Responsive: scale pixel buffer to display size × devicePixelRatio */
    function _resize() {
      var r = window.devicePixelRatio || 1;
      var w = _canvas.offsetWidth || 800;
      var h = Math.round(w * 0.5625);  /* 16:9 — adjust aspect ratio as needed */
      _canvas.width  = w * r;
      _canvas.height = h * r;
      _ctx.setTransform(r, 0, 0, r, 0, 0);
    }
    _resize();
    window.addEventListener('resize', _resize);

    /* Animation code goes here.
       Available: _canvas, _ctx, requestAnimationFrame.
       For doc2html-motion, Stage 05 replaces the placeholder below.
       For all other agents, write the complete animation directly. */
    /* ANIMATION_CODE_PLACEHOLDER_[uid] */

  })();
  </script>
</div>
```

CSS for motion-canvas widget:

```css
.motion-canvas-widget {
  background: var(--surface-2);
  border-radius: var(--radius, 8px);
  overflow: hidden;
}
.motion-canvas-el { display: block; width: 100%; height: auto; }
@media print { .motion-canvas-widget { display: none !important; } }
```

**Sidebar nav link** — add to `{{SIDEBAR_NAV}}` with the parent `<section>`'s id:
```html
<a class="nav-link" href="#[parent-section-id]" data-target="[parent-section-id]">[label]</a>
```

**Multi-instance example** (two animated sections in one document):
```html
<!-- Section A -->
<div class="motion-canvas-widget widget" id="mc-risk-sim">
  <canvas id="canvas-risk-sim" class="motion-canvas-el" width="800" height="450" aria-label="Risk simulation"></canvas>
  <script>(function() { /* risk animation code */ })();</script>
</div>

<!-- Section B -->
<div class="motion-canvas-widget widget" id="mc-budget-flow">
  <canvas id="canvas-budget-flow" class="motion-canvas-el" width="800" height="450" aria-label="Budget flow"></canvas>
  <script>(function() { /* budget animation code */ })();</script>
</div>
```

### Chart container CSS (shared)

Size charts proportionally to their data density. A doughnut with 6 slices
doesn't need 640px; a Gantt with 10 tasks does. Use these wrappers:

```css
.chart-container { position: relative; width: 100%; }
.chart-container canvas { width: 100% !important; }

/* Per-type max-width — keeps charts from blowing up on wide screens */
.chart-container--doughnut { max-width: 320px; }          /* compact, data-light */
.chart-container--bar      { max-width: 520px; }          /* moderate */
.chart-container--scurve   { max-width: 560px; }          /* moderate */
.chart-container--bubble   { max-width: 460px; }          /* square-ish */
.chart-container--gantt    { max-width: 100%; }            /* wide by nature — full width OK */
.chart-container--risk     { max-width: 460px; }           /* square-ish */
```

Apply the type modifier alongside the base class:
`<div class="chart-container chart-container--doughnut">`

### Chart uid naming rule

`[uid]` is a short content-descriptive kebab-case identifier (e.g. `mercado`, `receita`, `roadmap`).
NEVER include the chart type in the uid — the `window.__[type]_` prefix already namespaces it.
The SAME `[uid]` string must appear in BOTH `<canvas id="chart-[uid]">` AND `window.__[type]_[uid]`.

The `chart-` prefix on canvas IDs prevents collisions with `<section id="[kebab-id]">` elements
that share the same slug for sidebar navigation. Without this prefix, `document.getElementById`
returns the section instead of the canvas and the chart silently fails to render.

```
✓ uid = "mercado"  → <canvas id="chart-mercado">  + window.__doughnut_mercado
✗ uid = "doughnut-mercado" → WRONG — duplicates type prefix
✗ uid = "mercado" with <canvas id="mercado"> → WRONG — collides with <section id="mercado">
```

---

## 5. JavaScript Patterns

### 5.1 Theme Toggle

```javascript
// Restore saved theme on load
(function() {
  try {
    const saved = localStorage.getItem('doc2html_theme');
    if (saved) document.documentElement.setAttribute('data-theme', saved);
  } catch(e) {}
})();

function toggleTheme() {
  const html = document.documentElement;
  const next = html.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
  html.setAttribute('data-theme', next);
  try { localStorage.setItem('doc2html_theme', next); } catch(e) {}
  if (typeof updateChartColors === 'function') updateChartColors();
}
```

### 5.2 Mobile Sidebar

```javascript
function toggleSidebar() {
  document.getElementById('sidebar').classList.toggle('open');
}
document.addEventListener('click', function(e) {
  const sidebar = document.getElementById('sidebar');
  const hamburger = document.getElementById('hamburger');
  if (sidebar && sidebar.classList.contains('open') &&
      !sidebar.contains(e.target) && !hamburger.contains(e.target)) {
    sidebar.classList.remove('open');
  }
});
```

### 5.3 Modal

```javascript
function openModal(title, html) {
  document.getElementById('modal-title').textContent = title;
  document.getElementById('modal-body').innerHTML = html;
  document.getElementById('detail-modal').classList.add('open');
  document.getElementById('modal-backdrop').classList.add('open');
  document.body.style.overflow = 'hidden';
}
function closeModal() {
  document.getElementById('detail-modal').classList.remove('open');
  document.getElementById('modal-backdrop').classList.remove('open');
  document.body.style.overflow = '';
}
document.addEventListener('keydown', function(e) { if (e.key === 'Escape') closeModal(); });

function openRowModal(tr) {
  try {
    const data = JSON.parse(tr.getAttribute('data-row'));
    const fields = Object.entries(data)
      .filter(([k, v]) => v !== '' && v !== null && v !== undefined)
      .map(([k, v]) =>
        '<div class="modal-field">' +
        '<div class="modal-field-label">' + k + '</div>' +
        '<div class="modal-field-value">' + String(v).replace(/</g,'&lt;').replace(/>/g,'&gt;') + '</div>' +
        '</div>'
      ).join('');
    openModal(String(data[Object.keys(data)[0]] || 'Details'), fields);
  } catch(e) {}
}
```

### 5.4 KPI Count-Up Animation

```javascript
function countUp(el, target, dur) {
  dur = dur || 800;
  const start = performance.now();
  const isFloat = target % 1 !== 0;
  const original = el.textContent;
  function step(now) {
    const t = Math.min((now - start) / dur, 1);
    const ease = t < 0.5 ? 2*t*t : -1 + (4 - 2*t)*t;
    const v = target * ease;
    el.textContent = isFloat ? v.toFixed(1) : Math.round(v).toLocaleString();
    if (t < 1) requestAnimationFrame(step);
    else el.textContent = original;
  }
  requestAnimationFrame(step);
}
```

### 5.5 Section Entrance + Active Nav + Progress Bar

Progressive enhancement: add `js-ready` to `<html>` so CSS hides sections
only when JS is confirmed working. Include a 2-second timeout fallback that
forces all sections visible in case `IntersectionObserver` never fires
(e.g. iOS Files viewer, restrictive WebViews).

```javascript
(function() {
  /* Enable progressive-enhancement animations */
  document.documentElement.classList.add('js-ready');

  const links    = document.querySelectorAll('.nav-link');
  const sections = document.querySelectorAll('section.section');
  const fill     = document.getElementById('progress-fill');
  const viewed   = new Set();
  const total    = sections.length;

  const obs = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        e.target.classList.add('visible');
        viewed.add(e.target.id);
        links.forEach(l => l.classList.remove('active'));
        const link = document.querySelector('.nav-link[data-target="' + e.target.id + '"]');
        if (link) link.classList.add('active');
        if (fill && total) fill.style.width = Math.round(viewed.size / total * 100) + '%';
        e.target.querySelectorAll('[data-countup]').forEach(el => {
          if (!el.dataset.counted) {
            el.dataset.counted = '1';
            const val = parseFloat(el.getAttribute('data-countup'));
            if (!isNaN(val)) countUp(el, val, 800);
          }
        });
      }
    });
  }, { threshold: 0.12 });
  sections.forEach(s => obs.observe(s));

  /* Fallback: if IO hasn't revealed any section after 2s, force all visible.
     Covers iOS Files viewer, WKWebView quirks, and similar environments. */
  setTimeout(() => {
    sections.forEach(s => { if (!s.classList.contains('visible')) s.classList.add('visible'); });
  }, 2000);

  /* Fallback: trigger countUp for visible sections after CSS fallback fires,
     covering environments where IO never fires (iOS Files, restrictive WebViews). */
  setTimeout(() => {
    sections.forEach(s => {
      if (s.classList.contains('visible')) {
        s.querySelectorAll('[data-countup]').forEach(el => {
          if (!el.dataset.counted) {
            el.dataset.counted = '1';
            const val = parseFloat(el.getAttribute('data-countup'));
            if (!isNaN(val)) countUp(el, val, 800);
          }
        });
      }
    });
  }, 2100);
})();
```

### 5.6 Sortable Tables

```javascript
function sortTable(tableId, colIdx) {
  const table = document.getElementById(tableId);
  if (!table) return;
  const th = table.querySelectorAll('th')[colIdx];
  const tbody = table.tBodies[0];
  const rows = Array.from(tbody.rows);
  const asc = !th.classList.contains('asc');
  table.querySelectorAll('th').forEach(h => h.classList.remove('asc','desc'));
  th.classList.add(asc ? 'asc' : 'desc');
  rows.sort((a, b) => {
    const ca = a.cells[colIdx], va = ca ? ca.textContent.trim() : '';
    const cb = b.cells[colIdx], vb = cb ? cb.textContent.trim() : '';
    const na = parseFloat(va), nb = parseFloat(vb);
    if (!isNaN(na) && !isNaN(nb)) return asc ? na - nb : nb - na;
    return asc ? va.localeCompare(vb) : vb.localeCompare(va);
  });
  rows.forEach(r => tbody.appendChild(r));
}
```

### 5.7 Tabs

```javascript
function switchTab(widgetId, tabId) {
  const widget = document.getElementById(widgetId);
  if (!widget) return;
  widget.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  widget.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
  const btn = [...widget.querySelectorAll('.tab-btn')].find(
    b => b.getAttribute('onclick').includes("'" + tabId + "'")
  );
  if (btn) btn.classList.add('active');
  const panel = document.getElementById(widgetId + '-' + tabId);
  if (panel) panel.classList.add('active');
}
```

### 5.8 Checklist Persistence

```javascript
function updateChecklist(uid, itemId, done) {
  const item = document.getElementById('ci-' + itemId);
  if (item) item.classList.toggle('done', done);
  const key = 'cl_' + uid;
  let state = {};
  try { state = JSON.parse(localStorage.getItem(key) || '{}'); } catch(e) {}
  state[itemId] = done;
  try { localStorage.setItem(key, JSON.stringify(state)); } catch(e) {}
  _updateRing(uid);
}
function _updateRing(uid) {
  const widget = document.getElementById(uid);
  if (!widget) return;
  const items = widget.querySelectorAll('.checklist-item');
  const done  = widget.querySelectorAll('.checklist-item.done').length;
  const total = items.length;
  const pct   = total ? Math.round(done / total * 100) : 0;
  const ring  = document.getElementById(uid + '-ring');
  const pctEl = document.getElementById(uid + '-pct');
  const circ  = 150.8;
  if (ring) ring.style.strokeDashoffset = circ - (circ * pct / 100);
  if (pctEl) pctEl.textContent = pct + '%';
}
function toggleChecklistGroup(labelEl) {
  labelEl.closest('.checklist-group').classList.toggle('collapsed');
}
// Restore on load
document.addEventListener('DOMContentLoaded', function() {
  document.querySelectorAll('.checklist-widget').forEach(function(widget) {
    const uid = widget.id;
    let state = {};
    try { state = JSON.parse(localStorage.getItem('cl_' + uid) || '{}'); } catch(e) {}
    Object.entries(state).forEach(([itemId, done]) => {
      const item = document.getElementById('ci-' + itemId);
      if (item) {
        item.classList.toggle('done', done);
        const cb = item.querySelector('input[type=checkbox]');
        if (cb) cb.checked = done;
      }
    });
    _updateRing(uid);
  });
});
```

### 5.9 Risk Filter

```javascript
function filterRisks(uid, level) {
  const filterBar = document.getElementById(uid + '-filters');
  if (filterBar) {
    filterBar.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
    const active = [...filterBar.querySelectorAll('.filter-btn')].find(
      b => b.getAttribute('onclick').includes("'" + level + "'")
    );
    if (active) active.classList.add('active');
  }
  const table = document.getElementById(uid + '-table');
  if (!table) return;
  table.querySelectorAll('tbody tr').forEach(tr => {
    tr.style.display = (level === 'all' || tr.getAttribute('data-level') === level) ? '' : 'none';
  });
}
```

### 5.10 Tree Expand/Collapse

```javascript
function expandAllTree(uid) {
  const tree = document.getElementById(uid);
  if (tree) tree.querySelectorAll('details').forEach(d => d.open = true);
}
function collapseAllTree(uid) {
  const tree = document.getElementById(uid);
  if (tree) tree.querySelectorAll('details').forEach(d => d.open = false);
}
```

---

## 6. Chart.js Initialization

Include this block only when charts are used. It runs as an IIFE after all `window.__[type]_[id]` data globals are set.

### Chart aspect ratios

Every Chart.js chart **must** set `maintainAspectRatio: true` and an explicit
`aspectRatio` so the canvas scales proportionally and never overflows the viewport.

| Chart type | `aspectRatio` | Why |
|-----------|--------------|-----|
| Doughnut | 1.2 | Nearly square, compact |
| Bar (grouped) | 1.6 | Landscape, moderate |
| S-curve (bar+line) | 1.6 | Landscape, moderate |
| Bubble / scatter | 1.1 | Nearly square for X×Y grids |
| Gantt (horizontal bar) | Compute: `max(1.2, tasks.length * 0.35)` | Tall enough for all bars, never excessively wide |
| Risk heatmap (bubble) | 1.1 | Nearly square |

Never set `height` attribute on `<canvas>` elements — let `aspectRatio` + container `max-width` control sizing.

```javascript
(function() {
  if (typeof Chart === 'undefined') return;   // CDN may not load (offline / iOS Files Quick Look)
  window.__chartRegistry = window.__chartRegistry || [];

  function tok(name) {
    return getComputedStyle(document.documentElement).getPropertyValue(name).trim();
  }
  function ink() { return tok('--ink'); }

  const gridColor = 'rgba(128,128,128,.18)';
  const COLORS = [
    tok('--accent'), tok('--info'), tok('--ok'),
    tok('--warn'),   tok('--danger'), tok('--accent-2'),
  ];

  Chart.defaults.color = ink();
  Chart.defaults.borderColor = gridColor;
  if (window.innerWidth < 768) { Chart.defaults.font.size = 10; }

  window.updateChartColors = function() {
    const c = ink();
    Chart.defaults.color = c;
    window.__chartRegistry.forEach(chart => {
      Object.values(chart.options.scales || {}).forEach(ax => {
        if (ax.ticks) ax.ticks.color = c;
        if (ax.title) ax.title.color = c;
      });
      const leg = (chart.options.plugins || {}).legend;
      if (leg) { leg.labels = leg.labels || {}; leg.labels.color = c; }
      chart.update('none');
    });
  };

  function reg(chart) { window.__chartRegistry.push(chart); return chart; }

  function legendToggle(e, item, legend) {
    Chart.defaults.plugins.legend.onClick.call(this, e, item, legend);
    const chart = legend.chart;
    if (chart.options.scales && chart.options.scales.y) {
      delete chart.options.scales.y.min;
      delete chart.options.scales.y.max;
    }
    chart.update('active');
  }

  // Doughnut
  for (const [key, d] of Object.entries(window).filter(([k]) => k.startsWith('__doughnut_'))) {
    const id = key.replace('__doughnut_', '');
    const canvas = document.getElementById('chart-' + id);
    if (!canvas) continue;
    const colors = d.labels.map((_, i) => (d.colors && d.colors[i]) || COLORS[i % COLORS.length]);
    reg(new Chart(canvas, {
      type: 'doughnut',
      data: { labels: d.labels, datasets: [{ data: d.values, backgroundColor: colors, hoverOffset: 6 }] },
      options: { responsive: true, maintainAspectRatio: true, aspectRatio: 1.2, cutout: '65%', plugins: { legend: { position: 'bottom' }, title: { display: !!d.total_label, text: d.total_label } } }
    }));
  }

  // Bar
  for (const [key, d] of Object.entries(window).filter(([k]) => k.startsWith('__bar_'))) {
    const id = key.replace('__bar_', '');
    const canvas = document.getElementById('chart-' + id);
    if (!canvas) continue;
    reg(new Chart(canvas, {
      type: 'bar',
      data: { labels: d.categories, datasets: d.series.map((s, i) => ({ label: s.label, data: s.values, backgroundColor: COLORS[i % COLORS.length] })) },
      options: { responsive: true, maintainAspectRatio: true, aspectRatio: 1.6, plugins: { legend: { position: 'top', onClick: legendToggle } }, scales: { x: { grid: { color: gridColor }, ticks: { color: ink() } }, y: { grid: { color: gridColor }, ticks: { color: ink() } } } }
    }));
  }

  // S-Curve (bar + line combo)
  for (const [key, d] of Object.entries(window).filter(([k]) => k.startsWith('__scurve_'))) {
    const id = key.replace('__scurve_', '');
    const canvas = document.getElementById('chart-' + id);
    if (!canvas) continue;
    reg(new Chart(canvas, {
      type: 'bar',
      data: { labels: d.labels, datasets: [
        { label: 'Monthly', data: d.monthly, type: 'bar', backgroundColor: COLORS[1] + 'cc' },
        { label: 'Cumulative', data: d.cumulative, type: 'line', borderColor: COLORS[0], backgroundColor: 'transparent', tension: 0.4, fill: false, pointRadius: 3 }
      ] },
      options: { responsive: true, maintainAspectRatio: true, aspectRatio: 1.6, scales: { x: { grid: { color: gridColor }, ticks: { color: ink() } }, y: { grid: { color: gridColor }, ticks: { color: ink() } } }, plugins: { legend: { position: 'top', onClick: legendToggle } } }
    }));
  }

  // Bubble heatmap
  for (const [key, d] of Object.entries(window).filter(([k]) => k.startsWith('__bubble_'))) {
    const id = key.replace('__bubble_', '');
    const canvas = document.getElementById('chart-' + id);
    if (!canvas) continue;
    reg(new Chart(canvas, {
      type: 'bubble',
      data: { datasets: [{ data: d.points.map(p => ({ x: p.x, y: p.y, r: (p.r || 8), label: p.label })), backgroundColor: COLORS[0] + '99' }] },
      options: { responsive: true, maintainAspectRatio: true, aspectRatio: 1.1, scales: { x: { title: { display: true, text: d.x_label }, min: 0, max: d.x_max, grid: { color: gridColor }, ticks: { color: ink() } }, y: { title: { display: true, text: d.y_label }, min: 0, max: d.y_max, grid: { color: gridColor }, ticks: { color: ink() } } }, plugins: { legend: { display: false }, tooltip: { callbacks: { label: ctx => ctx.raw.label || (ctx.raw.x + ', ' + ctx.raw.y) } } } }
    }));
  }

  // Gantt (horizontal bar with floating bars)
  for (const [key, d] of Object.entries(window).filter(([k]) => k.startsWith('__gantt_'))) {
    const id = key.replace('__gantt_', '');
    const canvas = document.getElementById('chart-' + id);
    if (!canvas) continue;
    const colors = d.tasks.map(t => t.critical ? (tok('--danger') || '#f85149') : (COLORS[0] + 'cc'));
    reg(new Chart(canvas, {
      type: 'bar',
      data: { labels: d.tasks.map(t => t.name.length > 40 ? t.name.slice(0,40)+'\u2026' : t.name), datasets: [{ data: d.tasks.map(t => [t.start, t.end]), backgroundColor: colors, borderSkipped: false, borderRadius: 3 }] },
      options: { responsive: true, maintainAspectRatio: true, aspectRatio: Math.max(1.2, d.tasks.length * 0.35), indexAxis: 'y', plugins: { legend: { display: false }, tooltip: { callbacks: { label: ctx => { const t = d.tasks[ctx.dataIndex]; return [t.name, d.period_label + ' ' + t.start + ' \u2192 ' + t.end, t.owner ? 'Owner: ' + t.owner : '', t.critical ? '\u26a0 Critical path' : ''].filter(Boolean); } } } }, scales: { x: { title: { display: true, text: d.period_label }, stacked: false, max: d.month_count, grid: { color: gridColor }, ticks: { color: ink() } }, y: { grid: { color: 'transparent' }, ticks: { color: ink() } } } }
    }));
  }

  // Risk heatmap (bubble with level colors)
  for (const [key, d] of Object.entries(window).filter(([k]) => k.startsWith('__risk_'))) {
    const id = key.replace('__risk_', '');
    const canvas = document.getElementById('chart-' + id);
    if (!canvas) continue;
    const levelColor = { critical: tok('--danger') || '#f85149', high: tok('--warn') || '#d29922', medium: tok('--info') || '#388bfd', low: tok('--ok') || '#3fb950' };
    reg(new Chart(canvas, {
      type: 'bubble',
      data: { datasets: [{ data: d.risks.map(r => ({ x: r.probability, y: r.impact, r: Math.max(6, (r.probability||1) * (r.impact||1) * 1.2), label: r.label, level: r.level })), backgroundColor: d.risks.map(r => (levelColor[r.level] || COLORS[5]) + 'cc'), borderColor: d.risks.map(r => levelColor[r.level] || COLORS[5]), borderWidth: 1 }] },
      options: { responsive: true, maintainAspectRatio: true, aspectRatio: 1.1, scales: { x: { title: { display: true, text: 'Probability' }, min: 0, max: 6, grid: { color: gridColor }, ticks: { color: ink() } }, y: { title: { display: true, text: 'Impact' }, min: 0, max: 6, grid: { color: gridColor }, ticks: { color: ink() } } }, plugins: { legend: { display: false }, tooltip: { callbacks: { label: ctx => [ctx.raw.label, 'Level: ' + ctx.raw.level, 'P=' + ctx.raw.x + '  I=' + ctx.raw.y] } } } }
    }));
  }
})();
```

---

## 7. CDN Dependencies

> **Offline note**: The shared `html-shell/html_embed.py::finalize()` function
> post-processes the final HTML to make it fully self-contained: Chart.js CDN
> `<script>` tags are replaced with the inlined vendor bundle from
> `html-shell/vendor/chart.umd.min.js`, and Google Fonts `<link>` tags are stripped
> (CSS `var()` fallbacks like `sans-serif` ensure readability). This guarantees the
> HTML works in offline environments such as iOS Files app (Quick Look WKWebView).
> For `doc2html-motion`, Stage 05 calls this function. Other agents call it directly
> from their programmatic export stage.

| Library | CDN URL | When to include | Offline handling |
|---------|---------|-----------------|------------------|
| Chart.js 4 | `https://cdn.jsdelivr.net/npm/chart.js@4/dist/chart.umd.min.js` | Any chart widget used | Stage 05 inlines from `program/vendor/chart.umd.min.js` |
| Google Fonts | URL from design style file `fonts_url` field | Always | Stage 05 strips; system fonts used as fallback |
| KaTeX | `https://cdn.jsdelivr.net/npm/katex@0.16/dist/katex.min.js` + CSS | Math/formulas detected | Not yet inlined — future work |
| Mermaid | `https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js` | Mermaid code blocks detected | Not yet inlined — future work |
