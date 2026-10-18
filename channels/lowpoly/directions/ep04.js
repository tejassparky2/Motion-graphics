// Episode 4, "I Told Claude I'm Not a Real Developer" (ep04_commits.py). Dev and Claude only; warm, quiet.
import {EMO as E, POSES as P, BODY as B, SHOTS as S} from "./base.js";
export const CAST = {codex: false, claude: [0, -.05]};
export const DETAILS = true, SMOOTH = true;                          // warm low-key room (no night window)
export const EMO = E, POSES = P, BODY = B, SHOTS = S;
export const DIR = {
  e1:  {dev: ["sad", "rest"], claude: ["watch", "idle"], flicker: true},
  e2:  {dev: ["sad", "rest"], claude: ["soft", "idle"]},
  e3:  {dev: ["sad", "sink"], claude: ["soft", "idle"]},
  e4:  {dev: ["sad", "sink"], claude: ["soft", "nubup"]},
  e5:  {dev: ["sad", "sink"], claude: ["soft", "idle"]},
  e6:  {dev: ["tired", "rest"], claude: ["soft", "idle"]},
  e7:  {dev: ["tired", "rest"], claude: ["warm", "idle"]},
  e8:  {dev: ["tired", "rest"], claude: ["soft", "nubup"]},
  e9:  {dev: ["sad", "rest"], claude: ["soft", "idle"]},
  e10: {dev: ["sad", "rest"], claude: ["warm", "idle"]},
  e11: {dev: ["smallsmile", "rest"], claude: ["warm", "idle"]},
  e12: {dev: ["hopeful", "rest"], claude: ["soft", "idle"]},
  e13: {dev: ["hopeful", "rest"], claude: ["soft", "idle"]},
  e14: {dev: ["smallsmile", "rest"], claude: ["warm", "idle"]},
  e15: {dev: ["smallsmile", "type"], claude: ["eager", "idle"]},
  e16: {dev: ["smallsmile", "rest"], claude: ["warm", "cheer"]},
};
