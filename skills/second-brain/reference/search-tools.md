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
  2. Once per session: `{OBSIDIAN} vaults verbose` lists each vault with its path. Take the name of the vault whose path is `{BRAIN_PATH}` and pass `vault="<name>"` on every call. If no vault has that path, the CLI would answer for another vault: don't use it.
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
- **Results** are `#docid,score,qmd://<collection>/<path>`. The file is the collection's `Path:` plus `<path>`. To print a note without mapping the path: `{QMD} get "qmd://<collection>/<path>"`.
- **Freshness.** QMD answers from its index, which can be behind the files. `{QMD} update` re-reads changed files (about a second), and it also runs any update command the user attached to a collection, so run it only when the Atlas config has `ATLAS_QMD_REFRESH=1`: that is the user saying a refresh is cheap and safe here. With the flag, run `{QMD} update` once, before the first search of a session; in Claude Code the plugin also runs it after an agent writes a note, one refresh at a time. Without the flag, don't run it. Either way, use grep for a note written a moment ago.

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
{OBSIDIAN} vault="{VAULT}" search query='"disk encryption" path:areas/remote-setup' limit=20 format=json
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

Measured on a 2,576-note brain in November 2026: 171 requests with a known right note, the first query each agent would try, one shot per tool.

| Kind of request                       | grep, best ordering | Obsidian CLI search | QMD keyword lines + meaning |
| ------------------------------------- | ------------------- | ------------------- | --------------------------- |
| Literal phrase                        | 100%                | 100%                | 100%                        |
| A note recalled by name               | 40%                 | 35%                 | 92%                         |
| A question in other words             | 32%                 | 28%                 | 82%                         |
| The same question in another language | 35%                 | 28%                 | 78%                         |

The figure is the share of requests with the right note in the first 5 results. grep and Obsidian usually do contain the note (72 to 100% of the time), but among a median of 13 to 30 unranked matches, which is what costs the extra round trips. For backlinks, the Obsidian CLI returned 231 real links where grepping for the note names returned 1,321 hits, 1,091 of them not links.
