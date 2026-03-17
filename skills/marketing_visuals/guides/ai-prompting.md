# AI Image Prompting

Compose prompts for AI image generators (conceptual illustrations, hero images, mood visuals).

## Process

### Step 1: Check for Visual Identity

```bash
cat ${PROJECT_PATH}/marketing/visual-identity.md 2>/dev/null
```

If exists, use as color/style defaults.

### Step 2: Gather Requirements from User

**If visual identity exists (Step 1), use it as the source of truth** for colors, style, mood, and rendering. Only ask the user about subject, purpose, and restrictions.

**If no visual identity exists**, prompt the user to create one first using the visual identity foundation (`second_brain/foundations/visual-identity.md`). If the user declines, ask the style/color/mood/rendering questions below before composing.

> **Note**: Examples throughout this guide (e.g., "isometric", "3D depth", specific hex codes) define the prompt _structure_, not recommended defaults. Never treat example values as the style to use.

**Always ask:**

1. **Subject**: "What should the image depict? What concept or scene?"

2. **Purpose/Size**: "What's this for?"
   - Blog header (1200x600)
   - Social card (1200x630)
   - Square post (1080x1080)
   - Hero background (1920x1080)
   - Thumbnail/card (400x300)
   - Other (ask dimensions)

3. **Restrictions**: "Anything to avoid?"
   - Default: no text, no logos, no human faces. Can be overwritten by visual identity, it always has priority.

**Only ask if no visual identity is defined and user declined to create one:**

4. **Colors**: "What colors should dominate? Primary? Secondary?"

5. **Style**: "What visual style?" (clean/minimal, dramatic/bold, futuristic, classic/elegant, playful, organic, etc.)

6. **Mood**: "What feeling should it evoke?" (professional, warm, energetic, calm, bold, sophisticated, etc.)

7. **Rendering**: "Illustrated or photorealistic? 2D flat or 3D depth?"

### Step 3: Compose the Prompt

## Prompt Structure

Include sections as needed:

```
STYLE: {aesthetic based on user's style + mood}

PERSPECTIVE: {viewing angle - isometric, front, dramatic, etc.}

COMPOSITION: {layout - centered, rule of thirds, canvas fill percentage}

CANVAS: {width}x{height} pixels, {aspect ratio}.

BACKGROUND: {solid color, gradient, or scene description}

LIGHTING: {direction and quality}

COLORS: {palette with hex codes}

RENDERING: {vector-like, painterly, flat, 3D depth, etc.}

RESTRICTIONS: {what NOT to include}

SUBJECT: {main concept/scene}

ELEMENTS: {specific objects with colors and positions}
```

## Key Principles

### Be Specific About Colors

Always use hex codes: "Primary #0077B6 (ocean blue)" not "blue tones"

### Define Composition

- Specify canvas fill (60%, 75%, etc.)
- Define positioning (centered, off-center)
- Leave room for text overlays if needed

### Always Add Restrictions

Defaults + user restrictions:

- No text, words, letters, numbers
- No logos or brand names
- No human faces (unless user wants them)

### Match Complexity to Size

- Small (thumbnails): fewer elements, simpler
- Large (heroes): more detail and elements

### Describe Elements with Colors

Each element should reference the palette:

- "Central icon in Primary (#0077B6)"
- "Accent shapes in Tertiary (#90E0EF)"

## Elements Inspiration

| Concept       | Possible Elements                                 |
| ------------- | ------------------------------------------------- |
| Growth        | Stairs, upward arrows, plants, charts trending up |
| Connection    | Nodes with lines, puzzle pieces, bridges          |
| Speed         | Motion lines, streamlined shapes, blur trails     |
| Security      | Shields, locks, enclosed spaces                   |
| Data          | Charts, grids, flowing streams, dashboards        |
| Creativity    | Lightbulbs, scattered shapes, color splashes      |
| Success       | Checkmarks, stars, trophies, peaks                |
| Communication | Speech bubbles, envelopes, signals                |

## Output Location

Save prompts and generated images to the content's `resources/` folder:

```
${CONTENT_FOLDER}/resources/
├── hero-prompt.md            # The composed prompt
├── hero.png                  # Generated image
└── ...
```
