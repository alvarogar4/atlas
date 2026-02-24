# Workflow: Review

Periodic business reviews at four cadences. Determine the period from the conversation:

- "weekly review", "how was this week" → Weekly
- "monthly review", "this month" → Monthly
- "quarterly review", "Q1 review", "strategic review" → Quarterly
- "annual review", "year in review", "yearly review" → Annual
- "review" with no qualifier → Default to weekly

All templates are in `templates/review.md`.

---

## Weekly

**Purpose**: Reflect on week, plan next week.

**Config**: **Basic** from `atlas:second_brain`.

### Process

1. Get current week: `date '+%Y-W%V'`

2. **Find recent activity**:

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

3. Walk through review questions with user:

- **Wins & Accomplishments**: What went well? What progress was made?
- **Challenges & Learnings**: What didn't go as planned? What did you learn?
- **Key Metrics** (if applicable): Any numbers to track?
- **Open Loops**: What's unfinished? What needs follow-up?
- **Next Week Focus**: Top 3 priorities? Important dates?

4. Save using the Weekly Review template from `templates/review.md`. Path from `reference/folder-structure.md` (brain-level reviews).

---

## Monthly

**Purpose**: Reflect on month, assess progress, set direction.

**Config**: **Basic** from `atlas:second_brain`.

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
- areas/reviews/ - Weekly reviews

Return:
- File paths grouped by category
- Summary of activity level per area
- Key changes identified"
```

3. Read weekly reviews for the month to synthesize.

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

**Config**: **Project** from `atlas:second_brain` when project-scoped, **Basic** when personal.

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

**Config**: **Project** from `atlas:second_brain` when project-scoped, **Basic** when personal.

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
