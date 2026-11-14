"""Shots u056-u111 of the Uttara Kanda long video (Sita returns to the earth, Kaal at the door, Lakshmana's end,
Rama's end, the closing question). Same conventions as uk_shots_a."""
import math

import cairo

import uk_base as B
from poster import clamp, ease, prog
from puppet_core import depth, keyed, prop
from scenes_jayadratha import flash_at, tint
from scenes_ruru import sepia
from scenes_six_c import brahma

GL = B.GL


def dark_aura(cr, x, y, r, a):
    """A dark purple shadow-light behind a figure (Death)."""
    if a <= 0.01:
        return
    g = cairo.RadialGradient(x, y, 0, x, y, r)
    g.add_color_stop_rgba(0, 0.18, 0.06, 0.24, 0.75 * a)
    g.add_color_stop_rgba(1, 0.18, 0.06, 0.24, 0.0)
    cr.save()
    cr.set_operator(cairo.OPERATOR_MULTIPLY)
    cr.set_source(g)
    cr.arc(x, y, r, 0, 2 * math.pi)
    cr.fill()
    cr.restore()


def crack(cr, t, x, y, w, p, a=1.0):
    """A glowing crack opening in the ground."""
    if p <= 0.01:
        return
    pts = [(x - w / 2 + w * i / 14, y + (10 if i % 2 else -6)) for i in range(15)]
    n = max(2, int(len(pts) * clamp(p)))
    B.trail(cr, pts[:n], a)
    B.warm(cr, x, y, w * 0.6 * p, a)


def nagas(cr, t, x, y, s, a):
    """Two serpents rising either side of the throne (the throne is held up by Nagas)."""
    for side in (-1, 1):
        cr.save()
        cr.translate(x + side * 190 * s, y)
        cr.scale(side, 1)
        cr.move_to(0, 0)
        for i in range(1, 13):
            u = i / 12
            cr.line_to(20 * math.sin(u * 8 + t * 2), -300 * s * u)
        cr.set_source_rgba(0.20, 0.42, 0.22, a)
        cr.set_line_width(26 * s)
        cr.stroke()
        cr.arc(0, -300 * s, 26 * s, 0, 2 * math.pi)
        cr.set_source_rgba(0.20, 0.42, 0.22, a)
        cr.fill()
        cr.restore()


def s_summon(cr, t, tl, t0, t1):
    """u056-u057: Rama sends for Sita, with a condition: an oath before everyone."""
    t57 = B.ls(tl, "u057")
    B.palace(cr)
    B.rama(cr, t, 760, 0.64, front=(-1.4, -0.3), hits=[(t0 + 0.2, 0.4), (t57, 0.3)])
    B.walker(cr, t, lambda cr_, t_, x, s, **kw: B.man(cr_, t_, B.TOWN[0][0], B.TOWN[0][1], x, s, **kw),
             t0 + 0.3, t57 + 1.5, 1000, 1900, 0.56)

    def ui(cr_):
        if t > t57:
            B.card(cr_, t, t57 + 0.1, 1300, 360, "शर्त", "सबके सामने क़सम")
    return {"ui": ui}


def s_assembly(cr, t, tl, t0, t1):
    """u058-u059: the full assembly; Valmiki brings Sita; he swears she is pure."""
    t59 = B.ls(tl, "u059")
    B.palace(cr)
    B.townsfolk(cr, t, (120, 280, 1640, 1800), 0.5)
    B.rama(cr, t, 1460, 0.6, flip=True, front=(-0.3, -0.5))
    x = 500 + 260 * ease(clamp((t - t0) / max(0.6, t59 - t0)))
    B.valmiki(cr, t, x, 0.62, front=(-2.6, 0.2) if t > t59 else (-0.6, -0.6), hits=[(t59, 0.5)])
    B.sita(cr, t, x + 240, 0.6, head=0.1)
    return {}


def s_earth(cr, t, tl, t0, t1):
    """u060-u064: Sita prays to Mother Earth; the ground opens, a shining throne rises with serpents, the Earth
    goddess takes Sita on her lap, and they go down into the earth."""
    t61, t62, t63, t64 = (B.ls(tl, k) for k in ("u061", "u062", "u063", "u064"))
    B.palace(cr, 0.6)
    B.townsfolk(cr, t, (140, 300, 1620, 1780), 0.5, front=(-2.2, 0.1) if t > t62 else (-0.3, -0.5))
    sink = 360 * ease(clamp((t - t64 - 0.3) / 2.2))
    if t > t62 - 0.2:
        crack(cr, t, 960, GL - 4, 640, prog(t, t62 - 0.2, 0.5))
        up = ease(clamp((t - t62) / 1.2))
        ty = GL + 200 - 200 * up + sink
        B.warm(cr, 960, ty - 200, 420, up)
        nagas(cr, t, 960, ty, 1.0, 0.9 * up)
        prop(cr, "kk_throne", 960, ty, 0.8, alpha=up)
        if t > t63 - 0.3:
            B.earth(cr, t, 900, 0.62, feet=ty - 10, alpha=prog(t, t63 - 0.3, 0.4) * (1 - prog(t, t64 + 1.6, 0.6)),
                    front=(-1.2, -0.6), rods=False)
    sx = 960 if t < t63 else 1040
    sy = (GL if t < t63 else GL + 200 - 200 * ease(clamp((t - t62) / 1.2)) - 30) + sink
    B.sita(cr, t, sx, 0.62, feet=sy, head=0.12 if t < t62 else 0.0, alpha=1 - prog(t, t64 + 1.6, 0.6),
           **(B.ANJ if t < t63 else {}))
    B.ground(cr, a=0.55)
    return dict(flash=flash_at(t, t62, 0.3), eve=0.2)


def s_born(cr, t, tl, t0, t1):
    """u065-u067: a memory: King Janaka ploughing finds the baby Sita in the furrow; and she went back to the earth."""
    t66, t67 = B.ls(tl, "u066"), B.ls(tl, "u067")
    if t < t67:
        B.ground(cr, GL - 40)
        for k in range(4):                                  # furrows in the ploughed field
            cr.move_to(150, GL - 18 + k * 22)
            cr.line_to(1770, GL - 30 + k * 22)
            cr.set_source_rgba(0.30, 0.18, 0.08, 0.7)
            cr.set_line_width(5)
            cr.stroke()
        x = 500 + 300 * clamp((t - t0) / 3.0)
        B.janaka(cr, t, x, 0.62, front=(-0.9, -0.3))
        B.warm(cr, 1200, GL - 60, 200, prog(t, t66, 0.4))
        prop(cr, "c6_rama_cradle", 1200, GL - 20, 0.4, alpha=prog(t, t66, 0.4))

        def ui(cr_):
            sepia(cr_, 0.55)
        return {"ui": ui}
    B.palace(cr, 0.6)
    B.ground(cr)
    crack(cr, t, 960, GL - 4, 640, 1 - prog(t, t67 + 0.3, 1.2), 0.8)
    B.petals(cr, t, t67, 600, 1300, 0.8, 14)
    return {}


def s_grief(cr, t, tl, t0, t1):
    """u068-u069: Rama, in grief and anger, demands Sita back from the earth; she never came back."""
    t69 = B.ls(tl, "u069")
    B.palace(cr, 0.5)
    B.ground(cr)
    B.red_spot(cr, 960, GL - 200, 380, 0.5 * (1 - prog(t, t69, 0.5)))
    B.rama(cr, t, 960, 0.7, kneel="uk_rama_kneel", head=0.3,
           front=keyed(t, [(0, (-2.4, 0.3)), (t0 + 0.8, (-0.6, -0.1)), (t0 + 1.6, (-2.4, 0.3)), (t69, (-0.4, -0.6))]))
    return dict(night=0.35 + 0.2 * prog(t, t69, 0.5))


def s_years(cr, t, tl, t0, t1):
    """u070-u073: many years pass (sun and moon race over the palace); an ascetic comes; he is Death himself
    (a dark shadow of Yama rises behind him)."""
    t71, t73 = B.ls(tl, "u071"), B.ls(tl, "u073")
    prop(cr, "mt_city", 960, GL - 10, 0.75, alpha=0.8, blur=3)
    B.ground(cr)
    if t < t71:
        u = (t - t0) * 1.4
        B.orb(cr, t, 960 + 820 * math.cos(math.pi * (u % 1.0)), 520 - 380 * math.sin(math.pi * (u % 1.0)), 40, 1.0)
        return dict(night=0.3 * (int(u) % 2))
    if t > t73 - 0.3:
        dark_aura(cr, 1180, GL - 420, 460, prog(t, t73 - 0.3, 0.5))
        B.yama(cr, t, 1240, 0.78, flip=True, alpha=0.5 * prog(t, t73 - 0.3, 0.6), blur=6, rods=False)
    B.walker(cr, t, B.kaal, t71, t71 + 2.4, 1700, 1180, 0.62, flip=True)
    return dict(night=0.15 + 0.3 * prog(t, t73, 0.5), flash=flash_at(t, t73, 0.2))


def s_room(cr, t, tl, t0, t1):
    """u074-u077: inside, Rama and Death talk alone; whoever sees or hears must die; Lakshmana guards the door
    outside (a wall splits the picture); Death gives Brahma's message: your work on earth is done."""
    t75, t76, t77 = B.ls(tl, "u075"), B.ls(tl, "u076"), B.ls(tl, "u077")
    B.palace(cr, 0.7)
    cr.save()
    cr.rectangle(1180, 160, 70, GL - 160)
    cr.set_source_rgba(0.45, 0.26, 0.12, 0.9)
    cr.fill()
    cr.restore()
    B.rama(cr, t, 380, 0.6, front=(-0.6, -0.6), head=0.1 * (t > t77))
    dark_aura(cr, 850, GL - 380, 300, 0.7)
    B.kaal(cr, t, 850, 0.6, flip=True, front=(-1.2, -0.5), hits=[(t0 + 0.2, 0.3), (t75, 0.3), (t77, 0.4)])
    if t > t76 - 0.3:
        B.lakshmana(cr, t, 1520, 0.6, flip=True, alpha=prog(t, t76 - 0.3, 0.4))
    if t > t77:
        B.warm(cr, 620, GL - 520, 200, prog(t, t77, 0.5))

    def ui(cr_):
        if t75 - 0.1 < t < t76:
            B.card(cr_, t, t75, 620, 330, "जो सुनेगा", "उसे मौत")
    return dict(ui=ui, night=0.3)


def s_durvasa(cr, t, tl, t0, t1):
    """u078-u082: the sage Durvasa, famous for his anger, at the gate; must see Rama now; Lakshmana begs him to wait;
    he blazes up: he will curse the whole kingdom."""
    t80, t81, t82 = B.ls(tl, "u080"), B.ls(tl, "u081"), B.ls(tl, "u082")
    prop(cr, "mt_city", 960, GL - 10, 0.75, alpha=0.6, blur=4)
    B.ground(cr)
    B.red_spot(cr, 1350, GL - 420, 420, 0.3 + 0.5 * prog(t, t82, 0.3))
    B.durvasa(cr, t, 1350, 0.66, flip=True, front=(-1.5, 0.0) if t > t80 else (-0.4, -0.6),
              backa=(-2.6, 0.2) if t > t82 else (0.3, -0.4), hits=[(t80, 0.5), (t82, 0.8)])
    B.lakshmana(cr, t, 760, 0.62, **(B.ANJ if t > t81 else dict(front=(-0.3, -0.5))))
    if t > t82:
        for k in range(3):
            B.trail(cr, [(1360, 380), (1300 - 60 * k, 300 - 90 * k), (1200 - 40 * k, 220 - 60 * k)],
                    1 - prog(t, t82 + 0.4 + 0.2 * k, 0.4))
    return dict(flash=flash_at(t, t82 + 0.1, 0.35))


def s_choice(cr, t, tl, t0, t1):
    """u083-u084: Lakshmana thinks: better that I alone die than everyone (Ayodhya under a red sky); he walks in."""
    t84 = B.ls(tl, "u084")
    B.palace(cr, 0.6)
    if t < t84:
        B.lakshmana(cr, t, 1100, 0.66, flip=True, head=0.15, front=B.HEART["front"], backa=B.HEART["backa"])

        def ui(cr_):
            q = B.bubble(cr_, t, t0 + 0.2, 600, 360, 1.6)
            if q > 0.01:
                prop(cr_, "mt_city", 600, 470, 0.26, alpha=q)
                B.red_spot(cr_, 600, 400, 200, q)
        return {"ui": ui}
    B.walker(cr, t, B.lakshmana, t84, t84 + 1.6, 1300, 760, 0.66, flip=True)
    cr.save()
    cr.rectangle(1180, 160, 70, GL - 160)
    cr.set_source_rgba(0.45, 0.26, 0.12, 0.9 * (1 - prog(t, t84 + 0.6, 0.6)))
    cr.fill()
    cr.restore()
    return {}


def s_sees(cr, t, tl, t0, t1):
    """u085-u086: Rama sees his dearest brother and understands; break the promise, or lose the brother?"""
    t86 = B.ls(tl, "u086")
    B.palace(cr, 0.6)
    B.rama(cr, t, 700, 0.7, front=B.HEART["front"], backa=B.HEART["backa"], head=0.1)
    B.lakshmana(cr, t, 1240, 0.66, flip=True, head=0.2, **B.ANJ)

    def ui(cr_):
        if t > t86 - 0.1:
            B.card(cr_, t, t86, 520, 330, "वादा?", "धर्म")
            B.card(cr_, t, t86 + 0.9, 1400, 330, "भाई?", "लक्ष्मण")
            if t > t86 + 1.4:
                n = int((t - t86 - 1.4) / 0.9)
                B.red_ring(cr_, (520, 1400)[n % 2], 334, 200, 140, prog(t, t86 + 1.4 + 0.9 * n, 0.35), 9)
    return dict(ui=ui, night=0.25)


def s_banish(cr, t, tl, t0, t1):
    """u087-u090: Lakshmana: keep your promise; Vasishtha: a broken promise breaks dharma; Rama, heavy-hearted:
    I give you up; for a man of honour, being given up is the same as death."""
    t88, t89, t90 = B.ls(tl, "u088"), B.ls(tl, "u089"), B.ls(tl, "u090")
    B.palace(cr)
    B.rama(cr, t, 640, 0.68, front=(-2.2, 0.0) if t > t89 else (-0.4, -0.5), head=0.18, hits=[(t89, 0.5)])
    B.lakshmana(cr, t, 1180, 0.64, flip=True, kneel="uk_lk_kneel" if t < t88 else None,
                head=0.2, **B.ANJ)
    if t > t88 - 0.3:
        b, k, a = depth(t, t88 - 0.3, 0.45)
        B.vasishtha(cr, t, 1520, 0.62 * k, flip=True, alpha=a, blur=b, front=(-1.4, -0.3), hits=[(t88, 0.4)])

    def ui(cr_):
        if t > t90:
            B.card(cr_, t, t90 + 0.1, 960, 330, "त्याग = मौत", "इज़्ज़तदार के लिए")
    return dict(ui=ui, night=0.2, flash=flash_at(t, t89 + 0.3, 0.12))


def s_sarayu(cr, t, tl, t0, t1):
    """u091-u093: Lakshmana goes to the Sarayu, sits in meditation, holds his breath; flowers rain; light carries
    him up to heaven."""
    t92, t93 = B.ls(tl, "u092"), B.ls(tl, "u093")
    B.sky(cr, t, 0.5)
    B.ground(cr)
    B.river(cr, t, GL - 40, 150)
    if t < t92:
        B.walker(cr, t, B.lakshmana, t0, t92, 300, 900, 0.62)
    else:
        rise = 260 * ease(clamp((t - t93 - 0.8) / 2.2))
        a = 1 - 0.6 * prog(t, t93 + 1.2, 1.2)
        B.glow(cr, 900, GL - 300 - rise, 300, prog(t, t92, 0.6))
        B.lakshmana(cr, t, 900, 0.62, kneel="uk_lk_kneel", y=GL - 250 * 0.62 - rise, head=0.05, alpha=a, **B.ANJ)
        B.petals(cr, t, t93, 500, 1300)
        B.lights(cr, t, 900, GL - 400 - rise, 260, 14, prog(t, t93, 0.5))
    return dict(eve=0.25)


def s_together(cr, t, tl, t0, t1):
    """u094: a memory: Rama and Lakshmana walking together in the forest, then the empty path."""
    B.forest(cr, t)
    a = 1 - prog(t, t1 - 1.6, 0.8)
    B.walker(cr, t, B.rama, t0, t1, 500, 1100, 0.6)
    B.walker(cr, t, B.lakshmana, t0, t1, 280, 880, 0.58, alpha=a)

    def ui(cr_):
        sepia(cr_, 0.45)
    return {"ui": ui}


def s_kingdoms(cr, t, tl, t0, t1):
    """u095-u097: without Lakshmana Rama no longer wants to stay; he shares the kingdom between his sons: Kusha
    gets Kushavati, Lava Shravasti."""
    t96, t97 = B.ls(tl, "u096"), B.ls(tl, "u097")
    B.palace(cr)
    B.rama(cr, t, 960, 0.64, head=0.15 * (t < t96), front=(-1.0, -0.6) if t > t96 else (-0.2, -0.3))
    if t > t96 - 0.2:
        for k, x in enumerate((560, 1360)):
            q = prog(t, t96 - 0.2 + 0.3 * k, 0.4)
            B.boy(cr, t, x, 0.56, flip=k == 1, alpha=q, **B.ANJ)
            prop(cr, "kk_crown", x + (8 if k == 0 else -8), GL - 590, 0.36,
                 alpha=prog(t, t96 + 0.6 + 0.3 * k, 0.4))

    def ui(cr_):
        if t > t97:
            for k, (x, name) in enumerate(((560, "कुश: कुशावती"), (1360, "लव: श्रावस्ती"))):
                B.label(cr_, t, t97 + 0.6 * k, name, t1 - 0.1, x=x, y=GL - 700, size=56)
    return {"ui": ui}


def s_hanuman(cr, t, tl, t0, t1):
    """u098-u100: Rama tells Hanuman to stay on earth, alive as long as his story is told; people say he is still
    here (Hanuman on a hilltop, a glowing book of the story)."""
    t99, t100 = B.ls(tl, "u099"), B.ls(tl, "u100")
    if t < t100:
        B.palace(cr)
        B.rama(cr, t, 760, 0.66, front=(-1.4, -0.9) if t > t99 else (-1.0, -0.5), hits=[(t99, 0.4)])
        B.hanuman(cr, t, 1200, 0.62, flip=True, kneel="uk_hanu_kneel", head=0.1, **B.ANJ)
        if t > t99:
            B.glow(cr, 1150, GL - 360, 260, prog(t, t99, 0.5))
        return {}
    B.sky(cr, t, 0.7)
    cr.save()
    pc_poly = __import__("puppet_core").poly
    pc_poly(cr, [(600, GL), (960, GL - 260), (1320, GL)])
    cr.set_source_rgba(0.48, 0.34, 0.22, 0.9)
    cr.fill()
    cr.restore()
    B.hanuman(cr, t, 960, 0.46, feet=GL - 250, **B.ANJ)
    B.book(cr, t, t100 + 0.3, 1240, 520, 0.9)
    return dict(eve=0.3)


def s_walk(cr, t, tl, t0, t1):
    """u101-u103: one morning Rama walks to the Sarayu; the people of Ayodhya follow; no one wants to stay
    without him."""
    t102 = B.ls(tl, "u102")
    B.sky(cr, t, 0.5)
    B.ground(cr)
    B.river(cr, t, GL - 10, 120)
    B.walker(cr, t, B.rama, t0, t1 + 2.0, 600, 1500, 0.6)
    if t > t102 - 0.3:
        x0 = 600 + 900 * clamp((t - t0) / (t1 + 2.0 - t0)) - 420
        B.townsfolk(cr, t, (x0, x0 - 170, x0 - 340, x0 - 510), 0.5, alpha=prog(t, t102 - 0.3, 0.5), blur=1)
    return dict(eve=0.3)


def s_vishnu(cr, t, tl, t0, t1):
    """u104-u107: Brahma and the gods in the sky; Rama steps into the Sarayu and returns to his true form, Vishnu
    (a great blue-gold light); those who followed rise to heaven as lights."""
    t105, t106, t107 = B.ls(tl, "u105"), B.ls(tl, "u106"), B.ls(tl, "u107")
    B.sky(cr, t, 0.8)
    brahma(cr, t, 380, 470, 0.36, alpha=prog(t, t0, 0.5))
    B.lights(cr, t, 1500, 300, 260, 16, prog(t, t0 + 0.3, 0.5))
    B.ground(cr)
    B.river(cr, t, GL - 60, 200)
    if t < t106:
        sink = 180 * ease(clamp((t - t105 - 0.3) / 1.6))
        B.rama(cr, t, 1000, 0.62, y=GL - 434 * 0.62 + sink, **B.ANJ)
    g = prog(t, t106 - 0.2, 0.8)
    if g > 0.01:
        B.glow(cr, 1000, GL - 380, 520, g)
        B.warm(cr, 1000, GL - 380, 420, g, col=(0.45, 0.62, 1.0))
        B.orb(cr, t, 1000, GL - 420, 60 * g, g)
        B.burst(cr, t, 1000, GL - 420, t106, rmax=900, alpha=0.7)
    if t > t107 - 0.2:
        for i in range(10):
            u = clamp((t - t107 - 0.1 * i) / 3.0)
            B.orb(cr, t, 300 + 140 * i, GL - 80 - 700 * ease(u), 12, (1 - u) * prog(t, t107, 0.3))
    return dict(eve=0.2, flash=flash_at(t, t106, 0.35))


def s_end(cr, t, tl, t0, t1):
    """u108-u111: the three together; Rama alone, the hero who beat Ravana lost his family to his duty; Sita fades,
    then Lakshmana; the question: a king's duty, or the family?"""
    t109, t110, t111 = B.ls(tl, "u109"), B.ls(tl, "u110"), B.ls(tl, "u111")
    B.ground(cr)
    B.glow(cr, 960, GL - 350, 520, 0.6)
    if t < t111:
        B.sita(cr, t, 600, 0.6, alpha=1 - prog(t, t110 + 0.2, 0.6))
        B.lakshmana(cr, t, 1320, 0.6, flip=True, alpha=1 - prog(t, t110 + 1.4, 0.6))
        B.rama(cr, t, 960, 0.64, head=0.15 * (t > t109))

        def ui0(cr_):
            return None
        return dict(ui=ui0, night=0.2)
    B.rama(cr, t, 960, 0.5, head=0.15)

    def ui(cr_):
        B.card(cr_, t, t111 + 0.2, 520, 360, "राजा का धर्म?", "प्रजा पहले")
        B.card(cr_, t, t111 + 1.2, 1400, 360, "परिवार?", "अपने पहले")
        if t > t111 + 1.6:
            n = int((t - t111 - 1.6) / 0.9)
            B.red_ring(cr_, (520, 1400)[n % 2], 364, 240, 150, prog(t, t111 + 1.6 + 0.9 * n, 0.35), 9)
    return dict(ui=ui, night=0.3)
