#!/usr/bin/env bash
# humanizer lint: deterministic checks for the mechanically detectable patterns.
#
#   ./tools/lint.sh FILE.md [FILE.md ...]   lint content
#   ./tools/lint.sh --self-check            verify the skill itself is internally consistent
#
# BLOCK = zero tolerance, no legitimate use. Exit 1.
# WARN  = needs human judgement, reported but does not fail.
#
# This sees roughly a third of the 43 patterns and none of the structural ones.
# Passing is necessary, never sufficient. YAML frontmatter and fenced code are skipped.
#
# Do not run this on the skill's own files. SKILL.md and reference/ quote every banned
# phrase as ban lists and before/after examples, so they fail by design. Use --self-check.
set -uo pipefail

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"

if [[ "${1:-}" == "--self-check" ]]; then
  status=0
  for n in $(seq 1 43); do
    hits=$(grep -l "^### $n\. " "$SKILL_DIR"/reference/*.md 2>/dev/null | wc -l | tr -d ' ')
    row=$(grep -cE "^\| $n +\|" "$SKILL_DIR/SKILL.md" 2>/dev/null || true)
    [[ "$hits" == "1" ]] || { echo "pattern $n: in $hits reference files, expected 1"; status=1; }
    [[ "$row"  == "1" ]] || { echo "pattern $n: $row checklist rows in SKILL.md, expected 1"; status=1; }
  done
  bad=$(grep -ohE "^### [0-9]+\. " "$SKILL_DIR"/reference/*.md | grep -oE "[0-9]+" | sort -n | uniq | awk '$1<1||$1>43')
  [[ -z "$bad" ]] || { echo "reference/ defines out-of-range patterns: $bad"; status=1; }
  [[ $status -eq 0 ]] && echo "self-check ok: 43 patterns, one reference section and one checklist row each"
  exit $status
fi

[[ $# -gt 0 ]] || { echo "usage: lint.sh FILE.md [FILE.md ...] | --self-check" >&2; exit 2; }

# id ~ severity ~ label ~ extended-regex ~ [s = case sensitive, default insensitive]
read -r -d '' RULES <<'RULES_EOF'
13~BLOCK~em dash~—
13~BLOCK~double hyphen used as dash~[[:alnum:]] -- [[:alnum:]]
18~BLOCK~curly quote or apostrophe~[‘’“”]
17~BLOCK~emoji~[😀-🿿🚀-🛿✀-➿⚠-⚡✅✔❌❗]
19~BLOCK~chatbot artifact~(i hope this helps|let me know if|feel free to ask|would you like me to|here is a (brief|short|quick) (overview|summary))
21~BLOCK~sycophancy~(great question|excellent point|you're absolutely right|that's a great)
20~BLOCK~knowledge-cutoff disclaimer~(as of my (last|knowledge)|up to my last training|based on available information|while specific details (are|about))
7~BLOCK~AI vocabulary~\b(delve|tapestry|testament to|pivotal|underscore(s|d)?|showcas(e|es|ing)|intricate|interplay|garner(ed|s)?|multifaceted|realm of|myriad|robust solution|seamless(ly)?|holistic|paradigm shift)\b
7~WARN~AI vocabulary, softer~\b(crucial|vibrant|enduring|foster(s|ing)?|enhance(s|d)?|landscape|leverage|align with|key (role|moment|factor))\b
35~BLOCK~confessional adverb~\b(genuinely|honestly|truly|literally|fundamentally|inherently|inevitably|crucially|importantly|interestingly|remarkably|incredibly)\b
35~WARN~filler adverb~\b(really|simply|actually|just|deeply|notably|certainly|absolutely|exactly|precisely)\b
30~BLOCK~business jargon~([Dd]eep dive|[Cc]ircle back|[Dd]ouble down|[Gg]ame.changer|[Ll]ean into|[Tt]ake a step back|[Mm]oving forward|[Oo]n the same page|[Uu]npack (the|this|these))~s
30~BLOCK~dead metaphor~(where (did|do|does|will|would) (you|they|we|it) land|draws? the line|drawing the line|(something|anything|nothing) to sit on|caught my eye)
30~WARN~dead metaphor, check literal~\b(landed|landing|lands?) (on|in)\b
31~BLOCK~throat-clearing opener~(here's (the thing|what|why|how|this|that)|the uncomfortable truth|it turns out|let me be clear|the truth is,|i'm going to be honest|can we talk about|what most people miss|the real (question|unlock|problem) is|the interesting (part|bit|thing) (is|here)|the honest answer|in the end\b)
19~BLOCK~silence tie-back~(never got your side|so i'?ll go first|haven'?t heard back, so)
32~BLOCK~emphasis crutch~(let that sink in|full stop\.|make no mistake|here's why that matters|this matters because|i keep coming back to)
33~BLOCK~meta-commentary~(plot twist|spoiler:|let me walk you through|in this section|as we'll see|more on that later|but that's another (post|story)|the rest of this (essay|post|article))
34~BLOCK~rhetorical setup~(think about it[:.]|here's what i mean|and that's okay|sound familiar|but wait[.,])
22~BLOCK~filler phrase~(in order to|it is important to note|at this point in time|due to the fact that|at the end of the day|in a world where|at its core|it's worth noting|the reality is|when it comes to)
24~BLOCK~generic positive conclusion~(future looks bright|exciting times|journey toward|step in the right direction|watch this space)
9~BLOCK~negative parallelism~(not just [[:alpha:]',[:space:]-]{2,30}(but|it'?s)|isn'?t (about|the problem|just)|not only [[:alpha:]',[:space:]-]{2,30} but|the (question|answer|problem|point) isn'?t|(isn'?t|wasn'?t|weren'?t|aren'?t|didn'?t|doesn'?t) [[:alpha:]',[:space:]-]{2,40}[.,;] +(it'?s|it is|that'?s|they'?re|we (were|are|did)|they (were|are|did))|(is|was|are|were) not [[:alpha:]',[:space:]-]{2,40}[.,;] +(it'?s|it is|that'?s))
23~WARN~excessive hedging~(could potentially|might possibly|it could be argued|somewhat of a|a bit of a)
36~WARN~lazy extreme~\b(everyone|everybody|nobody|always|never|every single)\b
15~WARN~inline-header list~^[[:space:]]*[-*][[:space:]]+\*\*[^*]+:\*\*
41~WARN~Wh- sentence starter~(^|\. )(What|When|Where|Which|Who|Why|How) [a-z]
42~WARN~possible fragment ending a paragraph~^[A-Z][a-z]+( [a-z]+){0,2}\.$
RULES_EOF

status=0
for file in "$@"; do
  [[ -f "$file" ]] || { echo "lint: no such file: $file" >&2; status=2; continue; }

  # blank out YAML frontmatter, fenced code, inline code and URLs; keep line numbers intact
  body="$(awk '
      NR==1 && /^---[[:space:]]*$/ {fm=1; print ""; next}
      fm && /^---[[:space:]]*$/    {fm=0; print ""; next}
      fm                          {print ""; next}
      /^[[:space:]]*```/          {inb=!inb; print ""; next}
      inb                         {print ""; next}
                                  {print}
    ' "$file" | sed -E 's/`[^`]*`//g; s#https?://[^ )"]*##g')"

  blocks=0; warns=0
  while IFS='~' read -r id sev label regex csense; do
    [[ -z "${id:-}" ]] && continue
    if [[ "${csense:-}" == "s" ]]; then
      hits="$(printf '%s\n' "$body" | grep -nE "$regex" || true)"
    else
      hits="$(printf '%s\n' "$body" | grep -niE "$regex" || true)"
    fi
    [[ -z "$hits" ]] && continue
    n=$(printf '%s\n' "$hits" | grep -c .)
    if [[ "$sev" == "BLOCK" ]]; then blocks=$((blocks+n)); else warns=$((warns+n)); fi
    while IFS= read -r hit; do
      ln="${hit%%:*}"; txt="${hit#*:}"
      printf '%s:%s: %-5s p%-2s %-32s %s\n' "$file" "$ln" "$sev" "$id" "$label" \
        "$(printf '%s' "$txt" | sed 's/^[[:space:]]*//' | cut -c1-80)"
    done <<< "$hits"
  done <<< "$RULES"

  if [[ $blocks -gt 0 ]]; then
    echo "$file: FAIL  $blocks blocking, $warns warnings"
    status=1
  else
    echo "$file: pass  0 blocking, $warns warnings"
  fi
done
exit $status
