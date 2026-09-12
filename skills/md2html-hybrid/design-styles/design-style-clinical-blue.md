# Design Style — clinical-blue

Crisp white surfaces, steel-blue accent, conservative typography. For compliance reports, financial documents, healthcare materials, audit dossiers.

Default theme: **light**.

---

## Color Tokens

### `:root` (light, primary)

| Token | Value |
|-------|-------|
| `--bg` | `#f7f9fc` |
| `--surface` | `#ffffff` |
| `--surface-2` | `#eef2f7` |
| `--border` | `#dce3ec` |
| `--ink` | `#0f1e35` |
| `--ink-55` | `#5b6b80` |
| `--ink-20` | `#b8c2d1` |
| `--accent` | `#1c63b8` |
| `--accent-2` | `#3b85e0` |
| `--accent-bg` | `#e3eefb` |
| `--accent-deep` | `#0d3b75` |
| `--ok` | `#0f7f5e` |
| `--ok-bg` | `#d8f0e6` |
| `--warn` | `#a76800` |
| `--warn-bg` | `#fdedce` |
| `--danger` | `#b8242e` |
| `--danger-bg` | `#fbe2e5` |
| `--info` | `#1c63b8` |
| `--info-bg` | `#e3eefb` |

### `[data-theme="dark"]` overrides

| Token | Value |
|-------|-------|
| `--bg` | `#0f1e35` |
| `--surface` | `#172a47` |
| `--surface-2` | `#1f3556` |
| `--border` | `#2c456a` |
| `--ink` | `#eaf1fb` |
| `--ink-55` | `#9bb0cc` |
| `--ink-20` | `#3a527a` |

### Rules

| Rule | Why |
|------|-----|
| Pure white surfaces on subtle blue-tinted background. | Reads as document-paper. |
| `--accent` only on key CTAs, active states, KPI digits. | Conservative restraint. |
| Semantic colors are desaturated, never neon. | Medical/financial sobriety. |

---

## Typography

### Families

| Role | Family | Weights |
|------|--------|---------|
| Display | Source Serif Pro | 400, 600, 700 |
| Body / UI | Inter | 400, 500, 600, 700 |
| Mono / numbers | IBM Plex Mono | 400, 500 |

### Google Fonts URL

```
https://fonts.googleapis.com/css2?family=Source+Serif+Pro:wght@400;600;700&family=Inter:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap
```

### Scale

| Role | Family | Size | Weight |
|------|--------|------|--------|
| Hero | Source Serif | `clamp(32px, 4vw, 48px)` | 700 |
| Section title | Source Serif | 28px | 700 |
| Subsection | Source Serif | 20px | 600 |
| Body | Inter | 15px | 400 |
| Body strong | Inter | 15px | 600 |
| KPI digit | IBM Plex Mono | 30px | 500 (color `--accent`) |
| KPI label | Inter | 11px | 500 (uppercase, .05em, `--ink-55`) |
| Eyebrow / section num | IBM Plex Mono | 11px | 500 (color `--accent`, .1em tracking) |
| Nav link | Inter | 14px | 500 |
| Table cell | Inter | 13px | 400 |
| Table header | Inter | 11px | 600 (uppercase, .06em, `--ink-55`) |
| Footnote | Inter | 12px | 400 (color `--ink-55`) |

### Rules

- Serif for hierarchy. Sans for UI. Mono for figures.
- All caps reserved for short labels and table headers.
- Line-height 1.55–1.65 on body (longer reading).

---

## Spacing

Base unit: 4px. Scale: `4 8 12 16 20 24 32 40 48 64 80`.

| Context | Value |
|---------|-------|
| Section padding | 56px 40px |
| Card padding | 24px |
| KPI card padding | 20px |
| Sidebar width | 280px |
| Topbar height | 60px |
| Reading column max | 720px |

---

## Radii

| Token | Value | Use |
|-------|-------|-----|
| `--radius` | 8px | Cards, modal, container |
| `--radius-sm` | 4px | Inner blocks, badges |
| pill | 100px | Buttons only |

Conservative radii. No pill chips. Documents feel structured.

---

## Components

### Buttons

```css
.btn-primary {
  background: var(--accent);
  color: #fff;
  font: 600 14px var(--font-body);
  padding: 10px 20px;
  border-radius: 100px;
  border: none;
}
.btn-primary:hover { background: var(--accent-deep); }

.btn-secondary {
  background: var(--surface);
  color: var(--accent);
  border: 1px solid var(--accent);
  padding: 9px 19px;
  border-radius: 100px;
}
```

### Cards

```css
.card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 24px;
  transition: box-shadow .18s ease;
}
.card:hover { box-shadow: 0 4px 16px rgba(15,30,53,.06); }
```

### KPI card

White, thin border, mono digit in `--accent`. Label below in small caps. No hover scale — clinical sobriety.

### Badges

Square-ish (`--radius-sm`). 11px 600. 3px 8px padding. Semantic backgrounds with matching foreground color from semantic pair.

### Pull quote / callout

```css
.callout {
  background: var(--accent-bg);
  border-left: 4px solid var(--accent);
  padding: 16px 20px;
  border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
  font: 400 15px var(--font-body);
  color: var(--accent-deep);
}
```

### Section eyebrow

Mono, uppercase, accent color, `.1em` tracking. Section title below in serif 28px.

### Sidebar active state

Left-border accent stripe (3px solid `--accent`), text `--accent`, weight 600, **no** background change. Subtle.

### Tables

```css
.table-wrap { border: 1px solid var(--border); border-radius: var(--radius); }
thead th {
  background: var(--surface-2);
  text-transform: uppercase;
  font: 600 11px var(--font-body);
  letter-spacing: .06em;
  color: var(--ink-55);
  padding: 12px 16px;
  border-bottom: 2px solid var(--accent);
}
tbody td {
  padding: 11px 16px;
  border-bottom: 1px solid var(--border);
  font-size: 13px;
}
tbody tr:hover { background: var(--surface-2); }
```

### Modal

Right slide-in. Header has `border-bottom: 2px solid var(--accent)`. Body breathes (32px padding). Field labels in mono uppercase 11px.

### Charts (Chart.js overrides)

- Primary: `--accent`
- Secondary: `--ok`
- Tertiary: `--warn`
- Quaternary: `--danger`
- Gridlines: `var(--border)`
- Ticks: `--ink-55`, Inter 11px
- Tooltip bg: `--surface`, border `--border`, ink `--ink`

### Footnote / source line

Below tables and charts. Inter 12px italic, color `--ink-55`. Prefixed by `Fonte:` or `Source:`.

---

## Motion

| Element | Transition |
|---------|-----------|
| All interactive | `.2s ease` |
| Card hover | shadow only — no transform |
| Section entrance | fade only (no slide), 400ms ease |
| Modal | 250ms ease translateX |
| Chart draw | 1000ms easeOutQuart |

Rules:
- No translateY hover. No scale. Stillness reads as authority.
- Easing strictly `ease` or `ease-out`. No cubic-bezier.
- Reduce-motion disables fade entrance entirely.

---

## Iconography

Phosphor Icons Bold weight. 16/20px. Color `--ink-55` default, `--accent` active. Single-stroke geometric.

---

## Layout

| Breakpoint | Behavior |
|-----------|----------|
| ≥1280px | Sidebar 280px + content 1100px max + optional right rail 240px |
| 768–1279px | Sidebar visible, no right rail |
| <768px | Sidebar off-canvas. Single column. |

- Content max-width 1100px, centered.
- Reading prose max-width 720px (long-form sections).
- Strict 12-col grid for tables and KPI rows.

**Responsive rule:** All heading, KPI-digit, and hero font sizes use `clamp()` with mobile-floor and desktop-ceiling. Card padding reduces ~30% below 768px. Design tokens (colors, radii, fonts) do not change across breakpoints — only layout and spacing adapt.

---

## Print

Clinical-blue is print-first. Print rules:

```css
@media print {
  #sidebar, #sidebar-toggle, #topbar .topbar-actions, #detail-modal { display: none; }
  body { background: #fff; color: #000; }
  section { break-inside: avoid; padding: 24px 0; border: none; }
  .card, .table-wrap { box-shadow: none; border: 1px solid #ccc; }
  .chart-container { border: 1px solid #ccc; }
}
```

Every page footer prints with page number and source line.

---

## Principles

| Principle | Rule |
|-----------|------|
| Document-first | Reads like a report, not an app. |
| Serif hierarchy | Section titles in serif. Authority. |
| Restraint | One accent. No gradients. No decorative shadows. |
| Conservative motion | Stillness. Fade only. No transform on hover. |
| Print-ready | Every component prints clean. |
| Sourceable | Footnotes under tables/charts. Always cite. |
