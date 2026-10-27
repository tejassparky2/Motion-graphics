"""Time Lock, Part 1: a bank heist in the illustrated 2D style. Original story (owner, 27 Oct 2026: "Make next story
on bank heist"), written against the checklist in reports/Horror Shorts hooks retention comments.md.

You're the night clerk behind the teller glass. Four masked robbers walk in; one says your name. The vault's time lock
opens at 2:10 for six minutes; the silent alarm is an inch from your foot; they only want box 41, which is in your
name and opens with a brass key on your keyring. The masked man is your brother Danny, lost at sea five years ago.
No weapons, nobody hurt. The vote: help your brother, or press the alarm.

Rewatch clues: the scar on his hand, the "D" tag on the brass key, his eyes are yours. Red herring for Part 2: the
manager's office light is on.

    /home/user/.venv-main/bin/python channels/horror/make_2d.py timelock_2d   -> out/horror/timelock_2d.mp4
"""
import math

from motion import audio, voice
from motion.engine import W, H, cairo, clamp01, cue, seg

from channels.horror import hud, hud2d, sound  # noqa: F401  (sound registers the horror effects)
from channels.horror import toon2d as tk
from channels.horror.toon2d import INK, glow, grade, hexa, mix, noise, poly, toon

NARRATOR = dict(turbo=True)
TAIL = 0.5
MUSIC = "horror"
voice.SPEAKERS["danny"] = dict(voice="am_eric", turbo_ref="am_eric-1", fx="lowpass=f=3400,volume=1.35")   # behind a mask
audio.GAINS.update(hum=0.3)

SCRIPT = [
    dict(id="k1", scene="glass", text="Four masked robbers walk into your bank. And one of them says your name."),
    dict(id="k2", scene="desk", text="You're alone on the night shift, counting cash behind the glass."),
    dict(id="k3", scene="vault", text="At [two-ten,|2:10,] the vault's time lock opens. For six minutes. Then it "
                                      "seals until morning."),
    dict(id="k4", scene="alarm", text="Under your desk is the silent alarm. Your foot is an inch away."),
    dict(id="k5", scene="lobby", text="They don't touch the cash. They want one deposit box. Number [forty-one.|41.]"),
    dict(id="k6", scene="box", text="The box is in your name. You've never rented a box in your life."),
    dict(id="k7", scene="keys", text="It takes two keys. He has one. The other is on your keyring."),
    dict(id="k8", scene="glass", text="Easy, kiddo. Nobody gets hurt tonight.", speaker="danny", gap=0.35),
    dict(id="k9", scene="face", text="Kiddo. Only one person ever called you that.", gap=0.35),
    dict(id="k10", scene="vault", text="At [two-ten,|2:10,] the vault clicks open. Six minutes."),
    dict(id="k11", scene="photo", text="Inside box [forty-one,|41,] there's no money. Just a photo of you, taken this "
                                       "morning."),
    dict(id="k12", scene="alarm", text="Your foot touches the alarm."),
    dict(id="k13", scene="glass", text="Don't. Please. Not after five years.", speaker="danny", gap=0.35),
    dict(id="k14", scene="glass", text="He pulls off the mask.", gap=0.35),
    dict(id="k15", scene="reveal", text="It's your brother, Danny. Lost at sea five years ago.", gap=1.2),   # the silent beat
    dict(id="k16", scene="reveal", text="Help him, and you're a thief."),
    dict(id="k17", scene="alarm", text="Press the alarm, and you lose him again."),
    dict(id="k18", scene="split", text="Whatever most of you choose happens in Part [two.|2.]"),
    dict(id="k19", scene="split", text="So, do you help your brother? Or press the alarm?", gap=0.3),
]

METADATA = dict(
    title="The Bank Robber Knows Your Name 🏦",
    alt_titles=["They Didn't Want the Money. They Wanted Box 41. 🏦", "6 Minutes. One Box. And It's in Your Name. 🏦"],
    description="""2 AM. You're alone on the night shift when four masked robbers walk into your bank... and one of them says your name. 🏦

They don't want the cash. They want box 41. It's in your name, and you've never rented a box in your life.

Time Lock, Part 1. An interactive mystery: YOU decide what happens next.
💬 Help him, or press the alarm? Comment A or B. Most comments decide Part 2. 👇

(Fiction. 2D animation. Nobody gets hurt.)""",
    hashtags=["#Mystery", "#InteractiveStory", "#Shorts"],
    tags=["bank heist", "heist story", "interactive story", "you decide", "choose your ending", "mystery story",
          "suspense", "2d animation", "plot twist", "part 1"],
    pinned_comment="Team alarm. He let you grieve for FIVE years and came back with a heist. Family or not, that's on "
                   "him. Help him, or press it? 👇 (Look at his hand 👀)",
)

KEY = {"masked", "name", "alone", "six", "seals", "silent", "alarm", "inch", "cash", "one", "never", "two", "keyring",
       "kiddo", "nobody", "photo", "morning", "touches", "don't", "mask", "brother", "danny", "thief", "lose"}

SHIRT = (hexa("#e8ecf1"), hexa("#b9c1cc"), hexa("#ffffff"))          # you: the clerk's white shirt
VEST = (hexa("#263a5c"), hexa("#16243b"), hexa("#35507a"))           # ... under a navy vest
DANNY = (hexa("#2c2f36"), hexa("#1a1c21"), hexa("#3d414a"))          # his charcoal hoodie
MASK, MASK_D = hexa("#18181c"), hexa("#0b0b0e")
TEAL = (0.55, 0.9, 0.85)                                            # the bank's night lights
BRASS = hexa("#c9a050")
STEEL, STEEL_D = hexa("#8c949c"), hexa("#565d65")
ALARM_RED = (1.0, 0.12, 0.1)
COLD_RIM = (0.65, 0.95, 0.9, 0.55)


def camera(cr, t, s0, s1, z0=1.0, z1=1.06, cx=W / 2, cy=H / 2, shake=1.0):
    k = seg(t, s0, s1)
    z = z0 + (z1 - z0) * k
    cr.translate(cx + 4 * shake * noise(t * 0.7, 1), cy + 3 * shake * noise(t * 0.6, 4))
    cr.rotate(0.004 * shake * noise(t * 0.5, 7))
    cr.scale(z, z)
    cr.translate(-cx, -cy)


# ------------------------------------------------------------------ people
def ski_mask(cr, x, y, s, t, lift=0.0):
    """A black knit mask over a you_bust-shaped head (x, y = base of the neck). lift 0..1 pulls it up off the face."""
    hx, hy = x, y - 175 * s
    cr.save()
    cr.translate(hx, hy)
    cr.scale(s, s)
    cut = 116 - 300 * lift                                    # the mask's lower edge rises as it comes off
    cr.save()
    cr.rectangle(-200, -260, 400, cut + 260)
    cr.clip()
    shape = lambda c: (tk.curve(c, [(-112, -10), (-110, -96), (-66, -150), (0, -162), (66, -150), (110, -96),
                                    (112, -10), (100, 56), (66, 100), (0, 120), (-66, 100), (-100, 56)]),
                       c.new_sub_path(), c.save(), c.translate(-42, -8), c.scale(1, 0.62), c.arc(0, 0, 40, 0, 2 * math.pi),
                       c.restore(), c.new_sub_path(), c.save(), c.translate(42, -8), c.scale(1, 0.62),
                       c.arc(0, 0, 40, 0, 2 * math.pi), c.restore(), c.new_sub_path(), c.save(), c.translate(0, 66),
                       c.scale(1, 0.55), c.arc(0, 0, 30, 0, 2 * math.pi), c.restore())
    cr.new_path()
    shape(cr)
    cr.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)
    cr.set_source_rgba(*MASK)
    cr.fill_preserve()
    cr.save()
    cr.clip()
    cr.set_source_rgba(1, 1, 1, 0.05)                         # knit ribs
    cr.set_line_width(3)
    for k in range(-11, 12):
        cr.move_to(k * 10, -170)
        cr.line_to(k * 11, 130)
        cr.stroke()
    cr.set_source_rgba(*COLD_RIM[:3], 0.35)                   # a cold rim of light along one side
    cr.set_line_width(10)
    cr.arc(8, -10, 122, math.pi * 1.05, math.pi * 1.5)
    cr.stroke()
    cr.restore()
    cr.set_fill_rule(cairo.FILL_RULE_WINDING)
    cr.new_path()
    shape(cr)
    cr.set_source_rgba(*INK)
    cr.set_line_width(4.5)
    cr.stroke()
    cr.restore()
    if lift > 0:                                              # the rolled-up band where the mask bunches
        cr.save()
        cr.translate(0, cut)
        toon(cr, lambda c: tk.tk_rrect(c, -118, -16, 236, 32, 14), MASK, MASK_D, (0, -5), None, lw=4)
        cr.restore()
    cr.restore()


def stubble(cr, x, y, s):
    hx, hy = x, y - 175 * s
    cr.set_source_rgba(0.12, 0.08, 0.06, 0.5)
    for k in range(80):
        a = (k * 0.618 * 2 * math.pi) % (2 * math.pi)
        r = 0.55 + 0.45 * ((k * 0.382) % 1)
        px, py = 88 * r * math.cos(a), 30 + 76 * r * abs(math.sin(a))
        if py > 50 and not (abs(px) < 30 and 54 < py < 84):
            cr.arc(hx + px * s, hy + py * s, 1.7 * s + 0.4, 0, 2 * math.pi)
            cr.fill()


def danny(cr, x, y, s, t, mask=1.0, face=None, look=(0.0, 0.0), rim=COLD_RIM):
    """Your older brother: your face, older and tired, stubble; a black knit mask (mask = 1 on, 0 off)."""
    f = face or tk.face_mix("calm", "uneasy", 0.6)
    tk.you_bust(cr, x, y, s, f, t, look=look, rim=rim, rim_from=(-10, -4), coat=DANNY, blink=True)
    if mask < 1:
        stubble(cr, x, y, s)
    if mask > 0:
        ski_mask(cr, x, y, s, t, lift=1 - mask)


def you(cr, x, y, s, t, face, look=(0.0, 0.0), sweat=0.0, tremble=0.0, rim=COLD_RIM):
    """The night clerk: white shirt, navy vest, a lanyard badge."""
    tk.you_bust(cr, x, y, s, face, t, look=look, rim=rim, rim_from=(-10, -4), coat=VEST, sweat=sweat, tremble=tremble)
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    toon(cr, lambda c: poly(c, [(-30, -6), (30, -6), (14, 120), (-14, 120)]), SHIRT[0], SHIRT[1], (0, -4), None, lw=3)
    cr.set_source_rgba(0.75, 0.12, 0.12, 1)                  # lanyard and badge
    cr.set_line_width(6)
    cr.move_to(-40, 10)
    cr.line_to(-8, 200)
    cr.move_to(40, 10)
    cr.line_to(8, 200)
    cr.stroke()
    toon(cr, lambda c: tk.tk_rrect(c, -40, 196, 80, 100, 8), hexa("#f2f2f2"), hexa("#cfcfcf"), (-3, -3), None, lw=3)
    cr.set_source_rgba(*VEST[0])
    cr.rectangle(-30, 206, 60, 14)
    cr.fill()
    cr.restore()


# ------------------------------------------------------------------ the bank
def lobby(cr, t, crew=0.0, office=True):
    """The banking hall at night, from behind the counter: marble floor, pillars, the big brass clock, the exit sign;
    the manager's office light on at the back (Part 2's red herring)."""
    vx, vy = 360, 560
    g = cairo.LinearGradient(0, 0, 0, H)
    g.add_color_stop_rgba(0, 0.07, 0.11, 0.12, 1)
    g.add_color_stop_rgba(1, 0.03, 0.05, 0.06, 1)
    cr.set_source(g)
    cr.paint()
    cr.set_source_rgba(0.16, 0.2, 0.2, 1)                     # back wall
    cr.rectangle(150, 260, 420, 330)
    cr.fill()
    hud2d._text(cr, "HARBOUR & PINE", 360, 312, 34, (0.85, 0.72, 0.42, 0.9), "Liberation Serif", "center")
    toon(cr, lambda c: c.arc(360, 420, 62, 0, 2 * math.pi), hexa("#e9e2cf"), hexa("#cfc5aa"), (-4, -3), None, lw=5)
    cr.set_source_rgba(*BRASS)
    cr.set_line_width(7)
    cr.arc(360, 420, 66, 0, 2 * math.pi)
    cr.stroke()
    for frac, ln, w in ((2.0 / 12, 30, 6), (0.0, 46, 4)):     # two o'clock
        a = frac * 2 * math.pi
        cr.set_source_rgba(*INK)
        cr.set_line_width(w)
        cr.move_to(360, 420)
        cr.line_to(360 + ln * math.sin(a), 420 - ln * math.cos(a))
        cr.stroke()
    if office:                                                # a lit office door at the back
        cr.set_source_rgba(1, 0.86, 0.55, 0.85)
        cr.rectangle(470, 480, 46, 110)
        cr.fill()
        glow(cr, 493, 535, 90, (1, 0.8, 0.5), 0.35)
        hud2d._text(cr, "MANAGER", 493, 470, 13, (0.85, 0.8, 0.7, 0.8), "Liberation Sans", "center")
    cr.set_source_rgba(0.9, 0.1, 0.08, 1)                     # exit sign
    cr.rectangle(200, 470, 48, 18)
    cr.fill()
    glow(cr, 224, 479, 60, (1, 0.15, 0.1), 0.3)
    for k in range(-8, 9):                                     # marble floor in perspective
        cr.move_to(vx + k * 26, 590)
        cr.line_to(vx + k * 170, H)
        cr.set_source_rgba(0.5, 0.5, 0.45, 0.25)
        cr.set_line_width(2)
        cr.stroke()
    poly(cr, [(150, 590), (570, 590), (W + 300, H), (-300, H)])
    g = cairo.LinearGradient(0, 590, 0, H)
    g.add_color_stop_rgba(0, 0.24, 0.26, 0.25, 0.85)
    g.add_color_stop_rgba(1, 0.42, 0.42, 0.38, 0.85)
    cr.set_source(g)
    cr.fill()
    for k in range(6):
        y = 590 + (H - 590) * (k / 6) ** 1.7
        cr.move_to(0, y)
        cr.line_to(W, y)
        cr.set_source_rgba(0.12, 0.12, 0.12, 0.35)
        cr.set_line_width(2)
        cr.stroke()
    for x0, x1 in ((40, 130), (590, 680)):                    # pillars
        toon(cr, lambda c, x0=x0, x1=x1: c.rectangle(x0, 120, x1 - x0, 900), hexa("#cfc8b6"), hexa("#a39b88"),
             (-8, 0), None, lw=4)
        cr.set_source_rgba(0, 0, 0, 0.15)
        for j in range(4):
            cr.rectangle(x0 + 12 + j * 20, 130, 4, 880)
        cr.fill()
    for k in range(3):                                         # cash trolleys by the counter
        bx = 180 + k * 150
        toon(cr, lambda c, bx=bx: c.rectangle(bx, 760, 110, 70), STEEL, STEEL_D, (-4, -3), None, lw=3)
        for j in range(3):
            toon(cr, lambda c, bx=bx, j=j: c.rectangle(bx + 8 + j * 32, 738, 28, 22), hexa("#8fb08a"), hexa("#6a8a66"),
                 (-2, -2), None, lw=2)
    if crew > 0:                                               # three masked figures crossing the hall
        for k, (x, y, sc) in enumerate(((210, 760, 0.42), (360, 740, 0.38), (520, 770, 0.44))):
            ox = (1 - crew) * 120 * (1 if k % 2 else -1)
            cr.save()
            cr.translate(ox, 0)
            tk.you_bust(cr, x, y, sc, tk.FACES["calm"], t + k, coat=DANNY, rim=COLD_RIM, rim_from=(-10, -4))
            ski_mask(cr, x, y, sc, t)
            cr.restore()
    g = cairo.LinearGradient(0, 0, 0, 400)                     # teal night lights from above
    g.add_color_stop_rgba(0, *TEAL, 0.18)
    g.add_color_stop_rgba(1, *TEAL, 0.0)
    cr.set_source(g)
    cr.paint()


def teller_glass(cr, t, fog=0.0, fog_at=(372, 800)):
    """The bulletproof glass between you and him: a faint reflection, the round speaking grille, his breath fogging it."""
    g = cairo.LinearGradient(0, 0, W, H)
    g.add_color_stop_rgba(0, 1, 1, 1, 0.07)
    g.add_color_stop_rgba(0.45, 1, 1, 1, 0.0)
    g.add_color_stop_rgba(0.6, 1, 1, 1, 0.05)
    g.add_color_stop_rgba(1, 1, 1, 1, 0.0)
    cr.set_source(g)
    cr.paint()
    cr.set_source_rgba(1, 1, 1, 0.1)
    cr.set_line_width(14)
    cr.move_to(80, 0)
    cr.line_to(-120, 600)
    cr.stroke()
    gx, gy = 600, 640                                          # the speaking grille
    toon(cr, lambda c: c.arc(gx, gy, 54, 0, 2 * math.pi), (0.75, 0.78, 0.8, 0.5), None, (0, 0), None, lw=4)
    cr.set_source_rgba(0.1, 0.1, 0.12, 0.85)
    for i in range(-3, 4):
        for j in range(-3, 4):
            if i * i + j * j <= 9:
                cr.arc(gx + i * 13, gy + j * 13, 3.5, 0, 2 * math.pi)
                cr.fill()
    if fog > 0:
        glow(cr, fog_at[0], fog_at[1], 120, (0.85, 0.9, 0.92), 0.35 * fog, op=cairo.OPERATOR_OVER)


def counter(cr, t, hands=True, tray=0.0, keys=False):   # hands = the cash stack you were counting
    """Your side of the counter, in the foreground: the wooden top, a cash stack, your hands; the steel deal tray."""
    toon(cr, lambda c: c.rectangle(-20, 1040, W + 40, 260), hexa("#5b3e2a"), hexa("#3b271a"), (0, -8), None, lw=5)
    cr.set_source_rgba(*BRASS[:3], 0.9)
    cr.rectangle(-20, 1036, W + 40, 8)
    cr.fill()
    toon(cr, lambda c: tk.tk_rrect(c, 250, 1050, 220, 70, 10), STEEL, STEEL_D, (0, -5), (1, 1, 1, 0.3), (0, -5), lw=4)
    if hands:
        for k in range(5):                                     # a stack of notes
            toon(cr, lambda c, k=k: c.rectangle(80 + k * 2, 1130 - k * 9, 170, 34), hexa("#9db694"), hexa("#78926f"),
                 (-3, -3), None, lw=2.5)
        cr.set_source_rgba(0.85, 0.2, 0.15, 1)                # a paper band around the stack
        cr.rectangle(150, 1094, 30, 40)
        cr.fill()
        toon(cr, lambda c: tk.tk_rrect(c, 520, 1100, 150, 90, 10), hexa("#3a3d42"), hexa("#24262a"), (-3, -3), None,
             lw=4)                                             # the note counter
        hud2d._text(cr, "0000", 595, 1150, 30, (0.5, 1, 0.6, 1), "Liberation Mono", "center")
    if keys:                                                   # your keyring sliding through the tray
        kx = 360 - 120 * tray
        keyring(cr, kx, 1080, 0.7)


def keyring(cr, x, y, s, tag=True):
    """Your keys: two silver house keys and a small brass one with a paper tag: "D"."""
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    cr.set_source_rgba(0.78, 0.8, 0.84, 1)
    cr.set_line_width(6)
    cr.arc(0, 0, 26, 0, 2 * math.pi)
    cr.stroke()
    for k, (a, col, ln) in enumerate(((0.6, (0.8, 0.82, 0.86, 1), 90), (1.2, (0.7, 0.72, 0.76, 1), 80),
                                      (2.3, BRASS, 60))):
        cr.save()
        cr.rotate(a)
        cr.translate(26, 0)
        toon(cr, lambda c, ln=ln: (c.arc(14, 0, 14, 0, 2 * math.pi), c.rectangle(24, -6, ln, 12)), col,
             mix(col, INK, 0.35), (-2, -2), None, lw=3)
        cr.restore()
    if tag:
        cr.save()
        cr.rotate(2.3)
        cr.translate(140, 20)
        cr.rotate(-2.3 + 0.2)
        toon(cr, lambda c: tk.tk_rrect(c, -26, -18, 52, 36, 5), hexa("#efe6cf"), hexa("#d4c8a8"), (-2, -2), None, lw=3)
        hud2d._text(cr, "D", 0, 12, 30, (0.1, 0.1, 0.3, 1), "Kalam", "center")
        cr.restore()
    cr.restore()


def scar_hand(cr, x, y, s, t, holding="key"):
    """His bare right hand, a scar across the back of it, holding a brass key (or a photo)."""
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    toon(cr, lambda c: tk.curve(c, [(-260, -40), (-90, -70), (-60, 40), (-250, 60)]), DANNY[0], DANNY[1], (-6, -5),
         None)                                                 # the sleeve
    toon(cr, lambda c: tk.curve(c, [(-100, -56), (-20, -70), (40, -60), (80, -40), (86, -10), (60, 20), (10, 40),
                                    (-80, 44)]), tk.SKIN, tk.SKIN_D, (-6, -5), None, lw=4)
    for k in range(4):                                         # knuckles and fingers curled over
        toon(cr, lambda c, k=k: tk.curve(c, [(40 + k * 4, -54 + k * 22), (96 + k * 2, -48 + k * 22),
                                             (100 + k * 2, -30 + k * 22), (44 + k * 4, -36 + k * 22)]), tk.SKIN,
             tk.SKIN_D, (-4, -3), None, lw=3)
    cr.set_source_rgba(0.72, 0.38, 0.36, 1)                   # the scar
    cr.set_line_width(7)
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    cr.move_to(-70, -36)
    cr.curve_to(-40, -10, -10, 0, 30, 14)
    cr.stroke()
    cr.set_source_rgba(0.95, 0.75, 0.7, 0.9)
    cr.set_line_width(2.5)
    for k in range(5):
        px = -60 + k * 20
        cr.move_to(px, -30 + k * 10 - 7)
        cr.line_to(px + 6, -30 + k * 10 + 7)
        cr.stroke()
    if holding == "key":
        cr.save()
        cr.translate(100, 30)
        cr.rotate(0.3)
        toon(cr, lambda c: (c.arc(0, 0, 16, 0, 2 * math.pi), c.rectangle(10, -6, 70, 12)), BRASS, mix(BRASS, INK, 0.35),
             (-2, -2), None, lw=3)
        cr.restore()
    cr.restore()


def alarm_desk(cr, t, gap=1.0, press=0.0, flat=False):
    """Under the desk, lit by the alarm's red light and the lamp above: a shoe, an inch (gap = 1) from the red
    silent-alarm pedal; a yellow measure marks the inch. flat = a woman's black flat (Lena's) instead of an oxford."""
    g = cairo.LinearGradient(0, 0, 0, H)                     # the knee-space: the desk's back panel, then carpet
    g.add_color_stop_rgba(0, *hexa("#4a3424"))
    g.add_color_stop_rgba(0.55, *hexa("#33241a"))
    cr.set_source(g)
    cr.paint()
    cr.set_source_rgba(0, 0, 0, 0.25)
    for k in range(6):
        cr.rectangle(0, 120 + k * 100, W, 3)
    cr.fill()
    toon(cr, lambda c: c.rectangle(-20, -20, W + 40, 130), hexa("#5b3e2a"), hexa("#3b271a"), (0, -6), None, lw=5)
    g = cairo.LinearGradient(0, 760, 0, H)
    g.add_color_stop_rgba(0, *hexa("#4b4d52"))
    g.add_color_stop_rgba(1, *hexa("#2c2e32"))
    cr.rectangle(0, 760, W, H - 760)
    cr.set_source(g)
    cr.fill()
    cr.set_source_rgba(1, 1, 1, 0.05)                        # carpet weave
    for k in range(60):
        x, y = (k * 97.3) % W, 770 + (k * 53.1) % (H - 780)
        cr.rectangle(x, y, 18, 2)
    cr.fill()
    glow(cr, 360, 0, 700, (1, 0.85, 0.6), 0.18)             # the desk lamp's spill over the edge
    px, py = 500, 860                                          # the pedal box, big and centred right
    on = 0.65 + 0.35 * (noise(t * 6, 2) > 0) if press > 0 else 0.6
    glow(cr, px, py + 40, 330, ALARM_RED, 0.32 * on)
    toon(cr, lambda c: tk.tk_rrect(c, px - 120, py, 240, 140, 16), hexa("#4a4e55"), hexa("#2e3136"), (-5, -5),
         (1, 0.6, 0.55, 0.45), (0, -6), lw=5)
    toon(cr, lambda c: (c.save(), c.translate(px, py + 8 + 10 * press), c.scale(1, 0.42), c.arc(0, 0, 84, 0, 2 * math.pi),
                        c.restore()), (0.92, 0.12, 0.09, 1), (0.6, 0.05, 0.05, 1), (0, -5), (1, 0.7, 0.7, 0.6), (0, -6),
         lw=5)
    hud2d._text(cr, "ALARM", px, py + 118, 32, (0.98, 0.94, 0.9, 1), "Liberation Sans", "center")
    toe = px - 132 - 46 * gap                                  # an inch is ~46 px at this distance
    cr.save()
    cr.translate(toe, 930 - 14 * press)
    toon(cr, lambda c: poly(c, [(-470, -620), (-250, -640), (-170, -150), (-360, -120)]), VEST[0], VEST[1], (-6, -5),
         (0.8, 0.9, 1, 0.3), (6, 0), lw=5)                     # the trouser leg, from the knee down
    shoe = (lambda c: tk.curve(c, [(-340, -110), (-170, -118), (-60, -104), (0, -74), (8, -34), (-30, -6), (-360, -4),
                                   (-370, -56)])) if flat else (
        lambda c: tk.curve(c, [(-360, -150), (-170, -170), (-60, -140), (0, -96), (8, -40), (-30, -6), (-380, -4),
                               (-392, -70)]))
    toon(cr, shoe, hexa("#1d1d21"), hexa("#0f0f12"), (0, -6), (1, 0.55, 0.5, 0.55), (-8, 0), lw=5)
    cr.set_source_rgba(0.55, 0.55, 0.6, 1)                    # the sole
    cr.rectangle(-386, -12, 384, 12)
    cr.fill()
    cr.set_source_rgba(1, 1, 1, 0.3)                          # a shine along the toe
    cr.set_line_width(5)
    cr.move_to(-180, -150)
    cr.curve_to(-110, -152, -50, -132, -14, -92)
    cr.stroke()
    if flat:                                                  # a thin strap across the foot
        cr.set_source_rgba(0.1, 0.1, 0.12, 1)
        cr.set_line_width(8)
        cr.move_to(-250, -118)
        cr.line_to(-226, -20)
        cr.stroke()
    else:
        cr.set_source_rgba(0.6, 0.6, 0.65, 0.9)               # laces
        cr.set_line_width(3)
        for k in range(4):
            cr.move_to(-250 + k * 22, -160 + k * 2)
            cr.line_to(-236 + k * 22, -138 + k * 2)
            cr.stroke()
    cr.restore()
    if gap > 0.15:                                             # the inch, measured
        ya = 1000
        cr.set_source_rgba(*hud2d.YELLOW)
        cr.set_line_width(4)
        cr.move_to(toe + 8, ya)
        cr.line_to(px - 120, ya)
        for xx in (toe + 8, px - 120):
            cr.move_to(xx, ya - 14)
            cr.line_to(xx, ya + 14)
        cr.stroke()
        hud2d._text(cr, "1 INCH", (toe + px - 112) / 2, ya + 48, 30, hud2d.YELLOW, hud2d.ROUND, "center",
                    outline=INK, ow=6)


def vault_door(cr, t, open_k=0.0, dials=True):
    """The round vault door in the steel wall behind your desk, with its time-lock dials; it swings open on open_k."""
    tex_g = cairo.LinearGradient(0, 0, W, 0)
    tex_g.add_color_stop_rgba(0, *STEEL_D)
    tex_g.add_color_stop_rgba(0.5, *STEEL)
    tex_g.add_color_stop_rgba(1, *STEEL_D)
    cr.set_source(tex_g)
    cr.paint()
    cx, cy, r = 360, 620, 290
    cr.set_source_rgba(0.06, 0.06, 0.07, 1)                  # the opening
    cr.arc(cx, cy, r + 12, 0, 2 * math.pi)
    cr.fill()
    if open_k > 0:                                            # light from inside, and the box wall far in
        cr.save()
        cr.arc(cx, cy, r + 8, 0, 2 * math.pi)
        cr.clip()
        g = cairo.RadialGradient(cx, cy, 20, cx, cy, r)
        g.add_color_stop_rgba(0, 1, 0.95, 0.8, 0.95 * open_k)
        g.add_color_stop_rgba(1, 0.5, 0.45, 0.35, 0.8 * open_k)
        cr.set_source(g)
        cr.paint()
        box_grid(cr, t, cx - 170, cy - 200, 340, 400, hi=None, a=open_k)
        cr.restore()
    ang = open_k * 1.25                                        # the door swings toward you on its hinge (right)
    sx = math.cos(ang)
    cr.save()
    cr.translate(cx + r * (1 - sx), cy)
    cr.scale(max(0.08, sx), 1)
    toon(cr, lambda c: c.arc(0, 0, r, 0, 2 * math.pi), hexa("#a9b1b9"), hexa("#6d757d"), (-10, -8), (1, 1, 1, 0.4),
         (0, -8), lw=8)
    for rr in (r - 40, r - 90):
        cr.set_source_rgba(*INK[:3], 0.5)
        cr.set_line_width(4)
        cr.arc(0, 0, rr, 0, 2 * math.pi)
        cr.stroke()
    for k in range(14):                                        # bolts
        a = k * 2 * math.pi / 14
        toon(cr, lambda c, a=a: c.arc((r - 22) * math.cos(a), (r - 22) * math.sin(a), 11, 0, 2 * math.pi),
             hexa("#d0d6dc"), hexa("#8d959d"), (-2, -2), None, lw=3)
    cr.set_source_rgba(0.2, 0.22, 0.24, 1)                   # the wheel
    cr.set_line_width(16)
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    rot = t * 0.0 + open_k * 1.2
    for k in range(4):
        a = rot + k * math.pi / 2
        cr.move_to(0, 0)
        cr.line_to(120 * math.cos(a), 120 * math.sin(a))
        cr.stroke()
    toon(cr, lambda c: c.arc(0, 0, 34, 0, 2 * math.pi), hexa("#c9ced3"), hexa("#8d959d"), (-3, -3), None, lw=4)
    cr.restore()
    if dials:                                                  # the time-lock box: three clock movements
        toon(cr, lambda c: tk.tk_rrect(c, 430, 210, 250, 110, 12), hexa("#2d3034"), None, (0, 0), None, lw=5)
        for k in range(3):
            dx = 475 + k * 80
            toon(cr, lambda c, dx=dx: c.arc(dx, 265, 30, 0, 2 * math.pi), hexa("#efe9da"), None, (0, 0), None, lw=3)
            cr.set_source_rgba(*INK)
            cr.set_line_width(3)
            a = 2 * math.pi * ((t / 20 + k * 0.13) % 1)
            cr.move_to(dx, 265)
            cr.line_to(dx + 22 * math.sin(a), 265 - 22 * math.cos(a))
            cr.stroke()
        hud2d._text(cr, "TIME LOCK", 555, 345, 22, (0.9, 0.9, 0.85, 1), "Liberation Mono", "center")


def box_grid(cr, t, x0, y0, w, h, hi=41, a=1.0, label=False, open_k=0.0):
    """Rows of numbered safe-deposit doors; `hi` glows. label = your ID photo on box 41's holder card."""
    cols, rows = 6, 8                                          # 48 boxes, so 41 is on the wall
    bw, bh = w / cols, h / rows
    for r in range(rows):
        for c in range(cols):
            n = r * cols + c + 1
            x, y = x0 + c * bw, y0 + r * bh
            base = mix(hexa("#b9c0c7"), hexa("#d8b56a"), 0.6) if n == hi else hexa("#b9c0c7")
            cr.save()
            cr.push_group()
            toon(cr, lambda cc, x=x, y=y: tk.tk_rrect(cc, x + 3, y + 3, bw - 6, bh - 6, 4), base, mix(base, INK, 0.3),
                 (-2, -2), None, lw=2.5)
            for kx in (0.35, 0.65):                            # two keyholes
                cr.set_source_rgba(0.1, 0.1, 0.1, 1)
                cr.arc(x + bw * kx, y + bh * 0.55, max(2, bw * 0.05), 0, 2 * math.pi)
                cr.fill()
            hud2d._text(cr, str(n), x + bw * 0.5, y + bh * 0.32, max(9, bh * 0.22), INK, "Liberation Mono", "center")
            cr.pop_group_to_source()
            cr.paint_with_alpha(a)
            cr.restore()
            if n == hi:
                glow(cr, x + bw / 2, y + bh / 2, bw, (1, 0.85, 0.45), 0.4 * a)
                if label:
                    toon(cr, lambda cc, x=x, y=y: tk.tk_rrect(cc, x + bw * 0.12, y + bh * 0.7, bw * 0.76, bh * 0.26, 3),
                         hexa("#f4f1e8"), None, (0, 0), None, lw=2)


def box_closeup(cr, t, glow_k=1.0, holder=None, note=None, key_in=False):
    """Box 41 up close: its holder card with a photo (holder draws it; default: you) and the word HOLDER; note = an
    extra line on the card (e.g. RENTED 5 YEARS AGO); key_in = one key already in its lock, the other keyhole glowing."""
    cr.set_source_rgba(0.12, 0.13, 0.15, 1)
    cr.paint()
    box_grid(cr, t, -120, -80, 960, 1440, hi=41, a=1.0)
    cx, cy = 360, 640
    toon(cr, lambda c: tk.tk_rrect(c, 70, 400, 580, 470, 18), mix(hexa("#b9c0c7"), hexa("#d8b56a"), 0.6),
         hexa("#8a7340"), (-6, -5), (1, 1, 1, 0.4), (0, -6), lw=6)
    hud2d._text(cr, "41", cx, 500, 90, INK, "Liberation Mono", "center")
    for kx in (250, 470):
        cr.set_source_rgba(0.08, 0.08, 0.08, 1)
        cr.arc(kx, 600, 18, 0, 2 * math.pi)
        cr.fill()
        cr.rectangle(kx - 5, 600, 10, 34)
        cr.fill()
    if key_in:                                                 # his key in the left lock; the right one waits
        toon(cr, lambda c: (c.arc(250, 560, 22, 0, 2 * math.pi), c.rectangle(242, 560, 16, 50)), BRASS,
             mix(BRASS, INK, 0.35), (-2, -2), None, lw=3)
        glow(cr, 470, 610, 90, (1, 0.85, 0.45), 0.45 + 0.25 * math.sin(t * 5))
    toon(cr, lambda c: tk.tk_rrect(c, 130, 680, 460, 160, 8), hexa("#f4f1e8"), hexa("#d9d3c2"), (-3, -3), None, lw=3)
    hud2d._text(cr, "HOLDER", 360, 716, 26, (0.3, 0.3, 0.35, 1), "Liberation Mono", "center")
    cr.save()                                                  # your ID photo on the card
    cr.rectangle(150, 690, 110, 140)
    cr.clip()
    cr.set_source_rgba(0.75, 0.82, 0.88, 1)
    cr.paint()
    if holder:
        holder(cr)
    else:
        tk.you_bust(cr, 205, 860, 0.36, tk.FACES["calm"], t, coat=VEST, blink=False)
    cr.restore()
    cr.set_source_rgba(*INK)
    cr.set_line_width(3)
    cr.rectangle(150, 690, 110, 140)
    cr.stroke()
    if note:
        hud2d._text(cr, note, 420, 790, 30, (0.6, 0.12, 0.1, 1), "Liberation Mono", "center")
    else:
        for k in range(3):
            cr.set_source_rgba(0.4, 0.4, 0.45, 0.6)
            cr.rectangle(290, 750 + k * 28, 260 - k * 60, 10)
            cr.fill()
    glow(cr, 360, 640, 420, (1, 0.85, 0.45), 0.25 * glow_k)


def photo_card(cr, x, y, s, t, rot=-0.05):
    """The photo from box 41: you at a bus stop this morning, a printed date in the corner."""
    cr.save()
    cr.translate(x, y)
    cr.rotate(rot)
    cr.scale(s, s)
    cr.set_source_rgba(0, 0, 0, 0.4)
    cr.rectangle(-200, -150, 420, 330)
    cr.fill()
    cr.set_source_rgba(0.97, 0.96, 0.93, 1)
    cr.rectangle(-210, -160, 420, 330)
    cr.fill()
    cr.rectangle(-190, -140, 380, 270)
    cr.clip()
    g = cairo.LinearGradient(0, -140, 0, 130)
    g.add_color_stop_rgba(0, 0.72, 0.8, 0.88, 1)
    g.add_color_stop_rgba(1, 0.86, 0.84, 0.78, 1)
    cr.set_source(g)
    cr.paint()
    cr.set_source_rgba(0.55, 0.58, 0.6, 1)                    # a building and the bus stop
    cr.rectangle(70, -140, 120, 270)
    cr.fill()
    cr.set_source_rgba(0.2, 0.45, 0.35, 1)
    cr.rectangle(-170, -110, 10, 230)
    cr.fill()
    toon(cr, lambda c: c.arc(-165, -110, 26, 0, 2 * math.pi), hexa("#2f7a5a"), None, (0, 0), None, lw=3)
    hud2d._text(cr, "BUS", -165, -102, 18, (1, 1, 1, 1), "Liberation Sans", "center")
    tk.you_bust(cr, -60, 180, 0.62, tk.FACES["calm"], t, look=(0.6, 0), coat=VEST, blink=False)
    cr.restore()
    cr.save()
    cr.translate(x, y)
    cr.rotate(rot)
    cr.scale(s, s)
    hud2d._text(cr, "TODAY 07:42", 182, 118, 30, (1, 0.55, 0.15, 1), "Liberation Mono", "right", outline=INK, ow=3)
    cr.restore()


# ------------------------------------------------------------------ the film
def shots(tl):
    A, B = tl.at, tl.by_id
    return [
        (0.0, "glass"), (B["k2"].start - 0.2, "desk"), (B["k3"].start - 0.2, "vault"), (B["k4"].start - 0.2, "alarm"),
        (B["k5"].start - 0.2, "lobby"), (A("k5", "They", nth=2) - 0.15, "boxes"), (B["k6"].start - 0.2, "box"),
        (B["k7"].start - 0.2, "keys"), (B["k8"].start - 0.2, "glass2"), (B["k9"].start - 0.2, "face"),
        (B["k10"].start - 0.2, "vault_open"), (B["k11"].start - 0.2, "photo"), (B["k12"].start - 0.2, "alarm2"),
        (B["k13"].start - 0.2, "glass3"), (B["k14"].start - 0.2, "reveal"), (B["k17"].start - 0.2, "alarm3"),
        (B["k18"].start - 0.2, "split"), (tl.total + 1, "end")]


_shots = {}


def draw(cr, t, tl):
    A, B = tl.at, tl.by_id
    if id(tl) not in _shots:
        _shots[id(tl)] = shots(tl)
    sh = _shots[id(tl)]
    k = max(i for i, (at, _) in enumerate(sh) if at <= t or i == 0)
    s0, name, s1 = sh[k][0], sh[k][1], sh[k + 1][0]
    t_open = A("k10", "clicks") - 0.05
    t_lift0, t_lift1 = A("k14", "pulls") - 0.1, B["k14"].end + 0.9
    t_touch = A("k12", "touches") - 0.1
    grade_n = ((0.8, 0.95, 0.95), (0.42, 0.5, 0.55))

    def behind_glass(face_fn, fog=0.0):
        hud2d.blurred(cr, lambda c: lobby(c, t, crew=0.0), sigma=9)
        face_fn()
        teller_glass(cr, t, fog=fog)
        counter(cr, t)

    cr.save()
    if name in ("glass", "glass2", "glass3"):
        camera(cr, t, s0, s1, 1.02, 1.1, cy=700)
        lean = 1.0 if name != "glass" else 0.85 + 0.15 * seg(t, 0, 1.2)
        fog = 0.5 + 0.5 * math.sin(t * 1.8) if name != "glass3" else 0.8
        behind_glass(lambda: danny(cr, 360, 980, 1.38 * lean + 0.06, t, mask=1.0, look=(0, 0.1)), fog=fog)
        grade(cr, *grade_n)
    elif name == "desk":
        camera(cr, t, s0, s1, 1.0, 1.06, cy=800)
        hud2d.blurred(cr, lambda c: lobby(c, t, crew=0.5), sigma=7)
        teller_glass(cr, t)
        counter(cr, t)
        cr.save()                                              # the framed photo on your desk: you and your brother
        cr.translate(560, 980)
        cr.rotate(0.06)
        toon(cr, lambda c: c.rectangle(-90, -110, 180, 150), hexa("#5a3a24"), None, (0, 0), None, lw=4)
        cr.rectangle(-76, -96, 152, 122)
        cr.clip()
        cr.set_source_rgba(0.85, 0.75, 0.55, 1)
        cr.paint()
        tk.you_bust(cr, -32, 60, 0.3, tk.FACES["calm"], t, coat=VEST, blink=False)
        tk.you_bust(cr, 30, 60, 0.36, tk.FACES["calm"], t, coat=DANNY, blink=False)
        cr.restore()
        grade(cr, *grade_n)
    elif name in ("vault", "vault_open"):
        camera(cr, t, s0, s1, 1.0, 1.08, cy=620)
        vault_door(cr, t, open_k=seg(t, t_open, t_open + 1.4) if name == "vault_open" else 0.0)
        grade(cr, *grade_n)
    elif name in ("alarm", "alarm2", "alarm3"):
        camera(cr, t, s0, s1, 1.02, 1.12, cy=900, shake=1.0 + (name != "alarm"))
        gap = {"alarm": 1.0, "alarm2": 1 - seg(t, t_touch, t_touch + 0.6), "alarm3": 0.0}[name]
        alarm_desk(cr, t, gap=gap, press=0.15 if name == "alarm3" else 0.0)
        grade(cr, (0.85, 0.85, 0.9), (0.45, 0.45, 0.5))
    elif name == "lobby":
        camera(cr, t, s0, s1, 1.0, 1.06, cy=700)
        lobby(cr, t, crew=seg(t, s0, s0 + 1.2))
        grade(cr, *grade_n)
    elif name == "boxes":
        camera(cr, t, s0, s1, 1.0, 1.3, cx=510, cy=690)        # push in on 41
        cr.set_source_rgba(0.12, 0.13, 0.15, 1)
        cr.paint()
        box_grid(cr, t, 60, 40, 600, 800, hi=41)
        grade(cr, *grade_n)
    elif name == "box":
        camera(cr, t, s0, s1, 1.0, 1.1, cy=640)
        box_closeup(cr, t)
        grade(cr, (0.95, 0.95, 0.95), (0.55, 0.55, 0.6))
    elif name == "keys":
        camera(cr, t, s0, s1, 1.0, 1.08, cy=760)
        hud2d.blurred(cr, lambda c: (lobby(c, t), danny(c, 360, 980, 1.4, t)), sigma=10)
        teller_glass(cr, t)
        scar_hand(cr, 300, 430, 1.35, t)                       # his hand, the scar, the key, behind the glass
        counter(cr, t, hands=False, tray=seg(t, A("k7", "other") - 0.2, B["k7"].end), keys=True)
        keyring(cr, 470, 700, 1.25)                             # and yours, up close
        grade(cr, *grade_n)
    elif name == "face":
        camera(cr, t, s0, s1, 1.04, 1.12)
        hud2d.blurred(cr, lambda c: (lobby(c, t), teller_glass(c, t)), sigma=8)
        f = tk.face_mix("alarmed", "terror", seg(t, A("k9", "Only") - 0.1, A("k9", "Only") + 0.4))
        you(cr, 360, 930, 1.42, t, f, look=(0, -0.1), sweat=0.7)
        grade(cr, *grade_n)
    elif name == "photo":
        camera(cr, t, s0, s1, 1.0, 1.08, cy=640)
        hud2d.blurred(cr, lambda c: (lobby(c, t), danny(c, 360, 980, 1.4, t)), sigma=10)
        photo_card(cr, 360, 600, 1.35, t)
        scar_hand(cr, 40, 880, 0.8, t, holding=None)          # holding the photo by its corner, clear of your face
        teller_glass(cr, t)
        counter(cr, t, hands=False)
        grade(cr, *grade_n)
    elif name == "reveal":
        camera(cr, t, s0, s1, 1.04, 1.12, cy=700, shake=0.6)
        lift = seg(t, t_lift0, t_lift1)
        f = tk.face_mix("calm", "uneasy", 0.5)
        behind_glass(lambda: danny(cr, 360, 980, 1.44, t, mask=1 - lift, face=f, look=(0, 0.05)), fog=0.3)
        flash_k = seg(t, B["k15"].start + 1.3, B["k15"].start + 1.5) * (1 - seg(t, B["k15"].end, B["k15"].end + 0.2))
        if flash_k > 0:                                        # the plants, flashed back in two small insets
            for (ix, iy), draw_in in (((140, 250), lambda c: scar_hand(c, 160, 270, 0.62, t)),
                                      ((580, 250), lambda c: keyring(c, 560, 230, 0.75))):
                cr.save()
                cr.arc(ix, iy, 100, 0, 2 * math.pi)
                cr.set_source_rgba(0.04, 0.05, 0.06, 0.92 * flash_k)
                cr.fill_preserve()
                cr.clip()
                cr.push_group()
                draw_in(cr)
                cr.pop_group_to_source()
                cr.paint_with_alpha(flash_k)
                cr.restore()
                cr.set_source_rgba(*hud2d.YELLOW[:3], flash_k)
                cr.set_line_width(5)
                cr.arc(ix, iy, 100, 0, 2 * math.pi)
                cr.stroke()
        grade(cr, *grade_n)
    elif name == "split":
        camera(cr, t, s0, s1, 1.0, 1.03, shake=0.5)
        cr.save()
        cr.rectangle(0, 0, W, H / 2)
        cr.clip()
        cr.translate(0, -340)
        behind_glass(lambda: danny(cr, 360, 980, 1.44, t, mask=0.0, face=tk.face_mix("calm", "uneasy", 0.5)))
        cr.restore()
        cr.save()
        cr.rectangle(0, H / 2, W, H / 2)
        cr.clip()
        cr.translate(0, 120)
        alarm_desk(cr, t, gap=0.0, press=0.15)
        cr.restore()
        cr.set_source_rgba(0.85, 0.95, 0.95, 0.9)
        cr.rectangle(0, H / 2 - 3, W, 6)
        cr.fill()
        grade(cr, *grade_n)
    cr.restore()
    hud.finish(cr, t, flash_at=[], vig=0.55, grain=0.06)
    if t < t_open:
        vault = ("VAULT", "LOCKED", None) if t < B["k3"].start else ("VAULT", "OPENS 2:10", "warn", B["k3"].start)
    else:
        left = max(0.0, 360 - (t - t_open) * (360 - 271) / max(1.0, tl.total - t_open))   # 6:00 down to ~4:31
        vault = ("VAULT SEALS", f"{int(left // 60)}:{int(left % 60):02d}", "bad", t_open)
    clock_v = ("TIME", "2:10 AM", None, t_open) if t >= t_open else ("TIME", "2:00 AM", None)
    alarm = (("ALARM", "TOUCHING", "bad", t_touch) if t >= t_touch else
             ("ALARM", "1 INCH", "warn", B["k4"].start) if t >= B["k4"].start else ("ALARM", "ARMED", None))
    hud2d.stats(cr, t, [clock_v, vault, alarm])
    hud2d.hook(cr, t, [("HE KNOWS", False), ("YOUR NAME", True)], end=B["k1"].end + 0.15, y=270, size=96)
    hud2d.rule_tag(cr, t, A("k3", "six"), B["k3"].end + 0.3, "TIME LOCK: 6 MINUTES", y=190)
    hud2d.stamp(cr, t, A("k6", "name.", end=True) - 0.1, B["k6"].end + 0.3, ["BOX 41:", "YOURS?"], y=280)
    hud2d.bubble(cr, t, B["k8"].start, B["k8"].end, "Easy, kiddo. Nobody gets hurt tonight.", 360, 250, (380, 470))
    hud2d.bubble(cr, t, B["k13"].start, B["k13"].end, "Don't. Please. Not after five years.", 360, 250, (380, 470))
    hud2d.ab_card(cr, t, A("k19", "help"), "HELP DANNY", "PRESS IT", kicker="TIME LOCK · PART 1 · YOUR CHOICE",
                  decides="Part 2")
    hud2d.captions(cr, t, tl, KEY, skip=("k8", "k13"))
    cue("hum", t, 0.0, tl.total)                                # the bank's night air from the first frame
    cue("click", t, B["k10"].start - 0.3)                        # the time lock trips before the line
    cue("doors", t, B["k10"].end + 0.05)                         # the vault door, after the words
    cue("heartbeat", t, B["k12"].start, B["k17"].end - B["k12"].start)
    cue("riser", t, B["k18"].start, B["k19"].start - B["k18"].start)
