// Episode 36, AI news: LiteLLM hack (ep36_litellm.py). Dev and Codex; night.
import {EMO as E, POSES as P, BODY as B, SHOTS as S} from "./base.js";
export const CAST = {claude: false, codex: [0, -.02]};
export const DETAILS = true, MOOD = "night", SMOOTH = true, ROUND = true, BIGEYES = true, HEAD = 1.12;
export const EMO = {...E,
  flat:    {brow: -.05, ang: .05, lid: .45, smile: -.1, wide: .98, look: [.15, .35]},
  done:    {brow: -.2, ang: .1, lid: .5, smile: -.25, wide: .95, look: [.15, .35]},
  baffled: {brow: .5, ang: .2, lid: 0, smile: -.15, wide: 1.15, look: [.1, .35]},
  hyped:   {brow: .4, ang: 0, lid: 0, smile: .9, wide: 1.12, look: [.15, .35], happyEyes: .3},
  grin:    {brow: .25, ang: .1, lid: .25, smile: .85, wide: 1, look: [.15, .3], happyEyes: .6},
  tired2:  {brow: .1, ang: .45, lid: .45, smile: -.35, wide: .95, look: [.2, .1]},
  touched: {brow: .3, ang: .4, lid: .1, smile: .35, wide: 1.05, look: [.15, .35]},
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
  n1: D2(["hyped", "rest"], ["watch", "idle"]),
  n2: D2(["squint", "rest"], ["eager", "idle"]),
  n3: D2(["baffled", "rest"], ["watch", "idle"]),
  n4: D2(["squint", "rest"], ["eager", "idle"]),
  n5: D2(["squint", "rest"], ["watch", "idle"]),
  n6: D2(["squint", "rest"], ["watch", "idle"]),
  n7: D2(["squint", "rest"], ["eager", "idle"]),
  n8: D2(["baffled", "rest"], ["watch", "idle"]),
  n9: D2(["squint", "rest"], ["watch", "idle"]),
  n10: D2(["squint", "rest"], ["watch", "idle"]),
  n11: D2(["squint", "rest"], ["eager", "idle"]),
  n12: D2(["baffled", "rest"], ["watch", "idle"]),
  n13: D2(["squint", "rest"], ["eager", "idle"]),
  n14: D2(["tired2", "rest"], ["watch", "idle"]),
  n15: D2(["squint", "rest"], ["watch", "idle"]),
  n16: D2(["squint", "rest"], ["eager", "idle"]),
  n17: D2(["squint", "rest"], ["watch", "idle"]),
  n18: D2(["squint", "rest"], ["watch", "idle"]),
  n19: D2(["tired2", "rest"], ["watch", "idle"]),
  n20: D2(["squint", "rest"], ["deadpan", "idle"]),
};
