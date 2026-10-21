// Test only: the big glossy eyes, wet eyes and a tear (ep15 timing).
import * as E15 from "./ep15.js";
export const CAST = E15.CAST, SHOTS = E15.SHOTS, POSES = E15.POSES, BODY = E15.BODY;
export const DETAILS = true, MOOD = "night", SMOOTH = true, BIGEYES = true, HEAD = 1.12, ROUND = true;
export const EMO = {...E15.EMO,
  teary: {brow: .35, ang: .6, lid: .25, smile: -.2, wide: 1, look: [.3, .2], wet: 1},
  crying: {brow: .4, ang: .7, lid: .35, smile: -.35, wide: 1, look: [0, -.2], wet: 1, tear: 1},
};
const D3 = (dev, jr, cl, extra = {}) => ({dev, junior: jr, claude: cl, ...extra});
export const DIR = Object.fromEntries(Object.keys(E15.DIR).map((k, i) => [k, D3([["teary", "crying", "smallsmile", "stunned"][i % 4], "rest"], ["teary", "rest"], ["soft", "idle"], {cuts: [[0, i % 2 ? "jrclose" : "devclose"]]})]));
