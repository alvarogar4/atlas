# Launch Film

A 20-60 s film that tells something: a product or feature launch, a release, a promo. The film is a story with one viewer doing one real task, not a list of features with a logo on it.

**Use this for**: anything over about 15 s that should make someone want the product. **Don't use this for**: a single idea in 8-15 s (a flow, a before/after, a headline): that is a loop, see `video-generation.md`.

The most common failure is good motion around no story: a logo opener, a code panel floating in a dark canvas, a grid of feature cards, a URL. Every step below exists to prevent that.

## Engine

- **HyperFrames** (preferred when installed): HeyGen's open-source HTML-to-video framework (Apache 2.0, Node 22+). Its `hyperframes` skill covers motion craft, transitions, a render contract and a measured review (`npx hyperframes check`, `snapshot --review`). Install it with `npx skills add heygen-com/hyperframes`. Atlas still owns steps 1-4 and 7-8 below. Hand HyperFrames the picked storyboard (with its `Says:`, spine, beats, `BANNED:` and `Sources:`) and the brand tokens, and tell it the story is decided, so it skips its own storyline step. Paid items (HeyGen voices, avatars, catalog music) only with the user's OK.
- **Remotion** (fallback, no new toolchain): the template from `video-generation.md`. Add a `Film` entry to `FORMATS` (1920x1080), set `FPS = 30`, and render the MP4 only with `GIF=0 COMP=Film bun render ...`. The kit's `Backdrop` (glow and dot grid) suits loops, not films: replace it with grounds taken from the brand (see `BANNED:` below).

Run the helper commands from `{SKILLS_DIR}/marketing-visuals/tools/video-generation-assets`, as for loops.

## Workflow

1. **Sources and brand.** Read the visual identity and collect the real material: the product's screens (screenshots or a recording, named per beat), the brand's logo and fonts, the copy the user approved. Everything that claims to be the product is the product. If a beat needs a screen you don't have, put a labelled placeholder ("Screenshot: Settings → Members") and ask for it. Never draw a plausible dashboard.

2. **Reference intake.** Most strong launch films start from a reference: the user sends one or picks one from a gallery of launch videos. Download it to the scratchpad and look at it:

   ```bash
   bun sheet ${SCRATCH}/ref.mp4      # → ref-sheet.png, one frame a second, plus frozen stretches
   ```

   `Read` the sheet and write the reference's beat map: time, act, what is on screen, how it moves to the next beat. Then write one adherence line per dimension, so the user can say how much to borrow:

   ```markdown
   Reference: {url}
   | Dimension   | Adherence           | Note                                   |
   | ----------- | ------------------- | -------------------------------------- |
   | Structure   | follow / adapt / no | e.g. problem → betrayal → reveal → ... |
   | Pacing      | follow / adapt / no | seconds per beat, holds                |
   | Transitions | follow / adapt / no | which kinds, what causes them          |
   | Look        | no                  | always the brand's                     |
   | Copy        | no                  | never; nor subjects or logos           |
   ```

   No reference: skip this step and say so in the storyboard.

3. **Three storylines, in words.** Write three that are three different films, not three titles for one film. Each picks a device and gives:
   - its device and, in two sentences, what the viewer sees and feels;
   - the first 2 s, exactly;
   - its beats in one line (`hook → … → end card`);
   - its sound in one line.

   | Device                  | What the viewer sees                                                                  |
   | ----------------------- | ------------------------------------------------------------------------------------- |
   | Before and after        | the old way failing as a scene (the 45-step guide, the error), then the new way      |
   | The result first        | the finished output plays, then the camera pulls back to show where it came from      |
   | A moment in someone's day | a person, a time, the message that creates the need ("the migration runs tonight") |
   | One object across tools | the thing being made travels from another tool into the product, which keeps working on it |
   | A number lands          | one real number, earned by a scene, then made physical                                |
   | Type carries it         | large kinetic type that cuts on the music, the product appearing in between           |

   Make one of the three the bold one. Recommend one with the reason in a clause, save all three as `resources/{NN}-{name}-storylines.md`, and stop until the user picks. With a reference at "Structure: follow", one storyline follows it and the other two don't.

4. **Storyboard.** Write `resources/{NN}-{name}-storyboard.md` for the picked storyline and get the user's OK before building:

   ```markdown
   Says: {the one thing a viewer remembers, in their words, not the slogan}
   Spine: {one viewer} does {one real task}; {one piece of data} travels from hook to payoff
   Formats: Film (1920x1080, 30 fps) [, Square, Story]
   Engine: HyperFrames | Remotion
   Sound: {music bed source and licence, or silent and why}

   | Time   | Beat    | Caption (≤ 6 words)        | On screen                     | Exit state → next beat     |
   | ------ | ------- | -------------------------- | ----------------------------- | -------------------------- |
   | 0-4s   | Hook    | AI assistants promised ... | prompt box, assistants' icons | icons fade, line resolves  |

   BANNED: {defaults below, plus anything this film must not become}
   Sources: {every screen, number, logo and quote → where it comes from}
   Reference: {adherence table from step 2, or "none"}
   ```

   **The shape.** A launch of about 35 s; scale it to the story, never pad it:

   | Beat     | Share | Job                                                                 |
   | -------- | ----- | ------------------------------------------------------------------- |
   | Hook     | ~8%   | the need, or the feature already working on something recognisable |
   | Tension  | ~12%  | the old way failing on screen                                      |
   | Reveal   | ~8%   | the product named, 20-30% in ("Introducing" is fine after the pain) |
   | Proof    | ~40%  | the real task in the real UI as 3-6 verbs, one beat each           |
   | Payoff   | ~20%  | the result arrives, at normal speed: the biggest moment, once      |
   | Claim    | ~8%   | the one thing, in one line                                         |
   | End card | ~8%   | the mark lands, then the call to action holds 2-3 s                |

   - **The spine** carries the film. A named person renewing her ID, a query that goes from failing to 1.4 s: the same data shows up in the hook, the proof and the payoff. A feature that matters to buyers (privacy, permissions, cost) gets its own proof beat that shows it working, not a card that claims it.
   - **Captions narrate.** One line at a time, at most 6 words, built word by word with one accent word. They carry the story on mute, so product text can stay small. A line holds 0.5 s plus 0.3 s a word; the last line at least 2 s.
   - **Grounds carry the plot.** Change the ground when the story turns (problem, product, turn), within the brand's palette, and enter each new ground through something already on screen (the clicked icon opens into the next scene).
   - **Product on screen.** Rebuild only the part the beat uses (the panel, the row that changes) at 1.6-2× its real size, with text at least 26 px at 1080p. Never a small window in the middle of an empty canvas.
   - **The first frame is the thumbnail** on X and LinkedIn: it shows the hook, never black and never the logo alone.
   - **Copy** follows `atlas:humanizer`: no "unlock", "seamless", "supercharge", "in seconds" unless measured. Real numbers only, from `Sources:`.

5. **Build.** Hand off to HyperFrames, or build in Remotion with stills per beat as in `video-generation.md` step 5. Motion rules for Remotion builds:
   - something new every 2-4 s; a demo may hold one framing for 7-10 s while the UI acts;
   - a landed title holds still until it leaves; exits are about half as long as entrances;
   - vary how titles enter (word by word, blur in, grey to ink), never the same fade-and-slide on every line;
   - 3-5 kinds of transition, each caused by something on screen (a click, a zoom through a button, a colour flood).

6. **Review, measured then blind.** After the first full render:

   ```bash
   bun sheet ${SCRATCH}/{NN}-{name}/out/{NN}-{name}.mp4        # film sheet, frozen stretches, first frame
   bun sheet ${SCRATCH}/{NN}-{name}/out/{NN}-{name}.mp4 360    # phone width: every caption still readable?
   ```

   | Check            | Passes when                                                                          |
   | ---------------- | ------------------------------------------------------------------------------------ |
   | Dead stretches   | `frozen 3 s+` is empty, or each stretch is a deliberate hold named in the storyboard |
   | First frame      | no black warning, and frame 0 shows the hook                                        |
   | Read time        | every caption is on screen for 0.5 s + 0.3 s a word (check against the beat table)  |
   | Phone sheet      | every caption reads at 360 px wide                                                  |
   | Words alone      | the captions, read in order as plain text, make the pitch to a stranger             |
   | BANNED           | no default from the list below appears; any new one found goes into `BANNED:`       |

   Then the blind review from `video-generation.md` step 6, with the film sheet and the phone sheet. Add to the prompt: "Say which beat is the weakest and whether you would watch to the end." If its sentence doesn't match `Says:`, fix the story before anything else. Two rounds at most.

7. **Save.** Remotion: `bun save` as for loops. HyperFrames: copy the MP4 into `resources/` and the project (without `node_modules` and `renders/`) into `resources/{NN}-{name}-src/`.

8. **Hand off** as in `video-generation.md` step 10: open defects, placeholders still waiting for a real screen, unverified sources, and that nobody has listened to the sound.

## BANNED by default

Generated films fall into these when nothing else is decided. Each is banned unless the brand's own visual identity or the reference uses it, and then only as they use it:

- a small window or code panel floating in the middle of an empty canvas (the hero fills at least 40% of the frame);
- glow, orbs, particles or a dot grid as decoration;
- the logo as the opener, or docked in a corner during the film;
- a grid of feature cards, three cards in a row, a title over a dimmed screenshot;
- every element fading and sliding up; text moving while it is read;
- typing into a prompt box as the opener with nothing else on screen (a few seconds in, as a story step, it's fine);
- an invented screen, button or number.

## Worked example

Reforma Digital's desktop launch (@disamdev, Oct 2026, 65 s), built with Opus, video-use and HyperFrames from a reference gallery of viral launch films:

| Time   | Beat     | What happens                                                                                  |
| ------ | -------- | --------------------------------------------------------------------------------------------- |
| 0-5s   | Hook     | "AI assistants promised to do your paperwork", typed, with the assistants' icons (dark ground) |
| 5-11s  | Tension  | "Instead, they give you" 45 step cards, then "I can't book it for you, fill in the form yourself" |
| 11-15s | Turn     | "And to help, you give them your data"                                                        |
| 15-19s | Reveal   | the app icon in the dock opens into the red brand card                                        |
| 19-48s | Proof    | three pillars (official sites, your data, your permission), then one beat each: Lucía renews her ID card in Sevilla, the agent fills the form and asks before booking (light ground) |
| 48-57s | Proof    | her name and ID number turn into `{{placeholders}}`: "The AI only sees placeholders"         |
| 57-65s | Claim, end card | "Your paperwork, done with you" (dark ground), then the brand card with the URL         |

It works because of the spine (one person, one task, her data in the demo and in the trust beat), captions that narrate every beat, and grounds that change with the story. Its weak spots by the rules above: the prompt-box opener, a three-pillar list before the proof, and product text too small to read in a feed.
