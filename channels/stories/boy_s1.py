"""THE BOY WHO INHERITED ANOTHER BODY, Short 1: "The Last Thing Neil Bought" (9:16). The owner's story
(channels/stories/boy_who_inherited_bible.md); scenes from the approved reconstructed Chapter 1
(channels/stories/boy_who_inherited_ch1.md, parts I and II and the start of III). Auto-approved, 27 Oct 2026.

Hook: seventeen, five million, dead the next day. The trade (the fake buy walls, selling into the spike), the canon
number, the text to Maya, the café, the receipt, the crossing, the car. Ends on the half second: push her, or pull
her back? (Short 2 shows what he did.)

    /home/user/.venv-main/bin/python channels/horror/make_2d.py boy_s1   -> out/stories/boy_s1.mp4
"""
import math

from motion import audio, voice
from motion.engine import W, H, clamp01, cue, seg

from channels.horror import hud, hud2d, sound  # noqa: F401
from channels.horror.toon2d import INK, glow, grade, noise
from channels.stories import boy_art as B

NARRATOR = dict(turbo=True, turbo_ref="bm_george")
TAIL = 2.0
MUSIC = "horror"
TWIST = "b17"
voice.SPEAKERS.update({
    "neil": dict(voice="am_liam", turbo_ref="am_liam"),
    "maya": dict(voice="af_nova", turbo_ref="af_nova"),
})
audio.GAINS.update(click=0.5, brakes=0.7)
BAL = "$5,014,382.61"

SCRIPT = [
    dict(id="b1", scene="hook", text="At seventeen, Neil turned a thousand dollars into five million."),
    dict(id="b2", scene="hook", text="The next day, he was dead.", gap=0.5),
    dict(id="b3", scene="room", text="Nineteen minutes before the closing bell, his stock jumped eleven percent. "
                                     "Everyone said hold.", gap=0.5),
    dict(id="b4", scene="book", text="Neil watched the order book instead. Huge buy orders kept appearing, and "
                                     "vanishing before anyone could sell into them."),
    dict(id="b5", scene="book", text="Someone wanted the crowd to believe in a floor that wasn't there."),
    dict(id="b6", scene="room", text="He sold everything into the spike. Six minutes later, the floor disappeared.",
         gap=0.5),
    dict(id="b7", scene="balance", text="[Five million, fourteen thousand, three hundred and eighty-two dollars, and "
                                        "sixty-one cents.|$5,014,382.61.]", gap=0.4),
    dict(id="b8", scene="phone", text="He didn't tell anyone. Except Maya."),
    dict(id="b9", scene="phone", text="You awake?", speaker="neil"),
    dict(id="b10", scene="phone", text="Always. Why are you?", speaker="maya"),
    dict(id="b11", scene="phone", text="Of everyone he knew, she was the only one who never asked him how much.",
         gap=0.5),
    dict(id="b12", scene="cafe", text="The next afternoon, he told her. She didn't ask him for anything."),
    dict(id="b13", scene="cafe", text="Neil. You could do anything.", speaker="maya"),
    dict(id="b14", scene="cafe", text="I'm starting with hot chocolate.", speaker="neil", gap=0.4),
    dict(id="b15", scene="receipt", text="Two hot chocolates. Nine dollars and twenty cents. It was the last thing "
                                         "Neil ever bought.", gap=0.6),
    dict(id="b16", scene="street", text="At the crossing, the light turned green. Maya stepped off the kerb, laughing "
                                        "at him."),
    dict(id="b17", scene="street", text="And Neil noticed the one thing on the street that didn't fit.", gap=0.4),
    dict(id="b18", scene="car", text="A car that wasn't slowing down.", gap=0.6),
    dict(id="b19", scene="car", text="Half a second. Do you push her? Or pull her back?", gap=0.3),
]

METADATA = dict(
    title="At 17 He Turned $1,000 Into $5,014,382.61. The Next Day He Was Dead. 💸",
    alt_titles=["The Last Thing He Bought Cost $9.20 💸", "The Boy Who Inherited Another Body, Part 1 💸"],
    description="""At seventeen, Neil turned a thousand dollars into $5,014,382.61. He told one person: Maya. The next day, at a crossing, a car didn't slow down. 💸

The Boy Who Inherited Another Body, Part 1. Part 2: what happened in that half second, and where Neil woke up.
💬 Half a second: do you push her, or pull her back? 👇

(Original story. Fiction. 2D animation. Not financial advice.)""",
    hashtags=["#Thriller", "#Story", "#Shorts"],
    tags=["the boy who inherited another body", "thriller", "psychological thriller", "trader", "stock market",
          "story", "reincarnation", "plot twist", "2d animation", "part 1"],
    pinned_comment="Push. Pulling her back means she's still in the road when it hits. Push or pull? 👇 "
                   "(Look at what she's holding 👀)",
)

KEY = {"seventeen", "thousand", "million", "dead", "hold", "vanishing", "floor", "everything", "disappeared", "maya",
       "awake", "always", "how", "anything", "chocolate", "last", "bought", "green", "laughing", "fit", "slowing",
       "push", "pull"}


def camera(cr, t, s0, s1, z0=1.0, z1=1.06, cx=W / 2, cy=H / 2, shake=1.0):
    k = seg(t, s0, s1)
    z = z0 + (z1 - z0) * k
    cr.translate(cx + 4 * shake * noise(t * 0.7, 1), cy + 3 * shake * noise(t * 0.6, 4))
    cr.rotate(0.004 * shake * noise(t * 0.5, 7))
    cr.scale(z, z)
    cr.translate(-cx, -cy)


def big_number(cr, t, k, y=None):
    """The account balance, huge, counting up into place."""
    y = y or H * 0.42
    if k <= 0:
        return
    cr.set_source_rgba(0.01, 0.03, 0.03, 0.9 * k)
    cr.paint()
    glow(cr, W / 2, y, W * 0.6, (0.3, 1, 0.6), 0.25 * k)
    sz = min(96.0, 96 * (W - 60) / B.text_width(cr, BAL, 96, "Liberation Mono"))
    hud2d._text(cr, BAL, W / 2, y + sz * 0.35, sz, (0.45, 1, 0.65, k), "Liberation Mono", "center")
    hud2d._text(cr, "ACCOUNT BALANCE", W / 2, y - sz * 0.9, 26, (0.6, 0.85, 1, 0.8 * k), "Liberation Mono", "center")


def cup_spin(cr, t, t0, x, y, s):
    """Maya's hot chocolate, spinning across the road."""
    a = (t - t0) * 7
    cr.save()
    cr.translate(x + (t - t0) * 160, y - 40 * math.sin(min(math.pi, (t - t0) * 3)))
    cr.rotate(a)
    cr.scale(s, s)
    B.toon(cr, lambda c: B.poly(c, [(-36, -60), (36, -60), (28, 50), (-28, 50)]), B.hexa("#f4efe6"), B.hexa("#cfc7b8"),
           (-3, -3), None, lw=3.5)
    B.toon(cr, lambda c: B.tk.tk_rrect(c, -42, -78, 84, 22, 8), B.hexa("#5a3a24"), None, (0, 0), None, lw=3)
    cr.restore()


# ------------------------------------------------------------------ the film
def shots(tl):
    A_, Bb = tl.at, tl.by_id
    return [
        (0.0, "hook"), (Bb["b2"].start - 0.1, "hook2"), (Bb["b3"].start - 0.2, "neil_room"),
        (A_("b3", "Everyone") - 0.1, "chart"), (Bb["b4"].start - 0.15, "book"), (Bb["b5"].start - 0.1, "neil_focus"),
        (Bb["b6"].start - 0.15, "chart_fall"), (Bb["b7"].start - 0.15, "balance"), (Bb["b8"].start - 0.15, "neil_phone"),
        (Bb["b9"].start - 0.15, "phone"), (Bb["b11"].start - 0.1, "neil_smile"), (Bb["b12"].start - 0.15, "cafe"),
        (Bb["b13"].start - 0.15, "maya"), (Bb["b14"].start - 0.15, "neil_cafe"), (Bb["b15"].start - 0.15, "cups"),
        (A_("b15", "It") - 0.1, "receipt"), (Bb["b16"].start - 0.15, "crossing"), (Bb["b17"].start - 0.1, "neil_notice"),
        (Bb["b18"].start - 0.1, "car"), (Bb["b19"].start - 0.1, "freeze"), (tl.total + 1, "end")]


_shots = {}


def draw(cr, t, tl):
    A_, Bb = tl.at, tl.by_id
    if id(tl) not in _shots:
        _shots[id(tl)] = shots(tl)
    sh = _shots[id(tl)]
    k = max(i for i, (at, _) in enumerate(sh) if at <= t or i == 0)
    s0, name, s1 = sh[k][0], sh[k][1], sh[k + 1][0]
    talk = lambda who: 1.0 if tl.speaking(who, t) else 0.0
    by = 940
    blue = (0.55, 0.75, 1, 0.7)
    crash = seg(t, A_("b6", "Six"), Bb["b6"].end)

    cr.save()
    if name in ("hook", "hook2"):
        camera(cr, t, s0, s1, 1.0, 1.08)
        hud2d.blurred(cr, lambda c: B.trading_room(c, t, balance=BAL), sigma=9)
        B.bust(cr, W / 2, by + 60, 1.2, t, "neil", "calm" if name == "hook" else "focus", look=(0, 0.2), rim=blue,
               rim_from=(0, -10))
        if name == "hook2":
            cr.set_source_rgba(0, 0, 0, 0.45 * seg(t, s0, s0 + 0.5))
            cr.paint()
    elif name in ("neil_room", "neil_focus"):
        camera(cr, t, s0, s1, 1.02, 1.1)
        hud2d.blurred(cr, lambda c: B.trading_room(c, t, flash_walls=1.0 if name == "neil_focus" else 0.0), sigma=7)
        B.bust(cr, W / 2, by + 60, 1.2, t, "neil", "focus", look=(0.1, -0.3), rim=blue, rim_from=(0, -10))
    elif name in ("chart", "chart_fall"):
        camera(cr, t, s0, s1, 1.0, 1.1, cy=H * 0.36)
        B.trading_room(cr, t, crash=crash if name == "chart_fall" else 0.0)
    elif name == "book":
        camera(cr, t, s0, s1, 1.0, 1.12, cx=W * 0.7, cy=H * 0.25)
        B.trading_room(cr, t, flash_walls=1.0)
    elif name == "balance":
        camera(cr, t, s0, s1, 1.0, 1.05)
        B.trading_room(cr, t, balance=BAL, crash=1.0)
    elif name in ("neil_phone", "neil_smile"):
        camera(cr, t, s0, s1, 1.02, 1.08)
        hud2d.blurred(cr, lambda c: B.trading_room(c, t, balance=BAL, crash=1.0), sigma=9)
        B.bust(cr, W / 2, by + 60, 1.2, t, "neil", "smile" if name == "neil_smile" else "calm", look=(0, 0.5),
               rim=blue, rim_from=(0, 10))
    elif name == "phone":
        camera(cr, t, s0, s1, 1.0, 1.04)
        hud2d.blurred(cr, lambda c: B.trading_room(c, t, balance=BAL, crash=1.0), sigma=12)
        msgs = [("You awake?", True, seg(t, Bb["b9"].start, Bb["b9"].end)),
                ("Always. Why are you?", False, seg(t, Bb["b10"].start, Bb["b10"].end))]
        B.phone_chat(cr, t, W / 2, H * 0.48, 1.35, msgs, typing=Bb["b9"].end < t < Bb["b10"].start)
    elif name in ("cafe", "maya", "neil_cafe"):
        camera(cr, t, s0, s1, 1.02, 1.06)
        hud2d.blurred(cr, lambda c: B.cafe(c, t, dusk=0.3), sigma=9)
        if name == "cafe":
            B.bust(cr, 220, by + 80, 0.95, t, "neil", "smile", look=(0.6, 0), outfit="jacket")
            B.bust(cr, 510, by + 60, 1.0, t, "maya", "smile", look=(-0.6, 0))
        else:
            who = "maya" if name == "maya" else "neil"
            B.bust(cr, W / 2, by + 40, 1.2, t, who, "smile" if who == "maya" else "grin", look=(0.2, 0),
                   talk=talk(who), outfit="jacket" if who == "neil" else None)
    elif name == "cups":
        camera(cr, t, s0, s1, 1.0, 1.08, cy=H * 0.65)
        B.cafe(cr, t, cups=1.0, dusk=0.3)
    elif name == "receipt":
        camera(cr, t, s0, s1, 1.0, 1.1, cy=H * 0.5)
        cr.set_source_rgba(*B.hexa("#3a2a20"))
        cr.paint()
        B.receipt(cr, t, W / 2, H * 0.48, 1.6)
    elif name == "crossing":
        camera(cr, t, s0, s1, 1.0, 1.06)
        B.street(cr, t, "green", dusk=0.55)
        B.bust(cr, W * 0.62, H * 0.98, 0.95, t, "maya", "laugh", look=(-0.5, 0))
        B.bust(cr, W * 0.22, H * 1.04, 0.85, t, "neil", "smile", look=(0.6, 0), outfit="jacket")
    elif name == "neil_notice":
        camera(cr, t, s0, s1, 1.02, 1.12, shake=1.3)
        hud2d.blurred(cr, lambda c: B.street(c, t, "green", car=0.2, dusk=0.55), sigma=8)
        B.bust(cr, W / 2, by + 40, 1.2, t, "neil", "focus", look=(-0.8, 0), outfit="jacket")
    elif name in ("car", "freeze"):
        frozen = name == "freeze"
        tt = Bb["b19"].start if frozen else t
        camera(cr, tt, s0, s1, 1.0, 1.12, shake=0.0 if frozen else 2.0)
        cprog = 0.4 + 0.45 * seg(tt, Bb["b18"].start, Bb["b18"].end + 0.5)
        B.street(cr, tt, "green", car=cprog, dusk=0.55)
        B.bust(cr, W * 0.62, H * 1.0, 0.95, tt, "maya", "shock", look=(-0.8, 0), rim=(1, 0.97, 0.85, 0.9),
               rim_from=(-10, 0))
        if frozen:                                              # a freeze frame: everything stops
            cr.set_source_rgba(0.6, 0.65, 0.75, 0.25)
            cr.paint()
            grade(cr, (0.8, 0.82, 0.9), (0.4, 0.42, 0.5))
    cr.restore()

    hud.finish(cr, t, flash_at=[], vig=0.45, grain=0.05)
    if name == "balance":
        big_number(cr, t, seg(t, Bb["b7"].start - 0.1, Bb["b7"].start + 0.4))
    hud2d.hook(cr, t, [("17 YEARS OLD.", False), (BAL, True)], end=Bb["b1"].end + 0.05, y=240, size=74)
    hud2d.stamp(cr, t, Bb["b2"].start, Bb["b2"].end + 0.3, ["THE NEXT DAY: DEAD"], y=330)
    hud2d.stamp(cr, t, A_("b15", "last") - 0.1, Bb["b15"].end + 0.3, ["THE LAST THING", "HE EVER BOUGHT"], y=300,
                col=hud2d.YELLOW)
    if t < A_("b19", "Do"):
        hud2d.captions(cr, t, tl, KEY, y=1010)
    final_card(cr, t, A_("b19", "Do"))
    cue("click", t, Bb["b6"].start - 0.15)
    cue("heartbeat", t, Bb["b16"].start, Bb["b18"].end - Bb["b16"].start)
    cue("brakes", t, Bb["b18"].end + 0.05)
    cue("riser", t, Bb["b18"].start, Bb["b19"].start - Bb["b18"].start)


def final_card(cr, t, start):
    """HALF A SECOND. PUSH HER / PULL HER BACK, held over the tail."""
    if t < start:
        return
    k = clamp01((t - start) / 0.3)
    cr.set_source_rgba(0.02, 0.02, 0.04, 0.78 * k)
    cr.paint()
    hud2d._text(cr, "HALF A SECOND.", W / 2, 320, 64, (1, 1, 1, k), hud2d.ROUND, "center", shadow=0.5)
    for n, (lab, col) in enumerate((("PUSH HER", hud2d.RED), ("PULL HER BACK", hud2d.GREEN))):
        p = clamp01((t - start - 0.2 - 0.15 * n) / 0.25)
        if p <= 0:
            continue
        y = 480 + n * 150
        B.tk.tk_rrect(cr, W / 2 - 250, y - 55, 500, 110, 22)
        cr.set_source_rgba(0.06, 0.06, 0.08, p)
        cr.fill_preserve()
        cr.set_source_rgba(*col[:3], p)
        cr.set_line_width(6)
        cr.stroke()
        hud2d._text(cr, lab, W / 2, y + 16, 46, (1, 1, 1, p), hud2d.ROUND, "center")
    p = clamp01((t - start - 0.6) / 0.25)
    if p > 0:
        hud2d._text(cr, "COMMENT PUSH OR PULL · PART 2 SHOWS WHAT HE DID", W / 2, 820, 24, (1, 1, 1, 0.85 * p),
                    hud2d.ROUND, "center")
