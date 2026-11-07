"""2D pass for helper 3's Episode 3 shots (DIORAMA_EP03.md), over the Blender frames, from
build/monsters/diorama_ep03/<SHOT>_anchors.json (written by diorama_ep03/helper3.py):

    S02  A: the mark glowing on Kai's raised forearm (soft, in the foreground). B: the crack in the sky (helper 3's rift
         look, as in Ep 2 S15). C: the mark upright on his arm and the crack above him; at f_echo a coral echo of the
         zigzag rises from the mark and lands on the crack (the same shape, eased in size and tilt), then both pulse
         together: the match.

The zigzag is the Ep 1 crack (helper 9's post_helper9.crack()), the mark drawn by post_helper9.mark().

    /home/user/tools/postenv/bin/python channels/monsters/diorama_ep03/post_helper3.py S02            # mp4 + sheet
    /home/user/tools/postenv/bin/python channels/monsters/diorama_ep03/post_helper3.py S02 --still 52  # one frame

Reads build/monsters/diorama_ep03/<SHOT>/0001.png ... (render_shot.py's OUT_DIR, or H3_SRC), filling frames rendered
elsewhere from out/monsters/diorama_ep03/parts/<SHOT>_fAAA-BBB.mp4; writes <SHOT>_post/ and
out/monsters/diorama_ep03/shots/<SHOT>.mp4 (crf 10, bitexact, stream-copy remux, no encoder strings) + <SHOT>_sheet.jpg.
"""
import glob
import json
import math
import os
import re
import shutil
import subprocess
import sys

import numpy as np

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
sys.path.insert(0, ROOT)

from motion.engine import cairo  # noqa: E402
from channels.monsters import fx2d  # noqa: E402
from channels.monsters.diorama_ep02 import post_helper9 as P9  # noqa: E402
from channels.monsters.diorama_v3 import helper3_fx as h3fx  # noqa: E402

BUILD = os.path.join(ROOT, "build", "monsters", "diorama_ep03")
SHOTS_OUT = os.path.join(ROOT, "out", "monsters", "diorama_ep03", "shots")
PARTS = os.path.join(ROOT, "out", "monsters", "diorama_ep03", "parts")
CLEAN = P9.CLEAN
ECHO = 9                                   # frames for the echo to rise from the mark to the crack
SKY_KEY = (183, 219, 244)                  # the flat colour the compositor's haze makes of the 3D sky (RGB)
# the evening sky by elevation (deg): peach low, rose, lilac, deeper blue up top (S04's sunset is the next line)
SKY_STOPS = ((0, (255, 192, 142)), (7, (250, 168, 128)), (18, (226, 158, 166)), (32, (160, 146, 200)),
             (52, (92, 112, 192)), (80, (54, 74, 152)))


def anchors(shot, still=False):
    name = f"{shot}_anchors_still.json" if still and os.path.exists(os.path.join(BUILD, f"{shot}_anchors_still.json")) \
        else f"{shot}_anchors.json"
    with open(os.path.join(BUILD, name)) as fh:
        a = json.load(fh)
    return a["meta"], {int(f): v for f, v in a["frames"].items()}


def _rift(cr, A, f, f_open, k):
    spark = dict(rift={str(g): v.get("rift") for g, v in A.items()}, crack_on=[-30, -25], f_in=f_open,
                 crack=P9.crack())
    h3fx.rift(cr, spark, f, k)


def _outline(cr, geo, k, col, a, width):
    line = P9._pts(geo, k, 0.5)
    if len(line) < 2:
        return
    cr.save()
    cr.set_line_join(cairo.LINE_JOIN_ROUND)
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    for wdt, aa in ((width * 4, 0.18), (width * 2, 0.4), (width, 1.0)):
        cr.new_path()
        cr.move_to(line[0][0], line[0][1])
        for x, y, _ in line[1:]:
            cr.line_to(x, y)
        cr.set_source_rgba(*col, a * aa)
        cr.set_line_width(wdt)
        cr.stroke()
    cr.restore()


def s02(cr, f, meta, A, k):
    fb, fc, fe = meta["fb"], meta["fc"], meta["f_echo"]
    g = A[f]
    lvl = g.get("level", 1.0)
    if f < fb:                                                   # A: the mark on his raised forearm, foreground
        if g.get("mark") and g["mark"]["z"] > 0:
            P9.mark(cr, P9._on_arm(g["mark"]), k, 0.5, lvl, f, bold=1.2)
        return
    if f < fc:                                                   # B: the crack in the sky
        _rift(cr, A, f, fb - 14, k)
        if f == fb:
            r = g.get("rift")
            if r:
                fx2d._glow(cr, r["c"][0] * k, r["c"][1] * k, math.hypot(*r["ey"]) * k * 0.9, h3fx.GLOW, 0.35)
        return
    # C: the crack above him, the mark on his arm; the echo; then both pulse together
    _rift(cr, A, f, fb - 14, k)
    land = fe + ECHO
    pulse = max(0.0, 1 - abs(f - land) / 6)
    if g.get("mark") and g["mark"]["z"] > 0:
        P9.mark(cr, P9._on_arm(g["mark"]), k, 0.5, lvl + 0.35 * pulse, f, bold=2.2)
    r = g.get("rift")
    if r and pulse > 0:
        fx2d._glow(cr, r["c"][0] * k, r["c"][1] * k, math.hypot(*r["ey"]) * k * 0.8, P9.CORAL_HOT, 0.35 * pulse)
    if fe <= f <= land + 2 and g.get("mark") and r:
        u = min(1.0, (f - fe) / ECHO)
        e = u * u * (3 - 2 * u)
        geo = P9._lerp_geo(P9._on_arm(g["mark"]), r, e)
        _outline(cr, geo, k, P9.CORAL_HOT, (1 - 0.35 * e) if f <= land else 0.6 * (land + 2 - f) / 2,
                 4.5 * k)
        fx2d._glow(cr, geo["c"][0] * k, geo["c"][1] * k, math.hypot(*geo["ey"]) * k * 0.5, P9.CORAL, 0.25)


DRAW = {"S02": s02}


def _sky_rows(els, h, k):
    """The evening gradient's colour per screen row, from the rows of elevations 0, 10, ... 90 (None = off-screen)."""
    pts = [(y * k, e * 10) for e, y in enumerate(els) if y is not None]
    rows = np.arange(h, dtype=np.float32)
    if len(pts) < 2:
        el = np.full(h, 30.0, np.float32)
    else:
        ys = np.array([p[0] for p in pts], np.float32)
        es = np.array([p[1] for p in pts], np.float32)
        order = np.argsort(ys)
        ys, es = ys[order], es[order]
        el = np.interp(rows, ys, es)                                 # flat beyond the last marker...
        slope = (es[-1] - es[0]) / (ys[-1] - ys[0])                  # ...so extend linearly instead
        el = np.where(rows < ys[0], es[0] + (rows - ys[0]) * slope, el)
        el = np.where(rows > ys[-1], es[-1] + (rows - ys[-1]) * slope, el)
    el = np.clip(el, 0, 90)
    se = np.array([e for e, _ in SKY_STOPS], np.float32)
    out = np.stack([np.interp(el, se, np.array([c[i] for _, c in SKY_STOPS], np.float32)) for i in range(3)], 1)
    return out


def _clouds(surf, clouds, k):
    """Wispy, flat-bottomed clouds catching the low warm light: lilac tops, peach undersides, soft edges."""
    cr = cairo.Context(surf)
    for i, (x, y, wd) in enumerate(clouds):
        x, y, wd = x * k, y * k, max(20.0 * k, wd * k)
        rnd = np.random.default_rng(i + 7)
        for j in range(6):
            dx = (j - 2.5) / 2.5 * wd * 0.42 + rnd.uniform(-0.05, 0.05) * wd
            rw, rh = wd * rnd.uniform(0.26, 0.4), wd * rnd.uniform(0.08, 0.13)
            for (oy, col, a) in ((-rh * 0.35, (0.84, 0.74, 0.88), 0.30), (rh * 0.25, (1.0, 0.8, 0.66), 0.42)):
                cr.save()
                cr.translate(x + dx, y + oy)
                cr.scale(rw, rh)
                g = cairo.RadialGradient(0, 0, 0, 0, 0, 1)
                g.add_color_stop_rgba(0, *col, a)
                g.add_color_stop_rgba(0.6, *col, a * 0.6)
                g.add_color_stop_rgba(1, *col, 0)
                cr.set_source(g)
                cr.arc(0, 0, 1, 0, 2 * math.pi)
                cr.fill()
                cr.restore()


def late_afternoon(rgb):
    """The coordinator's grade, flowing into helper 9's S04 sunset: greens ~25% less saturated, the level ~10% down,
    the highlights warmed toward peach."""
    lum = rgb @ np.array([0.299, 0.587, 0.114], np.float32)
    g_dom = np.clip((rgb[..., 1] - np.maximum(rgb[..., 0], rgb[..., 2])) / 50.0, 0, 1)[..., None]
    rgb = rgb + 0.25 * g_dom * (lum[..., None] - rgb)
    rgb = rgb * 0.9
    hi = (np.clip((lum - 120.0) / 135.0, 0, 1) ** 1.5)[..., None]
    return rgb + hi * np.array([16.0, 5.0, -12.0], np.float32)


def evening(surf, sky, k):
    """Key out the flat 3D sky and paint the evening sky behind everything (a soft key, so blurred treetops blend);
    then the late-afternoon grade over the whole frame."""
    surf.flush()
    h, w = surf.get_height(), surf.get_width()
    arr = np.ndarray((h, w, 4), np.uint8, buffer=surf.get_data(), strides=(surf.get_stride(), 4, 1))
    rgb = arr[..., 2::-1].astype(np.float32)                         # cairo is BGRA in memory
    if sky:
        d = np.abs(rgb - np.array(SKY_KEY, np.float32)).sum(axis=2)
        a = np.clip(1.0 - (d - 8.0) / 42.0, 0, 1)[..., None]
        if a.max() > 0:
            paint = np.repeat(_sky_rows(sky["el"], h, k)[:, None, :], w, axis=1)
            cl = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
            _clouds(cl, sky.get("clouds", []), k)
            cl.flush()
            ca = np.ndarray((h, w, 4), np.uint8, buffer=cl.get_data(), strides=(cl.get_stride(), 4, 1))
            cal = ca[..., 3:4].astype(np.float32) / 255.0
            crgb = ca[..., 2::-1].astype(np.float32)                 # premultiplied
            paint = paint * (1 - cal) + crgb
            rgb = rgb + a * (paint - np.array(SKY_KEY, np.float32))
    rgb = late_afternoon(rgb)
    arr[..., 2::-1] = np.clip(rgb, 0, 255).astype(np.uint8)
    surf.mark_dirty()


def frame(shot, f, src, dst, meta, A):
    surf = cairo.ImageSurface.create_from_png(src)
    if surf.get_format() != cairo.FORMAT_ARGB32:
        s2 = cairo.ImageSurface(cairo.FORMAT_ARGB32, surf.get_width(), surf.get_height())
        c2 = cairo.Context(s2)
        c2.set_source_surface(surf)
        c2.paint()
        surf = s2
    if shot == "S02":
        evening(surf, A[f].get("sky"), surf.get_width() / 720)
    cr = cairo.Context(surf)
    DRAW[shot](cr, f, meta, A, surf.get_width() / 720)
    surf.flush()
    surf.write_to_png(dst)


def _src(shot):
    return os.environ.get("H3_SRC") or os.path.join(BUILD, shot)


def join(shot, n):
    """Fill <src>/NNNN.png from raw parts (parts/<SHOT>_fAAA-BBB.mp4) wherever no Blender frame is here."""
    src_dir = _src(shot)
    os.makedirs(src_dir, exist_ok=True)

    def rng(path):
        m = re.search(r"_f(\d+)-(\d+)(?:_v\d+)?\.mp4$", path)
        return int(m.group(1)), int(m.group(2))
    for part in sorted(glob.glob(os.path.join(PARTS, f"{shot}_f*.mp4")), key=lambda p: (rng(p)[1] - rng(p)[0], p)):
        a, b = rng(part)
        if all(os.path.exists(os.path.join(src_dir, f"{f:04d}.png")) for f in range(a, b + 1)):
            continue
        tmp = os.path.join(BUILD, f"{shot}_join")
        shutil.rmtree(tmp, ignore_errors=True)
        os.makedirs(tmp)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", part, "-start_number", str(a),
                        os.path.join(tmp, "%04d.png")], check=True)
        for gname in sorted(os.listdir(tmp)):
            if not os.path.exists(os.path.join(src_dir, gname)):
                shutil.move(os.path.join(tmp, gname), os.path.join(src_dir, gname))
        shutil.rmtree(tmp)
    missing = [f for f in range(1, n + 1) if not os.path.exists(os.path.join(src_dir, f"{f:04d}.png"))]
    if missing:
        raise SystemExit(f"{shot}: missing frames {missing[0]}..{missing[-1]} ({len(missing)})")


def run(shot):
    meta, A = anchors(shot)
    n = max(A)
    join(shot, n)
    src_dir, out_frames = _src(shot), os.path.join(BUILD, f"{shot}_post")
    shutil.rmtree(out_frames, ignore_errors=True)
    os.makedirs(out_frames)
    for f in range(1, n + 1):
        frame(shot, f, os.path.join(src_dir, f"{f:04d}.png"), os.path.join(out_frames, f"{f:04d}.png"), meta, A)
    os.makedirs(SHOTS_OUT, exist_ok=True)
    mp4, tmp = os.path.join(SHOTS_OUT, f"{shot}.mp4"), os.path.join(BUILD, f"{shot}_enc.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "24", "-i",
                    os.path.join(out_frames, "%04d.png"), "-c:v", "libx264", "-crf", "10", "-preset", "slow",
                    "-pix_fmt", "yuv420p", *CLEAN, tmp], check=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", tmp, "-c", "copy", *CLEAN, "-movflags", "+faststart",
                    mp4], check=True)
    os.remove(tmp)
    P9.sheet(out_frames, n, os.path.join(SHOTS_OUT, f"{shot}_sheet.jpg"))
    print(mp4, n, "frames")


def stills(shot, src_dir, dst_dir, frames):
    """The 2D pass over check stills (NNNN.png in src_dir) -> dst_dir, from the full anchors file."""
    meta, A = anchors(shot)
    os.makedirs(dst_dir, exist_ok=True)
    for f in frames:
        frame(shot, f, os.path.join(src_dir, f"{f:04d}.png"), os.path.join(dst_dir, f"{f:04d}.png"), meta, A)


if __name__ == "__main__":
    if "--stills" in sys.argv:                                   # SHOT --stills SRC DST 3,20,40
        i = sys.argv.index("--stills")
        stills(sys.argv[1], sys.argv[i + 1], sys.argv[i + 2], [int(x) for x in sys.argv[i + 3].split(",")])
    else:
        run(sys.argv[1])
