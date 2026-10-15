# Foundation: Project Strategy

Interactive wizard for defining the project's strategic direction.

## Pattern

1. Check if file exists → offer to overwrite
2. Ask the user questions, one at a time (use a structured question tool such as AskUserQuestion if your harness has one)
3. Fill template from `templates/strategy.md`
4. Save to the appropriate path

## Setup

Execute **Project** config from SKILL.md.

## Pre-checks

- Create `{PROJECT_PATH}/strategy/` directory
- Check if strategy.md exists → ask what to update or overwrite

## Questions

1. "Vision (where do you want to be in 2-3 years)?"
2. "Mission (how do you create value)?"
3. "Primary goal (the #1 thing you're trying to achieve)?"
4. "Supporting goals (2-3 additional objectives)?"
5. "Primary target segment?"
6. "Key differentiation?"
7. "This quarter's focus initiatives?"
8. "Success metrics?"

## Execution

- Generate strategy.md using the Strategy template from `templates/strategy.md`
- Write to `{PROJECT_PATH}/strategy/strategy.md`

## Output

```
Strategy defined: {PROJECT_PATH}/strategy/strategy.md

Vision: {summary}
Primary Goal: {goal}

Next: Want to document competitors or define brand voice?
```
