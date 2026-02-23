# Foundation: Visual Identity

Interactive wizard for defining the project's visual style and color palette.

## Pattern

1. Check if file exists → offer to overwrite
2. Ask questions via AskUserQuestion
3. Fill template from `templates/visual-identity.md`
4. Save to the appropriate path

## Setup

Execute **Project** config from SKILL.md.

## Pre-checks

- Check if visual-identity.md exists → ask to overwrite
- Create `{PROJECT_PATH}/marketing/` directory

## Questions

1. "What is your primary brand color?" (hex or name)
2. "What is your secondary brand color?"
3. "What visual style?" (modern, classic, playful, minimal, bold)
4. "What mood/feeling?" (energetic, calm, professional, creative)
5. "Any design references or inspirations?"

## Execution

- Ask user for the visual identity and palette.
- Derive extended color palette from primary and secondary colors:
  - **Accent**: High-contrast variant for interactive states
  - **Surface**: Light neutral (#FFFFFF or near-white)
  - **Muted**: Desaturated variant of primary for subtle elements
  - **Border**: Light gray derived from surface
  - **Error**: Matches the palette look
  - **Warning**: Matches the palette look
  - **Info**: Matches the palette look
  - **Success**: Matches the palette look
- Generate visual-identity.md using the Visual Identity template from `templates/visual-identity.md`
- Write to `{PROJECT_PATH}/marketing/visual-identity.md`

## Output

```
Visual identity defined: {PROJECT_PATH}/marketing/visual-identity.md

Primary: {hex}
Secondary: {hex}
Style: {aesthetic} | Mood: {mood}
```
