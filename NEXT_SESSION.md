# Handoff for the next session (written 14 Oct 2026)

Read CLAUDE.md first. Then pick up here:

## 1. Hindi (Hinglish) channel: ElevenLabs voice samples, FIRST
- The owner added an ElevenLabs key as the environment secret `ELEVENLABS_API_KEY` (check it exists; never print it).
- Make 3-4 Hinglish samples of this line with emotional ElevenLabs voices (the eleven_v3 model supports Hindi and
  audio tags like [excited], [whispers], [laughs]; otherwise eleven_multilingual_v2):
  "सर, क्या भगवान इतना heavy पत्थर बना सकते हैं, कि वो खुद भी उसे lift ना कर पाएं? पूरी class एकदम silent. और teacher? वो बस smile करते रहे।"
- Target: emotional storyteller delivery like the owner's reference (Abhay Create's Hindi Shorts). Try 2 male and 1
  female premade Hindi/Indian voices from the ElevenLabs voice library. Do not clone any real person's voice.
- Check each sample with Whisper medium (multilingual, cached: WhisperModel("medium", local_files_only=True),
  language="hi"), save to out/hindi_samples/, send to the owner, ask which one.
- Rejected so far: Kokoro hm_omega/hm_psi/hf_alpha, Chatterbox multilingual (stock and owner clone).
- Indic Parler-TTS is ready in ~/.venv-indic (tools/hindi_parler_test.py) but needs `HF_TOKEN` (gated model).
- Waiting for approval: out/hindi/scripts_batch1_hinglish.md (5 videos). After the voice is chosen and the scripts are
  approved, add a Hindi narration path to motion/voice.py (ElevenLabs per sentence, cached in build/), Devanagari
  captions (needs a Noto Sans Devanagari font), and render the Hindi versions into out/hindi/.

## 2. English: Turbo narrator test
- out/court_paradox_turbo.mp4 = the court paradox with Chatterbox Turbo's stock voice
  (`NARRATOR_ENGINE=clone CLONE_MODEL=turbo`). Posting slot: row 42 (Oct 19, 9:30 PM). Compare its stayed-to-watch %
  with similar Shorts before switching more videos to Turbo.

## 3. Waiting on the owner
- out/scripts_genie_style_batch1.md: 5 genie-style scripts (robot, principal, mirror, genie returns, ghost Halloween).
  Owner said the genie video is doing well; make these after approval for the open slots from Oct 21, 9:30 PM.
- Calendar: out/content_calendar.md. Upload reminders (trig_...) send packs via tools/make_pack.py.
