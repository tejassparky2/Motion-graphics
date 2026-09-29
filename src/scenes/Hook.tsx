import React from 'react';
import {AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {copy, theme} from '../config';
import {MiniFigure} from '../components/MiniFigure';
import {BrandTag, PopText, SceneFade, SparkBurst, clamp} from '../components/ui';

/** 0–3 s: pattern-interrupt + self-reference hook. */
export const Hook: React.FC<{duration: number}> = ({duration}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const s = spring({frame, fps, config: {damping: 9, stiffness: 160, mass: 0.8}});
  const scale = 0.35 + 0.65 * s;
  // squash & stretch on landing
  const squash = 1 + Math.sin(Math.min(frame, 24) / 24 * Math.PI) * 0.08 * (1 - s * 0.5);
  const wave = interpolate(frame, [28, 36, 44, 52, 60, 68], [0, 1, 0.75, 1, 0.75, 1], clamp);
  const blink = interpolate(frame, [70, 73, 76], [0, 1, 0], clamp);
  const glow = 0.55 + 0.15 * Math.sin(frame / 6);
  return (
    <SceneFade duration={duration} inFrames={0}>
      <BrandTag opacity={interpolate(frame, [30, 45], [0, 1], clamp)} />
      <AbsoluteFill style={{alignItems: 'center', top: 380}}>
        <PopText text={copy.hookSmall} size={84} color={theme.muted} weight={600} delay={-6} />
        <PopText text={copy.hookBig} size={138} delay={10} highlight={['you']} style={{marginTop: 6}} />
      </AbsoluteFill>
      <div
        style={{
          position: 'absolute',
          left: 540 - 330,
          top: 1010 - 330,
          width: 660,
          height: 660,
          borderRadius: 660,
          background: `radial-gradient(circle, rgba(255,200,61,${glow * 0.55}) 0%, rgba(139,108,255,0.18) 45%, transparent 70%)`,
        }}
      />
      <div
        style={{
          position: 'absolute',
          left: 540 - 260,
          top: 700,
          transformOrigin: '50% 100%',
          transform: `scale(${scale * (2 - squash)}, ${scale * squash})`,
        }}
      >
        <MiniFigure id="hookfig" width={520} wave={wave} blink={blink} />
      </div>
      <SparkBurst x={540} y={1000} delay={4} count={18} radius={420} />
    </SceneFade>
  );
};
