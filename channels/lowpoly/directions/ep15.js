// Episode 15, "My Junior Asked Me, Not the AI." (ep15_junior.py). Dev at his desk, the junior beside him, Claude.
import {EMO as E, POSES as P, BODY as B, SHOTS as S} from "./base.js";
export const CAST = {codex: false, claude: [0, -.05],
  guest: {name: "junior", skin: 0xc98a62, cloth: 0x4f8a6a, hair: 0x1d1412, ponytail: true, glasses: false, pants: 0x2a2f44, pos: [.66, -.86], turn: -.55}};
export const DETAILS = true, MOOD = "night", SMOOTH = true, RAIN = true, REACTION_CUTS = true;
export const EMO = {...E,
  grin:     {brow: .3, ang: -.1, lid: .2, smile: .9, wide: 1.05, look: [.5, .35]},
  flat:     {brow: -.05, ang: .05, lid: .45, smile: -.05, wide: 1, look: [0, .35]},
  earnest:  {brow: .3, ang: .35, lid: .05, smile: .1, wide: 1.05, look: [-.4, .3]},
  small:    {brow: .2, ang: .5, lid: .35, smile: -.15, wide: .95, look: [0, -.4]},
  lit:      {brow: .4, ang: .2, lid: 0, smile: .6, wide: 1.1, look: [-.4, .3]},
  softdev:  {brow: .15, ang: .4, lid: .2, smile: .25, wide: 1, look: [.5, .35]},
};
export const POSES = P, BODY = B;
export const SHOTS = {...S,
  two:     {pos: [-1.15, 1.55, -.25], look: [.3, 1.08, -.9], push: .06, fov: 50},
  jr:      {pos: [.02, 1.36, .07], look: [.66, 1.2, -.86], push: .06, fov: 44, track: "junior"},
  jrclose: {pos: [.0, 1.34, .02], look: [.66, 1.22, -.86], push: .06, fov: 42, track: "junior", aperture: .07},
  devjr:   {pos: [-.95, 1.3, .3], look: [.25, 1.15, -.9], push: .05, fov: 46, track: "dev", aperture: .06},   // Dev, her behind him
  screen:  {pos: [-.3, 1.45, -1.38], look: [0, .95, .1], push: .1, fov: 46},   // over Dev's shoulder at the code
};
const D3 = (dev, jr, cl, extra = {}) => ({dev, junior: jr, claude: cl, ...extra});
const W = ["watch", "idle"];
export const DIR = {
  r1:  D3(["flat", "type"], ["earnest", "rest"], W, {cuts: [[0, "two"], [.55, "jr"]]}),
  r2:  D3(["flat", "type"], ["earnest", "rest"], W),
  r3:  D3(["flat", "rest"], ["earnest", "rest"], W),
  r4:  D3(["flat", "rest"], ["small", "rest"], W),
  r5:  D3(["flat", "rest"], ["small", "slump"], W),
  r6:  D3(["stunned", "doubletake"], ["small", "rest"], ["soft", "idle"]),
  r7:  D3(["deadpan", "rest"], ["small", "rest"], ["soft", "idle"]),
  r8:  D3(["deadpan", "rest"], ["small", "rest"], ["soft", "nubup"]),
  r9:  D3(["deadpan", "rest"], ["small", "rest"], ["warm", "idle"], {punch: .08}),
  r10: D3(["tired", "type"], ["small", "rest"], ["soft", "idle"]),
  r11: D3(["tired", "rest"], ["small", "slump"], ["sad", "idle"]),
  r12: D3(["sad", "rest"], ["small", "rest"], ["sad", "lookdown"]),
  r13: D3(["softdev", "sitback"], ["small", "rest"], W),
  r14: D3(["softdev", "rest"], ["small", "rest"], W),
  r15: D3(["softdev", "rest"], ["lit", "rest"], ["warm", "idle"]),
  r16: D3(["softdev", "nod"], ["lit", "rest"], ["warm", "idle"]),
  r17: D3(["smallsmile", "pointscreen"], ["lit", "lean"], W, {cuts: [[0, "screen"], [.6, "devjr"]]}),
  r18: D3(["smallsmile", "rest"], ["earnest", "lean"], W),
  r19: D3(["smallsmile", "shrug"], ["lit", "rest"], ["warm", "idle"]),
  r20: D3(["smallsmile", "rest"], ["lit", "rest"], ["eager", "nubup"]),
  r21: D3(["grin", "rest"], ["lit", "rest"], ["oops", "idle"]),
  r22: D3(["grin", "rest"], ["lit", "nod"], ["warm", "cheer"], {punch: .08}),
};
