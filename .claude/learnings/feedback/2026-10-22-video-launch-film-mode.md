---
date: "2026-10-22 13:24:34"
sha: "ce10704"
category: "missing-context"
status: applied
applied-date: "2026-10-22 13:29:49"
target: "skills/marketing-visuals/tools/launch-film.md"
change-type: "create"
observed-workflows:
  subagents: []
  skills: ["atlas:second-brain", "atlas:marketing-visuals", "compound:feedback"]
  commands: []
---

# Video tool only knows 8-15 s diagram loops; launch films come out as feature lists

## Observation

Alvaro shared a friend's launch video (Reforma Digital, @disamdev, 65 s, made with Opus + browser-use/video-use + HyperFrames, concept seeded from galleries of viral launch videos with an explicit "how much to follow the reference" dial). It tells a story: problem (AI assistants promised to do your paperwork) → old way failing on screen → twist → reveal → three pillars each proven by a demo beat → trust beat (personal data becomes `{{placeholders}}`) → claim → end card. One person, one task and one piece of data travel through the whole film; kinetic captions narrate; the ground colour carries the plot.

Our own chkit launch video (`projects/obsessiondb/work/marketing/content/2026-06-18_chkit-launch-posts/resources/chkit-launch-video.mp4`, 32 s) is the opposite: logo opener held ~5 s, small code panel floating in a dark void, a six-card feature grid, no tension, no viewer or task, ~5 s static holds.

The user wants the skill to learn from this: a launch-film mode with a story arc, reference intake, several storylines before building, a banned-defaults line, measured review checks, and a hand-off to HyperFrames for films.

## Context

Reviewing the friend's video and comparing it with the HyperFrames skill (`heygen-com/hyperframes` skills/hyperframes: references/story.md, spec.md, motion.md, review.md, types/launch.md) and the video-use SKILL.md (`browser-use/video-use`).

## Analysis

`marketing-visuals/tools/video-generation.md` is scoped to one-idea 8-15 s animations: a single storyboard of 3-5 beats, an optional reference step that only extracts style (palette, pacing, motion), a template whose `Backdrop` is black + glow + dot grid, and a blind review judged by eye. It has no guidance for a 20-60 s film: no story shape (hook, tension, reveal, proof, payoff, claim, end card), no spine (one viewer doing one real task), no alternative storylines, no list of the generated-video defaults to avoid (dark void with small floating UI, glow, card grids, logo opener), and no measured checks (read time per line, dead stretches, first frame as thumbnail, phone-width legibility). Without that context, a launch video defaults to a feature list with a logo on it.
