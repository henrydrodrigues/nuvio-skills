---
name: md2html-cognitive
description: >
  Transform markdown source file into single self-contained interactive HTML
  page with embedded CSS and JS. Output is NOT a transcription — it is a
  re-organization of source content into an interactive experience: cards,
  charts, Gantt timelines, hierarchical trees, tags and filters, left index
  sidebar, right detail panel, flow diagrams, sortable tables, search,
  collapsible sections, theme toggle, scroll-spy navigation. Use whenever
  user wants to turn markdown (plan, report, spec, dossier, brief, study,
  proposal, documentation) into navigable HTML. Triggers: "transforme em
  html", "interactive html from markdown", "renderiza esse md", "make a
  dashboard from this doc", "single-file html", "html navegável", any
  request to produce a one-file html artifact from markdown source. Design
  is driven by selectable style sheet: pick one of bundled design-style-*.md
  files or accept user-provided override.
---

# md2html-cognitive

Convert markdown to single-file interactive HTML. Reorganize content. Do not transcribe.

## When to Use

| Trigger | Action |
|---------|--------|
| User supplies markdown + asks for HTML | Run full pipeline. |
| User says "interactive" / "dashboard" / "navegável" / "single page" | Run full pipeline. |
| User wants static rendering of markdown | Stop. Use plain pandoc instead. Not this skill. |
| User wants multi-page site | Stop. Not this skill. |

## Core Principle

Source markdown = data. HTML = experience. Read source. Extract structured data. Pick best visual primitive per data shape. Build interactive page.

Never paste markdown paragraphs into HTML body unchanged. Always restructure.

## Pipeline

1. Read source markdown.
2. Pick design style — see Design Style section.
3. Extract data — see Content Extraction section.
4. Pick widgets per data shape — see Widget Selection table.
5. Build single HTML file — see Build Rules section.
6. Run audit — see Audit table.
7. Save to `/mnt/user-data/outputs/[slug].html`. Present file.

---

## Design Style

Five bundled styles ship with this skill:

| Slug | Mood | Best for |
|------|------|----------|
| `editorial-warm` | Magazine, warm cream, serif headings | Reports, essays, brand docs, proposals |
| `dark-terminal` | GitHub-dark, mono accents, amber highlight | Project plans, technical specs, dashboards |
| `clinical-blue` | Crisp white, blue accent, medical/finance feel | Audits, compliance, healthcare, financial reports |
| `brutalist-mono` | High contrast, black/white, oversized type | Manifestos, pitches, single-idea statements |
| `pastel-soft` | Muted pastels, rounded everything, friendly | Onboarding guides, education, internal handbooks |

Each style is a markdown file at `design-style-[slug].md` next to this SKILL. Read the chosen style file before writing CSS. It declares: color tokens, typography, spacing, radii, motion, component rules.

### How to pick a style

| Source signals | Pick |
|---------------|------|
| Technical/dev/data-heavy | `dark-terminal` |
| Business report, proposal, brand | `editorial-warm` |
| Compliance, health, finance, audit | `clinical-blue` |
| Manifesto, pitch deck, opinion | `brutalist-mono` |
| Tutorial, guide, education | `pastel-soft` |

If user provides own `design-style-[slug].md` file, use that — override bundled choice.

If unclear, ask user once with three suggestions. Do not ask more than once.

---

## Content Extraction

Read full markdown. Detect source language first — infer from prose, headings, or `lang` frontmatter. Apply semantic detection by **structure and data shape**, never by fixed keywords. The examples in the Detection cue column are illustrative only; reason about meaning, not string matching.

| Shape | Detection cue (structural — language-agnostic) | Widget |
|-------|------------------------------------------------|--------|
| Headings hierarchy | `#`, `##`, `###` | Left sidebar nav + scroll-spy + section anchors |
| Top-level summary | First section or section whose heading signals overview / introduction intent | Hero block + KPI row |
| Key numbers | **Bold** values, percentages, currency symbols, numeric quantities with units | KPI cards (mono digits) |
| Bullet lists ≤8 items | `- ` or `* ` short items | Highlight list with accent bullet |
| Bullet lists >8 items | Long flat lists | Sortable/filterable card grid |
| Tables | Markdown `|` tables | Sortable HTML tables + filter bar if has category column |
| Tables with date/period range | Columns containing months, weeks, dates, or numeric period ranges (e.g. `1–3`, `Jan`, `Q2`) | Gantt chart (Chart.js horizontal bar) |
| Tables with status column | Column whose values are a small fixed set of states (e.g. done/pending, open/closed, active/inactive, pass/fail) | Color-coded badges + status filter |
| Tables with category + percentage | Column of named categories + column of `%` or share values | Doughnut chart + table |
| Tables with cumulative numbers | Column that monotonically increases (running total, cumulative spend, S-curve data) | S-curve / line chart |
| Tables with two numeric score columns | Two numeric columns both ≤5 or ≤10 scale, often multiplied together (probability × impact, power × interest) | Bubble / heatmap scatter |
| Hierarchical lists | Nested `- ` bullets 2+ levels deep | Expand/collapse tree |
| Process flows | Numbered or sequenced items (Step N, Phase N, ordered list) or prose with directional arrows `→ ` | Flow diagram (numbered blocks + connectors) |
| Comparative options | Section or table with 2–5 parallel alternatives (each covering same attributes) | Tab panels + comparison chart |
| Checklist / action items | `- [ ]` / `- [x]` syntax, or section whose heading signals tasks, actions, or next steps | Interactive checklist with localStorage |
| Glossary / definitions | Pattern of `**term**` followed by definition, or table with Term / Definition columns | Searchable definition list |
| Risks / threats | Table or list with likelihood + impact columns (numeric or qualitative), or heading signals risk | Heatmap + filterable risk register |
| RACI / responsibility matrix | Table with columns `R`, `A`, `C`, `I` or equivalent responsibility role headers, mapped to tasks | RACI table with role badges |
| Long prose | Sections consisting mainly of paragraphs without lists or tables | Compact reading card with pull-quotes |
| Quotes | `> ` blockquotes | Pull-quote callout block |
| Code blocks | ` ``` ` fenced blocks | Syntax-highlighted code card with copy button |
| Images | `![alt](url)` | Lazy-loaded figure with caption |
| Links | `[text](url)` | Inline accent link with external icon |

---

## Widget Selection

Pick at least one feature-rich widget per major section. Avoid 3+ identical widgets in a row — vary the visual rhythm.

### Required UI shell (every output has these)

| Element | Purpose |
|---------|---------|
| Left sidebar | Section index, scroll-spy active state, reading progress bar |
| Topbar (sticky on scroll) | Title, status badge, theme toggle, print button |
| Section blocks | Numbered `01`, `02`, ... eyebrow + title + subtitle |
| Right detail panel (modal slide-in) | Click any data row → open detail panel with full info |
| Footer | Brand line, meta info, generation date |
| Theme toggle | Light/dark, persisted to localStorage |
| Mobile sidebar | Off-canvas with hamburger toggle |

### Conditional widgets (only if data shape matches)

| Widget | Trigger | Lib |
|--------|---------|-----|
| Gantt | Date/month range table | Chart.js horizontal bar |
| Doughnut | Category percentages | Chart.js doughnut |
| S-curve | Cumulative monthly | Chart.js line |
| Bubble heatmap | 2D score grid (risks, stakeholders) | Chart.js scatter |
| Stacked bar | Multi-series comparison | Chart.js bar |
| Tree (expand/collapse) | Nested bullets, WBS | Pure DOM |
| Tab panels | Scenarios, options | Pure DOM |
| Filter bar | Tables with category column | Pure DOM |
| Sortable table | Any data table | Pure DOM `data-col` |
| Checklist | "Next steps" or `- [ ]` | Pure DOM + localStorage |
| Flow diagram | Process / pipeline | Inline SVG, numbered nodes + arrows |
| Pull quote | `> ` block | Styled aside |
| KPI row | Top numbers | Grid of cards |
| Search input | If >30 items in any table/list | Pure DOM filter on keystroke |
| Tag chips | Tags / categories in frontmatter or inline `#tag` | Pill chips, click to filter |
| Code copy | Fenced code | Button + clipboard API |
| Remotion animation embed | Source has "animation" or motion concept | Iframe to remotion bundle — only if explicitly requested |

---

## Build Rules

| Rule | Why |
|------|-----|
| Single `.html` file. CSS in `<style>`. JS in `<script>`. No external files except CDN. | Self-contained artifact. |
| Use Chart.js 4 from cdn.jsdelivr.net for charts. | Stable CDN. |
| Use Google Fonts CDN for typography declared in style sheet. | Required by style. |
| All data lives in JS const objects at top of `<script>`. Builders render from these. | Single source of truth. Easy to edit. |
| Every interactive element has hover state, focus state, ARIA label where needed. | Accessibility. |
| Sections visible by default; JS adds `.js-ready` to `<html>`, then hides and reveals with `IntersectionObserver` fade-up. 2s timeout fallback forces all visible if IO never fires. | Progressive enhancement — content always visible on iOS Files viewer, restrictive WebViews, or no-JS. |
| Theme variables in `:root` and `[data-theme="light"]` (or reverse). | Style sheet defines which is primary. |
| Sidebar scroll-spy updates active nav item via `IntersectionObserver`. | Standard pattern. |
| Detail modal slides in from right, backdrop blur, ESC closes. | Standard pattern. |
| Print stylesheet hides sidebar, topbar actions, modal. | Printable output. |
| Three responsive breakpoints: 1024px (tablet — reduce padding/spacing), 768px (mobile — sidebar off-canvas, vertical flow diagrams, single-col cards, horizontal-scroll tabs, full-width modal), 480px (small phone — single-col KPI, compact topbar, minimal indent). Use `clamp()` for fluid font sizes. | Responsive. |
| Reduced-motion media query disables fade-ups and chart animations. | Accessibility. |
| No `localStorage` access without `try/catch`. | Privacy modes break it otherwise. |
| Every Chart.js chart must set `maintainAspectRatio: true` and an explicit `aspectRatio` (doughnut 1.2, bar/scurve 1.6, bubble/risk 1.1, gantt `max(1.2, tasks*0.35)`). Never set `height` on `<canvas>`. | Charts must fit on screen without scrolling. |
| Chart containers use type-specific `max-width` via modifier class (doughnut 320px, bar 520px, scurve 560px, bubble/risk 460px, gantt full-width). See `html-conventions.md` Section 4. | Prevents charts from blowing up on wide screens. |

### CSS variable contract

Every style sheet declares at minimum these tokens. Use these names exactly:

```
--bg          base background
--surface     card / panel background
--surface-2   nested surface, table header bg
--border      hairline divider
--ink         primary text
--ink-55      secondary text (~55% opacity)
--ink-20      tertiary text / icon
--accent      brand color, sole accent
--accent-2    accent variant (hover, light bg)
--ok          success / green
--warn        warning / amber
--danger      error / red
--info        info / blue
--radius      base radius for cards
--radius-sm   inner radius for chips, badges
--font-display font family for headings
--font-body    font family for UI/body
--font-mono    monospace family for numbers/code
--transition   default easing duration
```

Style files override values but never rename tokens. Builder JS references these only.

---

## Output Skeleton

Page structure — always emit this scaffold, populate based on extracted data:

```html
<!DOCTYPE html>
<html lang="[detect from source]" data-theme="[default per style]">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[doc title]</title>
  <link href="[Google Fonts URL per style]" rel="stylesheet">
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4/dist/chart.umd.min.js"></script>
  <style>
    /* :root tokens from chosen style file */
    /* [data-theme="..."] overrides */
    /* reset + base */
    /* layout (sidebar, topbar, content) */
    /* components (cards, tables, badges, modal, charts, tree, tabs, filters) */
    /* responsive (1024px, 768px, 480px) */
    /* print */
    /* prefers-reduced-motion */
  </style>
</head>
<body>
  <aside id="sidebar">...</aside>
  <button id="sidebar-toggle">☰</button>
  <main id="content">
    <header id="topbar">...</header>
    <section id="s-[slug]">...</section>
    <!-- one section per top-level heading in source -->
    <footer id="footer">...</footer>
  </main>
  <div id="detail-modal">...</div>
  <script>
    const DATA_[SECTION] = [...]; // one const per data shape, JSON inlined
    /* builders: buildNav, buildKPIs, buildSection_X, ... */
    /* utilities: el, $, fmt, openModal, closeModal */
    /* init: DOMContentLoaded → call every builder → revealSections → initScrollSpy */
  </script>
</body>
</html>
```

---

## Audit

Run before saving output. Every check must pass.

| Check | Pass condition |
|-------|---------------|
| Single file | Output is one `.html`, no companion files. |
| Self-contained | Only allowed external refs: Google Fonts CDN, Chart.js CDN. No other assets. |
| Sidebar present | Left index with one entry per top-level section, scroll-spy active state works. |
| Detail panel present | At least one widget triggers right modal on click. |
| Theme toggle works | Clicking flips `data-theme`, persists to localStorage. |
| Source coverage | Every top-level heading in source has a section in HTML. |
| No raw markdown dump | No section is a plain prose copy of source paragraphs without restructure. |
| Widget variety | At least 3 distinct widget types used in total (KPI + table + chart minimum). |
| Charts render | If Chart.js used, every `<canvas>` has matching builder call in init. |
| Responsive | Page works at 375px, 768px, 1440px without horizontal scroll except inside `.table-wrap`. |
| Print works | Print preview hides sidebar, topbar buttons, modal. |
| Style tokens applied | No hardcoded hex outside `:root`. All color refs use `var(--...)`. |
| Reduced motion respected | `@media (prefers-reduced-motion: reduce)` disables animations. |
| Title set | `<title>` and topbar title match source H1. |
| Footer meta | Footer includes generation date and source slug. |

---

## Edge Cases

| Case | Handling |
|------|----------|
| Source has no tables | Skip Gantt, doughnut, S-curve. Lean on cards, lists, pull-quotes, KPIs. |
| Source has only one section | Skip sidebar — collapse to single-page layout with topbar nav anchors. |
| Source has 20+ sections | Group sidebar nav by H1 with collapsible H2 sub-items. |
| Source has math / formulas | Add KaTeX CDN. Render `$...$` and `$$...$$`. |
| Source has Mermaid blocks | Add Mermaid CDN. Render fenced ` ```mermaid ` blocks. |
| Source is huge (>5000 lines) | Chunk by H1. Lazy-render sections via IntersectionObserver. |
| Source has frontmatter (YAML) | Parse for title, author, date, tags. Use in topbar + footer. |
| Detect source language | Infer from prose. Set `<html lang="[code]">` accordingly. All generated UI labels (buttons, placeholders, tooltips) use same language as source. |

---

## Bundled References

| File | Purpose |
|------|---------|
| `design-style-editorial-warm.md` | Warm magazine style |
| `design-style-dark-terminal.md` | Dark technical style |
| `design-style-clinical-blue.md` | Clinical/finance light style |
| `design-style-brutalist-mono.md` | High-contrast manifesto style |
| `design-style-pastel-soft.md` | Soft education/onboarding style |

## Related Skills

| Skill | Use when |
|-------|----------|
| `frontend-design` | Need deeper visual-design judgment beyond bundled styles. |
| `remotion-best-practices` | Source requests motion / animated diagrams. |
| `caveman-writing` | Compressing this skill or related agent-facing docs. |
