"""Hindi reel 05 (Yours3D Hindi page): the English reel 05 edit (projects3d/reel05/build.py) with Sowmya's testimonial
dubbed into Hinglish in her own cloned voice. Owner (25 Oct 2026): "She can't talk hindi and she agrees to clone and
dub". Captions stay her real English words (owner's Hindi-page rule: voice Hinglish, text English). No on-screen
dub note (owner, 25 Oct 2026: she is the owner's business partner); the Instagram AI label is the owner's call.

  python projects3d/hindi/dub.py projects3d/hindi/reel05/dub.txt reel05 --voice sowmya --prompt PROMPT.wav
  python projects3d/hindi/reel05/build.py ARGS-OF-THE-ENGLISH-BUILD          # -> out/3d/hindi/reel05_hi.mp4
"""
import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location("reel05_build", os.path.join(HERE, "..", "..", "reel05", "build.py"))
en = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(en)
T = en.T


def main():
    segs = en.segments(*sys.argv[1:])
    dub = [os.path.join(T.ROOT, "out", "3d", "hindi", "dub", f"reel05_{k + 1:02d}.wav") for k in range(len(segs))]
    os.makedirs(os.path.join(T.ROOT, "out", "3d", "hindi"), exist_ok=True)
    T.build(os.path.join("hindi", "reel05_hi"), segs, en.TITLE, end_extra=getattr(en, "END_EXTRA", None), dub=dub)


if __name__ == "__main__":
    main()
