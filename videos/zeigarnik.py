"""Hook test H5 (abstract concept): "The Zeigarnik Effect" -- ends mid-sentence so it loops.

Script: out/scripts_hook_test.md, H5 (owner approved 15 Oct 2026). Bluma Zeigarnik's 1927 study of interrupted tasks;
the café-waiter story is the classic account of how it started (later replications are mixed, so the script says
"people remembered", not "always"). Turbo voice with tags (narrator only).
"""
import math

from motion import thriller as th
from motion.engine import W, H, cue, ease_out, hexc, lerp, seg
from motion.kit import whip
from motion.polish import (OUTLINE, WHITE, appear, bold_text, camera, captions, ellipse, enter, lin, paint, rad,
                           rrect, sign, soft_disc, stamp, stroke_line, vignette)
from motion.toons import person
from videos.last_bencher_4 import BLUE, GOLD, GREEN, PURPLE, RED, sparkles, studio

NARRATOR = dict(turbo=True)
TAIL = 0.0          # it stops dead, mid-sentence, and loops back to the first frame
SEPIA = hexc("#d9b98a")

SCRIPT = [
    dict(id="b1", scene="tv", text="There's a reason you can't stop thinking about an unfinished show. It's called "
                                   "the [Zay-gar-nik|Zeigarnik] effect."),
    dict(id="b2", scene="cafe", text="In the [nineteen twenties,|1920s,] a psychologist named Bluma "
                                     "[Zay-gar-nik|Zeigarnik] sat in a busy cafe in Berlin."),
    dict(id="b3", scene="cafe", text="She noticed something strange about the waiters."),
    dict(id="b4", scene="orders", text="They remembered every order that wasn't paid yet. Perfectly."),
    dict(id="b5", scene="orders", text="But once a table paid, they forgot it almost instantly."),
    dict(id="b6", scene="test", text="So she tested it. People remembered unfinished tasks much better than finished "
                                     "ones."),
    dict(id="b7", scene="tabs", text="Your brain keeps a tab open for anything unfinished. That's why cliffhangers "
                                     "work. [chuckle]"),
    dict(id="b8", scene="cut", text="And that's exactly why I'm going to stop this video right..."),
]

METADATA = dict(
    title="Your Brain Can't Let This Go 🧠",
    alt_titles=["Why You Can't Stop Thinking About Cliffhangers 🧠", "The Zeigarnik Effect in 40 Seconds"],
    description="""There's a reason you can't stop thinking about an unfinished show. It's called the Zeigarnik effect. 🧠

In the 1920s, psychologist Bluma Zeigarnik noticed that waiters in a busy Berlin café remembered every unpaid order perfectly... and forgot them as soon as the table paid. Her experiments found that people remember unfinished tasks better than finished ones.

Your brain keeps a "tab" open for anything unfinished. That's why cliffhangers work. And that's exactly why this video ends...

💬 What's the one cliffhanger you still think about? 👇

🔔 Interestingly Strange: weird psychology, clever twists and mind-bending paradoxes, animated in under a minute.""",
    hashtags=["#Psychology", "#Brain", "#Shorts"],
    tags=["zeigarnik effect", "psychology facts", "brain facts", "cliffhanger", "why cant i stop thinking",
          "bluma zeigarnik", "memory", "mind blowing", "psychology", "interestingly strange"],
    pinned_comment="What's the one cliffhanger you STILL think about? 📺 👇",
)


def tv(cr, t, x, y, s, label="TO BE CONTINUED..."):
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    rrect(cr, -280, -190, 560, 380, 30)
    paint(cr, hexc("#2a2a33"), OUTLINE, 10)
    rrect(cr, -250, -165, 500, 320, 16)
    paint(cr, lin(0, -165, 0, 155, [(0, hexc("#3a4a7a")), (1, hexc("#1a1a3a"))]), OUTLINE, 5)
    for k in range(12):                                            # scanlines
        cr.rectangle(-250, -165 + k * 27, 500, 3)
        cr.set_source_rgba(1, 1, 1, 0.05)
        cr.fill()
    rrect(cr, -40, -50, 26, 90, 6)                                 # pause symbol
    paint(cr, WHITE, None)
    rrect(cr, 14, -50, 26, 90, 6)
    paint(cr, WHITE, None)
    bold_text(cr, label, 0, 120, 34, GOLD)
    stroke_line(cr, [(-80, 190), (-140, 260)], 12, OUTLINE, curve=False)
    stroke_line(cr, [(80, 190), (140, 260)], 12, OUTLINE, curve=False)
    cr.restore()


def scene_tv(cr, t, tl):
    A = tl.at
    cr.rectangle(0, 0, W, H)
    cr.set_source(lin(0, 0, 0, H, [(0, hexc("#141428")), (1, hexc("#2a1a3a"))]))
    cr.fill()
    soft_disc(cr, 360, 640, 420, (0.4, 0.5, 1.0, 0.25))
    cr.save()
    enter(cr, camera(t, [(0.0, (1.0, 360, 640)), (A("b1", "called"), (1.12, 360, 620))], dur=1.0))
    tv(cr, t, 360, 620, 1.0)
    cr.restore()
    sign(cr, t, A("b1", "called"), 360, 330, "THE ZEIGARNIK EFFECT", col=PURPLE, size=48)
    vignette(cr, 0.45)


def cafe_bg(cr, t):
    cr.rectangle(0, 0, W, H)
    cr.set_source(lin(0, 0, 0, H, [(0, hexc("#5a3a22")), (0.55, hexc("#8a5e3a")), (0.56, hexc("#b88a5a")),
                                   (1, hexc("#7a5434"))]))
    cr.fill()
    for k, x in enumerate((120, 360, 600)):                        # hanging lamps
        stroke_line(cr, [(x, 0), (x, 160)], 4, OUTLINE, curve=False)
        cr.arc(x, 180, 34, math.pi, 2 * math.pi)
        paint(cr, GOLD, OUTLINE, 4)
        soft_disc(cr, x, 230, 140, (1, 0.85, 0.5, 0.25 + 0.05 * math.sin(t * 3 + k)))
    for k, x in enumerate((150, 570)):                             # tables
        ellipse(cr, x, 800, 120, 30)
        paint(cr, WHITE, OUTLINE, 6)
        stroke_line(cr, [(x, 830), (x, 960)], 12, OUTLINE, curve=False)


def scene_cafe(cr, t, tl):
    A = tl.at
    cafe_bg(cr, t)
    cr.save()
    enter(cr, camera(t, [(A("b2") - 0.3, (1.0, 360, 640)), (A("b3", "waiters."), (1.25, 420, 600))], dur=0.8))
    person(cr, t, 200, 980, 0.8, "teacher", eyes="open" if t < A("b3", "strange") else "wide",
           mouth="smile" if t < A("b3", "strange") else "o", arms=("front", "front"), look=(0.6, 0))
    walk = (t - A("b2")) * 9
    wx = 460 + 90 * math.sin((t - A("b2")) * 0.9)
    person(cr, t, wx, 980, 0.8, "reporter", fedora=None, suit=hexc("#1a1a1a"), shirt=WHITE, tie=hexc("#1a1a1a"),
           eyes="open", mouth="smile", arms=("hold", "down"), walk=walk, seed=4)
    cr.restore()
    sign(cr, t, A("b2", "nineteen"), 360, 160, "BERLIN, 1920s", col=SEPIA, size=58, end=A("b2", "psychologist") - 0.05)
    sign(cr, t, A("b2", "psychologist"), 360, 160, "BLUMA ZEIGARNIK", col=PURPLE, size=54, end=A("b3") - 0.05)
    sign(cr, t, A("b3", "strange"), 360, 160, "THE WAITERS...", col=GOLD, size=60)
    vignette(cr, 0.5)


def bubble(cr, x, y, s, text, col):
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    rrect(cr, -95, -45, 190, 90, 26)
    paint(cr, col, OUTLINE, 6)
    bold_text(cr, text, 0, 14, 34, WHITE)
    cr.restore()


def scene_orders(cr, t, tl):
    A = tl.at
    cafe_bg(cr, t)
    paid = A("b5", "paid,")
    orders = (("COFFEE", 160, 560), ("CAKE", 560, 520), ("TEA", 360, 420), ("SOUP", 200, 330), ("PIE", 540, 300))
    for k, (txt, x, y) in enumerate(orders):
        st = A("b4") + 0.2 * k
        if t < st:
            continue
        gone = k < 3 and t >= paid + 0.25 * k
        if gone:                                                    # paid: a coin drops, the bubble pops
            u = seg(t, paid + 0.25 * k, paid + 0.25 * k + 0.4)
            if u < 1:
                bubble(cr, x, y, 1 - u, txt, GREEN)
                cue("kaching", t, paid + 0.25 * k)
            continue
        glow = 0.6 + 0.4 * math.sin(t * 5 + k)
        soft_disc(cr, x, y, 110, (1, 0.9, 0.4, 0.35 * glow))
        bubble(cr, x, y + 6 * math.sin(t * 2 + k), appear(t, st, 0.3), txt, RED)
        cue("pop", t, st)
    sign(cr, t, A("b4", "Perfectly."), 360, 140, "NOT PAID = REMEMBERED", col=RED, size=46, end=paid - 0.05)
    sign(cr, t, paid, 360, 140, "PAID = FORGOTTEN", col=GREEN, size=54)
    vignette(cr, 0.45)


def scene_test(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#d8e4ff"), hexc("#fff6e8"), seed=3)
    for side, (label, col, key) in enumerate((("DONE", hexc("#9aa3b5"), "finished"), ("NOT DONE", RED, "unfinished"))):
        x = 200 + side * 320
        st = A("b6", key)
        if t < st:
            continue
        for k in range(5):                                          # a pile of task cards
            a = 1.0 if side else max(0.15, 1 - seg(t, st + 0.4, st + 1.6))
            cr.save()
            cr.translate(x + (k % 2) * 10 - 5, 760 - k * 38)
            cr.rotate(0.06 * (k - 2))
            rrect(cr, -110, -30, 220, 60, 10)
            paint(cr, (*col[:3], a), (*OUTLINE[:3], a), 5)
            cr.restore()
        if side:
            soft_disc(cr, x, 640, 200, (1, 0.4, 0.3, 0.25 + 0.1 * math.sin(t * 4)))
        sign(cr, t, st, x, 470, label, col=col, size=46)
    sign(cr, t, A("b6", "tested"), 360, 160, "THE EXPERIMENT", col=PURPLE, size=58)
    vignette(cr, 0.3)


def scene_tabs(cr, t, tl):
    A = tl.at
    cr.rectangle(0, 0, W, H)
    cr.set_source(lin(0, 0, 0, H, [(0, hexc("#1a2448")), (1, hexc("#2a1a48"))]))
    cr.fill()
    ellipse(cr, 360, 640, 250, 280)                                 # a head (silhouette)
    paint(cr, hexc("#3a4a7a"), OUTLINE, 8)
    n = int(1 + 7 * seg(t, A("b7"), A("b7", "unfinished.", end=True)))
    for k in range(n):                                              # browser tabs stacking up inside it
        x, y = 240 + (k % 3) * 120, 470 + (k // 3) * 90
        rrect(cr, x - 55, y - 30, 110, 60, 12)
        paint(cr, (BLUE, GOLD, GREEN, PURPLE, RED)[k % 5], OUTLINE, 4)
        bold_text(cr, "x", x + 36, y + 10, 26, WHITE)
        cue("pop", t, A("b7") + 0.15 * k)
    sign(cr, t, A("b7", "tab"), 360, 170, "1 TAB PER UNFINISHED THING", col=GOLD, size=40)
    vignette(cr, 0.4)


def scene_cut(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#cdb8ff"), hexc("#fff1d6"), seed=8)
    tv(cr, t, 360, 600, 0.8, "")
    sign(cr, t, A("b8", "stop"), 360, 170, "STOPPING RIGHT...", col=RED, size=56)
    if t >= A("b8", "right...") + 0.25:                            # hard cut to black, mid-word
        cr.set_source_rgba(0, 0, 0, 1)
        cr.paint()
    vignette(cr, 0.3)


SCENES = {"tv": scene_tv, "cafe": scene_cafe, "orders": scene_orders, "test": scene_test, "tabs": scene_tabs,
          "cut": scene_cut}


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    SCENES[name](cr, t, tl)
    cr.restore()
    th.hook(cr, t, [("YOUR BRAIN", False), ("HATES THIS", True)], end=tl.at("b1", "called"), y=170, size=100)
    if t < tl.at("b8", "right...") + 0.25:
        captions(cr, t, tl)
