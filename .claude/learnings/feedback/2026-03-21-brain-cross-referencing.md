---
date: "2026-03-21 12:02:21"
sha: "13c60c4"
category: "missing-check"
status: applied
applied-date: "2026-03-21 15:13:20"
target: "skills/second_brain/reference/cross-referencing.md, skills/marketing_content/workflow/*.md, skills/marketing_content/calendar/plan.md, agents/locate_knowledge.md"
change-type: "create+update"
observed-workflows:
  subagents: ["atlas:atlas:locate_knowledge", "atlas:atlas:analyze_knowledge", "code:codebase-analyzer"]
  skills: ["atlas:second_brain", "atlas:marketing_content"]
  commands: ["/compound:feedback"]
---

# Brain files must be cross-referenced to enable graph navigation and context discovery

## Observation

The atlas brain was fully unconnected — 56% of files had zero outgoing links, zero bidirectional links existed across the entire project. This means:
1. Graph visualization tools (Obsidian) showed scattered dots instead of connected clusters
2. Atlas agents (locate_knowledge, analyze_knowledge) couldn't follow links to discover related context
3. When loading a file for content writing, the agent had no way to navigate to related audiences, themes, strategy docs, or previous content without manual searching

The user had to manually drive the entire cross-referencing session. The second_brain skill should enforce this by default across all operations — not just marketing content, but every piece of knowledge: resources, areas, projects, decisions, captures.

## Context

During a Q1 quarterly review of the personal-brand project, we discovered that:

**Project config files** (context, strategy, brand-voice, themes, audiences) were created as isolated documents. None linked to each other. The user asked for cross-references and we added them manually.

**Content pipeline files** (context → research → plan → draft → review → results) within each content folder had no links between them. We added "See also" lines where every file links to every sibling in its folder, creating tight bubbles in the graph. Results files also link outward to the calendar and Q1 review.

**Calendar** had no links to the content folders it schedules. We added "Content:" lines under each week linking to the folders.

**Series posts** (ClickHouse deep dives, Rudel launch chain) had no navigable prev/next links between them. We added series navigation in results files.

**Resource directories** couldn't be linked in graph tools because they're directories, not files. We created `resources/index.md` in each to give the graph a node to connect to.

**Unpublished content** (no results file yet) was disconnected from the graph entirely. We added calendar links to their context files as the outward connection.

The full pattern that emerged:
- Every file should link to all related files it knows about
- Within a folder, files should form a "bubble" (full mesh)
- Between folders, links should flow through shared references (calendar, reviews, series)
- Directory references need an index.md to be graph-navigable
- Files without a natural outward link (no results yet) need an explicit connection to the parent structure

## Analysis

The second_brain skill creates and manages files but has no concept of maintaining a connected graph. Each workflow (capture, search, entity CRUD, content pipeline) operates on individual files without checking or establishing links to related files. This is a missing-check that should be applied across all brain operations:

1. **Entity creation** (themes, audiences, competitors, projects): When creating any entity, scan for related entities and add bidirectional links
2. **Content pipeline**: When creating any pipeline step, add "See also" links to all existing siblings in the folder
3. **Captures and notes**: When saving to inbox/areas/resources, check for related notes and cross-link
4. **Foundation updates** (context, strategy, brand-voice): When updating any foundation doc, verify links to all related foundation docs exist
5. **Reviews**: When creating periodic reviews, link to all referenced content, strategies, and calendars

The graph connectivity is not cosmetic — it directly improves the locate_knowledge and analyze_knowledge agents' ability to discover relevant context by following links rather than relying solely on grep/glob searches.
