# helper 7 status (Ep 2 sound)

Updated 2 Nov 2026.

**Mix:** `out/monsters/ep02/mix.wav`, built by `channels/monsters/ep02_sound.py` from the cached ep02 takes (it refuses to
synthesise). 57.343 s, 48 kHz stereo, **-14.02 LUFS, -1.35 dBTP**, no metadata.

**Whisper medium.en, per line on the mix:** 18/19 as written. **l2 "The bird dived first." is heard "The bird died first."**
- Done as asked: the dive whoosh now starts after "first" ends (+0.03 s), and everything under l2 (music, effects,
  ambience) is another 6 dB down, with the 10 dB duck on top. Still "died".
- I tested it further:
  - On the dry voice stem alone, the check window (line -0.15 s to +0.25 s) gives "dived". A 2 s window (2.6-4.6 s)
    gives "died" on the voice alone.
  - With the music, or the effects, or both added back at any level down to -26 dB, it reads "died" even in the tight
    window.
  - So the /v/ in this take is too weak to survive any bed. **Please re-voice l2** (or reword it, e.g. "The bird dove
    first." / "The bird struck first.", owner's call). After a re-voice the mix picks up the new take on the next run,
    as long as the timing doesn't change.

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

Still placeholders, because those shots haven't landed: S05 drip (f40), S14 glow chime (on "glow"), S15 sky-crack sting
(on "crack"), S19 lake and the drip on "dry", and S20 split whoosh (f0). The A/B stingers sit on the spoken letters.
S16's bells sit on "bells" (40.28 s), which is right for helper 1's S16 (the villagers come over the hill from the cut).

The music drops 0.1 s before S09 (TWIST l9). No heartbeat, no riser, all original.

Status: waiting for the l2 re-voice and the S05/S14/S15/S19/S20 shots; I'll re-run and re-check when they land.
