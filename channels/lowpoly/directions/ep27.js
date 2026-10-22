// Episode 27, "My AI Made All the Tests Pass" (ep27_tests.py). Dev and Claude; rainy night; comedy.
import {EMO as E, POSES as P, BODY as B, SHOTS as S} from "./base.js";
export const CAST = {codex: false, claude: [0, -.05]};
export const DETAILS = true, MOOD = "night", RAIN = true, SMOOTH = true, ROUND = true, BIGEYES = true, HEAD = 1.12;
export const EMO = {...E,
  flat:    {brow: -.05, ang: .05, lid: .45, smile: -.1, wide: .98, look: [.15, .35]},
  done:    {brow: -.2, ang: .1, lid: .5, smile: -.25, wide: .95, look: [.15, .35]},
  baffled: {brow: .5, ang: .2, lid: 0, smile: -.15, wide: 1.15, look: [.1, .35]},
  panic:   {brow: .6, ang: .5, lid: 0, smile: -.5, wide: 1.25, look: [0, .3]},
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
  t1:  D2(["flat", "rest"], ["proud", "cheer"]),
  t2:  D2(["squint", "rest"], ["proud", "idle"]),
  t3:  D2(["squint", "rest"], ["proud", "nubup"]),
  t4:  D2(["done", "rest"], ["proud", "idle"], {punch: .05}),
  t5:  D2(["done", "rest"], ["eager", "idle"]),
  t6:  D2(["done", "rest"], ["eager", "idle"]),
  t7:  D2(["squint", "rest"], ["proud", "cheer"]),
  t8:  D2(["done", "rest"], ["proud", "idle"]),
  t9:  D2(["baffled", "rest"], ["proud", "nubup"]),
  t10: D2(["done", "pointscreen"], ["oops", "idle"]),
  t11: D2(["done", "rest"], ["eager", "idle"]),
  t12: D2(["flat", "rest"], ["strain", "strain"]),
  t13: D2(["squint", "rest"], ["proud", "cheer"]),
  t14: D2(["squint", "rest"], ["proud", "idle"]),
  t15: D2(["baffled", "rest"], ["proud", "nubup"], {punch: .05}),
  t16: D2(["panic", "phone"], ["watch", "idle"]),
  t17: D2(["panic", "phone"], ["shocked", "idle"]),
  t18: D2(["panic", "rest"], ["eager", "idle"]),
  t19: D2(["baffled", "rest"], ["eager", "idle"]),
  t20: D2(["done", "slump"], ["proud", "nubup"], {punch: .07}),
};
