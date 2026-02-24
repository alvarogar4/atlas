---
name: atlas:business_strategy
description: Business strategy frameworks and patterns. Use when discussing strategy, business model, competitive positioning, market analysis, or major business decisions.
tools: Read, Write, Grep, Glob, Bash, WebSearch, WebFetch, Task, AskUserQuestion
user_invocable: true
---

# Business Strategy

Frameworks and patterns for strategic planning, business analysis, and decision-making.

## Config

Follow the **Basic** or **Project** config level from `atlas:second_brain` depending on context.

Requires: `BRAIN_PATH` (minimum), `ACTIVE_PROJECT` (when analyzing a specific project)

## Capabilities

| What the user wants                               | Workflow                |
| ------------------------------------------------- | ----------------------- |
| Analyze a strategic question, understand position | `workflows/analyze.md`  |
| Document a business decision                      | `workflows/decision.md` |
| Weekly/monthly/quarterly/annual review            | `workflows/review.md`   |

### Intent Detection for Review Period

When user asks for a review, route to the correct section in `workflows/review.md`:

- "weekly review", "how was this week" → Weekly section
- "monthly review", "month in review" → Monthly section
- "quarterly review", "Q1 review", "strategic review" → Quarterly section
- "annual review", "year in review", "yearly review" → Annual section
- "review" with no qualifier → Default to Weekly

### Config Notes

- `analyze.md` and `decision.md`: **Project** config when project-scoped (need `ACTIVE_PROJECT`), **Basic** config when general or area-scoped.
- Quarterly and Annual reviews: **Project** config when project-scoped, **Basic** config when personal. If no `ACTIVE_PROJECT`, default to personal.
- Weekly and Monthly reviews use **Basic** config (only need `BRAIN_PATH`).

## Framework Selection Guide

| Situation                   | Recommended Framework | File                        |
| --------------------------- | --------------------- | --------------------------- |
| Understand current position | SWOT                  | `frameworks/swot.md`        |
| Analyze industry dynamics   | Porter's Five Forces  | `frameworks/porters.md`     |
| Assess macro environment    | PESTEL                | `frameworks/pestel.md`      |
| Map internal operations     | Value Chain           | `frameworks/value-chain.md` |
| Design business model       | Business Model Canvas | `frameworks/bmc.md`         |
| Early-stage startup         | Lean Canvas           | `frameworks/lean-canvas.md` |
| Create new market space     | Blue Ocean            | `frameworks/blue-ocean.md`  |
| Understand customer needs   | Jobs-to-be-Done       | `frameworks/jtbd.md`        |
| Set and track goals         | OKRs                  | `frameworks/okrs.md`        |
| Understand competitors      | Competitive Analysis  | `frameworks/competitive.md` |
| Prioritize tasks            | Eisenhower Matrix     | `frameworks/eisenhower.md`  |
| Score initiatives           | ICE/RICE Scoring      | `frameworks/ice-rice.md`    |

## Templates

- Decision Log: `templates/decision.md`
- Analysis: `templates/analysis.md`
- Review: `templates/review.md`

## Agent Dependencies

Strategy workflows spawn these agents:

- **`atlas:locate_knowledge`** — Find existing analyses, decisions, and market intelligence in the brain
- **`atlas:strategist`** — Apply strategic frameworks, synthesize findings, produce recommendations
- **`atlas:analyze_knowledge`** — Deep synthesis when the strategist has too many files to read directly

## Error Handling

- **Brain not configured**: "Let's set up Atlas first — where should I store your knowledge base?"
- **No active project** (when needed): List available projects, ask user to choose
- **Required file missing**: Explain what's needed and offer to create it
- **External service failure**: Retry once, continue with available data. Never fabricate information

## Storage

All paths follow `atlas:second_brain` → `reference/folder-structure.md`. This skill determines **scope**:

1. **Project** — `ACTIVE_PROJECT` is set AND topic relates to the project → project-level paths
2. **Area** (decisions only) — Topic maps to a known `{BRAIN_PATH}/areas/{area}/` folder → area-level paths
3. **General** — No match → brain-level paths
4. **Ambiguous** — Ask the user: "Is this about {ACTIVE_PROJECT}, a specific area (health, finances, etc.), or a general decision?"

Analyses skip step 2 — they are reference material (PARA: resources) and route either project or general.

Reviews: weekly/monthly are always brain-level. Quarterly/annual ask whether project-scoped or personal.
