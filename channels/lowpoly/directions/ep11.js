// Episode 11, "My Dad Found My AI at 3 AM" (ep11_dad.py). Dad in Dev's chair, Dev beside him, Claude; warm room.
import {EMO as E, POSES as P, BODY as B, SHOTS as S} from "./base.js";
export const CAST = {codex: false, claude: [0, -.05], dev: [.64, -.86], devTurn: -.55,
  guest: {name: "dad", skin: 0xd9a386, cloth: 0x7a5a3a, hair: 0xbdbdbd, hoodie: false, bald: true, moustache: true, pos: [0, -.95]}};
export const DETAILS = true, SMOOTH = true;
export const EMO = E, POSES = P, BODY = B;
export const SHOTS = {...S,
  two:      {pos: [1.25, 1.42, -.15], look: [.25, 1.12, -.95], push: .08, fov: 50},            // from the right: Dev near, Dad far
  dad:      {pos: [-.72, 1.32, -.12], look: [0, 1.25, -.95], push: .08, fov: 44, track: "dad"},
  dadclose: {pos: [-.46, 1.3, -.4], look: [0, 1.26, -.95], push: .08, fov: 40, track: "dad"},
  devside:  {pos: [.1, 1.32, -.1], look: [.64, 1.25, -.86], push: .08, fov: 44, track: "dev"},
  devside2: {pos: [.25, 1.3, -.35], look: [.64, 1.26, -.86], push: .08, fov: 40, track: "dev"},
  highwide: {pos: [.4, 2.0, -1.7], look: [.1, .9, -.2], push: .1, fov: 52},
};
export const DIR = {
  m1:  {dev: ["stunned", "doubletake"], dad: ["smallsmile", "type"], claude: ["soft", "idle"], cuts: [[0, "two"], [.6, "devside"]]},
  m2:  {dev: ["stunned", "rest"], dad: ["smallsmile", "type"], claude: ["soft", "idle"]},
  m3:  {dev: ["deadpan", "rest"], dad: ["smallsmile", "type"], claude: ["soft", "idle"]},
  m4:  {dev: ["deadpan", "rest"], dad: ["warm", "rest"], claude: ["soft", "nubup"], punch: .06},
  m5:  {dev: ["squint", "rest"], dad: ["warm", "rest"], claude: ["soft", "idle"]},
  m6:  {dev: ["squint", "rest"], dad: ["proud", "shrug"], claude: ["warm", "idle"], punch: .08},
  m7:  {dev: ["deadpan", "rest"], dad: ["warm", "rest"], claude: ["warm", "nubup"]},
  m8:  {dev: ["deadpan", "rest"], dad: ["warm", "nod"], claude: ["warm", "idle"]},
  m9:  {dev: ["irritated", "rest"], dad: ["smallsmile", "rest"], claude: ["watch", "idle"], cuts: [[0, "devside2"], [.7, "claude"]]},
  m10: {dev: ["stunned", "flinch"], dad: ["smallsmile", "rest"], claude: ["polite", "idle"], punch: true},
  m11: {dev: ["deadpan", "rest"], dad: ["proud", "type"], claude: ["warm", "idle"]},
  m12: {dev: ["deadpan", "rest"], dad: ["warm", "rest"], claude: ["soft", "idle"]},
  m13: {dev: ["soft", "rest"], dad: ["soft", "rest"], claude: ["soft", "idle"]},
  m14: {dev: ["smallsmile", "sitback"], dad: ["smallsmile", "rest"], claude: ["soft", "idle"], cuts: [[0, "devside2"], [.5, "highwide"]]},
  m15: {dev: ["smallsmile", "rest"], dad: ["warm", "rest"], claude: ["soft", "idle"]},
  m16: {dev: ["smallsmile", "rest"], dad: ["proud", "nubup"], claude: ["warm", "idle"]},
  m17: {dev: ["hopeful", "rest"], dad: ["smallsmile", "rest"], claude: ["watch", "idle"]},
  m18: {dev: ["hopeful", "rest"], dad: ["smallsmile", "rest"], claude: ["soft", "nubup"]},
  m19: {dev: ["stunned", "doubletake"], dad: ["warm", "nod"], claude: ["warm", "idle"], cuts: [[0, "dadclose"], [.55, "devside2"]], punch: .1},
};
