"""Video 4: "Machhar ke munh se 3D printing" - a dead mosquito's feeding tube as a 3D-printer nozzle (3D necroprinting,
McGill + Drexel, Science Advances). Script approved by the owner 30 Oct 2026 ("Approve both"; scripts_batch2.md,
video 4); narration below is that script word for word, in Devanagari for the voice, with numbers written as words.
Hook b0 added by the owner, 30 Oct 2026 ("make strong hook as in further your kidney and liver can be 3d printed with
help of mosquito what yes mosquito"); it says "ho sakte hain" (could be), and b19-b20 still answer "not yet".
Organs appear only as the field's dream and as "not yet": the study printed tiny cell-laden structures, not organs."""
import math
import os

from PIL import Image

from poster import (CORAL, CREAM, GOLD, GREEN, INK, MARGIN, RED, W, calendar, card, clamp, counter, draw_text, ease,
                    footnote, gauge, headline, path, photo, prog, ring, stamp, text_size, yes_no_card)

# the narrator, music and tail are channel-wide; render_hi reads them from this module
from channel import ASSETS_ROOT, MUSIC, NARRATOR, NARRATOR_LABEL, REVEAL_GAP, TAIL, VOICE_REF  # noqa: F401
from shots import T, asset_finder, checklist, draw_frame, pic, starts

SCRIPT = [
    dict(id="b0", text="फ्यूचर में तुम्हारी किडनी और लिवर थ्री-डी प्रिंट हो सकते हैं... एक मच्छर की मदद से। क्या? हाँ, मच्छर।"),
    dict(id="b1", text="सोचो, जो मच्छर तुम्हारा ख़ून चूसता है... उसका मुँह अब साइंटिस्ट्स के थ्री-डी प्रिंटर की नोज़ल "
                       "बन गया है।"),
    dict(id="b2", text="और ये नोज़ल ज़िंदा सेल्स प्रिंट करती है। वो भी मच्छर के मरने के बाद।"),
    dict(id="b3", text="ये कोई साइंस-फ़िक्शन मूवी नहीं है। कनाडा की मैक-गिल यूनिवर्सिटी और अमेरिका की ड्रेक्सल यूनिवर्सिटी "
                       "की रिसर्च है।", gap=REVEAL_GAP),
    dict(id="b4", text="इसे नाम दिया गया: थ्री-डी नेक्रो-प्रिंटिंग। नेक्रो मतलब... मौत।"),
    dict(id="b5", text="थ्री-डी प्रिंटर समझना है? मेहंदी कोन सोचो।"),
    dict(id="b6", text="कोन दबाओ, पतला पेस्ट निकले, और लाइन पे लाइन डिज़ाइन बन जाए। थ्री-डी प्रिंटर भी बिल्कुल यही करता है।"),
    dict(id="b7", text="और जितना पतला कोन का छेद, उतना बारीक डिज़ाइन।"),
    dict(id="b8", text="अब डॉक्टर्स का एक बड़ा सपना है: इंसान का टिशू, और एक दिन पूरे ऑर्गन्स प्रिंट करना।"),
    dict(id="b9", text="इसके लिए ज़िंदा सेल्स को बहुत ही बारीक लाइन्स में रखना पड़ता है।"),
    dict(id="b10", text="पर इतनी बारीक नोज़ल्स बनाना मुश्किल है। काँच की नोज़ल्स महँगी होती हैं, और आसानी से टूट जाती हैं।"),
    dict(id="b11", text="तो साइंटिस्ट्स ने कई कीड़ों के मुँह चेक किए... और जीत गया मच्छर।"),
    dict(id="b12", text="क्योंकि मादा मच्छर का मुँह, जिससे वो ख़ून चूसती है, पहले से एक पतली, खोखली और मज़बूत नली है।",
         gap=REVEAL_GAP),
    dict(id="b13", text="और सबसे हैरानी की बात? इसका छेद सिर्फ़ बीस माइक्रॉन का है। इंसान के बाल से कई गुना पतला।"),
    dict(id="b14", text="सबसे पतली इंजेक्शन की सुई का छेद भी इससे कई गुना बड़ा होता है।"),
    dict(id="b15", text="साइंटिस्ट्स ने माइक्रोस्कोप के नीचे मच्छर का मुँह निकाला, और उसे एक सिरिंज की टिप पे चिपका दिया।"),
    dict(id="b16", text="फिर इससे प्रिंट किए: एक हनीकॉम्ब, एक मेपल लीफ़, और ग्रिड वाले छोटे ढाँचे। चावल के दाने से भी छोटे।"),
    dict(id="b17", text="और इनमें ज़िंदा सेल्स थे: ख़ून के लाल सेल्स, और कैंसर रिसर्च वाले सेल्स।"),
    dict(id="b18", text="प्रिंट होने के बाद लगभग छियासी परसेंट सेल्स ज़िंदा बचे।"),   # "प्रिंटिंग के बाद" came out
                                                                                # "printinting" in 9/9 takes (two spellings)
    dict(id="b19", text="तो क्या अब मच्छर से ऑर्गन्स बनेंगे?"),
    dict(id="b20", text="अभी नहीं। ये एक शुरुआत है: टिशू के छोटे ढाँचे, जिन पर सेल्स उगाए जा सकते हैं।"),
    dict(id="b21", text="और इसकी लिमिट्स भी हैं। ज़्यादा प्रेशर पे नोज़ल फट जाती है, और एक नोज़ल कुछ दिनों तक ही चलती है।"),
    dict(id="b22", text="पर ये सस्ती है, आसानी से मिल जाती है, और मिट्टी में घुल जाती है।", gap=REVEAL_GAP),
    dict(id="b23", text="सोचो, जो मच्छर हर साल लाखों जानें लेता है... वही एक दिन जान बचाने वाले टिशू बनाने में मदद कर सकता है।"),
    dict(id="b24", text="अगर मच्छर के मुँह से बना टिशू कभी तुम्हारे इलाज में लगे... तुम लगवाओगे? यस या नो, कमेंट में बताओ।"),
]

METADATA = dict(
    title="Machhar ke munh se 3D printing",
    caption="Future mein tumhari kidney aur liver 3D print ho sakte hain... ek machhar ki madad se. Kya? Haan, "
            "machhar 😳\n\n"
            "Jo machhar tumhara khoon choosta hai, uska munh ab 3D printer ki nozzle hai, aur ye zinda cells print "
            "karta hai.\n\n"
            "Scientists ne mare hue machhar ki feeding tube ko nozzle banaya: lines sirf ~20 micron, insaan ke baal se "
            "kai guna patli. Printing ke baad ~86% cells zinda bache.\n\n"
            "Organs abhi nahi, par tissue ki taraf ye ek pehla qadam hai.\n\n"
            "Machhar ke munh se bana tissue tumhare ilaaj mein lage, toh lagwaoge? Comment mein YES ya NO likho 👇",
    yt_title="Machhar Se 3D Print Hogi Kidney? 😳 | Necroprinting",
    yt_description="Canada ki McGill University aur America ki Drexel University ke scientists ne mare hue machhar ki "
                   "feeding tube ko 3D printer ki nozzle bana diya: 3D necroprinting. Lines sirf ~20 micron, aur zinda "
                   "cells ke saath printing. Organs abhi nahi, par tissue ki taraf ek pehla qadam.",
    hashtags=["#3dprinting", "#mosquito", "#science", "#techinhindi", "#factsinhindi"],
    pinned_comment="Machhar ke munh se bana tissue ilaaj mein lage, toh lagwaoge? 🦟 YES ya NO? 👇",
    sources=["Puma et al., 3D Necroprinting, Science Advances (McGill University, Drexel University)",
             "Interesting Engineering; Earth.com; 3D Printing Industry",
             "Hypodermic needle gauge table",
             "WHO, malaria and vector-borne diseases"],
)

_find = asset_finder("mosquito", "toxoplasma2")
P = {k: _find(k) for k in ("mosquito", "mosquito_proboscis", "mehndi_cone", "henna_hand", "printer_3d",
                           "bioprinter_lab", "glass_pipette", "syringe", "needle_tip", "tweezers", "rice_grains",
                           "human_hair", "red_blood_cells", "petri_dish", "honeybee", "housefly", "clapperboard",
                           "world_map", "university_building", "heart_engraving", "kidney_engraving", "pressure_gauge",
                           "microscope", "mosquito_proboscis_sem", "henna_hand_alt", "kidney_bioart", "liver_bioart")}
USED_ASSETS = [os.path.basename(v) for v in P.values() if v]
CREDITS_FILES = [os.path.join(ASSETS_ROOT, d, "credits.json") for d in ("mosquito", "toxoplasma2")]

HENNA, STEEL, CELL = (0.45, 0.22, 0.08), (0.62, 0.64, 0.68), (0.85, 0.25, 0.30)


def _pic(cr, key, cx, cy, h, t, t0, **kw):
    pic(cr, P.get(key), cx, cy, h, t, t0, **kw)


# ---------- drawing pieces for this video ----------

def syringe_tip(cr, x, y, p, alpha=1.0):
    """A plastic dispenser tip (grey taper) arriving from the left to meet the proboscis at (x, y)."""
    if p <= 0:
        return
    dx = -300 * (1 - ease(p))
    cr.move_to(x - 260 + dx, y - 60)
    cr.line_to(x + dx, y - 10)
    cr.line_to(x + dx, y + 10)
    cr.line_to(x - 260 + dx, y + 60)
    cr.close_path()
    cr.set_source_rgba(*STEEL, alpha)
    cr.fill_preserve()
    cr.set_source_rgba(*INK, 0.8 * alpha)
    cr.set_line_width(4)
    cr.stroke()


def cell_stream(cr, t, x0, y0, x1, y1, alpha=1.0, n=10):
    """Living cells (red dots) flowing from (x0, y0) to (x1, y1), then laid as a line from x1 onward."""
    for i in range(n):
        f = (t * 0.6 + i / n) % 1.0
        cr.set_source_rgba(*CELL, alpha * 0.9)
        cr.arc(x0 + (x1 - x0) * f, y0 + (y1 - y0) * f, 9, 0, 2 * math.pi)
        cr.fill()


def swirl(cx, cy, r, turns=2.2, n=90):
    return [(cx + r * (i / n) * math.cos(turns * 2 * math.pi * i / n),
             cy + r * (i / n) * math.sin(turns * 2 * math.pi * i / n)) for i in range(n + 1)]


def layers(cr, t, t0, x, y, w, n=8, alpha=1.0):
    """A 3D print growing layer by layer: n stacked lines appear in turn, with the print head riding the top one."""
    k = clamp((t - t0) / 0.35, 0, n)
    for i in range(int(k) + 1):
        if i >= n:
            break
        f = clamp(k - i)
        yy = y - 22 * i
        path(cr, [(x, yy), (x + w * f, yy)], 1.0, 16, HENNA, alpha)
        if i == int(k):
            cr.set_source_rgba(*STEEL, alpha)
            cr.rectangle(x + w * f - 30, yy - 90, 60, 70)
            cr.fill()


def hexgrid(cr, cx, cy, r, p, alpha=1.0):
    cells = [(0, 0), (1.5, 0.87), (1.5, -0.87), (-1.5, 0.87), (-1.5, -0.87), (0, 1.73), (0, -1.73)]
    for i, (u, v) in enumerate(cells):
        q = clamp(p * len(cells) - i)
        if q <= 0:
            break
        pts = [(cx + r * u + r * math.cos(a), cy + r * v + r * math.sin(a))
               for a in [k * math.pi / 3 for k in range(7)]]
        path(cr, pts, q, 6, CELL, alpha)


def leaf(cr, cx, cy, s, p, alpha=1.0):
    """A simple maple-leaf outline drawn as one stroke."""
    pts = [(0, 1.0), (0.05, 0.45), (0.55, 0.55), (0.42, 0.3), (0.95, 0.0), (0.55, -0.05), (0.62, -0.45),
           (0.25, -0.25), (0.0, -0.95), (-0.25, -0.25), (-0.62, -0.45), (-0.55, -0.05), (-0.95, 0.0), (-0.42, 0.3),
           (-0.55, 0.55), (-0.05, 0.45), (0, 1.0)]
    path(cr, [(cx + s * u, cy - s * v) for u, v in pts], p, 6, CELL, alpha)


def grid(cr, cx, cy, s, p, alpha=1.0, n=5):
    for i in range(n + 1):
        q = clamp(p * 2 * (n + 1) - i)
        o = -s / 2 + s * i / n
        path(cr, [(cx - s / 2, cy + o), (cx + s / 2, cy + o)], q, 5, CELL, alpha)
        path(cr, [(cx + o, cy - s / 2), (cx + o, cy + s / 2)], clamp(q - 0.5), 5, CELL, alpha)


def tube_section(cr, cx, cy, r_out, r_in, alpha=1.0):
    """Cross-section of the proboscis: a wall ring around an empty channel."""
    cr.set_source_rgba(0.35, 0.22, 0.14, alpha)
    cr.arc(cx, cy, r_out, 0, 2 * math.pi)
    cr.fill()
    cr.set_source_rgba(0.95, 0.91, 0.82, alpha)
    cr.arc(cx, cy, r_in, 0, 2 * math.pi)
    cr.fill()


def to_scale(cr, t, t0, items, cx, y, k=4.0):
    """Circles to scale (diameter in microns x k px), side by side, labelled; items: [(label, microns, colour)]."""
    x = cx - sum(d * k for _, d, _ in items) / 2 - 40 * (len(items) - 1) / 2
    for i, (label, d, col) in enumerate(items):
        p = prog(t, t0 + 0.25 * i, 0.3)
        r = d * k / 2
        cr.set_source_rgba(*col, 0.9 * p)
        cr.set_line_width(6)
        cr.arc(x + r, y, r * (0.4 + 0.6 * p), 0, 2 * math.pi)
        cr.stroke()
        draw_text(cr, label, x + r, y + max(r, 40) + 30, 40, col, p, anchor="ct")
        x += 2 * r + 40


def crack(cr, x, y, p, alpha=1.0):
    pts = [(x, y), (x + 30, y + 40), (x + 5, y + 80), (x + 40, y + 130), (x + 15, y + 180)]
    path(cr, pts, p, 5, INK, alpha)


# ---------- shots ----------
# Rules (style bible + parasite-reels study): a new picture every ~3-4 s cut on the word, the literal noun on screen,
# red = the key word, green = good news, gold = numbers, dark slate for the microscopic world.

_SIZE = {}


def printing(cr, t, key, cx, cy, h, p):
    """A photo being 3D printed: shown from the bottom up to p (0-1), a fresh layer and the print head on the top edge."""
    if not P.get(key) or p <= 0:
        return
    if key not in _SIZE:
        with Image.open(P[key]) as im:
            _SIZE[key] = im.width / im.height
    w, y = h * _SIZE[key], cy + h / 2 - h * p
    cr.save()
    cr.rectangle(0, y, W, 1920)
    cr.clip()
    _pic(cr, key, cx, cy, h, t, -1)
    cr.restore()
    if p < 1:
        path(cr, [(cx - w / 2, y), (cx + w / 2, y)], 1.0, 6, HENNA, 0.9)
        x = cx + 0.45 * w * math.sin(t * 7)
        cr.set_source_rgba(*STEEL, 1)
        cr.rectangle(x - 30, y - 90, 60, 66)
        cr.fill()
        cr.move_to(x - 14, y - 24)
        cr.line_to(x + 14, y - 24)
        cr.line_to(x, y - 2)
        cr.close_path()
        cr.fill()


def h_organs(cr, t, tl, t0):                             # b0 frame 0: "someday your kidney and liver could be 3D printed..."
    printing(cr, t, "kidney_bioart", 290, 1120, 560, 0.6 + 0.4 * prog(t, 0.0, 1.6))
    printing(cr, t, "liver_bioart", 800, 1160, 360, 0.5 + 0.5 * prog(t, 0.6, 1.6))
    headline(cr, t, "SOMEDAY, YOUR KIDNEY & LIVER", "3D PRINTED", -1, min(1.8, T(tl, "b0", "प्रिंट")), t_ghost=-1)


def h_mosq(cr, t, tl, t0):                               # b0 "...with the help of a mosquito"
    _pic(cr, "liver_bioart", 230, 1000, 190, t, -1)
    _pic(cr, "kidney_bioart", 230, 1330, 300, t, -1)
    _pic(cr, "mosquito", 1320 - 560 * prog(t, t0, 0.5), 1170, 360, t, -1)   # flies in from the right
    headline(cr, t, "WITH THE HELP OF A", "MOSQUITO", t0, t0 + 0.15)


def h_what(cr, t, tl, t0):                               # b0 "What? Yes, a mosquito."
    th = T(tl, "b0", "हाँ")
    _pic(cr, "mosquito", W / 2 + 60, 1180, 420, t, t0 - 0.2, flip=True)   # on screen from the cut's first frame
    q = prog(t, t0, 0.25) * (1 - prog(t, th, 0.2))
    draw_text(cr, "?", 230, 900, 300 * (0.8 + 0.2 * q), RED, q, anchor="cm")
    stamp(cr, t, "YES!", th, 230, 900, 90)
    headline(cr, t, "WHAT? YES,", "A MOSQUITO", t0, th, t_ghost=t0)


def h_mouth(cr, t, tl, t0):                              # b1 "socho: the mosquito that sucks your blood..."
    _pic(cr, "mosquito", W / 2, 1060, 520, t, t0)
    ring(cr, 230, 1090, 170, 90, prog(t, t0 + 0.6, 0.5))
    headline(cr, t, "THE SAME ONE THAT", "DRINKS YOUR BLOOD", t0, T(tl, "b1", "चूसता"))


def h_nozzle(cr, t, tl, t0):                             # b1 "...its mouth is now a 3D printer's nozzle"
    _pic(cr, "mosquito_proboscis", W / 2, 1060, 0, t, t0, frame=(860, 600))
    ring(cr, W / 2 - 20, 1150, 70, 190, prog(t, t0 + 0.3, 0.5))
    card(cr, t, t0 + 0.6, 620, 1400, ["= NOZZLE"], size=56)
    headline(cr, t, "NOW IT'S A", "NOZZLE", t0, T(tl, "b1", "नोज़ल"))


def h_cells(cr, t, tl, t0):                              # b2 "this nozzle prints living cells"
    syringe_tip(cr, 420, 900, 1.0)
    path(cr, [(420, 900), (620, 960)], 1.0, 6, (0.35, 0.22, 0.14), 1.0)
    cell_stream(cr, t, 420, 900, 620, 960)
    path(cr, [(620, 1000), (980, 1000), (980, 1100), (200, 1100), (200, 1200), (980, 1200)],
              prog(t, t0 + 0.3, 2.5), 14, CELL)
    headline(cr, t, "IT PRINTS", "LIVING CELLS", t0, T(tl, "b2", "ज़िंदा"))


def h_dead(cr, t, tl, t0):                               # b2 "...after the mosquito is dead"
    _pic(cr, "mosquito", W / 2, 1100, 640, t, -1, tint=(0.55, 0.55, 0.55))
    stamp(cr, t, "DEAD", t0 + 0.3, W / 2, 1440, 100)
    headline(cr, t, "AFTER IT'S", "DEAD", t0, t0 + 0.3)


def r_real(cr, t, tl, t0):                               # b3 "not a sci-fi movie..."
    _pic(cr, "clapperboard", W / 2, 1080, 600, t, t0)
    stamp(cr, t, "NOT SCI-FI", t0 + 0.6, W / 2, 1420, 80)
    headline(cr, t, "NOT A", "SCI-FI MOVIE", t0, t0 + 0.4)


def r_unis(cr, t, tl, t0):                               # b3 "...research from McGill (Canada) and Drexel (USA)"
    _pic(cr, "world_map", W / 2, 960, 440, t, t0, tint=(0.55, 0.47, 0.38))
    for i, (x, y, lab) in enumerate(((350, 880, "McGILL, CANADA"), (338, 912, "DREXEL, USA"))):
        q = prog(t, t0 + 0.4 + 0.4 * i, 0.3)
        cr.set_source_rgba(*RED, q)
        cr.arc(x, y, 12, 0, 2 * math.pi)
        cr.fill()
        card(cr, t, t0 + 0.5 + 0.4 * i, 90, 1240 + 120 * i, [lab], size=44)
    _pic(cr, "university_building", 800, 1330, 0, t, t0 + 0.8, rot=0.03, frame=(400, 280))
    footnote(cr, "Science Advances journal", prog(t, t0 + 1.2, 0.4), y=1520)
    headline(cr, t, "REAL RESEARCH:", "McGILL + DREXEL", t0, T(tl, "b3", "कनाडा"), big_size=130)


def n_name(cr, t, tl, t0):                               # b4 "its name: 3D necroprinting; necro means... death"
    _pic(cr, "mosquito", W / 2, 920, 480, t, t0, tint=(0.55, 0.55, 0.55))
    tn = T(tl, "b4", "नेक्रो")
    for i, (txt, ty) in enumerate((("3D NECRO-", 1240), ("PRINTING", 1360))):
        p = prog(t, tn + 0.3 * i, 0.3)
        if p > 0:
            tw_, th = text_size(txt, 96)
            cr.set_source_rgba(*RED, 0.92)
            cr.rectangle(MARGIN, ty - 12, (tw_ + 50) * p, th + 24)
            cr.fill()
            draw_text(cr, txt, MARGIN + 25, ty, 96, CREAM, clamp(p * 2 - 1))
    card(cr, t, T(tl, "b4", "मौत"), 620, 640, ["NECRO = DEATH"], size=44)
    headline(cr, t, "ITS NAME", "", t0, 1e9)


def m_printer(cr, t, tl, t0):                            # b5 "how does a 3D printer work?"
    _pic(cr, "printer_3d", W / 2, 1080, 680, t, t0)
    headline(cr, t, "HOW DOES A", "3D PRINTER WORK?", t0, t0 + 0.3, big_size=120)


def m_cone(cr, t, tl, t0):                               # b5 "...think of a mehndi cone"
    _pic(cr, "henna_hand", W / 2, 1080, 0, t, t0, frame=(860, 600))
    headline(cr, t, "THINK OF A", "MEHNDI CONE", t0, t0 + 0.3)


def m_henna(cr, t, tl, t0):                              # b6 "squeeze, thin paste, line on line"
    pts, p = swirl(W / 2 - 60, 1120, 200), prog(t, t0 + 0.3, 2.2)
    path(cr, pts, p, 9, HENNA, 0.95)
    k = min(len(pts) - 1, int(p * (len(pts) - 1)))
    if P["mehndi_cone"]:                                       # the cone's tip (lower left of the photo) on the line
        photo(cr, P["mehndi_cone"], pts[k][0] + 0.45 * 546, pts[k][1] - 0.42 * 420, 420)
    headline(cr, t, "SQUEEZE, DRAW,", "LINE BY LINE", t0, T(tl, "b6", "लाइन"))


def m_layers(cr, t, tl, t0):                             # b6 "...a 3D printer does exactly this"
    _pic(cr, "printer_3d", 240, 1360, 300, t, t0)
    layers(cr, t, t0 + 0.2, 420, 1300, 480)
    headline(cr, t, "A 3D PRINTER", "DOES THE SAME", t0, t0 + 0.3)


def m_finer(cr, t, tl, t0):                              # b7 "the thinner the hole, the finer the design"
    for i, (w, y, lab) in enumerate(((40, 900, "WIDE HOLE"), (8, 1250, "THIN HOLE"))):
        q = prog(t, t0 + 0.6 * i, 0.3)
        draw_text(cr, lab, MARGIN, y - 90, 46, INK, q)
        path(cr, swirl(620, y, 150, 1.6), prog(t, t0 + 0.6 * i, 1.0), w, HENNA, q)
    headline(cr, t, "THINNER HOLE,", "FINER DESIGN", t0, T(tl, "b7", "बारीक"))   # Anton's "=" is tiny


def o_dream(cr, t, tl, t0):                              # b8 "doctors' dream: tissue, one day whole organs"
    _pic(cr, "bioprinter_lab", W / 2, 960, 0, t, t0, frame=(820, 520))
    t_o = T(tl, "b8", "ऑर्गन्स")
    _pic(cr, "heart_engraving", 330, 1390, 0, t, t_o - 0.2, rot=-0.04, frame=(320, 320))
    _pic(cr, "kidney_engraving", 760, 1390, 0, t, t_o, rot=0.04, frame=(300, 320))
    stamp(cr, t, "SOMEDAY", t_o + 0.5, W / 2, 1220, 60)
    headline(cr, t, "THE DREAM:", "PRINT ORGANS", t0, t_o)


def o_cells(cr, t, tl, t0):                              # b9 "living cells must be laid in very fine lines" (slate)
    for r in range(7):
        q = prog(t, t0 + 0.15 * r, 0.6)
        for c in range(int(16 * q)):
            cr.set_source_rgba(*CORAL, 0.9)
            cr.arc(200 + 45 * c, 820 + 90 * r, 12, 0, 2 * math.pi)
            cr.fill()
    headline(cr, t, "CELLS IN", "FINE LINES", t0, t0 + 0.4, small_color=CREAM, big_color=CORAL)


def o_glass(cr, t, tl, t0):                              # b10 "glass nozzles: expensive, break easily"
    _pic(cr, "glass_pipette", W / 2, 1100, 260, t, t0)
    card(cr, t, T(tl, "b10", "महँगी"), 620, 800, ["EXPENSIVE"], size=48)
    crack(cr, 600, 1030, prog(t, T(tl, "b10", "टूट"), 0.4))
    headline(cr, t, "HARD TO MAKE,", "EASY TO BREAK", t0, T(tl, "b10", "टूट"))


def o_tested(cr, t, tl, t0):                             # b11 "they checked many insects' mouths... the mosquito won"
    cr.set_source_rgba(0.55, 0.38, 0.22, prog(t, t0, 0.3))      # a wooden specimen box
    cr.rectangle(120, 760, 840, 640)
    cr.fill()
    cr.set_source_rgba(0.93, 0.89, 0.80, prog(t, t0, 0.3))
    cr.rectangle(150, 790, 780, 580)
    cr.fill()
    for i, (key, x, lab) in enumerate((("honeybee", 290, "BEE"), ("housefly", 540, "FLY"), ("mosquito", 790, "MOSQUITO"))):
        _pic(cr, key, x, 1040, 230, t, t0 + 0.3 + 0.3 * i)
        draw_text(cr, lab, x, 1230, 36, RED if key == "mosquito" else INK, prog(t, t0 + 0.3 + 0.3 * i, 0.3),
                  anchor="ct")
    ring(cr, 790, 1060, 150, 180, prog(t, T(tl, "b11", "जीत"), 0.5))
    stamp(cr, t, "WINNER", T(tl, "b11", "जीत") + 0.3, 790, 760, 60)
    headline(cr, t, "THEY TESTED", "INSECT MOUTHS", t0, t0 + 0.4)


def o_tube(cr, t, tl, t0):                               # b12 "the female's mouth is already a thin, hollow, strong tube"
    _pic(cr, "mosquito_proboscis_sem", 330, 1060, 0, t, t0, frame=(460, 560))
    tube_section(cr, 780, 960, 150 * prog(t, t0 + 0.3, 0.4), 70 * prog(t, t0 + 0.3, 0.4))
    for i, (lab, cue) in enumerate((("THIN", "पतली"), ("HOLLOW", "खोखली"), ("STRONG", "मज़बूत"))):
        card(cr, t, T(tl, "b12", cue) - 0.1, 640, 1170 + 110 * i, [lab], size=50)
    headline(cr, t, "A FEMALE'S MOUTH:", "A READY TUBE", t0, t0 + 0.4)


def p_micron(cr, t, tl, t0):                             # b13 "the strangest part? its hole is only 20 microns"
    tube_section(cr, W / 2, 1000, 220, 100, prog(t, t0, 0.3))
    counter(cr, t, T(tl, "b13", "बीस"), W / 2, 1360, "20", 160, color=GOLD)
    draw_text(cr, "MICRONS", W / 2, 1460, 60, INK, prog(t, T(tl, "b13", "बीस") + 0.3, 0.3), anchor="ct")
    small, big = ("THE STRANGEST", "PART") if t < T(tl, "b13", "बीस") else ("ITS HOLE:", "20 MICRONS")
    headline(cr, t, small, big, t0, t0 + 0.4 if big == "PART" else T(tl, "b13", "बीस"), t_ghost=t0)


def p_hair(cr, t, tl, t0):                               # b13 "...many times thinner than a human hair"
    _pic(cr, "human_hair", W / 2, 860, 0, t, t0, frame=(820, 340))
    to_scale(cr, t, t0 + 0.3, [("HAIR ~70", 70, INK), ("HOLE 20", 20, RED)], W / 2, 1300)
    headline(cr, t, "THINNER THAN", "A HAIR", t0, T(tl, "b13", "बाल"))


def p_needle(cr, t, tl, t0):                             # b14 "even the thinnest needle's hole is many times bigger"
    _pic(cr, "needle_tip", W / 2, 860, 0, t, t0, frame=(820, 340))
    to_scale(cr, t, t0 + 0.3, [("NEEDLE ~130", 130, INK), ("HOLE 20", 20, RED)], W / 2, 1320, k=3.0)
    headline(cr, t, "EVEN A NEEDLE'S HOLE IS", "BIGGER", t0, t0 + 0.6)


def b_pull(cr, t, tl, t0):                               # b15 "under a microscope they took out the mouth..."
    _pic(cr, "microscope", 320, 1120, 720, t, t0)
    _pic(cr, "tweezers", 760, 1080, 520, t, t0 + 0.3, rot=0.5)
    headline(cr, t, "UNDER A MICROSCOPE:", "PULLED OUT", t0, T(tl, "b15", "निकाला"))


def b_glue(cr, t, tl, t0):                               # b15 "...and glued it on a syringe tip"
    _pic(cr, "syringe", 640, 1100, 120, t, t0)
    q = prog(t, t0 + 0.4, 0.4)                                  # the proboscis fixed on the needle end
    cr.set_source_rgba(0.35, 0.22, 0.14, q)
    cr.set_line_width(7)
    cr.move_to(240, 1100)
    cr.line_to(240 - 130 * q, 1112)
    cr.stroke()
    cr.set_source_rgba(0.95, 0.85, 0.30, 0.9 * prog(t, t0 + 0.8, 0.3))   # a drop of UV glue
    cr.arc(242, 1100, 18, 0, 2 * math.pi)
    cr.fill()
    ring(cr, 200, 1105, 120, 70, prog(t, t0 + 1.0, 0.4))
    headline(cr, t, "GLUED ON A", "SYRINGE TIP", t0, T(tl, "b15", "सिरिंज"))


def b_prints(cr, t, tl, t0):                             # b16 "they printed a honeycomb, a maple leaf, grids"
    hexgrid(cr, 250, 1000, 70, prog(t, T(tl, "b16", "हनीकॉम्ब") - 0.2, 1.0))
    leaf(cr, 560, 1000, 150, prog(t, T(tl, "b16", "मेपल") - 0.2, 1.0))
    grid(cr, 860, 1000, 220, prog(t, T(tl, "b16", "ग्रिड") - 0.2, 1.0))
    headline(cr, t, "THEY PRINTED:", "TINY SHAPES", t0, t0 + 0.4)


def b_rice(cr, t, tl, t0):                               # b16 "...smaller than a grain of rice"
    _pic(cr, "rice_grains", 640, 1100, 520, t, t0)
    hexgrid(cr, 300, 1060, 22, 1.0)
    leaf(cr, 300, 1220, 50, 1.0)
    footnote(cr, "honeycomb ~0.6 mm, leaf ~0.9 mm, rice grain ~6 mm", prog(t, t0 + 0.4, 0.4), y=1500)
    headline(cr, t, "SMALLER THAN", "A RICE GRAIN", t0, t0 + 0.3)


def b_cells(cr, t, tl, t0):                              # b17 "with living cells: red blood cells, cancer-research cells"
    _pic(cr, "red_blood_cells", 300, 1080, 0, t, t0 + 0.1, frame=(440, 440))   # on screen from the cut, not at "लाल"
    _pic(cr, "petri_dish", 790, 1100, 420, t, T(tl, "b17", "कैंसर") - 0.2)
    card(cr, t, T(tl, "b17", "लाल"), 120, 1360, ["RED BLOOD CELLS"], size=40)
    card(cr, t, T(tl, "b17", "कैंसर"), 600, 1360, ["CANCER-RESEARCH", "CELLS"], size=36)
    headline(cr, t, "INSIDE:", "LIVING CELLS", t0, t0 + 0.4)


def b_86(cr, t, tl, t0):                                 # b18 "about 86% of the cells survived"
    counter(cr, t, t0 + 0.2, W / 2 - 80, 900, "86", 240, color=GOLD)   # "%" is wider than a flip card
    draw_text(cr, "%", W / 2 + 110, 900, 200, INK, prog(t, t0 + 0.4, 0.2), anchor="lm")
    gauge(cr, t, t0 + 0.3, W / 2, 1360, 230, 0.0, 0.86, labels=("0", "100%"))
    headline(cr, t, "AFTER PRINTING:", "86% ALIVE", t0, t0 + 0.5, big_color=GREEN)


def q_organs(cr, t, tl, t0):                             # b19 re-hook: "so will mosquitoes make organs now?"
    _pic(cr, "heart_engraving", 330, 1080, 0, t, t0, frame=(420, 440))
    _pic(cr, "mosquito", 780, 1100, 300, t, t0 + 0.2)
    q = prog(t, t0 + 0.4, 0.3)
    draw_text(cr, "?", W / 2 + 40, 900, 300 * (0.8 + 0.2 * q), RED, q, anchor="cm")
    headline(cr, t, "SO, ORGANS FROM", "MOSQUITOES?", t0, t0 + 0.3, t_ghost=t0)


def q_not_yet(cr, t, tl, t0):                            # b20 "not yet: a start, tiny tissue scaffolds cells can grow on"
    grid(cr, W / 2, 1120, 520, prog(t, t0 + 0.3, 1.2))
    for i in range(int(30 * prog(t, T(tl, "b20", "उगाए"), 1.5))):
        a, d = i * 2.4, 40 + (i * 37) % 220
        cr.set_source_rgba(*CORAL, 0.85)
        cr.arc(W / 2 + d * math.cos(a), 1120 + d * math.sin(a), 13, 0, 2 * math.pi)
        cr.fill()
    stamp(cr, t, "NOT YET", t0 + 0.1, 800, 760, 70)
    headline(cr, t, "NOT YET:", "A FIRST STEP", t0, T(tl, "b20", "शुरुआत"))


def l_pressure(cr, t, tl, t0):                           # b21 "limits: too much pressure and it cracks"
    _pic(cr, "pressure_gauge", 360, 1080, 520, t, t0)
    path(cr, [(700, 860), (700, 1300)], 1.0, 10, (0.35, 0.22, 0.14), prog(t, t0 + 0.2, 0.3))
    crack(cr, 700, 980, prog(t, T(tl, "b21", "फट"), 0.4))
    headline(cr, t, "TOO MUCH PRESSURE:", "IT CRACKS", t0, T(tl, "b21", "फट"))


def l_days(cr, t, tl, t0):                               # b21 "...and one nozzle lasts only a few days"
    calendar(cr, t, t0 + 0.1, W / 2, 1060, ["DAY 1", "DAY 2", "DAY 3", "DAY 4"], "ONE NOZZLE", interval=0.35)
    headline(cr, t, "IT LASTS", "A FEW DAYS", t0, t0 + 0.4)


def l_good(cr, t, tl, t0):                               # b22 "but it's cheap, easy to get, and biodegradable"
    checklist(cr, t, 110, 700, 860, "THE MOSQUITO NOZZLE",
              [("CHEAP", T(tl, "b22", "सस्ती") - 0.2, "tick", T(tl, "b22", "सस्ती")),
               ("EASY TO GET", T(tl, "b22", "आसानी") - 0.2, "tick", T(tl, "b22", "आसानी")),
               ("BIODEGRADABLE", T(tl, "b22", "मिट्टी") - 0.2, "tick", T(tl, "b22", "मिट्टी"))])
    headline(cr, t, "BUT IT'S", "CHEAP & GREEN", t0, t0 + 0.4, big_color=GREEN)


def e_taking(cr, t, tl, t0):                             # b23 "socho: the mosquito that takes lakhs of lives a year..."
    _pic(cr, "mosquito", W / 2, 1080, 680, t, -1)
    headline(cr, t, "IT TAKES", "LAKHS OF LIVES", t0, T(tl, "b23", "लाखों"), t_ghost=t0)


def e_saving(cr, t, tl, t0):                             # b23 "...may one day help make life-saving tissue"
    _pic(cr, "mosquito", 300, 1120, 380, t, -1)
    _pic(cr, "heart_engraving", 760, 1080, 0, t, t0 + 0.2, frame=(380, 400))
    path(cr, [(480, 1100), (560, 1090)], prog(t, t0 + 0.4, 0.4), 7, GREEN, 0.9, arrow=True)
    headline(cr, t, "AND ONE DAY,", "SAVE THEM?", t0, T(tl, "b23", "बचाने"), big_color=GREEN)


def e_question(cr, t, tl, t0):                           # b24 "would you take tissue made with a mosquito's mouth?"
    _pic(cr, "mosquito", 280, 1420, 260, t, t0)
    yes_no_card(cr, t, t0 + 0.4, 640, 980, w=640, h=300, question="COMMENT: YES OR NO")
    headline(cr, t, "WOULD YOU", "TAKE IT?", t0, T(tl, "b24", "लगवाओगे"), t_ghost=t0)


SHOTS = [   # (line, cue where the shot starts, draw function, background)
    ("b0", None, h_organs, "paper"), ("b0", "मच्छर", h_mosq, "paper"), ("b0", "क्या", h_what, "paper"),
    ("b1", None, h_mouth, "paper"), ("b1", "मुँह", h_nozzle, "paper"),
    ("b2", None, h_cells, "paper"), ("b2", "वो", h_dead, "paper"),
    ("b3", None, r_real, "paper"), ("b3", "कनाडा", r_unis, "paper"),
    ("b4", None, n_name, "paper"),
    ("b5", None, m_printer, "paper"), ("b5", "मेहंदी", m_cone, "paper"),
    ("b6", None, m_henna, "paper"), ("b6", "थ्री", m_layers, "paper"), ("b7", None, m_finer, "paper"),
    ("b8", None, o_dream, "paper"), ("b9", None, o_cells, "slate"), ("b10", None, o_glass, "paper"),
    ("b11", None, o_tested, "paper"), ("b12", None, o_tube, "paper"),
    ("b13", None, p_micron, "paper"), ("b13", "बाल", p_hair, "paper"), ("b14", None, p_needle, "paper"),
    ("b15", None, b_pull, "paper"), ("b15", "और", b_glue, "paper"),
    ("b16", None, b_prints, "paper"), ("b16", "चावल", b_rice, "paper"),
    ("b17", None, b_cells, "paper"), ("b18", None, b_86, "paper"),
    ("b19", None, q_organs, "paper"), ("b20", None, q_not_yet, "paper"),
    ("b21", None, l_pressure, "paper"), ("b21", "कुछ", l_days, "paper"), ("b22", None, l_good, "paper"),
    ("b23", None, e_taking, "paper"), ("b23", "वही", e_saving, "paper"),
    ("b24", None, e_question, "paper"),
]


def draw(cr, t, tl):
    draw_frame(cr, t, tl, SHOTS)


def sfx(tl):
    """A whoosh on every cut, thuds on stamps, a tick (and a music dip) before the re-hooks and the closing line."""
    ev = [(s, "whoosh", 0.25) for s in starts(tl, SHOTS)[1:]]
    ev += [(T(tl, "b0", "हाँ"), "thud", 0.0), (T(tl, "b2", "वो") + 0.3, "thud", 0.0), (T(tl, "b11", "जीत") + 0.3, "thud", 0.0),
           (T(tl, "b13", None) - 0.35, "tick", 0.0), (T(tl, "b19", None) - 0.35, "tick", 0.0),
           (T(tl, "b23", None) - 0.35, "tick", 0.0), (T(tl, "b24", "यस"), "typing", 1.0)]
    for bid in ("b4", "b8", "b12", "b16", "b18"):
        ev.append((tl[bid].start + 0.4, "pop", 0.0))
    ev += [(at, "dip", 0.5) for at, name, _ in list(ev) if name == "tick"]   # the bed dips just before a reveal
    return ev
