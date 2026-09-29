import React from 'react';
import {AbsoluteFill, interpolate, random, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {copy, theme} from '../config';
import {BrandTag, Pill, PopText, SceneFade, clamp} from '../components/ui';
import {MiniFigure, FigureLook} from '../components/MiniFigure';

const CAST: {look: FigureLook; x: number; w: number; delay: number}[] = [
  {look: {hairStyle: 'long', hair: '#6B3E2E', shirt: '#2EC4B6', pants: '#3A3D6B', shoes: '#FF6B6B', bolt: false}, x: 300, w: 330, delay: 18},
  {look: {kind: 'dog'}, x: 540, w: 250, delay: 30},
  {look: {hairStyle: 'short', glasses: true, beard: true, shirt: '#8B6CFF', pants: '#2F3142', skin: '#E0A980', bolt: false}, x: 780, w: 330, delay: 24},
];

/** 24–28 s: gifting emotion – vicarious pride & "I see you". */
export const Gift: React.FC<{duration: number}> = ({duration}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const blink = interpolate(frame, [80, 83, 86], [0, 1, 0], clamp);
  return (
    <SceneFade duration={duration} inFrames={6}>
      <BrandTag />
      <AbsoluteFill style={{alignItems: 'center', top: 370}}>
        <PopText text={copy.giftTitleA} size={80} weight={600} color={theme.muted} />
        <PopText text={copy.giftTitleB} size={132} delay={8} color={theme.spark} />
      </AbsoluteFill>

      {/* floating hearts */}
      {new Array(10).fill(0).map((_, i) => {
        const t = (frame - i * 7) / 70;
        if (t < 0 || t > 1) return null;
        const x = 140 + random(`h${i}`) * 800;
        return (
          <div key={i} style={{position: 'absolute', left: x, top: 1250 - t * 600, fontSize: 40 + random(`hs${i}`) * 30, opacity: Math.sin(t * Math.PI), transform: `rotate(${Math.sin(t * 6 + i) * 15}deg)`}}>
            {i % 3 === 0 ? '💛' : i % 3 === 1 ? '🧡' : '💜'}
          </div>
        );
      })}

      {CAST.map((c, i) => {
        const s = spring({frame: frame - c.delay, fps, config: {damping: 10, stiffness: 150}});
        const h = c.w * 1.5;
        return (
          <div
            key={i}
            style={{
              position: 'absolute',
              left: c.x - c.w / 2,
              top: 1330 - h,
              transformOrigin: '50% 100%',
              transform: `translateY(${(1 - s) * 500}px) scale(${0.7 + 0.3 * s}) rotate(${Math.sin((frame + i * 20) / 12) * 2}deg)`,
              zIndex: i === 1 ? 2 : 1,
            }}
          >
            <MiniFigure id={`gift${i}`} width={c.w} look={c.look} layerLines blink={blink} wave={i === 2 ? interpolate(frame, [50, 60, 70, 80], [0, 1, 0.7, 1], clamp) : 0} />
          </div>
        );
      })}

      {/* occasions */}
      <div style={{position: 'absolute', top: 1360, left: 40, right: 40, display: 'flex', flexWrap: 'wrap', justifyContent: 'center', gap: 14}}>
        {copy.occasions.map((o, i) => {
          const s = spring({frame: frame - 40 - i * 5, fps, config: {damping: 12, stiffness: 200}});
          return (
            <div key={o} style={{transform: `scale(${s})`}}>
              <Pill size={34}>{o}</Pill>
            </div>
          );
        })}
      </div>
    </SceneFade>
  );
};
