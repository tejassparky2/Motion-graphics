// Style test for episode 2 (ep02_style_test.py): the "That's Not My Dad" reference's camera language on our cast.
// Wide lens with barrel distortion, close and low or tilted angles, handheld shake, a cut inside most lines.
export const LOOK = {fisheye: .32, shake: 1, exposure: 1.1};
export const SHOTS = {
  devlow:  {pos: [.18, 1.0, -.3], look: [0, 1.24, -.92], push: .06, fov: 78, roll: -.12},   // up at Dev from the desk
  devback: {pos: [-.3, 1.42, -1.32], look: [0, .98, .3], push: .1, fov: 74, roll: .06},       // over his shoulder
  devturn: {pos: [-.4, 1.3, -.56], look: [0, 1.27, -.95], push: .05, fov: 70, roll: -.08},
  clxcu:   {pos: [-.06, .88, -.52], look: [-.18, .9, -.05], push: .06, fov: 70, roll: .1},    // Claude, lens almost touching
  cxcu:    {pos: [.32, 1.0, -.44], look: [.2, .99, -.02], push: .08, fov: 72, roll: -.14},
  topdown: {pos: [-.3, 2.1, -1.55], look: [0, .85, -.1], push: .1, fov: 68, roll: .12},      // high, from behind Dev
  clpush:  {pos: [-.2, .9, -.55], look: [-.18, .9, -.05], push: .22, fov: 58, roll: 0, shake: .4},
};
export const DIR = {
  t1: {dev: ["annoyed", "type"], claude: ["watch", "idle"], codex: ["watch", "idle"], flicker: true, cuts: [[0, "devlow"], [.5, "devback"]]},
  t2: {dev: ["tired", "rest"], claude: ["eager", "nubup"], codex: ["watch", "idle"], cuts: [[0, "clxcu"]]},
  t3: {dev: ["done", "turn"], claude: ["watch", "idle"], codex: ["watch", "idle"], cuts: [[0, "devback"], [.45, "devturn"]]},
  t4: {dev: ["tired", "rest"], claude: ["watch", "idle"], codex: ["eager", "bounce"], cuts: [[0, "cxcu"]]},
  t5: {dev: ["hopeful", "rest"], claude: ["shocked", "freeze"], codex: ["shocked", "idle"], cuts: [[0, "topdown"], [.5, "devlow"]]},
  t6: {dev: ["hopeful", "rest"], claude: ["shocked", "freeze"], codex: ["horrified", "backoff"], cuts: [[0, "clpush"]]},
};
