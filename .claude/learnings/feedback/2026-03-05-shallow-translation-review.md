---
date: "2026-03-05 18:09:42"
sha: "e0a6cb1"
category: "missing-check"
status: applied
applied-date: "2026-03-17 14:04:58"
target: "skills/translator/SKILL.md"
change-type: "update"
observed-workflows:
  subagents: []
  skills: ["atlas:translator"]
  commands: []
---

# Translation review skipped systematic checklist on first pass

## Observation

When reviewing Spanish translations of two blog posts, the first pass only caught surface-level issues (missing opening question marks, one false friend, pronoun stuffing) but missed 21 deeper naturalness problems: calques ("como efecto secundario", "lo que significa que", "significan"), stiff vocabulary ("permanecieron", "habría requerido", "disponibilidad de recursos"), structural borrowings ("para una fila dada", "El trabajo estuvo en"), and register issues ("no deberías necesitar"). The user had to explicitly ask for a second review to get the thorough pass that should have happened the first time.

## Context

User asked for a native Spanish (Spain) translation review of two ClickHouse blog posts against their English originals, with explicit instructions to check against the translator skill's 18-pattern checklist. The atlas:translator skill was loaded, which provides a zero-tolerance checklist of 18 anti-patterns. Despite having the checklist in context, the first pass treated it as a reference rather than a mandatory systematic scan.

## Analysis

Root cause: The skill was loaded into context but not used as a forcing function. The agent did a "read and spot what jumps out" review instead of methodically going through each of the 18 patterns against every paragraph. The checklist exists precisely to prevent this — patterns like calques (pattern 3), stiff vocabulary (pattern 9), and structural borrowing (pattern 13) are invisible on a casual read but obvious when you actively look for them. The skill instructions say "Run through the 18 anti-patterns checklist" as step 4 of the process, but the agent skipped that systematic step and relied on intuition, which missed the subtler issues.
