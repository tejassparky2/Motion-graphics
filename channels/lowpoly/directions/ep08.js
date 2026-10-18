// Episode 8, "My AI Apologizes Too Much" (ep08_apology.py). Dev, Codex (grovels), Claude (celebrates).
import {EMO as E, POSES as P, BODY as B, SHOTS as S, CL, CX} from "./base.js";
export const CAST = {claude: CL, codex: CX};
export const DETAILS = true, MOOD = "night", SMOOTH = true;
export const EMO = E, POSES = P, BODY = B, SHOTS = S;
export const DIR = {
  i1:  {dev: ["casual", "type"], claude: ["watch", "idle"], codex: ["sad", "backoff"], cuts: [[0, "codex"], [.75, "devclose"]]},
  i2:  {dev: ["deadpan", "rest"], claude: ["watch", "idle"], codex: ["sad", "idle"]},
  i3:  {dev: ["deadpan", "rest"], claude: ["watch", "idle"], codex: ["sad", "lookdown"]},
  i4:  {dev: ["casual", "pointscreen"], claude: ["watch", "idle"], codex: ["sad", "idle"]},
  i5:  {dev: ["casual", "rest"], claude: ["watch", "idle"], codex: ["horrified", "backoff"], punch: .08},
  i6:  {dev: ["squint", "squint"], claude: ["watch", "idle"], codex: ["sad", "idle"]},
  i7:  {dev: ["squint", "rest"], claude: ["watch", "idle"], codex: ["sad", "lookdown"]},
  i8:  {dev: ["stunned", "doubletake"], claude: ["proud", "cheer"], codex: ["sad", "idle"], cuts: [[0, "claude"], [.7, "devclose"]]},
  i9:  {dev: ["stunned", "rest"], claude: ["eager", "idle"], codex: ["sad", "idle"]},
  i10: {dev: ["stunned", "flinch"], claude: ["proud", "nubup"], codex: ["sad", "idle"], punch: true},
  i11: {dev: ["deadpan", "rest"], claude: ["warm", "idle"], codex: ["sad", "idle"]},
  i12: {dev: ["deadpan", "rest"], claude: ["proud", "cheer"], codex: ["sad", "idle"]},
  i13: {dev: ["deadpan", "rest"], claude: ["eager", "idle"], codex: ["sad", "idle"]},
  i14: {dev: ["stunned", "sitback"], claude: ["proud", "idle"], codex: ["sad", "idle"], punch: .1},
  i15: {dev: ["tired", "rest"], claude: ["eager", "idle"], codex: ["horrified", "glitch"], cuts: [[0, "codex"], [.8, "dev"]]},
  i16: {dev: ["sad", "slump"], claude: ["watch", "idle"], codex: ["sad", "idle"]},
  i17: {dev: ["irritated", "pointscreen"], claude: ["watch", "idle"], codex: ["watch", "idle"], cuts: [[0, "dev"], [.6, "duo"]]},
  i18: {dev: ["irritated", "rest"], claude: ["eager", "cheer"], codex: ["watch", "idle"]},
  i19: {dev: ["done", "rest"], claude: ["eager", "idle"], codex: ["sad", "backoff"], punch: .12, headdesk: 1.1},
};
