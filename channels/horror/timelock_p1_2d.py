"""Time Lock, Part 1 (v2): the bank heist from the thief's side. Owner, 27 Oct 2026: "For story 2 the mc is thief...
let mc for story 2 be different character not same as story 1"; picked "Remake Part 1 as thief" and the look "Sharp
and stylish" (toon2d.thief_bust). Script: out/horror/scripts_timelock_part1.md.

YOU are the thief: you faked your death five years ago; tonight you rob a bank and the night clerk behind the glass is
your little sister Lena, who thinks you drowned. Box 41 is in her name; its second key is on her keyring (the "D"
tag); her foot is an inch from the silent alarm; the time lock gives six minutes. No guns, nobody hurt. The vote: take
off the mask, or run.

    /home/user/.venv-main/bin/python channels/horror/make_2d.py timelock_p1_2d   -> out/horror/timelock_p1_2d.mp4
"""
import math

from motion import voice
from motion.engine import W, H, cairo, cue, seg

from channels.horror import hud, hud2d, sound  # noqa: F401  (sound registers the horror effects)
from channels.horror import timelock_2d as v1  # the bank: lobby, glass, counter, vault, boxes, keys, alarm
from channels.horror import toon2d as tk
from channels.horror.toon2d import INK, glow, grade, hexa, mix, noise, poly, toon

NARRATOR = dict(turbo=True)
TAIL = 0.5
MUSIC = "horror"
voice.SPEAKERS["lena"] = dict(voice="af_sky", turbo_ref="af_sky")

SCRIPT = [
    dict(id="p1", scene="shoulder", text="You walk into the bank in a mask. The night clerk is your sister."),
    dict(id="p2", scene="clipping", text="She thinks you drowned five years ago."),
    dict(id="p3", scene="lobby", text="A year of planning. Three of your crew. No guns."),
    dict(id="p4", scene="vault", text="At [two-ten,|2:10,] the vault's time lock opens. For six minutes. Then it "
                                      "seals until morning."),
    dict(id="p5", scene="boxes", text="You don't want the cash. You want one deposit box. Number [forty-one.|41.]"),
    dict(id="p6", scene="box", text="It's in her name. You rented it the week you died."),
    dict(id="p7", scene="keys", text="And the second key is on her keyring. You gave it to her for her birthday."),
    dict(id="p8", scene="alarm", text="Under her desk, her foot is an inch from the silent alarm."),
    dict(id="p9", scene="lena", text="Who are you?", speaker="lena", gap=0.35),
    dict(id="p10", scene="you", text="You can't answer. Your voice would give you away.", gap=0.35),
    dict(id="p11", scene="vault", text="At [two-ten,|2:10,] the vault clicks open. Six minutes."),
    dict(id="p12", scene="box", text="Your crew is inside. Box [forty-one|41] needs her key."),
    dict(id="p13", scene="note", text="You slide a note under the glass. One word."),
    dict(id="p14", scene="note", text="Kiddo. Only you ever called her that."),
    dict(id="p15", scene="alarm", text="Her foot touches the alarm."),
    dict(id="p16", scene="lena", text="Her eyes fill. She knows.", gap=1.2),          # the near-silent beat before it
    dict(id="p17", scene="you", text="Take off the mask, and she knows you lied for five years."),
    dict(id="p18", scene="doors", text="Run now, and box [forty-one|41] stays shut forever."),
    dict(id="p19", scene="split", text="Whatever most of you choose happens in Part [two.|2.]"),
    dict(id="p20", scene="split", text="So, do you take off the mask? Or run?", gap=0.3),
]

METADATA = dict(
    title="You Rob a Bank. The Night Clerk Is Your Sister. 🏦",
    alt_titles=["She Thinks You Drowned. Tonight You Rob Her Bank. 🏦",
                "6 Minutes, One Box, and Your Sister Behind the Glass 🏦"],
    description="""2 AM. You walk into the bank in a mask... and the night clerk is your little sister. She thinks you drowned five years ago. 🏦

You don't want the cash. You want box 41. And its second key is on her keyring.

Time Lock, Part 1. An interactive heist story: YOU decide what happens next.
💬 Take off the mask, or run? Comment A or B. Most comments decide Part 2. 👇

(Fiction. 2D animation. No guns, nobody gets hurt.)""",
    hashtags=["#HeistStory", "#InteractiveStory", "#Shorts"],
    tags=["bank heist", "heist story", "interactive story", "you decide", "choose your ending", "thief story",
          "suspense", "2d animation", "plot twist", "part 1"],
    pinned_comment="Take it off. Five years of lying is enough, she deserves the truth even if it costs you the box. "
                   "Mask off, or run? 👇 (What's on the key tag? 👀)",
)

KEY = {"mask", "sister", "drowned", "crew", "guns", "six", "seals", "cash", "one", "name", "died", "key", "birthday",
       "inch", "silent", "alarm", "answer", "voice", "note", "kiddo", "touches", "knows", "lied", "run", "forever"}
GLOVE, GLOVE_D = hexa("#16161a"), hexa("#0a0a0c")
COAT = (tk.TH_COAT, tk.TH_COAT_D)
LENA_RIM = (1, 0.85, 0.6, 0.5)


def camera(cr, t, s0, s1, z0=1.0, z1=1.06, cx=W / 2, cy=H / 2, shake=1.0):
    k = seg(t, s0, s1)
    z = z0 + (z1 - z0) * k
    cr.translate(cx + 4 * shake * noise(t * 0.7, 1), cy + 3 * shake * noise(t * 0.6, 4))
    cr.rotate(0.004 * shake * noise(t * 0.5, 7))
    cr.scale(z, z)
    cr.translate(-cx, -cy)


def you_masked(cr, x, y, s, t, expr="tense", look=(0.0, 0.0), hand=0.0):
    """You in the black knit mask; hand 0..1 raises a gloved hand to the mask's hem."""
    tk.thief_bust(cr, x, y, s, t, expr, look=look, mask=1.0, rim=v1.COLD_RIM, rim_from=(-10, -4))
    v1.ski_mask(cr, x, y + 5 * s, s, t)
    if hand > 0:
        hx, hy = x + 70 * s, y - 70 * s + (1 - hand) * 260 * s
        cr.save()
        cr.translate(hx, hy)
        cr.scale(s, s)
        toon(cr, lambda c: tk.curve(c, [(-40, 300), (-50, 90), (40, 80), (70, 300)]), *COAT, (-10, -8), None)
        toon(cr, lambda c: tk.curve(c, [(-46, 96), (-52, 30), (-30, -10), (10, -20), (44, -6), (52, 40), (40, 96)]),
             GLOVE, GLOVE_D, (-6, -5), (0.7, 0.8, 0.85, 0.4), (0, -5), lw=4)
        cr.set_source_rgba(1, 1, 1, 0.12)
        cr.set_line_width(3)
        for k in range(3):
            cr.move_to(-30 + k * 22, -8)
            cr.line_to(-28 + k * 22, 30)
            cr.stroke()
        cr.restore()


def back_office(cr, t):
    """Lena's side of the glass, behind her: the round vault door, a desk lamp, the dark office."""
    v1.vault_door(cr, t, 0.0, dials=False)
    cr.set_source_rgba(0.02, 0.03, 0.04, 0.45)
    cr.paint()
    glow(cr, 600, 760, 260, (1, 0.85, 0.6), 0.25)


def shoulder(cr, t, fear=0.4):
    """Frame 0: over your masked shoulder, Lena behind the teller glass, staring at you."""
    hud2d.blurred(cr, lambda c: back_office(c, t), sigma=10)
    tk.lena_bust(cr, 430, 1000, 1.32, t, fear=fear, look=(-0.4, 0.05), rim=LENA_RIM, rim_from=(10, -4))
    v1.teller_glass(cr, t)
    toon(cr, lambda c: c.rectangle(-20, 1080, W + 40, 220), hexa("#5b3e2a"), hexa("#3b271a"), (0, -8), None, lw=5)
    cr.save()                                                  # the back of your masked head and coat, foreground left
    cr.translate(120, 1360)
    cr.scale(1.55, 1.55)
    toon(cr, lambda c: tk.curve(c, [(-70, -10), (-180, 30), (-210, 200), (210, 200), (180, 30), (70, -10)]),
         tk.TH_COAT, tk.TH_COAT_D, (8, -6), v1.COLD_RIM, (-10, 0))
    toon(cr, lambda c: tk.curve(c, [(-108, -150), (-100, -250), (-50, -320), (20, -332), (90, -300), (112, -220),
                                    (104, -120), (60, -70), (-60, -70)]), v1.MASK, v1.MASK_D, (8, -6), v1.COLD_RIM,
         (-10, 0))
    cr.set_source_rgba(1, 1, 1, 0.05)
    cr.set_line_width(3)
    for k in range(-9, 10):
        cr.move_to(k * 11, -330)
        cr.line_to(k * 12, -80)
        cr.stroke()
    cr.restore()


def clipping(cr, t, k=1.0):
    """The clipping on her desk: LOCAL MAN LOST AT SEA, your photo (the only time we see your face)."""
    cr.set_source_rgba(0.24, 0.17, 0.12, 1)
    cr.paint()
    cr.save()
    cr.translate(360, 600)
    cr.rotate(-0.05)
    cr.set_source_rgba(0, 0, 0, 0.4)
    cr.rectangle(-266, -330, 548, 700)
    cr.fill()
    cr.set_source_rgba(*hexa("#e8e1cc"))
    cr.rectangle(-276, -342, 548, 700)
    cr.fill()
    hud2d._text(cr, "THE HARBOUR GAZETTE", 0, -292, 30, (0.2, 0.2, 0.2, 1), "Liberation Serif", "center")
    cr.set_source_rgba(0.2, 0.2, 0.2, 1)
    cr.rectangle(-250, -278, 500, 3)
    cr.fill()
    hud2d._text(cr, "LOCAL MAN", 0, -214, 64, (0.1, 0.1, 0.1, 1), "Liberation Serif", "center")
    hud2d._text(cr, "LOST AT SEA", 0, -148, 64, (0.1, 0.1, 0.1, 1), "Liberation Serif", "center")
    cr.save()
    cr.rectangle(-220, -110, 230, 280)
    cr.clip()
    cr.set_source_rgba(0.78, 0.76, 0.7, 1)
    cr.paint()
    tk.thief_bust(cr, -105, 200, 0.62, t, "calm", look=(0, 0))
    cr.set_operator(cairo.OPERATOR_SATURATE)
    cr.set_source_rgba(0.5, 0.5, 0.5, 1)                      # newsprint grey
    cr.paint()
    cr.restore()
    cr.set_source_rgba(0.1, 0.1, 0.1, 1)
    cr.set_line_width(2)
    cr.rectangle(-220, -110, 230, 280)
    cr.stroke()
    for j in range(9):                                        # column text
        cr.set_source_rgba(0.35, 0.35, 0.35, 0.8)
        cr.rectangle(30, -100 + j * 30, 210 - (j % 3) * 22, 9)
        cr.fill()
    hud2d._text(cr, "OCT 2021", 120, 220, 26, (0.5, 0.12, 0.1, 1), "Liberation Mono", "center")
    for j in range(4):
        cr.set_source_rgba(0.35, 0.35, 0.35, 0.8)
        cr.rectangle(-220, 200 + j * 30, 460 - (j % 2) * 60, 9)
        cr.fill()
    cr.restore()
    glow(cr, 560, 200, 420, (1, 0.85, 0.6), 0.22)


def keys_desk(cr, t):
    """Her keyring on the desk by the till: house keys and the small brass one with your tag on it, "D"."""
    cr.set_source_rgba(*hexa("#5b3e2a"))
    cr.paint()
    for k in range(9):
        cr.set_source_rgba(0, 0, 0, 0.12)
        cr.rectangle(0, k * 150, W, 4)
        cr.fill()
    glow(cr, 360, 300, 600, (1, 0.85, 0.6), 0.25)
    toon(cr, lambda c: tk.tk_rrect(c, 40, 120, 300, 200, 14), hexa("#2d3034"), None, (0, 0), None, lw=5)   # the till
    v1.keyring(cr, 360, 620, 2.1)
    cr.save()                                                  # a curled birthday ribbon still on the ring
    cr.translate(300, 560)
    cr.set_source_rgba(0.85, 0.2, 0.3, 1)
    cr.set_line_width(5)
    cr.move_to(0, 0)
    cr.curve_to(-40, 40, 30, 70, -10, 120)
    cr.stroke()
    cr.restore()


def note_tray(cr, t, slide=0.0, big=0.0):
    """Your gloved hand slides a deposit slip through the steel tray; then the slip, big: KIDDO."""
    hud2d.blurred(cr, lambda c: back_office(c, t), sigma=10)
    tk.lena_bust(cr, 430, 1000, 1.32, t, fear=0.7, look=(0, 0.4), rim=LENA_RIM, rim_from=(10, -4))
    v1.teller_glass(cr, t)
    toon(cr, lambda c: c.rectangle(-20, 1040, W + 40, 260), hexa("#5b3e2a"), hexa("#3b271a"), (0, -8), None, lw=5)
    toon(cr, lambda c: tk.tk_rrect(c, 200, 1050, 320, 90, 12), v1.STEEL, v1.STEEL_D, (0, -5), (1, 1, 1, 0.3), (0, -5),
         lw=4)
    sx = 360 + 0 * slide
    sy = 1200 - 120 * slide
    cr.save()
    cr.translate(sx, sy)
    cr.rotate(-0.04)
    toon(cr, lambda c: c.rectangle(-110, -40, 220, 80), hexa("#e9f0e6"), hexa("#c9d3c5"), (-2, -2), None, lw=3)
    hud2d._text(cr, "KIDDO", 0, 18, 44, (0.1, 0.12, 0.35, 1), "Kalam", "center")
    cr.restore()
    tk.hand_point(cr, sx + 90, sy + 160, 1.0, t, skin=GLOVE, sleeve=COAT)
    if big > 0:                                                # the slip, filling the screen
        cr.set_source_rgba(0, 0, 0, 0.6 * big)
        cr.paint()
        cr.save()
        cr.translate(360, 620)
        cr.rotate(-0.04)
        cr.scale(0.6 + 0.4 * big, 0.6 + 0.4 * big)
        toon(cr, lambda c: c.rectangle(-300, -160, 600, 320), hexa("#e9f0e6"), hexa("#c9d3c5"), (-4, -4), None, lw=5)
        hud2d._text(cr, "HARBOUR & PINE · DEPOSIT", -270, -118, 22, (0.35, 0.45, 0.35, 1), "Liberation Mono")
        for j in range(3):
            cr.set_source_rgba(0.6, 0.7, 0.6, 1)
            cr.rectangle(-270, -80 + j * 50, 540, 2)
            cr.fill()
        hud2d._text(cr, "KIDDO", 0, 60, 150, (0.1, 0.12, 0.35, 1), "Kalam", "center")
        cr.restore()


def entrance(cr, t):
    """The bank's glass front doors; outside, your van idling with its hazard lights blinking."""
    cr.set_source_rgba(*hexa("#20282b"))
    cr.paint()
    x0, x1, y0, y1 = 110, 610, 240, 1060
    cr.save()
    cr.rectangle(x0, y0, x1 - x0, y1 - y0)
    cr.clip()
    g = cairo.LinearGradient(0, y0, 0, y1)
    g.add_color_stop_rgba(0, 0.02, 0.03, 0.06, 1)
    g.add_color_stop_rgba(1, 0.08, 0.08, 0.1, 1)
    cr.set_source(g)
    cr.paint()
    cr.set_source_rgba(0.12, 0.12, 0.13, 1)                   # the street, the far kerb, the van
    cr.rectangle(x0, 820, x1 - x0, y1 - 820)
    cr.fill()
    toon(cr, lambda c: tk.tk_rrect(c, 170, 600, 380, 240, 24), hexa("#3b3f45"), hexa("#25282c"), (-6, -5), None, lw=5)
    toon(cr, lambda c: tk.tk_rrect(c, 190, 620, 150, 90, 10), hexa("#0d1015"), None, (0, 0), None, lw=4)
    for wx in (230, 480):
        toon(cr, lambda c, wx=wx: c.arc(wx, 840, 40, 0, 2 * math.pi), hexa("#121314"), None, (0, 0), None, lw=4)
    blink = 1.0 if (t % 0.9) < 0.45 else 0.15
    for hx in (190, 530):
        glow(cr, hx, 790, 90, (1, 0.6, 0.15), 0.8 * blink)
    glow(cr, 560, 760, 220, (1, 0.95, 0.8), 0.4)
    cr.restore()
    for xx in (x0, W / 2, x1):                                 # the door frames, brass handles
        toon(cr, lambda c, xx=xx: c.rectangle(xx - 12, y0 - 20, 24, y1 - y0 + 40), hexa("#2b2d30"), None, (0, 0), None,
             lw=4)
    for hx in (W / 2 - 50, W / 2 + 30):
        toon(cr, lambda c, hx=hx: tk.tk_rrect(c, hx, 600, 20, 160, 10), v1.BRASS, mix(v1.BRASS, INK, 0.35), (-3, -3),
             None, lw=3)
    g = cairo.LinearGradient(x0, y0, x1, y1)
    g.add_color_stop_rgba(0, 1, 1, 1, 0.08)
    g.add_color_stop_rgba(0.5, 1, 1, 1, 0.0)
    cr.set_source(g)
    cr.rectangle(x0, y0, x1 - x0, y1 - y0)
    cr.fill()
    g = cairo.LinearGradient(0, y1, 0, H)                      # marble floor
    g.add_color_stop_rgba(0, 0.3, 0.31, 0.3, 1)
    g.add_color_stop_rgba(1, 0.45, 0.45, 0.42, 1)
    cr.rectangle(0, y1 + 20, W, H)
    cr.set_source(g)
    cr.fill()


def lena_glass(cr, t, fear, tears=0.0, look=(-0.2, 0.0)):
    hud2d.blurred(cr, lambda c: back_office(c, t), sigma=10)
    tk.lena_bust(cr, 360, 1000, 1.42, t, fear=fear, tears=tears, look=look, rim=LENA_RIM, rim_from=(10, -4))
    v1.teller_glass(cr, t)
    v1.counter(cr, t, hands=False)


def you_glass(cr, t, expr="tense", hand=0.0):
    hud2d.blurred(cr, lambda c: v1.lobby(c, t), sigma=9)
    you_masked(cr, 360, 990, 1.4, t, expr, look=(0, 0.05), hand=hand)
    v1.teller_glass(cr, t, fog=0.4 + 0.3 * math.sin(t * 1.7))
    toon(cr, lambda c: c.rectangle(-20, 1080, W + 40, 220), hexa("#5b3e2a"), hexa("#3b271a"), (0, -8), None, lw=5)


# ------------------------------------------------------------------ the film
def shots(tl):
    A, B = tl.at, tl.by_id
    return [
        (0.0, "shoulder"), (B["p2"].start - 0.2, "clipping"), (B["p3"].start - 0.2, "lobby"),
        (B["p4"].start - 0.2, "vault"), (B["p5"].start - 0.2, "lobby_cash"), (A("p5", "You", nth=2) - 0.15, "boxes"),
        (B["p6"].start - 0.2, "box"), (B["p7"].start - 0.2, "keys"), (B["p8"].start - 0.2, "alarm"),
        (B["p9"].start - 0.2, "lena"), (B["p10"].start - 0.2, "you"), (B["p11"].start - 0.2, "vault_open"),
        (B["p12"].start - 0.2, "box_key"), (B["p13"].start - 0.2, "note"), (B["p15"].start - 0.2, "alarm2"),
        (B["p16"].start - 1.3, "tears"), (B["p17"].start - 0.2, "mask"), (B["p18"].start - 0.2, "doors"),
        (B["p19"].start - 0.2, "split"), (tl.total + 1, "end")]


_shots = {}


def draw(cr, t, tl):
    A, B = tl.at, tl.by_id
    if id(tl) not in _shots:
        _shots[id(tl)] = shots(tl)
    sh = _shots[id(tl)]
    k = max(i for i, (at, _) in enumerate(sh) if at <= t or i == 0)
    s0, name, s1 = sh[k][0], sh[k][1], sh[k + 1][0]
    t_open = A("p11", "clicks") - 0.05
    t_touch = A("p15", "touches") - 0.1
    gn = ((0.82, 0.95, 0.95), (0.42, 0.5, 0.55))
    warm = ((1.0, 0.95, 0.88), (0.55, 0.5, 0.45))

    cr.save()
    if name == "shoulder":
        camera(cr, t, s0, s1, 1.02, 1.1, cy=760)
        shoulder(cr, t, fear=0.3 + 0.5 * seg(t, A("p1", "sister.") - 0.3, A("p1", "sister.") + 0.3))
        grade(cr, *gn)
    elif name == "clipping":
        camera(cr, t, s0, s1, 1.0, 1.1, cy=560)
        clipping(cr, t)
        grade(cr, *warm)
    elif name in ("lobby", "lobby_cash"):
        camera(cr, t, s0, s1, 1.0, 1.08, cy=700)
        v1.lobby(cr, t, crew=seg(t, s0, s0 + 1.2) if name == "lobby" else 1.0)
        grade(cr, *gn)
    elif name in ("vault", "vault_open"):
        camera(cr, t, s0, s1, 1.0, 1.08, cy=620)
        v1.vault_door(cr, t, open_k=v1.seg(t, t_open, t_open + 1.4) if name == "vault_open" else 0.0)
        grade(cr, *gn)
    elif name == "boxes":
        camera(cr, t, s0, s1, 1.0, 1.3, cx=510, cy=690)
        cr.set_source_rgba(0.12, 0.13, 0.15, 1)
        cr.paint()
        v1.box_grid(cr, t, 60, 40, 600, 800, hi=41)
        grade(cr, *gn)
    elif name in ("box", "box_key"):
        camera(cr, t, s0, s1, 1.0, 1.1, cy=640)

        def holder(c):
            c.set_source_rgba(0.85, 0.82, 0.78, 1)
            c.paint()
            tk.lena_bust(c, 205, 870, 0.34, t, fear=0.0)
        v1.box_closeup(cr, t, holder=holder, note="RENTED 2021", key_in=name == "box_key")
        grade(cr, (0.95, 0.95, 0.95), (0.55, 0.55, 0.6))
    elif name == "keys":
        camera(cr, t, s0, s1, 1.0, 1.12, cy=620)
        keys_desk(cr, t)
        grade(cr, *warm)
    elif name in ("alarm", "alarm2"):
        camera(cr, t, s0, s1, 1.02, 1.12, cy=900, shake=1.0 + (name == "alarm2"))
        gap = 1.0 if name == "alarm" else 1 - seg(t, t_touch, t_touch + 0.6)
        v1.alarm_desk(cr, t, gap=gap, flat=True)
        grade(cr, (0.85, 0.85, 0.9), (0.45, 0.45, 0.5))
    elif name == "lena":
        camera(cr, t, s0, s1, 1.04, 1.12, cy=700)
        lena_glass(cr, t, fear=1.0)
        grade(cr, *gn)
    elif name == "you":
        camera(cr, t, s0, s1, 1.04, 1.14, cy=700)
        you_glass(cr, t, "tense")
        grade(cr, *gn)
    elif name == "note":
        camera(cr, t, s0, s1, 1.0, 1.06, cy=760)
        note_tray(cr, t, slide=seg(t, B["p13"].start, A("p13", "glass.", end=True)),
                  big=seg(t, B["p14"].start - 0.2, B["p14"].start + 0.3))
        grade(cr, *gn)
    elif name == "tears":
        camera(cr, t, s0, s1, 1.06, 1.16, cy=680, shake=0.5)
        lena_glass(cr, t, fear=0.5, tears=seg(t, s0, s0 + 0.8), look=(0, 0))
        grade(cr, *gn)
    elif name == "mask":
        camera(cr, t, s0, s1, 1.04, 1.12, cy=700)
        you_glass(cr, t, "sorrow", hand=seg(t, s0, s0 + 0.7))
        grade(cr, *gn)
    elif name == "doors":
        camera(cr, t, s0, s1, 1.0, 1.08, cy=640)
        entrance(cr, t)
        grade(cr, *gn)
    elif name == "split":
        camera(cr, t, s0, s1, 1.0, 1.03, shake=0.5)
        cr.save()
        cr.rectangle(0, 0, W, H / 2)
        cr.clip()
        cr.translate(0, -360)
        you_glass(cr, t, "sorrow", hand=1.0)
        cr.restore()
        cr.save()
        cr.rectangle(0, H / 2, W, H / 2)
        cr.clip()
        cr.translate(0, 300)
        entrance(cr, t)
        cr.restore()
        cr.set_source_rgba(0.85, 0.95, 0.95, 0.9)
        cr.rectangle(0, H / 2 - 3, W, 6)
        cr.fill()
        grade(cr, *gn)
    cr.restore()
    hud.finish(cr, t, flash_at=[], vig=0.55, grain=0.06)
    if t < t_open:
        vault = ("VAULT", "LOCKED", None) if t < B["p4"].start else ("VAULT", "OPENS 2:10", "warn", B["p4"].start)
    else:
        left = max(0.0, 360 - (t - t_open) * (360 - 271) / max(1.0, tl.total - t_open))   # 6:00 down to ~4:31
        vault = ("VAULT SEALS", f"{int(left // 60)}:{int(left % 60):02d}", "bad", t_open)
    clock_v = ("TIME", "2:10 AM", None, t_open) if t >= t_open else ("TIME", "2:00 AM", None)
    alarm = (("ALARM", "TOUCHING", "bad", t_touch) if t >= t_touch else
             ("ALARM", "1 INCH", "warn", B["p8"].start) if t >= B["p8"].start else ("ALARM", "ARMED", None))
    hud2d.stats(cr, t, [clock_v, vault, alarm])
    hud2d.hook(cr, t, [("THE CLERK IS", False), ("YOUR SISTER", True)], end=B["p1"].end + 0.15, y=270, size=96)
    hud2d.rule_tag(cr, t, A("p4", "six"), B["p4"].end + 0.3, "TIME LOCK: 6 MINUTES", y=190)
    hud2d.stamp(cr, t, A("p6", "name.", end=True) - 0.1, B["p6"].end + 0.3, ["HER NAME"], y=300)
    hud2d.bubble(cr, t, B["p9"].start, B["p9"].end, "Who are you?", 360, 260, (380, 520))
    hud2d.ab_card(cr, t, A("p20", "take"), "MASK OFF", "RUN", kicker="TIME LOCK · PART 1 · YOUR CHOICE",
                  decides="Part 2")
    hud2d.captions(cr, t, tl, KEY, skip=("p9",))
    cue("hum", t, 0.0, tl.total)                                 # the bank's night air from the first frame
    cue("click", t, B["p11"].start - 0.3)                         # the time lock trips before the line
    cue("doors", t, B["p11"].end + 0.05)                          # the vault door, after the words
    cue("heartbeat", t, B["p15"].start, B["p18"].end - B["p15"].start)
    cue("riser", t, B["p19"].start, B["p20"].start - B["p19"].start)
