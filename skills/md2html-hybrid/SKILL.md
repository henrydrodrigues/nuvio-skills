---
name: md2html-hybrid
description: >
  Reference knowledge for the md2html-hybrid agent Stage 01 (cognitive). Covers
  widget vocabulary, per-widget data payload specs, document plan schema, content
  shape detection, and design style selection. Load this skill when Stage 01 needs
  to map markdown source to document-plan.json. Does not describe process steps —
  those live in the stage CONTEXT.md. For a fully cognitive single-stage alternative,
  see md2html-cognitive.
---

# md2html-hybrid — Reference

---

## Design Styles

| Slug | Best for | Default theme |
|------|----------|---------------|
| `editorial-warm` | Reports, proposals, brand docs | light |
| `dark-terminal` | Technical specs, dashboards, project plans | dark |
| `clinical-blue` | Compliance, finance, healthcare, audits | light |
| `brutalist-mono` | Manifestos, pitches, opinion pieces | light |
| `pastel-soft` | Tutorials, onboarding, education | light |

### Selection rules

| Source signals | Slug |
|---------------|------|
| Technical / data-heavy / dev-facing | `dark-terminal` |
| Business report, proposal, brand | `editorial-warm` |
| Compliance, health, finance, audit | `clinical-blue` |
| Manifesto, pitch, single bold idea | `brutalist-mono` |
| Tutorial, guide, education | `pastel-soft` |
| User specified slug or provided own style file | Use that. Override all rules. |

Each style file (`design-style-[slug].md`) declares all CSS token values. Read
the chosen style file and copy every token into `css_tokens` in the plan.

---

## CSS Variable Contract

Every style file declares exactly these tokens. Extract all of them.

```
--bg            base background
--surface       card / panel background
--surface-2     nested surface, table header bg
--border        hairline divider
--ink           primary text
--ink-55        secondary text
--ink-20        tertiary / icon
--accent        sole brand accent
--accent-2      accent variant
--ok            success / green
--warn          warning / amber
--danger        error / red
--info          info / blue
--radius        base card radius
--radius-sm     chip / badge radius
--font-display  display / heading family
--font-body     UI / body family
--font-mono     monospace family
--transition    default easing + duration
```

---

## Content Shape → Widget Slug

Detect by structure and semantics. Never by fixed keywords. Cues are illustrative.

| Shape | Detection cue | Slug |
|-------|--------------|------|
| Summary / overview section | First section or heading signals introduction intent | `kpi-summary` |
| Key numbers | Bold values, currency, percentages, quantities with units | `kpi-row` |
| Bullet list ≤ 8 items | Short flat `- ` or `* ` items | `highlight-list` |
| Bullet list > 8 items | Long flat list | `card-grid` |
| Plain table | `\|` table, no special columns | `sortable-table` |
| Table with date / period range | Columns with months, weeks, dates, numeric period ranges | `gantt` |
| Table with status column | Column values are small fixed set of states | `status-table` |
| Table with category + percentage | Named categories + `%` or share column | `doughnut` |
| Table with cumulative numbers | Column monotonically increases | `scurve` |
| Table with two numeric score columns | Two numeric columns ≤ 10 scale, often multiplied | `bubble-heatmap` |
| Multi-series comparison table | 3+ numeric value columns across named rows | `bar-chart` |
| Nested bullets 2+ levels | Indented `-` 2+ levels deep | `tree` |
| Numbered / sequenced process | Ordered list, step N, phase N, `→` arrows | `flow-diagram` |
| Parallel alternatives | 2–5 alternatives covering same attributes | `tabs` |
| Checklist / action items | `- [ ]` / `- [x]` or heading signals tasks / next steps | `checklist` |
| Glossary / definitions | `**term**` + definition, or Term/Definition columns | `definition-list` |
| Risk register | Table/list with likelihood + impact columns | `risk-heatmap` |
| RACI matrix | Columns R, A, C, I or equivalent role headers mapped to tasks | `raci-table` |
| Long prose | Paragraphs only, no lists or tables | `prose-card` |
| Blockquotes | `> ` blocks | `pull-quote` |
| Fenced code | ` ``` ` blocks | `code-block` |
| Images | `![alt](url)` | `figure` |
| No matching shape | Anything unclassified | `prose-card` |

One section may contain multiple shapes → multiple widgets. Order: KPIs first,
charts second, tables third, prose last.

---

## Widget Vocabulary

Closed set. Only emit slugs from this table.

| Slug | Lib | Required data keys |
|------|-----|--------------------|
| `kpi-summary` | DOM | `text`, `kpis[]` |
| `kpi-row` | DOM | `kpis[]` |
| `highlight-list` | DOM | `items[]` |
| `card-grid` | DOM | `cards[]` |
| `sortable-table` | DOM | `columns[]`, `rows[]` |
| `status-table` | DOM | `columns[]`, `rows[]`, `status_column`, `status_map` |
| `gantt` | Chart.js | `tasks[]`, `month_count`, `period_label` |
| `doughnut` | Chart.js | `segments[]`, `total_label` |
| `scurve` | Chart.js | `points[]` |
| `bubble-heatmap` | Chart.js | `points[]`, `x_label`, `y_label`, `x_max`, `y_max` |
| `bar-chart` | Chart.js | `series[]`, `categories[]` |
| `tree` | DOM | `nodes[]` |
| `flow-diagram` | SVG | `steps[]` |
| `tabs` | DOM | `tabs[]` |
| `checklist` | DOM | `groups[]` |
| `definition-list` | DOM | `entries[]` |
| `risk-heatmap` | Chart.js + DOM | `risks[]` |
| `raci-table` | DOM | `tasks[]`, `members[]`, `matrix{}` |
| `prose-card` | DOM | `paragraphs[]`, `quotes[]` |
| `pull-quote` | DOM | `text` |
| `code-block` | DOM | `lang`, `code` |
| `figure` | DOM | `src`, `alt` |

---

## Per-Widget Payload Spec

### `kpi-summary`
```
text:  string
kpis:  array of { label: string, value: string, mono: bool, semantic?: "ok"|"warn"|"danger"|"info" }
```

### `kpi-row`
```
kpis: array of { label: string, value: string, mono: bool, semantic?: "ok"|"warn"|"danger"|"info" }
```

### `highlight-list`
```
items: array of { text: string, badge?: string, semantic?: "ok"|"warn"|"danger"|"info" }
```

### `card-grid`
```
cards: array of { title: string, body: string, tags?: string[], badge?: string }
```

### `sortable-table`
```
columns: array of { key: string, label: string, mono?: bool }
rows:    array of objects — keys match column keys
```

### `status-table`
```
columns:       array of { key: string, label: string, mono?: bool }
rows:          array of objects
status_column: string — key of the status column
status_map:    object — status value → "ok"|"warn"|"danger"|"info"|"muted"
```

### `gantt`
```
tasks:        array of { id: string, name: string, start: int, end: int, critical?: bool, owner?: string }
month_count:  int
period_label: string — e.g. "Month", "Week", "Sprint"
```

### `doughnut`
```
segments:    array of { label: string, value: number, color?: string }
total_label: string
currency?:   string — prefix symbol if monetary
```

### `scurve`
```
points: array of { label: string, monthly: number, cumulative: number }
```

### `bubble-heatmap`
```
points:  array of { id: string, label: string, x: number, y: number, r?: number, detail?: string }
x_label: string
y_label: string
x_max:   int
y_max:   int
```

### `bar-chart`
```
categories: array of strings
series:     array of { label: string, values: number[] }
```

### `tree`
```
nodes: array of { id: string, label: string, meta?: string, children?: node[] }
```

### `flow-diagram`
```
steps: array of { id: string, label: string, sublabel?: string, type?: "start"|"end"|"step"|"decision" }
```

### `tabs`
```
tabs: array of { id: string, label: string, recommended?: bool, kpis?: kpi[], body: string }
```

### `checklist`
```
groups: array of {
  label: string,
  items: array of { id: string, text: string, done?: bool, owner?: string, due?: string, overdue?: bool }
}
```

### `definition-list`
```
entries: array of { term: string, definition: string, tags?: string[] }
```

### `risk-heatmap`
```
risks: array of {
  id: string, label: string, probability: int, impact: int,
  level: "critical"|"high"|"medium"|"low",
  strategy?: string, owner?: string, detail?: string
}
```

### `raci-table`
```
tasks:   array of { id: string, label: string }
members: array of { id: string, label: string }
matrix:  object — keys "{task_id}:{member_id}", values "R"|"A"|"C"|"I"|""
```

### `prose-card`
```
paragraphs: array of strings
quotes:     array of strings — from `> ` blocks
```

### `pull-quote`
```
text:          string
attribution?:  string
```

### `code-block`
```
lang: string
code: string — preserve whitespace exactly
```

### `figure`
```
src:      string
alt:      string
caption?: string
```

---

## Document Plan Schema

Output contract for `document-plan.json`. All fields required unless `?`.

```
{
  "title":           string  — from H1 or frontmatter
  "slug":            string  — kebab-case; becomes output filename
  "lang":            string  — BCP-47 code
  "style_slug":      string  — one of the five slugs
  "default_theme":   string  — "light" or "dark"
  "fonts_url":       string  — Google Fonts URL from style file
  "needs_chartjs":   bool    — true iff any widget uses Chart.js
  "needs_katex"?:    bool
  "needs_mermaid"?:  bool
  "single_section"?: bool    — true if source has only one # heading
  "css_tokens":      object  — { "--token": "value" } for every contract token
  "meta": {
    "author"?:   string
    "date"?:     string
    "version"?:  string
    "status"?:   string
    "org"?:      string
  },
  "sections": array of {
    "id":        string  — kebab-case anchor
    "num":       string  — zero-padded ("01", "02", ...)
    "heading":   string  — source language
    "subtitle"?: string
    "widgets":   array of { "slug": string, "data": object }
  },
  "nav_groups"?: array of { "label": string, "section_ids": string[] },
  "footer": {
    "org"?:        string
    "generated":   string  — ISO date
    "source_slug": string
  }
}
```

### Constraints

| Rule | Constraint |
|------|-----------|
| Nesting | Max 3 levels anywhere in the plan. |
| Slugs | kebab-case, no spaces. |
| Widget slugs | Closed vocabulary only. |
| css_tokens keys | Exact token names from contract. No additions. |
| sections | One entry per top-level `#` heading. No omissions. |
| widgets | Never empty. Every section has at least one widget. |
| needs_chartjs | True iff at least one widget slug has Chart.js in vocabulary table. |

---

## Bundled Style Files

| File | Tokens for |
|------|-----------|
| `design-style-editorial-warm.md` | `editorial-warm` |
| `design-style-dark-terminal.md` | `dark-terminal` |
| `design-style-clinical-blue.md` | `clinical-blue` |
| `design-style-brutalist-mono.md` | `brutalist-mono` |
| `design-style-pastel-soft.md` | `pastel-soft` |
