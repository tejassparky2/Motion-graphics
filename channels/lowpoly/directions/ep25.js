// Episode 25, "I Let My AI Be My Lawyer" (ep25_lawyer.py). Dev and Claude; the judge is a video-call card on the
// monitor (ots shots); morning.
import {EMO as E, POSES as P, BODY as B, SHOTS as S} from "./base.js";
export const CAST = {codex: false, claude: [0, -.05]};
export const DETAILS = true, MOOD = "day", SMOOTH = true, ROUND = true, BIGEYES = true, HEAD = 1.12;
export const EMO = {...E,
  confident: {brow: .1, ang: -.1, lid: .15, smile: .4, wide: 1.02, look: [.2, .35]},
  nervous:   {brow: .4, ang: .5, lid: .05, smile: -.1, wide: 1.08, look: [.2, .35]},
  caught:    {brow: .5, ang: .2, lid: 0, smile: -.15, wide: 1.18, look: [0, .35]},
  done:      {brow: -.2, ang: .1, lid: .5, smile: -.25, wide: .95, look: [.15, .35]},
};
export const POSES = P, BODY = B;
export const SHOTS = {...S,
  devmid:   {pos: [-.85, 1.3, .25], look: [.02, 1.25, -.9], push: .05, fov: 40, track: "dev", aperture: .06},
  devclose: {pos: [-.72, 1.37, .02], look: [0, 1.32, -.94], push: .06, fov: 41, track: "dev", aperture: .07},
  solo:     {pos: [-.42, 1.0, -.72], look: [0, .9, -.05], push: .05, fov: 40, aperture: .05},
  soloclose:{pos: [-.26, .98, -.7], look: [0, .91, -.05], push: .07, fov: 40, aperture: .06},
  ots:      {pos: [-.62, 1.4, -1.15], look: [.05, 1.0, .2], push: .05, fov: 44},
};
const D2 = (dev, cl, extra = {}) => ({dev, claude: cl, ...extra});
export const DIR = {
  k1:  D2(["confident", "rest"], ["eager", "idle"]),
  k2:  D2(["confident", "rest"], ["proud", "nubup"]),
  k3:  D2(["squint", "rest"], ["proud", "idle"]),
  k4:  D2(["squint", "rest"], ["proud", "nubup"]),
  k5:  D2(["nervous", "rest"], ["watch", "idle"]),
  k6:  D2(["confident", "rest"], ["proud", "idle"]),
  k7:  D2(["nervous", "rest"], ["watch", "idle"]),
  k8:  D2(["nervous", "rest"], ["eager", "idle"]),
  k9:  D2(["nervous", "rest"], ["proud", "idle"]),
  k10: D2(["caught", "rest"], ["shocked", "idle"]),
  k11: D2(["caught", "rest"], ["shocked", "freeze"], {punch: .06}),
  k12: D2(["caught", "rest"], ["eager", "cheer"]),
  k13: D2(["done", "pointscreen"], ["oops", "idle"]),
  k14: D2(["caught", "rest"], ["sheepish", "idle"]),
  k15: D2(["nervous", "rest"], ["watch", "idle"]),
  k16: D2(["done", "rest"], ["watch", "idle"]),
  k17: D2(["done", "rest"], ["eager", "nubup"]),
  k18: D2(["done", "slump"], ["oops", "idle"], {punch: .06}),
};
