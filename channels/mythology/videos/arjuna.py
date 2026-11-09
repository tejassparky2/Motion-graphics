"""Mythology video 10: Arjuna raises his sword on his own elder brother, and Krishna's two tricks (owner picked this
topic, "1", on 9 Nov 2026 after the first YouTube results: the winners are one impossible-sounding claim + shadow
puppets; script approved "Ok"). Narrator with the "सोचो..." hook, every step said plainly, debate ending.
Look: Togalu Gombeyaata shadow puppets; the sword is only raised and stopped, nobody is hurt on screen. Calm sound.

Facts (Mahabharata, Karna Parva, K. M. Ganguli translation, sections 68-71):
- 68: Yudhishthira, beaten and mocked by Karna that day, thinks Arjuna has come after killing Karna; learning Karna
  lives, he says "give this thy Gandiva today to some other king" and "Fie on thy Gandiva".
- 69: Arjuna: "I would cut off the head of that man who would tell me 'Give thy Gandiva to another person.'"
  Krishna: "A superior, O Bharata, by being addressed as 'thou,' is killed though not deprived of life."
- 70: Arjuna, using "thou": "It was thou that hadst gambled. It was for thee that we lost our kingdom." Then he draws
  his sword to slay himself; Krishna: "Declare now, in words, thy own merit. Thou shalt then, O Partha, have slain thy
  own self." Arjuna praises himself and bows at Yudhishthira's feet; Yudhishthira forgives them (70-71).
"""
from channel import ASSETS_ROOT, MUSIC, NARRATORS, NARRATOR_LABEL, REVEAL_GAP, TAIL  # noqa: F401

SCRIPTS = {
    "hi": [
        dict(id="a1", text="सोचो, अर्जुन ने अपने ही बड़े भाई पर तलवार उठा ली... और कृष्ण ने रास्ता बताया: भाई को मार दो, "
                           "पर बिना मारे।", gap=REVEAL_GAP),
        dict(id="a2", text="ये कोई फ़िल्मी कहानी नहीं है। ये महाभारत के कर्ण पर्व में लिखा है।"),
        dict(id="a3", text="युधिष्ठिर, पांडवों में सबसे बड़े भाई थे। अर्जुन, उनका छोटा भाई, और सबसे बड़ा धनुर्धारी।"),
        dict(id="a4", text="अर्जुन के धनुष का नाम था, गांडीव। और अर्जुन ने चुपचाप एक क़सम खाई थी।"),
        dict(id="a5", text="जो भी मुझसे कहेगा, अपना गांडीव किसी और को दे दो... मैं उसका सिर काट दूँगा।", gap=REVEAL_GAP),
        dict(id="a6", text="कौरवों का सबसे बड़ा योद्धा था, कर्ण। एक दिन कर्ण ने युधिष्ठिर को बुरी तरह हराया, और उनका मज़ाक "
                           "उड़ाकर छोड़ दिया।"),
        dict(id="a7", text="घायल युधिष्ठिर अपने तंबू में लौटे। अर्जुन, कृष्ण के साथ उनका हाल पूछने आया।"),
        dict(id="a8", text="युधिष्ठिर को लगा, अर्जुन कर्ण को मारकर आया है। पर कर्ण अभी ज़िंदा था।"),
        dict(id="a9", text="ग़ुस्से में युधिष्ठिर बोले: धिक्कार है तुम्हारे गांडीव पर! इसे किसी और को दे दो!", gap=REVEAL_GAP),
        dict(id="a10", text="बस, अर्जुन की क़सम सामने आ गई। उसने तलवार निकाली... अपने ही बड़े भाई को मारने के लिए।",
             gap=REVEAL_GAP),
        dict(id="a11", text="कृष्ण ने उसका हाथ रोका। अर्जुन बोला: क़सम तोड़ूँ, तो झूठा बनूँगा। भाई को मारूँ, तो पापी। अब "
                            "क्या करूँ?"),
        dict(id="a12", text="कृष्ण बोले: बड़ों की इज़्ज़त ही उनकी जान होती है। बड़े भाई को आप की जगह तू कहकर डाँटोगे, तो "
                            "समझो, तुमने उन्हें मार दिया, बिना मारे।"),
        dict(id="a13", text="अर्जुन ने वही किया। उसने बड़े भाई को तू कहकर डाँटा: तूने जुआ खेला, तेरी वजह से हमारा राज्य "
                            "गया!"),
        dict(id="a14", text="क़सम भी पूरी हो गई, और भाई भी ज़िंदा रहे।", gap=REVEAL_GAP),
        dict(id="a15", text="पर अब अर्जुन को इतनी शर्म आई, कि उसने फिर तलवार निकाली... इस बार, अपने आप को मारने के लिए।",
             gap=REVEAL_GAP),
        dict(id="a16", text="कृष्ण ने फिर रास्ता निकाला: अपनी तारीफ़ ख़ुद करना, अपने आप को मारने जैसा है। तो अपनी तारीफ़ "
                            "करो।"),
        dict(id="a17", text="अर्जुन ने अपनी ख़ूब बड़ाई की। फिर बड़े भाई के पैरों में गिर पड़ा, और युधिष्ठिर ने उसे माफ़ कर "
                            "दिया।", gap=REVEAL_GAP),
        dict(id="a18", text="कृष्ण की ये चाल: समझदारी थी, या क़सम के साथ धोखा? कमेंट में बताओ।"),
    ],
    "kn": [
        dict(id="a1", text="ಯೋಚಿಸಿ... ಅರ್ಜುನ ತನ್ನ ಸ್ವಂತ ಅಣ್ಣನ ಮೇಲೇ ಕತ್ತಿ ಎತ್ತಿದ... ಕೃಷ್ಣ ದಾರಿ ಹೇಳಿದ: ಅಣ್ಣನನ್ನ ಕೊಲ್ಲು, "
                           "ಆದ್ರೆ ಕೊಲ್ಲದೆ.", gap=REVEAL_GAP),
        dict(id="a2", text="ಇದು ಸಿನಿಮಾ ಕಥೆ ಅಲ್ಲ. ಮಹಾಭಾರತದ ಕರ್ಣ ಪರ್ವದಲ್ಲೇ ಇದೆ."),
        dict(id="a3", text="ಯುಧಿಷ್ಠಿರ, ಪಾಂಡವರಲ್ಲಿ ಎಲ್ಲರಿಗಿಂತ ದೊಡ್ಡ ಅಣ್ಣ. ಅರ್ಜುನ, ಅವರ ತಮ್ಮ, ಅತಿ ದೊಡ್ಡ ಬಿಲ್ಲುಗಾರ."),
        dict(id="a4", text="ಅರ್ಜುನನ ಬಿಲ್ಲಿನ ಹೆಸರು, ಗಾಂಡೀವ. ಅರ್ಜುನ ಯಾರಿಗೂ ಹೇಳದೆ ಒಂದು ಪ್ರತಿಜ್ಞೆ ಮಾಡಿದ್ದ."),
        dict(id="a5", text="ಯಾರಾದ್ರೂ ನನಗೆ, ನಿನ್ನ ಗಾಂಡೀವನ ಬೇರೆಯವರಿಗೆ ಕೊಡು ಅಂದ್ರೆ... ಅವರ ತಲೆ ಕಡಿತೀನಿ.", gap=REVEAL_GAP),
        dict(id="a6", text="ಕೌರವರ ಕಡೆಯ ಅತಿ ದೊಡ್ಡ ಯೋಧ, ಕರ್ಣ. ಒಂದು ದಿನ ಕರ್ಣ ಯುಧಿಷ್ಠಿರನನ್ನ ಕೆಟ್ಟದಾಗಿ ಸೋಲಿಸಿ, ಅವಮಾನ "
                           "ಮಾಡಿ ಕಳಿಸಿದ."),
        dict(id="a7", text="ಗಾಯಗೊಂಡ ಯುಧಿಷ್ಠಿರ ಟೆಂಟ್‌ಗೆ ವಾಪಸ್ ಬಂದ್ರು. ಅರ್ಜುನ, ಕೃಷ್ಣನ ಜೊತೆ ಅವರನ್ನ ನೋಡೋಕೆ ಬಂದ."),
        dict(id="a8", text="ಯುಧಿಷ್ಠಿರನಿಗೆ ಅನ್ನಿಸ್ತು, ಅರ್ಜುನ ಕರ್ಣನನ್ನ ಕೊಂದು ಬಂದಿದ್ದಾನೆ ಅಂತ. ಆದ್ರೆ ಕರ್ಣ ಇನ್ನೂ ಬದುಕಿದ್ದ."),
        dict(id="a9", text="ಕೋಪದಲ್ಲಿ ಯುಧಿಷ್ಠಿರ ಹೇಳಿದ್ರು: ನಿನ್ನ ಗಾಂಡೀವಕ್ಕೆ ಧಿಕ್ಕಾರ! ಅದನ್ನ ಬೇರೆ ಯಾರಿಗಾದ್ರೂ ಕೊಟ್ಟುಬಿಡು!",
             gap=REVEAL_GAP),
        dict(id="a10", text="ಅಷ್ಟೇ, ಅರ್ಜುನನಿಗೆ ಪ್ರತಿಜ್ಞೆ ನೆನಪಾಯ್ತು. ಅವನು ಕತ್ತಿ ಎಳೆದ... ತನ್ನ ಸ್ವಂತ ಅಣ್ಣನನ್ನೇ ಕೊಲ್ಲೋಕೆ.",
             gap=REVEAL_GAP),
        dict(id="a11", text="ಕೃಷ್ಣ ಅವನನ್ನ ತಡೆದ. ಅರ್ಜುನ ಹೇಳಿದ: ಪ್ರತಿಜ್ಞೆ ಮುರಿದ್ರೆ ನಾನು ಸುಳ್ಳುಗಾರ. ಅಣ್ಣನನ್ನ ಕೊಂದ್ರೆ ಪಾಪಿ. "
                            "ಈಗ ಏನು ಮಾಡ್ಲಿ?"),
        dict(id="a12", text="ಕೃಷ್ಣ ಹೇಳಿದ: ದೊಡ್ಡವರಿಗೆ ಮರ್ಯಾದೆನೇ ಜೀವ. ಅಣ್ಣನಿಗೆ ನೀವು ಅನ್ನೋ ಬದಲು, ನೀನು ಅಂತ ಏಕವಚನದಲ್ಲಿ "
                            "ಬೈದ್ರೆ, ಅವರನ್ನ ಕೊಂದ ಹಾಗೇ, ಕೊಲ್ಲದೆ."),
        dict(id="a13", text="ಅರ್ಜುನ ಹಾಗೇ ಮಾಡಿದ. ಅಣ್ಣನಿಗೆ ಏಕವಚನದಲ್ಲಿ ಬೈದ: ನೀನು ಜೂಜಾಡಿದೆ, ನಿನ್ನಿಂದಾನೇ ನಮ್ಮ ರಾಜ್ಯ ಹೋಯ್ತು!"),
        dict(id="a14", text="ಪ್ರತಿಜ್ಞೆನೂ ಉಳೀತು, ಅಣ್ಣನೂ ಬದುಕಿದ್ರು.", gap=REVEAL_GAP),
        dict(id="a15", text="ಆದ್ರೆ ಈಗ ಅರ್ಜುನನಿಗೆ ತುಂಬಾ ನಾಚಿಕೆ ಆಯ್ತು. ಮತ್ತೆ ಕತ್ತಿ ಎಳೆದ... ಈ ಸಲ, ತನ್ನನ್ನ ತಾನೇ "
                            "ಕೊಂದುಕೊಳ್ಳೋಕೆ.", gap=REVEAL_GAP),
        dict(id="a16", text="ಕೃಷ್ಣ ಮತ್ತೆ ದಾರಿ ತೋರಿಸಿದ: ತನ್ನನ್ನ ತಾನೇ ಹೊಗಳಿಕೊಳ್ಳೋದು, ತನ್ನನ್ನ ತಾನೇ ಕೊಂದುಕೊಂಡ ಹಾಗೇ. "
                            "ನಿನ್ನನ್ನ ನೀನೇ ಹೊಗಳಿಕೋ."),
        dict(id="a17", text="ಅರ್ಜುನ ತನ್ನನ್ನ ತಾನೇ ಜೋರಾಗಿ ಹೊಗಳಿಕೊಂಡ. ಆಮೇಲೆ ಅಣ್ಣನ ಕಾಲಿಗೆ ಬಿದ್ದ, ಯುಧಿಷ್ಠಿರ ಅವನನ್ನ "
                            "ಕ್ಷಮಿಸಿದ್ರು.", gap=REVEAL_GAP),
        dict(id="a18", text="ಕೃಷ್ಣನ ಈ ತಂತ್ರ: ಬುದ್ಧಿವಂತಿಕೆನಾ, ಅಥವಾ ಪ್ರತಿಜ್ಞೆಗೆ ಮೋಸನಾ? ಕಾಮೆಂಟ್ ಮಾಡಿ ಹೇಳಿ."),
    ],
}

_SOURCES = ["Mahabharata, Karna Parva, sections 68-71 (K. M. Ganguli translation)"]
METADATA = {
    "hi": dict(
        title="Arjun ne apne hi bhai par talwar uthayi",
        caption="Socho, Arjun ne apne hi bade bhai Yudhishthir par talwar utha li... aur Krishna ne kaha: maar do, "
                "par bina maare 😳\n\n"
                "Mahabharat, Karna Parva: Arjun ki chupi kasam thi, jo kahega 'apna Gandiv kisi aur ko de do', uska "
                "sir kaat doonga. Karn se haare Yudhishthir ne gusse mein wahi keh diya. Krishna ka raasta: bade bhai "
                "ko 'aap' ki jagah 'tu' kehna, bina maare maarne jaisa hai.\n\n"
                "Krishna ki ye chaal: samajhdaari thi, ya kasam ke saath dhokha? Comment mein batao 👇",
        yt_title="Arjun Ne Apne Hi Bhai Par Talwar Uthayi 😳 | Krishna Ki Chaal | Mahabharat",
        yt_description="Arjun ne chupchaap kasam khaayi thi: jo bhi kahega 'apna Gandiv kisi aur ko de do', uska sir "
                       "kaat doonga. Karn se haarkar lautey Yudhishthir ne gusse mein yahi keh diya, aur Arjun ne "
                       "talwar nikaal li. Krishna ne kaha, bade ki izzat hi unki jaan hai: unhe 'tu' keh kar daanto, "
                       "toh kasam bhi poori, bhai bhi zinda. Phir sharm se Arjun khud ko maarne chala, aur Krishna ka "
                       "doosra raasta: apni taareef khud karna, khud ko maarne jaisa hai.",
        hashtags=["#mahabharat", "#krishna", "#arjun", "#mythology", "#kahani"],
        pinned_comment="Krishna ki ye chaal: samajhdaari thi, ya kasam ke saath dhokha? 👇",
        sources=_SOURCES),
    "kn": dict(
        title="Arjuna tanna annana mele katti ettida",
        caption="Yochisi: Arjuna tanna swanta annana mele katti ettida... Krishna helida: kollu, aadre kollade 😳\n\n"
                "Mahabharata, Karna Parva: Arjunana guttu pratijne, yaaru 'ninna Gandiva bereyavrige kodu' antaaro, "
                "avara tale kaditeeni. Karnana kaili sota Yudhishthira kopadalli ade helidru. Krishnana daari: "
                "annanige 'neevu' badalu 'neenu' anta ekavachanadalli baidre, kollade kondanthe.\n\n"
                "Krishnana ee tantra: buddhivantikena, illa pratijnege mosana? Comment maadi 👇",
        yt_title="Arjuna Tanna Annana Mele Katti Ettida 😳 | Krishnana Tantra | Mahabharata",
        yt_description="Arjuna yaarigu helade pratijne maadidda: yaaru 'ninna Gandiva bereyavrige kodu' antaaro avara "
                       "tale kaditeeni. Karnana kaili sotu banda Yudhishthira kopadalli ade helidru, Arjuna katti "
                       "eleda. Krishna helida: doddavarige maryaadene jeeva, annanige ekavachanadalli baidre pratijnenu "
                       "ulitu, annanu badukidru. Aamele naachikeyinda Arjuna tannannu taane kolloke hoda; Krishnana "
                       "eradane daari: tannannu taane hogalikolluvudu, taane kondukondante.",
        hashtags=["#kannada", "#mahabharata", "#krishna", "#kannadastory", "#mythology"],
        pinned_comment="Krishnana ee tantra: buddhivantikena, illa pratijnege mosana? 👇",
        sources=_SOURCES),
}


USED_ASSETS, CREDITS_FILES = [], []      # everything in this video is drawn in code


def draw(cr, t, tl):
    from scenes_arjuna import draw as _draw
    _draw(cr, t, tl)


def sfx(tl):
    from scenes_arjuna import sfx as _sfx
    return _sfx(tl)
