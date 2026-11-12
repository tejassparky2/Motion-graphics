"""Mythology video 22: Death herself wept, because she did not want to kill anyone; her tears became diseases (the
owner's "Continue" after videos 15-19, 12 Nov 2026). A cosmic-origin story: a world with no death, a burdened Earth,
Brahma's anger as fire, the girl who refused, and the twist of the tears; debate: is death a punishment or a need?
Look: Hindi = Togalu Gombeyaata shadow puppets, Kannada = Yakshagana stage. Death is a dignified young woman, never a
skull or a monster; the fire is light only, nobody burns on screen. Calm sound.

Facts (Mahabharata, Drona Parva, Narada's story to King Akampana, who grieved his son; K. M. Ganguli translation,
the "origin of Death" sections; sacred-texts m07050-m07051):
- Brahma created beings and they multiplied; "the goddess Earth, afflicted with the heavy weight of creatures,
  always urged me for destroying the creatures on her"; Brahma's wrath became a fire "blasting rocks and trees and
  rivers"; Sthanu (Shiva) pleaded that the wrath be withdrawn so that "creatures endued with life may not cease to
  be"; Brahma restrained it, and from the doors of his senses came a woman, dark, red and tawny, with bright earrings,
  whom he named Death and told to slay all creatures.
- She wept aloud; the Grandsire caught her tears in his two hands. She asked how she, a woman created by him, could
  do such a cruel act; she stood on one leg for "sixteen billions of years", then on her toes, to be released; he
  would not release her.
- Brahma: "Those tear-drops of thine that are in my hands, even they will become diseases, springing from living
  creatures themselves"; "Thou shalt commit no sin, O Death, by slaying these creatures"; she agreed ("Yes!"), and
  took the lives of creatures when their time came. Akampana's grief left him.
"""
from channel import ASSETS_ROOT, MUSIC, NARRATORS, NARRATOR_LABEL, REVEAL_GAP, TAIL  # noqa: F401

G = REVEAL_GAP
SCRIPTS = {
    "hi": [
        dict(id="mr1", text="सोचो, जिस मौत से सारी दुनिया डरती है... वो ख़ुद रोई थी! क्योंकि वो, किसी को मारना नहीं चाहती थी।", gap=G),
        dict(id="mr2", text="ये महाभारत की सच्ची कहानी है।"),
        dict(id="mr3", text="बहुत पहले, जब ब्रह्मा जी ने दुनिया बनाई, तब कोई मरता ही नहीं था।"),
        dict(id="mr4", text="इंसान, जानवर, सब बढ़ते गए, बढ़ते गए। धरती पर, पैर रखने की जगह नहीं बची।", gap=G),
        dict(id="mr5", text="धरती माँ बोझ से थक गईं, और ब्रह्मा जी से बोलीं: ये बोझ, अब मुझसे नहीं उठता!"),
        dict(id="mr6", text="ब्रह्मा जी को इतना ग़ुस्सा आया, कि उनके ग़ुस्से से आग निकली। और दुनिया जलने लगी।", gap=G),
        dict(id="mr7", text="तब शिव जी आए, और बोले: रुकिए! सबको जलाइए मत।"),
        dict(id="mr8", text="ब्रह्मा जी ने आग, वापस अपने अंदर खींच ली। और उसी पल, उनके शरीर से, एक लड़की निकली।", gap=G),
        dict(id="mr9", text="ब्रह्मा जी ने उसका नाम रखा: मृत्यु, यानी मौत। और हुक्म दिया: जाओ, सबकी जान लो।"),
        dict(id="mr10", text="ये सुनते ही, वो लड़की फूट फूटकर रोने लगी। बोली: मैं किसी की जान, कैसे लूँ?"),
        dict(id="mr11", text="ब्रह्मा जी ने उसके आँसू, अपनी दोनों हथेलियों में भर लिए।", gap=G),
        dict(id="mr12", text="मना करने के लिए, वो एक पैर पर खड़ी रही... अरबों सालों तक!"),
        dict(id="mr13", text="पर ब्रह्मा जी नहीं माने। और उनकी हथेलियों में, अब भी उसके आँसू थे।", gap=G),
        dict(id="mr13q", text="तो उन आँसुओं का, क्या हुआ?"),
        dict(id="mr14", text="ब्रह्मा जी बोले: तुम्हारे ये आँसू, बीमारियाँ बनेंगे। और लोग, बीमारियों से मरेंगे।"),
        dict(id="mr15", text="तुम बस, सही समय आने पर, उन्हें ले जाना। इसका पाप, तुम्हें नहीं लगेगा।", gap=G),
        dict(id="mr16", text="तब जाकर, वो रोती हुई लड़की मानी। और दुनिया में, मौत आई।"),
        dict(id="mr16c", text="जिस मौत से हम सब डरते हैं... उसने पहली जान लेने से पहले, आँसू बहाए थे।", gap=G),
        dict(id="mr17", text="तो मौत, दुनिया के लिए सज़ा है, या ज़रूरत? कमेंट में बताओ।"),
    ],
}
KN = {
    "mr1": "ಯೋಚಿಸಿ... ಇಡೀ ಪ್ರಪಂಚ ಹೆದರೋ ಮೃತ್ಯು... ಅವಳೇ ಅತ್ತಿದ್ಲು! ಯಾಕಂದ್ರೆ ಅವಳಿಗೆ, ಯಾರನ್ನೂ ಕೊಲ್ಲೋಕೆ ಇಷ್ಟ ಇರಲಿಲ್ಲ.",
    "mr2": "ಇದು ಮಹಾಭಾರತದ ನಿಜವಾದ ಕಥೆ.",
    "mr3": "ತುಂಬಾ ಹಿಂದೆ, ಬ್ರಹ್ಮ ಪ್ರಪಂಚ ಸೃಷ್ಟಿ ಮಾಡಿದಾಗ, ಯಾರೂ ಸಾಯ್ತಾನೇ ಇರಲಿಲ್ಲ.",
    "mr4": "ಮನುಷ್ಯರು, ಪ್ರಾಣಿಗಳು, ಎಲ್ಲಾ ಜಾಸ್ತಿ ಆಗ್ತಾನೇ ಹೋದ್ರು. ಭೂಮಿ ಮೇಲೆ, ಕಾಲಿಡೋಕೂ ಜಾಗ ಇರಲಿಲ್ಲ.",
    "mr5": "ಭೂಮಿ ತಾಯಿ ಭಾರದಿಂದ ಸುಸ್ತಾಗಿ, ಬ್ರಹ್ಮನಿಗೆ ಹೇಳಿದ್ಲು: ಈ ಭಾರ, ಇನ್ನು ನನ್ನಿಂದ ಹೊರೋಕಾಗಲ್ಲ!",
    "mr6": "ಬ್ರಹ್ಮನಿಗೆ ಎಷ್ಟು ಕೋಪ ಬಂತು ಅಂದ್ರೆ, ಆ ಕೋಪದಿಂದ ಬೆಂಕಿ ಹುಟ್ಟಿತು. ಪ್ರಪಂಚ, ಸುಡೋಕೆ ಶುರುವಾಯ್ತು.",
    "mr7": "ಆಗ ಶಿವ ಬಂದು ಹೇಳಿದ: ನಿಲ್ಲಿ! ಎಲ್ಲರನ್ನೂ ಸುಡಬೇಡಿ.",
    "mr8": "ಬ್ರಹ್ಮ ಬೆಂಕಿನ, ವಾಪಸ್ ತನ್ನೊಳಗೆ ಎಳ್ಕೊಂಡ. ಅದೇ ಕ್ಷಣ, ಅವನ ದೇಹದಿಂದ, ಒಬ್ಬ ಹುಡುಗಿ ಹೊರಗೆ ಬಂದ್ಲು.",
    "mr9": "ಬ್ರಹ್ಮ ಅವಳಿಗೆ ಹೆಸರಿಟ್ಟ: ಮೃತ್ಯು, ಅಂದ್ರೆ ಸಾವು. ಆಜ್ಞೆ ಕೊಟ್ಟ: ಹೋಗು, ಎಲ್ಲರ ಪ್ರಾಣ ತಗೋ.",
    "mr10": "ಇದನ್ನ ಕೇಳಿದ ತಕ್ಷಣ, ಆ ಹುಡುಗಿ ಜೋರಾಗಿ ಅಳೋಕೆ ಶುರು ಮಾಡಿದ್ಲು. ಹೇಳಿದ್ಲು: ನಾನು ಯಾರ ಪ್ರಾಣ, ಹೇಗೆ ತಗೊಳ್ಳಲಿ?",
    "mr11": "ಬ್ರಹ್ಮ ಅವಳ ಕಣ್ಣೀರನ್ನ, ತನ್ನ ಎರಡೂ ಅಂಗೈಯಲ್ಲಿ ಹಿಡ್ಕೊಂಡ.",
    "mr12": "ಬೇಡ ಅಂತ ಹೇಳೋಕೆ, ಅವಳು ಒಂದೇ ಕಾಲಲ್ಲಿ ನಿಂತ್ಕೊಂಡ್ಲು... ನೂರಾರು ಕೋಟಿ ವರ್ಷ!",
    "mr13": "ಆದ್ರೆ ಬ್ರಹ್ಮ ಒಪ್ಪಲಿಲ್ಲ. ಅವನ ಅಂಗೈಯಲ್ಲಿ, ಇನ್ನೂ ಅವಳ ಕಣ್ಣೀರು ಇತ್ತು.",
    "mr13q": "ಹಾಗಾದ್ರೆ ಆ ಕಣ್ಣೀರು, ಏನಾಯ್ತು?",
    "mr14": "ಬ್ರಹ್ಮ ಹೇಳಿದ: ನಿನ್ನ ಈ ಕಣ್ಣೀರು, ರೋಗಗಳಾಗುತ್ತೆ. ಜನ, ರೋಗಗಳಿಂದ ಸಾಯ್ತಾರೆ.",
    "mr15": "ನೀನು ಬರೀ, ಸರಿಯಾದ ಸಮಯ ಬಂದಾಗ, ಅವರನ್ನ ಕರ್ಕೊಂಡು ಹೋಗು. ಆ ಪಾಪ, ನಿನಗೆ ತಟ್ಟಲ್ಲ.",
    "mr16": "ಆಗ, ಆ ಅಳ್ತಿದ್ದ ಹುಡುಗಿ ಒಪ್ಪಿದ್ಲು. ಪ್ರಪಂಚಕ್ಕೆ, ಸಾವು ಬಂತು.",
    "mr16c": "ನಾವೆಲ್ಲ ಹೆದರೋ ಮೃತ್ಯು... ಮೊದಲ ಪ್ರಾಣ ತಗೊಳ್ಳೋಕೆ ಮುಂಚೆ, ಕಣ್ಣೀರು ಹಾಕಿದ್ಲು.",
    "mr17": "ಹಾಗಾದ್ರೆ ಸಾವು, ಪ್ರಪಂಚಕ್ಕೆ ಶಿಕ್ಷೆನಾ, ಅಥವಾ ಅಗತ್ಯನಾ? ಕಾಮೆಂಟ್ ಮಾಡಿ ಹೇಳಿ.",
}
SCRIPTS["kn"] = [dict(line, text=KN[line["id"]]) for line in SCRIPTS["hi"]]   # same ids and pauses as Hindi

_SOURCES = ["Mahabharata, Drona Parva, Narada's story to King Akampana (K. M. Ganguli translation)"]
METADATA = {
    "hi": dict(
        title="Maut khud roi thi",
        caption="Socho, jis maut se saari duniya darti hai... woh khud roi thi 😳\n\n"
                "Mahabharat: pehle koi marta hi nahi tha. Dharti bojh se thak gayi, Brahma ji ke gusse se aag nikli. "
                "Phir unke shareer se ek ladki nikli: Mrityu. Hukm mila: sabki jaan lo. Aur woh ro padi...\n\n"
                "Maut duniya ke liye saza hai ya zaroorat? Comment mein batao 👇",
        yt_title="Maut Khud Roi Thi 😳 | Mrityu Ki Kahani | Mahabharat",
        yt_description="Mahabharat ke Drona Parva mein Narad ji ek kahani sunaate hain: shuru mein duniya mein koi "
                       "marta hi nahi tha. Dharti bojh se thak gayi, Brahma ji ke gusse se aag nikli, Shiv ji ne unhe "
                       "roka. Tab Brahma ji ke shareer se ek ladki nikli, Mrityu. Use hukm mila sabki jaan lene ka, par "
                       "woh ro padi aur arbon saal ek pair par khadi rahi. Brahma ji ne uske aansu apni hatheliyon mein "
                       "bhar liye. Un aansuon ka kya hua?",
        hashtags=["#mahabharat", "#mrityu", "#mythology", "#kahani", "#hindu"],
        pinned_comment="Maut duniya ke liye saza hai, ya zaroorat? 👇",
        sources=_SOURCES),
    "kn": dict(
        title="Mrityu taane attidlu",
        caption="Yochisi: ellaru hedaro Mrityu... avale attidlu 😳\n\n"
                "Mahabharata: modalu yaaru saaytaane iralilla. Bhoomi bhaaradinda sustaadlu, Brahmana kopadinda benki "
                "huttitu. Aamele avana dehadinda ondu hudugi bandlu: Mrityu. Aajne bantu: ellara praana tago. Avalu "
                "attubittlu...\n\nSaavu prapanchakke shikshe na, agatya na? Comment maadi 👇",
        yt_title="Mrityu Taane Attidlu 😳 | Saavina Kathe | Mahabharata",
        yt_description="Mahabharatada Drona Parvadalli Narada ondu kathe heltaare: modalu prapanchadalli yaaru "
                       "saaytaane iralilla. Bhoomi bhaaradinda sustaadlu, Brahmana kopadinda benki huttitu, Shiva "
                       "tadeda. Aaga Brahmana dehadinda ondu hudugi bandlu, Mrityu. Ellara praana tago anta aajne "
                       "bantu, aadre avalu attu, nooraaru koti varsha ondu kaalalli nintlu. Brahma avala kanneerannu "
                       "tanna angaiyalli hidkonda. Aa kanneeru enaaytu?",
        hashtags=["#kannada", "#mahabharata", "#mrityu", "#kannadastory", "#mythology"],
        pinned_comment="Saavu prapanchakke shikshe na, agatya na? 👇",
        sources=_SOURCES),
}


USED_ASSETS, CREDITS_FILES = [], []      # everything in this video is drawn in code


def _scenes(tl):
    """Hindi: shadow puppets (scenes_mrityu); Kannada: Yakshagana stage (scenes_mrityu_yk), so the two channels never
    share pictures."""
    import importlib
    yk = getattr(tl, "lang", "hi") == "kn"
    return importlib.import_module("scenes_mrityu_yk" if yk else "scenes_mrityu")


def draw(cr, t, tl):
    _scenes(tl).draw(cr, t, tl)


def sfx(tl):
    return _scenes(tl).sfx(tl)
