"""Build an Interestingly Strange 3D video: voices -> timing.json -> 3D frames -> captions/cards/soundtrack -> MP4.

    python channels/is3d/make_is3d.py EPISODE                  -> out/EPISODE.mp4 (+ _preview.mp4, _metadata.md)
    python channels/is3d/make_is3d.py EPISODE --stills 1.0,5.2  (3D check frames only, in build/is3d/check)
    python channels/is3d/make_is3d.py EPISODE --reuse-frames    (redo captions/sound on existing frames)
Same engine as the low-poly channel (channels/lowpoly/make_skit.py, three.js in headless Chromium), with our own cast
and sets in scene_is3d.html. EPISODE is a module in channels/is3d; the narrator has no on-screen mouth, characters
(kid, bolt, teacher) get a mouth envelope from their voice.
"""
import importlib.util
import json
import os
import shutil
import subprocess
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)
os.chdir(ROOT)
import render   # noqa: E402
from render import narrator   # noqa: E402

HERE = os.path.join(ROOT, "channels", "is3d")
BUILD = os.path.join(ROOT, "build", "is3d")
CHARS = ("kid", "bolt", "teacher")
EPISODE = next(a for a in sys.argv[1:] if not a.startswith("--") and "," not in a)

spec = importlib.util.spec_from_file_location(f"videos.{EPISODE}", os.path.join(HERE, f"{EPISODE}.py"))
mod = importlib.util.module_from_spec(spec)
sys.modules[f"videos.{EPISODE}"] = mod      # so render.load() finds it like a normal video module
spec.loader.exec_module(mod)
render.load(EPISODE)
tl = render.timeline()

# timing.json: beats, word times and a mouth-opening envelope per character, sampled at the frame rate
fps, n = render.FPS, int(round(tl.total * render.FPS)) + 1
env = {who: np.zeros(n) for who in CHARS}
beats = []
for b in tl.beats:
    who = b.speaker if b.speaker in CHARS else "narrator"
    beats.append(dict(id=b.id, scene=b.scene, who=who, start=b.start, end=b.end,
                      words=[[u.start, u.end] for u in b.units]))
    if who == "narrator":
        continue
    a = np.asarray(b.audio, dtype=float)
    hop = narrator.SR / fps
    t0 = tl.at(b.id, b.speaker_from) if b.speaker_from else b.start
    for i in range(int(len(a) / hop)):
        f = int(round(b.start * fps)) + i
        if 0 <= f < n and f / fps >= t0:
            env[who][f] = max(env[who][f], float(np.sqrt(np.mean(a[int(i * hop):int((i + 1) * hop)] ** 2))))
for who, e in env.items():
    peak = np.percentile(e[e > 0], 95) if (e > 0).any() else 1.0
    env[who] = np.clip(e / peak, 0, 1).round(3).tolist()
os.makedirs(BUILD, exist_ok=True)
with open(os.path.join(BUILD, "timing.json"), "w") as f:
    json.dump(dict(total=tl.total, fps=fps, beats=beats, env=env), f)

frames = mod.FRAMES
stills = sys.argv[sys.argv.index("--stills") + 1] if "--stills" in sys.argv else None
os.environ["SCENE"] = f"scene_is3d.html?dir={mod.DIRECTION}"
if stills:
    out = os.path.join(BUILD, "check")
    shutil.rmtree(out, ignore_errors=True)
    subprocess.check_call(["node", os.path.join(HERE, "render.mjs"), out, str(fps), "1", stills])
    sys.exit(0)
if "--reuse-frames" not in sys.argv:     # caption/sound-only changes can skip the 3D render
    shutil.rmtree(frames, ignore_errors=True)
    subprocess.check_call(["node", os.path.join(HERE, "render.mjs"), frames, str(fps)])
render.render_video(os.path.join(ROOT, "out", f"{EPISODE}.mp4"))
