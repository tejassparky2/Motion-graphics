# Interestingly Strange: standing rules

**This branch is the doctor channel ("Doc and the Organs"; new videos carry its corner logo, old ones stay as released), separate from Interestingly Strange.** Read
`DOCTOR_CHANNEL.md` first: format, the finished kidney video, approved voices, setup and commands. Commit and push
doctor work to `ccr-56282fe5-evehq4-doctor` only. The rules below apply to both channels.

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

## Paradoxes must be explained so any viewer understands
- Clarity beats length: add a few seconds (45–50 s is fine) rather than skip a step.
- State the rule plainly first, then walk the logic one step per sentence, with no jumps ("we'd know it's Friday,
  so it's no surprise, so it can't be Friday").
- Every number the narrator uses must come from something already said (e.g. "one minute for every hundred cars"
  before "20 minutes").
- Show each step on screen as it's spoken: a card, a chart or a counter, kept above the caption line and fully in frame.
- Hook with the impossible-sounding claim, and end on a question that invites comments.

## Channel basics
- 2D hand-drawn Shorts: weird animals and insects, weird history, paradoxes, clever or funny twist stories.
- Fast pacing, no dead air, a visual change about every second, facts checked (disputed claims left out).
- Each video ships with an upload sheet: title, alternative titles, description, hashtags, tags, pinned comment.
- No metadata or encoder tags in outputs; never strip other parties' provenance watermarks (e.g. SynthID).
- Riddle series is called **The Last Bencher** (not "Last Row Kid").
