"""THE BOY WHO INHERITED ANOTHER BODY, Short 2: "The Last Position" (9:16). Auto-approved by the owner, 27 Oct 2026.
Scenes from the approved reconstructed Chapter 1, part III (channels/stories/boy_who_inherited_ch1.md), and the law
the owner fixed: he can only reincarnate into the nearest and weakest body.

The push (canon: he dies protecting Maya), his last position, the quiet; he wakes heavy and old, the spotted hand with
a gold ring, the nurse ("Mr. Vance"), the wristband (VANCE, ARTHUR. AGE 82), Maya kneeling at the crossing about a
hundred metres below; the law; Arthur's fortune, family and enemies (plot point 6), now Neil's. Ends on the hook into
Part 3: "And soon, they would bury Neil." (plot point 7, his own funeral)

    /home/user/.venv-main/bin/python channels/horror/make_2d.py boy_s2   -> out/stories/boy_s2.mp4
"""
import math
import os

from motion import audio, satsuei, voice
from motion.engine import W, H, cue, seg

from channels.horror import hud, hud2d, sound  # noqa: F401
from channels.horror.toon2d import INK, glow, grade, noise
from channels.stories import boy_anime, boy_art, serial

B = boy_art if os.environ.get("ANIME") == "0" else boy_anime     # ANIME=0: the old vector look

NARRATOR = dict(turbo=True, turbo_ref="bm_george")
TAIL = 2.0
MUSIC = "horror"
TWIST = "e13"
voice.SPEAKERS.update({
    "maya": dict(voice="af_nova", turbo_ref="af_nova"),
    "nurse": dict(voice="af_sarah", turbo_ref="af_sarah"),
})
audio.GAINS.update(sting=0.55, brakes=0.7)

SCRIPT = [
    dict(id="e1", scene="push", text="Neil had half a second. He didn't think. He moved."),
    dict(id="e2", scene="push", text="He shoved Maya out of the way. She landed on the far kerb. Safe.", gap=0.3),
    dict(id="e3", scene="push", text="Neil's last position was the middle of the crossing.", gap=0.8),
    dict(id="e4", scene="quiet", text="It didn't hurt. There was a sound, and the sky turning over. Then a quiet, like "
                                      "the market after the closing bell.", gap=1.0),
    dict(id="e5", scene="quiet", text="Neil!", speaker="maya", gap=0.6),
    dict(id="e6", scene="wake", text="Neil opened his eyes. And his body was wrong.", gap=1.4),
    dict(id="e7", scene="wake", text="Heavy. Old. A machine beeping beside him."),
    dict(id="e8", scene="hand", text="The hand in front of his face was spotted, and shaking. There was a gold ring "
                                     "on it."),
    dict(id="e9", scene="nurse", text="Mister Vance? Don't try to sit up.", speaker="nurse", gap=0.4),
    dict(id="e10", scene="band", text="The wristband said: Vance, Arthur. Age [eighty-two.|82.]"),
    dict(id="e11", scene="window", text="Through the window, far below: blue lights. And Maya, kneeling at the "
                                        "crossing."),
    dict(id="e12", scene="window", text="About a hundred metres away.", gap=0.6),
    dict(id="e13", scene="law", text="The law gave him no choice. The nearest body. And the weakest.", gap=0.6),
    dict(id="e14", scene="arthur", text="Neil wasn't dead. He was an [eighty-two-year-old|82-year-old] billionaire, "
                                        "in a body that was failing."),
    dict(id="e15", scene="arthur", text="Arthur Vance had money. He had a family. And he had enemies.", gap=0.4),
    dict(id="e16", scene="arthur", text="Now, Neil had all of it.", gap=0.6),
    dict(id="e17", scene="arthur", text="And soon, they would bury Neil.", gap=0.3),
]

METADATA = dict(
    title="He Died at 17. He Woke Up as an 82-Year-Old Billionaire. ⏳",
    alt_titles=["The Nearest. The Weakest. He Didn't Get to Choose. ⏳",
                "The Boy Who Inherited Another Body, Part 2 ⏳"],
    description="""Neil had half a second. He shoved Maya out of the way. Then he opened his eyes in a hospital bed, with an old man's hands and a wristband that said VANCE, ARTHUR. AGE 82. ⏳

About a hundred metres away, Maya was kneeling at the crossing.

The Boy Who Inherited Another Body, Part 2.
Arthur Vance had money, a family and enemies. Now, Neil had all of it. And soon, they would bury Neil.

(Original story. Fiction. Anime-style animation.)""",
    hashtags=["#Thriller", "#Story", "#Shorts"],
    tags=["the boy who inherited another body", "reincarnation", "body swap", "billionaire", "thriller",
          "psychological thriller", "story", "plot twist", "2d animation", "part 2"],
    pinned_comment="Part 3 is next. Would you go to your own funeral, if Maya would be there and couldn't know it "
                   "was you?",
)

KEY = {"half", "moved", "shoved", "safe", "last", "crossing", "quiet", "wrong", "heavy", "old", "ring", "vance",
       "eighty-two", "maya", "hundred", "nearest", "weakest", "billionaire", "failing", "money", "family", "enemies", "bury"}


def camera(cr, t, s0, s1, z0=1.0, z1=1.06, cx=W / 2, cy=H / 2, shake=1.0):
    k = seg(t, s0, s1)
    z = z0 + (z1 - z0) * k
    cr.translate(cx + 4 * shake * noise(t * 0.7, 1), cy + 3 * shake * noise(t * 0.6, 4))
    cr.rotate(0.004 * shake * noise(t * 0.5, 7))
    cr.scale(z, z)
    cr.translate(-cx, -cy)


def shots(tl):
    A_, Bb = tl.at, tl.by_id
    return [
        (0.0, "headlights"), (A_("e1", "He", nth=2) - 0.05, "neil_move"), (Bb["e2"].start - 0.1, "maya_kerb"),
        (A_("e2", "Safe.") - 0.1, "cup"), (Bb["e3"].start - 0.1, "crossing_empty"), (Bb["e3"].end + 0.2, "white"),
        (Bb["e4"].start - 0.1, "black"), (Bb["e5"].start - 0.1, "maya_cry"), (Bb["e6"].start - 1.0, "ceiling"),
        (A_("e6", "And") - 0.1, "arthur_wake"), (Bb["e7"].start - 0.1, "monitor"), (Bb["e8"].start - 0.1, "hand"),
        (Bb["e9"].start - 0.15, "nurse"), (Bb["e10"].start - 0.1, "band"), (Bb["e11"].start - 0.15, "window"),
        (Bb["e12"].start - 0.1, "window_close"), (Bb["e13"].start - 0.15, "law"), (Bb["e14"].start - 0.15, "arthur"),
        (Bb["e16"].start - 0.1, "arthur_close"), (Bb["e17"].start - 0.1, "question"), (tl.total + 1, "end")]


_shots = {}


def draw(cr, t, tl):
    A_, Bb = tl.at, tl.by_id
    if id(tl) not in _shots:
        _shots[id(tl)] = shots(tl)
    sh = _shots[id(tl)]
    k = max(i for i, (at, _) in enumerate(sh) if at <= t or i == 0)
    s0, name, s1 = sh[k][0], sh[k][1], sh[k + 1][0]
    by = 940
    head_light = (1, 0.97, 0.85, 0.9)
    cold = (0.75, 0.85, 1, 0.6)

    cr.save()
    if name == "headlights":
        camera(cr, t, s0, s1, 1.0, 1.1, shake=2.0)
        hud2d.blurred(cr, lambda c: B.street(c, t, "green", car=0.85, dusk=0.55), sigma=6)
        B.bust(cr, W / 2, by + 60, 1.2, t, "neil", "focus", look=(-0.8, 0), outfit="jacket", rim=head_light,
               rim_from=(-12, 0))
    elif name == "neil_move":
        camera(cr, t, s0, s1, 1.04, 1.16, shake=3.0)
        hud2d.blurred(cr, lambda c: B.street(c, t, "green", car=0.92, dusk=0.55), sigma=10)
        B.bust(cr, W / 2 + 40 * seg(t, s0, s1), by + 60, 1.25, t, "neil", "fear", look=(-0.2, 0), outfit="jacket",
               rim=head_light, rim_from=(-12, 0))
    elif name == "maya_kerb":
        camera(cr, t, s0, s1, 1.0, 1.06, shake=2.0)
        hud2d.blurred(cr, lambda c: B.street(c, t, "green", car=0.95, dusk=0.55), sigma=8)
        B.bust(cr, W / 2, by + 140, 1.1, t, "maya", "shock", look=(-0.6, -0.3), rim=head_light, rim_from=(-12, 0))
    elif name == "cup":
        camera(cr, t, s0, s1, 1.0, 1.04)
        B.street(cr, t, "green", car=0.0, dusk=0.6)
        from channels.stories.boy_s1 import cup_spin
        cup_spin(cr, t, s0, W * 0.3, H * 0.75, 1.1)
    elif name == "crossing_empty":
        camera(cr, t, s0, s1, 1.0, 1.12, shake=1.2)
        B.street(cr, t, "green", car=1.0, dusk=0.55)
    elif name == "white":
        cr.set_source_rgba(1, 0.98, 0.92, 1)
        cr.paint()
    elif name == "black":
        cr.set_source_rgba(0, 0, 0, 1)
        cr.paint()
        for j in range(40):                                    # the quiet: a few drifting specks, like closing prices
            a = 0.25 * (0.5 + 0.5 * math.sin(t * 0.8 + j))
            cr.set_source_rgba(0.6, 0.8, 1, a)
            cr.arc((j * 137.5) % W, ((j * 71.3) + t * 8) % H, 1.5, 0, 2 * math.pi)
            cr.fill()
    elif name == "maya_cry":
        camera(cr, t, s0, s1, 1.02, 1.1)
        hud2d.blurred(cr, lambda c: B.street(c, t, "red", dusk=0.7, blue=0.0), sigma=9)
        B.bust(cr, W / 2, by + 60, 1.2, t, "maya", "grief", look=(0, 0.6), tears=1.0,
               talk=1.0 if tl.speaking("maya", t) else 0.0)
        cr.set_source_rgba(0, 0, 0, 0.35)
        cr.paint()
    elif name == "ceiling":
        cr.set_source_rgba(*B.hexa("#cfd6da"))
        cr.paint()
        for k2 in range(5):
            B.toon(cr, lambda c, k2=k2: c.rectangle(W * 0.2, H * (0.15 + k2 * 0.18), W * 0.6, 18), B.hexa("#eef3f5"),
                   None, (0, 0), None, lw=2)
        cr.set_source_rgba(0, 0, 0, 1 - seg(t, s0, s0 + 1.2))     # eyes opening
        cr.paint()
    elif name in ("arthur_wake", "arthur", "arthur_close"):
        z1 = 1.18 if name == "arthur_close" else 1.08
        camera(cr, t, s0, s1, 1.02, z1, cy=H * 0.55)
        hud2d.blurred(cr, lambda c: B.hospital(c, t, window_view=0.4), sigma=9)
        fx = "fear" if name == "arthur_wake" else ("shock" if name == "arthur" else "worry")
        B.bust(cr, W / 2, by + 60, 1.25, t, "arthur", fx, look=(0, -0.1), cannula=True, rim=cold, rim_from=(10, -6),
               tremble=0.6)
    elif name == "monitor":
        camera(cr, t, s0, s1, 1.0, 1.12, cx=W * 0.78, cy=H * 0.5)
        B.hospital(cr, t, window_view=0.0)
    elif name == "hand":
        camera(cr, t, s0, s1, 1.0, 1.08)
        hud2d.blurred(cr, lambda c: B.hospital(c, t), sigma=10)
        B.old_hand(cr, t, W / 2, H * 0.62, 2.0)
    elif name == "nurse":
        camera(cr, t, s0, s1, 1.02, 1.08)
        hud2d.blurred(cr, lambda c: B.hospital(c, t), sigma=9)
        B.bust(cr, W / 2, by + 40, 1.15, t, "nurse", "worry", look=(0, 0.3),
               talk=1.0 if tl.speaking("nurse", t) else 0.0)
    elif name == "band":
        camera(cr, t, s0, s1, 1.0, 1.1)
        hud2d.blurred(cr, lambda c: B.hospital(c, t), sigma=12)
        B.old_hand(cr, t, W / 2 + 60, H * 0.8, 1.6, tremble=0.6)
        B.wristband(cr, t, W / 2, H * 0.5, 1.2)
    elif name in ("window", "window_close"):
        camera(cr, t, s0, s1, 1.0, 1.4 if name == "window_close" else 1.1, cx=W * 0.5, cy=H * 0.25)
        B.hospital(cr, t, window_view=seg(t, Bb["e11"].start, Bb["e11"].start + 1.0) if name == "window" else 1.0)
    elif name == "law":
        cr.set_source_rgba(0, 0, 0, 1)
        cr.paint()
    elif name == "question":
        camera(cr, t, s0, s1, 1.0, 1.1, cy=H * 0.55)
        hud2d.blurred(cr, lambda c: B.hospital(c, t, window_view=1.0), sigma=12)
        B.bust(cr, W / 2, by + 60, 1.25, t, "arthur", "grief", look=(0.4, -0.4), cannula=True, rim=cold,
               rim_from=(10, -6), tremble=0.5)
    cr.restore()

    if name not in ("white", "black", "law"):
        if B is boy_anime:                                      # satsuei: glow, light, aberration, grain
            satsuei.apply(cr, t, glow=0.25, shade=((0.5, 0.3), (0.35, 0.3, 0.45), 0.3), ca=1.0, grain=0.03)
            hud.finish(cr, t, flash_at=[], vig=0.5, grain=0.0)
        else:
            hud.finish(cr, t, flash_at=[], vig=0.5, grain=0.05)
    if name == "law":
        B.law_card(cr, t, seg(t, s0, s0 + 0.4), seg(t, s0 + 0.4, Bb["e13"].end))
    hud2d.hook(cr, t, [("HALF A SECOND.", False), ("HE DIDN'T THINK.", True)], end=Bb["e1"].end + 0.05, y=230,
               size=70)
    hud2d.stamp(cr, t, A_("e12", "hundred") - 0.1, Bb["e12"].end + 0.4, ["~100 METRES"], y=760)
    if t < Bb["e17"].end + 0.1 and name not in ("law",):
        hud2d.captions(cr, t, tl, KEY, y=1010)
    serial.next_card(cr, t, Bb["e17"].end + 0.1, "THE BOY WHO INHERITED ANOTHER BODY", "PART 3")
    cue("brakes", t, 0.0)
    cue("sting", t, Bb["e3"].end + 0.2)                       # the impact, in the silence after "crossing"
    cue("hum", t, Bb["e6"].start - 0.5, Bb["e9"].end - Bb["e6"].start)
    cue("heartbeat", t, Bb["e10"].start, Bb["e13"].end - Bb["e10"].start)
    cue("riser", t, Bb["e16"].start, Bb["e17"].start - Bb["e16"].start)
