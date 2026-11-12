"""Mythology video 17: Kumbhakarna never asked for sleep; Saraswati sat on his tongue (owner, 11 Nov 2026: "Make next
5 shorts all on good topics"). A myth-bust inside (the "Indrasana/Nidrasana" pun is not Valmiki's) and a twist:
Valmiki gives two different reasons for his sleep, a boon and a curse. Debate: boon or curse? Look: Togalu
Gombeyaata shadow puppets; Kumbhakarna's eating is implied (a huge mouth, a shadow), never shown. Calm sound.

Facts (Valmiki Ramayana, H. P. Shastri translation):
- Uttara Kanda 10: the three brothers' austerities; the gods to Brahma: "As for Kumbhakarna, do not grant him any
  boons! You knowest well how the Three Worlds fear this perverse wretch!" (he had devoured Apsaras and servants of
  Indra); Brahma to Sarasvati: "be you in the mouth of that Indra among the Rakshasas and utter that which the Gods
  desire"; Kumbhakarna: "To sleep for innumerable years, O Lord of Lords, this is my desire!"; afterwards: "How can
  such words have passed my lips? I must have been bemused by the Gods who came hither."
- Yuddha Kanda 61: Vibhishana tells Rama that Kumbhakarna devoured creatures from birth; Brahma cursed him to sleep
  like the dead; at Ravana's plea, he would sleep six months and wake for one day.
- The popular Indrasana/Nidrasana wordplay is a later retelling, not in Valmiki.
"""
# (earlier) Rewritten 12 Nov 2026 for kid-level clarity (owner: "the hook needs to be strong and story clear so even a kid can understand"): max 3 names, one storyline, a concrete hook.
# Rewritten 12 Nov 2026 to 5-year-old level (owner: "I want story so clear and very good explained even a 5 year old can understand"): short sentences, everyday words, hard words explained.
from channel import ASSETS_ROOT, MUSIC, NARRATORS, NARRATOR_LABEL, REVEAL_GAP, TAIL  # noqa: F401

G = REVEAL_GAP
SCRIPTS = {
    "hi": [
        dict(id="k1", text="सोचो, कुंभकर्ण ने सोने का वरदान माँगा ही नहीं था... उसकी ज़ुबान पर, देवी सरस्वती बैठ गई थीं!", gap=G),
        dict(id="k2", text="ये रामायण की सच्ची कहानी है।"),
        dict(id="k3", text="कुंभकर्ण, रावण का भाई था। एक बहुत बड़ा राक्षस, जो कुछ भी खा जाता था।"),
        dict(id="k4", text="उसने भगवान ब्रह्मा की पूजा की। ब्रह्मा जी ख़ुश हुए, और बोले: माँगो, तुम्हें क्या चाहिए।", gap=G),
        dict(id="k5", text="पर बाकी देवता डर गए। बोले: इसे ताक़त मिली, तो ये पूरी दुनिया खा जाएगा!"),
        dict(id="k5q", text="पर ब्रह्मा जी तो वचन दे चुके थे। तो अब क्या करें?"),
        dict(id="k6", text="तब ब्रह्मा जी ने, बोलने की देवी सरस्वती से कहा: जाइए, उसकी ज़ुबान पर बैठ जाइए।"),
        dict(id="k7", text="सरस्वती छोटी सी बनकर, कुंभकर्ण की ज़ुबान पर बैठ गईं।", gap=G),
        dict(id="k8", text="ब्रह्मा जी ने पूछा: क्या चाहिए? और उसके मुँह से निकला: मुझे बहुत सालों तक सोना है!", gap=G),
        dict(id="k9", text="ब्रह्मा जी बोले: ठीक है, ऐसा ही होगा।"),
        dict(id="k10", text="सरस्वती बाहर निकलीं, तो कुंभकर्ण को होश आया: अरे! मैंने ये क्या माँग लिया?", gap=G),
        dict(id="k11", text="उसकी अपनी ज़ुबान ने ही, उसे धोखा दे दिया था।"),
        dict(id="k12", text="और इसीलिए, जब राम और रावण की लड़ाई शुरू हुई, कुंभकर्ण सो रहा था।"),
        dict(id="k13", text="उसे जगाने के लिए ढोल बजाए गए, और उसके ऊपर हाथी तक चलाए गए!", gap=G),
        dict(id="k13c", text="जो पूरी दुनिया खा सकता था... उसे उसकी अपनी ज़ुबान ने, सुला दिया।", gap=G),
        dict(id="k14", text="तो क्या देवताओं ने कुंभकर्ण के साथ धोखा किया? हाँ या ना, कमेंट में बताओ।"),
    ],
}
KN = {
    "k1": "ಯೋಚಿಸಿ... ಕುಂಭಕರ್ಣ ನಿದ್ದೆಯ ವರ ಕೇಳಲೇ ಇಲ್ಲ... ಅವನ ನಾಲಿಗೆ ಮೇಲೆ ಸರಸ್ವತಿ ದೇವಿ ಕೂತಿದ್ರು!",
    "k2": "ಇದು ರಾಮಾಯಣದ ನಿಜವಾದ ಕಥೆ.",
    "k3": "ಕುಂಭಕರ್ಣ ರಾವಣನ ತಮ್ಮ. ಒಬ್ಬ ದೊಡ್ಡ ರಾಕ್ಷಸ, ಏನು ಸಿಕ್ಕಿದ್ರೂ ತಿಂದುಬಿಡ್ತಿದ್ದ.",
    "k4": "ಅವನು ಬ್ರಹ್ಮನ ಪೂಜೆ ಮಾಡಿದ. ಬ್ರಹ್ಮ ಖುಷಿಯಾಗಿ ಹೇಳಿದ: ಕೇಳು, ನಿನಗೆ ಏನು ಬೇಕು.",
    "k5": "ಆದ್ರೆ ಬೇರೆ ದೇವತೆಗಳು ಹೆದರಿದ್ರು. ಹೇಳಿದ್ರು: ಇವನಿಗೆ ಶಕ್ತಿ ಸಿಕ್ಕಿದ್ರೆ, ಇಡೀ ಜಗತ್ತನ್ನೇ ತಿಂದುಬಿಡ್ತಾನೆ!",
    "k5q": "ಆದ್ರೆ ಬ್ರಹ್ಮ ಆಗಲೇ ಮಾತು ಕೊಟ್ಟಿದ್ದ. ಈಗ ಏನು ಮಾಡೋದು?",
    "k6": "ಆಗ ಬ್ರಹ್ಮ, ಮಾತಿನ ದೇವಿ ಸರಸ್ವತಿಗೆ ಹೇಳಿದ: ಹೋಗಿ, ಅವನ ನಾಲಿಗೆ ಮೇಲೆ ಕೂತ್ಕೊಳ್ಳಿ.",
    "k7": "ಸರಸ್ವತಿ ಚಿಕ್ಕದಾಗಿ, ಕುಂಭಕರ್ಣನ ನಾಲಿಗೆ ಮೇಲೆ ಕೂತ್ರು.",
    "k8": "ಬ್ರಹ್ಮ ಕೇಳಿದ: ಏನು ಬೇಕು? ಕುಂಭಕರ್ಣನ ಬಾಯಿಂದ ಬಂತು: ನನಗೆ ಎಷ್ಟೋ ವರ್ಷ ನಿದ್ದೆ ಮಾಡಬೇಕು!",
    "k9": "ಬ್ರಹ್ಮ ಹೇಳಿದ: ಸರಿ, ಹಾಗೇ ಆಗಲಿ.",
    "k10": "ಸರಸ್ವತಿ ಹೊರಗೆ ಬಂದ ಮೇಲೆ, ಕುಂಭಕರ್ಣನಿಗೆ ಪ್ರಜ್ಞೆ ಬಂತು: ಅಯ್ಯೋ! ನಾನು ಏನು ಕೇಳಿಬಿಟ್ಟೆ?",
    "k11": "ಅವನ ನಾಲಿಗೆಯೇ, ಅವನಿಗೆ ಮೋಸ ಮಾಡಿತ್ತು.",
    "k12": "ಅದಕ್ಕೇ, ರಾಮ ರಾವಣರ ಯುದ್ಧ ಶುರುವಾದಾಗ, ಕುಂಭಕರ್ಣ ನಿದ್ದೆಯಲ್ಲಿದ್ದ.",
    "k13": "ಅವನನ್ನ ಎಬ್ಬಿಸೋಕೆ ಡೋಲು ಬಾರಿಸಿದ್ರು, ಅವನ ಮೇಲೆ ಆನೆಗಳನ್ನೂ ನಡೆಸಿದ್ರು!",
    "k13c": "ಇಡೀ ಜಗತ್ತನ್ನೇ ತಿನ್ನಬಹುದಾಗಿದ್ದವನನ್ನ... ಅವನ ನಾಲಿಗೆಯೇ, ಮಲಗಿಸಿಬಿಟ್ಟಿತು.",
    "k14": "ಹಾಗಾದ್ರೆ ದೇವತೆಗಳು ಕುಂಭಕರ್ಣನಿಗೆ ಮೋಸ ಮಾಡಿದ್ರಾ? ಹೌದಾ ಇಲ್ವಾ, ಕಾಮೆಂಟ್ ಮಾಡಿ ಹೇಳಿ.",
}
SCRIPTS["kn"] = [dict(line, text=KN[line["id"]]) for line in SCRIPTS["hi"]]   # same ids and pauses as Hindi

_SOURCES = ["Valmiki Ramayana, Uttara Kanda 10 (H. P. Shastri translation)", "Valmiki Ramayana, Yuddha Kanda 61"]
METADATA = {
    "hi": dict(
        title="Kumbhakarna ne neend maangi hi nahi thi",
        caption="Socho, Kumbhakarna ne neend ka vardaan maanga hi nahi tha... uski zubaan par devi Saraswati baith gayi "
                "thi 😳\n\nValmiki Ramayan: devta dar gaye, Brahma ji ne Saraswati ko uske munh mein bheja. Aur "
                "'Indrasan-Nidrasan' wala shabdon ka khel Valmiki mein hai hi nahi.\n\n"
                "Kumbhakarna ki neend: vardaan ya shraap? Comment mein batao 👇",
        yt_title="Kumbhakarna Ne Neend Maangi Hi Nahi Thi 😳 | Saraswati Ka Khel | Valmiki Ramayan",
        yt_description="Valmiki Ramayan ke Uttar Kand mein devta Brahma ji se kehte hain ki Kumbhakarna ko vardaan mat "
                       "dijiye. Brahma ji Saraswati ko uske munh mein bhejte hain aur woh bol padta hai: mujhe bahut "
                       "saalon tak sona hai. Indrasan-Nidrasan ka shabdon ka khel Valmiki mein nahi hai, aur Yuddh Kand "
                       "mein neend ki ek doosri wajah bhi likhi hai: Brahma ji ka shraap, chhah mahine neend aur ek din "
                       "jaagna.",
        hashtags=["#kumbhakarna", "#ramayan", "#mythology", "#kahani", "#hindu"],
        pinned_comment="Kumbhakarna ki neend: vardaan thi ya shraap? 👇",
        sources=_SOURCES),
    "kn": dict(
        title="Kumbhakarna nidde kelale illa",
        caption="Yochisi: Kumbhakarna nidde vara kelale illa... avana naalige mele Saraswati devi kootidru 😳\n\n"
                "Valmiki Ramayana: devategalu hedaridru, Brahma Saraswatiyannu avana baayige kalisida. "
                "'Indrasana-Nidrasana' padada aata Valmikiyalli ilve illa.\n\n"
                "Kumbhakarnana nidde: vara na, shaapa na? Comment maadi 👇",
        yt_title="Kumbhakarna Nidde Kelale Illa 😳 | Saraswatiya Aata | Valmiki Ramayana",
        yt_description="Valmiki Ramayanada Uttara Kandadalli devategalu Brahmanige helutaare Kumbhakarnanige vara "
                       "kodabedi anta. Brahma Saraswatiyannu avana baayige kalisutaane, avanu heltaane: nanage eshto "
                       "varsha nidde maadbeku. Indrasana-Nidrasana padada aata Valmikiyalli illa, mattu Yuddha "
                       "Kandadalli niddege innondu kaarana ide: Brahmana shaapa, aaru tingalu nidde, ondu dina eccara.",
        hashtags=["#kannada", "#kumbhakarna", "#ramayana", "#kannadastory", "#mythology"],
        pinned_comment="Kumbhakarnana nidde: vara na, shaapa na? 👇",
        sources=_SOURCES),
}


USED_ASSETS, CREDITS_FILES = [], []      # everything in this video is drawn in code


def _scenes(tl):
    """Hindi: shadow puppets (scenes_kumbhakarna); Kannada: Yakshagana stage (scenes_kumbhakarna_yk), so the two channels never share
    pictures."""
    import importlib
    yk = getattr(tl, "lang", "hi") == "kn"
    return importlib.import_module("scenes_kumbhakarna_yk" if yk else "scenes_kumbhakarna")


def draw(cr, t, tl):
    _scenes(tl).draw(cr, t, tl)


def sfx(tl):
    return _scenes(tl).sfx(tl)
