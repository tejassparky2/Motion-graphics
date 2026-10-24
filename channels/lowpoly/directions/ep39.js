// Episode 39, AI news: Claude Duet (ep39_duet.py). Dev and Claude; night.
import {EMO as E, POSES as P, BODY as B, SHOTS as S} from "./base.js";
export const CAST = {codex: false, claude: [0, -.05]};
export const DETAILS = true, MOOD = "night", SMOOTH = true, ROUND = true, BIGEYES = true, HEAD = 1.12;
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
  solo:     {pos: [-.42, 1.0, -.72], look: [0, .9, -.05], push: .05, fov: 40, aperture: .05},
  soloclose:{pos: [-.26, .98, -.7], look: [0, .91, -.05], push: .07, fov: 40, aperture: .06},
  ots:      {pos: [-.62, 1.4, -1.15], look: [.05, .95, .15], push: .05, fov: 44},
};
const D2 = (dev, cl, extra = {}) => ({dev, claude: cl, ...extra});
export const DIR = {
  d1: D2(["hyped", "rest"], ["watch", "idle"]),
  d2: D2(["squint", "rest"], ["proud", "idle"]),
  d3: D2(["baffled", "rest"], ["watch", "idle"]),
  d4: D2(["squint", "rest"], ["proud", "idle"]),
  d5: D2(["squint", "rest"], ["watch", "idle"]),
  d6: D2(["squint", "rest"], ["watch", "idle"]),
  d7: D2(["baffled", "rest"], ["watch", "idle"]),
  d8: D2(["squint", "rest"], ["proud", "idle"]),
  d9: D2(["grin", "rest"], ["watch", "idle"]),
  d10: D2(["squint", "rest"], ["proud", "idle"]),
  d11: D2(["hyped", "rest"], ["watch", "idle"]),
  d12: D2(["squint", "rest"], ["watch", "idle"]),
  d13: D2(["squint", "rest"], ["watch", "idle"]),
  d14: D2(["squint", "rest"], ["proud", "idle"]),
  d15: D2(["squint", "rest"], ["watch", "idle"]),
  d16: D2(["squint", "rest"], ["proud", "idle"]),
  d17: D2(["touched", "rest"], ["watch", "idle"]),
  d18: D2(["squint", "rest"], ["soft", "idle"]),
};
