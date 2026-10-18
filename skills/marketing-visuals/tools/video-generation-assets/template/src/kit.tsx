import React from 'react'
import { AbsoluteFill, Easing, interpolate, staticFile } from 'remotion'

// Brand tokens. Fill these from the project's visual-identity.md before writing the scene.
export const T = {
  bg: '#0a0a0a',
  surface: '#141414',
  ink: '#f3f1ed',
  ink2: '#a3a09a',
  ink3: '#8a8780',
  stroke: 'rgba(243,241,237,0.55)',
  accent: 'rgb(254,161,110)',
  accentDim: 'rgba(254,161,110,0.16)',
  display: 'Schibsted Grotesk',
  mono: 'Geist Mono',
}

// One entry per .woff2 in public/fonts/. Missing files fall back to system fonts silently,
// so check a still before rendering the full video.
const FONTS: { family: string; file: string; weight: string }[] = [
  { family: 'Schibsted Grotesk', file: 'SchibstedGrotesk-Variable-Latin.woff2', weight: '400 900' },
  { family: 'Geist Mono', file: 'GeistMono-Variable.woff2', weight: '100 900' },
]

export const FontFaces: React.FC = () => (
  <style>
    {FONTS.map((f) => `@font-face { font-family: '${f.family}'; src: url('${staticFile(`fonts/${f.file}`)}') format('woff2'); font-weight: ${f.weight}; }`).join('\n')}
  </style>
)

// ---------- timing ----------
export const clamp = { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' } as const

// 0 → 1 over `len` frames starting at `start`, eased out. Use for every entrance.
export const appear = (frame: number, start: number, len = 14) =>
  interpolate(frame, [start, start + len], [0, 1], { ...clamp, easing: Easing.out(Easing.cubic) })

// 0 → 1 between two frames, eased in and out. Use for scene transitions where figures travel.
export const travel = (frame: number, start: number, end: number) =>
  interpolate(frame, [start, end], [0, 1], { ...clamp, easing: Easing.bezier(0.65, 0, 0.35, 1) })

// Whole-video opacity: fades in from black and back out, so a GIF loop has no visible seam.
export const master = (frame: number, duration: number, fadeIn = 18, fadeOut = 30) =>
  Math.min(appear(frame, 0, fadeIn), interpolate(frame, [duration - fadeOut, duration - 2], [1, 0], clamp))

export const lerp = (a: number, b: number, t: number) => a + (b - a) * t
export type P = [number, number]
export const lerpP = (a: P, b: P, t: number): P => [lerp(a[0], b[0], t), lerp(a[1], b[1], t)]

// ---------- backdrop ----------
export const Backdrop: React.FC<{ opacity: number; children: React.ReactNode }> = ({ opacity, children }) => (
  <AbsoluteFill style={{ background: '#000' }}>
    <FontFaces />
    <AbsoluteFill style={{ opacity, background: T.bg }}>
      <AbsoluteFill style={{ background: 'radial-gradient(60% 70% at 50% 60%, rgba(254,161,110,0.06) 0%, rgba(254,161,110,0.015) 45%, transparent 72%)' }} />
      <AbsoluteFill style={{ backgroundImage: 'radial-gradient(circle, rgba(255,255,255,0.045) 1px, transparent 1px)', backgroundSize: '18px 18px' }} />
      {children}
    </AbsoluteFill>
  </AbsoluteFill>
)

// ---------- text ----------
// Headline that reveals word by word. Words from `accentFrom` on take the accent color.
export const Words: React.FC<{ words: string[]; frame: number; start: number; size: number; top: number; left?: number; accentFrom?: number }> = ({
  words, frame, start, size, top, left = 90, accentFrom,
}) => (
  <div style={{ position: 'absolute', top, left, right: left, fontFamily: T.display, fontWeight: 500, fontSize: size, letterSpacing: '-0.01em', textTransform: 'uppercase' }}>
    {words.map((w, i) => {
      const s = appear(frame, start + i * 5, 10)
      const accent = accentFrom !== undefined && i >= accentFrom
      return (
        <span key={i} style={{ display: 'inline-block', marginRight: '0.28em', opacity: s, transform: `translateY(${(1 - s) * 8}px)`, color: accent ? T.accent : s > 0.9 ? T.ink : T.ink3 }}>{w}</span>
      )
    })}
  </div>
)

// Small mono label inside the <svg>, positioned in absolute canvas coordinates.
export const Label: React.FC<{ at: P; text: string; show: number; color?: string; anchor?: 'middle' | 'end' | 'start'; size?: number }> = ({
  at, text, show, color = T.ink3, anchor = 'middle', size = 12,
}) => (
  <text x={at[0]} y={at[1]} textAnchor={anchor} fontFamily={T.mono} fontSize={size} letterSpacing="0.12em" fill={color} opacity={show}>
    {text.toUpperCase()}
  </text>
)

// ---------- figures ----------
// Places an SVG figure drawn around (0,0). Skips rendering when invisible.
export const Fig: React.FC<{ at: P; scale?: number; opacity?: number; children: React.ReactNode }> = ({ at, scale = 1, opacity = 1, children }) =>
  scale <= 0.001 || opacity <= 0.001 ? null : <g transform={`translate(${at[0]}, ${at[1]}) scale(${scale})`} opacity={opacity}>{children}</g>

// ---------- data flow ----------
const bez = (a: P, c: P, b: P, t: number): P => [
  (1 - t) * (1 - t) * a[0] + 2 * (1 - t) * t * c[0] + t * t * b[0],
  (1 - t) * (1 - t) * a[1] + 2 * (1 - t) * t * c[1] + t * t * b[1],
]

// Dots travelling a curved path from `a` to `b`, `count` in flight, one lap every `period` frames.
// `stopAt` (0-1) blocks them partway: each dot pops in an accent ring at that point.
export const Bubbles: React.FC<{
  a: P; b: P; bend?: number; frame: number; start: number; end?: number; count?: number; period?: number; color?: string; size?: number; stopAt?: number
}> = ({ a, b, bend = 0, frame, start, end = 1e9, count = 4, period = 40, color = T.ink, size = 5, stopAt }) => {
  if (frame < start || frame > end + period) return null
  const c: P = [(a[0] + b[0]) / 2, (a[1] + b[1]) / 2 + bend]
  return (
    <>
      {Array.from({ length: count }, (_, k) => {
        const born = start + (k * period) / count
        if (frame < born) return null
        const cycle = Math.floor((frame - born) / period)
        if (born + cycle * period > end) return null
        const u = ((frame - born) % period) / period
        if (stopAt !== undefined && u > stopAt) {
          const pop = (u - stopAt) / (1 - stopAt)
          if (pop > 0.35) return null
          const [x, y] = bez(a, c, b, stopAt)
          return <circle key={k} cx={x} cy={y} r={size + pop * 40} fill="none" stroke={T.accent} strokeWidth={2} opacity={1 - pop / 0.35} />
        }
        const [x, y] = bez(a, c, b, u)
        const o = Math.min(1, u * 8, (1 - u) * 8)
        return (
          <g key={k} opacity={o}>
            <circle cx={x} cy={y} r={size * 2.4} fill={color} opacity={0.12} />
            <circle cx={x} cy={y} r={size} fill={color} />
          </g>
        )
      })}
    </>
  )
}
