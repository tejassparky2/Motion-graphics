"""Episode 1 v3 S09 (helper 3), 2D pass on the rendered frames, from out/monsters/diorama_v3/shots/S09_spark.json
(written by helper3.s09: the rift's and the ball's screen paths, frame by frame):

    the black: S08b ends on black, so S09 opens on true black; the crack tears open in it and spills light, and the sky
        comes in only through and around the crack as the black pulls back from it (f2-11)
    the rift: the S07/S08 tank crack's zigzag hung in the sky (the one his soul fell through): a glowing hairline at
        first; from his POV ("In another world.") it has opened into a jagged gap with a violet-black void and a few
        stars inside, glowing white-pink edges, 4 shards drifting off its edges, shimmering on 2s
    the soul spark: the 3D ball's comet trail, twinkles and landing (flash, a ring lying on him, a sparkle pop), in
        fx2d.soul_spark's look; the 3D ball stays the spark itself (depth and blur)

    /home/user/tools/postenv/bin/python channels/monsters/diorama_v3/helper3_fx.py FRAMES_DIR [SPARK_JSON]

FRAMES_DIR holds 0001.png ... (frame 1 = the shot's first frame); the frames are drawn on in place.
"""
import json
import math
import os
import random
import sys

import cv2
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, ROOT)

from channels.monsters import fx2d  # noqa: E402
from motion.engine import cairo  # noqa: E402

SIZE = 15            # spark size on a 720-wide frame (fx2d's default is 22; the 3D ball is the core)
LAND = 11            # frames of the landing (0.45 s)
VOID = (0.035, 0.012, 0.085)            # inside the rift: violet-black
EDGE = (1.0, 0.9, 0.97)                 # its rim: white-pink
GLOW = (1.0, 0.78, 0.92)
HOT = (1.0, 0.42, 0.78)                 # the rift's outer glow (reads against a light sky)
SHARDS = ((-0.33, 1, 0), (-0.08, -1, 1), (0.17, 1, 2), (0.36, -1, 3))   # (along, side, seed): off the rift's edges


def _ease_in(u):
    u = max(0.0, min(1.0, u))
    return u * u


def _rift_line(spark, f, k):
    """The crack's zigzag on screen at frame f (drawn on from its middle over crack_on), with each point's along-value
    (y, -0.5..0.5); None if it's behind the camera or not drawn yet."""
    r = spark["rift"].get(str(f))
    c0, c1 = spark["crack_on"]
    if r is None or f < c0:
        return None
    hb = min(1.0, (f - c0 + 1) / (c1 - c0 + 1)) / 2        # drawn band: |y| <= hb
    pts = []
    crack = spark["crack"]
    for (ax, ay), (bx, by) in zip(crack[:-1], crack[1:]):    # each segment clipped to the band
        t0, t1 = 0.0, 1.0
        dy = by - ay
        for lim in (hb, -hb):
            if dy == 0:
                if abs(ay) > hb:
                    t0, t1 = 1.0, 0.0
                continue
            t = (lim - ay) / dy
            if (ay > lim) == (lim > 0):                      # starts outside this bound
                t0 = max(t0, t) if (lim > 0 and dy < 0) or (lim < 0 and dy > 0) else 1.0
            elif (by > lim) == (lim > 0) and by != lim:      # ends outside
                t1 = min(t1, t)
        if t0 < t1:
            for t in (t0, t1):
                p = (ax + (bx - ax) * t, ay + dy * t)
                if not pts or math.hypot(p[0] - pts[-1][0], p[1] - pts[-1][1]) > 1e-6:
                    pts.append(p)
    cx, cy = r["c"]
    ex, ey = r["ex"], r["ey"]
    out = [((cx + ex[0] * x + ey[0] * y) * k, (cy + ex[1] * x + ey[1] * y) * k, y) for x, y in pts]
    return out, math.hypot(*ey) * k


def _width(spark, f):
    """The rift's half-width in crack-height units: a hairline until the soul comes through, a hairline still while
    the camera is down on him; from his POV it opens into a gap on "In another world." (8 frames)."""
    f_in = spark["f_in"]
    if f < f_in:
        return 0.0
    return 0.02 + 0.045 * (1 - (1 - min(1.0, (f - f_in) / 8)) ** 2)


def _offsets(line, hw_px, f):
    """Left and right rims: each point pushed out along its screen normal by a jagged, tapered half-width that
    shimmers on 2s."""
    left, right, hws = [], [], []
    for i, (x, y, a) in enumerate(line):
        p0 = line[max(0, i - 1)]
        p1 = line[min(len(line) - 1, i + 1)]
        dx, dy = p1[0] - p0[0], p1[1] - p0[1]
        ln = math.hypot(dx, dy) or 1
        nx, ny = -dy / ln, dx / ln
        jag = random.Random(i * 7 + 3).uniform(0.45, 1.35) * (1 + 0.12 * random.Random(i * 31 + f // 2).uniform(-1, 1))
        taper = max(0.0, 1 - (2 * abs(a)) ** 2) ** 0.6
        h = hw_px * jag * taper
        hws.append(h)
        left.append((x + nx * h, y + ny * h))
        right.append((x - nx * h, y - ny * h))
    return left, right, hws


def black(arr, spark, f, k):
    """True black over the frame, pulled back from the crack: nothing at f1, a sliver of sky around the crack while it
    draws on, then the black falls away from it (gone by crack_on[1] + 6)."""
    c0, c1 = spark["crack_on"]
    if f > c1 + 6:
        return
    h, w = arr.shape[:2]
    if f < c0:
        alpha = np.ones((h, w), np.float32)
    else:
        rl = _rift_line(spark, f, k)
        if rl is None:
            return
        line, hpx = rl
        r = (2 + 14 * (f - c0) / max(1, c1 - c0)) * k if f <= c1 else (16 * k + 1600 * k * _ease_in((f - c1) / 6))
        mask = np.full((h, w), 255, np.uint8)
        pts = np.array([[p[0], p[1]] for p in line], np.int32).reshape(-1, 1, 2)
        cv2.polylines(mask, [pts], False, 0, max(1, int(2 * k)))
        d = cv2.distanceTransform(mask, cv2.DIST_L2, 5)
        feather = 8 * k + 1.1 * r
        alpha = np.clip((d - r) / feather, 0, 1).astype(np.float32)
        if f > c1:                                            # and the rest of the dark lifts as the camera turns away
            u = min(1.0, (f - c1) / 6)
            alpha *= 1 - u * u * (3 - 2 * u)
    arr[..., :3] = (arr[..., :3].astype(np.float32) * (1 - alpha[..., None])).astype(np.uint8)


def rift(cr, spark, f, k):
    rl = _rift_line(spark, f, k)
    if rl is None:
        return
    line, hpx = rl
    if len(line) < 2 or all(not (-200 * k < x < 920 * k and -200 * k < y < 1480 * k) for x, y, _ in line):
        return
    c0, c1 = spark["crack_on"]
    shimmer = 0.85 + 0.15 * math.sin((f // 2) * 1.9)
    spill = max(0.0, 1 - (f - c1) / 8) if f >= c0 else 0.0    # in the dark it spills more light
    hw = _width(spark, f) * hpx
    left, right, hws = _offsets(line, hw, f)
    cr.save()
    cr.set_line_join(cairo.LINE_JOIN_ROUND)
    cr.set_line_cap(cairo.LINE_CAP_ROUND)

    def outline():
        cr.new_path()
        cr.move_to(*left[0])
        for p in left[1:]:
            cr.line_to(*p)
        for p in reversed(right):
            cr.line_to(*p)
        cr.close_path()

    def centre():
        cr.new_path()
        cr.move_to(line[0][0], line[0][1])
        for x, y, _ in line[1:]:
            cr.line_to(x, y)
    for wdt, a in ((70, 0.10 * spill), (34, 0.16 * spill)):                 # the spill of light in the black
        if a > 0:
            centre()
            cr.set_source_rgba(*GLOW, a)
            cr.set_line_width(wdt * k)
            cr.stroke()
    if max(hws) < 1.5 * k:                                    # still a hairline: glow + white core
        for wdt, a in ((18, 0.12), (9, 0.24), (4.5, 0.5)):
            centre()
            cr.set_source_rgba(*GLOW, a * shimmer)
            cr.set_line_width(wdt * k)
            cr.stroke()
        centre()
        cr.set_source_rgba(1, 0.98, 1, 1)
        cr.set_line_width(2.2 * k)
        cr.stroke()
    else:
        for wdt, a, col in ((90, 0.12, HOT), (56, 0.2, HOT), (32, 0.32, HOT), (16, 0.6, GLOW), (8, 0.9, EDGE)):
            outline()                                         # glow outside the rim: magenta-pink to white
            cr.set_source_rgba(*col, a * shimmer)
            cr.set_line_width(wdt * k)
            cr.stroke()
        outline()                                             # the void
        cr.set_source_rgb(*VOID)
        cr.fill_preserve()
        cr.save()
        cr.clip()
        rnd = random.Random(5)
        for i in range(9):                                    # a few stars inside, twinkling on 2s
            j = rnd.randrange(1, len(line) - 1)
            lat = rnd.uniform(-0.55, 0.55)
            x = line[j][0] + (left[j][0] - line[j][0]) * lat * 2 if lat > 0 else line[j][0] + (right[j][0] - line[j][0]) * -lat * 2
            y = line[j][1] + (left[j][1] - line[j][1]) * lat * 2 if lat > 0 else line[j][1] + (right[j][1] - line[j][1]) * -lat * 2
            tw = 0.5 + 0.5 * math.sin((f // 2) * 1.3 + i * 2.1)
            cr.set_source_rgba(1, 0.95, 1, 0.55 + 0.45 * tw)
            fx2d._star4(cr, x, y, (1.6 + 2.2 * tw) * k, 0.4)
            cr.fill()
        cr.restore()
        outline()                                             # the rim
        cr.set_source_rgba(*EDGE, 1.0)
        cr.set_line_width(3.4 * k * (0.9 + 0.2 * shimmer))
        cr.stroke()
        if f >= spark["f_in"]:                                # shards drifting off its edges
            for along, side, sd in SHARDS:
                j = min(range(len(line)), key=lambda i: abs(line[i][2] - along))
                rim = left[j] if side > 0 else right[j]
                nx, ny = rim[0] - line[j][0], rim[1] - line[j][1]
                ln = math.hypot(nx, ny) or 1
                nx, ny = nx / ln, ny / ln
                rnd = random.Random(sd)
                drift = (18 + 1.1 * (f - spark["f_in"]) + rnd.uniform(0, 10)) * k
                x, y = rim[0] + nx * drift, rim[1] + ny * drift + 0.3 * (f - spark["f_in"]) * k
                sz = rnd.uniform(12, 20) * k
                rot = rnd.uniform(0, 6.3) + 0.04 * (f - spark["f_in"]) * side
                cr.new_path()
                for q in range(3):
                    ang = rot + q * 2.1 + rnd.uniform(-0.4, 0.4)
                    rr = sz * rnd.uniform(0.6, 1.2)
                    (cr.move_to if q == 0 else cr.line_to)(x + math.cos(ang) * rr, y + math.sin(ang) * rr)
                cr.close_path()
                cr.set_source_rgb(*VOID)
                cr.fill_preserve()
                cr.set_source_rgba(*EDGE, 0.9 * shimmer)
                cr.set_line_width(2.2 * k)
                cr.stroke()
                fx2d._glow(cr, x, y, sz * 2.6, GLOW, 0.3 * shimmer)
    cr.restore()


def draw_all(surf, f, spark):
    k = surf.get_width() / 720
    surf.flush()
    arr = np.ndarray((surf.get_height(), surf.get_width(), 4), np.uint8, buffer=surf.get_data(),
                     strides=(surf.get_stride(), 4, 1))
    black(arr, spark, f, k)
    surf.mark_dirty()
    cr = cairo.Context(surf)
    rift(cr, spark, f, k)
    draw(cr, f, spark, k)
    surf.flush()


def _streak(ball, trail, length=300.0, n=18):
    """The trail as a streak behind the ball: walk back along where it was (as this frame's camera sees it) for at most
    `length` px (the camera swings fast, so the older points fly far off-screen), then resample to n points, oldest
    first, ending just behind the ball."""
    pts, total = [tuple(ball)], 0.0
    for p in reversed(trail):
        a = pts[-1]
        d = math.hypot(p[0] - a[0], p[1] - a[1])
        if total + d >= length:
            u = (length - total) / d if d else 0
            pts.append((a[0] + (p[0] - a[0]) * u, a[1] + (p[1] - a[1]) * u))
            total = length
            break
        pts.append(tuple(p))
        total += d
    if total < 1:
        return []
    out, seg, acc = [], 0, 0.0                                # resample by arc length, from the far end to the ball
    lens = [math.hypot(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1]) for i in range(len(pts) - 1)]
    for j in range(n):
        t = total * (1 - (j + 0.5) / n)                       # distance back from the ball
        acc, seg = 0.0, 0
        while seg < len(lens) - 1 and acc + lens[seg] < t:
            acc += lens[seg]
            seg += 1
        u = (t - acc) / lens[seg] if lens[seg] else 0
        a, b = pts[seg], pts[seg + 1]
        out.append((a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u))
    return out


def draw(cr, f, spark, k=1.0):
    path, (f0, f1) = spark["path"], spark["fall"]
    size = SIZE * k
    col, white = fx2d.SOUL, fx2d.WHITE
    if f0 - 1 <= f <= f1:                                     # flying: trail, twinkles, a halo round the ball
        tr = _streak(path[str(f)]["ball"], path[str(f)]["trail"])
        for j, (x, y) in enumerate(tr):
            x, y = x * k, y * k
            q = (j + 1) / (len(tr) + 1)
            fx2d._glow(cr, x, y, size * (0.6 + 1.6 * q), col, 0.24 * q)
            cr.set_source_rgba(1, 1, 1, 0.55 * q * q)
            cr.arc(x, y, size * 0.32 * q, 0, 2 * math.pi)
            cr.fill()
        rnd = random.Random(101 + f // 2 * 2)                 # twinkles on 2s
        for _ in range(4 if tr else 0):
            j = rnd.randrange(len(tr))
            x, y = tr[j][0] * k, tr[j][1] * k
            life = 0.3 + 0.7 * (j + 1) / len(tr)
            cr.set_source_rgba(*col[:3], 0.9 * life)
            fx2d._star4(cr, x + rnd.uniform(-18, 18) * k, y + rnd.uniform(-10, 10) * k, size * 0.5 * life + 3 * k,
                        rnd.uniform(0, 0.8))
            cr.fill()
        x, y = (c * k for c in path[str(f)]["ball"])
        fx2d._glow(cr, x, y, size * 4.0, col, 0.45)
        fx2d._glow(cr, x, y, size * 1.6, white, 0.75)
        cr.set_source_rgba(1, 1, 1, 0.95)                     # a core too: the 3D ball can sit under the black
        cr.arc(x, y, size * 0.32, 0, 2 * math.pi)
        cr.fill()
    elif f1 < f <= f1 + LAND:                                 # landing: flash, a ring on the ground, sparkle pop
        u = (f - f1) / LAND
        x, y = (c * k for c in path[str(f1)]["ball"])
        fx2d._glow(cr, x, y, size * (5 + 6 * u), white, (1 - u) * 0.9)
        cr.set_source_rgba(*col[:3], 1 - u)
        cr.set_line_width((4 * (1 - u) + 1) * k)
        cr.save()
        cr.translate(x, y)
        cr.scale(1, 0.35)
        cr.arc(0, 0, size * (1.5 + 7 * fx2d.ease_out(u)), 0, 2 * math.pi)
        cr.restore()
        cr.stroke()
        rnd = random.Random(10)
        for i in range(6):
            ang = i * math.pi / 3 + rnd.uniform(-0.3, 0.3)
            r = size * (1.2 + 4.5 * fx2d.ease_out(u))
            cr.set_source_rgba(1, 1, 1, 1 - u)
            fx2d._star4(cr, x + math.cos(ang) * r, y + math.sin(ang) * r * 0.6, size * 0.5 * (1 - u) + 2 * k, 0.3)
            cr.fill()


def main(frames_dir, spark_json):
    with open(spark_json) as fh:
        spark = json.load(fh)
    for f in range(1, len(spark["rift"]) + 1):
        p = os.path.join(frames_dir, f"{f:04d}.png")
        if not os.path.exists(p):
            continue
        surf = cairo.ImageSurface.create_from_png(p)
        if surf.get_format() != cairo.FORMAT_ARGB32:
            s2 = cairo.ImageSurface(cairo.FORMAT_ARGB32, surf.get_width(), surf.get_height())
            c2 = cairo.Context(s2)
            c2.set_source_surface(surf)
            c2.paint()
            surf = s2
        draw_all(surf, f, spark)
        surf.write_to_png(p)
        print("fx", f)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else
         os.path.join(ROOT, "out", "monsters", "diorama_v3", "shots", "S09_spark.json"))
