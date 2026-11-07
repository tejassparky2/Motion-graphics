"""2D pass for helper 4's Episode 2 shots (DIORAMA_EP02.md), over the Blender frames with comp.py:

    S05 "...In my bare hands."  After the cut up to his face (f50) the anime sweat drop pops in beside his head on
        "In my" (fx2d_anime.sweat_drop, tracked to his eyes).
    S20bot "Option B: show her the glowing mark."  The coral zigzag on his raised forearm (helper 9's S14 mark, via
        post_helper9.mark) flares on "glowing mark" with a burst and sparkles, then glows softly to the end.
    S06 "...Straight ahead."  On "Straight", an arrow-like jet streak shoots straight out of the claw to the frame
        edge (the claw's own line, nothing in any other direction): a tapered white jet with an ink outline and an
        arrowhead front, two speed lines riding along it and a small pressure ring at the muzzle. No text.

    FPS=24 python channels/monsters/diorama_ep02/post_helper4.py S05 [S06]                (mp4 + sheet per shot)
    FPS=24 python channels/monsters/diorama_ep02/post_helper4.py S06 --still 70 STILL.png OUT.png   (a preview)

Reads build/monsters/diorama_ep02/render/<SHOT>/0001.png ... (or SRC=...) and <SHOT>_anchors.json (written by
diorama_ep02/helper4.py). Writes out/monsters/diorama_ep02/shots/<SHOT>.mp4 + <SHOT>_sheet.jpg (crf 10, no tags).
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

from channels.monsters import comp, fx2d_anime  # noqa: E402
from channels.monsters.diorama_v3.post_helper1 import CLEAN, sheet  # noqa: E402
from motion.engine import FPS, cairo  # noqa: E402

EP = os.environ.get("EP", "ep02")                       # EP=ep03 for Episode 3's shots (S01, S11)
BUILD = os.path.join(ROOT, "build", "monsters", f"diorama_{EP}")
SHOTS_OUT = os.path.join(ROOT, "out", "monsters", f"diorama_{EP}", "shots")
S05_CUT = 50                                  # helper4.S05_CUT
INK = (0.106, 0.094, 0.188, 1.0)              # puffshrimp INK #1b1830
JET = (0.93, 0.98, 1.0, 1.0)
JET_EDGE = (0.62, 0.88, 1.0, 1.0)


def anchors(shot):
    with open(os.path.join(BUILD, f"{shot}_anchors.json")) as fh:
        return {int(k): v for k, v in json.load(fh).items()}


def at(a, t, name):
    f = min(max(1, int(round(t * FPS)) + 1), max(a))
    return a[f][name]


def _words(line_id):
    with open(os.path.join(ROOT, "channels", "monsters", EP, "timing.json")) as f:
        d = json.load(f)
    ln = next(x for x in d["lines"] if x["id"] == line_id)
    s0 = next(s["start"] for s in d["shots"] if s["shot"] == ln["scene"])
    return {w["w"]: (w["start"] - s0, w["end"] - s0) for w in ln["words"]}


# ------------------------------------------------------------------------------------------------------------ S05
def sweat(a, side=1, k=2.6):
    def draw(cr, t, start, end=None):
        (lx, ly), (rx, ry) = at(a, t, "eye_l"), at(a, t, "eye_r")
        d = math.hypot(rx - lx, ry - ly)
        tilt = math.atan2(ry - ly, rx - lx)
        if abs(tilt) > math.pi / 2:
            tilt -= math.copysign(math.pi, tilt)
        fx2d_anime.sweat_drop(cr, t, start, x=(lx + rx) / 2, y=(ly + ry) / 2, size=d * k, end=end, side=side,
                              tilt=tilt)
    return draw


def terror(a, k=0.34):
    """Pin-prick terror eyes over his own (fx2d_anime.terror_eyes, the blue shock lines included), tracked."""
    def draw(cr, t, start, end=None):
        (lx, ly), (rx, ry) = at(a, t, "eye_l"), at(a, t, "eye_r")
        d = math.hypot(rx - lx, ry - ly)
        tilt = math.atan2(ry - ly, rx - lx)
        if abs(tilt) > math.pi / 2:
            tilt -= math.copysign(math.pi, tilt)
        fx2d_anime.terror_eyes(cr, t, start, x=(lx + rx) / 2, y=(ly + ry) / 2, size=d * 2.6, end=end,
                               eyes=((lx, ly), (rx, ry)), er=k * d, tilt=tilt)
    return draw


# ------------------------------------------------------------------------------------------------------------ S06
def _ease_out(u):
    u = max(0.0, min(1.0, u))
    return 1 - (1 - u) ** 3


def jet(a):
    """The arrow-like jet: its front races from the muzzle to past the frame edge in 4 frames, holds 5, then the
    tail catches up and it thins away over 5 (on 1s, it's an effect)."""
    def draw(cr, t, start, end=None):
        u = t - start
        if u < 0 or u > 14 / FPS:
            return
        (x0, y0), (x1, y1) = at(a, t, "tip"), at(a, t, "ahead")
        ang = math.atan2(y1 - y0, x1 - x0)
        ca = math.cos(ang)
        L = (690.0 - x0) / ca if ca > 0.2 else 600.0                      # the point stops just inside the right edge
        front = L * _ease_out(u / (4 / FPS))
        tail = L * max(0.0, (u - 9 / FPS) / (5 / FPS)) ** 1.5
        thin = 1.0 - max(0.0, (u - 9 / FPS) / (5 / FPS))
        if front - tail < 4:
            return
        cr.save()
        cr.translate(x0, y0)
        cr.rotate(ang)
        w0, w1 = 12.0 * thin + 3, 40.0 * thin + 4                          # tapered: thin at the muzzle
        head = min(70.0, front - tail)

        def body(grow):
            cr.new_path()
            cr.move_to(tail, -(w0 + grow) / 2)
            cr.line_to(front - head, -(w1 + grow) / 2)
            cr.line_to(front - head, -(w1 * 2.0 + grow) / 2)               # the arrowhead's barbs
            cr.line_to(front + grow * 0.6, 0)
            cr.line_to(front - head, (w1 * 2.0 + grow) / 2)
            cr.line_to(front - head, (w1 + grow) / 2)
            cr.line_to(tail, (w0 + grow) / 2)
            cr.close_path()
        body(9.0)
        cr.set_source_rgba(*INK)
        cr.fill()
        body(3.0)
        cr.set_source_rgba(*JET_EDGE)
        cr.fill()
        body(-5.0)
        cr.set_source_rgba(*JET)
        cr.fill()
        for off, k in ((-1, 0.55), (1, 0.75)):                           # speed lines riding along it
            yy = off * (w1 * 1.4 + 14)
            xa, xb = tail + (front - tail) * 0.15, tail + (front - tail) * k
            if xb - xa > 10:
                cr.new_path()
                cr.move_to(xa, yy)
                cr.line_to(xb, yy)
                cr.set_line_width(6.0 * thin + 1)
                cr.set_line_cap(cairo.LINE_CAP_ROUND)
                cr.set_source_rgba(*INK)
                cr.stroke()
        if u < 6 / FPS:                                                   # the pressure ring at the muzzle
            r = 18 + 70 * _ease_out(u / (6 / FPS))
            cr.save()
            cr.scale(0.45, 1.0)
            cr.new_path()
            cr.arc(0, 0, r, 0, 2 * math.pi)
            cr.set_line_width(7.0 * (1 - u / (6 / FPS)) + 1)
            cr.set_source_rgba(*INK)
            cr.stroke()
            cr.restore()
        cr.restore()
    return draw


# ---------------------------------------------------------------------------------------------------------- S20bot
MARK20_K = 2.0                                                              # S20bot's mark: 2x S14's on screen
PINK = (1.0, 0.62, 0.74)


def mark20():
    """S20bot (the owner's new ending, "show her the glowing mark"): helper 9's S14 wrist mark (post_helper9.mark, the
    same zigzag, colours and bloom), on his raised left forearm from S20bot_mark.json: faint once the arm is up, the
    flare on "glowing mark" (a burst and sparkles), then a soft pulsing glow through the standoff."""
    from channels.monsters import fx2d
    from channels.monsters.diorama_ep02 import post_helper9 as P9
    with open(os.path.join(BUILD, "S20bot_mark.json")) as fh:
        d = json.load(fh)
    meta, A = d["meta"], {int(f): v for f, v in d["frames"].items()}
    fg, fe = meta["f_glow"], meta["f_mark_end"]

    def draw(cr, t, start, end=None):
        f = min(max(1, int(round(t * FPS)) + 1), max(A))
        g = A[f]
        lvl = g["level"]
        if lvl <= 0 or g.get("z", 1) <= 0:
            return
        geo = P9._on_arm(g)
        geo = dict(geo, ex=[v * MARK20_K for v in geo["ex"]], ey=[v * MARK20_K for v in geo["ey"]])   # 2x the S14 size
        x, y = geo["c"]
        size = math.hypot(*geo["ey"])
        halo = min(1.0, lvl)
        fx2d._glow(cr, x, y, size * 1.25, PINK, 0.45 * halo)             # the soft pink halo round the wrist
        if f >= fg:                                                         # the flare: a white-hot bloom
            fl = max(0.0, 1.0 - abs(f - (fg + 3)) / 6.0)
            fx2d._glow(cr, x, y, size * 0.8, (1.0, 0.93, 0.88), 0.55 * fl)
        P9.mark(cr, geo, 1.0, 0.5, min(1.3, lvl), f, bold=3.2)
        (lx, ly, _), (rx, ry, _) = g["w_eye_l"], g["w_eye_r"]                 # a faint coral spill on Wren's face
        fx2d._glow(cr, (lx + rx) / 2, (ly + ry) / 2 + 10, math.hypot(rx - lx, ry - ly) * 3.2, P9.CORAL,
                   0.16 * halo)
        t0 = (fg + 3 - 1) / FPS                                             # the flare's peak
        fx2d.glow_burst(cr, t, t0, x, y, r=size * 2.4, col=P9.CORAL_HOT, dur=0.5, rays=10, seed=3)
        fx2d.sparkles(cr, t, t0 + 0.04, x, y, n=8, radius=size * 1.0, size=size * 0.17,
                      cols=((1, 0.8, 0.7, 1), fx2d.WHITE, (1, 0.6, 0.5, 1)), life=1.1, seed=5)
        if f >= fe:                                                         # a few soft sparkles in the hold
            fx2d.sparkles(cr, t, (fe - 1) / FPS, x, y, n=4, radius=size * 0.8, size=size * 0.11,
                          cols=((1, 0.8, 0.7, 1), (1, 0.6, 0.5, 1)), life=1.6, seed=9)
    return draw


def wren_fear():
    """S20bot: Wren's wide, pin-prick eyes (fx2d_anime.terror_eyes, the blue shock lines included) from the moment she
    sees the mark flare, tracked to her eyes (S20bot_mark.json's w_eye_l / w_eye_r)."""
    with open(os.path.join(BUILD, "S20bot_mark.json")) as fh:
        d = json.load(fh)
    meta, A = d["meta"], {int(f): v for f, v in d["frames"].items()}

    def draw(cr, t, start, end=None):
        f = min(max(1, int(round(t * FPS)) + 1), max(A))
        (lx, ly, _), (rx, ry, _) = A[f]["w_eye_l"], A[f]["w_eye_r"]
        dd = math.hypot(rx - lx, ry - ly)
        tilt = math.atan2(ry - ly, rx - lx)
        if abs(tilt) > math.pi / 2:
            tilt -= math.copysign(math.pi, tilt)
        fx2d_anime.terror_eyes(cr, t, start, x=(lx + rx) / 2, y=(ly + ry) / 2, size=dd * 2.6, end=end,
                               eyes=((lx, ly), (rx, ry)), er=0.34 * dd, tilt=tilt)
    return draw, (meta["f_fear"] - 1) / FPS, (max(A) - 1) / FPS


def mark_s01():
    """Ep 3 S01 (the hook): the mark blazing on his wrist big in the foreground from frame 0: helper 9's zigzag
    (post_helper9.mark) at its projected size, white-hot, a pink halo, a steady pulse and sparkles popping every
    ~0.6 s; and Wren's terror eyes carrying on from Ep 2."""
    from channels.monsters import fx2d
    from channels.monsters.diorama_ep02 import post_helper9 as P9
    with open(os.path.join(BUILD, "S01_mark.json")) as fh:
        d = json.load(fh)
    A = {int(f): v for f, v in d["frames"].items()}
    k_size = float(os.environ.get("S01_MARK_K", "1.3"))

    def draw(cr, t, start, end=None):
        f = min(max(1, int(round(t * FPS)) + 1), max(A))
        g = A[f]
        if g.get("z", 1) <= 0:
            return
        geo = P9._on_arm(g)
        geo = dict(geo, ex=[v * k_size for v in geo["ex"]], ey=[v * k_size for v in geo["ey"]])
        x, y = geo["c"]
        size = math.hypot(*geo["ey"])
        lvl = g["level"]
        fx2d._glow(cr, x, y, size * 1.4, PINK, 0.5)
        fx2d._glow(cr, x, y, size * 0.7, (1.0, 0.93, 0.88), 0.25 + 0.1 * math.sin(f / 4.0))
        P9.mark(cr, geo, 1.0, 0.5, min(1.3, lvl), f, bold=2.6)
        for j, t0 in enumerate(np_arange(-0.2, t + 0.01, 0.6)):
            fx2d.sparkles(cr, t, t0, x, y, n=5, radius=size * 0.95, size=size * 0.14,
                          cols=((1, 0.8, 0.7, 1), fx2d.WHITE, (1, 0.6, 0.5, 1)), life=1.0, seed=11 + j)

    def eyes(cr, t, start, end=None):
        f = min(max(1, int(round(t * FPS)) + 1), max(A))
        (lx, ly, lz), (rx, ry, _) = A[f]["w_eye_l"], A[f]["w_eye_r"]
        if lz <= 0:
            return
        dd = math.hypot(rx - lx, ry - ly)
        tilt = math.atan2(ry - ly, rx - lx)
        if abs(tilt) > math.pi / 2:
            tilt -= math.copysign(math.pi, tilt)
        fx2d_anime.terror_eyes(cr, t, -1.0, x=(lx + rx) / 2, y=(ly + ry) / 2, size=dd * 2.6, end=end,
                               eyes=((lx, ly), (rx, ry)), er=0.34 * dd, tilt=tilt)
    n = max(A)
    return [(draw, dict(start=0.0)), (eyes, dict(start=0.0, end=(n - 1) / FPS))]


def s11_pass():
    """Ep 3 S11 (the explainer): a soft bloom round the coral light all through; from "backs" a soft glow line from the
    light to the moth's back (an arrow-like taper ending in a small head at its back), drawing on over 6 frames and
    breathing. No text."""
    from channels.monsters import fx2d
    with open(os.path.join(BUILD, "S11_anchors.json")) as fh:
        d = json.load(fh)
    meta, A = d["meta"], {int(f): v for f, v in d["frames"].items()}
    f0 = meta["f_backs"] - 4
    coral, hot = (1.0, 0.52, 0.40), (1.0, 0.86, 0.78)

    def draw(cr, t, start, end=None):
        f = min(max(1, int(round(t * FPS)) + 1), max(A))
        g = A[f]
        lx, ly = g["light"][:2]
        rr = abs(g["r_orb"][1] - ly) or 12.0
        fx2d._glow(cr, lx, ly, rr * 7.0, coral, 0.45)                   # the light's bloom
        fx2d._glow(cr, lx, ly, rr * 2.6, hot, 0.6)
        if f < f0:
            return
        u = _ease_out((f - f0) / 6.0)
        bx, by = g["back"][:2]
        L = math.hypot(bx - lx, by - ly)
        if L < 1:
            return
        ang = math.atan2(by - ly, bx - lx)
        r0 = rr * 1.4                                                   # start just outside the orb
        r1 = r0 + (L - r0 - 6) * u                                      # the tip races out to its back
        breathe = 0.85 + 0.15 * math.sin(f / 3.0)
        cr.save()
        cr.translate(lx, ly)
        cr.rotate(ang)
        for wdt, a in ((22.0, 0.10), (12.0, 0.22), (5.0, 0.75)):        # a soft glowing line, tapered
            cr.new_path()
            cr.move_to(r0, -wdt * 0.25)
            cr.line_to(r1 - 10, -wdt * 0.5)
            cr.line_to(r1 - 10, wdt * 0.5)
            cr.line_to(r0, wdt * 0.25)
            cr.close_path()
            cr.set_source_rgba(*coral, a * breathe)
            cr.fill()
        if u > 0.6:                                                     # the head, at its back
            cr.new_path()
            cr.move_to(r1 + 4, 0)
            cr.line_to(r1 - 16, -11)
            cr.line_to(r1 - 16, 11)
            cr.close_path()
            cr.set_source_rgba(*hot, min(1.0, (u - 0.6) / 0.4) * breathe)
            cr.fill()
        cr.restore()
        fx2d._glow(cr, bx, by, 26.0, coral, 0.35 * u * breathe)          # where it lands: its back lit
    return [(draw, dict(start=0.0))]


def np_arange(a, b, step):
    out, v = [], a
    while v < b:
        out.append(v)
        v += step
    return out


def overlays(shot):
    if EP == "ep03" and shot == "S01":
        return mark_s01()
    if EP == "ep03" and shot == "S11":
        return s11_pass()
    if shot == "S20bot":
        fear, t0, t1 = wren_fear()
        return [(mark20(), dict(start=0.0)), (fear, dict(start=t0, end=t1))]
    if shot not in ("S05", "S06"):
        return []
    a = anchors(shot)
    n = max(a)
    if shot == "S05":
        w = _words("l5")
        return [(terror(a), dict(start=(S05_CUT - 1) / FPS, end=(n - 1) / FPS)),
                (sweat(a), dict(start=w["In"][0] - 2 / FPS, end=(n - 1) / FPS))]
    if shot == "S06":
        w = _words("l6")
        return [(jet(a), dict(start=w["Straight"][0]))]
    return []


PARTS = os.path.join(ROOT, "out", "monsters", f"diorama_{EP}", "parts")


def fill_from_parts(shot, n):
    """Frames rendered elsewhere: decode out/monsters/diorama_ep02/parts/<SHOT>_v2_fAAA-BBB.mp4 (S20bot v2's split) into
    the render folder wherever a frame is missing, then check every frame 1..n is there."""
    import glob
    import re
    d = os.path.join(BUILD, "render", shot)
    os.makedirs(d, exist_ok=True)
    for part in sorted(glob.glob(os.path.join(PARTS, f"{shot}_v2_f*.mp4"))):
        a, b = map(int, re.search(r"_f(\d+)-(\d+)\.mp4$", part).groups())
        if all(os.path.exists(os.path.join(d, f"{f:04d}.png")) for f in range(a, b + 1)):
            continue
        tmp = tempfile.mkdtemp()
        subprocess.run(["ffmpeg", "-v", "error", "-i", part, "-start_number", str(a), os.path.join(tmp, "%04d.png")],
                       check=True)
        got = sorted(os.listdir(tmp))
        if len(got) != b - a + 1:
            raise SystemExit(f"{part}: {len(got)} frames, expected {b - a + 1}")
        for g in got:
            if not os.path.exists(os.path.join(d, g)):
                shutil.move(os.path.join(tmp, g), os.path.join(d, g))
        shutil.rmtree(tmp)
        print("filled from", os.path.basename(part))
    missing = [f for f in range(1, n + 1) if not os.path.exists(os.path.join(d, f"{f:04d}.png"))]
    if missing:
        raise SystemExit(f"{shot}: frames missing {missing[:12]}{'...' if len(missing) > 12 else ''}")
    for f in sorted(int(x[:4]) for x in os.listdir(d) if x[:4].isdigit() and x.endswith(".png")):
        if f > n:
            os.remove(os.path.join(d, f"{f:04d}.png"))                    # extra frames past the shot (a longer chunk)


def run(shot):
    if shot == "S20bot":
        with open(os.path.join(ROOT, "channels", "monsters", EP, "timing.json")) as fh:
            n20 = next(s["render_frames"] for s in json.load(fh)["shots"] if s["shot"] == "S20")
        fill_from_parts(shot, n20)
    src = comp.Source(os.environ.get("SRC") or os.path.join(BUILD, "render", shot))
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
    """Preview frame f: the overlays over one rendered still (scaled to 720x1280 if it is a half-scale still)."""
    tmp = tempfile.mkdtemp()
    im = Image.open(png).convert("RGB").resize((720, 1280))
    im.save(os.path.join(tmp, f"{f:04d}.png"))
    for i in range(1, f):
        os.symlink(os.path.join(tmp, f"{f:04d}.png"), os.path.join(tmp, f"{i:04d}.png"))
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
