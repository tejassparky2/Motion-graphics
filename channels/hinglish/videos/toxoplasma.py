"""Batch 1, video 1: "Ye parasite chuhe ka darr mita deta hai" (Toxoplasma gondii). Script approved by the owner
29 Oct 2026 (scripts_batch1.md #1); narration below is that script word for word, in Devanagari for the voice."""
import math
import os

import cairo

from poster import (CORAL, CREAM, GOLD, GREEN, INK, MARGIN, MONO_FONT, RED, FADED, W, H, _round, blob, calendar,
                    card, clamp, counter, cross, cyst, draw_text, drop, ease, erase, finish, footnote, framed_photo,
                    gauge, head_profile, headline, icon_array, knock, magnifier, paper, parasite, path, person,
                    photo, photo_width, prog, push, ring, rule, slate, slide, stamp, text_size, tick, window, yes_no_card)

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
ASSETS = os.path.join(os.path.dirname(REPO), "hinglish_assets", "toxoplasma")   # outside the public repo
A = {k: os.path.join(ASSETS, v) for k, v in {
    "rat": "rat_1.png", "cat": "cat_1.png", "cat_indoor": "cat_indoor_1.png", "micro": "toxo_micro_2.jpg",
    "cyst": "toxo_micro_1.jpg", "meat": "raw_meat_1.png", "veg": "vegetables_2.png"}.items()}
# rat_1 faces right, cat_1 faces left: so the rat walks right toward the cat with no flips
USED_ASSETS = [os.path.basename(v) for v in A.values()]
CREDITS_FILES = [os.path.join(ASSETS, "credits.json")]

# Owner, 29 Oct 2026: "Aman looks good" / "the words are not clear". Aman's voice comes from Indic Parler-TTS
# (named speaker, prompt 'named_aman_s3'); IndicF5 then speaks every line in that synthetic voice: WER 33% -> 22%,
# UTMOS 2.76 -> 3.66, same voice (ECAPA 0.81 to the prompt) in the 3-line test.
_VOICES = os.path.join(os.path.dirname(REPO), "mayank", "voice")
NARRATOR = dict(engine="f5", studio="v3", tempo=1.13,   # one even speed-up for every line (owner: "speed up voice little")
                ref_audio=os.path.join(_VOICES, "f5_refs", "named_aman_s3_ref.wav"),
                ref_text="सोचो, एक ऐसा पौधा जो कीड़ों को खा जाता है। और ये कोई फ़िल्म का सीन नहीं है, ये बिल्कुल सच है।")
VOICE_REF = os.path.join(_VOICES, "f5_refs", "named_aman_s3_ref.wav")
NARRATOR_LABEL = ("synthetic narrator: Indic Parler-TTS named speaker 'Aman' (Apache-2.0; datasets CC BY 4.0) as the "
                  "voice prompt, spoken by AI4Bharat IndicF5 (MIT), studio chain; nobody is cloned")
MUSIC = "pad"
TAIL = 0.9

# v2, approved by the owner 29 Oct 2026 ("Yes"): hook, Tom & Jerry anchor, "only the cat fear" beat and the "socho"
# bookend come from research_notes/meanwhilemayank_parasite_reels_study_2026-10-29.md. "gap" = the longer pause
# Mayank leaves only before a reveal (the name, the precision beat, the closing line).
REVEAL_GAP = 0.8
SCRIPT = [
    dict(id="b1", text="सोचो, अगर कोई तुम्हारा डर ही मिटा दे... और तुम ख़ुद चल के अपने शिकारी के पास पहुँच जाओ।"),
    dict(id="b2", text="टॉम एंड जेरी में चूहा बिल्ली से डरता नहीं था। पर वो कार्टून था।"),
    dict(id="b3", text="असली दुनिया में ये सच में होता है। एक छोटा सा पैरासाइट चूहे का डर मिटा देता है।"),
    dict(id="b4", text="और सबसे अजीब बात? ये तुम्हारे अंदर भी हो सकता है। "
                       "अंदाज़ा है कि दुनिया में हर तीन में से एक इंसान के अंदर ये है।", gap=REVEAL_GAP),
    dict(id="b5", text="इसका नाम है टॉक्सो-प्लाज़्मा गोंडी।"),
    dict(id="b6", text="इस पैरासाइट की ज़िंदगी का एक ही गोल है: बिल्ली के पेट तक पहुँचना।"),
    dict(id="b7", text="क्योंकि ये अपने बच्चे सिर्फ़ बिल्ली के अंदर ही बना सकता है।"),
    dict(id="b8", text="बिल्ली की पॉटी से इसके अंडे मिट्टी और पानी में आते हैं। चूहा उन्हें खा लेता है।"),
    dict(id="b9", text="फिर ये पैरासाइट चूहे के दिमाग़ तक पहुँचता है, और वहाँ छोटे-छोटे सिस्ट्स बना के छुप जाता है।"),
    dict(id="b10", text="नॉर्मल चूहा बिल्ली के पेशाब की स्मेल आते ही भाग जाता है। ये डर उसके अंदर जन्म से होता है।"),
    dict(id="b11", text="पर इन्फ़ेक्टेड चूहा इस स्मेल से डरता ही नहीं।"),
    dict(id="b12", text="ऑक्सफ़र्ड के एक एक्सपेरिमेंट में, इन्फ़ेक्टेड चूहे उल्टा उस कोने में ज़्यादा टाइम बिताने लगे, "
                        "जहाँ बिल्ली की स्मेल थी।"),
    dict(id="b13", text="साइंटिस्ट्स ने इसको नाम दिया: फ़ेटल अट्रैक्शन। यानी जानलेवा आकर्षण।", gap=REVEAL_GAP),
    dict(id="b14", text="और सबसे हैरानी की बात? बाक़ी सारे डर वैसे ही रहते हैं। दूसरे शिकारियों की स्मेल से, खुली जगह से, "
                        "चूहा अब भी डरता है। मिटता है तो सिर्फ़ बिल्ली का डर।"),
    dict(id="b15", text="चूहा बिल्ली के पास जाता है। बिल्ली उसे खा लेती है। और पैरासाइट अपनी मंज़िल तक पहुँच जाता है।"),
    dict(id="b16", text="तो सवाल ये है: अगर ये इंसानों के अंदर भी है... तो क्या ये हमारे दिमाग़ के साथ भी कुछ करता है?"),
    dict(id="b17", text="इंसान के अंदर भी ये दिमाग़ और मसल्स में सालों तक चुपचाप सो सकता है। "
                        "ज़्यादातर लोगों को कभी पता भी नहीं चलता।"),
    dict(id="b18", text="कुछ स्टडीज़ ने इन्फ़ेक्टेड लोगों के बिहेवियर में फ़र्क़ देखा है। पर ये अभी प्रूफ़ नहीं है। "
                        "साइंटिस्ट्स अभी भी इससे लेकर डिबेट कर रहे हैं।"),
    dict(id="b19", text="इंसान को ये अक्सर बिल्ली से नहीं, बल्कि कच्चे या अधपके मीट से, और बिना धुले फल-सब्ज़ी से मिलता है।"),
    dict(id="b20", text="पर एक जगह ये सच में ख़तरनाक है: प्रेग्नेंसी। अगर प्रेग्नेंसी में पहली बार इन्फ़ेक्शन हो, "
                        "तो ये बच्चे तक पहुँच सकता है।"),
    dict(id="b21", text="इसलिए डॉक्टर कहते हैं: प्रेग्नेंसी में बिल्ली का लिटर बॉक्स ख़ुद साफ़ मत करो, मीट अच्छे से पकाओ, "
                        "और सब्ज़ी धो के खाओ।"),
    dict(id="b22", text="और हाँ, इसका मतलब ये नहीं कि बिल्ली पालना ग़लत है। जो बिल्ली घर के अंदर रहती है और कच्चा मीट "
                        "नहीं खाती, उसके इन्फ़ेक्टेड होने का चांस काफ़ी कम होता है।", gap=REVEAL_GAP),
    dict(id="b23", text="सोचो, एक सेल वाला जीव, जो आँख से दिखता भी नहीं... वो चूहे का वो डर मिटा देता है, "
                        "जो उसके अंदर जन्म से था।"),
    dict(id="b24", text="तुम्हारे घर में बिल्ली है? और क्या तुम्हें ये पता था? कमेंट में बताओ।"),
]

METADATA = dict(
    title="Ye parasite chuhe ka darr mita deta hai",
    caption="Ye chuha billi se bhaagta nahi... khud uski taraf jaata hai 😳\n"
            "Aur yahi parasite duniya ke lagbhag har 3 mein se 1 insaan ke andar ho sakta hai.",
    yt_title="Ye Parasite Chuhe Ko Billi Ki Taraf Bhejta Hai 😳 | Toxoplasma",
    yt_description="Ek parasite jo chuhe ka darr mita deta hai, aur jo duniya ke lagbhag har 3 mein se 1 insaan ke "
                   "andar ho sakta hai. Pregnancy mein kya dhyan rakhein, aur billi paalna safe hai ya nahi.",
    hashtags=["#toxoplasma", "#parasite", "#science", "#facts", "#factsinhindi", "#documentary"],
    pinned_comment="Tumhare ghar mein billi hai? Aur kya tumhe ye pehle se pata tha? 👇",
    sources=["Berdoy, Webster & Macdonald 2000, Proc. R. Soc. B, 'Fatal attraction in rats infected with "
             "Toxoplasma gondii' https://pmc.ncbi.nlm.nih.gov/articles/PMC1690701",
             "Vyas et al. 2007, PNAS 104:6442, 'Behavioral changes induced by Toxoplasma infection of rodents are "
             "highly specific to aversion of cat odors' https://pmc.ncbi.nlm.nih.gov/articles/PMC1851063",
             "House, Vyas & Sapolsky 2011, PLoS ONE 6:e23277, 'Predator cat odors activate sexual arousal pathways "
             "in brains of Toxoplasma gondii infected rats' https://pubmed.ncbi.nlm.nih.gov/21858053",
             "CDC, Toxoplasmosis: prevention (pregnancy, litter box, indoor cats) https://www.cdc.gov/toxoplasmosis/",
             "'1 in 3 people worldwide' is a widely cited estimate; said as andaza (estimate)"],
)


# ---------- helpers kept from v1 ----------

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


def _scent(cr, cx, cy, t, alpha):
    for i in range(6):
        y = cy - 200 + 80 * i
        ph = t * 2.5 + i
        pts = [(cx - 170 + 34 * k, y + 22 * math.sin(ph + k * 0.9)) for k in range(11)]
        path(cr, pts, 1.0, 10, (0.62, 0.55, 0.12), 0.8 * alpha)


# ---------- shots ----------
# v2 rebuild (owner, 29 Oct 2026: "visuals seems changing slow and repetitive", "make videos like mayank like on hiv
# chickenpox"). Rules from the style bible and the parasite-reels study: a new picture every ~2.7 s, cut on the spoken
# word; the visual is the literal noun of the sentence; one recurring metaphor (an eraser rubbing out FEAR); red =
# threat, green = reassurance, gold = numbers; dark slate for inside a body; no section labels (bare rule only).

TOXO2 = os.path.join(os.path.dirname(REPO), "hinglish_assets", "toxoplasma2")


def _a2(name):
    """First file in toxoplasma2 whose name starts with `name` (None if the asset search hasn't found one yet)."""
    if os.path.isdir(TOXO2):
        for f in sorted(os.listdir(TOXO2)):
            if f.startswith(name) and f.lower().endswith((".png", ".jpg", ".jpeg")) and "_orig" not in f:
                return os.path.join(TOXO2, f)
    return None


B = {k: _a2(k) for k in ("balance_scale", "cat_food_bowl", "cat_sitting_front", "cooking_meat_pan", "gray_anatomy_brain",
                         "gray_anatomy_muscles", "kitten_or_cat_indian_home", "litter_box_with_scoop", "magnet_horseshoe",
                         "magnifying_glass", "microscope", "oxford_university", "people_crowd_india", "rat_running",
                         "rat_sniffing_ground", "raw_chicken_or_meat_plate", "research_papers_stack", "soil_closeup",
                         "stopwatch", "ultrasound_scan", "warning_sign", "washing_vegetables_tap", "water_puddle",
                         "mannequin", "old_tv", "pregnant_woman_silhouette", "litter_scoop")}
B["eraser"] = _a2("eraser_plain")                       # brand text smoothed off (public domain original)
B["gray_anatomy_muscles"] = _a2("gray_anatomy_muscles_alt_sobotta")   # the sharper engraving
USED_ASSETS += [os.path.basename(v) for v in B.values() if v]
CREDITS_FILES.append(os.path.join(TOXO2, "credits.json"))

def T(tl, bid, cue=None):
    """Time of a cue inside line `bid`: None = line start, str = that word, float = fraction of the line."""
    b = tl[bid]
    if cue is None:
        return b.start
    return b.at(cue) if isinstance(cue, str) else b.at(frac=cue)


def _pic(cr, key, cx, cy, h, t, t0, rot=0.0, flip=False, tint=None, alpha=1.0, frame=None):
    """Photo cut-out (or framed photo when `frame` = (w, h)) that pops up into place at t0."""
    path_ = B.get(key) or A.get(key)
    if not path_:
        return
    p = prog(t, t0, 0.3)
    if frame:
        framed_photo(cr, path_, cx, cy + 50 * (1 - p), frame[0], frame[1], alpha=p * alpha, rot=rot)
    else:
        photo(cr, path_, cx, cy + 50 * (1 - p), h, alpha=p * alpha, rot=rot, flip=flip, tint=tint)


def _mq(cr, x, cy, h, t=0.0, bob=True, red=0.0, alpha=1.0):
    """The wooden mannequin photo (the hook's stand-in for "you"), running right with a small bob; `red` fills its
    head red (the parasite inside you). Returns the head position."""
    y = cy - (18 * abs(math.sin(t * 9)) if bob else 0)
    photo(cr, B["mannequin"], x, y, h, alpha=alpha)
    w = photo_width(B["mannequin"], h)
    hx, hy = x - w / 2 + 0.62 * w, y - h / 2 + 0.10 * h
    if red > 0:
        cr.set_source_rgba(*RED, 0.85 * red * alpha)
        cr.arc(hx, hy, h * 0.04, 0, 2 * math.pi)
        cr.fill()
    return hx, hy


def _tv(cr, cx, cy, h, alpha=1.0):
    """The old CRT photo (logo removed); returns its screen glass rectangle (measured on the photo) so a picture can
    be drawn into it."""
    photo(cr, B["old_tv"], cx, cy, h, alpha=alpha)
    w = photo_width(B["old_tv"], h)
    x0, y0 = cx - w / 2, cy - h / 2
    return x0 + 0.136 * w, y0 + 0.083 * h, 0.634 * w, 0.356 * h


def _screen(cr, rect, alpha, on=1.0):
    """CRT picture area: pale glow when on; collapses to a line then a dot as `on` goes 1 -> 0."""
    sx, sy, sw_, sh_ = rect
    vy = max(0.02, clamp(on * 2 - 1)) if on < 1 else 1.0
    vx = clamp(on * 2) if on < 1 else 1.0
    cx, cy = sx + sw_ / 2, sy + sh_ / 2
    cr.set_source_rgba(0.80, 0.86, 0.82, alpha * (1 if on > 0 else 0))
    _round(cr, cx - sw_ * vx / 2, cy - sh_ * vy / 2, sw_ * vx, sh_ * vy, 30 * vy)
    cr.fill()


def _checklist(cr, t, x, y, w, title, items, alpha=1.0):
    """Kraft card with a title and rows: (label, t_show, mark, t_mark), mark in {"tick", "cross", "erase", None}."""
    rows = len(items)
    h = 120 + 110 * rows
    p = prog(t, items[0][1] - 0.35, 0.3) * alpha
    if p <= 0:
        return
    cr.set_source_rgba(0, 0, 0, 0.2 * p)
    _round(cr, x + 8, y + 14, w, h, 16)
    cr.fill()
    cr.set_source_rgba(0.83, 0.72, 0.54, p)
    _round(cr, x, y, w, h, 16)
    cr.fill()
    draw_text(cr, title, x + 40, y + 34, 40, INK, p, MONO_FONT, tracking=4)
    for i, (label, t_show, mark, t_mark) in enumerate(items):
        ry = y + 150 + 110 * i
        q = prog(t, t_show, 0.25) * alpha
        if q <= 0:
            continue
        cr.set_source_rgba(*INK, 0.85 * q)
        cr.set_line_width(5)
        cr.rectangle(x + 40, ry - 32, 64, 64)
        cr.stroke()
        if mark == "erase":
            erase(cr, t, t_mark, label, x + 130, ry, 70, INK, dur=0.8, eraser=B["eraser"], anchor="lm")
        else:
            draw_text(cr, label, x + 130, ry, 70, INK, q, anchor="lm")
        if mark == "tick":
            tick(cr, x + 48, ry - 4, 62, prog(t, t_mark, 0.3))
        elif mark == "cross":
            cross(cr, x + 72, ry, 56, prog(t, t_mark, 0.3))


def _fear_tag(cr, t, x, y, t0, t_erase=None, size=96, anchor=None):
    """The word FEAR on a string tied to the animal at `anchor`; rubbed out at t_erase."""
    p = prog(t, t0, 0.3)
    if p <= 0:
        return
    if anchor:
        path(cr, [anchor, (x - 12, y)], p, 3, INK, 0.7)
    if t_erase is None:
        draw_text(cr, "FEAR", x, y, size, RED, p, anchor="lm")
    else:
        erase(cr, t, t_erase, "FEAR", x, y, size, RED, dur=0.8, eraser=B["eraser"], anchor="lm")


# hook: the ant reel's second person, made true; the wasp reel's escalation (study sections 1-2)
def h_you(cr, t, tl, t0):                                # b1 "socho... your fear erased"
    photo(cr, A["cat"], 820, 1080, 980, alpha=0.22 * prog(t, 0.6, 0.6), tint=INK, shadow=False)
    _mq(cr, 300 + 90 * t, 1230, 620, t)
    t_er = T(tl, "b1", "मिटा")
    draw_text(cr, "WHAT IF YOUR", MARGIN, 200, 64, INK)
    if t < t_er - 0.1:
        draw_text(cr, "FEAR", MARGIN, 276, 190, RED if t >= 0.5 else FADED, 1.0 if t >= 0.5 else 0.4)
    else:
        erase(cr, t, t_er - 0.1, "FEAR", MARGIN, 276, 190, RED, dur=0.45, eraser=B["eraser"])
        stamp(cr, t, "ERASED", t_er + 0.3, 690, 380, 64)


def h_walk(cr, t, tl, t0):                               # b1 "...you walk to your hunter"
    t_h = T(tl, "b1", "शिकारी")
    grow = prog(t, t_h, 0.6)
    photo(cr, A["cat"], 830, 1060, 900 + 140 * grow, alpha=0.25 + 0.75 * grow, tint=None if grow > 0.5 else INK,
          shadow=False)
    x = 300 + 220 * clamp((t - t0) / 2.8)
    _mq(cr, x, 1260, 560, t)
    path(cr, [(x + 200, 1560), (700, 1560)], prog(t, t0 + 0.3, 0.8), 6, RED, 0.85, dash=[18, 14], arrow=True)
    headline(cr, t, "YOU WALK TO", "THE HUNTER", t0, t_h, t_ghost=t0 + 0.2)


def h_cartoon(cr, t, tl, t0):                            # b2 "in Tom & Jerry the mouse wasn't scared"
    rect = _tv(cr, W / 2, 1150, 1120)
    _screen(cr, rect, 1.0)
    sx, sy, sw_, sh_ = rect
    cr.save()
    _round(cr, sx, sy, sw_, sh_, 30)
    cr.clip()
    photo(cr, A["cat"], sx + sw_ * 0.74, sy + sh_ * 0.52, sh_ * 0.62, tint=(0.18, 0.2, 0.2), shadow=False)
    hop = abs(math.sin(t * 7)) * 30
    photo(cr, A["rat"], sx + sw_ * 0.24, sy + sh_ * 0.80 - hop, sh_ * 0.30, tint=(0.55, 0.36, 0.26), shadow=False)
    cr.reset_clip()
    cr.restore()
    headline(cr, t, "IN CARTOONS, THE MOUSE", "ISN'T SCARED", t0, T(tl, "b2", "डरता"), t_ghost=t0 + 0.3)


def h_fiction(cr, t, tl, t0):                            # b2 "...but that was a cartoon"
    rect = _tv(cr, W / 2, 1150, 1120)
    _screen(cr, rect, 1.0, on=1 - prog(t, t0 + 0.2, 0.5))
    headline(cr, t, "BUT THAT WAS", "A CARTOON", t0, T(tl, "b2", "कार्टून"))
    stamp(cr, t, "FICTION", T(tl, "b2", "कार्टून") + 0.3, 760, 1500, 64, rot=0.08)


def h_real(cr, t, tl, t0):                               # b3 "in the real world it happens"
    photo(cr, A["rat"], 540, drop(t, t0, 1180), 420)
    stamp(cr, t, "REAL", T(tl, "b3", "सच"), 820, 900, 90)
    headline(cr, t, "IN REAL LIFE", "IT HAPPENS", t0, T(tl, "b3", "सच"))


def h_parasite(cr, t, tl, t0):                           # b3 "a tiny parasite erases the rat's fear"
    photo(cr, A["rat"], 400, 1230, 420)
    q = prog(t, t0, 0.4)
    parasite(cr, 470, 1060, 150 * q, -0.3, wobble=t * 3, alpha=q)
    ring(cr, 470, 1060, 120, 80, prog(t, t0 + 0.3, 0.4))
    _fear_tag(cr, t, 600, 860, t0, T(tl, "b3", "मिटा"), anchor=(640, 1120))
    headline(cr, t, "A TINY PARASITE", "ERASES ITS FEAR", t0, T(tl, "b3", "मिटा"))


def h_inside_you(cr, t, tl, t0):                         # b4 "and it could be inside you"
    t_you = T(tl, "b4", "तुम्हारे")
    hx, hy = _mq(cr, 520, 1130, 860, bob=False, red=prog(t, t_you + 0.1, 0.3))
    ring(cr, hx, hy, 130, 130, prog(t, t_you + 0.2, 0.4))
    headline(cr, t, "AND IT COULD BE", "INSIDE YOU", t0, t_you, t_ghost=t0)


def h_one_in_three(cr, t, tl, t0):                       # b4 "estimated: 1 in 3 people"
    t3 = T(tl, "b4", "तीन")
    counter(cr, t, t3 - 0.1, 300, 640, "1", 230, color=GOLD)
    draw_text(cr, "IN", 540, 640, 130, INK, prog(t, t3, 0.25), anchor="cm")
    counter(cr, t, t3 + 0.1, 780, 640, "3", 230, color=GOLD)
    icon_array(cr, t, t0 + 0.2, 12, 6, 165, 1060, 120, red=(2, 5, 8, 11), red_at=T(tl, "b4", "इंसान"))
    headline(cr, t, "ESTIMATED:", "1 IN 3 PEOPLE", t0, T(tl, "b4", "इंसान"))
    footnote(cr, "a widely cited worldwide estimate", prog(t, t3, 0.4), y=1530)


def h_name(cr, t, tl, t0):                               # b5 "its name: Toxoplasma gondii"
    _pic(cr, "micro", W / 2, 930, 0, t, t0, rot=-0.02, frame=(760, 640))
    t_n = T(tl, "b5", "टॉक्सो")
    for i, (txt, ty) in enumerate((("TOXOPLASMA", 1320), ("GONDII", 1440))):
        p = prog(t, t_n + 0.35 * i, 0.3)
        if p > 0:
            tw, th = text_size(txt, 96)
            cr.set_source_rgba(*RED, 0.92)
            cr.rectangle(MARGIN, ty - 12, (tw + 50) * p, th + 24)
            cr.fill()
            draw_text(cr, txt, MARGIN + 25, ty, 96, (0.97, 0.94, 0.88), clamp(p * 2 - 1))
    headline(cr, t, "ITS NAME", "", t0, 1e9)


# life cycle
def c_goal(cr, t, tl, t0):                               # b6 "one goal: the cat's gut"
    _pic(cr, "cat", 640, 1100, 700, t, t0)
    parasite(cr, 190, 1460, 160, -0.6, wobble=t * 3)
    path(cr, [(260, 1420), (420, 1300), (600, 1170)], prog(t, T(tl, "b6", "गोल"), 0.8), 7, RED, 0.9, arrow=True)
    if t >= T(tl, "b6", "पेट"):
        ring(cr, 640, 1160, 150, 110, prog(t, T(tl, "b6", "पेट"), 0.4))
    headline(cr, t, "ONE GOAL:", "THE CAT'S GUT", t0, T(tl, "b6", "पेट"), t_ghost=t0 + 0.3)


def c_breeds(cr, t, tl, t0):                             # b7 "it can only breed inside a cat" (inside = slate)
    photo(cr, A["cat"], 560, 1100, 820, alpha=0.35, tint=CREAM, shadow=False)
    n = int(2 + 22 * clamp((t - T(tl, "b7", "बच्चे")) / 1.6))
    for i in range(n):
        a, r = i * 2.4, 25 + 9 * i ** 0.8
        parasite(cr, 560 + r * math.cos(a), 1120 + 0.7 * r * math.sin(a), 70, a, wobble=t * 3 + i)
    headline(cr, t, "IT BREEDS ONLY", "INSIDE CATS", t0, T(tl, "b7", "अंदर"), small_color=CREAM, big_color=CORAL)


def c_eggs(cr, t, tl, t0):                               # b8 "eggs reach soil and water"
    _pic(cr, "soil_closeup", 330, 1250, 0, t, t0, rot=-0.03, frame=(520, 420))
    _pic(cr, "water_puddle", 760, 1330, 0, t, T(tl, "b8", "पानी") - 0.2, rot=0.04, frame=(460, 360))
    for i in range(12):
        tt = t0 + 0.2 + 0.07 * i
        y = drop(t, tt, 1150 + (i % 4) * 40, 0.4, 500)
        if t >= tt:
            x = 150 + (i * 53) % 400 if i % 2 else 600 + (i * 37) % 300
            cr.set_source_rgba(0.96, 0.92, 0.80, 1)
            cr.arc(x, y, 15, 0, 2 * math.pi)
            cr.fill_preserve()
            cr.set_source_rgba(*INK, 0.9)
            cr.set_line_width(4)
            cr.stroke()
    headline(cr, t, "ITS EGGS GO INTO", "SOIL & WATER", t0, T(tl, "b8", "अंडे"))


def c_rat_eats(cr, t, tl, t0):                           # b8 "the rat eats them"
    x = slide(t, t0, -250, 420, 0.7)
    _pic(cr, "rat_sniffing_ground", x, 1250, 340, t, t0, flip=True)

    def lens(c):
        for i in range(5):
            c.set_source_rgba(0.96, 0.92, 0.80, 1)
            c.arc(780 + (i % 3) * 50, 1160 + (i // 3) * 50, 20, 0, 2 * math.pi)
            c.fill_preserve()
            c.set_source_rgba(*INK, 0.9)
            c.set_line_width(4)
            c.stroke()
    magnifier(cr, t, t0 + 0.3, 830, 1190, 190, lens)
    headline(cr, t, "THE RAT", "EATS THEM", t0, T(tl, "b8", "खा"))


def c_to_brain(cr, t, tl, t0):                           # b9 "it travels to the rat's brain" (x-ray)
    photo(cr, A["rat"], 520, 1180, 420, alpha=0.4, tint=CREAM, shadow=False)
    route = [(450, 1250), (560, 1190), (660, 1130), (760, 1090)]
    path(cr, route, prog(t, t0 + 0.2, 1.4), 5, CORAL, 0.9, dash=[12, 10])
    px, py = route[min(3, int(4 * prog(t, t0 + 0.2, 1.4)))]
    parasite(cr, px, py - 30, 90, -0.3, wobble=t * 4)
    ring(cr, 760, 1090, 110, 90, prog(t, T(tl, "b9", "दिमाग़"), 0.4), color=CORAL)
    headline(cr, t, "STRAIGHT TO THE", "BRAIN", t0, T(tl, "b9", "दिमाग़"), small_color=CREAM, big_color=CORAL)


def c_cysts(cr, t, tl, t0):                              # b9 "...makes small cysts and hides"
    p = prog(t, t0, 0.4)
    _brain(cr, 540, 1080, 2.0 * (0.92 + 0.08 * p), p)
    for i, (x, y) in enumerate([(400, 1020), (560, 920), (700, 1050), (500, 1150), (760, 940)]):
        q = prog(t, T(tl, "b9", "सिस्ट्स") + 0.12 * i, 0.3)
        if q > 0:
            cyst(cr, x, y, 46 * q, t, q, n=8)
    _pic(cr, "cyst", 760, 1450, 0, t, T(tl, "b9", "छुप"), rot=0.03, frame=(400, 300))
    card(cr, t, T(tl, "b9", "छुप") + 0.3, 90, 1390, ["TISSUE CYST", "REAL · USDA"], size=34)
    headline(cr, t, "IT HIDES IN", "CYSTS", t0, T(tl, "b9", "सिस्ट्स"))


# fear
def f_normal(cr, t, tl, t0):                             # b10 "a normal rat smells cat urine and runs"
    _scent(cr, 830, 1100, t, prog(t, t0, 0.3))
    card(cr, t, t0 + 0.3, 640, 1390, ["CAT URINE"], size=40)
    run = prog(t, T(tl, "b10", "भाग"), 0.6)
    _pic(cr, "rat_running", 420 - 300 * run, 1180, 300, t, t0)
    headline(cr, t, "NORMAL RAT:", "RUNS", t0, T(tl, "b10", "भाग"))


def f_born(cr, t, tl, t0):                               # b10 "...this fear is in it from birth"
    photo(cr, A["rat"], 380, 1200, 400)
    _fear_tag(cr, t, 560, 850, t0, anchor=(600, 1100))
    ring(cr, 380, 1200, 260, 200, prog(t, T(tl, "b10", "जन्म"), 0.5))
    headline(cr, t, "BORN WITH", "THIS FEAR", t0, T(tl, "b10", "जन्म"))


def f_infected(cr, t, tl, t0):                           # b11 "an infected rat isn't scared at all"
    _scent(cr, 830, 1100, t, 1.0)
    rx = 330 + 160 * prog(t, t0 + 0.6, 1.2)
    photo(cr, A["rat"], rx, 1220, 380)
    parasite(cr, rx + 70, 1100, 70, wobble=t * 3)
    _fear_tag(cr, t, rx - 60, 860, t0, T(tl, "b11", "डरता"), size=88, anchor=(rx + 170, 1110))
    stamp(cr, t, "INFECTED", T(tl, "b11", "इन्फ़ेक्टेड"), 330, 1480, 58)
    headline(cr, t, "INFECTED RAT:", "NO FEAR", t0, T(tl, "b11", "डरता"))


def f_oxford(cr, t, tl, t0):                             # b12 "an experiment at Oxford"
    _pic(cr, "oxford_university", W / 2, 1000, 0, t, t0, rot=-0.02, frame=(860, 600))
    card(cr, t, t0 + 0.4, 120, 1400, ["OXFORD · 2000", "BERDOY, WEBSTER & MACDONALD"], size=34)
    headline(cr, t, "AN EXPERIMENT AT", "OXFORD", t0, t0 + 0.3)


def f_corner(cr, t, tl, t0):                             # b12 "infected rats spent more time in the cat corner"
    x0, y0, s = 150, 640, 780
    p = prog(t, t0, 0.4)
    cr.set_source_rgba(*INK, 0.9 * p)
    cr.set_line_width(8)
    cr.rectangle(x0, y0, s, s)
    cr.stroke()
    t_cat = T(tl, "b12", "टाइम")
    for cx, cy, name in [(x0 + 110, y0 + 110, "RAT"), (x0 + s - 110, y0 + 110, "NEUTRAL"),
                         (x0 + 110, y0 + s - 110, "RABBIT"), (x0 + s - 110, y0 + s - 110, "CAT")]:
        cat = name == "CAT"
        if cat and t >= t_cat:
            cr.set_source_rgba(*RED, 0.25 * prog(t, t_cat, 0.6))
            cr.arc(cx, cy, 120, 0, 2 * math.pi)
            cr.fill()
        cr.set_source_rgba(*(RED if cat else INK), 0.85 * p)
        cr.set_line_width(5)
        cr.arc(cx, cy, 70, 0, 2 * math.pi)
        cr.stroke()
        below = cy < y0 + s / 2
        draw_text(cr, name, cx, cy + (92 if below else -92), 42, RED if cat else INK, p, anchor="ct" if below else "cb")
    cx, cy = x0 + s - 110, y0 + s - 110
    route = [(x0 + s / 2, y0 + s / 2), (x0 + 260, y0 + 330), (x0 + 420, y0 + 600)]
    route += [(cx + 75 * math.cos(a), cy + 75 * math.sin(a)) for a in [3.6 + 0.5 * k for k in range(22)]]
    path(cr, route, prog(t, t0 + 0.3, 2.4), 5, INK, 0.75)
    _pic(cr, "stopwatch", 860, 1520, 260, t, t_cat)
    headline(cr, t, "MORE TIME IN THE", "CAT CORNER", t0, T(tl, "b12", "बिल्ली"))


def f_fatal(cr, t, tl, t0):                              # b13 "scientists called it: fatal attraction"
    pull = prog(t, T(tl, "b13", "अट्रैक्शन"), 1.2)
    _pic(cr, "cat", 900, 1230, 430, t, t0)
    _pic(cr, "magnet_horseshoe", 610, 1150, 170, t, t0 + 0.2, flip=True)
    rx = 170 + 120 * pull
    photo(cr, A["rat"], rx, 1330, 240)
    for i in range(3):                                          # pull lines
        path(cr, [(rx + 170, 1300 - 30 * i), (515, 1120 + 25 * i)], prog(t, t0 + 0.5, 0.4), 4, RED, 0.6, dash=[10, 10])
    headline(cr, t, "THEY CALLED IT", "FATAL ATTRACTION", t0, T(tl, "b13", "फ़ेटल"), big_size=130)
    card(cr, t, T(tl, "b13", "जानलेवा"), 130, 1520, ["JAANLEVA AAKARSHAN"], size=38)


# the precision beat (study section 3: "everything is precise" -> awe), sources Vyas 2007, House 2011
def p_strangest(cr, t, tl, t0):                          # b14 "and the most surprising part?"
    photo(cr, A["rat"], 480, 1250, 460)

    def inner(c):
        _brain(c, 720, 1050, 0.9)
    magnifier(cr, t, t0 + 0.2, 720, 1050, 210, inner)
    headline(cr, t, "THE STRANGEST", "PART", t0, t0 + 0.5, t_ghost=t0)


def p_fears(cr, t, tl, t0):                              # b14 "all other fears stay... other predators, open spaces"
    t_p, t_o, t_c = T(tl, "b14", "शिकारियों"), T(tl, "b14", "खुली"), T(tl, "b14", "मिटता")
    _checklist(cr, t, 110, 560, 860, "THE RAT'S FEARS",
               [("PREDATORS", t0 + 0.1, "tick", t_p), ("OPEN SPACE", t_o - 0.2, "tick", t_o + 0.2),
                ("CATS", t_o + 0.4, "erase", t_c + 0.2)])
    if t >= t_c:
        headline(cr, t, "ERASED:", "ONLY CATS", t_c, t_c + 0.3)
        stamp(cr, t, "ONLY THIS ONE", t_c + 1.0, 700, 1300, 50, rot=-0.08)
    else:
        headline(cr, t, "EVERY OTHER FEAR", "STAYS", t0, t_p - 0.3)
    footnote(cr, "Vyas et al. 2007, PNAS · House, Vyas & Sapolsky 2011, PLoS ONE", prog(t, t_p, 0.4), y=1530)


# the loop
def l_walks(cr, t, tl, t0):                              # b15 "the rat goes to the cat"
    photo(cr, A["cat"], 850, 1190, 460)
    x = 160 + 160 * prog(t, t0, 1.6)
    photo(cr, A["rat"], x, 1340 - 8 * abs(math.sin(t * 12)), 280)
    path(cr, [(x + 150, 1430), (560, 1430)], prog(t, t0 + 0.2, 0.6), 6, RED, 0.85, dash=[16, 12], arrow=True)
    headline(cr, t, "THE RAT", "WALKS IN", t0, t0 + 0.4)


def l_eaten(cr, t, tl, t0):                              # b15 "the cat eats it"
    t_e = T(tl, "b15", "उसे")
    cx = slide(t, t_e - 0.1, 850, 640, 0.25)
    rx, ry, rot, a = knock(t, t_e + 0.1, 360, 1340, dx=-500, dy=500, spin=-1.5)
    photo(cr, A["rat"], rx, ry, 260, alpha=a, rot=rot)
    photo(cr, A["cat"], cx, 1190, 520)
    cross(cr, 360, 1340, 200, prog(t, t_e + 0.35, 0.3))
    headline(cr, t, "THE CAT", "EATS IT", t0, t_e)


def l_cycle(cr, t, tl, t0):                              # b15 "the parasite reaches its destination"
    pts = [(260, 900), (820, 900), (540, 1450)]
    photo(cr, A["rat"], *pts[0], 220, alpha=prog(t, t0, 0.3))
    photo(cr, A["cat"], pts[1][0], pts[1][1] - 20, 380, alpha=prog(t, t0 + 0.1, 0.3))
    parasite(cr, *pts[2], 180, wobble=t * 3, alpha=prog(t, t0 + 0.2, 0.3))
    path(cr, [(380, 880), (680, 880)], prog(t, t0 + 0.2, 0.5), 7, RED, 0.9, arrow=True)
    path(cr, [(800, 1080), (630, 1380)], prog(t, t0 + 0.6, 0.5), 7, RED, 0.9, arrow=True)
    path(cr, [(450, 1380), (280, 1030)], prog(t, t0 + 1.0, 0.5), 7, RED, 0.9, arrow=True)
    headline(cr, t, "MISSION", "COMPLETE", t0, T(tl, "b15", "मंज़िल"))


# humans
def u_humans(cr, t, tl, t0):                             # b16 "if it's inside humans too..."
    _pic(cr, "people_crowd_india", W / 2, 1050, 0, t, t0, rot=0.02, frame=(900, 620))
    headline(cr, t, "AND IF IT'S IN", "HUMANS?", t0, T(tl, "b16", "इंसानों"), t_ghost=t0 + 0.2)


def u_our_brain(cr, t, tl, t0):                          # b16 "...does it do something to our brain?"
    p = prog(t, t0, 0.4)
    head_profile(cr, 520, 1180, 900 * (0.95 + 0.05 * p), INK, p)
    q = prog(t, T(tl, "b16", "हमारे"), 0.3)
    draw_text(cr, "?", 560, 1060, 360 * (0.8 + 0.2 * q), RED, q, anchor="cm")
    headline(cr, t, "DOES IT CHANGE", "OUR BRAIN?", t0, T(tl, "b16", "हमारे"))


def u_tissues(cr, t, tl, t0):                            # b17 "in humans it can sit in the brain and muscles"
    _pic(cr, "gray_anatomy_brain", 300, 1080, 0, t, t0, rot=-0.03, frame=(440, 520))
    _pic(cr, "gray_anatomy_muscles", 780, 1100, 0, t, T(tl, "b17", "मसल्स") - 0.2, rot=0.03, frame=(400, 560))
    for i, (x, y, tt) in enumerate([(300, 1020, t0 + 0.5), (820, 1060, T(tl, "b17", "मसल्स") + 0.2)]):
        q = prog(t, tt, 0.3)
        if q > 0:
            cyst(cr, x, y, 50 * q, t, q, n=8)
    footnote(cr, "engravings: Sobotta's Atlas of Human Anatomy (1909), public domain", prog(t, t0, 0.4), y=1530)
    headline(cr, t, "BRAIN AND", "MUSCLES", t0, T(tl, "b17", "मसल्स"))


def u_years(cr, t, tl, t0):                              # b17 "...asleep for years"
    calendar(cr, t, t0 + 0.2, 330, 1150, ["YEAR 1", "YEAR 2", "YEAR 5", "YEAR 10", "YEAR 20"], "ASLEEP", interval=0.35)
    for i, (x, y) in enumerate([(760, 1050), (840, 1210)]):
        cyst(cr, x, y, 60, t, prog(t, t0, 0.3), n=8)
        zz = (t * 0.8 + i * 0.3) % 1.0
        draw_text(cr, "z", x + 50 + 30 * zz, y - 60 - 60 * zz, 46, INK, 1 - zz, anchor="cm")
    headline(cr, t, "ASLEEP FOR", "YEARS", t0, T(tl, "b17", "सालों"))


def u_never_know(cr, t, tl, t0):                         # b17 "most people never find out"
    icon_array(cr, t, t0, 12, 6, 165, 1000, 120)
    card(cr, t, t0 + 0.6, 170, 1420, ["MOST HAVE NO SYMPTOMS"], size=40)
    headline(cr, t, "MOST PEOPLE", "NEVER KNOW", t0, t0 + 0.4)


def u_studies(cr, t, tl, t0):                            # b18 "some studies saw behaviour differences"
    _pic(cr, "research_papers_stack", W / 2, 1150, 620, t, t0)
    headline(cr, t, "SOME STUDIES SAY:", "BEHAVIOUR?", t0, T(tl, "b18", "बिहेवियर"))


def u_debate(cr, t, tl, t0):                             # b18 "not proof... still debated"
    tilt = 0.12 * math.sin((t - t0) * 2.2)
    _pic(cr, "balance_scale", W / 2, 1150, 640, t, t0, rot=tilt)
    stamp(cr, t, "NOT PROVEN", T(tl, "b18", "प्रूफ़") - 0.1, W / 2, 900, 80, rot=-0.1)
    headline(cr, t, "NOT PROVEN.", "STILL DEBATED", T(tl, "b18", "प्रूफ़") - 0.2, T(tl, "b18", "डिबेट"))


# how people get it, pregnancy, the rules
def s_not_cat(cr, t, tl, t0):                            # b19 "usually not from the cat"
    _pic(cr, "cat_sitting_front", W / 2, 1150, 640, t, t0)
    cross(cr, W / 2, 1150, 420, prog(t, T(tl, "b19", "बिल्ली") + 0.2, 0.4))
    headline(cr, t, "USUALLY", "NOT THE CAT", t0, T(tl, "b19", "बिल्ली"))


def s_meat(cr, t, tl, t0):                               # b19 "...raw or undercooked meat"
    _pic(cr, "raw_chicken_or_meat_plate", W / 2, 1150, 560, t, t0)
    ring(cr, W / 2, 1150, 380, 260, prog(t, t0 + 0.4, 0.5))
    headline(cr, t, "RAW OR UNDERCOOKED", "MEAT", t0, t0 + 0.4)


def s_veg(cr, t, tl, t0):                                # b19 "...unwashed fruit and vegetables"
    _pic(cr, "veg", W / 2, 1150, 440, t, t0)
    for i in range(14):                                       # soil specks still on them
        cr.set_source_rgba(0.35, 0.25, 0.15, 0.8 * prog(t, t0 + 0.3 + 0.03 * i, 0.2))
        cr.arc(330 + (i * 97) % 420, 1000 + (i * 61) % 300, 8, 0, 2 * math.pi)
        cr.fill()
    headline(cr, t, "UNWASHED", "VEGETABLES", t0, T(tl, "b19", "धुले"))


def s_danger(cr, t, tl, t0):                             # b20 "one place it really is dangerous: pregnancy"
    _pic(cr, "warning_sign", 790, 860, 300, t, t0, rot=0.05)
    _pic(cr, "pregnant_woman_silhouette", 400, 1150, 920, t, t0 + 0.2)
    headline(cr, t, "ONE REAL DANGER:", "PREGNANCY", t0, T(tl, "b20", "प्रेग्नेंसी"))


def s_baby(cr, t, tl, t0):                               # b20 "first infection in pregnancy can reach the baby"
    _pic(cr, "ultrasound_scan", W / 2, 1050, 0, t, t0, rot=-0.02, frame=(820, 620))
    ring(cr, W / 2, 1050, 260, 200, prog(t, T(tl, "b20", "बच्चे"), 0.5))
    card(cr, t, t0 + 0.3, 110, 1430, ["FIRST INFECTION", "DURING PREGNANCY"], size=36)
    headline(cr, t, "IT CAN REACH", "THE BABY", t0, T(tl, "b20", "बच्चे"))


def s_rules(cr, t, tl, t0):                              # b21 the doctors' three rules, one picture per rule
    cues = [T(tl, "b21", "लिटर"), T(tl, "b21", "मीट"), T(tl, "b21", "सब्ज़ी")]
    k = max([0] + [i for i, c in enumerate(cues) if t >= c - 0.3])
    key = ("litter_box_with_scoop", "cooking_meat_pan", "washing_vegetables_tap")[k]
    _pic(cr, key, W / 2, 1380, 420, t, t0 if k == 0 else cues[k] - 0.3,
         frame=(620, 420) if key.startswith("washing") else None)
    if k == 0:
        _pic(cr, "litter_scoop", 820, 1420, 300, t, cues[0], rot=0.3)
    for i, (txt, c) in enumerate(zip(("LITTER BOX: NOT YOU", "COOK MEAT WELL", "WASH VEGETABLES"), cues)):
        y = 650 + 120 * i
        p = prog(t, c - 0.3, 0.3)
        cr.set_source_rgba(*INK, 0.85 * prog(t, t0 + 0.15 * i, 0.3))
        cr.set_line_width(6)
        cr.rectangle(MARGIN + 10, y - 40, 80, 80)
        cr.stroke()
        draw_text(cr, txt, MARGIN + 130, y, 60, INK, p, anchor="lm")
        tick(cr, MARGIN + 20, y - 5, 72, prog(t, c + 0.3, 0.35))
    headline(cr, t, "IN PREGNANCY:", "3 RULES", t0, T(tl, "b21", "प्रेग्नेंसी"))


def s_not_wrong(cr, t, tl, t0):                          # b22 "keeping a cat is not wrong" (green = reassurance)
    _pic(cr, "kitten_or_cat_indian_home", W / 2, 1080, 0, t, t0, rot=0.02, frame=(840, 680))
    tick(cr, 780, 1400, 160, prog(t, T(tl, "b22", "ग़लत"), 0.4), color=GREEN)
    headline(cr, t, "A PET CAT IS", "NOT WRONG", t0, T(tl, "b22", "ग़लत"), big_color=GREEN)


def s_low_risk(cr, t, tl, t0):                           # b22 "indoor cat, no raw meat: low chance"
    _pic(cr, "cat_indoor", 300, 1180, 380, t, t0)
    _pic(cr, "cat_food_bowl", 300, 1420, 170, t, T(tl, "b22", "कच्चा"))
    gauge(cr, t, T(tl, "b22", "कम") - 0.3, 790, 1120, 180, 0.75, 0.12)
    headline(cr, t, "INDOOR CAT, NO RAW MEAT:", "LOW RISK", t0, T(tl, "b22", "कम"), big_color=GREEN)


# the "socho" bookend + the YES/NO card (study section 4)
def e_one_cell(cr, t, tl, t0):                           # b23 "socho: a single-celled creature you can't even see"
    _pic(cr, "microscope", 320, 1150, 700, t, t0)

    def inner(c):
        parasite(c, 760, 1050, 170, -0.4, wobble=t * 3)
    magnifier(cr, t, T(tl, "b23", "सेल") - 0.1, 760, 1050, 220, inner)
    headline(cr, t, "ONE CELL.", "INVISIBLE.", t0, T(tl, "b23", "आँख"), t_ghost=t0 + 0.2)


def e_erases(cr, t, tl, t0):                             # b23 "...erases the fear the rat was born with"
    photo(cr, A["rat"], 420, 1260, 440)
    erase(cr, t, T(tl, "b23", "मिटा"), "FEAR", 560, 820, 170, RED, dur=0.9, eraser=B["eraser"], anchor="lm")
    ring(cr, 420, 1260, 280, 220, prog(t, T(tl, "b23", "जन्म"), 0.5))
    headline(cr, t, "IT ERASES", "AN INSTINCT", t0, T(tl, "b23", "जन्म"))


def e_question(cr, t, tl, t0):                           # b24 "is there a cat in your home? tell me in the comments"
    _pic(cr, "cat_indoor", 300, 1330, 380, t, t0, rot=-0.04)
    yes_no_card(cr, t, t0 + 0.4, 640, 980, w=640, h=300, question="COMMENT: YES OR NO")
    headline(cr, t, "A CAT IN", "YOUR HOME?", t0, T(tl, "b24", "बिल्ली"), t_ghost=t0)


SHOTS = [   # (line, cue where the shot starts, draw function, background)
    ("b1", None, h_you, "paper"), ("b1", "ख़ुद", h_walk, "paper"),
    ("b2", None, h_cartoon, "paper"), ("b2", "पर", h_fiction, "paper"),
    ("b3", None, h_real, "paper"), ("b3", "एक", h_parasite, "paper"),
    ("b4", None, h_inside_you, "paper"), ("b4", "अंदाज़ा", h_one_in_three, "paper"),
    ("b5", None, h_name, "paper"),
    ("b6", None, c_goal, "paper"), ("b7", None, c_breeds, "slate"),
    ("b8", None, c_eggs, "paper"), ("b8", "चूहा", c_rat_eats, "paper"),
    ("b9", None, c_to_brain, "slate"), ("b9", "वहाँ", c_cysts, "paper"),
    ("b10", None, f_normal, "paper"), ("b10", "ये", f_born, "paper"), ("b11", None, f_infected, "paper"),
    ("b12", None, f_oxford, "paper"), ("b12", "इन्फ़ेक्टेड", f_corner, "paper"),
    ("b13", None, f_fatal, "paper"),
    ("b14", None, p_strangest, "paper"), ("b14", "बाक़ी", p_fears, "paper"),
    ("b15", None, l_walks, "paper"), ("b15", "उसे", l_eaten, "paper"), ("b15", "पैरासाइट", l_cycle, "paper"),
    ("b16", None, u_humans, "paper"), ("b16", "तो क्या", u_our_brain, "paper"),
    ("b17", None, u_tissues, "paper"), ("b17", "सालों", u_years, "paper"), ("b17", "ज़्यादातर", u_never_know, "paper"),
    ("b18", None, u_studies, "paper"), ("b18", "पर", u_debate, "paper"),
    ("b19", None, s_not_cat, "paper"), ("b19", "कच्चे", s_meat, "paper"), ("b19", "धुले", s_veg, "paper"),
    ("b20", None, s_danger, "paper"), ("b20", "अगर", s_baby, "paper"),
    ("b21", None, s_rules, "paper"),
    ("b22", None, s_not_wrong, "paper"), ("b22", "जो", s_low_risk, "paper"),
    ("b23", None, e_one_cell, "paper"), ("b23", "वो", e_erases, "paper"),
    ("b24", None, e_question, "paper"),
]


def _starts(tl):
    out = []
    for k, (bid, cue, _, _) in enumerate(SHOTS):
        if k == 0:
            out.append(0.0)
            continue
        s = T(tl, bid, cue)
        if cue is not None:
            s -= 0.12                                            # cut just before the word lands
        out.append(max(s, out[-1] + 0.5))
    return out


def _shot_at(t, tl):
    starts = getattr(tl, "_shot_starts", None)
    if starts is None:
        starts = tl._shot_starts = _starts(tl)
    k = max(i for i, s in enumerate(starts) if t >= s)
    return k, starts[k], starts[k + 1] if k + 1 < len(starts) else tl.total


def draw(cr, t, tl):
    k, t0, t1 = _shot_at(t, tl)
    _, _, fn, bg = SHOTS[k]
    if bg == "slate":
        slate(cr)
    else:
        paper(cr, seed=1 + k % 3)
    cr.save()
    push(cr, t, t0, t1, 1.0, 1.04)
    fn(cr, t, tl, t0)
    cr.restore()
    rule(cr, color=CREAM if bg == "slate" else INK)
    finish(cr)


def sfx(tl):
    """Small sounds on the turning points: a whoosh on every cut, a scribble when FEAR is erased, thuds on stamps,
    a tick before the precision re-hook and the closing line."""
    starts = _starts(tl)
    ev = [(s, "whoosh", 0.25) for s in starts[1:]]
    ev += [(T(tl, "b1", "मिटा"), "scribble", 0.6), (T(tl, "b3", "मिटा"), "scribble", 0.6),
           (T(tl, "b11", "डरता"), "scribble", 0.6), (T(tl, "b14", "मिटता") + 0.2, "scribble", 0.6),
           (T(tl, "b23", "मिटा"), "scribble", 0.7),
           (T(tl, "b3", "सच"), "thud", 0.0), (T(tl, "b18", "प्रूफ़") - 0.1, "thud", 0.0),
           (T(tl, "b14", None) - 0.35, "tick", 0.0), (T(tl, "b23", None) - 0.35, "tick", 0.0),
           (T(tl, "b24", "कमेंट"), "typing", 1.0)]
    for bid in ("b5", "b7", "b9", "b12", "b17", "b20"):
        ev.append((tl[bid].start + 0.4, "pop", 0.0))
    return ev
