"""2D pass for helper 1's v3 shots (DIORAMA_EP01_V3.md), over the Blender frames with comp.py:

    S08a "And I was standing in it."  From f24 (his face drops): the anime sweat drop beside his head and the blue
         vertical gloom lines over his forehead; from f4, tiny electric arcs fizzing at the power strip's plugs (on
         1s, the cable to his feet in the same frame).

    FPS=24 python channels/monsters/diorama_v3/post_helper1.py S08a            (the shot: mp4 + sheet)
    FPS=24 python channels/monsters/diorama_v3/post_helper1.py S08a --still 30 STILL.png OUT.png   (a preview)

Reads build/monsters/diorama_v3/<SHOT>/0001.png ... and <SHOT>_anchors.json (written by diorama_v3/helper1.py). Needs
pycairo, numpy, scipy, pillow (fx2d) and ffmpeg. No text.
"""
import json
import math
import os
import shutil
import subprocess
import sys
import tempfile

os.environ.setdefault("FPS", "24")
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
sys.path.insert(0, ROOT)

from PIL import Image  # noqa: E402

from motion.engine import FPS, cairo  # noqa: E402
from channels.monsters import comp, fx2d, fx2d_anime  # noqa: E402

BUILD = os.path.join(ROOT, "build", "monsters", "diorama_v3")
SHOTS_OUT = os.path.join(ROOT, "out", "monsters", "diorama_v3", "shots")
CLEAN = ["-map_metadata", "-1", "-map_chapters", "-1", "-fflags", "+bitexact", "-flags:v", "+bitexact",
         "-bsf:v", "filter_units=remove_types=6", "-metadata:s:v", "handler_name="]
DROP = 24                                   # S08a: his face drops (FEAR_STAND from f20, the fear face settled by 24)


def anchors(shot):
    with open(os.path.join(BUILD, f"{shot}_anchors.json")) as fh:
        return {int(k): v for k, v in json.load(fh).items()}


def at(a, t, name):
    f = min(max(1, int(round(t * FPS)) + 1), max(a))
    return a[f][name]


def tracked(fn, a, keys):
    """Wrap an overlay so its x, y (and size, tilt) follow the face anchors frame by frame (the camera moves)."""
    def draw(cr, t, start, **kw):
        (lx, ly), (rx, ry) = at(a, t, "eye_l"), at(a, t, "eye_r")
        d = math.hypot(rx - lx, ry - ly)
        tilt = math.atan2(ry - ly, rx - lx)
        if abs(tilt) > math.pi / 2:
            tilt -= math.copysign(math.pi, tilt)
        fn(cr, t, start, x=(lx + rx) / 2, y=(ly + ry) / 2, size=d * 2.6, tilt=tilt, **kw)
    return draw


def gloom_lines(cr, t, start, x, y, size, tilt=0.0, end=None):
    """The anime blue vertical lines of shock hanging over the forehead (fx2d_anime.terror_eyes' shade, on its own)."""
    if t < start or (end is not None and t > end):
        return
    u = min(1.0, (t - start) / 0.15)                        # they drop in over ~4 frames
    cr.save()
    cr.translate(x, y)
    cr.rotate(tilt)
    size *= 1.5                                             # over the whole forehead
    top, bot = -0.2 * size, 0.0                           # from under the brim down to his eyes
    g = cairo.LinearGradient(0, top, 0, bot)
    g.add_color_stop_rgba(0, 0.1, 0.18, 0.55, 0.9)
    g.add_color_stop_rgba(1, 0.12, 0.2, 0.55, 0)
    cr.set_source(g)
    for i in range(11):
        xx = (-0.42 + 0.084 * i) * size
        cr.rectangle(xx, top, max(2.5, 0.025 * size), (bot - top) * u * (0.75 + 0.25 * ((i * 7) % 3) / 2))
    cr.fill()
    cr.restore()


def fizz(cr, t, start, a, end=None):
    """Tiny arcs crackling at the plugs (the anchor "plug"), on 1s: two short bolts off the strip, a flicker."""
    px, py = at(a, t, "plug")
    for j, (dx, dy) in enumerate(((-26, -22), (22, -30), (-8, -36))):
        fx2d.electric_arcs(cr, t, start, end, path=((px, py), (px + dx, py + dy)), n=1, width=1.6, branches=1,
                           rough=0.35, flicker=0.45, glow=True, sound=False, seed=11 + j)


def overlays(shot):
    a = anchors(shot)
    if shot == "S08a":
        return [(fizz, dict(start=3 / FPS, a=a)),
                (tracked(gloom_lines, a, ()), dict(start=(DROP - 1) / FPS)),
                (tracked(fx2d_anime.sweat_drop, a, ()), dict(start=(DROP + 1) / FPS, end=99))]
    return []


def sheet(frames_dir, n, path):
    ims = [Image.open(os.path.join(frames_dir, f"{f:05d}.png")).convert("RGB") for f in range(1, n + 1, 6)]
    w, h = ims[0].size[0] // 3, ims[0].size[1] // 3
    cols = min(len(ims), 6)
    out = Image.new("RGB", (w * cols, h * (-(-len(ims) // cols))), "white")
    for i, im in enumerate(ims):
        out.paste(im.resize((w, h)), ((i % cols) * w, (i // cols) * h))
    out.save(path, quality=88)


def run(shot):
    src = comp.Source(os.path.join(BUILD, shot))
    out_frames = os.path.join(BUILD, f"{shot}_post")
    rep = comp.render([comp.Shot(src, overlays=overlays(shot), name=shot)], out_frames, verbose=False)
    os.makedirs(SHOTS_OUT, exist_ok=True)
    mp4, tmp = os.path.join(SHOTS_OUT, f"{shot}.mp4"), os.path.join(BUILD, f"{shot}_enc.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "24", "-i",
                    os.path.join(out_frames, "%05d.png"), "-c:v", "libx264", "-crf", "10", "-preset", "slow",
                    "-pix_fmt", "yuv420p", *CLEAN, tmp], check=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", tmp, "-c", "copy", *CLEAN, "-movflags", "+faststart",
                    mp4], check=True)
    os.remove(tmp)
    sheet(out_frames, rep["frames"], os.path.join(SHOTS_OUT, f"{shot}_sheet.jpg"))
    data = open(mp4, "rb").read()
    print(f"{shot}: {rep['frames']} frames -> {mp4}, tags",
          {s: data.count(s.encode()) for s in ("Lavf", "Lavc", "x264", "encoder")})


def still(shot, f, png, out):
    """Preview frame f: the overlays over one rendered still (scaled up to 720x1280 if it is a half-scale still)."""
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
    if "--still" in sys.argv:
        i = sys.argv.index("--still")
        still(sys.argv[1], int(sys.argv[i + 1]), sys.argv[i + 2], sys.argv[i + 3])
    else:
        for s in sys.argv[1:]:
            run(s)
