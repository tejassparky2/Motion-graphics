"""The Mechanical Turk: a chess "machine" from 1770 that was really a man in a box -- trickster history, polished look.

Wolfgang von Kempelen built the automaton in 1770 for Empress Maria Theresa; it toured Europe and America and was
destroyed by fire in Philadelphia in 1854. A chess master hid inside on a sliding seat while the doors were opened
one side at a time; magnets under the board showed him the moves and a lever system moved the arm. The games against
Benjamin Franklin and Napoleon are reported, so the script says "it's said" and "the story goes".
Script approved by the owner on 13 Oct 2026 (out/scripts_batch_47-50.md doc, with the "Hook fix" first line).
"""
import math

from motion.engine import W, H, cue, ease_out, hexc, lerp, seg
from motion.kit import whip
from motion.pkit import BLUE, GOLD, GREEN, PURPLE, RED, buttons, card, check, red_x, sparkles, studio, tag
from motion.polish import (OUTLINE, WHITE, alpha, appear, bold_text, camera, captions, counter, ellipse, enter,
                           light_rays, lin, paint, put, rad, rrect, shade, sign, smooth, soft_disc, soft_rrect,
                           sprite, stamp, stroke_line, vignette)
from motion.toons import head, person, portrait

NARRATOR = dict(speed=0.96)
TAIL = 0.9

SCRIPT = [
    dict(id="t1", scene="napoleon", text="Napoleon sits down to play chess. His opponent is a machine."),
    dict(id="t2", scene="cabinet", text="In [seventeen seventy,|1770,] a machine played chess against humans, and won.",
         gap=0.3),
    dict(id="t3", scene="cabinet", text="It was a big wooden cabinet, with a life-sized figure sitting on top."),
    dict(id="t4", scene="doors", text="Before every show, the inventor opened every door, so people could see the gears "
                                      "inside."),
    dict(id="t5", scene="doors", text="No person. Just machinery."),
    dict(id="t6", scene="move", text="Then the figure lifted its arm, picked up a piece, and played."),
    dict(id="t7", scene="tour", text="For over eighty years, it toured Europe and America."),
    dict(id="t8", scene="franklin", text="It's said to have played Benjamin Franklin too."),
    dict(id="t9", scene="illegal", text="The story goes, Napoleon tried an illegal move. The machine put the piece back.",
         gap=0.3),
    dict(id="t10", scene="how", text="So how did a machine from [seventeen seventy|1770] play chess?", gap=0.3),
    dict(id="t11", scene="how", text="It didn't.", gap=0.35, pace=0.9),
    dict(id="t12", scene="inside", text="A chess master was hidden inside, sliding his seat as each door opened, so he "
                                        "was never seen."),
    dict(id="t13", scene="inside", text="Magnets under the board showed him every move, and levers moved the arm."),
    dict(id="t14", scene="box", text="The world's first chess computer, was a man in a box.", pace=0.95),
    dict(id="t15", scene="ai", text="Today we ask the same thing about [A I.|AI.]", gap=0.3),
    dict(id="t16", scene="ai", text="If a machine fools everyone, does it matter how it works?", pace=0.95),
]

METADATA = dict(
    title="Napoleon Played Chess vs a MACHINE in 1809 ♟️",
    alt_titles=["In 1770, a Robot Beat Humans at Chess… ♟️", "The First Chess Computer Was a Man in a Box",
                "The Chess Robot That Fooled the World ♟️"],
    description="""In 1770, the Mechanical Turk beat people at chess, reportedly even Napoleon. Here's the trick behind the first "chess robot". ♟️

Napoleon sits down to play chess. His opponent is a machine: a big wooden cabinet with a life-sized figure on top. Before every show, the inventor opened every door so people could see the gears inside. No person. Just machinery. Then the figure lifted its arm and played.
For over 80 years it toured Europe and America. It's said to have played Benjamin Franklin too, and the story goes that when Napoleon tried an illegal move, the machine put the piece back.

So how did a machine from 1770 play chess? It didn't. A chess master was hidden inside, sliding his seat as each door opened. Magnets under the board showed him every move, and levers moved the arm. The world's first chess computer was a man in a box.

Built by Wolfgang von Kempelen in 1770; destroyed by fire in Philadelphia in 1854. The Franklin and Napoleon games are reported stories.

💬 If a machine fools everyone, does it matter how it works? 👇

🔔 Interestingly Strange: weird history, mind-bending paradoxes, The Last Bencher and strange stories, animated.""",
    hashtags=["#History", "#Chess", "#Shorts"],
    tags=["mechanical turk", "chess robot 1770", "napoleon chess", "chess hoax", "history hoax", "chess history",
          "kempelen", "weird history", "first chess computer", "interestingly strange"],
    pinned_comment="Would YOU have spotted the trick? ♟️ And does it matter how a machine works if it fools everyone? 👇",
)

WOOD = hexc("#8a5a2e")
ROBE = hexc("#2f7a5a")


# ---------------------------------------------------------------- backdrop and props
def _salon(c):
    c.rectangle(0, 0, W, H)
    c.set_source(lin(0, 0, 0, 860, [(0, hexc("#6a3a3a")), (1, hexc("#8a5040"))]))
    c.fill()
    for x in range(30, W, 140):            # wall panels
        rrect(c, x, 200, 110, 520, 10)
        paint(c, None, alpha(hexc("#e0b84a"), 0.5), 4)
    c.rectangle(0, 860, W, H - 860)
    c.set_source(lin(0, 860, 0, H, [(0, hexc("#7a5030")), (1, hexc("#4a2e1a"))]))
    c.fill()
    for k in range(0, W, 90):
        c.rectangle(k, 860, 3, H - 860)
        c.set_source_rgba(0, 0, 0, 0.15)
        c.fill()


def salon(cr, t):
    put(cr, sprite("turk_salon", W, H, _salon), 0, 0)
    soft_disc(cr, 360, 90, 220, (1, 0.85, 0.5, 0.25 + 0.03 * math.sin(t * 3)))    # chandelier glow
    light_rays(cr, t, 360, 40, n=3, a=0.05)


def board(cr, x, y, w=300, piece=None):
    """A chess board seen from slightly above; `piece` = (col, row) of a moving gold knight."""
    cr.save()
    cr.translate(x, y)
    for r in range(4):
        for k in range(8):
            x0 = -w / 2 + k * w / 8 + (r - 2) * 6
            cr.rectangle(x0, -36 + r * 9, w / 8, 9)
            cr.set_source_rgba(*(hexc("#f1e4c8") if (r + k) % 2 else hexc("#3a2418")))
            cr.fill()
    cr.rectangle(-w / 2 - 12, -36, w + 24, 36)
    cr.set_line_width(4)
    cr.set_source_rgba(*OUTLINE)
    cr.stroke()
    for k in (1, 3, 6):                      # a few pieces
        bold_text(cr, "♟", -w / 2 + k * w / 8 + 18, -22, 34, WHITE, font="DejaVu Sans", outline=OUTLINE, ow=4,
                  shadow=0)
    if piece:
        bold_text(cr, "♞", piece[0], piece[1], 48, GOLD, font="DejaVu Sans", outline=OUTLINE, ow=5, shadow=0)
    cr.restore()


def turk(cr, t, x, y, s=1.0, arm=0.0, glint=False):
    """The automaton: a robed figure with a turban, seated behind the cabinet; (x, y) = the cabinet top centre.
    `arm` 0..1 lifts its hand over the board."""
    cr.save()
    cr.translate(x - 120 * s, y)
    cr.scale(s, s)
    smooth(cr, [(-80, 0), (-70, -150), (-20, -190), (40, -190), (90, -150), (100, 0)])         # robe
    paint(cr, lin(0, -190, 0, 0, [(0, shade(ROBE, 0.25)), (1, shade(ROBE, -0.2))]), OUTLINE, 6)
    stroke_line(cr, [(10, -185), (10, 0)], 6, alpha(GOLD, 0.8), curve=False)
    cr.arc(10, -240, 52, 0, 2 * math.pi)                                                        # wooden face
    paint(cr, rad(-6, -258, 70, [(0, hexc("#e8b888")), (1, hexc("#b8804a"))]), OUTLINE, 6)
    for side in (-1, 1):
        cr.arc(10 + side * 18, -244, 6, 0, 2 * math.pi)
        paint(cr, OUTLINE, None, 0)
    smooth(cr, [(-14, -222), (10, -228), (34, -222), (10, -214)])                               # moustache
    paint(cr, hexc("#2b1d16"), None, 0)
    smooth(cr, [(-46, -262), (-40, -312), (10, -334), (60, -312), (66, -262), (10, -276)])       # turban
    paint(cr, lin(0, -334, 0, -262, [(0, WHITE), (1, hexc("#d8d0c0"))]), OUTLINE, 6)
    cr.arc(10, -300, 9, 0, 2 * math.pi)
    paint(cr, RED, OUTLINE, 3)
    # the arm: shoulder at (80, -150) reaching to the board
    hx = lerp(150, 210, arm)
    hy = lerp(-30, -110, math.sin(arm * math.pi)) - 10
    stroke_line(cr, [(80, -150), (130, -80 + 30 * arm), (hx, hy)], 26, shade(ROBE, -0.1))
    stroke_line(cr, [(80, -150), (130, -80 + 30 * arm), (hx, hy)], 20, ROBE)
    cr.arc(hx, hy, 16, 0, 2 * math.pi)
    paint(cr, hexc("#d8a878"), OUTLINE, 4)
    if glint:
        sparkles(cr, t, 0, 10, -244, n=3, seed=5, col=GOLD, spread=40)
    cr.restore()


def cabinet(cr, t, x, y, s=1.0, doors=0.0, gears=True, inside=None):
    """The cabinet with its top at (x, y). `doors` 0..1 swings the front doors open on whirling gears; `inside`
    draws something in the open cabinet instead of gears."""
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    w, h = 400, 230
    soft_rrect(cr, -w / 2, 12, w, h, 12, (0, 0, 0, 0.35), sigma=14)
    rrect(cr, -w / 2, 0, w, h, 10)
    paint(cr, lin(0, 0, 0, h, [(0, shade(WOOD, 0.25)), (1, shade(WOOD, -0.25))]), OUTLINE, 6)
    for side in (-1, 1):
        rrect(cr, side * (w / 2 - 30) - 12, h, 24, 40, 6)
        paint(cr, shade(WOOD, -0.3), OUTLINE, 4)
    # the inside, visible when the doors open
    cr.save()
    rrect(cr, -w / 2 + 16, 16, w - 32, h - 32, 6)
    cr.clip()
    cr.set_source_rgba(0.12, 0.08, 0.05, 1)
    cr.paint()
    if inside:
        inside(cr)
    elif gears:
        for k, (gx, gy, r) in enumerate(((-110, 80, 50), (-30, 140, 40), (60, 70, 56), (140, 150, 38))):
            cr.save()
            cr.translate(gx, gy)
            cr.rotate(t * (1.5 if k % 2 else -1.5))
            for j in range(10):
                cr.rotate(math.pi / 5)
                rrect(cr, -6, -r - 10, 12, 16, 3)
                paint(cr, hexc("#c8a040"), OUTLINE, 2)
            cr.arc(0, 0, r, 0, 2 * math.pi)
            paint(cr, hexc("#d8b050"), OUTLINE, 3)
            cr.arc(0, 0, r * 0.3, 0, 2 * math.pi)
            paint(cr, hexc("#7a5a20"), OUTLINE, 3)
            cr.restore()
    cr.restore()
    # doors (left and right halves) swing open by squashing toward the hinges
    for side in (-1, 1):
        dw = (w / 2 - 16) * (1 - 0.85 * doors)
        x0 = -w / 2 + 16 if side < 0 else w / 2 - 16 - dw
        rrect(cr, x0, 16, dw, h - 32, 6)
        paint(cr, lin(0, 16, 0, h, [(0, shade(WOOD, 0.1)), (1, shade(WOOD, -0.15))]), OUTLINE, 4)
        if dw > 30:
            cr.arc(x0 + (dw - 14 if side < 0 else 14), h / 2, 6, 0, 2 * math.pi)
            paint(cr, GOLD, OUTLINE, 2)
    cr.restore()


def turk_set(cr, t, x, y, s=1.0, arm=0.0, doors=0.0, glint=False, piece=None, inside=None):
    turk(cr, t, x, y, s, arm=arm, glint=glint)
    cabinet(cr, t, x, y, s, doors=doors, inside=inside)
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    board(cr, 40, 2, 280, piece=piece)
    cr.restore()


def crowd(cr, t, y=1130, gasp=False):
    for k, (x, who) in enumerate(((90, "inventor"), (260, "franklin"), (450, "napoleon"), (630, "inventor"))):
        head(cr, t, x, y + math.sin(t * 2 + k) * 4, 95, who, eyes="wide" if gasp else "open",
             mouth="o" if gasp else "smile", brows="up" if gasp else None, look=(0, -0.6))


# ---------------------------------------------------------------- scenes
def scene_napoleon(cr, t, tl):
    A = tl.at
    salon(cr, t)
    cr.save()
    enter(cr, camera(t, [(0, (1.0, 360, 640)), (A("t1", "machine."), (1.12, 380, 640))], dur=0.8))
    turk_set(cr, t, 470, 620, 0.8, arm=0.3 + 0.2 * math.sin(t * 2), glint=t >= A("t1", "machine."))
    person(cr, t, 150, 900, 0.85, "napoleon", eyes="half", mouth="smug", arms=("chin", "down"), brows="raise")
    cr.restore()
    sign(cr, t, -0.5, 360, 120, "NAPOLEON vs A MACHINE", col=GOLD, size=52)
    if t >= A("t1", "machine."):
        cue("hit", t, A("t1", "machine."))
    vignette(cr, 0.4)


def scene_cabinet(cr, t, tl):
    A = tl.at
    salon(cr, t)
    turk_set(cr, t, 360, 600, 0.95, arm=0.2)
    tag(cr, t, A("t2", "1770,"), 360, 170, "1770", col=GOLD, size=60)
    stamp(cr, t, A("t2", "won."), 360, 290, "IT WON", col=RED, size=70, end=A("t3") - 0.05)
    if t >= A("t3", "cabinet,"):
        sign(cr, t, A("t3", "cabinet,"), 160, 520, "WOODEN BOX", col=BLUE, size=36, rot=-0.06)
    if t >= A("t3", "figure"):
        sign(cr, t, A("t3", "figure"), 560, 300, "LIFE-SIZED FIGURE", col=PURPLE, size=34, rot=0.05)
    crowd(cr, t)
    vignette(cr, 0.4)


def scene_doors(cr, t, tl):
    A = tl.at
    salon(cr, t)
    u = ease_out(seg(t, A("t4", "opened"), A("t4", "opened") + 0.8))
    turk_set(cr, t, 400, 560, 1.0, doors=u)
    person(cr, t, 110, 960, 0.8, "inventor", eyes="happy", mouth="talk" if t < A("t5") else "smile",
           arms=("point", "down"))
    if t >= A("t5"):
        card(cr, t, A("t5"), 360, 230, 460, 170, "NO PERSON.", ["Just machinery."], col=GREEN, title_size=46,
             line_size=42, mark="ok", mark_at=A("t5", "machinery."))
    else:
        sign(cr, t, A("t4", "gears"), 360, 190, "LOOK: GEARS!", col=GOLD, size=56)
    vignette(cr, 0.4)


def scene_move(cr, t, tl):
    A = tl.at
    salon(cr, t)
    lift = A("t6", "lifted")
    u = seg(t, lift, A("t6", "played.", end=True))
    cr.save()
    enter(cr, camera(t, [(A("t6") - 0.3, (1.0, 360, 640)), (lift, (1.6, 380, 560))], dur=0.6))
    px = lerp(-60, 60, ease_out(seg(t, A("t6", "piece,"), A("t6", "played."))))
    turk_set(cr, t, 360, 620, 1.0, arm=u, piece=(px, -40))
    cr.restore()
    crowd(cr, t, gasp=t >= A("t6", "played."))
    sign(cr, t, A("t6", "played."), 360, 160, "OOOOH!", col=GOLD, size=72)
    vignette(cr, 0.4)


def _parchment(c):
    c.rectangle(0, 0, W, H)
    c.set_source(rad(360, 600, 800, [(0, hexc("#f4e4c0")), (1, hexc("#c8a868"))]))
    c.fill()
    smooth(c, [(80, 330), (230, 270), (300, 360), (250, 520), (300, 640), (220, 720), (150, 600), (90, 470)])
    paint(c, hexc("#b8c890"), OUTLINE, 4)                                      # the Americas
    smooth(c, [(420, 300), (560, 260), (640, 320), (600, 420), (500, 440), (440, 400)])
    paint(c, hexc("#b8c890"), OUTLINE, 4)                                      # Europe
    for k in range(5):
        c.move_to(310, 380 + k * 40)
        c.curve_to(350, 360 + k * 40, 380, 400 + k * 40, 420, 380 + k * 40)
        c.set_line_width(2)
        c.set_source_rgba(0.3, 0.4, 0.6, 0.4)
        c.stroke()


def scene_tour(cr, t, tl):
    A = tl.at
    put(cr, sprite("turk_map", W, H, _parchment), 0, 0)
    pins = [(500, 330), (560, 300), (600, 360), (470, 390), (200, 360), (240, 450), (180, 540)]
    for k, (x, y) in enumerate(pins):
        st = A("t7") + 0.15 + 0.28 * k
        if t >= st:
            kk = appear(t, st, 0.25)
            cr.arc(x, y - 30 * kk, 14, 0, 2 * math.pi)
            paint(cr, RED, OUTLINE, 3)
            stroke_line(cr, [(x, y - 30 * kk + 14), (x, y)], 4, OUTLINE, curve=False)
            cue("pop", t, st)
    yr = int(lerp(1770, 1854, seg(t, A("t7"), A("t7", end=True))))
    bold_text(cr, f"{yr}", 360, 820, 110, WHITE)
    tag(cr, t, A("t7", "Europe"), 540, 220, "EUROPE", col=BLUE, size=38)
    tag(cr, t, A("t7", "America."), 200, 220, "AMERICA", col=GREEN, size=38)
    sign(cr, t, A("t7"), 360, 120, "80+ YEARS ON TOUR", col=PURPLE, size=50)


def scene_franklin(cr, t, tl):
    A = tl.at
    salon(cr, t)
    portrait(cr, t, A("t8") - 0.1, 360, 480, 190, "franklin", eyes="wide", mouth="o", brows="up",
             bg=hexc("#9fc8ff"))
    tag(cr, t, A("t8", "Benjamin"), 360, 230, "BENJAMIN FRANKLIN", col=hexc("#9fc8ff"), size=44)
    sign(cr, t, A("t8"), 360, 760, "IT'S SAID...", col=GOLD, size=56, rot=0.03)
    vignette(cr, 0.4)


def scene_illegal(cr, t, tl):
    A = tl.at
    salon(cr, t)
    cheat = A("t9", "illegal")
    back = A("t9", "back.")
    cr.save()
    enter(cr, camera(t, [(A("t9") - 0.3, (1.0, 360, 640)), (cheat, (1.3, 380, 620))], dur=0.6))
    if t < back:
        px = lerp(-60, 120, ease_out(seg(t, cheat, cheat + 0.6)))
        arm = 0.1
    else:
        px = lerp(120, -60, ease_out(seg(t, back, back + 0.5)))
        arm = 1 - seg(t, back, back + 0.5) * 0.4
    turk_set(cr, t, 470, 620, 0.8, arm=arm, piece=(px, -40))
    shocked = t >= back
    person(cr, t, 150, 900, 0.85, "napoleon", eyes="wide" if shocked else "half", mouth="o" if shocked else "smug",
           arms=("point", "down") if not shocked else ("face", "down"), brows="up" if shocked else "raise",
           sweat=shocked)
    cr.restore()
    stamp(cr, t, cheat + 0.2, 360, 150, "ILLEGAL MOVE", col=RED, size=70, end=back - 0.05)
    stamp(cr, t, back, 360, 150, "NOPE.", col=PURPLE, size=90)
    vignette(cr, 0.4)


def scene_how(cr, t, tl):
    A = tl.at
    cr.rectangle(0, 0, W, H)
    cr.set_source_rgba(0.08, 0.06, 0.08, 1)
    cr.fill()
    soft_disc(cr, 360, 620, 360, (1, 0.9, 0.6, 0.25))
    turk_set(cr, t, 360, 600, 0.95, arm=0.2)
    if t < A("t11"):
        bold_text(cr, "?", 600, 380 + math.sin(t * 5) * 8, 170 * appear(t, A("t10", "how"), 0.4), GOLD)
    else:
        cue("thud", t, A("t11"))
        stamp(cr, t, A("t11"), 360, 220, "IT DIDN'T.", col=RED, size=96)
    vignette(cr, 0.5)


def hidden_man(cr, t, x, s=0.62, eyes="open"):
    person(cr, t, x, 220, s, "fermi", eyes=eyes, mouth="flat", arms=("hold", "chin"), shadow=False)


def scene_inside(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#3a2a2a"), hexc("#6a4a3a"), seed=7)
    # alternate: left door open while he slides right, then right door open while he slides left
    phase = (t - A("t12", "sliding")) / 1.4 if t >= A("t12", "sliding") else 0.0
    left_open = int(phase) % 2 == 0
    pos = (phase % 1.0)
    slide = ease_out(min(1, pos * 2))
    mx = lerp(-90, 90, slide) if left_open else lerp(90, -90, slide)
    magnets = t >= A("t13")

    def inside(c):
        c.rectangle(-200, 0, 400, 230)
        c.set_source_rgba(0.25, 0.18, 0.1, 1)
        c.fill()
        if left_open:      # the open side shows gears only
            for k in range(2):
                c.arc(-120, 70 + k * 80, 32, 0, 2 * math.pi)
                paint(c, hexc("#d8b050"), OUTLINE, 3)
        else:
            for k in range(2):
                c.arc(120, 70 + k * 80, 32, 0, 2 * math.pi)
                paint(c, hexc("#d8b050"), OUTLINE, 3)
        rrect(c, mx - 60, 175, 120, 18, 6)                     # the sliding seat
        paint(c, hexc("#c8a040"), OUTLINE, 3)
        hidden_man(c, t, mx, 0.42, eyes="wide" if magnets else "open")
        if magnets:
            for k in range(5):                                 # magnets dangling under the board
                bx = -150 + k * 75
                jump = 6 * math.sin(t * 9 + k * 1.7) if k in (1, 3) else 0
                stroke_line(c, [(bx, 0), (bx, 48 + jump)], 4, OUTLINE, curve=False)
                c.arc(bx, 56 + jump, 13, 0, 2 * math.pi)
                paint(c, RED, OUTLINE, 3)
            stroke_line(c, [(mx + 20, 120), (150, 20)], 8, hexc("#9aa0ac"), curve=False)   # lever to the arm

    cr.save()
    cr.translate(360, 330)
    cr.scale(1.5, 1.5)
    cr.translate(-360, -330)
    cabinet(cr, t, 360, 330, 1.0, doors=1.0, inside=inside)
    cr.restore()
    # the doors as overlays: one side open at a time (the cabinet is drawn 1.5x, inside x 84-636, y 354-651)
    rrect(cr, 84 if not left_open else 360, 354, 276, 297, 8)
    paint(cr, alpha(shade(WOOD, 0.05), 0.45), OUTLINE, 5)
    bold_text(cr, "CLOSED", 222 if not left_open else 498, 520, 34, alpha(WHITE, 0.8))
    bold_text(cr, "OPEN", 498 if not left_open else 222, 640, 30, GOLD)
    tag(cr, t, A("t12", "chess"), 360, 150, "A CHESS MASTER INSIDE", col=GOLD, size=40, end=A("t13") - 0.05)
    tag(cr, t, A("t13", "Magnets"), 360, 150, "MAGNETS + LEVERS", col=RED, size=44)
    if t >= A("t12", "never"):
        sign(cr, t, A("t12", "never"), 360, 800, "NEVER SEEN", col=PURPLE, size=50, end=A("t13") - 0.05)
    vignette(cr, 0.4)


def scene_box(cr, t, tl):
    A = tl.at
    salon(cr, t)
    peek = ease_out(seg(t, A("t14", "man"), A("t14", "man") + 0.4))

    def inside(c):
        hidden_man(c, t, 0, 0.5, eyes="happy")

    turk_set(cr, t, 360, 620, 0.9, doors=peek, inside=inside)
    card(cr, t, A("t14", "computer,"), 360, 260, 560, 200, "1st CHESS COMPUTER", ["= 1 man in a box"], col=PURPLE,
         title_size=44, line_size=48)
    vignette(cr, 0.4)


def scene_ai(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#cfe0ff"), hexc("#fff1d6"), seed=4)
    turk_set(cr, t, 210, 640, 0.55, arm=0.4 + 0.3 * math.sin(t * 2))
    # a phone with a chat bubble
    rrect(cr, 430, 360, 220, 400, 26)
    paint(cr, hexc("#1b1b1f"), OUTLINE, 5)
    rrect(cr, 446, 380, 188, 360, 16)
    paint(cr, hexc("#eef4ff"), None, 0)
    if t >= A("t15", "AI."):
        k = appear(t, A("t15", "AI."), 0.3)
        rrect(cr, 462, 420, 150 * k, 70, 16)
        paint(cr, BLUE, None, 0)
        bold_text(cr, "Hi! I'm", 537, 450, 26 * k, WHITE, font="Fredoka", outline=None, shadow=0)
        bold_text(cr, "a machine.", 537, 478, 26 * k, WHITE, font="Fredoka", outline=None, shadow=0)
        bold_text(cr, "?", 540, 640, 90 * k, GOLD)
    sign(cr, t, A("t15"), 360, 150, "TODAY: AI", col=BLUE, size=60, end=A("t16") - 0.05)
    buttons(cr, t, A("t16", "matter"), [("MATTERS", GREEN), ("DOESN'T", RED)], y=200, size=44, w=300)
    vignette(cr, 0.35)


SCENES = {"napoleon": scene_napoleon, "cabinet": scene_cabinet, "doors": scene_doors, "move": scene_move,
          "tour": scene_tour, "franklin": scene_franklin, "illegal": scene_illegal, "how": scene_how,
          "inside": scene_inside, "box": scene_box, "ai": scene_ai}


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    SCENES[name](cr, t, tl)
    cr.restore()
    captions(cr, t, tl)
