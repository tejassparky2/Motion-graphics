// Episode 42, "My Interview Is Tomorrow. No AI Allowed." (ep42_interview.py). Dev and Codex; rainy night; emotional.
import {EMO as E, POSES as P, BODY as B, SHOTS as S} from "./base.js";
export const CAST = {claude: false, codex: [0, -.02]};
export const DETAILS = true, MOOD = "night", RAIN = true, SMOOTH = true, ROUND = true, BIGEYES = true, HEAD = 1.12;
export const EMO = {...E,
  flat:    {brow: -.05, ang: .05, lid: .45, smile: -.1, wide: .98, look: [.15, .35]},
  done:    {brow: -.2, ang: .1, lid: .5, smile: -.25, wide: .95, look: [.15, .35]},
  baffled: {brow: .5, ang: .2, lid: 0, smile: -.15, wide: 1.15, look: [.1, .35]},
  hyped:   {brow: .4, ang: 0, lid: 0, smile: .9, wide: 1.12, look: [.15, .35], happyEyes: .3},
  grin:    {brow: .25, ang: .1, lid: .25, smile: .85, wide: 1, look: [.15, .3], happyEyes: .6},
  tired2:  {brow: .1, ang: .45, lid: .45, smile: -.35, wide: .95, look: [.2, .1]},
  touched: {brow: .3, ang: .4, lid: .1, smile: .35, wide: 1.05, look: [.15, .35]},
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
  e1: D2(["tired2", "rest"], ["watch", "idle"]),
  e2: D2(["tired2", "rest"], ["soft", "idle"]),
  e3: D2(["squint", "rest"], ["soft", "idle"]),
  e4: D2(["baffled", "rest"], ["deadpan", "idle"]),
  e5: D2(["tired2", "slump"], ["soft", "idle"]),
  e6: D2(["tired2", "rest"], ["soft", "idle"]),
  e7: D2(["tired2", "rest"], ["soft", "idle"]),
  e8: D2(["touched", "rest"], ["soft", "idle"]),
  e9: D2(["tired2", "rest"], ["watch", "idle"]),
  e10: D2(["tired2", "rest"], ["deadpan", "idle"]),
  e11: D2(["tired2", "slump"], ["soft", "idle"]),
  e12: D2(["touched", "rest"], ["soft", "idle"]),
  e13: D2(["grin", "rest"], ["proud", "idle"]),
  e14: D2(["grin", "rest"], ["proud", "nod"]),
  e14h: D2(["squint", "type"], ["watch", "idle"]),
  e15: D2(["touched", "rest"], ["proud", "bounce"]),
  e16: D2(["touched", "rest"], ["soft", "idle"]),
  e17: D2(["tired2", "rest"], ["soft", "idle"]),
  e18: D2(["touched", "rest"], ["soft", "idle"]),
  e19: D2(["grin", "rest"], ["soft", "idle"]),
  e20: D2(["grin", "rest"], ["proud", "nod"], {punch: .05}),
};
