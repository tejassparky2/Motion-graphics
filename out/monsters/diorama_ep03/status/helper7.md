# helper 7 status (Ep 3 sound)

Updated 7 Nov 2026, after S14 FINAL landed (ef0558d).

## Coordinator
- **S14 render part 3 (f043-063): I can't take it.** This session has no Blender (not installed, and the disk
  allowance is nearly spent: ~2 GB free after I sparse-excluded other channels' outputs). Please reassign part 3.

## S13 retimed to bGqrs's final shot (pushed)
On S13's frames (1-based; bGqrs's beats): a cloth swish on the dip (f3); **the thud and grass swish as he lands flat
on f13**; the arm swept out over the grass (f17); the mark's bloom up through the grass on f26 ("below").
Mix still -14.00 LUFS, -1.34 dBTP; Whisper medium.en 18/18.

## S14 retimed to helper 10's landings (pushed)
The flip now follows `channels/monsters/diorama_ep03/S14_landings.json` (1-based S14 frames; S14 f1 = cut frame 772):
- f1-12: the held hush. The music has dropped, the night ambience is out, only the mark's hum (mix ~-45 dB RMS).
- f12: a soft whoosh as the wave of rolls starts; f14-40: the stall, a frantic wing flutter that dies away.
- **Hero plops on f32, f38, f44** (-12 dB, panned by each moth's screen x), then a softer plop on every other
  landing frame f47-66 (the patter, 25 moths). The night ambience comes back on f44.
- From f50: tiny dazed trills into S15/S16.

**Mix pushed:** `out/monsters/ep03/mix.wav` from the FINAL timing and takes (8274b7a): **54.090 s (1298 frames)**,
48 kHz stereo, **-14.00 LUFS, -1.34 dBTP**, LRA 3.9, no metadata. Built on word and shot-start timing; the picture
beats get retimed to the real frames as each shot lands.

**Whisper medium.en, per line on the mix: 18/18 as written** (l14 has no words). Two spelling-only differences are
counted as the same words: Whisper writes the name "Wren" as "Ren" (l16, l19) and "fluffmoths" as "fluff moths" (l6).
Everything else is word for word. l8 "Ring the bells! Bells will drive them off!" heard exactly.

**l18 whisper:** in the mix it sits 5.1 dB under Wren's l17 (-20.6 vs -15.5 dB RMS), with presence, air and a breath
under the words, and everything else 5 dB further back under the line.

**Code:** `channels/monsters/ep03_sound.py` (ep02_sound.py's way: ep01v2_sound.py with EPISODE = "ep03"; the cached
takes only, it refuses to synthesise; the 20/300 ms duck, two-pass loudnorm to -14 LUFS / -1 dBTP, Whisper medium.en
per line).

**Cue code written, on the word and shot timing** (to be retimed to the real frames as the shots land). All original,
synthesised, no heartbeat, no riser:
- the mark: a bloom on S01 f0, then a quiet warm hum under the whole episode; Wren's stumble (two scuffs + a knocked
  bell); villagers scattering;
- S02: the sky-crack eerie sting on "cracked" and a low rift hum from "sky";
- S03: villagers' steps backing off; doors and shutters banging shut (five, staggered L/R);
- S04: the dusk (birdsong thinning, crickets coming in), a soft chime as the sun goes down; S05 on: the night
  (crickets, low wind, a far frog);
- S06-S09: the swarm's soft fluffy wing flutter, growing; one close flutter on "fluffmoths"; the wing-dust glitter in
  S07; a scratch on "stings"; Wren's cape swish; every bell ringing from "Ring", still ringing until S10;
- S10-S13: the orbit whoosh swinging L-R-L (4 turns), the swarm at full; Kai drops into the grass on "put";
- S14 THE FLIP (TWIST l14): the music drops 0.1 s before the shot; then on helper 10's frames (above);
- S15-S16: a soft comic pad; Wren's last bell clink after "bell";
- S17-S18: a tender pad; **l18 whispered, quieter and closer** (4.5 dB down, presence and air up, a breath under the
  words, and the whole world 5 dB further back under the line); the lake lapping from S18 to the end; the lighthouse
  glow chime on "lighthouse";
- S19: the split whoosh, the A/B stingers on the letters, the "Comment" blip; the sting bed from the first "Option".

**Next:** as each shot lands in `out/monsters/diorama_ep03/shots/`, I read its beats (the flare, the stumble, the door
bangs, the scratch, the drop into the grass, the flip's first roll and plops, the clink, the lighthouse cut) and move
those cues onto its frames, re-run, Whisper and push. Shots in so far: S11, S12 (no cue beats of their own beyond the orbit whoosh), S13 (retimed), S14 (final, 84 frames: the landings file is unchanged, so the flip cues already sit on its frames; no re-mix needed).
