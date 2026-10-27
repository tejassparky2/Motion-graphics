"""Speak sentences in the channel owner's own cloned voice (Chatterbox, MIT licence). Runs in the separate clone
virtualenv (torch); motion/voice.py calls it once per render with every sentence that isn't cached yet.

  /home/user/.venv-clone/bin/python tools/clone_tts.py jobs.json
  jobs.json: [["text", "out.wav"], ...]   ->   24 kHz mono wavs, start/end silence trimmed gently
  With CLONE_MODEL=turbo a job can add a third item, a reference wav (a character's synthetic Kokoro voice) whose
  timbre Turbo takes; without it Turbo uses its own stock voice. Turbo voices tags like [chuckle] in the text.

Chatterbox's Perth watermark is left in place.
"""
import json
import os
import sys

import numpy as np
import soundfile as sf
from chatterbox.tts import ChatterboxTTS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# The owner's clip sped up x1.2: the clone copies the prompt's pace, and this lands it near Teacher Bluffed's
# 5.2 syllables/s instead of ~3.2 (tested: 4.9 median, clearer and more even than the plain prompt).
PROMPT = os.path.join(ROOT, "assets", "voice", "owner_prompt_fast.wav")
EXAGGERATION, CFG = 0.6, 0.6     # cfg 0.6 follows the text more closely: better pronunciation


def trim(w, sr):
    """Gentle trim: keeps soft first consonants ("Put" was clipped to "could" by a harder trim)."""
    env = np.convolve(np.abs(w), np.ones(int(sr * 0.01)) / (sr * 0.01), mode="same")
    loud = np.nonzero(env > 0.004)[0]
    if not len(loud):
        return w
    return w[max(0, loud[0] - int(0.09 * sr)): loud[-1] + int(0.06 * sr)]


def stock_voice(jobs):
    """CLONE_MODEL=stock: Chatterbox's full model with its own built-in stock voice (no prompt; nobody is cloned).
    The doctor channel's explainer voice from 27 Oct 2026 (clearest and most expressive of the voices tested)."""
    if any(len(j) > 2 for j in jobs):
        sys.exit("clone_tts: the stock voice takes no reference voices")
    model = ChatterboxTTS.from_pretrained(device="cpu")      # its default conditionals = the stock voice
    for k, (text, out) in enumerate(jobs, 1):
        w = model.generate(text, exaggeration=STOCK_EXAGGERATION, cfg_weight=STOCK_CFG)[0].numpy()
        os.makedirs(os.path.dirname(out), exist_ok=True)
        sf.write(out + ".tmp.wav", trim(w, model.sr), model.sr)
        os.replace(out + ".tmp.wav", out)
        print(f"clone voice {k}/{len(jobs)}: {text}", file=sys.stderr, flush=True)


STOCK_EXAGGERATION, STOCK_CFG = 0.5, 0.5     # tested 27 Oct: 98.4% Whisper medium confidence under the music


def main():
    jobs = json.load(open(sys.argv[1]))
    if os.environ.get("CLONE_MODEL") == "stock":
        return stock_voice(jobs)
    turbo = os.environ.get("CLONE_MODEL") == "turbo"     # Chatterbox Turbo's stock voice, no prompt (not a clone)
    if turbo:
        from chatterbox.tts_turbo import ChatterboxTurboTTS
        model = ChatterboxTurboTTS.from_pretrained(device="cpu")
    else:
        model = ChatterboxTTS.from_pretrained(device="cpu")
        model.prepare_conditionals(PROMPT, exaggeration=EXAGGERATION)
    stock = model.conds if turbo else None
    if not turbo and os.environ.get("ALLOW_OWNER_CLONE") != "1":
        # owner, 15 Oct 2026: "I don't want videos in my cloned voice" / "Don't use my cloned voice"
        sys.exit("clone_tts: the owner's cloned voice is switched off (owner, 15 Oct 2026). Use CLONE_MODEL=turbo, "
                 "or set ALLOW_OWNER_CLONE=1 only if the owner asks for it again.")
    if not turbo and any(len(j) > 2 for j in jobs):
        sys.exit("clone_tts: jobs carry Turbo reference voices but CLONE_MODEL is not 'turbo'; refusing to voice them "
                 "in the owner's cloned voice")
    for k, (text, out, *ref) in enumerate(jobs, 1):
        if turbo:
            if ref:
                model.prepare_conditionals(ref[0])
            else:
                model.conds = stock
            w = model.generate(text)[0].numpy()
        else:
            w = model.generate(text, exaggeration=EXAGGERATION, cfg_weight=CFG)[0].numpy()
        os.makedirs(os.path.dirname(out), exist_ok=True)
        sf.write(out + ".tmp.wav", trim(w, model.sr), model.sr)
        os.replace(out + ".tmp.wav", out)
        print(f"clone voice {k}/{len(jobs)}: {text}", file=sys.stderr, flush=True)


if __name__ == "__main__":
    main()
