"""Video 8 (science + tech): "Tumhara sir pairon se tez budha ho raha hai" - gravity bends time, and your phone's GPS
would drift kilometres a day without Einstein. Owner, 1 Nov 2026, after the internet video: "Everyone knows this i
want something unique and seems like unbelievable auto approved". Narration in Devanagari for the voice, numbers
written as words.
Facts: NIST 2010 (Chou et al., Science 329:1630): two aluminium-ion clocks, one raised 33 cm (about a foot), the upper
one ran faster as general relativity predicts; head vs feet (~1.7 m) over 80 years is ~0.5 microseconds (g h / c^2).
GPS (Ashby, Physics Today, May 2002): ~20,000 km up, ~4 km/s (~14,000 km/h); gravity makes the orbiting clocks gain
~45 us a day, speed loses ~7 us, net ~38 us; uncorrected, "navigational errors of more than 11 km" in one day; the
clocks get a factory offset before launch (4.4645 parts in 10^10, so 10.23 MHz is set to 10.22999999543 MHz); in
1977 the first GPS satellite's clock ran three weeks uncorrected because the size and even the sign of the shift
were uncertain: it came out 4.425 parts in 10^10, within 1% of relativity. 31 GPS satellites operational (2025);
a phone needs 4 to fix time and position; GPS is receive-only. NavIC: IRNSS-1A's three rubidium clocks failed in
2016, so it no longer serves navigation (only messaging); IRNSS-1I replaced it in 2018."""
import math
import os

import cairo

from poster import (CORAL, CREAM, GOLD, GREEN, INK, MONO_FONT, RED, W, calendar, card, counter, cross, draw_text,
                    header, headline, magnifier, path, person, prog, ring, stamp, strike, tick, yes_no_card)

# the narrator, music and tail are channel-wide; render_hi reads them from this module
from channel import ASSETS_ROOT, MUSIC, NARRATOR, NARRATOR_LABEL, REVEAL_GAP, TAIL, VOICE_REF  # noqa: F401
from shots import T, asset_finder, draw_frame, pic, starts

SCRIPT = [
    dict(id="b1", text="सोचो, तुम्हारा सिर... तुम्हारे पैरों से ज़्यादा तेज़ी से बूढ़ा हो रहा है।"),
    dict(id="b2", text="ये कोई फ़िलॉसफ़ी नहीं है, ये फ़िज़िक्स है। और तुम्हारा फ़ोन, हर रोज़ इसे सच साबित करता है।"),
    dict(id="b3", text="आइंस्टीन ने कहा था: ज़मीन से जितना ऊपर जाओ, टाइम उतनी तेज़ी से चलता है।"),
    dict(id="b4", text="दो हज़ार दस में, अमेरिका की एक लैब ने दुनिया की दो सबसे सटीक घड़ियाँ लीं... "
                       "और एक को बस एक फ़ुट ऊपर रख दिया।"),
    dict(id="b5", text="और ऊपर वाली घड़ी... सच में ज़्यादा तेज़ी से चली।", gap=REVEAL_GAP),
    dict(id="b6", text="फ़र्क बहुत छोटा है। पूरी ज़िंदगी में, एक सेकंड के दस लाखवें हिस्से से भी कम। "
                       "पर तुम्हारे फ़ोन के लिए... यही फ़र्क सब कुछ है।"),
    dict(id="b7", text="आसमान में, बीस हज़ार किलोमीटर ऊपर, तीस से ज़्यादा जीपीएस सैटेलाइट घूम रहे हैं। "
                       "और हर एक के अंदर, एटॉमिक घड़ियाँ लगी हैं।"),
    dict(id="b8", text="और मज़े की बात... सैटेलाइट को पता ही नहीं कि तुम कहाँ हो। वो बस लगातार अपना टाइम भेजता रहता है।"),
    dict(id="b9", text="तुम्हारा फ़ोन चार सैटेलाइट्स का टाइम सुनता है, और नापता है कि सिग्नल आने में कितनी देर लगी। "
                       "उसी से तुम्हारी जगह निकलती है।"),
    dict(id="b10", text="सिग्नल रोशनी की स्पीड से आता है। तो टाइम में एक माइक्रोसेकंड की गलती... मतलब तीन सौ मीटर की गलती।"),
    dict(id="b11", text="अब ट्विस्ट सुनो। इतनी ऊँचाई पर, सैटेलाइट की घड़ी हर दिन, ज़मीन की घड़ी से अड़तीस माइक्रोसेकंड "
                        "आगे निकल जाती है।", gap=REVEAL_GAP),
    dict(id="b13", text="और टाइम में अड़तीस माइक्रोसेकंड की गलती... मतलब ग्यारह किलोमीटर से ज़्यादा की गलती। हर एक दिन।"),
    dict(id="b14", text="अगर इसे ठीक न किया जाए, तो कुछ ही दिनों में तुम्हारा मैप, तुम्हें किसी और शहर में दिखाता।"),
    dict(id="b15", text="पर उन्नीस सौ सतहत्तर में, जब पहला जीपीएस सैटेलाइट ऊपर गया... किसी को पक्का नहीं पता था कि "
                        "उसकी घड़ी तेज़ चलेगी, या धीमी। तो उन्होंने क्या किया?"),
    dict(id="b16", text="घड़ी को तीन हफ़्ते, बिना करेक्शन के चलने दिया। और घड़ी ठीक उतनी तेज़ निकली... "
                        "जितना आइंस्टीन का हिसाब कहता था। एक परसेंट से भी कम का फ़र्क।", gap=REVEAL_GAP),
    dict(id="b17", text="तब से हर जीपीएस घड़ी को, लॉन्च से पहले ही जानबूझकर थोड़ा धीमा सेट किया जाता है... "
                        "ताकि ऊपर पहुँचकर वो बिल्कुल सही चले।"),
    dict(id="b18", text="भारत का अपना जीपीएस, नाविक, भी इन्हीं एटॉमिक घड़ियों पर चलता है। "
                        "और जब इसरो के एक सैटेलाइट की तीनों घड़ियाँ बंद हुईं... वो रास्ता बताने के लायक नहीं रहा।"),
    dict(id="b19", text="तो अगली बार जब डिलीवरी वाला ठीक तुम्हारे दरवाज़े तक पहुँचे... याद रखना, "
                        "उसके पीछे आइंस्टीन का हिसाब चल रहा है।"),
    dict(id="b20", text="तुम्हें पता था कि तुम्हारा सिर, पैरों से तेज़ बूढ़ा होता है? यस या नो, कमेंट में बताओ।"),
]

METADATA = dict(
    title="Tumhara sir pairon se tez budha hota hai",
    caption="Tumhara sir tumhare pairon se zyada tez budha ho raha hai... aur ye sach hai 😳\n\n"
            "Einstein ne kaha tha: zameen se jitna upar, time utna tez. 2010 mein ek lab ne do atomic ghadiyan ek foot "
            "ke farak par rakhi, aur upar wali sach mein tez chali.\n\n"
            "Tumhara GPS isi par chalta hai: satellite ki ghadi roz 38 microsecond aage nikalti hai. Theek na karo, "
            "toh ek hi din mein 11 km se zyada ki galti.\n\n"
            "Tumhe pata tha ki tumhara sir pairon se tez budha hota hai? Comment mein YES ya NO likho 👇",
    yt_title="Tumhara Sir Pairon Se Tez Budha Hota Hai? 😳 | GPS & Einstein",
    yt_description="Zameen se jitna upar jao, time utna tez chalta hai: 2010 mein do atomic ghadiyon ne ise ek foot ke "
                   "farak par naap liya. Tumhare phone ka GPS isi par chalta hai, satellite ki ghadi roz 38 microsecond "
                   "aage nikalti hai, aur ise launch se pehle hi theek kiya jaata hai. Saath mein 1977 ka pehla GPS "
                   "satellite aur Bharat ka NavIC.",
    hashtags=["#einstein", "#gps", "#sciencefacts", "#factsinhindi", "#techinhindi"],
    pinned_comment="Tumhe pata tha ki tumhara sir pairon se tez budha hota hai? ⏱️ YES ya NO? 👇",
    sources=["Chou et al. 2010, Science (NIST aluminium-ion clocks)",
             "Ashby 2002, Physics Today, Relativity and the Global Positioning System",
             "gps.gov, GPS space segment",
             "ISRO, IRNSS-1A clock failures (2016-17 reports)"],
)

_find = asset_finder("time", "toxoplasma2", "krait2")
P = {k: _find(k) for k in ("person", "einstein", "lab_clock", "gps_sat", "nts2", "irnss", "scooter", "earth_globe",
                           "india_map")}
USED_ASSETS = [os.path.basename(v) for v in P.values() if v]
CREDITS_FILES = [os.path.join(ASSETS_ROOT, d, "credits.json") for d in ("time", "toxoplasma2", "krait2")]

FACE, BLUE, ROAD = (0.97, 0.95, 0.90), (0.16, 0.45, 0.95), (0.99, 0.98, 0.95)


def _pic(cr, key, cx, cy, h, t, t0, **kw):
    pic(cr, P.get(key), cx, cy, h, t, t0, **kw)


# ---------- drawing pieces for this video ----------

def glow(cr, x, y, r, color=(0.55, 0.95, 1.0), alpha=1.0):
    for k, a in ((2.6, 0.12), (1.6, 0.3), (1.0, 1.0)):
        cr.arc(x, y, r * k, 0, 2 * math.pi)
        cr.set_source_rgba(*color, a * alpha)
        cr.fill()


def clock(cr, x, y, r, t, rate=1.0, alpha=1.0, label=None, label_color=INK, stopped=None):
    """An analogue clock. The red second hand sweeps a turn every 4 s / rate, so a faster clock visibly runs ahead
    (sped up for the eye); after `stopped` the hand freezes."""
    if alpha <= 0:
        return
    cr.arc(x + 6, y + 10, r, 0, 2 * math.pi)
    cr.set_source_rgba(0, 0, 0, 0.22 * alpha)
    cr.fill()
    cr.arc(x, y, r, 0, 2 * math.pi)
    cr.set_source_rgba(*FACE, alpha)
    cr.fill_preserve()
    cr.set_source_rgba(*INK, alpha)
    cr.set_line_width(r * 0.09)
    cr.stroke()
    for k in range(12):
        a = 2 * math.pi * k / 12
        l0 = 0.78 if k % 3 else 0.68
        cr.move_to(x + r * l0 * math.sin(a), y - r * l0 * math.cos(a))
        cr.line_to(x + r * 0.86 * math.sin(a), y - r * 0.86 * math.cos(a))
        cr.set_line_width(r * (0.05 if k % 3 else 0.08))
        cr.stroke()
    for a, l, wd in ((-1.05, 0.45, 0.08), (0.95, 0.66, 0.06)):          # hour and minute hands, still
        cr.move_to(x, y)
        cr.line_to(x + r * l * math.sin(a), y - r * l * math.cos(a))
        cr.set_line_width(r * wd)
        cr.stroke()
    ts = t if stopped is None else min(t, stopped)
    a = 2 * math.pi * ts * rate / 4
    cr.move_to(x - r * 0.15 * math.sin(a), y + r * 0.15 * math.cos(a))
    cr.line_to(x + r * 0.8 * math.sin(a), y - r * 0.8 * math.cos(a))
    cr.set_source_rgba(*RED, alpha)
    cr.set_line_width(max(3, r * 0.035))
    cr.stroke()
    cr.arc(x, y, r * 0.07, 0, 2 * math.pi)
    cr.fill()
    if label:
        draw_text(cr, label, x, y + r + 18, max(26, int(r * 0.3)), label_color, alpha, MONO_FONT, "ct", tracking=2)


def map_pin(cr, x, y, s, color=RED, alpha=1.0):
    """A map pin whose tip is at (x, y)."""
    cr.move_to(x, y)
    cr.curve_to(x - s * 0.9, y - s * 1.1, x - s * 0.75, y - s * 2.0, x, y - s * 2.0)
    cr.curve_to(x + s * 0.75, y - s * 2.0, x + s * 0.9, y - s * 1.1, x, y)
    cr.set_source_rgba(*color, alpha)
    cr.fill()
    cr.arc(x, y - s * 1.35, s * 0.32, 0, 2 * math.pi)
    cr.set_source_rgba(1, 1, 1, alpha)
    cr.fill()


def you_dot(cr, x, y, t, r=16, alpha=1.0):
    f = (t * 0.9) % 1
    cr.arc(x, y, r * (1 + 2.2 * f), 0, 2 * math.pi)
    cr.set_source_rgba(*BLUE, 0.35 * (1 - f) * alpha)
    cr.fill()
    cr.arc(x, y, r + 5, 0, 2 * math.pi)
    cr.set_source_rgba(1, 1, 1, alpha)
    cr.fill()
    cr.arc(x, y, r, 0, 2 * math.pi)
    cr.set_source_rgba(*BLUE, alpha)
    cr.fill()


def streets(cr, x, y, w, h, alpha=1.0, seed=2):
    """A plain drawn street map in the box: blocks, a river, a park, a few roads."""
    cr.save()
    cr.rectangle(x, y, w, h)
    cr.clip()
    cr.set_source_rgba(0.92, 0.90, 0.83, alpha)
    cr.paint_with_alpha(alpha)
    cr.rectangle(x + w * 0.62, y + h * 0.08, w * 0.25, h * 0.18)
    cr.set_source_rgba(0.68, 0.84, 0.60, alpha)
    cr.fill()
    cr.move_to(x - 10, y + h * 0.78)
    cr.curve_to(x + w * 0.3, y + h * 0.70, x + w * 0.6, y + h * 0.95, x + w + 10, y + h * 0.82)
    cr.set_source_rgba(0.62, 0.80, 0.95, alpha)
    cr.set_line_width(max(10, w * 0.05))
    cr.stroke()
    lw = max(5, w * 0.022)
    for k in range(1, 6):
        xx = x + w * (k / 6 + 0.03 * math.sin(k * seed))
        cr.move_to(xx, y)
        cr.line_to(xx + w * 0.04, y + h)
        yy = y + h * (k / 6 + 0.02 * math.cos(k * seed))
        cr.move_to(x, yy)
        cr.line_to(x + w, yy - h * 0.03)
    cr.set_source_rgba(*ROAD, alpha)
    cr.set_line_width(lw)
    cr.stroke()
    cr.move_to(x, y + h * 0.95)
    cr.line_to(x + w, y + h * 0.15)
    cr.set_source_rgba(0.98, 0.85, 0.45, alpha)
    cr.set_line_width(lw * 1.8)
    cr.stroke()
    cr.restore()


def rrect(cr, x, y, w, h, r):
    cr.new_sub_path()
    cr.arc(x + w - r, y + r, r, -math.pi / 2, 0)
    cr.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    cr.arc(x + r, y + h - r, r, math.pi / 2, math.pi)
    cr.arc(x + r, y + r, r, math.pi, 3 * math.pi / 2)
    cr.close_path()


def phone_map(cr, cx, cy, h, t, alpha=1.0, pin=None):
    """A plain phone (no brand) showing a street map with the blue 'you are here' dot in the middle.
    pin = (dx, dy, p): a red map pin at that offset from the dot, popping in with p. Returns the dot's position."""
    if alpha <= 0:
        return cx, cy
    w = h * 0.49
    x, y = cx - w / 2, cy - h / 2
    rrect(cr, x + 10, y + 16, w, h, w * 0.12)
    cr.set_source_rgba(0, 0, 0, 0.22 * alpha)
    cr.fill()
    rrect(cr, x, y, w, h, w * 0.12)
    cr.set_source_rgba(0.13, 0.13, 0.14, alpha)
    cr.fill()
    sx, sy, sw, sh = x + w * 0.05, y + h * 0.06, w * 0.9, h * 0.89
    cr.save()
    rrect(cr, sx, sy, sw, sh, w * 0.08)
    cr.clip()
    streets(cr, sx, sy, sw, sh, alpha)
    dot = (cx, sy + sh * 0.55)
    you_dot(cr, *dot, t, r=max(8, h * 0.02), alpha=alpha)
    if pin:
        dx, dy, p = pin
        if p > 0:
            map_pin(cr, dot[0] + dx, dot[1] + dy, h * 0.035, RED, alpha * p)
    cr.restore()
    return dot


def waves(cr, x, y, t, color=CORAL, alpha=1.0, a0=math.pi / 2, spread=0.55, r0=40, r1=420, n=3, speed=0.7):
    """Signal arcs spreading out from (x, y) around direction a0."""
    for k in range(n):
        f = (t * speed + k / n) % 1
        cr.new_sub_path()
        cr.arc(x, y, r0 + (r1 - r0) * f, a0 - spread, a0 + spread)
        cr.set_source_rgba(*color, alpha * (1 - f))
        cr.set_line_width(7)
        cr.stroke()


def earth(cr, t, t0, cy=2010, h=1300, alpha=1.0):
    _pic(cr, "earth_globe", W / 2, cy, h, t, t0, alpha=alpha)


def bracket(cr, x, y0, y1, p, label, sub=None, color=INK, alpha=1.0):
    """A vertical dimension line with end ticks, drawn as p goes 0 -> 1, and its label to the right."""
    if p <= 0:
        return
    ym = y0 + (y1 - y0) * p
    path(cr, [(x, y0), (x, ym)], 1.0, 5, color, alpha)
    for yy in (y0, ym):
        path(cr, [(x - 22, yy), (x + 22, yy)], 1.0, 5, color, alpha)
    draw_text(cr, label, x + 34, (y0 + y1) / 2, 54, color, alpha * p, anchor="lm")
    if sub:
        draw_text(cr, sub, x + 34, (y0 + y1) / 2 + 52, 30, color, 0.8 * alpha * p, MONO_FONT, "lm")


def stand(cr, x, y_top, y_floor, w=150, alpha=1.0):
    """A plain block that a clock sits on, from y_top down to the floor."""
    if y_floor - y_top < 2:
        return
    cr.rectangle(x - w / 2, y_top, w, y_floor - y_top)
    cr.set_source_rgba(0.55, 0.45, 0.35, alpha)
    cr.fill()


def two_clocks(cr, t, t0, raise_p, rate_hi=1.0, alpha=1.0):
    """The NIST test: two clocks on a bench; the right one lifted 'a foot' as raise_p goes 0 -> 1."""
    floor = 1560
    path(cr, [(70, floor), (1010, floor)], 1.0, 8, CREAM, alpha)
    clock(cr, 240, floor - 230, 150, t, 1.0, alpha * prog(t, t0, 0.3), "CLOCK A", CREAM)
    yr = floor - 230 - 300 * raise_p
    stand(cr, 640, yr + 150, floor, alpha=alpha * prog(t, t0 + 0.2, 0.3))
    clock(cr, 640, yr, 150, t, rate_hi, alpha * prog(t, t0 + 0.2, 0.3), "CLOCK B", CREAM)
    return yr


def knob(cr, x, y, r, angle, alpha=1.0):
    cr.arc(x, y, r, 0, 2 * math.pi)
    cr.set_source_rgba(0.30, 0.30, 0.32, alpha)
    cr.fill()
    cr.arc(x, y, r * 0.8, 0, 2 * math.pi)
    cr.set_source_rgba(0.55, 0.55, 0.58, alpha)
    cr.fill()
    cr.move_to(x, y)
    cr.line_to(x + r * 0.75 * math.sin(angle), y - r * 0.75 * math.cos(angle))
    cr.set_source_rgba(*CORAL, alpha)
    cr.set_line_width(12)
    cr.stroke()


def door(cr, x, y, h, alpha=1.0):
    """A front door standing on (x, y)."""
    w = h * 0.5
    cr.rectangle(x - w / 2 - 14, y - h - 14, w + 28, h + 14)
    cr.set_source_rgba(0.93, 0.89, 0.80, alpha)
    cr.fill()
    cr.rectangle(x - w / 2, y - h, w, h)
    cr.set_source_rgba(0.52, 0.30, 0.16, alpha)
    cr.fill()
    for k in range(2):
        cr.rectangle(x - w / 2 + 18, y - h + 20 + k * h * 0.48, w - 36, h * 0.4)
        cr.set_source_rgba(0.42, 0.24, 0.12, alpha)
        cr.fill()
    cr.arc(x + w / 2 - 22, y - h * 0.48, 8, 0, 2 * math.pi)
    cr.set_source_rgba(*GOLD, alpha)
    cr.fill()


# ---------- shots ----------
# Rules (style bible): a new picture every ~3 s cut on the word, the literal noun on screen, red = the key word,
# gold = numbers. The recurring picture is a ticking clock: the faster clock is the one higher up.

PERSON = (330, 1200, 1150)       # the man: centre x, centre y, height (photo is 0.336 x its height wide)


def head_and_feet(cr, t, t0, t_feet, x=PERSON[0], y=PERSON[1], h=PERSON[2], cx=830, r=100, alpha=1.0):
    """The man with a clock at his head (fast) and one at his feet, joined by leader lines."""
    _pic(cr, "person", x, y, h, t, t0, alpha=alpha)
    hy, fy = y - h * 0.43, y + h * 0.47
    for cy, rate, t_in, lab in ((hy, 1.6, t0, "HEAD"), (fy, 1.0, t_feet, "FEET")):
        p = prog(t, t_in, 0.3) * alpha
        path(cr, [(x + h * 0.06, cy), (cx - r - 10, cy)], p, 4, INK, 0.6 * alpha)
        clock(cr, cx, cy, r, t, rate, p)
        draw_text(cr, lab, cx + r + 20, cy, 40, INK, p, MONO_FONT, "lm")


def h_head(cr, t, tl, t0):                               # b1 frame 0: "your head is ageing faster than your feet"
    head_and_feet(cr, t, -1, T(tl, "b1", "पैरों") - 0.2, cx=800)
    stamp(cr, t, "THAN YOUR FEET", T(tl, "b1", "पैरों"), 780, 1180, 50)
    headline(cr, t, "YOUR HEAD IS AGING", "FASTER", -1, min(1.8, T(tl, "b1", "तेज़ी")), t_ghost=-1)


def p_physics(cr, t, tl, t0):                            # b2 "not philosophy, physics" (slate)
    tn, tp = T(tl, "b2", "नहीं"), T(tl, "b2", "फ़िज़िक्स")
    clock(cr, W / 2, 1100, 300, t, 1.0, prog(t, t0, 0.3))
    stamp(cr, t, "PHYSICS", tp, W / 2, 1560, 90, color=CORAL)
    headline(cr, t, "NOT", "PHILOSOPHY", t0, t0 + 0.2, small_color=CREAM, big_color=CREAM, strike_at=tn, struck=True)


def p_phone(cr, t, tl, t0):                              # b2 "...and your phone proves it every day"
    phone_map(cr, W / 2, 1150, 1000, t, prog(t, t0, 0.3))
    stamp(cr, t, "EVERY DAY", T(tl, "b2", "रोज़"), 820, 1560, 56)
    headline(cr, t, "YOUR PHONE", "PROVES IT", t0, T(tl, "b2", "साबित"))


def e_rule(cr, t, tl, t0):                               # b3 "Einstein: the higher you go, the faster time runs"
    header(cr, "gravitational time dilation", 1, prog(t, t0, 0.3), y=1840)
    _pic(cr, "einstein", 290, 1390, 760, t, t0)
    tg, tu = T(tl, "b3", "ज़मीन"), T(tl, "b3", "ऊपर")
    path(cr, [(600, 1680), (1040, 1680)], prog(t, tg - 0.2, 0.3), 8, INK)
    clock(cr, 900, 1570, 70, t, 1.0, prog(t, tg, 0.3), "GROUND")
    q = prog(t, tu - 0.3, 0.3)
    cr.move_to(640, 1380)
    cr.line_to(760, 1110)
    cr.line_to(880, 1380)
    cr.close_path()
    cr.set_source_rgba(0.55, 0.50, 0.44, q)
    cr.fill()
    clock(cr, 930, 1230, 70, t, 1.3, q, "MOUNTAIN")
    q2 = prog(t, tu + 0.2, 0.3)
    _pic(cr, "gps_sat", 720, 760, 170, t, tu + 0.2)
    clock(cr, 930, 830, 70, t, 1.7, q2, "SPACE")
    path(cr, [(600, 1600), (600, 760)], prog(t, tu, 0.6), 8, RED, arrow=True)
    headline(cr, t, "HIGHER UP, TIME RUNS", "FASTER", t0, T(tl, "b3", "तेज़ी"))


def n_lab(cr, t, tl, t0):                                # b4 "2010: a US lab took two of the world's most precise clocks"
    _pic(cr, "lab_clock", W / 2, 980, 0, t, t0, frame=(900, 640))
    counter(cr, t, t0 + 0.1, 760, 1520, "2010", 110)
    card(cr, t, t0 + 0.5, 90, 1400, ["A LAB IN THE USA", "NIST"], size=44)
    headline(cr, t, "2010: THE WORLD'S MOST", "PRECISE CLOCKS", t0, T(tl, "b4", "सटीक"))


def n_foot(cr, t, tl, t0):                               # b4 "...and put one just a foot higher" (slate)
    tu = T(tl, "b4", "ऊपर")
    rp = prog(t, tu - 0.3, 0.7)
    yr = two_clocks(cr, t, t0, rp)
    bracket(cr, 850, 1330, yr, rp, "33 CM", "1 FOOT", CREAM)
    headline(cr, t, "ONE CLOCK RAISED BY", "1 FOOT", t0, T(tl, "b4", "फ़ुट"), small_color=CREAM, big_color=CORAL)


def n_fast(cr, t, tl, t0):                               # b5 "...and the higher clock really ran faster" (slate)
    tf = T(tl, "b5", "तेज़")
    yr = two_clocks(cr, t, -9, 1.0, rate_hi=1.0 + 0.7 * prog(t, tf - 0.4, 0.4))
    tick(cr, 800, yr - 150, 110, prog(t, tf, 0.3), color=GREEN)
    stamp(cr, t, "FASTER", tf + 0.2, 640, yr + 290, 52, color=CORAL)
    headline(cr, t, "THE HIGHER CLOCK RAN", "FASTER", t0, tf, small_color=CREAM, big_color=CORAL)


def t_tiny(cr, t, tl, t0):                               # b6 "the difference is tiny: < a millionth of a second in a life"
    head_and_feet(cr, t, t0, t0, x=230, y=1270, h=980, cx=480, r=70)
    tz, td = T(tl, "b6", "ज़िंदगी"), T(tl, "b6", "दस")
    q = prog(t, tz - 0.2, 0.3)
    draw_text(cr, "A WHOLE LIFE", 640, 640, 40, INK, q, MONO_FONT, "lb", tracking=2)
    cr.rectangle(640, 670, 380, 46)
    cr.set_source_rgba(*INK, 0.25 * q)
    cr.fill()
    cr.rectangle(640, 670, 380 * prog(t, tz, 1.0), 46)
    cr.set_source_rgba(*GOLD, q)
    cr.fill()
    draw_text(cr, "0", 640, 730, 34, INK, q, MONO_FONT, "lt")
    draw_text(cr, "80 YEARS", 1020, 730, 34, INK, q, MONO_FONT, "rt")
    p = prog(t, td - 0.2, 0.3)
    draw_text(cr, "< 0.000001 s", 830, 1180, 76, RED, p, MONO_FONT, "cm")
    card(cr, t, td + 0.3, 600, 1300, ["LESS THAN", "A MILLIONTH OF A SECOND"], size=44)
    headline(cr, t, "HEAD VS FEET, IN A LIFETIME:", "TINY", t0, T(tl, "b6", "छोटा"))


def t_phone(cr, t, tl, t0):                              # b6 "...but for your phone, this difference is everything" (slate)
    phone_map(cr, W / 2, 1120, 980, t, prog(t, t0, 0.3))
    stamp(cr, t, "EVERYTHING", T(tl, "b6", "सब"), W / 2, 1720, 70, color=CORAL)
    headline(cr, t, "BUT FOR YOUR PHONE, IT'S", "EVERYTHING", t0, T(tl, "b6", "सब"), small_color=CREAM,
             big_color=CORAL)


def sat_ring(cr, t, t0, n=5, alpha=1.0):
    """Satellites drifting along an orbit arc above the Earth."""
    cx, cy, R = W / 2, 2010, 1330
    cr.new_sub_path()
    cr.arc(cx, cy, R, math.pi * 1.05, math.pi * 1.95)
    cr.set_dash([18, 16])
    cr.set_source_rgba(*CREAM, 0.6 * alpha)
    cr.set_line_width(4)
    cr.stroke()
    cr.set_dash([])
    for k in range(n):
        a = math.pi * (1.37 + 0.065 * k) + 0.012 * t
        _pic(cr, "gps_sat", cx + R * math.cos(a), cy + R * math.sin(a), 150, t, t0 + 0.12 * k, alpha=alpha)


def g_orbit(cr, t, tl, t0):                              # b7 "20,000 km up, over 30 GPS satellites circle" (slate)
    earth(cr, t, t0)
    sat_ring(cr, t, t0 + 0.2)
    counter(cr, t, T(tl, "b7", "बीस") - 0.1, W / 2, 1050, "20,000", 100)
    draw_text(cr, "KM UP", W / 2, 1150, 50, CREAM, prog(t, T(tl, "b7", "किलोमीटर"), 0.3), anchor="ct")
    headline(cr, t, "20,000 KM UP: OVER 30", "GPS SATELLITES", t0, T(tl, "b7", "जीपीएस"), small_color=CREAM,
             big_color=CORAL)


def g_inside(cr, t, tl, t0):                             # b7 "...and inside each one, atomic clocks"
    _pic(cr, "gps_sat", 470, 900, 560, t, t0)

    def inner(c):
        clock(c, 760, 1360, 150, t, 1.0)
        draw_text(c, "ATOMIC", 760, 1555, 34, INK, 1.0, MONO_FONT, "ct", tracking=3)
    magnifier(cr, t, T(tl, "b7", "एटॉमिक") - 0.3, 760, 1380, 250, inner)
    headline(cr, t, "INSIDE EACH ONE:", "ATOMIC CLOCKS", t0, T(tl, "b7", "एटॉमिक"))


def g_blind(cr, t, tl, t0):                              # b8 "the satellite doesn't even know where you are" (slate)
    _pic(cr, "gps_sat", W / 2, 720, 330, t, t0)
    tn = T(tl, "b8", "नहीं")
    closed = prog(t, tn, 0.3)
    from_eye = 1 - 0.95 * closed
    eye_x, eye_y = W / 2, 1180
    _eye(cr, eye_x, eye_y, 330, from_eye, prog(t, t0 + 0.2, 0.3))
    cross(cr, eye_x, eye_y, 200, prog(t, tn + 0.1, 0.3))
    person(cr, W / 2, 1760, 300, CREAM, prog(t, t0 + 0.4, 0.3))
    draw_text(cr, "?", W / 2 + 120, 1500, 120, CORAL, prog(t, T(tl, "b8", "कहाँ"), 0.3), anchor="cm")
    headline(cr, t, "IT DOESN'T KNOW", "WHERE YOU ARE", t0, T(tl, "b8", "कहाँ"), small_color=CREAM, big_color=CORAL)


def _eye(cr, x, y, w, open_=1.0, alpha=1.0):
    if alpha <= 0:
        return
    cr.save()
    cr.translate(x, y)
    cr.scale(1, max(0.04, open_))
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


def g_send(cr, t, tl, t0):                               # b8 "...it just keeps sending its time" (slate)
    _pic(cr, "gps_sat", W / 2, 700, 330, t, -9)
    waves(cr, W / 2, 860, t, CORAL, prog(t, t0, 0.3), r1=760)
    for k in range(3):
        f = (t * 0.35 + k / 3) % 1
        s = int(t * 7 + k) % 60
        draw_text(cr, f"12:00:{s:02d}.{int(t * 1e6) % 1000000:06d}", W / 2, 1000 + 520 * f, 40, CREAM,
                  prog(t, t0 + 0.3, 0.3) * (1 - f), MONO_FONT, "cm")
    stamp(cr, t, "ONE-WAY: ONLY SENDS", T(tl, "b8", "भेजता"), W / 2, 1650, 52, color=CORAL)
    headline(cr, t, "IT ONLY SENDS", "THE TIME", t0, T(tl, "b8", "टाइम"), small_color=CREAM, big_color=CORAL)


SATS4 = ((170, 690), (420, 600), (660, 600), (910, 690))


def g_four(cr, t, tl, t0):                               # b9 "your phone hears 4 satellites' time and times the signal" (slate)
    tc, td, tj = T(tl, "b9", "चार"), T(tl, "b9", "देर"), T(tl, "b9", "जगह")
    top = (W / 2, 1160)
    for i, ((x, y), ms) in enumerate(zip(SATS4, ("0.067 S", "0.071 S", "0.074 S", "0.082 S"))):
        _pic(cr, "gps_sat", x, y, 120, t, tc - 0.3 + 0.12 * i)
        p = prog(t, tc + 0.12 * i, 0.5)
        path(cr, [(x, y + 60), top], p, 4, CORAL, 0.9, dash=[14, 10])
        mx, my = (x + top[0]) / 2, (y + 60 + top[1]) / 2
        draw_text(cr, ms, mx + (40 if x > W / 2 else -40), my, 32, CREAM, prog(t, td + 0.1 * i, 0.3), MONO_FONT,
                  "lm" if x > W / 2 else "rm")
    phone_map(cr, W / 2, 1440, 560, t, pin=(0, 0, prog(t, tj, 0.3)))
    if t > tj:
        ring(cr, W / 2, 1480, 90, 60, prog(t, tj + 0.2, 0.4), color=CORAL)
    headline(cr, t, "YOUR PHONE LISTENS TO", "4 SATELLITES", t0, tc, small_color=CREAM, big_color=CORAL)


def l_light(cr, t, tl, t0):                              # b10 "the signal comes at the speed of light" (slate)
    _pic(cr, "gps_sat", 820, 650, 260, t, t0)
    dot = phone_map(cr, 300, 1430, 560, t, prog(t, t0 + 0.2, 0.3))
    pts = [(780, 760), (dot[0] + 40, dot[1] - 260)]
    path(cr, pts, prog(t, t0 + 0.2, 0.3), 6, CORAL, 0.8)
    for k in range(4):
        f = (t * 2.2 + k / 4) % 1
        glow(cr, pts[0][0] + (pts[1][0] - pts[0][0]) * f, pts[0][1] + (pts[1][1] - pts[0][1]) * f, 10,
             alpha=prog(t, t0 + 0.4, 0.3))
    card(cr, t, T(tl, "b10", "स्पीड"), 560, 1180, ["3 LAKH KM", "EVERY SECOND"], size=50)
    headline(cr, t, "THE SIGNAL COMES AT", "LIGHT SPEED", t0, T(tl, "b10", "रोशनी"), small_color=CREAM,
             big_color=CORAL)


def l_300(cr, t, tl, t0):                                # b10 "...so 1 microsecond wrong = 300 metres wrong"
    draw_text(cr, "1 µs", W / 2, 700, 150, INK, prog(t, t0, 0.3), anchor="cm")
    draw_text(cr, "= 0.000001 SECOND", W / 2, 820, 40, INK, prog(t, t0 + 0.3, 0.3), MONO_FONT, "cm")
    path(cr, [(W / 2, 900), (W / 2, 1040)], prog(t, t0 + 0.5, 0.3), 8, RED, arrow=True)
    tm = T(tl, "b10", "तीन")
    streets(cr, 90, 1090, 900, 520, prog(t, t0 + 0.5, 0.3))
    q = prog(t, tm - 0.3, 0.4)
    x0, x1 = 260, 260 + 560 * q
    you_dot(cr, x0, 1350, t, 20, prog(t, t0 + 0.6, 0.3))
    if q > 0:
        map_pin(cr, x1, 1350, 40, RED, q)
        path(cr, [(x0, 1450), (x1, 1450)], 1.0, 6, INK, q)
        draw_text(cr, "300 M", (x0 + x1) / 2, 1470, 60, INK, q, anchor="ct")
    headline(cr, t, "1 MICROSECOND WRONG:", "300 M OFF", t0, tm)


def twist_scene(cr, t, t0, rate_sat=1.0, alpha=1.0):
    earth(cr, t, t0, cy=2150)
    _pic(cr, "gps_sat", 290, 760, 280, t, t0)
    clock(cr, 760, 760, 130, t, rate_sat, prog(t, t0 + 0.2, 0.3) * alpha, "SATELLITE CLOCK", CREAM)
    clock(cr, 760, 1440, 130, t, 1.0, prog(t, t0 + 0.4, 0.3) * alpha, "GROUND CLOCK", CREAM)


def r_twist(cr, t, tl, t0):                              # b11 "now hear the twist" (slate)
    twist_scene(cr, t, t0)
    headline(cr, t, "NOW THE", "TWIST", t0, T(tl, "b11", "ट्विस्ट"), small_color=CREAM, big_color=CORAL)


def r_38(cr, t, tl, t0):                                 # b11 "...up there the clock gets 38 microseconds ahead every day" (slate)
    t38 = T(tl, "b11", "अड़तीस")
    twist_scene(cr, t, -9, 1.0 + 0.7 * prog(t, t38 - 0.4, 0.4))
    counter(cr, t, t38 - 0.1, 400, 1100, "38", 130)
    draw_text(cr, "µs AHEAD", 520, 1100, 64, CORAL, prog(t, t38 + 0.2, 0.3), anchor="lm")
    draw_text(cr, "EVERY DAY", 520, 1170, 34, CREAM, prog(t, t38 + 0.3, 0.3), MONO_FONT, "lm", tracking=2)
    headline(cr, t, "UP THERE, EVERY DAY:", "38 µs AHEAD", t0, t38, small_color=CREAM, big_color=CORAL)


def r_math(cr, t, tl, t0):                               # b13 "a 38 microsecond error... means more than 11 km"
    q = prog(t, t0, 0.3)
    cr.set_source_rgba(0.83, 0.72, 0.54, q)
    rrect(cr, 120, 660, 840, 700, 18)
    cr.fill()
    t11 = T(tl, "b13", "ग्यारह")
    rows = (("1 µs", "300 M", t0 + 0.1, INK), ("38 µs", "11.4 KM", t11 - 0.2, RED))
    for i, (a, b, ts, col) in enumerate(rows):
        p = prog(t, ts, 0.3)
        y = 820 + 260 * i
        draw_text(cr, a, 190, y, 96, col, p, MONO_FONT, "lm")
        path(cr, [(500, y), (600, y)], p, 7, col, arrow=True)
        draw_text(cr, b, 640, y, 96 if i == 0 else 72, col, p, MONO_FONT, "lm")
    headline(cr, t, "38 µs WRONG MEANS", "11 KM OFF", t0, t11)


def r_day(cr, t, tl, t0):                                # b13 "...every single day" (slate)
    calendar(cr, t, t0 + 0.1, W / 2, 1150, ["DAY 1", "DAY 2", "DAY 3"], "+11 km each", interval=0.35, w=420, h=440)
    headline(cr, t, "AND AGAIN,", "EVERY DAY", t0, t0 + 0.2, small_color=CREAM, big_color=CORAL)


DRIFT = [(400, 1300), (520, 1130), (650, 1010), (760, 880), (900, 760)]


def d_drift(cr, t, tl, t0):                              # b14 "uncorrected, in a few days your map puts you in another city"
    streets(cr, 90, 620, 690, 1000, prog(t, t0, 0.3), seed=3)
    streets(cr, 820, 560, 200, 300, prog(t, t0 + 0.2, 0.3), seed=5)
    draw_text(cr, "ANOTHER", 920, 880, 34, INK, prog(t, T(tl, "b14", "शहर") - 0.3, 0.3), MONO_FONT, "ct")
    draw_text(cr, "CITY", 920, 920, 34, INK, prog(t, T(tl, "b14", "शहर") - 0.3, 0.3), MONO_FONT, "ct")
    you_dot(cr, *DRIFT[0], t, 22, prog(t, t0, 0.3))
    draw_text(cr, "YOU", DRIFT[0][0] - 40, DRIFT[0][1] + 50, 40, BLUE, prog(t, t0, 0.3), anchor="ct")
    f = prog(t, T(tl, "b14", "दिनों") - 0.4, 2.0)
    pts = DRIFT
    seg = f * (len(pts) - 1)
    k = min(int(seg), len(pts) - 2)
    u = seg - k
    x, y = pts[k][0] + (pts[k + 1][0] - pts[k][0]) * u, pts[k][1] + (pts[k + 1][1] - pts[k][1]) * u
    path(cr, pts, f, 5, RED, 0.7, dash=[12, 10])
    for i, lab in enumerate(("DAY 1", "DAY 2", "DAY 3")):
        if seg >= i + 1:
            px, py = pts[i + 1]
            draw_text(cr, lab, px - 30, py + 10, 34, RED, 1.0, MONO_FONT, "rt")
    map_pin(cr, x, y, 34, RED, prog(t, t0 + 0.3, 0.3))
    headline(cr, t, "IN A FEW DAYS, YOUR MAP SAYS", "ANOTHER CITY", t0, T(tl, "b14", "शहर"))


def x_1977(cr, t, tl, t0):                               # b15 "but in 1977, when the first GPS satellite went up..."
    _pic(cr, "nts2", 320, 1110, 0, t, t0, frame=(500, 820), rot=-0.02)
    counter(cr, t, T(tl, "b15", "सतहत्तर") - 0.3, 780, 860, "1977", 100)
    card(cr, t, T(tl, "b15", "पहला"), 600, 1060, ["THE FIRST", "GPS SATELLITE"], size=46)
    card(cr, t, T(tl, "b15", "पहला") + 0.4, 600, 1260, ["NTS-2, US NAVY"], size=30, seed=6)
    headline(cr, t, "1977: THE FIRST", "GPS SATELLITE", t0, T(tl, "b15", "पहला"))


def x_unsure(cr, t, tl, t0):                             # b15 "...nobody knew: faster or slower? so what did they do?" (slate)
    tf, ts, tq = T(tl, "b15", "तेज़"), T(tl, "b15", "धीमी"), T(tl, "b15", "क्या")
    wob = 1.0 + 0.9 * math.sin(t * 2.5)
    clock(cr, W / 2, 1080, 220, t, wob, prog(t, t0, 0.3))
    draw_text(cr, "FASTER?", 860, 760, 70, CORAL, prog(t, tf, 0.3), anchor="cm")
    draw_text(cr, "SLOWER?", 220, 760, 70, CREAM, prog(t, ts, 0.3), anchor="cm")
    card(cr, t, tq - 0.1, 250, 1450, ["SO WHAT DID", "THEY DO?"], size=56)
    headline(cr, t, "NOBODY WAS", "SURE", t0, T(tl, "b15", "पक्का"), small_color=CREAM, big_color=CORAL)


def x_weeks(cr, t, tl, t0):                              # b16 "they let the clock run 3 weeks without correction"
    calendar(cr, t, T(tl, "b16", "हफ़्ते") - 0.2, W / 2, 1150, ["WEEK 1", "WEEK 2", "WEEK 3"], "no correction",
             interval=0.5, w=420, h=440)
    headline(cr, t, "THEY LET IT RUN FOR", "3 WEEKS", t0, T(tl, "b16", "हफ़्ते"))


def x_right(cr, t, tl, t0):                              # b16 "...it ran exactly as fast as Einstein's maths said: <1% off"
    _pic(cr, "einstein", 300, 1330, 760, t, t0)
    tick(cr, 780, 900, 170, prog(t, T(tl, "b16", "हिसाब"), 0.35), color=GREEN)
    card(cr, t, T(tl, "b16", "परसेंट") - 0.2, 560, 1180, ["LESS THAN 1%", "MEASURED VS EINSTEIN"], size=48)
    headline(cr, t, "EINSTEIN WAS", "RIGHT", t0, T(tl, "b16", "हिसाब"), big_color=GREEN)


def x_offset(cr, t, tl, t0):                             # b17 "since then, every GPS clock is set slow before launch" (slate)
    td = T(tl, "b17", "धीमा")
    draw_text(cr, "10.23 MHz", W / 2, 760, 96, CREAM, prog(t, t0, 0.3), MONO_FONT, "cm")
    if t > td - 0.2:
        strike(cr, 260, 770, 820, 760, prog(t, td - 0.2, 0.3))
    s = "10.22999999543 MHz"
    n = int(len(s) * prog(t, td, 1.0))
    draw_text(cr, s[:n], 90, 960, 66, CORAL, 1.0 if n else 0.0, MONO_FONT, "lm")
    knob(cr, W / 2, 1360, 150, -0.9 * prog(t, td, 0.8), prog(t, t0 + 0.2, 0.3))
    draw_text(cr, "BEFORE LAUNCH", W / 2, 1560, 44, CREAM, prog(t, t0 + 0.4, 0.3), MONO_FONT, "ct", tracking=3)
    headline(cr, t, "EVERY GPS CLOCK IS SET", "SLOWER", t0, td, small_color=CREAM, big_color=CORAL)


def x_orbit(cr, t, tl, t0):                              # b17 "...so up there it runs exactly right" (slate)
    earth(cr, t, t0, cy=2100)
    _pic(cr, "gps_sat", 420, 880, 380, t, t0)
    clock(cr, 800, 1150, 140, t, 1.0, prog(t, t0 + 0.2, 0.3))
    ts = T(tl, "b17", "सही")
    tick(cr, 900, 960, 110, prog(t, ts, 0.3), color=GREEN)
    headline(cr, t, "SO IN ORBIT IT RUNS", "EXACTLY RIGHT", t0, ts, small_color=CREAM, big_color=GREEN)


def n_navic(cr, t, tl, t0):                              # b18 "India's own GPS, NavIC, runs on these atomic clocks too"
    _pic(cr, "india_map", 400, 1220, 700, t, t0)
    _pic(cr, "irnss", 850, 980, 0, t, t0 + 0.4, frame=(320, 520), rot=0.03)
    draw_text(cr, "NAVIC SATELLITE", 850, 1260, 28, INK, prog(t, t0 + 0.6, 0.3), MONO_FONT, "ct")
    draw_text(cr, "(MODEL)", 850, 1295, 24, INK, prog(t, t0 + 0.6, 0.3), MONO_FONT, "ct")
    ta = T(tl, "b18", "एटॉमिक")
    clock(cr, 850, 1480, 80, t, 1.0, prog(t, ta, 0.3), "ATOMIC CLOCKS")
    headline(cr, t, "INDIA'S OWN GPS:", "NAVIC", t0, T(tl, "b18", "नाविक"))


def n_dead(cr, t, tl, t0):                               # b18 "...when an ISRO satellite's 3 clocks all stopped" (slate)
    t3 = T(tl, "b18", "तीनों")
    for i, x in enumerate((210, 540, 870)):
        stop = t3 + 0.35 * i
        clock(cr, x, 1030, 120, t, 1.0, prog(t, t0 + 0.1 * i, 0.3), stopped=stop)
        cross(cr, x, 1030, 120, prog(t, stop, 0.25))
    card(cr, t, t0 + 0.3, 330, 1300, ["IRNSS-1A", "ALL 3 CLOCKS FAILED, 2016"], size=46)
    stamp(cr, t, "NO MORE NAVIGATION", T(tl, "b18", "लायक") - 0.2, W / 2, 1640, 56, color=CORAL)
    headline(cr, t, "ISRO SATELLITE: ALL 3 CLOCKS", "STOPPED", t0, T(tl, "b18", "बंद"), small_color=CREAM,
             big_color=CORAL)


def z_door(cr, t, tl, t0):                               # b19 "next time the delivery reaches right to your door..."
    _pic(cr, "scooter", 300, 1110, 0, t, t0, frame=(480, 720), rot=-0.03)
    td = T(tl, "b19", "दरवाज़े")
    path(cr, [(560, 1300), (680, 1200), (720, 1400), (820, 1440)], prog(t, t0 + 0.4, 1.2), 6, RED, 0.8,
         dash=[14, 10], arrow=True)
    door(cr, 880, 1600, 420, prog(t, td - 0.4, 0.3))
    tick(cr, 960, 1200, 90, prog(t, td + 0.1, 0.3), color=GREEN)
    headline(cr, t, "WHEN THE DELIVERY REACHES", "YOUR DOOR", t0, td)


def z_einstein(cr, t, tl, t0):                           # b19 "...remember, Einstein's maths is behind it"
    _pic(cr, "einstein", 330, 1300, 800, t, t0)
    phone_map(cr, 820, 1260, 620, t, prog(t, t0 + 0.3, 0.3), pin=(0, 0, prog(t, t0 + 0.6, 0.3)))
    headline(cr, t, "BEHIND IT, EVERY TIME:", "EINSTEIN", t0, T(tl, "b19", "आइंस्टीन"))


def e_question(cr, t, tl, t0):                           # b20 "did you know your head ages faster than your feet?"
    _pic(cr, "person", 260, 1230, 1000, t, t0)
    clock(cr, 470, 760, 70, t, 1.6, prog(t, t0 + 0.2, 0.3))
    yes_no_card(cr, t, T(tl, "b20", "यस") - 0.2, 780, 1250, w=540, h=300, question="COMMENT: YES OR NO")
    headline(cr, t, "DID YOU KNOW YOUR HEAD AGES", "FASTER?", t0, T(tl, "b20", "तेज़"), t_ghost=t0)


SHOTS = [   # (line, cue where the shot starts, draw function, background)
    ("b1", None, h_head, "paper"),
    ("b2", None, p_physics, "slate"), ("b2", "फ़ोन", p_phone, "paper"),
    ("b3", None, e_rule, "paper"),
    ("b4", None, n_lab, "paper"), ("b4", "और", n_foot, "slate"),
    ("b5", None, n_fast, "slate"),
    ("b6", None, t_tiny, "paper"), ("b6", "पर", t_phone, "slate"),
    ("b7", None, g_orbit, "slate"), ("b7", "अंदर", g_inside, "paper"),
    ("b8", None, g_blind, "slate"), ("b8", "वो", g_send, "slate"),
    ("b9", None, g_four, "slate"),
    ("b10", None, l_light, "slate"), ("b10", "माइक्रोसेकंड", l_300, "paper"),
    ("b11", None, r_twist, "slate"), ("b11", "सैटेलाइट", r_38, "slate"),
    ("b13", None, r_math, "paper"), ("b13", "हर", r_day, "slate"),
    ("b14", None, d_drift, "paper"),
    ("b15", None, x_1977, "paper"), ("b15", "किसी", x_unsure, "slate"),
    ("b16", None, x_weeks, "paper"), ("b16", "आइंस्टीन", x_right, "paper"),
    ("b17", None, x_offset, "slate"), ("b17", "ताकि", x_orbit, "slate"),
    ("b18", None, n_navic, "paper"), ("b18", "इसरो", n_dead, "slate"),
    ("b19", None, z_door, "paper"), ("b19", "याद", z_einstein, "paper"),
    ("b20", None, e_question, "paper"),
]


def draw(cr, t, tl):
    draw_frame(cr, t, tl, SHOTS)


def sfx(tl):
    """A whoosh on every cut, thuds on the strike, the closed eye and the dead clocks, ticks (and music dips) before
    the twist, the re-hook and the closing line, typing under the offset number."""
    ev = [(s, "whoosh", 0.25) for s in starts(tl, SHOTS)[1:]]
    ev += [(T(tl, "b2", "नहीं"), "thud", 0.0), (T(tl, "b8", "नहीं"), "thud", 0.0), (T(tl, "b18", "तीनों"), "thud", 0.0),
           (T(tl, "b11", None) - 0.35, "tick", 0.0), (T(tl, "b15", None) - 0.35, "tick", 0.0),
           (T(tl, "b20", None) - 0.35, "tick", 0.0), (T(tl, "b17", "धीमा"), "typing", 1.0),
           (T(tl, "b20", "यस"), "typing", 1.0)]
    for bid in ("b4", "b7", "b13", "b16"):
        ev.append((tl[bid].start + 0.4, "pop", 0.0))
    ev += [(at, "dip", 0.5) for at, name, _ in list(ev) if name == "tick"]   # the bed dips just before a reveal
    return ev
