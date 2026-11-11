"""Mythology video 12: a butcher teaches dharma to a sage (owner, 11 Nov 2026: "Now make one short make on interesting
engaging arguable one please"). A new kind for variety: ordinary people (a housewife, a meat-seller) humble a proud
sage. Debate ending: who is more righteous? Look: Togalu Gombeyaata shadow puppets; the bird's death is a soft fall,
the meat shop is shown simply (hanging cuts as plain shapes, no blood). Calm sound.

Facts (Mahabharata, Vana Parva, Markandeya-Samasya, K. M. Ganguli translation, sections 205-214):
- 205: the Brahmana Kausika, reciting the Vedas under a tree, is fouled by a she-crane; his angry glance kills it;
  "Alas, I have done a bad deed, urged by anger and malice!" At a house for alms the housewife says "Stay", serves
  her husband first, and then: "I am no she-crane, O regenerate Rishi!"; he does not know true virtue; go to Mithila
  to a virtuous fowler (vyadha).
- 206: in Mithila the fowler sells meat in a butcher's yard and already knows: "The word that the chaste woman said
  unto thee, viz., Repair thou to Mithila, are known to me."
- 207: he admits his trade is cruel ("Those animals that are slain by me and whose meat I sell").
- 213: at home: "These my father and mother, O Brahmana, are my supreme gods"; "with my own hands I assist them in
  bathing and also wash their feet and give them food."
- 214: "thou hast left home without their permission"; "thy ascetic and aged parents have become entirely blind from
  grief at thy loss"; "Return to the side of thy father and mother". Kausika goes home to serve them.
"""
from channel import ASSETS_ROOT, MUSIC, NARRATORS, NARRATOR_LABEL, REVEAL_GAP, TAIL  # noqa: F401

G = REVEAL_GAP
SCRIPTS = {
    "hi": [
        dict(id="d1", text="सोचो, एक ऋषि की एक ग़ुस्से भरी नज़र से, एक पक्षी मर गया... और उसी ऋषि को, एक कसाई ने धर्म "
                           "सिखाया।", gap=G),
        dict(id="d2", text="ये कोई फ़िल्मी कहानी नहीं है। ये महाभारत के वन पर्व में लिखा है।"),
        dict(id="d3", text="कौशिक नाम के एक ऋषि, पेड़ के नीचे बैठकर वेद पढ़ रहे थे।"),
        dict(id="d4", text="ऊपर बैठे एक बगुले ने, उन पर बीट कर दी।"),
        dict(id="d5", text="ऋषि ने ग़ुस्से से ऊपर देखा... और बगुला मरकर नीचे गिर पड़ा।", gap=G),
        dict(id="d6", text="ऋषि को बहुत दुख हुआ। बोले: ये मैंने ग़ुस्से में क्या कर दिया।"),
        dict(id="d7", text="फिर वो भिक्षा माँगने एक घर गए। घर की औरत बोली: थोड़ा रुकिए।"),
        dict(id="d8", text="तभी उसका पति भूखा घर लौटा। उसने पहले पति को खाना खिलाया, और ऋषि को इंतज़ार करवाया।"),
        dict(id="d9", text="ऋषि को ग़ुस्सा आया। तब वो औरत बोली: मैं कोई बगुला नहीं हूँ, जो आपकी नज़र से मर जाऊँ।",
             gap=G),
        dict(id="d10", text="ऋषि हैरान रह गए। जंगल में क्या हुआ, ये इसे कैसे पता?"),
        dict(id="d11", text="औरत बोली: आप धर्म नहीं जानते। मिथिला जाइए। वहाँ मांस बेचने वाला एक कसाई, आपको धर्म सिखाएगा।"),
        dict(id="d12", text="ऋषि मिथिला पहुँचे। कसाई अपनी दुकान पर मांस बेच रहा था। ऋषि को देखते ही बोला: आपको उस औरत "
                            "ने भेजा है ना?", gap=G),
        dict(id="d13", text="वो ऋषि को अपने घर ले गया। वहाँ उसके बूढ़े माँ-बाप बैठे थे।"),
        dict(id="d14", text="कसाई बोला: यही मेरे भगवान हैं। मैं अपने हाथों से इन्हें नहलाता हूँ, इनके पैर धोता हूँ, और "
                            "खाना खिलाता हूँ।"),
        dict(id="d15", text="फिर बोला: और आप? आप अपने माँ-बाप को बिना बताए, घर छोड़कर तपस्या करने चले गए।"),
        dict(id="d16", text="आपके दुख में, वो अंधे हो गए हैं। जाइए, पहले उनकी सेवा कीजिए।", gap=G),
        dict(id="d17", text="और ऋषि सच में, अपने माँ-बाप की सेवा करने घर लौट गए।"),
        dict(id="d18", text="तो बड़ा धर्मी कौन: वेद पढ़ने वाला ऋषि, या माँ-बाप की सेवा करने वाला कसाई? कमेंट में बताओ।"),
    ],
}
KN = {
    "d1": "ಯೋಚಿಸಿ... ಒಬ್ಬ ಋಷಿಯ ಒಂದೇ ಕೋಪದ ನೋಟಕ್ಕೆ, ಒಂದು ಹಕ್ಕಿ ಸತ್ತುಹೋಯ್ತು... ಅದೇ ಋಷಿಗೆ, ಒಬ್ಬ ಕಟುಕ ಧರ್ಮ "
          "ಕಲಿಸಿದ.",
    "d2": "ಇದು ಸಿನಿಮಾ ಕಥೆ ಅಲ್ಲ. ಮಹಾಭಾರತದ ವನ ಪರ್ವದಲ್ಲೇ ಇದೆ.",
    "d3": "ಕೌಶಿಕ ಅನ್ನೋ ಒಬ್ಬ ಋಷಿ, ಮರದ ಕೆಳಗೆ ಕೂತು ವೇದ ಓದ್ತಿದ್ರು.",
    "d4": "ಮೇಲೆ ಕೂತಿದ್ದ ಒಂದು ಕೊಕ್ಕರೆ, ಅವರ ಮೇಲೆ ಹಿಕ್ಕೆ ಹಾಕಿತು.",
    "d5": "ಋಷಿ ಕೋಪದಿಂದ ಮೇಲೆ ನೋಡಿದ್ರು... ಕೊಕ್ಕರೆ ಸತ್ತು ಕೆಳಗೆ ಬಿತ್ತು.",
    "d6": "ಋಷಿಗೆ ತುಂಬಾ ಬೇಜಾರಾಯ್ತು. ಹೇಳಿದ್ರು: ಕೋಪದಲ್ಲಿ ನಾನು ಏನು ಮಾಡಿಬಿಟ್ಟೆ.",
    "d7": "ಆಮೇಲೆ ಅವರು ಭಿಕ್ಷೆ ಕೇಳೋಕೆ ಒಂದು ಮನೆಗೆ ಹೋದ್ರು. ಮನೆಯ ಹೆಂಗಸು ಹೇಳಿದ್ಳು: ಸ್ವಲ್ಪ ಇರಿ.",
    "d8": "ಅಷ್ಟರಲ್ಲಿ ಅವಳ ಗಂಡ ಹಸಿವಿಂದ ಮನೆಗೆ ಬಂದ. ಅವಳು ಮೊದಲು ಗಂಡನಿಗೆ ಊಟ ಹಾಕಿದ್ಳು, ಋಷಿನ ಕಾಯಿಸಿದ್ಳು.",
    "d9": "ಋಷಿಗೆ ಕೋಪ ಬಂತು. ಆಗ ಆ ಹೆಂಗಸು ಹೇಳಿದ್ಳು: ನಾನು ಕೊಕ್ಕರೆ ಅಲ್ಲ, ನಿಮ್ಮ ನೋಟಕ್ಕೆ ಸಾಯೋಕೆ.",
    "d10": "ಋಷಿಗೆ ಶಾಕ್ ಆಯ್ತು. ಕಾಡಲ್ಲಿ ಏನಾಯ್ತು ಅಂತ, ಇವಳಿಗೆ ಹೇಗೆ ಗೊತ್ತು?",
    "d11": "ಅವಳು ಹೇಳಿದ್ಳು: ನಿಮಗೆ ಧರ್ಮ ಗೊತ್ತಿಲ್ಲ. ಮಿಥಿಲೆಗೆ ಹೋಗಿ. ಅಲ್ಲಿ ಮಾಂಸ ಮಾರೋ ಒಬ್ಬ ಕಟುಕ, ನಿಮಗೆ ಧರ್ಮ ಕಲಿಸ್ತಾನೆ.",
    "d12": "ಋಷಿ ಮಿಥಿಲೆಗೆ ಬಂದ್ರು. ಕಟುಕ ತನ್ನ ಅಂಗಡಿಯಲ್ಲಿ ಮಾಂಸ ಮಾರ್ತಿದ್ದ. ಋಷಿನ ನೋಡಿದ ತಕ್ಷಣ ಹೇಳಿದ: ನಿಮ್ಮನ್ನ ಆ "
           "ಹೆಂಗಸು ಕಳಿಸಿದ್ಳು ಅಲ್ವಾ?",
    "d13": "ಅವನು ಋಷಿನ ತನ್ನ ಮನೆಗೆ ಕರ್ಕೊಂಡು ಹೋದ. ಅಲ್ಲಿ ಅವನ ವಯಸ್ಸಾದ ಅಪ್ಪ ಅಮ್ಮ ಕೂತಿದ್ರು.",
    "d14": "ಕಟುಕ ಹೇಳಿದ: ಇವರೇ ನನ್ನ ದೇವರು. ನನ್ನ ಕೈಯಿಂದಲೇ ಇವರಿಗೆ ಸ್ನಾನ ಮಾಡಿಸ್ತೀನಿ, ಕಾಲು ತೊಳೀತೀನಿ, ಊಟ "
           "ಮಾಡಿಸ್ತೀನಿ.",
    "d15": "ಆಮೇಲೆ ಹೇಳಿದ: ಮತ್ತೆ ನೀವು? ನಿಮ್ಮ ಅಪ್ಪ ಅಮ್ಮನಿಗೆ ಹೇಳದೆ, ಮನೆ ಬಿಟ್ಟು ತಪಸ್ಸಿಗೆ ಹೋದ್ರಿ.",
    "d16": "ನಿಮ್ಮ ಚಿಂತೆಯಲ್ಲಿ ಅವರು ಕುರುಡರಾಗಿದ್ದಾರೆ. ಹೋಗಿ, ಮೊದಲು ಅವರ ಸೇವೆ ಮಾಡಿ.",
    "d17": "ಋಷಿ ನಿಜವಾಗಲೂ, ಅಪ್ಪ ಅಮ್ಮನ ಸೇವೆ ಮಾಡೋಕೆ ಮನೆಗೆ ವಾಪಸ್ ಹೋದ್ರು.",
    "d18": "ಹಾಗಾದ್ರೆ ದೊಡ್ಡ ಧರ್ಮಿ ಯಾರು: ವೇದ ಓದೋ ಋಷಿನಾ, ಅಥವಾ ಅಪ್ಪ ಅಮ್ಮನ ಸೇವೆ ಮಾಡೋ ಕಟುಕನಾ? ಕಾಮೆಂಟ್ ಮಾಡಿ ಹೇಳಿ.",
}
SCRIPTS["kn"] = [dict(line, text=KN[line["id"]]) for line in SCRIPTS["hi"]]   # same ids and pauses as Hindi

_SOURCES = ["Mahabharata, Vana Parva, sections 205-214 (K. M. Ganguli translation)"]
METADATA = {
    "hi": dict(
        title="Ek kasai ne rishi ko dharm sikhaya",
        caption="Socho, ek rishi ki ek gusse bhari nazar se ek pakshi mar gaya... aur usi rishi ko ek kasai ne dharm "
                "sikhaya 😳\n\nMahabharat, Van Parva: ek aurat boli \"main koi bagula nahi hoon\", aur rishi ko "
                "Mithila ke kasai ke paas bheja. Kasai bola: mere maa-baap hi mere bhagwan hain.\n\n"
                "Bada dharmi kaun: rishi ya kasai? Comment mein batao 👇",
        yt_title="Ek Kasai Ne Rishi Ko Dharm Sikhaya 😳 | Dharmavyadh Ki Katha | Mahabharat",
        yt_description="Rishi Kaushik ki gusse bhari nazar se ek bagula mar gaya. Bhiksha maangne gaye toh ek aurat ne "
                       "unhe intezaar karvaya aur boli, main koi bagula nahi hoon. Usne unhe Mithila ke ek kasai ke "
                       "paas bheja, jo apne boodhe maa-baap ko bhagwan maankar unki seva karta tha. Kasai ne bataya ki "
                       "rishi ke apne maa-baap unke dukh mein andhe ho gaye hain.",
        hashtags=["#mahabharat", "#dharm", "#mythology", "#kahani", "#hindu"],
        pinned_comment="Bada dharmi kaun: ved padhne wala rishi, ya maa-baap ki seva karne wala kasai? 👇",
        sources=_SOURCES),
    "kn": dict(
        title="Rishige dharma kalisida katuka",
        caption="Yochisi: obba rishiya ondu kopada notakke ondu hakki sattuhoytu... ade rishige obba katuka dharma "
                "kalisida 😳\n\nMahabharata, Vana Parva: obba hengasu \"naanu kokkare alla\" andlu, rishiyannu "
                "Mithileya katukana hatra kalisidlu. Katuka helida: nanna appa amma ne nanna devaru.\n\n"
                "Dodda dharmi yaaru: rishi na, katuka na? Comment maadi 👇",
        yt_title="Rishige Dharma Kalisida Katuka 😳 | Dharmavyadha | Mahabharata",
        yt_description="Rishi Kaushikana kopada notakke ondu kokkare sattu bittu. Bhikshe kelalu hodaaga obba hengasu "
                       "avarannu kaayisi, naanu kokkare alla andlu. Avalu avarannu Mithileya obba katukana hatra "
                       "kalisidlu, avanu tanna vayassaada appa ammana seve maadtidda. Rishiya swanta appa amma avara "
                       "chinteyalli kurudaagiddaare anta katuka helida.",
        hashtags=["#kannada", "#mahabharata", "#dharma", "#kannadastory", "#mythology"],
        pinned_comment="Dodda dharmi yaaru: veda odo rishi na, appa ammana seve maado katuka na? 👇",
        sources=_SOURCES),
}


USED_ASSETS, CREDITS_FILES = [], []      # everything in this video is drawn in code


def draw(cr, t, tl):
    from scenes_dharmavyadha import draw as _draw
    _draw(cr, t, tl)


def sfx(tl):
    from scenes_dharmavyadha import sfx as _sfx
    return _sfx(tl)
