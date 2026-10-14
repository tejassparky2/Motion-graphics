# Interestingly Strange: the whole story so far (Sep 29 – Oct 14, 2026)

For any new chat: read **CLAUDE.md** (the standing rules), then this file, then **NEXT_SESSION.md** (what to do next).
Every owner message, word for word, is in **docs/owner_messages_log.md**.

## 1. The owner and the channel
- **Channel:** "Interestingly Strange" (YouTube handle ItsInterestinglyStrange). The owner picked the name on Sep 29
  and asked for names that are not India-only, because the target audience is the **USA / global**. The owner is in
  India and works in **IST**.
- **Content:** 2D hand-drawn YouTube Shorts: paradoxes, clever/funny twist stories, The Last Bencher riddles
  (teacher vs. kid), weird history, weird animals/insects, big theories (simulation, God), clever-words/quotes.
- **Posting:** **2 Shorts a day, 9:30 PM and 4:30 AM IST** (was 3 a day briefly; the owner went back to 2 on Oct 5
  as safer). The owner schedules uploads in Studio every ~2 days and wants **reminders that always include the video
  files and upload sheets** (Oct 13).
- **Workflow (owner, Oct 5):** script first → owner approves or edits → render → Whisper check → send files +
  upload sheet. The owner's edits and ideas keep the channel original (YouTube's inauthentic-content rule).
- **How the owner talks:** short phone messages, often with typos ("twai dead" = Mark Twain video, "bee one" =
  honeybee, "ber one", "hinglisj" = Hinglish, "en turbo" = the English Chatterbox Turbo voice sample).

## 2. Timeline
- **Sep 29:** Started from a reference Short ("How the Rich Fool You"). Built the code-driven 2D animation engine
  (pycairo) and the first video (The Pumpkin Trick). Added narration; the owner wanted **no silences, fast narration,
  fast visuals** → narration-driven timeline + word captions. Owner asked to remove AI watermarks/SynthID; we keep
  output free of encoder/metadata tags but **never strip other parties' provenance watermarks** (CLAUDE.md). Voice
  should be human-like with a little emotion → picked Kokoro **am_fenrir** (closest to the reference narrator).
  Channel name chosen: *Interestingly Strange*; logo, bio, SEO sheets made. Next videos: The Secret of Wife (follow
  the owner's script exactly, the owner was annoyed when the ending changed), lucky charm, lottery ticket, zombie ant,
  emu war. Best US-reach time discussed; owner chose 9:30 PM IST.
- **Sep 30:** Monty Hall, Backbencher vs Teacher (from the owner's reference "East or West Backbenchers is Best"),
  Shortest War, Infinite Hotel. 5 a day researched (owner chose 3, later 2). Batches: paradox / funny twist / insect /
  history. Class of Scammers ("The Teacher Bluffed") from the owner's reference. A **news & tech channel** idea
  (inspired by @omaragammy) → later its own chat and branch.
- **Oct 1–2:** Owner's **voice clone** (Chatterbox, prompt `assets/voice/owner_prompt.wav`); re-voiced batches.
  Owner renamed the riddle series **"The Last Bencher"** (not "Last Row Kid"). Rules born: **slow down riddles, never
  join sentences, full stops = real pauses** (applies to every video). Infinite Hotel hit **15K → 27K+ views**.
  **Doctor channel** ("Body Facts", cute organ voices) started → moved to its own chat/branch on Oct 3.
  Owner: "focus on paradox videos and shorter ~40 s", "explain paradoxes neatly so viewers understand", hook like the
  Hotel video, end with a question that brings comments.
- **Oct 3–4:** youtube-agent-skill repo shared (installed later, Oct 11). "Researchers said / clever words" series
  from the owner's reference (Abhay Create's Hindi Short about Napoleon). Owner: freedom to explore any topic,
  including controversial ones (keep it honest: real quotes, no calls to violence). Skipped #16, 18, 23, 26, 30 of
  an old batch ("no good content and understanding"); Diogenes needed clearer examples. **News & tech channel** moved
  to its own chat.
- **Oct 5:** **Swiping went up a lot on cloned-voice videos** → owner switched back to Kokoro am_fenrir ("our bot
  one") for this channel and the doctor/news channels. Back to **2 posts a day**. Script-first workflow agreed.
  Skipped #12 (exam answers). Pinocchio paradox swapped in for the principal video. Reminders every 2 days started.
- **Oct 6–7:** Asked for higher-quality animation and funnier narration (reference Video-26491) → built the
  **polished style** (`motion/polish.py`, `motion/toons.py`, `motion/pkit.py`): honeybee, Last Bencher 4, Achilles,
  Twain, jellyfish. Owner asked about running on their laptop (RTX 3080 4 GB) / VPS; decided to stay here for now.
- **Oct 9:** A separate **3D business voice-over/editing** chat (owner's cloned voice) was created, kept apart.
  "Pinocchio worked well, I want easy-to-understand, debate-worthy, mind-blowing ones" → court, crocodile, barber,
  spear & shield, with character voices and emotion. Big theories approved in advance: simulation, first cause (God),
  Fermi. **Research is light** (owner: use your own knowledge and creativity; original stories welcome, never present
  invented stories as true history).
- **Oct 10–11:** Polished style pushed to the doctor channel. Skipped the lottery-happiness video → the **genie
  wish** story was made (approved Oct 11). youtube-agent-skill installed (`.claude/skills/yt-*`, MIT), titles linted,
  sheets updated. Analytics export (Sep 29–Oct 11) analysed → `out/analytics_2026-10-11.md`. **Hook rules** added from
  that data (open on a scene, not a question). #47 rock-God video made, then v2 as a Last Bencher scene.
  Owner asked about 5-6 s meme Shorts (Nokia vs Apple reference, Spanish) → loops were "not funny" → three memes made
  (95 marks, exam chapter, 3 AM) → **memes belong to a different channel** (Oct 13), not this one.
- **Oct 13:** Reminders must always send the files (`tools/make_pack.py`). Owner skipped Socrates, Diogenes,
  marshmallow test ("not good"), kept Machiavelli. Approved the chess machine, heap paradox, lucky coin scripts.
  "Why did YT stop pushing my videos?" → Machiavelli 59.5% and Fermi 61.5% average viewed vs a ~90% channel average:
  talky explainers stall. Rule: **40–50 s, clearly understandable** (cut side facts, never logic steps).
- **Oct 14:** Owner had already scheduled Ben Franklin and Last Bencher 4; deleted the honeybee video (1:16, too long);
  skipped Mark Twain. **"The genie one is doing good, focus more on content like that"** → genie formula rule +
  5 genie-style scripts (waiting for approval). **Hindi channel** wanted: separate channel, same content, **Hinglish**,
  emotional voice like Abhay Create. Kokoro Hindi and Chatterbox Hindi rejected ("voice not good"). English with
  emotion wanted too: Chatterbox **Turbo** stock voice was "not bad" → one test video (court paradox, row 42).
  Owner added **ELEVENLABS_API_KEY**; only new sessions can see it → this handoff.

## 3. What works and what doesn't (owner feedback + analytics)
- **Works:** The Last Bencher / teacher-vs-kid stories (Last Row Kid 77.8% stayed, 15.5K views), The Teacher Bluffed
  (77.0%, 15.3K), Infinite Hotel (75.0%, 27.7K), Pinocchio (70%), the **genie** (doing well, Oct 14), Hanoi rats
  (1.2K in a day). Openings that drop you into a scene with something already wrong; endings that start a debate.
- **Doesn't:** talky thinker/study explainers (Machiavelli, Fermi ~60% viewed; Socrates, Diogenes, marshmallow,
  Twain, Ben Franklin-type skipped), long videos (honeybee 1:16 deleted), math/probability explainers (~50%), weird
  animal facts (~45%), the owner's cloned voice (more swipes), unfunny loops, memes (other channel).
- **Skipped/removed by the owner:** exam_answers (#12, Oct 5), principal video swapped for Pinocchio (Oct 5),
  old batch #16/18/23/26/30 (Oct 4), lottery_happiness (Oct 11), socrates_know, diogenes_alexander, marshmallow_test
  (Oct 13), honeybee_life (deleted, Oct 14), twain_dead_twice (Oct 14), the loop scripts L1-L3 (Oct 11).

## 4. Voices
- **English narrator now:** Kokoro `am_fenrir` (default). Characters use other Kokoro voices via `voice.SPEAKERS`
  (kid am_puck +2.5 st, sir am_michael, genie am_onyx, teacher af_bella, etc.).
- **Tried:** Piper (first days), the owner's Chatterbox clone (Oct 2–5, more swipes, dropped), Chatterbox stock
  lively/dramatic, **Chatterbox Turbo stock voice** ("not bad"; test video = row 42; engine:
  `NARRATOR_ENGINE=clone CLONE_MODEL=turbo`). Samples: `out/voice_samples/`.
- **Hindi tried and rejected:** Kokoro hm_omega/hm_psi/hf_alpha, Chatterbox multilingual (stock + owner clone).
  Indic Parler-TTS installed (`~/.venv-indic`) but gated (needs HF_TOKEN). Next: **ElevenLabs** (key added).
- **Rules:** clone only the owner's own voice, never a real third party; keep Perth/SynthID-style watermarks;
  every line checked with Whisper medium after rendering; misheard lines get reworded.

## 5. Other channels and chats (keep them apart)
- **Body Facts** (doctor channel): chat session_01SqhLvv9BAUwbaLsavHEv2W, branch `ccr-56282fe5-evehq4-doctor`.
- **Global news & tech**: branch `ccr-56282fe5-evehq4-news`.
- **3D business voice-over/editing** (owner's cloned voice): chat session_015ciz34JsfciV5Yzyk9A6zE, branch
  `ccr-56282fe5-evehq4-3d`.
- **Memes channel**: not set up yet; the three memes are kept in `videos/meme_*.py` / `out/meme_*.mp4`.
- **Hindi (Hinglish) channel**: being set up now (this handoff).

## 6. How the pipeline works (short)
- `python render.py --video NAME` → `out/NAME.mp4`, `_preview.mp4`, `_metadata.md` (upload sheet). `--sheet 1.5`
  contact sheet, `--still T` one frame. Videos are Python modules in `videos/` with `SCRIPT` (beats; `speaker`,
  `speaker_from`, `pace`, `gap`, `hold` for silent beats), `METADATA`, scene functions and `draw()`.
- Kits: `motion/polish.py` (drawing, captions, signs), `motion/toons.py` (characters: kid, sir, teacher, dad,
  napoleon, grandpa, aquinas, ...), `motion/pkit.py` (cards, buttons, stamps), `motion/meme.py`, `motion/timeline.py`
  (narration-driven timing, sentence takes and pauses), `motion/voice.py` (Kokoro / clone / turbo engines),
  `motion/audio.py` (music, sound effects, -14 LUFS).
- Checks: `python tools/audit.py NAME` (Whisper medium, every line), `tools/verify.py`, a frame scanner,
  `python tools/make_pack.py out/packs FIRST LAST` (dated files + combined upload sheet for the owner).
- Calendar: `out/content_calendar.md`. Analytics: `out/analytics_2026-10-11.md`. Scripts waiting:
  `out/scripts_genie_style_batch1.md`, `out/hindi/scripts_batch1_hinglish.md`.
- YouTube skills: `.claude/skills/yt-*` (title linter, hook scorer, retention reader...). Voice profile:
  `.claude/skills/_youtube-agent/voice.md`. Don't trust `hookscore.py` for this channel.

## 7. Open items right now
1. ElevenLabs samples: English (to compare with Turbo/fenrir) and Hinglish (for the Hindi channel). See NEXT_SESSION.
2. Owner approval of 5 genie-style scripts (robot, principal, mirror, genie returns, ghost Halloween on Oct 31).
3. Owner approval of 5 Hinglish scripts; then build the Hindi pipeline (voice, Devanagari captions).
4. Turbo voice test (row 42, Oct 19 9:30 PM): compare stayed-to-watch % before switching more videos.
5. Calendar: made through Oct 21 4:30 AM (row 45); open slots after that.
6. Move the upload reminders to the new chat (they fire into the old session).
