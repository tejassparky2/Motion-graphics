// Episode 10, "My AI Refused to Write Code" (ep10_refuse.py). Dev, Codex (refuses), Claude (over-delivers).
import {EMO as E, POSES as P, BODY as B, SHOTS as S, CL, CX} from "./base.js";
export const CAST = {claude: CL, codex: CX};
export const DETAILS = true, MOOD = "night", SMOOTH = true;
export const EMO = E, POSES = P, BODY = B, SHOTS = S;
export const DIR = {
  k1:  {dev: ["irritated", "pointscreen"], claude: ["watch", "idle"], codex: ["watch", "idle"], cuts: [[0, "dev"], [.75, "codexclose"]]},
  k2:  {dev: ["irritated", "rest"], claude: ["watch", "idle"], codex: ["suspicious", "headshake"], punch: .08},
  k3:  {dev: ["stunned", "flinch"], claude: ["watch", "idle"], codex: ["suspicious", "idle"]},
  k4:  {dev: ["stunned", "rest"], claude: ["watch", "idle"], codex: ["suspicious", "nod"]},
  k5:  {dev: ["deadpan", "rest"], claude: ["watch", "idle"], codex: ["watch", "idle"]},
  k6:  {dev: ["deadpan", "sitback"], claude: ["watch", "idle"], codex: ["proud", "bounce"]},
  k7:  {dev: ["irritated", "pointscreen"], claude: ["eager", "idle"], codex: ["suspicious", "lookother"], cuts: [[0, "dev"], [.5, "claude"]]},
  k8:  {dev: ["irritated", "rest"], claude: ["proud", "cheer"], codex: ["suspicious", "idle"], punch: true},
  k9:  {dev: ["stunned", "rest"], claude: ["eager", "idle"], codex: ["watch", "idle"]},
  k10: {dev: ["stunned", "doubletake"], claude: ["proud", "nubup"], codex: ["watch", "idle"]},
  k11: {dev: ["tired", "rest"], claude: ["eager", "idle"], codex: ["suspicious", "nod"], cuts: [[0, "codex"], [.7, "devclose"]]},
  k12: {dev: ["tired", "slump"], claude: ["watch", "idle"], codex: ["watch", "idle"]},
  k13: {dev: ["tired", "rest"], claude: ["eager", "idle"], codex: ["proud", "idle"]},
  k14: {dev: ["sad", "type"], claude: ["watch", "idle"], codex: ["watch", "idle"], cuts: [[0, "ots"], [.55, "devclose"]]},
  k15: {dev: ["sad", "rest"], claude: ["watch", "idle"], codex: ["suspicious", "idle"], punch: .1},
  k16: {dev: ["deadpan", "rest"], claude: ["eager", "cheer"], codex: ["watch", "idle"]},
  k17: {dev: ["pleading", "leanin"], claude: ["watch", "idle"], codex: ["watch", "idle"], cuts: [[0, "devclose"], [.6, "codexclose"]]},
  k18: {dev: ["done", "rest"], claude: ["watch", "idle"], codex: ["suspicious", "headshake"], punch: .12},
};
