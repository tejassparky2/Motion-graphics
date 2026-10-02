# Interestingly Strange: standing rules

## Narration must sound like a person telling the story (every video, not only riddles)
- **Never let sentences run together.** Every sentence ends with a full stop (or ? / !) in the script, and the
  pipeline voices each sentence as its own take with a real full-stop pause between them
  (`motion/timeline.py`: `SENTENCE_TAKES`, `STOP_PAUSE`, `QUESTION_PAUSE`, `BEAT_GAP`). Don't turn this off.
- Use full stops generously in scripts. Short punchy sentences ("Nope." "Twice.") must be their own sentences.
- A line that switches from narrator to a character uses `speaker_from`, so there's a pause at the hand-over.
- Riddles, quiz questions and answers are read slower with clear turns: call `clear_dialogue(SCRIPT, ...)`.
- After every render, check every line with Whisper **medium** (not just the small model in verify.py). Any line
  where words merge or get misheard ("No. Your age" heard as "Know your age") gets reworded and re-rendered.
- Pause lengths come from the reference videos the owner supplied (`out/voice_rhythm.md`).

## Channel basics
- 2D hand-drawn Shorts: weird animals and insects, weird history, paradoxes, clever or funny twist stories.
- Fast pacing, no dead air, a visual change about every second, facts checked (disputed claims left out).
- Each video ships with an upload sheet: title, alternative titles, description, hashtags, tags, pinned comment.
- No metadata or encoder tags in outputs; never strip other parties' provenance watermarks (e.g. SynthID).
- Riddle series is called **The Last Bencher** (not "Last Row Kid").
