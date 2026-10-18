import React from 'react'
import { useCurrentFrame } from 'remotion'
import { appear, Backdrop, Bubbles, Fig, Label, master, P, T, Words } from './kit'

// Canvas and timeline. Every beat is a named frame so retiming means editing one line.
export const W = 1200
export const H = 675
export const FPS = 24
export const DURATION = 240 // 10 s
const FLOW_START = 48
const BLOCK_START = 120

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

export const Scene: React.FC = () => {
  const frame = useCurrentFrame()
  const A: P = [300, 330]
  const B: P = [300, 520]
  const S: P = [860, 420]

  return (
    <Backdrop opacity={master(frame, DURATION)}>
      <Words words={['One', 'clear', 'idea.']} frame={frame} start={14} size={46} top={46} accentFrom={1} />
      <svg width={W} height={H} style={{ position: 'absolute', inset: 0 }}>
        <Bubbles a={[A[0] + 50, A[1]]} b={[S[0] - 80, S[1] - 20]} bend={-20} frame={frame} start={FLOW_START} count={4} period={36} />
        <Bubbles a={[B[0] + 50, B[1]]} b={[S[0] - 80, S[1] + 20]} bend={20} frame={frame} start={BLOCK_START} count={3} period={40} stopAt={0.55} />
        <Fig at={A} scale={appear(frame, 18)}><Source /></Fig>
        <Fig at={B} scale={appear(frame, BLOCK_START - 14)}><Source /></Fig>
        <Fig at={S} scale={appear(frame, 30, 16)}><Store glow={0.5 + 0.5 * Math.sin(frame / 8)} /></Fig>
        <Label at={[A[0], A[1] + 62]} text="Source A" show={appear(frame, 26)} />
        <Label at={[B[0], B[1] + 62]} text="Source B · blocked" show={appear(frame, BLOCK_START)} color={T.accent} />
        <Label at={[S[0], S[1] + 106]} text="Store" show={appear(frame, 40)} color={T.ink} size={13} />
      </svg>
    </Backdrop>
  )
}
