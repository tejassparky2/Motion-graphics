import React from 'react';
import {AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {copy, theme} from '../config';
import {BrandTag, Pill, PopText, SceneFade, SparkBurst, clamp} from '../components/ui';
import {MiniFigure} from '../components/MiniFigure';

const Callout: React.FC<{tx: number; ty: number; lx: number; ly: number; text: string; delay: number; align: 'left' | 'right'; color: string}> = ({
  tx,
  ty,
  lx,
  ly,
  text,
  delay,
  align,
  color,
}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const line = interpolate(frame, [delay, delay + 10], [0, 1], clamp);
  const pop = spring({frame: frame - delay - 6, fps, config: {damping: 11, stiffness: 180}});
  return (
    <>
      <svg width={1080} height={1920} style={{position: 'absolute', left: 0, top: 0}}>
        <line x1={tx} y1={ty} x2={tx + (lx - tx) * line} y2={ty + (ly - ty) * line} stroke={color} strokeWidth={5} strokeLinecap="round" />
        <circle cx={tx} cy={ty} r={12 * Math.min(1, line * 3)} fill={color} stroke="#fff" strokeWidth={4} />
      </svg>
      <div
        style={{
          position: 'absolute',
          top: ly - 36,
          ...(align === 'left' ? {right: 1080 - lx} : {left: lx}),
          transform: `scale(${pop})`,
          transformOrigin: align === 'left' ? '100% 50%' : '0% 50%',
        }}
      >
        <Pill size={38} bg={color} color="#150F3A">
          {text}
        </Pill>
      </div>
    </>
  );
};

/** 19–24 s: the reveal + personalisation cues ("your …"). */
export const Reveal: React.FC<{duration: number}> = ({duration}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const inS = spring({frame, fps, config: {damping: 10, stiffness: 120}});
  const float = Math.sin(frame / 14) * 12;
  const sway = Math.sin(frame / 22) * 2.5;
  const shine = interpolate(frame, [8, 40], [-60, 160], clamp);
  const wave = interpolate(frame, [60, 70, 80, 90, 100], [0, 1, 0.7, 1, 0], clamp);
  const [c1, c2, c3] = copy.callouts;
  const footS = spring({frame: frame - 84, fps, config: {damping: 12}});

  const fig = (id: string, extra?: React.CSSProperties) => (
    <div style={{position: 'absolute', left: 280, top: 600, ...extra}}>
      <MiniFigure id={id} width={520} layerLines wave={wave} />
    </div>
  );

  return (
    <SceneFade duration={duration} inFrames={0}>
      <BrandTag />
      <AbsoluteFill style={{alignItems: 'center', top: 380}}>
        <PopText text={copy.revealTitle} size={90} highlight={['your']} delay={2} />
      </AbsoluteFill>
      <div
        style={{
          position: 'absolute',
          left: 540 - 380,
          top: 760,
          width: 760,
          height: 760,
          borderRadius: 760,
          background: 'radial-gradient(circle, rgba(255,200,61,0.35) 0%, rgba(139,108,255,0.15) 45%, transparent 70%)',
        }}
      />
      <AbsoluteFill style={{transform: `translateY(${float + (1 - inS) * 200}px) rotate(${sway}deg) scale(${0.8 + 0.2 * inS})`, transformOrigin: '540px 1380px'}}>
        {fig('revealfig')}
        {/* light sweep, masked to a diagonal band */}
        {fig('revealshine', {
          filter: 'brightness(2.2) saturate(0.4)',
          opacity: 0.7,
          maskImage: `linear-gradient(115deg, transparent ${shine - 12}%, black ${shine}%, transparent ${shine + 12}%)`,
          WebkitMaskImage: `linear-gradient(115deg, transparent ${shine - 12}%, black ${shine}%, transparent ${shine + 12}%)`,
        })}
        <Callout tx={470} ty={700} lx={330} ly={640} text={c1} delay={26} align="left" color={theme.spark} />
        <Callout tx={548} ty={982} lx={790} ly={900} text={c3} delay={40} align="right" color={theme.coral} />
        <Callout tx={560} ty={1120} lx={350} ly={1210} text={c2} delay={54} align="left" color={theme.teal} />
      </AbsoluteFill>
      <SparkBurst x={540} y={950} delay={2} count={20} radius={480} />
      <div style={{position: 'absolute', top: 1410, left: 0, right: 0, display: 'flex', justifyContent: 'center', transform: `scale(${footS})`}}>
        <Pill size={40} bg="rgba(255,255,255,0.14)">
          🎨 {copy.revealFoot}
        </Pill>
      </div>
    </SceneFade>
  );
};
