"""Video 3: "Ye saanp sote hue kaatta hai" (common krait, snakebite in India). v2 of the script approved on
29 Oct 2026, approved again as v2 ("Approve both"; scripts_batch2.md, video 3); narration below is that script word
for word, in Devanagari for the voice, with numbers written as words."""
import math
import os

from poster import (CORAL, CREAM, GOLD, GREEN, INK, MARGIN, RED, W, calendar, card, clamp, counter, cross, draw_text,
                    footnote, headline, magnifier, path, person, photo, prog, ring, stamp, strike, text_size, tick,
                    yes_no_card)

# the narrator, music and tail are channel-wide; render_hi reads them from this module
from channel import ASSETS_ROOT, MUSIC, NARRATOR, NARRATOR_LABEL, REVEAL_GAP, TAIL, VOICE_REF  # noqa: F401
from shots import T, asset_finder, checklist, draw_frame, pic, screen, starts, tv

SCRIPT = [
    dict(id="b1", text="सोचो, तुम रात को ज़मीन पर सो रहे हो... एक साँप आता है, काट के चला जाता है... "
                       "और तुम्हें पता भी नहीं चलता। क्योंकि दर्द होता ही नहीं।"),
    dict(id="b2", text="फिर कुछ घंटों में पलकें भारी होने लगती हैं... और धीरे-धीरे साँस लेने वाली मसल्स काम करना बंद कर देती हैं।"),
    dict(id="b3", text="टीवी सीरियल में नागिन बदला लेती है, और सब उसे देख लेते हैं। पर असली ज़िंदगी में, "
                       "भारत के सबसे ख़तरनाक साँपों में से एक, अक्सर दिखता भी नहीं।", gap=REVEAL_GAP),
    dict(id="b4", text="इसका नाम है कॉमन क्रेट। कई जगह लोग इसे करैत कहते हैं।"),
    dict(id="b5", text="भारत में हर साल लगभग अट्ठावन हज़ार लोग साँप के काटने से मरते हैं। मतलब हर दिन लगभग एक सौ साठ लोग। "
                       "दुनिया में सबसे ज़्यादा।"),
    dict(id="b6", text="ज़्यादातर मौत चार साँपों से होती है: कोबरा, क्रेट, रसेल्स वाइपर और सॉ-स्केल्ड वाइपर। "
                       "इन्हें बिग फ़ोर कहते हैं।"),
    dict(id="b7", text="क्रेट रात को निकलता है। बारिश के मौसम में ये घरों में घुस आता है, और ज़मीन पर सोते लोगों को काट लेता है।"),
    dict(id="b8", text="इसके दाँत इतने छोटे होते हैं कि निशान अक्सर मुश्किल से दिखता है। न सूजन, न दर्द।", gap=REVEAL_GAP),
    dict(id="b9", text="और सबसे हैरानी की बात? इसका ज़हर नर्व्स पर हमला करता है। "
                       "दिमाग़ का सिग्नल मसल्स तक पहुँचने ही नहीं देता।"),
    dict(id="b10", text="पहले पलकें गिरती हैं। फिर निगलना मुश्किल होता है। फिर साँस की मसल्स रुक जाती हैं।"),
    dict(id="b11", text="पर इसका इलाज, एंटी-वेनम, भारत में ही बनता है। तो इतने लोग मरते क्यों हैं?"),
    dict(id="b12", text="क्योंकि ज़्यादातर मौत घर पर ही होती है। लोग हॉस्पिटल टाइम पर पहुँचते ही नहीं।"),
    dict(id="b13", text="कई लोग पहले झाड़-फूँक के पास जाते हैं। कुछ लोग ज़ख़्म काट के ज़हर चूसने की कोशिश करते हैं, "
                        "या रस्सी से कस के बाँध देते हैं।"),
    dict(id="b14", text="ये सब ग़लत है, और क़ीमती वक़्त बर्बाद करता है।"),
    dict(id="b15", text="अगर साँप काटे: घबराओ मत। जिस हाथ या पैर पर काटा है, उसे हिलाओ मत, सीधा रखो।"),
    dict(id="b16", text="अंगूठी, घड़ी और टाइट कपड़े निकाल दो। और तुरंत उस हॉस्पिटल जाओ जहाँ एंटी-वेनम हो। "
                        "एक सौ आठ पर कॉल कर सकते हो।"),
    dict(id="b17", text="और रात को कुछ काटे, तो दर्द न हो तब भी हॉस्पिटल जाओ। क्रेट का काटा दर्द नहीं देता।"),
    dict(id="b18", text="और अगर ज़मीन पर सोते हो, तो मच्छरदानी लगा के सो। नेपाल की एक स्टडी में, "
                        "मच्छरदानी के अंदर सोने वालों को साँप कम काटे।", gap=REVEAL_GAP),
    dict(id="b19", text="सोचो, एक साँप जिसका काटा दर्द भी नहीं देता... और इसी वजह से लोग हॉस्पिटल जाते ही नहीं।"),
    dict(id="b20", text="तुम्हारे घर या गाँव के पास कभी साँप निकला है? यस या नो, कमेंट में बताओ।"),
]

METADATA = dict(
    title="Ye saanp sote hue kaatta hai",
    caption="Ye saanp sote hue kaatta hai aur dard bhi nahi hota... Bharat mein roz ~160 log saanp ke kaatne se "
            "marte hain 😳\n\n"
            "Saanp kaate toh:\n✅ Ghabraao mat, kaata hua haath ya pair seedha aur sthir rakho\n"
            "✅ Ring, ghadi aur tight kapde nikaalo\n✅ Turant anti-venom wale hospital jao, 108 call karo\n"
            "❌ Kaatna, choosna, rassi se baandhna, jhaad-phoonk: sab galat\n"
            "❌ Dard nahi hai, toh bhi ignore mat karo\n\n"
            "Zameen par sote ho toh machhardaani lagao.\n\n"
            "Tumhare ghar ya gaon ke paas kabhi saanp nikla hai? Comment mein YES ya NO likho 👇",
    yt_title="Ye Saanp Sote Hue Kaatta Hai, Dard Bhi Nahi Hota 😳 | Krait",
    yt_description="Common krait raat ko zameen par sote logon ko kaatta hai, aur kaata dard bhi nahi deta. Bharat mein "
                   "har saal lagbhag 58,000 log saanp ke kaatne se marte hain. Saanp kaate toh kya karein, aur kya "
                   "bilkul na karein.\n\nSaanp kaate toh:\n✅ Ghabraao mat, kaata hua hissa seedha aur sthir rakho\n"
                   "✅ Ring, ghadi aur tight kapde nikaalo\n✅ Turant anti-venom wale hospital jao, 108 call karo\n"
                   "❌ Kaatna, choosna, rassi se baandhna, jhaad-phoonk: sab galat",
    hashtags=["#snake", "#krait", "#snakebite", "#factsinhindi", "#sciencefacts"],
    pinned_comment="Tumhare ghar ya gaon ke paas kabhi saanp nikla hai? 🐍 YES ya NO? 👇",
    sources=["Suraweera et al. 2020, eLife",
             "MoHFW Standard Treatment Guidelines, snakebite",
             "WHO SEARO, Guidelines for the management of snakebites, 2nd edition",
             "Indian common krait bite review, Chandigarh",
             "Chappuis et al. 2007, American Journal of Tropical Medicine and Hygiene"],
)

_find = asset_finder("krait", "krait2", "toxoplasma2")
P = {k: _find(k) for k in ("krait_3", "krait_2", "cobra_1", "russells_viper_1", "saw_scaled_viper_2",
                           "antivenom_vial_1", "mosquito_net_1", "floor_mat_1", "old_tv", "sleeping_person",
                           "india_map", "village_house_night", "monsoon_rain", "skin_closeup", "hospital",
                           "ambulance", "rope", "kitchen_knife", "wristwatch", "finger_ring", "eye_closeup",
                           "lungs_engraving", "clock", "gray_anatomy_brain", "gray_anatomy_muscles_alt_sobotta")}
USED_ASSETS = [os.path.basename(v) for v in P.values() if v]
CREDITS_FILES = [os.path.join(ASSETS_ROOT, d, "credits.json") for d in ("krait", "krait2", "toxoplasma2")]
NIGHT = (0.10, 0.12, 0.20)


def _pic(cr, key, cx, cy, h, t, t0, **kw):
    pic(cr, P.get(key), cx, cy, h, t, t0, **kw)


# ---------- drawing pieces for this video ----------

def sleeper(cr, t, x, y, alpha=1.0):
    """Someone asleep on a floor mat: the mat, the sleeping figure and drifting z's."""
    _pic(cr, "floor_mat_1", x, y + 40, 360, t, -1, alpha=alpha)
    if P["sleeping_person"]:
        photo(cr, P["sleeping_person"], x, y - 40, 260, alpha=alpha)
    else:
        cr.save()
        cr.translate(x + 210, y)                                       # lying down, head to the left, on the mat
        cr.rotate(-math.pi / 2)
        person(cr, 0, 0, 420, INK, 0.85 * alpha)
        cr.restore()
    for i in range(3):
        f = (t * 0.7 + i / 3) % 1.0
        draw_text(cr, "z", x + 150 + 40 * f, y - 180 - 120 * f, 50 + 20 * i, INK, alpha * (1 - f), anchor="cm")


def rain(cr, t, alpha=1.0):
    cr.set_source_rgba(0.75, 0.82, 0.95, 0.55 * alpha)
    cr.set_line_width(3)
    for i in range(70):
        x = (i * 157 + 400 * t) % (W + 200) - 100
        y = (i * 263 + 1600 * t) % 1500 + 300
        cr.move_to(x, y)
        cr.line_to(x - 18, y + 60)
    cr.stroke()


def nerve(cr, t, t0, t_block, x0, x1, y, alpha=1.0):
    """A nerve line carrying signal dots toward a muscle block; from t_block a red barrier stops them."""
    path(cr, [(x0, y), (x1 - 160, y)], 1.0, 10, CREAM, 0.8 * alpha)
    cr.set_source_rgba(0.80, 0.42, 0.40, alpha)                       # the muscle
    cr.rectangle(x1 - 150, y - 110, 150, 220)
    cr.fill()
    draw_text(cr, "MUSCLE", x1 - 75, y + 130, 36, CREAM, alpha, anchor="ct")
    draw_text(cr, "NERVE", x0, y - 40, 36, CREAM, alpha, anchor="lb")
    blocked = t >= t_block
    wall = x1 - 300
    for i in range(6):
        f = ((t - t0) * 0.8 + i / 6) % 1.0
        x = x0 + (x1 - 160 - x0) * f
        if blocked and x > wall - 20:
            x = wall - 20 - 25 * i
        cr.set_source_rgba(*(CORAL if blocked else GOLD), alpha)
        cr.arc(x, y, 14, 0, 2 * math.pi)
        cr.fill()
    if blocked:
        p = prog(t, t_block, 0.3)
        cr.set_source_rgba(*RED, 0.9 * p * alpha)
        cr.rectangle(wall, y - 120 * p, 22, 240 * p)
        cr.fill()


# ---------- shots ----------
# Rules (style bible + parasite-reels study): a new picture every ~3-4 s cut on the word, the literal noun on screen,
# red = threat, green = what to do / reassurance, gold = numbers, dark slate for inside the body.

def h_snake(cr, t, tl, t0):                              # b1 frame 0: "socho, you're asleep on the floor..."
    _pic(cr, "krait_3", W / 2, 1100, 420, t, -1)
    headline(cr, t, "IT BITES WHILE YOU", "SLEEP", -1, min(1.2, T(tl, "b1", "रहे")), t_ghost=-1)   # "सो" would match "सोचो"


def h_comes(cr, t, tl, t0):                              # b1 "...a snake comes, bites and leaves"
    sleeper(cr, t, 380, 1200)
    x = 1200 - 520 * prog(t, t0, 1.6)
    _pic(cr, "krait_2", x, 1330, 150, t, -1, flip=True)
    headline(cr, t, "A SNAKE COMES,", "BITES, LEAVES", t0, T(tl, "b1", "काट"))


def h_no_pain(cr, t, tl, t0):                            # b1 "...you don't even know. Because there's no pain."
    sleeper(cr, t, W / 2, 1200)
    stamp(cr, t, "NO PAIN", T(tl, "b1", "दर्द"), W / 2, 900, 90)
    headline(cr, t, "YOU DON'T EVEN", "FEEL IT", t0, T(tl, "b1", "पता"))


def h_eyelids(cr, t, tl, t0):                            # b2 "hours later the eyelids get heavy..."
    _pic(cr, "eye_closeup", W / 2, 1050, 0, t, t0, frame=(860, 520))
    p = prog(t, t0 + 0.6, 2.0)                                       # the upper lid drooping over the photo
    cr.save()
    cr.rectangle(W / 2 - 430, 790, 860, 520)
    cr.clip()
    cr.move_to(W / 2 - 430, 790)
    cr.line_to(W / 2 + 430, 790)
    cr.line_to(W / 2 + 430, 800 + 120 * p)
    cr.curve_to(W / 2 + 200, 860 + 220 * p, W / 2 - 200, 860 + 220 * p, W / 2 - 430, 800 + 120 * p)
    cr.close_path()
    cr.set_source_rgba(0.62, 0.45, 0.36, 0.93)
    cr.fill()
    cr.restore()
    headline(cr, t, "HOURS LATER: HEAVY", "EYELIDS", t0, t0 + 0.4)


def h_breathing(cr, t, tl, t0):                          # b2 "...the breathing muscles stop working"
    _pic(cr, "lungs_engraving", W / 2, 1060, 0, t, t0, frame=(720, 760))
    p = prog(t, t0 + 0.4, 1.5)
    cr.set_source_rgba(*RED, 0.35 * p)
    cr.rectangle(W / 2 - 350, 690, 700, 740)
    cr.fill()
    headline(cr, t, "THEN", "PARALYSIS", t0, T(tl, "b2", "साँस"))


def t_tv(cr, t, tl, t0):                                 # b3 "in TV serials the naagin takes revenge, everyone sees her"
    rect = tv(cr, P["old_tv"], W / 2, 1150, 1120)
    screen(cr, rect, 1.0)
    sx, sy, sw_, sh_ = rect
    cr.save()
    cr.rectangle(sx, sy, sw_, sh_)
    cr.clip()
    if P["cobra_1"]:
        photo(cr, P["cobra_1"], sx + sw_ / 2, sy + sh_ * 0.55, sh_ * 0.9, tint=(0.18, 0.2, 0.2), shadow=False)
    cr.reset_clip()
    cr.restore()
    headline(cr, t, "ON TV, EVERYONE", "SEES THE SNAKE", t0, T(tl, "b3", "देख"), big_size=130)


def t_real(cr, t, tl, t0):                               # b3 "...in real life, one of the most dangerous is hard to see"
    cr.set_source_rgba(*NIGHT, 0.85 * prog(t, t0, 0.5))
    cr.rectangle(0, 560, W, 1000)
    cr.fill()
    _pic(cr, "krait_3", W / 2, 1060, 420, t, t0 + 0.4, alpha=0.55)
    stamp(cr, t, "REAL LIFE", t0 + 0.2, 780, 640, 60)
    headline(cr, t, "IN REAL LIFE:", "HARD TO SEE", t0, T(tl, "b3", "दिखता"))


def n_name(cr, t, tl, t0):                               # b4 "its name: common krait. Many call it karait."
    _pic(cr, "krait_3", W / 2, 940, 400, t, t0)
    tn = T(tl, "b4", "कॉमन")
    for i, (txt, ty, sz) in enumerate((("COMMON KRAIT", 1300, 96), ("BUNGARUS CAERULEUS", 1430, 54))):
        p = prog(t, tn + 0.3 * i, 0.3)
        if p > 0:
            tw_, th = text_size(txt, sz)
            cr.set_source_rgba(*RED, 0.92)
            cr.rectangle(MARGIN, ty - 12, (tw_ + 50) * p, th + 24)
            cr.fill()
            draw_text(cr, txt, MARGIN + 25, ty, sz, CREAM, clamp(p * 2 - 1))
    card(cr, t, T(tl, "b4", "करैत"), 640, 620, ["ALSO: KARAIT"], size=40)
    headline(cr, t, "ITS NAME", "", t0, 1e9)


def n_58000(cr, t, tl, t0):                              # b5 "58,000 deaths a year in India..."
    _pic(cr, "india_map", 300, 1100, 560, t, t0, tint=INK)
    counter(cr, t, T(tl, "b5", "अट्ठावन"), 740, 980, "58,000", 150, color=GOLD)
    draw_text(cr, "EVERY YEAR", 740, 1090, 44, INK, prog(t, T(tl, "b5", "अट्ठावन") + 0.3, 0.3), anchor="ct")
    headline(cr, t, "SNAKEBITE DEATHS IN INDIA", "58,000/YEAR", t0, T(tl, "b5", "अट्ठावन"), big_size=140)


def n_per_day(cr, t, tl, t0):                            # b5 "...about 160 every day. The most in the world."
    counter(cr, t, t0 + 0.1, W / 2, 900, "160", 260, color=GOLD)
    draw_text(cr, "EVERY DAY", W / 2, 1080, 70, INK, prog(t, t0 + 0.4, 0.3), anchor="ct")
    stamp(cr, t, "MOST IN THE WORLD", T(tl, "b5", "दुनिया"), W / 2, 1360, 60)
    headline(cr, t, "THAT'S ABOUT", "160 A DAY", t0, t0 + 0.3)


def n_big_four(cr, t, tl, t0):                           # b6 "most deaths: cobra, krait, Russell's viper, saw-scaled viper"
    t_first = T(tl, "b6", "कोबरा") - 0.2
    if t < t_first:                                            # "four snakes" before the first name is spoken
        counter(cr, t, t0 + 0.1, W / 2, 1000, "4", 300, color=GOLD)
        draw_text(cr, "SNAKES", W / 2, 1200, 90, INK, prog(t, t0 + 0.3, 0.3), anchor="ct")
    for i, (key, cue, label) in enumerate((("cobra_1", "कोबरा", "COBRA"), ("krait_3", "क्रेट", "KRAIT"),
                                           ("russells_viper_1", "रसेल्स", "RUSSELL'S VIPER"),
                                           ("saw_scaled_viper_2", "सॉ", "SAW-SCALED VIPER"))):
        tc = T(tl, "b6", cue) - 0.2
        cx, cy = 290 + 500 * (i % 2), 820 + 470 * (i // 2)
        _pic(cr, key, cx, cy, 300, t, tc)
        draw_text(cr, label, cx, cy + 180, 38, RED if key == "krait_3" else INK, prog(t, tc, 0.3), anchor="ct")
    ring(cr, 790, 820, 230, 200, prog(t, T(tl, "b6", "बिग"), 0.5))
    headline(cr, t, "INDIA'S", "BIG FOUR", t0, T(tl, "b6", "बिग"))


def w_night(cr, t, tl, t0):                              # b7 "the krait comes out at night; in the rains it enters homes"
    _pic(cr, "village_house_night", W / 2, 1060, 0, t, t0, frame=(900, 640))
    rain(cr, t, prog(t, T(tl, "b7", "बारिश"), 0.4))
    calendar(cr, t, T(tl, "b7", "बारिश"), 820, 1420, ["JULY", "AUG", "SEPT"], "MONSOON", interval=0.35, w=260,
             h=280)
    headline(cr, t, "AT NIGHT, IN THE", "MONSOON", t0, T(tl, "b7", "बारिश"))


def w_floor(cr, t, tl, t0):                              # b7 "...and bites people sleeping on the floor"
    sleeper(cr, t, 420, 1250)
    x = 1150 - 480 * prog(t, t0, 1.4)
    _pic(cr, "krait_2", x, 1380, 140, t, -1, flip=True)
    headline(cr, t, "IT BITES PEOPLE ON THE", "FLOOR", t0, T(tl, "b7", "ज़मीन"))


def w_marks(cr, t, tl, t0):                              # b8 "its fangs are tiny, the marks hard to see"
    _pic(cr, "skin_closeup", W / 2, 1060, 0, t, t0, frame=(880, 620))

    def inner(c):
        c.set_source_rgba(0.45, 0.15, 0.15, 0.55)
        for dx in (-14, 14):
            c.arc(600 + dx, 1060, 5, 0, 2 * math.pi)
            c.fill()
    magnifier(cr, t, t0 + 0.4, 600, 1060, 170, inner)
    checklist(cr, t, 120, 1220, 840, "THE BITE", [("NO SWELLING", T(tl, "b8", "सूजन") - 0.2, "tick",
                                                    T(tl, "b8", "सूजन")),
                                                   ("NO PAIN", T(tl, "b8", "दर्द") - 0.2, "tick", T(tl, "b8", "दर्द"))])
    headline(cr, t, "TINY FANGS,", "FAINT MARKS", t0, t0 + 0.5)


def v_nerves(cr, t, tl, t0):                             # b9 "the strangest part? its venom attacks the nerves" (slate)
    nerve(cr, t, t0, T(tl, "b9", "पहुँचने"), 100, 980, 1060, prog(t, t0, 0.3))
    small, big = ("THE STRANGEST", "PART") if t < T(tl, "b9", "नर्व्स") else ("IT ATTACKS", "THE NERVES")
    headline(cr, t, small, big, t0, t0 + 0.4 if big == "PART" else T(tl, "b9", "नर्व्स"),
             small_color=CREAM, big_color=CORAL)


def v_blocked(cr, t, tl, t0):                            # b9 "...the brain's signal never reaches the muscles"
    _pic(cr, "gray_anatomy_brain", 280, 1000, 0, t, t0, rot=-0.02, frame=(400, 300))
    _pic(cr, "gray_anatomy_muscles_alt_sobotta", 820, 1060, 0, t, t0 + 0.2, rot=0.02, frame=(300, 560))
    path(cr, [(480, 1020), (660, 1040)], prog(t, t0 + 0.3, 0.5), 8, RED, 0.9, arrow=True)
    cross(cr, 570, 1030, 140, prog(t, T(tl, "b9", "पहुँचने"), 0.4))
    headline(cr, t, "THE SIGNAL IS", "BLOCKED", t0, T(tl, "b9", "पहुँचने"))


def v_steps(cr, t, tl, t0):                              # b10 "eyelids drop, swallowing gets hard, breathing stops"
    for i, (key, cue, label) in enumerate((("eye_closeup", "पलकें", "EYELIDS"), (None, "निगलना", "SWALLOWING"),
                                           ("lungs_engraving", "साँस", "BREATHING"))):
        tc = T(tl, "b10", cue) - 0.2
        y = 720 + 300 * i
        if key:
            _pic(cr, key, 260, y, 0, t, tc, frame=(300, 220))
        else:
            card(cr, t, tc, 120, y - 80, ["THROAT"], size=54)
        draw_text(cr, label, 470, y, 70, RED, prog(t, tc + 0.2, 0.3), anchor="lm")
    headline(cr, t, "ONE BY ONE,", "SHUT DOWN", t0, T(tl, "b10", "साँस"))


def r_made_here(cr, t, tl, t0):                          # b11 "the cure, anti-venom, is made in India"
    _pic(cr, "antivenom_vial_1", 380, 1080, 600, t, t0)
    card(cr, t, t0 + 0.4, 600, 900, ["ANTI-VENOM", "MADE IN INDIA"], size=44)
    tick(cr, 720, 1220, 150, prog(t, t0 + 0.8, 0.4), color=GREEN)
    headline(cr, t, "THE CURE IS", "MADE HERE", t0, T(tl, "b11", "भारत"), big_color=GREEN)


def r_why(cr, t, tl, t0):                                # b11 re-hook: "so why do so many die?"
    _pic(cr, "antivenom_vial_1", 300, 1080, 480, t, -1)
    q = prog(t, t0, 0.3)
    draw_text(cr, "WHY?", 700, 1060, 260 * (0.8 + 0.2 * q), RED, q, anchor="cm")
    headline(cr, t, "THEN WHY DO SO MANY", "DIE?", t0, T(tl, "b11", "मरते"), t_ghost=t0)


def r_home(cr, t, tl, t0):                               # b12 "most die at home; they don't reach hospital in time"
    _pic(cr, "village_house_night", 300, 950, 0, t, t0, frame=(440, 320))
    _pic(cr, "hospital", 800, 1300, 0, t, t0 + 0.3, frame=(420, 300))
    path(cr, [(440, 1120), (620, 1220)], prog(t, t0 + 0.5, 0.8), 6, INK, 0.7, dash=[14, 12])
    _pic(cr, "clock", 300, 1360, 230, t, T(tl, "b12", "टाइम") - 0.3)
    stamp(cr, t, "AT HOME", T(tl, "b12", "घर"), 300, 760, 64)
    headline(cr, t, "MOST DIE", "AT HOME", t0, T(tl, "b12", "घर"))


def m_myths(cr, t, tl, t0):                              # b13 "jhaad-phoonk, cut and suck, a tight rope"
    items = (("JHAAD-PHOONK", "झाड़", None), ("CUT & SUCK", "काट", "kitchen_knife"), ("TIGHT ROPE", "रस्सी", "rope"))
    for i, (label, cue, key) in enumerate(items):
        tc = T(tl, "b13", cue) - 0.2
        y = 700 + 300 * i
        card(cr, t, tc, 110, y - 70, [label], size=60)
        if key:
            _pic(cr, key, 800, y, 200, t, tc, rot=-0.2)
    headline(cr, t, "WHAT PEOPLE", "DO FIRST", t0, t0 + 0.4)


def m_wrong(cr, t, tl, t0):                              # b14 "all wrong, and it wastes precious time"
    for i, label in enumerate(("JHAAD-PHOONK", "CUT & SUCK", "TIGHT ROPE")):
        y = 700 + 300 * i
        card(cr, t, -1, 110, y - 70, [label], size=60)
        tw_, _ = text_size(label, 60)
        strike(cr, 130, y, 160 + tw_, y - 10, prog(t, t0 + 0.2 + 0.25 * i, 0.3))
    stamp(cr, t, "MYTH", t0 + 1.0, 800, 1000, 110, rot=-0.15)
    headline(cr, t, "ALL WRONG.", "TIME LOST", t0, T(tl, "b14", "वक़्त"))


def d_calm(cr, t, tl, t0):                               # b15 "if bitten: don't panic; keep the limb still and straight"
    cr.save()
    cr.translate(W / 2 + 320, 1250)                                    # lying down, resting
    cr.rotate(-math.pi / 2)
    person(cr, 0, 0, 640, INK, 0.85)
    cr.restore()
    path(cr, [(260, 1330), (820, 1330)], prog(t, T(tl, "b15", "सीधा"), 0.5), 12, GREEN, 0.9)
    tick(cr, 820, 900, 140, prog(t, T(tl, "b15", "सीधा") + 0.3, 0.4), color=GREEN)
    headline(cr, t, "IF BITTEN:", "STAY STILL", t0, T(tl, "b15", "हिलाओ"), big_color=GREEN)


def d_remove(cr, t, tl, t0):                             # b16 "take off rings, watch, tight clothes"
    for key, x, cue in (("finger_ring", 250, "अंगूठी"), ("wristwatch", 540, "घड़ी"), (None, 830, "कपड़े")):
        tc = T(tl, "b16", cue) - 0.2
        if key:
            _pic(cr, key, x, 1080, 260, t, tc)
        else:
            card(cr, t, tc, x - 130, 1020, ["TIGHT", "CLOTHES"], size=44)
        cross(cr, x, 1080, 220, prog(t, tc + 0.3, 0.3))
    headline(cr, t, "TAKE OFF", "RINGS, WATCH", t0, T(tl, "b16", "अंगूठी"), big_color=GREEN)


def d_hospital(cr, t, tl, t0):                           # b16 "...go straight to a hospital with anti-venom"
    _pic(cr, "hospital", 440, 1040, 0, t, t0, frame=(700, 500))
    _pic(cr, "antivenom_vial_1", 850, 1220, 300, t, t0 + 0.3)
    headline(cr, t, "GO NOW: A HOSPITAL WITH", "ANTI-VENOM", t0, t0 + 0.4, big_color=GREEN)


def d_108(cr, t, tl, t0):                                # b16 "...call 108"
    _pic(cr, "ambulance", W / 2, 1100, 0, t, t0, frame=(880, 600))
    counter(cr, t, t0 + 0.2, W / 2, 680, "108", 200, color=GOLD)
    headline(cr, t, "CALL", "108", t0, t0 + 0.2, big_color=GREEN)


def d_no_pain(cr, t, tl, t0):                            # b17 "a night bite with no pain: still go to hospital"
    cr.set_source_rgba(*NIGHT, 0.8)
    cr.rectangle(0, 560, W, 900)
    cr.fill()
    _pic(cr, "clock", 300, 1000, 300, t, t0)
    draw_text(cr, "NO PAIN,", 560, 940, 90, CREAM, prog(t, t0 + 0.3, 0.3), anchor="lm")   # (Anton has no "≠")
    draw_text(cr, "STILL DANGER", 560, 1060, 100, CORAL, prog(t, T(tl, "b17", "हॉस्पिटल"), 0.3), anchor="lm")
    headline(cr, t, "BITTEN AT NIGHT?", "GO ANYWAY", t0, T(tl, "b17", "हॉस्पिटल"), big_color=GREEN)


def d_net(cr, t, tl, t0):                                # b18 "on the floor, sleep under a mosquito net (Nepal study)"
    _pic(cr, "mosquito_net_1", 460, 1080, 760, t, t0)
    _pic(cr, "krait_2", 900, 1440, 130, t, t0 + 0.4, flip=True)
    headline(cr, t, "SLEEP UNDER A", "MOSQUITO NET", t0, T(tl, "b18", "मच्छरदानी"), big_color=GREEN)


def d_study(cr, t, tl, t0):                              # b18 "...in a Nepal study, people under nets were bitten less"
    _pic(cr, "mosquito_net_1", 330, 1180, 560, t, -1)
    card(cr, t, t0 + 0.1, 560, 760, ["NEPAL, 2007", "UNDER A NET:", "FEWER BITES"], size=48)
    _pic(cr, "krait_2", 820, 1420, 120, t, -1, flip=True)
    cross(cr, 820, 1420, 140, prog(t, T(tl, "b18", "कम"), 0.4))
    footnote(cr, "Chappuis et al. 2007, American Journal of Tropical Medicine and Hygiene", prog(t, t0, 0.4),
             y=1540)
    headline(cr, t, "A STUDY", "IN NEPAL", t0, t0 + 0.3, big_color=GREEN)


def e_bookend(cr, t, tl, t0):                            # b19 "socho: a snake whose bite doesn't hurt..."
    _pic(cr, "krait_3", W / 2, 1100, 420, t, -1)
    draw_text(cr, "NO PAIN", W / 2, 1450, 90, RED, 1 - prog(t, T(tl, "b19", "इसी"), 1.0), anchor="cm")
    headline(cr, t, "THE DANGER IS", "SILENCE", t0, T(tl, "b19", "इसी"), t_ghost=t0)


def e_question(cr, t, tl, t0):                           # b20 "a snake near your home or village? YES or NO"
    _pic(cr, "krait_2", 300, 1420, 150, t, t0)
    yes_no_card(cr, t, t0 + 0.4, 640, 980, w=640, h=300, question="COMMENT: YES OR NO")
    headline(cr, t, "A SNAKE NEAR", "YOUR HOME?", t0, T(tl, "b20", "घर"), t_ghost=t0)


SHOTS = [   # (line, cue where the shot starts, draw function, background)
    ("b1", None, h_snake, "paper"), ("b1", "साँप", h_comes, "paper"), ("b1", "पता", h_no_pain, "paper"),
    ("b2", None, h_eyelids, "paper"), ("b2", "साँस", h_breathing, "paper"),
    ("b3", None, t_tv, "paper"), ("b3", "असली", t_real, "paper"),
    ("b4", None, n_name, "paper"), ("b5", None, n_58000, "paper"), ("b5", "मतलब", n_per_day, "paper"),
    ("b6", None, n_big_four, "paper"),
    ("b7", None, w_night, "paper"), ("b7", "ज़मीन", w_floor, "paper"), ("b8", None, w_marks, "paper"),
    ("b9", None, v_nerves, "slate"), ("b9", "दिमाग़", v_blocked, "paper"), ("b10", None, v_steps, "paper"),
    ("b11", None, r_made_here, "paper"), ("b11", "तो", r_why, "paper"), ("b12", None, r_home, "paper"),
    ("b13", None, m_myths, "paper"), ("b14", None, m_wrong, "paper"),
    ("b15", None, d_calm, "paper"), ("b16", None, d_remove, "paper"), ("b16", "हॉस्पिटल", d_hospital, "paper"),
    ("b16", "एक सौ", d_108, "paper"), ("b17", None, d_no_pain, "paper"), ("b18", None, d_net, "paper"), ("b18", "नेपाल", d_study, "paper"),
    ("b19", None, e_bookend, "paper"), ("b20", None, e_question, "paper"),
]


def draw(cr, t, tl):
    draw_frame(cr, t, tl, SHOTS)


def sfx(tl):
    """A whoosh on every cut, thuds on stamps, scribbles on the myth strikes, a tick before the re-hook and the
    closing line, typing on the card."""
    ev = [(s, "whoosh", 0.25) for s in starts(tl, SHOTS)[1:]]
    ev += [(T(tl, "b1", "दर्द"), "thud", 0.0), (T(tl, "b5", "दुनिया"), "thud", 0.0),
           (T(tl, "b12", "घर"), "thud", 0.0), (T(tl, "b14", None) + 0.2, "scribble", 0.9),
           (T(tl, "b11", "तो") - 0.35, "tick", 0.0), (T(tl, "b19", None) - 0.35, "tick", 0.0),
           (T(tl, "b20", "यस"), "typing", 1.0)]
    for bid in ("b4", "b6", "b9", "b16", "b18"):
        ev.append((tl[bid].start + 0.4, "pop", 0.0))
    ev += [(at, "dip", 0.5) for at, name, _ in list(ev) if name == "tick"]   # the bed dips just before a reveal
    return ev
