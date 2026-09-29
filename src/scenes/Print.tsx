import React from 'react';
import {AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {copy, theme} from '../config';
import {BrandTag, PopText, SceneFade, clamp} from '../components/ui';
import {Printer} from '../components/Printer';
import timeline from '../timeline.json';

/** 11–19 s: the visual proof – multi-colour print with four toolheads swapping. */
export const Print: React.FC<{duration: number}> = ({duration}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const inS = spring({frame, fps, config: {damping: 14, stiffness: 110}});
  const second = frame >= 112;
  const done = frame >= timeline.print.end;
  const doneFlash = interpolate(frame, [timeline.print.end, timeline.print.end + 6, timeline.print.end + 24], [0, 0.35, 0], clamp);

  return (
    <SceneFade duration={duration} inFrames={6}>
      <BrandTag />
      <AbsoluteFill style={{alignItems: 'center', top: 360}}>
        {!second ? (
          <>
            <PopText text={copy.printTitle} size={96} highlight={['colour', 'color']} delay={4} />
            <PopText text={copy.printSub} size={54} weight={600} color={theme.muted} delay={14} font="body" style={{marginTop: 10}} />
          </>
        ) : (
          <>
            <PopText text={copy.toolTitle} size={82} highlight={['4', '1']} delay={112} />
            <PopText text={copy.toolSub} size={48} weight={700} color={theme.muted} delay={122} font="body" style={{marginTop: 10}} />
          </>
        )}
      </AbsoluteFill>
      <div style={{position: 'absolute', left: 110, top: 610, transform: `translateY(${(1 - inS) * 900}px)`}}>
        <Printer width={860} />
      </div>
      {done && <AbsoluteFill style={{background: '#fff', opacity: doneFlash}} />}
    </SceneFade>
  );
};
