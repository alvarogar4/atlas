# Retrieval evaluation

Compare two or more Atlas revisions on the same questions. The runner saves the answer, tool calls, line arrival times, usage and stderr for each trial. The scorer works offline. Python 3.11 and Git on macOS or Linux are sufficient for the self-test. Live trials also need the selected agent CLIs and their credentials.

## Try the recorded comparison

From the repository root, run the self-test or score a copy of the invented transcripts.

```sh
python3 -I evals/retrieval/selftest.py

cp -R evals/retrieval/fixtures/recorded /tmp/pier-replay
python3 -I evals/retrieval/score.py --out /tmp/pier-replay \
  --cases evals/retrieval/fixtures/cases.json
```

The recording has 24 trials, including one quota failure. The report compares the 11 complete pairs. The [fixture vault](fixtures/vault/) and its [cases](fixtures/cases.json) also work for live grep and file-read trials. QMD uses a fixed index of the real brain. Use that brain for a QMD comparison.

## Run on private notes

Keep the answer key in its own folder below the brain. Choose a dedicated output directory outside the brain. Transcripts, errors, judge files and reports can contain private note text.

```sh
python3 -I evals/retrieval/run.py --brain /home/user/brain \
  --cases /home/user/brain/private-cases/cases.json \
  --refs main=origin/main,pr=feat/lookup --agents opus,codex,grok \
  --reps 2 --parallel 4 --hide private-cases previous-results \
  --out /tmp/pier-eval

python3 -I evals/retrieval/score.py --out /tmp/pier-eval \
  --cases /home/user/brain/private-cases/cases.json
```

The runner reads the cases, moves their parent folder and any extra `--hide` paths under the output directory, and sets Git's skip-worktree bit on tracked files for the duration. QMD can still return snippets of hidden text until the next `qmd update`. Opening the hidden note by its brain path fails. The read-only case prompt and hidden folders reduce accidental exposure. The CLIs retain filesystem access.

Each version gets a detached worktree and a separate test folder. Claude loads the worktree with `--plugin-dir` and disables the installed Atlas plugin in its settings. Codex follows project skill links and uses a temporary Codex home with a copy of its config and credentials. Atlas is disabled in that config because a command-line override can leave the installed plugin active. Grok follows project skill links, disables the installed plugin in the test folder, and gets a trust entry for that folder. Only the real brain inherits its configured QMD and Obsidian commands. The evaluation config omits the live retrieval log.

Before trials, each agent lists its brain skills. The smoke check requires one distinct skill path that resolves inside the matching worktree or test folder. A failed check skips that agent on that version. Check `smoke/` for the answer. Workers run the versions back to back for each agent, case and repetition. Watch `progress.log` for completions and failures.

Rerun the same command to resume. Add `--retry-failed` to repeat failed trials, or `--only-cases c01,c03` to select questions. `--timeout` defaults to 900 seconds per process. An exhausted Grok balance can produce HTTP 402, which the runner reports as `quota`.

### Recovery

The runner journals worktree registrations, trust edits and hidden paths before changing them. It replays the journal on exit and at the next startup, and removes temporary Codex homes with their credentials and sessions. To recover after an interruption, run:

```sh
python3 -I evals/retrieval/run.py --cleanup --out /tmp/pier-eval
```

If a note reappears while hidden, cleanup preserves both copies and prints the paths. Move the replacement to a safe location and rerun cleanup to restore the original. Keep the output directory until recovery finishes.

## Read the scores

Found is the fraction of required paths in the final answer. Surfaced credits paths in a tool input or result. Latest checks the answer for the current fact. The report flags stale answers, reads confined to superseded evidence, and missed citations. Path matching uses substrings, so a citation can earn credit even if the agent misunderstood the note.

The scorer measures elapsed time and calls to first relevant evidence, and distinguishes search hits from opening the note. It counts unrelated brain notes opened, reports the first search tool, and totals reported costs and tokens. Skill calls do not count toward speed. The timing medians omit trials with no hit. In a paired comparison, a missing time loses to a measured one.

Each pair compares the same agent, case and repetition. Found share decides first, then latest if the case has a current fact, then seconds to the first relevant path. Ties drop out of the two-sided exact sign test. With 20 non-tied pairs, 13 wins against seven gives p = 0.263. That split alone gives little evidence of a difference.

The scorer prints the report and saves `report.md`. For each scored trial, `metrics.json` lists the wasted notes, time to first open and counts by tool class. Use `--reparse` to rebuild records from streams. Optional `--judge` sends the paired traces and gold facts to Codex and Sonnet in a seeded, blind order. It caches completed votes under `judge/` and appends them to the report.

## Budget

Allow about $0.25 to $0.45 per Opus trial as a planning estimate. Codex and Grok consume their quotas. A trial typically takes 30 to 90 seconds. For 14 cases, three agents, two versions and two repetitions, budget 40 to 60 minutes at `--parallel 4` for 168 trials. Smoke checks and optional judges add calls. The offline self-test and recorded comparison need no provider quota.

## Limits

- QMD has one index per machine, of the real brain. Against another brain (the fixture vault included) the runner leaves QMD out of the agents' Atlas config, so those runs test grep and file reads only.
- The agents get the brain through `ATLAS_CONFIG=<out>/atlas.env`. Codex passes only part of the environment to its shell when its config sets `shell_environment_policy`; its agent may then read your usual Atlas config. The prompt names the brain either way.
- Metrics are substring matches on paths and regular expressions on facts. A citation earns credit even if the answer misreads the note; read the flags and a few answers.
- Speed depends on machine load and on the model provider. Compare versions back to back (the runner does, per pair), not across days.
- Grok's usage balance can run out mid-run (HTTP 402, reported as `quota`). Run it first or on its own.
