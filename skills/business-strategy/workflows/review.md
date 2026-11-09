# Workflow: Review

Periodic reviews at five cadences. Determine the period from the conversation:

- "wrap up", "daily review", "how was today" → Daily
- "weekly review", "how was this week" → Weekly
- "monthly review", "this month" → Monthly
- "quarterly review", "Q1 review", "strategic review" → Quarterly
- "annual review", "year in review", "yearly review" → Annual
- "review" with no qualifier → Default to weekly

All templates are in `templates/review.md`.

---

## Daily

**Purpose**: Close the day in about 10 minutes, together with the user, so nothing stays as "I'll remember" and each day's lessons compound into the weekly review.

**Config**: **Basic** from `atlas:second-brain`.

**File**: `{BRAIN_PATH}/areas/reviews/{YYYY-WXX}/{YYYY-MM-DD}.md`, where the week is the ISO week of the day being reviewed: `date -j -f %Y-%m-%d {YYYY-MM-DD} '+%G-W%V'` (macOS) or `date -d {YYYY-MM-DD} '+%G-W%V'` (GNU). A wrap-up after midnight still reviews the previous day. Template: Daily Review in `templates/review.md`.

### Process

Before step 1, read on your own whatever the user keeps the day in: their task or time-block system (planned vs actual), their to-do list, tomorrow's calendar, and the day's file if a draft already exists. Ask only what those can't answer.

1. **Questions**: ask the user everything you can't answer from those sources: open or unclosed blocks, background work and its results, why something moved or didn't happen. One message, short list.
2. **Verify**: check the day's file is complete (blocks with planned vs actual, per-topic notes, open items, tomorrow, to-do delta). Close every open item in the user's task system with what actually happened, put carry-overs into new tasks or to-dos (never into the review file: the brain holds context, not to-dos), and write the missing pieces.
3. **Conclusions**: give your read on the day: what moved, what slipped and why, patterns across days, risks for tomorrow. Benchmark against the plan and the user's own rules, not an ideal day. The user corrects what's off and you discuss it.
4. **Final**: write the agreed conclusions into the file's "Read on the day" section and save (commit and push if the brain is a git repo).

Keep the day's file as a draft during the day if the user shares notes; the wrap-up turns it into the final version.

---

## Weekly

**Purpose**: Reflect on week, plan next week.

**Config**: **Basic** from `atlas:second-brain`.

**File**: `{BRAIN_PATH}/areas/reviews/{YYYY-WXX}/{YYYY-WXX}-weekly.md`, in the same folder as the week's daily reviews. Template: Weekly Review in `templates/review.md`.

### Process

1. Get current week: `date '+%G-W%V'` (ISO week-numbering year, so the folder matches the dailies around New Year).

2. **Prepare before the session.** If the review is scheduled, write a prep version of the file before it starts: fill Key Metrics and every data-backed section (from the steps below), and mark the parts only the user can write (wins they care about, learnings, how the week felt, top 3 priorities). The session then finishes the same file instead of starting from a blank page.

   Sources, in order:
   - The week's daily reviews in `areas/reviews/{YYYY-WXX}/`: blocks, conclusions, what slipped.
   - The user's task or time-block system, if they track one: planned vs actual time, unplanned (extra) work share, time by topic, blocks closed late or not done.
   - Content results, if they publish: per-post numbers and audience growth week over week.
   - The to-do list: done this week, still open, overdue, due next week.
   - Items that slipped: how many times each moved, and why.

   Also draft **Atlas's read and recommendations**: 3-6 concrete recommendations, ordered by expected impact, each tied to evidence from this week (a number, a pattern across dailies, a repeated slip). Before drafting, read the "Atlas's Read and Recommendations" tables of the last few weekly reviews: do not re-propose anything the user rejected or deferred unless the reason they gave no longer holds (for example "after the funding round" once it has closed). Benchmark against the user's own constraints and rules, not an ideal week.

3. **Find other activity this week**:

```
subagent_type: atlas:locate_knowledge
prompt: "Find all files modified this week in {BRAIN_PATH}/

Time filter: Files modified in the last 7 days (-mtime -7)

Search all PARA categories:
- projects/ - Active work
- areas/ - Ongoing areas of responsibility
- resources/ - Reference material
- inbox/ - New captures

Return:
- File paths grouped by category
- Modification dates
- Content type (note, decision, idea, etc.)
- Brief summary of what changed"
```

4. Walk through review questions with user, starting from the prep version:

- **Wins & Accomplishments**: What went well? What progress was made?
- **Challenges & Learnings**: What didn't go as planned? What did you learn?
- **Key Metrics**: planned vs actual, extra work, content results, anything else they track. Compare with last week.
- **What slipped**: which items moved, how many times, and what that says about planning.
- **How the week felt**: energy, focus, anything outside work that shaped it.
- **Open Loops**: What's unfinished? What needs follow-up?
- **Next Week Focus**: Top 3 priorities? Important dates?
- **Atlas's read**: present the recommendations after the user's own answers. The user agrees, changes or rejects each one; record every answer in the table with its outcome, adopted ones also go into the user's planning rules (or wherever they keep standing rules), and rejected or deferred ones stay in the table so later reviews don't propose them again.

5. Save the finished version into the same file (commit and push if the brain is a git repo). If the user keeps a recurring review slot, make sure next week's exists.

---

## Monthly

**Purpose**: Reflect on month, assess progress, set direction.

**Config**: **Basic** from `atlas:second-brain`.

### Process

1. Get current month: `date '+%Y-%m'`

2. **Gather monthly data**:

```
subagent_type: atlas:locate_knowledge
prompt: "Find all files modified this month in {BRAIN_PATH}/

Time filter: Files modified in the last 30 days (-mtime -30)

Search all PARA categories with emphasis on:
- projects/ - Project progress
- areas/decisions/ - Decisions made
- areas/reviews/*/ - Weekly reviews (YYYY-WXX-weekly.md) and their daily reviews

Return:
- File paths grouped by category
- Summary of activity level per area
- Key changes identified"
```

3. Read the month's weekly reviews (`areas/reviews/{YYYY-WXX}/{YYYY-WXX}-weekly.md`) to synthesize; open the daily reviews in the same folders only when a weekly one is missing or thin.

4. Walk through monthly questions:

- **Accomplishments**: What did you complete? Goal progress?
- **Learnings**: New knowledge or skills? Insights?
- **Metrics**: How did key metrics perform?
- **Projects**: Status updates? Completions or starts?
- **Next Month**: Goals? Adjustments needed?

5. Save using the Monthly Review template from `templates/review.md`. Path from `reference/folder-structure.md` (brain-level reviews).

---

## Quarterly

**Purpose**: Strategic review, major course corrections.

**Config**: **Project** from `atlas:second-brain` when project-scoped, **Basic** when personal.

### Process

1. Calculate quarter: `month=$(date '+%m'); year=$(date '+%Y'); quarter=$(( (month - 1) / 3 + 1 )); echo "${year}-Q${quarter}"`

2. **Determine review scope**:

Ask: "Is this a review of {ACTIVE_PROJECT} specifically, or a personal quarterly review?"

3. **Load project context** (project review only):

Read these files:

1. `{PROJECT_PATH}/context.md`
2. `{PROJECT_PATH}/strategy/strategy.md` -- compare quarterly results against strategic goals
3. all files in `{PROJECT_PATH}/competitors/` -- note competitive landscape changes

If they don't exist, mention it in the review.

4. **Gather quarterly data**:

**For project quarterly review:**

```
subagent_type: atlas:locate_knowledge
prompt: "Find all files modified this quarter related to {ACTIVE_PROJECT}.

Time filter: Files modified in the last 90 days (-mtime -90)

Search in:
- {PROJECT_PATH}/strategy/ - Topic folders with analyses and decisions
- {PROJECT_PATH}/strategy/reviews/ - Past project reviews

Do NOT search:
- {BRAIN_PATH}/areas/decisions/ (personal)
- {BRAIN_PATH}/areas/{area}/decisions/ (personal areas)

Return:
- File paths grouped by type (analysis, decision, review)
- Summary of quarter activity
- Major milestones and changes"
```

**For personal quarterly review:**

```
subagent_type: atlas:locate_knowledge
prompt: "Find all files modified this quarter in {BRAIN_PATH}/areas/

Time filter: Files modified in the last 90 days (-mtime -90)

Search in:
- {BRAIN_PATH}/areas/ - General decisions, area-scoped decisions, area activity

Do NOT search:
- {BRAIN_PATH}/resources/strategy/ (reference material, not decision history)
- {PROJECT_PATH}/strategy/ (project-specific)

For active projects, list project names and one-line status only (from {BRAIN_PATH}/projects/ or ATLAS_PATH_* variables). Do not read project strategy details.

Return:
- File paths grouped by area
- Summary of quarter activity
- Major decisions and changes"
```

5. Read other reviews if they exist for the quarter to synthesize.

6. Walk through quarterly questions:

- **Goals Achievement**: Quarter goals met? What was achieved? What wasn't, and why?
- **Strategic Progress**: Moving toward vision? Pivots needed? Compare against strategy.md goals.
- **Major Wins**: Biggest accomplishments? What made them possible?
- **Major Challenges**: Biggest obstacles? What would you do differently?
- **Next Quarter**: Strategic priorities? Changes to approach?

7. Save using the Quarterly Review template from `templates/review.md`. Resolve path from `reference/folder-structure.md` based on scope (project or personal).

---

## Annual

**Purpose**: Full-year retrospective, strategic reset, long-term direction.

**Config**: **Project** from `atlas:second-brain` when project-scoped, **Basic** when personal.

### Process

1. Get current year: `date '+%Y'`

2. **Determine review scope**:

If no ACTIVE_PROJECT is set → skip the question, default to personal review.
If ACTIVE_PROJECT is set → ask: "Is this an annual review of {ACTIVE_PROJECT} specifically, or a personal annual review?"

3. **Load project context** (project review only):
   1. Read `{PROJECT_PATH}/context.md`
   2. Read `{PROJECT_PATH}/strategy/strategy.md` -- compare annual results against vision and strategic goals
   3. Read all files in `{PROJECT_PATH}/competitors/` -- assess how competitive landscape evolved over the year

4. **Gather annual data**:

**For project annual review:**

```
subagent_type: atlas:locate_knowledge
prompt: "Find all files modified this year related to {ACTIVE_PROJECT}.

Time filter: Files modified in the last 365 days (-mtime -365)

Search in:
- {PROJECT_PATH}/strategy/ - Topic folders with analyses and decisions
- {PROJECT_PATH}/strategy/reviews/ - Past project reviews (quarterly)

Do NOT search:
- {BRAIN_PATH}/areas/decisions/ (personal)
- {BRAIN_PATH}/areas/{area}/decisions/ (personal areas)

Return:
- File paths grouped by type (analysis, decision, review)
- Summary of year activity
- Major milestones, pivots, and changes"
```

**For personal annual review:**

```
subagent_type: atlas:locate_knowledge
prompt: "Find all files modified this year in {BRAIN_PATH}/areas/

Time filter: Files modified in the last 365 days (-mtime -365)

Search in:
- {BRAIN_PATH}/areas/ - General decisions, area-scoped decisions, area activity

Do NOT search:
- {BRAIN_PATH}/resources/strategy/ (reference material, not decision history)
- {PROJECT_PATH}/strategy/ (project-specific)

For active projects, list project names and one-line status only (from {BRAIN_PATH}/projects/ or ATLAS_PATH_* variables). Do not read project strategy details.

Return:
- File paths grouped by area
- Summary of year activity
- Major decisions, pivots, and changes"
```

5. Read quarterly reviews for the year to synthesize.

6. Walk through annual questions:

- **Vision Progress**: Where did you want to be? Where are you? What's the gap?
- **Biggest Wins**: Top 3-5 accomplishments that moved the needle most. What made them possible?
- **Biggest Misses**: What didn't happen that should have? Root causes?
- **Strategic Pivots**: Did the strategy change during the year? Were those pivots right?
- **Competitive Evolution**: How did the landscape shift? Are you better or worse positioned?
- **What Would You Do Differently**: If you could redo the year, what changes?
- **Next Year Vision**: Where do you want to be in 12 months? What needs to change to get there?

7. Save using the Annual Review template from `templates/review.md`. Resolve path from `reference/folder-structure.md` based on scope (project or personal).
