# Voice takes for long videos rendered in another session

`dma_chNN_takes.tar` (one per chapter) holds every cached voice take that `channels/stories/dma_manga_chNN_long.py` uses (that chapter's
manga Shorts' takes, each already Whisper-checked in its Short): `build/clone_tts/*` (raw Turbo takes and their `.ok`
markers) and `build/tts/*` (the processed takes and their word timings), paths relative to the repo root.

    tar xf assets/voice_cache/dma_chNN_takes.tar      # from the repo root; then render as usual

With them in place the render reuses the same takes and never calls Chatterbox. Packed with the session's
export_takes.py (it records every file under build/ that the episode's timeline reads).
