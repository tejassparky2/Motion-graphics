"""Episode 1 v3 S09 (helper 3), 2D pass: the soul spark's comet trail, twinkles and landing (flash, a ring lying on
the meadow, a sparkle pop), drawn on the rendered frames along the 3D ball's own screen path (out/monsters/diorama_v3/
shots/S09_spark.json, written by helper3.s09). The 3D ball stays the spark itself (depth and blur); this only adds what
doesn't read at phone size. Same look as fx2d.soul_spark (its glow, star and colour).

    /home/user/tools/postenv/bin/python channels/monsters/diorama_v3/helper3_fx.py FRAMES_DIR [SPARK_JSON]

FRAMES_DIR holds 0001.png ... (frame 1 = the shot's first frame); the frames are drawn on in place.
"""
import json
import math
import os
import random
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, ROOT)

from channels.monsters import fx2d  # noqa: E402
from motion.engine import cairo  # noqa: E402

SIZE = 15            # spark size on a 720-wide frame (fx2d's default is 22; the 3D ball is the core)
LAND = 11            # frames of the landing (0.45 s)


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
    f0, f1 = spark["fall"]
    for f in range(f0 - 1, f1 + LAND + 1):
        p = os.path.join(frames_dir, f"{f:04d}.png")
        if not os.path.exists(p):
            continue
        surf = cairo.ImageSurface.create_from_png(p)
        cr = cairo.Context(surf)
        draw(cr, f, spark, surf.get_width() / 720)
        surf.flush()
        surf.write_to_png(p)
        print("fx", f)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else
         os.path.join(ROOT, "out", "monsters", "diorama_v3", "shots", "S09_spark.json"))
