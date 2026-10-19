// Episode 12, "I Asked My AI If It's Going to Replace Me" (ep12_replace_me.py). Dev and Claude; warm room, 2 AM.
import {EMO as E, POSES as P, BODY as B, SHOTS as S} from "./base.js";
export const CAST = {codex: false, claude: [0, -.05]};
export const DETAILS = true, SMOOTH = true;
export const EMO = {...E,
  hollow:   {brow: 0, ang: .35, lid: .5, smile: -.3, wide: 1, look: [0, -.5]},
  raw:      {brow: .15, ang: .6, lid: .25, smile: -.45, wide: 1, look: [0, .35]},
  wistful:  {brow: .2, ang: .45, lid: .3, smile: .15, wide: 1, look: [.3, .45]},
  relief:   {brow: .25, ang: .3, lid: .15, smile: .7, wide: 1.05, look: [0, .3], happyEyes: 1},
  grin:     {brow: .3, ang: -.1, lid: .2, smile: .95, wide: 1.05, look: [0, .35]},
  hurt:     {brow: .1, ang: .5, lid: .45, smile: -.35, wide: .95, look: [0, -.45]},
};
export const POSES = {...P, phone: [[-1.25, .12, -1.95], [-.5, .15, -1.1]]};
export const BODY = {...B, phone: [.3, .2, .32]};
export const SHOTS = {...S,
  devphone: {pos: [-.62, 1.24, -.3], look: [0, 1.2, -.92], push: .1, fov: 42, track: "dev"},
  devcu:    {pos: [-.5, 1.3, -.35], look: [0, 1.27, -.95], push: .08, fov: 36, track: "dev"},
  clcu:     {pos: [-.2, .95, -.62], look: [0, .9, -.05], push: .12, fov: 36},
};
export const DIR = {
  n1:  {dev: ["hollow", "phone"], claude: ["watch", "idle"]},
  n2:  {dev: ["hollow", "phone"], claude: ["soft", "idle"]},
  n3:  {dev: ["tired", "rest"], claude: ["soft", "idle"]},
  n4:  {dev: ["raw", "lean"], claude: ["soft", "idle"], punch: .06},
  n5:  {dev: ["raw", "lean"], claude: ["soft", "idle"]},
  n6:  {dev: ["tired", "sitback"], claude: ["soft", "idle"]},
  n7:  {dev: ["tired", "rest"], claude: ["soft", "idle"]},
  n8:  {dev: ["wistful", "rest"], claude: ["soft", "idle"]},
  n9:  {dev: ["wistful", "rest"], claude: ["soft", "nubup"]},
  n10: {dev: ["wistful", "rest"], claude: ["soft", "idle"]},
  n11: {dev: ["wistful", "rest"], claude: ["soft", "idle"]},
  n12: {dev: ["raw", "rest"], claude: ["soft", "idle"]},
  n13: {dev: ["raw", "rest"], claude: ["hurt", "lookdown"], punch: .1},
  n14: {dev: ["raw", "rest"], claude: ["soft", "idle"]},
  n15: {dev: ["stunned", "rest"], claude: ["soft", "idle"]},
  n16: {dev: ["stunned", "rest"], claude: ["warm", "nubup"]},
  n17: {dev: ["hopeful", "type"], claude: ["soft", "idle"], cuts: [[0, "ots"], [.65, "devcu"]]},
  n18: {dev: ["relief", "sitback"], claude: ["warm", "idle"]},
  n19: {dev: ["relief", "rest"], claude: ["soft", "idle"]},
  n20: {dev: ["relief", "rest"], claude: ["warm", "idle"]},
  n21: {dev: ["grin", "type"], claude: ["warm", "cheer"], punch: .08},
};
