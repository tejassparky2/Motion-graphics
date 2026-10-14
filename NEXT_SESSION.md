# Handoff for the next session (written 14 Oct 2026)

Read CLAUDE.md first, then PROJECT_HISTORY.md (everything since Sep 29) and docs/owner_messages_log.md
(every owner message, word for word). The owner added `ELEVENLABS_API_KEY` to this environment (check it exists; never print it).
The old chat can't see the key, so **this new chat takes over both channels** (English and Hindi), on the same branch
`ccr-56282fe5-evehq4`. Hindi files live under out/hindi/ and videos_hi/ (keep them apart from the English ones).

## Status (14 Oct, new chat session_01G9k2suGZz1hYE4uG6LGe8F)
- Step 0 done: the 4 upload reminders (rows 34-37, 38-41, 42-45, 46-49) now fire into this chat with prompts rebuilt
  from the calendar; the old ones are deleted.
- ElevenLabs account is on the **free plan** (10k characters/month, no commercial licence, attribution required;
  library voices and Voice Design are blocked through the API). English samples made with premade voices
  (out/voice_samples/en_eleven_{brian,chris,liam}.m4a, eleven_v3 + audio tags). Hindi native-accent voices
  (Viraj, Rahul Hinglish, Monika Sogam) need the Creator plan or $5 credits: then run
  `python tools/elevenlabs_samples.py library`. Free-plan Hindi samples with premade (US-accent) voices:
  out/hindi_samples/hi_eleven_{brian_male,liam_male,jessica_female}.m4a. Waiting for the owner's pick.

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
