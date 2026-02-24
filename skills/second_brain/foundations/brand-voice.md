# Foundation: Brand Voice

Interactive wizard for defining the project's brand voice and tone.

## Pattern

1. Check if file exists → offer to overwrite
2. Ask questions via AskUserQuestion
3. Fill template from `templates/brand-voice.md`
4. Save to the appropriate path

## Setup

Execute **Project** config from SKILL.md.

## Pre-checks

- Read context.md to inform questions (suggest creating it first if missing)
- Check if brand-voice.md exists → ask to overwrite
- Create `{PROJECT_PATH}/marketing/` directory

## Questions

1. "What 3-5 adjectives describe your brand personality?"
2. "What tone should content have?" (formal, casual, technical, friendly)
3. "Any words/phrases to always use?"
4. "Any words/phrases to never use?"
5. "Example brand you admire?" (style reference)

## Execution

- Generate brand-voice.md using the Brand Voice template from `templates/brand-voice.md`
- Derive key messages from context + personality
- Write to `{PROJECT_PATH}/marketing/brand-voice.md`

## Output

```
Brand voice defined: {PROJECT_PATH}/marketing/brand-voice.md

Personality: [adjectives]
Tone: [description]

Next: Want to define the visual identity?
```
