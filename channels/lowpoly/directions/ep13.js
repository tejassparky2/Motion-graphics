// Episode 13, "I Interviewed Claude and Codex for One Job" (ep13_interview.py). Reference 10 pacing: a reaction cut
// before every line, shallow-focus over-the-shoulder close-ups, rain on the window.
import {EMO as E, POSES as P, BODY as B, SHOTS as S, CL, CX} from "./base.js";
export const CAST = {claude: CL, codex: CX};
export const DETAILS = true, MOOD = "night", SMOOTH = true, RAIN = true, REACTION_CUTS = true;
export const EMO = {...E,
  flat:  {brow: -.05, ang: .05, lid: .45, smile: -.05, wide: 1, look: [0, .35]},
  blank: {brow: .35, ang: .1, lid: 0, smile: -.15, wide: 1.2, look: [0, .35]},
};
export const POSES = P, BODY = B;
export const SHOTS = {...S,
  clots: {pos: [-.44, 1.2, -1.2], look: [-.24, .9, -.1], push: .08, fov: 32, aperture: .09},   // past Dev's shoulder
  cxots: {pos: [.44, 1.24, -1.2], look: [.2, .98, -.06], push: .08, fov: 32, aperture: .09},
  devmid: {pos: [-.85, 1.26, .25], look: [.02, 1.18, -.9], push: .06, fov: 38, track: "dev", aperture: .07},
  trio:  {pos: [-.62, 1.9, -1.55], look: [-.02, .9, -.2], push: .06, fov: 48},
};
const D3 = (dev, cl, cx, extra = {}) => ({dev, claude: cl, codex: cx, ...extra});
const W = ["watch", "idle"];
export const DIR = {
  q1:  D3(["flat", "rest"], W, W, {cuts: [[0, "trio"], [.6, "devmid"]]}),
  q2:  D3(["flat", "rest"], W, ["eager", "bounce"]),
  q3:  D3(["flat", "rest"], W, ["eager", "idle"]),
  q4:  D3(["flat", "rest"], W, ["proud", "nod"]),
  q5:  D3(["flat", "rest"], ["soft", "nubup"], W),
  q6:  D3(["flat", "rest"], ["soft", "idle"], W),
  q7:  D3(["flat", "rest"], ["soft", "idle"], ["proud", "idle"]),
  q8:  D3(["squint", "squint"], ["soft", "idle"], ["proud", "idle"]),
  q9:  D3(["squint", "rest"], ["soft", "idle"], ["proud", "nod"]),
  q10: D3(["flat", "rest"], ["watch", "idle"], W),
  q11: D3(["flat", "rest"], ["sheepish", "idle"], W),
  q12: D3(["flat", "rest"], ["sheepish", "nubup"], W),
  q13: D3(["flat", "rest"], ["sheepish", "idle"], W),
  q14: D3(["flat", "rest"], W, ["proud", "idle"]),
  q15: D3(["deadpan", "pointscreen"], W, ["proud", "idle"]),
  q16: D3(["deadpan", "rest"], ["oops", "idle"], ["proud", "nod"]),
  q17: D3(["flat", "rest"], W, W),
  q18: D3(["flat", "rest"], ["warm", "idle"], W),
  q19: D3(["flat", "rest"], ["shocked", "freeze"], ["proud", "idle"], {punch: .1}),
  q20: D3(["blank", "doubletake"], ["shocked", "idle"], ["proud", "idle"]),
  q21: D3(["blank", "rest"], W, ["eager", "idle"]),
  q22: D3(["blank", "rest"], W, ["proud", "idle"], {punch: .08}),
  q23: D3(["flat", "rest"], W, W),
  q24: D3(["flat", "rest"], ["soft", "idle"], W),
  q25: D3(["flat", "rest"], ["watch", "idle"], ["proud", "bounce"]),
  q26: D3(["squint", "squint"], W, ["proud", "idle"]),
  q27: D3(["stunned", "flinch"], ["oops", "idle"], ["proud", "bounce"]),
  q28: D3(["stunned", "rest"], ["soft", "nubup"], ["watch", "idle"]),
  q29: D3(["flat", "rest"], ["soft", "idle"], ["watch", "idle"]),
  q30: D3(["flat", "rest"], ["warm", "idle"], ["watch", "lookother"], {punch: .08}),
  q31: D3(["blank", "rest"], ["watch", "lookother"], ["watch", "lookother"]),
  q32: D3(["blank", "slump"], ["soft", "idle"], ["proud", "idle"], {punch: .1}),
};
