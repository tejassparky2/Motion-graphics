// Episode 2, "When Your AI Forgets the Whole Project" (ep02_context_left.py). Dev + Codex; Claude pops up at line 20.
// Per line: [emotion, pose]; `cuts` switch shots inside a line ([fraction of the line, shot]).
import {EMO as E1, POSES as P1, BODY as B1} from "./ep01ar.js";
export const CAST = {codex: [.1, -.02], claude: [-.24, -.05], claudeFrom: "c20"};
export const DETAILS = true;
export const MOOD = "night";
export const SMOOTH = true;
export const EMO = {...E1,
  exhausted: {brow: -.1, ang: .3, lid: .55, smile: -.3, wide: 1, look: [0, .3]},
  calm:      {brow: 0, ang: .2, lid: .45, smile: .05, wide: 1, look: [0, .35]},
  panic2:    {brow: .55, ang: .55, lid: 0, smile: -.6, wide: 1.35, look: [0, .35]},
  blank:     {brow: .2, ang: 0, lid: 0, smile: .5, wide: 1.1, look: [0, .3]},
};
export const POSES = {...P1, hair: [[-2.35, -.3, -2.05], [-2.35, -.3, -2.05]]};
export const BODY = {...B1, hair: [.3, .3, .15], type: [.7, 0, .12]};
export const SHOTS = {
  codex:       {pos: [.55, 1.06, -.76], look: [.1, .98, -.02], push: .12, fov: 40},
  codexclose:  {pos: [.42, 1.03, -.56], look: [.1, .99, -.02], push: .14, fov: 38},
  codexcu:     {pos: [.34, 1.02, -.42], look: [.1, .99, -.02], push: .1, fov: 42},
  claudepop:   {pos: [-.58, .98, -.64], look: [-.24, .88, -.05], push: .12, fov: 40},
  dev:         {pos: [-1.0, 1.28, .4], look: [.02, 1.12, -.88], push: .12, fov: 44, track: "dev"},
  devclose:    {pos: [-.75, 1.32, -.1], look: [0, 1.25, -.94], push: .08, fov: 44, track: "dev"},
  ots:         {pos: [-.3, 1.45, -1.38], look: [0, .95, .1], push: .1, fov: 46},
  endside:     {pos: [-.62, 1.9, -1.55], look: [-.05, .85, -.15], push: .1, fov: 50},
};
export const DIR = {
  c1:  {dev: ["exhausted", "type"], codex: ["watch", "idle"], flicker: true},
  c2:  {dev: ["exhausted", "rest"], codex: ["eager", "bounce"]},
  c3:  {dev: ["deadpan", "rest"], codex: ["eager", "idle"]},
  c4:  {dev: ["deadpan", "rest"], codex: ["eager", "nod"]},
  c5:  {dev: ["deadpan", "rest"], codex: ["eager", "idle"]},
  c6:  {dev: ["deadpan", "rest"], codex: ["proud", "bounce"]},
  c7:  {dev: ["irritated", "pointscreen"], codex: ["eager", "idle"]},
  c8:  {dev: ["irritated", "rest"], codex: ["watch", "idle"]},
  c9:  {dev: ["irritated", "rest"], codex: ["watch", "idle"]},
  c10: {dev: ["stunned", "rest"], codex: ["oops", "idle"]},
  c11: {dev: ["stunned", "rest"], codex: ["neutral", "glitch"]},
  c12: {dev: ["stunned", "rest"], codex: ["eager", "wave"], cuts: [[0, "codex"], [.75, "devclose"]]},
  c13: {dev: ["panic2", "hair"], codex: ["eager", "idle"]},
  c14: {dev: ["calm", "type"], codex: ["eager", "idle"]},
  c15: {dev: ["calm", "rest"], codex: ["eager", "spin"]},
  c16: {dev: ["calm", "rest"], codex: ["neutral", "stuck"]},
  c17: {dev: ["panic2", "rest"], codex: ["neutral", "stuck"]},
  c18: {dev: ["panic2", "rest"], codex: ["warm", "off"]},
  c19: {dev: ["pleading", "rest"], codex: ["neutral", "gone"]},
  c20: {dev: ["pleading", "rest"], claude: ["eager", "cheer"], codex: ["neutral", "gone"], cuts: [[0, "claudepop"], [.85, "devclose"]]},
  c21: {dev: ["deadpan", "rest"], claude: ["eager", "idle"], codex: ["neutral", "gone"]},
};
// the last (silent) beat: Dev slowly lowers his head onto the desk (folds at the hips)
export function extra(t, {cur, devBody, devHead}) {
  if (cur.id !== "c21") return;
  const k = Math.min(1, Math.max(0, (t - cur.start - .5) / 1.1)), e = k * k * (3 - 2 * k), th = 1.0 * e;
  devBody.rotation.x += th; devBody.position.y += .55 - .55 * Math.cos(th); devBody.position.z -= .55 * Math.sin(th) + .08 * e;
  devHead.rotation.x += .25 * e;
}
