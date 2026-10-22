---
name: marketing-visuals
description: Visual content creation - image processing, schema diagrams, AI image prompting, short animations and launch films. Use when creating visual assets for marketing content.
---

# Marketing Visuals

Consolidated visual content creation tools and guides.

## Decision Tree

| Need                                   | Tool                          | File                         |
| -------------------------------------- | ----------------------------- | ---------------------------- |
| Edit a photo (crop, enhance, optimize) | CLI processing tools          | `tools/processing.md`        |
| Create a diagram/schema/flowchart      | HTML+CSS → PNG via Playwright | `tools/schema-generation.md` |
| Compose an AI image generation prompt  | Prompt composition guide      | `guides/ai-prompting.md`     |
| Create an animation/video (MP4, GIF)   | React → MP4/GIF via Remotion  | `tools/video-generation.md`  |
| Create a launch/feature film (20-60 s) | Story first, HyperFrames or Remotion | `tools/launch-film.md` |

## Canvas Size Quick Reference

| Use Case                    | Size      | Ratio        |
| --------------------------- | --------- | ------------ |
| Blog header                 | 1200x600  | 2:1          |
| OG/Social card              | 1200x630  | 1.91:1       |
| Blog wide diagram           | 1200x800+ | varies       |
| Project card                | 1200x900  | 4:3          |
| Square (Instagram/LinkedIn) | 1080x1080 | 1:1          |
| Story (vertical)            | 1080x1920 | 9:16         |
| Hero background             | 1920x1080 | 16:9         |
| Social video (X, LinkedIn)  | 1200x675  | 16:9         |
| Thumbnail                   | 400x300   | 4:3          |
| Icon/avatar                 | 400x400   | 1:1          |
| Comparison (2 panels)       | 1200x660  | side-by-side |
| Comparison (detailed)       | 1456x1020 | more space   |

## Output Location

All visual assets go in the content's `resources/` folder:

```
${CONTENT_FOLDER}/resources/
├── hero-prompt.md              # AI prompt composition
├── hero.png                    # Generated/processed image
├── 01-architecture.html        # Schema source
├── 01-architecture.png         # Schema output
├── 02-agent-flow.mp4           # Video (LinkedIn, blog)
├── 02-agent-flow.gif           # Looping GIF (X)
├── 02-agent-flow-src/          # Remotion source to re-render
├── portrait_nobg.png           # Background removed
└── hero-processed.webp         # Optimized for web
```

Reference in content as: `./resources/{filename}`

## Workflow Chaining

Visual tools compose together for common workflows:

| Scenario         | Chain                                                                                           |
| ---------------- | ----------------------------------------------------------------------------------------------- |
| Blog hero image  | `guides/ai-prompting.md` → generate image → `tools/processing.md` (crop to 1200x600) → optimize |
| Schema diagram   | `tools/schema-generation.md` (HTML+CSS → PNG) → `tools/processing.md` (optimize)                |
| Photo for social | `tools/processing.md` (remove background → crop to 1080x1080 → polish → optimize)               |
| OG card          | `guides/ai-prompting.md` → generate → `tools/processing.md` (crop to 1200x630)                  |
| Social animation | storyboard → `tools/video-generation.md` (stills → blind review → render → save); a still frame doubles as the fallback image |
| Launch film      | `tools/launch-film.md`: reference sheet → three storylines → storyboard → build → measured + blind review → save |

Always read the project's visual identity first for brand colors and style defaults.

## Prerequisites

`{SKILLS_DIR}` in tool commands is the folder holding the Atlas skills, i.e. the parent of this skill's directory (`${CLAUDE_PLUGIN_ROOT}/skills` in Claude Code).

**Always read the project's visual identity first** (if it exists):

```bash
cat ${PROJECT_PATH}/marketing/visual-identity.md 2>/dev/null
```

Use brand colors as defaults for all visual creation.
