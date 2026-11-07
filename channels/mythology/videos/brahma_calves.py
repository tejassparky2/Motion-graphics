"""Mythology video 2: Brahma hides Krishna's friends and calves; Krishna becomes every boy and calf for a year.
Approach B: a "living manuscript": CC0 Indian miniature paintings (Cleveland Museum of Art) cut into layers and moved
as a multiplane camera with drawn light, petals and dust. Hook style: a character's impossible question, Brahma's own
("I hid these children myself... so how are they playing here?"), then the narrator (owner, 6 Nov 2026: three
videos, each with a different approach, hook and animation).

Facts: Bhagavata Purana 10.13: lunch on the river bank (13.4-10); the calves wander deep into the forest after grass
(13.12); Brahma takes the calves and boys "to another place" (13.15) and keeps them asleep (13.41; the text does not
say "cave", though a museum painting's title does); Krishna expands into the exact boys and calves, "with their exact
bodily features", sticks, flutes, dress, ages and activities (13.19); the mothers' affection keeps increasing (13.22-
26); this goes on for a year, the herd returning "five or six nights before the completion of the year" (13.27-28);
Balarama notices (13.35-39); Brahma returns after a moment by his own measure while a year has passed for humans
(13.40); all the boys and calves appear four-armed, holding conch, disc, mace and lotus (13.46-48); Brahma falls at
Krishna's feet (13.62). 10.14.43-45: the boys, released, think only a moment has passed: "You have come back so
quickly! We have not eaten a single morsel."
"""
from channel import ASSETS_ROOT, MUSIC, NARRATORS, NARRATOR_LABEL, REVEAL_GAP, TAIL  # noqa: F401

SCRIPTS = {
    "hi": [
        dict(id="c1", text="मैंने इन बच्चों को अपने हाथों से छुपाया था... फिर ये यहाँ खेल कैसे रहे हैं?", gap=REVEAL_GAP),
        dict(id="c2", text="ये सवाल, ख़ुद ब्रह्मा जी के मन में उठा था। और इसका जवाब... एक साल पुराना था।"),
        dict(id="c3", text="भागवत पुराण, दसवाँ स्कंध। वृंदावन में, कृष्ण अपने दोस्तों के साथ नदी किनारे खाना खा रहे थे।"),
        dict(id="c4", text="बछड़े घास चरते-चरते, जंगल में दूर निकल गए। कृष्ण उन्हें ढूँढने चले गए।"),
        dict(id="c5", text="बस इसी मौक़े पर, ब्रह्मा जी ने सारे बछड़े, और सारे ग्वाल-बाल... छुपा दिए।"),
        dict(id="c6", text="वो देखना चाहते थे, कि अब कृष्ण क्या करेंगे।", gap=REVEAL_GAP),
        dict(id="c7", text="और कृष्ण ने वो किया, जो कोई सोच भी नहीं सकता। वो ख़ुद, हर एक बच्चा बन गए। और हर एक बछड़ा भी।"),
        dict(id="c8", text="वही शक्ल, वही कपड़े, वही बांसुरी, वही आदतें। कोई फ़र्क़ नहीं।"),
        dict(id="c9", text="शाम को सब घर लौटे। माँओं ने अपने बेटों को गले लगाया... और इस बार, प्यार कुछ ज़्यादा ही उमड़ "
                           "रहा था।"),
        dict(id="c10", text="ऐसे ही, पूरा एक साल बीत गया। और किसी को कुछ पता नहीं चला।"),
        dict(id="c11", text="पर ब्रह्मा जी के लिए? उनके लिए तो... बस एक पल बीता था।", gap=REVEAL_GAP),
        dict(id="c12", text="वो लौटे, तो देखा: बच्चे उनके पास भी सो रहे थे... और कृष्ण के साथ भी खेल रहे थे।"),
        dict(id="c13", text="फिर अचानक, हर बच्चा, हर बछड़ा... चार हाथों वाले विष्णु के रूप में दिखने लगा।"),
        dict(id="c14", text="ब्रह्मा जी कृष्ण के चरणों में गिर पड़े।", gap=REVEAL_GAP),
        dict(id="c15", text="और जब बच्चे जागे, तो बोले: कृष्ण, तुम इतनी जल्दी आ गए? हमने तो अभी एक निवाला भी नहीं खाया!"),
        dict(id="c16", text="पूरा गाँव एक साल तक, भगवान को अपने घर में खिलाता रहा... और किसी को पता तक नहीं चला।",
             gap=REVEAL_GAP),
        dict(id="c17", text="अगर तुम उस गाँव में होते, तो क्या पहचान पाते? यस या नो, कमेंट में बताओ।"),
    ],
    "kn": [
        dict(id="c1", text="ಈ ಮಕ್ಕಳನ್ನ ನಾನೇ ನನ್ ಕೈಯಾರೆ ಬಚ್ಚಿಟ್ಟಿದ್ದೆ... ಮತ್ತೆ ಇವ್ರು ಇಲ್ಲಿ ಹೇಗೆ ಆಟ ಆಡ್ತಿದ್ದಾರೆ?",
             gap=REVEAL_GAP),
        dict(id="c2", text="ಈ ಪ್ರಶ್ನೆ ಬಂದಿದ್ದು, ಸ್ವತಃ ಬ್ರಹ್ಮದೇವರ ಮನಸ್ಸಲ್ಲಿ. ಅದರ ಉತ್ತರ... ಒಂದು ವರ್ಷ ಹಳೆಯದು."),
        dict(id="c3", text="ಭಾಗವತ ಪುರಾಣ, ಹತ್ತನೇ ಸ್ಕಂಧ. ವೃಂದಾವನದಲ್ಲಿ, ಕೃಷ್ಣ ತನ್ನ ಸ್ನೇಹಿತರ ಜೊತೆ ನದಿ ದಡದಲ್ಲಿ ಕೂತು "
                           "ಊಟ ಮಾಡ್ತಿದ್ದ."),
        dict(id="c4", text="ಕರುಗಳು ಹುಲ್ಲು ಮೇಯ್ತಾ ಮೇಯ್ತಾ, ಕಾಡಿನೊಳಗೆ ದೂರ ಹೋಗ್ಬಿಟ್ವು. ಕೃಷ್ಣ ಅವನ್ನ ಹುಡುಕೋಕೆ ಹೋದ."),
        dict(id="c5", text="ಅದೇ ಸಮಯದಲ್ಲಿ, ಬ್ರಹ್ಮದೇವರು ಎಲ್ಲಾ ಕರುಗಳನ್ನೂ, ಎಲ್ಲಾ ಗೋಪಾಲಕ ಹುಡುಗರನ್ನೂ... ಬಚ್ಚಿಟ್ಟುಬಿಟ್ರು."),
        dict(id="c6", text="ಈಗ ಕೃಷ್ಣ ಏನ್ ಮಾಡ್ತಾನೆ ಅಂತ, ಅವರಿಗೆ ನೋಡ್ಬೇಕಿತ್ತು.", gap=REVEAL_GAP),
        dict(id="c7", text="ಆಗ ಕೃಷ್ಣ, ಯಾರೂ ಊಹಿಸೋಕೂ ಆಗದ್ದನ್ನ ಮಾಡಿದ. ಅವನೇ ಪ್ರತಿಯೊಬ್ಬ ಹುಡುಗನಾದ. ಪ್ರತಿಯೊಂದು ಕರುವೂ ಆದ."),
        dict(id="c8", text="ಅದೇ ಮುಖ, ಅದೇ ಬಟ್ಟೆ, ಅದೇ ಕೊಳಲು, ಅದೇ ಅಭ್ಯಾಸ. ಸ್ವಲ್ಪನೂ ವ್ಯತ್ಯಾಸ ಇಲ್ಲ."),
        dict(id="c9", text="ಸಂಜೆ ಎಲ್ಲರೂ ಮನೆಗೆ ಬಂದ್ರು. ಅಮ್ಮಂದಿರು ಮಕ್ಕಳನ್ನ ತಬ್ಕೊಂಡ್ರು... ಆದ್ರೆ ಈ ಸಲ, ಪ್ರೀತಿ ಯಾಕೋ "
                           "ಸಿಕ್ಕಾಪಟ್ಟೆ ಜಾಸ್ತಿ ಆಗಿತ್ತು."),
        dict(id="c10", text="ಹೀಗೇ, ಒಂದು ಇಡೀ ವರ್ಷ ಕಳೀತು. ಯಾರಿಗೂ ಏನೂ ಗೊತ್ತಾಗ್ಲಿಲ್ಲ."),
        dict(id="c11", text="ಆದ್ರೆ ಬ್ರಹ್ಮದೇವರಿಗೆ? ಅವರಿಗೆ ಕಳೆದಿದ್ದು... ಬರೀ ಒಂದು ಕ್ಷಣ.", gap=REVEAL_GAP),
        dict(id="c12", text="ಅವರು ವಾಪಸ್ ಬಂದು ನೋಡಿದ್ರೆ: ಮಕ್ಕಳು ಅವರ ಹತ್ರಾನೂ ಮಲಗಿದ್ದಾರೆ... ಕೃಷ್ಣನ ಜೊತೆನೂ "
                            "ಆಡ್ತಿದ್ದಾರೆ."),
        dict(id="c13", text="ಆಮೇಲೆ ಇದ್ದಕ್ಕಿದ್ದಂತೆ, ಪ್ರತಿ ಹುಡುಗ, ಪ್ರತಿ ಕರು... ನಾಲ್ಕು ಕೈಗಳ ವಿಷ್ಣುವಿನ ರೂಪದಲ್ಲಿ "
                            "ಕಾಣಿಸಿದ್ರು."),
        dict(id="c14", text="ಬ್ರಹ್ಮದೇವರು ಕೃಷ್ಣನ ಕಾಲಿಗೆ ಬಿದ್ರು.", gap=REVEAL_GAP),
        dict(id="c15", text="ಮಕ್ಕಳು ಎದ್ದಾಗ ಹೇಳಿದ್ರು: ಕೃಷ್ಣ, ಇಷ್ಟು ಬೇಗ ಬಂದ್ಬಿಟ್ಯಾ? ನಾವಿನ್ನೂ ಒಂದು ತುತ್ತೂ ತಿಂದಿಲ್ಲ!"),
        dict(id="c16", text="ಇಡೀ ಊರು ಒಂದು ವರ್ಷ, ದೇವರಿಗೇ ಮನೇಲಿ ಊಟ ಹಾಕ್ತಿತ್ತು... ಆದ್ರೆ ಯಾರಿಗೂ ಗೊತ್ತೇ ಆಗ್ಲಿಲ್ಲ.",
             gap=REVEAL_GAP),
        dict(id="c17", text="ನೀವು ಆ ಊರಲ್ಲಿ ಇದ್ದಿದ್ರೆ, ಕಂಡುಹಿಡೀತಿದ್ರಾ? ಹೌದಾ ಇಲ್ವಾ, ಕಾಮೆಂಟ್ ಮಾಡಿ ಹೇಳಿ."),
    ],
}

_SOURCES = ["Bhagavata Purana 10.13-10.14"]
METADATA = {
    "hi": dict(
        title="Ek saal tak har ghar mein Krishna the",
        caption="\"Maine in bachchon ko apne haathon se chhupaya tha... phir ye yahan khel kaise rahe hain?\" 😳\n\n"
                "Bhagavata Purana: Brahma ji ne gwal-baal aur bachhde chhupa diye. Krishna khud har bachcha aur har "
                "bachhda ban gaye, poore ek saal tak. Kisi maa ko pata nahi chala.\n\n"
                "Tum us gaanv mein hote toh pehchaan paate? YES ya NO, comment mein batao 👇",
        yt_title="Ek Saal Tak Har Ghar Mein Krishna The 😳 | Bhagavata Purana",
        yt_description="Brahma ji ne Krishna ke dost aur bachhde chhupa diye. Krishna khud har bachcha aur har bachhda ban "
                       "gaye: wahi shakal, wahi kapde, wahi bansuri. Poore ek saal kisi ko pata nahi chala. Brahma ji ke "
                       "liye bas ek pal beeta tha. Paintings: Cleveland Museum of Art (CC0).",
        hashtags=["#krishna", "#bhagavatapurana", "#mythology", "#vrindavan", "#kahani"],
        pinned_comment="Agar tum us gaanv mein hote, toh kya pehchaan paate? YES ya NO? 👇",
        sources=_SOURCES),
    "kn": dict(
        title="ಒಂದು ವರ್ಷ ಪ್ರತಿ ಮನೇಲಿ ಕೃಷ್ಣನೇ ಇದ್ದ",
        caption="\"ಈ ಮಕ್ಕಳನ್ನ ನಾನೇ ಬಚ್ಚಿಟ್ಟಿದ್ದೆ... ಮತ್ತೆ ಇವ್ರು ಇಲ್ಲಿ ಹೇಗೆ ಆಡ್ತಿದ್ದಾರೆ?\" 😳\n\n"
                "ಭಾಗವತ ಪುರಾಣ: ಬ್ರಹ್ಮದೇವರು ಗೋಪಾಲಕರನ್ನೂ ಕರುಗಳನ್ನೂ ಬಚ್ಚಿಟ್ರು. ಕೃಷ್ಣನೇ ಪ್ರತಿ ಹುಡುಗ, ಪ್ರತಿ ಕರು "
                "ಆದ, ಒಂದು ಇಡೀ ವರ್ಷ. ಯಾವ ಅಮ್ಮನಿಗೂ ಗೊತ್ತಾಗ್ಲಿಲ್ಲ.\n\n"
                "ನೀವು ಕಂಡುಹಿಡೀತಿದ್ರಾ? ಹೌದಾ ಇಲ್ವಾ, ಕಾಮೆಂಟ್ ಮಾಡಿ 👇",
        yt_title="ಒಂದು ವರ್ಷ ಪ್ರತಿ ಮನೇಲಿ ಕೃಷ್ಣನೇ ಇದ್ದ 😳 | ಭಾಗವತ ಪುರಾಣ",
        yt_description="ಬ್ರಹ್ಮದೇವರು ಕೃಷ್ಣನ ಸ್ನೇಹಿತರನ್ನ ಮತ್ತು ಕರುಗಳನ್ನ ಬಚ್ಚಿಟ್ರು. ಕೃಷ್ಣನೇ ಪ್ರತಿ ಹುಡುಗ, ಪ್ರತಿ ಕರು ಆದ: "
                       "ಅದೇ ಮುಖ, ಅದೇ ಬಟ್ಟೆ, ಅದೇ ಕೊಳಲು. ಒಂದು ಇಡೀ ವರ್ಷ ಯಾರಿಗೂ ಗೊತ್ತಾಗ್ಲಿಲ್ಲ. ಬ್ರಹ್ಮದೇವರಿಗೆ ಕಳೆದಿದ್ದು "
                       "ಒಂದೇ ಕ್ಷಣ. Paintings: Cleveland Museum of Art (CC0).",
        hashtags=["#kannada", "#krishna", "#bhagavatapurana", "#kannadastory", "#mythology"],
        pinned_comment="ನೀವು ಆ ಊರಲ್ಲಿ ಇದ್ದಿದ್ರೆ, ಕಂಡುಹಿಡೀತಿದ್ರಾ? ಹೌದಾ ಇಲ್ವಾ? 👇",
        sources=_SOURCES),
}


def __getattr__(name):                   # P, USED_ASSETS, CREDITS_FILES come from the scene code
    import scenes_brahma_calves as s
    return getattr(s, name)


def draw(cr, t, tl):
    from scenes_brahma_calves import draw as _draw
    _draw(cr, t, tl)


def sfx(tl):
    from scenes_brahma_calves import sfx as _sfx
    return _sfx(tl)
