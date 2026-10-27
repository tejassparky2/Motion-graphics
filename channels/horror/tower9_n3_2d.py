"""Tower 9, Night 3, in the illustrated 2D style. Original story; Night 2's vote was the hatch (owner, 27 Oct 2026: "All
said hatch"), and the owner approved the script ("Approved, make it"): out/horror/scripts_night3_tower9.md.

You open the hatch at 4:43 and your own hand reaches up: the other you, soaked and blue with cold. You bolt it at
4:44; the copy at the window stops smiling and is gone; every torch in the trees goes out (rule 3 worked). The test
(page one of the logbook) passes, and the narrator says "So it's you"; then the black window shows one reflection,
yours. It tells you not to answer the radio at five; at five, base calls and asks you to open the hatch. The vote:
answer the radio, or stay. Clues on screen, never spoken: its watch runs backwards (like the wall clock in Night 2),
and frost spreads on the floor where it sits.

    /home/user/.venv-main/bin/python channels/horror/make_2d.py tower9_n3_2d   -> out/horror/tower9_n3_2d.mp4
"""
import math

from motion import audio, voice
from motion.engine import W, H, cairo, clamp01, cue, seg
from motion.polish import text_width

from channels.horror import hud, hud2d, sound  # noqa: F401  (sound registers the horror effects)
from channels.horror import toon2d as tk
from channels.horror import tower9_2d as n1      # Night 1's sets: cabin, hatch, logbook, radio, trees, clock
from channels.horror import tower9_n2_2d as n2   # Night 2's window, the copy at the glass, the phone light
from channels.horror.toon2d import INK, glow, grade, hexa, mix, noise, toon

NARRATOR = dict(turbo=True)
TAIL = 2.0                     # the vote card stays up ~2 s (reference study, 27 Oct)
MUSIC = "horror"
TWIST = "n12"                  # the bed drops out under the reflection
voice.SPEAKERS["other"] = dict(voice="am_michael", turbo_ref="am_michael", fx="volume=1.0")   # 1.3 clipped the shout
voice.SPEAKERS["other_w"] = dict(voice="am_michael", turbo_ref="am_michael", fx="volume=2.0")
audio.GAINS.update(rain=0.15, static=0.4, slam=0.45, lock=0.45)

SCRIPT = [
    dict(id="n1", scene="open", text="Nearly all of you said hatch. So you open it, and your own hand reaches up."),
    dict(id="n2", scene="grip", text="Orange sleeve. Your watch. Then your face."),
    dict(id="n3", scene="other", text="It's you. Soaked. Shaking. Lips blue."),
    dict(id="n4", scene="other", text="Shut it! Before [four forty-four.|4:44.]", speaker="other", gap=0.3),
    dict(id="n5", scene="bolt", text="You slam the bolt. [Four forty-four.|4:44.]", gap=0.3),
    dict(id="n6", scene="window", text="At the window, your face stops smiling. Then it's gone."),
    dict(id="n7", scene="trees", text="Down in the trees, every torch goes out."),
    dict(id="n8", scene="you", text="So you test it. What did you write on page one of the logbook?", gap=0.5),
    dict(id="n9", scene="other", text="Day one. I hate heights.", speaker="other", gap=0.3),
    dict(id="n10", scene="both", text="Nobody's seen that page but you. So it's you.", gap=0.3),
    dict(id="n11", scene="glass", text="Then your phone lights up the black window."),
    dict(id="n12", scene="reflection", text="In the glass, there's your reflection. Beside it, nothing.", gap=0.5),
    dict(id="n13", scene="other", text="[whispering] Don't look at the glass. And at five, don't answer the radio.",
         speaker="other_w", gap=0.9),
    dict(id="n14", scene="radio", text="At five, the radio crackles."),
    dict(id="n15", scene="radio", text="Tower [nine,|9,] this is base. That thing isn't you. Open the hatch and come "
                                       "down.", speaker="base", gap=0.7),   # static fills this gap
    dict(id="n16", scene="rules", text="Answer it, and you break two rules for a voice calling after three."),
    dict(id="n17", scene="other", text="Stay, and you trust the one with no reflection."),
    dict(id="n18", scene="split", text="Whatever most of you choose happens on Night [four.|4.]"),
    dict(id="n19", scene="split", text="So, do you answer the radio? Or stay?", gap=0.3),
]

METADATA = dict(
    title="You Opened the Hatch. Your Own Hand Reached Up. 🚪",
    alt_titles=["Never Open the Hatch: Night 3 🚪", "Two of You in the Tower. Only One Reflection. 🚪"],
    description="""4:43 AM. Nearly all of you said hatch... so you open it, and your own hand reaches up. 🚪

Tower 9, Night 3. Rule 3 said let one in before 4:44. You did. Then the radio calls at five.
An interactive horror story: YOU decide what happens next.
💬 Answer the radio, or stay? Comment A or B. Most comments decide Night 4. 👇

(Fiction. 2D animation.)""",
    hashtags=["#HorrorStory", "#InteractiveStory", "#Shorts"],
    tags=["horror story", "interactive story", "you decide", "choose your ending", "fire tower", "forest horror",
          "scary story", "2d animation", "doppelganger", "night 3", "creepy"],
    pinned_comment="Stay. Base just asked you to break TWO rules, and since when does base call after three? "
                   "Radio or stay? 👇 (Look at its watch 👀)",
)

KEY = {"hatch", "hand", "watch", "face", "soaked", "slam", "smiling", "gone", "torch", "test", "page", "nobody's",
       "window", "reflection", "nothing", "radio", "five", "break", "rules", "three", "stay", "four"}
PHONE = n2.PHONE
COLD = (0.62, 0.78, 1.0)
OTHER_SKIN = mix(tk.SKIN, (0.66, 0.76, 0.9, 1), 0.4)       # the other you: blue with cold
WET_RANGER = (mix(tk.RANGER[0], (0.1, 0.1, 0.14, 1), 0.16), mix(tk.RANGER[1], (0.05, 0.05, 0.08, 1), 0.16),
              mix(tk.RANGER[2], (0.2, 0.2, 0.25, 1), 0.16))   # still orange, darkened by the wet
PHONE_SKIN = n2.PHONE_SKIN
HX0, HY0, HX1, HY1 = 170, 380, 550, 760                     # the hatch opening (as in Night 1)


def camera(cr, t, s0, s1, z0=1.0, z1=1.06, cx=W / 2, cy=H / 2, shake=1.0):
    k = seg(t, s0, s1)
    z = z0 + (z1 - z0) * k
    cr.translate(cx + 4 * shake * noise(t * 0.7, 1), cy + 3 * shake * noise(t * 0.6, 4))
    cr.rotate(0.004 * shake * noise(t * 0.5, 7))
    cr.scale(z, z)
    cr.translate(-cx, -cy)


# ------------------------------------------------------------------ the other you
def frost_hair(cr, x, y, s, t):
    """Ice crystals in its hair and on its shoulders."""
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    cr.set_source_rgba(0.9, 0.97, 1, 0.85)
    cr.set_line_width(2.2)
    for k in range(26):
        a = -math.pi * (0.1 + 0.8 * ((k * 0.618) % 1))
        r = 120 + 22 * ((k * 0.37) % 1)
        px, py = r * math.cos(a), -175 - 40 + r * math.sin(a) * 0.95
        if k >= 18:
            px, py = (-150 + (k - 18) * 40), 30 + 10 * math.sin(k)
        L = 6 + 5 * ((k * 0.7) % 1)
        for j in range(3):
            aa = j * math.pi / 3
            cr.move_to(px - L * math.cos(aa), py - L * math.sin(aa))
            cr.line_to(px + L * math.cos(aa), py + L * math.sin(aa))
        cr.stroke()
    cr.restore()


def drips(cr, x, y, s, t):
    """Water running off it."""
    for k in range(6):
        px = x + (-90 + 36 * k) * s
        ph = (t * 0.7 + k * 0.37) % 1
        py = y + (-120 + 260 * ph) * s
        cr.set_source_rgba(0.75, 0.88, 1, 0.75 * (1 - ph))
        cr.save()
        cr.translate(px, py)
        cr.scale(s, s)
        cr.move_to(0, -10)
        cr.curve_to(7, 0, 7, 8, 0, 9)
        cr.curve_to(-7, 8, -7, 0, 0, -10)
        cr.restore()
        cr.fill()


def other_bust(cr, x, y, s, t, face, look=(0.0, 0.0), turn=0.0, tremble=1.0, rim=(0.7, 0.85, 1, 0.6),
               rim_from=(0, -8)):
    """You, come up through the hatch: blue with cold, soaked, frost in its hair, shaking."""
    tk.you_bust(cr, x, y, s, face, t, look=look, turn=turn, skin=OTHER_SKIN, coat=WET_RANGER, rim=rim,
                rim_from=rim_from, sweat=1.0, tremble=tremble, breath=1.6)
    frost_hair(cr, x, y, s, t)
    drips(cr, x, y, s, t)


def watch(cr, x, y, r, t, backwards=True):
    """A wristwatch face; the second hand runs backwards (the clue, never spoken)."""
    toon(cr, lambda c: c.arc(x, y, r + 5, 0, 2 * math.pi), hexa("#2c2c30"), None, (0, 0), None, lw=3)
    toon(cr, lambda c: c.arc(x, y, r, 0, 2 * math.pi), hexa("#e9e4d6"), hexa("#c8c0aa"), (-3, -3), None, lw=2.5)
    sec = (-t if backwards else t) % 60
    for frac, ln, w, col in ((4.73 / 12, r * 0.5, 4, INK), (44.0 / 60, r * 0.75, 3, INK),
                             (sec / 60, r * 0.85, 1.6, (0.8, 0.1, 0.08, 1))):
        a = frac * 2 * math.pi
        cr.set_source_rgba(*col)
        cr.set_line_width(w)
        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        cr.move_to(x, y)
        cr.line_to(x + ln * math.sin(a), y - ln * math.cos(a))
        cr.stroke()


# ------------------------------------------------------------------ the hatch, open
def hatch_open(cr, t, hand=0.0, face=0.0, frost=1.0, rise=0.0, climber=0.0):
    """From above: the trapdoor thrown back, the shaft below full of cold light and the ladder going down; a hand in
    an orange sleeve grips the near edge (hand 0..1), then your own face rises into the light (face 0..1)."""
    n1.planks(cr, 0, 0, W, H, horizontal=False, seed=11, base=hexa("#6e4c31"), dark=hexa("#4a3120"), board=72)
    n1.planks(cr, HX0, HY0 - 360, HX1, HY0 - 6, horizontal=True, seed=13, base=hexa("#5d4029"),
              dark=hexa("#3e2a1a"), board=60)                  # the lid, thrown back flat
    cr.set_source_rgba(*INK)
    cr.set_line_width(5)
    cr.rectangle(HX0, HY0 - 360, HX1 - HX0, 354)
    cr.stroke()
    for yy in (HY0 - 290, HY0 - 76):
        toon(cr, lambda c, yy=yy: c.rectangle(HX0, yy - 14, HX1 - HX0, 28), hexa("#2c2d2f"), hexa("#1a1b1c"), (0, -4),
             None, lw=3)
    g = cairo.RadialGradient(360, 570, 20, 360, 570, 300)       # the shaft: cold light from far below
    g.add_color_stop_rgb(0, 0.42, 0.55, 0.7)
    g.add_color_stop_rgb(1, 0.03, 0.05, 0.08)
    cr.set_source(g)
    cr.rectangle(HX0, HY0, HX1 - HX0, HY1 - HY0)
    cr.fill()
    cr.save()
    cr.rectangle(HX0, HY0, HX1 - HX0, HY1 - HY0)
    cr.clip()
    cr.set_source_rgba(0.08, 0.08, 0.1, 0.9)                    # the ladder, falling away
    for sx in (-1, 1):
        cr.set_line_width(14)
        cr.move_to(360 + sx * 130, HY1 + 20)
        cr.line_to(360 + sx * 40, 570)
        cr.stroke()
    for k in range(7):
        u = k / 7
        yy = HY1 - (HY1 - 570) * (1 - (1 - u) ** 2)
        hw = 130 - 90 * (1 - (1 - u) ** 2)
        cr.set_line_width(10 - 6 * u)
        cr.move_to(360 - hw, yy)
        cr.line_to(360 + hw, yy)
        cr.stroke()
    if climber > 0 and face <= 0:                               # far down the ladder, already climbing: a shape
        sc = 0.18 + 0.2 * climber
        cy = 600 + 120 * climber
        cr.set_source_rgba(0.02, 0.03, 0.05, 0.95)
        cr.save()
        cr.translate(372, cy)
        cr.scale(sc, sc)
        cr.arc(0, -150, 95, 0, 2 * math.pi)
        cr.fill()
        tk.curve(cr, [(-60, -70), (-190, -20), (-210, 140), (210, 140), (190, -20), (60, -70)])
        cr.fill()
        cr.set_source_rgba(0.6, 0.75, 1, 0.5)
        cr.set_line_width(10)
        cr.arc(0, -150, 95, math.pi * 1.1, math.pi * 1.9)
        cr.stroke()
        cr.restore()
    if face > 0:                                                # your face, rising out of the light
        sc = 0.55 + 0.45 * face
        other_bust(cr, 400, 1010 - 330 * face + 40 * rise, sc * 1.05, t, tk.face_mix("uneasy", "terror", 0.6),
                   look=(0, -0.7), rim=(0.75, 0.88, 1, 0.8), rim_from=(0, 10))
    glow(cr, 360, 570, 260, COLD, 0.35)
    cr.restore()
    cr.set_source_rgba(*INK)
    cr.set_line_width(6)
    cr.rectangle(HX0, HY0, HX1 - HX0, HY1 - HY0)
    cr.stroke()
    if frost > 0:                                               # frost creeping across the boards from the edge
        cr.set_source_rgba(0.85, 0.95, 1, 0.8 * frost)
        cr.set_line_width(2.2)
        for k in range(60):
            side = k % 4
            u = (k * 0.618) % 1
            sx, sy = [(HX0 + u * (HX1 - HX0), HY0), (HX1, HY0 + u * (HY1 - HY0)), (HX0 + u * (HX1 - HX0), HY1),
                      (HX0, HY0 + u * (HY1 - HY0))][side]
            nx, ny = [(0, -1), (1, 0), (0, 1), (-1, 0)][side]
            if side == 0:
                continue
            L = (24 + 80 * ((k * 0.37) % 1)) * frost
            ex, ey = sx + nx * L + ny * L * 0.3, sy + ny * L + nx * L * 0.3
            cr.move_to(sx, sy)
            cr.line_to(ex, ey)
            for sgn in (-1, 1):
                mx, my = sx + (ex - sx) * 0.5, sy + (ey - sy) * 0.5
                cr.move_to(mx, my)
                cr.line_to(mx + (nx + sgn * ny) * L * 0.3, my + (ny + sgn * nx) * L * 0.3)
            cr.stroke()
    if hand > 0:                                                # the hand on the left edge: orange sleeve, watch
        cr.save()
        cr.translate(HX0 - 6 + 40 * (1 - hand), 640)
        cr.rotate(math.pi / 2)                                  # fingers over the rim onto the boards, arm in the shaft
        toon(cr, lambda c: tk.curve(c, [(-46, -120), (-40, -10), (50, -10), (56, -120)]), *tk.RANGER[:2], (-6, -5),
             None, lw=5)                                        # the sleeve, inside the shaft
        toon(cr, lambda c: tk.curve(c, [(-50, -14), (-56, 22), (-40, 52), (-16, 62), (8, 56), (30, 62), (52, 50),
                                        (58, 18), (52, -14)]), OTHER_SKIN, mix(OTHER_SKIN, (0, 0, 0, 1), 0.3),
             (-6, -5), None, lw=4)                              # fingers curled over the edge onto the boards
        cr.set_source_rgba(*INK[:3], 0.6)
        cr.set_line_width(2.5)
        for fx in (-30, -8, 14, 36):
            cr.move_to(fx, 20)
            cr.line_to(fx + 2, 52)
            cr.stroke()
        watch(cr, 4, -50, 26, t)
        cr.restore()


def floor_frost(cr, x, y, k):
    """Frost spreading over the boards around where it stands (the second clue)."""
    if k <= 0:
        return
    cr.set_source_rgba(0.88, 0.96, 1, 0.75)
    cr.set_line_width(2.4)
    for j in range(40):
        a = j * 2.399
        r = (40 + 260 * ((j * 0.37) % 1)) * k
        ex, ey = x + r * math.cos(a), y + r * math.sin(a) * 0.45
        cr.move_to(x + 0.3 * r * math.cos(a), y + 0.3 * r * math.sin(a) * 0.45)
        cr.line_to(ex, ey)
        cr.stroke()


def other_room(cr, t, face, look=(0.0, 0.0), frost_k=0.0, tremble=1.0, wipe=False):
    """The other you in the dark cabin, lit by your phone."""
    hud2d.blurred(cr, lambda c: (n1.cabin(c, t, on=0.0), grade(c, (0.3, 0.34, 0.46), (0.12, 0.13, 0.2))), sigma=8)
    other_bust(cr, 360, 960, 1.42, t, face, look=look, tremble=tremble)
    floor_frost(cr, 360, 1215, frost_k)
    glow(cr, 360, 1300, 520, PHONE, 0.3)
    n2.phone_dark(cr, 360, 1100, 1000, 0.7)


def you_room(cr, t, face, look=(0.0, 0.0)):
    hud2d.blurred(cr, lambda c: (n1.cabin(c, t, on=0.0), grade(c, (0.3, 0.34, 0.46), (0.12, 0.13, 0.2))), sigma=8)
    tk.you_bust(cr, 360, 960, 1.42, face, t, look=look, coat=tk.RANGER, light=(0, 14), rim=(0.8, 0.9, 1, 0.7),
                rim_from=(0, 10), skin=PHONE_SKIN, sweat=0.5)
    glow(cr, 360, 1300, 520, PHONE, 0.35)
    n2.phone_dark(cr, 360, 1100, 1000, 0.75)


def both(cr, t):
    """Face to face in the dark: you on the left, it on the right."""
    hud2d.blurred(cr, lambda c: (n1.cabin(c, t, on=0.0), grade(c, (0.3, 0.34, 0.46), (0.12, 0.13, 0.2))), sigma=8)
    tk.you_bust(cr, 190, 900, 1.0, tk.FACES["uneasy"], t, look=(0.8, 0), turn=0.6, coat=tk.RANGER, light=(0, 14),
                rim=(0.8, 0.9, 1, 0.7), rim_from=(0, 10), skin=PHONE_SKIN)
    other_bust(cr, 540, 900, 1.0, t, tk.FACES["calm"], look=(-0.8, 0), turn=-0.6, tremble=0.6)
    glow(cr, 360, 1250, 520, PHONE, 0.3)
    n2.phone_dark(cr, 360, 1150, 1000, 0.6)


def reflection(cr, t, k=1.0):
    """Over both your shoulders at the black window: in the glass, your reflection. Beside it, nothing."""
    def fig(c):
        c.push_group()
        tk.you_bust(c, 230, 860, 0.95, tk.FACES["alarmed"], t, look=(0, 0.1), coat=tk.RANGER, light=(0, 14),
                    skin=PHONE_SKIN, rim=(0.8, 0.9, 1, 0.5), rim_from=(0, 10))
        c.pop_group_to_source()
        c.paint_with_alpha(0.55 * k)
        glow(c, 230, 820, 160, PHONE, 0.25 * k)
    n2.window_scene(cr, t, fig, dark=0.25)
    tk.you_back(cr, 230, 1180, 1.05, t, coat=tk.RANGER, rim=(0.8, 0.9, 1, 0.5), rim_from=(0, -8))
    tk.you_back(cr, 500, 1190, 1.05, t, coat=WET_RANGER, rim=(0.7, 0.85, 1, 0.5), rim_from=(0, -8))
    frost_hair(cr, 500, 1190 + 30, 1.05, t)
    glow(cr, 250, 1280, 320, PHONE, 0.3)


def page_one(cr, t, k=1.0):
    """The logbook's first page, in your handwriting: Day 1. I hate heights."""
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
    ink = (0.12, 0.14, 0.3, 1)
    hud2d._text(cr, "TOWER 9  ·  LOG", -260, -310, 34, ink, "Kalam")
    for j, (ln, sz) in enumerate((("Day 1.", 64), ("I hate heights.", 64))):
        n = int(len(ln) * clamp01(k * 2 - j))
        if n:
            hud2d._text(cr, ln[:n], -250, -180 + j * 100, sz, ink, "Kalam")
    cr.restore()
    glow(cr, 380, 620, 420, PHONE, 0.2)
    n2.phone_dark(cr, 380, 600, 900, 0.8)


def rules_page(cr, t, hot):
    """Night 1's two rules on the logbook page, circled in red as the line names them."""
    n1.logbook(cr, t, 1.0, 1.0)
    grade(cr, (0.62, 0.68, 0.85), (0.32, 0.35, 0.46))
    n2.phone_dark(cr, 380, 600, 900, 0.75)
    for j in range(2):
        p = clamp01(hot * 2 - j)
        if p <= 0:
            continue
        cr.save()
        cr.translate(360 + 0.9 * 110, 560 + 0.9 * (-90 + j * 130))
        cr.scale(1.0, 0.42)
        cr.new_path()
        cr.arc(0, 0, 190, -math.pi / 2, -math.pi / 2 + 2 * math.pi * p)
        cr.restore()
        cr.set_source_rgba(*hud2d.RED[:3], 0.95)
        cr.set_line_width(8)
        cr.stroke()


# ------------------------------------------------------------------ the film
def shots(tl):
    A, B = tl.at, tl.by_id
    return [
        (0.0, "open"), (B["n2"].start - 0.15, "grip"), (A("n2", "Then") - 0.1, "rise"), (B["n3"].start - 0.15, "other"),
        (B["n5"].start - 0.15, "bolt"), (B["n6"].start - 0.15, "window"), (B["n7"].start - 0.15, "trees"),
        (B["n8"].start - 0.15, "you"), (B["n9"].start - 0.15, "other_answer"), (B["n10"].start - 0.15, "both"),
        (B["n11"].start - 0.15, "glass"), (B["n12"].start - 0.15, "reflection"), (B["n13"].start - 0.6, "other_w"),
        (B["n14"].start - 0.15, "radio"), (B["n16"].start - 0.15, "rules"), (B["n17"].start - 0.15, "other_stay"),
        (B["n18"].start - 0.15, "split"), (tl.total + 1, "end")]


_shots = {}


def draw(cr, t, tl):
    A, B = tl.at, tl.by_id
    if id(tl) not in _shots:
        _shots[id(tl)] = shots(tl)
    sh = _shots[id(tl)]
    k = max(i for i, (at, _) in enumerate(sh) if at <= t or i == 0)
    s0, name, s1 = sh[k][0], sh[k][1], sh[k + 1][0]
    t_hand = A("n1", "hand") - 0.3
    t_slam = A("n5", "bolt.", end=True) + 0.03             # after the words, never on them
    t_five = B["n14"].start

    cr.save()
    if name in ("open", "grip", "rise"):
        z = {"open": (1.14, 1.24), "grip": (1.9, 2.05), "rise": (1.05, 1.15)}[name]
        cy = {"open": 600, "grip": 640, "rise": 640}[name]
        cx = HX0 + 60 if name == "grip" else 360
        camera(cr, t, s0, s1, z[0], z[1], cx=cx, cy=cy)
        face = seg(t, A("n2", "Then"), B["n2"].end + 0.3) if name == "rise" else 0.0
        hatch_open(cr, t, hand=seg(t, t_hand, t_hand + 0.35), face=face, climber=seg(t, 0.0, t_hand))
        grade(cr, (0.62, 0.7, 0.88), (0.3, 0.32, 0.42))
        glow(cr, 360, 1250, 600, PHONE, 0.15)
    elif name in ("other", "other_answer", "other_w", "other_stay"):
        camera(cr, t, s0, s1, 1.03, 1.12, cy=700, shake=1.2 if name == "other" else 0.7)
        if name == "other":
            f = tk.face_mix("terror", "alarmed", seg(t, B["n4"].start - 0.2, B["n4"].start + 0.2))
            other_room(cr, t, f, look=(0, -0.2))
        elif name == "other_answer":
            other_room(cr, t, tk.FACES["uneasy"], tremble=0.6)
        elif name == "other_w":
            other_room(cr, t, tk.FACES["calm"], look=(0.3, 0), tremble=0.3)
        else:
            other_room(cr, t, tk.FACES["calm"], look=(0, 0), tremble=0.2, frost_k=seg(t, s0, s1 + 1.0))
    elif name == "bolt":
        camera(cr, t, s0, s1, 1.0, 1.06, cy=600, shake=1.0 + 2.0 * max(0.0, 1 - (t - t_slam) / 0.3) * (t >= t_slam))
        n1.hatch(cr, t, light=0.2, frost=1.0, bumps=(t_slam,), dust=(t_slam,))
        grade(cr, (0.6, 0.66, 0.84), (0.3, 0.33, 0.43))
        n2.phone_dark(cr, 360, 1150, 1100, 0.6)
    elif name == "window":
        camera(cr, t, s0, s1, 1.02, 1.1, cy=560, shake=0.6)
        t_gone = A("n6", "gone.") - 0.2
        smile = 1 - seg(t, A("n6", "stops") - 0.1, A("n6", "smiling.", end=True))
        face = tk.face_mix("calm", "smile", smile)
        fig0 = n2.copy_close(t, face)

        def fig(c):
            c.push_group()
            fig0(c)
            c.pop_group_to_source()
            c.paint_with_alpha(1 - seg(t, t_gone, t_gone + 0.25))
        n2.window_scene(cr, t, fig, dark=0.35)
    elif name == "trees":
        camera(cr, t, s0, s1, 1.0, 1.06, cy=640)
        left = int(round(24 * (1 - seg(t, A("n7", "every") - 0.1, B["n7"].end + 0.2))))
        n1.trees_down(cr, t, left)
        grade(cr, (0.75, 0.8, 0.95), (0.4, 0.42, 0.5))
    elif name == "you":
        camera(cr, t, s0, s1, 1.03, 1.12, cy=700)
        you_room(cr, t, tk.face_mix("uneasy", "alarmed", 0.3), look=(0.3, 0))
    elif name == "both":
        camera(cr, t, s0, s1, 1.0, 1.06, cy=760)
        both(cr, t)
    elif name == "glass":
        camera(cr, t, s0, s1, 1.0, 1.06, cy=560)
        n2.window_scene(cr, t, None, dark=0.3)
        glow(cr, 300, 820, 160, PHONE, 0.45 * seg(t, s0, s0 + 0.6))   # the phone's glare on the glass
    elif name == "reflection":
        camera(cr, t, s0, s1, 1.0, 1.08, cy=760, shake=0.5)
        reflection(cr, t, seg(t, s0, s0 + 0.5))
    elif name == "radio":
        camera(cr, t, s0, s1, 1.02, 1.1, cy=700)
        rx = 1.0 if B["n14"].end - 0.1 <= t <= B["n15"].end + 0.2 else 0.0
        n1.radio_scene(cr, t, rx)
        grade(cr, (0.55, 0.62, 0.8), (0.28, 0.3, 0.4))
        n2.phone_dark(cr, 360, 900, 1000, 0.55)
    elif name == "rules":
        camera(cr, t, s0, s1, 1.0, 1.06, cy=560)
        rules_page(cr, t, seg(t, A("n16", "two"), A("n16", "rules") + 0.4))
    elif name == "split":
        camera(cr, t, s0, s1, 1.0, 1.03, shake=0.5)
        cr.save()
        cr.rectangle(0, 0, W, H / 2)
        cr.clip()
        cr.translate(0, -200)
        n1.radio_scene(cr, t, 0.4)
        grade(cr, (0.55, 0.62, 0.8), (0.28, 0.3, 0.4))
        cr.restore()
        cr.save()
        cr.rectangle(0, H / 2, W, H / 2)
        cr.clip()
        cr.translate(0, 330)
        other_room(cr, t, tk.FACES["calm"], tremble=0.2, frost_k=1.0)
        cr.restore()
        cr.set_source_rgba(0.85, 0.9, 1, 0.8)
        cr.rectangle(0, H / 2 - 3, W, 6)
        cr.fill()
    cr.restore()

    if name == "other_answer":                                    # the page it quoted, in a ring
        inset(cr, 140, 330, 110, lambda c: (c.translate(140, 330), c.scale(0.4, 0.4), c.translate(-360, -470),
                                            page_one(c, t, seg(t, B["n9"].start, B["n9"].end))), "PAGE ONE")
    elif name == "bolt":
        inset(cr, 560, 1000, 115, lambda c: (c.translate(560, 1000), c.scale(0.45, 0.45), c.translate(-360, -560),
                                             n1.clock(c, t, h=4, m=44, sec0=0)), "4:44")
    hud.finish(cr, t, flash_at=[], vig=0.6, grain=0.06)
    clock = ("TIME", "5:00 AM", "bad", t_five) if t >= t_five else \
        ("TIME", "4:44 AM", "bad", t_slam) if t >= t_slam else ("TIME", "4:43 AM", "warn")
    phone = ("PHONE", f"{round(5 - 2 * seg(t, 0, tl.total))}%", "warn")
    inside = ("IN THE TOWER", "2", "bad", t_hand + 0.3) if t >= t_hand + 0.3 else ("IN THE TOWER", "1", None)
    hud2d.stats(cr, t, [clock, phone, inside])
    rules_row(cr, t, tl)
    chip(cr, t, "TOWER 9 · NIGHT 3", 0.0, B["n2"].start)
    hud2d.hook(cr, t, [("YOU CHOSE", False), ("THE HATCH.", True)], end=B["n1"].end + 0.1, y=250, size=92)
    hud2d.bubble(cr, t, B["n4"].start, B["n4"].end, "Shut it! Before 4:44!", 360, 290, (360, 470))
    hud2d.stamp(cr, t, t_slam - 0.05, B["n5"].end + 0.3, ["RULE 3: DONE"], y=250, col=hud2d.GREEN)
    hud2d.bubble(cr, t, B["n9"].start, B["n9"].end, "Day one. I hate heights.", 450, 440, (390, 640), w=330)
    hud2d.stamp(cr, t, A("n12", "nothing.") - 0.05, B["n12"].end + 0.5, ["1 REFLECTION"], y=300)
    hud2d.bubble(cr, t, B["n13"].start, B["n13"].end, "Don't look at the glass. And at five, don't answer the "
                 "radio.", 360, 280, (360, 470), creepy=True)
    hud2d.bubble(cr, t, B["n15"].start, B["n15"].end, "Tower 9, this is base. That thing isn't you. Open the hatch "
                 "and come down.", 360, 290, (330, 560), w=480)
    hud2d.ab_card(cr, t, A("n19", "answer"), "ANSWER RADIO", "STAY", kicker="TOWER 9 · NIGHT 3 · YOUR CHOICE",
                  decides="Night 4")
    hud2d.captions(cr, t, tl, KEY, skip=("n4", "n9", "n13", "n15"))
    cue("rain", t, 0.0, tl.total)
    cue("lock", t, 0.05)                                          # the bolt drawn back, frame 0
    cue("slam", t, t_slam)
    cue("heartbeat", t, B["n11"].start, B["n17"].end - B["n11"].start)
    cue("static", t, B["n14"].end + 0.05, B["n15"].start - B["n14"].end - 0.1)
    cue("riser", t, B["n18"].start, B["n19"].start - B["n18"].start)


def inset(cr, x, y, r, draw, label=None):
    """A circular close-up with a gold ring."""
    cr.save()
    cr.arc(x, y, r, 0, 2 * math.pi)
    cr.clip()
    cr.save()
    draw(cr)
    cr.restore()
    cr.reset_clip()
    cr.arc(x, y, r, 0, 2 * math.pi)
    cr.set_source_rgba(*INK)
    cr.set_line_width(12)
    cr.stroke()
    cr.arc(x, y, r, 0, 2 * math.pi)
    cr.set_source_rgba(*hexa("#f2c14e")[:3], 1)
    cr.set_line_width(7)
    cr.stroke()
    if label:
        w = text_width(cr, label, 24, hud2d.ROUND) + 28
        tk.tk_rrect(cr, x - w / 2, y + r - 20, w, 40, 20)
        cr.set_source_rgba(*hexa("#f2c14e")[:3], 1)
        cr.fill()
        hud2d._text(cr, label, x, y + r + 9, 24, (0.08, 0.06, 0.04, 1), hud2d.ROUND, "center")
    cr.restore()


def chip(cr, t, text, start, end):
    """The series chip under the stats bar (first seconds)."""
    if t < start or t > end + 0.2:
        return
    a = 1 - clamp01((t - end) / 0.2)
    w = text_width(cr, text, 24, hud2d.ROUND) + 36
    cr.save()
    cr.push_group()
    tk.tk_rrect(cr, W / 2 - w / 2, 120, w, 44, 22)
    cr.set_source_rgba(0.04, 0.04, 0.06, 0.85)
    cr.fill_preserve()
    cr.set_source_rgba(*hud2d.YELLOW)
    cr.set_line_width(2.5)
    cr.stroke()
    hud2d._text(cr, text, W / 2, 150, 24, hud2d.YELLOW, hud2d.ROUND, "center")
    cr.pop_group_to_source()
    cr.paint_with_alpha(a)
    cr.restore()


def rules_row(cr, t, tl):
    """The three rules as chips under the stats bar from the second line; the ones in play turn red."""
    A, B = tl.at, tl.by_id
    if t < B["n2"].start or t >= A("n19", "answer"):
        return
    rules = [("#1 NO RADIO AFTER 3", ("n14", "n15", "n16")), ("#2 NEVER OPEN HATCH", ("n15", "n16")),
             ("#3 ONE IN BY 4:44", ("n4", "n5"))]
    x = 16
    for text, hot_ids in rules:
        hot = any(B[i].start - 0.1 <= t <= B[i].end + 0.3 for i in hot_ids)
        size = 18
        w = text_width(cr, text, size, hud2d.ROUND) + 22
        tk.tk_rrect(cr, x, 116, w, 36, 18)
        cr.set_source_rgba(*(hud2d.RED[:3] if hot else (0.04, 0.04, 0.06)), 0.9)
        cr.fill_preserve()
        cr.set_source_rgba(1, 1, 1, 0.5)
        cr.set_line_width(2)
        cr.stroke()
        hud2d._text(cr, text, x + w / 2, 140, size, (1, 1, 1, 1), hud2d.ROUND, "center")
        x += w + 8
