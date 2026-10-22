// Episode 24, "My AI Recommended a Package That Doesn't Exist" (ep24_package.py). Dev and Codex; night; comedy.
import {EMO as E, POSES as P, BODY as B, SHOTS as S} from "./base.js";
export const CAST = {claude: false, codex: [0, -.02]};
export const DETAILS = true, MOOD = "night", SMOOTH = true, ROUND = true, BIGEYES = true, HEAD = 1.12;
export const EMO = {...E,
  flat:    {brow: -.05, ang: .05, lid: .45, smile: -.1, wide: .98, look: [.15, .35]},
  done:    {brow: -.2, ang: .1, lid: .5, smile: -.2, wide: .95, look: [.15, .35]},
  baffled: {brow: .5, ang: .2, lid: 0, smile: -.15, wide: 1.15, look: [.1, .35]},
};
export const POSES = P, BODY = B;
export const SHOTS = {...S,
  devmid:   {pos: [-.85, 1.3, .25], look: [.02, 1.25, -.9], push: .05, fov: 40, track: "dev", aperture: .06},
  devclose: {pos: [-.72, 1.37, .02], look: [0, 1.32, -.94], push: .06, fov: 41, track: "dev", aperture: .07},
  cx:       {pos: [.42, 1.06, -.76], look: [0, .98, -.02], push: .05, fov: 40, aperture: .05},
  cxclose:  {pos: [.3, 1.03, -.56], look: [0, .99, -.02], push: .07, fov: 38, aperture: .06},
  ots:      {pos: [-.62, 1.4, -1.15], look: [.05, .95, .15], push: .05, fov: 44},
};
const D2 = (dev, cx, extra = {}) => ({dev, codex: cx, ...extra});
export const DIR = {
  p1:  D2(["flat", "type"], ["proud", "idle"]),
  p2:  D2(["flat", "rest"], ["proud", "idle"]),
  p3:  D2(["flat", "rest"], ["eager", "bounce"]),
  p4:  D2(["deadpan", "type"], ["eager", "idle"]),
  p5:  D2(["deadpan", "rest"], ["eager", "idle"]),
  p6:  D2(["done", "type"], ["eager", "idle"]),
  p7:  D2(["done", "rest"], ["proud", "idle"]),
  p8:  D2(["done", "rest"], ["sheepish", "idle"], {punch: .06}),
  p9:  D2(["done", "rest"], ["proud", "idle"]),
  p10: D2(["squint", "rest"], ["sheepish", "idle"]),
  p11: D2(["squint", "rest"], ["proud", "idle"]),
  p12: D2(["baffled", "rest"], ["eager", "nod"]),
  p13: D2(["baffled", "rest"], ["proud", "idle"]),
  p14: D2(["stunned", "rest"], ["proud", "idle"]),
  p15: D2(["stunned", "rest"], ["proud", "idle"]),
  p16: D2(["stunned", "rest"], ["proud", "idle"], {punch: .06}),
  p17: D2(["baffled", "rest"], ["proud", "idle"]),
  p18: D2(["baffled", "rest"], ["proud", "idle"], {punch: .07}),
};
