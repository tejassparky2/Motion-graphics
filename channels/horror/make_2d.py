"""Build a 2D (pycairo-drawn) horror episode: voices -> timeline -> frames -> sound -> MP4.

    python channels/horror/make_2d.py EPISODE                   -> out/horror/EPISODE.mp4 (+ _preview, _metadata)
    python channels/horror/make_2d.py EPISODE --stills 1.0,5.2   (check frames in build/horror/check2d)
Episodes live in channels/horror/ or channels/stories/ (outputs go to out/<that folder>/); an episode named *_long is
rendered 16:9 (1280x720).
Same voice settings and pauses as make_horror.py (the 3D episodes), so narration takes are shared.
"""
import importlib.util
import os
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)
os.chdir(ROOT)
os.environ.setdefault("CLONE_RATE", "5.0")
EPISODE = next(a for a in sys.argv[1:] if not a.startswith("--") and "," not in a and not a[0].isdigit())
if EPISODE.endswith("_long"):                      # long videos are 16:9 (owner, 27 Oct 2026); set before the engine loads
    os.environ["CANVAS"] = "landscape"
HOME = next(d for d in ("horror", "stories") if os.path.exists(os.path.join(ROOT, "channels", d, f"{EPISODE}.py")))
if HOME == "stories":                              # anime timing: 24 fps, drawings held on 2s (reports/CPU anime ...)
    os.environ.setdefault("FPS", "24")
import render   # noqa: E402
from motion import timeline   # noqa: E402

timeline.STOP_PAUSE, timeline.QUESTION_PAUSE, timeline.BEAT_GAP = 0.36, 0.45, 0.4
spec = importlib.util.spec_from_file_location(f"videos.{EPISODE}", os.path.join(ROOT, "channels", HOME, f"{EPISODE}.py"))
mod = importlib.util.module_from_spec(spec)
sys.modules[f"videos.{EPISODE}"] = mod
spec.loader.exec_module(mod)
render.load(EPISODE)
tl = render.timeline()
import json   # noqa: E402  (beat times for check.py)
os.makedirs(os.path.join(ROOT, "build", HOME), exist_ok=True)
with open(os.path.join(ROOT, "build", HOME, f"timing_{EPISODE}.json"), "w") as f:
    json.dump(dict(total=tl.total, beats=[dict(id=b.id, start=b.start, end=b.end) for b in tl.beats]), f)
if "--stills" in sys.argv:
    out = os.path.join(ROOT, "build", HOME, "check2d")
    shutil.rmtree(out, ignore_errors=True)
    os.makedirs(out)
    for t in sys.argv[sys.argv.index("--stills") + 1].split(","):
        render.render_still(float(t), os.path.join(out, f"t{float(t):06.2f}.png"))
    sys.exit(0)
os.makedirs(os.path.join(ROOT, "out", HOME), exist_ok=True)
render.render_video(os.path.join(ROOT, "out", HOME, f"{EPISODE}.mp4"))
