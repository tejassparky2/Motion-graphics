"""Build a low-poly skit: voices -> timing.json -> 3D frames -> captions/cards/soundtrack -> MP4.

    python channels/lowpoly/make_skit.py [EPISODE]          -> out/lowpoly/EPISODE.mp4 (+ _preview.mp4)
    python channels/lowpoly/make_skit.py [EPISODE] --stills 1.0,5.2   (3D check frames only)
    python channels/lowpoly/make_skit.py [EPISODE] --reuse-frames     (redo captions/sound on existing frames)
EPISODE is a module in channels/lowpoly (default skit_test); its DIRECTION names directions/<DIRECTION>.js.
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

HERE = os.path.join(ROOT, "channels", "lowpoly")
BUILD = os.path.join(ROOT, "build", "lowpoly")
EPISODE = next((a for a in sys.argv[1:] if not a.startswith("--") and "," not in a), "skit_test")
NAME = f"lp_{EPISODE}"

spec = importlib.util.spec_from_file_location(f"videos.{NAME}", os.path.join(HERE, f"{EPISODE}.py"))
mod = importlib.util.module_from_spec(spec)
sys.modules[f"videos.{NAME}"] = mod      # so render.load() finds it like a normal video module
spec.loader.exec_module(mod)
render.load(NAME)
tl = render.timeline()

# timing.json: beats, word times and a mouth-opening envelope per character, sampled at the frame rate
fps, n = render.FPS, int(round(tl.total * render.FPS)) + 1
env = {who: np.zeros(n) for who in ("dev", "claude", "codex", "dad", "junior", "vo", "mom", "kid")}   # "vo": Dev's inner voice (mouth shut)
beats = []
for b in tl.beats:
    who = {"claude2": "claude", "vo": "vo"}.get(b.speaker, b.speaker) or "dev"   # claude2: a new Claude version, same body
    beats.append(dict(id=b.id, scene=b.scene, who=who, start=b.start, end=b.end,
                      words=[[u.start, u.end] for u in b.units]))
    a = np.asarray(b.audio, dtype=float)
    hop = narrator.SR / fps
    for i in range(int(len(a) / hop)):
        f = int(round(b.start * fps)) + i
        if 0 <= f < n:
            env[who][f] = max(env[who][f], float(np.sqrt(np.mean(a[int(i * hop):int((i + 1) * hop)] ** 2))))
for who, e in env.items():
    peak = np.percentile(e[e > 0], 95) if (e > 0).any() else 1.0
    env[who] = np.clip(e / peak, 0, 1).round(3).tolist()
os.makedirs(BUILD, exist_ok=True)
for name in ("timing.json", f"timing_{EPISODE}.json"):     # per-episode copy so two episodes can run at once
    with open(os.path.join(BUILD, name), "w") as f:
        json.dump(dict(total=tl.total, fps=fps, beats=beats, env=env), f)
os.environ["TIMING"] = os.path.join(BUILD, f"timing_{EPISODE}.json")

frames = mod.FRAMES
stills = sys.argv[sys.argv.index("--stills") + 1] if "--stills" in sys.argv else None
os.environ["SCENE"] = f"scene_skit.html?dir={getattr(mod, 'DIRECTION', 'test')}"
if stills:
    out = os.path.join(BUILD, "skit_check")
    shutil.rmtree(out, ignore_errors=True)
    subprocess.check_call(["node", os.path.join(HERE, "render.mjs"), out, str(fps), "1", stills])
    sys.exit(0)
if "--reuse-frames" not in sys.argv:     # caption/sound-only changes can skip the 3D render
    shutil.rmtree(frames, ignore_errors=True)
    subprocess.check_call(["node", os.path.join(HERE, "render.mjs"), frames, str(fps)])
out = os.path.join(ROOT, "out", "lowpoly", f"{EPISODE}.mp4")
render.render_video(out)
