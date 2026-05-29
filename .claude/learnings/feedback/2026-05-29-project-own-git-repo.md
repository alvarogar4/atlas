---
date: "2026-05-29 12:59:42"
sha: "7f8e292"
category: "missing-check"
status: applied
applied-date: "2026-05-29 13:01:51"
target: "skills/second_brain/SKILL.md"
change-type: "update"
observed-workflows:
  subagents: []
  skills: ["atlas:second_brain"]
  commands: []
---

# Atlas assumed brain-root repo covered a project that is its own git repo

## Observation

"atlas didnt follow instructions, he knows some projects may have its own github state, why?"

The user asked Atlas to `git pull` the obsessiondb project. Atlas ran `git pull` at the brain root (`atlas-brain`), reported "Already up to date," and even told the user that `projects/obsessiondb` was "a subfolder within that single git repo, not its own repo." The user had to push back twice ("fucking go there and pull") before Atlas `cd`'d into the project path, where `git rev-parse --show-toplevel` revealed obsessiondb is in fact its own independent repo (`github.com:obsessiondb/brain`, a team-shared repo) nested inside the brain working tree. The actual pull then fast-forwarded 1300+ lines of new content.

## Context

User loaded the obsessiondb project via the `atlas:second_brain` skill and asked to sync it from GitHub. A project under `{BRAIN_PATH}/projects/<name>` can be its own git repository (separate remote, separate branch, team-shared), distinct from the personal brain repo that contains it.

## Analysis

When performing a git operation scoped to a project path, Atlas assumed the enclosing brain repo was authoritative instead of verifying the actual repo boundary for that path. The correct first step for any git op on a project is to `cd` into the project directory and run `git rev-parse --show-toplevel` (and `--abbrev-ref HEAD`) to discover whether the project is its own repo — never infer repo membership from the parent. This is a skipped verification step (`missing-check`): the knowledge that projects may carry their own git state existed, but the skill provides no instruction to resolve the repo toplevel from inside the project path before acting, so Atlas defaulted to the parent repo and confidently reported a wrong result. The nested repo is also invisible to `git status` at the parent (the parent gitignores it), which makes the wrong assumption easy to "confirm."
