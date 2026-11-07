# Indian mythology channel: 2D-animated story reels in Hindi and Kannada

Started 6 Nov 2026 from the Socho with Tejas chat. Owner: "I want to make high quality 2d animation indian mythology
reels in hindi and kannada for hindi the voice you already have and we try to make kannada ... this is for different
chat". This channel has its own chat and its own branch, `ccr-56282fe5-evehq4-mythology`, in its own worktree
(`<shorts research>/Motion-graphics-myth`). Don't switch the branch of the shared `Motion-graphics` checkout.

**Owner decisions, still open:** Hindi channel name (Kannada is "Namma Purana"). Kannada voice: designed voice A
(7 Nov 2026). See Voices and Status.

## Owner instructions, 6 Nov 2026 (night)
- "make me three 60 seconds or more videos all 3 with different approach animation scene etc in both kannada and
  hindi ... i want all videos ready till morning"; "3 videos with different approach different hook different
  animation". Built without script approval because the owner asked for them ready by morning.
- Kannada: "normal everyday speaking kannada kanglish and standard kannada only city peoples taking kannada":
  Bengaluru-style spoken Kannada, written in Kannada script.
- **English only when needed** (owner, 7 Nov 2026: "Use English only when needed kanglish means not this much English
  refer to shorts chat hinglish it does better"): as much English as our Hindi versions, no more. Kannada words and
  verbs; English only for words city people really say in English (ಹಾಲಿವುಡ್, ಹಾರರ್, ಶಾಕ್, ಕಾಮೆಂಟ್, ಜೈಲು). Never an
  English verb + ಮಾಡು (ಇಮ್ಯಾಜಿನ್ ಮಾಡಿ, ವೇಟ್ ಮಾಡಿ, ಸೆಲೆಕ್ಟ್ ಮಾಡಿ), and no ಜಸ್ಟ್, ಸ್ಟೋರಿ, ಪ್ರಾಮಿಸ್, ಫ್ಯಾಮಿಲಿ, ಹೈಟ್,
  ಪ್ರಾಬ್ಲಮ್. Hook "ಯೋಚಿಸಿ..."; ending "ಹೌದಾ ಇಲ್ವಾ, ಕಾಮೆಂಟ್ ಮಾಡಿ ಹೇಳಿ." When a Kannada word changes, change its
  cue word in the scene code too (cues are `{"hi": ..., "kn": ...}` or `C(tl, id, hi, kn, frac)`).
- **Upload text in Kanglish** (owner, 7 Nov 2026: "I want captions titles also in kanglish", "I said caption and
  titles for Instagram and youtu not in videos"): Kannada METADATA (titles, captions, descriptions, pinned comments)
  is Kannada written in English letters, like the Hindi METADATA: "Neevu hogteera? Houda illva, comment maadi 👇".
  The spoken script stays in Kannada script (the voice reads it). `finish.py ... --pack-only` rebuilds just the
  upload sheet and copies it to Drive.
- Voice: "clear calm and well understandable": tempo 1.05 (Hindi) and 1.0 (Kannada), clarity retakes only.
- "Download everything is auto approved until my next message": SDXL checkpoint, Real-ESRGAN, ComfyUI's CUDA
  environment and the parallax helpers were downloaded under that approval. The Civitai miniature LoRA needs a login,
  so it was skipped (no logins).
- Another session also uses the GPU: voice_all.py waits until it is free.

## The three approaches (from the 2D playbook and the research report, myth_out/research/)
| Video | Approach | Hook style |
|---|---|---|
| kakudmi | A: code-drawn chibi cast (`myth_cast.py`: crowns, jewellery, dhoti, saree, three-headed Brahma) on SDXL background plates (`plates.py`) with light rays, petals, counters | second person: "imagine you waited a few moments..." |
| brahma_calves | B: living manuscript: CC0 Cleveland Museum miniatures cut into layers, multiplane parallax, glow and petals (`scenes_brahma_calves.py`) | a character's impossible question (Brahma's) |
| jarasandha | C: Togalu Gombeyaata leather shadow puppets drawn in code on a lamp-lit screen (`scenes_jarasandha.py`) | a staccato list: "one eye. one hand. one leg. half a face." |

Sound: `motion/audio.py` gained bell, conch, shimmer and damaru effects and a `tanpura` drone bed (channel MUSIC).
Finishing: `finish.py <video> <lang> <n>` makes the cover, the phone copy, the upload pack and the Drive copy.

## Standing rules (from the owner; never break these)
- The repo is **public** (tejassparky2/Motion-graphics). Never commit chat files, downloaded videos, keys or anything
  private. Pull before pushing. Commit messages end with `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.
- Keys live in `<shorts research>/.env`. Never read or print them; the scripts load them.
- **Voice cloning: only the consented Kannada voices.** On 7 Nov 2026 the owner approved clones of their own
  voice ("this is mine"), their brother's ("the first one was from my brother and he agress") and their friend
  Darshan's ("Clone this voice it's my friend's and he agrees", "Copy the same narration style from this voice") and
  their friend Hemanth's ("Try cloning this", then "Yes hemanth said yes") for the Kannada reels. Always confirm the
  person agreed before cloning (Hemanth's recording came without a word on consent; we asked first). Nobody else is ever cloned (no famous narrator, no TV-serial voice). Hindi stays synthetic Aman.
  The recordings and references stay in `myth_assets/voice/` and never go in the repo. Suggested to the owner (not
  yet decided): on upload, answer YouTube's "altered or synthetic content" question with yes and turn on Instagram's
  AI label. Those are upload settings, not caption words, so the no-AI-wording rule still holds.
- **No downloads** of new tools or models until the owner says "download". Explain the option and ask first.
- **No AI wording** in captions, descriptions or upload sheets.
- **Credits as names, never links.** Sources line: texts, translators, years. Art line 1: the sites the pictures came
  from. Line 2: CC BY authors' names. Licences: public domain, CC0, CC BY, Pixabay, Unsplash only; never BY-SA, NC, ND.
- No logging in to Instagram or any account; never enter passwords.
- **Religion: respectful and honest.**
  - Never mock a belief, a deity or a devotee; no political angle, no community-vs-community framing.
  - Name the text every story comes from (Valmiki Ramayana, the Mahabharata, a named Purana, with book and chapter
    in the module docstring).
  - When versions differ by text or region, say so in one short line ("kuch granthon mein...").
  - Never present a folk version or a TV-serial version as "the scripture says".
  - Never show a real person's face as a deity. Keep each character's look the same through a video.
  - No "science proves the Puranas" claims: a story can be compared with a modern idea, never offered as proof.

## Format (carried over from what worked on Socho with Tejas)
- Length 1:30-2:00. Over 2 minutes, cut side details first.
- **Frame 0:** one character or object alone on a plain ground, with a two-tier headline: a few small setup words
  plus ONE big key word carrying the contradiction, fully on screen by ~2 s and marked as it's spoken.
- **Line 1:** "सोचो..." / "ಯೋಚಿಸಿ..." or a question to *you*, with the impossible-sounding (but true to the text)
  contradiction inside it. Plain hooks get rejected (owner: "hook should be like impossible to assume belive simple
  hooks won't work").
- **Line 2, the source stamp:** "ye koi film ki kahani nahi... ye [text] mein likha hai".
- **Topics: little-known episodes**, the surprising detail most viewers have never heard, not the retelling everyone
  knows (owner, on the science channel: "Everyone knows this i want something unique and seems like unbelievable").
- A visible change every 1-1.5 s, densest in seconds 3-15. A re-hook question at about 60%.
- Ending: a short awe line, then a yes/no question ("Yes ya no, comment mein batao" / "ಹೌದು ಅಥವಾ ಇಲ್ಲ, ಕಾಮೆಂಟ್‌ನಲ್ಲಿ
  ಹೇಳಿ"). No subscribe ask, no part 2.
- Post on Instagram first, then YouTube the same evening, around 6 PM IST.

## One module, two languages
- `videos/<story>.py` holds `SCRIPTS = {"hi": [...], "kn": [...]}` with the **same line ids**, `METADATA = {"hi":
  {...}, "kn": {...}}`, the art (`P`, `USED_ASSETS`, `CREDITS_FILES`), `SHOTS`, `draw(cr, t, tl)` and `sfx(tl)`.
- The pictures and English on-screen headlines are shared; only the voice and the timing change.
- Cue words can be `{"hi": "...", "kn": "..."}`; `shots.T` picks the timeline's language (`tl.lang`).
- Scripts are written natively in each language, not translated word for word. Numbers are written as words, full
  stops for pauses, "..." for dramatic pauses.

## Voices
- **Hindi: "Aman"**, the Socho with Tejas narrator (owner: "for hindi the voice you already have"). Indic Parler-TTS
  named speaker Aman made the prompt; IndicF5 speaks every line; tempo x1.15, studio chain v3.
  Known slips: "नए/नई" comes out "नहीं"; "तेज़ चली" comes out "tes chali" (use "तेज़ी से"); a line starting with
  "प्रिंटिंग" stutters. Whisper often hears dh as d and jh as j; check the raw take before retaking.
- **Kannada (7 Nov 2026): a cloned real voice, the owner choosing which.** The owner rejected Suresh and Vidya
  ("The both kannada voice is not good") and sent two recordings: `brother_v1` (the brother, from muruli.mp3) and
  `tejas_v2` (the owner, from mine.mp3). Both had music under the voice: Demucs (HTDemucs) took it out, then a clean
  4-9 s piece cut at the quietest points, padded with 0.1 s / 0.4 s of silence, became the IndicF5 reference with its
  exact words in `<stem>.txt` beside it (channel.py reads it; choose with `MYTH_KN_VOICE`). A reference cut mid-word
  makes IndicF5 repeat the last syllable at the start of a line. Resemblyzer similarity of each clone to its speaker:
  0.93 (owner), 0.91 (brother). Turbo letter errors on the four sample lines: 4-34%, same range as Suresh.
- **Designed Kannada voices (7 Nov 2026)**, owner: "Try created new voice with description like we did in our shorts
  chat for hindi voice i want clear good voice similar to our hindi one", then "I want voice to feel human likeness".
  `kn_voice_design.py` (Indic Parler descriptions x seeds) -> `kn_voice_design_score.py` (turbo letter errors, pitch,
  pitch movement, Resemblyzer likeness to Aman) -> `kn_design_sample.py` (the Kakudmi teaser through IndicF5 and the
  studio chain). Findings: Parler's speaker **Aman reading Kannada** works (7-22% errors on the passage, 0.81-0.91
  like Aman); descriptions with no named speaker came out as gibberish in Kannada; IndicF5 prompted straight from the
  Hindi Aman clip also speaks clear Kannada. Through IndicF5 the best samples scored 5-7% mean errors (the clones:
  up to 44%). Sent as A `aman_orig_s11` (most pitch movement), B `aman_hindi` (the Hindi voice itself, 0.88 like
  Aman), C `aman_calm_s42` (calmer, flatter). More pitch movement reads as more human.
  **The owner picked A ("A", 7 Nov 2026): `design_aman_orig_s11` is the Kannada narrator** (channel.py default).
- **Darshan clone (7 Nov 2026)**: the owner's friend, with consent; "Copy the same narration style from this voice".
  His recording (65 s, music 13 dB under him, removed with HTDemucs) is fast continuous speech with only 0.1-0.2 s
  breaths. Reference `darshan_v1` = his first 9.5 s, cut at breaths (exact words in .txt). IndicF5 keeps his pace:
  13.7 letters/s against his real 13.5 (voice A: 12.6). Likeness 0.92, turbo errors 13% mean, 23% worst. A 4 s
  reference (`darshan_short`) came out too fast (17.9 letters/s) and less clear. **Rejected** (owner, 7 Nov 2026:
  "New voice a only looks good the clone is not good"): voice A stays the Kannada narrator. All three clones (owner,
  brother, Darshan) were judged worse than voice A by the owner's ear; don't offer clones again unless asked.
- **Hemanth clone (7 Nov 2026)**, asked for by the owner, consent confirmed. His recording is the cleanest so far
  (56 s, music 12 dB under him, real 0.25 s pauses between phrases). Reference `hemanth_v1` = 5.80-13.64 s, three
  complete sentences ("ನಾವು ಕಾರ್ ನೋಡಿದಾಗ..."). Turbo errors 5% mean / 11% worst (voice A: 5% / 18%), likeness 0.93,
  pitch movement 78 (= voice A), 11.5 letters/s. The 13.6 s reference (`hemanth_v2`) was less clear (16% / 28%).
  Lesson: a clean recording with pauses matters more than the tool. Waiting on the owner's ear.
- **Continuous narration in Hemanth's style** (owner, 7 Nov 2026: "I want you to copy same style continuity
  narration"): his reel has 0.23 s median pauses (longest 0.35 s) and wide pitch movement (96). Two changes copy it:
  (1) gaps between lines of 0.20 s (+ ~0.07 s kept edges) instead of GAP 0.36; (2) voicing three lines in one take,
  so the voice carries from sentence to sentence. On Kakudmi's first six lines both tools land on his pattern:
  median pause 0.24 s, pitch movement 93-95, likeness 0.92, turbo errors 6-11%; 32 s (IndicF5) / 35 s (OmniVoice)
  against voice A's 31 s. Line ends inside a multi-line take must be found again (pauses) for the visual cues.
- **OmniVoice** (k2-fsa, Apache-2.0, 2026; owner: "And try omni voice because it is latest", taken as the download
  approval for it alone): `tools/.venv-omni` (torch 2.14.1+cu126, omnivoice 0.2.1; model k2-fsa/OmniVoice, 3.1 GB in
  the Hugging Face cache), runner `omni_say.py` (JSON job on stdin, like f5_say.py). fp16 on the 4 GB GPU used
  2.7 GB. Its `generate()` also takes `language` and `instruct`. Kannada quality on par with IndicF5 here.
- Earlier, synthetic Kannada: `kn_voice_search.py` voices a two-sentence original passage with the model card's
  Kannada speakers (Suresh, Chetan, Anu, Vidya) x 4 seeds; `kn_voice_pick.py score` ranks them with Whisper medium
  (`language="kn"`) and pitch movement; `kn_voice_pick.py sample` voices a 15-20 s sample with IndicF5 from the best
  ones. The owner's ear decides, because Whisper is weak in Kannada. The pick becomes
  `myth_assets/voice/kn_refs/kn_narrator.wav` (channel.py).

## How to render (owner's laptop)
- Python: `<shorts research>/.venv-research/Scripts/python.exe -I -X utf8`.
- `channels/mythology/render_myth.py --video <story> --lang hi|kn|both`, with `--still T`, `--sheet 1.5`,
  `--check` (Whisper medium per line) and `--remix` (soundtrack only).
- `retake.py <story> <lang>` fixes misheard lines; `lively_retake.py <story> <lang>` keeps the liveliest clear take.
- Art and credits go in `<shorts research>/myth_assets/<story>/` with `credits.json`; renders and upload packs go in
  `<shorts research>/myth_out/` (`<story>_<lang>.mp4`, `<story>_<lang>_upload_sheet.md`, `upload_<story>/`).
- Masters: x264 crf 14, AAC 256k. The phone copy is a separate two-pass encode under 29 MB
  (`<shorts research>/channel_tools/phone_copy.py`).

## Video 4 and the "painted diorama" look (7 Nov 2026)
- Owner sent a reference reel (a Hindi Diwali-series reel, "Lakshmi has an elder sister") and said "make it like this";
  then chose "A new story" and "You, on the laptop" for the characters, and approved the script ("ok").
- `videos/bali.py` + `scenes_bali.py` + `diorama.py`: King Bali and Vamana (Bhagavata Purana 8.19-8.23, 5.17.1),
  timed for Bali Padyami. Painted characters generated once each with SDXL (`plates.py <video> --chars`, full-body
  prompt on a plain ground, cut out with BiRefNet-lite) and reused shot to shot; painted sets; the reference's paper
  devices (label row with FIG. n, torn tag, torn notes, calendar, checklist, target rings, dotted paths, paper clouds,
  fold lines). The warning beat uses a CC0 1700s Pahari painting of the scene (Cleveland Museum of Art 167578).
- Lessons: SDXL makes half-length portraits unless the prompt starts with "full body illustration of" and asks for
  feet and a plain ground; generated feet came out as a woman's adorned feet, and a code-drawn foot read as a boot, so
  the giant step reuses the Vamana cut-out at huge scale; reject any image with a sexualised goddess or wrong
  iconography; `plates.py` rewrites `credits.json`, so re-add museum credits after it runs.
- Windows treats `CUDA_VISIBLE_DEVICES=""` as unset; use `-1` to force the voice model onto the CPU.

## Status (6 Nov 2026, morning)
- Six reels finished: kakudmi (1:44 hi / 2:00 kn), brahma_calves (1:22 / 1:30), jarasandha (1:22 / 1:28), each with
  master, phone copy (< 29 MB), cover and upload pack in `myth_out/upload_<video>_<lang>/`, and on Drive under
  `My Drive/Mythology reels/`. Owner's summary: `myth_out/MORNING_REPORT.md`.
- Clarity: every line checked with Whisper large-v3-turbo (`kn_asr_check.py`, CPU): Kannada 0-19% letter errors,
  Hindi all under 33% except one line where turbo writes numbers as digits. Whisper medium is too weak in Kannada:
  use turbo for Kannada (`fix_line.py` re-voices one line and keeps the take turbo hears best).
- Lessons: IndicF5 drops or garbles very short staccato lines ("एक आँख। एक हाथ।"); commas work ("एक आंख, एक हाथ,
  एक पैर... और आधा चेहरा।"). SDXL drew pagodas for "heavenly court", so heaven is a lotus lake of light with no
  buildings; check every plate by eye. Real-ESRGAN ncnn picks the Intel GPU by default (use -g 1 for the NVIDIA).
- Waiting on the owner: channel names, Kannada voice (Suresh or Vidya), which look to make more of.
- 7 Nov 2026: all four Kannada reels re-voiced in voice A (`voice_all.py ... --langs kn --no-retake`, turbo check:
  every line 0-22% letter errors after `fix_line.py` re-took j5 and j15, whose first takes ended in a stray sound),
  re-rendered and finished: kakudmi 1:58, brahma_calves 1:28, jarasandha 1:27, bali 1:49; Drive packs replaced.
- 7 Nov 2026, later: Kannada scripts and captions rewritten with English only where needed (see the rule above),
  re-voiced (b18 and v15 re-taken), all 78 lines under 25% letter errors by turbo, re-rendered and finished again.
