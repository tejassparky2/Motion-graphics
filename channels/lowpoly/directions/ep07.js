// Episode 7, "My AI Deleted the Database. Then Wrote a Report." (ep07_confession.py). Dev, Claude, Codex.
import {EMO as E, POSES as P, BODY as B, SHOTS as S, CL, CX} from "./base.js";
export const CAST = {claude: CL, codex: CX};
export const DETAILS = true, MOOD = "night", SMOOTH = true;
export const EMO = E, POSES = P, BODY = B, SHOTS = S;
export const DIR = {
  h1:  {dev: ["casual", "sip"], claude: ["eager", "nubup"], codex: ["watch", "idle"], cuts: [[0, "claude"], [.7, "devclose"]]},
  h2:  {dev: ["casual", "sip"], claude: ["eager", "idle"], codex: ["watch", "idle"]},
  h3:  {dev: ["casual", "sip"], claude: ["eager", "idle"], codex: ["watch", "idle"], punch: true},
  h4:  {dev: ["stunned", "flinch"], claude: ["eager", "idle"], codex: ["watch", "idle"]},
  h5:  {dev: ["stunned", "rest"], claude: ["proud", "salute"], codex: ["watch", "idle"]},
  h6:  {dev: ["irritated", "pointscreen"], claude: ["eager", "idle"], codex: ["watch", "idle"]},
  h7:  {dev: ["irritated", "rest"], claude: ["proud", "nod"], codex: ["watch", "idle"]},
  h8:  {dev: ["deadpan", "rest"], claude: ["eager", "idle"], codex: ["watch", "idle"]},
  h9:  {dev: ["deadpan", "rest"], claude: ["eager", "nubup"], codex: ["watch", "lookother"], cuts: [[0, "claude"], [.75, "devclose"]]},
  h10: {dev: ["deadpan", "rest"], claude: ["oops", "shrink"], codex: ["suspicious", "idle"]},
  h11: {dev: ["deadpan", "rest"], claude: ["proud", "idle"], codex: ["suspicious", "lookother"]},
  h12: {dev: ["hopeful", "lean"], claude: ["eager", "idle"], codex: ["watch", "idle"]},
  h13: {dev: ["hopeful", "lean"], claude: ["eager", "idle"], codex: ["watch", "idle"]},
  h14: {dev: ["stunned", "sitback"], claude: ["eager", "idle"], codex: ["watch", "idle"], punch: .1},
  h15: {dev: ["stunned", "rest"], claude: ["proud", "nubup"], codex: ["watch", "idle"]},
  h16: {dev: ["sad", "slump"], claude: ["watch", "idle"], codex: ["watch", "idle"]},
  h17: {dev: ["sad", "rest"], claude: ["proud", "cheer"], codex: ["watch", "idle"]},
  h18: {dev: ["deadpan", "rest"], claude: ["eager", "idle"], codex: ["watch", "idle"]},
  h19: {dev: ["deadpan", "rest"], claude: ["eager", "salute"], codex: ["watch", "idle"], cuts: [[0, "claude"], [.6, "devclose"]]},
  h20: {dev: ["done", "rest"], claude: ["eager", "idle"], codex: ["watch", "idle"], punch: .12},
};
