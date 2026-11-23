# Finding Notes: grep, Obsidian CLI, QMD

Three tools can find a note. Each wins a different kind of request, so pick by the request, not by habit. grep and find always work. The Obsidian CLI and QMD are optional: use each one only where its check below passes, and fall back to grep where it doesn't.

## Which tool

| The request is...                                                                       | Use                                                                    | Why                                                                            |
| --------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| A note whose path you already have (given by the user, in memory, a known convention)   | Read it                                                                | No search needed                                                               |
| Work inside a folder you already know (a client folder, a draft, a calendar)            | grep and ls in that folder                                             | Few files, and exact strings pin things down                                   |
| A question, a topic, or "the note about X", location unknown                            | QMD: keyword lines plus one meaning line                               | Ranked; finds notes that use other words or another language                   |
| A phrase or a name you remember from a note                                             | QMD `search` with the phrase in quotes                                 | Finds it and ranks it first                                                    |
| An exact string inside a note (an identifier, a code, an error message), a regular expression | `grep -F` (or `-E`)                                              | Byte-exact. An index splits identifiers into words                             |
| A file name, or part of one                                                             | `find` or the harness's Glob                                           | grep reads contents, not names                                                 |
| A note written or edited a moment ago, a file that is not Markdown                      | grep                                                                   | It reads the files as they are now                                             |
| What links to a note, tags, orphans, unresolved links, properties                       | Obsidian CLI                                                           | It resolves links; grepping for a name also returns mentions that aren't links |
| QMD or the Obsidian CLI is not available here (another machine, a cloud session)        | grep                                                                   | Always there                                                                   |

After any search: read the top 3 to 5 results before answering. If none fits, rephrase once, then fall back to grep.

## Is the tool available?

A failed check is not an error to report: use grep.

- **QMD** is used only when the Atlas config names it: `ATLAS_QMD_CMD`, the absolute path of one executable (never a command line with arguments, never a relative path). Not set means not available, even if a `qmd` is on the PATH: naming it in the config is the user's consent, and whatever that command does when it searches is their setup. Check once per session:
  1. `cd "{BRAIN_PATH}" && {QMD} status` exits 0. Run every QMD command from the brain folder, so that a `.qmd` index in the project you happen to be working in is not used instead.
  2. At least one collection in that output has its folder inside `{BRAIN_PATH}` (`{QMD} collection show <name>` prints `Path:`). If none does, QMD does not cover this brain: use grep.
  3. Note whether any vectors are embedded.
- **Obsidian CLI**: the command is `ATLAS_OBSIDIAN_CMD` from the Atlas config when set, otherwise `obsidian`.
  1. Before every call, not once per session: the app is running (`pgrep -x Obsidian` on macOS and Linux). Calling the CLI with the app closed opens the app, and the user may have quit it since your last call.
  2. Once per session: `{OBSIDIAN} vaults verbose` lists each vault with its path. Take the name of the vault whose path is `{BRAIN_PATH}` and pass `vault="<name>"` on every call. If no vault has that path, or two vaults share that name, the CLI could answer for another vault: don't use it.
  3. "Command line interface is not enabled" means the user has it switched off.
- **grep and find**: always. Use the harness's own tools (Grep, Glob, ripgrep) when it has them.

What Atlas never does on its own:

- Install QMD, or switch the Obsidian CLI on. The Obsidian CLI can run code inside the app (`eval`), so turning it on is the user's decision.
- Start Obsidian in order to search.
- Run `{QMD} embed` or `{QMD} pull`. Depending on how the user set QMD up, they download models or send note text to an embedding service. Vectors are part of the user's setup.

## QMD

[QMD](https://github.com/tobi/qmd) keeps an index of the notes: keywords (BM25) and, when embeddings are set up, meaning (vectors).

```bash
cd "{BRAIN_PATH}"

# A question or a topic: 1 to 3 keyword lines (alternatives) and one sentence in plain words
{QMD} query $'lex: Newton School SOW\nlex: Newton School statement of work\nvec: the draft statement of work for Newton School' --no-rerank -n 5 --format files

# A phrase or a name you remember: all words must appear, quotes make an exact phrase
{QMD} search '"hidden-resentment trap"' -n 5 --format files

# One collection only; json adds the title, the line and a snippet
{QMD} search 'weekly review' -c brain -n 5 --format json
```

- **The command comes first**, options after it: `{QMD} query '...' -n 5`, not `{QMD} -n 5 query '...'`.
- **Write the lines yourself.** Each `lex:` line is a set of words that must all appear; several lines are alternatives. The `vec:` line is the question as you would ask a person, and it can stay in the user's language: a Spanish question finds English notes.
- **No vectors?** If `{QMD} status` shows nothing embedded, leave the `vec:` line out: keyword lines and `search` work on their own.
- **Don't use the automatic modes** (`{QMD} query "question"` without lines, `vsearch`, reranking) unless the user asks. They make QMD's own small models rewrite and rerank the query: slower, needs those models on the machine, and less accurate than lines you write.
- **Stay inside the brain.** QMD may index other folders too. If some collections live outside `{BRAIN_PATH}`, pass `-c <name>` for each collection that is inside it, on every search. With no collection inside it, don't use QMD (see the check above).
- **Stay inside the scope.** When the request says to look inside one project's or one client's folder, QMD still ranks notes from the whole collection: keep only the results under that folder, or search that folder with grep instead. A request about a client with no folder named ("everything about Acme") is brain-wide: keep all results.
- **Quote the command** if its path has spaces: `"{QMD}" query ...`.
- **Results** are `#docid,score,qmd://<collection>/<path>`. The file is the collection's `Path:` plus `<path>`. To print a note without mapping the path: `{QMD} get "qmd://<collection>/<path>"`.
- **Freshness.** QMD answers from its index, which can be behind the files. `{QMD} update` re-reads changed files in every collection of that index (about a second), and it also runs any update command the user attached to a collection, so run it only when the Atlas config has `ATLAS_QMD_REFRESH=1`: that is the user saying `qmd update` is cheap and safe here. With the flag, run `{QMD} update` once, before the first search of a session; in Claude Code the plugin also runs it after an agent writes a note, one refresh at a time. Without the flag, don't run it. Either way, use grep for a note written a moment ago: two refreshes that overlap can leave a brand-new note out of the index until the next one.

## Obsidian CLI

```bash
# Links and structure: what grep cannot answer exactly
{OBSIDIAN} vault="{VAULT}" backlinks path="areas/decisions/2026-04-02-budget.md" format=json
{OBSIDIAN} vault="{VAULT}" links path="areas/decisions/2026-04-02-budget.md"
{OBSIDIAN} vault="{VAULT}" unresolved
{OBSIDIAN} vault="{VAULT}" orphans
{OBSIDIAN} vault="{VAULT}" tags counts sort=count
{OBSIDIAN} vault="{VAULT}" properties

# Search of the live files, with Obsidian's operators
{OBSIDIAN} vault="{VAULT}" search query='"disk encryption" path:areas/setup' limit=20 format=json
{OBSIDIAN} vault="{VAULT}" search query="tenor (iceberg OR delta)" limit=20 format=json
```

- Words separated by spaces must all appear. `OR`, quoted phrases, `path:` and `tag:` work. Case and accents are ignored.
- Results are not ranked: it lists the notes that match, like `grep -l`. For search it does the same job as grep, with Obsidian's operators.
- `path=` is exact (`folder/note.md` from the vault root); `file=` resolves a name the way a wikilink does.
- `{VAULT}` is the name of the vault whose path is `{BRAIN_PATH}` (`{OBSIDIAN} vaults verbose`). Without `vault=`, the CLI answers for whichever vault was focused last.

## grep

```bash
# An exact string, anywhere in the brain
grep -rlF 'review-mwsd317q' --include='*.md' "{BRAIN_PATH}"

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

Measured on a 2,584-note brain in November 2026.

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
- For backlinks, the Obsidian CLI returned 231 real links where grepping for the note names returned 1,321 hits, 1,091 of them not links.

**End to end.** 30 requests, each answered by an agent following either the previous instructions (Obsidian CLI first, then grep) or this routing, free to retry.

| Agent         | Right note, before → now | Searches per request, before → now |
| ------------- | ------------------------ | ---------------------------------- |
| Claude Opus   | 26 → 25 of 30            | 2.5 → 1.6                          |
| Claude Sonnet | 24 → 25 of 30            | 2.8 → 1.4                          |
| Claude Haiku  | 22 → 26 of 30            | 4.3 → 2.5                          |
| Codex         | 24 → 25 of 30            | 6.4 → 1.5                          |
| Grok          | 26 → 25 of 30            | 3.8 → 2.3                          |

With retries, grep gets there about as often (122 against 126 of 150). The routing roughly halves the searches it takes.
