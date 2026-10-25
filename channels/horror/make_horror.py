"""Build an interactive 3D horror episode: voices -> timing.json -> 3D frames -> HUD/captions/sound -> MP4.

    python channels/horror/make_horror.py EPISODE                  -> out/horror/EPISODE.mp4 (+ _preview, _metadata)
    python channels/horror/make_horror.py EPISODE --voices          (voices + timing only)
    python channels/horror/make_horror.py EPISODE --stills 1.0,5.2  (3D check frames only, in build/horror/check)
    python channels/horror/make_horror.py EPISODE --reuse-frames    (redo HUD/captions/sound on existing frames)
Same pipeline as channels/is3d (three.js in headless Chromium, frames composited by render.py), with the horror sets
in scene_horror.html + sets/<SET>.js. EPISODE is a module in channels/horror; characters listed in its CHARS get a
mouth envelope from their voice.
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
os.environ.setdefault("CLONE_RATE", "5.0")   # a storyteller's pace for suspense (Interestingly Strange reads at 5.5)
import render   # noqa: E402
from motion import timeline   # noqa: E402
from render import narrator   # noqa: E402

# horror breathes: longer full stops and gaps between lines than the explainer channel (sentences stay separate takes)
timeline.STOP_PAUSE, timeline.QUESTION_PAUSE, timeline.BEAT_GAP = 0.36, 0.45, 0.4

HERE = os.path.join(ROOT, "channels", "horror")
BUILD = os.path.join(ROOT, "build", "horror")
EPISODE = next(a for a in sys.argv[1:] if not a.startswith("--") and "," not in a)

spec = importlib.util.spec_from_file_location(f"videos.{EPISODE}", os.path.join(HERE, f"{EPISODE}.py"))
mod = importlib.util.module_from_spec(spec)
sys.modules[f"videos.{EPISODE}"] = mod      # so render.load() finds it like a normal video module
spec.loader.exec_module(mod)
render.load(EPISODE)
tl = render.timeline()
if "--voices" in sys.argv:
    sys.exit(0)

# timing.json: beats, word times and a mouth-opening envelope per character, sampled at the frame rate
fps, n = render.FPS, int(round(tl.total * render.FPS)) + 1
env = {who: np.zeros(n) for who in mod.CHARS}
beats = []
for b in tl.beats:
    who = mod.MOUTH.get(b.speaker, b.speaker) if b.speaker else "narrator"
    beats.append(dict(id=b.id, scene=b.scene, who=who, start=b.start, end=b.end,
                      words=[[u.start, u.end] for u in b.units]))
    if who not in env:
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
timing = os.path.join(BUILD, f"timing_{EPISODE}.json")
with open(timing, "w") as f:
    json.dump(dict(total=tl.total, fps=fps, beats=beats, env=env), f)

frames = os.path.join(BUILD, f"{EPISODE}_frames")
mod.FRAMES = frames
stills = sys.argv[sys.argv.index("--stills") + 1] if "--stills" in sys.argv else None
os.environ["SCENE"] = f"scene_horror.html?set={mod.SET}&ep={EPISODE}"
os.environ["TIMING"] = timing
if stills:
    out = os.path.join(BUILD, "check")
    shutil.rmtree(out, ignore_errors=True)
    subprocess.check_call(["node", os.path.join(HERE, "render.mjs"), out, str(fps), "1", stills])
    if "--composite" in sys.argv:          # the same times with HUD and captions on top
        for name in sorted(os.listdir(out)):
            t = float(name[1:-4])
            render._tl.clear()
            render.render_still(t, os.path.join(out, f"c{name[1:]}"))
    sys.exit(0)
if "--reuse-frames" not in sys.argv:     # HUD/caption/sound-only changes can skip the 3D render
    shutil.rmtree(frames, ignore_errors=True)
    subprocess.check_call(["node", os.path.join(HERE, "render.mjs"), frames, str(fps)])
os.makedirs(os.path.join(ROOT, "out", "horror"), exist_ok=True)
render.render_video(os.path.join(ROOT, "out", "horror", f"{EPISODE}.mp4"))
