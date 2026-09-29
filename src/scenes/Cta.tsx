import React from 'react';
import {AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {brand, copy, theme} from '../config';
import {PopText, SceneFade, SparkBolt, SparkBurst, clamp} from '../components/ui';
import {MiniFigure} from '../components/MiniFigure';

/** 28–33 s: brand + single clear call to action. Ends on a warm high (peak-end). */
export const Cta: React.FC<{duration: number}> = ({duration}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const draw = interpolate(frame, [0, 16], [0, 1], clamp);
  const nameS = spring({frame: frame - 10, fps, config: {damping: 12, stiffness: 160}});
  const btnS = spring({frame: frame - 44, fps, config: {damping: 10, stiffness: 160}});
  const pulse = 1 + Math.max(0, Math.sin((frame - 60) / 6)) * 0.04 * (frame > 60 ? 1 : 0);
  const figS = spring({frame: frame - 26, fps, config: {damping: 10, stiffness: 140}});
  const wave = frame > 40 ? 0.75 + 0.25 * Math.sin(frame / 4) : 0;
  const footO = interpolate(frame, [60, 74], [0, 1], clamp);
  const contact = [brand.handle, brand.website].filter(Boolean).join('  ·  ');

  return (
    <SceneFade duration={duration} outFrames={1}>
      <AbsoluteFill style={{alignItems: 'center', top: 330}}>
        <div style={{display: 'flex', alignItems: 'center', gap: 18}}>
          <SparkBolt size={120} draw={draw} />
          <div
            style={{
              fontFamily: theme.headFont,
              fontWeight: 700,
              fontSize: 104,
              color: '#fff',
              letterSpacing: 1,
              opacity: nameS,
              transform: `translateX(${(1 - nameS) * 60}px)`,
              textShadow: `0 0 40px rgba(255,200,61,0.35)`,
            }}
          >
            {brand.name}
          </div>
        </div>
        <PopText text={copy.ctaTitle} size={86} delay={20} highlight={['mini', 'me']} style={{marginTop: 30, maxWidth: 940}} />
      </AbsoluteFill>

      <div style={{position: 'absolute', left: 540 - 150, top: 780, transformOrigin: '50% 100%', transform: `scale(${figS})`}}>
        <MiniFigure id="ctafig" width={300} layerLines wave={wave} />
      </div>
      <SparkBurst x={540} y={1000} delay={28} count={16} radius={360} />

      <div style={{position: 'absolute', top: 1270, left: 0, right: 0, display: 'flex', justifyContent: 'center', transform: `scale(${btnS * pulse})`}}>
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: 20,
            padding: '30px 56px',
            borderRadius: 999,
            background: `linear-gradient(135deg, #FFE07A, ${theme.spark})`,
            color: '#1B1446',
            fontFamily: theme.headFont,
            fontWeight: 700,
            fontSize: 60,
            boxShadow: '0 20px 50px rgba(255,200,61,0.45)',
          }}
        >
          📸 {copy.ctaButton} ➜
        </div>
      </div>
      <div style={{position: 'absolute', top: 1418, left: 0, right: 0, textAlign: 'center', opacity: footO, fontFamily: theme.bodyFont, fontWeight: 800, fontSize: 34, color: theme.muted}}>
        {contact ? <div style={{color: '#fff', fontSize: 44, marginBottom: 8}}>{contact}</div> : null}
        {copy.ctaFoot}
      </div>
    </SceneFade>
  );
};
