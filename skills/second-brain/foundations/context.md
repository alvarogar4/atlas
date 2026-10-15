# Foundation: Project Context

Interactive wizard for defining what the project is.

## Pattern

1. Check if file exists → offer to overwrite
2. Ask the user questions, one at a time (use a structured question tool such as AskUserQuestion if your harness has one)
3. Fill template from `templates/context.md`
4. Save to the appropriate path

## Setup

Execute **Project** config from SKILL.md.

## Pre-checks

- Check if `{PROJECT_PATH}/context.md` exists → ask to overwrite

## Questions (ask one at a time)

1. "What is this project/business?" (one sentence)
2. "What problem does it solve?"
3. "Who is the target audience?" (brief)
4. "What makes it unique?" (key differentiator)
5. "What's the primary goal?" (revenue, growth, awareness)
6. "What's the current stage?" (idea, MVP, growth, mature)
7. "Any constraints?" (technical, budget, timeline)

## Execution

- Generate context.md using the Context template from `templates/context.md`
- Generate a 2-3 sentence elevator pitch for the Summary
- Write to `{PROJECT_PATH}/context.md`
- Update README.md Overview section with the summary

## Output

```
Project context defined: {PROJECT_PATH}/context.md

Summary:
- Business: [one sentence]
- Audience: [brief]
- Differentiator: [key point]
- Stage: [current]

Next: Want to define the project strategy?
```
