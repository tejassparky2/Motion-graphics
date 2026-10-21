// Episode 17, "My AI Deleted 8 Months of My Work" (ep17_deleted.py). Dev, Claude, Codex; rainy night, then dawn.
import {EMO as E, POSES as P, BODY as B, SHOTS as S, CL, CX} from "./base.js";
export const CAST = {claude: CL, codex: CX};
export const DETAILS = true, MOOD = "night", RAIN = true, SMOOTH = true, ROUND = true, BIGEYES = true, HEAD = 1.12, DAWN = "b27";
export const EMO = {...E,
  flat:     {brow: -.05, ang: .05, lid: .4, smile: -.05, wide: 1, look: [.2, .35]},
  blank:    {brow: .4, ang: .1, lid: 0, smile: -.2, wide: 1.2, look: [0, .3]},
  low:      {brow: .15, ang: .45, lid: .4, smile: -.25, wide: 1, look: [.1, -.35], wet: .3},
  teary:    {brow: .35, ang: .6, lid: .25, smile: -.2, wide: 1.02, look: [.2, .1], wet: .9},
  crying:   {brow: .4, ang: .7, lid: .3, smile: -.15, wide: 1, look: [.2, .1], wet: 1, tear: 1},
  resolve:  {brow: -.1, ang: .15, lid: .2, smile: .15, wide: 1.02, look: [.25, .35], wet: .5},
  proud:    {brow: .25, ang: -.05, lid: .15, smile: .55, wide: 1.02, look: [.25, .35], wet: .3},
  grin:     {brow: .3, ang: -.1, lid: .2, smile: .85, wide: 1.05, look: [.3, .35]},
};
export const POSES = P, BODY = B;
export const SHOTS = {...S,
  devmid:  {pos: [-.85, 1.3, .25], look: [.02, 1.25, -.9], push: .05, fov: 40, track: "dev", aperture: .06},
  devclose:{pos: [-.72, 1.37, .02], look: [0, 1.32, -.94], push: .06, fov: 41, track: "dev", aperture: .07},
  ots:     {pos: [-.3, 1.48, -1.42], look: [0, .95, .05], push: .06, fov: 44},
  endside: {pos: [-1.3, 1.75, -1.75], look: [-.05, 1.05, -.4], push: .05, fov: 50},
};
const D3 = (dev, cl, cx, extra = {}) => ({dev, claude: cl, codex: cx, ...extra});
const W = ["watch", "idle"];
export const DIR = {
  b1:  D3(["flat", "type"], W, ["eager", "idle"]),
  b2:  D3(["flat", "type"], W, ["eager", "nod"]),
  b3:  D3(["flat", "rest"], ["suspicious", "idle"], ["proud", "idle"]),
  b4:  D3(["flat", "rest"], ["shocked", "idle"], ["proud", "idle"]),
  b5:  D3(["squint", "leanin"], ["shocked", "idle"], ["watch", "idle"]),
  b6:  D3(["stunned", "rest"], ["sad", "idle"], ["watch", "idle"]),
  b7:  D3(["blank", "rest"], ["sad", "idle"], ["horrified", "idle"], {punch: .07}),
  b8:  D3(["blank", "rest"], ["sad", "idle"], ["horrified", "idle"]),
  b9:  D3(["blank", "rest"], ["sad", "idle"], ["sad", "lookdown"]),
  b10: D3(["stunned", "rest"], W, ["sad", "idle"]),
  b11: D3(["stunned", "rest"], ["soft", "idle"], ["sad", "idle"]),
  b12: D3(["low", "slump"], ["sad", "idle"], ["sad", "lookdown"]),
  b13: D3(["low", "rest"], W, ["sheepish", "idle"]),
  b14: D3(["deadpan", "rest"], W, ["oops", "idle"]),
  b15: D3(["low", "rest"], ["sad", "idle"], ["sad", "lookdown"]),
  b16: D3(["teary", "rest"], ["sad", "idle"], ["sad", "idle"]),
  b17: D3(["teary", "rest"], ["sad", "idle"], ["sad", "lookdown"]),
  b18: D3(["crying", "rest"], ["sad", "lookdown"], ["sad", "lookdown"], {punch: .05}),
  b19: D3(["crying", "rest"], ["sad", "lookdown"], ["sad", "lookdown"]),
  b20: D3(["crying", "rest"], ["sad", "idle"], ["sad", "idle"]),
  b21: D3(["teary", "rest"], ["soft", "idle"], ["sad", "idle"]),
  b22: D3(["teary", "rest"], ["soft", "nubup"], ["watch", "idle"]),
  b23: D3(["resolve", "rest"], ["warm", "idle"], ["watch", "idle"], {punch: .06}),
  b24: D3(["resolve", "rest"], ["warm", "idle"], ["eager", "idle"]),
  b25: D3(["resolve", "type"], ["warm", "nod"], ["eager", "idle"]),
  b26: D3(["resolve", "type"], ["warm", "idle"], ["watch", "idle"]),
  b27: D3(["proud", "rest"], ["warm", "nubup"], ["eager", "idle"]),
  b28: D3(["proud", "sitback"], ["warm", "idle"], ["eager", "idle"]),
  b29: D3(["proud", "rest"], W, ["eager", "bounce"]),
  b30: D3(["grin", "rest"], W, ["sheepish", "idle"]),
  b31: D3(["grin", "rest"], ["warm", "idle"], ["eager", "idle"]),
  b32: D3(["deadpan", "rest"], ["warm", "idle"], ["oops", "idle"], {punch: .08}),
};
