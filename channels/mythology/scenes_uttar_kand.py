"""Scenes for videos/uttar_kand.py (long video 3, landscape): the shot list, a Hindi label for every sentence, the fast
camera (camera_beats: a new framing at every line, no framing held over 2.6 s), and sparse sound effects that never
start over a spoken word. The shots are in uk_shots_a (u001-u055) and uk_shots_b (u056-u111); shared pieces in
uk_base. Shots whose cards must stay whole set hud=True (their ui is drawn outside the camera's zoom)."""
import camera_beats
import puppet_core as pc
import uk_base as B
import uk_shots_a as A
import uk_shots_b as SB
from channel import SFX_KEEP, SFX_MIN_GAP
from scenes_jarasandha import motes
from scenes_jayadratha import tint
from shots import T

DUSK = (1.0, 0.64, 0.44)
PALACE = (1.0, 0.84, 0.64)
FOREST = (0.88, 1.0, 0.80)
NIGHT_BLUE = (0.60, 0.70, 1.0)
GOLDC = (1.0, 0.88, 0.60)
RIVER = (0.80, 0.92, 1.0)
ANGER = (1.0, 0.58, 0.48)

SHOTS = [   # (first line, draw function, options)
    ("u001", A.s_movie, dict(focus=(900, 640), place=(DUSK, 0.35))),
    ("u003", A.s_flash_sita, dict(focus=(960, 640), place=(FOREST, 0.3))),
    ("u004", A.s_flash_boys, dict(focus=(960, 640), place=(PALACE, 0.3))),
    ("u005", A.s_flash_lk, dict(focus=(960, 700), place=(RIVER, 0.35))),
    ("u006", A.s_books, dict(focus=(960, 560), place=(GOLDC, 0.25), hud=True)),
    ("u009", A.s_return, dict(focus=(960, 640), place=(DUSK, 0.3))),
    ("u011", A.s_wish, dict(focus=(960, 640), place=(PALACE, 0.3))),
    ("u015", A.s_court, dict(focus=(960, 640), place=(NIGHT_BLUE, 0.35))),
    ("u018", A.s_rumour, dict(focus=(960, 560), place=(NIGHT_BLUE, 0.3))),
    ("u021", A.s_heart, dict(focus=(960, 620), place=(NIGHT_BLUE, 0.3), hud=True)),
    ("u024", A.s_order, dict(focus=(960, 640), place=(PALACE, 0.3))),
    ("u026", A.s_question1, dict(focus=(960, 640), frames=[(1.0, (960, 640))], hud=True)),
    ("u027", A.s_chariot, dict(focus=(960, 700), place=(DUSK, 0.2))),
    ("u029", A.s_truth, dict(focus=(900, 660), place=(RIVER, 0.3))),
    ("u032", A.s_message, dict(focus=(860, 660), place=(RIVER, 0.3))),
    ("u036", A.s_valmiki, dict(focus=(960, 640), place=(FOREST, 0.3))),
    ("u040", A.s_twins, dict(focus=(960, 680), place=(GOLDC, 0.25))),
    ("u042", A.s_teach, dict(focus=(900, 640), place=(FOREST, 0.3))),
    ("u046", A.s_yagya, dict(focus=(960, 660), place=(GOLDC, 0.3))),
    ("u049", A.s_song, dict(focus=(1000, 640), place=(PALACE, 0.3))),
    ("u053", A.s_gold, dict(focus=(1000, 640), place=(GOLDC, 0.3))),
    ("u056", SB.s_summon, dict(focus=(960, 640), place=(PALACE, 0.3), hud=True)),
    ("u058", SB.s_assembly, dict(focus=(960, 640), place=(PALACE, 0.3))),
    ("u060", SB.s_earth, dict(focus=(960, 700), place=(GOLDC, 0.3))),
    ("u065", SB.s_born, dict(focus=(960, 700), place=(GOLDC, 0.25))),
    ("u068", SB.s_grief, dict(focus=(960, 700), place=(NIGHT_BLUE, 0.3))),
    ("u070", SB.s_years, dict(focus=(1100, 640), place=(DUSK, 0.3))),
    ("u074", SB.s_room, dict(focus=(900, 640), place=(NIGHT_BLUE, 0.3), hud=True)),
    ("u078", SB.s_durvasa, dict(focus=(1060, 640), place=(ANGER, 0.35))),
    ("u083", SB.s_choice, dict(focus=(960, 620), place=(ANGER, 0.25))),
    ("u085", SB.s_sees, dict(focus=(960, 640), frames=[(1.0, (960, 640)), (1.15, (960, 700))], hud=True,
                             place=(NIGHT_BLUE, 0.25))),
    ("u087", SB.s_banish, dict(focus=(960, 640), place=(NIGHT_BLUE, 0.3), hud=True)),
    ("u091", SB.s_sarayu, dict(focus=(900, 660), place=(RIVER, 0.3))),
    ("u094", SB.s_together, dict(focus=(800, 640), place=(FOREST, 0.3))),
    ("u095", SB.s_kingdoms, dict(focus=(960, 640), place=(PALACE, 0.3))),
    ("u098", SB.s_hanuman, dict(focus=(960, 640), place=(GOLDC, 0.3))),
    ("u101", SB.s_walk, dict(focus=(1000, 660), place=(DUSK, 0.25))),
    ("u104", SB.s_vishnu, dict(focus=(960, 600), place=(GOLDC, 0.25))),
    ("u108", SB.s_end, dict(focus=(960, 640), frames=[(1.0, (960, 640)), (1.12, (960, 680))], hud=True)),
]

LABELS = {
    "u001": "रामायण मूवी: रावण का अंत", "u002": "पर कहानी ख़त्म नहीं", "u003": "सीता: जंगल में",
    "u004": "अपने बेटे, अनजान", "u005": "लक्ष्मण का त्याग", "u006": "उत्तर कांड",
    "u007": "मानस में नहीं, वाल्मीकि में है", "u008": "रामायण के बाद...", "u009": "अयोध्या वापसी",
    "u010": "राम राजा बने", "u011": "सीता माँ बनने वाली थीं", "u012": "तुम्हें क्या चाहिए?",
    "u013": "ऋषियों के आश्रम", "u014": "कल ही जाना", "u015": "लोग क्या कहते हैं?", "u016": "दोस्त चुप",
    "u017": "एक बात...", "u018": "सीता: लंका में", "u019": "राजा वापस ले आए", "u020": "प्रजा की बातें",
    "u021": "राम का दिल टूटा", "u022": "सीता: पवित्र", "u023": "राजा का फ़र्ज़", "u024": "भाइयों को बुलाया",
    "u025": "सीता को छोड़ आओ", "u026": "क्या राम ने सही किया?", "u027": "अगली सुबह", "u028": "आश्रम घूमने?",
    "u029": "लक्ष्मण रो पड़े", "u030": "राम ने त्याग दिया", "u031": "सीता गिर पड़ीं",
    "u032": "गंगा में जान दे देती...", "u033": "पेट में राजा का वंश", "u034": "मैं अपने लिए दुखी नहीं",
    "u035": "लक्ष्मण लौट गए", "u036": "एक ऋषि आए", "u037": "वाल्मीकि", "u038": "रामायण लिखने वाले",
    "u039": "बेटी की तरह", "u040": "जुड़वाँ बेटे", "u041": "लव और कुश", "u042": "एक लंबा गीत",
    "u043": "पूरी रामायण", "u044": "अपने पिता की कहानी", "u045": "पर उन्हें पता नहीं", "u046": "राम का बड़ा यज्ञ",
    "u047": "दूसरी शादी नहीं", "u048": "सीता की सोने की मूर्ति", "u049": "वाल्मीकि, लव और कुश",
    "u050": "राम के सामने रामायण", "u051": "अपनी ही कहानी", "u052": "बिल्कुल राम जैसे!", "u053": "सोना? नहीं!",
    "u054": "हम आश्रम वाले", "u055": "ये राम के बेटे!", "u056": "सीता को बुलवाया", "u057": "एक शर्त",
    "u058": "भरी सभा", "u059": "वाल्मीकि की क़सम", "u060": "धरती माँ से विनती", "u061": "धरती माँ, गोद में ले लो",
    "u062": "धरती फटी!", "u063": "धरती माँ की गोद", "u064": "सीता धरती में समा गईं",
    "u065": "धरती से पैदा हुई थीं", "u066": "जनक को खेत में मिलीं", "u067": "धरती में ही लौट गईं",
    "u068": "राम का दुख", "u069": "सीता कभी नहीं लौटीं", "u070": "बहुत साल बीते", "u071": "एक तपस्वी",
    "u072": "कोई आम तपस्वी नहीं", "u073": "काल: मौत का रूप", "u074": "अकेले में बात", "u075": "जो सुनेगा, उसे मौत",
    "u076": "दरवाज़े पर लक्ष्मण", "u077": "आपका काम पूरा हुआ", "u078": "ऋषि दुर्वासा", "u079": "सबसे ग़ुस्सैल ऋषि",
    "u080": "अभी मिलना है!", "u081": "थोड़ा रुक जाइए", "u082": "पूरे राज्य को श्राप!", "u083": "अकेला मैं मरूँ",
    "u084": "लक्ष्मण अंदर गए", "u085": "राम समझ गए", "u086": "वादा, या भाई?", "u087": "अपना वादा निभाइए",
    "u088": "गुरु वशिष्ठ", "u089": "मैं तुम्हें त्यागता हूँ", "u090": "त्याग = मौत", "u091": "सरयू के किनारे",
    "u092": "ध्यान, साँस रोकी", "u093": "स्वर्ग की ओर", "u094": "चौदह साल का साथी", "u095": "राम अकेले",
    "u096": "राज्य बेटों में", "u097": "कुशावती और श्रावस्ती", "u098": "हनुमान, धरती पर रहना",
    "u099": "जब तक मेरी कहानी", "u100": "आज भी धरती पर?", "u101": "सरयू की ओर", "u102": "अयोध्या के लोग साथ",
    "u103": "राम के बिना नहीं", "u104": "ब्रह्मा और देवता", "u105": "राम सरयू में", "u106": "भगवान विष्णु का रूप",
    "u107": "सब स्वर्ग में", "u108": "रामायण के बाद", "u109": "फ़र्ज़ के लिए परिवार खोया",
    "u110": "पहले सीता, फिर लक्ष्मण", "u111": "राजा का धर्म, या परिवार?",
}
RED_LABELS = {"u005", "u026", "u030", "u055", "u062", "u064", "u073", "u075", "u082", "u086", "u089", "u090",
              "u106", "u111"}


def line_at(t, tl):
    """(index, beat) of the line being spoken at t (or the one just finished)."""
    k = 0
    for i, b in enumerate(tl.beats):
        if b.start - 0.15 <= t:
            k = i
    return k, tl.beats[k]


def labels(cr, t, tl):
    k, b = line_at(t, tl)
    nxt = tl.beats[k + 1].start - 0.2 if k + 1 < len(tl.beats) else tl.total - 0.1
    text = LABELS.get(b.id)
    if text:
        B.label(cr, t, b.start + 0.05, text, nxt, col=B.RED if b.id in RED_LABELS else B.INK,
                under=b.id in RED_LABELS)


def shot_at(t, tl):
    cache = getattr(tl, "_uk_shots", None)
    if cache is None:
        starts = [0.0]
        for first, _, _ in SHOTS[1:]:
            starts.append(max(T(tl, first) - 0.12, starts[-1] + 0.5))
        cache = tl._uk_shots = starts
    k = 0
    for i, s in enumerate(cache):
        if t >= s:
            k = i
    return k, cache[k], cache[k + 1] if k + 1 < len(cache) else tl.total


def draw(cr, t, tl):
    k, t0, t1 = shot_at(t, tl)
    _, fn, opt = SHOTS[k]
    z, (fx, fy) = camera_beats.camera(tl, t, t0, t1, opt)
    cr.save()
    cr.translate(fx, fy)
    cr.scale(z, z)
    cr.translate(-fx, -fy)
    pc.screen(cr)
    out = fn(cr, t, tl, t0, t1) or {}
    tint(cr, (1.0, 0.66, 0.42), out.get("eve", 0.0))
    if opt.get("place"):
        col, a = opt["place"]
        tint(cr, col, a)
    if out.get("ui") and not opt.get("hud"):
        out["ui"](cr)
    cr.restore()
    if out.get("ui") and opt.get("hud"):
        out["ui"](cr)                     # cards stay whole: drawn outside the zoom
    motes(cr, t)
    pc.lamp(cr, t, night=max(out.get("night", 0.0), opt.get("night", 0.0)), flash=out.get("flash", 0.0))
    labels(cr, t, tl)
    if k > 0 and t - t0 < 0.22:
        cr.set_source_rgba(0.02, 0.01, 0.0, 0.35 * (1 - (t - t0) / 0.22))
        cr.paint()
    pc.finish(cr, t)


def after_voice(tl, a):
    for b in tl.beats:
        if b.start - 0.15 <= a < b.end:
            return b.end + 0.06 if b.end + 1.0 < tl.total else max(0.0, b.start - 0.3)
    return a


def sfx(tl):
    """Sparse sounds at the turning points, each moved into the pause after its sentence, SFX_MIN_GAP apart."""
    want = [(B.lf(tl, "u001", 0.45), "conch"), (B.ls(tl, "u031"), "hit"), (B.ls(tl, "u062"), "shimmer"),
            (B.ls(tl, "u073"), "damaru"), (B.ls(tl, "u082"), "hit"), (B.ls(tl, "u089"), "bell"),
            (B.ls(tl, "u093"), "shimmer"), (B.ls(tl, "u106"), "conch"), (B.ls(tl, "u111"), "bell"),
            (B.ls(tl, "u055"), "shimmer"), (B.ls(tl, "u041"), "bell")]
    kept = []
    for a, n in want:
        if n in SFX_KEEP and all(abs(a - k[0]) >= SFX_MIN_GAP for k in kept):
            kept.append((a, n, 0))
    kept = [(after_voice(tl, a), n, d) for a, n, d in kept]
    dips = [(B.ls(tl, x) - 0.3, "dip", 0.45) for x in ("u031", "u062", "u073", "u089", "u106")]
    return [(round(max(0.0, a), 3), n, d) for a, n, d in sorted(kept + dips)]
