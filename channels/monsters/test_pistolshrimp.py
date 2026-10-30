"""The pistol shrimp's Episode 1 shots (EP01_SHOTS.md): S04a, S04b, S05a, S05b, S06, S08.

Stills (one key frame per shot, plus the S08 subject pass), into OUTDIR/pistolshrimp_<shot>.png:
    blender -b -P channels/monsters/test_pistolshrimp.py -- OUTDIR [W H SAMPLES] [S04a,S05b,...]
All frames of one shot (OUTDIR/<shot>/0001.png ...; S08 also OUTDIR/S08/subject/0001.png ...):
    blender -b -P channels/monsters/test_pistolshrimp.py -- OUTDIR W H SAMPLES S05b --frames"""
import os
import sys
import time

import bpy

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from channels.monsters.mk import pistolshrimp as ps  # noqa: E402

argv = sys.argv[sys.argv.index("--") + 1:]
out = argv[0]
W, H, S = (int(argv[1]), int(argv[2]), int(argv[3])) if len(argv) > 3 else (720, 1280, 16)
shots = argv[4].split(",") if len(argv) > 4 else list(ps.LENGTHS)
frames_mode = "--frames" in argv
KEY = dict(S04a=12, S04b=58, S05a=27, S05b=52, S06=118, S08=6)   # the still for each shot (sequence frame)
os.makedirs(out, exist_ok=True)


def render(path):
    sc = bpy.context.scene
    sc.render.filepath = path
    t0 = time.time()
    bpy.ops.render.render(write_still=True)
    return time.time() - t0


for sid in shots:
    info = ps.shot(sid, W, H, S)
    sc = info["scene"]
    f0, f1 = info["frames"]
    if frames_mode:
        passes = [("", False)] + ([("subject", True)] if sid in ps.SUBJECT_PASS else [])
        for sub, subject in passes:
            if subject:
                ps.subject_pass(info)
            d = os.path.join(out, sid, sub)
            os.makedirs(d, exist_ok=True)
            for fr in range(f0, f1 + 1):
                sc.frame_set(fr)
                path = os.path.join(d, "%04d.png" % (fr - f0 + 1))
                if os.path.exists(path):
                    continue
                print("RENDER_SECONDS %s%s %d: %.1f" % (sid, "/" + sub if sub else "", fr, render(path)), flush=True)
        continue
    sc.frame_set(KEY[sid])
    print("RENDER_SECONDS %s frame %d: %.1f" % (sid, KEY[sid], render(os.path.join(out, f"pistolshrimp_{sid}.png"))),
          flush=True)
    if sid in ps.SUBJECT_PASS:
        ps.subject_pass(info)
        sc.frame_set(KEY[sid])
        print("RENDER_SECONDS %s subject frame %d: %.1f" % (sid, KEY[sid], render(
            os.path.join(out, f"pistolshrimp_{sid}_subject.png"))), flush=True)
