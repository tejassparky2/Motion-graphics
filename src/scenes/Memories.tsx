import React from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame, Easing} from 'remotion';
import {copy, theme} from '../config';
import {BrandTag, PopText, SceneFade, clamp} from '../components/ui';
import {Portrait} from '../components/Portrait';

const ICONS = ['🎂', '🏖️', '💍', '🐶', '👶', '🎓', '🎄', '❤️', '🥳', '👨‍👩‍👧', '🏔️', '🐱', '🎉', '🌅', '👵', '⚽'];
const TILE_COLORS = ['#FF8E8E', '#FFD66E', '#7FE0D6', '#A995FF', '#FFB38A', '#8EC9FF'];

/** 3–7 s: emotional problem – memories trapped in the phone. */
export const Memories: React.FC<{duration: number}> = ({duration}) => {
  const frame = useCurrentFrame();
  const phoneIn = interpolate(frame, [0, 14], [0, 1], {...clamp, easing: Easing.out(Easing.back(1.4))});
  // fast scroll that slows down
  const scroll = interpolate(frame, [0, 80], [0, 1500], {...clamp, easing: Easing.out(Easing.cubic)});
  const lineB = frame >= 52;
  // at the end one photo lifts out of the phone
  const lift = interpolate(frame, [86, 112], [0, 1], {...clamp, easing: Easing.inOut(Easing.cubic)});

  const phoneW = 520;
  const phoneH = 900;
  const tile = 146;
  const gap = 10;
  const tiles = [];
  for (let i = 0; i < 48; i++) {
    const col = i % 3;
    const row = Math.floor(i / 3);
    const y = row * (tile + gap) - scroll + 60;
    if (y < -tile || y > phoneH) continue;
    tiles.push(
      <div
        key={i}
        style={{
          position: 'absolute',
          left: 20 + col * (tile + gap),
          top: y + 40,
          width: tile,
          height: tile,
          borderRadius: 14,
          background: `linear-gradient(135deg, ${TILE_COLORS[i % 6]}, ${TILE_COLORS[(i + 2) % 6]})`,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontSize: 64,
        }}
      >
        {ICONS[i % ICONS.length]}
      </div>
    );
  }

  return (
    <SceneFade duration={duration} outFrames={1}>
      <BrandTag />
      <AbsoluteFill style={{alignItems: 'center', top: 380}}>
        {!lineB ? (
          <PopText text={copy.memoriesA} size={100} />
        ) : (
          <PopText text={copy.memoriesB} size={92} delay={52} highlight={['stuck']} highlightColor={theme.coral} style={{maxWidth: 940}} />
        )}
      </AbsoluteFill>
      <div
        style={{
          position: 'absolute',
          left: 540 - phoneW / 2,
          top: 640,
          width: phoneW,
          height: phoneH,
          borderRadius: 64,
          background: '#0B0920',
          border: '10px solid #3B3572',
          boxShadow: '0 40px 80px rgba(0,0,0,0.5), inset 0 0 0 2px rgba(255,255,255,0.08)',
          overflow: 'hidden',
          transform: `translateY(${(1 - phoneIn) * 500}px) rotate(${(1 - phoneIn) * -8}deg)`,
          filter: `blur(${interpolate(frame, [0, 40, 80], [0, 1.2, 0], clamp)}px)`,
        }}
      >
        <div style={{position: 'absolute', top: 0, left: 0, right: 0, height: 64, background: 'rgba(11,9,32,0.92)', zIndex: 2, display: 'flex', alignItems: 'center', paddingLeft: 28, fontFamily: theme.bodyFont, fontWeight: 900, fontSize: 30, color: '#fff'}}>
          Recents
        </div>
        {tiles}
      </div>
      {lift > 0 && (
        <div
          style={{
            position: 'absolute',
            left: 540,
            top: interpolate(lift, [0, 1], [1100, 1000]),
            transform: `translate(-50%, -50%) scale(${interpolate(lift, [0, 1], [0.36, 1])}) rotate(${lift * -6}deg)`,
          }}
        >
          <Portrait size={420} />
        </div>
      )}
    </SceneFade>
  );
};
