// Episode 5, "I Asked Codex for One Tiny Change" (ep05_button_blue.py). Dev and Codex only.
import {EMO as E, POSES as P, BODY as B, SHOTS as S} from "./base.js";
export const CAST = {claude: false, codex: [.1, -.02]};
export const DETAILS = true, MOOD = "night", SMOOTH = true;
export const EMO = E, POSES = P, BODY = B, SHOTS = S;
export const DIR = {
  f1:  {dev: ["irritated", "pointscreen"], codex: ["watch", "idle"]},
  f2:  {dev: ["irritated", "rest"], codex: ["eager", "spin"]},
  f3:  {dev: ["irritated", "rest"], codex: ["proud", "bounce"]},
  f4:  {dev: ["stunned", "rest"], codex: ["proud", "idle"]},
  f5:  {dev: ["stunned", "rest"], codex: ["eager", "nod"]},
  f6:  {dev: ["deadpan", "rest"], codex: ["eager", "idle"]},
  f7:  {dev: ["deadpan", "rest"], codex: ["proud", "bounce"]},
  f8:  {dev: ["deadpan", "rest"], codex: ["eager", "idle"]},
  f9:  {dev: ["deadpan", "rest"], codex: ["proud", "idle"]},
  f10: {dev: ["stunned", "rest"], codex: ["eager", "idle"]},
  f11: {dev: ["stunned", "rest"], codex: ["eager", "wave"]},
  f12: {dev: ["panic2", "pointscreen"], codex: ["eager", "idle"]},
  f13: {dev: ["panic2", "rest"], codex: ["eager", "spin"]},
  f14: {dev: ["panic2", "lunge"], codex: ["eager", "idle"]},
  f15: {dev: ["panic2", "rest"], codex: ["neutral", "glitch"]},
  f16: {dev: ["stunned", "rest"], codex: ["proud", "bounce"]},
  f17: {dev: ["smallsmile", "rest"], codex: ["warm", "idle"]},
  f18: {dev: ["done", "rest"], codex: ["eager", "bounce"], headdesk: 1.2, cuts: [[0, "cxsolo"], [.85, "endside"]]},
};
