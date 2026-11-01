"""Video 7 (tech): "Internet samundar ke neeche se aata hai" - how the internet reaches your phone through cables on
the ocean floor. Owner, 1 Nov 2026: "make next video auto approved" after skipping the AI video; earlier asked for
"how internet works with examples". Narration in Devanagari for the voice, numbers written as words.
Facts: ~99% of international data rides undersea cables (ITU 2025; some say 95%); 500+ cables in service
(TeleGeography counts ~570-600 in 2025); data travels as light in glass fibres (~2 lakh km/s); Jan 2008 cuts off
Alexandria disrupted India's internet by up to 60% (press estimate), rerouted within a day; most faults are fishing
gear and anchors, fish/shark bites ~0 (ICPC)."""
import math
import os

import cairo

from poster import (CORAL, CREAM, GOLD, GREEN, INK, MONO_FONT, RED, W, calendar, card, clamp, counter, cross,
                    draw_text, footnote, headline, path, person, prog, ring, stamp, tick, yes_no_card)

# the narrator, music and tail are channel-wide; render_hi reads them from this module
from channel import ASSETS_ROOT, MUSIC, NARRATOR, NARRATOR_LABEL, REVEAL_GAP, TAIL, VOICE_REF  # noqa: F401
from shots import T, asset_finder, draw_frame, pic, starts

SCRIPT = [
    dict(id="b1", text="सोचो, तुम्हारे फ़ोन पर जो रील चल रही है... वो सैटेलाइट से नहीं आई। "
                       "वो समुंदर के नीचे बिछी एक केबल से आई है।"),
    dict(id="b2", text="एक केबल, जो गार्डन पाइप जितनी पतली है... और दुनिया का क़रीब निन्यानवे परसेंट इंटरनेशनल इंटरनेट, "
                       "ऐसी ही केबल्स से चलता है।"),
    dict(id="b3", text="ये कोई कहानी नहीं है। समुंदर के नीचे, ऐसी पाँच सौ से ज़्यादा केबल्स बिछी हुई हैं।", gap=REVEAL_GAP),
    dict(id="b4", text="इनके अंदर तुम्हारा डेटा रोशनी बनकर चलता है। काँच के, बाल जितने पतले धागों में।"),
    dict(id="b5", text="और ये रोशनी, एक सेकंड में क़रीब दो लाख किलोमीटर चलती है।"),
    dict(id="b6", text="इसलिए मुंबई से अमेरिका तक तुम्हारा मैसेज, पलक झपकते पहुँच जाता है।"),
    dict(id="b7", text="भारत में ये केबल्स ज़्यादातर मुंबई और चेन्नई के समुंदर किनारे निकलती हैं।"),
    dict(id="b8", text="वहाँ से ज़मीन के नीचे फ़ाइबर, शहर-शहर जाता है... और आख़िर में टावर से हवा के रास्ते, तुम्हारे फ़ोन तक।"),
    dict(id="b9", text="पर समुंदर में ये केबल बिछती कैसे है? एक ख़ास जहाज़, हज़ारों किलोमीटर केबल लेकर चलता है... "
                       "और धीरे-धीरे उसे समुंदर की ज़मीन पर बिछाता जाता है।"),
    dict(id="b10", text="कई जगह ये केबल, कई किलोमीटर गहराई में पड़ी है। जहाँ अँधेरा है, और बहुत ठंड।"),
    dict(id="b11", text="पर सोचो... अगर ये केबल कट जाए तो?"),
    dict(id="b12", text="ये हो चुका है। दो हज़ार आठ में, मिस्र के पास समुंदर में दो केबल्स कटीं... "
                        "और भारत का साठ परसेंट तक इंटरनेट बिगड़ गया।"),
    dict(id="b13", text="लोग सोचते हैं, शार्क इन केबल्स को काट देती है। पर असल में शार्क का हाथ बहुत ही कम है।"),
    dict(id="b14", text="असली दुश्मन हैं: मछली पकड़ने वाले जाल, और जहाज़ों के लंगर। ज़्यादातर केबल्स यही तोड़ते हैं।"),
    dict(id="b15", text="तब एक रिपेयर जहाज़ जाता है। काँटे से केबल को समुंदर की तह से ऊपर खींचता है... और जोड़ देता है।"),
    dict(id="b16", text="और तब तक इंटरनेट दूसरी केबल्स से घूमकर आ जाता है। दो हज़ार आठ में भी, एक दिन में काम चल पड़ा था।",
         gap=REVEAL_GAP),
    dict(id="b17", text="सोचो, तुम बिस्तर पर लेटकर जो वीडियो देख रहे हो... वो समुंदर के नीचे, अँधेरे में, "
                        "कई किलोमीटर गहराई से रोशनी बनकर आया है।"),
    dict(id="b18", text="तुम्हें पता था कि इंटरनेट समुंदर के नीचे से आता है? यस या नो, कमेंट में बताओ।"),
]

METADATA = dict(
    title="Internet samundar ke neeche se aata hai",
    caption="Tumhari reel satellite se nahi aati... wo samundar ke neeche bichhi ek cable se aati hai 😳\n\n"
            "Garden pipe jitni patli cable, andar kaanch ke baal jitne dhaage, aur unmein tumhara data roshni bankar "
            "chalta hai. Duniya ka qareeb 99% international internet aisi hi 500+ cables se chalta hai.\n\n"
            "Cable kat jaaye toh? 2008 mein Misr ke paas do cables kati thi, aur Bharat ka 60% tak internet bigad "
            "gaya tha. Aur asli dushman shark nahi, machhli ke jaal aur jahaazon ke langar hain.\n\n"
            "Tumhe pata tha ki internet samundar ke neeche se aata hai? Comment mein YES ya NO likho 👇",
    yt_title="Internet Satellite Se Nahi, Samundar Se Aata Hai? 😳",
    yt_description="Tumhare phone ka internet asal mein kahan se aata hai: samundar ke neeche bichhi fibre optic "
                   "cables, jinmein data roshni bankar chalta hai. Ye cables Bharat mein Mumbai aur Chennai mein "
                   "aati hain, kat jaayein toh kya hota hai, aur inhe asal mein kaun todta hai.",
    hashtags=["#internet", "#techinhindi", "#howitworks", "#sciencefacts", "#factsinhindi"],
    pinned_comment="Tumhe pata tha ki internet samundar ke neeche se aata hai? 🌊 YES ya NO? 👇",
    sources=["ITU 2025, submarine cables and international data",
             "TeleGeography, Submarine Cable Map and FAQ",
             "2008 submarine cable disruption (Arab News, TeleGeography)",
             "International Cable Protection Committee, causes of cable faults"],
)

_find = asset_finder("net", "toxoplasma2", "krait2", "mosquito")
P = {k: _find(k) for k in ("satellite", "cable_ship", "fibre", "shark", "anchor", "fishing_net", "world_map",
                           "human_hair", "stopwatch", "earth_globe", "india_map")}
USED_ASSETS = [os.path.basename(v) for v in P.values() if v]
CREDITS_FILES = [os.path.join(ASSETS_ROOT, d, "credits.json") for d in ("net", "toxoplasma2", "krait2", "mosquito")]

CABLE, LIGHT, SAND = (0.08, 0.08, 0.09), (0.55, 0.95, 1.0), (0.30, 0.26, 0.20)
MAP = (W / 2, 1060, 520)        # world_map.png drawn at this centre and height; its width is 1.884 x its height
INDIA = (W / 2, 1100, 760)      # india_map.png likewise; its width is 0.909 x its height
# places in percent of each map image (measured on a grid laid over it)
WP = dict(mumbai=(70.0, 43.5), chennai=(73.8, 47.5), alex=(57.5, 34.0), france=(50.0, 29.5), uk=(47.5, 22.5),
          newyork=(20.5, 31.0), singapore=(81.0, 55.0), japan=(88.5, 31.0), la=(8.5, 34.0), mombasa=(60.5, 57.5),
          brazil=(31.0, 60.0), lagos=(51.0, 51.0), perth=(84.5, 73.0))
ROUTES = [["mumbai", (64, 47), (61, 44), (59.5, 40), "alex", (53, 31.5), "france"],       # India-Europe via Suez
          ["chennai", (76, 52), "singapore"], ["singapore", (84, 46), (87, 38), "japan"],
          ["france", (45, 30), (35, 31), "newyork"], ["uk", (40, 25), (30, 26), "newyork"],
          ["japan", (99.5, 33)], [(0.5, 33), "la"], ["mumbai", (63, 50), "mombasa"],
          ["newyork", (25, 45), (30, 55), "brazil"], ["france", (45, 38), (45, 48), "lagos"],
          ["chennai", (74, 58), (78, 66), "perth"], ["singapore", (82, 63), "perth"]]
IP = dict(mumbai=(17, 56), chennai=(42, 73), delhi=(33, 28), kolkata=(67, 47), bengaluru=(33, 75),
          hyderabad=(36, 61), ahmedabad=(16, 45), lucknow=(45, 33), jaipur=(25, 33), pune=(20, 59))


def _pic(cr, key, cx, cy, h, t, t0, **kw):
    pic(cr, P.get(key), cx, cy, h, t, t0, **kw)


# ---------- drawing pieces for this video ----------

def mp(p, m=MAP, aspect=1.884):
    """A place (name or (fx, fy) percent) on a map drawn at m = (cx, cy, height)."""
    fx, fy = WP[p] if isinstance(p, str) else p
    cx, cy, h = m
    return cx + (fx / 100 - 0.5) * aspect * h, cy + (fy / 100 - 0.5) * h


def ip(p):
    fx, fy = IP[p]
    return mp((fx, fy), INDIA, 0.909)


def along(pts, f):
    """The point a fraction f of the way along a polyline."""
    seg = [math.dist(a, b) for a, b in zip(pts, pts[1:])]
    d = clamp(f) * sum(seg)
    for (a, b), s in zip(zip(pts, pts[1:]), seg):
        if d <= s and s > 0:
            return a[0] + (b[0] - a[0]) * d / s, a[1] + (b[1] - a[1]) * d / s
        d -= s
    return pts[-1]


def glow(cr, x, y, r, color=LIGHT, alpha=1.0):
    for k, a in ((2.6, 0.12), (1.6, 0.3), (1.0, 1.0)):
        cr.arc(x, y, r * k, 0, 2 * math.pi)
        cr.set_source_rgba(*color, a * alpha)
        cr.fill()


def pulses(cr, t, pts, n=6, speed=0.5, r=9, alpha=1.0):
    """Light pulses running along a cable."""
    for k in range(n):
        x, y = along(pts, (t * speed + k / n) % 1)
        glow(cr, x, y, r, alpha=alpha)


def world(cr, t, t0, routes=ROUTES, p_routes=1.0, alpha=1.0, pins=()):
    _pic(cr, "world_map", MAP[0], MAP[1], MAP[2], t, t0, tint=(0.55, 0.47, 0.38), alpha=alpha)
    for i, r in enumerate(routes):
        pts = [mp(q) for q in r]
        path(cr, pts, clamp(p_routes * len(routes) - i), 5, RED, 0.85 * alpha)
    for name in pins:
        x, y = mp(name)
        cr.arc(x, y, 11, 0, 2 * math.pi)
        cr.set_source_rgba(*GOLD, alpha)
        cr.fill()


def sea(cr, top=560, alpha=1.0):
    """Under the water: blue at the top, almost black at the bottom."""
    g = cairo.LinearGradient(0, top, 0, 1920)
    g.add_color_stop_rgba(0, 0.12, 0.38, 0.52, alpha)
    g.add_color_stop_rgba(1, 0.01, 0.04, 0.09, alpha)
    cr.rectangle(0, top, W, 1920 - top)
    cr.set_source(g)
    cr.fill()


def seabed(cr, y=1560, alpha=1.0):
    cr.move_to(0, 1920)
    for k in range(13):
        x = W * k / 12
        cr.line_to(x, y + 22 * math.sin(k * 1.7))
    cr.line_to(W, 1920)
    cr.close_path()
    cr.set_source_rgba(*SAND, alpha)
    cr.fill()


def bed_cable(y=1560):
    """A cable lying along seabed(y)."""
    return [(x, y - 14 + 22 * math.sin(x / W * 12 * 1.7)) for x in range(-20, 1101, 28)]


def cable(cr, pts, width=16, alpha=1.0, p=1.0):
    path(cr, pts, p, width, CABLE, alpha)


def surface(cr, y=640, alpha=1.0):
    """The sea surface seen from the side: a wavy line, sky above it."""
    cr.rectangle(0, 560, W, y - 560)
    cr.set_source_rgba(0.80, 0.88, 0.93, alpha)
    cr.fill()
    pts = [(W * k / 30, y + 8 * math.sin(k * 0.9)) for k in range(31)]
    path(cr, pts, 1.0, 6, (0.95, 0.98, 1.0), alpha)


def ship(cr, x, y, s=1.0, alpha=1.0):
    """A small ship on the surface line at y (side view)."""
    cr.move_to(x - 150 * s, y - 40 * s)
    cr.line_to(x + 160 * s, y - 40 * s)
    cr.line_to(x + 120 * s, y + 20 * s)
    cr.line_to(x - 130 * s, y + 20 * s)
    cr.close_path()
    cr.set_source_rgba(0.75, 0.15, 0.12, alpha)
    cr.fill()
    cr.rectangle(x - 60 * s, y - 100 * s, 110 * s, 60 * s)
    cr.set_source_rgba(0.95, 0.95, 0.92, alpha)
    cr.fill()
    cr.rectangle(x - 120 * s, y - 120 * s, 14 * s, 80 * s)
    cr.set_source_rgba(*INK, alpha)
    cr.fill()


def hook(cr, x, y, s=1.0, alpha=1.0):
    """A three-pronged grapnel hanging at (x, y)."""
    cr.set_source_rgba(0.75, 0.75, 0.78, alpha)
    cr.set_line_width(8 * s)
    cr.move_to(x, y - 40 * s)
    cr.line_to(x, y + 56 * s)                             # the shank, and the middle prong
    cr.stroke()
    for a in (-1, 1):                                     # two curved side prongs
        cr.new_sub_path()
        cr.arc(x + a * 26 * s, y + 30 * s, 26 * s, 0 if a < 0 else math.pi / 2, math.pi / 2 if a < 0 else math.pi)
        cr.stroke()


def cross_section(cr, x, y, r, p=1.0, alpha=1.0):
    """The cable cut open: plastic, steel wires, copper, and the glass fibres in the middle."""
    layers = ((1.0, (0.10, 0.10, 0.11)), (0.86, (0.92, 0.92, 0.90)), (0.70, (0.55, 0.56, 0.60)),
              (0.52, (0.80, 0.48, 0.22)), (0.36, (0.96, 0.93, 0.80)))
    for i, (k, c) in enumerate(layers):
        q = clamp(p * len(layers) - i) * alpha
        cr.arc(x, y, r * k, 0, 2 * math.pi)
        cr.set_source_rgba(*c, q)
        cr.fill()
    q = clamp(p * len(layers) - 2.5) * alpha                  # the steel wires
    for i in range(16):
        a = 2 * math.pi * i / 16
        cr.arc(x + 0.61 * r * math.cos(a), y + 0.61 * r * math.sin(a), 0.075 * r, 0, 2 * math.pi)
        cr.set_source_rgba(0.40, 0.41, 0.45, q)
        cr.fill()
    q = clamp(p * len(layers) - 4) * alpha                    # the fibres, glowing
    for i, c in enumerate(((0.3, 0.8, 1.0), (1.0, 0.5, 0.3), (0.5, 1.0, 0.5), (1.0, 0.9, 0.3), (0.9, 0.5, 1.0),
                           (1.0, 1.0, 1.0))):
        a = 2 * math.pi * i / 6
        glow(cr, x + 0.17 * r * math.cos(a), y + 0.17 * r * math.sin(a), 0.05 * r, c, q)


def pipe_end(cr, x, y, r, alpha=1.0):
    """A garden pipe cut open: a green ring, hollow inside."""
    cr.arc(x, y, r, 0, 2 * math.pi)
    cr.set_source_rgba(0.20, 0.62, 0.25, alpha)
    cr.fill()
    cr.arc(x, y, r * 0.68, 0, 2 * math.pi)
    cr.set_source_rgba(0.10, 0.25, 0.12, alpha)
    cr.fill()


def eye(cr, x, y, w, open_=1.0, alpha=1.0):
    h = w * 0.45 * max(0.04, open_)
    cr.save()
    cr.translate(x, y)
    cr.scale(1, h / (w * 0.45))
    cr.move_to(-w / 2, 0)
    cr.curve_to(-w / 4, -w * 0.45, w / 4, -w * 0.45, w / 2, 0)
    cr.curve_to(w / 4, w * 0.45, -w / 4, w * 0.45, -w / 2, 0)
    cr.close_path()
    cr.set_source_rgba(1, 1, 1, alpha)
    cr.fill_preserve()
    cr.set_source_rgba(*INK, alpha)
    cr.set_line_width(6)
    cr.stroke()
    cr.arc(0, 0, w * 0.17, 0, 2 * math.pi)
    cr.set_source_rgba(0.35, 0.22, 0.12, alpha)
    cr.fill()
    cr.arc(0, 0, w * 0.08, 0, 2 * math.pi)
    cr.set_source_rgba(0, 0, 0, alpha)
    cr.fill()
    cr.restore()


def tower(cr, x, y, h, t, alpha=1.0):
    """A phone tower (lattice) with its base at (x, y), sending waves."""
    top = y - h
    for s in (-1, 1):
        path(cr, [(x + s * h * 0.18, y), (x + s * h * 0.04, top)], 1.0, 8, INK, alpha)
    for k in range(1, 8):
        yy = y - h * k / 8
        w1 = h * (0.18 - 0.14 * k / 8)
        w0 = h * (0.18 - 0.14 * (k - 1) / 8)
        path(cr, [(x - w0, yy + h / 8), (x + w1, yy)], 1.0, 4, INK, 0.8 * alpha)
        path(cr, [(x + w0, yy + h / 8), (x - w1, yy)], 1.0, 4, INK, 0.8 * alpha)
    for s in (-1, 1):
        cr.rectangle(x + s * h * 0.07 - 10, top + 20, 20, 80)
        cr.set_source_rgba(0.85, 0.85, 0.85, alpha)
        cr.fill()
    for k in range(3):
        rr = 60 + 70 * ((t * 0.8 + k / 3) % 1)
        cr.new_sub_path()
        cr.arc(x, top + 40, rr, -0.6, 0.6)
        cr.set_source_rgba(*RED, alpha * (1 - ((t * 0.8 + k / 3) % 1)))
        cr.set_line_width(6)
        cr.stroke()


def rrect(cr, x, y, w, h, r):
    cr.new_sub_path()
    cr.arc(x + w - r, y + r, r, -math.pi / 2, 0)
    cr.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    cr.arc(x + r, y + h - r, r, math.pi / 2, math.pi)
    cr.arc(x + r, y + r, r, math.pi, 3 * math.pi / 2)
    cr.close_path()


def phone_reel(cr, cx, cy, h, t, alpha=1.0):
    """A plain phone (no brand) playing a reel: colour screen, play mark, a moving progress bar, a heart."""
    w = h * 0.49
    x, y = cx - w / 2, cy - h / 2
    rrect(cr, x + 10, y + 16, w, h, w * 0.12)
    cr.set_source_rgba(0, 0, 0, 0.22 * alpha)
    cr.fill()
    rrect(cr, x, y, w, h, w * 0.12)
    cr.set_source_rgba(0.13, 0.13, 0.14, alpha)
    cr.fill()
    sx, sy, sw, sh = x + w * 0.05, y + h * 0.06, w * 0.9, h * 0.89
    g = cairo.LinearGradient(sx, sy, sx + sw, sy + sh)
    g.add_color_stop_rgba(0, 0.45, 0.25, 0.70, alpha)
    g.add_color_stop_rgba(1, 0.98, 0.55, 0.25, alpha)
    rrect(cr, sx, sy, sw, sh, w * 0.08)
    cr.set_source(g)
    cr.fill()
    cr.move_to(cx - 40, cy - 55)
    cr.line_to(cx + 55, cy)
    cr.line_to(cx - 40, cy + 55)
    cr.close_path()
    cr.set_source_rgba(1, 1, 1, 0.85 * alpha)
    cr.fill()
    cr.rectangle(sx + 20, sy + sh - 40, (sw - 40) * ((t * 0.12) % 1), 8)
    cr.set_source_rgba(1, 1, 1, alpha)
    cr.fill()
    draw_text(cr, "<3", sx + sw - 40, sy + sh * 0.6, 44, (1, 1, 1), alpha, MONO_FONT, "cm")
    return sx, sy, sw, sh


def lying_person(cr, x, y, alpha=1.0):
    """Someone lying on a bed, looking at a glowing phone."""
    rrect(cr, x - 330, y, 660, 70, 16)
    cr.set_source_rgba(0.55, 0.40, 0.28, alpha)
    cr.fill()
    rrect(cr, x - 330, y - 40, 660, 50, 16)
    cr.set_source_rgba(0.92, 0.90, 0.85, alpha)
    cr.fill()
    cr.save()
    cr.translate(x + 270, y - 30)                         # feet at the foot of the bed, head towards the pillow end
    cr.rotate(-math.pi / 2)
    person(cr, 0, 0, 480, INK, alpha)
    cr.restore()
    glow(cr, x - 150, y - 190, 26, (0.8, 0.9, 1.0), alpha)
    rrect(cr, x - 175, y - 245, 50, 90, 8)
    cr.set_source_rgba(0.13, 0.13, 0.14, alpha)
    cr.fill()


# ---------- shots ----------
# Rules (style bible): a new picture every ~3 s cut on the word, the literal noun on screen, red = the key word,
# gold = numbers; the glowing light pulse in the cable is the one recurring picture (your data as light).

def h_reel(cr, t, tl, t0):                               # b1 frame 0: "the reel on your phone... did not come from a satellite"
    phone_reel(cr, 360, 1150, 820, t)
    ts = T(tl, "b1", "सैटेलाइट")
    _pic(cr, "satellite", 820, 820, 260, t, ts - 0.2, rot=-0.1)
    cross(cr, 820, 830, 170, prog(t, T(tl, "b1", "नहीं"), 0.3))
    headline(cr, t, "THIS REEL CAME FROM", "UNDER THE SEA", -1, min(1.8, T(tl, "b1", "समुंदर")), t_ghost=-1)


def h_cable(cr, t, tl, t0):                              # b1 "...it came through a cable on the sea floor" (slate)
    sea(cr)
    seabed(cr)
    pts = bed_cable()
    cable(cr, pts, p=prog(t, t0, 0.8))
    pulses(cr, t, pts, n=7, alpha=prog(t, t0 + 0.5, 0.3))
    headline(cr, t, "IT CAME THROUGH", "A CABLE", t0, T(tl, "b1", "केबल"), small_color=CREAM, big_color=CORAL)


def s_pipe(cr, t, tl, t0):                               # b2 "a cable as thin as a garden pipe..."
    cross_section(cr, 330, 1100, 150, prog(t, t0, 1.2))
    pipe_end(cr, 760, 1100, 150, prog(t, T(tl, "b2", "पाइप") - 0.2, 0.3))
    draw_text(cr, "THE CABLE", 330, 1300, 50, INK, prog(t, t0 + 0.4, 0.3), anchor="ct")
    draw_text(cr, "A GARDEN PIPE", 760, 1300, 50, INK, prog(t, T(tl, "b2", "पाइप"), 0.3), anchor="ct")
    headline(cr, t, "AS THIN AS A", "GARDEN PIPE", t0, T(tl, "b2", "पाइप"))


def s_99(cr, t, tl, t0):                                 # b2 "...and ~99% of international internet runs on such cables"
    _pic(cr, "earth_globe", W / 2, 1050, 520, t, t0)
    counter(cr, t, T(tl, "b2", "निन्यानवे") - 0.2, W / 2 - 40, 1450, "99", 150, color=GOLD)
    draw_text(cr, "%", W / 2 + 70, 1450, 120, INK, prog(t, T(tl, "b2", "निन्यानवे"), 0.2), anchor="lm")
    headline(cr, t, "INTERNATIONAL INTERNET:", "99% BY CABLE", t0, T(tl, "b2", "निन्यानवे"))


def m_map(cr, t, tl, t0):                                # b3 "not a story: 500+ cables under the sea"
    world(cr, t, t0, p_routes=prog(t, t0 + 0.3, 2.5))
    counter(cr, t, T(tl, "b3", "सौ") - 0.2, W / 2, 1480, "500+", 120, color=GOLD)
    stamp(cr, t, "NOT A STORY", t0 + 0.3, 800, 700, 56)
    headline(cr, t, "UNDER THE SEA:", "500+ CABLES", t0, T(tl, "b3", "सौ"))


def f_light(cr, t, tl, t0):                              # b4 "inside, your data travels as light..." (slate)
    cross_section(cr, W / 2, 1150, 330, 1.0)
    for i in range(6):                                   # the fibres pulse
        a = 2 * math.pi * i / 6
        glow(cr, W / 2 + 56 * math.cos(a), 1150 + 56 * math.sin(a), 20 + 6 * math.sin(t * 8 + i), alpha=0.6)
    headline(cr, t, "INSIDE, YOUR DATA IS", "LIGHT", t0, T(tl, "b4", "रोशनी"), small_color=CREAM, big_color=CORAL)


def f_glass(cr, t, tl, t0):                              # b4 "...in glass threads thin as a hair"
    _pic(cr, "fibre", W / 2, 960, 0, t, t0, frame=(860, 520))
    _pic(cr, "human_hair", 300, 1430, 0, t, t0 + 0.4, frame=(360, 260), rot=-0.03)
    card(cr, t, t0 + 0.7, 560, 1380, ["GLASS FIBRE", "AS THIN AS A HAIR"], size=44)
    headline(cr, t, "GLASS THREADS,", "THIN AS A HAIR", t0, t0 + 0.4)


def f_speed(cr, t, tl, t0):                              # b5 "this light travels about 2 lakh km in one second"
    _pic(cr, "stopwatch", 260, 1100, 380, t, t0)
    pts = [(480, 1100), (1060, 1100)]
    path(cr, pts, 1.0, 10, CABLE, prog(t, t0, 0.3))
    pulses(cr, t, pts, n=4, speed=2.0)
    counter(cr, t, t0 + 0.4, 760, 1350, "2,00,000", 70, color=GOLD)
    draw_text(cr, "KM EVERY SECOND", 760, 1430, 50, INK, prog(t, t0 + 0.8, 0.3), anchor="ct")
    headline(cr, t, "IN ONE SECOND:", "2 LAKH KM", t0, T(tl, "b5", "लाख"))


def f_blink(cr, t, tl, t0):                              # b6 "so Mumbai to America, in the blink of an eye"
    route = [mp(q) for q in ("mumbai", (64, 47), (61, 44), (59.5, 40), "alex", (53, 31.5), "france", (45, 30),
                             (35, 31), "newyork")]
    world(cr, t, t0 - 2, routes=[ROUTES[0], ROUTES[3]], pins=("mumbai", "newyork"))
    f = prog(t, t0 + 0.4, 1.4)
    x, y = along(route, f)
    path(cr, route, f, 8, GOLD, 0.9)
    glow(cr, x, y, 12)
    blink = 1 - abs(math.sin(math.pi * clamp((t - t0 - 1.0) / 0.4))) if t > t0 + 1.0 else 1.0
    eye(cr, W / 2, 1480, 260, blink)
    headline(cr, t, "MUMBAI TO AMERICA:", "IN A BLINK", t0, T(tl, "b6", "पलक"))


def i_landing(cr, t, tl, t0):                            # b7 "in India they come ashore at Mumbai and Chennai"
    _pic(cr, "india_map", INDIA[0], INDIA[1], INDIA[2], t, t0)
    for name, cue, sea_pts in (("mumbai", "मुंबई", [(0, 1260), (60, 1180)]),
                               ("chennai", "चेन्नई", [(W, 1390), (1020, 1330)])):
        x, y = ip(name)
        p = prog(t, T(tl, "b7", cue) - 0.3, 0.6)
        path(cr, sea_pts + [(x, y)], p, 8, RED, 0.9)
        cr.arc(x, y, 14 * p, 0, 2 * math.pi)
        cr.set_source_rgba(*GOLD, p)
        cr.fill()
        draw_text(cr, name.upper(), x + 30, y - 20, 44, INK, p, anchor="lb")
    headline(cr, t, "THEY COME ASHORE IN", "MUMBAI & CHENNAI", t0, T(tl, "b7", "चेन्नई"))


def i_cities(cr, t, tl, t0):                             # b8 "from there, fibre under the ground, city to city..."
    _pic(cr, "india_map", INDIA[0], INDIA[1], INDIA[2], t, t0 - 1)
    links = (("mumbai", "pune"), ("mumbai", "ahmedabad"), ("ahmedabad", "jaipur"), ("jaipur", "delhi"),
             ("delhi", "lucknow"), ("lucknow", "kolkata"), ("mumbai", "hyderabad"), ("chennai", "bengaluru"),
             ("chennai", "hyderabad"), ("hyderabad", "kolkata"), ("bengaluru", "pune"))
    for i, (a, b) in enumerate(links):
        q = prog(t, t0 + 0.1 + 0.12 * i, 0.4)
        path(cr, [ip(a), ip(b)], q, 5, GOLD, 0.95)
    for name in IP:
        x, y = ip(name)
        cr.arc(x, y, 10, 0, 2 * math.pi)
        cr.set_source_rgba(*INK, 0.9)
        cr.fill()
    headline(cr, t, "THEN, UNDERGROUND,", "CITY TO CITY", t0, t0 + 0.3)


def i_tower(cr, t, tl, t0):                              # b8 "...and at last from a tower, through the air, to your phone"
    tower(cr, 330, 1500, 720, t, prog(t, t0, 0.3))
    phone_reel(cr, 830, 1250, 520, t, prog(t, t0 + 0.3, 0.3))
    headline(cr, t, "LAST STOP:", "TOWER TO PHONE", t0, T(tl, "b8", "हवा"))


def l_ship(cr, t, tl, t0):                               # b9 "how is it laid? a special ship carries 1000s of km of cable"
    _pic(cr, "cable_ship", W / 2, 1060, 0, t, t0, frame=(900, 600))
    card(cr, t, t0 + 1.0, 110, 1450, ["A CABLE SHIP", "CARRIES 1000s OF KM"], size=46)
    headline(cr, t, "HOW IS IT LAID?", "BY A SHIP", t0, t0 + 0.9)


def l_lay(cr, t, tl, t0):                                # b9 "...and slowly lays it on the sea floor" (slate)
    sea(cr, top=640)
    surface(cr)
    seabed(cr)
    f = prog(t, t0, 3.0)
    sx = 900 - 700 * f                                    # the ship moves left, paying out cable behind it
    ship(cr, sx, 640)
    bed = [(x, 1545) for x in range(1100, int(sx) - 260, -20)] + [(sx - 260, 1545)]
    cable(cr, bed + [(sx - 120, 1100), (sx + 60, 650)])
    headline(cr, t, "SLOWLY, ON THE", "SEA FLOOR", t0, t0 + 0.6, small_color=CREAM, big_color=CORAL)


def d_deep(cr, t, tl, t0):                               # b10 "in places it lies kilometres deep, dark and very cold" (slate)
    sea(cr, top=560)
    seabed(cr, 1700)
    cable(cr, [(-20, 1690), (1100, 1690)])
    pulses(cr, t, [(-20, 1690), (1100, 1690)], n=5, speed=0.3)
    for k in range(9):                                    # a depth scale down the left
        y = 640 + 1000 * k / 8
        path(cr, [(60, y), (100, y)], 1.0, 4, CREAM, 0.8)
        draw_text(cr, f"{k} KM", 115, y, 36, CREAM, 0.9, MONO_FONT, "lm")
    card(cr, t, T(tl, "b10", "ठंड"), 560, 1200, ["DARK.", "NEAR FREEZING."], size=48)
    headline(cr, t, "IT LIES KILOMETRES", "DEEP", t0, T(tl, "b10", "गहराई"), small_color=CREAM, big_color=CORAL)


def q_cut(cr, t, tl, t0):                                # b11 re-hook: "but what if the cable breaks?" (slate)
    p = prog(t, t0 + 0.5, 0.4)
    cable(cr, [(60, 1150), (W / 2 - 30 - 40 * p, 1150 + 30 * p)], width=40)
    cable(cr, [(W / 2 + 30 + 40 * p, 1150 - 30 * p), (1020, 1150)], width=40)
    pulses(cr, t, [(60, 1150), (W / 2 - 40, 1150)], n=4, speed=0.6)
    draw_text(cr, "?", W / 2, 900, 300, CORAL, prog(t, t0 + 0.6, 0.3), anchor="cm")
    headline(cr, t, "BUT WHAT IF IT", "BREAKS?", t0, T(tl, "b11", "कट"), small_color=CREAM, big_color=CORAL)


def c_2008(cr, t, tl, t0):                               # b12 "it has happened: 2008, two cables cut near Egypt"
    world(cr, t, t0, routes=ROUTES[:4], pins=("alex",))
    x, y = mp("alex")
    cross(cr, x, y, 90, prog(t, T(tl, "b12", "कटीं") - 0.2, 0.3))
    card(cr, t, T(tl, "b12", "मिस्र"), 600, 760, ["NEAR EGYPT"], size=48)
    counter(cr, t, t0 + 0.2, W / 2, 1480, "2008", 120, color=GOLD)
    headline(cr, t, "IT HAPPENED:", "2 CABLES CUT", t0, T(tl, "b12", "कटीं"))


def c_india(cr, t, tl, t0):                              # b12 "...and up to 60% of India's internet was hit"
    _pic(cr, "india_map", INDIA[0], INDIA[1], INDIA[2], t, t0, tint=(0.45, 0.42, 0.38))
    counter(cr, t, t0 + 0.2, W / 2 - 40, 1160, "60", 200, color=GOLD)
    draw_text(cr, "%", W / 2 + 100, 1160, 160, CREAM, prog(t, t0 + 0.4, 0.2), anchor="lm")
    draw_text(cr, "UP TO", W / 2, 960, 70, CREAM, prog(t, t0 + 0.1, 0.3), anchor="cb")
    headline(cr, t, "INDIA'S INTERNET:", "UP TO 60% HIT", t0, T(tl, "b12", "साठ"), small_color=CREAM,
             big_color=CORAL)


def k_shark(cr, t, tl, t0):                              # b13 "people think sharks bite them... sharks hardly ever do"
    _pic(cr, "shark", W / 2, 1050, 0, t, t0, frame=(880, 580))
    ta = T(tl, "b13", "असल")
    cross(cr, W / 2, 1050, 260, prog(t, ta, 0.3))
    stamp(cr, t, "ALMOST NEVER", ta + 0.3, W / 2, 1450, 70)
    headline(cr, t, "SHARKS?", "ALMOST NEVER", t0, ta)


def k_enemy(cr, t, tl, t0):                              # b14 "the real enemy: fishing nets and ships' anchors"
    _pic(cr, "fishing_net", 330, 1020, 0, t, T(tl, "b14", "मछली") - 0.3, frame=(560, 400), rot=-0.03)
    _pic(cr, "anchor", 800, 1180, 520, t, T(tl, "b14", "लंगर") - 0.3)
    stamp(cr, t, "MOST CABLE BREAKS", T(tl, "b14", "यही"), W / 2, 1560, 60)
    headline(cr, t, "THE REAL ENEMY:", "NETS & ANCHORS", t0, T(tl, "b14", "लंगर"))


def r_hook(cr, t, tl, t0):                               # b15 "a repair ship comes; a hook pulls the cable up..." (slate)
    sea(cr, top=640)
    surface(cr)
    seabed(cr)
    ship(cr, W / 2, 640)
    tp = T(tl, "b15", "खींचता")
    down = prog(t, t0 + 0.3, 1.2)
    up = prog(t, tp, 1.4)
    hy = 700 + 840 * down - 600 * up
    path(cr, [(W / 2 + 100, 640), (W / 2 + 100, hy)], 1.0, 5, CREAM, 0.9)
    hook(cr, W / 2 + 100, hy)
    sag = 1540 - 600 * up                                  # the cable lifts in the middle as the hook rises
    cable(cr, [(-20, 1545), (W / 2 - 120, 1545 - (1545 - sag) * 0.6), (W / 2 + 100, sag + 60),
               (W / 2 + 320, 1545 - (1545 - sag) * 0.6), (1100, 1545)])
    tick(cr, W / 2 + 230, 1000, 90, prog(t, T(tl, "b15", "देता"), 0.3), color=GREEN)
    headline(cr, t, "A REPAIR SHIP", "HOOKS IT UP", t0, tp, small_color=CREAM, big_color=CORAL)


def w_reroute(cr, t, tl, t0):                            # b16 "meanwhile the internet comes round through other cables"
    world(cr, t, t0, routes=[ROUTES[0], ROUTES[7], ["mombasa", (50, 70), (40, 75), (30, 60), "newyork"]],
          pins=("mumbai",))
    x, y = mp("alex")
    cross(cr, x, y, 70, 1.0)
    detour = [mp(q) for q in ("mumbai", (63, 50), "mombasa", (50, 70), (40, 75), (30, 60), "newyork")]
    f = prog(t, t0 + 0.3, 2.0)
    path(cr, detour, f, 8, GREEN, 0.9)
    glow(cr, *along(detour, f), 12)
    headline(cr, t, "DATA TAKES", "ANOTHER CABLE", t0, t0 + 0.3, big_color=GREEN)


def w_day(cr, t, tl, t0):                                # b16 "...in 2008 too, things ran again within a day"
    calendar(cr, t, t0 + 0.1, W / 2, 1150, ["CUT", "DAY 1"], "2008", interval=0.6, w=380, h=400)
    tick(cr, W / 2 + 230, 1300, 100, prog(t, t0 + 1.2, 0.3), color=GREEN)
    headline(cr, t, "2008: WORKING AGAIN", "IN A DAY", t0, t0 + 0.4, big_color=GREEN)


def z_bed(cr, t, tl, t0):                                # b17 "socho: the video you watch lying in bed..."
    lying_person(cr, W / 2, 1300, prog(t, t0, 0.3))
    headline(cr, t, "THE VIDEO YOU WATCH", "IN BED...", t0, t0 + 0.3)


def z_journey(cr, t, tl, t0):                            # b17 "...came as light, from kilometres under the sea" (slate)
    sea(cr, top=560)
    seabed(cr, 1720)
    route = [(80, 1700), (540, 1700), (540, 1300), (900, 900), (900, 700)]
    path(cr, route, 1.0, 12, CABLE, 0.9)
    f = prog(t, t0 + 0.2, 2.4)
    glow(cr, *along(route, f), 18)
    phone_reel(cr, 900, 700, 260, t)
    headline(cr, t, "CAME AS LIGHT, FROM", "UNDER THE SEA", t0, T(tl, "b17", "रोशनी"), small_color=CREAM,
             big_color=CORAL)


def e_question(cr, t, tl, t0):                           # b18 "did you know the internet comes from under the sea?"
    phone_reel(cr, 300, 1300, 560, t, prog(t, t0, 0.3))
    yes_no_card(cr, t, t0 + 0.4, 690, 1000, w=600, h=300, question="COMMENT: YES OR NO")
    headline(cr, t, "DID YOU KNOW IT COMES FROM", "UNDER THE SEA?", t0, T(tl, "b18", "समुंदर"), t_ghost=t0)


SHOTS = [   # (line, cue where the shot starts, draw function, background)
    ("b1", None, h_reel, "paper"), ("b1", "समुंदर", h_cable, "slate"),
    ("b2", None, s_pipe, "paper"), ("b2", "दुनिया", s_99, "paper"),
    ("b3", None, m_map, "paper"),
    ("b4", None, f_light, "slate"), ("b4", "बाल", f_glass, "paper"),
    ("b5", None, f_speed, "paper"),
    ("b6", None, f_blink, "paper"),
    ("b7", None, i_landing, "paper"),
    ("b8", None, i_cities, "paper"), ("b8", "टावर", i_tower, "paper"),
    ("b9", None, l_ship, "paper"), ("b9", "धीरे", l_lay, "slate"),
    ("b10", None, d_deep, "slate"),
    ("b11", None, q_cut, "slate"),
    ("b12", None, c_2008, "paper"), ("b12", "भारत", c_india, "slate"),
    ("b13", None, k_shark, "paper"),
    ("b14", None, k_enemy, "paper"),
    ("b15", None, r_hook, "slate"),
    ("b16", None, w_reroute, "paper"), ("b16", "दो", w_day, "paper"),
    ("b17", None, z_bed, "paper"), ("b17", "समुंदर", z_journey, "slate"),
    ("b18", None, e_question, "paper"),
]


def draw(cr, t, tl):
    draw_frame(cr, t, tl, SHOTS)


def sfx(tl):
    """A whoosh on every cut, thuds on the crosses and stamps, ticks (and music dips) before the re-hook, the myth and
    the closing line, typing on the card."""
    ev = [(s, "whoosh", 0.25) for s in starts(tl, SHOTS)[1:]]
    ev += [(T(tl, "b1", "नहीं"), "thud", 0.0), (T(tl, "b12", "कटीं"), "thud", 0.0), (T(tl, "b13", "असल"), "thud", 0.0),
           (T(tl, "b11", None) - 0.35, "tick", 0.0), (T(tl, "b13", None) - 0.35, "tick", 0.0),
           (T(tl, "b18", None) - 0.35, "tick", 0.0), (T(tl, "b18", "यस"), "typing", 1.0)]
    for bid in ("b4", "b7", "b9", "b15"):
        ev.append((tl[bid].start + 0.4, "pop", 0.0))
    ev += [(at, "dip", 0.5) for at, name, _ in list(ev) if name == "tick"]   # the bed dips just before a reveal
    return ev
