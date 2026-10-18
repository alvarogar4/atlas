import React from 'react'
import { Composition } from 'remotion'
import { DURATION, FPS, H, Scene, W } from './Scene'

export const Root: React.FC = () => (
  <Composition id="Video" component={Scene} durationInFrames={DURATION} fps={FPS} width={W} height={H} />
)
