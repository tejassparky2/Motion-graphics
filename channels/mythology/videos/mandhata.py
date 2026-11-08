"""Mythology video 8: the king who got pregnant: Yuvanashva and the birth of Mandhata (owner, 8 Nov 2026: "make new
video now not only Ramayana any works should be interesting mind blowing shocking like jarasanda one"; script
"Auto approved"). One simple story, one step per sentence. Look: the Togalu Gombeyaata shadow puppets; the birth is
a burst of light from the king's side, never gory. Calm sound (render_myth.calm_sfx).

Facts:
- Bhagavata Purana 9.6.25-37 (vedabase): Yuvanashva "had no sons ... went to the forest" (25); the sages perform an
  Indra-yajna so that he "might have a son" (26); one night, thirsty, he "drank the sanctified water meant to be
  drunk by his wife" (27); the brahmanas accept it as providence (28-29); the son "came forth from the lower right
  side of King Yuvanashva's abdomen" (30); the baby cries for milk; Indra "put his index finger in the baby's mouth
  and said, 'You may drink me'" (31); the king "did not fall a victim to death" (32); Mandhata becomes emperor, his
  rule reaching wherever the sun rises and sets (33-37).
- Mahabharata, Vana Parva 126 (Ganguli): the son "pierced the left side of the king, and the king did not die";
  Indra introduces his forefinger; "Me he shall suck" gives the name Mandhata. Another passage of the Mahabharata
  (Ganguli's section LXII in the Drona Parva numbering) says the twin Ashvins "brought him out of his father's womb
  by a surgical operation": the reel says "in one part of the Mahabharata" and does not name a side.
"""
from channel import ASSETS_ROOT, MUSIC, NARRATORS, NARRATOR_LABEL, REVEAL_GAP, TAIL  # noqa: F401

SCRIPTS = {
    "hi": [
        dict(id="m1", text="सोचो, एक राजा गर्भवती हो गया... और उसके पेट से एक बेटा पैदा हुआ।", gap=REVEAL_GAP),
        dict(id="m2", text="ये कोई मज़ाक नहीं है। ये भागवत पुराण और महाभारत, दोनों में लिखा है।"),
        dict(id="m3", text="राजा युवनाश्व का कोई बेटा नहीं था। दुखी होकर वो जंगल चले गए।"),
        dict(id="m4", text="वहाँ ऋषियों ने उनके लिए एक यज्ञ किया, ताकि उन्हें बेटा हो।"),
        dict(id="m5", text="यज्ञ का पवित्र जल एक घड़े में रखा गया। ये जल रानी को पीना था।"),
        dict(id="m6", text="पर रात को राजा को बहुत प्यास लगी। ऋषि सो रहे थे।"),
        dict(id="m7", text="राजा ने वही जल पी लिया।", gap=REVEAL_GAP),
        dict(id="m8", text="सुबह ऋषियों ने देखा, घड़ा ख़ाली है। अब कुछ नहीं हो सकता था।"),
        dict(id="m9", text="और फिर... राजा के पेट में बच्चा पलने लगा।", gap=REVEAL_GAP),
        dict(id="m10", text="समय आने पर, बच्चा राजा के पेट की एक तरफ़ को चीरकर बाहर आया। और राजा ज़िंदा बच गए।"),
        dict(id="m11", text="महाभारत के एक हिस्से में तो लिखा है, देवताओं के वैद्य, अश्विनी कुमारों ने ऑपरेशन करके बच्चा "
                            "निकाला।"),
        dict(id="m12", text="अब नई मुश्किल: बच्चा भूख से रो रहा था। उसे दूध कौन पिलाएगा?", gap=REVEAL_GAP),
        dict(id="m13", text="तब इंद्र देव आए। उन्होंने अपनी उंगली बच्चे के मुँह में दी, और कहा: ये मुझे पिएगा।"),
        dict(id="m14", text="इसी से बच्चे का नाम पड़ा: मांधाता।"),
        dict(id="m15", text="बड़ा होकर मांधाता ऐसा राजा बना, जिसका राज वहाँ तक था, जहाँ से सूरज उगता है, और जहाँ डूबता है।",
             gap=REVEAL_GAP),
        dict(id="m16", text="क्या तुमने ये कहानी पहले सुनी थी? यस या नो, कमेंट में बताओ।"),
    ],
    "kn": [
        dict(id="m1", text="ಯೋಚಿಸಿ... ಒಬ್ಬ ರಾಜ ಗರ್ಭಿಣಿ ಆದ... ಅವನ ಹೊಟ್ಟೆಯಿಂದ ಒಬ್ಬ ಮಗ ಹುಟ್ಟಿದ.", gap=REVEAL_GAP),
        dict(id="m2", text="ಇದು ತಮಾಷೆ ಅಲ್ಲ. ಭಾಗವತ ಪುರಾಣ, ಮಹಾಭಾರತ, ಎರಡರಲ್ಲೂ ಇದೆ."),
        dict(id="m3", text="ರಾಜ ಯುವನಾಶ್ವನಿಗೆ ಮಕ್ಕಳಿರಲಿಲ್ಲ. ದುಃಖದಲ್ಲಿ ಅವನು ಕಾಡಿಗೆ ಹೋದ."),
        dict(id="m4", text="ಅಲ್ಲಿ ಋಷಿಗಳು ಅವನಿಗೆ ಮಗ ಹುಟ್ಟಲಿ ಅಂತ ಒಂದು ಯಜ್ಞ ಮಾಡಿದ್ರು."),
        dict(id="m5", text="ಯಜ್ಞದ ಪವಿತ್ರ ನೀರನ್ನ ಒಂದು ಕೊಡದಲ್ಲಿ ಇಟ್ರು. ಅದನ್ನ ರಾಣಿ ಕುಡಿಯಬೇಕಿತ್ತು."),
        dict(id="m6", text="ಆದ್ರೆ ರಾತ್ರಿ ರಾಜನಿಗೆ ತುಂಬಾ ಬಾಯಾರಿಕೆ ಆಯ್ತು. ಋಷಿಗಳು ಮಲಗಿದ್ರು."),
        dict(id="m7", text="ರಾಜ ಆ ನೀರನ್ನೇ ಕುಡಿದುಬಿಟ್ಟ.", gap=REVEAL_GAP),
        dict(id="m8", text="ಬೆಳಿಗ್ಗೆ ಋಷಿಗಳು ನೋಡಿದ್ರೆ, ಕೊಡ ಖಾಲಿ. ಈಗ ಏನೂ ಮಾಡೋಕಾಗಲ್ಲ."),
        dict(id="m9", text="ಆಮೇಲೆ... ರಾಜನ ಹೊಟ್ಟೆಯಲ್ಲಿ ಮಗು ಬೆಳೆಯೋಕೆ ಶುರುವಾಯ್ತು.", gap=REVEAL_GAP),
        dict(id="m10", text="ಸಮಯ ಬಂದಾಗ, ಮಗು ರಾಜನ ಹೊಟ್ಟೆಯ ಒಂದು ಬದಿ ಸೀಳಿಕೊಂಡು ಹೊರಗೆ ಬಂತು. ರಾಜ ಬದುಕುಳಿದ."),
        dict(id="m11", text="ಮಹಾಭಾರತದ ಒಂದು ಕಡೆ ಅಂತೂ, ದೇವತೆಗಳ ವೈದ್ಯರು, ಅಶ್ವಿನೀ ಕುಮಾರರು, ಆಪರೇಷನ್ ಮಾಡಿ ಮಗುವನ್ನ ಹೊರಗೆ "
                            "ತೆಗೆದ್ರು ಅಂತಿದೆ."),
        dict(id="m12", text="ಈಗ ಇನ್ನೊಂದು ಸಮಸ್ಯೆ: ಮಗು ಹಸಿವಿಂದ ಅಳ್ತಿತ್ತು. ಹಾಲು ಯಾರು ಕುಡಿಸ್ತಾರೆ?", gap=REVEAL_GAP),
        dict(id="m13", text="ಆಗ ಇಂದ್ರ ಬಂದ. ತನ್ನ ಬೆರಳನ್ನ ಮಗುವಿನ ಬಾಯಿಗೆ ಇಟ್ಟು ಹೇಳಿದ: ಇವನು ನನ್ನನ್ನ ಕುಡೀತಾನೆ."),
        dict(id="m14", text="ಅದರಿಂದಲೇ ಮಗುವಿಗೆ ಹೆಸರು ಬಂತು: ಮಾಂಧಾತ."),
        dict(id="m15", text="ದೊಡ್ಡವನಾದ ಮೇಲೆ ಮಾಂಧಾತ, ಸೂರ್ಯ ಹುಟ್ಟೋ ಕಡೆಯಿಂದ ಮುಳುಗೋ ಕಡೆವರೆಗೂ ಆಳಿದ ಚಕ್ರವರ್ತಿ ಆದ.",
             gap=REVEAL_GAP),
        dict(id="m16", text="ಈ ಕಥೆ ನಿಮಗೆ ಗೊತ್ತಿತ್ತಾ? ಹೌದಾ ಇಲ್ವಾ, ಕಾಮೆಂಟ್ ಮಾಡಿ ಹೇಳಿ."),
    ],
}

_SOURCES = ["Bhagavata Purana 9.6.25-37", "Mahabharata, Vana Parva 126 (K. M. Ganguli translation)"]
METADATA = {
    "hi": dict(
        title="Ek raja jo garbhvati ho gaya",
        caption="Socho, ek raja garbhvati ho gaya... aur uske pet se ek beta paida hua 😳\n\n"
                "Bhagavata Purana aur Mahabharat: Raja Yuvanashva ne raat ko woh pavitra jal pee liya jo rani ke liye "
                "tha. Bachcha raja ke pet ki ek taraf se bahar aaya, aur Indra ne use apni ungli se doodh pilaya. Wahi "
                "bachcha bana chakravarti Mandhata.\n\n"
                "Kya tumne ye kahani pehle suni thi? YES ya NO, comment mein batao 👇",
        yt_title="Ek Raja Jo Garbhvati Ho Gaya 😳 | Mandhata Ki Kahani | Bhagavata Purana",
        yt_description="Raja Yuvanashva ka koi beta nahi tha. Rishiyon ne yagya kiya, aur rani ke liye pavitra jal "
                       "rakha. Raat ko pyaase raja ne wahi jal pee liya, aur unke pet mein bachcha palne laga. Bachcha "
                       "raja ke pet ki ek taraf se bahar aaya, raja zinda bache, aur Indra ne bachche ko apni ungli "
                       "chusaayi: 'ye mujhe piyega'. Isi se naam pada Mandhata.",
        hashtags=["#mythology", "#bhagavatapurana", "#mahabharat", "#mandhata", "#kahani"],
        pinned_comment="Kya tumne ye kahani pehle suni thi? YES ya NO? 👇",
        sources=_SOURCES),
    "kn": dict(
        title="Garbhini aada raja",
        caption="Yochisi: obba raja garbhini aada... avana hotteyinda obba maga huttida 😳\n\n"
                "Bhagavata Purana mattu Mahabharata: Raja Yuvanashva raatri raaniyige itta pavitra neerannu "
                "kudidubitta. Magu rajana hotteya ondu badiyinda horage bantu, Indra tanna beralinda haalu "
                "kudisida. Aa magune chakravarti Mandhata.\n\n"
                "Ee kathe nimge gottittaa? Houda illva, comment maadi 👇",
        yt_title="Garbhini Aada Raja 😳 | Mandhatana Kathe | Bhagavata Purana",
        yt_description="Raja Yuvanashvanige makkalirlilla. Rishigalu yajna maadi, raaniyige pavitra neeru ittru. "
                       "Raatri baayaarike aada raja aa neerannu kudida, avana hotteyalli magu beleyitu. Magu rajana "
                       "hotteya ondu badiyinda horage bantu, raja badukulida, Indra tanna beralannu magu baayige "
                       "ittu 'ivanu nannannu kudeetaane' anda. Adarinda hesaru Mandhata.",
        hashtags=["#kannada", "#mythology", "#bhagavatapurana", "#kannadastory", "#mandhata"],
        pinned_comment="Ee kathe nimge gottittaa? Houda illva? 👇",
        sources=_SOURCES),
}

USED_ASSETS, CREDITS_FILES = [], []      # everything in this video is drawn in code


def draw(cr, t, tl):
    from scenes_mandhata import draw as _draw
    _draw(cr, t, tl)


def sfx(tl):
    from scenes_mandhata import sfx as _sfx
    return _sfx(tl)
