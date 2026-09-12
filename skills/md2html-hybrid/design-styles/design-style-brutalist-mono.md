# Design Style — brutalist-mono

High contrast, oversized type, raw boxes, monospace everywhere. For manifestos, pitch decks, opinion pieces, single-idea statements, founder letters.

Default theme: **light**.

---

## Color Tokens

### `:root` (light, primary)

| Token | Value |
|-------|-------|
| `--bg` | `#f2f0eb` |
| `--surface` | `#ffffff` |
| `--surface-2` | `#e8e5dd` |
| `--border` | `#0a0a0a` |
| `--ink` | `#0a0a0a` |
| `--ink-55` | `#4d4d4d` |
| `--ink-20` | `#a0a0a0` |
| `--accent` | `#ff4500` |
| `--accent-2` | `#ffcb00` |
| `--accent-bg` | `#fff2e8` |
| `--ok` | `#0a8030` |
| `--ok-bg` | `#d4f0c0` |
| `--warn` | `#bb6600` |
| `--warn-bg` | `#ffe8b8` |
| `--danger` | `#cc0000` |
| `--danger-bg` | `#ffd0d0` |
| `--info` | `#0050d0` |
| `--info-bg` | `#d0e0ff` |

### `[data-theme="dark"]` overrides

| Token | Value |
|-------|-------|
| `--bg` | `#0a0a0a` |
| `--surface` | `#1a1a1a` |
| `--surface-2` | `#262626` |
| `--border` | `#f2f0eb` |
| `--ink` | `#f2f0eb` |
| `--ink-55` | `#a0a0a0` |
| `--ink-20` | `#404040` |

### Rules

| Rule | Why |
|------|-----|
| Borders are heavy and black. 2px or 3px. | Brutalist signature. |
| Accent fluorescent orange — used sparingly as shock. | Contrast against muted off-white. |
| No semi-transparent overlays. Hard fills only. | Brutal honesty in pixels. |

---

## Typography

### Families

| Role | Family | Weights |
|------|--------|---------|
| Display + everything | JetBrains Mono | 400, 500, 700, 800 |
| Optional accent display | Archivo Black | 400 |

### Google Fonts URL

```
https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700;800&family=Archivo+Black&display=swap
```

### Scale

| Role | Family | Size | Weight | Tracking |
|------|--------|------|--------|----------|
| Hero | Archivo Black | `clamp(56px, 8vw, 120px)` | 400 | -0.04em |
| Section title | JetBrains Mono | `clamp(36px, 4.5vw, 56px)` | 800 | -0.02em |
| Subsection | JetBrains Mono | 24px | 700 | -0.01em |
| Body | JetBrains Mono | 16px | 400 | default |
| Body emphasis | JetBrains Mono | 16px | 700 | default |
| KPI digit | Archivo Black | 64px | 400 | -0.04em |
| KPI label | JetBrains Mono | 11px | 500 (uppercase) | .1em |
| Eyebrow / section num | JetBrains Mono | 14px | 700 | .1em uppercase, color `--accent` |
| Nav link | JetBrains Mono | 14px | 500 (uppercase) | .05em |
| Table cell | JetBrains Mono | 14px | 400 | default |
| Badge | JetBrains Mono | 11px | 700 | .08em uppercase |

### Rules

- Mono everywhere. Including body. The whole point.
- Archivo Black is the only non-mono — hero + KPI digits, used sparingly.
- ALL UPPERCASE for labels, navigation, badges, eyebrows.
- Mixed case for body and titles only.
- Line-height tight: 1.1 for headlines, 1.5 for body.

---

## Spacing

Base unit: 8px (doubled from default). Scale: `8 16 24 32 48 64 96 128`.

| Context | Value |
|---------|-------|
| Section padding | 96px 48px |
| Card padding | 32px |
| KPI card padding | 24px |
| Sidebar width | 220px |
| Grid gap | 0 (cards share borders) or 24px |

Generous whitespace between sections. Tight within blocks.

---

## Radii

| Token | Value | Use |
|-------|-------|-----|
| `--radius` | 0 | Everything |
| `--radius-sm` | 0 | Everything |
| pill | 0 | Everything |

**No rounded corners anywhere.** Even buttons. Even badges. Sharp.

---

## Components

### Buttons

```css
.btn-primary {
  background: var(--ink);
  color: var(--bg);
  font: 700 14px var(--font-body);
  text-transform: uppercase;
  letter-spacing: .08em;
  padding: 16px 32px;
  border: 3px solid var(--ink);
  cursor: pointer;
}
.btn-primary:hover {
  background: var(--accent);
  color: var(--ink);
}

.btn-secondary {
  background: var(--bg);
  color: var(--ink);
  border: 3px solid var(--ink);
  padding: 16px 32px;
  text-transform: uppercase;
}
.btn-secondary:hover {
  box-shadow: 6px 6px 0 var(--accent);
  transform: translate(-2px, -2px);
}
```

### Cards

```css
.card {
  background: var(--surface);
  border: 2px solid var(--ink);
  padding: 32px;
  transition: transform .12s ease, box-shadow .12s ease;
}
.card:hover {
  transform: translate(-4px, -4px);
  box-shadow: 8px 8px 0 var(--ink);
}
```

Offset shadow on hover — signature brutalist move. Solid color drop, no blur.

### KPI card

```css
.kpi-card {
  background: var(--bg);
  border: 2px solid var(--ink);
  padding: 24px;
}
.kpi-card:nth-child(odd) { background: var(--accent); color: var(--ink); }
.kpi-val { font: 400 64px var(--font-display); line-height: 1; }
.kpi-label { font: 700 11px var(--font-body); text-transform: uppercase; letter-spacing: .1em; margin-top: 12px; }
```

Alternate accent fill across KPI row for rhythm.

### Badges

```css
.badge {
  background: var(--ink);
  color: var(--bg);
  font: 700 11px var(--font-body);
  text-transform: uppercase;
  letter-spacing: .08em;
  padding: 4px 10px;
  border-radius: 0;
}
.badge-danger { background: var(--danger); color: #fff; }
.badge-ok { background: var(--ok); color: #fff; }
.badge-warn { background: var(--warn); color: #fff; }
```

### Pull quote / callout

```css
.callout {
  background: var(--accent);
  color: var(--ink);
  border: 2px solid var(--ink);
  padding: 32px;
  font: 700 24px var(--font-body);
  line-height: 1.3;
}
```

### Section eyebrow + title

```css
.section-num {
  font: 700 14px var(--font-body);
  letter-spacing: .1em;
  text-transform: uppercase;
  color: var(--accent);
  margin-bottom: 16px;
}
.section-title {
  font: 800 clamp(36px, 4.5vw, 56px) var(--font-body);
  letter-spacing: -.02em;
  line-height: 1.05;
  margin-bottom: 24px;
}
```

### Sidebar active state

Solid `--accent` background block. `--ink` text. No transition — instant snap. 3px solid `--ink` left border.

### Tables

```css
.table-wrap { border: 2px solid var(--ink); }
thead th {
  background: var(--ink);
  color: var(--bg);
  text-transform: uppercase;
  font: 700 12px var(--font-body);
  letter-spacing: .08em;
  padding: 14px 16px;
  text-align: left;
}
tbody td { padding: 14px 16px; border-bottom: 1px solid var(--ink); }
tbody tr:hover { background: var(--accent); cursor: pointer; }
tbody tr:last-child td { border-bottom: none; }
```

### Modal

Right slide-in. **No backdrop blur.** Hard black overlay `rgba(0,0,0,.85)`. Panel has 3px solid `--ink` border. Header has 2px solid `--ink` bottom border.

### Charts (Chart.js overrides)

- Bars/lines: solid `--ink`, secondary `--accent`, tertiary `--info`
- No transparency on fills
- Gridlines: solid `--ink-20`
- Tooltip: `--ink` bg, `--bg` text, no border-radius, 2px border `--accent`

---

## Motion

| Element | Transition |
|---------|-----------|
| All interactive | `.12s ease` (snappy) |
| Card hover | offset translate + solid color shadow |
| Section entrance | slam-in (translateY 0 from -8px, 250ms ease) |
| Modal | instant (no transition — appears) |
| Theme toggle | instant |

Rules:
- Snap. Don't ease.
- Chart animation `duration: 0` — no animation. Bars appear final.
- Solid color shadows only. Never blur.
- Reduce-motion disables hover transform entirely.

---

## Iconography

Inline SVG. **2.5px stroke**. Sharp corners. Black only (`currentColor`). 24px standard.

Or: ASCII-style unicode (`→ ← ↑ ↓ ✕ ▶ ▾`) at body weight.

---

## Layout

| Breakpoint | Behavior |
|-----------|----------|
| ≥1280px | Sidebar 220px + content. Grids: 3 or 4 cols. |
| 768–1279px | Sidebar visible. Grids: 2 cols. |
| <768px | Sidebar off-canvas. Single col. Hero 56px font. |

- Content max-width: **1400px** (wide).
- 0 grid gap on adjacent cards (they share borders).
- KPI row: `repeat(auto-fit, minmax(200px, 1fr))`.

**Responsive rule:** All heading, KPI-digit, and hero font sizes use `clamp()` with mobile-floor and desktop-ceiling. Card padding reduces ~30% below 768px. Design tokens (colors, radii, fonts) do not change across breakpoints — only layout and spacing adapt.

---

## Principles

| Principle | Rule |
|-----------|------|
| Mono | Body, labels, tables — all monospace. |
| Sharp | 0 border-radius. Everywhere. |
| Heavy borders | 2–3px solid `--ink` on everything. |
| Solid shadows | Offset color blocks, never blur. |
| Snap motion | 100–150ms. Instant or near-instant. |
| Capitals | UI labels uppercase. Body mixed-case. |
| Oversized type | Hero 100+ pixels. Don't shrink it. |
| Loud accent | One fluorescent color. Used like a punch. |
