"""Tower 9, Night 4, in the illustrated 2D style. Original story; Night 3's vote was stay (owner, 28 Oct 2026: "For tower
9 all said to stay"), and the owner approved the script ("Approved, make it"): out/horror/scripts_night4_tower9.md.

You let the radio crackle and its light goes out. The other you sits by the hatch, frost spreading under it, its watch
running backwards (Night 3's hidden clue, now spoken). The test: "Who's on the radio?" "Someone who answered." The
flip: the radio crackles again in your own voice and reads page one of the logbook, the page only you have seen. The
logbook falls open to its last page: your handwriting, dated tomorrow ("Day 2."). "Don't read it. I did." The vote:
read the last page, or burn the logbook. Clues on screen, never spoken: the other you's right sleeve is scorched, and
the radio's display reads 4:44 when your voice comes through.

    /home/user/.venv-main/bin/python channels/horror/make_2d.py tower9_n4_2d   -> out/horror/tower9_n4_2d.mp4
"""
import math

from motion import audio, voice
from motion.engine import W, H, cairo, clamp01, cue, seg

from channels.horror import hud, hud2d, sound  # noqa: F401  (sound registers the horror effects)
from channels.horror import toon2d as tk
from channels.horror import tower9_2d as n1      # Night 1's sets: cabin, radio, logbook, planks
from channels.horror import tower9_n2_2d as n2   # Night 2's phone light
from channels.horror import tower9_n3_2d as n3   # Night 3's other you, its watch, the frost, page one, insets
from channels.horror.toon2d import INK, glow, grade, hexa, mix, noise, toon

NARRATOR = dict(turbo=True)
TAIL = 2.0                     # the vote card stays up ~2 s (reference study, 27 Oct)
MUSIC = "horror"
TWIST = "k9"                   # the bed drops out under your own voice on the radio
audio.GAINS.update(rain=0.15, static=0.4, click=0.5)

SCRIPT = [
    dict(id="k1", scene="open", text="Nearly all of you said stay. So you let the radio crackle."),
    dict(id="k2", scene="radio", text="Tower [nine.|9.] Answer me.", speaker="base", gap=0.5),
    dict(id="k3", scene="radio", text="You don't. The radio's light goes out.", gap=0.5),
    dict(id="k4", scene="other", text="The other you sits by the hatch. Frost spreads wherever it sits."),
    dict(id="k5", scene="watch", text="Its watch reads [five.|5:00.] Then [four fifty-nine.|4:59.] Then "
                                      "[four fifty-eight.|4:58.]", gap=0.4),
    dict(id="k6", scene="you", text="So you ask it. Who's on the radio?", gap=0.5),
    dict(id="k7", scene="other", text="Someone who answered.", speaker="other", gap=0.4),
    dict(id="k8", scene="radio", text="Then the radio crackles again. In your voice.", gap=0.6),
    dict(id="k9", scene="radio", text="Day one. I hate heights.", speaker="radio", gap=0.6),   # static fills this gap
    dict(id="k10", scene="you", text="Page one. The page only you have seen.", gap=0.4),
    dict(id="k11", scene="other", text="Now you know why you don't answer.", speaker="other", gap=0.4),
    dict(id="k12", scene="book", text="The logbook falls open by itself. To the last page.", gap=0.5),
    dict(id="k13", scene="page", text="Your handwriting. Dated tomorrow.", gap=0.3),
    dict(id="k14", scene="other", text="Don't read it. I did.", speaker="other", gap=0.4),
    dict(id="k15", scene="choice", text="Read it, and you'll know how tonight ends. Burn it, and the rules burn "
                                        "with it.", gap=0.4),
    dict(id="k16", scene="split", text="Whatever most of you choose happens on Night [five.|5.]"),
    dict(id="k17", scene="split", text="So, do you read the last page? Or burn the logbook?", gap=0.3),
]

METADATA = dict(
    title="You Didn't Answer the Radio. Then It Spoke in Your Voice. 📻",
    alt_titles=["Never Answer the Radio After Three: Night 4 📻",
                "The Last Page Was in My Handwriting. Dated Tomorrow. 📻"],
    description="""5:00 AM. Nearly all of you said stay... so you let the radio crackle. 📻

Tower 9, Night 4. Then the radio calls again, in your own voice, and reads the one page only you have seen.
An interactive horror story: YOU decide what happens next.
💬 Read the last page, or burn the logbook? Comment A or B. Most comments decide Night 5. 👇

(Fiction. 2D animation.)""",
    hashtags=["#HorrorStory", "#InteractiveStory", "#Shorts"],
    tags=["horror story", "interactive story", "you decide", "choose your ending", "fire tower", "forest horror",
          "scary story", "2d animation", "doppelganger", "night 4", "creepy"],
    pinned_comment="Burn it. The other you read it, and look where that got it: stuck in this tower with you, its "
                   "watch running backwards. Read or burn? 👇 (Look at its sleeve 👀)",
)

KEY = {"stay", "crackle", "answer", "light", "out", "frost", "hatch", "watch", "five", "fifty-nine", "fifty-eight",
       "radio", "answered", "voice", "page", "only", "logbook", "last", "handwriting", "tomorrow", "read", "burn",
       "rules", "tonight"}
PHONE = n2.PHONE
RED = (1.0, 0.18, 0.12)


def camera(cr, t, s0, s1, z0=1.0, z1=1.06, cx=W / 2, cy=H / 2, shake=1.0):
    k = seg(t, s0, s1)
    z = z0 + (z1 - z0) * k
    cr.translate(cx + 4 * shake * noise(t * 0.7, 1), cy + 3 * shake * noise(t * 0.6, 4))
    cr.rotate(0.004 * shake * noise(t * 0.5, 7))
    cr.scale(z, z)
    cr.translate(-cx, -cy)


# ------------------------------------------------------------------ the radio
def radio(cr, t, rx, ch="CH 09"):
    """The radio on the desk in the dark cabin; rx = the RX light (and the bars); ch = what the display says."""
    hud2d.blurred(cr, lambda c: n1.cabin(c, t, on=0.0), sigma=8)
    n1.desk(cr, 860)
    n1.radio_unit(cr, t, 340, 760, 1.15, rx, ch=ch)
    grade(cr, (0.55, 0.62, 0.8), (0.28, 0.3, 0.4))
    n2.phone_dark(cr, 360, 900, 1000, 0.55)


# ------------------------------------------------------------------ the other you's sleeve and watch
def scorch(cr, x, y, s, a=1.0):
    """A burnt patch on the orange sleeve: a ragged black edge, browned cloth around it (the clue, never spoken)."""
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    for r, col in ((62, (0.35, 0.18, 0.06, 0.55 * a)), (44, (0.12, 0.07, 0.04, 0.85 * a)),
                   (26, (0.03, 0.02, 0.02, 0.95 * a))):
        cr.new_path()
        for j in range(19):
            ang = j * 2 * math.pi / 18
            rr = r * (0.78 + 0.32 * abs(math.sin(j * 2.3 + r)))
            (cr.move_to if j == 0 else cr.line_to)(rr * math.cos(ang), rr * math.sin(ang) * 0.7)
        cr.close_path()
        cr.set_source_rgba(*col)
        cr.fill()
    cr.restore()


def wrist(cr, t, minutes, k_scorch=1.0):
    """Close on its wrist: the wet orange cuff (scorched), a blue-cold hand, the watch going back a minute at a time
    while its second hand sweeps backwards."""
    hud2d.blurred(cr, lambda c: (n1.cabin(c, t, on=0.0), grade(c, (0.3, 0.34, 0.46), (0.12, 0.13, 0.2))), sigma=10)
    cr.save()
    cr.translate(360, 720)
    cr.rotate(-0.18)
    toon(cr, lambda c: tk.curve(c, [(-520, -150), (-60, -170), (-40, 170), (-520, 190)]), *n3.WET_RANGER[:2],
         (-8, -6), None, lw=6)                                  # the sleeve
    scorch(cr, -250, 40, 1.6, k_scorch)
    toon(cr, lambda c: tk.curve(c, [(-60, -150), (260, -130), (420, -60), (430, 70), (260, 140), (-60, 150)]),
         n3.OTHER_SKIN, mix(n3.OTHER_SKIN, (0, 0, 0, 1), 0.3), (-6, -6), None, lw=5)   # the wrist and the hand
    toon(cr, lambda c: tk.tk_rrect(c, 20, -170, 120, 340, 18), hexa("#2a2a2e"), None, (0, 0), None, lw=4)   # strap
    x, y, r = 80, 0, 150
    toon(cr, lambda c: c.arc(x, y, r + 12, 0, 2 * math.pi), hexa("#2c2c30"), None, (0, 0), None, lw=4)
    toon(cr, lambda c: c.arc(x, y, r, 0, 2 * math.pi), hexa("#e9e4d6"), hexa("#c8c0aa"), (-5, -5), None, lw=3)
    for j in range(12):                                         # hour marks
        a = j * math.pi / 6
        cr.set_source_rgba(*INK)
        cr.set_line_width(5 if j % 3 == 0 else 2.5)
        cr.move_to(x + 0.82 * r * math.sin(a), y - 0.82 * r * math.cos(a))
        cr.line_to(x + 0.94 * r * math.sin(a), y - 0.94 * r * math.cos(a))
        cr.stroke()
    h = (minutes / 60.0) % 12
    sec = (-t * 1.0) % 60                                       # backwards
    for frac, ln, w, col in ((h / 12, r * 0.5, 9, INK), ((minutes % 60) / 60, r * 0.78, 6, INK),
                             (sec / 60, r * 0.86, 2.5, (0.8, 0.1, 0.08, 1))):
        a = frac * 2 * math.pi
        cr.set_source_rgba(*col)
        cr.set_line_width(w)
        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        cr.move_to(x, y)
        cr.line_to(x + ln * math.sin(a), y - ln * math.cos(a))
        cr.stroke()
    cr.set_source_rgba(*INK)
    cr.arc(x, y, 8, 0, 2 * math.pi)
    cr.fill()
    cr.restore()
    n3.floor_frost(cr, 380, 1180, 0.8)
    glow(cr, 360, 1250, 520, PHONE, 0.3)
    n2.phone_dark(cr, 360, 1050, 950, 0.65)


def other_scorched(cr, t, face, look=(0.0, 0.0), frost_k=0.0, tremble=0.3):
    """Night 3's other you in the dark cabin, with the scorch on its right sleeve (viewer's left)."""
    n3.other_room(cr, t, face, look=look, frost_k=frost_k, tremble=tremble)
    scorch(cr, 190, 1120, 0.8)                                  # on the sleeve, viewer's left


# ------------------------------------------------------------------ the logbook
def book_base(cr):
    """The open logbook on the desk by phone light (Night 1's book, closer)."""
    n1.planks(cr, 0, 0, W, H, horizontal=False, seed=7, base=hexa("#7a5638"), dark=hexa("#553a24"), board=90)
    cr.save()
    cr.translate(360, 560)
    cr.rotate(-0.04)
    cr.scale(0.9, 0.9)
    cr.set_source_rgba(0, 0, 0, 0.45)
    tk.tk_rrect(cr, -330, -300, 670, 620, 14)
    cr.fill()
    toon(cr, lambda c: tk.tk_rrect(c, -340, -310, 670, 610, 12), hexa("#5a2a1c"), None, (0, 0), None, lw=5)
    for side in (-1, 1):
        toon(cr, lambda c, side=side: page_shape(c, side), hexa("#efe4c6"), hexa("#d9caa3"), (side * 6, -4), None,
             lw=4)


def page_shape(c, side, w=318):
    tk.curve(c, [(0, -290), (side * w * 0.5, -300), (side * w, -292), (side * w, 280), (side * w * 0.5, 286),
                 (0, 278)])


def scribble(cr, x0, y0, rows, width, col, seed=0, wobble=4):
    """Handwriting too small to read."""
    cr.set_source_rgba(*col)
    for k in range(rows):
        cr.set_line_width(2.2)
        x = x0
        cr.move_to(x, y0 + k * 40)
        n = int(width / 16 * (0.6 + 0.4 * abs(math.sin(k * 1.7 + seed))))
        for j in range(n):
            x += 16
            cr.line_to(x, y0 + k * 40 + wobble * math.sin(j * 2.1 + k + seed))
        cr.stroke()


def flipping_book(cr, t, k):
    """The logbook flipping by itself, faster and faster, then lying open at the last page (k = 0..1)."""
    book_base(cr)
    ink = (0.12, 0.14, 0.3, 0.55)
    if k < 1:
        scribble(cr, -290, -230, 12, 270, ink, seed=3)
        scribble(cr, 30, -230, 12, 270, ink, seed=5)
        n = 6
        for j in range(n):                                      # pages turning over the spine
            u = (k * n * 1.6 - j * 0.6) % 1.0 if k * n * 1.6 > j * 0.6 else 0.0
            if u <= 0:
                continue
            w = 318 * math.cos(math.pi * u)
            tk.poly(cr, [(0, -290), (w, -300 - 20 * math.sin(math.pi * u)), (w, 280 + 10 * math.sin(math.pi * u)),
                         (0, 278)])
            cr.set_source_rgba(*mix(hexa("#efe4c6"), (0, 0, 0, 1), 0.18 * math.sin(math.pi * u)))
            cr.fill_preserve()
            cr.set_source_rgba(*INK)
            cr.set_line_width(3)
            cr.stroke()
    else:                                                       # the last page: tomorrow, in your hand
        scribble(cr, -290, -230, 12, 270, ink, seed=3)
        last_page_text(cr, 1.0, small=True)
    cr.restore()
    glow(cr, 380, 620, 420, PHONE, 0.18)
    n2.phone_dark(cr, 380, 600, 760, 0.95)


def last_page_text(cr, k, small=False):
    """'Day 2.' and lines of your handwriting too small to read (on the right-hand page)."""
    ink = (0.12, 0.14, 0.3, 1)
    x0, y0 = (40, -230) if small else (-250, -300)
    sz = 46 if small else 80
    hud2d._text(cr, "Day 2.", x0, y0 + sz * 0.6, sz, ink, "Kalam")
    if k > 0:
        scribble(cr, x0 + 4, y0 + sz * 1.3, 9 if small else 10, 260 if small else 500, (0.12, 0.14, 0.3, 0.75 * k),
                 seed=11, wobble=5)


def last_page(cr, t, k):
    """Close on the last page: Day 2. Your handwriting, dated tomorrow, the words too small to read."""
    n1.planks(cr, 0, 0, W, H, horizontal=False, seed=7, base=hexa("#7a5638"), dark=hexa("#553a24"), board=90)
    cr.save()
    cr.translate(360, 600)
    cr.rotate(0.03)
    toon(cr, lambda c: tk.tk_rrect(c, -300, -380, 600, 760, 12), hexa("#efe4c6"), hexa("#d9caa3"), (-6, -4), None)
    cr.set_source_rgba(0.55, 0.65, 0.85, 0.4)
    cr.set_line_width(2)
    for j in range(13):
        cr.move_to(-280, -290 + j * 54)
        cr.line_to(280, -290 + j * 54)
        cr.stroke()
    hud2d._text(cr, "TOWER 9  ·  LOG", -260, -310, 34, (0.12, 0.14, 0.3, 1), "Kalam")
    last_page_text(cr, k)
    cr.restore()
    glow(cr, 380, 620, 420, PHONE, 0.2)
    n2.phone_dark(cr, 380, 600, 900, 0.8)


def lighter(cr, t, x, y, s, flame=1.0):
    """A steel lighter with its flame."""
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    toon(cr, lambda c: tk.tk_rrect(c, -46, -10, 92, 150, 14), hexa("#b9bcc2"), hexa("#7d8088"), (-6, -6),
         (1, 1, 1, 0.5), (-6, -4), lw=4)
    toon(cr, lambda c: tk.tk_rrect(c, -40, -64, 80, 58, 8), hexa("#c9ccd2"), hexa("#8d9098"), (-4, -4), None, lw=4)
    toon(cr, lambda c: c.arc(-12, -40, 13, 0, 2 * math.pi), hexa("#55585e"), None, (0, 0), None, lw=3)   # the wheel
    if flame > 0:
        fl = flame * (1 + 0.08 * math.sin(t * 23) + 0.05 * noise(t * 9, 3))
        glow(cr, 10, -130, 220, (1, 0.6, 0.2), 0.55 * flame)
        for sc, col in ((1.0, (1, 0.55, 0.12, 0.95)), (0.62, (1, 0.86, 0.4, 1)), (0.3, (1, 1, 0.9, 1))):
            cr.save()
            cr.translate(10, -70)
            cr.scale(sc, sc * fl)
            cr.move_to(0, 0)
            cr.curve_to(-46, -30, -26, -110, 0, -170 - 8 * math.sin(t * 17))
            cr.curve_to(26, -110, 46, -30, 0, 0)
            cr.restore()
            cr.set_source_rgba(*col)
            cr.fill()
    cr.restore()


def choice(cr, t, tl):
    """'Read it...' the last page; '...burn it' the lighter's flame over the rules."""
    A, B = tl.at, tl.by_id
    burn = A("k15", "Burn")
    if t < burn - 0.1:
        last_page(cr, t, 1.0)
    else:
        n3.rules_page(cr, t, 1.0)
        lighter(cr, t, 560, 1060, 1.3, flame=seg(t, burn - 0.05, burn + 0.15))


# ------------------------------------------------------------------ the film
def shots(tl):
    A, B = tl.at, tl.by_id
    return [
        (0.0, "open"), (B["k2"].start - 0.15, "radio"), (B["k4"].start - 0.15, "other_frost"),
        (B["k5"].start - 0.15, "watch"), (B["k6"].start - 0.15, "you"), (B["k7"].start - 0.15, "other_answer"),
        (B["k8"].start - 0.15, "radio2"), (B["k10"].start - 0.15, "you_frozen"), (B["k11"].start - 0.15, "other_close"),
        (B["k12"].start - 0.15, "book"), (B["k13"].start - 0.15, "page"), (B["k14"].start - 0.15, "other_dont"),
        (B["k15"].start - 0.15, "choice"), (B["k16"].start - 0.15, "split"), (tl.total + 1, "end")]


_shots = {}


def draw(cr, t, tl):
    A, B = tl.at, tl.by_id
    if id(tl) not in _shots:
        _shots[id(tl)] = shots(tl)
    sh = _shots[id(tl)]
    k = max(i for i, (at, _) in enumerate(sh) if at <= t or i == 0)
    s0, name, s1 = sh[k][0], sh[k][1], sh[k + 1][0]
    t_out = A("k3", "out.") - 0.1                                 # the radio's light dies on "goes out"
    t_back = B["k8"].start + 0.3                                  # ...and comes back for your voice

    cr.save()
    if name == "open":                                            # your face in the radio's red blink
        camera(cr, t, s0, s1, 1.04, 1.12, cy=700)
        n3.you_room(cr, t, tk.face_mix("uneasy", "alarmed", 0.4), look=(-0.4, 0.2))
        blink = 0.6 + 0.4 * (math.sin(t * 7) > 0)
        glow(cr, 60, 1180, 520, RED, 0.45 * blink)
        cr.set_source_rgba(*RED, 0.08 * blink)
        cr.paint()
    elif name == "radio":
        camera(cr, t, s0, s1, 1.02, 1.1, cy=700)
        rx = 1.0 if t < t_out else max(0.0, 1 - (t - t_out) / 0.25) * (0.5 + 0.5 * (noise(t * 30, 2) > 0))
        radio(cr, t, rx)
    elif name == "other_frost":
        camera(cr, t, s0, s1, 1.03, 1.12, cy=700, shake=0.7)
        other_scorched(cr, t, tk.FACES["calm"], look=(0.2, 0), frost_k=seg(t, s0, s1 + 0.5))
    elif name == "watch":
        camera(cr, t, s0, s1, 1.04, 1.14, cx=440, cy=700, shake=0.5)
        m = 300.0                                                 # 5:00, then a minute back on each number
        if t >= A("k5", "fifty-nine.") - 0.15:
            m = 299.0
        if t >= A("k5", "fifty-eight.") - 0.15:
            m = 298.0
        wrist(cr, t, m)
    elif name in ("you", "you_frozen"):
        camera(cr, t, s0, s1, 1.03, 1.14 if name == "you_frozen" else 1.1, cy=700)
        f = tk.FACES["terror"] if name == "you_frozen" else tk.face_mix("uneasy", "alarmed", 0.35)
        n3.you_room(cr, t, f, look=(0.3, 0) if name == "you" else (0, 0))
    elif name in ("other_answer", "other_close", "other_dont"):
        camera(cr, t, s0, s1, 1.04, 1.12, cy=700, shake=0.5)
        look = {"other_answer": (0, 0), "other_close": (0.2, 0.1), "other_dont": (-0.5, 0.4)}[name]
        other_scorched(cr, t, tk.FACES["calm"], look=look, frost_k=1.0, tremble=0.2)
    elif name == "radio2":
        camera(cr, t, s0, s1, 1.02, 1.14, cy=700, shake=0.8)
        rx = 0.0 if t < t_back else 1.0
        radio(cr, t, rx, ch="4:44" if t >= t_back else "CH 09")  # the display: 4:44 (never spoken)
    elif name == "book":
        camera(cr, t, s0, s1, 1.0, 1.08, cy=580)
        flipping_book(cr, t, seg(t, B["k12"].start + 0.2, A("k12", "last") + 0.2))
    elif name == "page":
        camera(cr, t, s0, s1, 1.04, 1.16, cy=520)
        last_page(cr, t, seg(t, s0, B["k13"].end))
    elif name == "choice":
        camera(cr, t, s0, s1, 1.0, 1.08, cy=600)
        choice(cr, t, tl)
    elif name == "split":
        camera(cr, t, s0, s1, 1.0, 1.03, shake=0.5)
        cr.save()
        cr.rectangle(0, 0, W, H / 2)
        cr.clip()
        cr.translate(0, -200)
        last_page(cr, t, 1.0)
        cr.restore()
        cr.save()
        cr.rectangle(0, H / 2, W, H / 2)
        cr.clip()
        cr.translate(0, 300)
        n3.rules_page(cr, t, 1.0)
        lighter(cr, t, 560, 900, 1.2)
        cr.restore()
        cr.set_source_rgba(0.85, 0.9, 1, 0.8)
        cr.rectangle(0, H / 2 - 3, W, 6)
        cr.fill()
    cr.restore()

    if name == "radio2" and t >= B["k9"].start - 0.2:            # the page it read, in a ring
        n3.inset(cr, 560, 1010, 110, lambda c: (c.translate(560, 1010), c.scale(0.4, 0.4), c.translate(-360, -470),
                                                n3.page_one(c, t, 1.0)), "PAGE ONE")
    hud.finish(cr, t, flash_at=[], vig=0.6, grain=0.06)
    hud2d.stats(cr, t, [("TIME", "5:00 AM", "bad"), ("PHONE", f"{round(3 - 2 * seg(t, 0, tl.total))}%", "warn"),
                        ("IN THE TOWER", "2", "bad")])
    rules_row(cr, t, tl)
    n3.chip(cr, t, "TOWER 9 · NIGHT 4", 0.0, B["k2"].start)
    hud2d.hook(cr, t, [("YOU CHOSE", False), ("TO STAY.", True)], end=B["k1"].end + 0.1, y=250, size=92)
    hud2d.bubble(cr, t, B["k2"].start, B["k2"].end, "Tower 9. Answer me.", 360, 290, (330, 560))
    hud2d.bubble(cr, t, B["k7"].start, B["k7"].end, "Someone who answered.", 360, 280, (360, 470), creepy=True)
    hud2d.bubble(cr, t, B["k9"].start, B["k9"].end, "Day one. I hate heights.", 360, 290, (330, 560), creepy=True)
    hud2d.stamp(cr, t, A("k8", "voice.") - 0.05, B["k9"].end + 0.3, ["YOUR VOICE"], y=640)   # under the bubble
    hud2d.bubble(cr, t, B["k11"].start, B["k11"].end, "Now you know why you don't answer.", 360, 280, (360, 470),
                 creepy=True)
    hud2d.bubble(cr, t, B["k14"].start, B["k14"].end, "Don't read it. I did.", 360, 280, (360, 470), creepy=True)
    hud2d.ab_card(cr, t, A("k17", "read"), "READ IT", "BURN IT", kicker="TOWER 9 · NIGHT 4 · YOUR CHOICE",
                  decides="Night 5")
    hud2d.captions(cr, t, tl, KEY, skip=("k2", "k7", "k9", "k11", "k14"))
    cue("rain", t, 0.0, tl.total)
    cue("static", t, 0.05, max(0.3, B["k2"].start - 0.1))         # frame 0: it's already crackling
    cue("static", t, B["k2"].end + 0.05, max(0.2, t_out - B["k2"].end))
    cue("click", t, t_out)
    cue("heartbeat", t, B["k6"].start, B["k11"].end - B["k6"].start)
    cue("static", t, t_back - 0.1, B["k9"].start - t_back + 0.1)
    cue("whoosh", t, B["k12"].start + 0.2)
    cue("click", t, A("k15", "Burn") - 0.05)                      # the lighter
    cue("riser", t, B["k16"].start, B["k17"].start - B["k16"].start)


def rules_row(cr, t, tl):
    """Night 1-3's rules as chips under the stats bar; the radio rule turns red whenever the radio speaks."""
    A, B = tl.at, tl.by_id
    if t < B["k2"].start or t >= A("k17", "read"):
        return
    rules = [("#1 NO RADIO AFTER 3", ("k2", "k3", "k8", "k9", "k11")), ("#2 NEVER OPEN HATCH", ()),
             ("#3 ONE IN BY 4:44", ())]
    x = 16
    for text, hot_ids in rules:
        hot = any(B[i].start - 0.1 <= t <= B[i].end + 0.3 for i in hot_ids)
        w = hud2d.text_width(cr, text, 18, hud2d.ROUND) + 22
        tk.tk_rrect(cr, x, 116, w, 36, 18)
        cr.set_source_rgba(*(hud2d.RED[:3] if hot else (0.04, 0.04, 0.06)), 0.9)
        cr.fill_preserve()
        cr.set_source_rgba(1, 1, 1, 0.5)
        cr.set_line_width(2)
        cr.stroke()
        hud2d._text(cr, text, x + w / 2, 140, 18, (1, 1, 1, 1), hud2d.ROUND, "center")
        x += w + 8
