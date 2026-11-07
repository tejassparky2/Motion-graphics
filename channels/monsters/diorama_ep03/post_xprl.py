"""2D pass and final encode for XprL's Episode 3 shots (DIORAMA_EP03.md), over the Blender frames with comp.py:

    S08  the bells ringing: arcs pulsing out on both sides of Wren's hand bell and of every porch bell that rings,
         on 2s, over each bell's ring span (Ep 2's post_helper1.bell_rings, as helper 1's S09).
    S16  no overlay (the picture as rendered).
    S17  Kai's mark on his inner left forearm (helper 9's zigzag, lit, night-bright, a soft halo) and Ep 2's three
         thin scratch marks beside it (post_helper1.torn_sleeve), as helper 1's S09.

    FPS=24 python channels/monsters/diorama_ep03/post_xprl.py SHOT FRAMES_DIR        (-> shots/SHOT.mp4 + sheet)
    FPS=24 python channels/monsters/diorama_ep03/post_xprl.py SHOT --still F STILL.png OUT.png   (a preview)

FRAMES_DIR holds render_shot.py's 0001.png ...; the anchors come from build/monsters/diorama_ep03/<SHOT>_anchors.json
(written by diorama_ep03/xprl.py). No text. The mp4 is crf 10, bitexact, stream-copied, with no encoder tags.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

os.environ.setdefault("FPS", "24")
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
sys.path.insert(0, ROOT)

from PIL import Image  # noqa: E402

from motion.engine import FPS  # noqa: E402
from channels.monsters import comp  # noqa: E402
from channels.monsters.diorama_ep02 import post_helper1 as E2  # noqa: E402
from channels.monsters.diorama_ep03 import post_helper1 as H1  # noqa: E402

BUILD = os.path.join(ROOT, "build", "monsters", "diorama_ep03")
SHOTS_OUT = os.path.join(ROOT, "out", "monsters", "diorama_ep03", "shots")


def _load(shot):
    path = os.path.join(BUILD, f"{shot}_anchors.json")
    if not os.path.exists(path):
        return {}, {}
    with open(path) as fh:
        d = json.load(fh)
    return {int(k): v for k, v in d["frames"].items()}, d.get("spans", {})


def overlays(shot):
    a, spans = _load(shot)
    if shot == "S08":
        return [(E2.bell_rings, dict(start=(f0 - 1) / FPS, end=(f1 - 1) / FPS, a=a, name=nm))
                for nm, (f0, f1) in sorted(spans.items())]
    if shot == "S17":
        return [(H1.mark(a, 1.15, 2.2, halo=0.35), dict(start=0.0)), (E2.torn_sleeve, dict(start=0.0, a=a))]
    return []


def run(shot, frames_dir):
    src = comp.Source(frames_dir)
    out_frames = os.path.join(BUILD, f"{shot}_post")
    shutil.rmtree(out_frames, ignore_errors=True)
    rep = comp.render([comp.Shot(src, overlays=overlays(shot), name=shot)], out_frames, verbose=False)
    os.makedirs(SHOTS_OUT, exist_ok=True)
    mp4, tmp = os.path.join(SHOTS_OUT, f"{shot}.mp4"), os.path.join(BUILD, f"{shot}_enc.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "24", "-i",
                    os.path.join(out_frames, "%05d.png"), "-c:v", "libx264", "-crf", "10", "-preset", "slow",
                    "-pix_fmt", "yuv420p", *E2.CLEAN, tmp], check=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", tmp, "-c", "copy", *E2.CLEAN, "-movflags",
                    "+faststart", mp4], check=True)
    os.remove(tmp)
    E2.sheet(out_frames, rep["frames"], os.path.join(SHOTS_OUT, f"{shot}_sheet.jpg"))
    data = open(mp4, "rb").read()
    print(f"{shot}: {rep['frames']} frames -> {mp4}, tags",
          {s: data.count(s.encode()) for s in ("Lavf", "Lavc", "x264", "encoder")})


def still(shot, f, png, out):
    """Preview frame f: the overlays over one rendered still (scaled to 720x1280 if it is a half-scale still)."""
    tmp = tempfile.mkdtemp()
    im = Image.open(png).convert("RGB").resize((720, 1280))
    for i in range(1, f + 1):
        im.save(os.path.join(tmp, f"{i:04d}.png")) if i == f else os.symlink(os.path.join(tmp, f"{f:04d}.png"),
                                                                             os.path.join(tmp, f"{i:04d}.png"))
    o = tempfile.mkdtemp()
    comp.render([comp.Shot(comp.Source(tmp), overlays=overlays(shot), name=shot)], o, frames=(f - 1, f - 1),
                verbose=False, check=False)
    shutil.copy(os.path.join(o, f"{f:05d}.png"), out)
    shutil.rmtree(tmp)
    shutil.rmtree(o)


if __name__ == "__main__":
    args = sys.argv[1:]
    if "--still" in args:
        i = args.index("--still")
        still(args[0], int(args[i + 1]), args[i + 2], args[i + 3])
    else:
        run(args[0], args[1])
