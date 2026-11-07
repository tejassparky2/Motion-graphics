"""Mythology video 1: King Kakudmi waits a few moments in Brahmaloka, and over 11 crore years pass on Earth.
Approach A: a code-drawn chibi cast (the vex2d method from the 2D playbook) on code-painted scenes with divine light.
Hook style: second person, "imagine you waited a few moments..." (owner, 6 Nov 2026: three videos, each with a
different approach, hook and animation; Kannada in everyday city Kannada with English words).

Facts: Bhagavata Purana 9.3.29-36 (Kakudmi takes Revati to Brahmaloka; Brahma is hearing the Gandharvas' music, the
king waits; Brahma laughs; "twenty-seven catur-yugas have already passed"; give her to Baladeva). Vishnu Purana 4.1
(Wilson 1840; Dutt 1894): the singers are Haha and Huha; "the ages ... seemed to him as a moment"; Kushasthali "is
now called Dwaraka"; mankind "greatly reduced in size and vigour and weakened in intellect"; Balarama "shortened
her with the end of his ploughshare". 1 chatur-yuga = 43,20,000 years; x27 = 11,66,40,000 years.
"""
from channel import ASSETS_ROOT, MUSIC, NARRATORS, NARRATOR_LABEL, REVEAL_GAP, TAIL  # noqa: F401

SCRIPTS = {
    "hi": [
        dict(id="b1", text="सोचो, तुम बस कुछ पल एक दरबार में रुके... और बाहर निकले, तो धरती पर ग्यारह करोड़ साल से "
                           "ज़्यादा बीत चुके थे।"),
        dict(id="b1b", text="तुम्हारा परिवार, तुम्हारा शहर, तुम्हारा पूरा ज़माना... सब ख़त्म।", gap=REVEAL_GAP),
        dict(id="b2", text="ये कोई हॉलीवुड फ़िल्म नहीं है। ये कहानी भागवत पुराण में लिखी है।"),
        dict(id="b3", text="एक राजा थे, ककुद्मी। और उनकी बेटी थीं, रेवती।"),
        dict(id="b4", text="रेवती इतनी गुणी थीं, कि धरती पर राजा को उनके लायक़ कोई वर ही नहीं मिला।"),
        dict(id="b5", text="तो राजा ने सोचा: जिसने सबको बनाया है, उन्हीं से पूछते हैं।"),
        dict(id="b6", text="वो रेवती को लेकर, सीधे ब्रह्मलोक पहुँच गए। ब्रह्मा जी के पास।"),
        dict(id="b7", text="पर वहाँ ब्रह्मा जी संगीत सुन रहे थे। दो गंधर्व, हाहा और हूहू, गा रहे थे।"),
        dict(id="b8", text="राजा ने सोचा, गाना ख़त्म हो जाए, फिर बात करेंगे। और वो चुपचाप खड़े रहे।"),
        dict(id="b9", text="गाना ख़त्म हुआ। राजा ने हाथ जोड़कर, अपने चुने हुए वरों के नाम बताए।"),
        dict(id="b10", text="ये सुनकर, ब्रह्मा जी हँसने लगे।"),
        dict(id="b11", text="राजन, जिनके नाम तुम ले रहे हो, वो सब कब के जा चुके हैं। आज धरती पर कोई उनका नाम तक नहीं "
                            "जानता।"),
        dict(id="b12", text="तुम यहाँ कुछ पल रुके... पर नीचे धरती पर, सत्ताईस चतुर्युग बीत चुके हैं।", gap=REVEAL_GAP),
        dict(id="b12b", text="जाओ, अपनी बेटी का हाथ बलराम को दो। वो अभी धरती पर हैं।"),
        dict(id="b13", text="एक चतुर्युग, यानी तैंतालीस लाख बीस हज़ार साल। और ऐसे, सत्ताईस।"),
        dict(id="b14", text="यानी ग्यारह करोड़ से भी ज़्यादा साल।", gap=REVEAL_GAP),
        dict(id="b15", text="पर असली झटका तो अभी बाकी था। धरती पर लौटकर, राजा ने क्या देखा?"),
        dict(id="b16", text="इंसान छोटे हो चुके थे। क़द में भी, ताक़त में भी, और समझ में भी।"),
        dict(id="b17", text="उनका अपना शहर, कुशस्थली... अब द्वारका कहलाता था।"),
        dict(id="b18", text="और एक मुश्किल और थी। पुराने ज़माने की रेवती, इस ज़माने के बलराम से... बहुत लंबी थीं।"),
        dict(id="b19", text="विष्णु पुराण कहता है, बलराम ने अपने हल के सिरे से, रेवती का क़द घटा दिया... और वो बाकी लोगों "
                            "जैसी हो गईं।"),
        dict(id="b20", text="कुछ पल का इंतज़ार... और करोड़ों साल का फ़ासला।", gap=REVEAL_GAP),
        dict(id="b21", text="तुम ब्रह्मलोक जाते? ये जानते हुए भी, कि लौटकर कोई अपना नहीं मिलेगा? यस या नो, कमेंट में "
                            "बताओ।"),
    ],
    # everyday city Kannada with common English words (owner, 6 Nov 2026: "normal everyday speaking kannada kanglish
    # and standard kannada only city peoples taking kannada")
    "kn": [
        dict(id="b1", text="ಯೋಚಿಸಿ... ನೀವು ಒಂದು ಸಭೆಯಲ್ಲಿ ಕೆಲವೇ ಕ್ಷಣ ಕಾಯ್ತೀರಾ. ಆದ್ರೆ ಹೊರಗೆ ಬಂದ್ರೆ, "
                           "ಭೂಮಿ ಮೇಲೆ ಹನ್ನೊಂದು ಕೋಟಿ ವರ್ಷಕ್ಕಿಂತ ಜಾಸ್ತಿ ಕಳೆದುಹೋಗಿರುತ್ತೆ."),
        dict(id="b1b", text="ನಿಮ್ ಮನೆಯವರು, ನಿಮ್ ಊರು, ನಿಮ್ ಇಡೀ ಕಾಲ... ಎಲ್ಲಾ ಮುಗಿದುಹೋಗಿರುತ್ತೆ.", gap=REVEAL_GAP),
        dict(id="b2", text="ಇದು ಯಾವ್ದೋ ಹಾಲಿವುಡ್ ಸಿನಿಮಾ ಕಥೆ ಅಲ್ಲ. ಭಾಗವತ ಪುರಾಣದಲ್ಲೇ ಇರೋ ಕಥೆ ಇದು."),
        dict(id="b3", text="ಒಬ್ರು ರಾಜ ಇದ್ರು, ಕಕುದ್ಮಿ ಅಂತ. ಅವರ ಮಗಳು, ರೇವತಿ."),
        dict(id="b4", text="ರೇವತಿ ಎಷ್ಟು ಗುಣವಂತೆ, ಎಷ್ಟು ಜಾಣೆ ಅಂದ್ರೆ, ಭೂಮಿ ಮೇಲೆ ಅವರಿಗೆ ತಕ್ಕ ಹುಡುಗನೇ "
                           "ಸಿಗ್ಲಿಲ್ಲ."),
        dict(id="b5", text="ಅದಕ್ಕೆ ರಾಜ ಯೋಚ್ನೆ ಮಾಡಿದ್ರು: ಎಲ್ಲರನ್ನೂ ಸೃಷ್ಟಿ ಮಾಡಿದವರನ್ನೇ ನೇರವಾಗಿ ಕೇಳೋಣ."),
        dict(id="b6", text="ರೇವತಿನ ಕರ್ಕೊಂಡು, ಸೀದಾ ಬ್ರಹ್ಮಲೋಕಕ್ಕೆ ಹೋದ್ರು. ಬ್ರಹ್ಮದೇವರ ಹತ್ರ."),
        dict(id="b7", text="ಆದ್ರೆ ಅಲ್ಲಿ ಬ್ರಹ್ಮದೇವರು ಸಂಗೀತ ಕೇಳ್ತಾ ಇದ್ರು. ಹಾಹಾ ಮತ್ತು ಹೂಹೂ ಅನ್ನೋ ಇಬ್ರು ಗಂಧರ್ವರು "
                           "ಹಾಡ್ತಾ ಇದ್ರು."),
        dict(id="b8", text="ಹಾಡು ಮುಗೀಲಿ, ಆಮೇಲೆ ಮಾತಾಡೋಣ ಅಂತ, ರಾಜ ಸುಮ್ಮನೆ ಕಾದು ನಿಂತ್ರು."),
        dict(id="b9", text="ಹಾಡು ಮುಗೀತು. ರಾಜ ಕೈಮುಗಿದು, ತಾವು ಆರಿಸಿದ್ದ ಹುಡುಗರ ಹೆಸರುಗಳನ್ನ ಹೇಳಿದ್ರು."),
        dict(id="b10", text="ಬ್ರಹ್ಮದೇವರು ನಕ್ಕುಬಿಟ್ರು."),
        dict(id="b11", text="ರಾಜನ್, ನೀನು ಹೇಳ್ತಿರೋ ಹುಡುಗರೆಲ್ಲ ಎಂದೋ ಹೋಗಿಬಿಟ್ಟಿದ್ದಾರೆ. ಇವತ್ತು ಭೂಮಿ ಮೇಲೆ ಅವರ ಹೆಸರೂ "
                            "ಯಾರಿಗೂ ಗೊತ್ತಿಲ್ಲ."),
        dict(id="b12", text="ನೀನು ಇಲ್ಲಿ ಕೆಲವೇ ಕ್ಷಣ ಕಾದೆ... ಆದ್ರೆ ಕೆಳಗೆ ಭೂಮಿ ಮೇಲೆ, ಇಪ್ಪತ್ತೇಳು ಚತುರ್ಯುಗ "
                            "ಕಳೆದುಹೋಗಿದೆ.", gap=REVEAL_GAP),
        dict(id="b12b", text="ಹೋಗು, ನಿನ್ ಮಗಳನ್ನ ಬಲರಾಮನಿಗೆ ಕೊಡು. ಅವನು ಈಗ ಭೂಮಿ ಮೇಲಿದ್ದಾನೆ."),
        dict(id="b13", text="ಒಂದು ಚತುರ್ಯುಗ ಅಂದ್ರೆ, ನಲವತ್ತಮೂರು ಲಕ್ಷ ಇಪ್ಪತ್ತು ಸಾವಿರ ವರ್ಷ. ಅಂಥಾದ್ದು ಇಪ್ಪತ್ತೇಳು."),
        dict(id="b14", text="ಅಂದ್ರೆ, ಹನ್ನೊಂದು ಕೋಟಿ ವರ್ಷಕ್ಕಿಂತ ಜಾಸ್ತಿ.", gap=REVEAL_GAP),
        dict(id="b15", text="ಆದ್ರೆ ನಿಜವಾದ ಶಾಕ್ ಇನ್ನೂ ಬಾಕಿ ಇತ್ತು. ಭೂಮಿಗೆ ವಾಪಸ್ ಬಂದ ರಾಜ ಏನ್ ನೋಡಿದ್ರು?"),
        dict(id="b16", text="ಜನ ಎಲ್ಲಾ ಚಿಕ್ಕೋರಾಗಿಹೋಗಿದ್ರು. ಎತ್ತರದಲ್ಲೂ, ಶಕ್ತಿಯಲ್ಲೂ, ಬುದ್ಧಿಯಲ್ಲೂ."),
        dict(id="b17", text="ಅವರ ಸ್ವಂತ ಊರು, ಕುಶಸ್ಥಲಿ... ಈಗ ದ್ವಾರಕೆ ಆಗಿಹೋಗಿತ್ತು."),
        dict(id="b18", text="ಇನ್ನೊಂದು ತೊಂದರೆ ಕೂಡ ಇತ್ತು. ಹಳೇ ಯುಗದ ರೇವತಿ, ಈ ಯುಗದ ಬಲರಾಮನಿಗಿಂತ... ತುಂಬಾ ಎತ್ತರ ಇದ್ರು."),
        dict(id="b19", text="ವಿಷ್ಣು ಪುರಾಣ ಹೇಳೋ ಪ್ರಕಾರ, ಬಲರಾಮ ತಮ್ಮ ನೇಗಿಲಿನ ತುದಿಯಿಂದ ರೇವತಿಯ ಎತ್ತರ ಕಮ್ಮಿ ಮಾಡಿದ್ರು... "
                            "ಆಮೇಲೆ ಅವರು ಬೇರೆಯವರ ತರಾನೇ ಆದ್ರು."),
        dict(id="b20", text="ಕಾದಿದ್ದು ಕೆಲವೇ ಕ್ಷಣ... ಆದ್ರೆ ಕಳೆದಿದ್ದು ಕೋಟಿಗಟ್ಟಲೆ ವರ್ಷ.", gap=REVEAL_GAP),
        dict(id="b21", text="ನೀವು ಬ್ರಹ್ಮಲೋಕಕ್ಕೆ ಹೋಗ್ತೀರಾ? ವಾಪಸ್ ಬಂದಾಗ ನಿಮ್ಮೋರು ಯಾರೂ ಇರಲ್ಲ ಅಂತ ಗೊತ್ತಿದ್ರೂ? ಹೌದಾ ಇಲ್ವಾ, "
                            "ಕಾಮೆಂಟ್ ಮಾಡಿ ಹೇಳಿ."),
    ],
}

_SOURCES = ["Bhagavata Purana 9.3", "Vishnu Purana 4.1 (H. H. Wilson 1840; M. N. Dutt 1894)"]
METADATA = {
    "hi": dict(
        title="Brahmalok mein kuch pal, dharti par 11 crore saal",
        caption="Socho, tum bas kuch pal ek darbar mein ruke... aur bahar nikle toh 11 crore saal beet chuke the 😳\n\n"
                "Bhagavata Purana: Raja Kakudmi apni beti Revati ke liye var poochhne Brahmalok gaye. Gandharvon ka "
                "gaana khatam hone tak ruke. Brahma ji hanse: dharti par 27 chaturyug beet chuke hain.\n\n"
                "Tum Brahmalok jaate? YES ya NO, comment mein batao 👇",
        yt_title="Brahmalok Mein Kuch Pal, Dharti Par 11 Crore Saal 😳 | Bhagavata Purana",
        yt_description="Raja Kakudmi apni beti Revati ke liye var poochhne Brahma ji ke paas gaye. Wahan kuch pal ruke, "
                       "aur dharti par 27 chaturyug (11 crore se zyada saal) beet gaye. Lautkar dekha: insaan chhote ho "
                       "gaye the, Kushasthali ab Dwarka thi, aur Revati ka vivah Balaram se hua.",
        hashtags=["#mythology", "#bhagavatapurana", "#hindumythology", "#balaram", "#kahani"],
        pinned_comment="Tum Brahmalok jaate, ye jaante hue bhi ki lautkar koi apna nahi milega? YES ya NO? 👇",
        sources=_SOURCES),
    "kn": dict(
        title="ಬ್ರಹ್ಮಲೋಕದಲ್ಲಿ ಕೆಲವೇ ಕ್ಷಣ, ಭೂಮಿಯಲ್ಲಿ 11 ಕೋಟಿ ವರ್ಷ",
        caption="ಯೋಚಿಸಿ: ಕೆಲವೇ ಕ್ಷಣ ಕಾದ್ರಿ... ಹೊರಗೆ ಬಂದ್ರೆ 11 ಕೋಟಿ ವರ್ಷ ಕಳೆದುಹೋಗಿದೆ 😳\n\n"
                "ಭಾಗವತ ಪುರಾಣ: ರಾಜ ಕಕುದ್ಮಿ ಮಗಳು ರೇವತಿಗೆ ವರ ಕೇಳೋಕೆ ಬ್ರಹ್ಮಲೋಕಕ್ಕೆ ಹೋದ್ರು. ಗಂಧರ್ವರ ಹಾಡು "
                "ಮುಗಿಯೋವರೆಗೂ ಕಾದ್ರು. ಬ್ರಹ್ಮದೇವರು ನಕ್ಕು ಹೇಳಿದ್ರು: ಭೂಮಿ ಮೇಲೆ 27 ಚತುರ್ಯುಗ ಕಳೆದಿದೆ.\n\n"
                "ನೀವು ಹೋಗ್ತೀರಾ? ಹೌದಾ ಇಲ್ವಾ, ಕಾಮೆಂಟ್ ಮಾಡಿ 👇",
        yt_title="ಬ್ರಹ್ಮಲೋಕದಲ್ಲಿ ಕೆಲವೇ ಕ್ಷಣ, ಭೂಮಿಯಲ್ಲಿ 11 ಕೋಟಿ ವರ್ಷ 😳 | ಭಾಗವತ ಪುರಾಣ",
        yt_description="ರಾಜ ಕಕುದ್ಮಿ ಮಗಳು ರೇವತಿಗೆ ವರ ಕೇಳೋಕೆ ಬ್ರಹ್ಮದೇವರ ಹತ್ರ ಹೋದ್ರು. ಅಲ್ಲಿ ಕೆಲವೇ ಕ್ಷಣ ಕಾದ್ರು, ಭೂಮಿ "
                       "ಮೇಲೆ 27 ಚತುರ್ಯುಗ (11 ಕೋಟಿಗಿಂತ ಜಾಸ್ತಿ ವರ್ಷ) ಕಳೆದುಹೋಯ್ತು. ವಾಪಸ್ ಬಂದಾಗ ಜನ ಚಿಕ್ಕೋರಾಗಿದ್ರು, "
                       "ಕುಶಸ್ಥಲಿ ದ್ವಾರಕೆ ಆಗಿತ್ತು, ರೇವತಿಯ ಮದುವೆ ಬಲರಾಮನ ಜೊತೆ ಆಯ್ತು.",
        hashtags=["#kannada", "#mythology", "#bhagavatapurana", "#kannadastory", "#balarama"],
        pinned_comment="ನೀವು ಬ್ರಹ್ಮಲೋಕಕ್ಕೆ ಹೋಗ್ತೀರಾ, ವಾಪಸ್ ಬಂದಾಗ ನಿಮ್ಮೋರು ಯಾರೂ ಇರಲ್ಲ ಅಂತ ಗೊತ್ತಿದ್ರೂ? ಹೌದಾ ಇಲ್ವಾ? 👇",
        sources=_SOURCES),
}

USED_ASSETS, CREDITS_FILES = [], []      # everything in this video is drawn in code


def draw(cr, t, tl):                     # replaced by the scene code (scenes_kakudmi)
    from scenes_kakudmi import draw as _draw
    _draw(cr, t, tl)


def sfx(tl):
    from scenes_kakudmi import sfx as _sfx
    return _sfx(tl)
