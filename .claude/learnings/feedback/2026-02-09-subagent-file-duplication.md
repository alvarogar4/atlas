---
date: "2026-02-09 22:50:25"
sha: "2ab19bc"
category: "wrong-pattern"
status: applied
applied-date: "2026-02-22 13:55:32"
target: "skills/second_brain/SKILL.md, agents/marketing_content_reviewer.md, agents/business_strategist.md, skills/marketing_content/workflow/review.md"
change-type: "update"
observed-workflows:
  subagents:
    [
      "atlas:locate_knowledge",
      "atlas:market_researcher",
    ]
  skills: ["atlas:second_brain", "atlas:second_brain"]
  commands: ["/atlas:marketing_content"]
---

# Subagent should not write research files -- main agent owns file creation

## Observation

The main agent should trigger as many agents as needed, insights should flow back and the main agent should write the research. Not the subagent, otherwise we have duplicates.

## Context

During `/atlas:marketing_content linkedin jarvis-compound-effect`, the market_researcher subagent was spawned to research the "compound effect" angle. The subagent autonomously created a content folder (`2026-02-10_compound-effect/`) and saved its own `1_research.md` file inside it. Meanwhile, the main agent also created a content folder (`2026-02-10_jarvis-compound-effect/`) and wrote its own `1_research.md`. This resulted in two separate folders with two separate research files for the same content piece, requiring manual cleanup and merging.

## Analysis

The root cause is a responsibility boundary problem in the orchestration pattern. The `market_researcher` subagent was given a research prompt but was not explicitly told to **only return findings** without writing files. The subagent took initiative and created its own folder structure + research file. The main agent, following the `/atlas:marketing_content` command workflow, also created a folder and wrote a research file as instructed by the command.

The `atlas:second_brain` skill defines a clear pattern: subagents locate and analyze, then the main agent synthesizes and writes. But the `market_researcher` subagent prompt in the content-research command doesn't enforce this boundary -- it says "Return: sources, angle, data points..." but doesn't say "Do NOT create files or folders."

The fix should be at two levels:

1. The content-research command's market_researcher prompt should explicitly instruct: "Return your findings as text. Do NOT create any files or folders."
2. The agent orchestration skill could reinforce that only the main agent writes output files -- subagents return data, main agent owns persistence.
