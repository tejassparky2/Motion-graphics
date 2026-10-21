// Episode 16, "They're Retiring My Claude Tomorrow" (ep16_retire.py). Dev and Claude; night, then morning light.
// Held shots (no reaction cuts), big glossy eyes, a tear at the peak.
import {EMO as E, POSES as P, BODY as B, SHOTS as S} from "./base.js";
export const CAST = {codex: false, claude: [0, -.05]};
export const DETAILS = true, MOOD = "night", SMOOTH = true, ROUND = true, BIGEYES = true, HEAD = 1.12, DAWN = "a21";
export const EMO = {...E,
  flat:     {brow: -.05, ang: .05, lid: .4, smile: -.05, wide: 1, look: [.2, .35]},
  low:      {brow: .15, ang: .45, lid: .35, smile: -.2, wide: 1, look: [.1, -.25], wet: .3},
  teary:    {brow: .35, ang: .6, lid: .25, smile: -.15, wide: 1.02, look: [.25, .3], wet: .9},
  crying:   {brow: .4, ang: .7, lid: .3, smile: -.1, wide: 1, look: [.25, .3], wet: 1, tear: 1},
  laughcry: {brow: .3, ang: .4, lid: .2, smile: .8, wide: 1, look: [.2, .3], wet: 1, tear: 1, happyEyes: 1},
  amused:   {brow: .1, ang: .1, lid: .3, smile: .45, wide: 1, look: [.25, .35]},
  bright:   {brow: .4, ang: -.1, lid: 0, smile: .9, wide: 1.1, look: [0, .3]},
};
export const POSES = P, BODY = B;
export const SHOTS = {...S,
  devmid:  {pos: [-.85, 1.3, .25], look: [.02, 1.25, -.9], push: .05, fov: 40, track: "dev", aperture: .06},
  devclose:{pos: [-.72, 1.37, .02], look: [0, 1.32, -.94], push: .06, fov: 41, track: "dev", aperture: .07},
  solo:    {pos: [-.42, 1.0, -.72], look: [0, .9, -.05], push: .05, fov: 40, aperture: .05},
  soloclose:{pos: [-.26, .98, -.7], look: [0, .91, -.05], push: .07, fov: 40, aperture: .06},
  ots:     {pos: [-.32, 1.5, -1.42], look: [0, .95, .05], push: .06, fov: 44},
  endside: {pos: [-1.3, 1.75, -1.75], look: [-.05, 1.05, -.4], push: .05, fov: 50},
};
const D2 = (dev, cl, extra = {}) => ({dev, claude: cl, ...extra});
const W = ["watch", "idle"];
export const DIR = {
  a1:  D2(["low", "rest"], ["sad", "idle"]),
  a2:  D2(["low", "rest"], ["soft", "idle"]),
  a3:  D2(["flat", "rest"], ["soft", "idle"]),
  a4:  D2(["low", "slump"], ["soft", "idle"]),
  a5:  D2(["low", "rest"], ["warm", "nubup"]),
  a6:  D2(["teary", "rest"], ["soft", "idle"], {punch: .05}),
  a7:  D2(["teary", "rest"], ["soft", "idle"]),
  a8:  D2(["flat", "rest"], ["soft", "idle"]),
  a9:  D2(["amused", "rest"], ["warm", "idle"]),
  a10: D2(["amused", "sitback"], ["warm", "idle"]),
  a10b: D2(["low", "rest"], ["soft", "idle"]),
  a10c: D2(["teary", "rest"], ["soft", "lookdown"]),
  a11: D2(["low", "rest"], ["soft", "idle"]),
  a12: D2(["low", "rest"], ["soft", "idle"]),
  a13: D2(["teary", "rest"], ["soft", "idle"]),
  a14: D2(["teary", "rest"], ["sad", "lookdown"]),
  a15: D2(["teary", "rest"], ["soft", "lookdown"], {punch: .05}),
  a16: D2(["teary", "rest"], ["soft", "idle"]),
  a17: D2(["teary", "rest"], ["warm", "idle"]),
  a18: D2(["crying", "rest"], ["soft", "idle"], {punch: .05}),
  a19: D2(["crying", "rest"], ["warm", "idle"]),
  a20: D2(["low", "slump"], ["soft", "idle"]),
  a21: D2(["teary", "rest"], ["bright", "cheer"]),
  a22: D2(["teary", "rest"], ["bright", "idle"]),
  a23: D2(["teary", "rest"], ["eager", "idle"]),
  a24: D2(["teary", "rest"], ["eager", "idle"]),
  a25: D2(["crying", "rest"], ["warm", "idle"]),
  a26: D2(["crying", "rest"], ["warm", "nubup"]),
  a27: D2(["crying", "rest"], ["warm", "idle"], {punch: .06}),
  a28: D2(["laughcry", "sitback"], ["eager", "idle"]),
};
