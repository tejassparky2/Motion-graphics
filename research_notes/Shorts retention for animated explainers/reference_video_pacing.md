# Measured pacing of the user's reference Short ("How the Rich fools you", 720x1280, 80.2 s, Hindi/Hinglish narration)

Method (run in this session, first-party measurement — not a web source):
- Speech: faster-whisper "small" model, word_timestamps=True, on the video's audio. Detected language: Hindi (p=0.99).
  Word counts from Whisper tokenisation of Hindi are approximate (±10%), so treat WPM as an estimate.
- Visual change: ffmpeg scene-score filter. Hard cuts = scene score > 0.25. "Visual change events" = frames at 10 fps with
  scene score > 0.03 (text pop-ins, character pose changes, camera moves), merged when closer than 0.35 s.

Results:
- 298 words over 0.0–80.1 s. Overall 223 wpm including the ending; 258–276 wpm in every 10-second window from 0–50 s,
  240 wpm at 50–60 s, 198 wpm at 60–70 s (talking-head outro). Speech effectively ends ~70 s.
- Pauses: median inter-word gap 0.0 s, 90th percentile gap 0.0 s. Only ONE gap ≥ 0.4 s in the whole video (1.38 s at 47.3 s).
  i.e. essentially continuous speech — no dead air.
- Visual change: 87 change events in 80 s → one visual change every ~0.92 s on average. Longest stretches with no visual
  change: 5.3, 3.8, 3.3, 3.2, 3.0 s; almost all others under 2.5 s.
- Hard cuts: 21, clustered (e.g. a burst of cuts around 30.3–30.8 s = a quick transition), otherwise cuts at ~1, 21, 29, 32.6,
  35.6, 38.3, 45.1, 49, 61.6, 67.2, 74.9 s. Most visual change comes from animation/text inside a held set, not from cuts.
- Structure observed from frames (1 fps contact sheets): opens on the creator on camera for ~1 s, then the animated story
  starts immediately with an on-screen handwritten premise line; handwritten numbers (prices, profit maths) pop on screen as
  they are said; a truck enters the frame repeatedly; a quick dim transition marks "next day"; the creator cuts back on camera
  mid-story (~30–40 s and ~60–80 s) to deliver commentary; the ending is the creator on camera.

Comparison — the current Pumpkin Trick render (v2, before this redesign):
- 82.1 s long, narration ~16 lines, Piper voice at natural pace; 16 gaps between lines, several 1.4–2.4 s long
  (e.g. 4.18→6.30 s, 13.82→15.70 s, 20.46→22.20 s, 29.98→32.00 s, 39.62→43.30 s (3.7 s), 55.32→59.50 s (4.2 s),
  73.45→75.80 s); speech covers ~70% of runtime. Estimated ~150–165 wpm while speaking.
