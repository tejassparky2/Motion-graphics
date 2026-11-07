# helper 7 status (Ep 3 sound)

Updated 7 Nov 2026.

**Started:** `channels/monsters/ep03_sound.py` (ep02_sound.py's way: ep01v2_sound.py with EPISODE = "ep03"; the cached
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
- S14 THE FLIP (TWIST l14): the music drops 0.1 s before the shot; a held hush (only the mark's hum), then the swarm
  rolls over (a soft whoosh), ~18 soft comic plops, tiny dazed trills into S15;
- S15-S16: a soft comic pad; Wren's last bell clink after "bell";
- S17-S18: a tender pad; **l18 whispered, quieter and closer** (4.5 dB down, presence and air up, a breath under the
  words, and the whole world 5 dB further back under the line); the lake lapping from S18 to the end; the lighthouse
  glow chime on "lighthouse";
- S19: the split whoosh, the A/B stingers on the letters, the "Comment" blip; the sting bed from the first "Option".

**Waiting for:** `channels/monsters/ep03/timing.json` and `assets/voice_cache/monsters_ep03_takes.tar`. Then I run it,
Whisper medium.en every line, push `out/monsters/ep03/mix.wav` and update this file.
