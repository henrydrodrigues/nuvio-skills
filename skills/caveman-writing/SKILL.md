---
name: caveman-writing
description: >
  Token-efficient writing style for internal-facing markdown artifacts read by
  AI agents, not humans. Apply whenever generating or editing ROUTING.md files,
  CONTEXT.md Process steps, Audit tables, build-log entries, smoke-test reports,
  or any markdown artifact consumed exclusively by a model at runtime. Triggers
  include: writing ROUTING.md in the Goal Engine, writing Process steps in ICM
  stage CONTEXT.md files, generating Agent Factory build-log entries, or any
  request to make agent-facing documentation more concise. Do NOT apply to
  user-facing documentation, agent briefs, store listings, or normative
  reference files read by humans.
---

# Caveman Writing Skill

Internal markdown read by models wastes tokens on prose that adds zero semantic
value. Caveman writing removes that waste without removing information.

The principle: **write what the model needs to act, nothing else.**

---

## The Core Rules

### 1. No articles
Drop `a`, `an`, `the` everywhere.

| Before | After |
|--------|-------|
| Read the spec file. | Read spec file. |
| Write the output to the artifacts folder. | Write output to artifacts folder. |
| Load the previous stage's context. | Load previous stage context. |

### 2. Imperative verbs only
Start every instruction with a verb. No subject, no preamble.

| Before | After |
|--------|-------|
| The agent should read the inputs table. | Read inputs table. |
| In this step you will write the draft. | Write draft. |
| This step is responsible for validating. | Validate. |

### 3. No transitional phrases
Cut `then`, `next`, `after that`, `once complete`, `finally`. Numbering already
encodes sequence.

| Before | After |
|--------|-------|
| First, read the spec. Then, validate the schema. | 1. Read spec. 2. Validate schema. |
| Once the output is written, update work.json. | Write output. Update work.json. |

### 4. No rationale in instructions
Rationale belongs in reference files. Process steps tell the model what to do,
not why.

| Before | After |
|--------|-------|
| Validate output against schema to ensure downstream stages receive correct data. | Validate output against schema. |
| Write ROUTING.md last, after all issues are shaped, so the tree reflects the final plan. | Write ROUTING.md after all issues are shaped. |

### 5. No meta-commentary
Cut phrases that describe the instruction rather than give it.

| Before | After |
|--------|-------|
| The following steps describe how to complete this stage. | *(delete entirely)* |
| This section outlines the expected outputs. | *(delete entirely)* |
| Note that the audit must pass before writing output. | Audit must pass before writing output. |

### 6. Compress multi-word noun phrases
| Before | After |
|--------|-------|
| the output of the previous stage | prev stage output |
| the currently active work | active work |
| the stage boundary interface contract | boundary contract |
| the list of pending issues | pending issues |

### 7. Tables over prose for conditions and checks
Audit and validation conditions are tables, not bullet lists with explanations.

```markdown
## Audit

| Check | Pass condition |
|-------|---------------|
| Schema valid | Output matches declared JSON Schema. |
| No skipped issues | All issues have status done, awaiting_review, or failed. |
| Handoff path exists | Output file present at declared location. |
```

Not:
> Before saving the output, verify that the schema is valid by checking it against
> the declared JSON Schema. Also make sure no issues were skipped...

---

## Where to Apply

### Apply — model-read artifacts

| Artifact | Location | What to compress |
|----------|----------|-----------------|
| `ROUTING.md` | Goal Engine plan tree | Issue descriptions, scope lines, status labels |
| Process steps | ICM stage `CONTEXT.md` | Every numbered step |
| Audit tables | ICM stage `CONTEXT.md` | Check names and pass conditions |
| `build-log.md` entries | Agent Factory Stage 02 | Outcome lines per stage |
| `smoke-test-[slug].md` | Agent Factory Stage 03 | Finding descriptions, verdict lines |
| `work.json` string fields | Goal Engine / Agent Factory | Status labels, stage names |

### Do NOT apply — human-read artifacts

| Artifact | Reason |
|----------|--------|
| `agent-[slug].[lang].md` | User-facing documentation |
| `agent-brief.md` | Operator-authored intent document |
| Store listing fields | Shown in catalog UI |
| `shared/interface-contract-rules.md` | Normative spec read by workspace authors |
| `_config/` files with prose rules | Humans edit these; legibility matters |
| `CLAUDE.md` workspace root | Read once per session; humans also read it for orientation |
| Questionnaire files | Humans fill these in |

---

## Cognitive Stage Exception

For **cognitive stage Process steps**, apply all rules above **except rule 4** (no
rationale). Cognitive stages need quality anchors — criteria that tell the model
what a good output looks like. These must survive compression.

Compress the framing, keep the criterion:

| Before | After |
|--------|-------|
| Write a formal executive summary in the third person, targeting senior leadership, with a maximum of 200 words, ensuring the tone remains neutral throughout. | Write executive summary. Third person. Max 200 words. Neutral tone. |
| The summary should capture the main argument without omitting any key findings from the source document. | Capture main argument. Include all key findings. |

The criterion survives. The prose wrapper does not.

---

## ROUTING.md Pattern

ROUTING.md entries are read by the Atomic Executor on every issue traversal.
Apply maximum compression.

**Before:**
```markdown
## Phase 1 — Foundation

This phase establishes the core infrastructure required for all subsequent
phases. It must be completed before any product work begins.

### Epic 1.1 — Authentication

Implement the authentication system that will be used throughout the product.

#### Issue 1.1.1 — JWT middleware

**Objective:** Implement JWT validation middleware for all protected routes.
**Scope:** `src/middleware/auth.ts`, `src/middleware/index.ts`
**Validation:** Unit tests covering valid token, expired token, malformed token.
**Status:** pending
```

**After:**
```markdown
## Phase 1 — Foundation

### Epic 1.1 — Authentication

#### Issue 1.1.1 — JWT middleware
Objective: JWT validation middleware for protected routes.
Scope: `src/middleware/auth.ts`, `src/middleware/index.ts`
Validation: unit_tests — valid token, expired token, malformed token.
Status: pending
```

---

## Process Steps Pattern

**Before:**
```markdown
## Process

1. Begin by reading the specification file from the previous stage to understand
   the agent's declared stages, boundary interfaces, and test input.
2. For each stage declared in the spec's Stages table, create the corresponding
   folder structure inside the workspace directory.
3. After all folders are created, write the CONTEXT.md for each stage based on
   the stage's job description and interface declarations.
4. Run the audit checks listed below. If any check fails, revise the output
   before saving it.
5. Write the scaffolding log to the output folder.
```

**After:**
```markdown
## Process

1. Read spec — stages table, boundary interfaces, test input.
2. Create folder structure for each declared stage.
3. Write CONTEXT.md per stage from job description and interface declarations.
4. Run audit. Revise if any check fails.
5. Write scaffolding log to output.
```

---

## Audit: Before Generating Any Artifact

Run this checklist before writing any internal markdown artifact:

| Check | Pass condition |
|-------|---------------|
| Articles removed | No `a`, `an`, `the` in instructions or descriptions. |
| Imperative verbs | Every instruction starts with a verb. |
| No transitional phrases | No `then`, `next`, `after that`, `once complete`. |
| No rationale in steps | Rationale lives in reference files, not Process steps. Exception: cognitive quality anchors retained. |
| No meta-commentary | No phrases that describe the instruction instead of giving it. |
| Tables for conditions | Audit and validation conditions use tables, not prose bullets. |
