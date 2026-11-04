"""Video 9 (science): "Socho, doctors ko lagta hai tum coma mein ho... par tum sab kuch sun rahe ho" - coma, the
vegetative state, and the patients who are aware inside. Owner, 4 Nov 2026: "make video on koma", script approved
("Approve"); then hook v2 in the second person (owner: "socho tum koma me chalegaye sab sun to pate par hat be nahi
hilisakte na bat karsakte tum jinda to ho par dead jese body me koi movement he nahi hota ... auto approved"). It
says "doctors think you're in a coma", because in a true coma nobody is aware; the people who hear everything are
the ones wrongly thought unaware. Narration in Devanagari for the voice, numbers written as words.
Facts: Martin Pistorius (South Africa) fell ill at 12 in 1988 (believed cryptococcal meningitis); doctors told his
parents to take him home and keep him comfortable until he died; awareness came back gradually from about 16 (full
by about 19) while he could not move or speak; Barney reruns played at his care centre; at about 25 an aromatherapist,
Virna van der Walt, noticed he responded, and the University of Pretoria's AAC centre confirmed it; he now speaks
through a computer, married Joanna in 2009, works as a web designer, and wrote Ghost Boy (2011) (NPR 2015; Wikipedia).
Coma: closed eyes, no sleep-wake cycles, rarely lasts more than about 4 weeks; the vegetative state brings back eye
opening and sleep-wake cycles without signs of awareness (UW TBI Model System; Oxford HEXI). Owen et al., Science 2006:
a 23-year-old woman in a vegetative state after a July 2005 car accident, asked in fMRI to imagine playing tennis,
activated the supplementary motor area like 12 healthy volunteers. Scott Routley (Canada), vegetative for 12 years
after a car crash, answered "not in pain" with the tennis / walking-through-the-house code (Owen, BBC, Nov 2012).
Bodien et al., NEJM 2024 (391:598): 353 adults with disorders of consciousness; of the 241 without an observable
response to commands, 25% (60) followed commands on task-based fMRI or EEG (cognitive motor dissociation). Pape et al.,
Neurorehabilitation and Neural Repair 2015: 15 patients; recorded family stories four times a day for six weeks, and
they recovered consciousness faster than with placebo."""
import math
import os

from poster import (CORAL, CREAM, GOLD, GREEN, INK, MONO_FONT, RED, SLATE, W, calendar, card, counter, cross,
                    draw_text, headline, path, person, prog, ring, stamp, strike, tick, yes_no_card)

# the narrator, music and tail are channel-wide; render_hi reads them from this module
from channel import ASSETS_ROOT, MUSIC, NARRATOR, NARRATOR_LABEL, REVEAL_GAP, TAIL, VOICE_REF  # noqa: F401
from shots import T, asset_finder, draw_frame, pic, starts

SCRIPT = [
    dict(id="b1", text="सोचो, डॉक्टरों को लगता है तुम कोमा में हो... पर तुम सब कुछ सुन रहे हो।"),
    dict(id="b1b", text="तुम हाथ तक नहीं हिला सकते। बोल भी नहीं सकते। तुम ज़िंदा हो... पर शरीर एक लाश की तरह पड़ा है।",
         gap=REVEAL_GAP),
    dict(id="b1c", text="ये कोई फ़िल्म नहीं है। साउथ अफ़्रीका के एक लड़के के साथ, ये सच में हुआ।"),
    dict(id="b2", text="बारह साल का मार्टिन अचानक बीमार पड़ा। और धीरे-धीरे उसका चलना, बोलना, सब बंद हो गया।"),
    dict(id="b3", text="डॉक्टरों ने उसके माँ-बाप से कहा: इसे घर ले जाओ, और आख़िरी दिनों तक आराम से रखो।"),
    dict(id="b4", text="पर कुछ साल बाद, मार्टिन का दिमाग़ फिर से जागने लगा। और उसके साथ ठीक वही हुआ, "
                       "जो तुमने अभी सोचा।"),
    dict(id="b5", text="और किसी को पता ही नहीं था, कि वो अंदर है।", gap=REVEAL_GAP),
    dict(id="b6", text="ऐसा कैसे? कोमा में दिमाग़ का जागने वाला स्विच बंद हो जाता है। आँखें बंद, कोई होश नहीं। "
                       "और ये अक्सर कुछ हफ़्तों में ख़त्म हो जाता है।"),
    dict(id="b7", text="कुछ लोग जाग जाते हैं। और कुछ एक अजीब हालत में पहुँच जाते हैं: आँखें खुली, सोना-जागना चालू... "
                       "पर किसी बात का कोई जवाब नहीं।"),
    dict(id="b8", text="डॉक्टर कहते हैं, मेरा हाथ दबाओ। जवाब नहीं आया, तो मान लिया जाता है... अंदर कोई होश नहीं है।"),
    dict(id="b9", text="पर दो हज़ार छह में, कैम्ब्रिज के एक साइंटिस्ट ने, ऐसी ही एक लड़की को एमआरआई में लिटाया, "
                       "और कहा: सोचो कि तुम टेनिस खेल रही हो।"),
    dict(id="b10", text="और उसके दिमाग़ का ठीक वही हिस्सा चमक उठा... जो किसी नॉर्मल इंसान का टेनिस सोचने पर चमकता है।",
         gap=REVEAL_GAP),
    dict(id="b11", text="वो अंदर थी। सब सुन रही थी। बस उसका शरीर, जवाब नहीं दे पा रहा था।"),
    dict(id="b12", text="फिर इसी ट्रिक को हाँ और ना बना दिया गया। और कनाडा के एक आदमी से, जो बारह साल से इसी हालत में "
                        "था, पूछा गया: क्या तुम्हें दर्द होता है?"),
    dict(id="b13", text="उसके दिमाग़ ने जवाब दिया: नहीं।", gap=REVEAL_GAP),
    dict(id="b14", text="और दो हज़ार चौबीस में, तीन सौ से ज़्यादा मरीज़ों की स्टडी में पता चला... जो मरीज़ बिल्कुल जवाब "
                        "नहीं देते, उनमें से हर चार में से एक का दिमाग़, बात समझ रहा था।"),
    dict(id="b15", text="और मार्टिन? पच्चीस की उम्र में, एक थेरेपिस्ट ने उसकी आँखों में हलचल देखी। टेस्ट हुए, "
                        "और सच सामने आ गया।"),
    dict(id="b16", text="आज मार्टिन कंप्यूटर से बात करता है, उसकी शादी हो चुकी है, और उसने अपनी कहानी पर किताब भी लिखी "
                        "है: घोस्ट बॉय।"),
    dict(id="b17", text="एक छोटी स्टडी में तो, अपनों की आवाज़ में पुरानी यादें सुनकर, मरीज़ जल्दी होश में आए।"),
    dict(id="b18", text="तो अगर कभी कोई अपना बेहोश दिखे... उससे बात करते रहना। शायद वो सब सुन रहा हो।"),
    dict(id="b19", text="तुम्हें पता था कि बेहोश दिखने वाला इंसान भी सब सुन सकता है? यस या नो, कमेंट में बताओ।"),
]

METADATA = dict(
    title="Doctors ko lagta hai tum coma mein ho, par tum sab sun rahe ho",
    caption="Socho, doctors ko lagta hai tum coma mein ho... par tum sab kuch sun rahe ho 😳\n\n"
            "Haath tak nahi hila sakte, bol bhi nahi sakte. South Africa ke Martin ke saath ye sach mein hua: kuch "
            "saal baad uska dimaag jaag gaya, aur kisi ko pata hi nahi tha ki wo andar hai.\n\n"
            "2024 ki ek badi study: jo mareez bilkul jawab nahi dete, unmein se har 4 mein se 1 ka dimaag baat "
            "samajh raha tha.\n\n"
            "Tumhe pata tha ki behosh dikhne wala insaan bhi sab sun sakta hai? Comment mein YES ya NO likho 👇",
    yt_title="Coma Mein Ho, Par Sab Sunai De Raha Hai? 😳 | Ghost Boy",
    yt_description="South Africa ke Martin Pistorius ko doctors ne \"kuch nahi samajhta\" maan liya tha, par wo saalon "
                   "tak sab sun raha tha. Coma aur vegetative state ka fark, 2006 ka tennis wala brain scan, 12 saal "
                   "baad \"kya tumhe dard hota hai?\" ka jawab, aur 2024 ki study: jawab na dene wale har 4 mein se 1 "
                   "mareez ka dimaag baat samajh raha tha.",
    hashtags=["#coma", "#brain", "#sciencefacts", "#factsinhindi", "#neuroscience"],
    pinned_comment="Tumhe pata tha ki behosh dikhne wala insaan bhi sab sun sakta hai? 🧠 YES ya NO? 👇",
    sources=["Owen et al. 2006, Science, Detecting awareness in the vegetative state",
             "Bodien et al. 2024, New England Journal of Medicine, Cognitive motor dissociation",
             "Pistorius, Ghost Boy (2011); NPR 2015",
             "BBC 2012, Scott Routley",
             "Pape et al. 2015, Neurorehabilitation and Neural Repair"],
)

_find = asset_finder("coma", "mosquito")
P = {k: _find(k) for k in ("patient", "hand_iv", "mri", "brain", "fmri_scan", "racket", "hands", "headphones", "eye",
                           "rings", "eeg", "doctor", "world_map")}
USED_ASSETS = [os.path.basename(v) for v in P.values() if v]
CREDITS_FILES = [os.path.join(ASSETS_ROOT, d, "credits.json") for d in ("coma", "mosquito")]

SKIN, HAIR, SHEET = (0.83, 0.64, 0.50), (0.18, 0.13, 0.10), (0.60, 0.70, 0.78)
WARM = (1.0, 0.80, 0.36)
MAP = (W / 2, 1060, 500)        # world_map.png drawn at this centre and height; its width is 1.884 x its height
WP = dict(south_africa=(57.5, 69.5), canada=(18.5, 29.5), uk=(47.5, 22.5))   # percent of the map image


def _pic(cr, key, cx, cy, h, t, t0, **kw):
    pic(cr, P.get(key), cx, cy, h, t, t0, **kw)


# ---------- drawing pieces for this video ----------

def glow(cr, x, y, r, color=WARM, alpha=1.0):
    if alpha <= 0 or r <= 0:
        return
    for k, a in ((2.6, 0.12), (1.6, 0.3), (1.0, 0.95)):
        cr.arc(x, y, r * k, 0, 2 * math.pi)
        cr.set_source_rgba(*color, a * alpha)
        cr.fill()


def rrect(cr, x, y, w, h, r):
    cr.new_sub_path()
    cr.arc(x + w - r, y + r, r, -math.pi / 2, 0)
    cr.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    cr.arc(x + r, y + h - r, r, math.pi / 2, math.pi)
    cr.arc(x + r, y + r, r, math.pi, 3 * math.pi / 2)
    cr.close_path()


def clamp01(x):
    return max(0.0, min(1.0, x))


def symbolic(cr, x, y, alpha=1.0, color=INK):
    draw_text(cr, "SYMBOLIC PHOTO", x, y, 24, color, 0.7 * alpha, MONO_FONT, "ct", tracking=2)


def sickbed(cr, cx, cy, w, alpha=1.0, mind=0.0, eyes=0.0, frame=(0.80, 0.82, 0.84)):
    """A hospital bed from the side, a patient under a blanket with the head on the left. mind 0..1 lights a warm
    glow inside the head (someone is in there); eyes 0 = closed, 1 = open. Returns the head centre."""
    x0 = cx - w / 2
    h = w * 0.07
    hr = w * 0.058
    hx, hy = x0 + w * 0.15, cy - h * 0.35 - hr * 0.75
    if alpha <= 0:
        return hx, hy
    dark = tuple(c * 0.6 for c in frame)
    for lx in (x0 + w * 0.08, x0 + w * 0.92):
        cr.rectangle(lx - 8, cy + h, 16, w * 0.16)
        cr.set_source_rgba(*dark, alpha)
        cr.fill()
        cr.arc(lx, cy + h + w * 0.16 + 12, 14, 0, 2 * math.pi)
        cr.set_source_rgba(0.12, 0.12, 0.13, alpha)
        cr.fill()
    cr.rectangle(x0 + w * 0.06, cy + h + w * 0.07, w * 0.88, 14)
    cr.set_source_rgba(*dark, alpha)
    cr.fill()
    rrect(cr, x0 - 20, cy - w * 0.2, 32, w * 0.2 + h + 14, 12)
    rrect(cr, x0 + w - 12, cy - w * 0.11, 32, w * 0.11 + h + 14, 12)
    cr.set_source_rgba(*frame, alpha)
    cr.fill()
    rrect(cr, x0, cy, w, h, h * 0.4)
    cr.set_source_rgba(0.97, 0.97, 0.96, alpha)
    cr.fill()
    cr.save()
    cr.translate(x0 + w * 0.13, cy - h * 0.25)
    cr.scale(w * 0.11, h * 0.62)
    cr.arc(0, 0, 1, 0, 2 * math.pi)
    cr.restore()
    cr.set_source_rgba(0.99, 0.99, 0.99, alpha)
    cr.fill()
    cr.arc(hx, hy, hr, 0, 2 * math.pi)                       # the head, face up
    cr.set_source_rgba(*SKIN, alpha)
    cr.fill()
    cr.new_sub_path()
    cr.arc(hx, hy, hr * 1.04, math.pi * 0.55, math.pi * 1.35)  # hair at the back of the head
    cr.close_path()
    cr.set_source_rgba(*HAIR, alpha)
    cr.fill()
    cr.move_to(hx + hr * 0.62, hy - hr * 0.78)               # the nose
    cr.line_to(hx + hr * 0.95, hy - hr * 1.1)
    cr.line_to(hx + hr * 1.0, hy - hr * 0.55)
    cr.set_source_rgba(*SKIN, alpha)
    cr.fill()
    ex, ey = hx + hr * 0.25, hy - hr * 0.62
    if eyes > 0.5:
        cr.arc(ex, ey, hr * 0.2, 0, 2 * math.pi)
        cr.set_source_rgba(1, 1, 1, alpha)
        cr.fill()
        cr.arc(ex + hr * 0.04, ey - hr * 0.04, hr * 0.1, 0, 2 * math.pi)
        cr.set_source_rgba(0.1, 0.07, 0.05, alpha)
        cr.fill()
    else:
        cr.new_sub_path()
        cr.arc(ex, ey - hr * 0.08, hr * 0.2, math.pi * 0.15, math.pi * 0.85)
        cr.set_source_rgba(0.25, 0.15, 0.10, alpha)
        cr.set_line_width(max(3, hr * 0.07))
        cr.stroke()
    xs = x0 + w * 0.22                                       # the blanket over the body
    cr.move_to(xs, cy + 2)
    cr.curve_to(xs - w * 0.02, cy - w * 0.08, xs + w * 0.06, cy - w * 0.1, xs + w * 0.16, cy - w * 0.085)
    cr.curve_to(xs + w * 0.36, cy - w * 0.07, xs + w * 0.55, cy - w * 0.05, x0 + w * 0.86, cy - w * 0.06)
    cr.curve_to(x0 + w * 0.92, cy - w * 0.09, x0 + w * 0.97, cy - w * 0.05, x0 + w * 0.97, cy + 2)
    cr.close_path()
    cr.set_source_rgba(*SHEET, alpha)
    cr.fill()
    if mind > 0:                                             # the light sits at the back of the head, off the face
        glow(cr, hx - hr * 0.3, hy + hr * 0.12, hr * 0.3 * (0.6 + 0.4 * mind), WARM, alpha * mind)
    return hx, hy


def incoming(cr, x, y, t, color=CORAL, alpha=1.0, a0=-math.pi / 4, spread=0.5, r0=70, r1=330, n=3, speed=0.8):
    """Sound arcs closing in on (x, y) from direction a0: someone talking to the patient."""
    if alpha <= 0:
        return
    for k in range(n):
        f = (t * speed + k / n) % 1
        cr.new_sub_path()
        cr.arc(x, y, r1 - (r1 - r0) * f, a0 - spread, a0 + spread)
        cr.set_source_rgba(*color, alpha * min(1.0, 2.5 * f) * (1 - 0.4 * f))
        cr.set_line_width(7)
        cr.stroke()


def switch(cr, x, y, s, on, alpha=1.0):
    """A wall switch: the lever is up at on = 1 (ON) and down at on = 0 (OFF)."""
    if alpha <= 0:
        return
    rrect(cr, x - s * 0.35 + 8, y - s * 0.55 + 12, s * 0.7, s * 1.1, s * 0.08)
    cr.set_source_rgba(0, 0, 0, 0.25 * alpha)
    cr.fill()
    rrect(cr, x - s * 0.35, y - s * 0.55, s * 0.7, s * 1.1, s * 0.08)
    cr.set_source_rgba(*CREAM, alpha)
    cr.fill()
    rrect(cr, x - s * 0.1, y - s * 0.3, s * 0.2, s * 0.6, s * 0.05)
    cr.set_source_rgba(0.2, 0.2, 0.22, alpha)
    cr.fill()
    ly = y - s * 0.17 * (2 * on - 1)
    rrect(cr, x - s * 0.13, ly - s * 0.12, s * 0.26, s * 0.24, s * 0.05)
    cr.set_source_rgba(*(GREEN if on > 0.5 else RED), alpha)
    cr.fill()
    draw_text(cr, "ON", x, y - s * 0.43, int(s * 0.1), INK, alpha, MONO_FONT, "cm")
    draw_text(cr, "OFF", x, y + s * 0.43, int(s * 0.1), INK, alpha, MONO_FONT, "cm")


def house(cr, x, y, s, color=INK, alpha=1.0):
    """A small house standing on (x, y)."""
    if alpha <= 0:
        return
    cr.rectangle(x - s * 0.4, y - s * 0.6, s * 0.8, s * 0.6)
    cr.move_to(x - s * 0.52, y - s * 0.58)
    cr.line_to(x, y - s * 1.0)
    cr.line_to(x + s * 0.52, y - s * 0.58)
    cr.close_path()
    cr.set_source_rgba(*color, alpha)
    cr.fill()
    cr.rectangle(x - s * 0.1, y - s * 0.3, s * 0.2, s * 0.3)
    cr.set_source_rgba(*CREAM, alpha)
    cr.fill()


def laptop(cr, cx, cy, w, alpha=1.0, text="", p_text=0.0):
    """A plain laptop whose screen types `text` as p_text goes 0 -> 1."""
    if alpha <= 0:
        return
    sh = w * 0.62
    rrect(cr, cx - w / 2, cy - sh, w, sh, w * 0.04)
    cr.set_source_rgba(0.16, 0.16, 0.18, alpha)
    cr.fill()
    cr.rectangle(cx - w / 2 + w * 0.04, cy - sh + w * 0.04, w * 0.92, sh - w * 0.08)
    cr.set_source_rgba(0.93, 0.95, 0.97, alpha)
    cr.fill()
    cr.move_to(cx - w * 0.56, cy + w * 0.06)
    cr.line_to(cx - w * 0.5, cy)
    cr.line_to(cx + w * 0.5, cy)
    cr.line_to(cx + w * 0.56, cy + w * 0.06)
    cr.close_path()
    cr.set_source_rgba(0.55, 0.56, 0.58, alpha)
    cr.fill()
    n = int(len(text) * clamp01(p_text))
    if n:
        draw_text(cr, text[:n], cx - w * 0.4, cy - sh / 2, int(w * 0.1), INK, alpha, MONO_FONT, "lm")


def book(cr, cx, cy, h, alpha=1.0, rot=0.04):
    """A plain hardback with the memoir's title (no cover art)."""
    if alpha <= 0:
        return
    w = h * 0.66
    cr.save()
    cr.translate(cx, cy)
    cr.rotate(rot)
    cr.rectangle(-w / 2 + 10, -h / 2 + 16, w, h)
    cr.set_source_rgba(0, 0, 0, 0.25 * alpha)
    cr.fill()
    cr.rectangle(-w / 2, -h / 2, w, h)
    cr.set_source_rgba(0.14, 0.20, 0.30, alpha)
    cr.fill()
    cr.rectangle(-w / 2, -h / 2, w * 0.08, h)
    cr.set_source_rgba(0.09, 0.13, 0.20, alpha)
    cr.fill()
    draw_text(cr, "GHOST", w * 0.04, -h * 0.18, int(h * 0.2), CREAM, alpha, anchor="cm")
    draw_text(cr, "BOY", w * 0.04, h * 0.04, int(h * 0.2), CORAL, alpha, anchor="cm")
    draw_text(cr, "MARTIN PISTORIUS", w * 0.04, h * 0.36, int(h * 0.045), CREAM, alpha, MONO_FONT, "cm", tracking=2)
    cr.restore()


def bubble(cr, x, y, w, h, tail, alpha=1.0, color=CREAM):
    """A thought bubble centred at (x, y) with three small circles trailing to `tail`."""
    if alpha <= 0:
        return
    for k, r in enumerate((10, 16, 24)):
        f = (k + 1) / 4
        cr.arc(tail[0] + (x - tail[0]) * f * 0.7, tail[1] + (y - tail[1]) * f * 0.7, r, 0, 2 * math.pi)
        cr.set_source_rgba(*color, alpha)
        cr.fill()
    cr.save()
    cr.translate(x, y)
    cr.scale(w / 2, h / 2)
    cr.arc(0, 0, 1, 0, 2 * math.pi)
    cr.restore()
    cr.set_source_rgba(*color, alpha)
    cr.fill()


def waveform(cr, x, y, w, h, t, color=CORAL, alpha=1.0, n=28):
    """Speech bars bouncing like a voice recording."""
    if alpha <= 0:
        return
    bw = w / n
    for k in range(n):
        a = 0.25 + 0.75 * abs(math.sin(t * 5.3 + k * 0.9) * math.sin(t * 2.1 + k * 0.37))
        rrect(cr, x + k * bw + bw * 0.2, y - h * a / 2, bw * 0.6, h * a, bw * 0.25)
        cr.set_source_rgba(*color, alpha)
        cr.fill()


def mp(p, m=MAP, aspect=1.884):
    fx, fy = WP[p] if isinstance(p, str) else p
    cx, cy, h = m
    return cx + (fx / 100 - 0.5) * aspect * h, cy + (fy / 100 - 0.5) * h


def map_pin(cr, x, y, s, color=RED, alpha=1.0):
    """A map pin whose tip is at (x, y)."""
    if alpha <= 0:
        return
    cr.move_to(x, y)
    cr.curve_to(x - s * 0.9, y - s * 1.1, x - s * 0.75, y - s * 2.0, x, y - s * 2.0)
    cr.curve_to(x + s * 0.75, y - s * 2.0, x + s * 0.9, y - s * 1.1, x, y)
    cr.set_source_rgba(*color, alpha)
    cr.fill()
    cr.arc(x, y - s * 1.35, s * 0.32, 0, 2 * math.pi)
    cr.set_source_rgba(1, 1, 1, alpha)
    cr.fill()


def world_pin(cr, t, t0, place, label, t_pin, color=RED):
    _pic(cr, "world_map", MAP[0], MAP[1], MAP[2], t, t0, tint=(0.55, 0.47, 0.38))
    x, y = mp(place)
    p = prog(t, t_pin, 0.3)
    map_pin(cr, x, y, 36, color, p)
    if p > 0:
        ring(cr, x, y, 60, 30, prog(t, t_pin + 0.1, 0.4), color=color)
    draw_text(cr, label, x, y + 30, 36, INK, p, MONO_FONT, "ct", tracking=2)


BRAIN_SPOT = (0.47, 0.40)   # where the "tennis" glow sits on brain.png (top of the brain, near the middle)


def lit_brain(cr, t, t0, cx, cy, h, p_glow, label=None, label_color=CREAM):
    """The brain photo with a warm glow at BRAIN_SPOT as p_glow goes 0 -> 1."""
    _pic(cr, "brain", cx, cy, h, t, t0)
    w = h * 472 / 373
    gx, gy = cx + (BRAIN_SPOT[0] - 0.5) * w, cy + (BRAIN_SPOT[1] - 0.5) * h
    if p_glow > 0:
        glow(cr, gx, gy, h * 0.07 * (0.8 + 0.2 * math.sin(t * 6)), (1.0, 0.85, 0.25), p_glow)
    if label:
        draw_text(cr, label, cx, cy + h * 0.55, 34, label_color, prog(t, t0 + 0.2, 0.3), MONO_FONT, "ct", tracking=2)
    return gx, gy


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
    cr.set_line_width(8)
    cr.stroke()
    cr.arc(0, 0, w * 0.17, 0, 2 * math.pi)
    cr.set_source_rgba(0.35, 0.22, 0.12, alpha)
    cr.fill()
    cr.arc(0, 0, w * 0.08, 0, 2 * math.pi)
    cr.set_source_rgba(0, 0, 0, alpha)
    cr.fill()
    cr.restore()


def sun_moon(cr, x, y, r, t, alpha=1.0):
    """Day and night taking turns: the sun and the moon cross-fade every ~1.4 s."""
    if alpha <= 0:
        return
    day = 0.5 + 0.5 * math.cos(t * 2.2)
    glow(cr, x, y, r * 0.6, GOLD, alpha * day)
    cr.arc(x, y, r * 0.6, 0, 2 * math.pi)
    cr.set_source_rgba(*CREAM, alpha * (1 - day))
    cr.fill()
    cr.arc(x + r * 0.3, y - r * 0.2, r * 0.5, 0, 2 * math.pi)
    cr.set_source_rgba(*SLATE, alpha * (1 - day))
    cr.fill()


# ---------- shots ----------
# Rules (style bible): a new picture every ~3 s cut on the word, the literal noun on screen, red = the key word.
# The recurring picture is the patient in bed with a warm light inside the head: someone is in there.

BED = (W / 2, 1300, 880)        # the drawn bed: centre x, mattress top y, width


def trapped_rows(cr, t, rows, x=150, y0=680, dy=170, size=90):
    """The hook's checklist on slate: (label, time it shows, can or can't)."""
    for i, (lab, ts, ok) in enumerate(rows):
        y = y0 + dy * i
        draw_text(cr, lab, x, y, size, CREAM, prog(t, ts - 0.1, 0.3), anchor="lm")
        if ok:
            tick(cr, 760, y, 90, prog(t, ts + 0.1, 0.3), color=GREEN)
        else:
            cross(cr, 810, y, 90, prog(t, ts + 0.1, 0.3), color=CORAL)


def _beat(ph):
    """One heartbeat of an ECG trace over phase 0..1 (P wave, the spike, T wave)."""
    if 0.10 < ph < 0.14:
        return 0.15 * math.sin((ph - 0.10) / 0.04 * math.pi)
    if 0.18 < ph < 0.20:
        return -0.15
    if 0.20 <= ph < 0.23:
        return 1.0 - abs(ph - 0.215) / 0.015
    if 0.23 <= ph < 0.25:
        return -0.3
    if 0.32 < ph < 0.42:
        return 0.25 * math.sin((ph - 0.32) / 0.10 * math.pi)
    return 0.0


def ecg(cr, x, y, w, h, t, alpha=1.0, color=(0.35, 0.95, 0.55)):
    """A heart monitor: a dark screen with a green trace beating about once a second."""
    if alpha <= 0:
        return
    rrect(cr, x + 8, y + 14, w, h, 24)
    cr.set_source_rgba(0, 0, 0, 0.25 * alpha)
    cr.fill()
    rrect(cr, x, y, w, h, 24)
    cr.set_source_rgba(0.08, 0.10, 0.11, alpha)
    cr.fill()
    step = 4
    n = int((w - 60) / step)
    for i in range(n + 1):
        ph = ((i * step) / (w * 0.45) - t * 1.1) % 1
        px, py = x + 30 + i * step, y + h * 0.6 - _beat(ph) * h * 0.4
        (cr.move_to if i == 0 else cr.line_to)(px, py)
    cr.set_source_rgba(*color, alpha)
    cr.set_line_width(6)
    cr.stroke()
    draw_text(cr, "HEARTBEAT", x + 30, y + 26, 30, color, alpha, MONO_FONT, tracking=2)


def h_you(cr, t, tl, t0):                                # b1 frame 0: "doctors think you're in a coma... but you hear everything"
    _pic(cr, "patient", W / 2, 1120, 0, t, -1, frame=(940, 627), rot=-0.015)
    symbolic(cr, W / 2, 1460)
    ts = T(tl, "b1", "सुन")
    ring(cr, 770, 1075, 150, 120, prog(t, T(tl, "b1", "कोमा"), 0.4))
    incoming(cr, 770, 1075, t, RED, prog(t, ts - 0.2, 0.3), a0=-math.pi * 0.62, r0=160, r1=290)
    stamp(cr, t, "DOCTORS: COMA", T(tl, "b1", "डॉक्टरों"), 330, 1580, 54)
    headline(cr, t, "IN A COMA, BUT YOU", "HEAR EVERYTHING", -1, min(1.8, ts), t_ghost=-1)


def t_trapped(cr, t, tl, t0):                            # b1b "you can't even move a hand. can't speak either" (slate)
    hx, hy = sickbed(cr, W / 2, 1480, 760, mind=1.0)
    incoming(cr, hx, hy, t, CORAL, prog(t, t0, 0.3), a0=-math.pi * 0.3, r1=260)
    trapped_rows(cr, t, (("HEAR", t0, True), ("MOVE", T(tl, "b1b", "हिला"), False),
                         ("SPEAK", T(tl, "b1b", "बोल"), False)))
    headline(cr, t, "AWAKE INSIDE, BUT", "TRAPPED", t0, T(tl, "b1b", "बोल"), small_color=CREAM, big_color=CORAL)


def t_alive(cr, t, tl, t0):                              # b1b "...you're alive, but the body lies there like a corpse"
    tz, tl_ = T(tl, "b1b", "ज़िंदा"), T(tl, "b1b", "लाश")
    ecg(cr, 110, 620, 860, 330, t, prog(t, t0, 0.3))
    stamp(cr, t, "ALIVE", tz, 800, 1060, 60, color=GREEN)
    sickbed(cr, W / 2, 1420, 800, prog(t, t0 + 0.2, 0.3), mind=1.0)
    card(cr, t, tl_ + 0.1, 290, 1640, ["MOVEMENT: ZERO"], size=48, seed=6)
    headline(cr, t, "ALIVE, BUT THE BODY LIES", "LIKE A CORPSE", t0, tl_)


def t_true(cr, t, tl, t0):                               # b1c "this is no film: it really happened to a boy in South Africa"
    ts = T(tl, "b1c", "सच")
    world_pin(cr, t, t0, "south_africa", "SOUTH AFRICA", T(tl, "b1c", "अफ़्रीका"))
    stamp(cr, t, "IT REALLY HAPPENED", ts, W / 2, 1520, 60)
    headline(cr, t, "THIS IS NOT A", "FILM", t0, T(tl, "b1c", "फ़िल्म"), strike_at=ts, struck=True)


def m_age(cr, t, tl, t0):                                # b2 "12-year-old Martin suddenly fell ill"
    counter(cr, t, T(tl, "b2", "बारह") - 0.1, W / 2, 980, "12", 220)
    draw_text(cr, "YEARS OLD", W / 2, 1200, 70, INK, prog(t, T(tl, "b2", "साल"), 0.3), anchor="ct")
    card(cr, t, T(tl, "b2", "बीमार"), 300, 1400, ["SUDDENLY FELL ILL", "1988, SOUTH AFRICA"], size=46, seed=5)
    headline(cr, t, "A 12-YEAR-OLD BOY:", "MARTIN", t0, T(tl, "b2", "मार्टिन"))


def m_fade(cr, t, tl, t0):                               # b2 "...slowly his walking, talking, everything stopped"
    tw, tt, tb = T(tl, "b2", "चलना"), T(tl, "b2", "बोलना"), T(tl, "b2", "बंद")
    person(cr, 290, 1700, 1000, INK, prog(t, t0, 0.3) * (1 - 0.7 * prog(t, tb - 0.2, 0.6)))
    for i, (lab, ts) in enumerate((("WALK", tw), ("TALK", tt), ("MOVE", tb - 0.2))):
        y = 880 + 260 * i
        draw_text(cr, lab, 600, y, 110, INK, prog(t, ts - 0.1, 0.3), anchor="lm")
        if t > ts + 0.1:
            strike(cr, 580, y + 8, 940, y - 8, prog(t, ts + 0.1, 0.3))
    headline(cr, t, "SLOWLY, EVERYTHING", "STOPPED", t0, tb)


def m_doctors(cr, t, tl, t0):                            # b3 "doctors told his parents: take him home, keep him comfortable"
    _pic(cr, "doctor", 290, 1270, 760, t, t0)
    symbolic(cr, 290, 1670)
    card(cr, t, T(tl, "b3", "आख़िरी") - 0.2, 470, 1060, ["\"KEEP HIM COMFORTABLE", "TILL THE END.\""], size=36)
    headline(cr, t, "THE DOCTORS TO HIS PARENTS:", "TAKE HIM HOME", t0, T(tl, "b3", "घर"))


def w_wake(cr, t, tl, t0):                               # b4 "but a few years later, Martin's brain started waking up" (slate)
    tj = T(tl, "b4", "जागने")
    sickbed(cr, *BED, alpha=prog(t, t0, 0.3), mind=prog(t, tj - 0.2, 0.8))
    card(cr, t, T(tl, "b4", "साल"), 470, 640, ["A FEW YEARS LATER", "AROUND AGE 16"], size=40)
    headline(cr, t, "HIS BRAIN STARTED", "WAKING UP", t0, tj, small_color=CREAM, big_color=CORAL)


def w_same(cr, t, tl, t0):                               # b4 "...and exactly what you just imagined happened to him" (slate)
    hx, hy = sickbed(cr, W / 2, 1480, 760, mind=1.0)
    incoming(cr, hx, hy, t, CORAL, prog(t, t0, 0.3), a0=-math.pi * 0.3, r1=260)
    trapped_rows(cr, t, (("HEARS", t0 + 0.2, True), ("MOVES", t0 + 0.55, False), ("SPEAKS", t0 + 0.9, False)))
    headline(cr, t, "EXACTLY WHAT YOU", "IMAGINED", t0, T(tl, "b4", "सोचा"), small_color=CREAM, big_color=CORAL)


def n_noone(cr, t, tl, t0):                              # b5 "and nobody even knew that he was in there"
    _pic(cr, "patient", W / 2, 1120, 0, t, t0, frame=(800, 533), rot=0.02)
    symbolic(cr, W / 2, 1410)
    for k, (x0, dx) in enumerate(((-160, 1400), (1240, -1400))):    # people walking past the bed
        f = clamp01((t - t0 - 0.3 - 0.5 * k) / 2.6)
        if 0 < f < 1:
            person(cr, x0 + dx * f, 1800, 520, INK, 0.85)
    ta = T(tl, "b5", "अंदर")
    ring(cr, 700, 1095, 130, 105, prog(t, ta, 0.4))
    headline(cr, t, "NOBODY KNEW HE WAS", "IN THERE", t0, ta)


def c_switch(cr, t, tl, t0):                             # b6 "how? in a coma, the brain's wake-up switch turns off" (slate)
    tb = T(tl, "b6", "बंद")
    lit_brain(cr, t, t0, 360, 1120, 480, 1 - prog(t, tb, 0.3))
    switch(cr, 850, 1120, 380, 1 - prog(t, tb - 0.1, 0.2), prog(t, t0 + 0.2, 0.3))
    stamp(cr, t, "COMA", T(tl, "b6", "कोमा"), 360, 1520, 70, color=CORAL)
    headline(cr, t, "THE BRAIN'S WAKE-UP SWITCH:", "OFF", t0, tb, small_color=CREAM, big_color=CORAL)


def c_eyes(cr, t, tl, t0):                               # b6 "...eyes closed, no awareness"
    _eye(cr, W / 2, 1020, 640, 1 - 0.96 * prog(t, t0 + 0.55, 0.4), prog(t, t0, 0.3))
    stamp(cr, t, "NO AWARENESS", T(tl, "b6", "होश"), W / 2, 1420, 64)
    headline(cr, t, "EYES", "CLOSED", t0, t0 + 0.3)


def c_weeks(cr, t, tl, t0):                              # b6 "...and it usually ends within a few weeks"
    tw = T(tl, "b6", "हफ़्तों")
    calendar(cr, t, tw - 0.3, W / 2, 1080, ["WEEK 1", "WEEK 2", "WEEK 3", "WEEK 4"], "a coma usually lasts",
             interval=0.3, w=460, h=470)
    card(cr, t, T(tl, "b6", "ख़त्म"), 290, 1450, ["RARELY MORE THAN", "ABOUT 4 WEEKS"], size=44)
    headline(cr, t, "USUALLY OVER IN A FEW", "WEEKS", t0, tw)


def v_fork(cr, t, tl, t0):                               # b7 "some wake up; some reach a strange state"
    tj, ta = T(tl, "b7", "जाग"), T(tl, "b7", "अजीब")
    card(cr, t, t0, 430, 600, ["COMA"], size=64)
    path(cr, [(540, 760), (540, 900), (290, 1060), (290, 1220)], prog(t, tj - 0.2, 0.5), 9, INK, arrow=True)
    path(cr, [(540, 900), (790, 1060), (790, 1220)], prog(t, ta - 0.2, 0.5), 9, RED, arrow=True)
    draw_text(cr, "WAKE UP", 290, 1270, 76, GREEN, prog(t, tj + 0.2, 0.3), anchor="ct")
    tick(cr, 245, 1470, 90, prog(t, tj + 0.4, 0.3), color=GREEN)
    draw_text(cr, "?", 790, 1260, 170, RED, prog(t, ta + 0.1, 0.3), anchor="ct")
    draw_text(cr, "A STRANGE STATE", 790, 1480, 34, RED, prog(t, ta + 0.3, 0.3), MONO_FONT, "ct", tracking=2)
    headline(cr, t, "AFTER A COMA:", "TWO PATHS", t0, tj)


def v_state(cr, t, tl, t0):                              # b7 "...eyes open, sleeping and waking, but no response" (slate)
    ts, tj = T(tl, "b7", "सोना"), T(tl, "b7", "जवाब")
    sickbed(cr, *BED, alpha=prog(t, t0, 0.3), eyes=1.0)
    sun_moon(cr, 780, 860, 130, t - ts, prog(t, ts - 0.2, 0.3))
    draw_text(cr, "EYES OPEN", 150, 820, 52, CREAM, prog(t, t0 + 0.2, 0.3), anchor="lm")
    draw_text(cr, "SLEEPS, WAKES", 150, 900, 52, CREAM, prog(t, ts, 0.3), anchor="lm")
    stamp(cr, t, "NO RESPONSE", tj, W / 2, 1650, 60, color=CORAL)
    draw_text(cr, "DOCTORS CALL IT A VEGETATIVE STATE", W / 2, 1770, 30, CREAM, prog(t, tj + 0.3, 0.3), MONO_FONT, "ct",
              tracking=1)
    headline(cr, t, "EYES OPEN, BUT", "NO RESPONSE", t0, tj, small_color=CREAM, big_color=CORAL)


def q_squeeze(cr, t, tl, t0):                            # b8 "doctors say: squeeze my hand. no answer..."
    _pic(cr, "hand_iv", W / 2, 1110, 0, t, t0, frame=(900, 675), rot=-0.02)
    tn = T(tl, "b8", "नहीं")
    cross(cr, 640, 1180, 200, prog(t, tn, 0.3))
    card(cr, t, tn + 0.2, 330, 1520, ["NO SQUEEZE"], size=56, seed=6)
    headline(cr, t, "THE BEDSIDE TEST:", "SQUEEZE MY HAND", t0, T(tl, "b8", "दबाओ"))


def q_nobody(cr, t, tl, t0):                             # b8 "...so it's assumed: there's no awareness inside" (slate)
    ta = T(tl, "b8", "अंदर")
    hx, hy = sickbed(cr, *BED, alpha=prog(t, t0, 0.3))
    ring(cr, hx, hy, 115, 115, prog(t, ta - 0.2, 0.4), color=CORAL)
    draw_text(cr, "?", hx + 150, hy - 190, 150, CORAL, prog(t, ta, 0.3), anchor="cm")
    headline(cr, t, "SO THEY ASSUME:", "NOBODY INSIDE", t0, ta, small_color=CREAM, big_color=CORAL)


def o_2006(cr, t, tl, t0):                               # b9 "but in 2006, a Cambridge scientist..."
    world_pin(cr, t, t0, "uk", "CAMBRIDGE, UK", T(tl, "b9", "कैम्ब्रिज"))
    counter(cr, t, T(tl, "b9", "हज़ार") - 0.2, W / 2, 1450, "2006", 110)
    card(cr, t, T(tl, "b9", "साइंटिस्ट"), 350, 1590, ["ADRIAN OWEN", "NEUROSCIENTIST"], size=44)
    headline(cr, t, "2006, CAMBRIDGE:", "A NEW TEST", t0, T(tl, "b9", "साइंटिस्ट"))


def o_mri(cr, t, tl, t0):                                # b9 "...put a young woman like this in an MRI"
    _pic(cr, "mri", 540, 1080, 620, t, t0)
    card(cr, t, T(tl, "b9", "लिटाया") - 0.2, 150, 1470, ["fMRI: SHOWS WHICH PART", "OF THE BRAIN IS WORKING"], size=40)
    headline(cr, t, "A YOUNG WOMAN, 23, IN AN", "MRI", t0, T(tl, "b9", "एमआरआई"))


def o_tennis(cr, t, tl, t0):                             # b9 "...and said: imagine you're playing tennis" (slate)
    tt = T(tl, "b9", "टेनिस")
    hx, hy = sickbed(cr, W / 2, 1580, 760, prog(t, t0, 0.3))
    bubble(cr, 700, 1010, 540, 440, (hx + 40, hy - 60), prog(t, t0 + 0.2, 0.3))
    _pic(cr, "racket", 700, 1010, 380, t, tt - 0.2, rot=0.5)
    headline(cr, t, "THEY SAID: IMAGINE PLAYING", "TENNIS", t0, tt, small_color=CREAM, big_color=CORAL)


def o_glow(cr, t, tl, t0):                               # b10 "and exactly that part of her brain lit up..." (slate)
    tc = T(tl, "b10", "चमक")
    lit_brain(cr, t, t0, W / 2, 1080, 620, prog(t, tc - 0.1, 0.3), "HER BRAIN")
    card(cr, t, tc, 230, 1530, ["THE AREA THAT", "PLANS MOVEMENT"], size=48)
    headline(cr, t, "HER BRAIN", "LIT UP", t0, tc, small_color=CREAM, big_color=CORAL)


def o_same(cr, t, tl, t0):                               # b10 "...the same as a healthy person's when they imagine tennis" (slate)
    tn = T(tl, "b10", "नॉर्मल")
    lit_brain(cr, t, -9, 290, 1050, 300, 1.0, "HER")
    lit_brain(cr, t, tn - 0.2, 790, 1050, 300, prog(t, tn + 0.2, 0.3), "HEALTHY PERSON")
    stamp(cr, t, "SAME SPOT", T(tl, "b10", "चमकता"), W / 2, 1450, 70, color=CORAL)
    headline(cr, t, "EXACTLY LIKE A", "HEALTHY BRAIN", t0, tn, small_color=CREAM, big_color=CORAL)


def o_inside(cr, t, tl, t0):                             # b11 "she was in there, hearing all; only her body couldn't answer"
    hx, hy = sickbed(cr, *BED, alpha=prog(t, t0, 0.3), mind=1.0)
    incoming(cr, hx, hy, t, RED, prog(t, T(tl, "b11", "सुन"), 0.3), a0=-math.pi * 0.3)
    card(cr, t, T(tl, "b11", "शरीर"), 260, 1620, ["ONLY HER BODY", "COULDN'T ANSWER"], size=48)
    headline(cr, t, "SHE WAS", "IN THERE", t0, T(tl, "b11", "अंदर"))


def y_code(cr, t, tl, t0):                               # b12 "then the trick was turned into yes and no"
    th = T(tl, "b12", "हाँ")
    _pic(cr, "racket", 280, 1000, 520, t, th - 0.3, rot=0.35)
    house(cr, 800, 1200, 360, INK, prog(t, th, 0.3))
    card(cr, t, th + 0.1, 110, 1360, ["TENNIS", "MEANS YES"], size=60)
    card(cr, t, th + 0.5, 610, 1360, ["HOUSE", "MEANS NO"], size=60, seed=6)
    headline(cr, t, "THE TRICK BECAME", "YES AND NO", t0, th)


def y_canada(cr, t, tl, t0):                             # b12 "...a man in Canada, in this state for 12 years..."
    world_pin(cr, t, t0, "canada", "CANADA", T(tl, "b12", "कनाडा"))
    counter(cr, t, T(tl, "b12", "बारह") - 0.1, 360, 1480, "12", 120)
    draw_text(cr, "YEARS", 470, 1480, 64, INK, prog(t, T(tl, "b12", "साल"), 0.3), anchor="lm")
    headline(cr, t, "CANADA: UNRESPONSIVE FOR", "12 YEARS", t0, T(tl, "b12", "बारह"))


def y_pain(cr, t, tl, t0):                               # b12 "...was asked: do you feel pain?" (slate)
    td = T(tl, "b12", "दर्द")
    _pic(cr, "mri", 540, 1150, 560, t, t0)
    draw_text(cr, "?", 880, 1500, 200, CORAL, prog(t, td, 0.3), anchor="cm")
    headline(cr, t, "THEN THEY ASKED HIM:", "ARE YOU IN PAIN?", t0, td, small_color=CREAM, big_color=CORAL)


def y_no(cr, t, tl, t0):                                 # b13 "his brain answered: no" (slate)
    tn = T(tl, "b13", "नहीं")
    lit_brain(cr, t, t0, W / 2, 900, 440, prog(t, T(tl, "b13", "दिमाग़"), 0.3))
    p = prog(t, tn, 0.25)
    cr.save()
    cr.translate(W / 2, 1400)
    cr.scale(1.3 - 0.3 * p, 1.3 - 0.3 * p)
    draw_text(cr, "NO", 0, 0, 320, CORAL, p, anchor="cm")
    cr.restore()
    card(cr, t, tn + 0.4, 330, 1620, ["NOT IN PAIN"], size=56)
    headline(cr, t, "HIS BRAIN", "ANSWERED", t0, T(tl, "b13", "जवाब"), small_color=CREAM, big_color=CORAL)


def s_study(cr, t, tl, t0):                              # b14 "and in 2024, a study of over 300 patients found..."
    counter(cr, t, T(tl, "b14", "चौबीस") - 0.3, W / 2, 640, "2024", 100)
    _pic(cr, "eeg", 300, 1060, 0, t, t0 + 0.2, frame=(480, 320), rot=-0.03)
    _pic(cr, "fmri_scan", 790, 1060, 0, t, t0 + 0.4, frame=(470, 266), rot=0.03)
    draw_text(cr, "EEG", 300, 1250, 36, INK, prog(t, t0 + 0.4, 0.3), MONO_FONT, "ct", tracking=2)
    draw_text(cr, "fMRI", 790, 1220, 36, INK, prog(t, t0 + 0.6, 0.3), MONO_FONT, "ct", tracking=2)
    card(cr, t, T(tl, "b14", "स्टडी"), 230, 1400, ["BRAIN SCANS: fMRI, EEG", "6 MEDICAL CENTRES"], size=44)
    headline(cr, t, "2024: A BIG STUDY OF", "353 PATIENTS", t0, T(tl, "b14", "तीन"))


QUARTER = (2, 5, 11, 14, 18)     # the 5 of 20 figures who light up: 1 in 4


def s_quarter(cr, t, tl, t0):                            # b14 "...of the patients who don't respond, 1 in 4's brain understood" (slate)
    t4, t1 = T(tl, "b14", "चार"), T(tl, "b14", "एक")
    for i in range(20):
        x, y = 190 + (i % 5) * 175, 830 + (i // 5) * 235
        lit = i in QUARTER and t > t1
        person(cr, x, y, 190, WARM if lit else CREAM, prog(t, t0 + 0.03 * i, 0.2))
        if lit:
            glow(cr, x, y - 190 * 0.87, 20, WARM, prog(t, t1 + 0.06 * QUARTER.index(i), 0.3))
    card(cr, t, T(tl, "b14", "समझ") - 0.2, 170, 1600, ["THEIR BRAINS FOLLOWED", "INSTRUCTIONS ON THE SCAN"], size=42)
    headline(cr, t, "PATIENTS WHO DON'T RESPOND:", "1 IN 4", t0, t4, small_color=CREAM, big_color=CORAL)


def r_martin(cr, t, tl, t0):                             # b15 "and Martin? at 25..."
    _pic(cr, "patient", W / 2, 1060, 0, t, t0, frame=(820, 547), rot=-0.02)
    symbolic(cr, W / 2, 1360)
    counter(cr, t, T(tl, "b15", "पच्चीस") - 0.1, 400, 1540, "25", 120)
    draw_text(cr, "YEARS OLD", 510, 1540, 56, INK, prog(t, T(tl, "b15", "उम्र"), 0.3), anchor="lm")
    headline(cr, t, "AND", "MARTIN?", t0, T(tl, "b15", "मार्टिन"))


def r_eye(cr, t, tl, t0):                                # b15 "...a therapist noticed movement in his eyes"
    _pic(cr, "eye", W / 2, 1060, 0, t, t0, frame=(940, 627), rot=0.015)
    symbolic(cr, W / 2, 1400)
    ring(cr, 515, 1170, 230, 120, prog(t, T(tl, "b15", "हलचल"), 0.4))
    card(cr, t, t0 + 0.3, 150, 1470, ["AN AROMATHERAPIST", "VIRNA VAN DER WALT"], size=44)
    headline(cr, t, "A THERAPIST SAW IT IN HIS", "EYES", t0, T(tl, "b15", "आँखों"))


def r_truth(cr, t, tl, t0):                              # b15 "...tests were done, and the truth came out" (slate)
    ts = T(tl, "b15", "सच")
    sickbed(cr, *BED, alpha=prog(t, t0, 0.3), mind=1.0, eyes=1.0)
    card(cr, t, t0 + 0.2, 110, 620, ["UNIVERSITY OF PRETORIA", "COMMUNICATION CENTRE"], size=38)
    tick(cr, 760, 900, 130, prog(t, ts, 0.3), color=GREEN)
    headline(cr, t, "TESTS PROVED IT: HE WAS", "AWARE", t0, ts, small_color=CREAM, big_color=CORAL)


def l_computer(cr, t, tl, t0):                           # b16 "today Martin talks through a computer"
    tc = T(tl, "b16", "कंप्यूटर")
    laptop(cr, W / 2, 1320, 720, prog(t, t0, 0.3), "HELLO.", prog(t, tc, 0.8))
    waveform(cr, 300, 1530, 480, 130, t, RED, prog(t, tc + 0.6, 0.3))
    headline(cr, t, "TODAY HE TALKS THROUGH A", "COMPUTER", t0, tc)


def l_life(cr, t, tl, t0):                               # b16 "...he's married, and wrote a book about it: Ghost Boy"
    _pic(cr, "rings", 290, 960, 250, t, t0)
    draw_text(cr, "MARRIED IN 2009", 290, 1110, 34, INK, prog(t, t0 + 0.2, 0.3), MONO_FONT, "ct", tracking=2)
    book(cr, 770, 1210, 600, prog(t, T(tl, "b16", "किताब") - 0.2, 0.3))
    draw_text(cr, "2011", 770, 1540, 36, INK, prog(t, T(tl, "b16", "किताब"), 0.3), MONO_FONT, "ct", tracking=2)
    headline(cr, t, "AND HE WROTE A BOOK:", "GHOST BOY", t0, T(tl, "b16", "घोस्ट"))


def f_voices(cr, t, tl, t0):                             # b17 "in one small study, hearing old memories in loved ones' voices..."
    _pic(cr, "headphones", 300, 1080, 540, t, t0)
    waveform(cr, 610, 960, 400, 160, t, RED, prog(t, T(tl, "b17", "आवाज़"), 0.3))
    card(cr, t, T(tl, "b17", "यादें") - 0.2, 560, 1120, ["FAMILY STORIES", "4 TIMES A DAY, 6 WEEKS"], size=40)
    card(cr, t, T(tl, "b17", "छोटी"), 290, 1520, ["15 PATIENTS, 2015"], size=44, seed=6)
    headline(cr, t, "LOVED ONES' VOICES, OLD", "MEMORIES", t0, T(tl, "b17", "यादें"))


def f_faster(cr, t, tl, t0):                             # b17 "...patients regained consciousness sooner" (slate)
    tj = T(tl, "b17", "जल्दी")
    for i, (lab, col, reach, dur) in enumerate((("WITH FAMILY STORIES", CORAL, 1.0, 0.9), ("WITHOUT", CREAM, 0.55, 1.4))):
        y = 700 + 230 * i
        draw_text(cr, lab, 120, y, 40, col, prog(t, t0 + 0.1 * i, 0.3), MONO_FONT, "lb", tracking=2)
        cr.rectangle(120, y + 20, 840, 50)
        cr.set_source_rgba(*CREAM, 0.15 * prog(t, t0, 0.3))
        cr.fill()
        cr.rectangle(120, y + 20, 840 * reach * prog(t, t0 + 0.3, dur), 50)
        cr.set_source_rgba(*col, prog(t, t0, 0.3))
        cr.fill()
    draw_text(cr, "WAKING UP, SMALL STUDY", W / 2, 1220, 30, CREAM, 0.7 * prog(t, t0 + 0.4, 0.3), MONO_FONT, "ct",
              tracking=2)
    sickbed(cr, W / 2, 1520, 640, prog(t, t0 + 0.2, 0.3), mind=1.0, eyes=1.0 if t > tj else 0.0)
    headline(cr, t, "THEY WOKE UP", "SOONER", t0, tj, small_color=CREAM, big_color=CORAL)


def z_hands(cr, t, tl, t0):                              # b18 "so if someone close to you ever seems unconscious..."
    _pic(cr, "hands", W / 2, 1090, 0, t, t0, frame=(940, 627), rot=-0.015)
    tb = T(tl, "b18", "बात")
    waveform(cr, 300, 1530, 480, 130, t, RED, prog(t, tb, 0.3))
    headline(cr, t, "IF A LOVED ONE IS UNCONSCIOUS,", "KEEP TALKING", t0, tb)


def z_hear(cr, t, tl, t0):                               # b18 "...they might be hearing everything" (slate)
    hx, hy = sickbed(cr, *BED, alpha=prog(t, t0, 0.3), mind=prog(t, t0 + 0.3, 0.6))
    incoming(cr, hx, hy, t, CORAL, prog(t, t0 + 0.2, 0.3), a0=-math.pi * 0.3)
    headline(cr, t, "THEY MIGHT BE", "LISTENING", t0, T(tl, "b18", "सुन"), small_color=CREAM, big_color=CORAL)


def e_question(cr, t, tl, t0):                           # b19 "did you know someone who looks unconscious can hear everything?"
    _pic(cr, "patient", W / 2, 880, 0, t, t0, frame=(760, 507), rot=-0.02)
    yes_no_card(cr, t, T(tl, "b19", "यस") - 0.2, W / 2, 1420, w=560, h=300, question="COMMENT: YES OR NO")
    headline(cr, t, "DID YOU KNOW THEY CAN", "HEAR YOU?", t0, T(tl, "b19", "सुन"), t_ghost=t0)


SHOTS = [   # (line, cue where the shot starts, draw function, background)
    ("b1", None, h_you, "paper"),
    ("b1b", None, t_trapped, "slate"), ("b1b", "ज़िंदा", t_alive, "paper"),
    ("b1c", None, t_true, "paper"),
    ("b2", None, m_age, "paper"), ("b2", "धीरे", m_fade, "paper"),
    ("b3", None, m_doctors, "paper"),
    ("b4", None, w_wake, "slate"), ("b4", "और", w_same, "slate"),
    ("b5", None, n_noone, "paper"),
    ("b6", None, c_switch, "slate"), ("b6", "आँखें", c_eyes, "paper"), ("b6", "अक्सर", c_weeks, "paper"),
    ("b7", None, v_fork, "paper"), ("b7", "आँखें", v_state, "slate"),
    ("b8", None, q_squeeze, "paper"), ("b8", "मान", q_nobody, "slate"),
    ("b9", None, o_2006, "paper"), ("b9", "ऐसी", o_mri, "paper"), ("b9", "कहा", o_tennis, "slate"),
    ("b10", None, o_glow, "slate"), ("b10", "जो", o_same, "slate"),
    ("b11", None, o_inside, "paper"),
    ("b12", None, y_code, "paper"), ("b12", "कनाडा", y_canada, "paper"), ("b12", "पूछा", y_pain, "slate"),
    ("b13", None, y_no, "slate"),
    ("b14", None, s_study, "paper"), ("b14", "जो", s_quarter, "slate"),
    ("b15", None, r_martin, "paper"), ("b15", "थेरेपिस्ट", r_eye, "paper"), ("b15", "टेस्ट", r_truth, "slate"),
    ("b16", None, l_computer, "paper"), ("b16", "शादी", l_life, "paper"),
    ("b17", None, f_voices, "paper"), ("b17", "मरीज़", f_faster, "slate"),
    ("b18", None, z_hands, "paper"), ("b18", "शायद", z_hear, "slate"),
    ("b19", None, e_question, "paper"),
]


def draw(cr, t, tl):
    draw_frame(cr, t, tl, SHOTS)


def sfx(tl):
    """A whoosh on every cut, thuds on the cross and the answer, ticks (and music dips) before the tennis reveal, the
    answer, the re-hook and the closing line, typing under the laptop."""
    ev = [(s, "whoosh", 0.25) for s in starts(tl, SHOTS)[1:]]
    ev += [(T(tl, "b8", "नहीं"), "thud", 0.0), (T(tl, "b13", "नहीं"), "thud", 0.0), (T(tl, "b2", "बंद"), "thud", 0.0),
           (T(tl, "b1b", "बोल"), "thud", 0.0), (T(tl, "b1c", None) - 0.35, "tick", 0.0),
           (T(tl, "b10", None) - 0.35, "tick", 0.0), (T(tl, "b13", None) - 0.35, "tick", 0.0),
           (T(tl, "b15", None) - 0.35, "tick", 0.0), (T(tl, "b19", None) - 0.35, "tick", 0.0),
           (T(tl, "b16", "कंप्यूटर"), "typing", 0.8), (T(tl, "b19", "यस"), "typing", 1.0)]
    for bid in ("b2", "b9", "b14", "b15"):
        ev.append((tl[bid].start + 0.4, "pop", 0.0))
    ev += [(at, "dip", 0.5) for at, name, _ in list(ev) if name == "tick"]   # the bed dips just before a reveal
    return ev
