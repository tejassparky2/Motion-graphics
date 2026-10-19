"""Hindi reel 04 (Yours3D Hindi page): the English reel 04 edit (projects3d/reel04/build.py, unchanged) with the
owner's Hinglish voice-over. Owner (19 Oct 2026): "Not letters in hindi, only voice", then "voice also be hinglish,
text English" -- so the voice is Hinglish (script.txt, Devanagari so the Hindi model says the English words the
Indian way) and every caption is English (captions.txt, one line per voice paragraph); labels and the end card stay
as in the English reel.

  python tools/hindi_voiceover.py projects3d/hindi/reel04/script.txt hindi/reel04_hi
  python projects3d/hindi/reel04/build.py MEDIA_DIR          # -> out/3d/hindi/reel04_hi.mp4
"""
import importlib.util
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location("reel04_build", os.path.join(HERE, "..", "..", "reel04", "build.py"))
r4 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(r4)
v2, ROOT = r4.v2, r4.ROOT

CAPTIONS = [" ".join(p.split()) for p in open(os.path.join(HERE, "captions.txt"), encoding="utf-8").read().strip()
            .split("\n\n")]


def word_timings(wav, cues):
    """Per cue: the English caption's words [(word, start, end)], spread over the spoken line by length (the Hinglish
    voice and the English caption don't share word boundaries one to one)."""
    assert len(CAPTIONS) == len(cues), (len(CAPTIONS), len(cues))
    out = []
    for (c0, c1, _), txt in zip(cues, CAPTIONS):
        ws = txt.split()
        lens = np.cumsum([0] + [len(w) + 1 for w in ws])
        tt = c0 + (c1 - c0) * lens / lens[-1]
        out.append([(w, tt[i], tt[i + 1]) for i, w in enumerate(ws)])
    return out


_karaoke = v2.karaoke


def caption(frame, words, t, y=v2.CAP_Y, age=1.0):
    """The English sentence as a whole, no word-by-word highlight (it wouldn't follow the Hinglish speech)."""
    _karaoke(frame, words, -1.0, y, age)


r4.NAME = os.path.join("hindi", "reel04_hi")
v2.word_timings = word_timings
v2.karaoke = caption

if __name__ == "__main__":
    os.makedirs(os.path.join(ROOT, "out", "3d", "hindi"), exist_ok=True)
    r4.main()
