"""Render one shot (or a frame range of it), so the final render can be split across sessions.

    blender -b -P channels/monsters/render_shot.py -- EPISODE SHOT OUT_DIR [--frames A-B] [--scale 0.5] [--subject]
                                                       [--samples 16] [--still N]

The shot builders live in channels/monsters/<EPISODE>/shots.py: SHOTS[SHOT]() builds the scene and returns
dict(frames=N, step=1|2|3, subject=[roots]). Frames are written as OUT_DIR/0001.png...; with --subject the character-only RGBA
pass goes to OUT_DIR/subject/. --still N renders one frame to OUT_DIR/still_N.png for checking."""
import importlib  # noqa: I001
import os
import sys
import time

import bpy

sys.path.insert(0, "/home/user/Motion-graphics")
from channels.monsters.mk import look  # noqa: E402

argv = sys.argv[sys.argv.index("--") + 1:]
ep, shot, out = argv[0], argv[1], argv[2]
opt, rest = {}, argv[3:]
while rest:
    if rest[0] == "--subject":
        opt["--subject"], rest = True, rest[1:]
    else:
        opt[rest[0]], rest = rest[1], rest[2:]
scale = float(opt.get("--scale", 1.0))
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = look.render_setup(int(720 * scale), int(1280 * scale), int(opt.get("--samples", 16)))
mod = importlib.import_module(f"channels.monsters.{ep}.shots")
info = mod.SHOTS[shot]()
n = info["frames"]
sc.frame_start, sc.frame_end = 1, n
os.makedirs(out, exist_ok=True)
if "--still" in opt:
    frames = [int(opt["--still"])]
elif "--frames" in opt:
    a, b = opt["--frames"].split("-")
    frames = list(range(int(a), int(b) + 1))
else:
    frames = list(range(1, n + 1))


step = int(info.get("step", 1))


def render(frames, folder, still=False):
    """With step > 1 (locked camera, characters on 2s/3s, no 1s effects) only every step-th frame is rendered; the
    frames in between are copies (TP13: render only frames that change)."""
    import shutil
    last = None
    for f in frames:
        if not still and step > 1 and last is not None and f % step != 0:
            shutil.copyfile(last, os.path.join(folder, f"{f:04d}.png"))
            continue
        sc.frame_set(f)
        sc.render.filepath = os.path.join(folder, f"still_{f}.png" if still else f"{f:04d}.png")
        t = time.time()
        bpy.ops.render.render(write_still=True)
        last = sc.render.filepath
        print(f"FRAME {f} {time.time() - t:.1f}s", flush=True)


render(frames, out, "--still" in opt)
if opt.get("--subject") and info.get("subject"):
    look.subject_only(info["subject"])
    render(frames, os.path.join(out, "subject"), "--still" in opt)
