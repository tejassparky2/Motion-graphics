"""Explainer 5: "Rabies: The Vaccine Works. So Why Do Thousands Still Die?" Made 30 Oct 2026 under the owner's
standing approval ("make new video auto approved from next"; "Next video"), in the Toxoplasma video's photo style
and the rabies-reel shape (the cure exists, so why do people still die?). Script and sources:
research_notes/explainer_5_rabies.md."""
import json
import math
import os

from poster import (CORAL, CREAM, GOLD, GREEN, INK, MARGIN, RED, W, _along, _round, calendar, card, clamp, counter,
                    cross, draw_text, footnote, gauge, headline, icon_array, magnifier, path, photo, photo_width, prog,
                    ring, stamp, strike, text_size, tick, yes_no_card)

# the narrator, music and pauses are channel-wide; render_doc reads them from this module
from channel import ASSETS_ROOT, GAP, REPO, MUSIC, NARRATOR, REVEAL_GAP, TAIL  # noqa: F401
from shots import T, checklist, draw_frame, pic, starts

SCRIPT = [
    dict(id="b1", text="Imagine you're very thirsty. But the moment you see water, your throat locks up in fear."),
    dict(id="b2", text="And it all started with a small scratch from a puppy. Weeks ago. You'd already forgotten it."),
    dict(id="b3", text="And by now, it's too late."),
    dict(id="b4", text="This isn't a zombie movie. It's real."),
    dict(id="b5", text="It's called rabies.", gap=REVEAL_GAP),
    dict(id="b6", text="In India, there are about nine million animal bites every year. Three out of four are from "
                       "dogs."),
    dict(id="b7", text="And an estimated five thousand seven hundred people die of rabies. Every year."),
    dict(id="b8", text="So how does a tiny scratch reach your brain?"),
    dict(id="b9", text="The virus lives in the saliva of an infected animal. A bite, a scratch, or a lick on broken "
                       "skin can let it in."),
    dict(id="b10", text="Then it climbs your nerves. Slowly. All the way up to your brain."),
    dict(id="b11", text="That's why it can hide for weeks, or even months, while you feel completely fine."),
    dict(id="b12", text="A bite on the face reaches the brain faster."),
    dict(id="b13", text="When it gets there, the signs begin. Fever. A strange tingling where you were bitten."),
    dict(id="b14", text="Then swallowing hurts so much that the throat goes into spasms. Even the sight of water can "
                        "set them off."),
    dict(id="b15", text="Once these signs start, rabies is almost always fatal."),
    dict(id="b16", text="But here's the strange part. There's a vaccine. And it works, even after the bite.",
         gap=REVEAL_GAP),
    dict(id="b17", text="So why do thousands still die?"),
    dict(id="b18", text="Because many people never get it. In one big study, more than one in five people bitten by a "
                        "dog got no vaccine at all."),
    dict(id="b19", text="And about half of those who started the shots never finished them."),
    dict(id="b20", text="Some put turmeric or chilli on the wound. Some go to a healer instead. Some think it was "
                        "just a puppy."),
    dict(id="b21", text="And no, it's not fourteen injections in the stomach anymore. Today, it's a few shots in the "
                        "arm."),
    dict(id="b22", text="So, if an animal bites or scratches you, wash the wound with soap and running water, for "
                        "fifteen minutes."),
    dict(id="b23", text="Then go to a hospital the same day. Even for a small scratch. Even if it was a puppy."),
    dict(id="b24", text="And finish every single dose."),
    dict(id="b25", text="Rabies kills almost everyone it reaches. But the vaccine can stop it, if you don't wait.",
         gap=REVEAL_GAP),
    dict(id="b26", text="Has a dog ever bitten or scratched you? Yes or no, tell me in the comments."),
]
for _b in SCRIPT:
    _b.setdefault("scene", _b["id"])
for _b in SCRIPT[1:]:
    _b.setdefault("gap", GAP)


METADATA = dict(
    title="Rabies: The Vaccine Works. So Why Do Thousands Still Die?",
    alt_titles=["A Puppy Scratch Can Kill You Months Later", "Why Rabies Makes You Afraid of Water",
                "The Disease That Climbs Your Nerves to Your Brain"],
    caption="Thirsty, but terrified of water 😳 That's rabies, and it still kills an estimated 5,700 people in India "
            "every year.\n\n"
            "If an animal bites or scratches you:\n✅ Wash the wound with soap and running water for 15 minutes\n"
            "✅ Go to a hospital the same day, even for a small scratch, even if it was a puppy\n"
            "✅ Finish every dose of the vaccine\n"
            "❌ No turmeric, chilli or anything else on the wound\n"
            "❌ It's not 14 injections in the stomach anymore: today it's a few shots in the arm\n\n"
            "Once the signs start, rabies is almost always fatal. The vaccine works, if you don't wait.\n\n"
            "Has a dog ever bitten or scratched you? Comment YES or NO 👇",
    yt_title="Why Rabies Makes You Afraid of Water 😳",
    yt_description="Rabies climbs your nerves to your brain, and once the signs start it's almost always fatal. "
                   "In India there are about 9 million animal bites a year, three in four from dogs, and an estimated "
                   "5,700 rabies deaths. The vaccine works even after the bite, so why do people still die?\n\n"
                   "If an animal bites or scratches you:\n✅ Wash the wound with soap and running water for 15 minutes\n"
                   "✅ Go to a hospital the same day, even for a small scratch\n"
                   "✅ Finish every dose of the vaccine\n"
                   "❌ No turmeric, chilli or anything else on the wound\n\n"
                   "General information, not medical advice.",
    hashtags=["#rabies", "#dogbite", "#healthawareness", "#india", "#sciencefacts"],
    tags=["rabies", "dog bite", "rabies vaccine", "hydrophobia", "fear of water", "anti rabies vaccine", "india",
          "stray dogs", "health facts", "science explained"],
    pinned_comment="Has a dog ever bitten or scratched you? 🐕 YES or NO? 👇",
    sources=["WHO, Rabies fact sheet",
             "CDC, Rabies: how it spreads, symptoms",
             "ICMR-National Institute of Epidemiology, The Lancet Infectious Diseases, 2025, burden of human rabies "
             "deaths and animal bites in India 2022-23",
             "Ministry of Health and Family Welfare, National Action Plan for Dog Mediated Rabies Elimination"],
)


# ---------- photos ----------
# Same sourcing as explainer 4 (the Hinglish chat's one-off search; cut out with rembg and checked on the paper).
# Shared cut-outs (mannequin, glass, thermometer, doctor, TV, tap...) come from the amoeba folder.
ASSETS = os.path.join(ASSETS_ROOT, "rabies")
SHARED = os.path.join(ASSETS_ROOT, "amoeba")
_FILES = {
    "mq_run": "mq_run.png", "mq_head": "mq_head.png", "mq_sit": "mq_sit.png", "glass": "glass.png",
    "thermometer": "thermometer.png", "doctor": "doctor.png", "tv": "tv_legs.png", "tap": "tap.png",
    "head_lineart": "head_lineart.png", "headache_man": "headache_man.png",
    "dog_street": "dog_street.png", "puppy": "puppy.png", "dog_snarl": "dog_snarl.png", "cat": "cat.png",
    "monkey": "monkey.png", "scratch": "scratch.jpg", "throat": "throat.png", "vaccine": "vaccine.png",
    "injection_arm": "injection_arm.jpg", "hospital": "hospital.jpg", "wash_hands": "wash_hands.jpg",
    "soap": "soap.png", "turmeric": "turmeric.png", "chillies": "chillies.png", "stopwatch": "stopwatch.png",
    "clapper": "clapper.png", "bandage": "bandage.png", "dog_lick": "dog_lick.jpg", "street_dogs": "street_dogs.jpg",
    "child_dog": "child_dog.jpg", "drinking": "drinking.png",
}
P = {}
for _k, _v in _FILES.items():
    for _d in (ASSETS, SHARED):
        if os.path.exists(os.path.join(_d, _v)):
            P[_k] = os.path.join(_d, _v)
            break
USED_ASSETS = [os.path.basename(v) for v in P.values()]
CREDITS_FILES = [os.path.join(ASSETS, "credits.json"), os.path.join(SHARED, "credits.json")]

VIRUS = (0.66, 0.16, 0.18)          # the rabies virus, the same in every shot (the recurring "intruder")
NERVE = (0.95, 0.78, 0.30)
WATER = (0.45, 0.72, 0.85)
MQ_HEAD = {"mq_run": (0.62, 0.075), "mq_head": (0.60, 0.075), "mq_sit": (0.50, 0.08)}
TV_SCREEN = (0.11, 0.06, 0.66, 0.385)
# mq_run: the nerve way from the front hand up the arm to the brain (fractions of the cut-out)
ARM_ROUTE = [(0.96, 0.44), (0.73, 0.36), (0.61, 0.26), (0.60, 0.18), (0.62, 0.08)]


def _pic(cr, key, cx, cy, h, t, t0, **kw):
    pic(cr, P.get(key), cx, cy, h, t, t0, **kw)


def cut(cr, key, cx, cy, h, alpha=1.0, **kw):
    """A cut-out photo centred at (cx, cy), `h` px tall; returns a (u, v) -> (x, y) mapper for points on it."""
    if key not in P:
        return lambda u, v: (cx + (u - 0.5) * h * 0.7, cy + (v - 0.5) * h)
    photo(cr, P[key], cx, cy, h, alpha=alpha, **kw)
    w = photo_width(P[key], h)
    flip = kw.get("flip")
    return lambda u, v: (cx + ((0.5 - u) if flip else (u - 0.5)) * w, cy + (v - 0.5) * h)


# ---------- drawn pieces ----------

def virus(cr, x, y, s, rot=0.0, alpha=1.0, t=0.0):
    """The rabies virus as it looks under the electron microscope: a bullet, one end round, one end flat, with
    short spikes all round and stripes across (the coiled core). s = length in px."""
    if alpha <= 0:
        return
    w = s * 0.42
    cr.save()
    cr.translate(x, y)
    cr.rotate(rot + 0.06 * math.sin(t * 3))
    cr.set_line_cap(1)
    cr.set_source_rgba(*VIRUS, 0.9 * alpha)                   # spikes
    cr.set_line_width(max(1.5, s * 0.025))
    for i in range(18):
        f = i / 17
        px = -s / 2 + w / 2 + f * (s - w / 2)
        for sy in (-1, 1):
            cr.move_to(px, sy * w / 2)
            cr.line_to(px, sy * (w / 2 + s * 0.06))
            cr.stroke()
    for i in range(7):                                        # spikes round the nose
        a = math.pi / 2 + math.pi * (i + 0.5) / 7
        cr.move_to(-s / 2 + w / 2 + w / 2 * math.cos(a), w / 2 * math.sin(a))
        cr.line_to(-s / 2 + w / 2 + (w / 2 + s * 0.06) * math.cos(a), (w / 2 + s * 0.06) * math.sin(a))
        cr.stroke()
    cr.new_path()                                             # body
    cr.arc(-s / 2 + w / 2, 0, w / 2, math.pi / 2, 3 * math.pi / 2)
    cr.line_to(s / 2, -w / 2)
    cr.line_to(s / 2, w / 2)
    cr.close_path()
    cr.set_source_rgba(*VIRUS, alpha)
    cr.fill_preserve()
    cr.set_source_rgba(0.30, 0.05, 0.06, alpha)
    cr.set_line_width(max(2, s * 0.03))
    cr.stroke()
    cr.set_source_rgba(0.98, 0.85, 0.80, 0.55 * alpha)       # the coiled core
    cr.set_line_width(max(1.5, s * 0.02))
    for i in range(8):
        px = -s / 2 + w * 0.6 + i * (s - w * 0.8) / 8
        cr.move_to(px, -w * 0.32)
        cr.line_to(px + s * 0.02, w * 0.32)
        cr.stroke()
    cr.restore()


def bite_marks(cr, x, y, s, p, color=RED, alpha=1.0):
    """Three short scratch lines drawn in as p goes 0..1."""
    for i in range(3):
        q = clamp(p * 3 - i)
        if q > 0:
            path(cr, [(x - s / 2 + i * s * 0.28, y - s / 2), (x - s / 2 + i * s * 0.28 + s * 0.45, y + s / 2)], q,
                 max(4, s * 0.06), color, 0.9 * alpha)


def spasm(cr, x, y, r, t, alpha=1.0):
    """Red zig-zag lines round a throat (spasms)."""
    for i, a in enumerate((-0.6, 0.0, 0.6)):
        for side in (-1, 1):
            cx, cy = x + side * r * math.cos(a), y + r * math.sin(a)
            j = 6 * math.sin(t * 25 + i)
            path(cr, [(cx, cy), (cx + side * 20, cy - 10 + j), (cx + side * 34, cy + 6 - j), (cx + side * 52, cy - 4)],
                 1.0, 6, RED, 0.85 * alpha)


def why(cr, t, t0, x, y, size=260):
    q = prog(t, t0, 0.3)
    draw_text(cr, "?", x, y, int(size * (0.8 + 0.2 * q)), RED, q, anchor="cm")


_INDIA = json.load(open(os.path.join(REPO, "assets", "maps", "india.json")))["india"]   # Natural Earth, public domain


def india(cr, x, y, h, alpha=1.0):
    """India's outline (Natural Earth), centred at (x, y), `h` px tall."""
    lat0, lat1, lon0, lon1 = 6.5, 37.2, 68.0, 97.5
    k = h / (lat1 - lat0)
    kx = k * math.cos(math.radians(22))
    for ring_ in _INDIA:
        cr.move_to(x + (ring_[0][0] - (lon0 + lon1) / 2) * kx, y - (ring_[0][1] - (lat0 + lat1) / 2) * k)
        for lon, lat in ring_[1:]:
            cr.line_to(x + (lon - (lon0 + lon1) / 2) * kx, y - (lat - (lat0 + lat1) / 2) * k)
        cr.close_path()
    cr.set_source_rgba(0.93, 0.89, 0.80, 0.95 * alpha)
    cr.fill_preserve()
    cr.set_source_rgba(*INK, alpha)
    cr.set_line_width(4)
    cr.stroke()


# ---------- shots ----------
# Built like the Hinglish channel's Toxoplasma video: a big photo cut-out or framed photo carries every shot, one mark
# on it, the headline above, a new picture every ~3 s cut on the spoken word; red = threat, green = what to do, gold =
# numbers; slate only for "inside the body". The wooden mannequin is "you"; the red bullet-shaped virus is the one
# recurring intruder.

def h_thirsty(cr, t, tl, t0):                            # b1 frame 0: "imagine you're very thirsty. But the moment..."
    tw = T(tl, "b1", "water")
    run = clamp(t / max(0.5, tw - 0.2))
    back = prog(t, tw, 0.35)
    x = 300 + 160 * run - 180 * back                       # walks to the glass, then jumps back from it
    cut(cr, "mq_run", x, 1150 - 20 * abs(math.sin(t * 8)) * (1 - back), 640, rot=-0.25 * back)
    X = cut(cr, "glass", 820, 1240, 520)
    x0, y0 = X(0.12, 0.40)
    x1, y1 = X(0.88, 0.97)
    cr.set_source_rgba(*WATER, 0.4)
    _round(cr, x0 + 18, y0, x1 - x0 - 36, y1 - y0, 26)
    cr.fill()
    if t >= tw:
        for i in range(4):                                  # shock lines from the head
            a = -2.6 + 0.45 * i
            hx, hy = x - 30, 1150 - 290
            path(cr, [(hx + 70 * math.cos(a), hy + 70 * math.sin(a)), (hx + 120 * math.cos(a), hy + 120 * math.sin(a))],
                 prog(t, tw + 0.05 * i, 0.2), 8, RED, 0.9)
    headline(cr, t, "THIRSTY, BUT AFRAID OF", "WATER", -1, 1.0, t_ghost=-1)


def h_throat(cr, t, tl, t0):                             # b1 "...your throat locks up in fear"
    X = cut(cr, "throat", W / 2, 1200, 900)
    tx, ty = X(0.5, 0.55)
    spasm(cr, tx, ty, 90, t, prog(t, T(tl, "b1", "locks"), 0.3))
    stamp(cr, t, "FEAR", T(tl, "b1", "fear"), 800, 760, 90)
    headline(cr, t, "YOUR THROAT", "LOCKS UP", t0, T(tl, "b1", "locks"))


def h_scratch(cr, t, tl, t0):                            # b2 "it all started with a small scratch from a puppy"
    _pic(cr, "puppy", 320, 1250, 560, t, t0)
    _pic(cr, "scratch", 760, 960, 0, t, T(tl, "b2", "scratch") - 0.2, frame=(440, 330), rot=0.04)
    bite_marks(cr, 760, 960, 110, prog(t, T(tl, "b2", "scratch"), 0.5))
    headline(cr, t, "IT STARTED WITH A", "SCRATCH", t0, T(tl, "b2", "scratch"))


def h_weeks(cr, t, tl, t0):                              # b2 "...weeks ago. You'd already forgotten it."
    calendar(cr, t, t0 + 0.1, 330, 950, ["WEEK 1", "WEEK 2", "WEEK 3", "WEEK 4", "WEEK 6"], "AFTER THE SCRATCH",
             interval=0.25, circle_last=False)
    _pic(cr, "mq_sit", 790, 1300, 600, t, t0 + 0.2)
    stamp(cr, t, "FORGOTTEN", T(tl, "b2", "forgotten"), 540, 1600, 70)
    headline(cr, t, "WEEKS", "AGO", t0, t0 + 0.2)


def h_late(cr, t, tl, t0):                               # b3 "and by now, it's too late"
    X = cut(cr, "mq_head", 420, 1150, 900)
    hx, hy = X(*MQ_HEAD["mq_head"])
    for i in range(5):
        virus(cr, hx - 40 + 30 * i, hy + 10 + 14 * math.sin(i * 2), 46, 0.3 * i, prog(t, t0 + 0.1 * i, 0.3), t + i)
    ring(cr, hx, hy, 120, 110, prog(t, t0 + 0.3, 0.4))
    stamp(cr, t, "TOO LATE", T(tl, "b3", "late"), 790, 1350, 90)
    headline(cr, t, "AND BY NOW, IT'S", "TOO LATE", t0, T(tl, "b3", "late"))


def _screen(cr, rect, t, on=1.0):
    """The TV's glass playing a "zombie movie" (the snarling dog in green night light), collapsing to a line as on -> 0."""
    sx, sy, sw, sh = rect
    if on <= 0:
        return
    vy = max(0.02, clamp(on * 2 - 1)) if on < 1 else 1.0
    vx = clamp(on * 2) if on < 1 else 1.0
    cx, cy = sx + sw / 2, sy + sh / 2
    cr.save()
    _round(cr, cx - sw * vx / 2, cy - sh * vy / 2, sw * vx, sh * vy, 24 * vy)
    cr.clip()
    cr.set_source_rgba(0.06, 0.08, 0.07, 1)
    cr.paint()
    if on >= 1:
        if "dog_snarl" in P:
            photo(cr, P["dog_snarl"], cx, cy + sh * 0.08, sh * 0.95, tint=(0.35, 0.55, 0.30), shadow=False)
        cr.set_source_rgba(0.2, 0.6, 0.2, 0.18 + 0.1 * math.sin(t * 13))
        cr.paint()
        cr.set_source_rgba(1, 1, 1, 0.06)
        for y in range(int(sy), int(sy + sh), 6):
            cr.rectangle(sx, y, sw, 2)
        cr.fill()
    else:
        cr.set_source_rgba(0.9, 0.95, 1.0, 1)
        cr.paint()
    cr.restore()


def h_movie(cr, t, tl, t0):                              # b4 "this isn't a zombie movie. It's real."
    tr = T(tl, "b4", "real")
    X = cut(cr, "tv", W / 2, 1150, 1050)
    x0, y0 = X(TV_SCREEN[0], TV_SCREEN[1])
    x1, y1 = X(TV_SCREEN[0] + TV_SCREEN[2], TV_SCREEN[1] + TV_SCREEN[3])
    _screen(cr, (x0, y0, x1 - x0, y1 - y0), t, on=1 - prog(t, tr - 0.1, 0.45))
    stamp(cr, t, "FICTION?", t0 + 0.6, 790, 1560, 60, rot=0.08)
    stamp(cr, t, "IT'S REAL", tr + 0.2, 330, 1560, 80, rot=-0.08)
    headline(cr, t, "THIS ISN'T A", "ZOMBIE MOVIE", t0, t0 + 0.4, strike_at=tr, struck=True)


def n_name(cr, t, tl, t0):                               # b5 "it's called rabies"
    _pic(cr, "dog_snarl", W / 2, 960, 720, t, t0)
    tn = T(tl, "b5", "rabies")
    for i, (txt, ty, sz, cue) in enumerate((("RABIES", 1380, 150, tn), ("A VIRUS", 1580, 70, tn + 0.4))):
        p = prog(t, cue, 0.3)
        if p > 0:
            tw_, th = text_size(txt, sz)
            cr.set_source_rgba(*RED, 0.92)
            cr.rectangle(MARGIN, ty - 12, (tw_ + 50) * p, th + 24)
            cr.fill()
            draw_text(cr, txt, MARGIN + 25, ty, sz, CREAM, clamp(p * 2 - 1))
    virus(cr, 820, 1640, 150, -0.2, prog(t, tn + 0.5, 0.3), t)
    headline(cr, t, "ITS NAME", "", t0, 1e9)


def n_bites(cr, t, tl, t0):                              # b6 "in India, about nine million animal bites every year"
    india(cr, 330, 1100, 680, prog(t, t0, 0.3))
    t9 = T(tl, "b6", "nine")
    counter(cr, t, t9 - 0.2, 760, 900, "9M", 170, color=GOLD)
    draw_text(cr, "BITES A YEAR", 760, 1030, 50, INK, prog(t, t9 + 0.2, 0.3), anchor="ct")
    for i in range(14):                                    # bite marks popping up across the map
        p = prog(t, t9 + 0.08 * i, 0.2)
        if p > 0:
            bx, by = 200 + (i * 97) % 280, 860 + (i * 151) % 420
            bite_marks(cr, bx, by, 34, p)
    footnote(cr, "ICMR-NIE survey, The Lancet Infectious Diseases, 2025", prog(t, t9, 0.3), y=1560)
    headline(cr, t, "INDIA, EVERY YEAR:", "9 MILLION BITES", t0, t9, big_size=130)


def n_dogs(cr, t, tl, t0):                               # b6 "three out of four are from dogs"
    keys = ("dog_street", "dog_street", "dog_street", "monkey" if "monkey" in P else "cat")
    for i, k in enumerate(keys):
        tc = t0 + 0.15 * i
        cx, cy = 290 + 500 * (i % 2), 820 + 520 * (i // 2)
        _pic(cr, k, cx, cy, 380, t, tc, flip=i % 2 == 1)
        if i < 3:
            ring(cr, cx, cy, 200, 200, prog(t, T(tl, "b6", "dogs") + 0.1 * i, 0.4), width=8)
    headline(cr, t, "3 OUT OF 4:", "DOGS", t0, T(tl, "b6", "dogs"))


def n_deaths(cr, t, tl, t0):                             # b7 "an estimated 5,700 people die of rabies. Every year."
    t5 = T(tl, "b7", "five")
    counter(cr, t, t5 - 0.1, W / 2, 900, "5,700", 200, color=RED)
    draw_text(cr, "DEATHS", W / 2, 1080, 70, INK, prog(t, t5 + 0.4, 0.3), anchor="ct")
    calendar(cr, t, T(tl, "b7", "Every") - 0.1, W / 2, 1420, ["2023", "2024", "2025"], "EVERY YEAR", interval=0.3,
             w=340, h=300, circle_last=False)
    footnote(cr, "Estimate: ICMR-NIE, The Lancet Infectious Diseases, 2025", prog(t, t5, 0.3), y=1640)
    headline(cr, t, "AN ESTIMATED", "5,700 DEATHS", t0, t5)


def m_how(cr, t, tl, t0):                                # b8 re-hook: "so how does a tiny scratch reach your brain?"
    X = cut(cr, "head_lineart", 520, 1120, 980)
    bx, by = X(0.5, 0.25)
    why(cr, t, t0 + 0.4, bx, by, 300)
    bite_marks(cr, 860, 1500, 110, prog(t, t0 + 0.2, 0.4))
    path(cr, [(860, 1450), (bx + 60, by + 90)], prog(t, t0 + 0.6, 0.8), 6, RED, 0.8, dash=[16, 12], arrow=True)
    headline(cr, t, "HOW DOES A SCRATCH REACH", "YOUR BRAIN?", t0, T(tl, "b8", "brain"), t_ghost=t0, big_size=130)


def m_saliva(cr, t, tl, t0):                             # b9 "the virus lives in the saliva of an infected animal"
    _pic(cr, "dog_snarl", 430, 1150, 700, t, t0)

    def lens(c):
        c.set_source_rgba(0.93, 0.90, 0.86, 1)
        c.paint()
        for i in range(6):
            virus(c, 700 + 90 * math.cos(i * 1.1), 820 + 80 * math.sin(i * 1.7), 70, i * 0.8, 1.0, t + i)
    magnifier(cr, t, T(tl, "b9", "saliva") - 0.2, 780, 820, 210, lens)
    card(cr, t, T(tl, "b9", "saliva"), 600, 1080, ["SALIVA"], size=48)
    headline(cr, t, "THE VIRUS LIVES IN", "SALIVA", t0, T(tl, "b9", "saliva"))


def m_ways(cr, t, tl, t0):                               # b9 "a bite, a scratch, or a lick on broken skin"
    checklist(cr, t, 110, 560, 860, "HOW IT GETS IN",
              [("BITE", T(tl, "b9", "bite") - 0.15, "tick", T(tl, "b9", "bite")),
               ("SCRATCH", T(tl, "b9", "scratch") - 0.15, "tick", T(tl, "b9", "scratch")),
               ("LICK ON BROKEN SKIN", T(tl, "b9", "lick") - 0.15, "tick", T(tl, "b9", "lick"))])
    _pic(cr, "dog_lick", W / 2, 1420, 0, t, T(tl, "b9", "lick") - 0.2, frame=(620, 413), rot=0.02)
    headline(cr, t, "A BITE, A SCRATCH,", "OR A LICK", t0, T(tl, "b9", "lick"))


def m_climb(cr, t, tl, t0):                              # b10 "then it climbs your nerves... up to your brain" (slate)
    X = cut(cr, "mq_run", 520, 1150, 900, alpha=0.6, tint=CREAM, shadow=False)
    pts = [X(*p) for p in ARM_ROUTE]
    tb = T(tl, "b10", "brain")
    path(cr, pts, 1.0, 10, NERVE, 0.95)
    f = clamp((t - t0) / max(0.8, tb - t0))
    for i in range(3):
        x, y = _along(pts, max(0.0, f - 0.08 * i))
        virus(cr, x, y, 54, -0.9, prog(t, t0 + 0.15 * i, 0.3), t + i)
    ring(cr, *X(*MQ_HEAD["mq_run"]), 90, 90, prog(t, tb, 0.4), color=CORAL)
    card(cr, t, t0 + 0.3, 600, 1640, ["NERVES"], size=44, pin_line=_along(pts, 0.3))
    headline(cr, t, "IT CLIMBS YOUR", "NERVES", t0, T(tl, "b10", "nerves"), small_color=CREAM, big_color=CORAL)


def m_hide(cr, t, tl, t0):                               # b11 "it can hide for weeks, or even months, while you feel fine"
    calendar(cr, t, T(tl, "b11", "weeks") - 0.1, 330, 950, ["WEEK 1", "WEEK 4", "MONTH 2", "MONTH 3"], "HIDING",
             interval=0.3, circle_last=False)
    _pic(cr, "mq_run", 760, 1300, 560, t, t0)
    stamp(cr, t, "FEELS FINE", T(tl, "b11", "fine"), 760, 1650, 64, color=GREEN)
    headline(cr, t, "IT HIDES FOR", "MONTHS", t0, T(tl, "b11", "months"))


def m_face(cr, t, tl, t0):                               # b12 "a bite on the face reaches the brain faster"
    X = cut(cr, "mq_run", 520, 1150, 900)
    pts = [X(*p) for p in ARM_ROUTE]
    path(cr, pts, prog(t, t0, 0.8), 9, NERVE, 0.9)
    hx, hy = X(*MQ_HEAD["mq_run"])
    path(cr, [(hx + 40, hy + 40), (hx + 4, hy + 4)], prog(t, T(tl, "b12", "face"), 0.3), 12, RED, 0.95, arrow=True)
    draw_text(cr, "HAND: SLOWER", 760, 1300, 46, INK, prog(t, t0 + 0.4, 0.3), anchor="lm")
    draw_text(cr, "FACE: FASTER", hx + 70, hy + 60, 46, RED, prog(t, T(tl, "b12", "faster"), 0.3), anchor="lm")
    headline(cr, t, "A BITE ON THE FACE IS", "FASTER", t0, T(tl, "b12", "faster"))


def s_fever(cr, t, tl, t0):                              # b13 "when it gets there, the signs begin. Fever."
    _pic(cr, "thermometer", W / 2, 1150, 700, t, t0, rot=-0.1)
    stamp(cr, t, "FEVER", T(tl, "b13", "Fever"), 760, 1550, 80)
    headline(cr, t, "THEN THE SIGNS", "BEGIN", t0, T(tl, "b13", "signs"))


def s_tingle(cr, t, tl, t0):                             # b13 "...a strange tingling where you were bitten"
    _pic(cr, "scratch", W / 2, 1060, 0, t, t0, frame=(820, 615), rot=-0.02)
    for i in range(6):                                     # tingling zig-zags round the wound
        a = i * math.pi / 3 + t * 2
        x, y = W / 2 + 200 * math.cos(a), 1060 + 160 * math.sin(a)
        path(cr, [(x, y), (x + 14, y - 14), (x + 28, y), (x + 42, y - 14)], prog(t, t0 + 0.3 + 0.08 * i, 0.3), 6,
             GOLD, 0.95)
    headline(cr, t, "A STRANGE", "TINGLING", t0, T(tl, "b13", "tingling"))


def s_spasm(cr, t, tl, t0):                              # b14 "swallowing hurts so much the throat goes into spasms"
    X = cut(cr, "throat", W / 2, 1200, 900)
    tx, ty = X(0.5, 0.55)
    spasm(cr, tx, ty, 90, t, prog(t, T(tl, "b14", "spasms"), 0.3))
    headline(cr, t, "THE THROAT GOES INTO", "SPASMS", t0, T(tl, "b14", "spasms"))


def s_water(cr, t, tl, t0):                              # b14 "even the sight of water can set them off"
    X = cut(cr, "glass", 380, 1180, 640)
    x0, y0 = X(0.12, 0.40)
    x1, y1 = X(0.88, 0.97)
    cr.set_source_rgba(*WATER, 0.4)
    _round(cr, x0 + 18, y0, x1 - x0 - 36, y1 - y0, 26)
    cr.fill()
    stamp(cr, t, "SPASM", T(tl, "b14", "sight"), 790, 980, 90)
    draw_text(cr, "!", 790, 1300, 260, RED, prog(t, T(tl, "b14", "sight") + 0.2, 0.3), anchor="cm")
    headline(cr, t, "EVEN THE SIGHT OF", "WATER", t0, T(tl, "b14", "water"))


def s_fatal(cr, t, tl, t0):                              # b15 "once these signs start, rabies is almost always fatal"
    gauge(cr, t, t0 + 0.2, W / 2, 1250, 300, 0.1, 0.98, labels=("SURVIVE", "FATAL"))
    footnote(cr, "WHO: once symptoms appear, rabies is virtually 100% fatal", prog(t, t0, 0.3), y=1500)
    headline(cr, t, "ONCE SIGNS START:", "ALMOST ALWAYS FATAL", t0, T(tl, "b15", "fatal"), big_size=120)


def v_vaccine(cr, t, tl, t0):                            # b16 "but here's the strange part. There's a vaccine..."
    tv_ = T(tl, "b16", "vaccine")
    _pic(cr, "vaccine", W / 2, 1100, 640, t, tv_ - 0.2)
    if t < tv_ - 0.2:
        why(cr, t, t0, W / 2, 1100, 300)
    tick(cr, 830, 760, 150, prog(t, T(tl, "b16", "works"), 0.4), color=GREEN)
    card(cr, t, T(tl, "b16", "after"), 110, 1500, ["WORKS EVEN", "AFTER THE BITE"], size=50)
    small, big = ("HERE'S THE", "STRANGE PART") if t < tv_ - 0.2 else ("THERE IS A", "VACCINE")
    headline(cr, t, small, big, t0 if big == "STRANGE PART" else tv_ - 0.2, t0 + 0.3 if big == "STRANGE PART" else tv_,
             big_color=RED if big == "STRANGE PART" else GREEN)


def v_why(cr, t, tl, t0):                                # b17 re-hook: "so why do thousands still die?"
    _pic(cr, "street_dogs", W / 2, 1060, 0, t, t0, frame=(820, 560), rot=0.02)
    why(cr, t, t0 + 0.3, 820, 1500, 320)
    headline(cr, t, "SO WHY DO THOUSANDS", "STILL DIE?", t0, T(tl, "b17", "die"), t_ghost=t0)


def v_never(cr, t, tl, t0):                              # b18 "many people never get it... more than 1 in 5: no vaccine"
    t5 = T(tl, "b18", "five")
    counter(cr, t, t5 - 0.3, 330, 760, "1", 200, color=GOLD)
    draw_text(cr, "IN", W / 2, 760, 120, INK, prog(t, t5 - 0.1, 0.25), anchor="cm")
    counter(cr, t, t5 - 0.1, 750, 760, "5", 200, color=GOLD)
    icon_array(cr, t, t0 + 0.2, 5, 5, 200, 1150, 150, red=(2,), red_at=T(tl, "b18", "vaccine"))
    footnote(cr, "Dog-bite victims with no anti-rabies vaccine: ICMR-NIE, Lancet Infect Dis 2025", prog(t, t5, 0.3),
             y=1560)
    headline(cr, t, "1 IN 5 GOT", "NO VACCINE", t0, T(tl, "b18", "vaccine"))


def v_unfinished(cr, t, tl, t0):                         # b19 "about half of those who started never finished"
    doses = ["DOSE 1", "DOSE 2", "DOSE 3", "DOSE 4"]
    checklist(cr, t, 110, 600, 860, "THE SHOTS", [(d, t0 + 0.2 + 0.25 * i, "tick" if i < 2 else "cross",
                                                    t0 + 0.4 + 0.25 * i + (0.6 if i >= 2 else 0))
                                                   for i, d in enumerate(doses)])
    stamp(cr, t, "HALF STOP", T(tl, "b19", "finished"), 540, 1500, 80)
    headline(cr, t, "HALF NEVER", "FINISHED", t0, T(tl, "b19", "finished"))


def v_myths(cr, t, tl, t0):                              # b20 "turmeric or chilli on the wound, a healer, just a puppy"
    items = (("turmeric", "turmeric", "TURMERIC", 280, 760), ("chillies", "chilli", "CHILLI", 800, 760),
             (None, "healer", "A HEALER", 280, 1250), ("puppy", "puppy", "\"JUST A PUPPY\"", 800, 1250))
    for key, cue, label, cx, cy in items:
        tc = T(tl, "b20", cue) - 0.2
        if key:
            _pic(cr, key, cx, cy, 300, t, tc)
        else:
            card(cr, t, tc, cx - 180, cy - 60, ["GO TO A", "HEALER"], size=56)
        draw_text(cr, label, cx, cy + 190, 40, INK, prog(t, tc, 0.3), anchor="ct")
        cross(cr, cx, cy, 240, prog(t, tc + 0.5, 0.3))
    headline(cr, t, "WHAT PEOPLE", "DO INSTEAD", t0, t0 + 0.3)


def v_shots(cr, t, tl, t0):                              # b21 "not fourteen injections in the stomach... a few in the arm"
    ta = T(tl, "b21", "Today")
    if t < ta - 0.15:
        for i in range(14):
            p = prog(t, t0 + 0.05 * i, 0.2)
            x, y = 220 + (i % 7) * 107, 820 + (i // 7) * 260
            cr.set_source_rgba(*INK, 0.85 * p)
            cr.set_line_width(10)
            cr.move_to(x, y - 90)
            cr.line_to(x, y + 70)
            cr.stroke()
            cr.rectangle(x - 18, y - 60, 36, 110)
            cr.fill()
        strike(cr, 160, 1150, 940, 830, prog(t, T(tl, "b21", "stomach"), 0.4))
        stamp(cr, t, "MYTH", T(tl, "b21", "anymore"), 540, 1450, 100)
        headline(cr, t, "NOT 14 SHOTS IN THE", "STOMACH", t0, T(tl, "b21", "stomach"))
        return
    _pic(cr, "injection_arm", W / 2, 1100, 0, t, ta - 0.15, frame=(820, 600), rot=-0.02)
    tick(cr, 820, 760, 140, prog(t, T(tl, "b21", "arm"), 0.4), color=GREEN)
    headline(cr, t, "TODAY: A FEW SHOTS", "IN THE ARM", ta - 0.15, T(tl, "b21", "arm"), big_color=GREEN)


def d_wash(cr, t, tl, t0):                               # b22 "wash the wound with soap and running water, 15 minutes"
    _pic(cr, "wash_hands", W / 2, 950, 0, t, t0, frame=(820, 560), rot=0.02)
    _pic(cr, "soap", 280, 1450, 260, t, T(tl, "b22", "soap") - 0.2)
    _pic(cr, "stopwatch", 800, 1450, 330, t, T(tl, "b22", "fifteen") - 0.2)
    counter(cr, t, T(tl, "b22", "fifteen"), 540, 1460, "15:00", 90, color=GOLD)
    headline(cr, t, "WASH IT FOR", "15 MINUTES", t0, T(tl, "b22", "fifteen"), big_color=GREEN)


def d_hospital(cr, t, tl, t0):                           # b23 "go to a hospital the same day, even a scratch, a puppy"
    _pic(cr, "hospital", W / 2, 900, 0, t, t0, frame=(820, 520), rot=-0.02)
    tp = T(tl, "b23", "puppy")
    _pic(cr, "puppy", 300, 1450, 360, t, tp - 0.3)
    bite_marks(cr, 760, 1400, 100, prog(t, T(tl, "b23", "scratch"), 0.4))
    tick(cr, 820, 1500, 120, prog(t, T(tl, "b23", "scratch") + 0.3, 0.3), color=GREEN)
    tick(cr, 470, 1300, 120, prog(t, tp, 0.3), color=GREEN)
    headline(cr, t, "GO TO A HOSPITAL", "THE SAME DAY", t0, T(tl, "b23", "same"), big_color=GREEN, big_size=130)


def d_doses(cr, t, tl, t0):                              # b24 "and finish every single dose"
    doses = ["DOSE 1", "DOSE 2", "DOSE 3", "DOSE 4"]
    checklist(cr, t, 110, 600, 860, "EVERY DOSE", [(d, t0 + 0.1 + 0.18 * i, "tick", t0 + 0.25 + 0.18 * i)
                                                   for i, d in enumerate(doses)])
    _pic(cr, "vaccine", 800, 1500, 360, t, t0 + 0.3)
    headline(cr, t, "FINISH EVERY", "DOSE", t0, T(tl, "b24", "dose"), big_color=GREEN)


def e_bookend(cr, t, tl, t0):                            # b25 "rabies kills almost everyone it reaches. But the vaccine..."
    tb = T(tl, "b25", "But")
    if t < tb - 0.15:
        X = cut(cr, "mq_head", 420, 1150, 900)
        hx, hy = X(*MQ_HEAD["mq_head"])
        for i in range(4):
            virus(cr, hx - 30 + 30 * i, hy + 10, 46, 0.4 * i, 1.0, t + i)
        headline(cr, t, "IT KILLS ALMOST", "EVERYONE IT REACHES", t0, T(tl, "b25", "reaches"), t_ghost=t0,
                 big_size=120)
        return
    _pic(cr, "vaccine", 380, 1150, 640, t, tb - 0.15)
    stamp(cr, t, "DON'T WAIT", T(tl, "b25", "wait"), 760, 1300, 90, color=GREEN)
    headline(cr, t, "THE VACCINE CAN", "STOP IT", tb - 0.15, T(tl, "b25", "stop"), big_color=GREEN)


def e_question(cr, t, tl, t0):                           # b26 "has a dog ever bitten or scratched you? YES or NO"
    _pic(cr, "child_dog" if "child_dog" in P else "street_dogs", W / 2, 1380, 0, t, -1, frame=(820, 546), rot=-0.02)
    yes_no_card(cr, t, T(tl, "b26", "Yes") - 0.2, 540, 820, w=700, h=320, question="COMMENT: YES OR NO")
    headline(cr, t, "HAS A DOG EVER", "BITTEN YOU?", t0, T(tl, "b26", "bitten"), t_ghost=t0)


SHOTS = [   # (line, cue where the shot starts, draw function, background)
    ("b1", None, h_thirsty, "paper"), ("b1", "throat", h_throat, "paper"), ("b2", None, h_scratch, "paper"),
    ("b2", "Weeks", h_weeks, "paper"), ("b3", None, h_late, "paper"), ("b4", None, h_movie, "paper"),
    ("b5", None, n_name, "paper"), ("b6", None, n_bites, "paper"), ("b6", "Three", n_dogs, "paper"),
    ("b7", None, n_deaths, "paper"), ("b8", None, m_how, "paper"), ("b9", None, m_saliva, "paper"),
    ("b9", "bite", m_ways, "paper"), ("b10", None, m_climb, "slate"), ("b11", None, m_hide, "paper"),
    ("b12", None, m_face, "paper"), ("b13", None, s_fever, "paper"), ("b13", "strange", s_tingle, "paper"),
    ("b14", None, s_spasm, "paper"), ("b14", "Even", s_water, "paper"), ("b15", None, s_fatal, "paper"),
    ("b16", None, v_vaccine, "paper"), ("b17", None, v_why, "paper"), ("b18", None, v_never, "paper"),
    ("b19", None, v_unfinished, "paper"), ("b20", None, v_myths, "paper"), ("b21", None, v_shots, "paper"),
    ("b22", None, d_wash, "paper"), ("b23", None, d_hospital, "paper"), ("b24", None, d_doses, "paper"),
    ("b25", None, e_bookend, "paper"), ("b26", None, e_question, "paper"),
]


def draw(cr, t, tl):
    draw_frame(cr, t, tl, SHOTS)


def sfx(tl):
    """A whoosh on every cut, thuds on stamps, a tick (and the bed dipping) before the name, each re-hook and the
    closing line, typing under the YES/NO card."""
    ev = [(s, "whoosh", 0.25) for s in starts(tl, SHOTS)[1:]]
    ev += [(T(tl, "b3", "late"), "thud", 0.0), (T(tl, "b4", "real") + 0.2, "thud", 0.0),
           (T(tl, "b14", "sight"), "thud", 0.0), (T(tl, "b21", "anymore"), "thud", 0.0)]
    for bid in ("b5", "b8", "b17", "b25"):
        ev.append((tl[bid].start - 0.45, "tick", 0.0))
    ev += [(T(tl, "b26", "Yes"), "typing", 1.0), (tl["b6"].start + 0.4, "pop", 0.0), (tl["b18"].start + 0.3, "pop", 0.0)]
    ev += [(at, "dip", 0.5) for at, name, _ in list(ev) if name == "tick"]
    return ev


def cover(cr):
    """Cover (Hinglish channel rule): a dark poster, one subject, at most three words, one big coloured key word,
    everything inside Instagram's 3:4 grid crop (y 240-1680)."""
    from poster import finish, slate
    slate(cr)
    if "dog_snarl" in P:
        photo(cr, P["dog_snarl"], W / 2, 1150, 820)
    draw_text(cr, "AFRAID OF", W / 2, 330, 110, CREAM, anchor="ct")
    draw_text(cr, "WATER", W / 2, 460, 230, CORAL, anchor="ct")
    finish(cr)
