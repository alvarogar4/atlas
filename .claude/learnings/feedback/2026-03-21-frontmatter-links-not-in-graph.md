---
date: "2026-03-21 20:16:08"
sha: "13c60c4"
category: "wrong-pattern"
status: applied
applied-date: "2026-03-21 20:23:52"
target: "skills/second_brain/reference/cross-referencing.md"
change-type: "update"
observed-workflows:
  subagents: []
  skills: ["atlas:second_brain"]
  commands: []
---

# Frontmatter `related:` plain paths are invisible in Obsidian graph

## Observation

After adding `related:` arrays with vault-root paths (e.g., `- /projects/personal-brand/context.md`) to 257 files across the brain, the Obsidian graph view showed no connections. Plain YAML strings in frontmatter are not parsed as links by Obsidian — only wikilinks (`[[note]]`) and markdown links in the body create graph edges.

## Context

User bumped atlas plugin versions and added body-level cross-references (## Related sections, **See also** footers) to ~250 files. The agent converted these to frontmatter `related:` arrays using plain vault-root paths per the cross-referencing spec (`reference/cross-referencing.md`). The body sections were then removed. Result: 1,794 links existed in metadata but zero showed in the Obsidian graph, breaking the "fully interconnected brain" goal.

## Analysis

The `cross-referencing.md` spec documents the `related` property format as plain paths (`- /projects/personal-brand/context.md`). This format works for agent discovery (agents parse YAML) but Obsidian's graph engine only indexes wikilinks and markdown links. The spec never mentions Obsidian graph compatibility or wikilink syntax. This is a wrong-pattern issue in the skill's reference documentation — it prescribes a format that achieves half the stated goals ("Agent discovery" works, "Graph navigation" does not). The fix required converting to `- "[[projects/personal-brand/context.md]]"` wikilink format.
