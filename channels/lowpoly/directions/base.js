// Shared acting and camera for episodes 3+ (Claude at the left of the desk, Codex at the right, Dev in front).
import {EMO as E1, POSES as P1, BODY as B1} from "./ep01ar.js";
import {EMO as E2, POSES as P2, BODY as B2} from "./ep02ctx.js";
export const EMO = {...E1, ...E2};
export const POSES = {...P1, ...P2};
export const BODY = {...B1, ...B2};
export const CL = [-.24, -.05], CX = [.2, -.02];       // Claude and Codex spots when both are on the desk
export const SHOTS = {
  dev:        {pos: [-1.0, 1.28, .4], look: [.02, 1.12, -.88], push: .12, fov: 44, track: "dev"},
  devclose:   {pos: [-.75, 1.32, -.1], look: [0, 1.25, -.94], push: .08, fov: 44, track: "dev"},
  ots:        {pos: [-.3, 1.45, -1.38], look: [0, .95, .1], push: .1, fov: 46},
  duo:        {pos: [0, 1.85, -1.1], look: [-.02, .88, -.05], push: .1, fov: 46},            // both AIs, from above Dev
  claude:     {pos: [-.64, .98, -.68], look: [-.24, .88, -.05], push: .12, fov: 40},
  claudeclose:{pos: [-.58, .98, -.6], look: [-.24, .9, -.05], push: .12, fov: 40},
  codex:      {pos: [.6, 1.06, -.74], look: [.2, .98, -.02], push: .12, fov: 40},
  codexclose: {pos: [.48, 1.03, -.54], look: [.2, .99, -.02], push: .12, fov: 38},
  endside:    {pos: [-.62, 1.9, -1.55], look: [-.05, .85, -.15], push: .1, fov: 50},
  // single-AI episodes (the AI centred)
  solo:       {pos: [-.5, .98, -.72], look: [0, .88, -.05], push: .12, fov: 40},
  soloclose:  {pos: [-.24, .95, -.72], look: [0, .9, -.05], push: .14, fov: 38},
  cxsolo:     {pos: [.55, 1.06, -.76], look: [.1, .98, -.02], push: .12, fov: 40},
  cxsoloclose:{pos: [.42, 1.03, -.56], look: [.1, .99, -.02], push: .14, fov: 38},
};
