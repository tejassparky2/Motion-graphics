"""Batch 1, video 1: "Ye parasite chuhe ka darr mita deta hai" (Toxoplasma gondii). Script approved by the owner
29 Oct 2026 (scripts_batch1.md #1); narration below is that script word for word, in Devanagari for the voice."""
import math
import os

from poster import (INK, MARGIN, RED, FADED, W, H, blob, card, clamp, counter, cross, draw_text, ease, framed_photo,
                    head_profile, header, headline, paper, path, person, phone_comments, photo, prog, push, ring,
                    stamp, strike, tick, window)

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
ASSETS = os.path.join(os.path.dirname(REPO), "hinglish_assets", "toxoplasma")   # outside the public repo
A = {k: os.path.join(ASSETS, v) for k, v in {
    "rat": "rat_1.png", "cat": "cat_1.png", "cat_indoor": "cat_indoor_1.png", "micro": "toxo_micro_2.jpg",
    "cyst": "toxo_micro_1.jpg", "meat": "raw_meat_1.png", "veg": "vegetables_2.png"}.items()}
# rat_1 faces right, cat_1 faces left: so the rat walks right toward the cat with no flips
USED_ASSETS = [os.path.basename(v) for v in A.values()]
CREDITS_FILES = [os.path.join(ASSETS, "credits.json")]

NARRATOR = dict(engine="edge", voice="hi-IN-MadhurNeural", rate="+35%")
NARRATOR_LABEL = "PLACEHOLDER Microsoft Madhur (hi-IN) via edge-tts, until the owner picks the channel voice"
MUSIC = "pad"
TAIL = 0.9

SCRIPT = [
    dict(id="b1", text="सोचो, एक ऐसा चूहा जो बिल्ली की स्मेल से भागता नहीं... बल्कि ख़ुद चल के उसकी तरफ़ जाता है।"),
    dict(id="b2", text="और ये कोई कार्टून नहीं है। ये एक छोटा सा पैरासाइट करवाता है।"),
    dict(id="b3", text="और सबसे अजीब बात? अंदाज़ा है कि दुनिया में हर तीन में से एक इंसान के अंदर भी ये हो सकता है।"),
    dict(id="b4", text="इसका नाम है टॉक्सोप्लाज़्मा गोंडी।"),
    dict(id="b5", text="इस पैरासाइट की ज़िंदगी का एक ही गोल है: बिल्ली के पेट तक पहुँचना।"),
    dict(id="b6", text="क्योंकि ये अपने बच्चे सिर्फ़ बिल्ली के अंदर ही बना सकता है।"),
    dict(id="b7", text="बिल्ली की पॉटी से इसके अंडे मिट्टी और पानी में आते हैं। चूहा उन्हें खा लेता है।"),
    dict(id="b8", text="फिर ये पैरासाइट चूहे के दिमाग़ तक पहुँचता है, और वहाँ छोटे-छोटे सिस्ट्स बना के छुप जाता है।"),
    dict(id="b9", text="नॉर्मल चूहा बिल्ली के पेशाब की स्मेल आते ही भाग जाता है। ये डर उसके अंदर जन्म से होता है।"),
    dict(id="b10", text="पर इन्फ़ेक्टेड चूहा इस स्मेल से डरता ही नहीं।"),
    dict(id="b11", text="ऑक्सफ़र्ड के एक एक्सपेरिमेंट में, इन्फ़ेक्टेड चूहे उल्टा उस कोने में ज़्यादा टाइम बिताने लगे, "
                        "जहाँ बिल्ली की स्मेल थी।"),
    dict(id="b12", text="साइंटिस्ट्स ने इसको नाम दिया: फ़ेटल अट्रैक्शन। यानी जानलेवा आकर्षण।"),
    dict(id="b13", text="चूहा बिल्ली के पास जाता है। बिल्ली उसे खा लेती है। और पैरासाइट अपनी मंज़िल तक पहुँच जाता है।"),
    dict(id="b14", text="तो सवाल ये है: अगर ये इंसानों के अंदर भी है... तो क्या ये हमारे दिमाग़ के साथ भी कुछ करता है?"),
    dict(id="b15", text="इंसान के अंदर भी ये दिमाग़ और मसल्स में सालों तक चुपचाप सो सकता है। "
                        "ज़्यादातर लोगों को कभी पता भी नहीं चलता।"),
    dict(id="b16", text="कुछ स्टडीज़ ने इन्फ़ेक्टेड लोगों के बिहेवियर में फ़र्क़ देखा है। पर ये अभी प्रूफ़ नहीं है। "
                        "साइंटिस्ट्स अभी भी इससे लेकर डिबेट कर रहे हैं।"),
    dict(id="b17", text="इंसान को ये अक्सर बिल्ली से नहीं, बल्कि कच्चे या अधपके मीट से, और बिना धुले फल-सब्ज़ी से मिलता है।"),
    dict(id="b18", text="पर एक जगह ये सच में ख़तरनाक है: प्रेगनेंसी। अगर प्रेगनेंसी में पहली बार इन्फ़ेक्शन हो, "
                        "तो ये बच्चे तक पहुँच सकता है।"),
    dict(id="b19", text="इसलिए डॉक्टर कहते हैं: प्रेगनेंसी में बिल्ली का लिटर बॉक्स ख़ुद साफ़ मत करिए, मीट अच्छे से पकाइए, "
                        "और सब्ज़ी धो के खाइए।"),
    dict(id="b20", text="और हाँ, इसका मतलब ये नहीं कि बिल्ली पालना ग़लत है। जो बिल्ली घर के अंदर रहती है और कच्चा मीट "
                        "नहीं खाती, उसके इन्फ़ेक्टेड होने का चांस काफ़ी कम होता है।"),
    dict(id="b21", text="आपके घर में बिल्ली है? और क्या आपको ये पता था? कमेंट में बताइए।"),
]

METADATA = dict(
    title="Ye parasite chuhe ka darr mita deta hai",
    caption="Ye chuha billi se bhaagta nahi... khud uski taraf jaata hai 😳\n"
            "Aur yahi parasite duniya ke lagbhag har 3 mein se 1 insaan ke andar ho sakta hai.",
    yt_title="Ye Parasite Chuhe Ko Billi Ki Taraf Bhejta Hai 😳 | Toxoplasma",
    yt_description="Ek parasite jo chuhe ka darr mita deta hai, aur jo duniya ke lagbhag har 3 mein se 1 insaan ke "
                   "andar ho sakta hai. Pregnancy mein kya dhyan rakhein, aur billi paalna safe hai ya nahi.",
    hashtags=["#toxoplasma", "#parasite", "#science", "#facts", "#factsinhindi", "#documentary"],
    pinned_comment="Aapke ghar mein billi hai? Aur kya aapko ye pehle se pata tha? 👇",
    sources=["Berdoy, Webster & Macdonald 2000, Proc. R. Soc. B, 'Fatal attraction in rats infected with "
             "Toxoplasma gondii' https://pmc.ncbi.nlm.nih.gov/articles/PMC1690701",
             "CDC, Toxoplasmosis: prevention (pregnancy, litter box, indoor cats) https://www.cdc.gov/toxoplasmosis/",
             "'1 in 3 people worldwide' is a widely cited estimate; said as andaza (estimate)"],
)


# ---------- scenes ----------

def s_hook(cr, t, tl):                                   # b1: the rat walks to the cat
    b = tl["b1"]
    header(cr, "hook", 1)
    walk = clamp(t / 4.0)                               # frame 0 already shows the rat, mid-step (research F1)
    rx = 230 + 110 * ease(walk)
    bob = 5 * math.sin(t * 14) * (1 - walk)
    photo(cr, A["cat"], 860, 1010, 300, alpha=0.95)                    # further back: smaller and higher
    path(cr, [(rx + 250, 1230), (640, 1110)], prog(t, 2.0, 1.0), 6, RED, 0.85, dash=[18, 14], arrow=True)
    photo(cr, A["rat"], rx, 1270 + bob, 240)
    headline(cr, t, "A RAT THAT WALKS", "TO THE CAT", -1.0, min(1.5, b.at(frac=0.6)), y=220, big_size=170)


def s_parasite(cr, t, tl):                               # b2: not a cartoon - a parasite
    b = tl["b2"]
    header(cr, "hook", 1)
    photo(cr, A["cat"], 860, 1010, 300, alpha=0.95)
    photo(cr, A["rat"], 340, 1270, 240)
    headline(cr, t, "NOT A CARTOON. IT'S A", "PARASITE", b.start, b.at("पैरासाइट"), y=220, big_size=170)
    stamp(cr, t, "REAL", b.start + 0.25, 420, 950, 70)


def s_one_in_three(cr, t, tl):                            # b3: 1 in 3 people
    b = tl["b3"]
    header(cr, "you", 1)
    headline(cr, t, "ESTIMATED: INSIDE", "", b.start, 1e9, y=220)
    t_n = b.at(frac=0.45)
    counter(cr, t, t_n, W / 2 - 230, 520, "1", 150)
    draw_text(cr, "IN", W / 2, 520, 110, INK, prog(t, t_n + 0.1, 0.25), anchor="cm")
    counter(cr, t, t_n + 0.15, W / 2 + 230, 520, "3", 150)
    t_red = b.at(frac=0.62)
    for i, x in enumerate((300, 540, 780)):
        p = prog(t, b.start + 0.15 * i, 0.3)
        red = i == 2 and t >= t_red
        person(cr, x, 1500 + 40 * (1 - p), 620, RED if red else INK, p * (1 if red else 0.88))
    ring(cr, 780, 1180, 170, 360, prog(t, t_red + 0.2, 0.5))


def s_name(cr, t, tl):                                   # b4: Toxoplasma gondii
    b = tl["b4"]
    header(cr, "the parasite", 2)
    p = prog(t, b.start, 0.35)
    framed_photo(cr, A["micro"], W / 2, 980 + 60 * (1 - p), 760, 760, alpha=p, rot=-0.02)
    card(cr, t, b.at("टॉक्सो"), 130, 1440, ["TOXOPLASMA GONDII", "SPECIMEN 01 · PROTOZOA"], size=40,
         pin_line=(W / 2 - 60, 1240))
    headline(cr, t, "ITS NAME", "", b.start, 1e9, y=220)


def s_goal(cr, t, tl):                                   # b5-b6: one goal - the cat's gut; only inside cats
    b5, b6 = tl["b5"], tl["b6"]
    header(cr, "life cycle", 3)
    photo(cr, A["cat"], 640, 1020, 640, alpha=prog(t, b5.start, 0.3))
    photo(cr, A["rat"], 200, 1500, 200, alpha=prog(t, b5.start + 0.2, 0.3))
    path(cr, [(300, 1450), (480, 1300), (650, 1090)], prog(t, b5.at(frac=0.55), 0.8), 7, RED, 0.9, arrow=True)
    if t >= b5.at(frac=0.75):
        pulse = 1 + 0.08 * math.sin((t - b5.start) * 6)
        blob(cr, 690, 1050, 44 * pulse, 3, RED, 0.85 * prog(t, b5.at(frac=0.75), 0.3))
    headline(cr, t, "ONE GOAL:", "THE CAT'S GUT", b5.start, b5.at(frac=0.6), y=220)
    card(cr, t, b6.start + 0.3, 460, 1560, ["BREEDS ONLY INSIDE CATS"], size=36)


def s_eggs(cr, t, tl):                                   # b7: eggs in soil and water, the rat eats them
    b = tl["b7"]
    header(cr, "life cycle", 3)
    soil_y = 1420
    p = prog(t, b.start, 0.4)
    cr.set_source_rgba(0.42, 0.31, 0.20, 0.85 * p)
    cr.rectangle(0, soil_y, W, H - soil_y)
    cr.fill()
    for i in range(70):                                  # pebbles in the soil
        x = (i * 151) % W
        y = soil_y + 30 + (i * 97) % (H - soil_y - 40)
        cr.set_source_rgba(0.30, 0.22, 0.14, 0.7 * p)
        cr.arc(x, y, 6 + (i % 5) * 3, 0, 2 * math.pi)
        cr.fill()
    cr.set_source_rgba(0.35, 0.52, 0.62, 0.8 * p)                  # a puddle on the right
    cr.save()
    cr.translate(820, soil_y + 10)
    cr.scale(1, 0.22)
    cr.arc(0, 0, 200, 0, 2 * math.pi)
    cr.restore()
    cr.fill()
    for i in range(14):                                  # oocysts dropping in
        tt = b.start + 0.25 + 0.08 * i
        q = clamp((t - tt) / 0.5)
        if q <= 0:
            continue
        x = 140 + (i * 67) % 760
        y = 700 + (soil_y - 700 + 10 + (i % 3) * 12) * ease(q)
        cr.save()
        cr.translate(x, y)
        cr.scale(1, 0.75)
        cr.arc(0, 0, 16, 0, 2 * math.pi)
        cr.restore()
        cr.set_source_rgba(0.95, 0.90, 0.78, 1)
        cr.fill_preserve()
        cr.set_source_rgba(*INK, 0.9)
        cr.set_line_width(4)
        cr.stroke()
    t_rat = b.at(frac=0.62)
    photo(cr, A["rat"], -200 + 520 * prog(t, t_rat, 0.8), soil_y - 70, 260, rot=0.08)
    headline(cr, t, "EGGS IN", "SOIL & WATER", b.start, b.at(frac=0.35), y=220)
    card(cr, t, b.start + 0.4, 600, 560, ["OOCYSTS", "FROM CAT DROPPINGS"], size=34)


def _brain(cr, cx, cy, s, alpha=1.0):
    """Side-view brain: a rounded lobe outline with a few folds."""
    cr.save()
    cr.translate(cx, cy)
    cr.scale(s, s)
    cr.move_to(-200, 40)
    cr.curve_to(-230, -60, -150, -150, -40, -150)
    cr.curve_to(60, -170, 190, -120, 210, -20)
    cr.curve_to(225, 50, 170, 110, 90, 110)
    cr.curve_to(40, 150, -20, 120, -40, 100)
    cr.curve_to(-120, 120, -190, 100, -200, 40)
    cr.close_path()
    cr.restore()
    cr.set_source_rgba(0.88, 0.71, 0.68, alpha)
    cr.fill_preserve()
    cr.set_source_rgba(*INK, 0.85 * alpha)
    cr.set_line_width(7)
    cr.stroke()
    folds = [[(-150, -40), (-90, -70), (-60, -20), (-10, -60)], [(-20, -110), (30, -70), (90, -100), (130, -50)],
             [(-130, 50), (-60, 20), (0, 60), (60, 20), (120, 50)], [(150, -40), (120, 10), (170, 40)]]
    cr.set_line_width(5)
    for f in folds:
        cr.move_to(cx + f[0][0] * s, cy + f[0][1] * s)
        for x, y in f[1:]:
            cr.line_to(cx + x * s, cy + y * s)
        cr.set_source_rgba(*INK, 0.5 * alpha)
        cr.stroke()


def s_brain(cr, t, tl):                                  # b8: cysts in the rat's brain
    b = tl["b8"]
    header(cr, "the brain", 4)
    photo(cr, A["rat"], 330, 760, 230, alpha=prog(t, b.start, 0.3))
    p = prog(t, b.start + 0.2, 0.4)
    _brain(cr, 560, 1200, 1.9 * (0.9 + 0.1 * p), p)
    path(cr, [(420, 760), (480, 900), (520, 990)], prog(t, b.start + 0.3, 0.6), 4, INK, 0.6, dash=[10, 10])
    t_c = b.at("सिस्ट्स") - 0.2
    for i, (x, y) in enumerate([(420, 1150), (560, 1060), (700, 1180), (520, 1260), (780, 1100), (640, 1300)]):
        q = clamp((t - t_c - 0.12 * i) / 0.25)
        if q > 0:
            blob(cr, x, y, 34 * (0.4 + 0.6 * q), 10 + i, (0.98, 0.95, 0.88), q)
            blob(cr, x, y, 34 * (0.4 + 0.6 * q), 10 + i, RED, q, fill=False, width=6)
            for k in range(4):
                cr.set_source_rgba(*RED, 0.8 * q)
                cr.arc(x - 12 + 8 * k, y - 4 + 6 * (k % 2), 4, 0, 2 * math.pi)
                cr.fill()
    headline(cr, t, "HIDES IN THE", "BRAIN", b.start, b.at(frac=0.35), y=220)
    q = prog(t, t_c + 0.5, 0.35)
    framed_photo(cr, A["cyst"], 790, 1620 + 50 * (1 - q), 400, 300, alpha=q, rot=0.03)
    card(cr, t, t_c + 0.8, 110, 1560, ["TISSUE CYST", "REAL, MOUSE BRAIN · USDA"], size=36)


def _scent(cr, cx, cy, t, alpha):
    for i in range(6):
        y = cy - 200 + 80 * i
        ph = t * 2.5 + i
        pts = [(cx - 170 + 34 * k, y + 22 * math.sin(ph + k * 0.9)) for k in range(11)]
        path(cr, pts, 1.0, 10, (0.62, 0.55, 0.12), 0.8 * alpha)


def s_fear(cr, t, tl):                                   # b9-b10: born with fear / infected: no fear
    b9, b10 = tl["b9"], tl["b10"]
    header(cr, "instinct", 5)
    _scent(cr, 830, 1100, t, prog(t, b9.start, 0.3))
    card(cr, t, b9.start + 0.3, 650, 1380, ["CAT URINE"], size=40)
    run = prog(t, b9.at(frac=0.35), 0.6)
    if t < b10.start:
        photo(cr, A["rat"], 460 - 260 * run, 1120, 320, flip=True)      # flees to the left
    else:
        q = prog(t, b10.start, 0.8)
        photo(cr, A["rat"], 200 + 250 * q, 1120, 320)                   # turns back toward the smell
    headline(cr, t, "BORN WITH", "FEAR", b9.start, b9.at("डर"), y=220, strike_at=b10.at("डरता"), struck=True)
    if t >= b10.start:
        stamp(cr, t, "INFECTED", b10.start + 0.15, 400, 880, 54)


def s_experiment(cr, t, tl):                             # b11: Oxford enclosure, the cat corner
    b = tl["b11"]
    header(cr, "the experiment", 6)
    x0, y0, s = 150, 640, 780
    p = prog(t, b.start, 0.4)
    cr.set_source_rgba(*INK, 0.9 * p)
    cr.set_line_width(8)
    cr.rectangle(x0, y0, s, s)
    cr.stroke()
    corners = [(x0 + 110, y0 + 110, "RAT"), (x0 + s - 110, y0 + 110, "NEUTRAL"), (x0 + 110, y0 + s - 110, "RABBIT"),
               (x0 + s - 110, y0 + s - 110, "CAT")]
    for cx, cy, name in corners:
        cat = name == "CAT"
        glow = prog(t, b.at(frac=0.55), 0.6) if cat else 0
        if glow:
            cr.set_source_rgba(*RED, 0.25 * glow)
            cr.arc(cx, cy, 120, 0, 2 * math.pi)
            cr.fill()
        cr.set_source_rgba(*(RED if cat else INK), 0.85 * p)
        cr.set_line_width(5)
        cr.arc(cx, cy, 70, 0, 2 * math.pi)
        cr.stroke()
        below = cy < y0 + s / 2
        draw_text(cr, name, cx, cy + (92 if below else -92), 30, RED if cat else INK, p,
                  anchor="ct" if below else "cb")
    # an infected rat's wander: a short look round, then it keeps circling the cat corner
    route = [(x0 + s / 2, y0 + s / 2), (x0 + 260, y0 + 330), (x0 + 200, y0 + 520), (x0 + 420, y0 + 600)]
    cx, cy = x0 + s - 110, y0 + s - 110
    route += [(cx + 75 * math.cos(a), cy + 75 * math.sin(a)) for a in [3.6 + 0.5 * k for k in range(22)]]
    path(cr, route, prog(t, b.start + 0.4, b.dur * 0.75), 5, INK, 0.75)
    card(cr, t, b.at("ऑक्सफ़र्ड") + 0.2, 150, 1500, ["OXFORD · 2000", "BERDOY, WEBSTER & MACDONALD"], size=34)
    headline(cr, t, "MORE TIME IN THE", "CAT CORNER", b.start, b.at(frac=0.6), y=220)


def s_fatal(cr, t, tl):                                  # b12: fatal attraction
    b = tl["b12"]
    header(cr, "the experiment", 6)
    photo(cr, A["rat"], 330, 1350, 280, alpha=prog(t, b.start, 0.3))
    photo(cr, A["cat"], 790, 1260, 560, alpha=prog(t, b.start, 0.3))
    path(cr, [(480, 1300), (600, 1240)], prog(t, b.start + 0.5, 0.4), 6, RED, 0.9, arrow=True)
    headline(cr, t, "SCIENTISTS CALLED IT", "FATAL", b.start, b.at("फ़ेटल"), y=220)
    draw_text(cr, "ATTRACTION", MARGIN, 520, 150, RED, prog(t, b.at("अट्रैक्शन"), 0.3))
    card(cr, t, b.at("यानी"), 560, 1640, ["JAANLEVA AAKARSHAN"], size=36)


def s_loop(cr, t, tl):                                   # b13: rat -> cat -> parasite home
    b = tl["b13"]
    header(cr, "life cycle", 3)
    pts = [(260, 900), (820, 900), (540, 1450)]
    photo(cr, A["rat"], *pts[0], 220, alpha=prog(t, b.start, 0.3))
    photo(cr, A["cat"], pts[1][0], pts[1][1] - 20, 380, alpha=prog(t, b.start + 0.1, 0.3))
    blob(cr, *pts[2], 70, 5, (0.98, 0.95, 0.88), prog(t, b.start + 0.2, 0.3))
    blob(cr, *pts[2], 70, 5, RED, prog(t, b.start + 0.2, 0.3), fill=False, width=7)
    draw_text(cr, "PARASITE", pts[2][0], pts[2][1] + 110, 34, INK, prog(t, b.start + 0.2, 0.3), anchor="ct")
    t1, t2, t3 = b.start + 0.2, b.at(frac=0.35), b.at(frac=0.68)
    path(cr, [(380, 880), (680, 880)], prog(t, t1, 0.6), 7, RED, 0.9, arrow=True)
    path(cr, [(800, 1080), (630, 1380)], prog(t, t2, 0.6), 7, RED, 0.9, arrow=True)
    path(cr, [(450, 1380), (280, 1030)], prog(t, t3, 0.6), 7, RED, 0.9, arrow=True)
    headline(cr, t, "MISSION", "COMPLETE", b.start, b.at("मंज़िल"), y=220)


def s_humans(cr, t, tl):                                 # b14: re-hook - and in humans?
    b = tl["b14"]
    header(cr, "in humans", 7)
    p = prog(t, b.start, 0.4)
    head_profile(cr, 520, 1180, 900 * (0.95 + 0.05 * p), INK, p)
    q = prog(t, b.at(frac=0.7), 0.3)
    draw_text(cr, "?", 560, 1060, 360 * (0.8 + 0.2 * q), RED, q, anchor="cm")
    headline(cr, t, "AND INSIDE", "HUMANS?", b.start, b.at("इंसानों"), y=220)


def s_sleep(cr, t, tl):                                  # b15: silent for years
    b = tl["b15"]
    header(cr, "in humans", 7)
    head_profile(cr, 520, 1180, 900, INK, 1.0)
    for i, (x, y) in enumerate([(420, 950), (520, 900), (600, 990), (470, 1040)]):
        q = prog(t, b.start + 0.3 + 0.15 * i, 0.3)
        blob(cr, x, y, 30, 20 + i, (0.98, 0.95, 0.88), q)
        blob(cr, x, y, 30, 20 + i, RED, q, fill=False, width=5)
        zz = (t * 0.8 + i * 0.3) % 1.0
        draw_text(cr, "z", x + 30 + 30 * zz, y - 40 - 60 * zz, 36, INK, q * (1 - zz), anchor="cm")
    headline(cr, t, "ASLEEP FOR", "YEARS", b.start, b.at("सालों"), y=220)
    card(cr, t, b.at("ज़्यादातर"), 560, 1600, ["MOST PEOPLE", "NEVER KNOW"], size=38)


def s_behaviour(cr, t, tl):                              # b16: behaviour? not proven
    b = tl["b16"]
    header(cr, "in humans", 7)
    for i, x in enumerate((260, 540, 820)):
        person(cr, x, 1520, 560, RED if i == 1 else INK, prog(t, b.start + 0.1 * i, 0.3) * 0.88)
    headline(cr, t, "CHANGES", "BEHAVIOUR?", b.start, b.at(frac=0.15), y=220)
    stamp(cr, t, "NOT PROVEN", b.at("प्रूफ़") - 0.1, W / 2, 1080, 80, rot=-0.1)
    card(cr, t, b.at("डिबेट") - 0.3, 330, 1650, ["STILL DEBATED"], size=38)


def s_how(cr, t, tl):                                    # b17: not usually the cat - raw meat, unwashed veg
    b = tl["b17"]
    header(cr, "how humans get it", 8)
    photo(cr, A["cat"], 540, 900, 380, alpha=prog(t, b.start, 0.3))
    cross(cr, 540, 900, 300, prog(t, b.at("बिल्ली") + 0.2, 0.4))
    photo(cr, A["meat"], 310, 1420, 330, alpha=prog(t, b.at("कच्चे"), 0.3), rot=-0.05)
    photo(cr, A["veg"], 790, 1420, 360, alpha=prog(t, b.at("धुले") - 0.3, 0.3), rot=0.04)
    ring(cr, 310, 1420, 230, 200, prog(t, b.at("अधपके"), 0.5))
    ring(cr, 790, 1420, 250, 210, prog(t, b.at("सब्ज़ी"), 0.5))
    headline(cr, t, "USUALLY NOT THE CAT:", "FOOD", b.start, b.at("कच्चे"), y=220)


def _pregnant(cr, x, y, h, color, alpha):
    person(cr, x, y, h, color, alpha)
    cr.set_source_rgba(*color, alpha)
    cr.arc(x + h * 0.13, y - h * 0.50, h * 0.12, -1.6, 1.6)
    cr.fill()


def s_pregnancy(cr, t, tl):                              # b18: the real danger - pregnancy
    b = tl["b18"]
    header(cr, "pregnancy", 9)
    p = prog(t, b.start, 0.4)
    _pregnant(cr, 520, 1600, 900, INK, 0.9 * p)
    q = prog(t, b.at(frac=0.7), 0.4)
    blob(cr, 600, 1150, 46, 9, RED, 0.85 * q)
    ring(cr, 600, 1150, 150, 150, q)
    headline(cr, t, "ONE REAL", "DANGER", b.start, b.at("ख़तरनाक"), y=220)
    card(cr, t, b.at("पहली"), 140, 1680, ["FIRST INFECTION IN PREGNANCY"], size=32)


def s_rules(cr, t, tl):                                  # b19: the doctor's three rules
    b = tl["b19"]
    header(cr, "what doctors say", 10)
    items = [("LITTER BOX: LET SOMEONE ELSE", "लिटर"), ("MEAT: COOK IT WELL", "मीट"), ("VEGETABLES: WASH THEM", "सब्ज़ी")]
    for i, (txt, cue) in enumerate(items):
        tc = b.at(cue)
        y = 880 + 280 * i
        p = prog(t, tc - 0.3, 0.3)
        cr.set_source_rgba(*INK, 0.85 * p)
        cr.set_line_width(6)
        cr.rectangle(MARGIN + 10, y - 50, 100, 100)
        cr.stroke()
        draw_text(cr, txt, MARGIN + 150, y, 54, INK, p, anchor="lm")
        tick(cr, MARGIN + 25, y - 5, 90, prog(t, tc + 0.3, 0.35))
    headline(cr, t, "IN PREGNANCY:", "3 RULES", b.start, b.at("डॉक्टर"), y=220)


def s_indoor(cr, t, tl):                                 # b20: indoor cats - low risk
    b = tl["b20"]
    header(cr, "your home", 11)
    p = prog(t, b.start, 0.4)
    photo(cr, A["cat_indoor"], W / 2, 1220, 640, alpha=p)
    t_low = b.at("कम")
    headline(cr, t, "INDOOR CAT, NO RAW MEAT:", "LOW RISK", b.start, b.at("अंदर"), y=220)
    tick(cr, 820, 900, 140, prog(t, t_low, 0.4))


def s_end(cr, t, tl):                                    # b21: your cat too? comment
    b = tl["b21"]
    header(cr, "your turn", 12)
    photo(cr, A["cat_indoor"], 300, 1640, 300, alpha=prog(t, b.start, 0.3), rot=-0.05)
    phone_comments(cr, t, b.at("कमेंट") - 0.4, 640, 1180, 820, reply="HAAN, MERI BILLI HAI!")
    headline(cr, t, "YOUR HOME", "A CAT TOO?", b.start, b.at("बिल्ली"), y=220)


SCENES = [(("b1",), s_hook), (("b2",), s_parasite), (("b3",), s_one_in_three), (("b4",), s_name),
          (("b5", "b6"), s_goal), (("b7",), s_eggs), (("b8",), s_brain), (("b9", "b10"), s_fear),
          (("b11",), s_experiment), (("b12",), s_fatal), (("b13",), s_loop), (("b14",), s_humans),
          (("b15",), s_sleep), (("b16",), s_behaviour), (("b17",), s_how), (("b18",), s_pregnancy),
          (("b19",), s_rules), (("b20",), s_indoor), (("b21",), s_end)]


def _scene_at(t, tl):
    """Each scene runs from its first line's start to the next scene's start (the gap belongs to the scene before)."""
    starts = [tl[ids[0]].start if k else 0.0 for k, (ids, _) in enumerate(SCENES)]
    k = max(i for i, s in enumerate(starts) if t >= s)
    end = starts[k + 1] if k + 1 < len(starts) else tl.total
    return k, starts[k], end


def draw(cr, t, tl):
    k, t0, t1 = _scene_at(t, tl)
    paper(cr, seed=1 + k % 3)
    cr.save()
    push(cr, t, t0, t1, 1.0, 1.045)
    SCENES[k][1](cr, t, tl)
    cr.restore()


def sfx(tl):
    """Small sounds at the turning points only (research A6): pops on labels, a scribble on strikes, a tick before
    the re-hook, a soft whoosh on scene changes."""
    ev = [(tl["b2"].start + 0.25, "thud", 0.0), (tl["b10"].at("डरता"), "scribble", 0.35),
          (tl["b14"].start - 0.35, "tick", 0.0), (tl["b16"].at("प्रूफ़") - 0.1, "thud", 0.0),
          (tl["b21"].at("कमेंट"), "typing", 1.0)]
    for ids, _ in SCENES[1:]:
        ev.append((tl[ids[0]].start, "whoosh", 0.3))
    for bid in ("b4", "b6", "b7", "b8", "b9", "b11", "b12", "b15", "b18"):
        ev.append((tl[bid].start + 0.4, "pop", 0.0))
    return ev
