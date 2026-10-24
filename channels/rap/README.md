# Rap music video channel

Original songs: Claude writes the lyrics and a music-app prompt, the owner generates the audio (Gemini or another
app; its SynthID watermark stays in), Claude makes the lyric video. Never imitate a real artist's voice, name or
lyrics; never use the owner's cloned voice. Songs and renders stay out of the repo (out/rap/ is git-ignored).

## Making a video
1. Whisper word timings for the whole song (faster-whisper medium; pass the audio as a numpy array, the installed
   PyAV rejects file paths): `python channels/rap/words.py SONG.wav WORDS.json LYRICS.txt`.
2. Measure the beat grid (BPM, first-beat PHASE) and write a song module like `still_breathing.py`
   (cut start/length in beats, lyric lines with marks, shots per line).
3. `python channels/rap/lyricvid.py still_breathing SONG.wav WORDS.json out/rap/NAME.mp4 [--preview 8]`
   Lyrics are the real text aligned to Whisper's timings, so captions never show Whisper's typos.

## What each reference is for (owner, 24 Oct 2026)
- **Reference 1 = visuals AND lyrics**: one big word per beat, key words red, dark teal/navy flat-anime close-ups
  cut on the beat, grain, chromatic edges; emotional "struggling but keep going" rap.
- **References 2 and 3 = lyrics and voice ONLY, never visuals** ("2nd and 3rd for wonderful lyrics and voice").
  (Still Breathing v1 borrowed red line-art frames and dips to black from them before this was said; the owner is
  watching it first, so it stays as is until they decide.)

## Voice (measured from refs 2 and 3, 24 Oct 2026)
- Both are **sung**, not rapped: about 86-90% of the voiced time is on held, steady notes; ours (Still Breathing)
  is 74%.
- **Slow**: 1.5-3 words a second (Still Breathing raps about 4-5), with a very slow first line (ref 3 opens at
  1.5 w/s) and real pauses between phrases.
- Ref 2: lighter, higher voice (median pitch ~190 Hz), almost bare backing (a 57x loudness range: near-silence,
  then the voice), slow ~60 BPM feel, intimate, like a story told quietly.
- Ref 3: low male baritone (~120 Hz), soft and tired-sounding, steady half-time beat (~65 BPM), melody on
  every line.
- Music-app prompt words for this: "soft, intimate, half-sung melodic vocal, close-mic, breathy, slow 60-70 BPM
  half-time, sparse piano / soft guitar, lots of space, gentle reverb". Never name a real artist.

## Lyric lessons from refs 2 and 3 (patterns only, never their lines)
- **Confess, don't announce.** The strongest lines are plain talk to one person: "I'm not X, I'm just Y" turns
  (denial, then the real feeling) hit harder than slogans.
- **Specific, small images.** A combed hair, a suit and tie, a name you still say: concrete details carry the emotion.
- **Twist the expectation.** Set up a cliché ("you think the devil has horns") and break it ("so did I, but I was
  wrong"): the line people quote is the reversal.
- **One impossible wish.** "If I could ..., I wouldn't ask for A or B, I'd just ..." builds a list and lands on a
  humble, personal ask.
- **Build the line in pieces.** Short phrases that stack word by word on screen ("He's / nice, / polite").
- **Address someone** (you / she / him): a story between two people beats a speech to the world.
- **Sung, soft hook + spoken verses**: a gentle, melodic voice on the emotional lines; keep the hook singable.
- **One vowel-sound rhyme chain** through a whole section instead of couplets: ref 2 runs the long "I"
  (tie / polite / surprise / bright / eye), ref 3 the long "A" (fame / became / name).
- **Repeat with a flip**: say a phrase, then repeat it with its meaning turned ("tired" ... "pretending I'm not
  tired").
- **Open on a quote or a confession**, not a scene description: "She said ..." / "I'm not ..., I'm just ...".
- **End on the smallest, most personal detail**: the last line is a tiny habit or object, not a big statement.
- Short-friendly: 15-30 s of the song must stand alone and end on its strongest line or loop into the hook.
