"""Mythology video 15: Hanuman forgot his own powers because sages cursed him as a child (owner, 11 Nov 2026: "Make
next 5 shorts all on good topics"). Impossible-sounding hook, a famous god, a twist (Jambavan's reminder) and a fair
debate (who is the real hero?). Look: Togalu Gombeyaata shadow puppets; Indra's thunderbolt is a flash, no injury
shown beyond a fall. Calm sound.

Facts (Valmiki Ramayana, Uttara Kanda 35-36, H. P. Shastri translation; Kishkindha Kanda 66-67):
- 35: the infant took the rising sun for a fruit and sprang at it; Indra struck him with the thunderbolt, he fell on
  a mountain and broke his jaw; Vayu withdrew into a cave and all beings suffered.
- 36: the gods' boons (Indra: the thunderbolt will not harm him, hence the name Hanuman from hanu, the jaw; Brahma:
  invincible, able to take any form at will, etc.). In the sages' hermitages he scattered "the spoons, jars,
  sacrificial fires, and heaps of bark"; the sages cursed him so that his knowledge of his powers was taken away;
  "when it is remembered by you, you shalt be able to wield it effectively".
- Kishkindha 64-67: no monkey can leap the hundred-yojana sea; Hanuman sits apart in silence; Jambavan recounts his
  birth from Vayu and his childhood leap at the sun; Hanuman swells to a huge size and leaps.
"""
# Rewritten 12 Nov 2026 to 5-year-old level (owner: "I want story so clear and very good explained even a 5 year old can understand"): short sentences, everyday words, hard words explained.
from channel import ASSETS_ROOT, MUSIC, NARRATORS, NARRATOR_LABEL, REVEAL_GAP, TAIL  # noqa: F401

G = REVEAL_GAP
SCRIPTS = {
    "hi": [
        dict(id="h1", text="सोचो, हनुमान जी इतने ताक़तवर थे... पर ये बात, उन्हें ख़ुद ही याद नहीं थी!", gap=G),
        dict(id="h2", text="ये रामायण की सच्ची कहानी है।"),
        dict(id="h3", text="जब हनुमान जी छोटे बच्चे थे, उन्होंने आसमान में लाल लाल सूरज देखा।"),
        dict(id="h4", text="उन्हें लगा, ये तो कोई मीठा लाल फल है! और वो उसे खाने के लिए, आसमान में उड़ गए।", gap=G),
        dict(id="h5", text="देवताओं के राजा इंद्र ने, उन्हें रोकने के लिए अपना हथियार फेंका। वो हनुमान जी की ठुड्डी पर लगा।"),
        dict(id="h6", text="ठुड्डी को हनु कहते हैं। इसीलिए उनका नाम पड़ा: हनुमान।"),
        dict(id="h7", text="फिर सारे देवताओं ने, उन्हें बहुत सारी शक्तियाँ दीं। अब कोई उन्हें हरा नहीं सकता था।", gap=G),
        dict(id="h8", text="पर बच्चे तो शरारती होते हैं! हनुमान जी ऋषियों की कुटिया में जाकर, उनका सामान फेंकने लगे।"),
        dict(id="h9", text="ऋषियों को ग़ुस्सा आया। उन्होंने कहा: जाओ, तुम अपनी सारी ताक़त भूल जाओगे।", gap=G),
        dict(id="h10", text="और हनुमान जी सच में सब भूल गए। सालों तक, बाकी वानरों की तरह, साधारण बनकर रहे।"),
        dict(id="h11", text="फिर एक दिन, सीता माता को ढूँढने के लिए, एक बहुत बड़ा समुद्र पार करना था।"),
        dict(id="h12", text="कोई भी उतनी दूर कूद नहीं सकता था। सब उदास बैठे थे।", gap=G),
        dict(id="h12q", text="तो अब क्या? हनुमान जी को अपनी ताक़त, याद कैसे आएगी?"),
        dict(id="h13", text="तब भालुओं के बूढ़े राजा जामवंत, हनुमान जी के पास आए। बोले: तुम तो बचपन में, सूरज तक उड़ गए थे!"),
        dict(id="h14", text="ये सुनते ही, हनुमान जी को सब याद आ गया। और वो पहाड़ जितने बड़े हो गए।", gap=G),
        dict(id="h15", text="फिर एक ही छलांग में, उन्होंने पूरा समुद्र पार कर दिया।"),
        dict(id="h15c", text="जो बचपन में सूरज तक उड़ गया था... उसके लिए समुद्र, बस एक छलांग था।", gap=G),
        dict(id="h16", text="तो असली हीरो कौन: छलांग लगाने वाले हनुमान जी, या याद दिलाने वाले जामवंत? कमेंट में बताओ।"),
    ],
}
KN = {
    "h1": "ಯೋಚಿಸಿ... ಹನುಮಂತ ಅಷ್ಟು ಶಕ್ತಿಶಾಲಿ... ಆದ್ರೆ ಆ ವಿಷಯ, ಅವನಿಗೇ ನೆನಪಿರಲಿಲ್ಲ!",
    "h2": "ಇದು ರಾಮಾಯಣದ ನಿಜವಾದ ಕಥೆ.",
    "h3": "ಹನುಮಂತ ಚಿಕ್ಕ ಮಗುವಾಗಿದ್ದಾಗ, ಆಕಾಶದಲ್ಲಿ ಕೆಂಪು ಕೆಂಪು ಸೂರ್ಯನನ್ನ ನೋಡಿದ.",
    "h4": "ಅವನಿಗೆ ಅನ್ನಿಸ್ತು, ಇದು ಯಾವುದೋ ಸಿಹಿಯಾದ ಕೆಂಪು ಹಣ್ಣು! ಅದನ್ನ ತಿನ್ನೋಕೆ, ಆಕಾಶಕ್ಕೆ ಹಾರಿದ.",
    "h5": "ದೇವತೆಗಳ ರಾಜ ಇಂದ್ರ, ಅವನನ್ನ ತಡೆಯೋಕೆ ತನ್ನ ಆಯುಧ ಎಸೆದ. ಅದು ಹನುಮಂತನ ದವಡೆಗೆ ಬಡೀತು.",
    "h6": "ದವಡೆಗೆ ಹನು ಅಂತಾರೆ. ಅದಕ್ಕೇ ಅವನ ಹೆಸರು: ಹನುಮಂತ.",
    "h7": "ಆಮೇಲೆ ಎಲ್ಲ ದೇವತೆಗಳು, ಅವನಿಗೆ ತುಂಬಾ ಶಕ್ತಿಗಳನ್ನ ಕೊಟ್ರು. ಈಗ ಯಾರೂ ಅವನನ್ನ ಸೋಲಿಸೋಕಾಗಲ್ಲ.",
    "h8": "ಆದ್ರೆ ಮಕ್ಕಳು ತುಂಟರು ಅಲ್ವಾ! ಹನುಮಂತ ಋಷಿಗಳ ಗುಡಿಸಲಿಗೆ ಹೋಗಿ, ಅವರ ಸಾಮಾನು ಎಸೆಯೋಕೆ ಶುರು ಮಾಡಿದ.",
    "h9": "ಋಷಿಗಳಿಗೆ ಕೋಪ ಬಂತು. ಹೇಳಿದ್ರು: ಹೋಗು, ನೀನು ನಿನ್ನ ಶಕ್ತಿನೆಲ್ಲ ಮರೆತುಬಿಡ್ತೀಯ.",
    "h10": "ಹನುಮಂತ ನಿಜವಾಗಲೂ ಎಲ್ಲ ಮರೆತುಬಿಟ್ಟ. ಎಷ್ಟೋ ವರ್ಷ, ಬೇರೆ ವಾನರರ ಹಾಗೆ ಸಾಮಾನ್ಯವಾಗಿ ಇದ್ದ.",
    "h11": "ಆಮೇಲೆ ಒಂದು ದಿನ, ಸೀತಾ ಮಾತೆಯನ್ನ ಹುಡುಕೋಕೆ, ಒಂದು ದೊಡ್ಡ ಸಮುದ್ರ ದಾಟಬೇಕಿತ್ತು.",
    "h12": "ಯಾರಿಗೂ ಅಷ್ಟು ದೂರ ಹಾರೋಕಾಗ್ತಿರಲಿಲ್ಲ. ಎಲ್ಲರೂ ಬೇಜಾರಾಗಿ ಕೂತಿದ್ರು.",
    "h12q": "ಈಗ ಏನು? ಹನುಮಂತನಿಗೆ ತನ್ನ ಶಕ್ತಿ, ಹೇಗೆ ನೆನಪಾಗುತ್ತೆ?",
    "h13": "ಆಗ ಕರಡಿಗಳ ಹಿರಿಯ ರಾಜ ಜಾಂಬವಂತ, ಹನುಮಂತನ ಹತ್ರ ಬಂದು ಹೇಳಿದ: ನೀನು ಚಿಕ್ಕವನಿದ್ದಾಗ, ಸೂರ್ಯನವರೆಗೂ ಹಾರಿದ್ದೆ!",
    "h14": "ಇದನ್ನ ಕೇಳಿದ ತಕ್ಷಣ, ಹನುಮಂತನಿಗೆ ಎಲ್ಲ ನೆನಪಾಯ್ತು. ಅವನು ಬೆಟ್ಟದಷ್ಟು ದೊಡ್ಡವನಾದ.",
    "h15": "ಆಮೇಲೆ ಒಂದೇ ಜಿಗಿತದಲ್ಲಿ, ಇಡೀ ಸಮುದ್ರ ದಾಟಿಬಿಟ್ಟ.",
    "h15c": "ಚಿಕ್ಕವನಿದ್ದಾಗ ಸೂರ್ಯನವರೆಗೂ ಹಾರಿದವನಿಗೆ... ಸಮುದ್ರ ಅಂದ್ರೆ, ಒಂದು ಜಿಗಿತ ಅಷ್ಟೇ.",
    "h16": "ಹಾಗಾದ್ರೆ ನಿಜವಾದ ಹೀರೋ ಯಾರು: ಜಿಗಿದ ಹನುಮಂತನಾ, ಅಥವಾ ನೆನಪಿಸಿದ ಜಾಂಬವಂತನಾ? ಕಾಮೆಂಟ್ ಮಾಡಿ ಹೇಳಿ.",
}
SCRIPTS["kn"] = [dict(line, text=KN[line["id"]]) for line in SCRIPTS["hi"]]   # same ids and pauses as Hindi

_SOURCES = ["Valmiki Ramayana, Uttara Kanda 35-36 (H. P. Shastri translation)", "Valmiki Ramayana, Kishkindha Kanda 66-67"]
METADATA = {
    "hi": dict(
        title="Hanuman ji apni shakti bhool gaye the",
        caption="Socho, Hanuman ji ko apni hi shaktiyan yaad nahi thi... kyunki bachpan mein rishiyon ne unhe shraap diya "
                "tha 😳\n\nValmiki Ramayan, Uttar Kand: suraj ko phal samajhkar chhalaang, Indra ka vajra, rishiyon ka "
                "shraap. Phir samudra ke kinare Jamvant ne yaad dilaya...\n\n"
                "Asli hero kaun: Hanuman ji ya Jamvant? Comment mein batao 👇",
        yt_title="Hanuman Ji Apni Shakti Bhool Gaye The 😳 | Rishiyon Ka Shraap | Valmiki Ramayan",
        yt_description="Bachpan mein Hanuman ji ne suraj ko laal phal samajhkar pakadne ki chhalaang lagayi, Indra ka "
                       "vajra unki thuddi (hanu) par laga. Devtaon ne vardaan diye, par rishiyon ke aashram mein "
                       "shararat karne par rishiyon ne shraap diya ki woh apni shakti bhool jaayenge. Saalon baad "
                       "samudra ke kinare Jamvant ne unhe unki kahani yaad dilayi, aur Hanuman ji pahaad jitne bade "
                       "ho gaye.",
        hashtags=["#hanuman", "#ramayan", "#mythology", "#kahani", "#hindu"],
        pinned_comment="Asli hero kaun tha: chhalaang lagaane wale Hanuman ji, ya yaad dilaane wale Jamvant? 👇",
        sources=_SOURCES),
    "kn": dict(
        title="Hanumantha tanna shakti marethidda",
        caption="Yochisi: Hanumantanige tanna shaktiye nenapirlilla... yaakandre chikkavaniddaaga rishigalu avanige "
                "shaapa kottidru 😳\n\nValmiki Ramayana, Uttara Kanda: sooryanannu hannu andkondu jigita, Indrana "
                "vajra, rishigala shaapa. Aamele samudrada dadadalli Jambavanta nenapisida...\n\n"
                "Nijavaada hero yaaru: Hanumantha na, Jambavanta na? Comment maadi 👇",
        yt_title="Hanumantha Tanna Shakti Marethidda 😳 | Rishigala Shaapa | Valmiki Ramayana",
        yt_description="Chikkavaniddaaga Hanumantha sooryanannu kempu hannu andkondu hidiyoke haarida, Indrana vajra "
                       "avana davadege (hanu) badeetu. Devategalu vara kottru, aadre rishigala aashramadalli "
                       "tuntaata maadidakke rishigalu shaapa kottru, avanu tanna shakti marethubidtaane anta. "
                       "Varshagala nantara samudrada dadadalli Jambavanta avanige avanade kathe nenapisida, Hanumantha "
                       "bettadashtu doddavanaada.",
        hashtags=["#kannada", "#hanuman", "#ramayana", "#kannadastory", "#mythology"],
        pinned_comment="Nijavaada hero yaaru: jigida Hanumantha na, nenapisida Jambavanta na? 👇",
        sources=_SOURCES),
}


USED_ASSETS, CREDITS_FILES = [], []      # everything in this video is drawn in code


def _scenes(tl):
    """Hindi: shadow puppets (scenes_hanuman_curse); Kannada: Yakshagana stage (scenes_hanuman_curse_yk), so the two channels never share
    pictures."""
    import importlib
    yk = getattr(tl, "lang", "hi") == "kn"
    return importlib.import_module("scenes_hanuman_curse_yk" if yk else "scenes_hanuman_curse")


def draw(cr, t, tl):
    _scenes(tl).draw(cr, t, tl)


def sfx(tl):
    return _scenes(tl).sfx(tl)
