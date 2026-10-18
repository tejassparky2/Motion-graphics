// Episode 9, "I Built an App in an Hour. Nobody Knows How It Works." (ep09_vibe.py). Dev and Claude only; warm room.
import {EMO as E, POSES as P, BODY as B, SHOTS as S} from "./base.js";
export const CAST = {codex: false, claude: [0, -.05]};
export const DETAILS = true, SMOOTH = true;
export const EMO = E, POSES = P, BODY = B, SHOTS = S;
export const DIR = {
  j1:  {dev: ["smug", "pointscreen"], claude: ["watch", "idle"], cuts: [[0, "dev"], [.8, "devclose"]]},
  j2:  {dev: ["squint", "squint"], claude: ["watch", "idle"]},
  j3:  {dev: ["squint", "rest"], claude: ["sheepish", "idle"], punch: .08},
  j4:  {dev: ["deadpan", "rest"], claude: ["sheepish", "idle"]},
  j5:  {dev: ["deadpan", "rest"], claude: ["proud", "nubup"]},
  j6:  {dev: ["irritated", "pointscreen"], claude: ["eager", "idle"]},
  j7:  {dev: ["stunned", "flinch"], claude: ["proud", "cheer"], punch: true},
  j8:  {dev: ["squint", "squint"], claude: ["watch", "idle"]},
  j9:  {dev: ["deadpan", "rest"], claude: ["sheepish", "shrink"]},
  j10: {dev: ["hopeful", "rest"], claude: ["watch", "idle"]},
  j11: {dev: ["deadpan", "sitback"], claude: ["eager", "idle"]},
  j12: {dev: ["irritated", "type"], claude: ["eager", "idle"]},
  j13: {dev: ["stunned", "doubletake"], claude: ["proud", "cheer"], cuts: [[0, "solo"], [.7, "devclose"]]},
  j14: {dev: ["stunned", "rest"], claude: ["eager", "idle"]},
  j15: {dev: ["deadpan", "rest"], claude: ["eager", "nod"], punch: .08},
  j16: {dev: ["sad", "slump"], claude: ["soft", "idle"]},
  j17: {dev: ["sad", "rest"], claude: ["soft", "nubup"]},
  j18: {dev: ["smallsmile", "type"], claude: ["soft", "idle"], cuts: [[0, "ots"], [.6, "devclose"]]},
  j19: {dev: ["smallsmile", "rest"], claude: ["sheepish", "idle"]},
  j20: {dev: ["smallsmile", "rest"], claude: ["soft", "idle"]},
  j21: {dev: ["smallsmile", "rest"], claude: ["eager", "nubup"]},
  j22: {dev: ["deadpan", "rest"], claude: ["oops", "shrink"], punch: .1},
};
