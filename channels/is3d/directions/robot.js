// "A Robot With 1 Rule" (robot_butler.py). Bedroom (around x=0) and classroom (around x=20).
// Per line: kid [emotion, pose], bolt [screen, pose], teacher [emotion, pose]; `cuts` switch shots inside a line
// ([fraction of the line, shot]); bolt's place follows the shot's set unless the line says otherwise.
export const SHOTS = {
  bed_wide:      {pos: [1.55, 1.3, 1.25], look: [.5, .82, -.55], push: .1, fov: 44, set: "bed"},   // medium shot: faces big from frame 0 (research F2)
  bed_side:      {pos: [-1.0, 1.25, 1.25], look: [.4, .82, -.5], push: .1, fov: 48, set: "bed"},
  kid_close:     {pos: [.6, 1.1, .38], look: [0, .98, -.72], push: .08, fov: 42, set: "bed", track: "kid"},
  bolt_close:    {pos: [.22, 1.02, -.12], look: [.95, .98, -.45], push: .08, fov: 50, set: "bed", track: "bolt"},
  bed_night:     {pos: [1.9, 1.42, 1.85], look: [.48, .8, -.5], push: .1, fov: 46, set: "bed"},
  class_wide:    {pos: [19.6, 1.7, -2.65], look: [20.6, .85, 1.0], push: .12, fov: 52, set: "class"},
  teacher_close: {pos: [20.7, 1.4, -.85], look: [20.3, 1.38, -2.5], push: .08, fov: 42, set: "class", track: "teacher"},
  bolt_class:    {pos: [20.7, 1.15, .2], look: [21.3, .82, 1.52], push: .1, fov: 42, set: "class", track: "bolt"},
};
export const DIR = {
  r1:  {kid: ["sleep", "sleep"], bolt: ["eye", "idle"], alarm: true},
  r2:  {kid: ["smug", "smug"], bolt: ["eye", "idle"]},
  r3:  {kid: ["smug", "smug"], bolt: ["load", "freeze"]},
  r4:  {kid: ["smug", "smug"], bolt: ["load", "freeze"]},
  r5:  {kid: ["smug", "smug"], bolt: ["load", "freeze"]},
  r6:  {kid: ["smug", "smug"], bolt: ["load", "strain"]},
  r7:  {kid: ["neutral", "rest"], bolt: ["load", "idle"], bulbAt: .5},
  r8:  {bolt: ["eye", "walk"], teacher: ["neutral", "point"], turn: true},
  r9:  {bolt: ["eye", "sit"], teacher: ["shocked", "chalk"], turn: true},
  r10: {bolt: ["happy", "raise"], teacher: ["shocked", "chalk"], turn: true},
  r11: {bolt: ["happy", "raise"], teacher: ["amazed", "rest"], kid: ["shocked", "shock"], cuts: [[0, "class_wide"], [.5, "bed_night"]],
        answers: true, notesAt: .5},
  r12: {kid: ["sad", "sad"], bolt: ["happy", "proud"]},
  r13: {kid: ["sad", "sad"], bolt: ["eye", "proud"]},
};
