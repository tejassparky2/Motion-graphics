// Episode 1, "I Tried to Make Claude Disagree With Me" (ep01_absolutely_right.py). Dev and Claude only.
// Per line: [emotion, pose]; `cuts` switch shots inside a line ([fraction of the line, shot]).
export const CAST = {codex: false, claude: [0, -.05]};          // Claude alone, centred in front of the monitor
export const DETAILS = true;
export const MOOD = "night";                                     // reference 7: navy room, city window behind Dev                                     // the lived-in desk: keyboard, cans, duck, clock...
export const EMO = {
  irritated: {brow: -.2, ang: -.3, lid: .3, smile: -.35, wide: 1, look: [0, .35]},
  squint:    {brow: -.3, ang: -.15, lid: .6, smile: -.2, wide: 1, look: [.15, .3]},
  smug:      {brow: .15, ang: -.25, lid: .4, smile: .65, wide: 1, look: [0, .35]},
  deadpan:   {brow: -.05, ang: 0, lid: .5, smile: -.12, wide: 1, look: [0, .35]},
  pleading:  {brow: .4, ang: .55, lid: .05, smile: -.25, wide: 1.1, look: [0, .3]},
  stunned:   {brow: .55, ang: .2, lid: 0, smile: -.3, wide: 1.3, look: [0, .35]},
  hopeful2:  {brow: .3, ang: .45, lid: .1, smile: .2, wide: 1.05, look: [0, .35]},
  betrayed:  {brow: .15, ang: .6, lid: .35, smile: -.65, wide: 1, look: [0, .3]},
  strain:    {brow: -.35, ang: -.2, lid: .75, smile: -.4, wide: 1, look: [0, 0]},
  polite:    {brow: .25, ang: .3, lid: .1, smile: .45, wide: 1, look: [.5, .3]},
};
export const POSES = {
  pointscreen: [[-1.3, .12, -.25], [-.5, .15, -1.1]],
  leanin:      [[-.75, .1, -1.3], [-.75, .1, -1.3]],
};
export const BODY = {leanin: [1.4, 0, .05], type: [.7, 0, .12], squint: [1.2, 0, -.05]};
export const SHOTS = {
  claude:      {pos: [-.5, .98, -.72], look: [0, .88, -.05], push: .12, fov: 40},
  claudeclose: {pos: [-.24, .95, -.72], look: [0, .9, -.05], push: .14, fov: 38},
  claudecu:    {pos: [.36, .99, -.4], look: [0, .9, -.05], push: .08, fov: 44},
  ots:         {pos: [-.3, 1.45, -1.38], look: [0, .95, .1], push: .1, fov: 46},     // over Dev's shoulder
  devlean:     {pos: [-1.0, 1.32, -.32], look: [0, 1.0, -.36], push: .06, fov: 48},  // side: Dev's face in Claude's
  devside:     {pos: [-1.05, 1.15, -.45], look: [0, .92, -.4], push: .05, fov: 50},   // side: head hits the desk
  dev:         {pos: [-1.0, 1.28, .4], look: [.02, 1.12, -.88], push: .12, fov: 44, track: "dev"},
  devclose:    {pos: [-.75, 1.32, -.1], look: [0, 1.25, -.94], push: .08, fov: 44, track: "dev"},
  endside:     {pos: [-.62, 1.9, -1.55], look: [.05, .85, -.15], push: .1, fov: 50},   // high behind-left: Dev face-down, Claude beaming
};
export const DIR = {
  a1:  {dev: ["irritated", "pointscreen"], claude: ["watch", "idle"], cuts: [[0, "dev"], [.55, "ots"]]},
  a2:  {dev: ["irritated", "rest"], claude: ["eager", "salute"]},
  a3:  {dev: ["squint", "squint"], claude: ["eager", "idle"]},
  a4:  {dev: ["squint", "rest"], claude: ["eager", "nubup"]},
  a5:  {dev: ["smug", "squint"], claude: ["eager", "idle"]},
  a6:  {dev: ["smug", "squint"], claude: ["eager", "cheer"]},
  a7:  {dev: ["deadpan", "rest"], claude: ["eager", "idle"]},
  a8:  {dev: ["deadpan", "rest"], claude: ["eager", "nubup"]},
  a9:  {dev: ["pleading", "leanin"], claude: ["eager", "idle"], },
  a10: {dev: ["pleading", "leanin"], claude: ["strain", "strain"], },
  a11: {dev: ["stunned", "rest"], claude: ["eager", "salute"], cuts: [[0, "claude"], [.62, "devclose"]]},
  a12: {dev: ["hopeful2", "rest"], claude: ["watch", "idle"], cuts: [[0, "devclose"], [.5, "claudeclose"]]},
  a13: {dev: ["hopeful2", "rest"], claude: ["strain", "strain"]},
  a14: {dev: ["hopeful2", "rest"], claude: ["polite", "idle"]},
  a15: {dev: ["betrayed", "rest"], claude: ["polite", "idle"]},
  a16: {dev: ["betrayed", "rest"], claude: ["warm", "cheer"], cuts: [[0, "claude"], [1.0, "endside"]]},
};
// the last beat: after Claude's line Dev's head drops onto the desk
export function extra(t, {cur, devBody, devHead}) {
  if (cur.id !== "a16") return;
  const k = Math.min(1, Math.max(0, (t - cur.end - .25) / .3)), e = k * k, th = 1.0 * e;   // fold forward at the hips
  devBody.rotation.x += th; devBody.position.y += .55 - .55 * Math.cos(th); devBody.position.z -= .55 * Math.sin(th) + .08 * e;
  devHead.rotation.x += .25 * e + .03 * Math.sin(Math.max(0, t - cur.end - .55) * 30) * Math.exp(-Math.max(0, t - cur.end - .55) * 8);
}
