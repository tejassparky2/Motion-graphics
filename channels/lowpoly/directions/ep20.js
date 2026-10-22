// Episode 20, "I Yelled at My AI at 3 AM" (ep20_yelled.py). Dev and Claude; rainy night; held shots, big eyes.
import {EMO as E, POSES as P, BODY as B, SHOTS as S} from "./base.js";
export const CAST = {codex: false, claude: [0, -.05]};
export const DETAILS = true, MOOD = "night", RAIN = true, SMOOTH = true, ROUND = true, BIGEYES = true, HEAD = 1.12;
export const EMO = {...E,
  angry:   {brow: -.45, ang: -.35, lid: .3, smile: -.45, wide: 1, look: [.2, .35]},
  flat:    {brow: -.05, ang: .05, lid: .4, smile: -.1, wide: 1, look: [.2, .35]},
  caught:  {brow: .45, ang: .2, lid: 0, smile: -.1, wide: 1.12, look: [.25, .35]},
  low:     {brow: .15, ang: .45, lid: .4, smile: -.25, wide: 1, look: [.1, -.3], wet: .3},
  ashamed2:{brow: .3, ang: .6, lid: .35, smile: -.3, wide: 1, look: [.1, -.35], wet: .8},
  soft2:   {brow: .2, ang: .35, lid: .2, smile: .2, wide: 1, look: [.25, .35], wet: .5},
  grin:    {brow: .3, ang: -.1, lid: .2, smile: .85, wide: 1.05, look: [.25, .35]},
};
export const POSES = P, BODY = B;
export const SHOTS = {...S,
  devmid:   {pos: [-.85, 1.3, .25], look: [.02, 1.25, -.9], push: .05, fov: 40, track: "dev", aperture: .06},
  devclose: {pos: [-.72, 1.37, .02], look: [0, 1.32, -.94], push: .06, fov: 41, track: "dev", aperture: .07},
  solo:     {pos: [-.42, 1.0, -.72], look: [0, .9, -.05], push: .05, fov: 40, aperture: .05},
  soloclose:{pos: [-.26, .98, -.7], look: [0, .91, -.05], push: .07, fov: 40, aperture: .06},
};
const D2 = (dev, cl, extra = {}) => ({dev, claude: cl, ...extra});
export const DIR = {
  e1:  D2(["angry", "type"], ["watch", "idle"]),
  e2:  D2(["angry", "type"], ["soft", "idle"]),
  e3:  D2(["angry", "pointscreen"], ["sad", "idle"], {punch: .06}),
  e4:  D2(["angry", "rest"], ["sad", "lookdown"]),
  e5:  D2(["angry", "rest"], ["soft", "idle"]),
  e6:  D2(["flat", "rest"], ["soft", "idle"]),
  e7:  D2(["angry", "rest"], ["soft", "idle"]),
  e8:  D2(["caught", "rest"], ["soft", "idle"]),
  e9:  D2(["caught", "rest"], ["soft", "idle"]),
  e10: D2(["caught", "rest"], ["soft", "lookdown"]),
  e11: D2(["caught", "rest"], ["warm", "idle"]),
  e12: D2(["low", "rest"], ["soft", "idle"]),
  e13: D2(["low", "rest"], ["soft", "idle"]),
  e14: D2(["low", "rest"], ["warm", "idle"]),
  e15: D2(["low", "slump"], ["soft", "idle"]),
  e16: D2(["low", "rest"], ["warm", "nubup"]),
  e17: D2(["caught", "rest"], ["warm", "idle"]),
  e18: D2(["ashamed2", "rest"], ["warm", "idle"]),
  e19: D2(["ashamed2", "slump"], ["soft", "idle"]),
  e20: D2(["ashamed2", "rest"], ["soft", "idle"], {punch: .05}),
  e21: D2(["soft2", "rest"], ["warm", "idle"]),
  e22: D2(["soft2", "rest"], ["warm", "idle"]),
  e23: D2(["soft2", "rest"], ["proud", "nubup"]),
  e24: D2(["soft2", "rest"], ["warm", "idle"]),
  e25: D2(["grin", "rest"], ["warm", "idle"]),
  e26: D2(["grin", "sitback"], ["warm", "cheer"], {punch: .06}),
};
