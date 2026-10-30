"""Explainer 4: "This Amoeba Eats Your Brain Through Your Nose" (Naegleria fowleri, Kerala 2025). Made 29 Oct 2026
under the owner's standing approval ("auto approved from next"), in the Hinglish channel's poster format and hook
rules (research_notes/from_shorts/). Script and sources: research_notes/explainer_4_amoeba.md.
v2 (30 Oct 2026, owner: "copy its style visuals everything ... this is not even close"): rebuilt on photo cut-outs
like the Hinglish channel's Toxoplasma video, with photos sourced through that channel's photo chat."""
import json
import math
import os

from poster import (CORAL, CREAM, GOLD, GREEN, INK, MARGIN, RED, W, _along, _round, calendar, card, clamp, counter,
                    cross, draw_text, footnote, framed_photo, gauge, headline, icon_array, magnifier, path, photo,
                    photo_width, prog, ring, stamp, text_size, tick, yes_no_card)

# the narrator, music and pauses are channel-wide; render_doc reads them from this module
from channel import ASSETS_ROOT, GAP, REPO, MUSIC, NARRATOR, REVEAL_GAP, TAIL  # noqa: F401
from shots import T, checklist, draw_frame, pic, starts

SCRIPT = [
    dict(id="b1", text="Imagine you jump into a pond on a hot day. A few days later, something is eating your brain."),
    dict(id="b2", text="It got in through your nose. Then it climbed the nerve you smell with."),
    dict(id="b3", text="And by the time your head starts to hurt, it's already in your brain."),
    dict(id="b4", text="This isn't a horror movie. It's real."),
    dict(id="b5", text="It's called Naegleria fowleri. The brain-eating amoeba.", gap=REVEAL_GAP),
    dict(id="b6", text="In [twenty twenty-five,|2025,] brain infections from amoebas hit about one hundred and seventy "
                       "people in Kerala. Forty-two of them died."),
    dict(id="b7", text="So how can one tiny cell, thinner than a hair, kill a grown adult?"),
    dict(id="b8", text="It lives in warm, fresh water. Ponds, lakes, rivers, and badly kept pools."),
    dict(id="b9", text="It loves heat. Cases usually come after long, hot spells."),
    dict(id="b10", text="Drinking that water won't infect you. The danger is your nose."),
    dict(id="b11", text="When water shoots up your nose, the amoeba can travel to the very top."),
    dict(id="b12", text="There, the bone has tiny holes. Your smell nerves pass through them, into the brain."),
    dict(id="b13", text="It follows those nerves, straight into your brain. And it starts eating brain tissue."),
    dict(id="b14", text="And the scariest part? The first signs look like a normal fever.", gap=REVEAL_GAP),
    dict(id="b15", text="Headache. Fever. Vomiting."),
    dict(id="b16", text="Then a stiff neck. Confusion. Seizures. It moves very fast."),
    dict(id="b17", text="It's very rare. But nearly everyone who gets it dies."),
    dict(id="b18", text="So why did some patients in Kerala survive?", gap=REVEAL_GAP),
    dict(id="b19", text="Because doctors there started testing for it early, and treating it fast."),
    dict(id="b20", text="And it doesn't spread from person to person."),
    dict(id="b21", text="So, hold your nose, or wear a nose clip, when you jump into fresh water."),
    dict(id="b22", text="Don't stir up the mud in shallow, warm water."),
    dict(id="b23", text="If you rinse your nose, like with a neti pot, use boiled and cooled water. Never straight "
                        "from the tap."),
    dict(id="b24", text="And if you get a bad headache and fever after swimming, see a doctor right away. Tell them you "
                        "swam."),
    dict(id="b25", text="It's rare. But one splash up your nose is all it needs.", gap=REVEAL_GAP),
    dict(id="b26", text="Do you swim in ponds, rivers or lakes? Yes or no, tell me in the comments."),
]
for _b in SCRIPT:
    _b.setdefault("scene", _b["id"])
for _b in SCRIPT[1:]:
    _b.setdefault("gap", GAP)

METADATA = dict(
    title="This Amoeba Eats Your Brain Through Your Nose",
    alt_titles=["One Swim Can Let an Amoeba Into Your Brain", "The Brain-Eating Amoeba Hiding in Warm Water",
                "Why You Should Never Rinse Your Nose With Tap Water"],
    caption="One swim in a warm pond… and an amoeba can climb up your nose into your brain 😳 Kerala: ~170 cases "
            "in 2025.\n\n"
            "To stay safe:\n✅ Hold your nose or wear a nose clip when you jump into fresh water\n"
            "✅ Don't stir up mud in shallow, warm water\n"
            "✅ Rinsing your nose (jal neti)? Use boiled and cooled water\n"
            "✅ Bad headache and fever after a swim? See a doctor right away, and tell them you swam\n"
            "❌ It doesn't spread from person to person\n❌ Drinking the water doesn't infect you\n\n"
            "It's very rare, but almost always deadly.\n\n"
            "Do you swim in ponds, rivers or lakes? Comment YES or NO 👇",
    yt_title="This Amoeba Eats Your Brain Through Your Nose 😳",
    yt_description="Naegleria fowleri, the brain-eating amoeba, lives in warm fresh water. It goes up the nose, follows "
                   "the smell nerves into the brain, and destroys brain tissue. In 2025, Kerala reported about 170 "
                   "amoeba brain infections and 42 deaths. It's very rare, and early testing and fast treatment saved "
                   "some patients.\n\n"
                   "To stay safe:\n✅ Hold your nose or wear a nose clip when you jump into fresh water\n"
                   "✅ Don't stir up mud in shallow, warm water\n"
                   "✅ Rinse your nose only with boiled and cooled water\n"
                   "✅ Bad headache and fever after swimming? See a doctor right away, and tell them you swam\n"
                   "❌ It doesn't spread from person to person, and drinking the water doesn't infect you\n\n"
                   "General information, not medical advice.",
    hashtags=["#braineatingamoeba", "#naegleriafowleri", "#kerala", "#healthawareness", "#sciencefacts"],
    tags=["brain eating amoeba", "naegleria fowleri", "amoebic meningoencephalitis", "kerala amoeba", "PAM",
          "swimming safety", "jal neti", "nasal rinse", "health facts", "science explained"],
    pinned_comment="Do you swim in ponds, rivers or lakes? 🏊 YES or NO? 👇",
    sources=["CDC, Naegleria fowleri: about, causes, symptoms, prevention",
             "Government of India, Lok Sabha reply on amoebic meningoencephalitis, December 2025",
             "The Lancet, 2025, Naegleria fowleri in Kerala, India: prevention over panic"],
)


# ---------- photos ----------
# Sourced the way the Hinglish channel sources its Toxoplasma video (its photo chat's search, 30 Oct 2026): Pixabay,
# Wikimedia Commons, Flickr (CC BY); cut out with rembg (isnet-general-use) and checked on the paper, or kept whole as
# framed photos for scenes and places. Credits: assets/doctor_photos/amoeba/credits.json.
ASSETS = os.path.join(ASSETS_ROOT, "amoeba")
_FILES = {
    # cut-outs: objects and bodies (the wooden mannequin is the reference's stand-in for "you")
    "mq_run": "mq_run.png", "mq_head": "mq_head.png", "mq_sit": "mq_sit.png", "head_lineart": "head_lineart.png",
    "microscope": "microscope.png", "thermometer": "thermometer.png", "glass": "glass.png", "tap": "tap.png",
    "doctor": "doctor.png", "headache_man": "headache_man.png", "tv": "tv_legs.png",
    # framed photos: scenes and places
    "micrograph": "micrograph_cdc.jpg", "pond_kerala": "pond_kerala.jpg", "kerala_tank": "kerala_tank.jpg",
    "pond_assam": "pond_assam.jpg", "boys_river": "boys_river.jpg", "lake_swim": "lake_swim.jpg",
    "pool_dark": "pool_dark.jpg", "sun_sky": "sun_sky.jpg", "cracked_earth": "cracked_earth.jpg",
    "hair_macro": "hair_macro.jpg", "mud_boots": "mud_boots.jpg", "blood_tubes": "blood_tubes.jpg",
    "pot_stove": "pot_stove.jpg", "boy_pier": "boy_pier.jpg", "profile_photo": "profile_photo.jpg",
    "gray_brain": "gray_brain.png", "gray_olfactory": "gray_olfactory.png", "gray_ethmoid": "gray_ethmoid.png",
}
P = {k: os.path.join(ASSETS, v) for k, v in _FILES.items() if os.path.exists(os.path.join(ASSETS, v))}
USED_ASSETS = [os.path.basename(v) for v in P.values()]
CREDITS_FILES = [os.path.join(ASSETS, "credits.json")]

AMOEBA = (0.55, 0.30, 0.62)          # the amoeba's colour, the same in every shot (the recurring "intruder")
NERVE = (0.95, 0.78, 0.30)
WATER = (0.45, 0.72, 0.85)
BRAIN = (0.86, 0.60, 0.58)
BONE = (0.90, 0.85, 0.74)

# Points on the line-art head (fractions of the picture, which faces right): the amoeba's way in
HEAD_PTS = dict(nostril=(0.905, 0.600), nose_mid=(0.845, 0.520), top=(0.785, 0.440), lobe=(0.72, 0.375),
                deep=(0.60, 0.30))
ROUTE = ("nostril", "nose_mid", "top", "lobe", "deep")
# fraction of the route at each point (for "up to the top of the nose" etc.)
AT_TOP, AT_LOBE = 0.42, 0.66
# where the photo subjects' heads are (fractions of each cut-out)
MQ_HEAD = {"mq_run": (0.72, 0.06), "mq_head": (0.60, 0.075), "mq_sit": (0.50, 0.08)}
TV_SCREEN = (0.11, 0.06, 0.66, 0.385)   # the TV photo's screen glass: x, y, w, h (fractions)


def _pic(cr, key, cx, cy, h, t, t0, **kw):
    pic(cr, P.get(key), cx, cy, h, t, t0, **kw)


def cut(cr, key, cx, cy, h, alpha=1.0, **kw):
    """A cut-out photo centred at (cx, cy), `h` px tall; returns a (u, v) -> (x, y) mapper for points on it."""
    photo(cr, P[key], cx, cy, h, alpha=alpha, **kw)
    w = photo_width(P[key], h)
    flip = kw.get("flip")
    return lambda u, v: (cx + ((0.5 - u) if flip else (u - 0.5)) * w, cy + (v - 0.5) * h)


def lineart(cr, cx, cy, h, alpha=1.0, dark=False):
    """The line-art head cross-section (face to the right). On slate it's drawn in cream lines, the reference's "inside
    the body" look. Returns the point mapper."""
    if dark:
        return cut(cr, "head_lineart", cx, cy, h, alpha=0.55 * alpha, tint=CREAM, shadow=False)
    return cut(cr, "head_lineart", cx, cy, h, alpha=alpha)


def route(X, f):
    return _along([X(*HEAD_PTS[k]) for k in ROUTE], f)


def nose_channel(cr, X, p=1.0, alpha=1.0, nerve=0.0):
    """The way in, drawn over the head: the nose channel (blue), the thin bone at its top, and the smell nerve
    (yellow) from there up into the brain; `nerve` 0..1 lights the nerve."""
    path(cr, [X(*HEAD_PTS[k]) for k in ROUTE[:3]], p, 26, WATER, 0.55 * alpha)
    tx, ty = X(*HEAD_PTS["top"])
    cr.set_source_rgba(*BONE, alpha)
    cr.set_line_width(9)
    for dx in (-46, -18, 10, 38):
        cr.move_to(tx + dx - 6, ty - 4 + dx * 0.25)
        cr.line_to(tx + dx + 14, ty - 4 + (dx + 20) * 0.25)
        cr.stroke()
    if nerve > 0:
        path(cr, [X(*HEAD_PTS[k]) for k in ROUTE[2:]], nerve, 9, NERVE, 0.95 * alpha)


# ---------- drawn pieces ----------

def amoeba(cr, x, y, r, t, alpha=1.0, seed=0, color=AMOEBA):
    """The amoeba: a lumpy cell whose pseudopods slowly flow, with a nucleus, a nucleolus and a few vacuoles."""
    if alpha <= 0:
        return
    ph = [seed * 1.7 + k * 2.1 for k in range(4)]
    n = 60
    pts = []
    for i in range(n):
        a = 2 * math.pi * i / n
        k = (0.16 * math.sin(2 * a + ph[0] + 1.3 * t) + 0.12 * math.sin(3 * a + ph[1] - 0.9 * t)
             + 0.07 * math.sin(5 * a + ph[2] + 2.1 * t))
        pts.append((x + r * (1 + k) * math.cos(a), y + r * (1 + k) * math.sin(a)))
    cr.move_to(*pts[0])
    for i in range(n):                                     # smooth closed curve through the points
        p0, p1, p2 = pts[i - 1], pts[i], pts[(i + 1) % n]
        p3 = pts[(i + 2) % n]
        cr.curve_to(p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6,
                    p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6, *p2)
    cr.close_path()
    cr.set_source_rgba(*color, 0.85 * alpha)
    cr.fill_preserve()
    cr.set_source_rgba(color[0] * 0.4, color[1] * 0.4, color[2] * 0.4, 0.95 * alpha)
    cr.set_line_width(max(2, r * 0.06))
    cr.stroke()
    nx, ny = x - r * 0.15 + r * 0.05 * math.sin(t), y - r * 0.1
    cr.set_source_rgba(0.80, 0.62, 0.85, 0.9 * alpha)
    cr.arc(nx, ny, r * 0.28, 0, 2 * math.pi)
    cr.fill()
    cr.set_source_rgba(0.15, 0.08, 0.18, 0.9 * alpha)
    cr.arc(nx, ny, r * 0.11, 0, 2 * math.pi)
    cr.fill()
    for k, (dx, dy, rr) in enumerate(((0.4, 0.3, 0.12), (-0.35, 0.42, 0.09), (0.3, -0.42, 0.08))):
        cr.set_source_rgba(1, 1, 1, 0.35 * alpha)
        cr.arc(x + r * dx, y + r * dy + r * 0.04 * math.sin(t * 2 + k), r * rr, 0, 2 * math.pi)
        cr.fill()


def splash(cr, x, y, t, t0, alpha=1.0):
    f = clamp((t - t0) / 0.7)
    if f <= 0 or f >= 1:
        return
    for i in range(14):
        a = math.pi + math.pi * (i + 0.5) / 14
        d = 60 + 220 * f
        cr.set_source_rgba(0.85, 0.93, 0.97, alpha * (1 - f))
        cr.arc(x + d * math.cos(a), y + d * math.sin(a) + 300 * f * f, 14 * (1 - 0.5 * f), 0, 2 * math.pi)
        cr.fill()


def nose_clip(cr, x, y, s, alpha=1.0):
    cr.set_source_rgba(0.20, 0.45, 0.80, alpha)
    cr.set_line_width(s * 0.12)
    cr.set_line_cap(1)
    cr.arc(x, y, s * 0.5, math.pi * 1.05, math.pi * 1.95)
    cr.stroke()
    for sx in (-1, 1):
        cr.set_source_rgba(0.12, 0.12, 0.14, alpha)
        _round(cr, x + sx * s * 0.5 - s * 0.14, y - s * 0.05, s * 0.28, s * 0.4, s * 0.1)
        cr.fill()


def neti(cr, x, y, s, alpha=1.0):
    """A neti pot (side view, spout to the right): rounded body, open top, long rising spout, handle at the back."""
    body = (0.30, 0.55, 0.62)
    cr.set_source_rgba(*body, alpha)
    cr.move_to(x - s, y)                                          # body
    cr.curve_to(x - s, y + s * 0.75, x + s, y + s * 0.75, x + s, y)
    cr.line_to(x + s * 0.8, y - s * 0.35)
    cr.line_to(x - s * 0.8, y - s * 0.35)
    cr.close_path()
    cr.fill()
    cr.move_to(x + s * 0.7, y + s * 0.1)                          # spout
    cr.curve_to(x + s * 1.3, y + s * 0.1, x + s * 1.5, y - s * 0.4, x + s * 1.9, y - s * 0.75)
    cr.line_to(x + s * 1.98, y - s * 0.62)
    cr.curve_to(x + s * 1.6, y - s * 0.2, x + s * 1.4, y + s * 0.35, x + s * 0.7, y + s * 0.4)
    cr.close_path()
    cr.fill()
    cr.set_line_width(s * 0.14)                                   # handle
    cr.arc(x - s * 1.05, y + s * 0.05, s * 0.32, math.pi * 0.5, math.pi * 1.5)
    cr.stroke()
    cr.set_source_rgba(0.18, 0.36, 0.42, alpha)                   # open top
    cr.save()
    cr.translate(x, y - s * 0.35)
    cr.scale(s * 0.8, s * 0.16)
    cr.arc(0, 0, 1, 0, 2 * math.pi)
    cr.restore()
    cr.fill()
    cr.set_source_rgba(1, 1, 1, 0.3 * alpha)                      # shine
    cr.set_line_width(s * 0.08)
    cr.arc(x - s * 0.1, y + s * 0.05, s * 0.6, math.pi * 0.85, math.pi * 1.1)
    cr.stroke()


_INDIA = json.load(open(os.path.join(REPO, "assets", "maps", "india.json")))["india"]   # Natural Earth, public domain
# Kerala, traced by hand from its lon/lat outline (coast and the border with Karnataka and Tamil Nadu)
_KERALA = [(74.87, 12.78), (75.15, 12.66), (75.50, 12.33), (75.85, 11.97), (76.10, 11.85), (76.42, 11.66),
           (76.40, 11.35), (76.60, 11.05), (76.88, 10.85), (76.82, 10.35), (77.20, 10.10), (77.25, 9.62),
           (77.18, 9.20), (77.17, 8.75), (77.17, 8.29), (76.95, 8.42), (76.55, 8.90), (76.30, 9.50), (76.20, 10.00),
           (76.00, 10.60), (75.80, 11.20), (75.55, 11.75), (75.30, 12.10), (75.00, 12.50)]


def kerala(cr, x, y, h, alpha=1.0, color=INK, lit=1.0):
    """India's outline (Natural Earth) centred at (x, y), `h` px tall, with Kerala filled red (lit 0..1).
    Returns Kerala's centre."""
    lat0, lat1, lon0, lon1 = 6.5, 37.2, 68.0, 97.5
    k = h / (lat1 - lat0)
    kx = k * math.cos(math.radians(22))

    def P(lon, lat):
        return x + (lon - (lon0 + lon1) / 2) * kx, y - (lat - (lat0 + lat1) / 2) * k

    def poly(pts):
        cr.move_to(*P(*pts[0]))
        for q in pts[1:]:
            cr.line_to(*P(*q))
        cr.close_path()
    for ring_ in _INDIA:
        poly(ring_)
    cr.set_source_rgba(0.93, 0.89, 0.80, 0.95 * alpha)
    cr.fill_preserve()
    cr.set_source_rgba(*color, alpha)
    cr.set_line_width(4)
    cr.stroke()
    poly(_KERALA)
    cr.set_source_rgba(*RED, alpha * lit)
    cr.fill()
    return P(76.4, 10.4)


def why(cr, t, t0, x, y, size=260):
    q = prog(t, t0, 0.3)
    draw_text(cr, "?", x, y, int(size * (0.8 + 0.2 * q)), RED, q, anchor="cm")


def zoom_photo(c, key, lx, ly, u, v, w, h):
    """Inside a magnifier at (lx, ly): the photo drawn at w x h with its point (u, v) (fractions) at the lens centre."""
    framed_photo(c, P[key], lx - (u - 0.5) * w, ly - (v - 0.5) * h, w, h)


# ---------- shots ----------
# Built like the Hinglish channel's Toxoplasma video (its code: channels/hinglish/videos/toxoplasma.py): a big photo
# cut-out or framed photo carries every shot (main subject 450-700 px, framed photos up to ~860x640), one mark on it,
# the headline above; a new picture every ~3 s cut on the spoken word; red = threat, green = what to do, gold =
# numbers; dark slate only for "inside the body", with the picture drawn in cream lines. The wooden mannequin is
# "you"; the purple amoeba is the one recurring intruder.

def _jump(cr, t, t_go, t_leap, t_in, cx=640, cy=1380, frame=(760, 500), key="pond_kerala"):
    """The mannequin runs in from the left (from t_go), leaps at t_leap and drops into the pond photo at t_in (the
    hook, and its bookend)."""
    _pic(cr, key, cx, cy, 0, t, -1, frame=frame, rot=0.02)
    run = clamp((t - t_go) / max(0.3, t_leap - t_go))
    q = clamp((t - t_leap) / max(0.3, t_in - t_leap))
    x0 = 310 + 130 * run
    x = x0 + (cx - x0) * q
    y = cy - 430 - 230 * math.sin(math.pi * min(1.0, q * 1.1)) + 300 * q * q
    bob = 16 * abs(math.sin(t * 9)) * (1 - q)
    a = 1 - prog(t, t_in, 0.2)
    if a > 0:
        cut(cr, "mq_run", x, y - bob, 600, alpha=a, rot=0.35 * q)
    splash(cr, cx, cy - frame[1] / 2 + 40, t, t_in)


def h_you(cr, t, tl, t0):                                # b1 frame 0: "imagine you jump into a pond on a hot day"
    _jump(cr, t, 0.0, T(tl, "b1", "hot") - 0.1, T(tl, "b1", "day") + 0.15)
    headline(cr, t, "SOMETHING EATS YOUR", "BRAIN", -1, 1.0, t_ghost=-1)


def h_days(cr, t, tl, t0):                               # b1 "a few days later..."
    calendar(cr, t, t0 + 0.15, 330, 900, ["DAY 1", "DAY 2", "DAY 3", "DAY 4", "DAY 5"], "AFTER THE SWIM",
             interval=0.3, circle_last=False)
    _pic(cr, "mq_sit", 760, 1260, 640, t, t0 + 0.2)
    headline(cr, t, "A FEW DAYS", "LATER", t0, t0 + 0.2)


def h_eating(cr, t, tl, t0):                             # b1 "...something is eating your brain"
    te = T(tl, "b1", "eating")
    X = lineart(cr, 540, 1120, 1000)
    for i, (u, v) in enumerate(((0.70, 0.22), (0.55, 0.15), (0.40, 0.20), (0.62, 0.30), (0.30, 0.28))):
        f = prog(t, te - 0.2 + 0.25 * i, 0.5)
        if f > 0:
            x, y = X(u, v)
            cr.set_source_rgba(0.55, 0.05, 0.08, 0.55 * f)
            cr.arc(x, y, 30 + 40 * f, 0, 2 * math.pi)
            cr.fill()
            amoeba(cr, x + 10, y - 6, 26, t + i, f, seed=i)
    headline(cr, t, "SOMETHING IS EATING", "YOUR BRAIN", t0, T(tl, "b1", "brain"))


def h_nose(cr, t, tl, t0):                               # b2 "it got in through your nose" (inside: slate)
    X = lineart(cr, 520, 1120, 1000, dark=True)
    tn = T(tl, "b2", "nose")
    nose_channel(cr, X, prog(t, t0, 0.6))
    amoeba(cr, *route(X, 0.22 * clamp((t - t0) / 2.0)), 28, t, prog(t, t0, 0.3))
    ring(cr, *X(*HEAD_PTS["nostril"]), 95, 80, prog(t, tn, 0.4), color=CORAL)
    headline(cr, t, "IT GOT IN THROUGH YOUR", "NOSE", t0, tn, small_color=CREAM, big_color=CORAL)


def h_climb(cr, t, tl, t0):                              # b2 "then it climbed the nerve you smell with" (slate)
    X = lineart(cr, 520, 1120, 1000, dark=True)
    ts = T(tl, "b2", "smell")
    nose_channel(cr, X, 1.0, nerve=prog(t, t0 + 0.2, 1.0))
    amoeba(cr, *route(X, 0.22 + (AT_LOBE - 0.22) * clamp((t - t0) / 2.2)), 28, t)
    card(cr, t, ts, 560, 1580, ["SMELL NERVE"], size=44, pin_line=X(0.75, 0.405))
    headline(cr, t, "UP THE NERVE YOU", "SMELL WITH", t0, ts, small_color=CREAM, big_color=CORAL)


def h_hurt(cr, t, tl, t0):                               # b3 "by the time your head starts to hurt, it's in your brain"
    th = T(tl, "b3", "hurt")
    ti = T(tl, "b3", "already")
    X = cut(cr, "mq_head", 360, 1140, 900)
    hx, hy = X(*MQ_HEAD["mq_head"])
    for i, a in enumerate((-2.3, -1.9, -1.2, -0.8)):                     # ache lines round the head
        r0 = 95 + 8 * math.sin(t * 10 + i)
        path(cr, [(hx + r0 * math.cos(a), hy + r0 * math.sin(a)), (hx + (r0 + 55) * math.cos(a) + 10,
                                                                   hy + (r0 + 55) * math.sin(a) - 10)],
             prog(t, th + 0.08 * i, 0.3), 9, RED, 0.9)

    def lens(c):
        c.set_source_rgba(*BRAIN, 1)
        c.paint()
        for k in range(7):
            c.set_source_rgba(0.62, 0.36, 0.36, 0.8)
            c.set_line_width(5)
            c.move_to(560 + 40 * k, 760)
            c.curve_to(590 + 40 * k, 720, 610 + 40 * k, 820, 640 + 40 * k, 780)
            c.stroke()
        amoeba(c, 780, 860, 70, t)
    magnifier(cr, t, ti - 0.1, 780, 860, 220, lens)
    path(cr, [(hx + 30, hy + 10), (600, 860)], prog(t, ti - 0.1, 0.3), 3, INK, 0.7)
    stamp(cr, t, "ALREADY INSIDE", ti + 0.2, 760, 1180, 54)
    headline(cr, t, "WHEN IT STARTS TO", "HURT", t0, th)


def _screen(cr, rect, t, on=1.0, monster=1.0):
    """The TV's glass: a dark horror-movie frame with a giant amoeba, collapsing to a line, then a dot, as `on` -> 0."""
    sx, sy, sw, sh = rect
    if on <= 0:
        return
    vy = max(0.02, clamp(on * 2 - 1)) if on < 1 else 1.0
    vx = clamp(on * 2) if on < 1 else 1.0
    cx, cy = sx + sw / 2, sy + sh / 2
    cr.save()
    _round(cr, cx - sw * vx / 2, cy - sh * vy / 2, sw * vx, sh * vy, 24 * vy)
    cr.clip()
    cr.set_source_rgba(0.10, 0.09, 0.11, 1)
    cr.paint()
    if on >= 1:
        amoeba(cr, cx, cy + 10, sh * 0.34 * monster, t * 1.5, 0.95)
        cr.set_source_rgba(0.8, 0.1, 0.1, 0.25 + 0.15 * math.sin(t * 12))       # red horror-movie light
        cr.paint()
        cr.set_source_rgba(1, 1, 1, 0.06)                                        # scan lines
        for y in range(int(sy), int(sy + sh), 6):
            cr.rectangle(sx, y, sw, 2)
        cr.fill()
    else:
        cr.set_source_rgba(0.9, 0.95, 1.0, 1)
        cr.paint()
    cr.restore()


def h_movie(cr, t, tl, t0):                              # b4 "this isn't a horror movie. It's real."
    tr = T(tl, "b4", "real")
    X = cut(cr, "tv", W / 2, 1150, 1050)
    x0, y0 = X(TV_SCREEN[0], TV_SCREEN[1])
    x1, y1 = X(TV_SCREEN[0] + TV_SCREEN[2], TV_SCREEN[1] + TV_SCREEN[3])
    _screen(cr, (x0, y0, x1 - x0, y1 - y0), t, on=1 - prog(t, tr - 0.1, 0.45), monster=0.6 + 0.4 * prog(t, t0, 1.2))
    stamp(cr, t, "FICTION?", t0 + 0.7, 790, 1560, 60, rot=0.08)
    stamp(cr, t, "IT'S REAL", tr + 0.2, 330, 1560, 80, rot=-0.08)
    headline(cr, t, "THIS ISN'T A", "HORROR MOVIE", t0, t0 + 0.4, strike_at=tr, struck=True)


def s_hair(cr, t, tl, t0):                               # b7 "one tiny cell, thinner than a hair"
    th = T(tl, "b7", "hair")
    _pic(cr, "hair_macro", W / 2, 920, 0, t, t0, frame=(820, 560), rot=-0.02)

    def lens(c):
        c.set_source_rgba(0.93, 0.89, 0.80, 1)
        c.paint()
        c.set_source_rgba(0.42, 0.40, 0.38, 1)                           # one hair, magnified
        c.rectangle(560, 1330, 400, 120)
        c.fill()
        c.set_source_rgba(0.55, 0.53, 0.50, 1)
        c.set_line_width(4)
        for k in range(7):
            c.move_to(575 + 55 * k, 1330)
            c.line_to(600 + 55 * k, 1450)
            c.stroke()
        amoeba(c, 760, 1530, 22, t)
    magnifier(cr, t, th - 0.3, 760, 1440, 220, lens)
    card(cr, t, th, 110, 1330, ["ONE HAIR", "vs ONE AMOEBA"], size=40)
    headline(cr, t, "THINNER THAN A", "HAIR", t0, th)


def s_kill(cr, t, tl, t0):                               # b7 "...kill a grown adult?"
    X = cut(cr, "mq_head", 330, 1120, 980, alpha=prog(t, t0, 0.3))
    amoeba(cr, 760, 1500, 16, t, prog(t, t0 + 0.2, 0.3))
    ring(cr, 760, 1500, 50, 40, prog(t, t0 + 0.3, 0.4))
    path(cr, [(740, 1470), X(*MQ_HEAD["mq_head"])], prog(t, t0 + 0.5, 0.6), 4, RED, 0.8, dash=[12, 10], arrow=True)
    why(cr, t, T(tl, "b7", "adult"), 820, 950)
    headline(cr, t, "HOW CAN IT KILL", "AN ADULT?", t0, T(tl, "b7", "kill"), t_ghost=t0)


def w_warm(cr, t, tl, t0):                               # b8 "it lives in warm, fresh water"
    _pic(cr, "pond_kerala", 500, 1080, 0, t, t0, frame=(820, 560), rot=-0.02)
    tw = T(tl, "b8", "warm")
    _pic(cr, "thermometer", 810, 1420, 520, t, tw - 0.2, rot=-0.15)
    for i in range(4):
        amoeba(cr, 260 + 140 * i, 1200 + 50 * math.sin(i * 1.7), 20, t + i, prog(t, t0 + 0.4 + 0.15 * i, 0.3), seed=i)
    headline(cr, t, "IT LIVES IN WARM", "FRESH WATER", t0, T(tl, "b8", "fresh"))


def w_where(cr, t, tl, t0):                              # b8 "ponds, lakes, rivers, and badly kept pools"
    items = (("pond_assam", "Ponds", "PONDS"), ("lake_swim", "lakes", "LAKES"), ("boys_river", "rivers", "RIVERS"),
             ("pool_dark", "pools", "BADLY KEPT POOLS"))
    for i, (key, cue, label) in enumerate(items):
        tc = T(tl, "b8", cue) - 0.2
        cx, cy = 290 + 500 * (i % 2), 760 + 500 * (i // 2)
        _pic(cr, key, cx, cy, 0, t, tc, frame=(440, 330), rot=(-0.03, 0.03, 0.02, -0.02)[i])
        draw_text(cr, label, cx, cy + 190, 40, INK, prog(t, tc, 0.3), anchor="ct")
    headline(cr, t, "PONDS, LAKES,", "RIVERS, POOLS", t0, T(tl, "b8", "pools"), big_size=130)


def w_heat(cr, t, tl, t0):                               # b9 "it loves heat."
    _pic(cr, "sun_sky", W / 2, 900, 0, t, t0, frame=(820, 560), rot=0.02)
    gauge(cr, t, t0 + 0.3, W / 2, 1480, 200, 0.2, 0.92, labels=("COOL", "HOT"))
    headline(cr, t, "IT LOVES", "HEAT", t0, T(tl, "b9", "heat"))


def w_spell(cr, t, tl, t0):                              # b9 "...cases usually come after long, hot spells"
    _pic(cr, "cracked_earth", W / 2, 900, 0, t, t0, frame=(820, 560), rot=-0.02)
    calendar(cr, t, T(tl, "b9", "long") - 0.1, W / 2, 1420, ["WEEK 1", "WEEK 2", "WEEK 3"], "HOT SPELL",
             interval=0.3, w=360, h=300, circle_last=False)
    headline(cr, t, "AFTER LONG", "HOT SPELLS", t0, T(tl, "b9", "spells"))


def w_drink(cr, t, tl, t0):                              # b10 "drinking that water won't infect you"
    ti = T(tl, "b10", "infect")
    X = cut(cr, "glass", 330, 1130, 640, alpha=prog(t, t0, 0.3))
    x0, y0 = X(0.10, 0.45)                                               # water in the glass
    x1, y1 = X(0.90, 0.97)
    cr.set_source_rgba(*WATER, 0.35 * prog(t, t0, 0.3))
    _round(cr, x0 + 20, y0, x1 - x0 - 40, y1 - y0, 30)
    cr.fill()
    tick(cr, 680, 980, 170, prog(t, ti, 0.4), color=GREEN)
    card(cr, t, ti, 600, 1240, ["SWALLOWED:", "DOESN'T INFECT"], size=42)
    headline(cr, t, "DRINKING IT", "WON'T INFECT YOU", t0, ti, big_color=GREEN, big_size=120)


def w_danger(cr, t, tl, t0):                             # b10 "...the danger is your nose" (real profile photo)
    tn = T(tl, "b10", "nose")
    fw, fh = 700, 960
    _pic(cr, "profile_photo", W / 2, 1100, 0, t, t0, frame=(fw, fh), rot=0.0)
    ring(cr, W / 2 - fw / 2 + 0.29 * fw, 1100 - fh / 2 + 0.425 * fh, 80, 70, prog(t, tn, 0.4), width=12)
    stamp(cr, t, "THE WAY IN", tn + 0.25, 780, 1640, 56)
    headline(cr, t, "THE DANGER IS YOUR", "NOSE", t0, tn)


def m_shoot(cr, t, tl, t0):                              # b11 "water shoots up your nose, the amoeba travels to the top"
    ttop = T(tl, "b11", "top")
    X = lineart(cr, 520, 1120, 1000)
    nose_channel(cr, X, 1.0)
    nx, ny = X(*HEAD_PTS["nostril"])
    path(cr, [(nx + 60, ny + 200), (nx, ny), X(*HEAD_PTS["nose_mid"]), X(*HEAD_PTS["top"])],
         prog(t, t0 + 0.1, 0.9), 20, (0.25, 0.55, 0.80), 0.9, arrow=True)
    f = AT_TOP * clamp((t - t0 - 0.6) / max(0.5, ttop - t0 - 0.4))
    amoeba(cr, *route(X, f), 28, t, prog(t, t0 + 0.6, 0.3))
    headline(cr, t, "WATER UP YOUR NOSE,", "TO THE TOP", t0, ttop)


def m_there(cr, t, tl, t0):                              # b12 "there, ..." the top of the nose
    X = lineart(cr, 520, 1120, 1000)
    nose_channel(cr, X, 1.0)
    ring(cr, *X(*HEAD_PTS["top"]), 90, 55, prog(t, t0, 0.4), width=8)
    amoeba(cr, *route(X, AT_TOP), 28, t)
    headline(cr, t, "AT THE TOP OF", "YOUR NOSE", t0, t0 + 0.2)


def m_follow(cr, t, tl, t0):                             # b13 "it follows those nerves, straight into your brain" (slate)
    X = lineart(cr, 520, 1120, 1000, dark=True)
    nose_channel(cr, X, 1.0, nerve=1.0)
    tb = T(tl, "b13", "brain")
    f = AT_TOP + (1 - AT_TOP) * clamp((t - t0) / max(0.6, tb - t0 + 0.3))
    for i in range(3):
        amoeba(cr, *route(X, max(AT_TOP, f - 0.1 * i)), 26, t + i, prog(t, t0 + 0.2 * i, 0.3), seed=i)
    ring(cr, *X(*HEAD_PTS["deep"]), 130, 100, prog(t, tb, 0.4), color=CORAL)
    headline(cr, t, "STRAIGHT INTO YOUR", "BRAIN", t0, tb, small_color=CREAM, big_color=CORAL)


def r_scary(cr, t, tl, t0):                              # b14 re-hook: "and the scariest part?"
    X = cut(cr, "mq_sit", 420, 1200, 820)
    hx, hy = X(*MQ_HEAD["mq_sit"])

    def lens(c):
        c.set_source_rgba(*BRAIN, 1)
        c.paint()
        amoeba(c, 800, 760, 60, t)
    magnifier(cr, t, t0 + 0.2, 800, 760, 190, lens)
    path(cr, [(hx + 40, hy), (640, 770)], prog(t, t0 + 0.2, 0.3), 3, INK, 0.7)
    headline(cr, t, "THE SCARIEST", "PART?", t0, T(tl, "b14", "part"), t_ghost=t0)


def r_fever(cr, t, tl, t0):                              # b14 "...the first signs look like a normal fever"
    cut(cr, "thermometer", 520, 1150, 700, alpha=prog(t, t0, 0.3), rot=-0.1)
    card(cr, t, T(tl, "b14", "normal"), 300, 1480, ["\"IT'S JUST", "A FEVER\""], size=52, rot=0.03)
    headline(cr, t, "IT LOOKS LIKE A", "NORMAL FEVER", t0, T(tl, "b14", "fever"))


SIGNS = (("b15", "Headache", "HEADACHE"), ("b15", "Fever", "FEVER"), ("b15", "Vomiting", "VOMITING"),
         ("b16", "stiff", "STIFF NECK"), ("b16", "Confusion", "CONFUSION"), ("b16", "Seizures", "SEIZURES"))


def r_signs(cr, t, tl, t0):                              # b15 "headache. Fever. Vomiting."
    checklist(cr, t, 110, 560, 860, "FIRST SIGNS",
              [(lbl, T(tl, b, cue) - 0.15, "tick", T(tl, b, cue)) for b, cue, lbl in SIGNS[:3]])
    _pic(cr, "headache_man", W / 2, 1450, 470, t, t0)
    headline(cr, t, "THE FIRST", "SIGNS", t0, t0 + 0.3)


def r_worse(cr, t, tl, t0):                              # b16 "then a stiff neck. Confusion. Seizures."
    checklist(cr, t, 110, 560, 860, "THEN",
              [(lbl, T(tl, b, cue) - 0.15, "cross", T(tl, b, cue)) for b, cue, lbl in SIGNS[3:]])
    _pic(cr, "mq_sit", W / 2, 1420, 520, t, t0)
    headline(cr, t, "THEN IT GETS", "WORSE", t0, T(tl, "b16", "stiff"), big_color=RED)


def k_why(cr, t, tl, t0):                                # b18 re-hook: "so why did some patients in Kerala survive?"
    _pic(cr, "kerala_tank", W / 2, 1000, 0, t, t0, frame=(820, 615), rot=0.02)
    card(cr, t, t0 + 0.3, 110, 1400, ["KERALA"], size=56)
    why(cr, t, t0 + 0.4, 820, 1450, 300)
    headline(cr, t, "SO WHY DID SOME", "SURVIVE?", t0, T(tl, "b18", "survive"), t_ghost=t0, big_color=GREEN)


def k_test(cr, t, tl, t0):                               # b19 "because doctors there started testing for it early"
    te = T(tl, "b19", "early")
    _pic(cr, "blood_tubes", 680, 1360, 0, t, t0 + 0.3, frame=(560, 380), rot=0.03)
    _pic(cr, "microscope", 340, 1000, 640, t, t0)
    tick(cr, 760, 800, 150, prog(t, te, 0.4), color=GREEN)
    headline(cr, t, "THEY TESTED", "EARLY", t0, te, big_color=GREEN)


def k_treat(cr, t, tl, t0):                              # b19 "...and treating it fast"
    _pic(cr, "doctor", 560, 1240, 720, t, t0)
    tick(cr, 820, 760, 150, prog(t, T(tl, "b19", "fast"), 0.4), color=GREEN)
    headline(cr, t, "AND TREATED IT", "FAST", t0, T(tl, "b19", "fast"), big_color=GREEN)


def k_spread(cr, t, tl, t0):                             # b20 "and it doesn't spread from person to person"
    cut(cr, "mq_head", 250, 1150, 720, alpha=prog(t, t0, 0.3))
    cut(cr, "mq_head", 830, 1150, 720, alpha=prog(t, t0 + 0.1, 0.3), flip=True)
    path(cr, [(400, 1000), (680, 1000)], prog(t, t0 + 0.3, 0.4), 10, INK, 0.8, arrow=True)
    cross(cr, 540, 1000, 160, prog(t, T(tl, "b20", "person"), 0.3))
    stamp(cr, t, "MYTH", T(tl, "b20", "spread"), 540, 1620, 80)
    headline(cr, t, "IT DOESN'T", "SPREAD", t0, T(tl, "b20", "spread"), big_color=GREEN)


def d_hold(cr, t, tl, t0):                               # b21 "hold your nose, or wear a nose clip, when you jump in"
    _pic(cr, "boy_pier", W / 2, 1200, 0, t, t0, frame=(860, 484), rot=-0.02)
    tc = T(tl, "b21", "clip")
    nose_clip(cr, 800, 800, 200, prog(t, tc - 0.2, 0.3))
    tick(cr, 900, 680, 110, prog(t, tc + 0.2, 0.3), color=GREEN)
    card(cr, t, tc, 110, 700, ["NOSE CLIP"], size=48)
    headline(cr, t, "IN FRESH WATER:", "HOLD YOUR NOSE", t0, T(tl, "b21", "hold"), big_color=GREEN, big_size=130)


def d_mud(cr, t, tl, t0):                                # b22 "don't stir up the mud in shallow, warm water"
    _pic(cr, "mud_boots", W / 2, 1060, 0, t, t0, frame=(820, 656), rot=0.02)
    cross(cr, W / 2, 1060, 300, prog(t, T(tl, "b22", "mud"), 0.4))
    headline(cr, t, "DON'T STIR UP", "THE MUD", t0, T(tl, "b22", "mud"), big_color=GREEN)


def d_neti(cr, t, tl, t0):                               # b23 "if you rinse your nose, like with a neti pot..."
    tb = T(tl, "b23", "boiled")
    neti(cr, 300, 1000, 130, prog(t, t0, 0.3))
    card(cr, t, T(tl, "b23", "neti"), 110, 1180, ["NETI POT", "JAL NETI"], size=44)
    _pic(cr, "pot_stove", 700, 1380, 0, t, tb - 0.2, frame=(560, 373), rot=0.03)
    tick(cr, 820, 1120, 140, prog(t, T(tl, "b23", "cooled"), 0.4), color=GREEN)
    small, big = ("RINSING YOUR", "NOSE?") if t < tb - 0.2 else ("USE BOILED,", "COOLED WATER")
    headline(cr, t, small, big, t0 if big == "NOSE?" else tb - 0.2, T(tl, "b23", "rinse") if big == "NOSE?" else tb,
             big_color=GREEN, big_size=130)


def d_tap(cr, t, tl, t0):                                # b23 "...never straight from the tap"
    _pic(cr, "tap", W / 2, 1100, 760, t, t0)
    cross(cr, W / 2 + 60, 1200, 320, prog(t, T(tl, "b23", "tap"), 0.4))
    headline(cr, t, "NEVER STRAIGHT", "FROM THE TAP", t0, T(tl, "b23", "tap"), big_size=130)


def d_doctor(cr, t, tl, t0):                             # b24 "bad headache and fever after swimming: see a doctor"
    td = T(tl, "b24", "doctor")
    _pic(cr, "lake_swim", 760, 700, 0, t, t0, frame=(420, 280), rot=0.03)
    checklist(cr, t, 110, 880, 860, "AFTER A SWIM", [("BAD HEADACHE", T(tl, "b24", "headache") - 0.15, "tick",
                                                       T(tl, "b24", "headache")),
                                                      ("FEVER", T(tl, "b24", "fever") - 0.15, "tick",
                                                       T(tl, "b24", "fever"))])
    _pic(cr, "doctor", 760, 1460, 420, t, td - 0.2)
    headline(cr, t, "AFTER A SWIM?", "SEE A DOCTOR", t0, td, big_color=GREEN, big_size=130)


def d_tell(cr, t, tl, t0):                               # b24 "...tell them you swam"
    _pic(cr, "doctor", 620, 1250, 700, t, -1)
    card(cr, t, t0 + 0.1, 110, 640, ["\"DOCTOR, I SWAM", "IN A POND 3 DAYS AGO\""], size=48, rot=0.02)
    tick(cr, 860, 900, 120, prog(t, T(tl, "b24", "swam"), 0.4), color=GREEN)
    headline(cr, t, "TELL THEM", "YOU SWAM", t0, T(tl, "b24", "swam"), big_color=GREEN)


def e_bookend(cr, t, tl, t0):                            # b25 "it's rare. But one splash up your nose is all it needs."
    _jump(cr, t, t0, T(tl, "b25", "splash") - 0.5, T(tl, "b25", "splash") + 0.1)
    headline(cr, t, "ONE SPLASH IS", "ALL IT NEEDS", t0, T(tl, "b25", "needs"), t_ghost=t0, big_size=130)


def e_question(cr, t, tl, t0):                           # b26 "do you swim in ponds, rivers or lakes? YES or NO"
    _pic(cr, "boys_river", W / 2, 1360, 0, t, -1, frame=(820, 546), rot=-0.02)
    yes_no_card(cr, t, T(tl, "b26", "Yes") - 0.2, 540, 820, w=700, h=320, question="COMMENT: YES OR NO")
    headline(cr, t, "DO YOU SWIM IN", "PONDS?", t0, T(tl, "b26", "ponds"), t_ghost=t0)


def n_name(cr, t, tl, t0):                               # b5 "it's called Naegleria fowleri. The brain-eating amoeba."
    if P["micrograph"]:
        _pic(cr, "micrograph", W / 2, 880, 0, t, t0, frame=(820, 560))
    else:
        amoeba(cr, W / 2, 860, 200, t)
    tn = T(tl, "b5", "called")
    for i, (txt, ty, sz, cue) in enumerate((("NAEGLERIA FOWLERI", 1230, 92, tn),
                                            ("THE BRAIN-EATING AMOEBA", 1370, 60, T(tl, "b5", "brain")))):
        p = prog(t, cue, 0.3)
        if p > 0:
            tw_, th = text_size(txt, sz)
            cr.set_source_rgba(*RED, 0.92)
            cr.rectangle(MARGIN, ty - 12, (tw_ + 50) * p, th + 24)
            cr.fill()
            draw_text(cr, txt, MARGIN + 25, ty, sz, CREAM, clamp(p * 2 - 1))
    if P["micrograph"]:                                  # the reference labels real photos: "TISSUE CYST / REAL · USDA"
        card(cr, t, t0 + 0.3, 620, 1120 - 470, ["IN BRAIN TISSUE", "REAL · CDC"], size=34, rot=0.03)
    headline(cr, t, "ITS NAME", "", t0, 1e9)


def n_kerala(cr, t, tl, t0):                             # b6 "in 2025, amoeba brain infections hit ~170 in Kerala"
    tk = T(tl, "b6", "Kerala")
    kx, ky = kerala(cr, 350, 1100, 680, prog(t, t0, 0.3), lit=prog(t, t0 + 0.4, 0.4))
    ring(cr, kx, ky, 55, 75, prog(t, tk + 0.2, 0.4))
    t170 = T(tl, "b6", "hundred")
    counter(cr, t, t170 - 0.3, 850, 940, "170", 140, color=GOLD)
    draw_text(cr, "CASES", 850, 1040, 54, INK, prog(t, t170, 0.3), anchor="ct")
    card(cr, t, t0 + 0.2, 640, 1250, ["KERALA, 2025", "AMOEBA BRAIN", "INFECTIONS"], size=40)
    headline(cr, t, "KERALA, 2025:", "170 CASES", t0, t170)


def n_died(cr, t, tl, t0):                               # b6 "...forty-two of them died"
    icon_array(cr, t, t0 - 0.2, 170, 17, 120, 640, 40, red=range(42), red_at=t0 + 0.4, step=0.004)
    counter(cr, t, t0 + 0.3, W / 2, 1480, "42", 170, color=RED)
    draw_text(cr, "DIED", W / 2, 1600, 60, RED, prog(t, t0 + 0.6, 0.3), anchor="ct")
    footnote(cr, "Govt of India, Lok Sabha reply, Dec 2025", prog(t, t0, 0.3), y=1700)
    headline(cr, t, "AND", "42 DIED", t0, t0 + 0.3)


def m_holes(cr, t, tl, t0):                              # b12 "...the bone has tiny holes" (Gray's ethmoid bone)
    th = T(tl, "b12", "holes")
    _pic(cr, "gray_ethmoid", W / 2, 900, 0, t, t0, frame=(760, 656))
    magnifier(cr, t, th - 0.2, 760, 1350, 230, lambda c: zoom_photo(c, "gray_ethmoid", 760, 1350, 0.47, 0.5, 1900, 1640))
    path(cr, [(W / 2 - 25, 900), (640, 1180)], prog(t, th - 0.2, 0.3), 3, INK, 0.7)
    stamp(cr, t, "TINY HOLES", th, 300, 1560, 58)
    headline(cr, t, "THE BONE HAS", "TINY HOLES", t0, th)


def m_nerves(cr, t, tl, t0):                             # b12 "your smell nerves pass through them, into the brain"
    _pic(cr, "gray_olfactory", W / 2, 960, 0, t, t0, frame=(860, 620))
    card(cr, t, T(tl, "b12", "smell"), 120, 1340, ["SMELL NERVES", "NOSE > BONE > BRAIN"], size=44)
    headline(cr, t, "SMELL NERVES GO", "STRAIGHT UP", t0, T(tl, "b12", "brain"))


def m_eat(cr, t, tl, t0):                                # b13 "...and it starts eating brain tissue" (Gray's brain)
    _pic(cr, "gray_brain", W / 2, 1000, 0, t, t0, frame=(860, 640))
    card(cr, t, t0 + 0.4, 600, 1350, ["HUMAN BRAIN", "GRAY'S ANATOMY, 1918"], size=34)
    spots = [(0.12, 0.2), (-0.2, 0.05), (0.25, -0.15), (-0.05, -0.25), (0.3, 0.25), (-0.3, -0.1), (0.0, 0.1)]
    for i, (dx, dy) in enumerate(spots):
        f = prog(t, t0 + 0.3 + 0.25 * i, 0.5)
        if f > 0:
            cr.set_source_rgba(0.45, 0.05, 0.07, 0.7 * f)
            cr.arc(W / 2 + dx * 860, 1000 + dy * 640, 30 + 40 * f, 0, 2 * math.pi)
            cr.fill()
    for i in range(4):
        amoeba(cr, W / 2 + spots[i][0] * 860, 1000 + spots[i][1] * 640, 34, t + i, prog(t, t0 + 0.2 * i, 0.3), seed=i)
    headline(cr, t, "AND IT STARTS", "EATING", t0, T(tl, "b13", "eating"), big_color=CORAL)


def r_fast(cr, t, tl, t0):                               # b16 "...it moves very fast"
    calendar(cr, t, t0 + 0.1, W / 2, 1050, ["DAY 1", "DAY 2", "DAY 3", "DAY 4", "DAY 5"], "AFTER SYMPTOMS",
             interval=0.22)
    footnote(cr, "CDC: death usually within about 5 days of symptoms", prog(t, t0, 0.3), y=1500)
    headline(cr, t, "IT MOVES", "FAST", t0, T(tl, "b16", "fast"))


def r_rare(cr, t, tl, t0):                               # b17 "it's very rare. But nearly everyone who gets it dies."
    tn = T(tl, "b17", "nearly")
    if t < tn - 0.15:
        gauge(cr, t, t0 + 0.1, W / 2, 1150, 260, 0.6, 0.06, labels=("RARE", "COMMON"))
        stamp(cr, t, "VERY RARE", T(tl, "b17", "rare"), W / 2, 1400, 80, color=GREEN)
        headline(cr, t, "IT'S VERY", "RARE", t0, T(tl, "b17", "rare"), big_color=GREEN)
        return
    icon_array(cr, t, tn - 0.15, 100, 10, 170, 700, 52, red=range(97), red_at=T(tl, "b17", "dies"), step=0.006)
    footnote(cr, "CDC: over 97% of known US cases died (1962-2024)", prog(t, tn, 0.3), y=1640)
    headline(cr, t, "BUT 97 IN 100", "DIE", tn - 0.15, T(tl, "b17", "dies"))


SHOTS = [   # (line, cue where the shot starts, draw function, background)
    ("b1", None, h_you, "paper"), ("b1", "few", h_days, "paper"), ("b1", "something", h_eating, "paper"),
    ("b2", None, h_nose, "slate"), ("b2", "climbed", h_climb, "slate"), ("b3", None, h_hurt, "paper"),
    ("b4", None, h_movie, "paper"), ("b5", None, n_name, "paper"), ("b6", None, n_kerala, "paper"),
    ("b6", "Forty", n_died, "paper"), ("b7", None, s_hair, "paper"), ("b7", "kill", s_kill, "paper"),
    ("b8", None, w_warm, "paper"), ("b8", "Ponds", w_where, "paper"), ("b9", None, w_heat, "paper"),
    ("b9", "Cases", w_spell, "paper"), ("b10", None, w_drink, "paper"), ("b10", "danger", w_danger, "paper"),
    ("b11", None, m_shoot, "paper"), ("b12", None, m_there, "paper"), ("b12", "bone", m_holes, "paper"),
    ("b12", "smell", m_nerves, "paper"), ("b13", None, m_follow, "slate"), ("b13", "eating", m_eat, "paper"),
    ("b14", None, r_scary, "paper"), ("b14", "first", r_fever, "paper"), ("b15", None, r_signs, "paper"),
    ("b16", None, r_worse, "paper"), ("b16", "moves", r_fast, "paper"), ("b17", None, r_rare, "paper"),
    ("b18", None, k_why, "paper"), ("b19", None, k_test, "paper"), ("b19", "treating", k_treat, "paper"),
    ("b20", None, k_spread, "paper"), ("b21", None, d_hold, "paper"), ("b22", None, d_mud, "paper"),
    ("b23", None, d_neti, "paper"), ("b23", "Never", d_tap, "paper"), ("b24", None, d_doctor, "paper"),
    ("b24", "Tell", d_tell, "paper"), ("b25", None, e_bookend, "paper"), ("b26", None, e_question, "paper"),
]


def draw(cr, t, tl):
    draw_frame(cr, t, tl, SHOTS)


def sfx(tl):
    """A whoosh on every cut, thuds on stamps, a tick (and the bed dipping) before the name, each re-hook and the
    closing line, a splash in the hook and the bookend, typing under the YES/NO card."""
    ev = [(s, "whoosh", 0.25) for s in starts(tl, SHOTS)[1:]]
    ev += [(T(tl, "b3", "already") + 0.2, "thud", 0.0), (T(tl, "b4", "real") + 0.2, "thud", 0.0),
           (T(tl, "b12", "holes"), "thud", 0.0), (T(tl, "b20", "spread"), "thud", 0.0)]
    for bid in ("b5", "b14", "b18", "b25"):
        ev.append((tl[bid].start - 0.45, "tick", 0.0))
    ev += [(T(tl, "b26", "Yes"), "typing", 1.0), (tl["b6"].start + 0.4, "pop", 0.0), (tl["b17"].start + 0.3, "pop", 0.0)]
    ev += [(at, "dip", 0.5) for at, name, _ in list(ev) if name == "tick"]
    return ev


def cover(cr):
    """Cover (Hinglish channel rule): a dark poster, one subject, at most three words, one big coloured key word,
    everything inside Instagram's 3:4 grid crop (y 240-1680)."""
    from poster import finish, slate
    slate(cr)
    X = lineart(cr, 540, 1180, 980, dark=True)
    for i, (u, v) in enumerate(((0.70, 0.22), (0.55, 0.15), (0.62, 0.30))):
        x, y = X(u, v)
        cr.set_source_rgba(0.75, 0.10, 0.12, 0.6)
        cr.arc(x, y, 70, 0, 2 * math.pi)
        cr.fill()
        amoeba(cr, x, y, 44, 1.0 + i, seed=i)
    draw_text(cr, "IT EATS YOUR", W / 2, 330, 96, CREAM, anchor="ct")
    draw_text(cr, "BRAIN", W / 2, 450, 230, CORAL, anchor="ct")
    finish(cr)
