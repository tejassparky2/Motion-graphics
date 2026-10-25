# Handoff for the next session (updated 18 Oct 2026; older notes below)

Read CLAUDE.md first, then PROJECT_HISTORY.md and docs/owner_messages_log.md (every owner message, word for word).
Branch: `ccr-56282fe5-evehq4` (Interestingly Strange, English). Always `git pull --rebase` before pushing: other chats
also push here. The repo is **public**.

## Status on 25 Oct 2026 (session_013CwwMNXoAKQ7CXyLhTs3ka)
- Sets go out 5 at a time from the row after the owner's last post; last set sent = rows 52, 53, 55, 56, 57 (row 54
  zeigarnik skipped: "not good"). Next set = rows 58-62. Calendar dates run ~1 day behind real posting.
- Made since 19 Oct: grandma_dog (72), perfect_life (73), and Big Questions batch 2 (owner approved 25 Oct, scripts in
  out/scripts_big_questions_batch2.md): who_made_evil (74), heaven_forever (76), pascal_bet (78), prayer_plan (80),
  kitten_evil (82), packed in out/packs/ with upload_sheets_74-82.md and sent. Rows 75 (operation_mincemeat idea), 77,
  79, 81 are non-religion slots still to script so God topics never run back to back.
- New separate chats in this account: doctor session_01JxTaQcbebRyNYhRFBsreT8, rap session_01HjoP5cAkbdN76zxdeHTtKA,
  3D horror session_0153qDV4AufFgT2PhEBEfS8n, Yours3D session_0156jCxcSbUyKaKSLzbUk5am, low-poly
  session_01FVT6MqPXrfUtaaECNhx18u. skill-finder skill installed on every branch (ask the owner before installing
  any third-party skill it finds).
- Owner said the God-rock video did well; owner asked about a pufferfish-interview comedy format (answered only).

## Status on 19 Oct 2026, early morning (new account chat, session_013CwwMNXoAKQ7CXyLhTs3ka)
- **Sent to the owner on 18 Oct:** pack 42-45; row 56 and rows 58, 60-64, 66 (the Oct 26-31 batch, pack 58-66);
  the 3D sample out/robot_butler.mp4 (not in the calendar; owner hasn't decided on 3D yet); the research report
  reports/Shorts hooks feeling and subscribers.md (47-rule checklist).
- **Big-question batch, rows 67-71 (Nov 1-3), owner: "After research make 5 videos based on it auto approved"**:
  free_will_god, print_money, trolley_problem, grandfather_paradox, euthyphro, made with the research-upgraded
  pipeline (see CLAUDE.md "Research rules"): music drop-out under the twist, sidechain duck, richer bed, slow push-in
  on every scene, series chip (rows 68 and 70 carry the silent "Subscribe · a new question tomorrow" wording as the
  E4/E5 test; 67, 69, 71 the plain series tag), 0.5 s tail. Pack: `python tools/make_pack.py out/packs 67 71`.
  **All five rendered, Whisper-medium clean, packed (out/packs/67-71) and sent to the owner on 18 Oct night.**
  Lengths 43.9 / 39.9 / 36.0 / 40.8 / 40.3 s. One script change from the approved text: trolley "One life, to save
  five" was heard as "say five", so it reads "One life, to rescue five." print_money's only audit flag ("dollars"
  missing) is Whisper writing "$100 trillion": the word is spoken (checked with word timestamps).
  Owner may also have meant 5 *additional* research-based videos (rows 72-76): ask in the morning.
- **Owner's standing asks from 18 Oct night:** "improve both animations narration sounds music everything according
  to research" and "animation upgrade as much you can it should look engaging for users to stay till end". Done in
  the pipeline for 2D (motion/kit.whip push-in, motion/audio bed + duck + hush, render.py TWIST/SERIES) and 3D
  (medium-shot opener, same audio). Still open for later: character acting upgrades in 2D (more poses/expressions
  per line), 3D set variety, and the on-channel tests in the report (CTA on/off, 2D vs 3D, hook text size).
- **Still unanswered by the owner:** re-voice rows 43-45 in Turbo; make the repo private + commit the chat export;
  upload reminders in this account (~11 AM IST); 3D or 2D going forward; which slot the 3D sample takes if posted.
- **Policy warnings to repeat to the owner (from the research):** the genie formula matches YouTube's inauthentic-
  content wording if outcomes don't rotate; 1,000 subs alone won't monetize (3M/10M/20M Shorts-view tiers).
- **Container notes:** pipeline = `/home/user/.venv-main/bin/python` (3.12, Kokoro 0.9.4); Turbo in `/home/user/.venv-clone`;
  3D deps in build/is3d (npm). Keep each background job under 2 h; never `pkill -f` a pattern that matches your own shell.

## Status on 18 Oct 2026 (from chat session_011eLEn9HbPwBg7ViAYhwmQ5)
- **Posting:** 4:30 PM and 7:30 PM IST, trial Oct 16-29 (then compare first-24h views with the old times).
- **Sent to the owner as packs:** rows 34-37 (Turbo versions), 38-41 (barber, heap, spear & shield, mechanical turk;
  Kokoro am_fenrir), 50-54 hook tests, 55/57/59 funny history (napoleon_bunnies, bucket_war, dancing_plague; Turbo +
  tags). Next due pack: rows 42-45 (`python tools/make_pack.py out/packs 42 45`, send files + sheet).
- **Voice:** never the owner's cloned voice. Story videos: Chatterbox Turbo stock narrator + tags. ElevenLabs Chris /
  Liam in the other chat's videos (needs ELEVENLABS_API_KEY in the environment).
- **Comments:** debate rule (take a side, one sharp, meaningful reason, end on a question); see CLAUDE.md.
- **Waiting on the owner:** swipe-away / APV screenshots for hook tests 50-54 (2-3 days after posting); Oct 29 timing
  comparison; whether to re-voice rows 38-49 (Kokoro) in Turbo.
- **Other channels, other chats:** low-poly Claude/Codex skits -> chat session_012rinrNzawPSmYoY5bBrYza, branch
  `ccr-56282fe5-evehq4-lowpoly` (handoff: channels/lowpoly/NEW_CHAT_PROMPT.md); doctor, news and 3D-print on their
  own branches; Hindi in the ElevenLabs chat.
- **New container setup:** the voice/whisper tools in this repo expect Chatterbox (Turbo) in `/home/user/.venv-clone`,
  Kokoro, faster-whisper (medium) and rubberband; a fresh container may need them installed before voicing.

# Older handoff (written 14 Oct 2026)

Read CLAUDE.md first, then PROJECT_HISTORY.md (everything since Sep 29) and docs/owner_messages_log.md
(every owner message, word for word). The owner added `ELEVENLABS_API_KEY` to this environment (check it exists; never print it).
The old chat can't see the key, so **this new chat takes over both channels** (English and Hindi), on the same branch
`ccr-56282fe5-evehq4`. Hindi files live under out/hindi/ and videos_hi/ (keep them apart from the English ones).

## Status (14 Oct, new chat session_01G9k2suGZz1hYE4uG6LGe8F, branch ccr-56282fe5-evehq4)
- Step 0 done: the 4 upload reminders (rows 34-37, 38-41, 42-45, 46-49) fire into this chat; old ones deleted.
- Voices chosen by the owner: **English = ElevenLabs Chris**, **Hindi = ElevenLabs Liam** (CLAUDE.md has the rules).
  Engine: `NARRATOR = dict(engine="elevenlabs")` in a video; samples in out/voice_samples/ and out/hindi_samples/.
- The five genie-style videos are made with Chris and Whisper-checked: robot_obey (46), principal_sentence (47),
  mirror_never_lies (48), genie_returns (49), ghost_deal (65, Oct 31). Sent to the owner for review.
- ElevenLabs free plan: ~6,100 of 10,000 characters used by 14 Oct; resets Nov 14. No commercial licence on the free
  plan; the owner was told a paid plan is needed for monetized uploads and for native Hindi library voices.
- Hindi: Liam sample of the Hinglish genie script (out/hindi_samples/hi_liam_genie_story.m4a, Abhay-style dramatic
  storyteller). Still waiting for the owner to approve out/hindi/scripts_batch1_hinglish.md before rendering. The
  Hindi pipeline still needs: Devanagari captions (Noto Sans Devanagari), a Hindi Whisper check in el_check
  (language="hi", model "medium"), and Hindi titles/sheets.

## 0. Move the upload reminders to this chat (done)
The every-2-days upload reminders were bound to the old session (session_011eLEn9HbPwBg7ViAYhwmQ5). List them
(list_triggers: "Upload reminder: rows 34-37", "rows 38-41", "rows 42-45", "rows 46-49"), recreate each one in this
session with the same time, then delete the old ones. Rewrite each prompt from out/content_calendar.md
(the old ones still name twain_dead_twice at row 37 and achilles at row 46; the calendar is right: 37 is immortal_jellyfish, 46-47 are open). Reminders ALWAYS send the video files
(python tools/make_pack.py out/packs FIRST LAST + SendUserFile).

## 1. ElevenLabs voice samples, FIRST (owner: "test elevenlabs English voice; if emotions are good we can switch")
- **English:** same lines as out/voice_samples/ (Teacher Bluffed): "A teacher finds a pack of cigarettes in the
  classroom trash can. / The school's cameras have been broken for years. / But the kids don't know that. / So he makes
  a plan. / Four minutes of silence. Then Tyler stands up. / Everyone leans in. And it's... candy cigarettes!"
  Make 3 samples with emotional premade storyteller voices (eleven_v3 with audio tags like [whispers], [excited],
  [gasps], [laughs]; or eleven_multilingual_v2). Compare with the owner's current favourites: Chatterbox Turbo
  (out/voice_samples/en_turbo_tags.m4a, "not bad") and Kokoro am_fenrir (current narrator).
- **Hindi (Hinglish):** "सर, क्या भगवान इतना heavy पत्थर बना सकते हैं, कि वो खुद भी उसे lift ना कर पाएं? पूरी class एकदम
  silent. और teacher? वो बस smile करते रहे।" Make 3 samples (2 male, 1 female), emotional storyteller like the
  owner's reference (Abhay Create's Hindi Shorts).
- Never clone a real person's voice; premade/library voices only. Check every sample with Whisper medium (English:
  medium.en; Hindi: WhisperModel("medium", local_files_only=True), language="hi"). Save to out/voice_samples/ and
  out/hindi_samples/, send to the owner, ask which ones.
- Rejected for Hindi so far: Kokoro hm_omega/hm_psi/hf_alpha, Chatterbox multilingual (stock and owner clone).
- If ElevenLabs wins: add an `elevenlabs` engine to motion/voice.py (one API call per sentence, cached in build/,
  keep SENTENCE_TAKES / full-stop pauses; characters can use other ElevenLabs voices), then follow the owner's call on
  which videos to switch.

## 2. Hindi channel
- Waiting for approval: out/hindi/scripts_batch1_hinglish.md (5 videos: hotel, Last Bencher, Teacher Bluffed, genie,
  lucky coin). After the voice and scripts are approved: Hindi narration + Devanagari captions (needs a Noto Sans
  Devanagari font), English on-screen signs for now, render into out/hindi/.

## 3. English channel status
- Calendar: out/content_calendar.md. Made through row 45 (Oct 21 4:30 AM). Row 42 (Oct 19 9:30 PM) is the Turbo voice
  test: out/packs/42_Oct19_930PM_court_paradox_TURBO_VOICE_TEST.mp4 (compare its stayed-to-watch %).
- Waiting for approval: out/scripts_genie_style_batch1.md (robot, principal, mirror, genie returns, ghost Halloween).
  The genie video is doing well; these fill the open slots from Oct 21 9:30 PM (ghost on Oct 31).
