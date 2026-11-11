"""Mythology video 19: myth-bust, "andhe ka putra andha" is not in the Mahabharata (owner, 11 Nov 2026: "Make next 5
shorts all on good topics"). The Lakshman Rekha pattern (the channel's best reel): a famous line the texts don't
have, then what Vyasa actually wrote, told precisely (Draupadi is absent from the narration; only Duryodhana's own
later complaint says she laughed; nobody says "blind"), and the reason the text itself gives: envy. Debate: Draupadi's
laughter or Duryodhana's envy? Look: Togalu Gombeyaata shadow puppets; the palace of illusions in crystal blues.
Calm sound.

Facts (Mahabharata, Sabha Parva, K. M. Ganguli translation):
- 46: in Maya's palace Duryodhana mistakes crystal for water and water for crystal and falls into a tank; "the
  mighty Bhima laughed aloud as also the menials of the palace"; "the mighty Bhima and Arjuna and both the twins--all
  laughed aloud". Draupadi is not mentioned.
- 48: Duryodhana tells Dhritarashtra his torment is envy of Yudhishthira's prosperity (the tribute, the wealth).
- 49: in his own account Duryodhana says "Draupadi also accompanied by other females joined in the laughter". No
  words like "son of a blind man" are spoken by anyone in these sections.
- The line is popular from later retellings and television.
"""
from channel import ASSETS_ROOT, MUSIC, NARRATORS, NARRATOR_LABEL, REVEAL_GAP, TAIL  # noqa: F401

G = REVEAL_GAP
SCRIPTS = {
    "hi": [
        dict(id="m1", text="सोचो, जिस एक लाइन की वजह से महाभारत हुआ... वो लाइन महाभारत में है ही नहीं।", gap=G),
        dict(id="m2", text="हम सबने सुना है: द्रौपदी ने दुर्योधन से कहा, अंधे का पुत्र अंधा।", gap=G),
        dict(id="m3", text="पर व्यास जी की महाभारत में, ये शब्द कहीं नहीं हैं। ये बाद की कहानियों और टीवी से आए।"),
        dict(id="m4", text="तो असल में क्या हुआ था? युधिष्ठिर के राजसूय यज्ञ के बाद, दुर्योधन मय दानव के बनाए महल में घूम रहा "
                           "था।"),
        dict(id="m5", text="वो महल जादुई था। जहाँ फ़र्श था, वहाँ पानी लगता था। और जहाँ पानी था, वहाँ फ़र्श।"),
        dict(id="m6", text="दुर्योधन ने फ़र्श को पानी समझकर, कपड़े ऊपर उठा लिए। फिर आगे, पानी को फ़र्श समझा, और सीधा तालाब में "
                           "गिर पड़ा।", gap=G),
        dict(id="m7", text="सभा पर्व कहता है: ये देखकर भीम हँसे, नौकर हँसे, और फिर अर्जुन, नकुल, सहदेव भी हँस पड़े।"),
        dict(id="m8", text="और द्रौपदी? उस हिस्से में, द्रौपदी का नाम तक नहीं है।", gap=G),
        dict(id="m9", text="हाँ, बाद में दुर्योधन ख़ुद अपने पिता से शिकायत करता है, कि द्रौपदी भी औरतों के साथ हँसी थी।"),
        dict(id="m10", text="पर अंधे का पुत्र अंधा, ये बात किसी ने नहीं कही। न द्रौपदी ने, न भीम ने।", gap=G),
        dict(id="m11", text="तो दुर्योधन ने जुए का खेल क्यों रचा? सभा पर्व में वो ख़ुद बताता है: पांडवों की दौलत और शान देखकर, "
                            "उसका दिल जल रहा था।"),
        dict(id="m12", text="यानी असली वजह थी: जलन।", gap=G),
        dict(id="m13", text="तो आपको क्या लगता है, महाभारत की असली वजह क्या थी: द्रौपदी की हँसी, या दुर्योधन की जलन? कमेंट "
                            "में बताओ।"),
    ],
}
KN = {
    "m1": "ಯೋಚಿಸಿ... ಯಾವ ಒಂದು ಮಾತಿಂದ ಮಹಾಭಾರತ ಆಯ್ತು ಅಂತಾರೋ... ಆ ಮಾತು ಮಹಾಭಾರತದಲ್ಲೇ ಇಲ್ಲ.",
    "m2": "ನಾವೆಲ್ಲ ಕೇಳಿರೋದು: ದ್ರೌಪದಿ ದುರ್ಯೋಧನನಿಗೆ ಹೇಳಿದ್ಳು, ಕುರುಡನ ಮಗ ಕುರುಡನೇ.",
    "m3": "ಆದ್ರೆ ವ್ಯಾಸರ ಮಹಾಭಾರತದಲ್ಲಿ, ಈ ಮಾತು ಎಲ್ಲೂ ಇಲ್ಲ. ಇದು ಆಮೇಲಿನ ಕಥೆಗಳಿಂದ, ಟಿವಿಯಿಂದ ಬಂದಿದ್ದು.",
    "m4": "ಹಾಗಾದ್ರೆ ನಿಜವಾಗಿ ಏನಾಯ್ತು? ಯುಧಿಷ್ಠಿರನ ರಾಜಸೂಯ ಯಜ್ಞದ ನಂತರ, ದುರ್ಯೋಧನ ಮಯಾಸುರ ಕಟ್ಟಿದ ಅರಮನೆಯಲ್ಲಿ "
          "ತಿರುಗಾಡ್ತಿದ್ದ.",
    "m5": "ಅದು ಮಾಯೆಯ ಅರಮನೆ. ನೆಲ ಇದ್ದ ಕಡೆ ನೀರಿನ ಹಾಗೆ ಕಾಣ್ತಿತ್ತು. ನೀರಿದ್ದ ಕಡೆ ನೆಲದ ಹಾಗೆ.",
    "m6": "ದುರ್ಯೋಧನ ನೆಲವನ್ನ ನೀರು ಅಂದ್ಕೊಂಡು, ಬಟ್ಟೆ ಮೇಲೆತ್ತಿದ. ಮುಂದೆ ನೀರನ್ನ ನೆಲ ಅಂದ್ಕೊಂಡು, ನೇರವಾಗಿ ಕೊಳದಲ್ಲಿ "
          "ಬಿದ್ದ.",
    "m7": "ಸಭಾ ಪರ್ವ ಹೇಳುತ್ತೆ: ಇದನ್ನ ನೋಡಿ ಭೀಮ ನಕ್ಕ, ಸೇವಕರು ನಕ್ಕರು, ಆಮೇಲೆ ಅರ್ಜುನ, ನಕುಲ, ಸಹದೇವನೂ ನಕ್ಕರು.",
    "m8": "ಮತ್ತೆ ದ್ರೌಪದಿ? ಆ ಭಾಗದಲ್ಲಿ, ದ್ರೌಪದಿಯ ಹೆಸರೇ ಇಲ್ಲ.",
    "m9": "ಹೌದು, ಆಮೇಲೆ ದುರ್ಯೋಧನನೇ ತನ್ನ ಅಪ್ಪನ ಹತ್ರ ದೂರು ಹೇಳ್ತಾನೆ, ದ್ರೌಪದಿನೂ ಹೆಂಗಸರ ಜೊತೆ ನಕ್ಕಳು ಅಂತ.",
    "m10": "ಆದ್ರೆ ಕುರುಡನ ಮಗ ಕುರುಡ ಅನ್ನೋ ಮಾತು, ಯಾರೂ ಹೇಳಿಲ್ಲ. ದ್ರೌಪದಿನೂ ಇಲ್ಲ, ಭೀಮನೂ ಇಲ್ಲ.",
    "m11": "ಹಾಗಾದ್ರೆ ದುರ್ಯೋಧನ ಜೂಜಾಟ ಯಾಕೆ ಏರ್ಪಡಿಸಿದ? ಸಭಾ ಪರ್ವದಲ್ಲಿ ಅವನೇ ಹೇಳ್ತಾನೆ: ಪಾಂಡವರ ಸಂಪತ್ತು, ಗೌರವ ನೋಡಿ, "
           "ಅವನ ಮನಸ್ಸು ಉರೀತಿತ್ತು.",
    "m12": "ಅಂದ್ರೆ ನಿಜವಾದ ಕಾರಣ: ಹೊಟ್ಟೆಕಿಚ್ಚು.",
    "m13": "ನಿಮಗೆ ಏನನ್ನಿಸುತ್ತೆ, ಮಹಾಭಾರತದ ನಿಜವಾದ ಕಾರಣ ಯಾವುದು: ದ್ರೌಪದಿಯ ನಗು, ಅಥವಾ ದುರ್ಯೋಧನನ ಹೊಟ್ಟೆಕಿಚ್ಚು? ಕಾಮೆಂಟ್ "
           "ಮಾಡಿ ಹೇಳಿ.",
}
SCRIPTS["kn"] = [dict(line, text=KN[line["id"]]) for line in SCRIPTS["hi"]]   # same ids and pauses as Hindi

_SOURCES = ["Mahabharata, Sabha Parva, sections 46-49 (K. M. Ganguli translation)"]
METADATA = {
    "hi": dict(
        title="Andhe ka putra andha: Mahabharat mein hai hi nahi",
        caption="Socho, jis ek line ki wajah se Mahabharat hua... woh line Mahabharat mein hai hi nahi 😳\n\n"
                "Vyas ji ki Mahabharat, Sabha Parv: Duryodhan maya mahal mein taalaab mein gira, Bheem, Arjun, Nakul, "
                "Sahdev aur naukar hanse. 'Andhe ka putra andha' kisi ne nahi kaha.\n\n"
                "Asli wajah kya thi: Draupadi ki hansi ya Duryodhan ki jalan? Comment mein batao 👇",
        yt_title="Andhe Ka Putra Andha: Mahabharat Mein Hai Hi Nahi 😳 | Sabha Parv Ka Sach",
        yt_description="Hum sabne suna hai ki Draupadi ne Duryodhan se kaha, andhe ka putra andha. Par Vyas ji ki "
                       "Mahabharat ke Sabha Parv mein ye shabd kahin nahi hain. Maya mahal mein Duryodhan taalaab mein "
                       "gira, toh Bheem, naukar, Arjun aur judwa bhai hanse; Draupadi ka naam us hisse mein nahi hai. "
                       "Baad mein Duryodhan khud kehta hai ki Draupadi bhi hansi thi. Aur jue ki asli wajah Duryodhan "
                       "khud batata hai: Pandavon ki daulat dekhkar jalan.",
        hashtags=["#mahabharat", "#draupadi", "#mythology", "#kahani", "#hindu"],
        pinned_comment="Mahabharat ki asli wajah: Draupadi ki hansi, ya Duryodhan ki jalan? 👇",
        sources=_SOURCES),
    "kn": dict(
        title="Kurudana maga kuruda: Mahabharatadalli ilve illa",
        caption="Yochisi: yaava ondu maatinda Mahabharata aaytu antaaro... aa maatu Mahabharatadalle illa 😳\n\n"
                "Vyasara Mahabharata, Sabha Parva: Duryodhana maayeya aramaneyalli koladalli bidda, Bheema, Arjuna, "
                "Nakula, Sahadeva mattu sevakaru nakkaru. 'Kurudana maga kuruda' yaaru helilla.\n\n"
                "Nijavaada kaarana yaavudu: Draupadiya nagu na, Duryodhanana hottekichchu na? Comment maadi 👇",
        yt_title="Kurudana Maga Kuruda: Mahabharatadalli Ilve Illa 😳 | Sabha Parvada Satya",
        yt_description="Naavella kelirodu Draupadi Duryodhananige kurudana maga kurudane anta helidlu anta. Aadre "
                       "Vyasara Mahabharatada Sabha Parvadalli ee maatu ellu illa. Maayeya aramaneyalli Duryodhana "
                       "koladalli bidda, Bheema, sevakaru, Arjuna mattu avali tammandiru nakkaru; aa bhaagadalli "
                       "Draupadiya hesare illa. Aamele Duryodhanane heltaane Draupadiyu nakkalu anta. Jujina nijavaada "
                       "kaarana avane heltaane: Pandavara sampattu nodi hottekichchu.",
        hashtags=["#kannada", "#mahabharata", "#draupadi", "#kannadastory", "#mythology"],
        pinned_comment="Mahabharatada nijavaada kaarana: Draupadiya nagu na, Duryodhanana hottekichchu na? 👇",
        sources=_SOURCES),
}


USED_ASSETS, CREDITS_FILES = [], []      # everything in this video is drawn in code


def draw(cr, t, tl):
    from scenes_andhe_ka_putra import draw as _draw
    _draw(cr, t, tl)


def sfx(tl):
    from scenes_andhe_ka_putra import sfx as _sfx
    return _sfx(tl)
