"""Funny history F2: "Two Cities Went to War. Over a Bucket." -- reference narration style (talks to the viewer, chat
and customer-support jokes on medieval history).

Script: out/scripts_funny_history.md, F2 narration-style version (owner approved 15 Oct 2026). Battle of Zappolino,
1325: Bologna ~30,000 infantry + ~2,000 cavalry vs Modena ~5,000 infantry + ~2,000 cavalry; Modena won. The stolen
bucket is the famous legend (historians tie the war to Guelph-Ghibelline politics; the script says so); a bucket is
kept in Modena's Ghirlandina tower. Turbo voice with tags (narrator only).
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
TAIL = 0.9
MOD = hexc("#f2c230")     # Modena's colours
BOL = hexc("#d8453c")     # Bologna's

SCRIPT = [
    dict(id="b1", scene="hook", text="In [thirteen twenty-five,|1325,] two cities in Italy went to war. Over a bucket. "
                                     "Not gold. Not land. A bucket."),
    dict(id="b2", scene="night", text="The legend says some soldiers from Modena sneak into Bologna at night, and "
                                      "steal the bucket from the town well."),
    dict(id="b3", scene="chat", text="Bologna. Give it back. Modena. Left on seen. [chuckle]"),
    dict(id="b4", scene="armies", text="So Bologna sends an army. Thirty thousand soldiers. For a bucket."),
    dict(id="b5", scene="armies", text="Modena has seven thousand. And the bucket."),
    dict(id="b6", scene="win", text="Now you're thinking, easy win for Bologna, right? [gasp] Modena wins."),
    dict(id="b7", scene="tower", text="Historians say the real reason was politics. Fine. But the bucket? Still in "
                                      "Modena. Seven hundred years. Locked in a tower, like a trophy."),
    dict(id="b8", scene="support", text="Bologna's return request is still pending. Customer support never replied. "
                                        "[laugh]"),
    dict(id="b9", scene="end", text="What's the smallest thing someone ever fought you over?", gap=0.3),
]

METADATA = dict(
    title="Two Cities Went to War. Over a Bucket. 🪣",
    alt_titles=["The Dumbest War in History? 🪣", "30,000 Soldiers. 1 Bucket. 700 Years Later..."],
    description="""In 1325, two cities in Italy went to war. Over a bucket. Not gold. Not land. A bucket. 🪣

The legend says soldiers from Modena sneaked into Bologna and stole the bucket from the town well. Bologna sent about 30,000 soldiers. Modena had about 7,000... and won.

Historians say the real reasons were politics. But the bucket is still in Modena, 700 years later, kept in a tower like a trophy. 😂

(Battle of Zappolino, 1325. Army sizes are historians' estimates.)

💬 What's the smallest thing someone ever fought you over? 👇

🔔 Interestingly Strange: funny history, clever twists and mind-bending paradoxes, animated in under a minute.""",
    hashtags=["#FunnyHistory", "#History", "#Shorts"],
    tags=["war of the bucket", "battle of zappolino", "funny history", "weird history", "italy history",
          "dumbest war", "history facts", "medieval history", "bucket war", "interestingly strange"],
    pinned_comment="My sibling once fought me over the TV remote for 3 days 📺 Yours? 👇",
)


def bucket(cr, x, y, s=1.0, glow=0.0):
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    if glow:
        soft_disc(cr, 0, -50, 140, (1, 0.85, 0.3, 0.45 * glow))
    cr.move_to(-55, -100)
    cr.line_to(55, -100)
    cr.line_to(42, 0)
    cr.line_to(-42, 0)
    cr.close_path()
    paint(cr, lin(-55, 0, 55, 0, [(0, hexc("#a8713e")), (0.5, hexc("#d9a46a")), (1, hexc("#8a5a2e"))]), OUTLINE, 6)
    for yy in (-80, -25):
        stroke_line(cr, [(-52, yy), (52, yy)], 7, hexc("#5a5a66"), curve=False)
    cr.arc(0, -100, 52, math.pi, 2 * math.pi)                      # handle
    cr.set_line_width(6)
    cr.set_source_rgba(*OUTLINE)
    cr.stroke()
    cr.restore()


def soldier(cr, t, x, y, s, side, k=0, march=False, holding=False):
    col = MOD if side == "mod" else BOL
    hold = (lambda c, hx, hy: bucket(c, hx + 10, hy + 40, 0.45)) if holding else None
    person(cr, t, x, y, s, "achilles", shirt=col, facing=1 if side == "mod" else -1, eyes="open",
           mouth="grin" if holding else "flat", arms=("hold", "down") if holding else ("down", "down"),
           walk=(t * 8 + k) if march else None, hold=hold, seed=k, shadow=False)


def army(cr, t, side, n, x0, x1, y0, s, march=False):
    cols = max(1, int(round(math.sqrt(n * 2))))
    rows = max(1, math.ceil(n / cols))
    for r in range(rows):
        for c in range(cols):
            if r * cols + c >= n:
                return
            x = lerp(x0, x1, c / max(1, cols - 1)) + (r % 2) * 10
            soldier(cr, t, x, y0 + r * 46 * s, s * (0.9 + 0.1 * r / max(1, rows)), side, k=r * 7 + c, march=march)


def scene_hook(cr, t, tl):
    A = tl.at
    cr.rectangle(0, 0, W, H)
    cr.set_source(lin(0, 0, 0, H, [(0, hexc("#9fd6ff")), (0.5, hexc("#e8f6ff")), (0.51, hexc("#b8d88a")),
                                   (1, hexc("#7aa84a"))]))
    cr.fill()
    cr.save()
    enter(cr, camera(t, [(0.0, (1.0, 360, 860)), (A("b1", "bucket."), (1.12, 360, 880))], dur=0.8))
    army(cr, t, "mod", 6, 50, 230, 820, 0.55)
    army(cr, t, "bol", 9, 470, 680, 820, 0.55)
    bucket(cr, 360, 1000, 1.3, glow=0.6 + 0.4 * math.sin(t * 4))
    cr.restore()
    for k, key in enumerate(("gold.", "land.")):
        if t >= A("b1", key):
            stamp(cr, t, A("b1", key), 360, 1000 + k * 110, "NOT " + key.rstrip(".").upper(), col=RED, size=56)
    sign(cr, t, A("b1", "Italy"), 360, 360, "ITALY, 1325", col=PURPLE, size=56, end=A("b1", "gold.") - 0.05)
    vignette(cr, 0.3)


def scene_night(cr, t, tl):
    A = tl.at
    cr.rectangle(0, 0, W, H)
    cr.set_source(lin(0, 0, 0, H, [(0, hexc("#0e1630")), (1, hexc("#26365a"))]))
    cr.fill()
    cr.arc(560, 220, 50, 0, 2 * math.pi)
    paint(cr, hexc("#fff3c4"), None)
    rrect(cr, 260, 760, 200, 140, 10)                              # the well
    paint(cr, hexc("#7a7a88"), OUTLINE, 7)
    stroke_line(cr, [(270, 760), (270, 560), (450, 560), (450, 760)], 12, hexc("#6a4a2a"), curve=False)
    lift = seg(t, A("b2", "steal"), A("b2", "well.", end=True))
    sneak = lerp(-60, 200, seg(t, A("b2", "sneak"), A("b2", "night,", end=True)))
    for k in range(2):
        soldier(cr, t, sneak - k * 110, 1000, 0.6, "mod", k=k, march=True,
                holding=(k == 0 and lift >= 1))
    if lift < 1:
        bucket(cr, 360, lerp(740, 640, lift), 0.6)
    sign(cr, t, A("b2", "legend"), 360, 150, "THE LEGEND", col=GOLD, size=64, end=A("b2", "steal") - 0.05)
    stamp(cr, t, A("b2", "steal"), 360, 380, "STOLEN", col=RED, size=80)
    vignette(cr, 0.45)


def chat_bubble(cr, t, start, x, y, who, text, col, right=False, seen=False):
    if t < start:
        return
    k = appear(t, start, 0.3)
    cr.save()
    cr.translate(x, y)
    cr.scale(k, k)
    w = 500
    rrect(cr, -w / 2, -80, w, 160, 34)
    paint(cr, col, OUTLINE, 6)
    bold_text(cr, who, -w / 2 + 28, -24, 36, WHITE, align="left", ow=5)
    bold_text(cr, text, -w / 2 + 28, 50, 58, WHITE, align="left", ow=7)
    cr.restore()
    if seen:
        bold_text(cr, "Seen ✓✓", x + 150, y + 125, 38, hexc("#4a8ad8"), outline=None, shadow=0)


def scene_chat(cr, t, tl):
    A = tl.at
    rrect(cr, 0, 0, W, H, 0)
    paint(cr, hexc("#ece5dd"), None)
    rrect(cr, 0, 0, W, 130, 0)
    paint(cr, hexc("#1f8a70"), None)
    bold_text(cr, "MODENA vs BOLOGNA", 360, 85, 40, WHITE, ow=6)
    chat_bubble(cr, t, A("b3", "Bologna."), 300, 330, "BOLOGNA", "Give it back.", BOL)
    cue("pop", t, A("b3", "Bologna."))
    seen = t >= A("b3", "seen.")
    chat_bubble(cr, t, A("b3", "Modena."), 420, 540, "MODENA", "...", MOD, right=True, seen=seen)
    if seen:
        stamp(cr, t, A("b3", "seen."), 360, 760, "LEFT ON SEEN", col=PURPLE, size=64)
    vignette(cr, 0.2)


def scene_armies(cr, t, tl):
    A = tl.at
    cr.rectangle(0, 0, W, H)
    cr.set_source(lin(0, 0, 0, H, [(0, hexc("#ffd6a8")), (0.5, hexc("#fff0d8")), (0.51, hexc("#c8d88a")),
                                   (1, hexc("#8aa84a"))]))
    cr.fill()
    if t < A("b5"):
        n = 6 + int(34 * seg(t, A("b4", "army."), A("b4", "soldiers.", end=True)))
        army(cr, t, "bol", n, 60, 660, 700, 0.32, march=True)
        count = int(30000 * ease_out(seg(t, A("b4", "Thirty"), A("b4", "soldiers.", end=True))))
        if t >= A("b4", "Thirty"):
            bold_text(cr, f"{count:,}", 360, 330, 110, BOL)
        sign(cr, t, A("b4", "bucket."), 360, 180, "...FOR A BUCKET", col=PURPLE, size=56)
    else:
        army(cr, t, "mod", 10, 160, 560, 760, 0.42)
        if t >= A("b5", "bucket."):
            soldier(cr, t, 360, 1060, 0.75, "mod", k=9, holding=True)
        bold_text(cr, "7,000", 360, 330, 110, MOD)
        sign(cr, t, A("b5", "bucket."), 360, 180, "+ 1 BUCKET", col=GOLD, size=64)
    vignette(cr, 0.3)


def scene_win(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#ffe7a8"), hexc("#fff6e8"), seed=4)
    if t < A("b6", "Modena"):
        bold_text(cr, "30,000  vs  7,000", 360, 520, 70, hexc("#2b1d16"), outline=None, shadow=0)
        sign(cr, t, A("b6", "easy"), 360, 230, "EASY WIN... RIGHT?", col=BLUE, size=56)
    else:
        stamp(cr, t, A("b6", "Modena"), 360, 420, "MODENA WINS", col=GREEN, size=86)
        bucket(cr, 360, 860, 1.4, glow=1.0)
        sparkles(cr, t, A("b6", "wins."), 360, 760, n=12, seed=3, col=GOLD, spread=220)
        cue("hit", t, A("b6", "Modena"))
    vignette(cr, 0.3)


def scene_tower(cr, t, tl):
    A = tl.at
    cr.rectangle(0, 0, W, H)
    cr.set_source(lin(0, 0, 0, H, [(0, hexc("#9fd0ff")), (1, hexc("#fff1d6"))]))
    cr.fill()
    rrect(cr, 250, 160, 220, 900, 8)                               # the Ghirlandina tower
    paint(cr, lin(250, 0, 470, 0, [(0, hexc("#e8dcc8")), (1, hexc("#c9b89a"))]), OUTLINE, 8)
    cr.move_to(240, 170)
    cr.line_to(360, 20)
    cr.line_to(480, 170)
    cr.close_path()
    paint(cr, hexc("#c9b89a"), OUTLINE, 8)
    for k in range(5):
        rrect(cr, 330, 260 + k * 150, 60, 90, 30)
        paint(cr, hexc("#5a4a3a"), OUTLINE, 4)
    if t >= A("b7", "bucket?"):                                   # the bucket in its glass case
        k = appear(t, A("b7", "bucket?"), 0.4)
        rrect(cr, 260, 520 - 120 * k, 200, 220 * k, 12)
        paint(cr, (0.85, 0.95, 1.0, 0.5), OUTLINE, 6)
        bucket(cr, 360, 690, 0.8 * k, glow=1.0)
    sign(cr, t, A("b7", "politics."), 360, 150, "HISTORIANS: POLITICS", col=BLUE, size=48, end=A("b7", "bucket?") - 0.05)
    sign(cr, t, A("b7", "Seven"), 360, 150, "700 YEARS LATER", col=PURPLE, size=60)
    stamp(cr, t, A("b7", "trophy."), 360, 330, "TROPHY", col=GOLD, size=70)
    vignette(cr, 0.3)


def scene_support(cr, t, tl):
    A = tl.at
    rrect(cr, 0, 0, W, H, 0)
    paint(cr, hexc("#eef1f6"), None)
    rrect(cr, 80, 220, 560, 520, 24)
    paint(cr, WHITE, OUTLINE, 6)
    bold_text(cr, "RETURN REQUEST #1325", 360, 300, 38, hexc("#2b1d16"), outline=None, shadow=0)
    bold_text(cr, "Item: 1 bucket", 120, 400, 36, hexc("#555566"), align="left", outline=None, shadow=0)
    bold_text(cr, "Opened: 1325", 120, 460, 36, hexc("#555566"), align="left", outline=None, shadow=0)
    yrs = int(1325 + 701 * ease_out(seg(t, A("b8"), A("b8", "pending.", end=True))))
    bold_text(cr, f"Today: {yrs}", 120, 520, 36, hexc("#555566"), align="left", outline=None, shadow=0)
    stamp(cr, t, A("b8", "pending."), 360, 640, "PENDING", col=GOLD, size=70)
    if t >= A("b8", "Customer"):
        rrect(cr, 120, 790, 480, 90, 20)
        paint(cr, hexc("#dfe6ef"), OUTLINE, 4)
        dots = "." * (1 + int(t * 3) % 3)
        bold_text(cr, "Support is typing" + dots, 150, 848, 34, hexc("#6a6a7a"), align="left", outline=None, shadow=0)
    vignette(cr, 0.2)


def scene_end(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#cdb8ff"), hexc("#fff1d6"), seed=8)
    sign(cr, t, A("b9"), 360, 200, "SMALLEST FIGHT EVER?", col=GOLD, size=58)
    bucket(cr, 360, 720, 1.6, glow=0.5 + 0.5 * math.sin(t * 3))
    vignette(cr, 0.3)


SCENES = {"hook": scene_hook, "night": scene_night, "chat": scene_chat, "armies": scene_armies, "win": scene_win,
          "tower": scene_tower, "support": scene_support, "end": scene_end}


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    SCENES[name](cr, t, tl)
    cr.restore()
    th.hook(cr, t, [("WAR.", False), ("OVER A BUCKET.", True)], end=tl.at("b1", "gold."), y=170, size=100)
    captions(cr, t, tl)
