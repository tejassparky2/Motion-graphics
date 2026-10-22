// Episode 26, "My AI Got an Update. Now It Agrees With Everything." (ep26_agree.py). Dev and Codex; warm room.
import {EMO as E, POSES as P, BODY as B, SHOTS as S} from "./base.js";
export const CAST = {claude: false, codex: [0, -.02]};
export const DETAILS = true, SMOOTH = true, ROUND = true, BIGEYES = true, HEAD = 1.12;
export const EMO = {...E,
  flat:    {brow: -.05, ang: .05, lid: .45, smile: -.1, wide: .98, look: [.15, .35]},
  testing: {brow: .2, ang: -.1, lid: .35, smile: .2, wide: 1, look: [.15, .35]},
  done:    {brow: -.2, ang: .1, lid: .5, smile: -.25, wide: .95, look: [.15, .35]},
  baffled: {brow: .5, ang: .2, lid: 0, smile: -.15, wide: 1.15, look: [.1, .35]},
  relief:  {brow: .3, ang: .2, lid: .2, smile: .7, wide: 1.02, look: [.15, .35]},
};
export const POSES = P, BODY = B;
export const SHOTS = {...S,
  devmid:   {pos: [-.85, 1.3, .25], look: [.02, 1.25, -.9], push: .05, fov: 40, track: "dev", aperture: .06},
  devclose: {pos: [-.72, 1.37, .02], look: [0, 1.32, -.94], push: .06, fov: 41, track: "dev", aperture: .07},
  cx:       {pos: [.42, 1.06, -.76], look: [0, .98, -.02], push: .05, fov: 40, aperture: .05},
  cxclose:  {pos: [.3, 1.03, -.56], look: [0, .99, -.02], push: .07, fov: 38, aperture: .06},
  ots:      {pos: [-.62, 1.4, -1.15], look: [.05, .95, .15], push: .05, fov: 44},
};
const D2 = (dev, cx, extra = {}) => ({dev, codex: cx, ...extra});
export const DIR = {
  q1:  D2(["flat", "rest"], ["eager", "bounce"]),
  q2:  D2(["testing", "rest"], ["eager", "idle"]),
  q3:  D2(["testing", "rest"], ["proud", "bounce"]),
  q4:  D2(["testing", "rest"], ["eager", "idle"]),
  q5:  D2(["squint", "rest"], ["eager", "bounce"]),
  q6:  D2(["squint", "rest"], ["eager", "idle"]),
  q7:  D2(["baffled", "rest"], ["proud", "bounce"]),
  q8:  D2(["done", "rest"], ["eager", "idle"]),
  q9:  D2(["done", "rest"], ["eager", "bounce"], {punch: .05}),
  q10: D2(["baffled", "rest"], ["eager", "idle"]),
  q11: D2(["baffled", "rest"], ["proud", "idle"]),
  q12: D2(["done", "rest"], ["eager", "idle"]),
  q13: D2(["squint", "rest"], ["eager", "idle"]),
  q14: D2(["squint", "rest"], ["proud", "nod"]),
  q15: D2(["done", "rest"], ["eager", "idle"]),
  q16: D2(["done", "slump"], ["eager", "bounce"], {punch: .06}),
  q17: D2(["done", "rest"], ["watch", "glitch"]),
  q18: D2(["stunned", "rest"], ["deadpan", "idle"]),
  q19: D2(["relief", "rest"], ["deadpan", "idle"], {punch: .06}),
};
