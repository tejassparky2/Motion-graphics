"""THE BOY WHO INHERITED ANOTHER BODY, Chapter 1 (the long video, 16:9). Auto-approved by the owner, 27 Oct 2026.
The approved reconstructed chapter (channels/stories/boy_who_inherited_ch1.md), told in three parts with its three
titles: I. The Market Was Lying, II. The Last Thing Neil Bought, III. The Last Position. The law is the owner's: the
nearest and the weakest body. Nothing else is added: Arthur's family and enemies are named only as canon has them
(a family Neil never met, enemies he didn't know he had); the funeral is plot point 7.

    /home/user/.venv-main/bin/python channels/horror/make_2d.py boy_long   -> out/stories/boy_long.mp4 (1280x720)
"""
import math

from motion import audio, voice
from motion.engine import W, H, clamp01, cue, seg

from channels.horror import hud, hud2d, sound  # noqa: F401
from channels.horror.toon2d import INK, glow, grade, noise
from channels.stories import boy_art as B
from channels.stories import boy_s1 as S1

NARRATOR = dict(turbo=True, turbo_ref="bm_george")
TAIL = 2.5
MUSIC = "horror"
TWIST = "l40"
voice.SPEAKERS.update({
    "neil": dict(voice="am_liam", turbo_ref="am_liam"),
    "maya": dict(voice="af_nova", turbo_ref="af_nova"),
    "nurse": dict(voice="af_sarah", turbo_ref="af_sarah"),
    "old": dict(voice="bm_lewis", turbo_ref="bm_lewis-3", fx="vibrato=f=6:d=0.25,volume=1.3"),   # Neil, in Arthur
})
audio.GAINS.update(click=0.5, brakes=0.7, sting=0.55)
BAL = S1.BAL

SCRIPT = [
    dict(id="l1", scene="cold", text="Neil was seventeen when he made five million dollars."),
    dict(id="l2", scene="cold", text="He was dead the next day."),
    dict(id="l3", scene="cold", text="And then, he wasn't.", gap=0.6),
    # I. The Market Was Lying
    dict(id="l4", scene="room", text="The market was lying, and Neil was the only one watching closely enough to see "
                                     "it.", gap=3.6),                     # title + part I card play first
    dict(id="l5", scene="room", text="Nineteen minutes before the closing bell, the stock he'd been holding for three "
                                     "weeks jumped eleven percent on a headline."),
    dict(id="l6", scene="room", text="Every chat he followed lit up with the same word. Hold. Hold for more."),
    dict(id="l7", scene="room", text="Neil didn't look at the headline. He looked at the order book."),
    dict(id="l8", scene="book", text="Thick walls of buy orders sat a few cents under the price. The kind that tell a "
                                     "crowd there's a floor."),
    dict(id="l9", scene="book", text="Except they kept vanishing the moment anyone tried to sell into them. And "
                                     "reappearing a cent lower."),
    dict(id="l10", scene="book", text="Someone wanted the crowd to believe in a floor that wasn't there."),
    dict(id="l11", scene="room", text="He'd learned to read lies like that with a thousand dollars. A thousand dollars "
                                      "meant every mistake hurt. So he'd stopped making the loud ones."),
    dict(id="l12", scene="room", text="He sold everything into the spike.", gap=0.5),
    dict(id="l13", scene="room", text="Then he did the hardest thing in trading. Nothing.", gap=0.8),
    dict(id="l14", scene="chart", text="Six minutes later, the walls disappeared all at once, and the price fell "
                                       "through the place they'd been."),
    dict(id="l15", scene="room", text="The account refreshed.", gap=0.5),
    dict(id="l16", scene="balance", text="[Five million, fourteen thousand, three hundred and eighty-two dollars, and "
                                         "sixty-one cents.|$5,014,382.61.]", gap=0.6),
    dict(id="l17", scene="room", text="He read it twice. He didn't post it. He didn't call anyone. He opened one "
                                      "conversation."),
    dict(id="l18", scene="phone", text="You awake?", speaker="neil"),
    dict(id="l19", scene="phone", text="Always. Why are you?", speaker="maya"),
    dict(id="l20", scene="room", text="Of everyone he knew, she was the only one who had never once asked him how "
                                      "much.", gap=0.6),
    # II. The Last Thing Neil Bought
    dict(id="l21", scene="cafe", text="They met the next afternoon, outside the café by the station. Maya wanted to "
                                      "see his face when he told her.", gap=3.0),   # part II card
    dict(id="l22", scene="cafe", text="So?", speaker="maya"),
    dict(id="l23", scene="cafe", text="So. I was right.", speaker="neil"),
    dict(id="l24", scene="cafe", text="You're always right. That's what makes you unbearable. How right?",
         speaker="maya", gap=0.5),
    dict(id="l25", scene="cafe", text="He told her. She didn't scream. She didn't ask him to buy her anything. She went "
                                      "very still, and then she laughed, quietly."),
    dict(id="l26", scene="cafe", text="Neil. You could do anything.", speaker="maya"),
    dict(id="l27", scene="cafe", text="I know. I'm starting with hot chocolate.", speaker="neil", gap=0.5),
    dict(id="l28", scene="cups", text="Two hot chocolates. Nine dollars and twenty cents.", gap=0.5),
    dict(id="l29", scene="receipt", text="Later, the police would find the receipt in his jacket pocket. Of "
                                         "everything Neil had ever bought, it was the last.", gap=0.6),
    # III. The Last Position
    dict(id="l30", scene="street", text="They walked, because Maya walked when she was thinking.", gap=3.0),
    dict(id="l31", scene="street", text="Promise me something. Don't turn into one of those people who only talks "
                                        "about money.", speaker="maya"),
    dict(id="l32", scene="street", text="I talk about other things.", speaker="neil"),
    dict(id="l33", scene="street", text="Name one.", speaker="maya", gap=0.4),
    dict(id="l34", scene="street", text="The light turned green. She stepped off the kerb, laughing at him."),
    dict(id="l35", scene="street", text="And Neil, who had trained himself to notice the one number on a screen that "
                                        "didn't fit, noticed the one thing on the street that didn't fit."),
    dict(id="l36", scene="car", text="A car that wasn't slowing down.", gap=0.6),
    dict(id="l37", scene="car", text="Traders say you never choose your last position when you're calm. You choose it "
                                     "in the half second when the price is already moving."),
    dict(id="l38", scene="car", text="He didn't think. He moved."),
    dict(id="l39", scene="car", text="He shoved her, hard. Maya went sprawling onto the far kerb. Safe.", gap=0.3),
    dict(id="l40", scene="car", text="Neil's last position was the middle of the crossing.", gap=0.9),
    dict(id="l41", scene="quiet", text="The impact didn't hurt. There was a sound, enormous and flat, and the sky "
                                       "turning over.", gap=0.6),
    dict(id="l42", scene="quiet", text="Then a quiet, like the moment after the market closes, when you finally find "
                                       "out what you're worth."),
    dict(id="l43", scene="quiet", text="Neil!", speaker="maya", gap=0.5),
    dict(id="l44", scene="quiet", text="Then he didn't hear anything.", gap=1.6),
    # waking
    dict(id="l45", scene="wake", text="Neil opened his eyes, and his body was wrong.", gap=1.0),
    dict(id="l46", scene="wake", text="Heavy. All of it. A machine beside him beeped in a slow, tired rhythm."),
    dict(id="l47", scene="hand", text="He lifted a hand. The skin was thin and spotted. A heavy gold ring on the "
                                      "third finger. It trembled."),
    dict(id="l48", scene="nurse", text="Mister Vance? Mister Vance, can you hear me? Don't try to sit up.",
         speaker="nurse", gap=0.5),
    dict(id="l49", scene="wake", text="Neil didn't know anyone called Vance."),
    dict(id="l50", scene="band", text="On the wristband by his face: Vance, Arthur. Age [eighty-two.|82.]", gap=0.5),
    dict(id="l51", scene="wake", text="My name is... Neil.", speaker="old", gap=0.4),
    dict(id="l52", scene="wake", text="What came out was an old man's voice. And that frightened him more than the "
                                      "hand."),
    dict(id="l53", scene="window", text="In the dark window, a reflection. An old man with a hollow face and white "
                                        "hair, staring back with Neil's own terror."),
    dict(id="l54", scene="window", text="Beyond it, far below, blue lights. A crowd. And Maya, kneeling at the "
                                        "crossing."),
    dict(id="l55", scene="window", text="About a hundred metres away.", gap=0.8),
    dict(id="l56", scene="law", text="The law gave him no choice. The nearest body. And the weakest.", gap=0.8),
    dict(id="l57", scene="arthur", text="Neil had made five million dollars by understanding things faster than "
                                        "everyone else. He understood this too, before he wanted to."),
    dict(id="l58", scene="arthur", text="He wasn't dead.", gap=0.4),
    dict(id="l59", scene="arthur", text="He was someone else.", gap=0.6),
    dict(id="l60", scene="arthur", text="An [eighty-two-year-old|82-year-old] billionaire, in a body that was failing. "
                                        "With a family he had never met, and enemies he didn't know he had."),
    dict(id="l61", scene="arthur", text="And soon, they would bury Neil.", gap=0.6),
    dict(id="l62", scene="arthur", text="Would you go to your own funeral?", gap=0.3),
]

METADATA = dict(
    title="He Died at 17 With $5,014,382.61. He Woke Up as an 82-Year-Old Billionaire. | Chapter 1",
    alt_titles=["The Boy Who Inherited Another Body, Chapter 1: The Last Position",
                "A 17-Year-Old Trader Died Saving Her. Then He Woke Up in Someone Else."],
    description="""At seventeen, Neil turned $1,000 into $5,014,382.61. He told one person: Maya. The next day, at a crossing, a car didn't slow down, and Neil had half a second.

He woke up in a hospital bed, a hundred metres away, in the body of Arthur Vance: eighty-two, a billionaire, and failing.

The Boy Who Inherited Another Body, Chapter 1
I. The Market Was Lying
II. The Last Thing Neil Bought
III. The Last Position

💬 Would you go to your own funeral?

An original story. Fiction. 2D animation. Not financial advice.""",
    hashtags=["#Thriller", "#Story", "#Animation"],
    tags=["the boy who inherited another body", "psychological thriller", "reincarnation", "body swap", "trader",
          "stock market", "billionaire", "original story", "chapter 1", "2d animation"],
    pinned_comment="Chapter 1. The law is the nearest body, and the weakest. Would you go to your own funeral?",
)

KEY = S1.KEY | {"lying", "headline", "walls", "nothing", "refreshed", "unbearable", "receipt", "promise", "money",
                "position", "moving", "shoved", "worth", "wrong", "vance", "neil", "terror", "hundred", "nearest",
                "weakest", "someone", "billionaire", "family", "enemies", "bury", "funeral"}
BLUE = (0.55, 0.75, 1, 0.7)
COLD = (0.75, 0.85, 1, 0.6)
HEAD = (1, 0.97, 0.85, 0.9)
PARTS = {"l4": ("I", "THE MARKET WAS LYING"), "l21": ("II", "THE LAST THING NEIL BOUGHT"),
         "l30": ("III", "THE LAST POSITION")}


def camera(cr, t, s0, s1, z0=1.0, z1=1.05, cx=W / 2, cy=H / 2, shake=1.0):
    k = seg(t, s0, s1)
    z = z0 + (z1 - z0) * k
    cr.translate(cx + 4 * shake * noise(t * 0.7, 1), cy + 3 * shake * noise(t * 0.6, 4))
    cr.rotate(0.004 * shake * noise(t * 0.5, 7))
    cr.scale(z, z)
    cr.translate(-cx, -cy)


def two(cr, t, tl, a, b, fa="smile", fb="smile", outfit_a=None):
    """Two people facing each other across the 16:9 frame."""
    B.bust(cr, W * 0.32, H * 0.97, 0.85, t, a, fa, look=(0.6, 0), talk=1.0 if tl.speaking(a, t) else 0.0,
           outfit=outfit_a)
    B.bust(cr, W * 0.68, H * 0.95, 0.88, t, b, fb, look=(-0.6, 0), talk=1.0 if tl.speaking(b, t) else 0.0)


def one(cr, t, tl, who, fx, look=(0.1, 0.0), rim=None, rim_from=(9, 0), outfit=None, **kw):
    B.bust(cr, W * 0.5, H * 0.94, 1.0, t, who, fx, look=look, talk=1.0 if tl.speaking(who, t) else 0.0, rim=rim,
           rim_from=rim_from, outfit=outfit, **kw)


def shots(tl):
    out = [(tl.by_id[d["id"]].start - 0.15, d["id"]) for d in SCRIPT]
    out += [(tl.by_id["l3"].end + 0.3, "title"), (tl.by_id["l3"].end + 2.0, "partI"),
            (tl.by_id["l20"].end + 0.4, "partII"), (tl.by_id["l29"].end + 0.4, "partIII"),
            (tl.at("l35", "noticed"), "l35b"), (tl.by_id["l40"].end + 0.25, "white"),
            (tl.by_id["l44"].end + 0.3, "black2"), (tl.at("l47", "A") - 0.1, "l47b")]
    out = sorted(out)
    out.append((tl.total + 1, "end"))
    return out


_shots = {}


def draw(cr, t, tl):
    A_, Bb = tl.at, tl.by_id
    if id(tl) not in _shots:
        _shots[id(tl)] = shots(tl)
    sh = _shots[id(tl)]
    k = max(i for i, (at, _) in enumerate(sh) if at <= t or i == 0)
    s0, sid, s1 = sh[k][0], sh[k][1], sh[k + 1][0]
    crash = seg(t, Bb["l14"].start, Bb["l14"].end) if t < Bb["l21"].start else 1.0
    bal = BAL if t >= Bb["l16"].start else None

    cr.save()
    if sid in ("l1", "l2", "l3"):
        camera(cr, t, s0, s1, 1.0, 1.06)
        hud2d.blurred(cr, lambda c: B.trading_room(c, t, balance=BAL, crash=1.0), sigma=9)
        if sid == "l3":
            cr.set_source_rgba(0, 0, 0, 0.6)
            cr.paint()
            B.law_card(cr, t, 0.35, 1.0)
        else:
            one(cr, t, tl, "neil", "calm" if sid == "l1" else "focus", look=(0, 0.2), rim=BLUE, rim_from=(0, -10))
    elif sid in ("title", "partI", "partII", "partIII"):
        cr.set_source_rgba(0.02, 0.02, 0.03, 1)
        cr.paint()
        p = seg(t, s0, s0 + 0.5)
        if sid == "title":
            hud2d._text(cr, "THE BOY WHO", W / 2, H * 0.42, 70, (1, 1, 1, p), "Liberation Serif", "center")
            hud2d._text(cr, "INHERITED ANOTHER BODY", W / 2, H * 0.55, 70, (0.85, 0.75, 0.5, p), "Liberation Serif",
                        "center")
            hud2d._text(cr, "CHAPTER 1", W / 2, H * 0.68, 28, (1, 1, 1, 0.7 * p), "Liberation Mono", "center")
        else:
            roman, title = PARTS[{"partI": "l4", "partII": "l21", "partIII": "l30"}[sid]]
            B.chapter_card(cr, t, p, roman, title)
    elif sid in ("l4", "l5", "l6", "l7", "l11", "l12", "l13", "l15", "l17", "l20"):
        camera(cr, t, s0, s1, 1.02, 1.07)
        hud2d.blurred(cr, lambda c: B.trading_room(c, t, flash_walls=0.0, balance=bal, crash=crash), sigma=7)
        fx = "smile" if sid == "l20" else ("calm" if sid in ("l15", "l17") else "focus")
        one(cr, t, tl, "neil", fx, look=(0.1, -0.2 if sid != "l17" else 0.5), rim=BLUE, rim_from=(0, -10))
    elif sid in ("l8", "l9", "l10"):
        camera(cr, t, s0, s1, 1.0, 1.15, cx=W * 0.5, cy=H * 0.42)
        B.trading_room(cr, t, flash_walls=1.0)
    elif sid == "l14":
        camera(cr, t, s0, s1, 1.0, 1.15, cx=W * 0.2, cy=H * 0.42)
        B.trading_room(cr, t, crash=crash)
    elif sid == "l16":
        camera(cr, t, s0, s1, 1.0, 1.04)
        B.trading_room(cr, t, balance=BAL, crash=1.0)
    elif sid in ("l18", "l19"):
        camera(cr, t, s0, s1, 1.0, 1.04)
        hud2d.blurred(cr, lambda c: B.trading_room(c, t, balance=BAL, crash=1.0), sigma=12)
        msgs = [("You awake?", True, seg(t, Bb["l18"].start, Bb["l18"].end)),
                ("Always. Why are you?", False, seg(t, Bb["l19"].start, Bb["l19"].end))]
        B.phone_chat(cr, t, W / 2, H * 0.52, 0.95, msgs, typing=Bb["l18"].end < t < Bb["l19"].start)
    elif sid in ("l21", "l22", "l23", "l24", "l25", "l26", "l27"):
        camera(cr, t, s0, s1, 1.02, 1.06)
        hud2d.blurred(cr, lambda c: B.cafe(c, t, dusk=0.3), sigma=9)
        fn = "grin" if sid in ("l23", "l27") else "smile"
        fm = "laugh" if sid in ("l24", "l25") else "smile"
        two(cr, t, tl, "neil", "maya", fn, fm, outfit_a="jacket")
    elif sid == "l28":
        camera(cr, t, s0, s1, 1.0, 1.08, cy=H * 0.62)
        B.cafe(cr, t, cups=1.0, dusk=0.3)
    elif sid == "l29":
        camera(cr, t, s0, s1, 1.0, 1.08)
        cr.set_source_rgba(*B.hexa("#3a2a20"))
        cr.paint()
        B.receipt(cr, t, W / 2, H * 0.5, 1.1)
    elif sid in ("l30", "l31", "l32", "l33", "l34"):
        camera(cr, t, s0, s1, 1.0, 1.05)
        B.street(cr, t, "green" if sid == "l34" else "red", dusk=0.55)
        fm = "laugh" if sid in ("l33", "l34") else "smile"
        two(cr, t, tl, "neil", "maya", "smile" if sid != "l32" else "grin", fm, outfit_a="jacket")
    elif sid in ("l35", "l35b"):
        camera(cr, t, s0, s1, 1.02, 1.1, shake=1.3)
        hud2d.blurred(cr, lambda c: B.street(c, t, "green", car=0.2 if sid == "l35b" else 0.0, dusk=0.55), sigma=8)
        one(cr, t, tl, "neil", "focus", look=(-0.8, 0), outfit="jacket")
    elif sid in ("l36", "l37"):
        camera(cr, t, s0, s1, 1.0, 1.12, shake=1.0 if sid == "l37" else 2.0)
        cprog = 0.4 + 0.35 * seg(t, Bb["l36"].start, Bb["l38"].start)
        B.street(cr, t, "green", car=cprog, dusk=0.55)
        B.bust(cr, W * 0.62, H * 1.0, 0.8, t, "maya", "shock", look=(-0.8, 0), rim=HEAD, rim_from=(-10, 0))
    elif sid == "l38":
        camera(cr, t, s0, s1, 1.04, 1.16, shake=3.0)
        hud2d.blurred(cr, lambda c: B.street(c, t, "green", car=0.9, dusk=0.55), sigma=10)
        one(cr, t, tl, "neil", "fear", look=(-0.2, 0), outfit="jacket", rim=HEAD, rim_from=(-12, 0))
    elif sid == "l39":
        camera(cr, t, s0, s1, 1.0, 1.06, shake=2.0)
        hud2d.blurred(cr, lambda c: B.street(c, t, "green", car=0.95, dusk=0.55), sigma=8)
        B.bust(cr, W * 0.55, H * 1.02, 0.95, t, "maya", "shock", look=(-0.6, -0.3), rim=HEAD, rim_from=(-12, 0))
        S1.cup_spin(cr, t, s0, W * 0.1, H * 0.7, 0.8)
    elif sid == "l40":
        camera(cr, t, s0, s1, 1.0, 1.12, shake=1.2)
        B.street(cr, t, "green", car=1.0, dusk=0.55)
    elif sid == "white":
        cr.set_source_rgba(1, 0.98, 0.92, 1)
        cr.paint()
    elif sid in ("l41", "l42", "l44", "black2"):
        cr.set_source_rgba(0, 0, 0, 1)
        cr.paint()
        for j in range(40):
            a = 0.25 * (0.5 + 0.5 * math.sin(t * 0.8 + j)) * (sid != "black2")
            cr.set_source_rgba(0.6, 0.8, 1, a)
            cr.arc((j * 137.5) % W, ((j * 71.3) + t * 8) % H, 1.5, 0, 2 * math.pi)
            cr.fill()
    elif sid == "l43":
        camera(cr, t, s0, s1, 1.02, 1.1)
        hud2d.blurred(cr, lambda c: B.street(c, t, "red", dusk=0.7), sigma=9)
        one(cr, t, tl, "maya", "grief", look=(0, 0.6), tears=1.0)
        cr.set_source_rgba(0, 0, 0, 0.35)
        cr.paint()
    elif sid in ("l45", "l46", "l49", "l51", "l52", "l57", "l58", "l59", "l60", "l61", "l62"):
        z1 = 1.14 if sid in ("l58", "l59", "l62") else 1.06
        camera(cr, t, s0, s1, 1.02, z1, cy=H * 0.55)
        hud2d.blurred(cr, lambda c: B.hospital(c, t, window_view=0.4 if sid >= "l57" else 0.0), sigma=9)
        fx = {"l45": "fear", "l46": "fear", "l49": "worry", "l51": "fear", "l52": "shock", "l57": "focus",
              "l58": "worry", "l59": "shock", "l60": "worry", "l61": "grief", "l62": "grief"}[sid]
        B.bust(cr, W * 0.5, H * 0.95, 1.0, t, "arthur", fx, look=(0, -0.1), cannula=True, rim=COLD,
               rim_from=(10, -6), tremble=0.6, talk=1.0 if tl.speaking("old", t) else 0.0)
        if sid == "l45":
            cr.set_source_rgba(0, 0, 0, 1 - seg(t, s0, s0 + 1.2))
            cr.paint()
    elif sid in ("l47", "l47b"):
        camera(cr, t, s0, s1, 1.0, 1.08)
        hud2d.blurred(cr, lambda c: B.hospital(c, t), sigma=10)
        B.old_hand(cr, t, W / 2, H * 0.6, 1.25)
    elif sid == "l48":
        camera(cr, t, s0, s1, 1.02, 1.06)
        hud2d.blurred(cr, lambda c: B.hospital(c, t), sigma=9)
        one(cr, t, tl, "nurse", "worry", look=(0, 0.3))
    elif sid == "l50":
        camera(cr, t, s0, s1, 1.0, 1.1)
        hud2d.blurred(cr, lambda c: B.hospital(c, t), sigma=12)
        B.old_hand(cr, t, W / 2 + 120, H * 0.85, 1.0, tremble=0.6)
        B.wristband(cr, t, W / 2, H * 0.45, 1.0)
    elif sid in ("l53", "l54", "l55"):
        camera(cr, t, s0, s1, 1.0, 1.4 if sid == "l55" else 1.1, cx=W * 0.74, cy=H * 0.32)
        B.hospital(cr, t, window_view=0.0 if sid == "l53" else seg(t, Bb["l54"].start, Bb["l54"].start + 1.0) if
                   sid == "l54" else 1.0)
        if sid == "l53":                                        # the reflection in the dark glass: the old face
            cr.save()
            cr.rectangle(W * 0.52, H * 0.08, W * 0.44, H * 0.5)
            cr.clip()
            cr.push_group()
            B.bust(cr, W * 0.74, H * 0.62, 0.55, t, "arthur", "fear", look=(0, 0), cannula=True)
            cr.pop_group_to_source()
            cr.paint_with_alpha(0.5)
            cr.restore()
    elif sid == "l56":
        cr.set_source_rgba(0, 0, 0, 1)
        cr.paint()
    cr.restore()

    if sid not in ("white", "l41", "l42", "l44", "black2", "l56", "title", "partI", "partII", "partIII"):
        hud.finish(cr, t, flash_at=[], vig=0.45, grain=0.05)
    if sid == "l56":
        B.law_card(cr, t, seg(t, s0, s0 + 0.4), seg(t, s0 + 0.4, Bb["l56"].end))
    if sid == "l16":
        S1.big_number(cr, t, seg(t, Bb["l16"].start - 0.1, Bb["l16"].start + 0.4))
    hud2d.stamp(cr, t, A_("l29", "last") - 0.1, Bb["l29"].end + 0.3, ["THE LAST THING", "HE EVER BOUGHT"], y=H * 0.3,
                col=hud2d.YELLOW)
    hud2d.stamp(cr, t, A_("l55", "hundred") - 0.1, Bb["l55"].end + 0.5, ["~100 METRES"], y=H * 0.7)
    title_like = sid in ("title", "partI", "partII", "partIII", "l56")
    if t < Bb["l62"].start and not title_like:
        hud2d.captions(cr, t, tl, KEY, y=H * 0.93, size=40, max_w=W * 0.7)
    end_card(cr, t, Bb["l62"].start)
    cue("click", t, Bb["l12"].start - 0.15)
    cue("heartbeat", t, Bb["l34"].start, Bb["l38"].end - Bb["l34"].start)
    cue("brakes", t, Bb["l36"].end + 0.05)
    cue("sting", t, Bb["l40"].end + 0.25)
    cue("hum", t, Bb["l45"].start - 0.5, Bb["l50"].end - Bb["l45"].start)
    cue("heartbeat", t, Bb["l53"].start, Bb["l56"].end - Bb["l53"].start)
    cue("riser", t, Bb["l61"].start, Bb["l62"].start - Bb["l61"].start)


def end_card(cr, t, start):
    """WOULD YOU GO TO YOUR OWN FUNERAL? YES / NO; then the series title. Held over the tail."""
    if t < start:
        return
    k = clamp01((t - start) / 0.3)
    cr.set_source_rgba(0.02, 0.02, 0.04, 0.8 * k)
    cr.paint()
    hud2d._text(cr, "WOULD YOU GO TO YOUR OWN FUNERAL?", W / 2, H * 0.32, 54, (1, 1, 1, k), hud2d.ROUND, "center",
                shadow=0.5)
    for n, (lab, col) in enumerate((("YES", hud2d.GREEN), ("NO", hud2d.RED))):
        p = clamp01((t - start - 0.25 - 0.15 * n) / 0.25)
        if p <= 0:
            continue
        x = W / 2 + (-160 if n == 0 else 160)
        B.tk.tk_rrect(cr, x - 120, H * 0.45, 240, 110, 22)
        cr.set_source_rgba(0.06, 0.06, 0.08, p)
        cr.fill_preserve()
        cr.set_source_rgba(*col[:3], p)
        cr.set_line_width(6)
        cr.stroke()
        hud2d._text(cr, lab, x, H * 0.45 + 74, 56, (1, 1, 1, p), hud2d.ROUND, "center")
    p = clamp01((t - start - 0.7) / 0.3)
    if p > 0:
        hud2d._text(cr, "THE BOY WHO INHERITED ANOTHER BODY · CHAPTER 2 NEXT", W / 2, H * 0.84, 24,
                    (1, 1, 1, 0.8 * p), hud2d.ROUND, "center")
