# Widget Patterns & Design Style Integration

Slim extract from `html-conventions.md` — contains only the sections the
cognitive agent needs to reason about. Static CSS/JS foundation is pre-compiled
into `html_foundation.html`.

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
