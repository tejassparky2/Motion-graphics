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
from channel import ASSETS_ROOT, MUSIC, NARRATORS, NARRATOR_LABEL, REVEAL_GAP, TAIL  # noqa: F401

G = REVEAL_GAP
SCRIPTS = {
    "hi": [
        dict(id="k1", text="सोचो, कुंभकर्ण ने नींद का वरदान माँगा ही नहीं था... उसकी ज़ुबान पर, देवी सरस्वती बैठ गई थीं।",
             gap=G),
        dict(id="k2", text="ये कोई फ़िल्मी कहानी नहीं है। ये वाल्मीकि रामायण के उत्तर कांड में लिखा है।"),
        dict(id="k3", text="रावण, कुंभकर्ण और विभीषण, तीनों भाइयों ने, ब्रह्मा जी को खुश करने के लिए बहुत कठोर तप किया।"),
        dict(id="k4", text="ब्रह्मा जी वरदान देने आए। पर देवता डर गए।"),
        dict(id="k5", text="देवता बोले: कुंभकर्ण को वरदान मत दीजिए। ये पहले ही अप्सराओं और इंद्र के सेवकों को खा चुका है। "
                           "वरदान मिला, तो तीनों लोक खा जाएगा।", gap=G),
        dict(id="k6", text="तब ब्रह्मा जी ने देवी सरस्वती को याद किया। बोले: उस राक्षस के मुँह में जाइए, और वो बुलवाइए, "
                           "जो देवता चाहते हैं।"),
        dict(id="k7", text="सरस्वती, कुंभकर्ण की ज़ुबान पर बैठ गईं।", gap=G),
        dict(id="k8", text="ब्रह्मा जी ने पूछा: क्या चाहिए? और कुंभकर्ण के मुँह से निकला: मुझे बहुत सालों तक सोना है।",
             gap=G),
        dict(id="k9", text="ब्रह्मा जी बोले: तथास्तु। और चले गए।"),
        dict(id="k10", text="सरस्वती बाहर निकलीं, तो कुंभकर्ण को होश आया। बोला: ये शब्द मेरे मुँह से कैसे निकले? ज़रूर "
                            "देवताओं ने मुझे भरमा दिया।", gap=G),
        dict(id="k11", text="और एक बात लोग नहीं जानते। हम सुनते हैं, उसने इंद्रासन की जगह, गलती से निद्रासन बोल दिया। ये "
                            "शब्दों का खेल, वाल्मीकि रामायण में नहीं है।"),
        dict(id="k12", text="वाल्मीकि में ही, युद्ध कांड में, उसकी नींद की एक दूसरी वजह भी लिखी है।"),
        dict(id="k13", text="वहाँ विभीषण बताते हैं: कुंभकर्ण जीवों को खाने लगा, तो ब्रह्मा जी ने श्राप दिया: तू मुर्दे की "
                            "तरह सोता रहेगा।"),
        dict(id="k14", text="रावण ने गिड़गिड़ाकर विनती की। तब ब्रह्मा जी ने कहा: ये छह महीने सोएगा, और एक दिन जागेगा।",
             gap=G),
        dict(id="k15", text="यानी एक ही रामायण में, नींद की दो कहानियाँ: एक वरदान, और एक श्राप।"),
        dict(id="k16", text="आपको क्या लगता है: कुंभकर्ण की नींद, वरदान थी या श्राप? कमेंट में बताओ।"),
    ],
}
KN = {
    "k1": "ಯೋಚಿಸಿ... ಕುಂಭಕರ್ಣ ನಿದ್ದೆಯ ವರ ಕೇಳಲೇ ಇಲ್ಲ... ಅವನ ನಾಲಿಗೆ ಮೇಲೆ, ಸರಸ್ವತಿ ದೇವಿ ಕೂತಿದ್ರು.",
    "k2": "ಇದು ಸಿನಿಮಾ ಕಥೆ ಅಲ್ಲ. ವಾಲ್ಮೀಕಿ ರಾಮಾಯಣದ ಉತ್ತರ ಕಾಂಡದಲ್ಲೇ ಇದೆ.",
    "k3": "ರಾವಣ, ಕುಂಭಕರ್ಣ, ವಿಭೀಷಣ, ಮೂವರು ಅಣ್ಣತಮ್ಮಂದಿರು, ಬ್ರಹ್ಮನನ್ನ ಒಲಿಸೋಕೆ ತುಂಬಾ ಕಠಿಣ ತಪಸ್ಸು ಮಾಡಿದ್ರು.",
    "k4": "ಬ್ರಹ್ಮ ವರ ಕೊಡೋಕೆ ಬಂದ. ಆದ್ರೆ ದೇವತೆಗಳು ಹೆದರಿದ್ರು.",
    "k5": "ದೇವತೆಗಳು ಹೇಳಿದ್ರು: ಕುಂಭಕರ್ಣನಿಗೆ ವರ ಕೊಡಬೇಡಿ. ಇವನು ಆಗಲೇ ಅಪ್ಸರೆಯರನ್ನ, ಇಂದ್ರನ ಸೇವಕರನ್ನ ತಿಂದಿದ್ದಾನೆ. "
          "ವರ ಸಿಕ್ಕಿದ್ರೆ, ಮೂರು ಲೋಕನೂ ತಿಂದುಬಿಡ್ತಾನೆ.",
    "k6": "ಆಗ ಬ್ರಹ್ಮ ಸರಸ್ವತಿಯನ್ನ ನೆನೆದ. ಹೇಳಿದ: ಆ ರಾಕ್ಷಸನ ಬಾಯಲ್ಲಿ ಹೋಗಿ, ದೇವತೆಗಳಿಗೆ ಬೇಕಾದ ಮಾತು ಹೇಳಿಸು.",
    "k7": "ಸರಸ್ವತಿ, ಕುಂಭಕರ್ಣನ ನಾಲಿಗೆ ಮೇಲೆ ಕೂತ್ರು.",
    "k8": "ಬ್ರಹ್ಮ ಕೇಳಿದ: ಏನು ಬೇಕು? ಕುಂಭಕರ್ಣನ ಬಾಯಿಂದ ಬಂತು: ನನಗೆ ಎಷ್ಟೋ ವರ್ಷ ನಿದ್ದೆ ಮಾಡಬೇಕು.",
    "k9": "ಬ್ರಹ್ಮ ಹೇಳಿದ: ತಥಾಸ್ತು. ಮತ್ತು ಹೊರಟುಹೋದ.",
    "k10": "ಸರಸ್ವತಿ ಹೊರಗೆ ಬಂದ ಮೇಲೆ, ಕುಂಭಕರ್ಣನಿಗೆ ಪ್ರಜ್ಞೆ ಬಂತು. ಹೇಳಿದ: ಈ ಮಾತು ನನ್ನ ಬಾಯಿಂದ ಹೇಗೆ ಬಂತು? ದೇವತೆಗಳೇ "
           "ನನ್ನನ್ನ ಮೋಸ ಮಾಡಿದ್ರು.",
    "k11": "ಇನ್ನೊಂದು ವಿಷಯ ಜನರಿಗೆ ಗೊತ್ತಿಲ್ಲ. ಅವನು ಇಂದ್ರಾಸನದ ಬದಲು, ತಪ್ಪಿ ನಿದ್ರಾಸನ ಅಂದ ಅಂತ ನಾವು ಕೇಳಿದ್ದೀವಿ. ಈ ಪದದ "
           "ಆಟ, ವಾಲ್ಮೀಕಿ ರಾಮಾಯಣದಲ್ಲಿ ಇಲ್ಲ.",
    "k12": "ವಾಲ್ಮೀಕಿಯಲ್ಲೇ, ಯುದ್ಧ ಕಾಂಡದಲ್ಲಿ, ಅವನ ನಿದ್ದೆಗೆ ಇನ್ನೊಂದು ಕಾರಣನೂ ಇದೆ.",
    "k13": "ಅಲ್ಲಿ ವಿಭೀಷಣ ಹೇಳ್ತಾನೆ: ಕುಂಭಕರ್ಣ ಜೀವಿಗಳನ್ನ ತಿನ್ನೋಕೆ ಶುರು ಮಾಡಿದ, ಅದಕ್ಕೆ ಬ್ರಹ್ಮ ಶಾಪ ಕೊಟ್ಟ: ನೀನು ಸತ್ತವನ "
           "ಹಾಗೆ ಮಲಗಿರ್ತೀಯ.",
    "k14": "ರಾವಣ ಬೇಡಿಕೊಂಡ. ಆಗ ಬ್ರಹ್ಮ ಹೇಳಿದ: ಇವನು ಆರು ತಿಂಗಳು ಮಲಗ್ತಾನೆ, ಒಂದು ದಿನ ಎದ್ದಿರ್ತಾನೆ.",
    "k15": "ಅಂದ್ರೆ ಒಂದೇ ರಾಮಾಯಣದಲ್ಲಿ, ನಿದ್ದೆಗೆ ಎರಡು ಕಥೆ: ಒಂದು ವರ, ಇನ್ನೊಂದು ಶಾಪ.",
    "k16": "ನಿಮಗೆ ಏನನ್ನಿಸುತ್ತೆ: ಕುಂಭಕರ್ಣನ ನಿದ್ದೆ ವರನಾ, ಶಾಪನಾ? ಕಾಮೆಂಟ್ ಮಾಡಿ ಹೇಳಿ.",
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


def draw(cr, t, tl):
    from scenes_kumbhakarna import draw as _draw
    _draw(cr, t, tl)


def sfx(tl):
    from scenes_kumbhakarna import sfx as _sfx
    return _sfx(tl)
