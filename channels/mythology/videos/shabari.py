"""Mythology video 20: Shabari's tasted berries are in neither Valmiki's Ramayana nor Tulsidas's Ramcharitmanas (the
owner's "Continue" after videos 15-19, 12 Nov 2026). A myth-bust like Lakshman Rekha (27K views): one famous picture,
"it's not in the book", what the books really say, and the little-known real wonder of Shabari's hermitage. Respectful
to the belief: Rama's love for her is real in both books. Look: Hindi = Togalu Gombeyaata shadow puppets, Kannada =
Yakshagana stage. Her end is a soft light rising to the sky (no fire shown). Calm sound.

Facts:
- Valmiki Ramayana, Aranya Kanda 74 (Desiraju Hanumanta Rao translation): Shabari, an ascetic woman who served the
  sages of Matanga's woodland, touches the brothers' feet and gives water (6-7); her teachers told her Rama would
  come, and after seeing him she would go to the imperishable worlds (12-16); "I have gathered various forest fruits
  and eatables from the moorlands of Pampa" for you (17), no tasting; she shows the altar where the old sages offered
  flowers "with their doddery hands" (23); the bark cloths they spread on the trees after bathing "have not dried
  even now" (26); the garlands of lotuses are still fresh, "no discolouration" (27); with Rama's leave she gives up
  her body and goes to the place of her teachers (28-35).
- Ramcharitmanas, Aranya Kand, doha 34: "kand mool phal surasa ati diye Ram kahun aani; prem sahit prabhu khaaye
  baarambaar bakhaani" (she brought very sweet roots and fruits; the Lord ate them with love, praising them again
  and again). No tasting.
- The tasted-berries detail comes from later retellings and bhajans (the valmikiramayan.net commentary credits the
  Padma Purana); the reel only says "later stories and bhajans".
"""
from channel import ASSETS_ROOT, MUSIC, NARRATORS, NARRATOR_LABEL, REVEAL_GAP, TAIL  # noqa: F401

G = REVEAL_GAP
SCRIPTS = {
    "hi": [
        dict(id="sb1", text="सोचो, शबरी के जूठे बेर, जिन्हें राम जी ने प्यार से खाया... वो कहानी, वाल्मीकि रामायण में है ही नहीं!", gap=G),
        dict(id="sb2", text="ना वाल्मीकि रामायण में, और ना तुलसीदास जी की रामचरितमानस में।"),
        dict(id="sb3", text="शबरी, जंगल में रहने वाली एक भोली औरत थीं। वो कुछ बूढ़े ऋषियों की सेवा करती थीं।"),
        dict(id="sb4", text="ऋषियों ने उनसे कहा: एक दिन, राम जी यहाँ आएँगे। तुम उनका इंतज़ार करना।", gap=G),
        dict(id="sb5", text="फिर ऋषि, स्वर्ग चले गए। और शबरी, अकेली रह गईं।"),
        dict(id="sb6", text="सालों तक, शबरी रोज़ रास्ता देखतीं। और राम जी के लिए, जंगल से फल लाकर रखतीं।", gap=G),
        dict(id="sb7", text="फिर एक दिन, सीता माता को ढूँढते ढूँढते, राम जी सच में वहाँ आ गए!"),
        dict(id="sb8", text="शबरी ने उनके पैर छुए, पानी दिया, और अपने इकट्ठा किए हुए फल दिए।", gap=G),
        dict(id="sb8q", text="पर क्या शबरी ने, बेर चख चखकर दिए थे?"),
        dict(id="sb9", text="वाल्मीकि रामायण में बस इतना है: शबरी ने जंगल के, तरह तरह के फल इकट्ठा किए थे। चखने की कोई बात नहीं।"),
        dict(id="sb10", text="तुलसीदास जी लिखते हैं: राम जी ने वो मीठे फल, प्यार से, तारीफ़ करते करते खाए। पर चखने की बात, यहाँ भी नहीं।", gap=G),
        dict(id="sb11", text="जूठे बेर की बात, बहुत बाद में, दूसरी कहानियों और भजनों में आई।"),
        dict(id="sb12", text="पर वाल्मीकि रामायण में, शबरी की कहानी में, एक असली चमत्कार है।", gap=G),
        dict(id="sb13", text="ऋषियों को गए हुए, सालों बीत गए थे... पर उनके चढ़ाए फूल, अब तक ताज़ा थे। मुरझाए ही नहीं!"),
        dict(id="sb14", text="और नहाकर, पेड़ों पर सुखाए उनके कपड़े, अब तक गीले थे!", gap=G),
        dict(id="sb15", text="राम जी से मिलकर, शबरी का इंतज़ार पूरा हुआ। और वो अपने गुरुओं के पास, स्वर्ग चली गईं।"),
        dict(id="sb15c", text="बेर जूठे थे या नहीं... पर शबरी का इंतज़ार, दोनों रामायणों में सच्चा है।", gap=G),
        dict(id="sb16", text="तो तुम कौन सी कहानी मानते हो: जूठे बेर वाली, या वाल्मीकि वाली? कमेंट में बताओ।"),
    ],
}
KN = {
    "sb1": "ಯೋಚಿಸಿ... ಶಬರಿ ರುಚಿ ನೋಡಿ ಕೊಟ್ಟ ಎಂಜಲು ಹಣ್ಣು, ರಾಮ ಪ್ರೀತಿಯಿಂದ ತಿಂದ ಆ ಕಥೆ... ವಾಲ್ಮೀಕಿ ರಾಮಾಯಣದಲ್ಲಿ ಇಲ್ಲವೇ ಇಲ್ಲ!",
    "sb2": "ವಾಲ್ಮೀಕಿ ರಾಮಾಯಣದಲ್ಲೂ ಇಲ್ಲ, ತುಳಸೀದಾಸರ ರಾಮಚರಿತಮಾನಸದಲ್ಲೂ ಇಲ್ಲ.",
    "sb3": "ಶಬರಿ, ಕಾಡಲ್ಲಿ ಇರ್ತಿದ್ದ ಒಬ್ಬ ಮುಗ್ಧ ಹೆಂಗಸು. ಕೆಲವು ವಯಸ್ಸಾದ ಋಷಿಗಳ ಸೇವೆ ಮಾಡ್ತಿದ್ಲು.",
    "sb4": "ಋಷಿಗಳು ಅವಳಿಗೆ ಹೇಳಿದ್ರು: ಒಂದು ದಿನ, ರಾಮ ಇಲ್ಲಿಗೆ ಬರ್ತಾನೆ. ನೀನು ಅವನಿಗಾಗಿ ಕಾಯ್ತಿರು.",
    "sb5": "ಆಮೇಲೆ ಋಷಿಗಳು ಸ್ವರ್ಗಕ್ಕೆ ಹೋದ್ರು. ಶಬರಿ, ಒಬ್ಬಳೇ ಉಳಿದ್ಲು.",
    "sb6": "ಎಷ್ಟೋ ವರ್ಷ, ಶಬರಿ ದಿನಾ ದಾರಿ ನೋಡ್ತಿದ್ಲು. ರಾಮನಿಗಾಗಿ, ಕಾಡಿಂದ ಹಣ್ಣು ತಂದು ಇಡ್ತಿದ್ಲು.",
    "sb7": "ಆಮೇಲೆ ಒಂದು ದಿನ, ಸೀತೆಯನ್ನ ಹುಡುಕ್ತಾ ಹುಡುಕ್ತಾ, ರಾಮ ನಿಜವಾಗಲೂ ಅಲ್ಲಿಗೆ ಬಂದ!",
    "sb8": "ಶಬರಿ ಅವನ ಕಾಲು ಮುಟ್ಟಿ ನಮಸ್ಕಾರ ಮಾಡಿದ್ಲು, ನೀರು ಕೊಟ್ಲು, ತಾನು ಕೂಡಿಸಿಟ್ಟ ಹಣ್ಣುಗಳನ್ನ ಕೊಟ್ಲು.",
    "sb8q": "ಆದ್ರೆ, ಶಬರಿ ಹಣ್ಣನ್ನ, ರುಚಿ ನೋಡಿ ನೋಡಿ ಕೊಟ್ಲಾ?",
    "sb9": "ವಾಲ್ಮೀಕಿ ರಾಮಾಯಣದಲ್ಲಿ ಇಷ್ಟೇ ಇದೆ: ಶಬರಿ, ಕಾಡಿನ ಬೇರೆ ಬೇರೆ ಹಣ್ಣುಗಳನ್ನ ಕೂಡಿಸಿಟ್ಟಿದ್ಲು. ರುಚಿ ನೋಡಿದ ಮಾತೇ ಇಲ್ಲ.",
    "sb10": "ತುಳಸೀದಾಸರು ಬರೀತಾರೆ: ರಾಮ ಆ ಸಿಹಿ ಹಣ್ಣುಗಳನ್ನ, ಪ್ರೀತಿಯಿಂದ, ಹೊಗಳ್ತಾ ಹೊಗಳ್ತಾ ತಿಂದ. ಆದ್ರೆ ರುಚಿ ನೋಡಿದ ಮಾತು, ಇಲ್ಲೂ ಇಲ್ಲ.",
    "sb11": "ಎಂಜಲು ಹಣ್ಣಿನ ಮಾತು, ತುಂಬಾ ಆಮೇಲೆ, ಬೇರೆ ಕಥೆಗಳಲ್ಲಿ ಮತ್ತು ಭಜನೆಗಳಲ್ಲಿ ಬಂತು.",
    "sb12": "ಆದ್ರೆ ವಾಲ್ಮೀಕಿ ರಾಮಾಯಣದಲ್ಲಿ, ಶಬರಿಯ ಕಥೆಯಲ್ಲಿ, ಒಂದು ನಿಜವಾದ ಅದ್ಭುತ ಇದೆ.",
    "sb13": "ಋಷಿಗಳು ಹೋಗಿ, ಎಷ್ಟೋ ವರ್ಷ ಆಗಿತ್ತು... ಆದ್ರೆ ಅವರು ಇಟ್ಟ ಹೂವು, ಇನ್ನೂ ತಾಜಾ ಆಗಿತ್ತು. ಬಾಡೇ ಇರಲಿಲ್ಲ!",
    "sb14": "ಸ್ನಾನ ಮಾಡಿ, ಮರದ ಮೇಲೆ ಒಣಗೋಕೆ ಹಾಕಿದ್ದ ಅವರ ಬಟ್ಟೆ, ಇನ್ನೂ ಒದ್ದೆ ಆಗೇ ಇತ್ತು!",
    "sb15": "ರಾಮನನ್ನ ನೋಡಿದ ಮೇಲೆ, ಶಬರಿ ಕಾದಿದ್ದು ಸಾರ್ಥಕ ಆಯ್ತು. ಅವಳು ತನ್ನ ಗುರುಗಳ ಹತ್ರ, ಸ್ವರ್ಗಕ್ಕೆ ಹೋದ್ಲು.",
    "sb15c": "ಹಣ್ಣು ಎಂಜಲೋ ಅಲ್ವೋ... ಆದ್ರೆ ಶಬರಿ ಕಾದಿದ್ದು, ಎರಡೂ ರಾಮಾಯಣಗಳಲ್ಲಿ ನಿಜ.",
    "sb16": "ಹಾಗಾದ್ರೆ ನೀವು ಯಾವ ಕಥೆ ನಂಬ್ತೀರ: ಎಂಜಲು ಹಣ್ಣಿನ ಕಥೆನಾ, ಅಥವಾ ವಾಲ್ಮೀಕಿಯ ಕಥೆನಾ? ಕಾಮೆಂಟ್ ಮಾಡಿ ಹೇಳಿ.",
}
SCRIPTS["kn"] = [dict(line, text=KN[line["id"]]) for line in SCRIPTS["hi"]]   # same ids and pauses as Hindi

_SOURCES = ["Valmiki Ramayana, Aranya Kanda 74", "Ramcharitmanas (Tulsidas), Aranya Kand, doha 34"]
METADATA = {
    "hi": dict(
        title="Shabari ke jhoothe ber Ramayan mein hain hi nahi",
        caption="Socho, Shabari ke jhoothe ber wali kahani... na Valmiki Ramayan mein hai, na Ramcharitmanas mein 😳\n\n"
                "Valmiki likhte hain: Shabari ne Ram ji ke liye jungle ke phal ikatthe kiye the. Tulsidas ji likhte "
                "hain: Ram ji ne woh meethe phal pyaar se, taareef karte hue khaaye. Chakhne ki baat dono mein nahi. "
                "Par Valmiki mein ek asli chamatkar hai: rishiyon ke chadhaaye phool saalon baad bhi taaze the...\n\n"
                "Tum kaunsi kahani maante ho? Comment mein batao 👇",
        yt_title="Shabari Ke Jhoothe Ber Ramayan Mein Hain Hi Nahi 😳 | Valmiki vs Ramcharitmanas",
        yt_description="Shabari ke jhoothe ber ki kahani sab jaante hain. Par Valmiki Ramayan (Aranya Kand 74) mein "
                       "Shabari bas jungle ke phal ikatthe karke deti hain, aur Tulsidas ji ki Ramcharitmanas mein Ram "
                       "ji woh phal pyaar se, taareef karte hue khaate hain. Chakhne ki baat baad ki kahaniyon aur "
                       "bhajanon mein aayi. Valmiki mein asli chamatkar kuch aur hai: rishiyon ko gaye saal beet gaye, "
                       "par unke chadhaaye phool aaj bhi taaze the aur unke kapde abhi tak geele the.",
        hashtags=["#shabari", "#ramayan", "#mythology", "#kahani", "#hindu"],
        pinned_comment="Tum kaunsi kahani maante ho: jhoothe ber wali, ya Valmiki wali? 👇",
        sources=_SOURCES),
    "kn": dict(
        title="Shabari enjalu hannu Ramayanadalle illa",
        caption="Yochisi: Shabari ruchi nodi kotta enjalu hannina kathe... Valmiki Ramayanadallu illa, "
                "Ramacharitamanasadallu illa 😳\n\nValmiki bareetaare: Shabari Ramanigaagi kaadina hannu koodisittidlu. "
                "Tulasidasaru bareetaare: Rama aa hannu preetiyinda hogalta hogalta tinda. Ruchi nodida maatu "
                "eraradallu illa. Aadre Valmikiyalli ondu nijavaada adbhuta ide...\n\n"
                "Neevu yaava kathe nambteera? Comment maadi 👇",
        yt_title="Shabari Enjalu Hannu Ramayanadalle Illa 😳 | Valmiki Ramayana",
        yt_description="Shabari ruchi nodi kotta enjalu hannina kathe ellarigu gottu. Aadre Valmiki Ramayana (Aranya "
                       "Kanda 74) dalli Shabari kaadina hannu koodisittu kodtaale, Tulasidasara Ramacharitamanasadalli "
                       "Rama aa hannu preetiyinda tintaane. Ruchi nodida maatu aamele bandiddu. Valmikiyalli nijavaada "
                       "adbhuta bere: rishigalu hogi eshto varsha aagittu, aadre avaru itta hoovu innu taaja aagittu, "
                       "avara batte innu odde aagittu.",
        hashtags=["#kannada", "#shabari", "#ramayana", "#kannadastory", "#mythology"],
        pinned_comment="Neevu yaava kathe nambteera: enjalu hannu kathe na, Valmiki kathe na? 👇",
        sources=_SOURCES),
}


USED_ASSETS, CREDITS_FILES = [], []      # everything in this video is drawn in code


def _scenes(tl):
    """Hindi: shadow puppets (scenes_shabari); Kannada: Yakshagana stage (scenes_shabari_yk), so the two channels never
    share pictures."""
    import importlib
    yk = getattr(tl, "lang", "hi") == "kn"
    return importlib.import_module("scenes_shabari_yk" if yk else "scenes_shabari")


def draw(cr, t, tl):
    _scenes(tl).draw(cr, t, tl)


def sfx(tl):
    return _scenes(tl).sfx(tl)
