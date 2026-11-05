# Indian mythology channel: 2D-animated story reels in Hindi and Kannada

Started 6 Nov 2026 from the Socho with Tejas chat. Owner: "I want to make high quality 2d animation indian mythology
reels in hindi and kannada for hindi the voice you already have and we try to make kannada ... this is for different
chat". This channel has its own chat and its own branch, `ccr-56282fe5-evehq4-mythology`, in its own worktree
(`<shorts research>/Motion-graphics-myth`). Don't switch the branch of the shared `Motion-graphics` checkout.

**Owner decisions, still open:** channel name(s); Kannada voice (Suresh in use, Vidya the alternative). See Status.

## Owner instructions, 6 Nov 2026 (night)
- "make me three 60 seconds or more videos all 3 with different approach animation scene etc in both kannada and
  hindi ... i want all videos ready till morning"; "3 videos with different approach different hook different
  animation". Built without script approval because the owner asked for them ready by morning.
- Kannada: "normal everyday speaking kannada kanglish and standard kannada only city peoples taking kannada":
  Bengaluru-style spoken Kannada with common English words, written in Kannada script (ಟೈಮ್, ಸ್ಟೋರಿ, ಶಾಕ್).
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
- **No voice cloning.** Never the owner's cloned voice, never any real person's voice (no famous narrator, no
  TV-serial voice). Synthetic voices from Indic Parler-TTS named speakers only, spoken by IndicF5.
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
- **Kannada: being chosen.** `kn_voice_search.py` voices a two-sentence original passage with the model card's
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

## Status (6 Nov 2026)
- Scaffold made: channel settings, narration, renderer, retakes and the Kannada voice search, all language-aware.
- Waiting on the owner: art route, channel name(s), first story, Kannada voice.
