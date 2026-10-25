# Finding a voice like the reference reels (25 Oct 2026, owner: "find best and good voice as reference video")

Method: a speaker embedding (Resemblyzer) of the narrator, averaged over one minute of each of the owner's 9
reference reels (the same narrator in all 9: similarity 0.97-1.00 to the mean), compared with the same English test
passage read by every stock voice we can use. Plus pitch, brightness, pace and Whisper medium clarity. We match the
*type* of voice with stock synthetic voices; we never clone the creator's (a real person's) voice.

Reference narrator: closest to male voices (the top 8 matches are all male), median pitch ~165 Hz, warm/dark
(spectral centroid ~1200 Hz), calm storyteller pace.

| Rank | Voice | Similarity | Clarity (Whisper medium) | Pace |
|---|---|---|---|---|
| 1 | Turbo + Kokoro `hm_omega` timbre (Indian male) | 0.714 | 100% | 173 wpm |
| 2 | Kokoro `hm_omega` (Indian male, reading English) | 0.673 | 100% | 175 wpm |
| 3 | Turbo + `am_puck` timbre | 0.654 | 100% | 228 wpm |
| 4 | Turbo + `am_echo` timbre | 0.647 | 100% | 195 wpm |
| 5 | Kokoro `am_echo` / `am_puck` / `am_onyx` | 0.64-0.65 | 100% | 193-211 wpm |
| 31 | Turbo stock female (used for explainers 1-3) | 0.508 | | |

Audition video for the owner: `out/doc_voice_audition.mp4` (voices A-E, same passage).
To use the winner: `NARRATOR = dict(turbo=True, turbo_ref="hm_omega", rate=4.7, tempo_min=0.88)`.
