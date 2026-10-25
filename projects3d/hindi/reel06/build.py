"""Hindi reel 06 (Yours3D Hindi page): the English reel 06 edit (projects3d/reel06/build.py) with Sowmya's testimonial
dubbed into Hinglish in her own cloned voice. Owner (25 Oct 2026): "She can't talk hindi and she agrees to clone and
dub". Captions stay her real English words (owner's Hindi-page rule: voice Hinglish, text English); a small
"Hindi dub · AI voice" note opens the reel, and the post gets Instagram's AI label (realistic AI audio).

  python projects3d/hindi/dub.py projects3d/hindi/reel06/dub.txt reel06 --voice sowmya --prompt PROMPT.wav
  python projects3d/hindi/reel06/build.py ARGS-OF-THE-ENGLISH-BUILD          # -> out/3d/hindi/reel06_hi.mp4
"""
import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location("reel06_build", os.path.join(HERE, "..", "..", "reel06", "build.py"))
en = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(en)
T = en.T


def main():
    segs = en.segments(*sys.argv[1:])
    dub = [os.path.join(T.ROOT, "out", "3d", "hindi", "dub", f"reel06_{k + 1:02d}.wav") for k in range(len(segs))]
    os.makedirs(os.path.join(T.ROOT, "out", "3d", "hindi"), exist_ok=True)
    T.build(os.path.join("hindi", "reel06_hi"), segs, en.TITLE, end_extra=getattr(en, "END_EXTRA", None), dub=dub,
            label="HINDI DUB  ·  AI VOICE")


if __name__ == "__main__":
    main()
