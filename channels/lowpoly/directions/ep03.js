// Episode 3, "I Asked 2 AIs to Fix One Bug" (ep03_great_point.py). Dev, Claude and Codex.
import {EMO as E, POSES as P, BODY as B, SHOTS as S, CL, CX} from "./base.js";
export const CAST = {claude: CL, codex: CX};
export const DETAILS = true, MOOD = "night", SMOOTH = true;
export const EMO = E, POSES = P, BODY = B, SHOTS = S;
export const DIR = {
  d1:  {dev: ["irritated", "pointscreen"], claude: ["watch", "idle"], codex: ["watch", "idle"], flicker: true},
  d2:  {dev: ["irritated", "rest"], claude: ["warm", "lookother"], codex: ["eager", "idle"]},
  d3:  {dev: ["irritated", "rest"], claude: ["warm", "idle"], codex: ["warm", "lookother"]},
  d4:  {dev: ["deadpan", "rest"], claude: ["warm", "lookother"], codex: ["proud", "idle"]},
  d5:  {dev: ["deadpan", "rest"], claude: ["proud", "idle"], codex: ["warm", "lookother"]},
  d6:  {dev: ["panic2", "lean"], claude: ["warm", "idle"], codex: ["warm", "idle"]},
  d7:  {dev: ["panic2", "rest"], claude: ["warm", "nubup"], codex: ["eager", "idle"]},
  d8:  {dev: ["deadpan", "rest"], claude: ["warm", "idle"], codex: ["warm", "nod"]},
  d9:  {dev: ["deadpan", "rest"], claude: ["warm", "lookother"], codex: ["eager", "idle"], cuts: [[0, "duo"]]},
  d10: {dev: ["deadpan", "rest"], claude: ["proud", "idle"], codex: ["proud", "bounce"]},
  d11: {dev: ["irritated", "type"], claude: ["watch", "idle"], codex: ["watch", "idle"], flicker: true},
  d12: {dev: ["smug", "rest"], claude: ["shocked", "freeze"], codex: ["shocked", "idle"]},
  d13: {dev: ["smug", "rest"], claude: ["eager", "cheer"], codex: ["eager", "idle"]},
  d14: {dev: ["deadpan", "rest"], claude: ["warm", "idle"], codex: ["eager", "bounce"]},
  d15: {dev: ["deadpan", "rest"], claude: ["warm", "lookother"], codex: ["warm", "idle"], cuts: [[0, "duo"]]},
  d16: {dev: ["done", "rest"], claude: ["warm", "idle"], codex: ["warm", "idle"], headdesk: .6, cuts: [[0, "devclose"], [.4, "endside"]]},
};
