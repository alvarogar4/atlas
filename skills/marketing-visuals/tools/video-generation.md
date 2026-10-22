# Video Generation

Short animated explainers (MP4 + looping GIF) written as React code with [Remotion](https://www.remotion.dev), rendered frame by frame, checked as stills before the full render.

**Use this for**: social-post animations, before/after flows, data moving through a system, a headline that builds word by word. One idea per video, 8-15 s.

**Don't use this for**: screen recordings, talking heads, real footage or voice-over. Those need a video editor. A launch or feature film over about 15 s that tells a story: `launch-film.md`. Sound is optional and off by default (see [Sound (Optional)](#sound-optional)).

## Workflow

Run every command from the assets folder (no `bun install` needed here; `scaffold` installs Remotion in the working directory):

```bash
cd {SKILLS_DIR}/marketing-visuals/tools/video-generation-assets
```

`{NN}-{name}` below follows the content folder's numbering, shared with diagrams (`01-architecture.png`, `02-agent-flow.mp4`).

1. **Read the visual identity** (`${PROJECT_PATH}/marketing/visual-identity.md`) and find the brand font files (`.woff2`). The template ships with dark Blueprint-style defaults; replace them with the project's.

2. **Write the storyboard first**, in the content folder as `resources/{NN}-{name}-storyboard.md`. Get the user's OK on it before animating if the post depends on the beats.

   ```markdown
   Says: {the one sentence a viewer should remember}
   Formats: Video (1200x675) [, Square, Story]

   | Time  | Beat   | Entry state         | Exit state                 | Why it exists           |
   | ----- | ------ | ------------------- | -------------------------- | ----------------------- |
   | 0-2s  | Hook   | empty canvas        | headline + source A        | names the problem       |
   | 2-5s  | Flow   | A idle              | A's data reaching the store | shows the normal path  |
   | 5-8s  | Block  | B idle              | B's data stopped at a wall | the point of the post   |

   Sources: {where every number, screen and logo comes from}
   Reference: {optional, see below}
   ```

   - **3-5 beats.** A before/after is two beats plus the transition. A beat that can't fill "Why it exists" gets cut.
   - **Write states, not effects.** "B's data stopped at a wall" is a state; "zoom, then morph" is not. Figures move between known states.
   - **Never invent facts.** Every number, product screen, query and logo in the video traces to a line in `Sources:` (the post draft, a benchmark note, a real screenshot). If one is missing, stop and ask. Never draw a plausible stand-in.
   - **Reference (optional).** When the user gives a video, GIF or frame to match, look at it (`bun sheet ref.mp4` makes a one-frame-a-second contact sheet of a video) and write what it teaches: palette (hex), type, pacing (seconds between changes), motion (snap, glide, overshoot, cut, hold). Copy nothing of its subjects, copy or logos.

3. **Scaffold outside the brain** (the scratchpad), never in `resources/`:

   ```bash
   bun scaffold ${SCRATCH}/{NN}-{name} /path/to/brand/fonts
   ```

   This copies the template (pinned Remotion 4.0.535, React 19), copies the fonts into `public/fonts/` and installs dependencies with bun.

4. **Set the tokens** in `src/kit.tsx`: colors in `T`, one `FONTS` entry per font file. Then write the scene in `src/Scene.tsx`: `FPS`, `DURATION` and one named constant per beat at the top, then one `FORMATS` entry per format in the storyboard.

   Each format is its own composition with its own layout, never a crop or a scale of another. A 1080x1920 story needs larger figures and labels (`fig`, `label`), fewer elements side by side, a stacked flow and labels moved out of the dots' new path. The starter's `Video` and `Story` layouts show the difference. Remove formats the post doesn't use.

5. **Check stills before rendering** (MANDATORY). Render one frame per beat plus the transition midpoint, then `Read` the contact sheet. Then render a strip every 2 frames around the fastest transition: labels and moving dots collide between beats, not on them.

   ```bash
   bun stills ${SCRATCH}/{NN}-{name} 10 60 130 200
   bun stills ${SCRATCH}/{NN}-{name} 120 122 124 126 128 130
   COMP=Story bun stills ${SCRATCH}/{NN}-{name} 10 60 130 200   # every other format
   # each run → ${SCRATCH}/{NN}-{name}/out/stills.png (overwritten, Read it before the next run)
   ```

   Fix layout here. A still takes seconds; a full render takes a minute.

6. **Blind review** (MANDATORY). The agent that built the scene sees what it meant to draw. Hand the beat contact sheet of each format to a fresh subagent that has not seen the storyboard or the code, with this prompt:

   ```
   You are reviewing a short silent animation from its contact sheet.
   Contact sheet: {path to a copy of out/stills.png}
   Frames shown, left to right, top to bottom: {frames} ({FPS} fps). Canvas: {w}x{h}, viewed on {a phone / a laptop feed}.

   Read the image. Judge only what is rendered. You have not seen the brief or the code; do not look for them.
   1. In one sentence, say what this video communicates to a viewer with sound off and no caption.
   2. List the 3 largest defects, worst first. For each: the frame, the evidence (what you see and where
      on the canvas), and a local fix (what to change in that spot, not "redo the video").
   Check readability at that size, text inside the safe area, awkward mid-transition states, where the
   eye goes first, and one clear focus per frame. If fewer than 3 real defects exist, list fewer.
   ```

   - If its sentence doesn't match the storyboard's `Says:`, the story failed. Fix that before any polish.
   - Patch only the listed defects, then re-render the stills for the frames they touch.
   - Two review rounds at most. Defects still open after that go into the handoff (step 10), not into a third round.
   - If the harness can't spawn subagents, review the sheet yourself without re-reading the storyboard or `Scene.tsx` first.

7. **Render and verify the encoded output**:

   ```bash
   bun render ${SCRATCH}/{NN}-{name} {NN}-{name}
   COMP=Story bun render ${SCRATCH}/{NN}-{name} {NN}-{name}-story   # other formats: -{format} suffix
   ```

   It writes `out/{NN}-{name}.mp4` (h264, crf 18) and `out/{NN}-{name}.gif` (every 2nd frame), prints sizes and the luma of the first and last GIF frame, reports loudness when the scene has sound, and builds `out/gif-sheet.png` from 6 encoded frames. `Read` the sheet: GIF palettes can band gradients and drop faint dots that looked fine in the stills.

8. **Save into the content folder**:

   ```bash
   bun save ${SCRATCH}/{NN}-{name} ${CONTENT_FOLDER}/resources {NN}-{name}
   ```

   Copies the MP4 and GIF of every format rendered under that name, plus `resources/{NN}-{name}-src/` (source, `package.json`, audio files if any, re-render README). Never `node_modules` or fonts.

9. **Write alt text** in the draft next to the visual line: what each beat shows, in order.

10. **Hand off with what still needs a human**: defects left open after the review rounds, any `Sources:` line you could not verify, and, if the video has sound, that nobody has listened to it yet (an agent can't). The video is done when this list is empty or the user accepts it, not when the render command exits.

## Quality Checks

Check every item on the stills and again on the GIF sheet. If one fails: edit, re-run stills, re-render.

**Story**
- One idea. A viewer with sound off and no caption gets it in one loop: the blind reviewer's sentence matches `Says:`.
- Every beat has an entry state, an exit state and a reason in the storyboard.
- The headline (`Words`) states the idea; labels name the parts; nothing else on screen is text.
- The before state reads as a problem on its own (blocked flow, missing piece), not as a neutral diagram. Show it in the picture (a wall, a gap), not only in a label.

**Motion**
- Everything derives from `useCurrentFrame()`. No `Math.random()`, CSS transitions or `setTimeout`: they render differently per frame or per worker.
- Entrances are staggered (`appear(frame, start + i * 5)`), never everything at once.
- Figures travel between beats (`travel` + `lerpP`) instead of cutting, so the viewer can follow what moved.
- Each beat holds still for at least 2 s after its last entrance, so it can be read.
- Loops (`Bubbles`) stop before the fade-out begins.

**Loop**
- The video fades in from black and out to black (`master`). `render` warns if the first or last GIF frame is not black: a GIF autoplays on loop and a hard cut shows as a glitch.

**Facts**
- Every number, screen and logo matches a `Sources:` line in the storyboard.

**Readability**
- Headline at least 40px, sub-headline 24px, labels 12px at 1200 wide. A 1080x1920 story needs about 80px, 40px and 30px: set them in its `FORMATS` layout, don't scale the wide one.
- Labels sit clear of moving dots along their whole path, not only in the still you checked.
- One accent color, used for the thing the post is about.

**Figures**
- Solid filled shapes (`fill={T.surface}` plus a stroke) instead of outline icons; outlines disappear in GIF compression.
- No emoji, no logos of third parties unless the brand guide allows them.

## Formats and Limits

| Channel    | File  | Canvas    | `FORMATS` id | Notes                                                    |
| ---------- | ----- | --------- | ------------ | -------------------------------------------------------- |
| X          | GIF   | 1200x675  | `Video`      | Autoplays and loops. Keep under 15 MB. Always silent.    |
| LinkedIn   | MP4   | 1200x675 or 1080x1080 | `Video` / `Square` | Plays inline, muted until tapped. Upload as video, not document. |
| Story/Reel | MP4   | 1080x1920 | `Story`      | Keep text inside the middle 1080x1420, 60px+ from the sides. |
| Blog       | MP4   | 1200x675  | `Video`      | `<video autoplay muted loop playsinline>`, GIF as fallback. |

`Square` isn't in the starter; add it to `FORMATS` with its own layout when a post needs it.

24 fps is enough for diagram motion and halves the GIF size against 30. If a GIF goes over the limit: shorten the video, re-render with `GIF_NTH=3 bun render ...` (every 3rd frame), or shrink the dot-grid and glow areas, which are the most expensive to encode.

## Sound (Optional)

Off by default. X plays the GIF, which has no sound; LinkedIn and the blog autoplay muted. Every video must work muted, so sound only adds to it. Add it only when the user asks or supplies a track, typically for a blog or LinkedIn video people will unmute.

1. **Get the files**: a track the user supplies or licenses, or short cues you synthesize. Never download music without a license. A soft tick:

   ```bash
   ffmpeg -f lavfi -i "sine=frequency=1400:duration=0.04" -af "afade=t=out:st=0.01:d=0.03,volume=14dB" public/audio/tick.wav
   ```

2. **Put them on the picture's timeline** in `Scene.tsx`: `TRACK` for a music bed, `CUES` for one-off sounds. Each cue's `at` is a beat constant (`{ at: BLOCK_START, file: 'tick.wav' }`), never a raw number, so retiming a beat moves its sound with it. The track fades in and out with `master`.
3. **With music, cut to its beat.** Ask for the BPM. One beat lasts `FPS * 60 / BPM` frames (24 fps at 120 BPM = 12 frames), so set the beat constants on multiples of it.
4. **Check the numbers `render` prints.** For a music bed, aim for -16 to -14 LUFS integrated. Cue-only audio reads low on LUFS, so check that its peak sits between -10 and -1 dB (above -1 clips on phone speakers).
5. **Say in the handoff that nobody has listened to it yet.** Ask the user to listen once with their eyes closed: if it has no shape without the picture, the sound isn't finished.

## Kit Reference (`src/kit.tsx`)

| Export | What it does |
| --- | --- |
| `T`, `FONTS` | Brand tokens and font files. Edit per project. |
| `Backdrop` | Black base, brand background, glow and dot grid. Pass `opacity={master(frame, DURATION)}`. |
| `appear(frame, start, len)` | 0 → 1 eased entrance. |
| `travel(frame, start, end)` | 0 → 1 eased in and out, for figures moving between beats. |
| `master(frame, duration)` | Fade in from black and back out. |
| `lerp`, `lerpP` | Interpolate numbers and points. |
| `toward(a, b, d)` | The point `d` px from `a` towards `b`. Starts a flow at a figure's edge in any layout. |
| `Words` | Headline revealed word by word, accent from a given word on. |
| `Label` | Uppercase mono label, inside the SVG. |
| `Fig` | Places an SVG figure drawn around (0,0) with scale and opacity. |
| `Bubbles` | Dots flowing along a curve between two points; `stopAt` makes them pop against a barrier. |
| `pathAt(a, b, bend, t)` | Point along the same curve; put a visible barrier at `stopAt`. |
| `Soundtrack`, `Cue` | Optional sound: a track plus cues started at beat frames. Renders nothing when empty. |

The template's `Scene.tsx` uses all of them. For a larger scene, start from a `resources/*-src/` folder this tool saved for an earlier post.

## File Naming

```
{NN}-{description}-storyboard.md   # Says, beats with states, sources
{NN}-{description}.mp4             # LinkedIn, blog (Video format)
{NN}-{description}.gif             # X
{NN}-{description}-{format}.mp4    # Other formats: -story, -square
{NN}-{description}-src/            # Remotion source (+ audio/) to re-render
```

Examples:

- `02-agent-flow.mp4`
- `03-before-after-migration.gif`
