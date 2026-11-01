"""2D pass for helper 1's Episode 2 shots (DIORAMA_EP02.md), over the Blender frames with comp.py:

    S02  speed lines streaming behind the diving bird (tapered streaks along its line of flight, re-dealt on 2s, from
         the moment it folds its wings), plus a few thin falling streaks across the frame for the plunge.
    S04  the talon rake: three white claw streaks slicing past his forearm on the hit, then the torn sleeve and three
         thin scratch marks on the arm (no blood), a wince accent and a sweat drop.
    S16  the bells ringing: little arcs pulsing out on both sides of each hand bell (on 2s).

    FPS=24 python channels/monsters/diorama_ep02/post_helper1.py S02 [S04 S16]       (the shot: mp4 + sheet)
    FPS=24 python channels/monsters/diorama_ep02/post_helper1.py S02 --still 20 STILL.png OUT.png   (a preview)

Reads build/monsters/diorama_ep02/<SHOT>/0001.png ... and <SHOT>_anchors.json (written by diorama_ep02/helper1.py).
No text.
"""
import json
import math
import os
import random
import shutil
import subprocess
import sys
import tempfile

os.environ.setdefault("FPS", "24")
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
sys.path.insert(0, ROOT)

from PIL import Image  # noqa: E402

from motion.engine import FPS, cairo  # noqa: E402
from channels.monsters import comp, fx2d_anime  # noqa: E402

BUILD = os.path.join(ROOT, "build", "monsters", "diorama_ep02")
SHOTS_OUT = os.path.join(ROOT, "out", "monsters", "diorama_ep02", "shots")
CLEAN = ["-map_metadata", "-1", "-map_chapters", "-1", "-fflags", "+bitexact", "-flags:v", "+bitexact",
         "-bsf:v", "filter_units=remove_types=6", "-metadata:s:v", "handler_name="]


def anchors(shot):
    with open(os.path.join(BUILD, f"{shot}_anchors.json")) as fh:
        return {int(k): v for k, v in json.load(fh).items()}


def frame_of(t):
    return int(round(t * FPS)) + 1


def at(a, f, name):
    f = min(max(1, f), max(a))
    return a[f][name]


def _streak(cr, x0, y0, x1, y1, w, col, alpha):
    """A tapered stroke: hair-thin at (x0, y0), `w` wide at (x1, y1)."""
    dx, dy = x1 - x0, y1 - y0
    L = math.hypot(dx, dy) or 1.0
    nx, ny = -dy / L, dx / L
    cr.move_to(x0, y0)
    cr.line_to(x1 + nx * w / 2, y1 + ny * w / 2)
    cr.line_to(x1 - nx * w / 2, y1 - ny * w / 2)
    cr.close_path()
    cr.set_source_rgba(*col, alpha)
    cr.fill()


# ------------------------------------------------------------------------------------------------------------ S02
def dive_lines(cr, t, start, a, end=None):
    """Streaks trailing the bird along its line of flight (from where it came), dealt again every 2 frames, longer
    and denser as it speeds up; a handful of thin falling streaks across the whole frame."""
    f = frame_of(t)
    if t < start or (end is not None and t > end):
        return
    f2 = f - f % 2
    bx, by, bz = at(a, f, "bird")
    px, py, _ = at(a, f - 4, "bird")
    dx, dy = bx - px, by - py
    sp = math.hypot(dx, dy)
    if sp < 1 or bz <= 0:
        return
    ux, uy = dx / sp, dy / sp
    nx, ny = -uy, ux
    k = min(1.0, (t - start) / 0.25)                            # they snap in over 6 frames
    r = random.Random(f2 * 13 + 1)
    length = min(520.0, 60 + sp * 5.5)
    for i in range(16):                                          # behind the bird, along its path
        off = r.gauss(0, 34)
        back = r.uniform(30, 90)
        Lr = length * r.uniform(0.5, 1.0)
        x1, y1 = bx - ux * back + nx * off, by - uy * back + ny * off
        x0, y0 = x1 - ux * Lr, y1 - uy * Lr
        _streak(cr, x0, y0, x1, y1, r.uniform(3, 9), (1, 1, 1), 0.85 * k)
    for i in range(10):                                          # the whole frame rushes: thin streaks, same angle
        x1, y1 = r.uniform(-40, 760), r.uniform(-40, 1320)
        Lr = r.uniform(120, 300)
        _streak(cr, x1 - ux * Lr, y1 - uy * Lr, x1, y1, r.uniform(1.5, 3.5), (1, 1, 1), 0.38 * k)


# ------------------------------------------------------------------------------------------------------------ S16
def bell_rings(cr, t, start, a, name, end=None, period=4):
    """Two or three short arcs pulsing out on both sides of a bell (the ring), on 2s; drawn only while the bell is in
    front of the camera."""
    if t < start or (end is not None and t > end):
        return
    f = frame_of(t)
    f2 = f - f % 2
    x, y, z = at(a, f2, name)
    if z <= 0:
        return
    for k in range(3):
        u = ((f2 / period + k / 3.0) % 1.0)
        rr = 16 + 30 * u
        al = 0.95 * (1 - u)
        for side in (-1, 1):
            cr.new_path()
            a0 = (0 if side > 0 else math.pi) - 0.75
            cr.arc(x, y, rr, a0, a0 + 1.5)
            cr.set_line_width(4.5 * (1 - 0.5 * u))
            cr.set_source_rgba(1, 0.96, 0.75, al)
            cr.stroke()


# ------------------------------------------------------------------------------------------------------------ S04
SKIN = (0.98, 0.84, 0.72)


def claw_slash(cr, t, start, a, dur=0.3, length=190.0):
    """Three white claw streaks slicing across his forearm along the bird's line of flight at the hit: they draw on
    in 2 frames, hold 2, then thin away."""
    u = (t - start) / dur
    if not 0 <= u <= 1:
        return
    f0 = frame_of(start)
    ex, ey, _ = at(a, f0 + 1, "elbow")
    wx, wy, _ = at(a, f0 + 1, "wrist")
    mx, my = (ex + wx) / 2, (ey + wy) / 2
    (bx0, by0, _), (bx1, by1, _) = at(a, f0 - 1, "bird"), at(a, f0 + 3, "bird")
    L = math.hypot(bx1 - bx0, by1 - by0) or 1.0
    ux, uy = (bx1 - bx0) / L, (by1 - by0) / L                    # the bird's direction on screen
    nx, ny = -uy, ux
    grow = min(1.0, u / 0.25)
    thin = 1.0 - max(0.0, (u - 0.5) / 0.5)
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    for i in (-1, 0, 1):
        cx, cy = mx + nx * i * 22, my + ny * i * 22
        x0, y0 = cx - ux * length / 2, cy - uy * length / 2
        x1, y1 = x0 + ux * length * grow, y0 + uy * length * grow
        cr.new_path()
        cr.move_to(x0, y0)
        cr.curve_to(x0 + (x1 - x0) * 0.35 + nx * 14, y0 + (y1 - y0) * 0.35 + ny * 14,
                    x0 + (x1 - x0) * 0.7 + nx * 14, y0 + (y1 - y0) * 0.7 + ny * 14, x1, y1)
        cr.set_line_width(16 * thin)
        cr.set_source_rgba(1, 1, 1, 0.35 * thin)
        cr.stroke_preserve()
        cr.set_line_width(5.5 * thin)
        cr.set_source_rgba(1, 1, 1, 0.97 * thin)
        cr.stroke()


def torn_sleeve(cr, t, start, a, band=(0.16, 0.6, 0.62)):
    """From the hit on: three thin pink scratch marks across his bare forearm (his sleeves are short) and a torn,
    frayed nick in the teal wristband beside them. Light, no blood. Tracks the forearm anchors frame by frame."""
    if t < start:
        return
    f = frame_of(t)
    ex, ey, ez = at(a, f, "elbow")
    wx, wy, wz = at(a, f, "wrist")
    if ez <= 0 or wz <= 0:
        return
    pop = min(1.0, (t - start) / 0.08)
    L = math.hypot(wx - ex, wy - ey) or 1.0
    ax, ay = (wx - ex) / L, (wy - ey) / L
    nx, ny = -ay, ax
    s = max(L, 40.0)                                              # (the forearm is foreshortened toward the lens)
    cx, cy = ex + (wx - ex) * 0.45, ey + (wy - ey) * 0.45
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    for i in (-1, 0, 1):                                         # three thin marks, diagonal to the arm
        mx, my = cx + ax * i * s * 0.16, cy + ay * i * s * 0.16
        h = s * 0.42 * pop
        x0, y0 = mx - nx * h - ax * h * 0.4, my - ny * h - ay * h * 0.4
        x1, y1 = mx + nx * h + ax * h * 0.4, my + ny * h + ay * h * 0.4
        cr.new_path()
        cr.move_to(x0, y0)
        cr.line_to(x1, y1)
        cr.set_line_width(4.5)
        cr.set_source_rgba(1.0, 0.93, 0.88, 0.8)                   # a pale weal round each...
        cr.stroke_preserve()
        cr.set_line_width(2.2)
        cr.set_source_rgba(0.86, 0.42, 0.45, 0.95)                 # ...thin pink line: a scratch, not a wound
        cr.stroke()
    bx, by = ex + (wx - ex) * 0.9, ey + (wy - ey) * 0.9           # the wristband: a frayed V-nick out of its edge
    r = random.Random(3)
    cr.new_path()
    cr.move_to(bx - nx * s * 0.2, by - ny * s * 0.2)
    for k in range(5):
        v = -0.2 + 0.1 * (k + 1)
        dep = s * (0.16 if k % 2 == 0 else 0.07) * pop + r.uniform(-1, 1)
        cr.line_to(bx + nx * s * v - ax * dep, by + ny * s * v - ay * dep)
    cr.close_path()
    cr.set_source_rgba(*SKIN, 1.0)
    cr.fill_preserve()
    cr.set_line_width(2.0)
    cr.set_source_rgba(band[0] * 0.6, band[1] * 0.6, band[2] * 0.6, 1.0)
    cr.stroke()


def tracked_face(fn, a):
    def draw(cr, t, start, **kw):
        f = frame_of(t)
        (lx, ly, _), (rx, ry, _) = at(a, f, "eye_l"), at(a, f, "eye_r")
        d = math.hypot(rx - lx, ry - ly)
        tilt = math.atan2(ry - ly, rx - lx)
        if abs(tilt) > math.pi / 2:
            tilt -= math.copysign(math.pi, tilt)
        fn(cr, t, start, x=(lx + rx) / 2, y=(ly + ry) / 2, size=d * 2.6, tilt=tilt, **kw)
    return draw


# ------------------------------------------------------------------------------------------------------------ shots
def overlays(shot):
    a = anchors(shot)
    meta = a.get(0, {}) if 0 in a else {}
    if shot == "S02":
        return [(dive_lines, dict(start=10 / FPS, a=a))]
    if shot == "S16":
        names = [k for k in a[1] if k.startswith("bell")]
        return [(bell_rings, dict(start=0.0, a=a, name=nm)) for nm in names]
    if shot == "S04":
        import re                                                # (helper1 needs bpy: read F_RAKE from its source)
        src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "helper1.py")).read()
        hit = (int(re.search(r"^F_RAKE = (\d+)", src, re.M).group(1)) - 1) / FPS
        return [(claw_slash, dict(start=hit - 1 / FPS, a=a)),
                (torn_sleeve, dict(start=hit + 1 / FPS, a=a)),
                (tracked_face(fx2d_anime.sweat_drop, a), dict(start=hit + 6 / FPS, end=99))]
    del meta
    return []


def sheet(frames_dir, n, path):
    ims = [Image.open(os.path.join(frames_dir, f"{f:05d}.png")).convert("RGB") for f in range(1, n + 1, 4)]
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
