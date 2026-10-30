"""Video 5: "Space se wapas aaya keeda, do sar ke saath" - the planarian that regrew a head at both ends after five
weeks on the ISS (Morokuma et al. 2017, Regeneration; Tufts). Script approved by the owner 30 Oct 2026 ("Approve";
scripts_batch3.md); narration below is that script word for word, in Devanagari for the voice, with numbers written
as words. It says 1 of 15, and that nobody knows why (the "fluke" critique is in line 17)."""
import math
import os
import random

import cairo

from poster import (CORAL, CREAM, GOLD, INK, MONO_FONT, RED, W, calendar, card, clamp, counter, draw_text, erase,
                    footnote, headline, path, person, photo_width, prog, ring, stamp, yes_no_card)

# the narrator, music and tail are channel-wide; render_hi reads them from this module
from channel import ASSETS_ROOT, MUSIC, NARRATOR, NARRATOR_LABEL, REVEAL_GAP, TAIL, VOICE_REF  # noqa: F401
from shots import T, asset_finder, draw_frame, pic, starts

SCRIPT = [
    dict(id="b1", text="सोचो, एक कीड़ा स्पेस गया... और वापस आया, तो उसके दो सिर थे। एक आगे, एक पीछे।"),
    dict(id="b2", text="और जब साइंटिस्ट्स ने उसके दोनों सिर काट दिए... तो जो हुआ, उसने सबको हिला दिया।"),
    dict(id="b3", text="ये कोई साइंस-फ़िक्शन नहीं है। ये अमेरिका की टफ्ट्स यूनिवर्सिटी का एक्सपेरिमेंट है, "
                       "जो इंटरनेशनल स्पेस स्टेशन पर हुआ।", gap=REVEAL_GAP),
    dict(id="b4", text="इस कीड़े का नाम है प्लेनेरियन। पानी में रहने वाला, एक-दो सेंटीमीटर का चपटा कीड़ा।"),
    dict(id="b5", text="छिपकली की पूँछ कट जाए, तो वापस उग आती है ना? ये कीड़ा उससे बहुत आगे है।"),
    dict(id="b6", text="इसे कई टुकड़ों में काट दो... तो हर टुकड़ा एक पूरा नया कीड़ा बन जाता है। सिर, दिमाग़, आँखें, सब।"),
    dict(id="b7", text="और हर टुकड़ा जानता है कि सिर किस तरफ़ बनाना है, और पूँछ किस तरफ़। "
                       "जैसे शरीर के अंदर कोई नक्शा हो।"),
    dict(id="b8", text="तो साइंटिस्ट्स ने सोचा: स्पेस में, जहाँ ग्रैविटी ना के बराबर है, ये नक्शा कैसे काम करेगा?"),
    dict(id="b9", text="दो हज़ार पंद्रह में पंद्रह कीड़ों के सिर और पूँछ काटे गए, और उन्हें पाँच हफ़्ते के लिए "
                       "स्पेस स्टेशन भेज दिया गया।"),
    dict(id="b10", text="वापस आए, तो पहला झटका: कीड़े सिकुड़ के पड़े थे, हिल भी नहीं रहे थे। "
                        "दो घंटे बाद जाकर नॉर्मल हुए।"),
    dict(id="b11", text="और फिर... पंद्रह में से एक टुकड़े ने सिर उगाया। पर एक नहीं... दो। पूँछ की जगह भी सिर।",
         gap=REVEAL_GAP),
    dict(id="b12", text="साइंटिस्ट्स ने कहा: अठारह साल में उन्होंने इस कीड़े में अपने आप ऐसा कभी नहीं देखा था।"),
    dict(id="b13", text="पर असली झटका तो इसके बाद आया।"),
    dict(id="b14", text="धरती पर साइंटिस्ट्स ने दोनों सिर काट दिए। बीच का टुकड़ा बचा... और उसने फिर से दो सिर उगा लिए।"),
    dict(id="b15", text="मतलब ये कोई एक बार की ग़लती नहीं लगती। जैसे इसका नक्शा ही बदल गया हो।"),
    dict(id="b16", text="और बाक़ी कीड़े भी बदले। वो अँधेरे में कम रहने लगे, और बीस महीने बाद भी उनका बर्ताव अलग था।"),
    dict(id="b17", text="पर ऐसा हुआ क्यों? साइंटिस्ट्स को आज भी पक्का नहीं पता। कुछ कहते हैं ये बस इत्तेफ़ाक़ हो सकता है, "
                        "क्योंकि पंद्रह में से सिर्फ़ एक था।", gap=REVEAL_GAP),
    dict(id="b18", text="सोचो, अगर स्पेस सच में शरीर का नक्शा बदल सकता है... तो सालों तक मंगल पर रहने वाले इंसानों का "
                        "क्या होगा?"),
    dict(id="b19", text="क्या स्पेस ने इस कीड़े का नक्शा बदल दिया? यस या नो, कमेंट में बताओ।"),
]

METADATA = dict(
    title="Space se wapas aaya keeda, do sar ke saath",
    caption="Ek keeda space gaya... aur wapas aaya toh uske do sar the. Phir scientists ne dono kaat diye 😳\n\n"
            "2015 mein Tufts University ne 15 planarian keedon ke sar aur poonchh kaat ke unhe 5 hafte ke liye "
            "International Space Station bheja. Wapas aake 15 mein se ek ne dono taraf sar uga liya. Dono sar kaate, "
            "toh beech wale tukde ne phir se do sar uga liye.\n\n"
            "Kyun hua, ye aaj bhi pakka nahi pata. Kuch scientists kehte hain ye bas ittefaq ho sakta hai.\n\n"
            "Kya space ne is keede ka naksha badal diya? Comment mein YES ya NO likho 👇",
    yt_title="Space Se Wapas Aaya Keeda, Do Sar Ke Saath 😳 | Planarian",
    yt_description="2015 mein Tufts University ke scientists ne planarian flatworms ko 5 hafte ke liye International "
                   "Space Station bheja. 15 mein se ek kata hua tukda wapas aake dono taraf sar ke saath ugaa, aur "
                   "dono sar kaatne par beech ke tukde ne phir se do sar uga liye. Kyun hua, ye aaj bhi pakka nahi "
                   "pata.",
    hashtags=["#space", "#planarian", "#science", "#sciencefacts", "#factsinhindi"],
    pinned_comment="Kya space ne is keede ka naksha badal diya? 🪱 YES ya NO? 👇",
    sources=["Morokuma et al. 2017, Planarian regeneration in space, Regeneration (Tufts University)",
             "Sluys & Stocchino 2017, and the authors' reply, Regeneration",
             "ISS National Laboratory, Space Worms Have Scientists Seeing Double (Heads)"],
)

_find = asset_finder("planarian", "mosquito", "toxoplasma2", "speaker", "krait2")
P = {k: _find(k) for k in ("planarian.", "planarian_twohead", "iss", "rocket_launch", "gecko", "mars", "astronaut",
                           "scissors", "clapperboard", "world_map", "petri_dish", "earth_globe", "balance_scale",
                           "clock", "eraser_plain")}
P["planarian"] = P.pop("planarian.")
USED_ASSETS = [os.path.basename(v) for v in P.values() if v]
CREDITS_FILES = [os.path.join(ASSETS_ROOT, d, "credits.json") for d in ("planarian", "mosquito", "toxoplasma2",
                                                                         "speaker", "krait2")]

WORM, WORM_D, WORM_L = (0.47, 0.34, 0.21), (0.30, 0.20, 0.12), (0.68, 0.55, 0.38)
BLAST = (0.93, 0.80, 0.74)               # fresh regrowing tissue (the blastema) is pale before it darkens
BLUE = (0.15, 0.31, 0.52)                # the blueprint: the video's one metaphor, the body's "naksha"


def _pic(cr, key, cx, cy, h, t, t0, **kw):
    pic(cr, P.get(key), cx, cy, h, t, t0, **kw)


# ---------- drawing pieces for this video ----------

def _spline(cr, pts):
    """Closed Catmull-Rom curve through pts."""
    n = len(pts)
    cr.move_to(*pts[0])
    for i in range(n):
        p0, p1, p2, p3 = pts[i - 1], pts[i], pts[(i + 1) % n], pts[(i + 2) % n]
        cr.curve_to(p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6,
                    p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6, p2[0], p2[1])
    cr.close_path()


def _end(kind, g, hw, w):
    """Outline (u, v) of a left-pointing end at u = 0, from the top edge round the tip to the bottom edge.
    A head is the planarian's arrow shape with its two side flaps; g (0-1) grows it out of the cut."""
    if kind == "head" and g > 0:
        L, e = 1.15 * w * g, 0.55 + 0.45 * g
        pts = [(-0.30 * L, -hw * 1.05 * e), (-0.48 * L, -hw * 1.5 * e), (-0.6 * L, -hw * 0.85),
               (-0.86 * L, -hw * 0.5), (-L, 0)]
    elif kind == "tail" and g > 0:
        L = 1.5 * w * g
        pts = [(-0.5 * L, -hw * 0.62), (-0.92 * L, -hw * 0.18), (-L, 0)]
    else:                                                  # a fresh cut: a flat end
        pts = [(-0.04 * w, -hw * 0.5), (-0.05 * w, 0)]
    return [(0, -hw)] + pts + [(u, -v) for u, v in reversed(pts[:-1])] + [(0, hw)]


def worm(cr, cx, cy, length, w=100, left="head", right="tail", gl=1.0, gr=1.0, rot=0.0, alpha=1.0, wiggle=0.0,
         t=0.0, ghost=False):
    """A planarian centred at (cx, cy); `length` is the trunk between its two ends. Each end is "head", "tail" or
    "cut"; gl/gr (0-1) grow that end out of pale new tissue. ghost: only a dashed cream outline (on the blueprint)."""
    if alpha <= 0:
        return
    hw, n = w / 2, 10

    def xy(u, v):
        return u - length / 2, v + wiggle * w * 0.35 * math.sin(2 * math.pi * u / max(length, 1) + t * 2.5)

    top = [(length * k / n, -hw * (1 + 0.08 * math.sin(math.pi * k / n))) for k in range(1, n)]
    pts = (list(reversed(_end(left, gl, hw, w))) + top + [(length - u, v) for u, v in _end(right, gr, hw, w)]
           + [(u, -v) for u, v in reversed(top)])
    pts = [xy(u, v) for u, v in pts]
    cr.save()
    cr.translate(cx, cy)
    cr.rotate(rot)
    if ghost:
        _spline(cr, pts)
        cr.set_source_rgba(*CREAM, alpha)
        cr.set_line_width(5)
        cr.set_dash([16, 10])
        cr.stroke()
        cr.restore()
        return
    cr.save()
    cr.translate(8, 12)
    _spline(cr, pts)
    cr.set_source_rgba(0, 0, 0, 0.18 * alpha)
    cr.fill()
    cr.restore()
    grad = cairo.LinearGradient(0, -hw * 1.5, 0, hw * 1.5)
    for s, c in ((0, WORM_L), (0.5, WORM_D), (1, WORM_L)):
        grad.add_color_stop_rgba(s, *c, alpha)
    _spline(cr, pts)
    cr.set_source(grad)
    cr.fill_preserve()
    cr.set_source_rgba(*WORM_D, 0.7 * alpha)
    cr.set_line_width(3)
    cr.stroke()
    for kind, g, x_end, sgn in ((left, gl, -length / 2, -1), (right, gr, length / 2, 1)):
        if kind != "cut" and 0 < g < 1:                    # new tissue, still pale
            cr.save()
            _spline(cr, pts)
            cr.clip()
            cr.rectangle(x_end if sgn > 0 else x_end - 400, -w * 3, 400, w * 6)
            cr.set_source_rgba(*BLAST, 0.85 * (1 - g) * alpha)
            cr.fill()
            cr.restore()
        if kind == "head" and g > 0.5:                     # two eye-spots, pupils to the middle: the cross-eyed look
            a = clamp((g - 0.5) / 0.4) * alpha
            u = (0 if sgn < 0 else length) + sgn * 0.6 * 1.15 * w * g
            for side in (-1, 1):
                ex, ey = xy(u, side * hw * 0.34)
                cr.save()
                cr.translate(ex, ey)
                cr.scale(1, 0.78)
                cr.arc(0, 0, w * 0.12, 0, 2 * math.pi)
                cr.set_source_rgba(1, 1, 1, a)
                cr.fill()
                cr.restore()
                px, py = xy(u, side * hw * 0.22)
                cr.arc(px, py, w * 0.055, 0, 2 * math.pi)
                cr.set_source_rgba(0.05, 0.04, 0.03, a)
                cr.fill()
    cr.restore()


def cut_line(cr, x, y, h, p, alpha=1.0):
    """A red dashed cut mark across the worm at x."""
    if p <= 0:
        return
    path(cr, [(x, y - h / 2), (x, y - h / 2 + h * p)], 1.0, 6, RED, 0.9 * alpha, dash=[14, 9])


def blueprint(cr, cx, cy, w, h, alpha=1.0, rot=0.0, title="BODY MAP"):
    """The body's map: a blue drafting sheet with a grid, a border and a title."""
    if alpha <= 0:
        return
    cr.save()
    cr.translate(cx, cy)
    cr.rotate(rot)
    cr.set_source_rgba(0, 0, 0, 0.22 * alpha)
    cr.rectangle(-w / 2 + 10, -h / 2 + 14, w, h)
    cr.fill()
    cr.set_source_rgba(*BLUE, alpha)
    cr.rectangle(-w / 2, -h / 2, w, h)
    cr.fill()
    cr.set_source_rgba(1, 1, 1, 0.13 * alpha)
    cr.set_line_width(2)
    for gx in range(int(-w / 2) + 40, int(w / 2), 40):
        cr.move_to(gx, -h / 2)
        cr.line_to(gx, h / 2)
    for gy in range(int(-h / 2) + 40, int(h / 2), 40):
        cr.move_to(-w / 2, gy)
        cr.line_to(w / 2, gy)
    cr.stroke()
    cr.set_source_rgba(*CREAM, 0.8 * alpha)
    cr.set_line_width(3)
    cr.rectangle(-w / 2 + 14, -h / 2 + 14, w - 28, h - 28)
    cr.stroke()
    draw_text(cr, title, -w / 2 + 32, -h / 2 + 28, 28, CREAM, alpha, MONO_FONT)
    cr.restore()


def mono(cr, text, x, y, size, color=CREAM, alpha=1.0, anchor="cm"):
    draw_text(cr, text, x, y, size, color, alpha, MONO_FONT, anchor)


def curled(cr, x, y, r, rot, alpha=1.0):
    """A worm curled up tight and not moving (how they came back)."""
    pts = [(x + r * (0.2 + 0.8 * k / 30) * math.cos(rot + 3.4 * math.pi * k / 30),
            y + r * (0.2 + 0.8 * k / 30) * math.sin(rot + 3.4 * math.pi * k / 30)) for k in range(31)]
    path(cr, pts, 1.0, r * 0.42, WORM, alpha)


def dish(cr, cx, cy, r, n_dark, alpha=1.0, seed=1):
    """A dish half dark, half light, with 20 small worms: n_dark of them on the dark half."""
    cr.arc(cx, cy, r, 0, 2 * math.pi)
    cr.set_source_rgba(*CREAM, alpha)
    cr.fill()
    cr.move_to(cx, cy - r)
    cr.arc_negative(cx, cy, r, -math.pi / 2, math.pi / 2)
    cr.close_path()
    cr.set_source_rgba(*INK, 0.85 * alpha)
    cr.fill()
    cr.arc(cx, cy, r, 0, 2 * math.pi)
    cr.set_source_rgba(*INK, 0.6 * alpha)
    cr.set_line_width(6)
    cr.stroke()
    rng = random.Random(seed)
    for i in range(20):
        dark = i < n_dark
        a = rng.uniform(math.pi / 2 + 0.25, 3 * math.pi / 2 - 0.25) if dark else rng.uniform(-math.pi / 2 + 0.25,
                                                                                           math.pi / 2 - 0.25)
        d = rng.uniform(0.25, 0.8) * r
        x, y, o = cx + d * math.cos(a), cy + d * math.sin(a), rng.uniform(0, math.pi)
        path(cr, [(x - 16 * math.cos(o), y - 16 * math.sin(o)), (x + 16 * math.cos(o), y + 16 * math.sin(o))], 1.0,
             10, WORM_L if dark else WORM, alpha)


def fifteen(cr, t, t0, cx, cy, glow=None, alpha=1.0):
    """The 15 cut pieces sent to space, in a 5 x 3 grid; `glow` (index, p) rings one of them."""
    for i in range(15):
        p = prog(t, t0 + 0.05 * i, 0.25)
        x, y = cx + (i % 5 - 2) * 170, cy + (i // 5 - 1) * 150
        worm(cr, x, y + 30 * (1 - p), 70, 46, "cut", "cut", alpha=p * alpha)
        if glow and glow[0] == i:
            ring(cr, x, y, 100, 60, glow[1], alpha=alpha)


# ---------- shots ----------
# Rules (style bible + parasite-reels study): a new picture every ~3 s cut on the word, the literal noun on screen,
# red = the key word, gold = numbers, dark slate for space; the blueprint "naksha" is the one recurring metaphor.

def h_twohead(cr, t, tl, t0):                            # b1 frame 0: "a worm went to space and came back with two heads"
    _pic(cr, "iss", 830, 690, 0, t, T(tl, "b1", "स्पेस") - 0.1, rot=0.04, frame=(340, 220))
    worm(cr, W / 2, 1150, 440, 150, "head", "head", wiggle=0.25, t=t)
    ring(cr, 234, 1150, 125, 125, prog(t, T(tl, "b1", "आगे"), 0.4))      # on each head (trunk ends at 320 / 760)
    ring(cr, 846, 1150, 125, 125, prog(t, T(tl, "b1", "पीछे"), 0.4))
    footnote(cr, "illustration", 0.8)
    headline(cr, t, "IT CAME BACK FROM SPACE WITH", "TWO HEADS", -1, min(1.8, T(tl, "b1", "दो")), t_ghost=-1)


def h_snip(cr, t, tl, t0):                               # b2 "and when scientists cut off both its heads..."
    tc = T(tl, "b2", "काट")
    p = prog(t, tc, 0.6)
    if p <= 0:                                           # the frame-0 worm, cut 30 px inside each head
        worm(cr, W / 2, 1150, 440, 150, "head", "head", wiggle=0.15, t=t)
    else:
        worm(cr, W / 2, 1150, 380, 150, "cut", "cut", wiggle=0.15, t=t)
        worm(cr, 335 - 130 * p, 1150 + 50 * p, 30, 150, "head", "cut", rot=-0.25 * p)
        worm(cr, 745 + 130 * p, 1150 + 50 * p, 30, 150, "cut", "head", rot=0.25 * p)
    for x in (350, 730):
        cut_line(cr, x, 1150, 260, prog(t, tc - 0.4, 0.3), 1 - prog(t, tc + 0.4, 0.3))
    _pic(cr, "scissors", 330, 860, 230, t, tc - 0.5, rot=0.5)
    headline(cr, t, "THEN THEY CUT OFF", "BOTH HEADS", t0, tc)


def h_shock(cr, t, tl, t0):                              # b2 "...what happened shocked everyone"
    s = 1 + 0.04 * math.sin(t * 6)
    worm(cr, W / 2, 1200, 380 * s, 150, "cut", "cut", wiggle=0.2, t=t)
    q = prog(t, t0 + 0.1, 0.3)
    draw_text(cr, "?", W / 2, 860, 320 * (0.8 + 0.2 * q), RED, q, anchor="cm")
    headline(cr, t, "WHAT HAPPENED NEXT", "SHOCKED EVERYONE", t0, t0 + 0.3)


def r_notscifi(cr, t, tl, t0):                           # b3 "this is no science fiction..."
    _pic(cr, "clapperboard", W / 2, 1080, 420, t, t0)
    stamp(cr, t, "NOT SCI-FI", t0 + 0.5, W / 2, 1400, 70)
    headline(cr, t, "THIS IS", "NOT SCI-FI", t0, t0 + 0.4)


def r_tufts(cr, t, tl, t0):                              # b3 "...an experiment by Tufts University in America"
    _pic(cr, "world_map", W / 2, 960, 440, t, t0, tint=(0.55, 0.47, 0.38))
    q = prog(t, t0 + 0.4, 0.3)
    cr.set_source_rgba(*RED, q)
    cr.arc(358, 896, 13, 0, 2 * math.pi)
    cr.fill()
    card(cr, t, t0 + 0.5, 90, 1240, ["TUFTS UNIVERSITY, USA"], size=46)
    headline(cr, t, "A REAL EXPERIMENT:", "TUFTS, USA", t0, t0 + 0.3)


def r_iss(cr, t, tl, t0):                                # b3 "...done on the International Space Station"
    _pic(cr, "iss", W / 2, 1060, 0, t, t0, frame=(880, 580))
    headline(cr, t, "AND IT HAPPENED ON THE", "SPACE STATION", t0, t0 + 0.3)


def n_name(cr, t, tl, t0):                               # b4 "its name is planarian"
    _pic(cr, "planarian", W / 2, 1080, 560, t, t0)
    ring(cr, 205, 905, 95, 70, prog(t, t0 + 0.8, 0.4))
    card(cr, t, t0 + 1.0, 90, 1420, ["2 EYE-SPOTS"], size=44)
    headline(cr, t, "ITS NAME:", "PLANARIAN", t0, t0 + 0.5)


def n_size(cr, t, tl, t0):                               # b4 "...lives in water, a flat worm 1-2 cm long"
    for i in range(3):                                   # water
        y = 1290 + 40 * i
        path(cr, [(150 + 30 * k, y + 8 * math.sin(k * 0.9 + t * 3 + i)) for k in range(27)],
             prog(t, t0, 0.6), 5, (0.35, 0.55, 0.70), 0.6)
    worm(cr, W / 2, 1000, 330, 90, "head", "tail", wiggle=0.3, t=t, alpha=prog(t, t0, 0.3))
    q = prog(t, t0 + 0.4, 0.4)                            # a scale bar under it
    path(cr, [(238, 1090), (238, 1110), (842, 1110), (842, 1090)], q, 5, INK, 0.8)
    draw_text(cr, "1-2 CM", W / 2, 1130, 70, INK, q, anchor="ct")
    headline(cr, t, "A FLAT WORM IN WATER,", "1-2 CM", t0, T(tl, "b4", "सेंटीमीटर"))


def l_gecko(cr, t, tl, t0):                              # b5 "a lizard's tail grows back, right?"
    if P.get("gecko"):
        h, cx, cy = 440, W / 2 + 40, 1100
        w = photo_width(P["gecko"], h)
        x0, tail = cx - w / 2, 0.45 * w
        g = prog(t, t0 + 0.7, 1.6)
        cr.save()
        cr.rectangle(x0 + tail * (1 - g) - 30, 0, W, 1920)      # the tail grows back from the cut
        cr.clip()
        _pic(cr, "gecko", cx, cy, h, t, t0)
        cr.restore()
        cut_line(cr, x0 + tail, cy + 40, 160, prog(t, t0 + 0.3, 0.3), 1 - g)
    headline(cr, t, "A LIZARD'S TAIL", "GROWS BACK", t0, T(tl, "b5", "उग"))


def l_beyond(cr, t, tl, t0):                             # b5 "...this worm is far ahead of that"
    _pic(cr, "gecko", 250, 1300, 170, t, t0 - 0.3)
    worm(cr, 640, 1000, 300, 110, "head", "tail", wiggle=0.3, t=t, alpha=prog(t, t0, 0.3))
    draw_text(cr, ">>", 400, 1180, 120, RED, prog(t, t0 + 0.3, 0.3), anchor="cm")
    headline(cr, t, "THIS WORM GOES", "WAY BEYOND", t0, t0 + 0.3)


def c_cut(cr, t, tl, t0):                                # b6 "cut it into many pieces..."
    tc = T(tl, "b6", "काट")
    p = prog(t, tc, 0.6)
    kinds = [("head", "cut"), ("cut", "cut"), ("cut", "cut"), ("cut", "tail")]
    if p <= 0:
        worm(cr, W / 2, 1100, 640, 110, "head", "tail", wiggle=0.2, t=t)
    else:
        for k, (l, r) in enumerate(kinds):
            worm(cr, 300 + 160 * k + (k - 1.5) * 70 * p, 1100 + 20 * math.sin(k * 2.1) * p, 160, 110, l, r,
                 rot=0.06 * (k - 1.5) * p)
    for k in (1, 2, 3):
        cut_line(cr, 220 + 160 * k, 1100, 220, prog(t, tc - 0.4, 0.3), 1 - prog(t, tc + 0.3, 0.3))
    _pic(cr, "scissors", 560, 830, 210, t, tc - 0.5, rot=0.5)
    headline(cr, t, "CUT IT INTO", "PIECES", t0, tc)


def c_regrow(cr, t, tl, t0):                             # b6 "...every piece becomes a whole new worm"
    g = prog(t, t0 + 0.2, 1.6)
    spots = [(290, 900, "head", "tail", 1, g), (790, 900, "head", "tail", g, g),
             (290, 1180, "head", "tail", g, g), (790, 1180, "head", "tail", g, 1)]
    for x, y, l, r, gl, gr in spots:
        worm(cr, x, y, 160, 100, l, r, gl, gr, wiggle=0.2 * g, t=t)
    card(cr, t, T(tl, "b6", "सिर"), 120, 1420, ["HEAD, BRAIN, EYES: ALL OF IT"], size=40)
    counter(cr, t, t0 + 1.6, 860, 1460, "4", 110, color=GOLD)
    headline(cr, t, "EVERY PIECE:", "A NEW WORM", t0, t0 + 0.4)


def m_knows(cr, t, tl, t0):                              # b7 "every piece knows where the head goes, and the tail"
    g = prog(t, t0 + 0.5, 1.5)
    worm(cr, W / 2, 1080, 260, 120, "head", "tail", g, g, wiggle=0.15, t=t)
    mono(cr, "<- HEAD", 230, 900, 46, INK, prog(t, T(tl, "b7", "सिर"), 0.3))
    mono(cr, "TAIL ->", 850, 900, 46, INK, prog(t, T(tl, "b7", "पूँछ"), 0.3))
    headline(cr, t, "EACH PIECE KNOWS", "WHICH WAY", t0, T(tl, "b7", "सिर"))


def m_map(cr, t, tl, t0):                                # b7 "...as if there's a map inside the body"
    p = prog(t, t0, 0.4)
    blueprint(cr, W / 2, 1080, 900, 560, p, rot=-0.02)
    worm(cr, W / 2, 1100, 330, 120, "head", "tail", alpha=prog(t, t0 + 0.3, 0.5), ghost=True)
    mono(cr, "HEAD", 230, 960, 44, CREAM, prog(t, t0 + 0.6, 0.3))
    mono(cr, "TAIL", 860, 960, 44, CREAM, prog(t, t0 + 0.8, 0.3))
    headline(cr, t, "LIKE A", "BODY MAP", t0, t0 + 0.3)


def g_space(cr, t, tl, t0):                              # b8 "in space, with almost no gravity, how would the map work?" (slate)
    _pic(cr, "earth_globe", W / 2, 1650, 380, t, t0)
    f = math.sin(t * 1.3)
    blueprint(cr, W / 2, 1000 + 30 * f, 760, 460, prog(t, t0, 0.4), rot=0.08 * f)
    worm(cr, W / 2, 1010 + 30 * f, 280, 100, "head", "tail", rot=0.08 * f + 0.15 * math.sin(t * 0.9),
         alpha=prog(t, t0 + 0.2, 0.4))
    q = prog(t, T(tl, "b8", "नक्शा"), 0.3)
    draw_text(cr, "?", 900, 760, 200, CORAL, q, anchor="cm")
    headline(cr, t, "IN SPACE: ALMOST NO", "GRAVITY", t0, T(tl, "b8", "बराबर") - 0.3, small_color=CREAM,
             big_color=CORAL)


def x_15(cr, t, tl, t0):                                 # b9 "2015: 15 worms, heads and tails cut off..."
    counter(cr, t, t0 + 0.1, W / 2, 720, "2015", 150, color=GOLD)
    tk = T(tl, "b9", "कीड़ों")
    fifteen(cr, t, tk - 0.3, W / 2, 1130)
    headline(cr, t, "2015:", "15 WORMS, CUT", t0, tk)


def x_launch(cr, t, tl, t0):                             # b9 "...sent to the space station for five weeks"
    _pic(cr, "rocket_launch", 330, 1080, 0, t, t0, frame=(470, 700), rot=-0.02)
    calendar(cr, t, T(tl, "b9", "लिए") - 0.6, 790, 1080, ["WEEK 1", "WEEK 2", "WEEK 3", "WEEK 4", "WEEK 5"],
             "IN SPACE", interval=0.3, w=320, h=340)
    headline(cr, t, "5 WEEKS ON THE", "SPACE STATION", t0, T(tl, "b9", "स्टेशन"))


def b_curled(cr, t, tl, t0):                             # b10 "back home, first shock: curled up, not moving"
    _pic(cr, "petri_dish", W / 2, 1100, 600, t, t0)
    for i, (x, y, r) in enumerate(((440, 1020, 60), (640, 1060, 52), (520, 1200, 58), (680, 1220, 48),
                                   (400, 1180, 46))):
        curled(cr, x, y, r, i * 1.3 + 0.03 * math.sin(t * 20 + i), prog(t, t0 + 0.2 + 0.1 * i, 0.3))
    headline(cr, t, "FIRST SHOCK:", "CURLED UP, FROZEN", t0, T(tl, "b10", "हिल"))


def b_2h(cr, t, tl, t0):                                 # b10 "...only normal again after two hours"
    _pic(cr, "clock", 290, 1060, 380, t, t0)
    g = prog(t, t0 + 0.6, 1.4)
    for i, y in enumerate((930, 1090, 1250)):
        if g < 0.5:
            curled(cr, 760, y, 50, i * 1.3)
        else:
            worm(cr, 760, y, 170, 70, "head", "tail", wiggle=0.4, t=t + i)
    counter(cr, t, t0 + 0.3, 290, 1420, "2", 120, color=GOLD)
    draw_text(cr, "HOURS", 290, 1510, 50, INK, prog(t, t0 + 0.5, 0.3), anchor="ct")
    headline(cr, t, "NORMAL AGAIN AFTER", "2 HOURS", t0, t0 + 0.3)


def k_one(cr, t, tl, t0):                                # b11 "and then... one piece out of 15 grew a head"
    te = T(tl, "b11", "एक")
    fifteen(cr, t, t0 - 1, W / 2, 1130, glow=(7, prog(t, te, 0.4)))
    headline(cr, t, "AND THEN...", "1 OF 15", t0, te)


def k_two(cr, t, tl, t0):                                # b11 "...not one head... two. A head where the tail should be"
    td = T(tl, "b11", "दो")
    worm(cr, W / 2, 1120, 300, 130, "head", "head", prog(t, t0, 0.8), prog(t, td - 0.2, 0.9), wiggle=0.2, t=t)
    card(cr, t, T(tl, "b11", "जगह"), 110, 1400, ["A HEAD WHERE THE TAIL SHOULD BE"], size=40)
    headline(cr, t, "NOT ONE HEAD...", "TWO", t0, td)


def s_never(cr, t, tl, t0):                              # b12 "never seen this in 18 years"
    _pic(cr, "planarian_twohead", W / 2, 1060, 0, t, t0, frame=(820, 640))
    footnote(cr, "photo: a two-headed planarian from a different lab experiment (Nogi et al.)",
             prog(t, t0 + 0.3, 0.4))
    headline(cr, t, "18 YEARS:", "NEVER SEEN", t0, T(tl, "b12", "कभी"))


def rh_shock(cr, t, tl, t0):                             # b13 re-hook: "but the real shock came after this" (slate)
    cr.set_source_rgba(*CORAL, 0.18 + 0.08 * math.sin(t * 5))
    cr.arc(W / 2, 1100, 330, 0, 2 * math.pi)
    cr.fill()
    worm(cr, W / 2, 1100, 300, 100, "head", "head", wiggle=0.25, t=t)
    headline(cr, t, "THE REAL SHOCK", "CAME NEXT", t0, t0 + 0.3, small_color=CREAM, big_color=CORAL)


def t_cut3(cr, t, tl, t0):                               # b14 "on Earth, they cut off both heads..."
    _pic(cr, "earth_globe", 880, 700, 200, t, t0)
    tc = T(tl, "b14", "काट")
    p = prog(t, tc, 0.6)
    if p <= 0:
        worm(cr, W / 2, 1150, 600, 110, "head", "head", wiggle=0.15, t=t)
    else:
        for k, (l, r) in enumerate((("head", "cut"), ("cut", "cut"), ("cut", "head"))):
            worm(cr, 340 + 200 * k + (k - 1) * 90 * p, 1150, 200, 110, l, r, rot=0.08 * (k - 1) * p)
    for x in (440, 640):
        cut_line(cr, x, 1150, 220, prog(t, tc - 0.4, 0.3), 1 - prog(t, tc + 0.3, 0.3))
    _pic(cr, "scissors", 470, 880, 210, t, tc - 0.5, rot=0.5)
    headline(cr, t, "BACK ON EARTH:", "CUT IN THREE", t0, tc)


def t_middle(cr, t, tl, t0):                             # b14 "...the middle piece was left..."
    q = 1 - prog(t, t0, 0.5)
    worm(cr, 160 - 120 * (1 - q), 1150, 200, 110, "head", "cut", alpha=q)
    worm(cr, 920 + 120 * (1 - q), 1150, 200, 110, "cut", "head", alpha=q)
    worm(cr, W / 2, 1150, 200 + 80 * (1 - q), 110 + 20 * (1 - q), "cut", "cut")
    ring(cr, W / 2, 1150, 230, 120, prog(t, t0 + 0.4, 0.4))
    headline(cr, t, "ONLY THE", "MIDDLE PIECE", t0, t0 + 0.2)


def t_again(cr, t, tl, t0):                              # b14 "...and it grew two heads AGAIN"
    g = prog(t, t0 + 0.1, 1.4)
    worm(cr, W / 2, 1150, 280, 130, "head", "head", g, g, wiggle=0.2 * g, t=t)
    tu = T(tl, "b14", "उगा")
    stamp(cr, t, "AGAIN!", tu, W / 2, 1450, 90)
    headline(cr, t, "TWO HEADS", "AGAIN", t0, tu)


def u_glitch(cr, t, tl, t0):                             # b15 "so this doesn't look like a one-time glitch"
    for i, (x, lab) in enumerate(((290, "IN SPACE"), (790, "ON EARTH"))):
        q = prog(t, t0 + 0.2 + 0.4 * i, 0.3)
        worm(cr, x, 1080, 180, 90, "head", "head", alpha=q, wiggle=0.2, t=t + i)
        card(cr, t, t0 + 0.3 + 0.4 * i, x - 150, 1260, [lab], size=44)
    headline(cr, t, "NOT A ONE-TIME", "GLITCH", t0, t0 + 0.3, strike_at=t0 + 1.0, struck=True)


def u_map(cr, t, tl, t0):                                # b15 "...as if its map itself had changed"
    blueprint(cr, W / 2, 1080, 900, 560, prog(t, t0, 0.3), rot=-0.02)
    te = t0 + 0.4
    worm(cr, W / 2, 1100, 330, 120, "head", "head" if t >= te + 0.9 else "tail", ghost=True)
    draw_text(cr, "HEAD", 230, 960, 60, CREAM, anchor="cm")      # Anton here: erase() rubs out Anton text
    erase(cr, t, te, "TAIL", 860, 960, 60, CREAM, eraser=P.get("eraser_plain"), anchor="cm")
    draw_text(cr, "HEAD", 860, 960, 60, CORAL, prog(t, te + 0.9, 0.3), anchor="cm")
    headline(cr, t, "AS IF ITS MAP", "CHANGED", t0, T(tl, "b15", "बदल"))


def v_dark(cr, t, tl, t0):                               # b16 "the others changed too: less time in the dark"
    for i, (x, lab, n, pct) in enumerate(((290, "EARTH WORMS", 19, "95"), (790, "SPACE WORMS", 14, "70"))):
        q = prog(t, t0 + 0.2 + 0.4 * i, 0.3)
        mono(cr, lab, x, 850, 36, INK, q)
        dish(cr, x, 1080, 200, n, q, seed=3 + i)
        counter(cr, t, t0 + 0.6 + 0.4 * i, x - 40, 1390, pct, 100, color=GOLD)    # digits only: "%" is wider
        draw_text(cr, "%", x + 40, 1390, 90, INK, prog(t, t0 + 0.8 + 0.4 * i, 0.2), anchor="lm")
    draw_text(cr, "OF THE TIME IN THE DARK", W / 2, 1500, 46, INK, prog(t, t0 + 1.2, 0.3), anchor="ct")
    headline(cr, t, "THE OTHERS CHANGED TOO:", "LESS DARK", t0, T(tl, "b16", "कम"))


def v_20(cr, t, tl, t0):                                 # b16 "...still different 20 months later"
    calendar(cr, t, t0, W / 2, 1100, ["MONTH 1", "MONTH 5", "MONTH 10", "MONTH 15", "MONTH 20"], "AFTER SPACE",
             interval=0.3, w=380, h=400)
    headline(cr, t, "STILL DIFFERENT", "20 MONTHS LATER", t0, t0 + 0.3)


def w_why(cr, t, tl, t0):                                # b17 "why? scientists still aren't sure"
    q = prog(t, t0, 0.3)
    draw_text(cr, "?", W / 2, 960, 420 * (0.8 + 0.2 * q), RED, q, anchor="cm")
    worm(cr, W / 2, 1380, 260, 90, "head", "head", wiggle=0.2, t=t, alpha=prog(t, t0 + 0.3, 0.3))
    headline(cr, t, "WHY?", "NOBODY KNOWS", t0, T(tl, "b17", "पता"))


def w_fluke(cr, t, tl, t0):                              # b17 "...some say a fluke: only 1 of 15"
    _pic(cr, "balance_scale", W / 2, 1150, 520, t, t0)
    card(cr, t, t0 + 0.3, 90, 800, ["SPACE DID IT?"], size=44)
    card(cr, t, T(tl, "b17", "बस"), 580, 800, ["JUST A FLUKE?"], size=44)
    stamp(cr, t, "ONLY 1 OF 15", T(tl, "b17", "पंद्रह"), W / 2, 1500, 64)
    headline(cr, t, "OR JUST A", "FLUKE?", t0, T(tl, "b17", "बस"))


def z_body(cr, t, tl, t0):                               # b18 "socho: if space can really change the body's map..."
    blueprint(cr, W / 2, 1100, 820, 640, prog(t, t0, 0.3), title="HUMAN BODY MAP")
    person(cr, W / 2, 1360, 460, CREAM, prog(t, t0 + 0.3, 0.4))
    headline(cr, t, "IF SPACE CAN CHANGE", "THE BODY MAP...", t0, T(tl, "b18", "बदल"))


def z_mars(cr, t, tl, t0):                               # b18 "...what happens to people living on Mars for years?" (slate)
    _pic(cr, "mars", W / 2 + 140, 1050, 620, t, t0)
    _pic(cr, "astronaut", 320, 1380, 300, t, t0 + 0.3, rot=-0.2 + 0.05 * math.sin(t * 1.5))
    draw_text(cr, "?", 880, 1450, 220, CORAL, prog(t, t0 + 0.6, 0.3), anchor="cm")
    headline(cr, t, "WHAT ABOUT PEOPLE ON", "MARS?", t0, t0 + 0.2, small_color=CREAM, big_color=CORAL)


def e_question(cr, t, tl, t0):                           # b19 "did space change this worm's map? yes or no"
    worm(cr, W / 2, 1450, 260, 90, "head", "head", wiggle=0.25, t=t, alpha=prog(t, t0, 0.3))
    yes_no_card(cr, t, t0 + 0.4, 640, 980, w=640, h=300, question="COMMENT: YES OR NO")
    headline(cr, t, "DID SPACE CHANGE", "ITS BODY MAP?", t0, T(tl, "b19", "बदल"), t_ghost=t0)


SHOTS = [   # (line, cue where the shot starts, draw function, background)
    ("b1", None, h_twohead, "paper"),
    ("b2", None, h_snip, "paper"), ("b2", "हुआ", h_shock, "paper"),
    ("b3", None, r_notscifi, "paper"), ("b3", "अमेरिका", r_tufts, "paper"), ("b3", "इंटरनेशनल", r_iss, "paper"),
    ("b4", None, n_name, "paper"), ("b4", "पानी", n_size, "paper"),
    ("b5", None, l_gecko, "paper"), ("b5", "कीड़ा", l_beyond, "paper"),
    ("b6", None, c_cut, "paper"), ("b6", "हर", c_regrow, "paper"),
    ("b7", None, m_knows, "paper"), ("b7", "जैसे", m_map, "paper"),
    ("b8", None, g_space, "slate"),
    ("b9", None, x_15, "paper"), ("b9", "उन्हें", x_launch, "paper"),
    ("b10", None, b_curled, "paper"), ("b10", "घंटे", b_2h, "paper"),
    ("b11", None, k_one, "paper"), ("b11", "पर", k_two, "paper"),
    ("b12", None, s_never, "paper"),
    ("b13", None, rh_shock, "slate"),
    ("b14", None, t_cut3, "paper"), ("b14", "बीच", t_middle, "paper"), ("b14", "फिर", t_again, "paper"),
    ("b15", None, u_glitch, "paper"), ("b15", "जैसे", u_map, "paper"),
    ("b16", None, v_dark, "paper"), ("b16", "बीस", v_20, "paper"),
    ("b17", None, w_why, "paper"), ("b17", "कुछ", w_fluke, "paper"),
    ("b18", None, z_body, "paper"), ("b18", "मंगल", z_mars, "slate"),
    ("b19", None, e_question, "paper"),
]


def draw(cr, t, tl):
    draw_frame(cr, t, tl, SHOTS)


def sfx(tl):
    """A whoosh on every cut, thuds on the cuts and stamps, a tick (and a music dip) before the re-hook, the doubt and
    the closing line, typing on the card."""
    ev = [(s, "whoosh", 0.25) for s in starts(tl, SHOTS)[1:]]
    ev += [(T(tl, "b2", "काट"), "thud", 0.0), (T(tl, "b11", "दो"), "thud", 0.0), (T(tl, "b14", "उगा"), "thud", 0.0),
           (T(tl, "b13", None) - 0.35, "tick", 0.0), (T(tl, "b17", None) - 0.35, "tick", 0.0),
           (T(tl, "b19", None) - 0.35, "tick", 0.0), (T(tl, "b19", "यस"), "typing", 1.0)]
    for bid in ("b4", "b9", "b12", "b16"):
        ev.append((tl[bid].start + 0.4, "pop", 0.0))
    ev += [(at, "dip", 0.5) for at, name, _ in list(ev) if name == "tick"]   # the bed dips just before a reveal
    return ev
