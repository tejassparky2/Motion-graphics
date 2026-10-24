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

## Look (from the owner's three references)
- Ref 1: one big word per beat, key words red, dark teal/navy flat-anime close-ups cut on the beat, grain, CA edges.
- Ref 2: thin white or red line-art on black or a full-red flood; the line builds up word by word in mixed fonts
  (small italic words, big bold key words, one accent colour).
- Ref 3: glowing words, a dip to black as a new line lands, soft confessional vocal.

## Lyric lessons from the references (patterns only, never their lines)
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
- Short-friendly: 15-30 s of the song must stand alone and end on its strongest line or loop into the hook.
