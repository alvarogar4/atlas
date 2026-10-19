import React from 'react'
import { Composition } from 'remotion'
import { DURATION, FORMATS, FPS, Scene } from './Scene'

// One composition per entry in FORMATS. Render one with COMP=<id> (default: Video).
export const Root: React.FC = () => (
  <>
    {Object.entries(FORMATS).map(([id, layout]) => (
      <Composition key={id} id={id} component={Scene} defaultProps={{ layout }} durationInFrames={DURATION} fps={FPS} width={layout.w} height={layout.h} />
    ))}
  </>
)
