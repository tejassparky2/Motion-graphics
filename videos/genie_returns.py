"""The Genie Is Back -- genie-style story #4, a sequel to genie_wish (out/scripts_genie_style_batch1.md, approved by
the owner on 14 Oct 2026). New rule: the wish only comes true if the genie can't guess it first. The kid's folded
wish: "I wish the genie guesses my wish." Original story; narrated by ElevenLabs Chris. Same genie, lamp and desert
as the first video, so viewers recognise them.
"""
import math

from motion import voice
from motion.engine import W, H, cue, ease_out, hexc, lerp, seg
from motion.kit import whip
from motion.pkit import BLUE, GOLD, GREEN, INKC, PINK, PURPLE, RED, bubble, buttons, card, shake, sparkles, tag
from motion.polish import (OUTLINE, WHITE, alpha, appear, bold_text, camera, captions, enter, lin, paint, particles,
                           rrect, shade, sign, smooth, soft_disc, stamp, stroke_line, vignette)
from motion.rulekit import either_way, mouth, note
from motion.toons import person
from videos.genie_wish import CHOC, bar, choc_mountain, desert, genie, lamp

NARRATOR = dict(engine="elevenlabs")
TAIL = 0.9
voice.SPEAKERS.clear()      # genie_wish's Kokoro cast is replaced by ElevenLabs voices
voice.SPEAKERS.update({
    "genie": dict(el=voice.ELEVEN["callum"], tone="smug"),
    "kid": dict(el=voice.ELEVEN["liam"], pitch=2.5, tone="confidently"),
})

SCRIPT = [
    dict(id="g1", scene="back", text="The genie is back. And this time, his rules are tighter.", tone="dramatic"),
    dict(id="g2", scene="rules", text="One wish. No tricks. And your wish only comes true if I can't guess it first.",
         speaker="genie", gap=0.3),
    dict(id="g3", scene="write", text="So the kid writes his wish on a paper, and folds it.", gap=0.3),
    dict(id="g4", scene="guess", text="Chocolate again?", speaker="genie", gap=0.35),
    dict(id="g5", scene="guess", text="Nope.", speaker="kid", gap=0.35),
    dict(id="g6", scene="open", text="The kid opens the paper. It says: I wish the genie guesses my wish.",
         gap=0.3, tone="mischievously"),
    dict(id="g7", scene="freeze", text="The genie freezes. Again.", gap=0.45, pace=0.92, tone="amused"),
    dict(id="g8", scene="logic", text="He didn't guess it. So the wish comes true. But the wish says he guessed it."),
    dict(id="g9", scene="logic", text="And if he guessed it, the wish can't come true."),
    dict(id="g10", scene="logic", text="Either way, the genie loses. Again.", pace=0.95, tone="amused"),
    dict(id="g11", scene="shop", text="So the genie quit. He sells chocolate now.", gap=0.3, tone="amused"),
    dict(id="g12", scene="end", text="Round three: genie, or kid?", gap=0.3, pace=0.95, tone="excited"),
]

METADATA = dict(
    title="The Genie Came Back With New Rules 🧞 (Kid Wins Again?)",
    alt_titles=["The Genie Is BACK… and the Kid Broke Him Again 🧞", "\"I Wish the Genie Guesses My Wish\" 🤯",
                "Genie vs Kid: Round 2 🧞‍♂️"],
    description="""The genie is back. And this time, his rules are tighter. 🧞

"One wish. No tricks. And your wish only comes true if I can't guess it first."

So the kid writes his wish on a paper, and folds it. "Chocolate again?" "Nope."
The kid opens the paper. It says: I wish the genie guesses my wish.

The genie freezes. Again. He didn't guess it, so the wish comes true. But the wish says he guessed it. And if he guessed it, the wish can't come true. Either way, the genie loses. Again.

So the genie quit. He sells chocolate now. 🍫

Part 2 of our original genie story (Part 1: "3 Wishes. 1 Rule. The Kid Broke the Genie").

💬 Round three: genie, or kid? 👇

🔔 Interestingly Strange: mind-bending paradoxes, clever stories, weird animals and bizarre history, animated in under a minute.""",
    hashtags=["#Paradox", "#Genie", "#Shorts"],
    tags=["genie paradox", "genie part 2", "wish paradox", "guess my wish", "paradox", "brain teaser",
          "funny story", "logic puzzle", "mind blowing", "interestingly strange"],
    pinned_comment="Give the genie a rule the kid CAN'T break 🧞 Best one becomes Round 3 👇",
)

LAMP_XY = (470 + 108, 900 - 56)
PAPER = hexc("#fff8e6")


def kid(cr, t, tl, x, y, s=1.0, **kw):
    kw.setdefault("mouth", mouth(tl, "kid", t, kw.pop("rest", "smug")))
    person(cr, t, x, y, s, "kid", glasses=True, **kw)


def folded(cr, x, y, s=1.0, open_=0.0, rot=-0.15):
    """A folded slip of paper that unfolds (open_ 0..1)."""
    cr.save()
    cr.translate(x, y)
    cr.rotate(rot)
    cr.scale(s, s)
    w = lerp(70, 140, open_)
    rrect(cr, -w / 2, -50, w, 100, 6)
    paint(cr, PAPER, OUTLINE, 4)
    if open_ < 0.5:
        stroke_line(cr, [(0, -46), (0, 46)], 3, alpha(OUTLINE, 0.4), curve=False)
    else:
        for k in range(4):
            stroke_line(cr, [(-50, -28 + k * 18), (50, -28 + k * 18)], 3, alpha(BLUE, 0.5), curve=False)
    cr.restore()


# ---------------------------------------------------------------- scenes
def scene_back(cr, t, tl):
    A = tl.at
    desert(cr, t)
    pop = 0.15
    cr.save()
    enter(cr, camera(t, [(0, (1.25, 380, 520)), (A("g1", "this"), (1.0, 360, 640))], dur=0.8))
    lamp(cr, t, 470, 900, 0.9, glow=1.0)
    if t < pop + 1.2:
        particles(cr, t, 5, 30, (0.75, 0.6, 1.0, 0.6 * (1 - seg(t, pop, pop + 1.2))), area=(380, 560, 260, 300),
                  r=(4, 12), speed=60)
    genie(cr, t, 360, 600, 0.9, eyes="angry", mouth="smug", arms=("cross", "cross"), brows="angry",
          lamp_xy=LAMP_XY, rise=1.0)
    cr.restore()
    sign(cr, t, -0.5, 360, 140, "HE'S BACK", col=PURPLE, size=84, end=A("g1", "rules") - 0.05)
    stamp(cr, t, A("g1", "rules"), 360, 150, "NEW RULES", col=RED, size=90)
    vignette(cr, 0.45)


def scene_rules(cr, t, tl):
    A = tl.at
    desert(cr, t)
    cr.save()
    enter(cr, camera(t, [(A("g2") - 0.3, (1.0, 360, 640))]))
    lamp(cr, t, 470, 900, 0.9)
    genie(cr, t, 390, 720, 0.7, eyes="half", mouth=mouth(tl, "genie", t, "smug"), arms=("wag", "down"),
          brows="raise", lamp_xy=LAMP_XY)
    person(cr, t, 140, 1000, 0.62, "kid", glasses=True, eyes="half", mouth="flat", arms=("hips", "hips"),
           look=(0.6, -0.4))
    cr.restore()
    rules = [("g2", "One"), ("g2", "No"), ("g2", "guess")]
    lines = ["1 WISH", "NO TRICKS", "I GUESS IT = NO WISH"]
    shown = [ln for (b, w), ln in zip(rules, lines) if t >= A(b, w)]
    if shown:
        card(cr, t, A("g2", "One"), 360, 90 + (110 + 52 * len(shown)) / 2, 580, 110 + 52 * len(shown), "NEW RULES",
             shown, col=RED, line_size=42)
    vignette(cr, 0.45)


def scene_write(cr, t, tl):
    A = tl.at
    desert(cr, t)
    fold = A("g3", "folds")
    cr.save()
    enter(cr, camera(t, [(A("g3") - 0.3, (1.3, 300, 700))]))
    writing = t < fold
    kid(cr, t, tl, 300, 1000, 0.95, eyes="half", rest="smug", arms=("write", "hold"),
        hold=lambda c, hx, hy: folded(c, hx + 20, hy - 10, 0.9, open_=0.0 if not writing else 1.0))
    cr.restore()
    if writing:
        cue("scribble", t, A("g3", "writes"), fold - A("g3", "writes"))
    tag(cr, t, A("g3", "wish"), 360, 220, "TOP SECRET", col=RED, size=60)
    vignette(cr, 0.45)


def scene_guess(cr, t, tl):
    A = tl.at
    desert(cr, t)
    nope = A("g5")
    cr.save()
    enter(cr, (1.0, 360, 640))
    lamp(cr, t, 470, 900, 0.9)
    genie(cr, t, 400, 620, 0.75, eyes="half" if t < nope else "wide", mouth=mouth(tl, "genie", t, "smug" if t < nope
          else "o"), arms=("chin", "down"), brows="raise" if t < nope else "up", lamp_xy=LAMP_XY)
    kid(cr, t, tl, 150, 1000, 0.7, eyes="half", rest="smug", arms=("hold", "hips"), look=(0.6, -0.4),
        hold=lambda c, hx, hy: folded(c, hx, hy - 10, 0.8))
    cr.restore()
    bubble(cr, t, A("g4"), 470, 200, "CHOCOLATE AGAIN?", col=WHITE, size=48, tail=1, end=nope - 0.05)
    stamp(cr, t, nope + 0.05, 200, 380, "NOPE.", col=RED, size=96)
    vignette(cr, 0.45)


def scene_open(cr, t, tl):
    A = tl.at
    desert(cr, t)
    says = A("g6", "says:")
    cr.save()
    enter(cr, camera(t, [(A("g6") - 0.3, (1.2, 260, 700))]))
    kid(cr, t, tl, 250, 1000, 0.95, eyes="half", rest="smug", arms=("hold", "hips"), brows="raise",
        hold=lambda c, hx, hy: folded(c, hx, hy - 10, 0.9, open_=ease_out(seg(t, A("g6", "opens"),
                                                                                  A("g6", "opens") + 0.5))))
    cr.restore()
    note(cr, t, says, 400, 330, ["\"I WISH THE", "GENIE GUESSES", "MY WISH.\""], hot=1, w=520, size=56)
    vignette(cr, 0.5)


def scene_freeze(cr, t, tl):
    A = tl.at
    desert(cr, t)
    fr = A("g7", "freezes.")
    dx, dy = shake(t, fr, 0.3, 8)
    cr.save()
    cr.translate(dx, dy)
    enter(cr, camera(t, [(A("g7") - 0.3, (1.15, 360, 520))]))
    lamp(cr, t, 470, 900, 0.9)
    genie(cr, t, 360, 600, 0.95, eyes="wide", mouth="o", brows="up", arms=("down", "down"), lamp_xy=LAMP_XY,
          grey=seg(t, fr, fr + 0.4))
    cr.restore()
    if t >= fr:
        cue("hit", t, fr)
    stamp(cr, t, fr, 360, 170, "FROZEN", col=hexc("#5a6478"), size=100)
    stamp(cr, t, A("g7", "Again."), 470, 290, "AGAIN.", col=RED, size=70, rot=0.08)
    vignette(cr, 0.5)


def _stuck(cr, t, spin):
    genie(cr, t, 360, 760, 0.42, eyes="x" if spin and t % 1 > 0.5 else "wide", mouth="o", brows="up",
          arms=("up", "up") if spin else ("chin", "down"), lamp_xy=(360 + (120 * math.sin(t * 5) if spin else 60), 900))


def scene_logic(cr, t, tl):
    from motion.pkit import studio
    studio(cr, t, hexc("#4a3a7a"), hexc("#c99adf"), seed=3)
    either_way(cr, t, tl, "g8", "g9", "g10",
               ("NOT GUESSED?", ["Wish comes true...", "but it says he", "GUESSED it!"], GREEN),
               ("GUESSED?", ["Then the wish", "can't come", "TRUE!"], RED),
               "GENIE LOSES. AGAIN.", PURPLE, ("g8", "it.", False, 2), ("g9", "true."), figure=_stuck)
    vignette(cr, 0.4)


def shop(cr, t):
    """A little sweet-shop counter with a striped awning."""
    rrect(cr, 60, 380, 600, 60, 10)
    paint(cr, hexc("#8a4fc9"), OUTLINE, 5)
    bold_text(cr, "GENIE'S CHOCOLATES", 360, 424, 40, GOLD)
    for k in range(8):                       # awning
        x = 60 + k * 75
        smooth(cr, [(x, 440), (x + 75, 440), (x + 75, 500), (x + 37, 520), (x, 500)])
        paint(cr, RED if k % 2 == 0 else WHITE, OUTLINE, 3.5)
    rrect(cr, 60, 780, 600, 240, 12)         # counter
    paint(cr, lin(0, 780, 0, 1020, [(0, hexc("#c98a4a")), (1, hexc("#8a5a2e"))]), OUTLINE, 5)
    for k in range(5):                       # bars on the counter
        cr.save()
        cr.translate(150 + k * 105, 760)
        rrect(cr, -34, -40, 68, 40, 6)
        paint(cr, CHOC, OUTLINE, 3.5)
        rrect(cr, -36, -16, 72, 18, 4)
        paint(cr, [RED, GOLD, BLUE, GREEN, PINK][k], OUTLINE, 3)
        cr.restore()


def scene_shop(cr, t, tl):
    A = tl.at
    desert(cr, t)
    sells = A("g11", "sells")
    if t < sells:
        cr.save()
        enter(cr, (1.0, 360, 640))
        genie(cr, t, 360, 640, 0.85, eyes="sad", mouth="sad", arms=("down", "down"), lamp_xy=LAMP_XY)
        lamp(cr, t, 470, 900, 0.9)
        cr.restore()
        stamp(cr, t, A("g11", "quit."), 360, 180, "I QUIT", col=RED, size=100)
    else:
        genie(cr, t, 360, 760, 0.7, eyes="half", mouth="flat", arms=("down", "down"), lamp_xy=(360, 900))
        shop(cr, t)
        sparkles(cr, t, sells, 360, 420, n=8, seed=5, col=GOLD)
    vignette(cr, 0.45)


def scene_end(cr, t, tl):
    A = tl.at
    desert(cr, t)
    cr.save()
    enter(cr, (1.0, 360, 640))
    lamp(cr, t, 480, 930, 0.85)
    genie(cr, t, 400, 650, 0.75, eyes="angry", mouth="flat", arms=("cross", "cross"), brows="angry",
          lamp_xy=(480 + 102, 930 - 53))
    kid(cr, t, tl, 150, 1000, 0.7, eyes="half", rest="smug", arms=("hips", "hold"), hold_back=bar, look=(0.6, -0.4))
    cr.restore()
    sign(cr, t, A("g12"), 360, 140, "ROUND 3?", col=PURPLE, size=72)
    buttons(cr, t, A("g12", "genie,"), [("GENIE", BLUE), ("KID", GOLD)], y=290)
    vignette(cr, 0.45)


SCENES = {"back": scene_back, "rules": scene_rules, "write": scene_write, "guess": scene_guess, "open": scene_open,
          "freeze": scene_freeze, "logic": scene_logic, "shop": scene_shop, "end": scene_end}


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    SCENES[name](cr, t, tl)
    cr.restore()
    captions(cr, t, tl)
