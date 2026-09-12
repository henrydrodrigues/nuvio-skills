# Design Style — editorial-warm

Magazine-feel, warm cream surfaces, serif display headings, single orange accent. For reports, proposals, brand-forward documents.

Default theme: **light**.

---

## Color Tokens

### `:root` (light, primary)

| Token | Value |
|-------|-------|
| `--bg` | `#faf7f2` |
| `--surface` | `#ffffff` |
| `--surface-2` | `#f4f0e8` |
| `--border` | `rgba(30,26,20,.16)` |
| `--ink` | `#1e1a14` |
| `--ink-55` | `rgba(30,26,20,.55)` |
| `--ink-20` | `rgba(30,26,20,.16)` |
| `--accent` | `#c45c1a` |
| `--accent-2` | `#fdecd8` |
| `--accent-deep` | `#8c3a08` |
| `--ok` | `#0d7a6e` |
| `--ok-bg` | `#d1f0eb` |
| `--warn` | `#b06a0f` |
| `--warn-bg` | `#fdf0dc` |
| `--danger` | `#a8304c` |
| `--danger-bg` | `#fce8ed` |
| `--info` | `#1f5d99` |
| `--info-bg` | `#dce8f4` |

### `[data-theme="dark"]` overrides

| Token | Value |
|-------|-------|
| `--bg` | `#1e1a14` |
| `--surface` | `#2a2520` |
| `--surface-2` | `#332e28` |
| `--border` | `rgba(244,240,232,.14)` |
| `--ink` | `#f4f0e8` |
| `--ink-55` | `rgba(244,240,232,.55)` |
| `--ink-20` | `rgba(244,240,232,.14)` |

### Rules

| Rule | Why |
|------|-----|
| No pure `#000` or `#fff` for text/bg. | Use `--ink` and `--bg`. |
| `--bg` is warm off-white. Never cool gray. | Warmth is the brand. |
| `--accent` is sole accent. CTAs, active nav, KPI digits, brand mark only. | Restraint reads as quality. |

---

## Typography

### Families

| Role | Family | Weights |
|------|--------|---------|
| Display | Playfair Display | 400, 500, 400i, 500i |
| Body / UI | DM Sans | 300, 400, 500, 600, 700 |
| Mono / numbers | JetBrains Mono | 400, 500 |

### Google Fonts URL

```
https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,500;1,400;1,500&family=DM+Sans:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap
```

### Scale

| Role | Family | Size | Weight | Tracking |
|------|--------|------|--------|----------|
| Hero | Playfair | `clamp(36px,4.8vw,58px)` | 500 | -0.02em |
| Section title | Playfair | 34px | 500 | -0.02em |
| Subsection | Playfair | 24px | 400 | -0.02em |
| Pull quote | Playfair italic | 18px | 400 | default |
| Body | DM Sans | 16px | 300 | default |
| Body strong | DM Sans | 16px | 500 | default |
| Eyebrow / label | DM Sans | 12px | 600 | 0.08em uppercase |
| Nav link | DM Sans | 14px | 500 | default |
| Button | DM Sans | 14px | 600 | default |
| KPI digit | JetBrains Mono | 32px | 500 | default |
| Table | DM Sans | 13px | 400 | default |

### Rules

- Playfair for headings + pull-quotes only. Never body or labels.
- Playfair italic reserved for emphasis word in hero / one key term per section.
- DM Sans 300 for body. 500–600 for interactive.
- Mono for numbers, codes, timestamps. Never prose.

---

## Spacing

Base unit: 4px. Scale: `4 8 12 16 20 24 32 40 48 64 80`.

| Context | Value |
|---------|-------|
| Section vertical padding | 64px top/bottom, 32px sides |
| Card padding | 24px |
| KPI card padding | 18px 20px |
| Inline gap (chips, badges) | 6px |
| Grid gap | 20px |
| Sidebar width | 260px |

---

## Radii

| Token | Value | Use |
|-------|-------|-----|
| `--radius` | 16px | Cards, modal, large containers |
| `--radius-sm` | 10px | Inner blocks, code, table wrap |
| pill | 100px | Buttons, badges, tags |
| micro | 6px | Inputs, mini chips |

---

## Components

### Buttons

```css
.btn-primary {
  background: var(--accent);
  color: #fff;
  font: 600 14px var(--font-body);
  padding: 12px 24px;
  border-radius: 100px;
  border: none;
  transition: opacity .18s ease;
}
.btn-primary:hover { opacity: .88; }

.btn-ghost {
  background: transparent;
  color: var(--ink-55);
  border: 1px solid var(--border);
  border-radius: 100px;
  padding: 10px 18px;
}
```

### Cards

```css
.card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 24px;
  transition: transform .18s ease, box-shadow .18s ease;
}
.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 28px rgba(30,26,20,.08);
}
```

### KPI card

White surface. Accent-colored digit. Mono font. Small label below in `--ink-55`.

### Badges / chips

Pill shape. DM Sans 600 11px. 3px 10px padding. Semantic backgrounds: `--accent-2`, `--ok-bg`, `--warn-bg`, `--danger-bg`, `--info-bg`.

### Pull quote / insight block

```css
.pull-quote {
  background: var(--accent-2);
  border: 1px solid rgba(196,92,26,.18);
  border-radius: var(--radius-sm);
  padding: 16px 20px;
  font: italic 18px var(--font-display);
  color: var(--accent-deep);
}
```

### Section eyebrow

```css
.section-num {
  font: 600 12px var(--font-body);
  letter-spacing: .08em;
  text-transform: uppercase;
  color: var(--accent);
}
```

### Sidebar active state

Left-border accent stripe (3px solid `--accent`), background `--surface-2`, text `--accent`.

### Tables

White surface inside `--radius-sm` wrap with `--border`. Header row: `--surface-2` background, 11px uppercase eyebrow. Row hover: `--surface-2`. Numeric cells use mono font.

### Charts

Chart.js default colors override:
- Primary series: `--accent`
- Secondary: `--ok`
- Tertiary: `--info`
- Quaternary: `--danger`
- Gridlines: `--border` at 60% opacity
- Tick labels: `--ink-55`, DM Sans 11px

---

## Motion

| Element | Transition |
|---------|-----------|
| All interactive | `all .18s ease` |
| Card hover | `translateY(-2px)` + soft shadow |
| Section entrance | fade-up 16px → 0 over 550ms, 120ms stagger |
| Modal slide-in | translateX from right, 300ms ease |
| Theme switch | instant (no transition on color) |

Rules:
- No bounce. No spring. Ease or linear only.
- Max entrance duration 600ms.
- Hover transitions 150–200ms max.
- Disable all entrance animations under `prefers-reduced-motion: reduce`.

---

## Iconography

Phosphor Icons (Regular weight) via SVG. 16/20/24px. Color `--ink` or `--accent`. Geometric, single weight, no serifs on strokes.

---

## Layout

| Breakpoint | Width |
|-----------|-------|
| mobile | <768px |
| tablet | 768–1199px |
| desktop | 1200px+ |

- Max content width: 1100px.
- Shell padding: 32px horizontal desktop, 16px mobile.
- Hero layout: asymmetric 2-column (3fr text + 2fr stat stack).
- KPI row: `repeat(auto-fit, minmax(160px, 1fr))`.
- Charts: 1fr / 1.6fr split where two charts share a row.

**Responsive rule:** All heading, KPI-digit, and hero font sizes use `clamp()` with mobile-floor and desktop-ceiling. Card padding reduces ~30% below 768px. Design tokens (colors, radii, fonts) do not change across breakpoints — only layout and spacing adapt.

---

## Principles

| Principle | Rule |
|-----------|------|
| Warm | `--bg` is `#faf7f2`. Never substitute cool gray. |
| Flat | No gradients, no drop shadows except subtle hover. No textures. |
| Restrained | `--accent` is the only accent fill — nowhere else. |
| Editorial | Headings are serif. Body is breathable. Lots of whitespace. |
| Print-ready | Every layout must print cleanly with sidebar hidden. |
