# helper 7 status (Ep 2 sound)

Updated 2 Nov 2026.

**Mix:** `out/monsters/ep02/mix.wav`, built by `channels/monsters/ep02_sound.py` from the cached ep02 takes (e6a1dbb's
tar, with l2 re-voiced; it refuses to synthesise). 57.325 s, 48 kHz stereo, **-13.99 LUFS, -1.34 dBTP**, no metadata.

**Whisper medium.en, per line on the mix: 19/19 as written**, including l2 "The bird struck first." (heard exactly).
- The dive whoosh still starts after "first" ends, and the 6 dB dip under l2 stays; both are harmless now.
- The 1-frame cut moves (S02 32, S03 from f98, S08 from f413, S09 from f473, S12 63, S18 75, S20 from f1231) need no
  constant changes: every picture beat is a frame offset inside its shot, added to that shot's start from timing.json,
  so the hits move with the cuts (e.g. the SNAP is S09 f33 = cut frame 506).

**Picture beats** (0-based frames in the cut, read from the final shots on 2 Nov; constants at the top of ep02_sound.py):

| Shot | Beat (frame) | Sound |
|---|---|---|
| S01 | head-on dive, in the gap after "it." | a low shadow whoosh (between sentences) |
| S02 | after "first" ends, into the cut to S03 | the dive whoosh, peaking across the cut |
| S03 | knees down f8, scoop splash f27, bird's shadow f44 | knee slide, splash, shadow whoosh |
| S04 | talons cross the arm f11, bird climbs away f16 | talon swipe + sleeve tear, two wing beats |
| S09 | wind-up cut f14, impact frames f33-35, ring f36 | claw cock + hush f14-33, THE SNAP f33, shockwave f36 |
| S10 | bird already in the thorns on the cut, f0 | thorn crash, dazed tweets and stars |
| S11 | drop f18, puffball f43, huff f70, stomp-off f74-104 | plop, the "poomf", huff, five stomps |
| S12 | the claw comes up f14 | a low creak; the tense second held |
| S13 | the claw touches his nose f15 | the "tink" (the tense bed stops on it) |
| S17 | Wren marches in from f0, stops ~f45 | her steps every 0.36 s, her hand bell on the stop |
| S20 | both halves open on the cut f0 (S20top + S20bot) | the split whoosh |
| S20bot | Wren turns her back f55-65, bell at her hip f61 | cloth swish (right), a small bell ring |
| S20bot | Kai's hands to collar f81, shrimp slips in f89, teal bulge pops f97 ("shirt") | two cloth rustles (left), a soft rubbery "bloop" |
| S20bot | Wren glances back f115-121, turns away again f139-145 | swish + a faint bell jingle, swish |

**S20bot landed (8a9a5d4) and is now scored** (beats read by frame diffs on its two halves and a contact sheet).
Still placeholders, because those shots haven't landed: S05 drip (f40), S14 glow chime (on "glow"), S15 sky-crack sting
(on "crack"), S19 lake and the drip on "dry" (helper 1's raw S19 f001-062 part is in, but not the final shot). The A/B stingers sit on the spoken letters.
S16's bells sit on "bells" (40.28 s), which is right for helper 1's S16 (the villagers come over the hill from the cut).

The music drops 0.1 s before S09 (TWIST l9). No heartbeat, no riser, all original.

Status: done on the shots that have landed. Waiting for S05/S14/S15/S19 (and the re-rendered S02/S04, which keep their beats unless the action moves); I'll re-run, re-check and push when they land.
