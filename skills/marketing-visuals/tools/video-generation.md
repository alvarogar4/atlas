# Video Generation

Short animated explainers (MP4 + looping GIF) written as React code with [Remotion](https://www.remotion.dev), rendered frame by frame, checked as stills before the full render.

**Use this for**: social-post animations, before/after flows, data moving through a system, a headline that builds word by word. One idea per video, 8-15 s.

**Don't use this for**: screen recordings, talking heads, anything with real footage or audio. Those need a video editor.

## Workflow

The helper is `{SKILLS_DIR}/marketing-visuals/tools/video-generation-assets/video.sh`. Call it `V` below.

1. **Read the visual identity** (`${PROJECT_PATH}/marketing/visual-identity.md`) and find the brand font files (`.woff2`). The template ships with dark Blueprint-style defaults; replace them with the project's.

2. **Write the storyboard first**, in the content folder as `resources/{name}-storyboard.md`: the one sentence the video says, then 3-5 beats with their time in seconds and what moves. A before/after is two beats plus the transition. Get the user's OK on the beats before animating if the post depends on them.

3. **Scaffold outside the brain** (the scratchpad), never in `resources/`:

   ```bash
   V new ${SCRATCH}/{name} /path/to/brand/fonts
   ```

   This copies the template (pinned Remotion 4.0.535, React 19), copies the fonts into `public/fonts/` and installs dependencies with bun.

4. **Set the tokens** in `src/kit.tsx`: colors in `T`, one `FONTS` entry per font file. Then write the scene in `src/Scene.tsx`: canvas size, `FPS`, `DURATION` and one named constant per beat at the top.

5. **Check stills before rendering** (MANDATORY). Render one frame per beat plus the transition midpoint, then `Read` the contact sheet:

   ```bash
   V stills ${SCRATCH}/{name} 10 60 130 200
   # → ${SCRATCH}/{name}/out/stills.png
   ```

   Fix layout here. A still takes seconds; a full render takes a minute.

6. **Render and verify the encoded output**:

   ```bash
   V render ${SCRATCH}/{name} {name}
   ```

   It writes `out/{name}.mp4` (h264, crf 18) and `out/{name}.gif` (every 2nd frame), prints sizes and the luma of the first and last GIF frame, and builds `out/gif-sheet.png` from 6 encoded frames. `Read` the sheet: GIF palettes can band gradients and drop faint dots that looked fine in the stills.

7. **Save into the content folder**:

   ```bash
   V save ${SCRATCH}/{name} ${CONTENT_FOLDER}/resources {name}
   ```

   Copies the MP4 and GIF, plus `resources/{name}-src/` (source, `package.json`, re-render README). Never `node_modules` or fonts.

8. **Write alt text** in the draft next to the visual line: what each beat shows, in order.

## Quality checks

Check every item on the stills and again on the GIF sheet. If one fails: edit, re-run stills, re-render.

**Story**
- One idea. A viewer with sound off and no caption gets it in one loop.
- The headline (`Words`) states the idea; labels name the parts; nothing else on screen is text.
- The before state reads as a problem on its own (blocked flow, missing piece), not as a neutral diagram.

**Motion**
- Everything derives from `useCurrentFrame()`. No `Math.random()`, CSS transitions or `setTimeout`: they render differently per frame or per worker.
- Entrances are staggered (`appear(frame, start + i * 5)`), never everything at once.
- Figures travel between beats (`travel` + `lerpP`) instead of cutting, so the viewer can follow what moved.
- Each beat holds still for at least 2 s after its last entrance, so it can be read.
- Loops (`Bubbles`) stop before the fade-out begins.

**Loop**
- The video fades in from black and out to black (`master`). `render` warns if the first or last GIF frame is not black: a GIF autoplays on loop and a hard cut shows as a glitch.

**Readability**
- Headline at least 40px, sub-headline 24px, labels 12px at 1200 wide. Scale up for 1080x1080 and 1080x1920.
- Labels sit clear of moving dots along their whole path, not only in the still you checked.
- One accent color, used for the thing the post is about.

**Figures**
- Solid filled shapes (`fill={T.surface}` plus a stroke) instead of outline icons; outlines disappear in GIF compression.
- No emoji, no logos of third parties unless the brand guide allows them.

## Formats and limits

| Channel    | File  | Canvas    | Notes                                                    |
| ---------- | ----- | --------- | -------------------------------------------------------- |
| X          | GIF   | 1200x675  | Autoplays and loops. Keep under 15 MB.                   |
| LinkedIn   | MP4   | 1200x675 or 1080x1080 | Plays inline. Upload as video, not document. |
| Story/Reel | MP4   | 1080x1920 | Keep text inside the middle 1080x1420.                   |
| Blog       | MP4   | 1200x675  | `<video autoplay muted loop playsinline>`, GIF as fallback. |

24 fps is enough for diagram motion and halves the GIF size against 30. If a GIF goes over the limit: shorten the video, re-render with `GIF_NTH=3 V render ...` (every 3rd frame), or shrink the dot-grid and glow areas, which are the most expensive to encode.

## Kit reference (`src/kit.tsx`)

| Export | What it does |
| --- | --- |
| `T`, `FONTS` | Brand tokens and font files. Edit per project. |
| `Backdrop` | Black base, brand background, glow and dot grid. Pass `opacity={master(frame, DURATION)}`. |
| `appear(frame, start, len)` | 0 → 1 eased entrance. |
| `travel(frame, start, end)` | 0 → 1 eased in and out, for figures moving between beats. |
| `master(frame, duration)` | Fade in from black and back out. |
| `lerp`, `lerpP` | Interpolate numbers and points. |
| `Words` | Headline revealed word by word, accent from a given word on. |
| `Label` | Uppercase mono label, inside the SVG. |
| `Fig` | Places an SVG figure drawn around (0,0) with scale and opacity. |
| `Bubbles` | Dots flowing along a curve between two points; `stopAt` makes them pop against a barrier. |

The template's `Scene.tsx` uses all of them. For a larger scene, start from a `resources/*-src/` folder this tool saved for an earlier post.

## File naming

```
{name}-storyboard.md   # Beats and timing
{name}.mp4             # LinkedIn, blog
{name}.gif             # X
{name}-src/            # Remotion source to re-render
```
