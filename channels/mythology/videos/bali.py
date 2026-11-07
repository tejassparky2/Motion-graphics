"""Mythology video 4: King Bali and Vamana. God takes everything from a king... then promises him he will one day be
king of heaven; and, it is believed, the day after Diwali he still comes back to visit his people (Bali Padyami).
Look: the owner's reference reel (7 Nov 2026, "make it like this", the Diwali-series "Lakshmi has an elder sister"):
painted cut-out characters on painted stage sets, two-tier headlines, a top label row with "FIG. n", a torn tag,
torn-paper notes, a checklist card and counters. Characters and sets made on the laptop with SDXL (owner: "You, on the
laptop"), cut out and reused shot to shot.

Facts (Bhagavata Purana, checked 7 Nov 2026 on vedabase):
- 8.19.16: Vamana asks only "three paces of land, to the measurement of My steps"; 8.19.28: Bali grants it.
- 8.19.32-35: Shukracharya warns that the boy is Vishnu, who will take everything and give it to Indra.
- 8.20: Bali keeps his word; Vamana grows; one step covers the earth, the second the heavens (8.20.33-34).
- 5.17.1: "He extended His left foot to the end of the universe and pierced a hole in its covering with the nail of His
  big toe. Through the hole, the pure water of the Causal Ocean entered this universe as the Ganges River."
- 8.22.2: Bali: "place Your third lotus footstep on my head." 8.22.14: bound by the ropes of Varuna.
- 8.22.31: "He will become King of the heavenly planets during the period of the Manu known as Savarni."
- 8.22.33: Sutala, "desired even by the demigods"; 8.22.35: "I shall always be with you and give you protection".
- Not used: Vishnu as Bali's doorkeeper (not in these verses; only in summaries and folk tellings).
- Bali Pratipada / Bali Padyami: the day after Diwali's Amavasya (Kartika Shukla Pratipada); the belief that Bali returns
  to earth for one day a year (Wikipedia, Balipratipada) is a tradition, so the script says "it is believed".
"""
from channel import ASSETS_ROOT, MUSIC, NARRATORS, NARRATOR_LABEL, REVEAL_GAP, TAIL  # noqa: F401

SCRIPTS = {
    "hi": [
        dict(id="v1", text="सोचो, भगवान ने एक राजा से उसका सब कुछ ले लिया... और फिर उससे वादा किया: एक दिन, तुम ही "
                           "स्वर्ग के राजा बनोगे।", gap=REVEAL_GAP),
        dict(id="v2", text="और मान्यता है, दिवाली के अगले दिन, वो राजा आज भी अपनी प्रजा से मिलने धरती पर आता है।"),
        dict(id="v3", text="ये है राजा बलि की कहानी। भागवत पुराण, आठवाँ स्कंध।"),
        dict(id="v4", text="बलि असुरों का राजा था। उसने इंद्र को हराया, और पूरा स्वर्ग जीत लिया।"),
        dict(id="v5", text="तब देवताओं की माँ अदिति ने प्रार्थना की। और भगवान विष्णु, उनके बेटे बनकर आए: एक छोटा सा "
                           "ब्राह्मण बालक, वामन।"),
        dict(id="v6", text="बलि एक बड़ा यज्ञ कर रहा था। वामन वहाँ पहुँचे, और बोले: मुझे बस तीन क़दम ज़मीन चाहिए। मेरे "
                           "अपने क़दमों से नापी हुई।"),
        dict(id="v7", text="बलि मुस्कुराया। बस तीन क़दम? जो चाहिए, ले लो।"),
        dict(id="v8", text="पर गुरु शुक्राचार्य ने रोका: ये बालक नहीं, ख़ुद विष्णु हैं। ये तुम्हारा सब कुछ ले लेंगे।",
             gap=REVEAL_GAP),
        dict(id="v9", text="बलि ने कहा: मैंने वचन दे दिया है। अब पीछे नहीं हटूँगा।"),
        dict(id="v10", text="जैसे ही दान का जल गिरा, वामन बढ़ने लगे। और बढ़ते ही गए।"),
        dict(id="v11", text="पहले क़दम में, पूरी धरती। दूसरे क़दम में, पूरा आकाश, स्वर्ग तक।"),
        dict(id="v12", text="और पैर इतना ऊँचा गया, कि अँगूठे के नाख़ून से ब्रह्मांड का कवच फट गया... और उसी छेद से, "
                            "गंगा अंदर बहने लगीं।", gap=REVEAL_GAP),
        dict(id="v13", text="अब तीसरा क़दम कहाँ रखें? कुछ बचा ही नहीं था।"),
        dict(id="v14", text="बलि ने सिर झुकाया, और कहा: तीसरा क़दम, मेरे सिर पर रखिए।", gap=REVEAL_GAP),
        dict(id="v15", text="और यहीं कहानी पलट गई। भगवान ने बलि को सुतल लोक दिया: ऐसा लोक, जिसे देवता भी चाहते हैं।"),
        dict(id="v16", text="और वादा किया: मैं हमेशा तुम्हारे साथ रहूँगा, और तुम्हारी रक्षा करूँगा।"),
        dict(id="v17", text="और आने वाले युग में, सावर्णि मनु के समय, तुम ही स्वर्ग के राजा बनोगे।", gap=REVEAL_GAP),
        dict(id="v18", text="इसीलिए दिवाली के अगले दिन, बलि प्रतिपदा मनाई जाती है। कर्नाटक में, बलि पाड्यमी। मान्यता है, "
                            "उस दिन बलि अपनी प्रजा से मिलने लौटते हैं।"),
        dict(id="v19", text="जिसने वचन के लिए सब कुछ दे दिया... उसे वो मिला, जो देवताओं को भी नहीं मिलता।",
             gap=REVEAL_GAP),
        dict(id="v20", text="तुम बलि की जगह होते, तो वचन निभाते? यस या नो, कमेंट में बताओ।"),
    ],
    # everyday city Kannada with common English words (owner, 6 Nov 2026)
    "kn": [
        dict(id="v1", text="ಜಸ್ಟ್ ಇಮ್ಯಾಜಿನ್ ಮಾಡಿ... ದೇವರು ಒಬ್ಬ ರಾಜನ ಹತ್ರ ಇದ್ದದ್ದೆಲ್ಲಾ ತಗೊಂಡ್ರು. ಆಮೇಲೆ ಪ್ರಾಮಿಸ್ "
                           "ಮಾಡಿದ್ರು: ಒಂದು ದಿನ, ನೀನೇ ಸ್ವರ್ಗದ ರಾಜ ಆಗ್ತೀಯ.", gap=REVEAL_GAP),
        dict(id="v2", text="ನಂಬಿಕೆ ಪ್ರಕಾರ, ದೀಪಾವಳಿಯ ಮಾರನೇ ದಿನ, ಆ ರಾಜ ಇವತ್ತಿಗೂ ತನ್ನ ಜನರನ್ನ ನೋಡೋಕೆ ಭೂಮಿಗೆ ಬರ್ತಾನೆ."),
        dict(id="v3", text="ಇದು ಬಲಿ ಚಕ್ರವರ್ತಿಯ ಕಥೆ. ಭಾಗವತ ಪುರಾಣ, ಎಂಟನೇ ಸ್ಕಂಧ."),
        dict(id="v4", text="ಬಲಿ ಅಸುರರ ರಾಜ. ಇಂದ್ರನನ್ನ ಸೋಲಿಸಿ, ಇಡೀ ಸ್ವರ್ಗವನ್ನೇ ಗೆದ್ದುಬಿಟ್ಟ."),
        dict(id="v5", text="ಆಗ ದೇವತೆಗಳ ಅಮ್ಮ ಅದಿತಿ ಪ್ರಾರ್ಥನೆ ಮಾಡಿದ್ರು. ವಿಷ್ಣು ಅವರ ಮಗನಾಗಿ ಬಂದ್ರು: ಒಬ್ಬ ಪುಟ್ಟ "
                           "ಬ್ರಾಹ್ಮಣ ಹುಡುಗ, ವಾಮನ."),
        dict(id="v6", text="ಬಲಿ ಒಂದು ದೊಡ್ಡ ಯಜ್ಞ ಮಾಡ್ತಿದ್ದ. ವಾಮನ ಅಲ್ಲಿಗೆ ಬಂದು ಕೇಳಿದ್ರು: ನಂಗೆ ಜಸ್ಟ್ ಮೂರು ಹೆಜ್ಜೆ ಜಾಗ "
                           "ಸಾಕು. ನನ್ನ ಹೆಜ್ಜೆಯಲ್ಲೇ ಅಳತೆ ಮಾಡಿದ್ದು."),
        dict(id="v7", text="ಬಲಿ ನಕ್ಕ. ಬರೀ ಮೂರು ಹೆಜ್ಜೆನಾ? ಏನ್ ಬೇಕೋ ತಗೊಳ್ಳಿ."),
        dict(id="v8", text="ಆದ್ರೆ ಗುರು ಶುಕ್ರಾಚಾರ್ಯರು ತಡೆದ್ರು: ಇವನು ಹುಡುಗ ಅಲ್ಲ, ಸಾಕ್ಷಾತ್ ವಿಷ್ಣು. ನಿನ್ನ ಹತ್ರ ಇರೋದೆಲ್ಲಾ "
                           "ತಗೊಂಡುಬಿಡ್ತಾನೆ.", gap=REVEAL_GAP),
        dict(id="v9", text="ಬಲಿ ಹೇಳಿದ: ನಾನು ಮಾತು ಕೊಟ್ಟಾಗಿದೆ. ಈಗ ಹಿಂದೆ ಸರಿಯಲ್ಲ."),
        dict(id="v10", text="ದಾನದ ನೀರು ಬಿದ್ದ ತಕ್ಷಣ, ವಾಮನ ದೊಡ್ಡವರಾಗ್ತಾ ಹೋದ್ರು. ಇನ್ನೂ ಇನ್ನೂ ದೊಡ್ಡವರಾದ್ರು."),
        dict(id="v11", text="ಮೊದಲ ಹೆಜ್ಜೆಯಲ್ಲಿ, ಇಡೀ ಭೂಮಿ. ಎರಡನೇ ಹೆಜ್ಜೆಯಲ್ಲಿ, ಇಡೀ ಆಕಾಶ, ಸ್ವರ್ಗದವರೆಗೂ."),
        dict(id="v12", text="ಕಾಲು ಎಷ್ಟು ಮೇಲೆ ಹೋಯ್ತು ಅಂದ್ರೆ, ಹೆಬ್ಬೆರಳಿನ ಉಗುರಿನಿಂದ ಬ್ರಹ್ಮಾಂಡದ ಕವಚವೇ ಒಡೆದುಹೋಯ್ತು... ಅದೇ "
                            "ತೂತಿನಿಂದ, ಗಂಗೆ ಒಳಗೆ ಹರಿಯೋಕೆ ಶುರುವಾದಳು.", gap=REVEAL_GAP),
        dict(id="v13", text="ಈಗ ಮೂರನೇ ಹೆಜ್ಜೆ ಎಲ್ಲಿ ಇಡೋದು? ಏನೂ ಉಳಿದೇ ಇರಲಿಲ್ಲ."),
        dict(id="v14", text="ಬಲಿ ತಲೆ ಬಾಗಿಸಿ ಹೇಳಿದ: ಮೂರನೇ ಹೆಜ್ಜೆ, ನನ್ನ ತಲೆ ಮೇಲೆ ಇಡಿ.", gap=REVEAL_GAP),
        dict(id="v15", text="ಇಲ್ಲೇ ಸ್ಟೋರಿ ಟ್ವಿಸ್ಟ್ ಆಯ್ತು. ದೇವರು ಬಲಿಗೆ ಸುತಲ ಲೋಕ ಕೊಟ್ರು: ದೇವತೆಗಳೂ ಆಸೆ ಪಡೋ ಲೋಕ."),
        dict(id="v16", text="ಮತ್ತೆ ಪ್ರಾಮಿಸ್ ಮಾಡಿದ್ರು: ನಾನು ಯಾವಾಗ್ಲೂ ನಿನ್ ಜೊತೆ ಇರ್ತೀನಿ, ನಿನ್ನ ಕಾಪಾಡ್ತೀನಿ."),
        dict(id="v17", text="ಮುಂದಿನ ಯುಗದಲ್ಲಿ, ಸಾವರ್ಣಿ ಮನುವಿನ ಕಾಲದಲ್ಲಿ, ನೀನೇ ಸ್ವರ್ಗದ ರಾಜ ಆಗ್ತೀಯ.", gap=REVEAL_GAP),
        dict(id="v18", text="ಅದಕ್ಕೇ ದೀಪಾವಳಿಯ ಮಾರನೇ ದಿನ, ನಾವು ಬಲಿ ಪಾಡ್ಯಮಿ ಆಚರಿಸ್ತೀವಿ. ನಂಬಿಕೆ ಪ್ರಕಾರ, ಆ ದಿನ ಬಲಿ ತನ್ನ ಜನರನ್ನ "
                            "ನೋಡೋಕೆ ವಾಪಸ್ ಬರ್ತಾನೆ."),
        dict(id="v19", text="ಮಾತಿಗಾಗಿ ಎಲ್ಲಾನೂ ಕೊಟ್ಟವನಿಗೆ... ದೇವತೆಗಳಿಗೂ ಸಿಗದ್ದು ಸಿಕ್ತು.", gap=REVEAL_GAP),
        dict(id="v20", text="ನೀವು ಬಲಿ ಜಾಗದಲ್ಲಿ ಇದ್ದಿದ್ರೆ, ಮಾತು ಉಳಿಸ್ಕೊಳ್ತಿದ್ರಾ? ಎಸ್ ಆರ್ ನೋ, ಕಮೆಂಟ್ ಮಾಡಿ."),
    ],
}

_SOURCES = ["Bhagavata Purana 8.19-8.23, 5.17.1"]
METADATA = {
    "hi": dict(
        title="Bhagwan ne sab le liya, phir swarg ka raja banaya",
        caption="Socho, Bhagwan ne ek raja se sab kuch le liya... aur phir vaada kiya: ek din tum hi swarg ke raja "
                "banoge 😳\n\nBhagavata Purana: Raja Bali ne Vaman ko teen kadam zameen di. Do kadam mein dharti aur "
                "aakash, teesra kadam Bali ke sir par. Aur maanyata hai, Diwali ke agle din Bali apni praja se milne "
                "aate hain.\n\nTum Bali ki jagah hote toh vachan nibhate? YES ya NO, comment mein batao 👇",
        yt_title="Bhagwan Ne Sab Le Liya, Phir Swarg Ka Raja Banaya 😳 | Raja Bali | Bali Pratipada",
        yt_description="Raja Bali ne Vaman ko teen kadam zameen ka daan diya. Shukracharya ne roka, par Bali vachan se "
                       "nahi hate. Do kadam mein dharti aur aakash, aur teesra kadam Bali ke sir par. Phir Bhagwan ne "
                       "Bali ko Sutal lok diya aur vaada kiya ki Savarni Manu ke samay wo swarg ke raja banenge. "
                       "Diwali ke agle din Bali Pratipada isi ki yaad mein manayi jaati hai.",
        hashtags=["#rajabali", "#vamana", "#diwali", "#bhagavatapurana", "#mythology"],
        pinned_comment="Tum Bali ki jagah hote, toh vachan nibhate? YES ya NO? 👇",
        sources=_SOURCES),
    "kn": dict(
        title="ದೇವರು ಎಲ್ಲಾ ತಗೊಂಡ್ರು, ಆಮೇಲೆ ಸ್ವರ್ಗದ ರಾಜನ ಪ್ರಾಮಿಸ್ ಕೊಟ್ರು",
        caption="ಜಸ್ಟ್ ಇಮ್ಯಾಜಿನ್: ದೇವರು ಒಬ್ಬ ರಾಜನ ಹತ್ರ ಇದ್ದದ್ದೆಲ್ಲಾ ತಗೊಂಡ್ರು... ಆಮೇಲೆ ಹೇಳಿದ್ರು: ನೀನೇ ಸ್ವರ್ಗದ ರಾಜ "
                "ಆಗ್ತೀಯ 😳\n\nಭಾಗವತ ಪುರಾಣ: ಬಲಿ ಚಕ್ರವರ್ತಿ ವಾಮನನಿಗೆ ಮೂರು ಹೆಜ್ಜೆ ಜಾಗ ಕೊಟ್ಟ. ಎರಡು ಹೆಜ್ಜೆಯಲ್ಲಿ ಭೂಮಿ, "
                "ಆಕಾಶ; ಮೂರನೇ ಹೆಜ್ಜೆ ಬಲಿಯ ತಲೆ ಮೇಲೆ. ಬಲಿ ಪಾಡ್ಯಮಿ ದಿನ ಬಲಿ ತನ್ನ ಜನರನ್ನ ನೋಡೋಕೆ ಬರ್ತಾನೆ ಅನ್ನೋ ನಂಬಿಕೆ.\n\n"
                "ನೀವು ಮಾತು ಉಳಿಸ್ಕೊಳ್ತಿದ್ರಾ? YES or NO, ಕಮೆಂಟ್ ಮಾಡಿ 👇",
        yt_title="ದೇವರು ಎಲ್ಲಾ ತಗೊಂಡ್ರು, ಆಮೇಲೆ ಸ್ವರ್ಗದ ರಾಜನ ಪ್ರಾಮಿಸ್ 😳 | ಬಲಿ ಪಾಡ್ಯಮಿ | ವಾಮನ",
        yt_description="ಬಲಿ ಚಕ್ರವರ್ತಿ ವಾಮನನಿಗೆ ಮೂರು ಹೆಜ್ಜೆ ಜಾಗ ದಾನ ಕೊಟ್ಟ. ಶುಕ್ರಾಚಾರ್ಯರು ತಡೆದ್ರೂ, ಬಲಿ ಮಾತಿಂದ "
                       "ಹಿಂದೆ ಸರಿಯಲಿಲ್ಲ. ಎರಡು ಹೆಜ್ಜೆಯಲ್ಲಿ ಭೂಮಿ ಆಕಾಶ, ಮೂರನೇ ಹೆಜ್ಜೆ ಬಲಿಯ ತಲೆ ಮೇಲೆ. ದೇವರು ಬಲಿಗೆ ಸುತಲ "
                       "ಲೋಕ ಕೊಟ್ಟು, ಸಾವರ್ಣಿ ಮನುವಿನ ಕಾಲದಲ್ಲಿ ಸ್ವರ್ಗದ ರಾಜ ಆಗ್ತೀಯ ಅಂತ ಪ್ರಾಮಿಸ್ ಮಾಡಿದ್ರು. ಬಲಿ ಪಾಡ್ಯಮಿ ಇದರ "
                       "ನೆನಪಿಗೆ.",
        hashtags=["#kannada", "#balipadyami", "#deepavali", "#vamana", "#kannadastory"],
        pinned_comment="ನೀವು ಬಲಿ ಜಾಗದಲ್ಲಿ ಇದ್ದಿದ್ರೆ, ಮಾತು ಉಳಿಸ್ಕೊಳ್ತಿದ್ರಾ? YES or NO? 👇",
        sources=_SOURCES),
}


def __getattr__(name):                   # P, USED_ASSETS, CREDITS_FILES come from the scene code
    import scenes_bali as s
    return getattr(s, name)


def draw(cr, t, tl):
    from scenes_bali import draw as _draw
    _draw(cr, t, tl)


def sfx(tl):
    from scenes_bali import sfx as _sfx
    return _sfx(tl)
