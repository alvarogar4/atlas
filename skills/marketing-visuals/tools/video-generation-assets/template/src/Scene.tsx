import React from 'react'
import { useCurrentFrame } from 'remotion'
import { appear, Backdrop, Bubbles, Cue, Fig, Label, master, P, pathAt, Soundtrack, T, toward, Words } from './kit'

// Timeline. Every beat is a named frame so retiming means editing one line.
export const FPS = 24
export const DURATION = 240 // 10 s
const FLOW_START = 48
const BLOCK_START = 120

// One composition per format, each with its own layout. Never crop or scale one format into
// another: vertical gets bigger type and a stacked flow, so labels move out of the dots' path.
export type Layout = {
  w: number; h: number
  head: { size: number; top: number; left: number }
  fig: number; label: number // figure scale and label size: phone-sized formats need both larger
  A: P; B: P; S: P // positions of the figures
  la: P; lb: P; ls: P // positions of their labels
}
export const FORMATS: Record<string, Layout> = {
  Video: {
    w: 1200, h: 675, head: { size: 46, top: 46, left: 90 }, fig: 1, label: 12,
    A: [300, 330], B: [300, 520], S: [860, 420],
    la: [300, 392], lb: [300, 582], ls: [860, 526],
  },
  Story: {
    w: 1080, h: 1920, head: { size: 84, top: 300, left: 90 }, fig: 2.2, label: 34,
    A: [300, 820], B: [780, 820], S: [540, 1320],
    la: [300, 720], lb: [780, 720], ls: [540, 1524],
  },
}

// Sound is off by default. To add it, put files in public/audio/ and fill these
// (see "Sound (Optional)" in video-generation.md). Cues start at beat constants, never raw numbers.
const TRACK: string | undefined = undefined
const CUES: Cue[] = [] // e.g. [{ at: BLOCK_START, file: 'tick.wav' }]

// Starter scene: a source sends data to a store, then a second source gets blocked.
// Replace it with the story of the post: one idea, one before/after or one flow.

function Source() {
  return (
    <g>
      <rect x={-44} y={-32} width={88} height={64} rx={6} fill={T.surface} stroke={T.stroke} strokeWidth={1.5} />
      <line x1={-44} y1={-16} x2={44} y2={-16} stroke={T.stroke} strokeWidth={1} />
      <text x={-30} y={14} fontFamily={T.mono} fontSize={14} fill={T.ink2}>{'>_'}</text>
    </g>
  )
}

function Store({ glow }: { glow: number }) {
  return (
    <g>
      <rect x={-70} y={-70} width={140} height={140} rx={14} fill={T.accentDim} stroke={T.accent} strokeWidth={2} />
      <rect x={-78} y={-78} width={156} height={156} rx={18} fill="none" stroke={T.accent} strokeOpacity={0.25 * glow} strokeWidth={1.5} />
    </g>
  )
}

// A wall across the flow, so "blocked" shows in the picture and not only in a label.
function Barrier({ at, angle }: { at: P; angle: number }) {
  return (
    <g transform={`translate(${at[0]}, ${at[1]}) rotate(${angle})`}>
      <rect x={-4} y={-34} width={8} height={68} rx={4} fill={T.accent} />
    </g>
  )
}

export const Scene: React.FC<{ layout: Layout }> = ({ layout: L }) => {
  const frame = useCurrentFrame()
  const { A, B, S } = L
  const b0 = toward(B, S, 56 * L.fig)
  const b1 = toward(S, B, 90 * L.fig)
  const wall = pathAt(b0, b1, 20, 0.55)

  return (
    <Backdrop opacity={master(frame, DURATION)}>
      <Soundtrack track={TRACK} cues={CUES} duration={DURATION} />
      <Words words={['One', 'clear', 'idea.']} frame={frame} start={14} size={L.head.size} top={L.head.top} left={L.head.left} accentFrom={1} />
      <svg width={L.w} height={L.h} style={{ position: 'absolute', inset: 0 }}>
        <Bubbles a={toward(A, S, 56 * L.fig)} b={toward(S, A, 90 * L.fig)} bend={-20} frame={frame} start={FLOW_START} count={4} period={36} size={5 * L.fig} />
        <Bubbles a={b0} b={b1} bend={20} frame={frame} start={BLOCK_START} count={3} period={40} stopAt={0.55} size={5 * L.fig} />
        <Fig at={wall} scale={appear(frame, BLOCK_START + 10) * L.fig}><Barrier at={[0, 0]} angle={(Math.atan2(b1[1] - b0[1], b1[0] - b0[0]) * 180) / Math.PI} /></Fig>
        <Fig at={A} scale={appear(frame, 18) * L.fig}><Source /></Fig>
        <Fig at={B} scale={appear(frame, BLOCK_START - 14) * L.fig}><Source /></Fig>
        <Fig at={S} scale={appear(frame, 30, 16) * L.fig}><Store glow={0.5 + 0.5 * Math.sin(frame / 8)} /></Fig>
        <Label at={L.la} text="Source A" show={appear(frame, 26)} size={L.label} />
        <Label at={L.lb} text="Source B · blocked" show={appear(frame, BLOCK_START + 10)} color={T.accent} size={L.label} />
        <Label at={L.ls} text="Store" show={appear(frame, 40)} color={T.ink} size={L.label + 1} />
      </svg>
    </Backdrop>
  )
}
