# Interestingly Strange: standing rules

## Workflow: script first, owner approves, then render (protects monetization)
- For every new video, first send the owner the script: each narration line, a one-line note of what's on screen,
  the title and the sources. **Don't render until the owner approves it** or sends changes.
- The owner adds or changes lines as they like; keep their words. If one of their lines would be misheard by the
  voice, say so and suggest a fix rather than changing it silently.
- The owner's own ideas, opinions and edits are what make each video original (YouTube's "inauthentic content" rule
  targets mass-produced, templated videos), so ask for them and vary formats, scenes and characters.
- Post **2 videos a day** (9:30 PM and 4:30 AM IST until Oct 31), not 3.

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
- Narrator: Kokoro `am_fenrir` (the default). The owner switched back from their cloned voice on 5 Oct 2026 because
  more viewers swiped away on the cloned-voice videos. Use the clone (`NARRATOR_ENGINE=clone`) only if the owner asks.

## Hooks: people must stay, not swipe (owner, 11 Oct 2026)
- From our own analytics (Sep 29–Oct 11): the openings that kept 75–78% drop the viewer into a scene they can picture in
  one second with something already wrong or tense ("A kid in the last row raises his hand…", "A teacher finds a pack
  of cigarettes in the classroom trash can", "a hotel with infinite rooms, and every single one is full"). The weakest
  open on a statement about a topic, "Meet X", a quiz setup or a bare philosophy question (Ship of Theseus 52%, Monty
  Hall 43%, Mystery Kid 36%).
- Line 1 = a character in a scene, mid-action, or an image with a contradiction built in. Put a big question in a
  character's mouth instead of asking the viewer cold. Never open with "Meet…", "This X has…" or a series name.
- Frame 0 is already moving and shows the hook as big on-screen text: no fade-in, no empty establishing shot.
- Open a loop in the first 5 seconds that only the ending closes ("but the teacher just smiles").
- Don't trust `hookscore.py` for this channel (it scores our best openings WEAK); judge hooks against these rules.

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
- Fast pacing, no dead air, a visual change about every second, disputed claims left out.
- Research is light (owner, 9 Oct 2026): write from your own knowledge and creativity, and look things up only when a
  claim is surprising, very specific (exact quotes, dates, numbers) or you're unsure. Original clever stories with a
  twist (no research needed) are welcome alongside real ones; don't present invented stories as true history.
- Any topic is open, including controversial ones (religion, money, power): the owner wants to explore freely.
  Keep it honest: quote people's real, sourced words (say "often credited to" when the source is unknown) and
  never phrase anything as a call to violence.
- Each video ships with an upload sheet: title, alternative titles, description, hashtags, tags, pinned comment.
- Upload reminders always come with the files (owner, 13 Oct 2026): build the pack with
  `python tools/make_pack.py out/packs FIRST LAST` and send every due video plus its upload sheet in the same reply.
- No metadata or encoder tags in outputs; never strip other parties' provenance watermarks (e.g. SynthID).
- Riddle series is called **The Last Bencher** (not "Last Row Kid").
- The doctor channel ("Body Facts") is a separate channel with its own chat and branch (`ccr-56282fe5-evehq4-doctor`). Don't make doctor videos on this branch.
- The global news & tech channel is also separate, with its own chat and branch (`ccr-56282fe5-evehq4-news`). Don't make news videos on this branch.
