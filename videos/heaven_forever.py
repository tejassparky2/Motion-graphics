"""Big question: "Would Forever Get Boring?" -- a boy and his sister on the roof at night; he does the maths on
forever, in the polished look. Original story.

Script: out/scripts_big_questions_batch2.md, video 5 (owner approved 25 Oct 2026). Bernard Williams, "The Makropulos
Case: Reflections on the Tedium of Immortality" (1973, in Problems of the Self): an endless life would eventually
become unbearably boring. The reply about pleasures that don't wear out: John Martin Fischer, "Why Immortality Is Not
So Bad" (1994). About living forever, not about any one religion; nobody's belief is mocked. Turbo stock female
narrator with tags; the boy and his sister through Turbo with Kokoro reference voices (no tags on them).
"""
import math

from motion import thriller as th
from motion import voice
from motion.engine import W, H, cue, hexc, lerp, seg
from motion.kit import whip
from motion.pkit import BLUE, GOLD, GREEN, PURPLE, RED, buttons, card, sparkles, studio, tag
from motion.polish import (OUTLINE, WHITE, alpha, appear, bold_text, camera, captions, ellipse, enter, lin, paint,
                           rad, rrect, shade, sign, smooth, soft_disc, stamp, stroke_line, vignette)
from motion.timeline import clear_dialogue
from motion.toons import head
from videos.bq_kit import heart_shape, moon, night_sky, talker

NARRATOR = dict(turbo=True)
TAIL = 0.5
TWIST = "h6"          # music drops out on Williams' answer (research 18 Oct 2026, A5)
SERIES = "Big Questions"
END_TAG = "Subscribe · a new question tomorrow"      # alternate videos test the silent subscribe wording (research E4/E5)
voice.SPEAKERS.update({"boy": dict(voice="am_puck", speed=1.04, pitch=2.5, turbo_ref="am_puck+3"),
                       "sis": dict(voice="af_heart", speed=1.0, turbo_ref="af_heart")})
BOY = dict(skin="tan", shirt=hexc("#4a8ad0"), tie=None, pants=hexc("#2f3550"))
SIS = dict(skin="tan", hair="pony", hair_col=hexc("#2b1a12"), shirt=hexc("#b07ad8"), tie=None,
           pants=hexc("#2f3550"), build="kid")

SCRIPT = [
    dict(id="h1", scene="roof", text="When we die, we go to heaven forever, right?", speaker="boy"),
    dict(id="h2", scene="roof", text="That's what they say. Forever.", speaker="sis"),
    dict(id="h3", scene="roof", text="Like, a billion years?", speaker="boy"),
    dict(id="h4", scene="roof", text="And then a billion more. And it never ends.", speaker="sis"),
    dict(id="h5", scene="song", text="The boy goes quiet. He just pictured his favourite song. On repeat. For a billion "
                                     "years. [gasp]"),
    dict(id="h6", scene="williams", text="Philosopher Bernard Williams argued this in [nineteen seventy three.|1973.] "
                                         "Live forever, and everything eventually gets boring.", gap=0.4),
    dict(id="h7", scene="joys", text="Others disagree. Some joys never wear out. Food when you're hungry. Sleep when "
                                     "you're tired. A hug."),
    dict(id="h8", scene="shuffle", text="So heaven would need new songs.", speaker="boy"),
    dict(id="h9", scene="shuffle", text="Or a really good shuffle button.", speaker="sis"),
    dict(id="h10", scene="end", text="So, would forever be paradise, or the most boring thing ever?", gap=0.3),
]
clear_dialogue(SCRIPT, ids={"h1", "h2", "h3", "h4"}, pace=0.97, turn_gap=0.32)

METADATA = dict(
    title="Heaven Is Forever. Then the Boy Did the Math ♾️",
    alt_titles=["Would Forever Get Boring? ♾️", "A Billion Years of Your Favourite Song ♾️"],
    description="""A boy and his sister on the roof, under the stars. "When we die, we go to heaven forever, right? Like, a billion years?" "And then a billion more. And it never ends." ♾️

He just pictured his favourite song. On repeat. For a billion years.

Philosopher Bernard Williams argued in 1973 that if you live forever, everything eventually gets boring. Others disagree: some joys never wear out. Food when you're hungry. Sleep when you're tired. A hug.

So heaven would need new songs... or a really good shuffle button.

An original story. Sources: Bernard Williams, "The Makropulos Case: Reflections on the Tedium of Immortality" (1973); John Martin Fischer, "Why Immortality Is Not So Bad" (1994).

💬 Would forever be paradise, or the most boring thing ever? 👇

🔔 Interestingly Strange: mind-bending questions, clever twists and The Last Bencher, animated in under a minute.""",
    hashtags=["#BigQuestions", "#Philosophy", "#Shorts"],
    tags=["would heaven be boring", "living forever", "immortality boring", "bernard williams", "forever",
          "philosophy", "deep questions", "brother and sister", "big questions", "interestingly strange"],
    pinned_comment="PARADISE or BORING? What's the one thing you'd never get tired of? 👇",
)


# ---------------------------------------------------------------- props
def skyline(cr):
    for k, (bx, bw, bh) in enumerate([(-20, 140, 230), (110, 120, 330), (225, 160, 260), (380, 130, 380),
                                       (505, 120, 280), (620, 130, 340)]):
        rrect(cr, bx, 820 - bh, bw, bh, 4)
        paint(cr, hexc("#141836"), None, 0)
        for wy in range(int(820 - bh + 24), 800, 48):
            for wx in range(int(bx + 16), int(bx + bw - 24), 36):
                if (k * 5 + wx // 36 + wy // 48) % 5 == 0:
                    rrect(cr, wx, wy, 16, 22, 2)
                    paint(cr, hexc("#ffd98a"), None, 0)


def parapet(cr):
    rrect(cr, -20, 1014, W + 40, 300, 6)
    paint(cr, lin(0, 1014, 0, H, [(0, hexc("#5a5a78")), (1, hexc("#33334a"))]), OUTLINE, 6)
    rrect(cr, -20, 1000, W + 40, 34, 6)
    paint(cr, hexc("#6e6e8e"), OUTLINE, 5)


def shooting_star(cr, t, start, dur=0.9):
    u = seg(t, start, start + dur)
    if not 0 < u < 1:
        return
    x, y = lerp(120, 560, u), lerp(160, 330, u)
    stroke_line(cr, [(x - 120, y - 46), (x, y)], 4, (1, 1, 0.9, 0.6 * (1 - u)), curve=False)
    soft_disc(cr, x, y, 16, (1, 1, 0.9, 0.9))


def roof(cr, t):
    night_sky(cr, t)
    moon(cr, 560, 200, 54)
    skyline(cr)


def boy(cr, t, tl, x=245, y=1250, s=1.45, **kw):
    talker(cr, t, tl, "boy", "kid", x, y, s, rest="smile", **dict(BOY, **kw))


def sis(cr, t, tl, x=490, y=1250, s=1.5, **kw):
    talker(cr, t, tl, "sis", "student1", x, y, s, rest="smile", **dict(SIS, **kw))


def kids_on_roof(cr, t, tl, boy_kw=None, sis_kw=None):
    boy(cr, t, tl, **(boy_kw or {}))
    sis(cr, t, tl, **(sis_kw or {}))
    parapet(cr)


def years_counter(cr, t, start, x, y, rate=0.0, size=74):
    """1,000,000,000 that keeps rolling up after it lands (`rate` years per second)."""
    if t < start:
        return
    u = min(1.0, (t - start) / 0.8)
    v = int(1_000_000_000 * u + max(0.0, t - start - 0.8) ** 1.6 * rate)
    k = appear(t, start, 0.3)
    cr.save()
    cr.translate(x, y)
    cr.scale(k, k)
    bold_text(cr, f"{v:,}", 0, 0, size, GOLD)
    bold_text(cr, "YEARS", 0, size * 0.7, size * 0.42, WHITE)
    cr.restore()


def song_bubble(cr, t, start, x, y, plays):
    k = appear(t, start, 0.35)
    if k <= 0.01:
        return
    cr.save()
    cr.translate(x, y)
    cr.scale(k, k)
    for r, dy in ((16, 170), (26, 130)):
        ellipse(cr, -90, dy, r, r)
        paint(cr, WHITE, OUTLINE, 4)
    rrect(cr, -230, -110, 460, 220, 60)
    paint(cr, WHITE, OUTLINE, 6)
    cr.arc(-120, 0, 50, math.pi, 2 * math.pi)                      # headphones
    cr.set_source_rgba(*OUTLINE)
    cr.set_line_width(10)
    cr.stroke()
    for side in (-1, 1):
        rrect(cr, -120 + side * 50 - 14, -6, 28, 46, 10)
        paint(cr, RED, OUTLINE, 4)
    bold_text(cr, "FAV SONG", 60, -30, 40, OUTLINE, outline=None, shadow=0)
    bold_text(cr, f"PLAY #{plays:,}", 60, 30, 34, RED, outline=None, shadow=0)
    a0 = t * 4                                                     # the repeat arrow spinning
    cr.arc(60, 75, 18, a0, a0 + 5.0)
    cr.set_line_width(5)
    cr.stroke()
    cr.restore()


def shuffle_button(cr, t, start, x, y, r=110):
    k = appear(t, start, 0.45)
    if k <= 0.01:
        return
    soft_disc(cr, x, y, r * 2.2, (0.4, 0.8, 1, 0.3 + 0.1 * math.sin(t * 5)))
    cr.save()
    cr.translate(x, y)
    cr.scale(k, k)
    ellipse(cr, 0, 0, r, r)
    paint(cr, rad(-20, -30, r * 1.2, [(0, hexc("#7ad8ff")), (1, hexc("#2a7ad8"))]), OUTLINE, 6)
    for flip in (1, -1):                                            # two crossing arrows
        stroke_line(cr, [(-50, -24 * flip), (-10, -24 * flip), (20, 24 * flip), (50, 24 * flip)], 10, WHITE,
                    curve=False)
        cr.move_to(62, 24 * flip)
        cr.line_to(42, 10 * flip)
        cr.line_to(42, 38 * flip)
        cr.close_path()
        paint(cr, WHITE, None, 0)
    cr.restore()


# ---------------------------------------------------------------- scenes
def scene_roof(cr, t, tl):
    A = tl.at
    roof(cr, t)
    shooting_star(cr, t, 0.3)
    cr.save()
    enter(cr, camera(t, [(0, (1.0, 360, 640)), (A("h3"), (1.08, 360, 700))], dur=0.8))
    kids_on_roof(cr, t, tl, dict(eyes="open", look=(0.2, -0.8), arms=("down", "down")),
                 dict(eyes="half", look=(0.0, -0.8), arms=("down", "down")))
    cr.restore()
    years_counter(cr, t, A("h3", "billion"), 360, 290, rate=0.0 if t < A("h4") else 9e8)
    if t >= A("h4", "never"):
        tag(cr, t, A("h4", "never"), 360, 430, "IT NEVER ENDS", col=PURPLE, size=44)
    vignette(cr, 0.4)


def scene_song(cr, t, tl):
    A = tl.at
    roof(cr, t)
    cr.save()
    enter(cr, camera(t, [(tl.scene_at(t)[1], (1.2, 290, 690))], dur=0.6))
    kids_on_roof(cr, t, tl, dict(eyes="wide" if t >= A("h5", "billion") else "half", mouth="o" if t >= A("h5",
                 "billion") else "flat", look=(0.0, -0.4), arms=("down", "down")),
                 dict(eyes="half", mouth="smile", look=(-0.6, -0.4), arms=("down", "down")))
    cr.restore()
    plays = int(1 + max(0.0, t - A("h5", "favourite")) ** 3 * 4000)
    if t >= A("h5", "favourite"):
        song_bubble(cr, t, A("h5", "favourite"), 400, 330, plays)
    vignette(cr, 0.4)


def scene_williams(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#1e1a38"), hexc("#3a2f60"), seed=81)
    card(cr, t, tl.scene_at(t)[1], 360, 300, 480, 230, "BERNARD WILLIAMS · 1973", ["FOREVER =", "BORING"], col=PURPLE,
         title_size=32, line_size=56)
    if t >= A("h6", "Live"):
        tag(cr, t, A("h6", "Live"), 360, 470, "EVEN PARADISE?", col=GOLD, size=48)
    yawn = 0.5 + 0.5 * math.sin((t - tl.scene_at(t)[1]) * 1.8)          # a bored face, yawning on a loop
    head(cr, t, 360, 700, 120, "kid", eyes="half" if yawn < 0.7 else "closed", mouth="o" if yawn > 0.5 else "flat",
         **dict(BOY, tie=None))
    for k in range(3):
        zt = ((t * 0.6 + k / 3) % 1.0)
        bold_text(cr, "z", 470 + 40 * zt + 14 * k, 620 - 160 * zt, 30 + 26 * zt, alpha(WHITE, 1 - zt), outline=None,
                  shadow=0)
    vignette(cr, 0.45)


def icon_plate(cr, x, y):
    ellipse(cr, x, y, 70, 26)
    paint(cr, WHITE, OUTLINE, 5)
    ellipse(cr, x, y - 10, 40, 18)
    paint(cr, hexc("#f0b060"), OUTLINE, 4)


def icon_pillow(cr, x, y):
    rrect(cr, x - 70, y - 34, 140, 68, 30)
    paint(cr, hexc("#cfe2ff"), OUTLINE, 5)
    bold_text(cr, "z z", x + 40, y - 50, 34, BLUE, outline=None, shadow=0)


def scene_joys(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#ffd8e0"), hexc("#fff0d8"), seed=82)
    sign(cr, t, tl.scene_at(t)[1], 360, 200, "SOME JOYS NEVER WEAR OUT", col=GREEN, size=42)
    for k, (key, label, fn) in enumerate((("Food", "FOOD", icon_plate), ("Sleep", "SLEEP", icon_pillow),
                                          ("hug", "A HUG", None))):
        st = A("h7", key)
        if t < st:
            continue
        x, y = 360, 400 + k * 190
        sc = 1.6 * appear(t, st, 0.35)
        cr.save()
        cr.translate(x - 120, y)
        cr.scale(sc, sc)
        cr.translate(-(x - 120), -y)
        if fn:
            fn(cr, x - 120, y)
        else:
            heart_shape(cr, x - 120, y, 0.9, hexc("#ff7a9a"))
        cr.restore()
        bold_text(cr, label, x + 100, y + 18, 60, OUTLINE, outline=None, shadow=0)
    vignette(cr, 0.3)


def scene_shuffle(cr, t, tl):
    A = tl.at
    roof(cr, t)
    cr.save()
    enter(cr, camera(t, [(tl.scene_at(t)[1], (1.08, 360, 700))]))
    kids_on_roof(cr, t, tl, dict(eyes="half", look=(0.5, 0.0), arms=("think", "down")),
                 dict(eyes="happy", look=(-0.5, 0.0), arms=("down", "point") if t >= A("h9") else ("down", "down")))
    cr.restore()
    if t >= A("h9", "shuffle"):
        shuffle_button(cr, t, A("h9", "shuffle"), 360, 330)
        sparkles(cr, t, A("h9", "shuffle"), 360, 330, n=8, seed=83, col=WHITE, spread=150)
    vignette(cr, 0.4)


def scene_end(cr, t, tl):
    A = tl.at
    roof(cr, t)
    cr.save()
    enter(cr, camera(t, [(A("h10"), (1.03, 360, 680))]))
    kids_on_roof(cr, t, None, dict(eyes="half", mouth="smile", look=(0.2, -0.8)),
                 dict(eyes="happy", mouth="smile", look=(-0.2, -0.8)))
    cr.restore()
    sign(cr, t, A("h10", "paradise"), 360, 220, "PARADISE, OR BORING?", col=GOLD, size=50)
    buttons(cr, t, A("h10", "paradise"), [("PARADISE", GREEN), ("BORING", RED)], y=350, size=48)
    vignette(cr, 0.35)


SCENES = {"roof": scene_roof, "song": scene_song, "williams": scene_williams, "joys": scene_joys,
          "shuffle": scene_shuffle, "end": scene_end}


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    SCENES[name](cr, t, tl)
    cr.restore()
    th.hook(cr, t, [("WOULD FOREVER", False), ("GET BORING?", True)], end=tl.at("h3"), y=190, size=86)
    captions(cr, t, tl)
