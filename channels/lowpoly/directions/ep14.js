// Episode 14, "My AI Wrote It. I Got Promoted." (ep14_promoted.py). Dev, Claude, Codex; warm room; reaction cuts.
import {EMO as E, POSES as P, BODY as B, SHOTS as S, CL, CX} from "./base.js";
export const CAST = {claude: CL, codex: CX};
export const DETAILS = true, SMOOTH = true, REACTION_CUTS = true;
export const EMO = {...E,
  flat:   {brow: -.05, ang: .05, lid: .45, smile: -.05, wide: 1, look: [0, .35]},
  dazed:  {brow: .3, ang: .2, lid: .1, smile: .1, wide: 1.15, look: [0, -.3]},
  guilty: {brow: .15, ang: .5, lid: .4, smile: -.25, wide: 1, look: [.4, -.3]},
  grin:   {brow: .3, ang: -.1, lid: .2, smile: .9, wide: 1.05, look: [0, .35]},
};
export const POSES = P, BODY = B;
export const SHOTS = {...S,
  clots:  {pos: [-.44, 1.2, -1.2], look: [-.24, .9, -.1], push: .08, fov: 32, aperture: .09},
  cxots:  {pos: [.44, 1.24, -1.2], look: [.2, .98, -.06], push: .08, fov: 32, aperture: .09},
  devmid: {pos: [-.85, 1.26, .25], look: [.02, 1.18, -.9], push: .06, fov: 38, track: "dev", aperture: .07},
  trio:   {pos: [-.62, 1.9, -1.55], look: [-.02, .9, -.2], push: .06, fov: 48},
};
const D3 = (dev, cl, cx, extra = {}) => ({dev, claude: cl, codex: cx, ...extra});
const W = ["watch", "idle"];
export const DIR = {
  p1:  D3(["dazed", "phone"], W, W, {cuts: [[0, "devmid"]]}),
  p2:  D3(["dazed", "phone"], ["warm", "idle"], ["eager", "cheer"]),
  p3:  D3(["guilty", "rest"], W, ["eager", "idle"]),
  p4:  D3(["guilty", "rest"], W, ["proud", "nod"], {punch: .06}),
  p5:  D3(["guilty", "slump"], W, ["proud", "idle"]),
  p6:  D3(["guilty", "rest"], ["soft", "nubup"], W),
  p7:  D3(["deadpan", "rest"], ["soft", "idle"], W),
  p8:  D3(["deadpan", "rest"], ["warm", "nod"], W),
  p9:  D3(["stunned", "phone"], W, W),
  p10: D3(["stunned", "flinch"], ["oops", "idle"], ["eager", "idle"]),
  p11: D3(["stunned", "rest"], W, ["proud", "bounce"]),
  p12: D3(["guilty", "rest"], W, ["proud", "idle"]),
  p13: D3(["guilty", "rest"], W, ["suspicious", "idle"]),
  p14: D3(["sad", "slump"], ["soft", "idle"], ["watch", "idle"]),
  p15: D3(["sad", "rest"], ["soft", "lookother"], ["watch", "lookother"]),
  p16: D3(["sad", "rest"], ["soft", "nubup"], W),
  p17: D3(["hopeful", "rest"], ["soft", "idle"], W),
  p18: D3(["hopeful", "rest"], ["warm", "idle"], W),
  p19: D3(["hopeful", "rest"], ["warm", "nod"], W),
  p20: D3(["smallsmile", "rest"], ["warm", "idle"], W, {punch: .08}),
  p21: D3(["smallsmile", "rest"], ["warm", "idle"], ["proud", "idle"]),
  p22: D3(["smallsmile", "nod"], W, ["proud", "idle"]),
  p23: D3(["smallsmile", "type"], ["warm", "idle"], ["watch", "idle"], {cuts: [[0, "ots"]]}),
  p24: D3(["deadpan", "rest"], W, ["eager", "bounce"]),
  p25: D3(["deadpan", "rest"], W, ["oops", "idle"]),
  p26: D3(["deadpan", "rest"], W, ["sheepish", "idle"]),
  p27: D3(["grin", "rest"], ["warm", "idle"], ["proud", "cheer"], {punch: .08}),
};
