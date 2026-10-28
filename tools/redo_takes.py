"""Throw away the cloned-voice takes for some sentences so the next render makes them again.

  python tools/redo_takes.py "The last bencher is back." "Sir, just one."
  python tools/redo_takes.py --episode dma_s2 --who momo "Rule one. The highest unique bid wins the key."
      (--episode loads that episode's voice settings and speakers first; --who picks the character's voice)
"""
import glob
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
args = sys.argv[1:]
episode = who = None
if "--episode" in args:
    i = args.index("--episode")
    episode = args[i + 1]
    del args[i:i + 2]
if "--who" in args:
    i = args.index("--who")
    who = args[i + 1]
    del args[i:i + 2]
if episode:                                       # the same setup make_2d.py does before a render
    if episode.endswith("_long"):
        os.environ["CANVAS"] = "landscape"
    os.environ.setdefault("CLONE_RATE", "5.0")
    os.chdir(ROOT)
    import importlib.util
    home = next(d for d in ("horror", "stories") if os.path.exists(os.path.join(ROOT, "channels", d, f"{episode}.py")))
    import render  # noqa: E402
    spec = importlib.util.spec_from_file_location(f"videos.{episode}", os.path.join(ROOT, "channels", home,
                                                                                    f"{episode}.py"))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[f"videos.{episode}"] = mod
    spec.loader.exec_module(mod)
    render.load(episode)
from motion import voice  # noqa: E402

for text in args:
    gone = [voice._clone_raw(text, who)]
    for pace in (1.0, 0.9):
        k = voice._key(text, pace, who)
        gone += glob.glob(os.path.join(voice.ROOT, "build", "tts", k + "*"))
    n = 0
    for p in gone:
        if os.path.exists(p):
            os.remove(p)
            n += 1
    print(f"redo ({n} files): {text}")
