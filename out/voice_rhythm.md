# How our narrator should pause (measured)

Measured on the owner's 5 reference videos (narrator voice separated from the music with Hybrid Demucs, then
silences found from loudness) and on our own videos.

| Narration | Pauses per minute | Typical pause | Middle half of pauses |
|---|---|---|---|
| Reference: Class of Scammers | 9 | 0.09 s | 0.08–0.10 s |
| Reference: Video-75449 | 17 | 0.13 s | 0.11–0.17 s |
| Reference: Backbenchers | 4 | 0.11 s | 0.10–0.14 s |
| Reference: How the Rich Fool You, Secret of Wife | almost none (talks straight through) | | |
| **Ours: The Teacher Bluffed (owner says the sentences are good)** | 32 | 0.19 s | 0.13–0.22 s |
| Ours: Ship of Theseus (old) | 28 | 0.19 s | 0.14–0.21 s |

## What this means
- Human Shorts narrators **don't make long silences**. They mark the end of a sentence with their voice (the pitch drops),
  then go straight into the next one.
- "Joined sentences" happen when the voice reads two sentences as one: no drop at the full stop. So the fix is to make
  every sentence end properly, not to add long gaps.
- Teacher Bluffed works because its script is short, complete sentences, and the characters mostly get their own lines.

## Settings (motion/timeline.py)
- `SENTENCE_TAKES = True`: every sentence is voiced as its own take, so it always ends with a proper full stop.
- `STOP_PAUSE = 0.24 s` after a full stop, `QUESTION_PAUSE = 0.30 s` after a question, `BEAT_GAP = 0.24 s` between
  lines. That's Teacher Bluffed's rhythm (0.19 s typical) plus a little air for the sentence end.
- `turn_pause = 0.32 s` where the narrator hands over to a character inside one line.
- Riddle videos use `clear_dialogue()`: questions and answers at 90% speed, 0.42 s at each change of speaker.

## Writing rules
- One idea per sentence. Use full stops generously. Short punchy sentences ("Nope." "Twice.") stay on their own.
- Don't start a character's speech in the middle of a narrator sentence without `speaker_from`.
- After rendering, check every line with Whisper medium and reword anything it mishears.
