# Foundation: Visual Identity

Interactive wizard for defining the project's visual style and color palette.

## Pattern

1. Check if file exists → offer to overwrite
2. Ask the user questions, one at a time (use a structured question tool such as AskUserQuestion if your harness has one)
3. Fill template from `templates/visual-identity.md`
4. Save to the appropriate path

## Setup

Execute **Project** config from SKILL.md.

## Pre-checks

- Check if visual-identity.md exists → ask to overwrite
- Create `{PROJECT_PATH}/marketing/` directory

## Questions

### Brand Colors

1. "What is your primary brand color?" (hex or name)
2. "What is your secondary brand color?"

### Visual Style

3. "What visual style?" (modern, classic, playful, minimal, bold)
4. "What mood/feeling?" (energetic, calm, professional, creative)

### AI Image Generation

5. "For AI-generated images — what perspective?" (front-facing, bird's-eye, isometric, dramatic angle)
6. "For AI-generated images — what rendering style?" (flat vector, 3D with soft shadows, painterly, photorealistic)
7. "For AI-generated images — any restrictions?" (e.g., no human faces, no text overlays)

### AI Schema Diagrams

8. "For schema diagrams — what visual patterns?" (e.g., rounded cards, sharp edges, glassmorphism)
9. "For schema diagrams — what should they convey?" (e.g., technical precision, approachable simplicity, data flow)

### References

10. "Any design references or inspirations?"

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
