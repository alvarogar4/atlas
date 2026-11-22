# Finding Notes: grep, Obsidian CLI, QMD

Three tools can find a note. Each wins a different kind of request, so pick by the request, not by habit. grep always works. The Obsidian CLI and QMD are optional: use each one only where its check below passes, and fall back to grep where it doesn't.

## Which tool

| The request is...                                                                            | Use                                                                                    | Why                                                                           |
| -------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| A note whose path you already have (given by the user, in memory, a known convention)        | Read it                                                                                | No search needed                                                              |
| Work inside a folder you already know (a client folder, a draft, a calendar)                 | grep and ls in that folder                                                             | Few files, and exact strings pin things down                                  |
| A question, a topic, or "the note about X", location unknown                                 | QMD: keyword lines plus one meaning line                                               | Ranked; finds notes that use other words or another language                  |
| A literal phrase, a name, an identifier                                                      | QMD keywords with the phrase in quotes. grep when QMD is missing or the note is recent | Both find it; QMD ranks it first                                              |
| A note written or edited in this session, a file that is not Markdown, a regular expression  | grep                                                                                   | It reads the files as they are now                                            |
| What links to a note, tags, orphans, unresolved links, properties                            | Obsidian CLI                                                                           | It resolves links; grepping for a name also returns mentions that aren't links |
| Neither optional tool is available (another machine, a cloud session)                        | grep                                                                                   | Always there                                                                  |

After any search: read the top 3 to 5 results before answering. If none fits, rephrase once, then fall back to grep.

## Is the tool available?

Check once per session, not before every call.

- **QMD**: the command is `ATLAS_QMD_CMD` from the Atlas config when set, otherwise `qmd` when it is on the PATH. It is available when `{QMD} status` exits 0.
- **Obsidian CLI**: the command is `ATLAS_OBSIDIAN_CMD` from the Atlas config when set, otherwise `obsidian` when it is on the PATH. It is available when `{OBSIDIAN} version` prints a version. It needs the Obsidian app running on this machine with the vault open. "Command line interface is not enabled" means the user has it switched off.
- **grep**: always. Use the harness's own search tool (Grep, ripgrep) when it has one.

Never install QMD or switch the Obsidian CLI on for the user. The Obsidian CLI can run code inside the app (`eval`), so turning it on is their decision.

## QMD

[QMD](https://github.com/tobi/qmd) keeps an index of the notes: keywords (BM25) and, when embeddings are set up, meaning (vectors).

```bash
# A question or a topic: 1 to 3 keyword lines (alternatives) and one sentence in plain words
{QMD} query $'lex: Newton School SOW\nlex: Newton School statement of work\nvec: the draft statement of work for Newton School' --no-rerank -n 5 --format files

# A literal phrase or a name: all words must appear, quotes make an exact phrase
{QMD} search '"hidden-resentment trap"' -n 5 --format files

# One collection only, or snippets and line numbers
{QMD} search 'weekly review' -c brain -n 5 --format json
```

- **Write the lines yourself.** Each `lex:` line is a set of words that must all appear; several lines are alternatives. The `vec:` line is the question as you would ask a person, and it can stay in the user's language: a Spanish question finds English notes.
- **Don't use the automatic modes** (`{QMD} query "question"` without lines, `vsearch`, reranking) unless the user asks. They make QMD's own small models rewrite and rerank the query: slower, needs those models on the machine, and less accurate than lines you write.
- **Results** are `#docid,score,qmd://<collection>/<path>`. Open one with `{QMD} get "#docid"`, or read the file itself: `{QMD} collection show <collection>` prints the collection's folder.
- **Freshness.** QMD answers from its index. Before the first search of a session run `{QMD} update`: it re-reads only changed files and takes about a second. `{QMD} embed` then adds vectors for new notes. Where the setup refreshes by itself both return at once. A note you wrote a moment ago is found by keywords after `update`, and by meaning once `embed` has run.
- **No vectors?** If `{QMD} status` shows nothing embedded, keep to keyword lines and `search`.

## Obsidian CLI

```bash
# Links and structure: what grep cannot answer exactly
{OBSIDIAN} backlinks path="areas/decisions/2026-04-02-budget.md" format=json
{OBSIDIAN} links path="areas/decisions/2026-04-02-budget.md"
{OBSIDIAN} unresolved
{OBSIDIAN} orphans
{OBSIDIAN} tags counts sort=count
{OBSIDIAN} properties

# Search of the live files, with Obsidian's operators
{OBSIDIAN} search query='"disk encryption" path:areas/remote-setup' limit=20 format=json
{OBSIDIAN} search query="tenor (iceberg OR delta)" limit=20 format=json
```

- Words separated by spaces must all appear. `OR`, quoted phrases, `path:` and `tag:` work. Case and accents are ignored.
- Results are not ranked: it lists the notes that match, like `grep -l`. Use it for search when the note may be newer than QMD's index and you want Obsidian's operators.
- `path=` is exact (`folder/note.md` from the vault root); `file=` resolves a name the way a wikilink does.

## grep

```bash
# Inside a known folder
grep -rilE 'compaction|merge tree' --include='*.md' "{BRAIN_PATH}/projects/acme/work"

# Across the brain, most matching lines first
grep -rciE 'pattern' --include='*.md' "{BRAIN_PATH}" | grep -v ':0$' | sort -t: -k2 -nr | head -10
```

- Scope it to a folder whenever you know one. Across a whole brain a generic word matches hundreds of notes in no useful order.
- It is the only one of the three that sees a file the moment it is written, reads files that are not Markdown, and takes regular expressions.

## What the choice is based on

Measured on a 2,576-note brain in November 2026: 171 requests with a known right note, the first query each agent would try, one shot per tool.

| Kind of request                       | grep, best ordering | Obsidian CLI search | QMD keyword lines + meaning |
| ------------------------------------- | ------------------- | ------------------- | --------------------------- |
| Literal phrase                        | 100%                | 100%                | 100%                        |
| A note recalled by name               | 40%                 | 35%                 | 92%                         |
| A question in other words             | 32%                 | 28%                 | 82%                         |
| The same question in another language | 35%                 | 28%                 | 78%                         |

The figure is the share of requests with the right note in the first 5 results. grep and Obsidian usually do contain the note (72 to 100% of the time), but among a median of 13 to 30 unranked matches, which is what costs the extra round trips. For backlinks, the Obsidian CLI returned 231 real links where grepping for the note names returned 1,321 hits, 1,091 of them not links.
