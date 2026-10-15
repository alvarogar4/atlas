# Workflow: Content Status

**Purpose**: Cross-topic overview of all content in the pipeline.

## Setup

Execute **Project** config from `atlas:second-brain`.

## Process

1. List all directories in `{PROJECT_PATH}/marketing/content/`. If user asks for a range of dates, use the calendar to identify the content in that range.
2. For each directory, check which pipeline files exist:
   - `0_context.md` -> Context defined
   - `1_research.md` -> Research complete
   - `2_plan.md` -> Planned
   - `3_draft-{channel}.md` -> Draft complete (note which channels)
   - `4_review-{channel}.md` -> Reviewed (note which channels)
   - `5_results-{channel}.md` -> Results tracked (note which channels)
3. Determine pipeline stage: the latest completed step
4. Read the current quarter's calendar to identify scheduled but not-yet-started content

### Output

Display a summary table:

| Topic   | Date   | Stage                                          | Channels               | Next Step         |
| ------- | ------ | ---------------------------------------------- | ---------------------- | ----------------- |
| {topic} | {date} | {Context/Research/Plan/Draft/Review/Published/Results} | {channels with status} | {what to do next} |

**Summary statistics**:

- Total topics: {n}
- In research: {n}
- In planning: {n}
- Drafts ready: {n}
- Under review: {n}
- Published: {n}
- Results tracked: {n}

**Calendar gaps**: Content scheduled in the calendar but not yet started.
