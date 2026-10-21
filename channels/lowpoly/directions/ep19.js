// Episode 19, "My Boss Made AI Mandatory" (ep19_mandatory.py). Dev and Codex (pops in at d3); warm evening room.
import {EMO as E, POSES as P, BODY as B, SHOTS as S} from "./base.js";
export const CAST = {claude: false, codex: [0, -.02]};
export const DETAILS = true, SMOOTH = true, ROUND = true, BIGEYES = true, HEAD = 1.12;
export const EMO = {...E,
  flat:     {brow: -.05, ang: .05, lid: .45, smile: -.1, wide: .98, look: [.15, .35]},
  grumpy:   {brow: -.3, ang: -.2, lid: .35, smile: -.3, wide: 1, look: [.2, .35]},
  caught:   {brow: .45, ang: .2, lid: 0, smile: -.05, wide: 1.12, look: [.3, .35]},
  low:      {brow: .15, ang: .45, lid: .4, smile: -.2, wide: 1, look: [.1, -.3], wet: .3},
  open:     {brow: .3, ang: .4, lid: .15, smile: .2, wide: 1.02, look: [.25, .35], wet: .5},
  moved:    {brow: .35, ang: .55, lid: .2, smile: .3, wide: 1.02, look: [.25, .35], wet: 1},
  grin:     {brow: .3, ang: -.1, lid: .2, smile: .85, wide: 1.05, look: [.25, .35]},
};
export const POSES = P, BODY = B;
export const SHOTS = {...S,
  devmid:  {pos: [-.85, 1.3, .25], look: [.02, 1.25, -.9], push: .05, fov: 40, track: "dev", aperture: .06},
  devclose:{pos: [-.62, 1.36, -.08], look: [0, 1.33, -.94], push: .07, fov: 38, track: "dev", aperture: .07},
  cx:      {pos: [.45, 1.06, -.76], look: [0, .98, -.02], push: .05, fov: 40, aperture: .05},
  cxclose: {pos: [.3, 1.03, -.56], look: [0, .99, -.02], push: .08, fov: 38, aperture: .06},
  ots:     {pos: [-.3, 1.48, -1.42], look: [0, .95, .05], push: .06, fov: 44},
  two:     {pos: [-.62, 1.9, -1.55], look: [-.02, .9, -.2], push: .05, fov: 48},
};
const D2 = (dev, cx, extra = {}) => ({dev, codex: cx, ...extra});
const H = ["hidden", "idle"];
export const DIR = {
  d1:  D2(["flat", "phone"], H),
  d2:  D2(["grumpy", "rest"], H),
  d3:  D2(["caught", "flinch"], ["eager", "wave"]),
  d4:  D2(["grumpy", "rest"], ["eager", "idle"]),
  d5:  D2(["grumpy", "rest"], ["proud", "idle"]),
  d6:  D2(["grumpy", "pointscreen"], ["eager", "nod"]),
  d7:  D2(["flat", "type"], ["watch", "idle"]),
  d8:  D2(["flat", "type"], ["eager", "idle"]),
  d9:  D2(["deadpan", "type"], ["eager", "idle"]),
  d10: D2(["deadpan", "type"], ["eager", "idle"]),
  d11: D2(["deadpan", "type"], ["sheepish", "idle"]),
  d12: D2(["deadpan", "type"], ["sheepish", "idle"]),
  d13: D2(["flat", "type"], ["eager", "bounce"]),
  d14: D2(["flat", "type"], ["watch", "idle"]),
  d15: D2(["caught", "rest"], ["watch", "idle"]),
  d16: D2(["low", "rest"], ["soft", "idle"]),
  d17: D2(["low", "rest"], ["watch", "idle"]),
  d18: D2(["open", "rest"], ["watch", "idle"]),
  d19: D2(["open", "rest"], ["soft", "idle"]),
  d20: D2(["moved", "rest"], ["soft", "nod"], {punch: .05}),
  d21: D2(["open", "rest"], ["soft", "idle"]),
  d22: D2(["stunned", "phone"], ["sad", "idle"]),
  d23: D2(["low", "rest"], ["soft", "idle"]),
  d24: D2(["low", "rest"], ["soft", "idle"]),
  d25: D2(["low", "rest"], ["soft", "idle"]),
  d26: D2(["flat", "type"], ["watch", "lookdown"]),
  d27: D2(["caught", "rest"], ["soft", "idle"]),
  d28: D2(["open", "rest"], ["soft", "idle"]),
  d29: D2(["moved", "rest"], ["warm", "idle"], {punch: .05}),
  d30: D2(["moved", "rest"], ["warm", "idle"]),
  d31: D2(["grin", "phone"], ["proud", "idle"]),
  d32: D2(["grin", "rest"], ["eager", "idle"]),
  d33: D2(["grin", "rest"], ["proud", "idle"], {punch: .07}),
};
