---
date: "2026-03-17 11:47:37"
sha: "no-git"
category: "missing-check"
status: applied
applied-date: "2026-03-17 14:04:58"
target: "skills/marketing_content/workflow/write.md, skills/marketing_content/workflow/review.md"
change-type: "update"
observed-workflows:
  subagents: []
  skills: ["atlas:second_brain", "atlas:marketing_content", "atlas:humanizer"]
  commands: []
---

# Humanizer missed negative parallelism pattern ("not X, Y" / "It's not X. It's Y.")

## Observation

The humanizer skill was loaded and applied during LinkedIn draft writing, but the agent still produced the phrase: "We weren't experimenting with AI coding. We were betting on it." This is a negative parallelism (pattern #9 in the humanizer: "Not only...but..." / "It's not just about..., it's..."). The "not X. [but] Y." construction is one of the most common AI writing tells. The humanizer explicitly lists this pattern as high signal strength, yet it slipped through.

User's rubber duck insight: "AI always fucking ends with Its not X. Its Y."

## Context

Writing a LinkedIn draft for the rudel.ai launch post. The humanizer skill was loaded before writing as required by the marketing_content workflow. The draft was generated with all 29 anti-patterns supposedly applied as generation-time constraints. The negative parallelism pattern was present in the first version of the LinkedIn draft (line in the blog draft: "We weren't experimenting with AI coding. We were betting on it.") and carried over into the LinkedIn adaptation.

## Analysis

The humanizer skill documents negative parallelisms as pattern #9 with "High" signal strength, but the pattern has subtle variants that the agent doesn't consistently catch. The classic "Not only X but Y" and "It's not just X, it's Y" forms are well-documented, but the "We weren't X. We were Y." variant is structurally identical and equally AI-sounding. The agent applied the skill as a checklist rather than internalizing the underlying principle: any sentence pair where the first negates and the second affirms using parallel structure is the same pattern. The check needs to be broader than exact phrase matching.
