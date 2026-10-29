"""Video 2 (tech): "Speaker awaaz banata hi nahi" - how a moving-coil speaker works. Script approved by the owner
29 Oct 2026 ("Approve both"; scripts_batch2.md, video 2); narration below is that script word for word, in Devanagari
for the voice, with numbers written as words so the voice reads them right."""
import math
import os

from poster import (CORAL, CREAM, GOLD, INK, MARGIN, RED, W, calendar, card, clamp, counter, draw_text, drop, ease,
                    footnote, headline, magnifier, path, person, photo, prog, ring, stamp, text_size, yes_no_card)

# the narrator, music and tail are channel-wide; render_hi reads them from this module
from channel import ASSETS_ROOT, MUSIC, NARRATOR, NARRATOR_LABEL, REVEAL_GAP, TAIL, VOICE_REF  # noqa: F401
from shots import T, asset_finder, draw_frame, pic, starts

SCRIPT = [
    dict(id="b1", text="सोचो, तुम्हारे फ़ोन का स्पीकर आवाज़ बनाता ही नहीं... वो बस हवा को धक्का देता है। "
                       "एक सेकंड में हज़ारों बार।"),
    dict(id="b2", text="और ये काम करता है एक छोटा सा मैग्नेट, और तार का एक गोला। बस इतना ही।"),
    dict(id="b3", text="शादी में डीजे के पास खड़े हो, तो सीने में धक-धक महसूस होती है ना?"),
    dict(id="b4", text="वो आवाज़ नहीं... हवा का धक्का है, जो तुम्हें छू रहा है।", gap=REVEAL_GAP),
    dict(id="b5", text="इस स्पीकर का नाम है मूविंग-कॉइल स्पीकर। और ये आइडिया सौ साल पुराना है: उन्नीस सौ पच्चीस में "
                       "दो इंजीनियर्स, चेस्टर राइस और एडवर्ड केलॉग ने इसे बनाया था।"),
    dict(id="b6", text="अंदर तीन चीज़ें होती हैं: एक मैग्नेट, तार का एक कॉइल, और एक पतला सा कोन। "
                       "कई स्पीकर्स में ये कोन काग़ज़ का होता है।"),
    dict(id="b7", text="जब गाना बजता है, फ़ोन कॉइल में बिजली भेजता है। और बिजली वाला कॉइल ख़ुद एक मैग्नेट बन जाता है।"),
    dict(id="b8", text="अब दो मैग्नेट आमने-सामने। कभी खिंचते हैं, कभी धकेलते हैं। और कोन आगे-पीछे हिलने लगता है।"),
    dict(id="b9", text="कोन हवा को आगे धकेलता है, फिर पीछे खींचता है। और हवा में एक लहर बन जाती है।"),
    dict(id="b10", text="मुंबई लोकल सोचो। पीछे से एक धक्का लगता है, और वो धक्का आदमी से आदमी होते हुए आगे तक पहुँच जाता है।"),
    dict(id="b11", text="कोई ख़ुद आगे नहीं जाता। बस धक्का जाता है। हवा के साथ भी बिल्कुल यही होता है।"),
    dict(id="b12", text="ये धक्का एक सेकंड में लगभग तीन सौ तैंतालीस मीटर चलता है, और तुम्हारे कान के पर्दे तक पहुँचता है।"),
    dict(id="b13", text="पर्दा हिलता है... और दिमाग़ कहता है: आवाज़!", gap=REVEAL_GAP),
    dict(id="b14", text="और सबसे हैरानी की बात? गाने में ड्रम, गिटार और सिंगर, सब एक साथ बजते हैं... "
                        "और फ़ोन का एक ही छोटा सा कोन, एक ही वक़्त पे, ये सब बना देता है।"),
    dict(id="b15", text="धीमा बेस मतलब कोन सेकंड में बस तीस-चालीस बार हिलता है। सीटी जैसी पतली आवाज़ मतलब हज़ारों बार। "
                        "और हमारे कान बीस से बीस हज़ार बार तक का हिलना सुन लेते हैं।"),
    dict(id="b16", text="और तुम्हारे फ़ोन का स्पीकर? बस एक-डेढ़ सेंटीमीटर का। और उसका कोन आधे मिलीमीटर से भी कम हिलता है।"),
    dict(id="b17", text="तो फिर डीजे का बेस सीने तक क्यों पहुँचता है... और फ़ोन का बेस क्यों नहीं?"),
    dict(id="b18", text="क्योंकि बेस के लिए बहुत सारी हवा धकेलनी पड़ती है। बड़ा कोन, ज़्यादा हवा। "
                        "इसलिए डीजे के स्पीकर इतने बड़े होते हैं, और फ़ोन का बेस पतला लगता है।"),
    dict(id="b19", text="एक और अजीब बात। स्पीकर को उल्टा चलाओ, तो वो माइक्रोफ़ोन बन जाता है।"),
    dict(id="b20", text="आवाज़ कोन को हिलाती है, कॉइल मैग्नेट के पास हिलता है, और बिजली बन जाती है। "
                        "स्टेज पर सिंगर्स जो डायनेमिक माइक पकड़ते हैं, वो इसी तरह काम करता है।"),
    dict(id="b21", text="और स्मार्टवॉच? कुछ वॉचेस पानी में जाने के बाद अपने स्पीकर से एक ख़ास आवाज़ बजाती हैं... "
                        "और स्पीकर का धक्का अंदर का पानी बाहर फेंक देता है।", gap=REVEAL_GAP),
    dict(id="b22", text="सोचो, तुम्हारा पसंदीदा गाना... असल में बस एक मैग्नेट है, जो हवा को हज़ारों बार धक्का दे रहा है। "
                        "और तुम्हारा दिमाग़ उससे म्यूज़िक बना देता है।"),
    dict(id="b23", text="शादी में डीजे का बेस तुम्हें सीने में महसूस होता है? यस या नो, कमेंट में बताओ।"),
]

METADATA = dict(
    title="Speaker awaaz banata hi nahi",
    caption="Tumhare phone ka speaker awaaz nahi banata... wo hawa ko ek second mein hazaaron baar dhakka deta hai 😳\n\n"
            "Andar bas ek magnet, taar ka coil aur ek patla cone. Ye idea 1925 mein Chester Rice aur Edward Kellogg "
            "ne banaya tha.\n\n"
            "Shaadi ke DJ ka seene wala dhak-dhak? Wo awaaz nahi, hawa ka dhakka hai. Aur speaker ko ulta chalao toh "
            "wo microphone ban jaata hai.\n\n"
            "Shaadi mein DJ ka bass tumhe seene mein mehsoos hota hai? Comment mein YES ya NO likho 👇",
    yt_title="Speaker Awaaz Banata Hi Nahi? 😳 Kaise Kaam Karta Hai",
    yt_description="Phone ka speaker asal mein kaise kaam karta hai: magnet, coil aur cone se hawa ko dhakka, aur wo "
                   "dhakka tumhare kaan tak kaise pahunchta hai. DJ ka bass seene mein kyun lagta hai, phone ka bass "
                   "patla kyun hota hai, aur speaker ko ulta chalao toh wo microphone kaise ban jaata hai.",
    hashtags=["#speaker", "#howitworks", "#techinhindi", "#sciencefacts", "#factsinhindi"],
    pinned_comment="Shaadi mein DJ ka bass seene mein mehsoos hota hai? 🔊 YES ya NO? 👇",
    sources=["Rice & Kellogg 1925, the moving-coil loudspeaker, General Electric",
             "Apple Support, Use Water Lock on Apple Watch",
             "Knowles microspeaker datasheets; audioXpress, Characterizing the Microspeaker Industry",
             "IEC Electropedia, electroacoustic reciprocity"],
)

_find = asset_finder("speaker", "toxoplasma2")
P = {k: _find(k) for k in ("phone_speaker_grille", "phone_face_down", "magnet", "copper_coil", "speaker_driver",
                           "speaker_driver_side", "dj_speakers", "rice_kellogg_1925", "mumbai_local_crowd",
                           "ear_engraving", "drum", "acoustic_guitar", "stage_microphone", "whistle", "ruler",
                           "micro_speaker", "smartwatch", "water_drops", "earphones", "stopwatch",
                           "gray_anatomy_brain")}
P["phone_face_down"] = _find("smartphone_hand")          # no logo-free phone back exists; the phone in a hand
P["ear_engraving"] = _find("ear_engraving_gray907")      # the cross-section, eardrum labelled
P["magnet"] = _find("magnet_neodymium_discs")            # small magnets with a matchstick for scale
USED_ASSETS = [os.path.basename(v) for v in P.values() if v]
CREDITS_FILES = [os.path.join(ASSETS_ROOT, d, "credits.json") for d in ("speaker", "toxoplasma2")]

COPPER, STEEL, PAPER_CONE, BOLT = (0.78, 0.45, 0.20), (0.36, 0.37, 0.40), (0.92, 0.86, 0.72), (0.98, 0.80, 0.15)


def _pic(cr, key, cx, cy, h, t, t0, **kw):
    pic(cr, P.get(key), cx, cy, h, t, t0, **kw)


# ---------- drawing pieces for this video ----------

def air(cr, t, x0, y0, w, h, cols=16, rows=9, amp=18.0, freq=1.6, alpha=1.0, color=INK, start_x=None):
    """Air as rows of dots carrying a longitudinal wave (the recurring "dhakka" picture): each dot only swings
    back and forth around its own place while the bunching travels right. With start_x, only dots left of that
    x move yet (pass a growing start_x to show the push spreading out)."""
    dx, dy = w / (cols - 1), h / (rows - 1)
    for j in range(rows):
        for i in range(cols):
            bx = x0 + i * dx
            phase = 2 * math.pi * (freq * t - i / 5.0)
            reach = 1.0 if start_x is None else clamp((start_x - bx) / 120 + 1)
            x = bx + amp * reach * math.sin(phase)
            cr.set_source_rgba(*color, 0.8 * alpha)
            cr.arc(x, y0 + j * dy, 7, 0, 2 * math.pi)
            cr.fill()


def wave_line(cr, x0, y, w, amp, cycles, phase=0.0, color=INK, width=6, alpha=1.0, p=1.0):
    n = 160
    cr.set_source_rgba(*color, alpha)
    cr.set_line_width(width)
    for i in range(int(n * clamp(p)) + 1):
        f = i / n
        yy = y + amp * math.sin(2 * math.pi * cycles * f + phase)
        (cr.move_to if i == 0 else cr.line_to)(x0 + w * f, yy)
    cr.stroke()


def section(cr, cx, cy, s=1.0, d=0.0, alpha=1.0, glow=0.0, labels=None):
    """Side cut-away of a moving-coil speaker facing right: magnet block + pole, copper coil and paper cone, which
    move together by d px. labels: {"magnet": p, "coil": p, "cone": p} -> leader labels fading in."""
    cr.save()
    cr.translate(cx, cy)
    cr.scale(s, s)
    cr.set_source_rgba(*STEEL, alpha)                                 # magnet block + centre pole
    cr.rectangle(-270, -130, 140, 260)
    cr.fill()
    cr.rectangle(-130, -32, 90, 64)
    cr.fill()
    cr.set_source_rgba(*STEEL, 0.6 * alpha)                           # basket
    cr.set_line_width(6)
    for sgn in (-1, 1):
        cr.move_to(-130, sgn * 130)
        cr.line_to(190, sgn * 250)
        cr.stroke()
    cone = [(-60 + d, -48), (170 + d, -235), (170 + d, 235), (-60 + d, 48)]
    cr.move_to(*cone[0])
    for q in cone[1:]:
        cr.line_to(*q)
    cr.close_path()
    cr.set_source_rgba(*PAPER_CONE, alpha)
    cr.fill_preserve()
    cr.set_source_rgba(*INK, 0.9 * alpha)
    cr.set_line_width(5)
    cr.stroke()
    for sgn in (-1, 1):                                               # rubber surround at the rim
        cr.arc(180 + d / 2, sgn * 242, 14, 0, 2 * math.pi)
        cr.stroke()
    for sgn in (-1, 1):                                               # coil windings round the pole
        cr.set_source_rgba(*(BOLT if glow > 0.5 else COPPER), alpha)
        cr.rectangle(-110 + d, sgn * 36 - 10, 70, 20)
        cr.fill()
    cr.restore()
    if labels:
        for key, (lx, ly, tx, ty) in {"magnet": (-200, -140, -330, -330), "coil": (-75, -50, 40, -400),
                                      "cone": (100, 150, 250, 330)}.items():
            p = labels.get(key, 0)
            if p > 0:
                path(cr, [(cx + lx * s, cy + ly * s), (cx + tx * s, cy + ty * s)], p, 4, RED, 0.9)
                draw_text(cr, key.upper(), cx + tx * s, cy + ty * s, 52, RED, p,
                          anchor="cb" if ty < 0 else "ct")


def magnets(cr, t, cx, cy, t0, alpha=1.0):
    """The coil-magnet (left, copper) facing the fixed magnet (right, steel); every half second they swap between
    pulling together and pushing apart, and the copper one moves."""
    k = int(max(0.0, t - t0) / 0.55) % 2                             # 0 pull, 1 push
    off = (1 if k else -1) * 40 * ease(((t - t0) % 0.55) / 0.25)
    for x, col, poles in ((cx - 230 + off, COPPER, ("S", "N") if k else ("N", "S")), (cx + 230, STEEL, ("N", "S"))):
        cr.set_source_rgba(*col, alpha)
        cr.rectangle(x - 150, cy - 90, 300, 180)
        cr.fill()
        draw_text(cr, poles[0], x - 80, cy, 90, CREAM, alpha, anchor="cm")
        draw_text(cr, poles[1], x + 80, cy, 90, CREAM, alpha, anchor="cm")
    for sgn in (-1, 1):                                               # arrows point in (pull) or out (push)
        y = cy + sgn * 140
        for side in (-1, 1):
            outer, inner = (cx + side * 130, y), (cx + side * 40, y)
            path(cr, [outer, inner] if k == 0 else [inner, outer], 1, 7, RED, 0.9 * alpha, arrow=True)
    return "PULL" if k == 0 else "PUSH"


def bolt(cr, pts, p, alpha=1.0):
    """Electricity running along a wire: a jagged yellow spark travelling along the polyline."""
    path(cr, pts, 1.0, 8, INK, 0.7 * alpha)
    if p <= 0:
        return
    n = len(pts) - 1
    seg = min(n - 1, int(p * n))
    f = p * n - seg
    x = pts[seg][0] + (pts[seg + 1][0] - pts[seg][0]) * f
    y = pts[seg][1] + (pts[seg + 1][1] - pts[seg][1]) * f
    zig = [(x - 40, y - 30), (x - 5, y - 8), (x - 25, y + 2), (x + 30, y + 30), (x + 5, y + 6), (x + 22, y - 2)]
    cr.move_to(*zig[0])
    for q in zig[1:]:
        cr.line_to(*q)
    cr.close_path()
    cr.set_source_rgba(*BOLT, alpha)
    cr.fill()


def note(cr, x, y, s, alpha=1.0, color=INK):
    """A music quaver: tilted oval head, stem and flag."""
    cr.save()
    cr.translate(x, y)
    cr.rotate(-0.35)
    cr.scale(1, 0.72)
    cr.arc(0, 0, 22 * s, 0, 2 * math.pi)
    cr.restore()
    cr.set_source_rgba(*color, alpha)
    cr.fill()
    cr.set_line_width(6 * s)
    cr.move_to(x + 19 * s, y - 6 * s)
    cr.line_to(x + 19 * s, y - 95 * s)
    cr.curve_to(x + 45 * s, y - 75 * s, x + 50 * s, y - 55 * s, x + 40 * s, y - 35 * s)
    cr.stroke()


def chest(cr, t, x, y, t0, reach=1.0, alpha=1.0):
    """A person (side figure) with bass rings travelling into the chest from the left."""
    person(cr, x, y, 620, INK, 0.9 * alpha)
    for i in range(4):
        f = ((t - t0) * 1.4 + i / 4) % 1.0
        r = 40 + 260 * f
        cr.set_source_rgba(*RED, 0.7 * (1 - f) * alpha * reach)
        cr.set_line_width(8)
        cr.arc(x - 330 + 300 * f * reach, y - 400, r * 0.5, -0.9, 0.9)
        cr.stroke()


# ---------- shots ----------
# Rules (style bible + parasite-reels study): a new picture every ~3 s cut on the word, the literal noun on screen,
# one recurring picture (air dots getting a dhakka), red = the key word, dark slate for "inside" (the air, the ear).

def h_no_sound(cr, t, tl, t0):                           # b1 "socho, your phone's speaker makes no sound..."
    _pic(cr, "phone_face_down", 440, 1000, 780, t, -1, rot=-0.04)

    def grille(c):                                             # the phone's speaker holes, zoomed
        if P["phone_speaker_grille"]:
            photo(c, P["phone_speaker_grille"], 700, 1390, 130, shadow=False)
    magnifier(cr, t, -1, 760, 1390, 200, grille)
    ring(cr, 760, 1390, 230, 230, prog(t, 0.9, 0.5))
    headline(cr, t, "YOUR SPEAKER MAKES", "NO SOUND", -1, min(1.2, T(tl, "b1", "नहीं")), t_ghost=-1)


def h_pushes_air(cr, t, tl, t0):                         # b1 "...it just pushes air"
    _pic(cr, "phone_face_down", 330, 1080, 560, t, -1, rot=-0.06)
    air(cr, t, 560, 860, 440, 440, cols=8, rows=8, amp=14, freq=2.2, start_x=560 + 600 * prog(t, t0, 1.2))
    headline(cr, t, "IT PUSHES", "AIR", t0, t0 + 0.4)


def h_thousands(cr, t, tl, t0):                          # b1 "...a thousand times a second"
    _pic(cr, "stopwatch", 300, 1050, 420, t, t0)
    counter(cr, t, t0 + 0.3, 720, 980, "1000s", 170, color=GOLD)
    draw_text(cr, "PUSHES / SECOND", 720, 1110, 46, INK, prog(t, t0 + 0.5, 0.3), anchor="ct")
    headline(cr, t, "IN ONE SECOND:", "THOUSANDS", t0, t0 + 0.3)


def h_magnet_wire(cr, t, tl, t0):                        # b2 "a small magnet and a coil of wire. That's it."
    tw = T(tl, "b2", "तार")
    _pic(cr, "magnet", 320, drop(t, t0 + 0.2, 1080), 360, t, t0 + 0.2)          # on screen from the cut
    _pic(cr, "copper_coil", 760, drop(t, tw - 0.2, 1080), 380, t, tw - 0.2)
    draw_text(cr, "+", W / 2, 1080, 120, RED, prog(t, tw - 0.1, 0.2), anchor="cm")
    stamp(cr, t, "THAT'S IT", T(tl, "b2", "इतना"), W / 2, 1420, 70)
    headline(cr, t, "JUST A MAGNET +", "A WIRE", t0, tw)


def h_dj(cr, t, tl, t0):                                 # b3 "near the DJ at a shaadi, the dhak-dhak in your chest?"
    _pic(cr, "dj_speakers", 280, 1080, 820, t, t0)
    chest(cr, t, 760, 1460, t0, reach=prog(t, T(tl, "b3", "सीने"), 0.6))
    headline(cr, t, "THAT THUMP IN YOUR", "CHEST?", t0, T(tl, "b3", "सीने"), t_ghost=t0)


def h_air_touch(cr, t, tl, t0):                          # b4 "that's not sound... it's air pushing you"
    _pic(cr, "dj_speakers", 230, 1080, 720, t, -1)
    air(cr, t, 400, 820, 260, 520, cols=5, rows=9, amp=16, freq=1.8)
    chest(cr, t, 820, 1460, t0)
    stamp(cr, t, "AIR", T(tl, "b4", "छू"), 820, 860, 90)
    headline(cr, t, "NOT SOUND:", "PUSHED AIR", t0, T(tl, "b4", "हवा"))


def n_name(cr, t, tl, t0):                               # b5 "its name: the moving-coil speaker"
    _pic(cr, "speaker_driver", W / 2, 960, 460, t, t0)
    tn = T(tl, "b5", "मूविंग")
    for i, (txt, ty) in enumerate((("MOVING-COIL", 1330), ("SPEAKER", 1450))):
        p = prog(t, tn + 0.3 * i, 0.3)
        if p > 0:
            tw_, th = text_size(txt, 96)
            cr.set_source_rgba(*RED, 0.92)
            cr.rectangle(MARGIN, ty - 12, (tw_ + 50) * p, th + 24)
            cr.fill()
            draw_text(cr, txt, MARGIN + 25, ty, 96, CREAM, clamp(p * 2 - 1))
    headline(cr, t, "ITS NAME", "", t0, 1e9)


def n_1925(cr, t, tl, t0):                               # b5 "...a hundred years old: 1925, Chester Rice and Edward Kellogg"
    calendar(cr, t, t0 + 0.1, 280, 900, ["2025", "1990", "1950", "1925"], "YEAR", interval=0.3, w=300, h=320)
    _pic(cr, "rice_kellogg_1925", 690, 1180, 0, t, T(tl, "b5", "चेस्टर") - 0.3, rot=0.03, frame=(560, 440))
    footnote(cr, "Chester Rice & Edward Kellogg, General Electric, 1925", prog(t, T(tl, "b5", "चेस्टर"), 0.4),
             y=1470)
    headline(cr, t, "100 YEARS OLD:", "1925", t0, T(tl, "b5", "उन्नीस"))


def p_parts(cr, t, tl, t0):                              # b6 "inside: a magnet, a coil of wire, a thin cone"
    lab = {"magnet": prog(t, T(tl, "b6", "मैग्नेट"), 0.4), "coil": prog(t, T(tl, "b6", "कॉइल"), 0.4),
           "cone": prog(t, T(tl, "b6", "कोन"), 0.4)}
    section(cr, 560, 1060, 1.25, alpha=prog(t, t0, 0.3), labels=lab)
    headline(cr, t, "INSIDE:", "3 PARTS", t0, t0 + 0.4)


def p_paper(cr, t, tl, t0):                              # b6 "...in many speakers the cone is paper"
    _pic(cr, "speaker_driver", 400, 1060, 460, t, t0)

    def inner(c):                                             # paper fibres of a (black-dyed) paper cone, zoomed
        c.set_source_rgba(0.13, 0.12, 0.11, 1)
        c.paint()
        c.set_source_rgba(0.42, 0.40, 0.37, 0.8)
        c.set_line_width(2)
        for i in range(90):
            x, y = 600 + (i * 53) % 400, 800 + (i * 97) % 400
            c.move_to(x, y)
            c.curve_to(x + 20, y + 8, x + 40, y - 6, x + 60 + i % 30, y + 4)
        c.stroke()
    magnifier(cr, t, t0 + 0.3, 800, 1000, 200, inner)
    stamp(cr, t, "PAPER", T(tl, "b6", "काग़ज़"), 800, 1290, 80)
    headline(cr, t, "THE CONE IS OFTEN", "PAPER", t0, T(tl, "b6", "काग़ज़"))


def e_current(cr, t, tl, t0):                            # b7 "when a song plays, the phone sends electricity into the coil"
    section(cr, 640, 1080, 1.1)
    bolt(cr, [(60, 1500), (300, 1500), (420, 1180), (530, 1120)], prog(t, T(tl, "b7", "बिजली") - 0.2, 1.2))
    _pic(cr, "phone_face_down", 160, 1380, 300, t, t0, rot=0.1)
    headline(cr, t, "THE SONG BECOMES", "ELECTRICITY", t0, T(tl, "b7", "बिजली"))


def e_coil_magnet(cr, t, tl, t0):                        # b7 "...and the coil itself becomes a magnet"
    g = prog(t, T(tl, "b7", "मैग्नेट") - 0.2, 0.3)
    section(cr, 640, 1080, 1.1, glow=g)
    for txt, dx in (("N", -60), ("S", 60)):
        draw_text(cr, txt, 640 - 95 + dx, 900, 80, RED, g, anchor="cm")
    headline(cr, t, "THE COIL BECOMES A", "MAGNET", t0, T(tl, "b7", "मैग्नेट"))


def e_pull_push(cr, t, tl, t0):                          # b8 "two magnets face to face: pull, push"
    word = magnets(cr, t, W / 2, 1060, t0, prog(t, t0, 0.3))
    draw_text(cr, word, W / 2, 1300, 110, RED, prog(t, t0 + 0.2, 0.2), anchor="ct")
    headline(cr, t, "PULL, PUSH,", "PULL, PUSH", t0, T(tl, "b8", "धकेलते"))


def e_cone_moves(cr, t, tl, t0):                         # b8 "...and the cone moves back and forth"
    d = 26 * math.sin((t - t0) * 2 * math.pi * 2.2)
    section(cr, 560, 1080, 1.25, d=d)
    path(cr, [(820, 760), (930, 760)], 1, 7, RED, 0.9, arrow=True)
    path(cr, [(930, 1400), (820, 1400)], 1, 7, RED, 0.9, arrow=True)
    headline(cr, t, "THE CONE", "MOVES", t0, T(tl, "b8", "कोन"))


def w_wave(cr, t, tl, t0):                               # b9 "the cone pushes the air... a wave forms" (inside the air = slate)
    d = 22 * math.sin((t - t0) * 2 * math.pi * 1.6)
    section(cr, 220, 1080, 0.75, d=d)
    air(cr, t, 420, 820, 560, 520, cols=12, rows=9, amp=20, freq=1.6, color=CREAM,
        start_x=420 + 700 * prog(t, t0, 1.5))
    headline(cr, t, "A WAVE IN THE", "AIR", t0, T(tl, "b9", "लहर"), small_color=CREAM, big_color=CORAL)


def w_local(cr, t, tl, t0):                              # b10 "think of a Mumbai local: a push passes person to person"
    _pic(cr, "mumbai_local_crowd", W / 2, 1050, 0, t, t0, rot=-0.02, frame=(900, 640))
    p = prog(t, T(tl, "b10", "आदमी"), 1.4)
    path(cr, [(150, 760), (350, 720), (550, 760), (750, 720), (950, 760)], p, 9, RED, 0.95, arrow=True)
    headline(cr, t, "THE PUSH", "TRAVELS", t0, T(tl, "b10", "आदमी"))


def w_people(cr, t, tl, t0):                             # b11 "nobody moves forward; only the push travels"
    k = int(((t - t0) * 3.0) % 7)
    for i in range(7):
        lean = 0.12 if i == k else 0.0
        cr.save()
        cr.translate(150 + 130 * i, 1450)
        cr.rotate(lean)
        person(cr, 0, 0, 480, RED if i == k else INK, 0.9)
        cr.restore()
    headline(cr, t, "NOBODY MOVES.", "ONLY THE PUSH", t0, T(tl, "b11", "बस"))


def w_same_air(cr, t, tl, t0):                           # b11 "...the same happens with air" (slate)
    air(cr, t, 120, 800, 840, 600, cols=14, rows=10, amp=22, freq=1.4, color=CREAM)
    headline(cr, t, "AIR DOES", "THE SAME", t0, t0 + 0.3, small_color=CREAM, big_color=CORAL)


def w_343(cr, t, tl, t0):                                # b12 "this push travels 343 metres a second"
    _pic(cr, "stopwatch", 310, 1080, 460, t, t0)
    counter(cr, t, T(tl, "b12", "तीन"), 740, 1000, "343 M", 150, color=GOLD)
    draw_text(cr, "EVERY SECOND", 740, 1120, 46, INK, prog(t, T(tl, "b12", "तीन") + 0.3, 0.3), anchor="ct")
    headline(cr, t, "IT TRAVELS", "343 M/S", t0, T(tl, "b12", "तीन"))


def w_ear(cr, t, tl, t0):                                # b12 "...and reaches your eardrum"
    _pic(cr, "ear_engraving", W / 2, 1050, 0, t, t0 - 0.1, rot=-0.02, frame=(860, 700))
    ring(cr, 560, 1110, 80, 110, prog(t, T(tl, "b12", "कान") + 0.3, 0.5))      # the eardrum on Gray 907
    footnote(cr, "engraving: Gray's Anatomy (1918), public domain", prog(t, t0, 0.4), y=1470)
    headline(cr, t, "TO YOUR", "EARDRUM", t0, T(tl, "b12", "कान"))


def w_brain(cr, t, tl, t0):                              # b13 "the eardrum moves... and the brain says: sound!"
    _pic(cr, "gray_anatomy_brain", W / 2, 1050, 0, t, T(tl, "b13", "दिमाग़") - 0.2, rot=0.02, frame=(820, 560))
    wobble = 12 * math.sin((t - t0) * 30) * (1 - prog(t, T(tl, "b13", "दिमाग़"), 0.3))
    ring(cr, W / 2 + wobble, 820, 120, 60, prog(t, t0, 0.3))
    stamp(cr, t, "SOUND!", T(tl, "b13", "आवाज़"), W / 2, 1440, 90)
    headline(cr, t, "THE BRAIN SAYS:", "SOUND!", t0, T(tl, "b13", "आवाज़"))


def m_band(cr, t, tl, t0):                               # b14 "and the strangest part? drums, guitar, singer, all at once..."
    _pic(cr, "phone_face_down", W / 2, 1450, 300, t, t0, rot=-0.05)     # the phone that will play all of them
    for key, x, cue in (("drum", 220, "ड्रम"), ("acoustic_guitar", 540, "गिटार"), ("stage_microphone", 860, "सिंगर")):
        _pic(cr, key, x, 1060, 380, t, T(tl, "b14", cue) - 0.2)
    headline(cr, t, "THE STRANGEST", "PART", t0, t0 + 0.5, t_ghost=t0)


def m_one_cone(cr, t, tl, t0):                           # b14 "...one tiny cone makes all of it at the same moment"
    p = prog(t, t0, 1.0)
    for i, (col, amp, cyc) in enumerate(((INK, 40, 2), (RED, 25, 5), (GOLD, 15, 11))):
        wave_line(cr, 80, 760 + 140 * i, 420, amp, cyc, (t - t0) * 6, col, 6, 0.9, p)
    q = prog(t, T(tl, "b14", "बना") - 0.6, 0.8)
    cr.set_source_rgba(*INK, q)
    cr.set_line_width(6)
    for i in range(161):                                       # the three added together = one wiggly line
        f = i / 160
        ph = (t - t0) * 6
        yy = 900 + 40 * math.sin(2 * math.pi * 2 * f + ph) + 25 * math.sin(2 * math.pi * 5 * f + ph) \
            + 15 * math.sin(2 * math.pi * 11 * f + ph)
        (cr.move_to if i == 0 else cr.line_to)(520 + 260 * f, yy)
    cr.stroke()
    section(cr, 880, 900, 0.55, d=8 * math.sin((t - t0) * 40) * q, alpha=prog(t, t0, 0.3))
    headline(cr, t, "ONE CONE.", "EVERYTHING.", t0, T(tl, "b14", "बना"))


def m_bass(cr, t, tl, t0):                               # b15 "deep bass: the cone moves only 30-40 times a second"
    wave_line(cr, 100, 1000, 880, 120, 2, (t - t0) * 3, INK, 9)
    counter(cr, t, T(tl, "b15", "तीस"), W / 2, 1260, "30-40", 130, color=GOLD)
    draw_text(cr, "PER SECOND", W / 2, 1390, 50, INK, prog(t, T(tl, "b15", "तीस") + 0.3, 0.3), anchor="ct")
    headline(cr, t, "DEEP BASS:", "SLOW", t0, T(tl, "b15", "तीस"))


def m_whistle(cr, t, tl, t0):                            # b15 "...a thin whistle: thousands of times"
    _pic(cr, "whistle", 240, 1480, 220, t, t0, rot=0.1)
    wave_line(cr, 100, 960, 880, 60, 24, (t - t0) * 30, RED, 5)
    counter(cr, t, t0 + 0.3, 700, 1240, "1000s", 130, color=GOLD)
    draw_text(cr, "PER SECOND", 700, 1370, 50, INK, prog(t, t0 + 0.6, 0.3), anchor="ct")
    headline(cr, t, "A WHISTLE:", "FAST", t0, t0 + 0.3)


def m_range(cr, t, tl, t0):                              # b15 "...and our ears hear from 20 to 20,000"
    _pic(cr, "ear_engraving", 250, 1050, 0, t, t0, rot=-0.03, frame=(360, 300))
    x0, x1, y = 120, 960, 1350
    p = prog(t, T(tl, "b15", "बीस"), 1.0)
    cr.set_source_rgba(*INK, 0.9)
    cr.set_line_width(6)
    cr.move_to(x0, y)
    cr.line_to(x0 + (x1 - x0) * p, y)
    cr.stroke()
    for f, lab in ((0.0, "20"), (0.33, "200"), (0.66, "2,000"), (1.0, "20,000")):
        if p >= f:
            draw_text(cr, lab, x0 + (x1 - x0) * f, y + 30, 46, RED if f in (0.0, 1.0) else INK, 1.0,
                      anchor="rt" if f == 1.0 else "ct")
    headline(cr, t, "YOUR EARS HEAR", "20 TO 20,000", t0, T(tl, "b15", "बीस"))


def s_tiny(cr, t, tl, t0):                               # b16 "your phone's speaker? just 1-1.5 cm"
    _pic(cr, "phone_speaker_grille", W / 2, 720, 150, t, t0)
    _pic(cr, "ruler", W / 2, 1360, 300, t, t0)
    p = prog(t, t0 + 0.3, 0.3)                                    # the micro-speaker inside: about 11 x 15 mm
    cr.set_source_rgba(0.12, 0.12, 0.13, p)
    cr.rectangle(W / 2 - 75, 960, 150, 110)
    cr.fill()
    cr.set_source_rgba(0.35, 0.35, 0.38, p)
    cr.rectangle(W / 2 - 55, 980, 110, 70)
    cr.fill()
    path(cr, [(W / 2 - 75, 1110), (W / 2 + 75, 1110)], prog(t, t0 + 0.6, 0.3), 5, RED, 0.9)
    draw_text(cr, "~1.5 CM", W / 2, 1125, 48, RED, prog(t, t0 + 0.7, 0.3), anchor="ct")
    headline(cr, t, "YOUR PHONE'S SPEAKER:", "1.5 CM", t0, T(tl, "b16", "सेंटीमीटर"))


def s_half_mm(cr, t, tl, t0):                            # b16 "...its cone moves less than half a millimetre"
    _pic(cr, "ruler", W / 2, 1180, 260, t, -1)

    def inner(c):
        c.set_source_rgba(*INK, 1)
        for i in range(9):
            x = 380 + 40 * i
            c.rectangle(x, 1000, 4, 60 if i % 5 == 0 else 35)
            c.fill()
        c.set_source_rgba(*RED, 0.9)
        c.rectangle(560 + 6 * math.sin((t - t0) * 20), 940, 20, 140)
        c.fill()
    magnifier(cr, t, t0 + 0.2, 560, 1020, 220, inner)
    headline(cr, t, "IT MOVES LESS THAN", "HALF A MM", t0, T(tl, "b16", "आधे"))


def r_why(cr, t, tl, t0):                                # b17 re-hook: "so why does DJ bass reach your chest, and the phone's doesn't?"
    _pic(cr, "dj_speakers", 270, 1100, 760, t, t0)
    _pic(cr, "phone_face_down", 760, 1250, 300, t, t0 + 0.2, rot=0.08)
    q = prog(t, T(tl, "b17", "फ़ोन"), 0.3)
    draw_text(cr, "?", 790, 900, 320 * (0.8 + 0.2 * q), RED, q, anchor="cm")
    headline(cr, t, "WHY NOT", "YOUR PHONE?", t0, T(tl, "b17", "फ़ोन"), t_ghost=t0)


def r_big_cone(cr, t, tl, t0):                           # b18 "bass needs lots of air: big cone, more air"
    section(cr, 230, 900, 0.85, d=20 * math.sin((t - t0) * 9))
    air(cr, t, 420, 720, 520, 360, cols=10, rows=8, amp=24, freq=1.4)
    section(cr, 230, 1390, 0.28, d=3 * math.sin((t - t0) * 9), alpha=prog(t, T(tl, "b18", "बड़ा"), 0.3))
    air(cr, t, 330, 1360, 160, 60, cols=4, rows=2, amp=5, freq=1.4, alpha=prog(t, T(tl, "b18", "बड़ा"), 0.3))
    headline(cr, t, "BIG BASS =", "BIG CONE", t0, T(tl, "b18", "बड़ा"))


def r_thats_why(cr, t, tl, t0):                          # b18 "...that's why DJ speakers are huge, and phone bass is thin"
    _pic(cr, "dj_speakers", 400, 1100, 720, t, t0)
    _pic(cr, "phone_face_down", 820, 1360, 230, t, t0 + 0.2, rot=0.08)
    stamp(cr, t, "THIN BASS", T(tl, "b18", "पतला"), 820, 1120, 54)
    headline(cr, t, "THAT'S WHY DJ SPEAKERS", "ARE HUGE", t0, t0 + 0.4)


def x_reverse(cr, t, tl, t0):                            # b19 "run a speaker backwards and it becomes a microphone"
    section(cr, 560, 1060, 1.1)
    for y in (760, 1360):
        path(cr, [(980, y), (760, y)], prog(t, T(tl, "b19", "उल्टा"), 0.5), 8, RED, 0.9, arrow=True)
    _pic(cr, "earphones", 860, 1500, 260, t, T(tl, "b19", "माइक्रोफ़ोन"))
    headline(cr, t, "RUN IT BACKWARDS:", "MICROPHONE", t0, T(tl, "b19", "माइक्रोफ़ोन"))


def x_flow(cr, t, tl, t0):                               # b20 "sound moves the cone, the coil moves near the magnet: electricity"
    steps = [("SOUND", "कोन"), ("CONE", "कोन"), ("COIL", "कॉइल"), ("ELECTRICITY", "बिजली")]
    for i, (lab, cue) in enumerate(steps):
        tc = T(tl, "b20", cue) + (0.0 if i != 1 else 0.4)
        y = 700 + 200 * i
        card(cr, t, tc - 0.3, 300, y, [lab], size=56)
        if i:
            path(cr, [(400, y - 90), (400, y - 20)], prog(t, tc - 0.3, 0.3), 7, RED, 0.9, arrow=True)
    bolt(cr, [(700, 1360), (950, 1360)], prog(t, T(tl, "b20", "बिजली"), 0.8))
    headline(cr, t, "SOUND IN,", "ELECTRICITY OUT", t0, T(tl, "b20", "बिजली"), big_size=130)


def x_stage(cr, t, tl, t0):                              # b20 "...the dynamic mic singers hold works this way"
    _pic(cr, "stage_microphone", 420, 1080, 760, t, t0, rot=-0.2)
    section(cr, 820, 900, 0.3, alpha=prog(t, t0 + 0.3, 0.3))
    path(cr, [(560, 820), (740, 880)], prog(t, t0 + 0.4, 0.3), 5, RED, 0.9, arrow=True)
    stamp(cr, t, "SAME IDEA", t0 + 0.8, 760, 720, 64)
    headline(cr, t, "A STAGE MIC:", "SAME IDEA", t0, t0 + 0.6)


def x_watch(cr, t, tl, t0):                              # b21 "some smartwatches play a special sound after water..."
    _pic(cr, "smartwatch", W / 2, 1100, 640, t, t0)
    _pic(cr, "water_drops", W / 2 + 140, 1080, 200, t, T(tl, "b21", "पानी") - 0.2)
    headline(cr, t, "A WATCH IN", "WATER", t0, T(tl, "b21", "पानी"))


def x_eject(cr, t, tl, t0):                              # b21 "...the speaker's push throws the water out"
    _pic(cr, "smartwatch", 420, 1100, 600, t, -1)
    for i in range(8):                                        # drops fly out in pulses
        f = ((t - t0) * 1.6 + i / 8) % 1.0
        x, y = 600 + 420 * f, 1100 - 120 * math.sin(i * 1.3) * f
        cr.set_source_rgba(0.35, 0.62, 0.85, 0.9 * (1 - f))
        cr.arc(x, y, 16 - 8 * f, 0, 2 * math.pi)
        cr.fill()
    headline(cr, t, "SOUND THAT", "PUSHES WATER OUT", t0, T(tl, "b21", "धक्का"), big_size=130)


def e_bookend(cr, t, tl, t0):                            # b22 "socho: your favourite song is just a magnet pushing air"
    _pic(cr, "phone_face_down", 330, 1080, 560, t, -1, rot=-0.06)
    air(cr, t, 560, 860, 440, 440, cols=8, rows=8, amp=14, freq=2.2)
    headline(cr, t, "YOUR FAVOURITE SONG:", "PUSHED AIR", t0, T(tl, "b22", "मैग्नेट"), t_ghost=t0)


def e_music(cr, t, tl, t0):                              # b22 "...and your brain turns it into music"
    _pic(cr, "gray_anatomy_brain", W / 2, 1100, 0, t, t0, rot=0.02, frame=(700, 480))
    for i in range(5):
        q = prog(t, T(tl, "b22", "म्यूज़िक") - 0.4 + 0.12 * i, 0.3)
        note(cr, 200 + 170 * i, 760 - 60 * math.sin(i + (t - t0) * 2), 1.2, q, RED if i % 2 else INK)
    headline(cr, t, "YOUR BRAIN MAKES IT", "MUSIC", t0, T(tl, "b22", "म्यूज़िक"))


def e_question(cr, t, tl, t0):                           # b23 "DJ bass in your chest at a shaadi? YES or NO"
    _pic(cr, "dj_speakers", 230, 1350, 560, t, t0, rot=-0.03)
    yes_no_card(cr, t, t0 + 0.4, 650, 980, w=640, h=300, question="COMMENT: YES OR NO")
    headline(cr, t, "DJ BASS IN", "YOUR CHEST?", t0, T(tl, "b23", "सीने"), t_ghost=t0)


SHOTS = [   # (line, cue where the shot starts, draw function, background)
    ("b1", None, h_no_sound, "paper"), ("b1", "हवा", h_pushes_air, "paper"), ("b1", "सेकंड", h_thousands, "paper"),
    ("b2", None, h_magnet_wire, "paper"),
    ("b3", None, h_dj, "paper"), ("b4", None, h_air_touch, "paper"),
    ("b5", None, n_name, "paper"), ("b5", "उन्नीस", n_1925, "paper"),
    ("b6", None, p_parts, "paper"), ("b6", "कई", p_paper, "paper"),
    ("b7", None, e_current, "paper"), ("b7", "वाला", e_coil_magnet, "paper"),
    ("b8", None, e_pull_push, "paper"), ("b8", "कोन", e_cone_moves, "paper"),
    ("b9", None, w_wave, "slate"),
    ("b10", None, w_local, "paper"), ("b11", None, w_people, "paper"), ("b11", "हवा", w_same_air, "slate"),
    ("b12", None, w_343, "paper"), ("b12", "कान", w_ear, "paper"), ("b13", None, w_brain, "paper"),
    ("b14", None, m_band, "paper"), ("b14", "फ़ोन", m_one_cone, "paper"),
    ("b15", None, m_bass, "paper"), ("b15", "सीटी", m_whistle, "paper"), ("b15", "हमारे", m_range, "paper"),
    ("b16", None, s_tiny, "paper"), ("b16", "कोन", s_half_mm, "paper"),
    ("b17", None, r_why, "paper"),
    ("b18", None, r_big_cone, "paper"), ("b18", "इसलिए", r_thats_why, "paper"),
    ("b19", None, x_reverse, "paper"), ("b20", None, x_flow, "paper"), ("b20", "स्टेज", x_stage, "paper"),
    ("b21", None, x_watch, "paper"), ("b21", "धक्का", x_eject, "paper"),
    ("b22", None, e_bookend, "paper"), ("b22", "दिमाग़", e_music, "paper"),
    ("b23", None, e_question, "paper"),
]


def draw(cr, t, tl):
    draw_frame(cr, t, tl, SHOTS)


def sfx(tl):
    """A whoosh on every cut, thuds on stamps, a tick before the re-hook and the closing line, typing on the card."""
    ev = [(s, "whoosh", 0.25) for s in starts(tl, SHOTS)[1:]]
    ev += [(T(tl, "b2", "इतना"), "thud", 0.0), (T(tl, "b4", "छू"), "thud", 0.0), (T(tl, "b13", "आवाज़"), "thud", 0.0),
           (T(tl, "b14", None) - 0.35, "tick", 0.0), (T(tl, "b17", None) - 0.35, "tick", 0.0),
           (T(tl, "b22", None) - 0.35, "tick", 0.0), (T(tl, "b23", "यस"), "typing", 1.0)]
    for bid in ("b5", "b6", "b12", "b16", "b20"):
        ev.append((tl[bid].start + 0.4, "pop", 0.0))
    ev += [(at, "dip", 0.5) for at, name, _ in list(ev) if name == "tick"]   # the bed dips just before a reveal
    return ev
