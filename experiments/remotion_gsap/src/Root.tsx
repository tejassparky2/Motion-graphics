import React from 'react';
import {Composition} from 'remotion';
import {RatHook} from './RatHook';

export const RemotionRoot: React.FC = () => (
  <Composition id="RatHook" component={RatHook} durationInFrames={198} fps={30} width={720} height={1280} />
);
