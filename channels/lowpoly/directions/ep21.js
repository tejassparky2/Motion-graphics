// Episode 21, "An AI Interviewed Me for a Job" (ep21_interview_ai.py). Dev and Codex; the interviewer is an overlay
// card on the monitor (ots shots look at the screen); morning light.
import {EMO as E, POSES as P, BODY as B, SHOTS as S} from "./base.js";
export const CAST = {claude: false, codex: [.28, -.02]};
export const DETAILS = true, MOOD = "day", SMOOTH = true, ROUND = true, BIGEYES = true, HEAD = 1.12;
export const EMO = {...E,
  nervous: {brow: .4, ang: .5, lid: .05, smile: -.1, wide: 1.08, look: [.25, .35]},
  flat:    {brow: -.05, ang: .05, lid: .4, smile: -.1, wide: 1, look: [.2, .35]},
  resolve: {brow: -.1, ang: .2, lid: .2, smile: 0, wide: 1.02, look: [0, .35], wet: .4},
  open:    {brow: .3, ang: .45, lid: .15, smile: .1, wide: 1.02, look: [0, .35], wet: .8},
  caught:  {brow: .5, ang: .2, lid: 0, smile: -.1, wide: 1.15, look: [0, .35]},
  hope:    {brow: .35, ang: .3, lid: .1, smile: .4, wide: 1.05, look: [0, .35], wet: .5},
};
export const POSES = P, BODY = B;
export const SHOTS = {...S,
  devmid:   {pos: [-.85, 1.3, .25], look: [.02, 1.25, -.9], push: .05, fov: 40, track: "dev", aperture: .06},
  devclose: {pos: [-.72, 1.37, .02], look: [0, 1.32, -.94], push: .06, fov: 41, track: "dev", aperture: .07},
  cx:       {pos: [.68, 1.06, -.72], look: [.28, .98, -.02], push: .05, fov: 40, aperture: .05},
  cxclose:  {pos: [.55, 1.03, -.52], look: [.28, .99, -.02], push: .07, fov: 38, aperture: .06},
  ots:      {pos: [-.62, 1.4, -1.15], look: [.05, 1.0, .2], push: .05, fov: 44},
  two:      {pos: [-.62, 1.9, -1.55], look: [.05, .9, -.2], push: .05, fov: 48},
};
const D2 = (dev, cx, extra = {}) => ({dev, codex: cx, ...extra});
export const DIR = {
  f1:  D2(["nervous", "rest"], ["eager", "idle"]),
  f2:  D2(["nervous", "rest"], ["eager", "nod"]),
  f3:  D2(["nervous", "rest"], ["proud", "idle"]),
  f4:  D2(["nervous", "rest"], ["proud", "idle"]),
  f5:  D2(["nervous", "rest"], ["watch", "idle"]),
  f6:  D2(["nervous", "rest"], ["watch", "idle"]),
  f7:  D2(["nervous", "rest"], ["watch", "idle"]),
  f8:  D2(["nervous", "rest"], ["eager", "idle"]),
  f9:  D2(["flat", "rest"], ["proud", "idle"]),
  f10: D2(["flat", "rest"], ["proud", "bounce"]),
  f11: D2(["nervous", "rest"], ["watch", "idle"]),
  f12: D2(["nervous", "rest"], ["eager", "idle"]),
  f13: D2(["resolve", "rest"], ["oops", "idle"], {punch: .06}),
  f14: D2(["resolve", "rest"], ["watch", "idle"]),
  f15: D2(["open", "rest"], ["soft", "idle"]),
  f16: D2(["open", "slump"], ["sad", "idle"], {punch: .05}),
  f17: D2(["open", "rest"], ["sad", "lookdown"]),
  f18: D2(["open", "rest"], ["watch", "idle"]),
  f19: D2(["nervous", "rest"], ["watch", "idle"]),
  f20: D2(["hope", "rest"], ["warm", "idle"]),
  f21: D2(["hope", "rest"], ["warm", "nod"]),
  f22: D2(["hope", "rest"], ["watch", "idle"]),
  f23: D2(["caught", "rest"], ["oops", "idle"]),
  f24: D2(["caught", "rest"], ["oops", "idle"]),
  f25: D2(["caught", "rest"], ["oops", "idle"], {punch: .06}),
};
