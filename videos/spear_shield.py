"""The Spear and the Shield (矛盾, maodun) -- Pinocchio-style paradox in the polished look.

Han Feizi, chapter "Difficulties" (Nan Yi), 3rd century BC: a man of Chu boasted that nothing could pierce his
shield and that his spear could pierce anything; asked what happens if the spear strikes the shield, he could not
answer. 矛 (mao, spear) + 盾 (dun, shield) = 矛盾 (maodun), the everyday Chinese word for "contradiction".
Sources: The China Story yearbook 2021 ("Contradiction and the Stubborn Bystander"); Han Feizi text.
Script approved by the owner on 9 Oct 2026 (out/scripts_paradox_batch2.md) with an everyday example, a clever
closing question and character voices added at the owner's request.
"""
import math
import random

from motion import voice
from motion.engine import W, H, cue, ease_out, hexc, lerp, seg
from motion.kit import whip
from motion.pkit import (BLUE, GOLD, GREEN, INKC, PURPLE, RED, bubble, buttons, calendar, card, hanzi, knot, red_x,
                         shake, sparkles, studio, tag)
from motion.polish import (OUTLINE, WHITE, alpha, appear, bold_text, camera, captions, ellipse, enter, ground_shadow,
                           light_rays, lin, paint, put, rad, rrect, shade, sign, smooth, soft_disc, soft_rrect, sprite,
                           stamp, stroke_line, vignette)
from motion.toons import head, person

NARRATOR = dict(speed=0.93)
TAIL = 0.9
voice.SPEAKERS.update({"seller": dict(voice="am_eric", speed=1.1, pitch=1.0),
                       "kid": dict(voice="af_nicole", speed=1.05, pitch=3.0)})

SCRIPT = [
    dict(id="s1", scene="hook", text="One salesman's lie became a word that over a billion people still use."),
    dict(id="s2", scene="shield", text="Ancient China. A man is selling a shield. Nothing can pierce my shield!",
         speaker="seller", speaker_from="Nothing"),
    dict(id="s3", scene="spear", text="Then he holds up a spear. My spear can pierce anything!", speaker="seller",
         speaker_from="My"),
    dict(id="s4", scene="ask", text="Someone in the crowd asks. What if your spear hits your shield?",
         speaker="kid", speaker_from="What", gap=0.35),
    dict(id="s5", scene="silent", text="The salesman has no answer.", gap=0.45, pace=0.92),
    dict(id="s6", scene="clash", text="If the spear goes through, the shield wasn't unbreakable."),
    dict(id="s7", scene="clash", text="If the shield stops it, the spear wasn't unstoppable."),
    dict(id="s8", scene="clash", text="Both things can't be true.", pace=0.95),
    dict(id="s9", scene="example", text="Today it would be an ad saying: this phone case can't break. And this hammer "
                                        "breaks everything."),
    dict(id="s10", scene="word", text="In Chinese, spear is [mao.|máo.] Shield is [dun.|dùn.] Together, [mao "
                                      "dun.|máodùn.]", pace=0.95),
    dict(id="s11", scene="word", text="And that's still the Chinese word for contradiction."),
    dict(id="s12", scene="book", text="The story comes from a book by Han Fei, written over two thousand years ago."),
    dict(id="s13", scene="end", text="So which one was the lie? The spear, or the shield?", gap=0.3, pace=0.95),
]

METADATA = dict(
    title="One Salesman's Lie Became the Chinese Word for \"Contradiction\" 🛡️",
    alt_titles=["The Unstoppable Spear vs the Unbreakable Shield 🛡️ (2,000-Year-Old Paradox)",
                "What If This Spear Hits This Shield? 🤯"],
    description="""One salesman's lie became a word that over a billion people still use. 🛡️

Ancient China: a man is selling a shield. "Nothing can pierce my shield!" Then he holds up a spear: "My spear can pierce anything!"
Someone in the crowd asks: "What if your spear hits your shield?" The salesman has no answer.

If the spear goes through, the shield wasn't unbreakable. If the shield stops it, the spear wasn't unstoppable. Both things can't be true. (Today it'd be an ad saying "this phone case can't break" and "this hammer breaks everything".)

In Chinese, spear is 矛 (máo) and shield is 盾 (dùn). Together, 矛盾 (máodùn), and that's still the Chinese word for contradiction.

Source: the Han Feizi (chapter "Difficulties"), by Han Fei, 3rd century BC.

💬 So which one was the lie: the spear, or the shield? 👇

🔔 Interestingly Strange: mind-bending paradoxes, weird animals, bizarre history and strange stories, animated in under a minute.""",
    hashtags=["#Paradox", "#China", "#Shorts"],
    tags=["spear and shield", "maodun", "chinese word for contradiction", "han feizi", "unstoppable force immovable object",
          "paradox", "logic", "chinese history", "word origins", "interestingly strange"],
    pinned_comment="Spear or shield: which one was lying? 🛡️⚔️ Defend your answer 👇",
)

LANTERN = hexc("#e8473f")


# ---------------------------------------------------------------- backgrounds and props
def _market(c):
    c.rectangle(0, 0, W, H)
    c.set_source(lin(0, 0, 0, 760, [(0, hexc("#ffb27a")), (0.6, hexc("#ffdcae")), (1, hexc("#fff0d0"))]))
    c.fill()
    for k, (col, y0, amp) in enumerate(((hexc("#c9a0b8"), 470, 110), (hexc("#a8889e"), 540, 80))):  # mountains
        c.move_to(0, 760)
        for x in range(0, W + 41, 40):
            c.line_to(x, y0 - amp * abs(math.sin(x / (170.0 + 40 * k) + k)))
        c.line_to(W, 760)
        c.close_path()
        c.set_source_rgba(*col)
        c.fill()
    for x0, w in ((-40, 300), (420, 340)):     # stall roofs with curved eaves
        c.move_to(x0 - 30, 390)
        c.curve_to(x0 + 20, 380, x0 + w * 0.3, 300, x0 + w / 2, 280)
        c.curve_to(x0 + w * 0.7, 300, x0 + w - 20, 380, x0 + w + 30, 390)
        c.close_path()
        paint(c, lin(0, 280, 0, 390, [(0, hexc("#5a6a8a")), (1, hexc("#3a4458"))]), OUTLINE, 5)
        c.rectangle(x0 + 10, 390, w - 20, 380)
        c.set_source(lin(0, 390, 0, 770, [(0, hexc("#c98a4a")), (1, hexc("#8a5a2e"))]))
        c.fill()
        for px in (x0 + 20, x0 + w - 40):
            rrect(c, px, 390, 20, 380, 4)
            paint(c, hexc("#a8402e"), OUTLINE, 3)
    c.rectangle(0, 770, W, H - 770)
    c.set_source(lin(0, 770, 0, H, [(0, hexc("#e0c08a")), (1, hexc("#b8945a"))]))
    c.fill()
    for k in range(10):
        c.rectangle(0, 790 + k * k * 5, W, 2)
        c.set_source_rgba(0.4, 0.3, 0.2, 0.15)
        c.fill()


def market(cr, t):
    put(cr, sprite("market_bg", W, H, _market), 0, 0)
    for k, x in enumerate((70, 210, 470, 640)):     # swinging lanterns
        sw = math.sin(t * 1.5 + k) * 0.08
        cr.save()
        cr.translate(x, 395)
        cr.rotate(sw)
        stroke_line(cr, [(0, 0), (0, 40)], 3, OUTLINE, curve=False)
        soft_disc(cr, 0, 80, 70, (1, 0.5, 0.3, 0.25))
        ellipse(cr, 0, 80, 34, 42)
        paint(cr, rad(-8, 66, 50, [(0, hexc("#ff8a6a")), (1, LANTERN)]), OUTLINE, 4)
        for yy in (44, 116):
            rrect(cr, -14, yy - 4, 28, 10, 3)
            paint(cr, GOLD, OUTLINE, 2.5)
        cr.restore()


def shield(cr, x, y, s=1.0, crack=0.0, rot=0.0):
    cr.save()
    cr.translate(x, y)
    cr.rotate(rot)
    cr.scale(s, s)
    soft_disc(cr, 0, 10, 100, (0, 0, 0, 0.3))
    cr.arc(0, 0, 92, 0, 2 * math.pi)
    paint(cr, lin(-90, -90, 90, 90, [(0, hexc("#fff0a8")), (0.4, GOLD), (1, hexc("#9a6a14"))]), OUTLINE, 6)
    cr.arc(0, 0, 70, 0, 2 * math.pi)
    paint(cr, rad(-20, -25, 90, [(0, hexc("#ff6a5a")), (1, hexc("#8a1a1a"))]), OUTLINE, 5)
    for k in range(8):       # a swirl of gold studs
        a = k * math.pi / 4 + 0.4
        cr.arc(math.cos(a) * 52, math.sin(a) * 52, 7, 0, 2 * math.pi)
        paint(cr, GOLD, OUTLINE, 2.5)
    cr.arc(0, 0, 22, 0, 2 * math.pi)
    paint(cr, rad(-6, -6, 26, [(0, WHITE), (1, GOLD)]), OUTLINE, 4)
    if crack > 0:
        pts = [(0, 0), (20 * crack, -30 * crack), (10 * crack, -60 * crack), (40 * crack, -85 * crack)]
        stroke_line(cr, pts, 6, OUTLINE, curve=False)
        stroke_line(cr, [(0, 0), (-35 * crack, 25 * crack), (-70 * crack, 30 * crack)], 6, OUTLINE, curve=False)
    ellipse(cr, -35, -45, 24, 10, -0.6)
    paint(cr, alpha(WHITE, 0.6), None, 0)
    cr.restore()


def spear(cr, x, y, ang=-1.3, length=380, s=1.0, bend=0.0):
    """A spear held at (x, y) (the grip), pointing at angle `ang`."""
    cr.save()
    cr.translate(x, y)
    cr.rotate(ang)
    cr.scale(s, s)
    stroke_line(cr, [(-120, 0), (length, 0)], 16, OUTLINE, curve=False)
    stroke_line(cr, [(-120, 0), (length, 0)], 9, hexc("#a8763a"), curve=False)
    cr.save()
    cr.translate(length, 0)
    cr.rotate(bend)
    for k in range(4):      # red tassel
        stroke_line(cr, [(-6, 0), (-30, -14 + k * 9)], 5, LANTERN)
    cr.move_to(0, -18)
    cr.line_to(70, 0)
    cr.line_to(0, 18)
    cr.close_path()
    paint(cr, lin(0, -18, 0, 18, [(0, WHITE), (0.5, hexc("#cfd5df")), (1, hexc("#8a94a8"))]), OUTLINE, 4.5)
    cr.restore()
    cr.restore()


def seller(cr, t, tl, x, y, s, arms, eyes="happy", mouth_rest="grin", hold=None, hold_back=None, **kw):
    person(cr, t, x, y, s, "seller", eyes=eyes, mouth="talk" if tl.speaking("seller", t) else mouth_rest, arms=arms,
           hold=hold, hold_back=hold_back, **kw)


def crate(cr, x, y, w=260):
    rrect(cr, x - w / 2, y - 90, w, 90, 8)
    paint(cr, lin(0, y - 90, 0, y, [(0, hexc("#c99460")), (1, hexc("#8a5a2e"))]), OUTLINE, 5)
    for k in range(1, 4):
        stroke_line(cr, [(x - w / 2 + k * w / 4, y - 88), (x - w / 2 + k * w / 4, y - 2)], 3, alpha(OUTLINE, 0.4),
                    curve=False)


def crowd(cr, t, seed=5, mood="open", n=5):
    rng = random.Random(seed)
    for k in range(n):
        x = 60 + k * 150 + rng.uniform(-20, 20)
        who = rng.choice(["villager", "teacher", "reporter"])
        kw = dict(glasses=False, fedora=None, suit=None, beard=None, shirt=rng.choice(
            [hexc("#4a8ad0"), hexc("#3fae6a"), hexc("#c86a8a"), hexc("#c9a46a")]), hair="topknot",
            hair_col=hexc("#1e130d"), skin=rng.choice(["light", "olive", "tan"]))
        head(cr, t, x, 1060 + math.sin(t * 2 + k) * 4, 70, who, eyes="wide" if mood == "wow" else "open",
             mouth="o" if mood == "wow" else "smile", **kw)


# ---------------------------------------------------------------- scenes
def scene_hook(cr, t, tl):
    A = tl.at
    market(cr, t)
    cr.save()
    enter(cr, camera(t, [(0, (1.0, 360, 640)), (A("s1", "billion"), (1.1, 360, 610))], dur=0.8))
    crate(cr, 360, 900, 280)
    seller(cr, t, tl, 360, 815, 0.88, ("hold", "hold"), mouth_rest="grin",
           hold=lambda c, hx, hy: spear(c, hx, hy, -1.35, 320, 0.9),
           hold_back=lambda c, hx, hy: shield(c, hx - 10, hy, 0.75))
    cr.restore()
    sign(cr, t, A("s1", "lie"), 360, 150, "ONE LIE...", col=RED, size=70, end=A("s1", "word") - 0.05)
    sign(cr, t, A("s1", "word"), 360, 150, "...ONE WORD", col=GOLD, size=70, end=A("s1", "billion") - 0.05)
    sign(cr, t, A("s1", "billion"), 360, 150, "1 BILLION+ USE IT", col=GREEN, size=60)
    vignette(cr, 0.4)


def scene_shield(cr, t, tl):
    A = tl.at
    market(cr, t)
    bang = A("s2", "Nothing")
    cr.save()
    enter(cr, camera(t, [(A("s2") - 0.3, (1.15, 360, 600)), (bang, (1.35, 380, 560))], dur=0.5))
    crate(cr, 360, 900, 280)
    knock = (math.sin((t - bang) * 18) * 0.3) if bang <= t < bang + 0.8 else 0.0
    seller(cr, t, tl, 360, 815, 0.9, ("fist", "hold"), mouth_rest="grin",
           hold_back=lambda c, hx, hy: shield(c, hx - 10, hy - 10, 0.95, rot=knock))
    cr.restore()
    if t >= bang:
        cue("hit", t, bang + 0.1)
        sparkles(cr, t, bang + 0.1, 300, 520, n=8, seed=4, col=GOLD)
    sign(cr, t, A("s2", "Ancient"), 360, 140, "ANCIENT CHINA", col=RED, size=60, end=bang - 0.05)
    sign(cr, t, A("s2", "pierce"), 360, 140, "UNBREAKABLE SHIELD", col=GOLD, size=52)
    vignette(cr, 0.4)


def scene_spear(cr, t, tl):
    A = tl.at
    market(cr, t)
    up = A("s3", "holds")
    cr.save()
    enter(cr, camera(t, [(A("s3") - 0.3, (1.15, 360, 600)), (A("s3", "My"), (1.3, 380, 520))], dur=0.5))
    crate(cr, 360, 900, 280)
    raise_ = ease_out(seg(t, up, up + 0.5))
    seller(cr, t, tl, 360, 815, 0.9, ("up" if raise_ > 0.5 else "hold", "hold"), mouth_rest="grin",
           hold=lambda c, hx, hy: spear(c, hx, hy, lerp(-0.4, -1.45, raise_), 340, 0.95),
           hold_back=lambda c, hx, hy: shield(c, hx - 10, hy, 0.7))
    cr.restore()
    sparkles(cr, t, A("s3", "pierce"), 420, 180, n=7, seed=6, col=WHITE)
    sign(cr, t, A("s3", "pierce"), 360, 140, "PIERCES ANYTHING", col=BLUE, size=56)
    vignette(cr, 0.4)


def scene_ask(cr, t, tl):
    A = tl.at
    market(cr, t)
    q = A("s4", "What")
    cr.save()
    enter(cr, camera(t, [(A("s4") - 0.3, (1.0, 360, 640)), (q, (1.15, 300, 640))], dur=0.5))
    crate(cr, 500, 900, 260)
    seller(cr, t, tl, 500, 815, 0.8, ("hold", "hold"), eyes="open", mouth_rest="smile",
           hold=lambda c, hx, hy: spear(c, hx, hy, -1.35, 300, 0.85),
           hold_back=lambda c, hx, hy: shield(c, hx - 10, hy, 0.65), facing=-1)
    person(cr, t, 160, 930, 0.85, "crowdkid", eyes="half" if t >= q else "open",
           mouth="talk" if tl.speaking("kid", t) else "smug", arms=("point", "hips") if t >= q else ("down", "down"),
           brows="raise" if t >= q else None)
    cr.restore()
    crowd(cr, t, mood="wow" if t >= A("s4", "shield?") else "open")
    bubble(cr, t, q, 330, 200, "WHAT IF YOUR SPEAR", size=44, tail=-1)
    bubble(cr, t, A("s4", "hits"), 330, 300, "HITS YOUR SHIELD?", size=48, tail=0, col=hexc("#fff3c4"))
    vignette(cr, 0.4)


def scene_silent(cr, t, tl):
    A = tl.at
    market(cr, t)
    cr.save()
    enter(cr, camera(t, [(A("s5") - 0.3, (1.3, 380, 560)), (A("s5", "answer."), (1.55, 380, 520))], dur=1.0))
    crate(cr, 360, 900, 280)
    person(cr, t, 360, 815, 0.9, "seller", eyes="wide", mouth="flat", brows="up", arms=("hold", "hold"), sweat=True,
           bob=False, hold=lambda c, hx, hy: spear(c, hx, hy, -1.35, 320, 0.9),
           hold_back=lambda c, hx, hy: shield(c, hx - 10, hy, 0.75))
    cr.restore()
    bubble(cr, t, A("s5", "no"), 520, 220, "...", size=70, tail=-1)
    sign(cr, t, A("s5", "answer."), 360, 120, "NO ANSWER", col=hexc("#5a6478"), size=64)
    vignette(cr, 0.5)


def scene_clash(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#ffd6a8"), hexc("#fff1d6"), seed=3)
    s6, s7, s8 = A("s6"), A("s7"), A("s8")
    if t < s8:
        path_a = t < s7
        st = s6 if path_a else s7
        fly = ease_out(seg(t, st + 0.1, st + 0.6))
        hit = fly >= 1
        sx = lerp(-200, 260, fly)
        if path_a:
            shield(cr, 470, 520, 1.5, crack=1.0 if hit else 0.0)
            spear(cr, sx + (60 if hit else 0), 520, 0.0, 300, 1.0)
        else:
            shield(cr, 470, 520, 1.5)
            spear(cr, sx - (40 if hit else 0), 520, 0.0, 300, 1.0, bend=0.5 if hit else 0.0)
        if hit:
            cue("hit", t, st + 0.6)
            sparkles(cr, t, st + 0.6, 360, 520, n=9, seed=7 if path_a else 8, col=GOLD)
        sign(cr, t, st, 360, 160, "SPEAR GOES THROUGH?" if path_a else "SHIELD STOPS IT?", col=BLUE if path_a else
             GOLD, size=50)
        stamp(cr, t, A("s6", "unbreakable.") if path_a else A("s7", "unstoppable."), 360, 830,
              "THE SHIELD LIED" if path_a else "THE SPEAR LIED", col=RED, size=62)
    else:
        knot(cr, t, s8, 360, 480, 160, RED)
        shield(cr, 300, 480, 0.6)
        spear(cr, 340, 520, -0.6, 160, 0.6)
        sign(cr, t, s8, 360, 160, "CAN'T BOTH BE TRUE", col=PURPLE, size=56)
    vignette(cr, 0.35)


def phone_case(cr, x, y, s=1.0):
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    rrect(cr, -70, -130, 140, 260, 26)
    paint(cr, lin(-70, 0, 70, 0, [(0, hexc("#5a6a8a")), (1, hexc("#2b3448"))]), OUTLINE, 6)
    rrect(cr, -54, -112, 108, 224, 16)
    paint(cr, lin(0, -112, 0, 112, [(0, hexc("#9fd8ff")), (1, hexc("#4a6ad0"))]), OUTLINE, 3)
    for k in range(3):
        sx = -30 + k * 30
        stroke_line(cr, [(sx, -80), (sx + 18, -60)], 5, alpha(WHITE, 0.6), curve=False)
    cr.restore()


def hammer(cr, x, y, s=1.0, rot=0.0):
    cr.save()
    cr.translate(x, y)
    cr.rotate(rot)
    cr.scale(s, s)
    rrect(cr, -14, -40, 28, 230, 10)
    paint(cr, lin(-14, 0, 14, 0, [(0, hexc("#e8473f")), (1, hexc("#a8262a"))]), OUTLINE, 5)
    rrect(cr, -90, -100, 180, 70, 14)
    paint(cr, lin(0, -100, 0, -30, [(0, hexc("#dfe6ee")), (1, hexc("#7a8494"))]), OUTLINE, 6)
    cr.restore()


def scene_example(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#9fd8ff"), hexc("#e8f0ff"), seed=9)
    case_t, ham_t = A("s9", "phone"), A("s9", "hammer")
    soft_rrect(cr, 40, 230, 640, 600, 30, (0, 0, 0, 0.3), sigma=14)     # a billboard / ad frame
    rrect(cr, 40, 220, 640, 600, 30)
    paint(cr, lin(0, 220, 0, 820, [(0, WHITE), (1, hexc("#eef2fa"))]), OUTLINE, 7)
    bold_text(cr, "MEGA SALE", 360, 300, 56, RED)
    if t >= case_t:
        phone_case(cr, 210, 560, appear(t, case_t, 0.4) * 1.0 + 0.01)
        bold_text(cr, "CAN'T BREAK!", 210, 760, 40, BLUE)
    if t >= ham_t:
        sw = math.sin(t * 6) * 0.25
        hammer(cr, 510, 540, appear(t, ham_t, 0.4) * 1.0 + 0.01, rot=sw)
        bold_text(cr, "BREAKS ALL!", 510, 760, 40, RED)
    sign(cr, t, A("s9"), 360, 120, "TODAY IT WOULD BE...", col=PURPLE, size=50)
    if t >= A("s9", "everything.", end=True):
        bold_text(cr, "?!", 360, 560, 120, GOLD)
    vignette(cr, 0.35)


def scene_word(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#ffe0c8"), hexc("#fff4e4"), seed=2)
    s11 = A("s11")
    together = A("s10", "Together,")
    if t < together:
        hanzi(cr, t, A("s10", "spear"), 200, 380, "矛", 190, RED, sub="máo = SPEAR")
        hanzi(cr, t, A("s10", "Shield"), 520, 380, "盾", 190, hexc("#c9900c"), sub="dùn = SHIELD")
        if t >= A("s10", "spear"):
            spear(cr, 130, 700, -0.3, 160, 0.7)
        if t >= A("s10", "Shield"):
            shield(cr, 520, 700, 0.6)
    else:
        u = ease_out(seg(t, together, together + 0.5))
        hanzi(cr, t, together, lerp(200, 250, u), 400, "矛", 190, RED)
        hanzi(cr, t, together, lerp(520, 470, u), 400, "盾", 190, hexc("#c9900c"))
        bold_text(cr, "máodùn", 360, 640, 70, WHITE, font="Fredoka")
        stamp(cr, t, A("s11", "contradiction."), 360, 790, "= CONTRADICTION", col=PURPLE, size=60, rot=-0.05)
    sign(cr, t, A("s10"), 360, 130, "IN CHINESE", col=RED, size=62, end=s11 - 0.05)
    sign(cr, t, A("s11", "still"), 360, 130, "STILL USED TODAY", col=GREEN, size=56)
    vignette(cr, 0.35)


def bamboo_book(cr, t, x, y, s=1.0):
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    soft_rrect(cr, -230, -150, 460, 300, 20, (0, 0, 0, 0.3), sigma=12)
    for k in range(11):       # bamboo slips tied together
        sx = -220 + k * 40
        rrect(cr, sx, -160, 34, 300, 8)
        paint(cr, lin(sx, 0, sx + 34, 0, [(0, hexc("#e8d08a")), (0.5, hexc("#f4e4a8")), (1, hexc("#c9a85a"))]),
              OUTLINE, 3.5)
        for j in range(5):
            stroke_line(cr, [(sx + 10, -130 + j * 50), (sx + 24, -126 + j * 50)], 4, alpha(OUTLINE, 0.55),
                        curve=False)
    for yy in (-100, 90):
        stroke_line(cr, [(-226, yy), (226, yy)], 5, hexc("#8a3a2a"), curve=False)
    cr.restore()


def scene_book(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#e8d8b8"), hexc("#fff4e4"), seed=6)
    k = appear(t, A("s12"), 0.5)
    bamboo_book(cr, t, 360, 480, max(k, 0.01))
    tag(cr, t, A("s12", "Han"), 360, 250, "HAN FEI", col=RED)
    calendar(cr, t, A("s12", "two"), 360, 760, "WRITTEN IN THE", "3RD C. BC", col=hexc("#8a3a2a"))
    vignette(cr, 0.35)


def scene_end(cr, t, tl):
    A = tl.at
    market(cr, t)
    cr.save()
    enter(cr, (1.0, 360, 640))
    crate(cr, 360, 920, 280)
    person(cr, t, 360, 835, 0.85, "seller", eyes="half", mouth="smug", arms=("hold", "hold"),
           hold=lambda c, hx, hy: spear(c, hx, hy, -1.35, 300, 0.85),
           hold_back=lambda c, hx, hy: shield(c, hx - 10, hy, 0.7))
    cr.restore()
    sign(cr, t, A("s13"), 360, 140, "WHICH ONE LIED?", col=PURPLE, size=60)
    buttons(cr, t, A("s13", "spear,"), [("SPEAR", BLUE), ("SHIELD", GOLD)], y=290)
    vignette(cr, 0.4)


SCENES = {"hook": scene_hook, "shield": scene_shield, "spear": scene_spear, "ask": scene_ask, "silent": scene_silent,
          "clash": scene_clash, "example": scene_example, "word": scene_word, "book": scene_book, "end": scene_end}


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    SCENES[name](cr, t, tl)
    cr.restore()
    captions(cr, t, tl)
