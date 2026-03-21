---
date: "2026-03-20 22:16:02"
sha: "6361526"
category: "missing-check"
status: applied
applied-date: "2026-03-21 15:13:20"
target: "skills/second_brain/reference/cross-referencing.md, skills/second_brain/SKILL.md, skills/second_brain/entities/theme.md, skills/second_brain/entities/audience.md, skills/second_brain/foundations/brand-voice.md"
change-type: "create+update"
observed-workflows:
  subagents: ["atlas:atlas:locate_knowledge", "atlas:atlas:analyze_knowledge", "code:codebase-analyzer"]
  skills: ["atlas:second_brain"]
  commands: []
---

# Marketing config files should cross-reference each other by default

## Observation

When Atlas creates or updates marketing config files (brand-voice, themes, audiences), it does not add cross-references between related files. The user had to explicitly ask for:
1. Brand voice to reference theme and audience files
2. Theme files to link to their target audience persona files
3. Audience files to reference which themes/content strategies they map to

These connections should be established automatically when creating or updating any marketing config file. The brain's value compounds when files are interconnected — isolated files lose context.

## Context

During a Q1 quarterly review of the personal-brand project, Atlas updated brand-voice.md, all three theme files, and created four new audience personas. Each file was created/updated in isolation without linking to related files. The user noticed the gap and asked for cross-references to be added. Later when personas were renamed (Dan→David, Victor→Jean, Alex→Marc), a stale reference was missed because the connections were added manually rather than being part of the creation workflow.

## Analysis

The atlas:second_brain skill's entity and foundation workflows don't enforce cross-referencing between related marketing files. When a theme is created, it should automatically link to its target audience files. When an audience is created, it should reference which themes target it. When brand-voice is updated, it should maintain a reference section to all related config files. This is a missing-check in the creation/update workflows — the skill should verify that bidirectional references exist between related marketing assets.
