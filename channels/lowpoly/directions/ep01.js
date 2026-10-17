// Episode 1, "I Asked AI to Review My Coworker's Code" (ep01_code_review.py). Per line: [emotion, pose].
export const LAPTOP = {x: .01, z0: -.42, z1: -.22, slideIn: true};   // Dev slides the laptop over in line 1
export const DIR = {
  e1:  {dev: ["casual", "slide"], claude: ["eager", "idle"], codex: ["eager", "idle"]},
  e2:  {dev: ["casual", "rest"], claude: ["eager", "salute"], codex: ["watch", "idle"]},
  e3:  {dev: ["casual", "rest"], claude: ["shocked", "freeze"], codex: ["reading", "lookdown"]},
  e4:  {dev: ["casual", "rest"], claude: ["shocked", "freeze"], codex: ["horrified", "backoff"]},
  e5:  {dev: ["casual", "rest"], claude: ["reading", "lookdown"], codex: ["horrified", "backoff"]},
  e6:  {dev: ["casual", "rest"], claude: ["horrified", "freeze"], codex: ["reading", "lookdown"]},
  e7:  {dev: ["casual", "sip"], claude: ["horrified", "idle"], codex: ["watch", "idle"]},
  e8:  {dev: ["casual", "sip"], claude: ["horrified", "nubup"], codex: ["horrified", "idle"]},
  e9:  {dev: ["ashamed", "rest"], claude: ["horrified", "freeze"], codex: ["horrified", "bounce"], flash: true},
  e10: {dev: ["ashamed", "sink"], claude: ["watch", "idle"], codex: ["watch", "idle"]},
  e11: {dev: ["ashamed", "sink"], claude: ["eager", "nubup"], codex: ["watch", "idle"]},
  e12: {dev: ["panic", "lunge"], claude: ["oops", "freeze"], codex: ["eager", "idle"]},
  e13: {dev: ["panic", "lunge"], claude: ["oops", "idle"], codex: ["proud", "bounce"]},
  e14: {dev: ["panic", "rest"], claude: ["suspicious", "idle"], codex: ["watch", "idle"]},
  e15: {dev: ["ashamed", "hood"], claude: ["suspicious", "idle"], codex: ["watch", "idle"]},
  e16: {dev: ["ashamed", "hood"], claude: ["warm", "nubup"], codex: ["eager", "idle"]},
  e17: {dev: ["ashamed", "hood"], claude: ["warm", "cheer"], codex: ["eager", "bounce"]},
  e18: {dev: ["ashamed", "hood"], claude: ["warm", "idle"], codex: ["proud", "bonk"]},
};
