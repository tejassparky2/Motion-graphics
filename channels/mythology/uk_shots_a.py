"""Shots u001-u055 of the Uttara Kanda long video (hook, the happy years, the rumour, Sita in the forest, Lava and
Kusha). Each shot covers one to six lines and changes its picture at the lines named in it; the fast camera adds a
new framing at every line. Every shot: (cr, t, tl, t0, t1) -> dict(ui=..., flash=..., night=..., eve=...)."""
import math

import uk_base as B
from poster import clamp, ease, prog
from puppet_core import depth, keyed, prop
from scenes_jayadratha import flash_at
from scenes_ravana import rv, rv_angles

GL = B.GL


def s_movie(cr, t, tl, t0, t1):
    """u001-u002: the film's ending (Rama's arrow, Ravana falls), then Valmiki's book glows: the story goes on."""
    tF, tB = B.lf(tl, "u001", 0.45), B.ls(tl, "u002")
    B.sky(cr, t, 0.6)
    B.ground(cr)
    fall = ease(clamp((t - tF) / 1.0))
    rs = 0.72
    rv(cr, t, 1340 + 60 * fall, GL - 434 * rs + 120 * fall, rs, rot=-0.9 * fall, flip=True,
       mood="angry" if t < tF else "calm", alpha=1 - 0.6 * prog(t, tB, 0.5), rods=False)
    B.rama(cr, t, 420, 0.7, front=(-1.6, 0.0), backa=(-1.5, -0.1), hits=[(tF - 0.2, 0.5)])
    if t > tF - 0.3:
        u = clamp((t - tF + 0.3) / 0.3)
        B.trail(cr, [(640, GL - 470), (640 + 620 * u, GL - 470 - 10 * u)], 1 - prog(t, tF + 0.4, 0.3))
    B.book(cr, t, tB, 960, 470, 1.6)
    return dict(flash=flash_at(t, tF, 0.25), eve=0.35)


def s_flash_sita(cr, t, tl, t0, t1):
    """u003: Sita alone in the forest."""
    B.forest(cr, t)
    B.sita(cr, t, 960, 0.7, front=B.HEART["front"], backa=B.HEART["backa"], head=0.15)
    return dict(night=0.3)


def s_flash_boys(cr, t, tl, t0, t1):
    """u004: two boys singing before Rama on his throne; he does not know them."""
    B.palace(cr)
    prop(cr, "kk_throne", 1350, GL, 0.7)
    B.rama(cr, t, 1350, 0.66, flip=True, front=(-0.4, -0.6))
    for x in (560, 760):
        B.boy(cr, t, x, 0.46, front=(-1.2, -0.6))
    B.notes(cr, t, 660, 560)

    def ui(cr_):
        B.qmark(cr_, t, t0 + 0.6, 1350, 300, 160)
    return dict(ui=ui)


def s_flash_lk(cr, t, tl, t0, t1):
    """u005: Lakshmana alone by the river, eyes down."""
    B.ground(cr)
    B.river(cr, t, GL - 40, 160)
    B.lakshmana(cr, t, 960, 0.66, kneel="uk_lk_kneel", head=0.25, **B.ANJ)
    return dict(night=0.35)


def s_books(cr, t, tl, t0, t1):
    """u006-u008: the last book, the Uttara Kanda; Ramcharitmanas (no) and Valmiki (yes); 'let's hear it'."""
    t7, t8 = B.ls(tl, "u007"), B.ls(tl, "u008")
    a6 = 1 - prog(t, t7 - 0.2, 0.3)
    if a6 > 0.01:
        B.book(cr, t, t0, 960, 520, 2.0, a6)
    if t > t7 - 0.3:
        q = prog(t, t7 - 0.3, 0.3) * (1 - prog(t, t8, 0.4))
        B.book(cr, t, t7 - 0.3, 620, 560, 1.3, 0.4 * q)
        B.book(cr, t, t7 - 0.3, 1300, 560, 1.3, 1.0 * q)
    if t > t8 - 0.2:
        B.forest(cr, t)
        B.rama(cr, t, 960, 0.66, alpha=prog(t, t8, 0.4))

    def ui(cr_):
        if t7 - 0.3 < t < t8:
            B.card(cr_, t, t7 - 0.2, 620, 300, "रामचरितमानस", "ये हिस्सा नहीं")
            B.card(cr_, t, t7 + 0.4, 1300, 300, "वाल्मीकि रामायण", "ये हिस्सा है")
    return dict(ui=ui)


def s_return(cr, t, tl, t0, t1):
    """u009-u010: the three walk home to Ayodhya; Rama is crowned, people cheer, petals."""
    t10 = B.ls(tl, "u010")
    prop(cr, "mt_city", 1450, GL - 20, 0.62, alpha=0.9, blur=3)
    B.ground(cr)
    if t < t10:
        B.walker(cr, t, B.rama, t0, t10, 300, 760, 0.6)
        B.walker(cr, t, B.lakshmana, t0, t10, 60, 520, 0.58)
        B.sita(cr, t, 120 + 460 * clamp((t - t0) / max(0.5, t10 - t0)), 0.56)
    else:
        prop(cr, "kk_throne", 960, GL, 0.7)
        pts = B.rama(cr, t, 960, 0.62, front=(-0.3, -0.6), hits=[(t10, 0.4)])
        prop(cr, "kk_crown", 960 + 8, GL - 640, 0.5, alpha=prog(t, t10, 0.4))
        B.townsfolk(cr, t, (200, 360, 520), 0.52, front=(-2.3, 0.2))
        B.townsfolk(cr, t, (1400, 1560, 1720), 0.52, flip=True, front=(-2.3, 0.2))
        B.petals(cr, t, t10, 300, 1600)
    return {}


def s_wish(cr, t, tl, t0, t1):
    """u011-u014: Rama and Sita in the palace; Sita expecting (soft lights); her wish: the hermitages on the Ganga."""
    t12, t13, t14 = B.ls(tl, "u012"), B.ls(tl, "u013"), B.ls(tl, "u014")
    B.palace(cr)
    B.warm(cr, 1180, GL - 380, 260, 0.6)
    B.lights(cr, t, 1180, GL - 400, 200, 10, 0.8)
    B.sita(cr, t, 1180, 0.64, flip=True, front=(-0.3, -0.7) if t > t13 else (-0.08, -0.35), hits=[(t13, 0.4)])
    B.rama(cr, t, 720, 0.66, front=(-1.0, -0.6) if t12 < t < t14 else (-0.3, -0.5),
           head=0.12 * prog(t, t14, 0.2) * (1 - prog(t, t14 + 0.6, 0.2)), hits=[(t12, 0.4), (t14, 0.3)])

    def ui(cr_):
        q = B.bubble(cr_, t, t13 - 0.1, 1420, 330, 1.3)
        if q > 0.01:
            prop(cr_, "lr_hut", 1380, 420, 0.32, alpha=q)
            prop(cr_, "lr_hut", 1500, 410, 0.26, alpha=q)
            cr_.save()
            cr_.rectangle(1270, 430, 330, 28)
            cr_.set_source_rgba(0.3, 0.5, 0.9, 0.6 * q)
            cr_.fill()
            cr_.restore()
    return dict(ui=ui, eve=0.15)


def s_court(cr, t, tl, t0, t1):
    """u015-u017: night; Rama asks his friends; one stays silent, then speaks, afraid."""
    t16, t17 = B.ls(tl, "u016"), B.ls(tl, "u017")
    B.palace(cr)
    prop(cr, "kk_throne", 520, GL, 0.68)
    B.rama(cr, t, 520, 0.64, front=(-1.1, -0.5), hits=[(t0 + 0.3, 0.3)])
    for i, x in enumerate((1100, 1320, 1540)):
        rig, key = B.TOWN[i]
        speak = i == 0 and t > t17
        B.man(cr, t, rig, key, x, 0.58, flip=True, head=0.2 if (i == 0 and t16 < t < t17) else 0.0,
              front=(-1.3, -0.4) if speak else (-0.3, -0.5), hits=[(t17, 0.4)] if i == 0 else ())
    return dict(night=0.45)


def s_rumour(cr, t, tl, t0, t1):
    """u018-u020: the rumour: Lanka with Sita; the king brings her home; townspeople whisper."""
    t19, t20 = B.ls(tl, "u019"), B.ls(tl, "u020")
    B.palace(cr, 0.5)
    if t < t20:
        q = B.bubble(cr, t, t0, 960, 480, 2.2)
        if t < t19:
            prop(cr, "rv_lanka", 960, 600, 0.5, alpha=q)
            B.sita(cr, t, 960, 0.3, feet=640, rods=False, alpha=q, front=B.HEART["front"])
        else:
            B.rama(cr, t, 860, 0.3, feet=640, rods=False, alpha=q)
            B.sita(cr, t, 1040, 0.3, feet=640, rods=False, alpha=q, flip=True)
    else:
        B.townsfolk(cr, t, (260, 460, 660, 1260, 1460, 1660), 0.56, front=(-1.6, -0.9), blur=0)

        def ui(cr_):
            for x in (560, 1360):
                B.qmark(cr_, t, t20 + 0.2, x, 330, 120)
        return dict(ui=ui, night=0.3)
    return dict(night=0.3)


def s_heart(cr, t, tl, t0, t1):
    """u021-u023: Rama heartbroken; he knows Sita is pure (her image in gold); but a king must listen."""
    t22, t23 = B.ls(tl, "u022"), B.ls(tl, "u023")
    B.palace(cr, 0.6)
    B.red_spot(cr, 960, GL - 420, 420, 0.5 * (1 - prog(t, t22, 0.4)))
    B.rama(cr, t, 960 if t < t23 else 960, 0.74, head=0.28, front=B.HEART["front"], backa=B.HEART["backa"])
    if t22 - 0.2 < t < t23:
        q = B.bubble(cr, t, t22 - 0.2, 1420, 330, 1.2)
        B.warm(cr, 1420, 360, 160, q)
        B.sita(cr, t, 1420, 0.3, feet=470, rods=False, alpha=q)

    def ui(cr_):
        if t > t23 - 0.1:
            B.card(cr_, t, t23 - 0.1, 480, 330, "प्रजा", "राजा का फ़र्ज़")
            B.card(cr_, t, t23 + 0.5, 1440, 330, "सीता", "पति का प्यार")
    return dict(ui=ui, night=0.25)


def s_order(cr, t, tl, t0, t1):
    """u024-u025: Rama calls his brothers; tells Lakshmana to leave Sita across the Ganga; Lakshmana is shocked."""
    t25 = B.ls(tl, "u025")
    B.palace(cr)
    B.rama(cr, t, 560, 0.66, front=(-1.2, -0.4) if t > t25 else (-0.3, -0.5), hits=[(t25, 0.4)])
    B.lakshmana(cr, t, 1000, 0.62, flip=True, **(dict(front=B.HEART["front"], backa=B.HEART["backa"], head=0.12)
                                                  if t > t25 + 0.8 else B.ANJ))
    B.bharata(cr, t, 1260, 0.6, flip=True, **B.ANJ)
    B.bharata(cr, t, 1500, 0.58, flip=True, **B.ANJ)
    return dict(night=0.15, flash=flash_at(t, t25 + 0.8, 0.12))


def s_question1(cr, t, tl, t0, t1):
    """u026: was Rama right? as a king, or as a husband? (two cards, a red ring switching)"""
    B.ground(cr)
    B.glow(cr, 960, GL - 320, 380, 0.7)
    B.rama(cr, t, 960, 0.5, head=0.2)

    def ui(cr_):
        B.card(cr_, t, t0 + 0.4, 520, 360, "राजा की तरह?", "प्रजा की सुनी")
        B.card(cr_, t, t0 + 1.4, 1400, 360, "पति की तरह?", "सीता को छोड़ा")
        if t > t0 + 1.8:
            n = int((t - t0 - 1.8) / 0.9)
            B.red_ring(cr_, (520, 1400)[n % 2], 364, 260, 150, prog(t, t0 + 1.8 + 0.9 * n, 0.35), 9)
    return dict(ui=ui, night=0.3)


def s_chariot(cr, t, tl, t0, t1):
    """u027-u028: morning; Sita happily in the chariot with Lakshmana; trees slide past."""
    B.ground(cr)
    off = (t - t0) * 260
    for i in range(5):
        x = (2200 - (off + i * 520)) % 2600 - 300
        prop(cr, "dv_tree", x, GL + 10, 0.5, alpha=0.6, blur=6)
    cx = 960 + 10 * math.sin(t * 6)
    B.sita(cr, t, cx + 90, 0.5, feet=GL - 80, rods=False, front=(-0.4, -0.9))
    B.lakshmana(cr, t, cx - 120, 0.52, feet=GL - 80, rods=False, head=0.15, front=(-1.0, -0.4))
    prop(cr, "jt_chariot", cx, GL - 40, 0.62)
    return dict(eve=0.1)


def s_truth(cr, t, tl, t0, t1):
    """u029-u031: across the Ganga Lakshmana weeps; he tells her; Sita falls."""
    t30, t31 = B.ls(tl, "u030"), B.ls(tl, "u031")
    B.forest(cr, t, trees=((1780, 0.66, 4, 0.85, False),))
    B.river(cr, t, GL - 30, 130)
    fall = ease(clamp((t - t31 - 0.2) / 0.7))
    B.sita(cr, t, 1100, 0.66, flip=True, rot=0.9 * fall, y=GL - 470 * 0.66 + 150 * fall,
           front=B.HEART["front"] if t > t30 + 0.5 else (-0.08, -0.35))
    B.lakshmana(cr, t, 700, 0.64, head=0.3 if t < t30 else 0.1,
                front=(-2.2, -0.9) if t < t30 else (-1.2, -0.4), hits=[(t30, 0.4)])
    return dict(flash=flash_at(t, t31 + 0.2, 0.15), night=0.15)


def s_message(cr, t, tl, t0, t1):
    """u032-u035: Sita speaks: she would give her life to the Ganga, but she carries the royal line; 'tell Rama I
    am not sad for myself'; Lakshmana goes back weeping."""
    t33, t34, t35 = B.ls(tl, "u033"), B.ls(tl, "u034"), B.ls(tl, "u035")
    B.forest(cr, t, trees=((1780, 0.66, 4, 0.85, False),))
    B.river(cr, t, GL - 30, 130)
    B.sita(cr, t, 1050, 0.66, flip=True, front=(-0.3, -0.5) if t < t34 else B.ANJ["front"],
           backa=B.ANJ["backa"] if t > t34 else (0.15, -0.2), hits=[(t33, 0.3)])
    if t33 - 0.2 < t < t35:
        B.warm(cr, 1040, GL - 330, 140, prog(t, t33 - 0.2, 0.4))
        B.lights(cr, t, 1040, GL - 330, 120, 8, prog(t, t33 - 0.2, 0.4))
    if t < t35:
        B.lakshmana(cr, t, 640, 0.64, head=0.25, **B.ANJ)
    else:
        B.walker(cr, t, B.lakshmana, t35, t35 + 2.8, 640, 120, 0.64, flip=True, head=0.25)
    return dict(night=0.2)


def s_valmiki(cr, t, tl, t0, t1):
    """u036-u039: a sage comes to the weeping Sita: Valmiki, who wrote the Ramayana; he takes her to his hermitage."""
    t37, t38, t39 = B.ls(tl, "u037"), B.ls(tl, "u038"), B.ls(tl, "u039")
    B.forest(cr, t, hut=(1700, 0.62))
    if t < t39:
        B.sita(cr, t, 620, 0.64, head=0.15, front=B.HEART["front"], backa=B.HEART["backa"])
        x = 1500 - 500 * ease(clamp((t - t0) / max(0.6, t37 - t0)))
        B.valmiki(cr, t, x, 0.64, flip=True, front=(-1.2, -0.4) if t > t37 else (-0.3, -0.5))
        B.book(cr, t, t38, x, 330, 0.9)
    else:
        B.walker(cr, t, B.valmiki, t39, t39 + 3.2, 1000, 1500, 0.64)
        B.sita(cr, t, 820 + 500 * clamp((t - t39) / 3.2), 0.62)
    return dict(eve=0.15)


def s_twins(cr, t, tl, t0, t1):
    """u040-u041: in the hermitage Sita has twin sons, Lava and Kusha (two cradles glowing)."""
    t41 = B.ls(tl, "u041")
    B.forest(cr, t, hut=(1600, 0.62))
    B.sita(cr, t, 700, 0.62, front=(-1.0, -0.8))
    for x in (980, 1180):
        B.warm(cr, x, GL - 120, 150, prog(t, t0 + 0.4, 0.4))
        prop(cr, "c6_rama_cradle", x, GL - 40, 0.42, alpha=prog(t, t0 + 0.3, 0.4))

    def ui(cr_):
        if t > t41:
            for x, name in ((980, "लव"), (1180, "कुश")):
                B.label(cr_, t, t41 + (0.1 if name == "लव" else 0.6), name, t1 - 0.1, x=x, y=GL - 300, size=70,
                        col=B.RED)
    return dict(ui=ui, eve=0.1)


def s_teach(cr, t, tl, t0, t1):
    """u042-u045: Valmiki teaches the boys a long song: the whole Ramayana, their own father's story; they don't know."""
    t43, t44, t45 = B.ls(tl, "u043"), B.ls(tl, "u044"), B.ls(tl, "u045")
    B.forest(cr, t, hut=(1700, 0.62))
    B.valmiki(cr, t, 560, 0.64, front=(-1.3, -0.5), hits=[(t0 + 0.3, 0.3), (t43, 0.3)])
    for i, x in enumerate((1000, 1200)):
        B.boy(cr, t, x, 0.48, flip=True, front=(-1.0, -0.8) if t < t45 else (-0.3, -0.5), head=0.1 * (t > t45))
    B.notes(cr, t, 1100, 520, prog(t, t0 + 0.4, 0.4))
    if t43 - 0.2 < t < t44 + 0.2:
        B.book(cr, t, t43 - 0.2, 760, 300, 1.0)

    def ui(cr_):
        q = B.bubble(cr_, t, t44 - 0.1, 1100, 300, 1.1)
        if q > 0.01:
            B.rama(cr_, t, 1100, 0.26, feet=420, rods=False, alpha=q)
        if t > t45:
            for x in (1000, 1200):
                B.qmark(cr_, t, t45 + 0.1, x, 480, 90)
    return dict(ui=ui)


def s_yagya(cr, t, tl, t0, t1):
    """u046-u048: years later Rama's great sacrifice; he never married again; a golden Sita sits beside him."""
    t47, t48 = B.ls(tl, "u047"), B.ls(tl, "u048")
    B.palace(cr, 0.4)
    B.ground(cr)
    fx, fy = 1300, GL - 60                           # the sacred fire
    B.warm(cr, fx, fy - 80, 220, 0.9 + 0.1 * math.sin(t * 9), col=(1.0, 0.55, 0.15))
    B.lights(cr, t, fx, fy - 120, 120, 12, 1.0, col=(1.0, 0.62, 0.2), speed=0.9)
    prop(cr, "jt_pyre", fx, GL, 0.35)
    B.rama(cr, t, 620, 0.62, front=(-0.6, -1.0), hits=[(t47, 0.3)])
    if t > t47 - 0.3:
        g = prog(t, t47 - 0.3, 0.5)
        B.warm(cr, 880, GL - 330, 220, g * (0.8 + 0.2 * math.sin(t * 3)))
        B.sita(cr, t, 880, 0.6, flip=True, alpha=0.75 * g, rods=False)
        for i in range(6):
            B.sparkle(cr, 880 + 90 * math.sin(i * 1.7 + t), GL - 300 - 160 * math.cos(i * 2.3 + t), 22, g)

    def ui(cr_):
        if t > t48:
            B.red_ring(cr_, 880, GL - 300, 170, 320, prog(t, t48 + 0.2, 0.4), 8)
    return dict(ui=ui, eve=0.2)


def s_song(cr, t, tl, t0, t1):
    """u049-u052: Valmiki brings the boys; they sing the Ramayana before Rama; people see they look just like him."""
    t50, t51, t52 = B.ls(tl, "u050"), B.ls(tl, "u051"), B.ls(tl, "u052")
    B.palace(cr)
    prop(cr, "kk_throne", 1480, GL, 0.66)
    B.rama(cr, t, 1480, 0.62, flip=True, head=0.12 * (t > t51), front=(-0.4, -0.6))
    xb = 620 + 160 * ease(clamp((t - t0) / max(0.6, t50 - t0)))
    B.valmiki(cr, t, xb - 300, 0.62, front=(-0.6, -0.6))
    for x in (xb, xb + 190):
        B.boy(cr, t, x, 0.46, front=(-1.3, -0.6) if t > t50 else (-0.3, -0.5))
    if t > t50:
        B.notes(cr, t, xb + 95, 560)
    if t > t52 - 0.2:
        B.townsfolk(cr, t, (1080, 1240), 0.52, flip=True, front=(-2.3, 0.2), alpha=prog(t, t52 - 0.2, 0.3))
    return dict(eve=0.1)


def s_gold(cr, t, tl, t0, t1):
    """u053-u055: Rama offers gold; the boys refuse ('what would hermits do with gold?'); then Rama learns they
    are Sita's sons, his own."""
    t54, t55 = B.ls(tl, "u054"), B.ls(tl, "u055")
    B.palace(cr)
    B.rama(cr, t, 1380, 0.64, flip=True, front=(-1.3, -0.4) if t < t55 else (-1.6, -0.2), hits=[(t55, 0.5)])
    if t < t55:
        for i in range(7):
            B.orb(cr, t, 1180 + 30 * (i % 4), GL - 380 - 26 * (i // 4), 14, 1 - prog(t, t54 + 0.6, 0.4))
    for x in (640, 830):
        B.boy(cr, t, x, 0.48, front=(-2.4, 0.4) if t54 - 0.4 < t < t55 else (-0.3, -0.5))
    if t > t55 - 0.1:
        g = prog(t, t55 - 0.1, 0.6)
        B.glow(cr, 1000, GL - 350, 520, g)
        B.trail(cr, B.arc_path((1250, GL - 420), (900, GL - 330), 120, 30, g), 0.8 * g)
    return dict(flash=flash_at(t, t55 + 0.3, 0.2))
