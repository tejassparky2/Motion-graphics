"""Researchers found: lottery winners and happiness.

1978: Brickman, Coates & Janoff-Bulman, "Lottery winners and accident victims: Is happiness relative?" (J. Pers. Soc.
Psych. 36:917-927). 22 major Illinois lottery winners vs controls: present happiness 4.00 vs 3.82 (0-5 scale), and the
winners took less pleasure in everyday things (3.33 vs 3.82: talking with a friend, breakfast, a funny joke, a
compliment...). Small, one-off study.
2020: Lindqvist, Östling & Cesarini, Review of Economic Studies 87:2703-2726. Swedish lottery players surveyed 5-22 years
after a win: big winners had a lasting rise in life satisfaction (over a decade, not fading), with much smaller effects
on happiness and mood. Both are told, so the video doesn't overstate the 1978 result.
Structure follows the owner's "Napoleon was once asked" reference.
"""
import math

from motion.captions import captions
from motion.characters import money_pile, person, ticket
from motion.engine import INK, RED, WHITE, at, blob, cue, ease_out, hexc, lerp, line, pop, rrect_pts, seg, shape, \
    write
from motion.kit import camera, confetti, hl, stamp, whip

NARRATOR = dict()
TAIL = 0.8

SCRIPT = [
    dict(id="l1", scene="hook", text="Would winning the lottery make you happier? Almost everyone says yes. In "
                                     "[nineteen seventy-eight,|1978,] scientists checked."),
    dict(id="l2", scene="study", text="They found [twenty-two|22] people who had won big lottery prizes. And they compared "
                                      "them with ordinary people, who had won nothing."),
    dict(id="l3", scene="study", text="Everyone rated how happy they were, from zero to five."),
    dict(id="l4", scene="scores", text="The winners scored four. The ordinary people scored "
                                       "[three point eight.|3.8.] Almost the same."),
    dict(id="l5", scene="everyday", text="And there was a twist. The winners enjoyed everyday things less. Like "
                                         "breakfast. A funny joke. Or a compliment."),
    dict(id="l6", scene="treadmill", text="Scientists call it the hedonic treadmill. Whatever happens to us, we get "
                                          "used to it. And we drift back to where we started."),
    dict(id="l7", scene="twist", text="But in [twenty twenty,|2020,] a much bigger study followed people in Sweden, who "
                                      "had won the lottery, for up to [twenty|20] years."),
    dict(id="l8", scene="twist", text="Big winners were more satisfied with their lives, for over ten years. But their "
                                      "everyday mood barely changed."),
    dict(id="l9", scene="end", text="So what do you think? Would money make you happier? Or just more comfortable?",
         pace=0.95),
]

METADATA = dict(
    title="Lottery Winners Weren't Happier… Then a Bigger Study Found THIS 💰",
    alt_titles=["Does Winning the Lottery Make You Happy? Science Checked 🎟️",
                "The Hedonic Treadmill: Why Money Stops Feeling Good 💸"],
    description="""Would winning the lottery make you happier? In 1978, scientists checked. 🎟️

They compared 22 big lottery winners with ordinary people. On a 0-5 scale, the winners scored 4, the ordinary people 3.8: almost the same. And the winners enjoyed everyday things less, like breakfast, a joke or a compliment. Scientists call it the hedonic treadmill: we get used to whatever happens and drift back to where we started.

But in 2020, a much bigger study followed lottery winners in Sweden for up to 20 years. Big winners were more satisfied with their lives for over a decade, while their everyday mood barely changed. 💰

Studies: Brickman, Coates & Janoff-Bulman (1978), Journal of Personality and Social Psychology; Lindqvist, Östling & Cesarini (2020), Review of Economic Studies.

💬 So what do you think? Would money make you happier, or just more comfortable? 👇

🔔 Interestingly Strange: weird animals, bizarre history, mind-bending paradoxes and strange stories, hand-drawn in under a minute.""",
    hashtags=["#Psychology", "#Money", "#Happiness"],
    tags=["lottery winners happiness", "hedonic treadmill", "does money buy happiness", "psychology study",
          "lottery study", "money and happiness", "researchers found", "psychology facts", "science facts",
          "interestingly strange"],
    pinned_comment="Be honest: would a lottery win make YOU happier, or just more comfortable? 💰👇",
)

SKY, GROUND = hexc("#eaf1f8"), hexc("#cfd8e3")
GOLD = hexc("#ffd23f")
GREEN, GREEN_D = hexc("#2e9e52"), hexc("#1f7a3e")
BLUE = hexc("#3f6fb5")
PINK = hexc("#e0487a")
BASE = (1.5, 360, 800)
WINNERS = (("sam", 130), ("mia", 220), ("kid_b", 310))
NORMAL = (("kid_a", 420), ("rocker_a", 510), ("kid_d", 600))
GROUPS = (1.25, 365, 820)


def bg(cr, t, keys, color=SKY, dur=0.3):
    cr.set_source_rgba(*color)
    cr.paint()
    z, fx, fy = camera(t, keys, dur=dur)
    cr.translate(360, 640)
    cr.scale(z, z)
    cr.translate(-fx, -fy)
    shape(cr, [(-600, 960), (1400, 960), (1400, 2200), (-600, 2200)], GROUND, seed=1, amp=0.5, lw=4)


def card(cr, x, y, s, top, bottom, top_col=INK, bottom_col=RED, seed=50):
    with at(cr, x, y, s, rot=-0.03):
        shape(cr, rrect_pts(-230, -90, 460, 180, 18, 14), hexc("#fdf6e3"), seed=seed, amp=0.5, lw=5)
        write(cr, [(top, top_col)], 0, -14, 50, align="center", bold=True)
        write(cr, [(bottom, bottom_col)], 0, 56, 58, align="center", bold=True)


def bar(cr, x, base_y, value, vmax, h, col, label, shown, seed, w=110):
    hh = h * value / vmax
    shape(cr, rrect_pts(x - w / 2, base_y - hh, w, hh, 8, 10), col, seed=seed, amp=0.3, lw=4)
    write(cr, [(shown, INK)], x, base_y - hh - 14, 40, align="center", bold=True)
    write(cr, [(label, INK)], x, base_y + 40, 30, align="center", bold=True)


def scene_hook(cr, t, tl):
    A = tl.at
    keys = [(0, (1.7, 300, 800)), (A("l1", "almost"), BASE), (A("l1", "1978,"), (1.5, 360, 760))]
    bg(cr, t, keys)
    person(cr, "sam", 250, 960, t, facing=1, arms=("cheer", "cheer"), eyes="happy", mouth="grin", scale=1.15,
           jump=abs(math.sin(t * 7)) * 14)
    with at(cr, 250, 640, 1.0, rot=math.sin(t * 5) * 0.08):
        ticket(cr, 0, 0, 1.6, nums="07 13 21 34 42")
    confetti(cr, t, 0.0)
    money_pile(cr, 480, 955, 0.45)
    if t >= A("l1", "1978,"):
        card(cr, 500, 780, max(0.6, pop(t, A("l1", "1978,"), 0.3)) * 0.6, "SCIENTISTS", "CHECKED", seed=60)
    hl(cr, t, [("would it make you ", INK), ("HAPPIER", GREEN), ("?", INK)], 215, 56, 0.0, end=A("l1", "1978,") - 0.05,
       bold=True, sound=False)
    hl(cr, t, [("1978", RED), (": scientists checked", INK)], 215, 56, A("l1", "1978,"), bold=True)


def group(cr, t, who, mood="dot", mouth="smile", winners=False):
    for k, (c, x) in enumerate(who):
        person(cr, c, x, 960, t, facing=1 if x < 365 else -1, eyes=mood, mouth=mouth, scale=0.85)
        if winners:
            money_pile(cr, x + 28, 968, 0.18, seed=70 + k)


def scene_study(cr, t, tl):
    A = tl.at
    keys = [(A("l2") - 0.2, GROUPS), (A("l2", "22"), (1.55, 230, 820)), (A("l2", "ordinary"), (1.55, 500, 820)),
            (A("l3"), GROUPS)]
    bg(cr, t, keys)
    group(cr, t, WINNERS, "happy", "grin", winners=True)
    if t >= A("l2", "compared"):
        group(cr, t, NORMAL)
    for x, lab, col, st in ((220, "WINNERS", GREEN, A("l2", "22")), (510, "ORDINARY", BLUE, A("l2", "ordinary"))):
        if t >= st:
            with at(cr, x, 700, max(0.6, pop(t, st, 0.25)) * 0.75):
                shape(cr, rrect_pts(-110, -34, 220, 68, 30, 12), col, seed=80 + x, amp=0.3, lw=3.5)
                write(cr, [(lab, WHITE)], 0, 12, 34, align="center", bold=True)
    if t >= A("l3"):   # the 0-5 scale
        with at(cr, 365, 600, max(0.6, pop(t, A("l3"), 0.25)) * 0.9):
            shape(cr, rrect_pts(-260, -40, 520, 80, 20, 12), WHITE, seed=90, amp=0.3, lw=4)
            for k in range(6):
                write(cr, [(str(k), RED if k in (0, 5) else INK)], -210 + k * 84, 14, 40, align="center", bold=True)
    hl(cr, t, [("22", RED), (" big winners", INK)], 215, 66, A("l2", "22"), end=A("l2", "ordinary") - 0.05, bold=True)
    hl(cr, t, [("vs ", INK), ("ordinary", BLUE), (" people", INK)], 215, 66, A("l2", "ordinary"), end=A("l3") - 0.05,
       bold=True)
    hl(cr, t, [("happiness: ", INK), ("0 to 5", RED)], 215, 66, A("l3"), bold=True)


def scene_scores(cr, t, tl):
    A = tl.at
    keys = [(A("l4") - 0.2, (1.5, 360, 780)), (A("l4", "almost"), (1.6, 360, 760))]
    bg(cr, t, keys)
    gw = ease_out(seg(t, A("l4", "winners"), A("l4", "four.", end=True)))
    go = ease_out(seg(t, A("l4", "ordinary"), A("l4", "3.8.", end=True)))
    if gw > 0:
        bar(cr, 260, 860, 4.0 * gw, 5, 300, GREEN, "WINNERS", f"{4.0 * gw:.1f}", seed=100)
    if go > 0:
        bar(cr, 460, 860, 3.82 * go, 5, 300, BLUE, "ORDINARY", f"{3.8 * go:.1f}", seed=101)
    line(cr, [(160, 860), (560, 860)], 5, INK, seed=102, amp=0.2)
    if t >= A("l4", "almost"):
        stamp(cr, t, A("l4", "almost"), "ALMOST THE SAME", dur=0.9, y=330)
    hl(cr, t, [("winners ", GREEN), ("4.0", INK), ("  vs  ", INK), ("3.8", BLUE)], 215, 62, A("l4", "ordinary"),
       bold=True)


def breakfast(cr, x, y, s):
    with at(cr, x, y, s):
        blob(cr, 0, 10, 60, 26, WHITE, seed=110, amp=0.4, lw=4)
        blob(cr, 0, 0, 52, 14, hexc("#f2c14e"), seed=111, amp=0.4, lw=3)
        shape(cr, rrect_pts(70, -30, 44, 50, 8, 8), hexc("#c0504d"), seed=112, amp=0.3, lw=3.5)


def scene_everyday(cr, t, tl):
    A = tl.at
    keys = [(A("l5") - 0.2, BASE), (A("l5", "breakfast."), (1.5, 360, 760))]
    bg(cr, t, keys)
    person(cr, "sam", 200, 960, t, facing=1, arms=("hip", "hip"), eyes="dot", mouth="flat", scale=1.1)
    money_pile(cr, 110, 968, 0.25)
    items = []
    if t >= A("l5", "breakfast."):
        breakfast(cr, 470, 610, max(0.6, pop(t, A("l5", "breakfast."), 0.25)) * 1.1)
        items.append(A("l5", "breakfast."))
    if t >= A("l5", "joke."):
        with at(cr, 470, 730, max(0.6, pop(t, A("l5", "joke."), 0.25)) * 1.1):
            shape(cr, rrect_pts(-90, -36, 180, 72, 30, 12), WHITE, seed=120, amp=0.4, lw=4)
            write(cr, [("HA HA!", PINK)], 0, 14, 40, align="center", bold=True)
    if t >= A("l5", "compliment."):
        with at(cr, 470, 845, max(0.6, pop(t, A("l5", "compliment."), 0.25)) * 1.1):
            shape(cr, rrect_pts(-110, -36, 220, 72, 30, 12), WHITE, seed=121, amp=0.4, lw=4)
            write(cr, [("nice shirt!", BLUE)], 0, 14, 36, align="center", bold=True)
    # a little joy meter that stays low
    if t >= A("l5", "less."):
        with at(cr, 270, 640, 0.95):
            shape(cr, rrect_pts(-120, -26, 240, 52, 24, 12), WHITE, seed=130, amp=0.3, lw=3.5)
            shape(cr, rrect_pts(-114, -20, 228 * 0.45, 40, 20, 10), hexc("#e0483d"), seed=131, amp=0.2, lw=0,
                  stroke=None)
            write(cr, [("JOY", INK)], 0, 12, 30, align="center", bold=True)
    hl(cr, t, [("the twist: ", INK), ("LESS", RED), (" joy", INK)], 215, 62, A("l5", "less."), bold=True)


def treadmill(cr, t, x, y, s):
    with at(cr, x, y, s):
        shape(cr, [(-170, 0), (170, -16), (180, 14), (-170, 30)], hexc("#3c3f4a"), seed=140, amp=0.3, lw=4)
        for k in range(7):
            u = ((k / 7) + t * 0.8) % 1
            line(cr, [(-160 + u * 330, 4 - u * 14), (-150 + u * 330, 26 - u * 14)], 3, hexc("#8a8f9c"), seed=141 + k,
                 amp=0.1)
        line(cr, [(150, -14), (170, -170), (130, -190)], 7, hexc("#3c3f4a"), seed=150, amp=0.2)


def scene_treadmill(cr, t, tl):
    A = tl.at
    keys = [(A("l6") - 0.2, BASE), (A("l6", "drift"), (1.5, 360, 780))]
    bg(cr, t, keys)
    treadmill(cr, t, 330, 970, 1.0)
    person(cr, "sam", 320, 950, t, facing=1, walk=t * 1.6, eyes="dot", mouth="flat", scale=1.05)
    # the mood line: a spike up, then it drifts back to where it started
    with at(cr, 360, 600, 0.8 if t >= A("l6", "whatever") else 1e-3):
        shape(cr, rrect_pts(-280, -90, 560, 180, 16, 12), WHITE, seed=160, amp=0.3, lw=4)
        u = seg(t, A("l6", "whatever"), A("l6", "started.", end=True))
        pts = []
        for k in range(int(40 * u) + 1):
            xx = -250 + k * 12.5
            spike = 70 * math.exp(-((k - 8) / 5) ** 2) if k >= 4 else 0
            pts.append((xx, 40 - spike))
        if len(pts) > 1:
            line(cr, pts, 6, GREEN, seed=161, amp=0.2)
        line(cr, [(-250, 40), (250, 40)], 2, hexc("#9aa0a8"), seed=162, amp=0.1)
    if t < A("l6", "whatever"):
        card(cr, 360, 600, max(0.6, pop(t, A("l6", "hedonic"), 0.3)) * 0.7, "HEDONIC", "TREADMILL", seed=170)
    hl(cr, t, [("we ", INK), ("get used", RED), (" to it", INK)], 215, 66, A("l6", "used"), end=A("l6", "drift") - 0.05,
       bold=True)
    hl(cr, t, [("back to ", INK), ("where we started", BLUE)], 215, 54, A("l6", "drift"), bold=True)


def sweden(cr, x, y, s):
    with at(cr, x, y, s):
        shape(cr, rrect_pts(-90, -60, 180, 120, 6, 10), hexc("#2c6eb5"), seed=180, amp=0.2, lw=4)
        shape(cr, rrect_pts(-50, -60, 28, 120, 2, 8), hexc("#f4c430"), seed=181, amp=0.1, lw=0, stroke=None)
        shape(cr, rrect_pts(-90, -14, 180, 28, 2, 8), hexc("#f4c430"), seed=182, amp=0.1, lw=0, stroke=None)


def meter(cr, x, y, label, level, col, s=0.8):
    with at(cr, x, y, s):
        shape(cr, rrect_pts(-150, -70, 300, 140, 18, 12), WHITE, seed=190 + int(x), amp=0.3, lw=4)
        write(cr, [(label, INK)], 0, -26, 30, align="center", bold=True)
        shape(cr, rrect_pts(-120, 0, 240, 36, 16, 10), hexc("#e6e9ee"), seed=191 + int(x), amp=0.2, lw=3)
        if level > 0.02:
            shape(cr, rrect_pts(-120, 0, 240 * level, 36, 16, 10), col, seed=192 + int(x), amp=0.2, lw=0, stroke=None)


def scene_twist(cr, t, tl):
    A = tl.at
    keys = [(A("l7") - 0.2, BASE), (A("l8", "satisfied"), (1.5, 360, 760)), (A("l8", "mood"), (1.5, 360, 760))]
    bg(cr, t, keys)
    if t < A("l8"):
        card(cr, 360, 640, max(0.6, pop(t, A("l7", "2020,"), 0.3)) * 0.7, "BIGGER STUDY", "2020", seed=200)
        if t >= A("l7", "sweden,"):
            sweden(cr, 360, 830, max(0.6, pop(t, A("l7", "sweden,"), 0.25)) * 0.9)
    else:
        up = ease_out(seg(t, A("l8", "satisfied"), A("l8", "years.", end=True)))
        meter(cr, 360, 610, "LIFE SATISFACTION", 0.5 + 0.35 * up, GREEN, s=1.15)
        if t >= A("l8", "mood"):
            meter(cr, 360, 820, "EVERYDAY MOOD", 0.52, BLUE, s=1.15)
    hl(cr, t, [("a much ", INK), ("BIGGER", RED), (" study", INK)], 215, 62, A("l7"), end=A("l8") - 0.05, bold=True)
    hl(cr, t, [("life satisfaction ", INK), ("UP", GREEN)], 215, 58, A("l8", "satisfied"), end=A("l8", "mood") - 0.05,
       bold=True)
    hl(cr, t, [("mood: ", INK), ("barely changed", BLUE)], 215, 58, A("l8", "mood"), bold=True)


def scene_end(cr, t, tl):
    A = tl.at
    keys = [(A("l9") - 0.2, BASE), (A("l9", "happier?"), (1.6, 300, 800)), (A("l9", "comfortable?"), BASE)]
    bg(cr, t, keys)
    person(cr, "sam", 260, 960, t, facing=1, arms=("chin", "hold"), eyes="sly", mouth="smirk", scale=1.15)
    with at(cr, 250, 650, 1.0):
        ticket(cr, 0, 0, 1.2)
    money_pile(cr, 480, 955, 0.4)
    for k, (lab, col, x) in enumerate((("HAPPIER", GREEN, 220), ("COMFORTABLE", BLUE, 500))):
        if t >= A("l9", "comfortable?"):
            with at(cr, x, 1060, max(0.6, pop(t, A("l9", "comfortable?") + k * 0.12, 0.25)) * 0.65):
                shape(cr, rrect_pts(-160, -46, 320, 92, 46, 14), col, seed=210 + k, amp=0.3, lw=4)
                write(cr, [(lab, WHITE)], 0, 16, 44, align="center", bold=True)
    hl(cr, t, [("happier... or just ", INK), ("comfortable", BLUE), ("?", INK)], 215, 50, A("l9", "happier?"),
       bold=True, underline=True)
    stamp(cr, t, A("l9", "comfortable?", end=True), "COMMENT BELOW!", dur=0.8, y=330)


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    {"hook": scene_hook, "study": scene_study, "scores": scene_scores, "everyday": scene_everyday,
     "treadmill": scene_treadmill, "twist": scene_twist, "end": scene_end}[name](cr, t, tl)
    cr.restore()
    captions(cr, t, tl)
