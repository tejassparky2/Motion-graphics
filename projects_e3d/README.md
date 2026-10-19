# Everything3D: videos (separate from Yours3D)

Started 19 Oct 2026 at the owner's request ("I wanna open a different chat for everything3d, voice will be completely
different, the user will record voice for clone"). This branch, `ccr-56282fe5-evehq4-everything3d`, and its own chat
are for Everything3D only. Yours3D reels stay on `ccr-56282fe5-evehq4-3d`, and the Interestingly Strange channel on
`ccr-56282fe5-evehq4`.

## Voice
- A **different voice** from Yours3D. The person who records it will supply their own recording for cloning.
- Clone only that person's voice, and only after they have said they agree to it being cloned (note who and when
  here). Never clone anyone else. Leave Chatterbox's watermark in place.
- Recording to ask for: 20-60 s of clean speech, one speaker, quiet room, phone held about 20 cm away, natural pace,
  WAV or the phone's original file (not a WhatsApp voice note). Save it as `assets/voice/e3d_prompt.wav` only if the
  speaker agrees to it being in this public repo; otherwise keep it out of git.
- `tools/voiceover.py --engine turbo` and `tools/turbo_clone_tts.py --prompt` can use a different prompt file.

## Still to learn from the owner
What Everything3D sells and to whom, brand name and look (logo, colours, fonts), call to action and contact,
prices/product facts, platform (Instagram Reels, YouTube Shorts, ...), and the first video's footage.

## Shared rules (same as the other projects)
- Workflow: look at the uploads, send the plan + script, wait for approval, then make it. Keep the owner's words;
  flag anything the voice may mishear.
- No metadata or encoder tags in outputs; keep other parties' watermarks.
- The repo is public: no customer photos, names or private data without consent; raw footage and finished videos stay
  out of git (`out/` folders that are ignored).
- Container setup: see NEXT_SESSION.md on `ccr-56282fe5-evehq4` (Python 3.12 venv for the pipeline; Python 3.11 venv
  with chatterbox-tts 0.1.7 for Turbo; add `setuptools<81` there or the watermarker fails to load; `av<16` for
  faster-whisper).
