import React from 'react';
import {AbsoluteFill, Img, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {copy, realPhotos} from '../config';
import {BrandTag, PopText, SceneFade} from '../components/ui';

/** Optional: real photos of finished prints (only shown when config.realPhotos has files). */
export const Proof: React.FC<{duration: number}> = ({duration}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const photos = realPhotos.slice(0, 3);
  const layouts = [
    {x: 540, y: 1000, r: 0, s: 1},
    {x: 330, y: 1060, r: -8, s: 0.82},
    {x: 750, y: 1060, r: 8, s: 0.82},
  ];
  // draw the side photos first so the first photo sits on top
  const order = photos.map((p, i) => ({p, i})).reverse();
  return (
    <SceneFade duration={duration}>
      <BrandTag />
      <AbsoluteFill style={{alignItems: 'center', top: 380}}>
        <PopText text={copy.proofTitle} size={88} highlight={['real']} style={{maxWidth: 960}} />
      </AbsoluteFill>
      {order.map(({p, i}) => {
        const L = layouts[photos.length === 1 ? 0 : i];
        const s = spring({frame: frame - 6 - i * 8, fps, config: {damping: 12, stiffness: 140}});
        return (
          <div
            key={p}
            style={{
              position: 'absolute',
              left: L.x,
              top: L.y,
              transform: `translate(-50%, -50%) rotate(${L.r}deg) scale(${L.s * s}) translateY(${(1 - s) * 400}px)`,
              background: '#fff',
              padding: 16,
              paddingBottom: 56,
              borderRadius: 10,
              boxShadow: '0 30px 60px rgba(0,0,0,0.5)',
            }}
          >
            <Img src={staticFile(p)} style={{width: 460, height: 560, objectFit: 'cover', display: 'block', borderRadius: 4}} />
          </div>
        );
      })}
    </SceneFade>
  );
};
