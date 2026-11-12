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
# (earlier) Rewritten 12 Nov 2026 for kid-level clarity (owner: "the hook needs to be strong and story clear so even a kid can understand"): max 3 names, one storyline, a concrete hook.
# Rewritten 12 Nov 2026 to 5-year-old level (owner: "I want story so clear and very good explained even a 5 year old can understand"): short sentences, everyday words, hard words explained.
from channel import ASSETS_ROOT, MUSIC, NARRATORS, NARRATOR_LABEL, REVEAL_GAP, TAIL  # noqa: F401

G = REVEAL_GAP
SCRIPTS = {
    "hi": [
        dict(id="m1", text="सोचो, द्रौपदी ने दुर्योधन से कभी नहीं कहा था: अंधे का पुत्र अंधा। ये बात महाभारत में है ही नहीं!", gap=G),
        dict(id="m2", text="हम सबने टीवी पर देखा है: दुर्योधन पानी में गिरा, और द्रौपदी हँसकर बोली, अंधे का पुत्र अंधा।"),
        dict(id="m3", text="पर व्यास जी ने जो असली महाभारत लिखी, उसमें ये बात कहीं नहीं है।", gap=G),
        dict(id="m4", text="तो असल में क्या हुआ था? पांडव और दुर्योधन, चचेरे भाई थे। पांडवों का एक जादुई महल था।"),
        dict(id="m5", text="उस महल में, ज़मीन पानी जैसी दिखती थी, और पानी ज़मीन जैसा।", gap=G),
        dict(id="m6", text="दुर्योधन वहाँ घूम रहा था। उसे पानी, ज़मीन लगा। वो आगे बढ़ा... और छपाक से पानी में गिर गया!", gap=G),
        dict(id="m7", text="ये देखकर भीम हँसे, नौकर हँसे, और अर्जुन, नकुल, सहदेव भी हँसे।"),
        dict(id="m8", text="पर उस वक़्त, द्रौपदी का नाम तक नहीं लिखा है।", gap=G),
        dict(id="m9", text="बाद में दुर्योधन ने अपने पिता से शिकायत की: द्रौपदी भी हँसी थी। पर अंधे का पुत्र अंधा, ये किसी ने नहीं कहा।"),
        dict(id="m10", text="दुर्योधन ने ख़ुद बताया, उसे असल में क्या चुभ रहा था: पांडवों का पैसा, और उनकी शान। उसे उनसे जलन हो रही थी।", gap=G),
        dict(id="m10c", text="यानी जिस हँसी को हम महाभारत की वजह मानते हैं... उसकी असली जड़, किसी और के दिल में थी।", gap=G),
        dict(id="m11", text="तो महाभारत की असली वजह क्या थी: द्रौपदी की हँसी, या दुर्योधन की जलन? कमेंट में बताओ।"),
    ],
}
KN = {
    "m1": "ಯೋಚಿಸಿ... ದ್ರೌಪದಿ ದುರ್ಯೋಧನನಿಗೆ ಯಾವತ್ತೂ ಹೇಳಿರಲಿಲ್ಲ: ಕುರುಡನ ಮಗ ಕುರುಡನೇ. ಈ ಮಾತು ಮಹಾಭಾರತದಲ್ಲೇ ಇಲ್ಲ!",
    "m2": "ನಾವೆಲ್ಲ ಟಿವಿಯಲ್ಲಿ ನೋಡಿದ್ದೀವಿ: ದುರ್ಯೋಧನ ನೀರಲ್ಲಿ ಬಿದ್ದ, ದ್ರೌಪದಿ ನಗ್ತಾ ಹೇಳಿದ್ಳು, ಕುರುಡನ ಮಗ ಕುರುಡನೇ.",
    "m3": "ಆದ್ರೆ ವ್ಯಾಸರು ಬರೆದ ನಿಜವಾದ ಮಹಾಭಾರತದಲ್ಲಿ, ಈ ಮಾತು ಎಲ್ಲೂ ಇಲ್ಲ.",
    "m4": "ಹಾಗಾದ್ರೆ ನಿಜವಾಗಿ ಏನಾಯ್ತು? ಪಾಂಡವರು ಮತ್ತು ದುರ್ಯೋಧನ, ಅಣ್ಣತಮ್ಮಂದಿರ ಮಕ್ಕಳು. ಪಾಂಡವರಿಗೆ ಒಂದು ಮಾಯೆಯ ಅರಮನೆ ಇತ್ತು.",
    "m5": "ಆ ಅರಮನೆಯಲ್ಲಿ, ನೆಲ ನೀರಿನ ಹಾಗೆ ಕಾಣ್ತಿತ್ತು, ನೀರು ನೆಲದ ಹಾಗೆ.",
    "m6": "ದುರ್ಯೋಧನ ಅಲ್ಲಿ ತಿರುಗಾಡ್ತಿದ್ದ. ನೀರನ್ನ ನೆಲ ಅಂದ್ಕೊಂಡು ಮುಂದೆ ಹೋದ... ದಢಾರ್ ಅಂತ ನೀರಲ್ಲಿ ಬಿದ್ದ!",
    "m7": "ಇದನ್ನ ನೋಡಿ ಭೀಮ ನಕ್ಕ, ಸೇವಕರು ನಕ್ಕರು, ಅರ್ಜುನ, ನಕುಲ, ಸಹದೇವನೂ ನಕ್ಕರು.",
    "m8": "ಆದ್ರೆ ಆ ಕ್ಷಣದಲ್ಲಿ, ದ್ರೌಪದಿಯ ಹೆಸರೇ ಬರೆದಿಲ್ಲ.",
    "m9": "ಆಮೇಲೆ ದುರ್ಯೋಧನ ಅಪ್ಪನ ಹತ್ರ ದೂರು ಹೇಳಿದ: ದ್ರೌಪದಿನೂ ನಕ್ಕಳು. ಆದ್ರೆ ಕುರುಡನ ಮಗ ಕುರುಡ ಅಂತ, ಯಾರೂ ಹೇಳಿಲ್ಲ.",
    "m10": "ದುರ್ಯೋಧನನೇ ತನ್ನ ನಿಜವಾದ ನೋವು ಹೇಳಿದ: ಪಾಂಡವರ ದುಡ್ಡು, ಅವರ ಗೌರವ ನೋಡಿ, ಅವನಿಗೆ ಹೊಟ್ಟೆಕಿಚ್ಚು ಆಗ್ತಿತ್ತು.",
    "m10c": "ಅಂದ್ರೆ ನಾವು ಮಹಾಭಾರತಕ್ಕೆ ಕಾರಣ ಅಂದ್ಕೊಂಡಿರೋ ಆ ನಗು... ಅದರ ನಿಜವಾದ ಬೇರು, ಬೇರೆಯವನ ಮನಸ್ಸಲ್ಲಿತ್ತು.",
    "m11": "ಹಾಗಾದ್ರೆ ಮಹಾಭಾರತದ ನಿಜವಾದ ಕಾರಣ ಯಾವುದು: ದ್ರೌಪದಿಯ ನಗು, ಅಥವಾ ದುರ್ಯೋಧನನ ಹೊಟ್ಟೆಕಿಚ್ಚು? ಕಾಮೆಂಟ್ ಮಾಡಿ ಹೇಳಿ.",
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


def _scenes(tl):
    """Hindi: shadow puppets (scenes_andhe_ka_putra); Kannada: Yakshagana stage (scenes_andhe_ka_putra_yk), so the two channels never share
    pictures."""
    import importlib
    yk = getattr(tl, "lang", "hi") == "kn"
    return importlib.import_module("scenes_andhe_ka_putra_yk" if yk else "scenes_andhe_ka_putra")


def draw(cr, t, tl):
    _scenes(tl).draw(cr, t, tl)


def sfx(tl):
    return _scenes(tl).sfx(tl)
