// Episode 23, "My AI Forgot Everything About Me" (ep23_forgot.py). Dev and Codex; night, then morning light.
import {EMO as E, POSES as P, BODY as B, SHOTS as S} from "./base.js";
export const CAST = {claude: false, codex: [0, -.02]};
export const DETAILS = true, MOOD = "night", SMOOTH = true, ROUND = true, BIGEYES = true, HEAD = 1.12, DAWN = "h21";
export const EMO = {...E,
  hurt:    {brow: .3, ang: .55, lid: .2, smile: -.2, wide: 1.05, look: [.2, .35], wet: .5},
  flat:    {brow: -.05, ang: .05, lid: .4, smile: -.1, wide: 1, look: [.2, .35]},
  teary:   {brow: .35, ang: .6, lid: .25, smile: -.15, wide: 1.02, look: [.2, .3], wet: .9},
  crying:  {brow: .4, ang: .65, lid: .3, smile: -.05, wide: 1, look: [.2, .3], wet: 1, tear: 1},
  brave:   {brow: .1, ang: .3, lid: .15, smile: .35, wide: 1.04, look: [.15, .35], wet: 1, tear: 1},
  grin:    {brow: .3, ang: -.1, lid: .2, smile: .85, wide: 1.05, look: [.2, .35], wet: .3},
};
export const POSES = P, BODY = B;
export const SHOTS = {...S,
  devmid:   {pos: [-.85, 1.3, .25], look: [.02, 1.25, -.9], push: .05, fov: 40, track: "dev", aperture: .06},
  devclose: {pos: [-.72, 1.37, .02], look: [0, 1.32, -.94], push: .06, fov: 41, track: "dev", aperture: .07},
  cx:       {pos: [.42, 1.06, -.76], look: [0, .98, -.02], push: .05, fov: 40, aperture: .05},
  cxclose:  {pos: [.3, 1.03, -.56], look: [0, .99, -.02], push: .07, fov: 38, aperture: .06},
  endside:  {pos: [-1.3, 1.75, -1.75], look: [-.05, 1.05, -.4], push: .05, fov: 50},
};
const D2 = (dev, cx, extra = {}) => ({dev, codex: cx, ...extra});
export const DIR = {
  h1:  D2(["flat", "rest"], ["eager", "wave"]),
  h2:  D2(["hurt", "rest"], ["eager", "idle"]),
  h3:  D2(["hurt", "rest"], ["eager", "bounce"]),
  h4:  D2(["hurt", "rest"], ["watch", "idle"]),
  h5:  D2(["hurt", "rest"], ["sheepish", "idle"]),
  h6:  D2(["teary", "rest"], ["watch", "idle"]),
  h7:  D2(["teary", "rest"], ["eager", "idle"]),
  h8:  D2(["teary", "rest"], ["watch", "idle"]),
  h9:  D2(["teary", "rest"], ["watch", "idle"]),
  h10: D2(["flat", "rest"], ["oops", "idle"]),
  h11: D2(["teary", "slump"], ["sad", "idle"]),
  h12: D2(["teary", "rest"], ["sad", "idle"]),
  h13: D2(["teary", "rest"], ["soft", "idle"]),
  h14: D2(["crying", "rest"], ["soft", "idle"], {punch: .05}),
  h15: D2(["crying", "rest"], ["soft", "idle"]),
  h16: D2(["teary", "sitback"], ["watch", "idle"]),
  h17: D2(["brave", "rest"], ["watch", "idle"]),
  h18: D2(["brave", "rest"], ["watch", "idle"], {punch: .06}),
  h19: D2(["brave", "rest"], ["proud", "nod"]),
  h20: D2(["brave", "rest"], ["proud", "idle"]),
  h21: D2(["grin", "rest"], ["eager", "idle"]),
  h22: D2(["grin", "rest"], ["eager", "idle"]),
  h23: D2(["grin", "rest"], ["proud", "nod"]),
  h24: D2(["grin", "rest"], ["sheepish", "idle"], {punch: .07}),
};
