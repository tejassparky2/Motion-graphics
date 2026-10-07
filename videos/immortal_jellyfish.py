"""The immortal jellyfish (Turritopsis dohrnii) -- weird animal, in the polished look.

Facts (out/scripts_polished_batch1.md, approved by the owner on 7 Oct 2026):
- About 4.5 mm across (Nathaniel Rich, NYT Magazine, Nov 2012): smaller than a little fingernail.
- Normal hydrozoan life cycle: polyp on a hard surface -> buds off a medusa (jellyfish) -> reproduces -> dies.
- When stressed, injured, sick or old, T. dohrnii can sink, shrink into a cyst-like blob and turn back into a polyp
  colony, then grow up again, by transdifferentiation (cells changing type). Wikipedia "Turritopsis dohrnii";
  Texas A&M (2021).
- Shin Kubota (Kyoto University) watched one rejuvenate 10 times in about two years (Biogeography 13, 2011).
- It can still be eaten or killed by disease; it just doesn't have to die of old age.
The red stomach drawn in the bell is a real feature of the species.
"""
import math
import random

from motion.engine import W, H, cue, ease_out, hexc, lerp, seg, clamp01
from motion.kit import whip
from motion.polish import (OUTLINE, WHITE, alpha, appear, bokeh, bold_text, camera, captions, counter, ellipse, enter,
                           light_rays, lin, paint, particles, put, rad, rrect, shade, sign, smooth, soft_disc,
                           soft_rrect, sprite, stamp, stroke_line, vignette)
from motion.toons import SKIN, fish, jelly_blob, jellyfish, polyp

NARRATOR = dict()
TAIL = 0.9

SCRIPT = [
    dict(id="j1", scene="hook", text="This animal can grow old. Then turn back into a baby."),
    dict(id="j2", scene="size", text="It's called the immortal jellyfish. And it's smaller than your little "
                                     "fingernail."),
    dict(id="j3", scene="cycle", text="A normal jellyfish starts as a tiny blob on a rock, called a polyp."),
    dict(id="j4", scene="cycle", text="It grows into a jellyfish. It has babies. Then it dies."),
    dict(id="j5", scene="cheat", text="This one cheats."),
    dict(id="j6", scene="sink", text="When it's old, hurt, or sick, it sinks to the sea floor."),
    dict(id="j7", scene="sink", text="Its body shrinks into a little blob."),
    dict(id="j8", scene="sink", text="And the blob turns back into a polyp. The baby stage."),
    dict(id="j9", scene="again", text="Then it grows up all over again."),
    dict(id="j10", scene="cells", text="Its cells switch jobs. Old jellyfish cells turn into baby polyp cells."),
    dict(id="j11", scene="lab", text="In a lab in Japan, one did this [ten|10] times in [two|2] years."),
    dict(id="j12", scene="danger", text="So is it truly immortal? Not quite."),
    dict(id="j13", scene="danger", text="Fish eat it. Disease kills it. It just doesn't have to die of old age."),
    dict(id="j14", scene="end", text="If you could go back to any age, which age would you pick?", gap=0.3),
]

METADATA = dict(
    title="This Jellyfish Can Turn Back Into A Baby. Again And Again. 🪼",
    alt_titles=["The Immortal Jellyfish That Reverses Its Own Age 🪼", "This Animal Doesn't Have to Die of Old Age 🤯"],
    description="""This animal can grow old... then turn back into a baby. 🪼

It's the immortal jellyfish (Turritopsis dohrnii), about 4.5 mm across: smaller than your little fingernail.
A normal jellyfish starts as a polyp on a rock, grows into a jellyfish, has babies and dies. This one cheats: when it's old, hurt or sick, it sinks to the sea floor, shrinks into a little blob, and turns back into a polyp, the baby stage. Then it grows up all over again. Its cells switch jobs to do it.
In a lab in Japan, one did this 10 times in 2 years.

Is it truly immortal? Not quite. Fish eat it and disease kills it. It just doesn't have to die of old age.

Sources: Wikipedia, "Turritopsis dohrnii"; Texas A&M Today (2021); N. Rich, The New York Times Magazine (2012); S. Kubota, Biogeography 13 (2011).

💬 If you could go back to any age, which age would you pick? 👇

🔔 Interestingly Strange: weird animals, bizarre history, mind-bending paradoxes and strange stories, animated in under a minute.""",
    hashtags=["#Jellyfish", "#Animals", "#Shorts"],
    tags=["immortal jellyfish", "turritopsis dohrnii", "jellyfish facts", "animal facts", "weird animals",
          "biological immortality", "ocean animals", "sea creatures", "science facts", "interestingly strange"],
    pinned_comment="Which age would you go back to? I'd pick 10 🪼👇",
)

RED = hexc("#e8473f")
GOLD = hexc("#ffcf3f")
BLUE = hexc("#4aa3f0")
GREEN = hexc("#3fbf6a")
PURPLE = hexc("#7a5bd0")
PINK = hexc("#ff6fa5")
FLOOR = 880.0


# ---------------------------------------------------------------- the sea
def _sea_layer(c):
    c.rectangle(0, 0, W, H)
    c.set_source(lin(0, 0, 0, H, [(0, hexc("#4fc3e8")), (0.45, hexc("#1f7fb8")), (1, hexc("#0d3a6a"))]))
    c.fill()
    rng = random.Random(8)
    for k in range(3):    # far rocks / reef silhouettes
        x = rng.uniform(-60, 720)
        c.arc(x, 980, rng.uniform(140, 240), 0, 2 * math.pi)
        c.set_source_rgba(*alpha(hexc("#0b3358"), 0.45))
        c.fill()
    c.move_to(0, FLOOR + 20)
    for x in range(0, W + 41, 40):
        c.line_to(x, FLOOR + 10 * math.sin(x / 70.0))
    c.line_to(W, H)
    c.line_to(0, H)
    c.close_path()
    c.set_source(lin(0, FLOOR, 0, H, [(0, hexc("#f2d79a")), (1, hexc("#b8945a"))]))
    c.fill()
    for _ in range(140):
        x, y = rng.uniform(0, W), rng.uniform(FLOOR + 20, H)
        c.arc(x, y, rng.uniform(1.5, 3.5), 0, 2 * math.pi)
        c.set_source_rgba(0.55, 0.4, 0.2, 0.35)
        c.fill()


def sea(cr, t, rays=True):
    put(cr, sprite("jelly_sea", W, H, _sea_layer), 0, 0)
    if rays:
        light_rays(cr, t, 360, -80, n=6, a=0.08, col=(0.85, 0.97, 1.0))
    particles(cr, t, 4, 40, (1, 1, 1, 0.35), r=(1.2, 3.0), speed=10)
    bubbles(cr, t)


def bubbles(cr, t, seed=3, n=10):
    rng = random.Random(seed)
    for k in range(n):
        x = rng.uniform(30, 690)
        sp = rng.uniform(60, 120)
        y = H - ((t * sp + rng.uniform(0, 1400)) % 1400)
        r = rng.uniform(5, 14)
        cr.arc(x + math.sin(t * 2 + k) * 8, y, r, 0, 2 * math.pi)
        cr.set_source_rgba(1, 1, 1, 0.18)
        cr.fill_preserve()
        cr.set_source_rgba(1, 1, 1, 0.55)
        cr.set_line_width(2)
        cr.stroke()


def rock(cr, x, y, s=1.0):
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    smooth(cr, [(-120, 10), (-110, -50), (-50, -90), (40, -84), (110, -40), (124, 10)])
    paint(cr, rad(-30, -70, 160, [(0, hexc("#8a8fa8")), (1, hexc("#4a4f68"))]), OUTLINE, 5)
    for k in range(3):
        ellipse(cr, -50 + k * 40, -50 + (k % 2) * 16, 14, 8, 0.3)
        paint(cr, alpha(hexc("#3fbf6a"), 0.6), None, 0)
    cr.restore()


def seaweed(cr, t, x, y, h=200, seed=0):
    pts = [(x + math.sin(t * 1.5 + seed + k * 0.6) * 12 * k / 5, y - h * k / 5) for k in range(6)]
    stroke_line(cr, pts, 18, OUTLINE)
    stroke_line(cr, pts, 11, hexc("#3fbf6a"))


def tombstone(cr, x, y, s=1.0, rot=0.0):
    cr.save()
    cr.translate(x, y)
    cr.rotate(rot)
    cr.scale(s, s)
    cr.new_path()
    cr.arc(0, -120, 70, math.pi, 2 * math.pi)
    cr.line_to(70, 0)
    cr.line_to(-70, 0)
    cr.close_path()
    paint(cr, lin(0, -190, 0, 0, [(0, hexc("#c4c8d4")), (1, hexc("#7a8094"))]), OUTLINE, 6)
    bold_text(cr, "R.I.P.", 0, -86, 36, hexc("#4a4f68"), outline=None, shadow=0)
    cr.restore()


def rewind_icon(cr, t, start, x, y, end=None):
    if t < start or (end is not None and t > end):
        return
    k = appear(t, start, 0.35)
    if k <= 0.01:
        return
    cr.save()
    cr.translate(x, y)
    cr.scale(k, k)
    soft_disc(cr, 0, 6, 76, (0, 0, 0, 0.3))
    cr.arc(0, 0, 70, 0, 2 * math.pi)
    paint(cr, lin(0, -70, 0, 70, [(0, shade(PURPLE, 0.4)), (1, shade(PURPLE, -0.15))]), OUTLINE, 6)
    for dx in (-26, 10):
        cr.move_to(dx + 30, -30)
        cr.line_to(dx - 6, 0)
        cr.line_to(dx + 30, 30)
        cr.close_path()
        paint(cr, WHITE, OUTLINE, 4)
    cr.restore()


def loop_arrow(cr, t, x, y, r, col=GOLD, k=1.0):
    a0 = -math.pi / 2 + t * 1.5
    cr.new_path()
    cr.arc(x, y, r, a0, a0 + 2 * math.pi * 0.82 * k)
    cr.set_line_width(20)
    cr.set_source_rgba(*OUTLINE)
    cr.stroke()
    cr.arc(x, y, r, a0, a0 + 2 * math.pi * 0.82 * k)
    cr.set_line_width(12)
    cr.set_source_rgba(*col)
    cr.stroke()
    a = a0 + 2 * math.pi * 0.82 * k
    hx, hy = x + math.cos(a) * r, y + math.sin(a) * r
    tx, ty = -math.sin(a), math.cos(a)
    nx, ny = math.cos(a), math.sin(a)
    cr.move_to(hx + tx * 30, hy + ty * 30)
    cr.line_to(hx + nx * 26, hy + ny * 26)
    cr.line_to(hx - nx * 26, hy - ny * 26)
    cr.close_path()
    paint(cr, col, OUTLINE, 4)


def tag(cr, t, start, x, y, text, col=GOLD, size=40, end=None):
    if t < start or (end is not None and t > end):
        return
    k = appear(t, start, 0.3)
    if k <= 0.01:
        return
    cr.save()
    cr.translate(x, y + math.sin(t * 4) * 4)
    cr.scale(k, k)
    bold_text(cr, text, 0, 0, size, col)
    cr.move_to(-12, 12)
    cr.line_to(12, 12)
    cr.line_to(0, 30)
    cr.close_path()
    paint(cr, col, OUTLINE, 4)
    cr.restore()


def jelly_or_polyp(cr, t, x, y, s, u, **kw):
    """Cross-fade between a jellyfish (u=0) and its polyp (u=1)."""
    if u < 1:
        cr.push_group()
        jellyfish(cr, t, x, y - 40 * u, s * (1 - 0.6 * u), **kw)
        cr.pop_group_to_source()
        cr.paint_with_alpha(1 - u)
    if u > 0:
        cr.push_group()
        polyp(cr, t, x, y + 140 * s, s * (0.5 + 0.5 * u), bonnet=True)
        cr.pop_group_to_source()
        cr.paint_with_alpha(u)


# ---------------------------------------------------------------- scenes
def scene_hook(cr, t, tl):
    A = tl.at
    sea(cr, t)
    old = A("j1", "old.")
    baby = A("j1", "baby.")
    cam = camera(t, [(0, (1.0, 360, 600)), (baby, (1.15, 360, 640))], dur=0.6)
    cr.save()
    enter(cr, cam)
    age = seg(t, A("j1", "grow"), old + 0.3) * (1 - seg(t, A("j1", "turn"), baby))
    u = seg(t, A("j1", "turn"), baby + 0.3)
    if u < 1:
        jellyfish(cr, t, 360, 520 + age * 60, 1.35 * (1 - 0.5 * u), age=age, eyes="half" if age > 0.5 else "open",
                  mouth="sad" if age > 0.5 else "smile", tilt=0.15 * age)
    if u > 0:
        polyp(cr, t, 360, 800, 1.5 * appear(t, A("j1", "turn") + 0.2, 0.4) + 0.01, bonnet=True)
    cr.restore()
    rewind_icon(cr, t, A("j1", "turn"), 600, 400, end=baby + 0.9)
    sign(cr, t, A("j1", "old."), 360, 200, "GROWS OLD...", col=hexc("#8a94a8"), size=62,
         end=A("j1", "turn") - 0.05)
    sign(cr, t, A("j1", "turn"), 360, 200, "BACK TO BABY!", col=PINK, size=66, rot=0.03)
    vignette(cr, 0.45)


def finger(cr, t, x, y, s=1.0):
    """A big fingertip coming in from the bottom right, nail up."""
    skin = SKIN["light"]
    cr.save()
    cr.translate(x, y)
    cr.rotate(-0.5)
    cr.scale(s, s)
    rrect(cr, -130, -170, 260, 800, 130)
    paint(cr, lin(-130, 0, 130, 0, [(0, shade(skin, -0.15)), (0.5, shade(skin, 0.2)), (1, shade(skin, -0.2))]),
          OUTLINE, 6)
    rrect(cr, -86, -140, 172, 220, 80)
    paint(cr, lin(0, -140, 0, 80, [(0, hexc("#ffe8ec")), (1, hexc("#f4c4c8"))]), OUTLINE, 5)
    ellipse(cr, -30, -80, 26, 50, 0.1)
    paint(cr, alpha(WHITE, 0.6), None, 0)
    cr.restore()


def scene_size(cr, t, tl):
    A = tl.at
    sea(cr, t)
    nail = A("j2", "fingernail.")
    if t < A("j2", "smaller"):
        jellyfish(cr, t, 360, 500, 1.25)
        tag(cr, t, A("j2", "immortal"), 360, 280, "IMMORTAL JELLYFISH", col=PINK, size=46)
    else:
        u = ease_out(seg(t, A("j2", "smaller"), A("j2", "smaller") + 0.6))
        finger(cr, t, lerp(900, 470, u), lerp(1300, 760, u), 1.0)
        js = lerp(1.25, 0.36, u)
        jellyfish(cr, t, lerp(360, 432, u), lerp(500, 560, u), js, eyes="happy" if t >= nail else "open",
                  mouth="grin")
        if t >= nail:
            stroke_line(cr, [(395, 470), (395, 450), (470, 450), (470, 470)], 6, WHITE, curve=False)
            bold_text(cr, "4.5 mm", 432, 432, 40, GOLD)
    sign(cr, t, A("j2", "smaller"), 360, 200, "SMALLER THAN", col=BLUE, size=58, sub="YOUR LITTLE FINGERNAIL",
         sub_col=WHITE)
    vignette(cr, 0.45)


def scene_cycle(cr, t, tl):
    A = tl.at
    sea(cr, t)
    j4 = A("j4")
    grows, babies, dies = A("j4", "grows"), A("j4", "babies."), A("j4", "dies.")
    seaweed(cr, t, 80, FLOOR + 10, 240, 1)
    seaweed(cr, t, 640, FLOOR + 10, 200, 2)
    rock(cr, 260, FLOOR + 10, 1.0)
    if t >= A("j3", "blob"):
        polyp(cr, t, 260, FLOOR - 70, 0.9 * appear(t, A("j3", "blob"), 0.4) + 0.01, eyes="happy")
    if t >= grows:
        rise = ease_out(seg(t, grows, grows + 1.0))
        fall = seg(t, dies, dies + 1.2)
        jx, jy = lerp(260, 470, rise), lerp(FLOOR - 220, 440, rise) + fall * 360
        jellyfish(cr, t, jx, jy, lerp(0.3, 0.95, rise), age=fall, eyes="x" if t >= dies + 0.3 else "open",
                  mouth="o" if t >= dies else "grin", tilt=fall * 0.6)
        if t >= babies:
            for k in range(3):
                st = babies + 0.12 * k
                if t >= st:
                    bx = jx - 120 + k * 110 + math.sin(t * 2 + k) * 10
                    jellyfish(cr, t, bx, jy + 190 - (t - st) * 20, 0.22, eyes="happy", mouth="smile", glow=0.4,
                              seed=k)
    if t >= dies + 0.5:
        tombstone(cr, 520, FLOOR + 30, 0.9 * appear(t, dies + 0.5, 0.4) + 0.01)
    sign(cr, t, A("j3", "polyp."), 360, 190, "POLYP = BABY", col=PINK, size=60, end=j4 - 0.05)
    sign(cr, t, grows, 360, 190, "GROWS UP", col=BLUE, size=62, end=babies - 0.05)
    sign(cr, t, babies, 360, 190, "HAS BABIES", col=GOLD, size=62, end=dies - 0.05)
    stamp(cr, t, dies, 360, 200, "THE END.", col=hexc("#4a4f68"), size=80)
    vignette(cr, 0.45)


def scene_cheat(cr, t, tl):
    A = tl.at
    sea(cr, t)
    st = A("j5", "cheats.")
    kick = ease_out(seg(t, st, st + 0.8))
    rock(cr, 360, FLOOR + 20, 1.2)
    tombstone(cr, lerp(520, 900, kick), FLOOR + 30 - math.sin(kick * math.pi) * 300, 0.9, rot=kick * 3)
    jellyfish(cr, t, 330, 480, 1.25, eyes="half", mouth="smug", tilt=-0.1 + 0.25 * kick)
    if t >= st:
        cue("whoosh", t, st, 0.3)
    stamp(cr, t, st, 360, 200, "IT CHEATS.", col=PINK, size=88)
    vignette(cr, 0.45)


def scene_sink(cr, t, tl):
    A = tl.at
    sea(cr, t)
    j7, j8 = A("j7"), A("j8")
    sinks = A("j6", "sinks")
    rock(cr, 600, FLOOR + 20, 0.8)
    seaweed(cr, t, 100, FLOOR + 10, 220, 3)
    if t < A("j7", "shrinks"):
        drop = ease_out(seg(t, sinks, A("j6", "floor.", end=True) + 0.4))
        jellyfish(cr, t, 360, lerp(420, FLOOR - 110, drop), 1.1, age=0.8, eyes="half", mouth="sad",
                  tilt=0.25 * math.sin(t * 1.5), pulse=False)
        if t >= A("j6", "old,"):
            bold_text(cr, "OLD", 150, 380, 52, hexc("#c4c8d4"))
        if t >= A("j6", "hurt,"):
            bold_text(cr, "HURT", 360, 330, 52, RED)
        if t >= A("j6", "sick,"):
            bold_text(cr, "SICK", 570, 380, 52, GREEN)
    else:
        sh = seg(t, A("j7", "shrinks"), A("j7", "shrinks") + 0.8)
        u = seg(t, A("j8", "turns"), A("j8", "polyp.") + 0.2) if t >= j8 else 0.0
        if sh < 1:
            jellyfish(cr, t, 360, lerp(FLOOR - 110, FLOOR - 40, sh), 1.1 * (1 - 0.7 * sh), age=0.8, eyes="closed",
                      mouth="flat", pulse=False, tentacles=sh < 0.6)
        if sh > 0 and u < 1:
            cr.push_group()
            jelly_blob(cr, t, 360, FLOOR + 5, 1.2 * appear(t, A("j7", "shrinks") + 0.3, 0.4) + 0.01,
                       eyes="closed" if t < j8 else "open", mouth="flat" if t < j8 else "o")
            cr.pop_group_to_source()
            cr.paint_with_alpha(min(1.0, sh * 2) * (1 - u))
        if u > 0:
            polyp(cr, t, 360, FLOOR + 10, 1.4 * max(u, 0.01), eyes="happy", mouth="grin", bonnet=True)
    sign(cr, t, sinks, 360, 190, "SINKS...", col=hexc("#5a6478"), size=64, end=j7 - 0.05)
    sign(cr, t, A("j7", "blob."), 360, 190, "SHRINKS TO A BLOB", col=PURPLE, size=52, end=j8 - 0.05)
    sign(cr, t, A("j8", "polyp."), 360, 190, "BABY AGAIN!", col=PINK, size=72, rot=0.03)
    rewind_icon(cr, t, A("j8", "turns"), 600, 420, end=A("j8", "polyp.") + 0.6)
    vignette(cr, 0.45)


def scene_again(cr, t, tl):
    A = tl.at
    sea(cr, t)
    st = A("j9", "grows")
    u = 1 - ease_out(seg(t, st, st + 1.2))
    loop_arrow(cr, t, 360, 560, 250, GOLD, appear(t, A("j9"), 0.6))
    jelly_or_polyp(cr, t, 360, 500, 1.1, u, eyes="happy", mouth="grin")
    sign(cr, t, A("j9", "again."), 360, 190, "AGAIN!", col=GOLD, size=84, rot=-0.04)
    vignette(cr, 0.45)


def cell(cr, t, x, y, r, hat, col, seed=0):
    cr.save()
    cr.translate(x, y + math.sin(t * 2.5 + seed) * 5)
    cr.arc(0, 0, r, 0, 2 * math.pi)
    paint(cr, rad(-r * 0.3, -r * 0.3, r * 1.3, [(0, shade(col, 0.5)), (1, col)]), OUTLINE, 5)
    cr.arc(r * 0.15, r * 0.1, r * 0.32, 0, 2 * math.pi)
    paint(cr, alpha(shade(col, -0.35), 0.7), None, 0)
    for side in (-1, 1):
        ellipse(cr, side * r * 0.32, -r * 0.2, r * 0.1, r * 0.14)
        paint(cr, OUTLINE, None, 0)
    cr.arc(0, r * 0.15, r * 0.22, 0.2, math.pi - 0.2)
    paint(cr, None, OUTLINE, 4)
    if hat == "jelly":     # a tiny jellyfish-bell cap
        cr.new_path()
        cr.arc(0, -r * 0.82, r * 0.5, math.pi, 2 * math.pi)
        cr.close_path()
        paint(cr, alpha(hexc("#ffb3c7"), 0.95), OUTLINE, 4)
        for k in range(4):
            stroke_line(cr, [(-r * 0.4 + k * r * 0.26, -r * 0.8), (-r * 0.4 + k * r * 0.26, -r * 0.6)], 3,
                        alpha(OUTLINE, 0.6), curve=False)
    else:                  # a baby bonnet
        cr.new_path()
        cr.arc(0, -r * 0.7, r * 0.6, math.pi, 2 * math.pi)
        cr.close_path()
        paint(cr, hexc("#9fd6ff"), OUTLINE, 4)
        cr.arc(0, -r * 1.32, r * 0.12, 0, 2 * math.pi)
        paint(cr, WHITE, OUTLINE, 3)
    cr.restore()


def scene_cells(cr, t, tl):
    A = tl.at
    sea(cr, t, rays=False)
    k = appear(t, A("j10"), 0.5)
    cr.save()      # the microscope view
    cr.translate(360, 560)
    cr.scale(max(k, 0.01), max(k, 0.01))
    soft_disc(cr, 0, 14, 320, (0, 0, 0, 0.4))
    cr.arc(0, 0, 300, 0, 2 * math.pi)
    cr.set_source(rad(0, 0, 300, [(0, hexc("#fff4f8")), (1, hexc("#f4c8d8"))]))
    cr.fill()
    cr.save()
    cr.arc(0, 0, 300, 0, 2 * math.pi)
    cr.clip()
    switch = A("j10", "turn")
    rng = random.Random(4)
    for j in range(7):
        a = j * 2 * math.pi / 7 + 0.3
        rr = 0 if j == 0 else 170
        x, y = math.cos(a) * rr, math.sin(a) * rr
        st = switch + 0.12 * j
        baby = t >= st
        col = hexc("#9fd6ff") if baby else hexc("#ffb3c7")
        cell(cr, t, x, y, 70 if j == 0 else 58, "baby" if baby else "jelly", col, seed=j)
        if st <= t < st + 0.4:
            soft_disc(cr, x, y, 90, (1, 1, 1, 0.6 * (1 - (t - st) / 0.4)))
    cr.restore()
    cr.arc(0, 0, 300, 0, 2 * math.pi)
    paint(cr, None, OUTLINE, 22)
    cr.arc(0, 0, 300, 0, 2 * math.pi)
    paint(cr, None, hexc("#5a6478"), 12)
    cr.restore()
    sign(cr, t, A("j10"), 360, 170, "CELLS SWITCH JOBS", col=PURPLE, size=52, end=switch - 0.05)
    sign(cr, t, switch, 360, 170, "OLD CELLS TO BABY CELLS", col=BLUE, size=44)
    vignette(cr, 0.45)


def lab_jar(cr, t, x, y, s=1.0):
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    soft_rrect(cr, -150, -330, 300, 350, 40, (0, 0, 0, 0.3), sigma=12)
    rrect(cr, -150, -340, 300, 350, 40)
    cr.set_source(lin(0, -340, 0, 10, [(0, (0.75, 0.92, 1.0, 0.55)), (1, (0.35, 0.65, 0.9, 0.65))]))
    cr.fill()
    jellyfish(cr, t, 0, -200, 0.6, eyes="happy", mouth="grin", glow=0.5)
    rrect(cr, -150, -340, 300, 350, 40)
    paint(cr, None, OUTLINE, 6)
    stroke_line(cr, [(-110, -280), (-110, -80)], 10, alpha(WHITE, 0.6), curve=False)
    rrect(cr, -160, -370, 320, 44, 14)
    paint(cr, lin(0, -370, 0, -326, [(0, hexc("#cfd5df")), (1, hexc("#8a94a8"))]), OUTLINE, 5)
    rrect(cr, -90, -150, 180, 60, 8)
    paint(cr, hexc("#fff8e6"), OUTLINE, 4)
    bold_text(cr, "SPECIMEN 1", 0, -110, 26, OUTLINE, outline=None, shadow=0, font="Fredoka")
    cr.restore()


def scene_lab(cr, t, tl):
    A = tl.at
    cr.rectangle(0, 0, W, H)
    cr.set_source(lin(0, 0, 0, H, [(0, hexc("#dff3ff")), (0.68, hexc("#bfe0f0")), (0.69, hexc("#9aa4b4")),
                                   (1, hexc("#6a7488"))]))
    cr.fill()
    bokeh(cr, t, 5, 10, [WHITE], rmin=20, rmax=60, area=(0, 0, W, 800))
    rrect(cr, 0, 860, W, 30, 0)
    paint(cr, hexc("#e8ecf2"), OUTLINE, 5)
    lab_jar(cr, t, 250, 860, 1.0)
    counter(cr, t, A("j11", "10"), 500, 470, 10, size=130, dur=1.3, suffix="X", sub="BACK TO BABY")
    if t >= A("j11", "2"):
        sign(cr, t, A("j11", "2"), 500, 660, "IN 2 YEARS", col=GOLD, size=46)
    sign(cr, t, A("j11", "lab"), 360, 160, "A LAB IN JAPAN", col=RED, size=58)
    vignette(cr, 0.35)


def scene_danger(cr, t, tl):
    A = tl.at
    sea(cr, t)
    j13 = A("j13")
    eat, dis, old = A("j13", "Fish"), A("j13", "Disease"), A("j13", "doesn't")
    rock(cr, 360, FLOOR + 20, 1.1)
    if t < j13:
        jellyfish(cr, t, 360, 480, 1.2, eyes="open", mouth="smile")
        stamp(cr, t, A("j12", "immortal?"), 360, 200, "IMMORTAL?", col=PURPLE, size=80, rot=-0.06)
        sign(cr, t, A("j12", "Not"), 360, 340, "NOT QUITE.", col=RED, size=64, rot=0.04)
    elif t < dis:
        u = seg(t, eat, eat + 0.9)
        if u < 0.75:
            jellyfish(cr, t, 400, 480, 0.9, eyes="wide", mouth="o")
        fish(cr, t, lerp(-200, 520, ease_out(u)), 480, 1.3, mouth_open=1.0 if u < 0.7 else 0.0)
        if u > 0.7:
            cue("hit", t, eat + 0.63)
        sign(cr, t, eat, 360, 190, "FISH EAT IT", col=hexc("#ff9a3c"), size=64)
    elif t < old:
        jellyfish(cr, t, 360, 480, 1.1, eyes="half", mouth="sad", age=0.3)
        for k in range(5):
            gx, gy = 260 + k * 50, 420 + 40 * math.sin(t * 3 + k)
            cr.arc(gx, gy, 10, 0, 2 * math.pi)
            paint(cr, alpha(hexc("#7ac84a"), 0.85), OUTLINE, 3)
        sign(cr, t, dis, 360, 190, "DISEASE", col=GREEN, size=72)
    else:
        jellyfish(cr, t, 360, 480, 1.2, eyes="happy", mouth="grin")
        sign(cr, t, old, 360, 190, "BUT NOT OLD AGE", col=PINK, size=58, rot=0.03)
    vignette(cr, 0.45)


def scene_end(cr, t, tl):
    A = tl.at
    sea(cr, t)
    jellyfish(cr, t, 360, 640, 0.9, eyes="happy", mouth="grin")
    sign(cr, t, A("j14"), 360, 170, "GO BACK TO WHICH AGE?", col=PINK, size=48)
    for k, (lab, col) in enumerate((("5", BLUE), ("10", GREEN), ("18", GOLD), ("25", PURPLE))):
        st = A("j14", "age") + 0.12 * k if t >= A("j14", "age") else 1e9
        if t < st:
            continue
        kk = appear(t, st, 0.35)
        x, y = 120 + k * 160, 360
        cr.save()
        cr.translate(x, y + math.sin(t * 3 + k) * 5)
        cr.scale(kk, kk)
        soft_disc(cr, 0, 10, 72, (0, 0, 0, 0.3))
        cr.arc(0, 0, 66, 0, 2 * math.pi)
        paint(cr, rad(-20, -25, 90, [(0, shade(col, 0.45)), (1, shade(col, -0.2))]), OUTLINE, 6)
        bold_text(cr, lab, 0, 22, 62, WHITE)
        cr.restore()
        cue("pop", t, st)
    vignette(cr, 0.45)


SCENES = {"hook": scene_hook, "size": scene_size, "cycle": scene_cycle, "cheat": scene_cheat, "sink": scene_sink,
          "again": scene_again, "cells": scene_cells, "lab": scene_lab, "danger": scene_danger, "end": scene_end}


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    SCENES[name](cr, t, tl)
    cr.restore()
    captions(cr, t, tl)
