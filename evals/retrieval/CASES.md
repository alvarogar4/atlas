# Case files

Use a JSON object with a `cases` array. The file's `as_of` date records when you checked the gold answers. A case can override it. The optional `brain_note` gives the maintainer room to describe the collection.

```json
{
  "as_of": "2030-03-14",
  "brain_note": "Invented notes from the pier workshop.",
  "cases": [
    {
      "id": "c01",
      "kind": "recency",
      "question": "Which build runs on the Quay tally board?",
      "must_find": ["areas/log/2030-03-11"],
      "may_find": ["projects/quay/README"],
      "current_fact": "v2\\.1\\.4",
      "stale_facts": ["v1\\.6\\.0"],
      "superseded": ["projects/quay/README"],
      "as_of": "2030-03-14",
      "facts": "Both screens run v2.1.4."
    }
  ]
}
```

| Case field | Meaning |
| --- | --- |
| `id` | Required unique filename component. Start with a letter, digit or `_`. Dots and dashes can follow. |
| `kind` | Required label shown in the per-case table, such as `recency`, `backlinks` or `paraphrase`. |
| `question` | Required question the runner gives the agent. |
| `must_find` | Required nonempty list of evidence paths. Each entry contributes one equal share of the citation score. |
| `may_find` | Optional paths that count as useful reading for the waste metric. |
| `current_fact` | Optional case-insensitive Python regular expression for the current answer. Omit it to exclude the case from latest scores. |
| `stale_facts` | Optional list of regular expressions for obsolete answers. A stale-only flag requires a stale match without a current match. |
| `superseded` | Optional older paths. Opening one without opening required evidence triggers the superseded-only flag. |
| `as_of` | Optional case-specific gold check date in YYYY-MM-DD form. |
| `facts` | Optional free text for the blind judges. Include the facts needed to decide between two answers. |

Write paths relative to the brain. You can include or omit the `.md` suffix. End a folder path with `/` to accept a note below it. The scorer strips the brain prefix and Markdown extension before substring matching against citations and tool activity. Distinctive paths reduce accidental matches. Escape a backslash twice in JSON when the regular expression needs one, as in the dotted build numbers above.

Keep private case files in a dedicated subfolder. The runner hides that folder during trials. For the public invented data, [cases.json](fixtures/cases.json) sits beside the vault.
