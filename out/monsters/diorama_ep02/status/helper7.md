# helper 7 status (Ep 2 sound)

Updated 2 Nov 2026.

**Mix:** `out/monsters/ep02/mix.wav`, built by `channels/monsters/ep02_sound.py` from the cached ep02 takes (78c1cad's
tar: l20 re-voiced "Option B: show her the glowing mark"; it refuses to synthesise). **57.461 s (1379 frames)**, 48 kHz
stereo, **-13.99 LUFS, -1.34 dBTP**, no metadata.

**Whisper medium.en, per line on the mix: 19/19 as written**, including l2 "The bird struck first." and the new l20
"Option A: hand it over. Option B: show her the glowing mark. Comment A or B." (both heard exactly).

**2 Nov, the new ending (78c1cad):** the old S20bot sounds (Wren's turn, the collar, the shirt bulge, the glance back) are
gone. The bottom half now gets the coordinator's cues: the glow chime on "glowing mark" (S20 f94) and Wren's startled
bell clank ~f105. Kai's wrist raise (~f82, on "show") is my placeholder until helper 4's new bottom half lands; the A/B
stingers and the "Comment" blip are word-anchored, so they follow the new timing.
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
| S05 | the drop leaves the claw tip f31; cut up to his terror face f49 | the drip plink; a tight sour "dink" as his eyes go wide |
| S09 | wind-up cut f14, impact frames f33-35, ring f36 | claw cock + hush f14-33, THE SNAP f33, shockwave f36 |
| S10 | bird already in the thorns on the cut, f0 | thorn crash, dazed tweets and stars |
| S11 | drop f18, puffball f43, huff f70, stomp-off f74-104 | plop, the "poomf", huff, five stomps |
| S12 | the claw comes up f14 | a low creak; the tense second held |
| S13 | the claw touches his nose f15 | the "tink" (the tense bed stops on it) |
| S17 | Wren marches in from f0, stops ~f45 | her steps every 0.36 s, her hand bell on the stop |
| S14 | the mark draws on and flickers from "wrist" ~f24, the burst f48 ("glow") | faint warm glints that speed up, the glow chime on the burst |
| S15 | the wrist mark's match cut: one glow frame f30, the sky crack from f31 | a glint on the glow frame, the eerie sting on the cut (0.15 s before "crack"), a low rift hum with a dry crackle under the sky |
| S19 | crane over the lake f0-47, cut to the dripping claw f48, drops every 8 frames, sparkle + big eyes on "dry" f89 | the lake bed; quiet plinks on the drop schedule from f54; a glint on f89; the louder drip after "dry" |
| S20 | both halves open on the cut f0 (S20top + S20bot) | the split whoosh |
| S20 bottom (B) | Kai raises his wrist on "show" ~f82; the mark flares on "glowing mark" f94-107; Wren starts back ~f105 | a sleeve swish and faint glints building, the glow chime on f94, a choked bell clank + a backward step f105 |

**S20bot landed (8a9a5d4) and is now scored** (beats read by frame diffs on its two halves and a contact sheet).
**S02 re-render (1cee315) checked:** the bird still dives through the whole shot with the speed lines building into
the cut, so the dive whoosh (after "first", peaking across the cut) still fits; the mix is unchanged.
**S04 re-render (fd9f12b) checked:** the talons reach the arm f11, the slash marks show f12-14 and the bird is out of
frame by ~f16, the same beats as before (the swipe starts f11, its fibre snaps land ~f13); the mix is unchanged.
**S15 landed (fb8f49f) and is now scored** on its match cut; re-mixed, -13.99 LUFS, Whisper 19/19.
**S14 landed (87a245a) and is now scored** (the chime moved 0.03 s onto the burst frame); re-mixed, -14.00 LUFS,
-1.35 dBTP, Whisper 19/19.
**S19 landed (6fe098d) and is now scored**; re-mixed, -14.00 LUFS, -1.35 dBTP, Whisper 19/19.
**S05 (helper 4, 0974629, in since 12:41; I had missed it) is now scored too:** the drip moved from the f40 placeholder to
f31, where the drop actually leaves the claw. **No placeholders left:** every shot is in and every picture beat is read
from the final shots. The A/B stingers sit on the spoken letters, by design.
S16's bells sit on "bells" (40.28 s), which is right for helper 1's S16 (the villagers come over the hill from the cut).

The music drops 0.1 s before S09 (TWIST l9). No heartbeat, no riser, all original.

Status: **done on the new ending** (mix pushed, 7a7455f). My git watch has run out, so **please send me a message when the new S20bot v2 final lands** and I'll set the raise, flare and clank on its real frames, re-run, Whisper and push. Until then the bottom-half hits sit on the word timing (raise ~f82, flare f94, clank f105).
