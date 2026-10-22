// Episode 22, "My Manager Wants 10x Output Because of AI" (ep22_tenx.py). Dev and Claude; warm evening room.
import {EMO as E, POSES as P, BODY as B, SHOTS as S} from "./base.js";
export const CAST = {codex: false, claude: [0, -.05]};
export const DETAILS = true, SMOOTH = true, ROUND = true, BIGEYES = true, HEAD = 1.12;
export const EMO = {...E,
  stress:  {brow: .45, ang: .55, lid: .1, smile: -.3, wide: 1.1, look: [.2, .35]},
  frazzle: {brow: .5, ang: .4, lid: .05, smile: -.4, wide: 1.18, look: [.1, .3]},
  low:     {brow: .15, ang: .45, lid: .4, smile: -.25, wide: 1, look: [.1, -.3], wet: .4},
  soft2:   {brow: .2, ang: .35, lid: .2, smile: .25, wide: 1, look: [.25, .35], wet: .6},
  resolve: {brow: -.05, ang: .1, lid: .2, smile: .3, wide: 1.02, look: [.25, .35]},
  grin:    {brow: .3, ang: -.1, lid: .2, smile: .85, wide: 1.05, look: [.25, .35]},
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
  g1:  D2(["stress", "phone"], ["watch", "idle"]),
  g2:  D2(["stress", "rest"], ["shocked", "idle"]),
  g3:  D2(["stress", "rest"], ["soft", "idle"]),
  g4:  D2(["stress", "pointscreen"], ["eager", "idle"]),
  g5:  D2(["stress", "rest"], ["eager", "cheer"]),
  g6:  D2(["frazzle", "type"], ["strain", "strain"]),
  g7:  D2(["frazzle", "rest"], ["oops", "idle"]),
  g8:  D2(["frazzle", "rest"], ["oops", "idle"]),
  g9:  D2(["low", "slump"], ["sad", "idle"]),
  g10: D2(["low", "rest"], ["soft", "nubup"]),
  g11: D2(["low", "rest"], ["soft", "idle"]),
  g12: D2(["low", "rest"], ["soft", "idle"]),
  g13: D2(["low", "rest"], ["soft", "idle"]),
  g14: D2(["low", "rest"], ["soft", "idle"]),
  g15: D2(["low", "rest"], ["soft", "idle"]),
  g16: D2(["low", "rest"], ["soft", "idle"], {punch: .05}),
  g17: D2(["soft2", "rest"], ["warm", "idle"]),
  g18: D2(["soft2", "rest"], ["warm", "nubup"]),
  g19: D2(["soft2", "rest"], ["warm", "idle"]),
  g20: D2(["soft2", "rest"], ["warm", "idle"], {punch: .05}),
  g21: D2(["resolve", "type"], ["warm", "idle"]),
  g22: D2(["resolve", "rest"], ["proud", "idle"]),
  g23: D2(["grin", "phone"], ["watch", "idle"]),
  g24: D2(["grin", "rest"], ["shocked", "idle"], {punch: .07}),
};
