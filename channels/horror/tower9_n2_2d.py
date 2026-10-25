"""Tower 9, Night 2, in the illustrated 2D style. Original story; the owner approved the script on 25 Oct 2026
("Approved, make it") after Night 1's vote: most commented B, keep the hatch shut.

The generator dies at 4:14; something taps on the window 30 m up; in the lightning it wears your orange jacket and your
face (Night 1's hidden detail paid off); your voice under the hatch says not to let it in; rule 3 in the logbook says
let one in before 4:44 or both come in. The vote: window or hatch. Rewatch detail: the wall clock runs backwards in
the window shots, and the copy never blinks.

    /home/user/.venv-main/bin/python channels/horror/make_2d.py tower9_n2_2d   -> out/horror/tower9_n2_2d.mp4
"""
import math

from motion import audio, voice
from motion.engine import W, H, cairo, clamp01, cue, seg

from channels.horror import hud, hud2d, sound  # noqa: F401  (sound registers the horror effects)
from channels.horror import toon2d as tk
from channels.horror import tower9_2d as n1   # Night 1's sets: cabin, hatch, logbook, clock, tower
from channels.horror.toon2d import INK, glow, grade, hexa, mix, noise, poly, toon

NARRATOR = dict(turbo=True)
TAIL = 0.5
MUSIC = "horror"
voice.SPEAKERS["hatch_w"] = dict(voice="am_michael", turbo_ref="am_michael", fx="lowpass=f=3000,volume=2.0")
audio.GAINS.update(generator=0.2, glass_tap=0.8)

SCRIPT = [
    dict(id="n1", scene="face", text="At [four fourteen,|4:14,] the lights die. And the knocking under your feet stops."),
    dict(id="n2", scene="recap", text="You're alone in fire tower [nine.|9.] An hour ago, something with your voice "
                                      "begged you to open the hatch."),
    dict(id="n3", scene="vote", text="Most of you said keep it shut. So you did."),
    dict(id="n4", scene="window", text="Then something taps on the window. Thirty metres up."),
    dict(id="n5", scene="window", text="Lightning. Someone is standing on the walkway outside. In an orange ranger "
                                       "jacket, just like yours.", gap=1.2),   # the taps land in this silence
    dict(id="n6", scene="copy", text="It has your face."),
    dict(id="n7", scene="copy", text="It smiles, and puts a finger to its lips."),
    dict(id="n8", scene="hatch", text="Under your feet, your own voice whispers.", gap=1.4),   # thunder rolls out first
    dict(id="n9", scene="hatch", text="[whispering] Don't let it in. It's been wearing your face all night.",
         speaker="hatch_w", gap=0.35),
    dict(id="n10", scene="logbook", text="In the light of your phone, the logbook shows a third rule. On a page you "
                                         "never turned.", gap=0.35),   # "By your phone's light" was heard as "phone flight"
    dict(id="n11", scene="logbook", text="If two of them come, let one in before [four forty-four.|4:44.] Or they "
                                         "both come in."),
    dict(id="n12", scene="clock", text="The clock says [four forty.|4:40.]"),
    dict(id="n13", scene="fog", text="On the window, a finger writes in the fog. It's under you. Let me in."),
    dict(id="n14", scene="copy", text="Let the window in, and you're face to face with yourself."),
    dict(id="n15", scene="hatch", text="Let the hatch in, and you meet the voice that's been crying all night."),
    dict(id="n16", scene="split", text="Whatever most of you choose happens on Night [three.|3.]"),
    dict(id="n17", scene="split", text="So who do you let in? The one at the window with your face? Or the voice "
                                       "under the hatch that sounds like you?", gap=0.3),
]

METADATA = dict(
    title="You Kept the Hatch Shut. Now Something Is at the Window. 🪟",
    alt_titles=["Two of Them Want In. You Can Only Pick One. (Night 2) 🪟", "Never Open the Hatch: Night 2 🪟"],
    description="""4:14 AM. The generator dies, and the knocking under your feet stops. You kept the hatch shut... and now something is tapping on the window, 30 metres up. 🪟

Tower 9, Night 2. Most of you voted B (keep it shut), so that's what happened.
An interactive horror story: YOU decide what happens next.
💬 Who do you let in: the window or the hatch? The most comments decide Night 3. 👇

(Fiction. 2D animation.)""",
    hashtags=["#HorrorStory", "#InteractiveStory", "#Shorts"],
    tags=["horror story", "interactive story", "you decide", "choose your ending", "fire tower", "forest horror",
          "scary story", "2d animation", "creepy", "night 2", "doppelganger"],
    pinned_comment="Window 🪟 or hatch 🚪? Most comments decide Night 3. (Watch the clock on the wall 👀)",
)

KEY = {"die", "stops", "alone", "hatch", "taps", "window", "lightning", "jacket", "yours", "face", "smiles", "lips",
       "whispers", "third", "never", "both", "fog", "under", "yourself", "crying", "who"}
PHONE = (0.78, 0.88, 1.0)                                   # the phone's cold white light
COPY_SKIN = mix(tk.SKIN, (0.72, 0.78, 0.86, 1), 0.5)       # the thing at the window: your face, drained
PHONE_SKIN = mix(tk.SKIN, (0.72, 0.82, 1.0, 1), 0.22)


def camera(cr, t, s0, s1, z0=1.0, z1=1.06, cx=W / 2, cy=H / 2, shake=1.0):
    k = seg(t, s0, s1)
    z = z0 + (z1 - z0) * k
    cr.translate(cx + 4 * shake * noise(t * 0.7, 1), cy + 3 * shake * noise(t * 0.6, 4))
    cr.rotate(0.004 * shake * noise(t * 0.5, 7))
    cr.scale(z, z)
    cr.translate(-cx, -cy)


def phone_dark(cr, x=360, y=1180, r=900, a=1.0):
    """Everything outside the phone's beam sinks into the dark."""
    g = cairo.RadialGradient(x, y, 60, x, y, r)
    g.add_color_stop_rgba(0, 0, 0, 0, 0)
    g.add_color_stop_rgba(0.55, 0, 0, 0, 0.35 * a)
    g.add_color_stop_rgba(1, 0, 0, 0, 0.88 * a)
    cr.set_source(g)
    cr.paint()


# ------------------------------------------------------------------ the window and the thing outside it
WX0, WY0, WX1, WY1 = 60, 170, 660, 990


def walkway(cr):
    """The catwalk railing outside the window."""
    for y, w in ((800, 12), (880, 10)):
        cr.set_source_rgba(0.12, 0.13, 0.15, 1)
        cr.rectangle(WX0, y, WX1 - WX0, w)
        cr.fill()
    for x in range(WX0 + 40, WX1, 160):
        cr.rectangle(x, 800, 12, WY1 - 800)
        cr.fill()


def copy_far(t, flash):
    """Standing at the railing, face lost in shadow until you're closer."""
    def fig(c):
        tk.you_bust(c, 360, 830, 0.85, tk.FACES["calm"], t, look=(0, 0), skin=COPY_SKIN, blink=False, coat=tk.RANGER,
                    rim=(0.85, 0.92, 1, 0.9 * flash), rim_from=(0, -10), breath=0.0)
        c.set_source_rgba(0.02, 0.02, 0.04, 0.9 - 0.3 * flash)   # the face stays in shadow
        c.save()
        c.translate(360, 830 - 175 * 0.85)
        c.scale(1, 1.15)
        c.arc(0, 0, 92, 0, 2 * math.pi)
        c.restore()
        c.fill()
    return fig


def copy_close(t, face, finger=0.0, write=None):
    """Your face at the glass. It never blinks."""
    def fig(c):
        tk.you_bust(c, 360, 1080, 1.55, face, t, look=(0, 0), skin=COPY_SKIN, blink=False, coat=tk.RANGER,
                    rim=(0.8, 0.9, 1, 0.5), rim_from=(0, -8), breath=0.3)
        if finger > 0:
            tk.finger_to_lips(c, 360, 1080 - 175 * 1.55 + 70 * 1.55 + 260 * (1 - finger), 1.55, COPY_SKIN,
                              tk.RANGER[:2])
        if write:
            write(c)
    return fig


def window_scene(cr, t, fig=None, flash=0.0, fog=0.0, writing=(), taps=(), dark=0.55):
    """Your cabin's window at night, from inside, by phone light. fig draws what's outside; writing = [(text, k)]
    cleared through the fog; taps = times of the knuckle taps (rings on the glass)."""
    n1.planks(cr, 0, 0, W, H, seed=2)
    cr.save()
    cr.rectangle(WX0, WY0, WX1 - WX0, WY1 - WY0)
    cr.clip()
    n1.night_window(cr, t, WX0, WY0, WX1, WY1, flash, horizon=0.66)
    walkway(cr)
    if fig:
        fig(cr)
    if flash > 0:
        cr.set_source_rgba(0.75, 0.85, 1, 0.25 * flash)
        cr.paint()
    for k in range(34):                                       # raindrops on the glass
        u, v = (k * 0.618) % 1, (k * 0.7548 + 0.3) % 1
        x, y = WX0 + 20 + u * (WX1 - WX0 - 40), WY0 + 20 + ((v + t * 0.02 * (k % 3 == 0)) % 1) * (WY1 - WY0 - 40)
        r = 3 + 4 * ((k * 0.37) % 1)
        cr.set_source_rgba(0.75, 0.85, 1, 0.2)
        cr.arc(x, y, r, 0, 2 * math.pi)
        cr.fill()
        cr.set_source_rgba(1, 1, 1, 0.4)
        cr.arc(x - r * 0.3, y - r * 0.3, r * 0.3, 0, 2 * math.pi)
        cr.fill()
    if fog > 0:                                               # breath fog on the glass, words cleared through it
        cr.push_group()
        cr.set_source_rgba(0.8, 0.84, 0.9, 0.42 * fog)
        cr.paint()
        cr.set_operator(cairo.OPERATOR_DEST_OUT)
        for k, (txt, kk, y) in enumerate(writing):
            n = int(len(txt) * clamp01(kk))
            size = min(70.0, 70 * (WX1 - WX0 - 90) / hud.text_width(cr, txt, 70, "Permanent Marker"))
            if n:
                hud2d._text(cr, txt[:n], W / 2 - hud.text_width(cr, txt, size, "Permanent Marker") / 2, y, size,
                            (0, 0, 0, 1), "Permanent Marker")
        cr.pop_group_to_source()
        cr.paint()
    for at in taps:                                           # knuckle marks: rings on the glass
        d = t - at
        if 0 <= d < 0.6:
            cr.set_source_rgba(1, 1, 1, 0.5 * (1 - d / 0.6))
            cr.set_line_width(3)
            cr.arc(470, 430, 10 + 60 * d, 0, 2 * math.pi)
            cr.stroke()
    g = cairo.LinearGradient(WX0, WY0, WX1, WY1)              # glass sheen
    g.add_color_stop_rgba(0, 1, 1, 1, 0.08)
    g.add_color_stop_rgba(0.5, 1, 1, 1, 0.0)
    cr.set_source(g)
    cr.paint()
    cr.restore()
    for (x0, y0, w, h) in ((WX0 - 26, WY0 - 26, WX1 - WX0 + 52, 26), (WX0 - 26, WY1, WX1 - WX0 + 52, 34),
                           (WX0 - 26, WY0 - 26, 26, WY1 - WY0 + 52), (WX1, WY0 - 26, 26, WY1 - WY0 + 52)):
        toon(cr, lambda c, x0=x0, y0=y0, w=w, h=h: c.rectangle(x0, y0, w, h), n1.PLANK, n1.PLANK_D, (-4, -3), None,
             lw=4)
    small_clock(cr, t, 610, 1110, 52)                         # on the wall under the window (clear of the stats bar)
    phone_dark(cr, 360, 1250, 1100, dark)


def small_clock(cr, t, x, y, r):
    """The wall clock beside the window. Its second hand runs backwards (the rewatch detail)."""
    toon(cr, lambda c: c.arc(x, y, r + 6, 0, 2 * math.pi), hexa("#2b2b2b"), None, (0, 0), None, lw=4)
    toon(cr, lambda c: c.arc(x, y, r, 0, 2 * math.pi), hexa("#e9e2cf"), hexa("#cfc5aa"), (-4, -3), None, lw=3)
    for frac, ln, w, col in ((4.67 / 12, r * 0.5, 6, INK), (40.0 / 60, r * 0.78, 4, INK),
                             ((-int(t * 1.0)) % 60 / 60, r * 0.85, 2, (0.8, 0.1, 0.08, 1))):
        a = frac * 2 * math.pi
        cr.set_source_rgba(*col)
        cr.set_line_width(w)
        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        cr.move_to(x, y)
        cr.line_to(x + ln * math.sin(a), y - ln * math.cos(a))
        cr.stroke()


# ------------------------------------------------------------------ the logbook's hidden page
def logbook3(cr, t, flip, k3):
    """The logbook by phone light; the page you never turned flips over, and rule 3 is on the other side."""
    n1.planks(cr, 0, 0, W, H, horizontal=False, seed=7, base=hexa("#7a5638"), dark=hexa("#553a24"), board=90)
    cr.save()
    cr.translate(360, 560)
    cr.rotate(-0.04)
    cr.scale(0.9, 0.9)
    cr.set_source_rgba(0, 0, 0, 0.45)
    tk.tk_rrect(cr, -330, -300, 670, 620, 14)
    cr.fill()
    toon(cr, lambda c: tk.tk_rrect(c, -340, -310, 670, 610, 12), hexa("#5a2a1c"), None, (0, 0), None, lw=5)
    page = lambda c, side: tk.curve(c, [(0, -290), (side * 160, -300), (side * 318, -292), (side * 318, 280),
                                        (side * 160, 286), (0, 278)])
    for side in (-1, 1):
        toon(cr, lambda c, side=side: page(c, side), hexa("#efe4c6"), hexa("#d9caa3"), (side * 6, -4), None, lw=4)
    ink = (0.12, 0.14, 0.3, 1)
    if flip >= 0.5:                                          # left: the rules you knew; right: the one you didn't
        hud2d._text(cr, "TOWER 9", -290, -230, 36, ink, "Kalam")
        for j, ln in enumerate(["1. NEVER answer", "the radio after 3 AM.", "", "2. NEVER open", "the hatch."]):
            hud2d._text(cr, ln, -294, -160 + j * 40, 28, ink, "Kalam")
        lines = ["3. If two of them", "come, let one in", "before 4:44.", "", "Or they both", "come in."]
        left = int(sum(len(x) for x in lines) * clamp01(k3))
        for j, ln in enumerate(lines):
            part = ln[:max(0, left)]
            left -= len(ln)
            if part:
                hud2d._text(cr, part, 24, -200 + j * 46, 33, (0.45, 0.08, 0.08, 1), "Kalam")
    else:                                                    # before: the rules on the right, old entries on the left
        cr.set_source_rgba(0.2, 0.25, 0.45, 0.35)
        for k in range(11):
            cr.set_line_width(2)
            x = -290
            cr.move_to(x, -230 + k * 44)
            for j in range(14):
                x += 18
                cr.line_to(x, -230 + k * 44 + 4 * math.sin(j * 1.9 + k))
            cr.stroke()
        hud2d._text(cr, "TOWER 9", 30, -230, 36, ink, "Kalam")
        for j, ln in enumerate(["1. NEVER answer", "the radio after 3 AM.", "", "2. NEVER open", "the hatch."]):
            hud2d._text(cr, ln, 26, -160 + j * 40, 28, ink, "Kalam")
    if 0 < flip < 1:                                         # the page turning over the spine
        w = 318 * math.cos(math.pi * flip)
        cr.save()
        poly(cr, [(0, -290), (w, -300 - 20 * math.sin(math.pi * flip)), (w, 280 + 10 * math.sin(math.pi * flip)),
                  (0, 278)])
        cr.set_source_rgba(*mix(hexa("#efe4c6"), (0, 0, 0, 1), 0.15 * math.sin(math.pi * flip)))
        cr.fill_preserve()
        cr.set_source_rgba(*INK)
        cr.set_line_width(4)
        cr.stroke()
        cr.restore()
    cr.restore()
    glow(cr, 380, 620, 420, PHONE, 0.18)
    phone_dark(cr, 380, 600, 760, 0.95)


# ------------------------------------------------------------------ the film
def shots(tl):
    A, B = tl.at, tl.by_id
    return [
        (0.0, "face"), (B["n2"].start - 0.2, "tower"), (A("n2", "An") - 0.1, "hatch_recap"),
        (B["n3"].start - 0.2, "boots"), (B["n4"].start - 0.2, "window"), (B["n5"].start - 0.15, "window_far"),
        (B["n6"].start - 0.2, "copy"), (B["n8"].start - 0.2, "hatch"), (B["n10"].start - 0.2, "logbook"),
        (B["n12"].start - 0.2, "clock"), (B["n13"].start - 0.2, "fog"), (B["n14"].start - 0.2, "copy2"),
        (B["n15"].start - 0.2, "hatch2"), (B["n16"].start - 0.2, "split"), (tl.total + 1, "end")]


_shots = {}


def draw(cr, t, tl):
    A, B = tl.at, tl.by_id
    if id(tl) not in _shots:
        _shots[id(tl)] = shots(tl)
    sh = _shots[id(tl)]
    k = max(i for i, (at, _) in enumerate(sh) if at <= t or i == 0)
    s0, name, s1 = sh[k][0], sh[k][1], sh[k + 1][0]
    t_die = A("n1", "die.", end=True) + 0.05
    taps0 = B["n5"].start - 1.05                               # three taps in the silence before "Lightning."
    taps = [taps0, taps0 + 0.38, taps0 + 0.76]
    flashes = [B["n5"].start + 0.05]
    fl = n1.flash_level(t, flashes)

    def hatch_dark(light=0.0, frost=0.0, boots=False, tremble=0.0):
        n1.hatch(cr, t, light=light, frost=frost, boots=boots, tremble=tremble)
        grade(cr, (0.55, 0.62, 0.8), (0.3, 0.33, 0.42))
        glow(cr, 360, 1200, 700, PHONE, 0.14)
        phone_dark(cr, 360, 1150, 1100, 0.75)

    def split(c_top, c_bottom):
        cr.save()
        cr.rectangle(0, 0, W, H / 2)
        cr.clip()
        cr.translate(0, -390)
        c_top()
        cr.restore()
        cr.save()
        cr.rectangle(0, H / 2, W, H / 2)
        cr.clip()
        cr.translate(0, 380)
        c_bottom()
        cr.restore()
        cr.set_source_rgba(0.85, 0.9, 1, 0.8)
        cr.rectangle(0, H / 2 - 3, W, 6)
        cr.fill()

    cr.save()
    if name == "face":
        camera(cr, t, s0, s1, 1.0, 1.07)
        on = 1.0 if t < t_die else 0.0
        if t_die - 0.6 < t < t_die:
            on = 0.35 if noise(t * 23, 3) > 0.2 else 1.0
        lit = t >= t_die
        hud2d.blurred(cr, lambda c: (n1.cabin(c, t, on=on),
                                     grade(c, (0.3, 0.34, 0.46), (0.12, 0.13, 0.2)) if lit else None), sigma=8)
        f = tk.face_mix("uneasy", "alarmed", seg(t, t_die, t_die + 0.4))
        tk.you_bust(cr, 360, 930, 1.42, f, t, look=(0.2, -0.5 if not lit else 0.3), coat=tk.RANGER,
                    light=(0, 14) if lit else (-18, -14), rim=(0.8, 0.9, 1, 0.7) if lit else n1.WARM_RIM,
                    rim_from=(0, 10) if lit else (-10, -4), skin=PHONE_SKIN if lit else None, sweat=0.6)
        if lit:
            glow(cr, 360, 1300, 520, PHONE, 0.35)
            phone_dark(cr, 360, 1100, 1000, 0.75)
    elif name == "tower":
        camera(cr, t, s0, s1, 1.0, 1.08, cy=500)
        n1.tower_ext(cr, t, 0.0, lit=0.0)                     # its windows dark now; one phone glow
        glow(cr, 360, 330 - 66, 40, PHONE, 0.5)
    elif name in ("hatch_recap", "boots", "hatch", "hatch2"):
        camera(cr, t, s0, s1, 1.0, 1.08, cy=600)
        if name == "hatch_recap":
            hatch_dark(frost=0.6)
            grade(cr, (1, 0.93, 0.8), (0.8, 0.7, 0.6))       # memory tint
        elif name == "boots":
            hatch_dark(frost=0.4, boots=True)
        elif name == "hatch":
            hatch_dark(frost=0.4 + 0.6 * seg(t, s0, B["n9"].end), light=0.15)
        else:
            hatch_dark(frost=1.0, light=0.5 + 0.2 * math.sin(t * 3))
    elif name in ("window", "window_far"):
        camera(cr, t, s0, s1, 1.0, 1.08, cy=560)
        fig = copy_far(t, max(fl, 0.25 * seg(t, B["n5"].start, B["n5"].end))) if name == "window_far" else None
        window_scene(cr, t, fig, flash=fl, taps=taps)
    elif name in ("copy", "copy2"):
        camera(cr, t, s0, s1, 1.02, 1.12, cy=560, shake=0.6)
        if name == "copy":
            face = tk.face_mix("calm", "smile", seg(t, A("n7", "smiles") - 0.1, A("n7", "smiles") + 0.3))
            finger = seg(t, A("n7", "finger") - 0.35, A("n7", "finger") + 0.2)
        else:
            face, finger = tk.FACES["smile"], 0.0
        window_scene(cr, t, copy_close(t, face, finger), dark=0.35)
    elif name == "fog":
        camera(cr, t, s0, s1, 1.0, 1.06, cy=480)
        w1 = seg(t, A("n13", "It's") - 0.1, A("n13", "you.", end=True))
        w2 = seg(t, A("n13", "Let") - 0.1, B["n13"].end)
        window_scene(cr, t, copy_close(t, tk.FACES["calm"]), fog=seg(t, s0, s0 + 0.8),
                     writing=[("IT'S UNDER YOU.", w1, 420), ("LET ME IN.", w2, 520)], dark=0.4)
    elif name == "logbook":
        camera(cr, t, s0, s1, 1.0, 1.08, cy=600)
        logbook3(cr, t, seg(t, A("n10", "page") - 0.3, A("n10", "turned.", end=True)),
                 seg(t, B["n11"].start, B["n11"].end))
    elif name == "clock":
        camera(cr, t, s0, s1, 1.0, 1.14, cy=560)
        n1.clock(cr, -t, h=4, m=40, sec0=int(s0) + 25)          # it runs backwards
        grade(cr, (0.6, 0.66, 0.82), (0.32, 0.35, 0.45))
        phone_dark(cr, 360, 700, 900, 0.7)
    elif name == "split":
        camera(cr, t, s0, s1, 1.0, 1.03, shake=0.5)
        split(lambda: window_scene(cr, t, copy_close(t, tk.FACES["smile"]), dark=0.35),
              lambda: hatch_dark(frost=1.0, light=0.6 + 0.2 * math.sin(t * 3)))
    cr.restore()
    hud.finish(cr, t, flash_at=flashes, vig=0.6, grain=0.06)
    clock_v = ("TIME", "4:40 AM", "bad", B["n12"].start) if t >= B["n12"].start else ("TIME", "4:14 AM", None)
    phone = ("PHONE", f"{round(9 - 4 * seg(t, t_die, tl.total))}%", "warn")
    third = (("LET ONE IN BY", "4:44", "bad", A("n11", "before")) if t >= A("n11", "before")
             else ("POWER", "OFF", "bad", t_die) if t >= t_die else ("POWER", "ON", None))
    hud2d.stats(cr, t, [clock_v, phone, third])
    hud2d.hook(cr, t, [("YOU KEPT IT SHUT.", False), ("NOW THE LIGHTS", False), ("ARE OUT", True)],
               end=B["n1"].end + 0.15, y=270)
    hud2d.stamp(cr, t, A("n3", "Most"), B["n3"].end + 0.4, ["YOU VOTED B", "KEEP IT SHUT"], y=300)
    hud2d.rule_tag(cr, t, B["n11"].start, B["n11"].end + 0.4, "RULE 3: LET ONE IN BY 4:44", y=190)
    hud2d.bubble(cr, t, B["n9"].start, B["n9"].end, "Don't let it in. It's been wearing your face all night.",
                 360, 260, (360, 390), creepy=True)
    hud2d.ab_card(cr, t, A("n17", "who"), "WINDOW", "HATCH", kicker="TOWER 9 · NIGHT 2 · YOUR CHOICE",
                  decides="Night 3")
    hud2d.captions(cr, t, tl, KEY, skip=("n9",))
    cue("generator", t, 0.0, t_die)
    cue("power_down", t, t_die)                                # after "die." (on the word it was heard as "sky")
    cue("glass_tap", t, taps0)
    cue("thunder", t, B["n7"].end + 0.05)                      # rolls out in the silence before n8
    cue("heartbeat", t, B["n10"].start, B["n15"].end - B["n10"].start)
    cue("riser", t, B["n16"].start, B["n17"].start - B["n16"].start)
