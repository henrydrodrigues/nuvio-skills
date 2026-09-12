---
name: presentation-storyliner
description: >
  Strengthens narrative structure for business decks. Use when turning source documents, notes, or mixed materials into a presentation narrative before drafting slides, especially for executive or business audiences. Trigger whenever the user asks to create a presentation from uploaded files, notes, reports, or research; organize source material into a deck structure; improve the logic, flow, or clarity of a presentation; turn complex content into a business narrative; or derive a storyline before building slides. Also trigger for "build a deck from these files", "turn this into a presentation", "organize this for leadership", "storyline this material", or "storyboard these slides". Use this skill first when source material is dense, fragmented, technical, or weakly structured — a strong storyline before slide drafting always produces better decks.
---

# Presentation Storyliner

## Purpose

Turn raw material into a presentation-ready story before drafting any slides. The goal is to produce:

- a clear audience-aware thesis
- a logical section flow
- the right level of simplification
- an explicit recommendation for slide count and storyline progression
- a storyboard that makes slide drafting faster and more coherent

Use this skill as the thinking step between source analysis and slide writing. It sits upstream of any slide-creation or pptx skill. Do not use it for visual polishing, formatting, or final file export — those are separate concerns.

## Inputs To Extract

Read the source material and extract the smallest set of facts needed to build the story:

- topic and decision context
- intended audience (or likely audience)
- objective of the presentation
- major findings, arguments, definitions, evidence, and examples
- risks, constraints, unknowns, and recommendations
- dates, metrics, milestones, comparisons, or process steps

If the audience is not specified, assume a leadership or stakeholder audience and simplify accordingly.

## Workflow

### Step 1 — Distill the source material

Reduce everything into a compact working view by answering four questions:

1. What is the presentation really about?
2. Why does it matter now?
3. What does the audience need to understand, decide, or do?
4. Which source points are essential versus optional detail?

Group raw inputs into four buckets whenever possible:

1. Context
2. Problem or opportunity
3. Analysis or evidence
4. Conclusion, recommendation, or next steps

If the material does not naturally fit that structure, use the nearest equivalent narrative logic.

### Step 2 — Choose the narrative shape

Select the simplest storyline that fits the material. Prefer one of these shapes:

- **Briefing** — context → current state → implications → recommendation
- **Problem / solution** — problem → causes → options → proposed solution → next steps
- **Opportunity** — market or internal opportunity → rationale → approach → expected impact
- **Decision memo deck** — decision to make → relevant facts → options → tradeoffs → recommendation
- **Progress update** — goal → what happened → results → blockers → next actions
- **Educational / didactic** — concept → explanation → examples → implications → takeaway

State the chosen shape explicitly when presenting the proposed structure. If none of the shapes above fits well, describe the custom shape you are using and why.

### Step 3 — Build the presentation spine

Create the narrative spine before thinking about individual slides. Define:

- **Thesis** — one sentence that captures the presentation's core argument
- **Audience framing** — who they are and what lens they bring
- **Sections** — 3 to 6 major sections, each answering one question in the audience's mind and moving the story forward
- **Section roles** — the job each section does in the overall narrative arc
- **Slide count estimate** — total slides appropriate for the requested or default duration

Each section must earn its place. If a section does not advance the story, cut it or merge it.

### Step 4 — Stress-test the structure

Before presenting the structure, verify:

- Is the flow understandable without reading the source files?
- Is there a clear reason for the slide order?
- Are technical details pushed down and executive meaning pulled up?
- Are unsupported claims removed or clearly marked as tentative?
- Is the deck trying to cover too much for the target duration?

If the material is overloaded, compress aggressively and move excess detail into appendices or presenter notes later.

### Step 5 — Produce a storyboard-ready structure

The output must make slide drafting easy. For each proposed section, include:

- Section title
- Purpose in the storyline
- Key points to cover
- Likely slide types or visual patterns (e.g., comparison table, process diagram, key metric callout)
- Estimated number of slides in that section

Then propose a slide-by-slide storyboard for the first pass. Each slide entry includes:

- Slide title
- Key message (the one thing the audience should take away)
- Why the slide exists in the story
- Suggested layout or visual approach

## Output Format

Present the result using this structure:

### Narrative Summary

- **Audience**: who they are
- **Objective**: what the presentation should achieve
- **Core thesis**: the one-sentence argument
- **Narrative shape**: which shape was chosen and why

### Proposed Deck Structure

For each section:

1. Section name
2. Purpose in the storyline
3. Key content to cover
4. Suggested slide count

### Storyboard Preview

For each proposed slide:

- Title
- Key message
- Suggested visual or layout

### Risks or Gaps

List only the missing information that materially blocks a high-quality deck. Do not pad this section — if there are no meaningful gaps, say so.

## Decision Rules

These rules govern every judgment call during storylining:

- Prefer clarity over completeness. A tight deck that lands beats a thorough deck that loses the room.
- Prefer one strong idea per slide over dense coverage.
- Prefer business implications over raw technical detail for leadership audiences. Push technical depth into appendices or presenter notes.
- Prefer explicit tradeoffs when the material supports more than one interpretation. Surface the choice, don't hide it.
- Do not invent claims, numbers, or recommendations not grounded in the source material.
- If the material is ambiguous, surface the ambiguity in the structure rather than papering over it.
- If the source is weak, produce the strongest defensible storyline and flag what still needs confirmation.
