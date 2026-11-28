# QMD Reference

[QMD](https://github.com/tobi/qmd) keeps an index of the notes: keywords (BM25) and, when embeddings are set up, meaning (vectors). It ranks its results, which grep and the Obsidian CLI do not. It is optional: Atlas works without it. For choosing between it, grep and the Obsidian CLI when searching, see `SKILL.md` → Finding Notes.

In the commands below `{QMD}` is the value of `ATLAS_QMD_CMD`.

## Config

Two optional lines in the Atlas config. `workflows/setup.md` (step 7) asks the user before adding either one.

- `ATLAS_QMD_CMD`: switches QMD on for Atlas. See Prerequisites.
- `ATLAS_QMD_REFRESH=1`: lets Atlas refresh QMD's index. See Freshness.

## Prerequisites

QMD is used only when the Atlas config names it: `ATLAS_QMD_CMD`, the absolute path of one executable (never a command line with arguments, never a relative path). Not set means not available, even if a `qmd` is on the PATH: naming it in the config is the user's consent, and whatever that command does when it searches is their setup.

Check once per session. A failed check is not an error to report: use grep.

1. `cd "{BRAIN_PATH}" && {QMD} status` exits 0. Run every QMD command from the brain folder, so that a `.qmd` index in the project you happen to be working in is not used instead.
2. At least one collection in that output has its folder inside `{BRAIN_PATH}` (`{QMD} collection show <name>` prints `Path:`). If none does, QMD does not cover this brain: use grep.
3. Note whether any vectors are embedded.

## What Atlas never does on its own

- Install QMD.
- Run `{QMD} embed` or `{QMD} pull`. Depending on how the user set QMD up, they download models or send note text to an embedding service. Vectors are part of the user's setup. QMD's own hints ("Run 'qmd embed'...") are meant for the user: ignore them.
- Run `{QMD} update` without `ATLAS_QMD_REFRESH=1` in the Atlas config. See Freshness.

## Commands

```bash
cd "{BRAIN_PATH}"

# A question or a topic: 1 to 3 keyword lines (alternatives) and one sentence in plain words
{QMD} query $'lex: Acme pricing proposal\nlex: Acme quote\nvec: the draft pricing proposal for Acme' --no-rerank -n 5 --format files

# A phrase or a name you remember: all words must appear, quotes make an exact phrase
{QMD} search '"single source of truth"' -n 5 --format files

# One collection only; json adds the title, the line and a snippet
{QMD} search 'weekly review' -c brain -n 5 --format json
```

- **The command comes first**, options after it: `{QMD} query '...' -n 5`, not `{QMD} -n 5 query '...'`.
- **Write the lines yourself.** Each `lex:` line is a set of words that must all appear; several lines are alternatives. The `vec:` line is the question as you would ask a person, and it can stay in the user's language: a Spanish question finds English notes.
- **No vectors?** If `{QMD} status` shows nothing embedded, leave the `vec:` line out: keyword lines and `search` work on their own.
- **Don't use the automatic modes unless the user asks.** `{QMD} query "question"` without lines has QMD's own small model write the query, and `vsearch` searches by meaning only: both found fewer notes than lines an agent writes (see the measurements in `search-tools.md`), and both need QMD's models on the machine. Reranking was not measured and needs one more model, so the examples pass `--no-rerank`.
- **Stay inside the brain.** QMD may index other folders too. If some collections live outside `{BRAIN_PATH}`, pass `-c <name>` for each collection that is inside it, on every search. With no collection inside it, don't use QMD (see the check above).
- **Stay inside the scope.** When the request says to look inside one project's or one client's folder, QMD still ranks notes from the whole collection: keep only the results under that folder, or search that folder with grep instead. A request about a client with no folder named ("everything about Acme") is brain-wide: keep all results.
- **Quote the command** if its path has spaces: `"{QMD}" query ...`.
- **Results** are `#docid,score,qmd://<collection>/<path>`. The file is the collection's `Path:` plus `<path>`. To print a note without mapping the path: `{QMD} get "qmd://<collection>/<path>"`.

## Freshness

QMD answers from its index, which can be behind the files. `{QMD} update` re-reads changed files in every collection of that index (about a second), and it also runs any update command the user attached to a collection, so run it only when the Atlas config has `ATLAS_QMD_REFRESH=1`: that is the user saying `qmd update` is cheap and safe here. With the flag, run `{QMD} update` once, before the first search of a session; in Claude Code the plugin also runs it after an agent writes a note, one refresh at a time. Without the flag, don't run it. Either way, use grep for a note written a moment ago: two refreshes that overlap can leave a brand-new note out of the index until the next one.
