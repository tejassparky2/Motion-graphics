"""Bench Three, Part 1, in the illustrated 2D style. A new Midnight with Nancy series, written from the 28 Oct research
(reports/Psychological death game design.md) and approved by the owner on 28 Oct 2026 ("Approved bench three, make
it"). Script: out/horror/scripts_bench_three_part1.md.

At 9:00:00 a text from ···0141 says fifty thousand dollars are under the third bench in Hollow Park; four seconds later,
"Sorry. Wrong number." It's the bench you eat lunch on every day. Under it, an envelope. At home you count it. At 11:31
a different number, ···0142: "I watched you take it. It belongs to a man who hurts people. He checks that bench at
midnight. Put it back before then, and he never learns your name." Then a photo of you on your bench, dated three
weeks ago. The envelope's back, in pen: "Thank you for coming." The vote: put it back, or keep it.

Clues on screen, never spoken: the first text is stamped 9:00:00; the two numbers are one digit apart; in the photo,
someone on the next bench holds two phones. The texts and the note are read in the same calm voice (one man; the
truth sheet is in the script file).

    /home/user/.venv-main/bin/python channels/horror/make_2d.py bench3_p1_2d   -> out/horror/bench3_p1_2d.mp4
"""
import math

from motion import audio, voice
from motion.engine import W, H, cairo, clamp01, cue, seg

from channels.horror import hud, hud2d, sound  # noqa: F401  (sound registers the horror effects)
from channels.horror import toon2d as tk
from channels.horror import tower9_n3_2d as n3   # the round insets and the series chip
from channels.horror.toon2d import INK, curve, glow, grade, hexa, noise, poly, toon

NARRATOR = dict(turbo=True)
TAIL = 2.0                     # the vote card stays up ~2 s
MUSIC = "horror"
TWIST = "b14"                  # the bed drops out under "Thank you for coming."
voice.SPEAKERS["texter"] = dict(voice="bm_lewis", turbo_ref="bm_lewis")    # the texts and the note: one calm voice
audio.GAINS.update(sting=0.5, click=0.5)

SCRIPT = [
    dict(id="b1", scene="face", text="Nine o'clock. A text from a number you don't know. Fifty thousand dollars. Under "
                                     "the third bench in Hollow Park."),
    dict(id="b2", scene="thread", text="Four seconds later.", gap=0.4),
    dict(id="b3", scene="thread", text="Sorry. Wrong number.", speaker="texter", gap=0.3),
    dict(id="b4", scene="bench", text="The third bench is your bench. You eat lunch there every day.", gap=0.5),
    dict(id="b5", scene="envelope", text="Under it, taped to the wood, an envelope."),
    dict(id="b6", scene="count", text="At home, you count it. Fifty thousand.", gap=0.45),
    dict(id="b7", scene="thread2", text="[Eleven thirty-one.|11:31.] A different number.", gap=0.5),
    dict(id="b8", scene="thread2", text="I watched you take it. It belongs to a man who hurts people.",
         speaker="texter", gap=0.35),
    dict(id="b9", scene="thread2", text="He checks that bench at midnight. Put it back before then, and he never "
                                        "learns your name.", speaker="texter", gap=0.3),
    dict(id="b10", scene="photo", text="Then a photo. You, on your bench. Eating lunch.", gap=0.45),
    dict(id="b11", scene="date", text="It's dated three weeks ago.", gap=0.3),
    dict(id="b12", scene="turn", text="You turn the envelope over.", gap=0.5),
    dict(id="b13", scene="note", text="In pen.", gap=0.3),
    dict(id="b14", scene="note", text="Thank you for coming.", speaker="texter", gap=0.35),
    dict(id="b15", scene="face2", text="It was never a wrong number.", gap=0.7),
    dict(id="b16", scene="split", text="Someone chose your bench three weeks ago. And wants you back there tonight.",
         gap=0.4),
    dict(id="b17", scene="dark", text="Put it back, and you walk out there alone. At midnight.", gap=0.4),
    dict(id="b18", scene="door", text="Keep it, and his money stays in your room. And he knows your face.", gap=0.3),
    dict(id="b19", scene="card", text="Put it back? Or keep it?", gap=0.35),
]

METADATA = dict(
    title="A Wrong Number Told Me Where $50,000 Was Hidden 💵",
    alt_titles=["$50,000 Under the Bench I Eat Lunch On 💵", "Bench Three, Part 1: The Wrong Number 💵"],
    description="""9:00 PM. A text from a number you don't know: fifty thousand dollars, under the third bench in Hollow Park.
Four seconds later: "Sorry. Wrong number." 💵

It's the bench you eat lunch on. Every day.

Bench Three, Part 1. An interactive story: YOU decide what happens next.
💬 Put it back, or keep it? Comment A or B. Most comments decide Part 2. 👇

(Fiction. 2D animation.)""",
    hashtags=["#HorrorStory", "#InteractiveStory", "#Shorts"],
    tags=["horror story", "interactive story", "you decide", "choose your ending", "wrong number", "scary text",
          "psychological thriller", "2d animation", "plot twist", "part 1"],
    pinned_comment="Put it back. If he's the one texting, he already knows your face AND your bench. Keeping his money "
                   "just gives him a reason to find your door. Put it back or keep it? 👇 (Look at both phone numbers 👀)",
)

KEY = {"nine", "fifty", "thousand", "dollars", "third", "bench", "hollow", "wrong", "number", "lunch", "envelope",
       "count", "eleven", "different", "watched", "hurts", "midnight", "name", "photo", "three", "weeks", "pen",
       "thank", "coming", "never", "chose", "tonight", "alone", "money", "face", "keep"}

NUM1, NUM2 = "555-0141", "555-0142"                          # one digit apart (the clue, never spoken)
SODIUM = (1.0, 0.76, 0.42)
WOOD, WOOD_D, WOOD_L = hexa("#7a5234"), hexa("#4e331f"), hexa("#9c6c45")
IRON, BRASS = hexa("#22252b"), hexa("#c9a24a")
PAPER, PAPER_D = hexa("#dcbc80"), hexa("#b38f56")            # the manila envelope
PEN = (0.13, 0.2, 0.58, 1)
SLEEVE = tk.RY_JACKET                                         # your purple puffer
COLD_RIM = (0.6, 0.75, 1.0, 0.7)


def camera(cr, t, s0, s1, z0=1.0, z1=1.06, cx=W / 2, cy=H / 2, shake=1.0):
    k = seg(t, s0, s1)
    z = z0 + (z1 - z0) * k
    cr.translate(cx + 4 * shake * noise(t * 0.7, 1), cy + 3 * shake * noise(t * 0.6, 4))
    cr.rotate(0.004 * shake * noise(t * 0.5, 7))
    cr.scale(z, z)
    cr.translate(-cx, -cy)


# ------------------------------------------------------------------ the park and bench three
def park(cr, t, day=False, lamp=1.0):
    """Hollow Park: sky, a tree line, the path and (at night) one sodium lamp over the bench."""
    g = cairo.LinearGradient(0, 0, 0, H)
    for at, col in ((0, "#8fbbe0"), (0.52, "#dcebf5"), (0.55, "#6f9a52"), (1, "#557a3c")) if day else \
            ((0, "#05070f"), (0.52, "#121828"), (0.55, "#0d1118"), (1, "#181c25")):
        g.add_color_stop_rgba(at, *hexa(col))
    cr.set_source(g)
    cr.paint()
    for i in range(10):                                       # the tree line
        x, r = -60 + i * 92, 80 + (i * 23) % 45
        cr.arc(x, 700 - (i * 37) % 55, r, 0, 2 * math.pi)
        cr.set_source_rgba(*(hexa("#3f6a3a")[:3] if day else (0.03, 0.045, 0.06)), 1)
        cr.fill()
    poly(cr, [(150, H), (570, H), (420, 712), (300, 712)])   # the path
    cr.set_source_rgba(*(hexa("#cdbd9c")[:3] if day else (0.12, 0.13, 0.16)), 1)
    cr.fill()
    if day:
        return
    flick = lamp * (0.85 + 0.15 * (noise(t * 9, 3) > -0.6))
    cr.set_source_rgba(*IRON[:3], 1)                          # the lamp post
    cr.rectangle(574, 380, 14, 640)
    cr.fill()
    toon(cr, lambda c: poly(c, [(552, 384), (610, 384), (600, 352), (562, 352)]), IRON, None, (0, 0), None, lw=3)
    poly(cr, [(560, 390), (602, 390), (760, 1040), (380, 1040)])      # its cone of light
    cr.set_source_rgba(*SODIUM, 0.09 * flick)
    cr.fill()
    glow(cr, 581, 392, 360, SODIUM, 0.55 * flick)
    glow(cr, 560, 1010, 260, SODIUM, 0.18 * flick)            # the wet path under it


def bench(cr, x, y, s, part="all", ring=0.0, day=False):
    """Bench three, from the front: iron sides, two back slats with a brass "3" plate, the seat. (x, y) = the middle
    of the seat's front edge. part: "back" (behind someone sitting), "seat" (in front of them) or "all"."""
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    if part in ("all", "back"):
        cr.set_source_rgba(*IRON[:3], 1)
        cr.set_line_width(16)
        for sx in (-1, 1):
            cr.move_to(sx * 222, -215)
            cr.curve_to(sx * 230, -120, sx * 214, -40, sx * 226, 150)
            cr.stroke()
        for yy in (-205, -152):
            toon(cr, lambda c, yy=yy: c.rectangle(-246, yy, 492, 38), WOOD, WOOD_D, (-6, -6), None, lw=4)
        toon(cr, lambda c: tk.tk_rrect(c, -30, -200, 60, 30, 5), BRASS, hexa("#8d6a24"), (-3, -3), None, lw=3)
        hud2d._text(cr, "3", 0, -176, 26, (0.15, 0.1, 0.02, 1), hud2d.ROUND, "center")
    if part in ("all", "seat"):
        toon(cr, lambda c: poly(c, [(-250, -70), (250, -70), (272, -8), (-272, -8)]), WOOD_L, WOOD, (-6, -6), None,
             lw=4)
        cr.set_source_rgba(*WOOD_D[:3], 0.8)
        cr.set_line_width(3)
        for yy in (-50, -29):
            cr.move_to(-258 - (yy + 70) * 0.35, yy)
            cr.line_to(258 + (yy + 70) * 0.35, yy)
            cr.stroke()
        toon(cr, lambda c: c.rectangle(-272, -8, 544, 30), WOOD, WOOD_D, (-6, -6), None, lw=4)
        if ring > 0:                                          # your coffee cup's ring, every lunch
            cr.save()
            cr.translate(-120, -40)
            cr.scale(1, 0.3)
            cr.arc(0, 0, 30, 0, 2 * math.pi)
            cr.restore()
            cr.set_source_rgba(0.3, 0.17, 0.07, 0.75 * ring)
            cr.set_line_width(5)
            cr.stroke()
        cr.set_source_rgba(*IRON[:3], 1)
        cr.set_line_width(16)
        for sx in (-1, 1):
            cr.move_to(sx * 226, 20)
            cr.line_to(sx * 232, 150)
            cr.stroke()
    cr.restore()


def bench_night(cr, t, s0, s1, ring=0.0, beam=None, env=0.0):
    """The night park with bench three under the lamp; beam 0..1 sweeps a car's headlights across it; env 0..1 an
    envelope's corner showing under the seat."""
    park(cr, t)
    if env > 0:
        envelope(cr, 230, 978, 0.32, rot=0.06, shade=1 - env * 0.7)
    bench(cr, 360, 930, 0.95, ring=ring)
    if beam is not None:
        bx = 980 - 1500 * beam
        g = cairo.RadialGradient(bx, 900, 10, bx, 900, 520)
        g.add_color_stop_rgba(0, 1, 0.97, 0.85, 0.75)
        g.add_color_stop_rgba(1, 1, 0.97, 0.85, 0)
        cr.set_source(g)
        cr.paint()
    grade(cr, (0.75, 0.8, 1.0), (0.48, 0.5, 0.64))


# ------------------------------------------------------------------ you
def you(cr, x, y, s, t, fear=0.4, look=(0.0, 0.0), phone=1.0):
    """You (beanie, purple puffer), lit from below by your phone."""
    tk.riley_bust(cr, x, y, s, t, fear=fear, look=look, light=(0, 14), rim=COLD_RIM, rim_from=(0, 9))
    if phone > 0:
        glow(cr, x, y + 40 * s, 300 * s, (0.55, 0.72, 1), 0.45 * phone)


def hands(cr, x, y, s, spread=190):
    """Your two hands holding something at (x, y): purple cuffs from the bottom, thumbs on top."""
    for sx in (-1, 1):
        cr.save()
        cr.translate(x + sx * spread * s, y)
        cr.scale(s, s)
        toon(cr, lambda c, sx=sx: curve(c, [(sx * 10, 420), (sx * -70, 160), (sx * -50, 70), (sx * 60, 60),
                                             (sx * 110, 170), (sx * 120, 420)]), *SLEEVE[:2], (-10, -8), None)
        toon(cr, lambda c, sx=sx: curve(c, [(sx * -46, 80), (sx * -60, 10), (sx * -30, -40), (sx * 20, -46),
                                             (sx * 52, -10), (sx * 50, 70)]), tk.RY_SKIN, tk.RY_SKIN_D, (-8, -6),
             None, lw=4)
        toon(cr, lambda c, sx=sx: curve(c, [(sx * -30, -30), (sx * -60, -70), (sx * -40, -92), (sx * -14, -60)]),
             tk.RY_SKIN, tk.RY_SKIN_D, (-6, -6), None, lw=3.5)
        cr.restore()


def envelope(cr, x, y, s, flip=1.0, shade=0.0, tape=0.0, rot=0.0, ink=1.0):
    """The envelope; flip 1 = front, -1 = back (the note in pen), in between it turns. shade 0..1 darkens it so the
    pen is there but can't be read (the plant under the bench). tape 0..1 the strip still stuck to it."""
    cr.save()
    cr.translate(x, y)
    cr.rotate(rot)
    cr.scale(s * max(0.04, abs(flip)), s)
    toon(cr, lambda c: tk.tk_rrect(c, -180, -115, 360, 230, 8), PAPER, PAPER_D, (-8, -8), None, lw=5)
    if flip > 0:
        cr.set_source_rgba(*PAPER_D[:3], 0.9)
        cr.set_line_width(3)
        cr.move_to(-176, -110)
        cr.line_to(0, 20)
        cr.line_to(176, -110)
        cr.stroke()
        if tape > 0:
            cr.set_source_rgba(0.95, 0.95, 0.85, 0.55)
            cr.rectangle(-120, -130, 240 * tape, 44)
            cr.fill()
    elif ink > 0:
        hud2d._text(cr, "Thank you for coming.", 0, 14, 44, (*PEN[:3], ink), "Kalam", "center")
    if shade > 0:                                             # under the slats: the pen is there, unreadable
        g = cairo.LinearGradient(-180, 0, 180, 0)
        g.add_color_stop_rgba(0, 0.02, 0.02, 0.04, 0.55 * shade)
        g.add_color_stop_rgba(1, 0.02, 0.02, 0.04, 0.92 * shade)
        cr.set_source(g)
        tk.tk_rrect(cr, -180, -115, 360, 230, 8)
        cr.fill()
    cr.restore()


def under_bench(cr, t, peel=0.0, flip=1.0):
    """Under the slats, by the lamp: your hands peel the envelope off the wood."""
    cr.set_source_rgba(0.03, 0.035, 0.05, 1)
    cr.paint()
    for k in range(4):                                        # the slats from below
        toon(cr, lambda c, k=k: c.rectangle(-40, 150 + k * 92, W + 80, 76), WOOD_D, hexa("#2e1d10"), (0, 6), None,
             lw=4)
    glow(cr, 620, 260, 420, SODIUM, 0.35)
    y = 470 + 120 * peel
    envelope(cr, W / 2, y, 1.1, flip=flip, shade=1.0 if flip < 0 else 0.35, tape=1 - peel, rot=-0.04 * peel)
    hands(cr, W / 2, y + 60, 1.0, spread=205)
    grade(cr, (0.75, 0.75, 0.95), (0.35, 0.33, 0.45))


# ------------------------------------------------------------------ your room
def room(cr, t, light=1.0, chain=0.0):
    """Your room: the door on the left with a FINAL NOTICE taped to it, a lamp, the table."""
    g = cairo.LinearGradient(0, 0, 0, H)
    g.add_color_stop_rgba(0, *hexa("#2b2433"))
    g.add_color_stop_rgba(1, *hexa("#17131d"))
    cr.set_source(g)
    cr.paint()
    toon(cr, lambda c: c.rectangle(30, 200, 250, 820), hexa("#5a3e2c"), hexa("#3b2819"), (-6, -6), None, lw=5)
    cr.set_source_rgba(*BRASS[:3], 1)                         # the knob
    cr.arc(250, 620, 13, 0, 2 * math.pi)
    cr.fill()
    toon(cr, lambda c: c.rectangle(70, 300, 170, 210), hexa("#f3efe6"), hexa("#cfc8ba"), (-4, -4), None, lw=3)
    cr.set_source_rgba(*hud2d.RED[:3], 1)
    cr.rectangle(70, 300, 170, 46)
    cr.fill()
    hud2d._text(cr, "FINAL NOTICE", 155, 332, 22, (1, 1, 1, 1), hud2d.ROUND, "center")
    cr.set_source_rgba(0.35, 0.33, 0.3, 0.8)
    for k in range(5):
        cr.rectangle(86, 370 + k * 24, 138 - (k % 2) * 30, 6)
        cr.fill()
    hud2d._text(cr, "RENT · OCT", 155, 498, 18, (*hud2d.RED[:3], 1), hud2d.MONO, "center")
    if chain > 0:                                             # the chain, on
        cr.set_source_rgba(0.75, 0.75, 0.78, chain)
        cr.set_line_width(4)
        for k in range(7):
            cr.arc(268 - k * 15, 430 + k * 5 + 4 * math.sin(k), 8, 0, 2 * math.pi)
            cr.stroke()
    glow(cr, 640, 640, 380, (1, 0.8, 0.55), 0.35 * light)
    toon(cr, lambda c: c.rectangle(-20, 1000, W + 40, 300), hexa("#4a3426"), hexa("#2e2016"), (0, -6), None, lw=5)


def cash(cr, k):
    """Bundles of hundreds on the table, k 0..1 of the fifty thousand."""
    n = int(round(10 * k))
    for i in range(n):
        x, y = 380 + (i % 5) * 62, 1090 - (i // 5) * 26
        toon(cr, lambda c, x=x, y=y: tk.tk_rrect(c, x, y, 58, 30, 4), hexa("#7fae78"), hexa("#4f7c4c"), (-3, -3),
             None, lw=3)
        cr.set_source_rgba(0.95, 0.93, 0.8, 1)
        cr.rectangle(x + 22, y, 12, 30)
        cr.fill()


# ------------------------------------------------------------------ the phone
def phone(cr, t, header, sub, items, glow_a=1.0, x0=105, y0=150):
    """Your phone, held up close: a message thread from an unknown number. items = [dict(at, text, time) or
    dict(at, photo=True, time)]; each new one buzzes in."""
    w, h = 510, 1010
    glow(cr, W / 2, 600, 560, (0.55, 0.7, 1), 0.25 * glow_a)
    for sx in (-1, 1):
        toon(cr, lambda c, sx=sx: curve(c, [(W / 2 + sx * 120, 1400), (W / 2 + sx * 310, 1300),
                                             (W / 2 + sx * 270, 960), (W / 2 + sx * 190, 930),
                                             (W / 2 + sx * 130, 1060)]), *SLEEVE[:2], (-14, -10), None)
    toon(cr, lambda c: tk.tk_rrect(c, x0, y0, w, h, 56), hexa("#141519"), None, (0, 0), None, lw=6)
    tk.tk_rrect(cr, x0 + 12, y0 + 12, w - 24, h - 24, 44)
    cr.set_source_rgba(0.96, 0.96, 0.975, 1)
    cr.fill()
    cr.save()
    tk.tk_rrect(cr, x0 + 12, y0 + 12, w - 24, h - 24, 44)
    cr.clip()
    cr.set_source_rgba(0.9, 0.9, 0.93, 1)
    cr.rectangle(x0, y0, w, 132)
    cr.fill()
    cr.set_source_rgba(0.62, 0.63, 0.68, 1)
    cr.arc(x0 + 74, y0 + 82, 28, 0, 2 * math.pi)
    cr.fill()
    hud2d._text(cr, "?", x0 + 74, y0 + 94, 32, (1, 1, 1, 1), hud2d.ROUND, "center")
    hud2d._text(cr, header, x0 + 118, y0 + 78, 34, (0.07, 0.07, 0.09, 1), hud2d.UI)
    hud2d._text(cr, sub, x0 + 118, y0 + 106, 19, (0.42, 0.42, 0.48, 1), hud2d.UI)
    yy = y0 + 160
    for it in items:
        if t < it["at"]:
            break
        k = clamp01((t - it["at"]) / 0.25)
        cue("buzz", t, it["at"])
        cr.save()
        cr.translate(0, (1 - k) * 40)
        if it.get("photo"):
            bw, bh = 380, 300
            cr.save()
            tk.tk_rrect(cr, x0 + 34, yy, bw, bh, 22)
            cr.clip()
            photo(cr, x0 + 34, yy, bw, bh, t)
            cr.restore()
        else:
            lines, cur = [], ""
            for word in it["text"].split():
                nxt = (cur + " " + word).strip()
                if cur and hud2d.text_width(cr, nxt, 28, hud2d.UI) > 350:
                    lines.append(cur)
                    cur = word
                else:
                    cur = nxt
            lines.append(cur)
            bw = max(hud2d.text_width(cr, ln, 28, hud2d.UI) for ln in lines) + 44
            bh = 26 + 36 * len(lines)
            tk.tk_rrect(cr, x0 + 34, yy, bw, bh, 24)
            cr.set_source_rgba(0.88, 0.88, 0.91, k)
            cr.fill()
            for j, ln in enumerate(lines):
                hud2d._text(cr, ln, x0 + 56, yy + 44 + 36 * j, 28, (0.06, 0.06, 0.08, k), hud2d.UI)
        hud2d._text(cr, it["time"], x0 + 40, yy + bh + 26, 19, (0.45, 0.45, 0.5, k), hud2d.UI)
        cr.restore()
        yy += bh + 52
    cr.restore()
    for sx in (-1, 1):                                        # thumbs over the edges
        toon(cr, lambda c, sx=sx: curve(c, [(W / 2 + sx * 250, 1060), (W / 2 + sx * 282, 990),
                                             (W / 2 + sx * 270, 930), (W / 2 + sx * 234, 920),
                                             (W / 2 + sx * 216, 980), (W / 2 + sx * 200, 1050)]),
             tk.RY_SKIN, tk.RY_SKIN_D, (-10, -8), None, lw=4)


def inbox(cr, t, new_at):
    """The message list: the new number on top, the first one under it. Their numbers differ by one digit."""
    rows = [(NUM2, "I watched you take it.", "11:31 PM", t >= new_at), (NUM1, "Sorry. Wrong number.", "9:00 PM", False)]
    x0, y0, w = 105, 150, 510
    phone(cr, t, "Messages", "", [])
    cr.set_source_rgba(0.96, 0.96, 0.975, 1)
    cr.rectangle(x0 + 12, y0 + 12, w - 24, 140)
    cr.fill()
    hud2d._text(cr, "Messages", x0 + 40, y0 + 100, 44, (0.06, 0.06, 0.08, 1), hud2d.ROUND)
    for k, (num, prev, at, new) in enumerate(rows):
        if k == 0 and t < new_at:
            continue
        yy = y0 + 190 + (k if t >= new_at else 1) * 130 - (130 if t < new_at else 0)
        cr.set_source_rgba(0.62, 0.63, 0.68, 1)
        cr.arc(x0 + 74, yy + 52, 34, 0, 2 * math.pi)
        cr.fill()
        hud2d._text(cr, num, x0 + 126, yy + 44, 34, (0.06, 0.06, 0.08, 1), hud2d.UI)
        hud2d._text(cr, prev, x0 + 126, yy + 84, 22, (0.4, 0.4, 0.46, 1), hud2d.UI)
        hud2d._text(cr, at, x0 + w - 40, yy + 44, 20, (0.4, 0.4, 0.46, 1), hud2d.UI, "right")
        if new:
            cr.set_source_rgba(0.2, 0.5, 1, 1)
            cr.arc(x0 + 30, yy + 52, 8, 0, 2 * math.pi)
            cr.fill()
        cr.set_source_rgba(0.85, 0.85, 0.88, 1)
        cr.rectangle(x0 + 126, yy + 116, w - 160, 2)
        cr.fill()


# ------------------------------------------------------------------ the photo (three weeks ago)
def photo(cr, x, y, w, h, t, stamp=True):
    """You on bench three at lunch, in daylight, three weeks ago. Half out of frame on the next bench: someone's
    hands, holding two phones (the clue, never spoken). A camera date stamp: OCT 7."""
    cr.save()
    cr.translate(x, y)
    cr.scale(w / 680, h / 560)
    cr.rectangle(0, 0, 680, 560)
    cr.clip()
    cr.save()
    cr.scale(680 / W, 560 / 700)
    cr.translate(0, -560)
    park(cr, t, day=True)
    cr.restore()
    bench(cr, 300, 470, 0.62, part="back", day=True)
    tk.riley_bust(cr, 300, 420, 0.55, t, fear=0.0, look=(-0.3, 0.2))
    bench(cr, 300, 470, 0.62, part="seat", ring=0.0, day=True)
    toon(cr, lambda c: poly(c, [(330, 452), (370, 470), (330, 470)]), hexa("#f1d9a4"), hexa("#c9a86a"), (-2, -2),
         None, lw=2.5)                                         # half a sandwich on the seat
    toon(cr, lambda c: poly(c, [(196, 470), (226, 470), (222, 430), (200, 430)]), hexa("#f4f1ea"), hexa("#cfc8ba"),
         (-2, -2), None, lw=2.5)                               # the coffee cup
    bench(cr, 820, 470, 0.62, part="all", day=True)            # the next bench, half out of frame
    for k, (px, py) in enumerate(((600, 392), (640, 408))):     # two hands, two phones
        toon(cr, lambda c, px=px, py=py: curve(c, [(px + 60, py + 90), (px + 10, py + 40), (px + 20, py + 10),
                                                    (px + 80, py + 30)]), hexa("#2b2d33"), hexa("#16171b"),
             (-3, -3), None, lw=3)
        toon(cr, lambda c, px=px, py=py: tk.tk_rrect(c, px - 12, py - 30, 30, 52, 6), hexa("#111216"), None, (0, 0),
             None, lw=3)
        cr.set_source_rgba(0.7, 0.85, 1, 0.9)
        tk.tk_rrect(cr, px - 8, py - 26, 22, 44, 4)
        cr.fill()
        toon(cr, lambda c, px=px, py=py: curve(c, [(px - 18, py + 10), (px - 4, py - 6), (px + 22, py), (px + 16, py + 22)]),
             tk.SKIN, tk.SKIN_D, (-2, -2), None, lw=2.5)
    if stamp:
        hud2d._text(cr, "OCT 7", 650, 535, 40, (1, 0.55, 0.12, 0.95), hud2d.MONO, "right")
    cr.restore()


def viewer(cr, t, zoom_k=0.0):
    """The photo, opened full screen; zoom_k 0..1 pushes in on its date stamp."""
    cr.set_source_rgba(0, 0, 0, 1)
    cr.paint()
    hud2d._text(cr, NUM2, W / 2, 196, 30, (1, 1, 1, 1), hud2d.UI, "center")
    hud2d._text(cr, "11:33 PM", W / 2, 228, 20, (0.7, 0.7, 0.75, 1), hud2d.UI, "center")
    z = 1 + 1.6 * zoom_k * zoom_k * (3 - 2 * zoom_k)
    cr.save()
    cr.translate(620, 760)
    cr.scale(z, z)
    cr.translate(-620, -760)
    photo(cr, 20, 290, 680, 560, t)
    cr.restore()


# ------------------------------------------------------------------ the film
def shots(tl):
    A, B = tl.at, tl.by_id
    return [
        (0.0, "face"), (B["b2"].start - 0.15, "thread"), (B["b4"].start - 0.15, "bench"),
        (B["b5"].start - 0.15, "under"), (B["b6"].start - 0.15, "count"), (B["b7"].start - 0.15, "inbox"),
        (B["b8"].start - 0.15, "thread2"), (B["b10"].start - 0.15, "viewer"), (B["b12"].start - 0.15, "turn"),
        (B["b14"].end + 0.05, "flash"), (B["b15"].start + 0.2, "face2"), (B["b16"].start - 0.15, "split"),
        (B["b17"].start - 0.15, "dark"), (B["b18"].start - 0.15, "door"), (B["b19"].start - 0.15, "card"),
        (tl.total + 1, "end")]


_shots = {}


def split(cr, t):
    cr.save()
    cr.rectangle(0, 0, W, H / 2)
    cr.clip()
    photo(cr, -110, 60, 940, 774, t)
    cr.restore()
    cr.save()
    cr.rectangle(0, H / 2, W, H / 2)
    cr.clip()
    cr.translate(0, 260)
    bench_night(cr, t, 0, 1, ring=0.0)
    cr.restore()
    cr.set_source_rgba(0.85, 0.9, 1, 0.8)
    cr.rectangle(0, H / 2 - 3, W, 6)
    cr.fill()


def draw(cr, t, tl):
    A, B = tl.at, tl.by_id
    if id(tl) not in _shots:
        _shots[id(tl)] = shots(tl)
    sh = _shots[id(tl)]
    k = max(i for i, (at, _) in enumerate(sh) if at <= t or i == 0)
    s0, name, s1 = sh[k][0], sh[k][1], sh[k + 1][0]
    first = [dict(at=0.0, text="$50,000. Under the third bench in Hollow Park.", time="9:00:00 PM")]
    second = dict(at=B["b3"].start, text="Sorry. Wrong number.", time="9:00:04 PM")
    plant = (B["b5"].end - 0.55, B["b6"].start - 0.15)          # the envelope's back, under the slats, ~1 s

    cr.save()
    if name == "face":                                          # frame 0: your face in the phone's light
        camera(cr, t, s0, s1, 1.03, 1.1, cy=760)
        room(cr, t, light=0.25)
        cr.set_source_rgba(0, 0, 0.02, 0.55)
        cr.paint()
        you(cr, 360, 990, 1.15, t, fear=0.3, look=(0, 0.35))
        tk.phone_in_hands(cr, 360, 1180, 1.2, t)
    elif name == "thread":
        camera(cr, t, s0, s1, 1.0, 1.05, cy=520)
        phone(cr, t, NUM1, "Unknown number", first + [second])
    elif name == "bench":                                       # bench three, your coffee ring on the slats
        camera(cr, t, s0, s1, 1.0, 1.25, cx=280, cy=900)
        bench_night(cr, t, s0, s1, ring=1.0)
        tk.riley_back(cr, 140, 1240, 0.9, t, rim=(1, 0.8, 0.5, 0.5))
    elif name == "under":
        camera(cr, t, s0, s1, 1.02, 1.1, cy=560, shake=0.6)
        k_turn = seg(t, plant[0], plant[0] + 0.3)
        under_bench(cr, t, peel=seg(t, B["b5"].start + 0.4, A("b5", "envelope.") + 0.1), flip=1 - 2 * k_turn)
    elif name == "count":
        camera(cr, t, s0, s1, 1.0, 1.06, cy=700)
        room(cr, t)
        you(cr, 470, 960, 1.0, t, fear=0.25, look=(0, 0.45), phone=0.0)
        cash(cr, seg(t, B["b6"].start + 0.3, B["b6"].end))
        hud2d._text(cr, f"${int(round(50 * seg(t, B['b6'].start + 0.3, B['b6'].end))) * 1000:,}", 470, 290, 96,
                    hud2d.GREEN, hud2d.ROUND, "center", outline=(0.03, 0.03, 0.05, 1), ow=12)
    elif name == "inbox":
        camera(cr, t, s0, s1, 1.0, 1.05, cy=520)
        inbox(cr, t, B["b7"].start + 0.5)
    elif name == "thread2":
        camera(cr, t, s0, s1, 1.0, 1.05, cy=520)
        phone(cr, t, NUM2, "Unknown number", [dict(at=s0, text="I watched you take it. It belongs to a man who hurts "
                                                   "people.", time="11:31 PM"),
                                              dict(at=B["b9"].start, text="He checks that bench at midnight. Put it "
                                                   "back before then, and he never learns your name.",
                                                   time="11:32 PM")])
    elif name == "viewer":
        viewer(cr, t, seg(t, B["b11"].start - 0.1, B["b11"].end))
    elif name == "turn":                                        # in your hands, under your lamp: the back, in pen
        camera(cr, t, s0, s1, 1.0, 1.12, cy=560)
        room(cr, t)
        cr.set_source_rgba(0, 0, 0, 0.45)
        cr.paint()
        f = 1 - 2 * seg(t, A("b12", "over.") - 0.25, A("b12", "over.") + 0.25)
        envelope(cr, W / 2, 560, 1.4, flip=f, ink=seg(t, B["b13"].start, B["b13"].start + 0.3) if f < 0 else 0)
        hands(cr, W / 2, 640, 1.1, spread=235)
        if t >= B["b14"].start:                                 # the pen line underlines itself
            cr.set_source_rgba(*PEN[:3], 0.9)
            cr.set_line_width(5)
            cr.move_to(W / 2 - 220, 600)
            cr.line_to(W / 2 - 220 + 440 * seg(t, B["b14"].start, B["b14"].end), 600)
            cr.stroke()
    elif name == "flash":                                       # cut back: the same envelope, under the slats
        under_bench(cr, t, peel=1.0, flip=-1.0)
        cr.set_source_rgba(0.9, 0.85, 0.7, 0.18)
        cr.paint()
        n3.chip(cr, t, "UNDER BENCH 3 · 9:20 PM", s0, s1 - 0.2)
    elif name == "face2":
        camera(cr, t, s0, s1, 1.05, 1.16, cy=760, shake=0.8)
        room(cr, t, light=0.2)
        cr.set_source_rgba(0, 0, 0.02, 0.55)
        cr.paint()
        you(cr, 360, 990, 1.15, t, fear=0.95, look=(0, 0.1))
    elif name == "split":
        camera(cr, t, s0, s1, 1.0, 1.03, shake=0.5)
        split(cr, t)
    elif name == "dark":
        camera(cr, t, s0, s1, 1.0, 1.08, cx=360, cy=900)
        bench_night(cr, t, s0, s1, beam=seg(t, B["b17"].start + 0.4, B["b17"].end))
    elif name == "door":
        camera(cr, t, s0, s1, 1.35, 1.45, cx=160, cy=520)
        room(cr, t, chain=1.0)
        cr.save()
        cr.identity_matrix()
        cr.translate(470, 980)
        cr.rotate(-0.08)
        toon(cr, lambda c: tk.tk_rrect(c, -120, -200, 240, 420, 26), hexa("#141519"), None, (0, 0), None, lw=5)
        cr.save()
        tk.tk_rrect(cr, -108, -188, 216, 396, 18)
        cr.clip()
        photo(cr, -260, -150, 520, 428, t, stamp=False)
        cr.restore()
        cr.restore()
    elif name in ("card", "end"):
        split(cr, t)
        cr.set_source_rgba(0, 0, 0, 0.35)
        cr.paint()
    cr.restore()

    hud.finish(cr, t, flash_at=[], vig=0.55, grain=0.06)
    clock = ("9:00 PM" if t < B["b4"].start - 0.15 else "9:20 PM" if t < B["b6"].start - 0.15 else
             "10:05 PM" if t < B["b7"].start - 0.15 else "11:31 PM" if t < B["b10"].start - 0.15 else
             "11:33 PM" if t < B["b15"].start else "11:36 PM")
    batt = "41%" if t < B["b7"].start - 0.15 else "9%"
    money = "$0" if t < B["b6"].start + 0.3 else "$50,000"
    hud2d.stats(cr, t, [("TIME", clock, "warn" if t >= B["b7"].start - 0.15 else None),
                        ("PHONE", batt, "bad" if t >= B["b7"].start - 0.15 else None, B["b7"].start - 0.15),
                        ("CASH", money, "warn" if t >= B["b6"].start else None, B["b6"].end)])
    n3.chip(cr, t, "BENCH THREE · PART 1", 0.0, 2.0)
    hud2d.hook(cr, t, [("$50,000", False), ("UNDER BENCH 3.", True)], end=B["b1"].end + 0.1, y=250, size=92)
    if name == "face" and t < B["b1"].end:                      # the first text, on screen from frame 0
        hud2d.bubble(cr, t, 0.0, B["b1"].end, f"{NUM1} · 9:00:00 PM: $50,000. Under the third bench in Hollow Park.",
                     360, 470, (360, 1060), w=520, size=28)
    hud2d.stamp(cr, t, B["b15"].start, B["b15"].end + 0.2, ["NEVER A WRONG NUMBER"], y=420)
    hud2d.ab_card(cr, t, A("b19", "Put"), "PUT IT BACK", "KEEP IT", kicker="BENCH THREE · PART 1 · YOUR CHOICE",
                  decides="Part 2")
    hud2d.captions(cr, t, tl, KEY, skip=("b3", "b8", "b9", "b14"))
    cue("heartbeat", t, B["b7"].start, B["b10"].start - B["b7"].start)
    cue("riser", t, B["b10"].start, B["b12"].start - B["b10"].start)
    cue("sting", t, B["b14"].start - 0.05)
    cue("heartbeat", t, B["b15"].start, B["b19"].start - B["b15"].start)
    cue("engine", t, B["b17"].start + 0.2, B["b17"].end - B["b17"].start)
