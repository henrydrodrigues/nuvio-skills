# Design Style — dark-terminal

GitHub-dark surfaces, amber accent, mono digits. For project plans, technical specs, engineering dashboards, dev-facing docs.

Default theme: **dark**.

---

## Color Tokens

### `:root` (dark, primary)

| Token | Value |
|-------|-------|
| `--bg` | `#0d1117` |
| `--surface` | `#161b22` |
| `--surface-2` | `#1c2128` |
| `--border` | `#21262d` |
| `--ink` | `#e6edf3` |
| `--ink-55` | `#8b949e` |
| `--ink-20` | `#30363d` |
| `--accent` | `#f0a500` |
| `--accent-2` | `#ffc947` |
| `--accent-bg` | `rgba(240,165,0,.12)` |
| `--ok` | `#3fb950` |
| `--ok-bg` | `rgba(63,185,80,.12)` |
| `--warn` | `#d29922` |
| `--warn-bg` | `rgba(210,153,34,.12)` |
| `--danger` | `#f85149` |
| `--danger-bg` | `rgba(248,81,73,.12)` |
| `--info` | `#388bfd` |
| `--info-bg` | `rgba(56,139,253,.12)` |
| `--purple` | `#8957e5` |

### `[data-theme="light"]` overrides

| Token | Value |
|-------|-------|
| `--bg` | `#f6f8fa` |
| `--surface` | `#ffffff` |
| `--surface-2` | `#f6f8fa` |
| `--border` | `#d0d7de` |
| `--ink` | `#1f2328` |
| `--ink-55` | `#636c76` |
| `--ink-20` | `#d0d7de` |

### Rules

| Rule | Why |
|------|-----|
| Amber `--accent` is sole brand accent. | Restraint reads as engineering quality. |
| Semantic colors fixed across themes. | Status meaning never shifts. |
| Borders are visible 1px lines. | Mimics terminal panel borders. |

---

## Typography

### Families

| Role | Family | Weights |
|------|--------|---------|
| Display + body | Space Grotesk | 400, 500, 600, 700 |
| Mono / numbers / code | DM Mono | 400, 500 |

### Google Fonts URL

```
https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=DM+Mono:wght@400;500&display=swap
```

### Scale

| Role | Family | Size | Weight |
|------|--------|------|--------|
| Hero / topbar title | Space Grotesk | `clamp(20px, 2.4vw, 28px)` | 700 |
| Section title | Space Grotesk | 22px | 700 |
| Section subtitle | Space Grotesk | 14px | 400 (color `--ink-55`) |
| Body | Space Grotesk | 14px | 400 |
| KPI digit | DM Mono | 28px | 700 (color `--accent`) |
| KPI label | Space Grotesk | 11px | 400 (color `--ink-55`) |
| Eyebrow / section num | DM Mono | 11px | 600 (color `--accent`, .08em tracking) |
| Nav link | Space Grotesk | 13px | 500 |
| Table cell | Space Grotesk | 13px | 400 |
| Table header | Space Grotesk | 11px | 600 (uppercase, .05em, color `--ink-55`) |
| Badge | Space Grotesk | 11px | 600 |
| Code | DM Mono | 13px | 400 |

### Rules

- Mono for: all numbers, IDs, codes, percentages, durations, dates.
- Sans for: headings, prose, labels, navigation.
- Section numbers `01`, `02` are mono.
- Never use mono for prose.

---

## Spacing

Base unit: 4px. Scale: `4 8 12 16 20 24 32 40 48`.

| Context | Value |
|---------|-------|
| Section padding | 40px 32px |
| Card padding | 20px |
| KPI card padding | 16px 18px |
| Sidebar width | 260px |
| Topbar height | ~52px |
| Grid gap (cards) | 16–20px |

---

## Radii

| Token | Value | Use |
|-------|-------|-----|
| `--radius` | 10px | Cards, modal, table wrap, chart container |
| `--radius-sm` | 6px | Buttons, inputs, inner blocks |
| pill | 20px | Badges, filter buttons |

---

## Components

### Cards

```css
.card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 20px;
}
.card:hover {
  box-shadow: 0 0 0 1px var(--accent), 0 4px 20px rgba(240,165,0,.1);
}
```

### KPI card

```css
.kpi-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 16px 18px;
}
.kpi-card:hover {
  transform: scale(1.03);
  box-shadow: 0 0 0 1px var(--accent), 0 6px 24px rgba(240,165,0,.15);
}
.kpi-val { font: 700 28px var(--font-mono); color: var(--accent); line-height: 1.1; }
.kpi-label { font-size: 11px; color: var(--ink-55); margin-top: 4px; }
```

### Sidebar active state

Left-border accent stripe (3px solid `--accent`), inner box-shadow `inset 3px 0 0 --accent`, background `--surface-2`, text `--accent`.

### Topbar

```css
#topbar {
  background: var(--surface);
  border-bottom: 2px solid var(--accent);
  backdrop-filter: blur(12px);
  position: sticky; top: 0;
}
```

Status badge in topbar uses `--info-bg` + `--info` color, pill shape.

### Badges

Pill shape, 11px 600, 2px 8px padding. Semantic backgrounds: `--accent-bg`, `--ok-bg`, `--warn-bg`, `--danger-bg`, `--info-bg`.

### Filter buttons

Default: `--surface` bg, `--border`, `--ink-55` color. Active: `--accent` border + text, `--accent-bg` fill. Semantic levels (Critical/Alto/Médio/Baixo) inherit their semantic color when active.

### Tables

```css
.table-wrap { border: 1px solid var(--border); border-radius: var(--radius); overflow-x: auto; }
thead th {
  background: var(--surface-2);
  text-transform: uppercase;
  font: 600 11px var(--font-body);
  letter-spacing: .05em;
  color: var(--ink-55);
  padding: 10px 14px;
  cursor: pointer;
}
tbody tr:hover { background: var(--surface-2); cursor: pointer; }
tbody td { padding: 9px 14px; border-bottom: 1px solid var(--border); }
tfoot td { background: var(--surface-2); color: var(--accent); font-weight: 700; border-top: 2px solid var(--accent); }
```

### Modal

Right-side slide-in panel. `--surface` bg with left border. Backdrop: `rgba(0,0,0,.7)` + `blur(4px)`. 300ms ease transform.

### Charts (Chart.js overrides)

- Primary fill: `--accent`
- Secondary: `--info`
- Tertiary: `--ok`
- Danger: `--danger`
- Gridlines: `rgba(33,38,45,.6)`
- Ticks: `--ink-55`, DM Mono 10px
- Tooltip bg: `var(--surface-2)`, border `var(--accent)`

### Progress ring

SVG circle `r=24`, `stroke-width=5`. Track: `--ink-20`. Fill: `--accent`. Rotated -90deg.

### Phase / progress bar

Multi-color stacked horizontal bar. Each phase block: 28px tall, white text 10px 600, hover brightens with `filter: brightness(1.2)`.

### Scrollbar

```css
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--ink-20); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--ink-55); }
```

---

## Motion

| Element | Transition |
|---------|-----------|
| All interactive | `.2s cubic-bezier(.4,0,.2,1)` |
| Section entrance | fade-up + scale, 500ms ease, staggered on scroll |
| Modal slide | 300ms ease translateX |
| Theme toggle | instant |
| Chart draw | 800ms easeOutQuart |
| Progress ring | 500ms ease stroke-dashoffset |

Rules:
- Snappy. Tech-feel. Cubic-bezier on all hovers.
- Reduce-motion disables fade-up + chart animation.

---

## Iconography

Inline SVG. 16px / 18px. Geometric, 1.5px stroke. Color `--ink-55` default, `--accent` active. Or emoji single-char `☰ 🌓 🖨` for utility buttons.

---

## Layout

| Breakpoint | Behavior |
|-----------|----------|
| ≥1200px | Sidebar 260px + content. 2-col grids active. |
| 768–1199px | Sidebar still visible. Grids collapse to 1-col. |
| <768px | Sidebar off-canvas. Hamburger top-left. KPI row 2 cols. |
| <480px | KPI row 1 col. Scenario tabs scroll horizontal. |

**Responsive rule:** All heading, KPI-digit, and hero font sizes use `clamp()` with mobile-floor and desktop-ceiling. Card padding reduces ~30% below 768px. Design tokens (colors, radii, fonts) do not change across breakpoints — only layout and spacing adapt.

---

## Principles

| Principle | Rule |
|-----------|------|
| Mono digits | Every number, ID, percent, duration, date uses `--font-mono`. |
| Amber accent | Single accent — CTAs, active states, KPI digits, topbar accent line. |
| Visible borders | 1px panels everywhere. No "floating" cards. |
| Dense | Compact spacing. Data-first. Whitespace earns its place. |
| Snappy | All transitions under 250ms. No bounce. |
