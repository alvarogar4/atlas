# Finding Notes: which tool for which request

Three tools can find a note. Each wins a different kind of request, so pick by the request, not by habit. grep and find always work. The Obsidian CLI and QMD are optional: use each one only where its check passes, and fall back to grep where it doesn't.

## Which tool

The routing table is in `SKILL.md` → Finding Notes, together with the default commands: it is the only copy, kept there so it is in front of the agent before its first search. This file holds what is behind it: the checks, the grep commands and the measurements.

## Before using a tool

QMD and the Obsidian CLI each have a check to pass first. A failed check is not an error to report: use grep.

- **QMD**: only when the Atlas config names it (`ATLAS_QMD_CMD`) and it indexes this brain. Read `qmd.md` once, before the first QMD call: the check, the commands, the query syntax, and what Atlas never runs.
- **Obsidian CLI**: only while the Obsidian app is already running, and always with the brain's vault named. Read `obsidian.md` (Obsidian CLI) before the first call: the check and the commands.
- **grep and find**: always. Use the harness's own tools (Grep, Glob, ripgrep) when it has them.

## grep

```bash
# An exact string, anywhere in the brain
grep -rlF 'INV-2026-0417' --include='*.md' "{BRAIN_PATH}"

# A file by its name
find "{BRAIN_PATH}" -iname '*budget*' -not -path '*/.*'

# Inside a known folder
grep -rilE 'compaction|merge tree' --include='*.md' "{BRAIN_PATH}/projects/acme/work"

# Across the brain, most matching lines first
grep -rciE 'pattern' --include='*.md' "{BRAIN_PATH}" | grep -v ':0$' | sort -t: -k2 -nr | head -10
```

- Scope it to a folder whenever you know one. Across a whole brain a generic word matches hundreds of notes in no useful order.
- It is the only one of the three that sees a file the moment it is written, reads files that are not Markdown, matches a string byte for byte, and takes regular expressions. It does not match file names: that is `find`.

## What the choice is based on

Measured on a 2,584-note brain in November 2026. Two things improve with this routing, by different amounts:

- **The right note on the first try: a large gain.** In one shot, the right note is in the first 5 results for 77 to 84% of requests with QMD (keyword lines plus a meaning line), against 50 to 55% for grep at its best ordering and 39 to 47% for an Obsidian CLI search.
- **Searches per request: about half. Notes found in the end: slightly more.** Agents free to retry found 126 of 150 notes with this routing against 122 with the previous instructions (Obsidian CLI first, then grep), in 1.4 to 2.5 searches per request instead of 2.5 to 6.4. Per agent, the notes found moved between one fewer and four more out of 30.

**One shot per tool.** 171 requests with a known right note. Five models (Opus, Sonnet, Haiku, Codex, Grok) each wrote, without seeing the notes, the first query they would try with each tool. The figure is the share of requests with the right note in the first 5 results, as a range across the five.

| Kind of request                       | grep, best ordering | Obsidian CLI search | QMD keyword lines | QMD keyword lines + meaning |
| ------------------------------------- | ------------------- | ------------------- | ----------------- | --------------------------- |
| Literal phrase                        | 100%                | 98 to 100%          | 98 to 100%        | 98 to 100%                  |
| A note recalled by name               | 40 to 55%           | 30 to 42%           | 82 to 95%         | 85 to 95%                   |
| A question in other words             | 25 to 40%           | 18 to 28%           | 50 to 72%         | 68 to 78%                   |
| The same question in another language | 28 to 40%           | 15 to 28%           | 52 to 75%         | 58 to 78%                   |
| All requests                          | 50 to 55%           | 39 to 47%           | 72 to 82%         | 77 to 84%                   |

- grep and Obsidian usually do contain the note (about 9 times in 10), but among a median of 9 to 19 unranked matches. QMD's gain is the ranking.
- The tool matters more than the model that writes the query: the five models are within a few points of each other on every tool.
- Meaning alone found 0 to 10% of literal phrases. It is one line to add to keyword lines, not a mode of its own.
- A raw question that QMD's own model expands into a query found fewer notes than keyword lines plus a meaning line in every kind of request (an earlier pass with one set of queries), and took 12 to 23 s a call on a CPU. Reranking was not measured.
- For backlinks, the Obsidian CLI returned 231 real links where grepping for the note names returned 1,321 hits, 1,091 of them not links.

**End to end.** 30 requests, each answered by an agent following either the previous instructions (Obsidian CLI first, then grep) or this routing, free to retry.

| Agent         | Right note, before → now | Searches per request, before → now |
| ------------- | ------------------------ | ---------------------------------- |
| Claude Opus   | 26 → 25 of 30            | 2.5 → 1.6                          |
| Claude Sonnet | 24 → 25 of 30            | 2.8 → 1.4                          |
| Claude Haiku  | 22 → 26 of 30            | 4.3 → 2.5                          |
| Codex         | 24 → 25 of 30            | 6.4 → 1.5                          |
| Grok          | 26 → 25 of 30            | 3.8 → 2.3                          |

With retries, the previous instructions get there almost as often (122 against 126 of 150), so end to end the gain in notes found is small and the gain in work is large: about half the searches. Why fewer searches also find slightly more notes was not measured.
