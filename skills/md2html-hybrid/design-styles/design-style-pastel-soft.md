# Design Style — pastel-soft

Muted pastels, rounded everything, friendly typography, breathable layout. For tutorials, onboarding guides, education materials, internal handbooks, knowledge bases.

Default theme: **light**.

---

## Color Tokens

### `:root` (light, primary)

| Token | Value |
|-------|-------|
| `--bg` | `#fbfaff` |
| `--surface` | `#ffffff` |
| `--surface-2` | `#f4f1fc` |
| `--border` | `#ece6f5` |
| `--ink` | `#2b2540` |
| `--ink-55` | `#6e6582` |
| `--ink-20` | `#cfc6dc` |
| `--accent` | `#7c5ce8` |
| `--accent-2` | `#a695f0` |
| `--accent-bg` | `#ece6fc` |
| `--accent-deep` | `#4a32a8` |
| `--ok` | `#3ea674` |
| `--ok-bg` | `#dff2e8` |
| `--warn` | `#d49431` |
| `--warn-bg` | `#fcefd2` |
| `--danger` | `#d8607a` |
| `--danger-bg` | `#fbe2ea` |
| `--info` | `#4f8fd6` |
| `--info-bg` | `#dfecfa` |
| `--pink` | `#f3a8c7` |
| `--mint` | `#a8e5cf` |
| `--peach` | `#f5c9a0` |

### `[data-theme="dark"]` overrides

| Token | Value |
|-------|-------|
| `--bg` | `#1a1726` |
| `--surface` | `#262238` |
| `--surface-2` | `#312c46` |
| `--border` | `#3a3450` |
| `--ink` | `#f0ecfb` |
| `--ink-55` | `#a097b8` |
| `--ink-20` | `#4d4566` |

### Rules

| Rule | Why |
|------|-----|
| All semantic colors are desaturated and muted. | Friendly, not aggressive. |
| Extra palette `--pink`, `--mint`, `--peach` available for category coloring. | Educational categorization. |
| Backgrounds tinted toward `--accent` hue. | Cohesive warmth. |

---

## Typography

### Families

| Role | Family | Weights |
|------|--------|---------|
| Display | Fraunces | 400, 500, 600, 700 |
| Body / UI | Nunito | 300, 400, 600, 700, 800 |
| Mono / numbers | JetBrains Mono | 400, 500 |

### Google Fonts URL

```
https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600;9..144,700&family=Nunito:wght@300;400;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap
```

### Scale

| Role | Family | Size | Weight |
|------|--------|------|--------|
| Hero | Fraunces | `clamp(40px, 5vw, 64px)` | 600 (opsz 144) |
| Section title | Fraunces | 32px | 600 |
| Subsection | Nunito | 20px | 700 |
| Body | Nunito | 16px | 400 |
| Body strong | Nunito | 16px | 700 |
| KPI digit | Fraunces | 36px | 700 (color `--accent`) |
| KPI label | Nunito | 12px | 600 (color `--ink-55`) |
| Eyebrow / section num | Nunito | 12px | 700 (color `--accent`, .06em) |
| Nav link | Nunito | 14px | 600 |
| Table cell | Nunito | 14px | 400 |
| Table header | Nunito | 12px | 700 (color `--ink-55`) |
| Tip / hint | Nunito | 13px | 400 italic |

### Rules

- Fraunces for personality (titles, hero, KPI digits — display optical size).
- Nunito everywhere else — rounded sans for warmth.
- No uppercase except table headers and eyebrows.
- Generous line-height: 1.65 body, 1.25 titles.

---

## Spacing

Base unit: 4px. Scale: `4 8 12 16 20 24 32 40 48 64 80 96`.

| Context | Value |
|---------|-------|
| Section padding | 64px 40px |
| Card padding | 28px |
| KPI card padding | 24px |
| Sidebar width | 280px |
| Topbar height | 60px |
| Reading column max | 720px |

Breathing room is a feature.

---

## Radii

| Token | Value | Use |
|-------|-------|-----|
| `--radius` | 20px | Cards, modal, containers |
| `--radius-sm` | 12px | Inner blocks, table wrap, buttons |
| `--radius-xs` | 8px | Inputs, mini chips |
| pill | 100px | Badges, tags, filter buttons |

**Round everything.** Even table cells get soft outer radius.

---

## Components

### Buttons

```css
.btn-primary {
  background: var(--accent);
  color: #fff;
  font: 700 14px var(--font-body);
  padding: 12px 24px;
  border-radius: var(--radius-sm);
  border: none;
  box-shadow: 0 4px 0 var(--accent-deep);
  transition: transform .15s ease, box-shadow .15s ease;
}
.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 0 var(--accent-deep);
}
.btn-primary:active {
  transform: translateY(2px);
  box-shadow: 0 2px 0 var(--accent-deep);
}
```

Drop-shadow button — playful skeuomorphic press.

```css
.btn-ghost {
  background: var(--accent-bg);
  color: var(--accent-deep);
  border: none;
  padding: 12px 22px;
  border-radius: var(--radius-sm);
}
```

### Cards

```css
.card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 28px;
  transition: transform .2s ease, box-shadow .2s ease;
}
.card:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 32px rgba(124,92,232,.12);
}
```

### KPI card

White surface. Display-font digit in `--accent`. Label in `--ink-55`. Optional emoji icon top-left (📈 ⏱ 🎯). Soft hover lift.

### Badges

Pill shape. Nunito 700 11px. Semantic bg + text pair. Optional emoji prefix.

```css
.tag-mint { background: var(--mint); color: #1d6045; }
.tag-pink { background: var(--pink); color: #8a2950; }
.tag-peach { background: var(--peach); color: #8a4a16; }
```

### Tip / callout

```css
.tip {
  background: var(--accent-bg);
  border-left: 4px solid var(--accent);
  padding: 16px 20px;
  border-radius: var(--radius-sm);
  font-size: 14px;
  color: var(--accent-deep);
}
.tip::before {
  content: "💡 ";
  font-size: 16px;
}
```

Variants: `.tip-warn` (warm bg, ⚠️), `.tip-ok` (mint bg, ✅), `.tip-danger` (rose bg, ⛔).

### Section eyebrow

`Nunito 700 12px .06em uppercase` in `--accent`. Title below in Fraunces 32px.

### Sidebar active state

`--accent-bg` background, `--accent-deep` text, no border stripe — instead, animated dot indicator left of text. Pill-shaped active item.

### Tables

```css
.table-wrap { border-radius: var(--radius); border: 1px solid var(--border); overflow: hidden; }
thead th {
  background: var(--surface-2);
  color: var(--ink-55);
  font: 700 12px var(--font-body);
  padding: 14px 16px;
  text-align: left;
}
tbody td { padding: 12px 16px; border-bottom: 1px solid var(--border); }
tbody tr:hover { background: var(--surface-2); cursor: pointer; }
tbody tr:last-child td { border-bottom: none; }
```

### Modal

Right slide-in. `--radius` on top-left and bottom-left corners. Soft backdrop `rgba(43,37,64,.4)` + blur(8px). Spring entrance feel via easing (still no actual spring per reduce-motion).

### Progress bar

```css
.progress-bar {
  height: 8px;
  background: var(--surface-2);
  border-radius: 100px;
  overflow: hidden;
}
.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--accent), var(--accent-2));
  border-radius: 100px;
}
```

**Only place gradients are allowed:** progress fills. Educational signal of completion.

### Checklist item

Rounded checkbox (border-radius 6px), animated check stroke draw on toggle (200ms). Done state: strikethrough text + checkbox fills `--ok` with white checkmark.

### Charts (Chart.js overrides)

- Multi-series uses extra palette: `--accent`, `--mint`, `--peach`, `--pink`, `--info`
- Bars: 8px border-radius
- Lines: 3px stroke, smooth tension 0.4
- Points: 5px radius circles
- Gridlines: `var(--border)` dashed
- Ticks: `--ink-55` Nunito 11px
- Tooltip bg: `--surface`, `--radius-sm`, border `--accent`

---

## Motion

| Element | Transition |
|---------|-----------|
| All interactive | `.2s ease-out` |
| Card hover | translateY + soft shadow grow |
| Button hover | translateY -2px + shadow grow |
| Section entrance | fade-up 20px → 0, 600ms ease-out, 100ms stagger |
| Modal | 350ms ease-out translateX |
| Progress fill | 800ms ease-out width |
| Checkbox check | 200ms ease-out stroke-dashoffset |

Rules:
- Ease-out everywhere — feels welcoming.
- Animation present but never aggressive.
- Reduce-motion disables fade-up + check-stroke. Buttons keep press feedback.

---

## Iconography

Phosphor Icons Regular or Duotone. 20/24px. Color `--accent` or `--ink`.

Or: emoji liberally for personality (💡 ⭐ 🎯 ⏱ 🚀 ✅ ⚠️ 📝). Especially in tips, KPI labels, section eyebrows.

---

## Layout

| Breakpoint | Behavior |
|-----------|----------|
| ≥1280px | Sidebar 280px + content max 1100px |
| 768–1279px | Sidebar visible, grids collapse to 2 cols |
| <768px | Sidebar off-canvas. KPI 2 cols. Card padding 20px. |

- Reading column max-width 720px for long-form sections.
- Generous section spacing (64px+).
- Grid gap 20–24px.

**Responsive rule:** All heading, KPI-digit, and hero font sizes use `clamp()` with mobile-floor and desktop-ceiling. Card padding reduces ~30% below 768px. Design tokens (colors, radii, fonts) do not change across breakpoints — only layout and spacing adapt.

---

## Illustrations

Pastel-soft is the only style where light illustrations are encouraged:
- Empty states
- First-run / onboarding
- Section openers (optional, decorative)

Style: flat, single-weight strokes, palette uses `--mint`, `--pink`, `--peach`, `--accent-2`. No drop shadows. No gradients except progress bars.

---

## Principles

| Principle | Rule |
|-----------|------|
| Friendly | Rounded everything. Soft colors. Warm typography. |
| Approachable | Emoji + plain language allowed. |
| Breathable | Generous padding. Long line-height. |
| Encouraging | Press-feedback buttons. Progress bars. Check-stroke animation. |
| Playful restraint | Pastels stay muted. Never neon. |
