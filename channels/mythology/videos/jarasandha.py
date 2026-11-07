"""Mythology video 3: Jarasandha, born as two halves of one child, joined by the rakshasi Jara.
Approach C: Karnataka's leather shadow-puppet theatre look (Togalu Gombeyaata): translucent, coloured, punched-leather
puppets on rods behind a lamp-lit cloth screen, all drawn in code. Hook style: a staccato list of impossible images
("one eye. one hand. one leg. half a face.") before any context (owner, 6 Nov 2026: three videos, each with a
different approach, hook and animation).

Facts (Mahabharata, Sabha Parva, K. M. Ganguli translation 1883-96): King Vrihadratha of Magadha married the twin
daughters of the king of Kasi (XVII); the sage Chanda-kausika gave him a mango; each queen ate half and bore half a
child: "each fragment had one eye, one arm, one leg, half a stomach, half a face"; the fragments were abandoned; the
Rakshasa woman Jara "united the fragments for facility of carrying them away", and the child "began to roar terribly
as rain-charged clouds"; he was named after Jara (Jarasandha). "He hath already brought eighty-six kings; fourteen
only are wanting to complete one hundred" (XV), to sacrifice to "the lord of Uma" (XIV). Krishna, Bhima and Arjuna
came as Snataka Brahmanas; Jarasandha chose Bhima; they fought from the first lunar day of Kartika "without
intermission and food, day and night, till the thirteenth lunar day"; on the fourteenth night Jarasandha stopped
from fatigue (XXIII). Bhima whirled him about a hundred times, "pressed his knee against Jarasandha's backbone and
broke his body in twain"; Krishna freed the imprisoned kings (XXIV). The later folk detail of Krishna splitting a
twig as a hint is not used: it is not in this text.
"""
from channel import ASSETS_ROOT, MUSIC, NARRATORS, NARRATOR_LABEL, REVEAL_GAP, TAIL  # noqa: F401

SCRIPTS = {
    "hi": [
        dict(id="j1", text="एक आंख, एक हाथ, एक पैर... और आधा चेहरा।", gap=REVEAL_GAP),
        dict(id="j2", text="ऐसे दो टुकड़े... दो अलग-अलग माँओं से पैदा हुए। और फिर, जुड़कर एक इंसान बन गए।"),
        dict(id="j3", text="ये कोई हॉरर फ़िल्म नहीं है। ये महाभारत के सभा पर्व में लिखा है।"),
        dict(id="j4", text="मगध के राजा बृहद्रथ की दो रानियाँ थीं, पर कोई संतान नहीं थी।"),
        dict(id="j5", text="एक ऋषि ने राजा को एक आम दिया। राजा ने वो आम, दोनों रानियों में आधा-आधा बाँट दिया।"),
        dict(id="j6", text="और दोनों रानियों ने, एक बच्चे का आधा-आधा हिस्सा जन्म दिया।", gap=REVEAL_GAP),
        dict(id="j7", text="डर के मारे, उन टुकड़ों को बाहर फेंक दिया गया।"),
        dict(id="j8", text="तभी जरा नाम की एक राक्षसी वहाँ से गुज़री। उसने दोनों टुकड़ों को उठाने के लिए... उन्हें एक साथ "
                           "मिलाया।"),
        dict(id="j9", text="और टुकड़े जुड़ गए। बच्चा बादलों की गरज जैसी आवाज़ में रोया।", gap=REVEAL_GAP),
        dict(id="j10", text="जरा ने जोड़ा था, इसलिए नाम पड़ा: जरासंध।"),
        dict(id="j11", text="बड़ा होकर उसने छियासी राजाओं को क़ैद कर लिया। वो सौ राजाओं की बलि देना चाहता था।"),
        dict(id="j12", text="तो इसे रोका किसने? और कैसे?", gap=REVEAL_GAP),
        dict(id="j13", text="कृष्ण, अर्जुन और भीम, ब्राह्मणों के भेस में मगध पहुँचे। और जरासंध ने कुश्ती के लिए भीम को चुना।"),
        dict(id="j14", text="कार्तिक महीने के पहले दिन से, तेरह दिन तक, दिन-रात... बिना खाए, बिना रुके।"),
        dict(id="j15", text="चौदहवीं रात, जरासंध थक गया। भीम ने उसे हवा में उठाया, सौ बार घुमाया... और उसका शरीर, दो "
                            "टुकड़ों में तोड़ दिया।", gap=REVEAL_GAP),
        dict(id="j16", text="कृष्ण ने क़ैद के सारे राजाओं को आज़ाद कर दिया।"),
        dict(id="j17", text="जो दो टुकड़ों से जुड़कर पैदा हुआ था... उसका अंत भी, दो टुकड़ों में ही हुआ।", gap=REVEAL_GAP),
        dict(id="j18", text="क्या तुम्हें जरासंध के जन्म की ये कहानी पता थी? यस या नो, कमेंट में बताओ।"),
    ],
    "kn": [
        dict(id="j1", text="ಒಂದು ಕಣ್ಣು. ಒಂದು ಕೈ. ಒಂದು ಕಾಲು. ಅರ್ಧ ಮುಖ.", gap=REVEAL_GAP),
        dict(id="j2", text="ಇಂಥಾ ಎರಡು ತುಂಡು... ಇಬ್ರು ಬೇರೆ ಬೇರೆ ಅಮ್ಮಂದಿರಿಗೆ ಹುಟ್ಟಿದ್ವು. ಆಮೇಲೆ, ಒಟ್ಟಿಗೆ ಸೇರಿ ಒಬ್ಬ "
                           "ಮನುಷ್ಯ ಆದ್ವು."),
        dict(id="j3", text="ಇದು ಯಾವ್ದೋ ಹಾರರ್ ಸಿನಿಮಾ ಅಲ್ಲ. ಮಹಾಭಾರತದ ಸಭಾ ಪರ್ವದಲ್ಲೇ ಇದೆ."),
        dict(id="j4", text="ಮಗಧದ ರಾಜ ಬೃಹದ್ರಥನಿಗೆ ಇಬ್ರು ರಾಣಿಯರು ಇದ್ರು. ಆದ್ರೆ ಮಕ್ಕಳಿರಲಿಲ್ಲ."),
        dict(id="j5", text="ಒಬ್ರು ಋಷಿ ರಾಜನಿಗೆ ಒಂದು ಮಾವಿನಹಣ್ಣು ಕೊಟ್ರು. ರಾಜ ಅದನ್ನ ಇಬ್ರು ರಾಣಿಯರಿಗೂ ಅರ್ಧ ಅರ್ಧ "
                           "ಹಂಚಿಕೊಟ್ಟ."),
        dict(id="j6", text="ಇಬ್ರು ರಾಣಿಯರೂ, ಒಂದು ಮಗುವಿನ ಅರ್ಧ ಅರ್ಧ ಭಾಗಕ್ಕೆ ಜನ್ಮ ಕೊಟ್ರು.", gap=REVEAL_GAP),
        dict(id="j7", text="ಭಯದಲ್ಲಿ, ಆ ತುಂಡುಗಳನ್ನ ಹೊರಗೆ ಬಿಸಾಕಿಬಿಟ್ರು."),
        dict(id="j8", text="ಆಗ ಜರಾ ಅನ್ನೋ ರಾಕ್ಷಸಿ ಅಲ್ಲಿಗೆ ಬಂದ್ಳು. ಎರಡೂ ತುಂಡನ್ನ ಎತ್ಕೊಂಡು ಹೋಗೋಕೆ ಸುಲಭ ಆಗ್ಲಿ ಅಂತ... "
                           "ಒಟ್ಟಿಗೆ ಸೇರಿಸಿದ್ಳು."),
        dict(id="j9", text="ತುಂಡುಗಳು ಒಂದಾಗ್ಬಿಟ್ವು. ಮಗು ಗುಡುಗಿನ ತರ ಜೋರಾಗಿ ಅಳೋಕೆ ಶುರು ಮಾಡ್ತು.", gap=REVEAL_GAP),
        dict(id="j10", text="ಜರಾ ಜೋಡಿಸಿದ್ದಕ್ಕೆ, ಹೆಸರು ಬಂತು: ಜರಾಸಂಧ."),
        dict(id="j11", text="ದೊಡ್ಡೋನಾದ ಮೇಲೆ, ಅವನು ಎಂಬತ್ತಾರು ರಾಜರನ್ನ ಜೈಲಲ್ಲಿ ಹಾಕಿದ. ನೂರು ರಾಜರನ್ನ ಬಲಿ ಕೊಡ್ಬೇಕು "
                            "ಅನ್ನೋದು ಅವನ ಗುರಿ."),
        dict(id="j12", text="ಹಾಗಾದ್ರೆ ಇವನನ್ನ ತಡೆದಿದ್ದು ಯಾರು? ಹೇಗೆ?", gap=REVEAL_GAP),
        dict(id="j13", text="ಕೃಷ್ಣ, ಅರ್ಜುನ, ಭೀಮ, ಬ್ರಾಹ್ಮಣರ ವೇಷದಲ್ಲಿ ಮಗಧಕ್ಕೆ ಬಂದ್ರು. ಜರಾಸಂಧ ಕುಸ್ತಿಗೆ ಭೀಮನನ್ನೇ "
                            "ಆರಿಸಿಕೊಂಡ."),
        dict(id="j14", text="ಕಾರ್ತಿಕ ಮಾಸದ ಮೊದಲ ದಿನದಿಂದ, ಹದಿಮೂರು ದಿನ, ಹಗಲು ರಾತ್ರಿ... ಊಟ ಇಲ್ಲ, ವಿಶ್ರಾಂತಿ ಇಲ್ಲ."),
        dict(id="j15", text="ಹದಿನಾಲ್ಕನೇ ರಾತ್ರಿ, ಜರಾಸಂಧ ಸುಸ್ತಾದ. ಭೀಮ ಅವನನ್ನ ಮೇಲೆ ಎತ್ತಿ, ನೂರು ಸಲ ತಿರುಗಿಸಿ... ಅವನ "
                            "ದೇಹವನ್ನ ಎರಡು ತುಂಡು ಮಾಡಿದ.", gap=REVEAL_GAP),
        dict(id="j16", text="ಕೃಷ್ಣ ಜೈಲಲ್ಲಿದ್ದ ಎಲ್ಲಾ ರಾಜರನ್ನೂ ಬಿಡುಗಡೆ ಮಾಡಿದ."),
        dict(id="j17", text="ಎರಡು ತುಂಡು ಸೇರಿ ಹುಟ್ಟಿದವನು... ಕೊನೆಗೆ ಎರಡು ತುಂಡಾಗಿಯೇ ಮುಗಿದ.", gap=REVEAL_GAP),
        dict(id="j18", text="ಜರಾಸಂಧನ ಹುಟ್ಟಿನ ಈ ಕಥೆ ನಿಮಗೆ ಗೊತ್ತಿತ್ತಾ? ಹೌದಾ ಇಲ್ವಾ, ಕಾಮೆಂಟ್ ಮಾಡಿ ಹೇಳಿ."),
    ],
}

_SOURCES = ["Mahabharata, Sabha Parva (K. M. Ganguli translation)"]
METADATA = {
    "hi": dict(
        title="Do maaon se paida hua ek bachcha: Jarasandh",
        caption="Ek aankh. Ek haath. Ek pair. Aadha chehra. 😳\n\n"
                "Mahabharat, Sabha Parva: Raja Brihadrath ki do raniyon ne ek bachche ka aadha-aadha hissa janma diya. "
                "Jara naam ki rakshasi ne dono tukde jode, aur naam pada Jarasandh. Ant mein Bhim ne use do tukdon mein "
                "tod diya.\n\nKya tumhe ye kahani pata thi? YES ya NO, comment mein batao 👇",
        yt_title="Do Maaon Se Paida Hua Ek Bachcha 😳 | Jarasandh Ki Kahani | Mahabharat",
        yt_description="Magadh ke raja Brihadrath ki do raniyon ne ek bachche ke do aadhe hisse janme. Rakshasi Jara ne "
                       "unhe joda, isliye naam pada Jarasandh. Usne 86 rajaon ko qaid kiya; Bhim ke saath 13 din, din-raat "
                       "kushti hui, aur jo do tukdon se juda tha, wo do tukdon mein hi khatam hua.",
        hashtags=["#mahabharat", "#jarasandh", "#bhim", "#mythology", "#kahani"],
        pinned_comment="Kya tumhe Jarasandh ke janm ki ye kahani pata thi? YES ya NO? 👇",
        sources=_SOURCES),
    "kn": dict(
        title="Ibbaru ammandirige huttida ondu magu: Jarasandha",
        caption="Ondu kannu. Ondu kai. Ondu kaalu. Ardha mukha. 😳\n\nMahabharata, Sabha Parva: Raja Brihadrathana "
                "ibbaru raniyaru ondu maguvina ardha ardha bhaagakke janma kottru. Jara anno rakshasi eradannu "
                "serisidlu, hesaru Jarasandha. Konege Bheema avanannu eradu tundu maadida.\n\nEe kathe nimge "
                "gottittaa? Houda illva, comment maadi 👇",
        yt_title="Ibbaru Ammandirige Huttida Ondu Magu 😳 | Jarasandhana Kathe | Mahabharata",
        yt_description="Magadhada raja Brihadrathana ibbaru raniyaru ondu maguvina eradu ardha bhaagagalige janma kottru. "
                       "Rakshasi Jara avannu serisidlu, adakke hesaru Jarasandha. Avanu 86 rajarannu jailalli haakida; "
                       "Bheemana jothe 13 dina hagalu raatri kusti nadeetu. Eradu tundu seri huttidavanu, eradu tundaagiye "
                       "mugida.",
        hashtags=["#kannada", "#mahabharata", "#jarasandha", "#kannadastory", "#mythology"],
        pinned_comment="Jarasandhana huttina ee kathe nimge gottittaa? Houda illva? 👇",
        sources=_SOURCES),
}

USED_ASSETS, CREDITS_FILES = [], []      # everything in this video is drawn in code


def draw(cr, t, tl):
    from scenes_jarasandha import draw as _draw
    _draw(cr, t, tl)


def sfx(tl):
    from scenes_jarasandha import sfx as _sfx
    return _sfx(tl)
