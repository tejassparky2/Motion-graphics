import './fonts';
import React from 'react';
import {AbsoluteFill, Audio, Composition, Sequence, staticFile} from 'remotion';
import {realPhotos} from './config';
import timeline from './timeline.json';
import {Background} from './components/ui';
import {Hook} from './scenes/Hook';
import {Memories} from './scenes/Memories';
import {Steps} from './scenes/Steps';
import {Print} from './scenes/Print';
import {Reveal} from './scenes/Reveal';
import {Proof} from './scenes/Proof';
import {Gift} from './scenes/Gift';
import {Cta} from './scenes/Cta';

const SCENES: Record<string, React.FC<{duration: number}>> = {
  hook: Hook,
  memories: Memories,
  steps: Steps,
  print: Print,
  reveal: Reveal,
  proof: Proof,
  gift: Gift,
  cta: Cta,
};

/** Scene list, inserting the optional real-photo proof scene after the reveal. */
const buildScenes = () => {
  const out: {id: string; from: number; duration: number}[] = [];
  let t = 0;
  for (const s of timeline.scenes) {
    out.push({id: s.id, from: t, duration: s.duration});
    t += s.duration;
    if (s.id === 'reveal' && realPhotos.length > 0) {
      out.push({id: 'proof', from: t, duration: timeline.proofSceneDuration});
      t += timeline.proofSceneDuration;
    }
  }
  return {scenes: out, total: t};
};

const {scenes, total} = buildScenes();

export const MiniMeAd: React.FC = () => (
  <AbsoluteFill style={{backgroundColor: '#0C0A24'}}>
    <Background />
    {scenes.map((s) => {
      const Scene = SCENES[s.id];
      return (
        <Sequence key={s.id} from={s.from} durationInFrames={s.duration} name={s.id}>
          <Scene duration={s.duration} />
        </Sequence>
      );
    })}
    <Audio src={staticFile('music.wav')} />
  </AbsoluteFill>
);

export const RemotionRoot: React.FC = () => (
  <Composition id="MiniMeAd" component={MiniMeAd} durationInFrames={total} fps={timeline.fps} width={1080} height={1920} />
);
