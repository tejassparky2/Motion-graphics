# Interestingly Strange: standing rules

## Workflow: script first, owner approves, then render (protects monetization)
- For every new video, first send the owner the script: each narration line, a one-line note of what's on screen,
  the title and the sources. **Don't render until the owner approves it** or sends changes.
- The owner adds or changes lines as they like; keep their words. If one of their lines would be misheard by the
  voice, say so and suggest a fix rather than changing it silently.
- The owner's own ideas, opinions and edits are what make each video original (YouTube's "inauthentic content" rule
  targets mass-produced, templated videos), so ask for them and vary formats, scenes and characters.
- Post **2 videos a day at 4:30 PM and 7:30 PM IST** (owner, 15 Oct 2026, from analytics: viewers peak 5-8 PM IST;
  India 21%, Philippines 16%, US 14%). Was 9:30 PM and 4:30 AM until Oct 15.
  **2-week trial, Oct 16-29** (owner agreed 15 Oct): then compare first-24-hour views with the old 9:30 PM / 4:30 AM
  posts and keep whichever does better.

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
- **Default narrator for new videos: Chatterbox Turbo's stock female voice + emotion tags** (owner, 18 Oct 2026:
  "Turbo default female"; `NARRATOR_ENGINE=clone CLONE_MODEL=turbo` or Turbo in the video's NARRATOR settings),
  characters in their own Turbo voices (`turbo_ref`). ElevenLabs Chris stays only in the videos already made with it
  (rows 46-49, 65). Earlier notes on both voices:
- Narrator: **ElevenLabs "Chris"** for new videos (owner, 14 Oct 2026: "Chris is good, make the genie scripts with him
  for emotions"). A video opts in with `NARRATOR = dict(engine="elevenlabs")`; characters get their own ElevenLabs
  voices in `voice.SPEAKERS` (`el=voice.ELEVEN[...]`, `pitch`, `fx`), each line can carry a `tone` (an eleven_v3 audio
  tag such as "dramatic", "whispers", never shown in captions). Every take is Whisper-checked and re-made if misheard
  (`voice.el_check`); `python tools/el_redo.py VIDEO "sentence"` throws a take away. Rushed narrator takes are slowed
  toward 5.5 syllables/s. Premade or library voices only, never a clone of a real person.
  Older videos keep Kokoro `am_fenrir`. **Never the owner's cloned voice** (owner, 15 Oct 2026: "I don't want videos
  in my cloned voice"); tools/clone_tts.py refuses it unless ALLOW_OWNER_CLONE=1. On 14-15 Oct a bug voiced the Milo
  videos and the first lucky-coin/rock "Turbo" versions with it (the Turbo setting didn't reach the voice tool); fixed
  in motion/voice.py (CLONE_MODEL passed to the subprocess, CLONE_VERSION v4) and all of them re-voiced.
- ElevenLabs account: **free plan** (10,000 characters a month, resets on the 14th; no commercial licence, attribution
  required; library voices and Voice Design blocked through the API). A 40 s video costs ~700 characters plus
  retakes. Check `GET /v1/user/subscription` before a batch and tell the owner when the quota runs low.
- **Turbo + emotion tags (owner, 14 Oct 2026: "This is better")**: the crocodile video re-voiced with Chatterbox Turbo
  for narrator AND characters (characters via `turbo_ref`), with sound tags placed where a storyteller would make the
  sound, won over the plain versions. Make new story videos this way (`NARRATOR_ENGINE=clone CLONE_MODEL=turbo`;
  how-to and what each tag really does: `out/turbo_tags_research.md`). One sound tag per line at most, 4-6 per video,
  none on logic lines. Keep comparing stayed-to-watch % (rows 36 and 42) against the Kokoro videos.

## Research rules (18 Oct 2026; full evidence in reports/Shorts hooks feeling and subscribers.md, 47-rule checklist)
- The gains are at the two ends: stayed-to-watch (~70%) is the channel's weak number, average % viewed (~92%) is strong.
  Frame 0: a face, the "wrong" object, big hook text, and sound from the first frame (SnapUGC: survival at 5 s
  correlates 0.93 with watch %). 3D opens on a medium/close shot, never a wide or dark establishing shot.
- The hook's question must be one the viewer can almost answer (curiosity peaks at "almost sure"); no clickbait
  wording (no measurable lift, costs credibility); never spoil the twist in the title.
- Ending: the either/or question is the literal last spoken line, cut within ~0.5 s (`TAIL = 0.5`); at most ~4 s of
  material after the twist; the callback is one sentence or folded into the question. No outro, no "comment below".
- Pipeline: `TWIST = "<beat id>"` drops the music under the twist line (a tick before it); `SERIES = "..."` shows a
  small series chip in the first 2 s and on the final line (`END_TAG` = silent subscribe wording, tested on
  alternate videos only, never a spoken ask before the payoff); every scene has a slow push-in (`motion/kit.whip`);
  music is a plucks + sub-bass + shaker bed with a sidechain duck (20 ms / 300 ms). Captions stay at 71% (moving
  them would cover faces; the band position is only anecdotal evidence).
- Rotate story outcomes (kid wins / authority wins / rule backfires / both lose / reframe): YouTube's inauthentic-
  content rule bans "characters put in the same situation over and over again with the same outcome". Log the
  outcome per calendar row; no two consecutive videos share one.
- Big questions are thought experiments about ideas, never contests between groups; both sides voiced by characters
  with one real reason each; moral words ("fair", "cheat", "deserve") in the debate line. Money videos never give
  financial advice.
- Measure against the channel's own median: stayed-to-watch >= 75%, APV >= 85%, subs per 1,000 engaged views >= 2.
  Monetization: 1,000 subs alone is not enough; the Shorts-view tiers are 3M/90 days (500-sub tier), 10M until
  31 Jan 2027, 20M after. The posting-time trial compares 7- and 28-day views too, not only the first 24 h.

## Line 1 = a character asking the impossible question (export of 26 Oct 2026; owner: "Ship it")
- Stayed-to-watch by opening, 59 Shorts: character asks from the first words ~72%; narrator sets a scene first ~62%;
  talking to the viewer / topic / "Meet" / "Did you know" / numbered list ~47%. Average viewed is 85.7%, so the swipe
  in the first seconds is the whole problem. Full numbers: out/analytics_2026-10-26.md.
- Every new script opens on a character's spoken question or demand ("Sir, can God...", "Beta, is Bruno eating
  properly?", "Press the button. Live the perfect life."); the narrator's setup comes second, in one short line.
- No more hook tests that talk to the viewer. Business ads (Yours3D) never go on this channel.

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

## Debate: in comments and in videos (owner, 16 Oct 2026: "we always debate that's what bring engagement also follow debates in video")
- Comment replies argue back: take a clear side, give one sharp reason, and end on a question the commenter has to
  answer. Don't concede or say "you're in good company"; stay friendly and never insult anyone.
- Videos set up a debate: show both sides fairly, let one character take a strong side, and end on a two-sided
  question people will argue about in the comments (e.g. "Did the teacher win, or did he dodge?").
- **Always meaningful** (owner, 16 Oct 2026: "always it should be meaningful"): every argument carries a real idea
  the viewer learns something from (a reason, a fact, a thinker's answer), and the closing question has two
  genuinely defensible sides. No arguing for its own sake, no rage-bait, no "comment YES or NO" filler.

## Big questions that are hard to answer (owner, 18 Oct 2026: "This did well we need to focus on more video like this which is cotervinal hard to assume arrise questions")
- The Last Bencher God-rock video (row 35, Turbo) held 0:34 of ~37 s (~92% viewed), 70.7% stayed to watch.
- Make more videos built on a **controversial, hard-to-answer question** (God, free will, right and wrong, money,
  life and death choices, time travel) that viewers can't guess the answer to and that makes them ask more.
- Put the question in a character's mouth in a scene (kid vs teacher works best), show why both answers break,
  then give a real thinker's answer (sourced: Aquinas, Boethius, Plato...) and end on a two-sided question.
  Respectful and honest, especially on religion: argue ideas, never mock believers or non-believers.

## What to make more of (owner, 14 Oct 2026): "the genie one is doing good"
- Lead with **genie-style stories**: a character with ONE rule (genie, robot, magic mirror, principal, ghost) and a kid
  who turns the rule against itself with one clever line. The authority freezes; the narrator shows both branches in
  two short sentences ("If he grants it... If he refuses..."), ends "Either way, ...", adds a funny callback, and
  closes on an either/or question ("Grant the wish, or not?"). Original stories, character voices, about 40 s.
- Vary the character and setting every time (inauthentic-content rule): never two of the same character in a row.

## Milo series: dropped (owner, 15 Oct 2026: "Don't want Milo videos, I didn't like it, skip it")
- Don't make Milo / AI-image thriller videos. The three made (milo_sweetie, milo_attic, milo_basement) and the batch-2
  scripts are shelved, not posted. The tools stay in the repo (tools/shots.py, motion/thriller.py) in case the owner
  wants them back.

## Long videos: idea only, not now (owner, 15 Oct 2026)
- If we ever make long-form videos, the topics are **"what if" scenarios, how finance/money works, and funny history**.
  Don't make any until the owner says so (monetization route: 4,000 long-form watch hours before the Feb 2027 change).

## Length: 40-50 s and clearly understandable (owner, 14 Oct 2026)
- Target **40-50 s**; clarity comes first: every step of the logic stays, one step per sentence. Cut side facts,
  repeats and extra examples instead. Machiavelli and Fermi (talky explainers) stalled at ~60% viewed against a ~90%
  channel average, so nothing over 50 s and no slow, abstract openings.
- Alternate formats in the queue: never two explainers back to back; stories (Last Bencher, twist stories) go first.

## Paradoxes must be explained so any viewer understands
- Clarity first, within 40-50 s: one step per sentence, no repeated steps or side facts.
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
  **Send 5 videos per set** (owner, 19 Oct 2026: "from now send 5 video in 1 set"), starting from the row after the
  last one the owner posted (set 1 = rows 42-46, after row 41 mechanical_turk "Napoleon chess").
- No metadata or encoder tags in outputs; never strip other parties' provenance watermarks (e.g. SynthID).
- Riddle series is called **The Last Bencher** (not "Last Row Kid").
- Memes (the 6–9 s "Me: / Dad:" reaction format) are for a **different channel**, not Interestingly Strange (owner,
  13 Oct 2026). The three made on 11 Oct (`meme_95_marks`, `meme_exam_chapter`, `meme_3am`) are kept for that channel.
- **Hindi channel** (owner, 14 Oct 2026): a separate channel with the same videos in **Hinglish** (everyday Hindi with
  common English words kept: teacher, class, exam, phone). The voice must carry emotion like the owner's reference
  (Abhay Create's Hindi Shorts). Kokoro Hindi and Chatterbox Hindi samples were rejected ("voice not good").
  Narrator: **ElevenLabs "Liam"** (owner, 14 Oct 2026: "for hindi Liam seems good"), read like a dramatic Hindi Shorts
  storyteller. Liam is a US premade voice, so some Hindi words carry an accent; native Hindi library voices (Viraj,
  Rahul Hinglish, Monika Sogam) need a paid plan.
  From 14 Oct the new chat (which can use ELEVENLABS_API_KEY) runs both channels; see NEXT_SESSION.md. The full history since
  Sep 29 is in PROJECT_HISTORY.md, and every owner message word for word is in docs/owner_messages_log.md.
- The doctor channel ("Body Facts") is a separate channel with its own chat and branch (`ccr-56282fe5-evehq4-doctor`). Don't make doctor videos on this branch.
  Since the account move its chat in this account is session_01JxTaQcbebRyNYhRFBsreT8 (owner, 24 Oct 2026: English
  medical explainers in the style of the Instagram page meanwhilemayank).
- **Low-poly 3D channel** (Claude/Codex dev-comedy skits; owner, 17 Oct 2026): a separate channel that **moves to its
  own chat** (owner, 17 Oct: "low poly goes to different chat"). Code and notes: `channels/lowpoly/` (README.md has
  the references, look, music and camera rules; episode 1 is out/lowpoly/ep01_code_review.mp4). Don't make low-poly
  videos in this chat, and don't put them in the Interestingly Strange calendar.
  Since the owner's account move (18 Oct 2026) its chat in this account is session_01FVT6MqPXrfUtaaECNhx18u
  ("Low-poly 3D channel: Claude & Codex skits"), branch `ccr-56282fe5-evehq4-lowpoly`.
- **Yours3D India business reels** (owner's 3D figurine business, Instagram; voice-over + editing): separate chat
  session_0156jCxcSbUyKaKSLzbUk5am, branch `ccr-56282fe5-evehq4-3d` (rules in projects3d/README.md there). Don't make
  them on this branch.
- **Rap music videos** (owner, 24 Oct 2026: "not for this channel"): separate chat session_01HjoP5cAkbdN76zxdeHTtKA,
  branch `ccr-56282fe5-evehq4-rap` (lyrics written by us, song generated by the owner in Gemini, dark-anime lyric video).
  Don't make them on this branch.
- **Interactive 3D horror stories** (owner, 25 Oct 2026: "not for this channel", "3D"): separate chat
  session_0153qDV4AufFgT2PhEBEfS8n, branch `ccr-56282fe5-evehq4-horror` (second-person, viewers vote what happens in
  part 2). Don't make them on this branch.
- The global news & tech channel is also separate, with its own chat and branch (`ccr-56282fe5-evehq4-news`). Don't make news videos on this branch.
