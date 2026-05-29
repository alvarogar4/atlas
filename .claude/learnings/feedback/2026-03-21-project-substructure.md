---
date: "2026-03-21 21:30:33"
sha: "6c88dd5"
category: "missing-context"
status: pending
observed-workflows:
  subagents: []
  skills: ["atlas:second_brain"]
  commands: ["/compound:feedback"]
---

# Second brain lacks built-in sub-project/product structure within projects

## Observation

The second brain skill doesn't support organizing sub-projects or products within a project's root. Personal brand project already does this organically and it works well, but it should be a built-in pattern in the skill itself. For example, ObsessionDB has multiple products (like Rudel) and currently uses `strategy-rudel` which doesn't make semantic sense — Rudel is a product with its own identity, not just a strategy variant. This is product information that deserves its own structure.

## Context

User noticed that the PARA-based project structure in `atlas:second_brain` treats each project as a flat silo. When a project has multiple products/sub-projects, there's no defined pattern for organizing them. The workaround (`strategy-rudel`, `strategy-{product}`) conflates product identity with strategy documents.

## Analysis

The `second_brain` skill defines a project structure (context.md, strategy/, competitors/, marketing/) but assumes one project = one product. Real-world projects like ObsessionDB are companies with multiple products, each needing their own context, strategy, competitors, and potentially marketing. The skill's folder-structure reference doesn't account for this nesting. This is a `missing-context` issue — the skill lacks the structural pattern for multi-product projects, forcing users into ad-hoc naming conventions that lose semantic meaning.
