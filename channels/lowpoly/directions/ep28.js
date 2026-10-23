// Episode 28, "I Asked Claude to Make GTA 5" (ep28_gta.py). Dev and Claude; night; reference 10's form (Claude flat).
import {EMO as E, POSES as P, BODY as B, SHOTS as S} from "./base.js";
export const CAST = {codex: false, claude: [0, -.05]};
export const DETAILS = true, MOOD = "night", SMOOTH = true, ROUND = true, BIGEYES = true, HEAD = 1.12;
export const EMO = {...E,
  flat:    {brow: -.05, ang: .05, lid: .45, smile: -.1, wide: .98, look: [.15, .35]},
  done:    {brow: -.2, ang: .1, lid: .5, smile: -.25, wide: .95, look: [.15, .35]},
  baffled: {brow: .5, ang: .2, lid: 0, smile: -.15, wide: 1.15, look: [.1, .35]},
  hyped:   {brow: .4, ang: 0, lid: 0, smile: .9, wide: 1.12, look: [.15, .35], happyEyes: .3},
  grin:    {brow: .25, ang: .1, lid: .25, smile: .85, wide: 1, look: [.15, .3], happyEyes: .6},
};
export const POSES = P, BODY = B;
export const SHOTS = {...S,
  devmid:   {pos: [-.85, 1.3, .25], look: [.02, 1.25, -.9], push: .05, fov: 40, track: "dev", aperture: .06},
  devclose: {pos: [-.72, 1.37, .02], look: [0, 1.32, -.94], push: .06, fov: 41, track: "dev", aperture: .07},
  solo:     {pos: [-.42, 1.0, -.72], look: [0, .9, -.05], push: .05, fov: 40, aperture: .05},
  soloclose:{pos: [-.26, .98, -.7], look: [0, .91, -.05], push: .07, fov: 40, aperture: .06},
  ots:      {pos: [-.62, 1.4, -1.15], look: [.05, .95, .15], push: .05, fov: 44},
};
const D2 = (dev, cl, extra = {}) => ({dev, claude: cl, ...extra});
export const DIR = {
  g1:  D2(["done", "rest"], ["watch", "idle"]),
  g2:  D2(["hyped", "rest"], ["watch", "idle"]),
  g3:  D2(["hyped", "rest"], ["flat", "idle"]),
  g4:  D2(["hyped", "pointscreen"], ["flat", "idle"]),
  g5:  D2(["hyped", "rest"], ["flat", "nubup"]),
  g6:  D2(["flat", "rest"], ["flat", "idle"]),
  g7:  D2(["squint", "rest"], ["flat", "idle"]),
  g8:  D2(["squint", "rest"], ["flat", "idle"]),
  g9:  D2(["baffled", "rest"], ["flat", "idle"], {punch: .05}),
  g10: D2(["hyped", "rest"], ["flat", "idle"]),
  g11: D2(["hyped", "rest"], ["flat", "nubup"]),
  g12: D2(["baffled", "rest"], ["flat", "idle"]),
  g13: D2(["done", "rest"], ["flat", "idle"], {punch: .05}),
  g13h: D2(["squint", "rest"], ["flat", "idle"]),
  g14: D2(["squint", "rest"], ["flat", "idle"]),
  g15: D2(["squint", "rest"], ["flat", "idle"]),
  g16: D2(["baffled", "rest"], ["flat", "idle"]),
  g17: D2(["done", "rest"], ["flat", "idle"], {punch: .05}),
  g17h: D2(["grin", "rest"], ["watch", "idle"]),
  g18: D2(["grin", "rest"], ["watch", "idle"]),
  g19: D2(["grin", "rest"], ["flat", "idle"]),
  g20: D2(["grin", "rest"], ["soft", "idle"]),
  g21: D2(["grin", "rest"], ["proud", "idle"]),
};
