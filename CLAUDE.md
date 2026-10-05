# Global News & Tech channel: standing rules

This branch is the owner's **global news & tech** Shorts channel (working name, the owner picks the final one).
Read `NEWS_CHANNEL.md` first. The narration rules below come from the owner's first channel and apply here too.

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
  be## Channel basics (news & tech)
- Short explainers (about 40–60 s) on world news, countries, and tech news, for a global audience. Inspired by the
  format of Omar Agamy (@omaragamyy): one surprising fact or fresh development per video, explained fast and simply.
  Inspired by, never copied: no use of his name, face, voice, branding, catchphrases or clips.
- **Accuracy first.** Every claim needs at least two reliable sources (official statements, wire services such as
  Reuters/AP, the original study or filing). Put the sources in the description. Say the date ("as of October 2026")
  for anything that can change. Leave out rumours and anything you can't confirm.
- Neutral and fair: report what happened and what each side says; label opinion as opinion. Any topic is open, but never
  phrase anything as a call to violence and never mock a group of people.
- Draw everything (maps, flags, logos as simple generic shapes, people as our own characters). No news footage,
  photos or clips from other outlets, and no real company logos copied exactly.
- Real people are shown as our own cartoon characters and quoted only with their real, sourced words.
- Each video ships with an upload sheet: title, alternative titles, description (with sources), hashtags, tags,
  pinned comment.
- No metadata or encoder tags in outputs; never strip other parties' provenance watermarks (e.g. SynthID).
- Only the owner's own voice is cloned. Don't make Interestingly Strange or doctor (Body Facts) videos on this branch:
  they have their own chats and branches (`ccr-56282fe5-evehq4`, `ccr-56282fe5-evehq4-doctor`).

## Owner's channel-wide decisions (5 Oct 2026)
1. **Voice: Kokoro, not the cloned voice.** The default narrator is Kokoro `am_fenrir` at speed 0.95 (`motion/voice.py`).
   Use the owner's cloned voice (`NARRATOR_ENGINE=clone`) only if the owner asks. On Interestingly Strange, more viewers
   swiped away on cloned-voice videos (about 35% stayed) and Whisper misheard it far more often. For a voice unique to
   this channel, Kokoro can blend voices (e.g. `NARRATOR_VOICE="am_fenrir,am_fenrir,am_michael"`): offer the owner
   2-3 short samples, checked with Whisper medium, before picking one.
2. **Posting: 2 videos a day, not 3.** Many similar videos a day is riskier under YouTube's "inauthentic /
   mass-produced content" rule.
3. **Script first.** For every new video, send the owner the script first (each line, what's on screen, title,
   sources) and render only after they approve or edit it. Keep their wording; if one of their lines would be
   misheard, say so and suggest a fix. Their ideas, opinions and edits make each video original, which protects
   monetization.
