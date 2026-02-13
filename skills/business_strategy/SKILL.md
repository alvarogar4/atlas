---
name: atlas:business:strategy
description: Business strategy frameworks and patterns. Use when discussing strategy, business model, competitive positioning, market analysis, or major business decisions.
tools: Read, Write, Grep, Glob, Bash, WebSearch, WebFetch, Task, AskUserQuestion
user_invocable: true
---

# Business Strategy

Frameworks and patterns for strategic planning, business analysis, and decision-making.

## Config

Follow the **Config Chain** from `second_brain_foundation/SKILL.md` (basic config required, project config for project-scoped analysis).

Requires: `BRAIN_PATH` (minimum), `ACTIVE_PROJECT` (when analyzing a specific project)

## Capabilities

| What the user wants | Workflow |
|---|---|
| Analyze a strategic question, understand position | `workflows/analyze.md` |
| Document a business decision | `workflows/decision.md` |
| Weekly/monthly/quarterly review | `workflows/review.md` |

### Intent Detection for Review Period

When user asks for a review, determine the period:
- "weekly review", "how was this week" → weekly mode
- "monthly review", "month in review" → monthly mode
- "quarterly review", "Q1 review", "strategic review" → quarterly mode
- "review" with no qualifier → default to weekly

## Framework Selection Guide

| Situation | Recommended Framework | File |
|-----------|----------------------|------|
| Understand current position | SWOT | `frameworks/swot.md` |
| Analyze industry dynamics | Porter's Five Forces | `frameworks/porters.md` |
| Assess macro environment | PESTEL | `frameworks/pestel.md` |
| Map internal operations | Value Chain | `frameworks/value-chain.md` |
| Design business model | Business Model Canvas | `frameworks/bmc.md` |
| Early-stage startup | Lean Canvas | `frameworks/lean-canvas.md` |
| Create new market space | Blue Ocean | `frameworks/blue-ocean.md` |
| Understand customer needs | Jobs-to-be-Done | `frameworks/jtbd.md` |
| Set and track goals | OKRs | `frameworks/okrs.md` |
| Understand competitors | Competitive Analysis | `frameworks/competitive.md` |
| Prioritize tasks | Eisenhower Matrix | `frameworks/eisenhower.md` |
| Score initiatives | ICE/RICE Scoring | `frameworks/ice-rice.md` |
| Document a decision | Decision Log | `templates/decision-log.md` |

## Error Handling

- **Brain not configured**: "Let's set up Atlas first — where should I store your knowledge base?"
- **No active project** (when needed): List available projects, ask user to choose
- **Required file missing**: Explain what's needed and offer to create it
- **External service failure**: Retry once, continue with available data. Never fabricate information

## Storage Locations

- Strategic analyses: `{BRAIN_PATH}/resources/strategy/{topic}/analysis.md`
- Decisions: `{BRAIN_PATH}/areas/decisions/YYYY-MM-DD-{topic}.md`
- Reviews: `{BRAIN_PATH}/areas/reviews/`
  - Weekly: `YYYY-WXX-weekly.md`
  - Monthly: `YYYY-MM-monthly.md`
  - Quarterly: `YYYY-QX-quarterly.md`
