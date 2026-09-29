import React from 'react';
import {AbsoluteFill, interpolate, random, spring, useCurrentFrame, useVideoConfig, Easing} from 'remotion';
import {theme} from '../config';

export const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;

export const usePop = (delay = 0, config = {damping: 11, stiffness: 170, mass: 0.7}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  return spring({frame: frame - delay, fps, config});
};

/** Fade + slide wrapper for whole scenes. */
export const SceneFade: React.FC<{duration: number; children: React.ReactNode; inFrames?: number; outFrames?: number}> = ({
  duration,
  children,
  inFrames = 8,
  outFrames = 8,
}) => {
  const frame = useCurrentFrame();
  const opacity =
    inFrames > 0
      ? interpolate(frame, [0, inFrames, duration - outFrames, duration], [0, 1, 1, 0], clamp)
      : interpolate(frame, [duration - outFrames, duration], [1, 0], clamp);
  const scale = interpolate(frame, [duration - outFrames, duration], [1, 1.06], {...clamp, easing: Easing.in(Easing.quad)});
  return <AbsoluteFill style={{opacity, transform: `scale(${scale})`}}>{children}</AbsoluteFill>;
};

export const Background: React.FC = () => {
  const frame = useCurrentFrame();
  const {width, height} = useVideoConfig();
  const sparks = new Array(26).fill(0).map((_, i) => {
    const x = random(`x${i}`) * width;
    const speed = 0.6 + random(`s${i}`) * 1.6;
    const y = (height + 60 - ((frame * speed + random(`y${i}`) * height) % (height + 120)));
    const size = 3 + random(`r${i}`) * 7;
    const hue = [theme.spark, theme.coral, theme.teal, theme.violet][i % 4];
    const tw = 0.35 + 0.35 * Math.sin(frame / 9 + i);
    return <div key={i} style={{position: 'absolute', left: x, top: y, width: size, height: size, borderRadius: size, background: hue, opacity: tw, boxShadow: `0 0 ${size * 3}px ${hue}`}} />;
  });
  return (
    <AbsoluteFill style={{background: `radial-gradient(120% 80% at 50% 38%, ${theme.bgTop} 0%, ${theme.bgBottom} 70%)`}}>
      <AbsoluteFill
        style={{
          backgroundImage: 'radial-gradient(rgba(255,255,255,0.09) 2px, transparent 2.5px)',
          backgroundSize: '44px 44px',
          backgroundPosition: `0px ${(frame * 0.5) % 44}px`,
          maskImage: 'radial-gradient(80% 60% at 50% 45%, black 20%, transparent 80%)',
          WebkitMaskImage: 'radial-gradient(80% 60% at 50% 45%, black 20%, transparent 80%)',
        }}
      />
      {sparks}
      <AbsoluteFill style={{background: 'radial-gradient(100% 70% at 50% 50%, transparent 55%, rgba(0,0,0,0.55) 100%)'}} />
    </AbsoluteFill>
  );
};

type TextProps = {
  size?: number;
  color?: string;
  delay?: number;
  weight?: number;
  font?: 'head' | 'body';
  style?: React.CSSProperties;
  from?: 'up' | 'scale' | 'none';
};

/** Headline that pops in word-by-word. */
export const PopText: React.FC<TextProps & {text: string; highlight?: string[]; highlightColor?: string; stagger?: number}> = ({
  text,
  size = 96,
  color = theme.ink,
  delay = 0,
  weight = 700,
  font = 'head',
  style,
  highlight = [],
  highlightColor = theme.spark,
  stagger = 3,
}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const words = text.split(' ');
  return (
    <div
      style={{
        fontFamily: font === 'head' ? theme.headFont : theme.bodyFont,
        fontSize: size,
        fontWeight: weight,
        color,
        lineHeight: 1.08,
        textAlign: 'center',
        display: 'flex',
        flexWrap: 'wrap',
        justifyContent: 'center',
        columnGap: size * 0.26,
        textShadow: '0 6px 24px rgba(0,0,0,0.45)',
        ...style,
      }}
    >
      {words.map((w, i) => {
        const s = spring({frame: frame - delay - i * stagger, fps, config: {damping: 12, stiffness: 200, mass: 0.6}});
        const clean = w.replace(/[^\p{L}\p{N}]/gu, '').toLowerCase();
        const hl = highlight.map((h) => h.toLowerCase()).includes(clean);
        return (
          <span
            key={i}
            style={{
              display: 'inline-block',
              opacity: interpolate(s, [0, 0.4], [0, 1], clamp),
              transform: `translateY(${(1 - s) * size * 0.55}px) scale(${0.7 + 0.3 * s})`,
              color: hl ? highlightColor : undefined,
            }}
          >
            {w}
          </span>
        );
      })}
    </div>
  );
};

export const Pill: React.FC<{children: React.ReactNode; bg?: string; color?: string; size?: number; style?: React.CSSProperties}> = ({
  children,
  bg = 'rgba(255,255,255,0.12)',
  color = theme.ink,
  size = 40,
  style,
}) => (
  <div
    style={{
      display: 'inline-flex',
      alignItems: 'center',
      gap: 14,
      padding: `${size * 0.35}px ${size * 0.7}px`,
      borderRadius: 999,
      background: bg,
      color,
      fontFamily: theme.bodyFont,
      fontWeight: 800,
      fontSize: size,
      border: '2px solid rgba(255,255,255,0.18)',
      backdropFilter: 'blur(6px)',
      whiteSpace: 'nowrap',
      ...style,
    }}
  >
    {children}
  </div>
);

/** Brand spark bolt icon. */
export const SparkBolt: React.FC<{size: number; draw?: number; color?: string}> = ({size, draw = 1, color = theme.spark}) => (
  <svg viewBox="0 0 100 100" width={size} height={size} style={{overflow: 'visible'}}>
    <defs>
      <linearGradient id="boltGrad" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0" stopColor="#FFE07A" />
        <stop offset="1" stopColor={color} />
      </linearGradient>
    </defs>
    <path
      d="M58 4 L18 58 L46 58 L38 96 L82 38 L54 38 Z"
      fill="url(#boltGrad)"
      stroke="#FFF3C4"
      strokeWidth={3}
      strokeLinejoin="round"
      pathLength={1}
      strokeDasharray={1}
      strokeDashoffset={1 - draw}
      fillOpacity={interpolate(draw, [0.5, 1], [0, 1], clamp)}
      style={{filter: `drop-shadow(0 0 ${size * 0.12}px ${color})`}}
    />
  </svg>
);

/** Small persistent brand tag near top of frame. */
export const BrandTag: React.FC<{opacity?: number}> = ({opacity = 1}) => (
  <div style={{position: 'absolute', top: 290, left: 0, right: 0, display: 'flex', justifyContent: 'center', opacity}}>
    <div style={{display: 'flex', alignItems: 'center', gap: 10, fontFamily: theme.headFont, fontWeight: 600, fontSize: 38, color: 'rgba(255,255,255,0.85)', letterSpacing: 1}}>
      <SparkBolt size={40} />
      Sparky3dcraft
    </div>
  </div>
);

/** Burst of little sparks around a point. */
export const SparkBurst: React.FC<{x: number; y: number; delay?: number; count?: number; radius?: number}> = ({x, y, delay = 0, count = 14, radius = 260}) => {
  const frame = useCurrentFrame() - delay;
  if (frame < 0 || frame > 40) return null;
  const t = frame / 40;
  const colors = [theme.spark, theme.coral, theme.teal, theme.violet];
  return (
    <>
      {new Array(count).fill(0).map((_, i) => {
        const a = (i / count) * Math.PI * 2 + random(`b${i}`) * 0.4;
        const d = Easing.out(Easing.cubic)(t) * radius * (0.7 + random(`d${i}`) * 0.5);
        const s = (1 - t) * 18;
        return (
          <div
            key={i}
            style={{
              position: 'absolute',
              left: x + Math.cos(a) * d - s / 2,
              top: y + Math.sin(a) * d - s / 2,
              width: s,
              height: s,
              borderRadius: i % 2 ? s : 2,
              transform: `rotate(${a}rad)`,
              background: colors[i % 4],
              boxShadow: `0 0 12px ${colors[i % 4]}`,
            }}
          />
        );
      })}
    </>
  );
};
