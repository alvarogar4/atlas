---
date: "2026-10-23 18:40:00"
sha: "9d8f08e"
category: "missing-context"
status: applied
applied-date: "2026-10-23 18:40:00"
target: "skills/marketing-content/channels/blog.md, skills/marketing-content/reference/review-checklist.md, skills/second-brain/agents/content_reviewer.md, skills/second-brain/entities/competitor.md, skills/second-brain/templates/competitor.md, skills/translator/SKILL.md"
change-type: "update"
observed-workflows:
  subagents: []
  skills: ["atlas:marketing-content", "atlas:humanizer", "atlas:translator"]
  commands: []
---

# Blog guidance silent on competitor links, schedules, honest refreshes and translated editions

## Observation

Building the Tirada blog (40 SEO/GEO posts in Spanish written in one batch, released Tuesdays and Saturdays, then a British English edition of all 40) surfaced gaps in the blog guidance:

- The posts and the landing's comparison pages linked competitors with `nofollow`: home pages, help pages, and newsletters hosted on `*.substack.com` and `*.ghost.io`. The user caught it: "Never link to them". It took about 1,700 links out across blog and landing, then a build check (`check_site.py`) so they don't come back.
- A batch released on a schedule needs links to later posts held back, `datePublished` set to the release instant with its offset, and unreleased posts kept out of the sitemap and feeds.
- The refresh cadence said every pass bumps `dateModified`. A pass that finds nothing to change should not. Tirada separates `updated` from `reviewed`, and adds `recheck` dates for facts with an expiry (a law entering into force, a price review).
- Translating for search needed rules the translator skill did not have: keywords researched in the target language, translated slugs and a slug map for internal links, length limits measured again, quotes restored to their original wording, locale conventions, glosses for local institutions and source-language-only UI.

## Analysis

`channels/blog.md` covered external links only as "link to authoritative sources" and had no notion of competitor domains. `entities/competitor.md` stored one website per competitor, not the list of domains a link check needs. The translator skill handled naturalness but nothing about the page as a search result.
