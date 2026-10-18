// Episode 6, "Explain It Like I'm Five" (ep06_simpler.py). Dev and Claude; Codex pops up for the answer.
import {EMO as E, POSES as P, BODY as B, SHOTS as S, CL, CX} from "./base.js";
export const CAST = {claude: CL, codex: CX};
export const DETAILS = true, SMOOTH = true;
export const EMO = E, POSES = P, BODY = B, SHOTS = S;
export const DIR = {
  g1:  {dev: ["tired", "pointscreen"], claude: ["watch", "idle"], codex: ["hidden", "idle"]},
  g2:  {dev: ["tired", "rest"], claude: ["proud", "nubup"], codex: ["hidden", "idle"]},
  g3:  {dev: ["deadpan", "rest"], claude: ["proud", "idle"], codex: ["hidden", "idle"]},
  g4:  {dev: ["deadpan", "rest"], claude: ["eager", "nubup"], codex: ["hidden", "idle"]},
  g5:  {dev: ["deadpan", "rest"], claude: ["eager", "idle"], codex: ["hidden", "idle"]},
  g6:  {dev: ["deadpan", "rest"], claude: ["eager", "nubup"], codex: ["hidden", "idle"]},
  g7:  {dev: ["irritated", "lean"], claude: ["oops", "idle"], codex: ["hidden", "idle"]},
  g8:  {dev: ["irritated", "lean"], claude: ["sad", "freeze"], codex: ["hidden", "idle"]},
  g9:  {dev: ["deadpan", "rest"], claude: ["sad", "idle"], codex: ["hidden", "idle"]},
  g10: {dev: ["stunned", "rest"], claude: ["sad", "idle"], codex: ["proud", "popup"]},
  g11: {dev: ["stunned", "rest"], claude: ["oops", "idle"], codex: ["proud", "idle"]},
  g12: {dev: ["deadpan", "rest"], claude: ["oops", "idle"], codex: ["proud", "nod"]},
  g13: {dev: ["irritated", "rest"], claude: ["oops", "idle"], codex: ["watch", "idle"]},
  g14: {dev: ["irritated", "rest"], claude: ["polite", "idle"], codex: ["watch", "idle"]},
  g15: {dev: ["deadpan", "rest"], claude: ["polite", "idle"], codex: ["oops", "idle"]},
  g16: {dev: ["deadpan", "rest"], claude: ["warm", "cheer"], codex: ["watch", "idle"]},
};
