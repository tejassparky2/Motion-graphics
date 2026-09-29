import React from 'react';
import {AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig, Easing} from 'remotion';
import {copy, theme} from '../config';
import {BrandTag, Pill, PopText, SceneFade, clamp} from '../components/ui';
import {Portrait} from '../components/Portrait';
import {MiniFigure} from '../components/MiniFigure';

const Num: React.FC<{n: number; color: string}> = ({n, color}) => (
  <span
    style={{
      display: 'inline-flex',
      width: 84,
      height: 84,
      borderRadius: 84,
      background: color,
      color: '#1B1446',
      alignItems: 'center',
      justifyContent: 'center',
      fontFamily: theme.headFont,
      fontWeight: 700,
      fontSize: 56,
      marginBottom: 14,
    }}
  >
    {n}
  </span>
);

/** 7–11 s: how it works – photo in, sculpt out. Keeps effort feeling tiny. */
export const Steps: React.FC<{duration: number}> = ({duration}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const move = interpolate(frame, [0, 22], [0, 1], {...clamp, easing: Easing.inOut(Easing.cubic)});
  const arrow = interpolate(frame, [30, 46], [0, 1], clamp);
  const sculpt = spring({frame: frame - 40, fps, config: {damping: 14, stiffness: 120}});
  const build = interpolate(frame, [42, 92], [0, 1], {...clamp, easing: Easing.inOut(Easing.quad)});
  const secondLine = frame >= 40;
  const approve = copy.showPreviewApproval ? spring({frame: frame - 86, fps, config: {damping: 12}}) : 0;
  const outline = '#2EC4B6';
  const scanY = 1270 - 522 * build;

  return (
    <SceneFade duration={duration} inFrames={0}>
      <BrandTag />
      <AbsoluteFill style={{alignItems: 'center', top: 360}}>
        {!secondLine ? (
          <div style={{display: 'flex', flexDirection: 'column', alignItems: 'center'}}>
            <Num n={1} color={theme.spark} />
            <PopText text={copy.step1} size={96} highlight={['one', 'photo']} />
          </div>
        ) : (
          <div style={{display: 'flex', flexDirection: 'column', alignItems: 'center'}}>
            <Num n={2} color={theme.teal} />
            <PopText text={copy.step2} size={96} delay={40} highlight={['mini', 'me']} highlightColor={theme.teal} />
          </div>
        )}
      </AbsoluteFill>

      {/* customer photo slides left */}
      <div
        style={{
          position: 'absolute',
          left: interpolate(move, [0, 1], [540, 290]),
          top: interpolate(move, [0, 1], [1000, 1010]),
          transform: `translate(-50%, -50%) scale(${interpolate(move, [0, 1], [1, 0.74])}) rotate(${interpolate(move, [0, 1], [-6, -4])}deg)`,
        }}
      >
        <Portrait size={420} />
      </div>

      {/* arrow */}
      <svg width={200} height={120} style={{position: 'absolute', left: 440, top: 950}} viewBox="0 0 200 120">
        <path
          d="M10 70 Q100 10 180 60"
          stroke={theme.spark}
          strokeWidth={12}
          strokeLinecap="round"
          fill="none"
          pathLength={1}
          strokeDasharray={1}
          strokeDashoffset={1 - arrow}
        />
        <path d="M160 34 L186 62 L150 76" stroke={theme.spark} strokeWidth={12} strokeLinecap="round" strokeLinejoin="round" fill="none" opacity={arrow > 0.9 ? 1 : 0} />
      </svg>

      {/* digital sculpt */}
      <div
        style={{
          position: 'absolute',
          left: 800 - 190,
          top: 700,
          opacity: interpolate(sculpt, [0, 0.3], [0, 1], clamp),
          transform: `scale(${0.6 + 0.4 * sculpt})`,
          transformOrigin: '50% 100%',
          filter: `grayscale(1) brightness(1.35) drop-shadow(3px 0 0 ${outline}) drop-shadow(-3px 0 0 ${outline}) drop-shadow(0 3px 0 ${outline}) drop-shadow(0 -3px 0 ${outline}) drop-shadow(0 0 24px ${outline})`,
        }}
      >
        <MiniFigure id="sculptfig" width={380} print={build} />
      </div>
      {build > 0 && build < 1 && (
        <div style={{position: 'absolute', left: 600, width: 400, top: scanY, height: 6, borderRadius: 6, background: outline, boxShadow: `0 0 30px 8px ${outline}`}} />
      )}
      <div style={{position: 'absolute', top: 640, left: 800, transform: `translateX(-50%) scale(${sculpt})`}}>
        <Pill size={32} bg="rgba(46,196,182,0.2)">3D sculpt</Pill>
      </div>

      {copy.showPreviewApproval && (
        <div style={{position: 'absolute', top: 1340, left: 0, right: 0, display: 'flex', justifyContent: 'center', transform: `scale(${approve})`}}>
          <Pill size={44} bg="rgba(46,196,182,0.9)" color="#0C0A24">
            ✓ {copy.step2b}
          </Pill>
        </div>
      )}
    </SceneFade>
  );
};
