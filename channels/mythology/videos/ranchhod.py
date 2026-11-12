"""Mythology video 21: Krishna ran away from battle, which is why one of his names is Ranchhod (the owner's "Continue"
after videos 15-19, 12 Nov 2026). Impossible-sounding hook with a famous god, a chase, a sleeping king with a deadly
boon, and the reveal that the run was the plan; debate: fear or brains? Look: Hindi = Togalu Gombeyaata shadow
puppets, Kannada = Yakshagana stage. Kalayavana's end is a white flash and ash drifting, no burning body. Calm sound.

Facts:
- Bhagavata Purana 10.50.44-57: Kalayavana besieges Mathura with thirty million soldiers; Krishna moves his people to
  Dvaraka, then walks out of the city unarmed.
- Bhagavata Purana 10.51.1-12 (vedabase): seeing him on foot and unarmed, Kalayavana sets aside his own weapons to
  catch him by hand; Krishna runs, staying just out of reach, and leads him to a mountain cave; Kalayavana, hurling
  insults, follows, sees a man lying asleep, takes him for Krishna and kicks him with all his strength; the man wakes,
  looks at him, and Kalayavana bursts into flames and is ash in a moment. 10.51.15-21: the sleeper is King
  Muchukunda, who had long guarded the gods in their war; released, he chose sleep as his boon.
- Vishnu Purana 5.23 (H. H. Wilson translation): the gods granted Muchukunda long repose, "whoever disturbs you shall
  be instantly burnt to ashes by fire emanating from your body"; Kalayavana, kicking him awake, is consumed.
- "Ranchhod" (ran = battle, chhod = leaving) is the popular name for Krishna from these Mathura episodes (Ranchhodrai
  of Dakor); the reel says "one of his names", not that the Bhagavata uses it.
"""
from channel import ASSETS_ROOT, MUSIC, NARRATORS, NARRATOR_LABEL, REVEAL_GAP, TAIL  # noqa: F401

G = REVEAL_GAP
SCRIPTS = {
    "hi": [
        dict(id="rc1", text="सोचो, भगवान कृष्ण, युद्ध छोड़कर भाग गए थे! इसीलिए, उनका एक नाम है: रणछोड़।", gap=G),
        dict(id="rc2", text="रण यानी युद्ध। रणछोड़ यानी, युद्ध छोड़कर भागने वाला। ये भागवत पुराण की सच्ची कहानी है।"),
        dict(id="rc3", text="एक बार, कालयवन नाम का एक ज़ालिम राजा, करोड़ों सैनिक लेकर, कृष्ण की नगरी पर चढ़ आया।", gap=G),
        dict(id="rc4", text="कृष्ण, बिना किसी हथियार के, अकेले बाहर निकले।"),
        dict(id="rc5", text="कालयवन ने सोचा: अकेला, और बिना हथियार? इसे तो मैं, हाथों से ही पकड़ लूँगा!"),
        dict(id="rc6", text="पर जैसे ही वो पास आया... कृष्ण, पीठ दिखाकर भाग गए!", gap=G),
        dict(id="rc7", text="कालयवन चिल्लाया: डरपोक! भागता कहाँ है? और उनके पीछे दौड़ा।"),
        dict(id="rc8", text="कृष्ण दौड़ते रहे, बस उसकी पकड़ से थोड़ा आगे... और एक अँधेरी गुफा में घुस गए।", gap=G),
        dict(id="rc8q", text="तो क्या भगवान कृष्ण, सच में डर गए थे?"),
        dict(id="rc9", text="उस गुफा में, बहुत सालों से, एक राजा सो रहा था। उसका नाम था, मुचुकुंद।"),
        dict(id="rc10", text="उसने देवताओं के लिए, बहुत लंबी लड़ाई लड़ी थी। इसलिए देवताओं ने उसे वरदान दिया: जी भरकर सो जाओ।", gap=G),
        dict(id="rc11", text="और जो भी तुम्हें जगाएगा, वो तुम्हारी नज़र पड़ते ही, जलकर राख हो जाएगा।"),
        dict(id="rc12", text="कालयवन गुफा में आया। अँधेरे में सोए आदमी को देखा, और सोचा: यही कृष्ण है! सोने का नाटक कर रहा है।"),
        dict(id="rc13", text="उसने पूरी ताक़त से, सोते हुए राजा को, लात मारी।", gap=G),
        dict(id="rc14", text="राजा की नींद टूटी। उसने ग़ुस्से से आँखें खोलीं... और कालयवन, वहीं जलकर राख हो गया।"),
        dict(id="rc15", text="कृष्ण डरकर नहीं भागे थे। वो दुश्मन को, सीधे उसकी मौत तक ले गए थे।", gap=G),
        dict(id="rc15c", text="जिसे दुश्मन ने डरपोक कहा... उसी रणछोड़ ने, बिना हथियार उठाए, लड़ाई जीत ली।", gap=G),
        dict(id="rc16", text="तो कृष्ण का भागना: डर था, या दिमाग़? कमेंट में बताओ।"),
    ],
}
KN = {
    "rc1": "ಯೋಚಿಸಿ... ಕೃಷ್ಣ, ಯುದ್ಧ ಬಿಟ್ಟು ಓಡಿಹೋಗಿದ್ದ! ಅದಕ್ಕೇ ಅವನಿಗೆ ಒಂದು ಹೆಸರಿದೆ: ರಣಛೋಡ್.",
    "rc2": "ರಣ ಅಂದ್ರೆ ಯುದ್ಧ. ರಣಛೋಡ್ ಅಂದ್ರೆ, ಯುದ್ಧ ಬಿಟ್ಟು ಓಡಿದವನು. ಇದು ಭಾಗವತದ ನಿಜವಾದ ಕಥೆ.",
    "rc3": "ಒಂದು ಸಲ, ಕಾಲಯವನ ಅನ್ನೋ ಒಬ್ಬ ಕ್ರೂರ ರಾಜ, ಕೋಟಿಗಟ್ಟಲೆ ಸೈನಿಕರನ್ನ ಕರ್ಕೊಂಡು, ಕೃಷ್ಣನ ಊರಿನ ಮೇಲೆ ದಾಳಿ ಮಾಡಿದ.",
    "rc4": "ಕೃಷ್ಣ, ಯಾವ ಆಯುಧನೂ ಇಲ್ಲದೆ, ಒಬ್ಬನೇ ಹೊರಗೆ ಬಂದ.",
    "rc5": "ಕಾಲಯವನ ಅಂದ್ಕೊಂಡ: ಒಬ್ಬನೇ, ಆಯುಧನೂ ಇಲ್ಲ? ಇವನನ್ನ, ಕೈಯಲ್ಲೇ ಹಿಡ್ಕೊಳ್ತೀನಿ!",
    "rc6": "ಆದ್ರೆ ಅವನು ಹತ್ರ ಬಂದ ತಕ್ಷಣ... ಕೃಷ್ಣ, ಬೆನ್ನು ತೋರಿಸಿ ಓಡಿಹೋದ!",
    "rc7": "ಕಾಲಯವನ ಕೂಗಿದ: ಹೇಡಿ! ಎಲ್ಲಿಗೆ ಓಡ್ತೀಯ? ಅಂತ, ಅವನ ಹಿಂದೆ ಓಡಿದ.",
    "rc8": "ಕೃಷ್ಣ ಓಡ್ತಾನೇ ಇದ್ದ, ಅವನ ಕೈಗೆ ಸಿಗದಷ್ಟು ಸ್ವಲ್ಪ ಮುಂದೆ... ಆಮೇಲೆ, ಒಂದು ಕತ್ತಲೆ ಗುಹೆಯೊಳಗೆ ಹೋದ.",
    "rc8q": "ಹಾಗಾದ್ರೆ ಕೃಷ್ಣ, ನಿಜವಾಗಲೂ ಹೆದರಿದ್ನಾ?",
    "rc9": "ಆ ಗುಹೆಯಲ್ಲಿ, ತುಂಬಾ ವರ್ಷಗಳಿಂದ, ಒಬ್ಬ ರಾಜ ಮಲಗಿದ್ದ. ಅವನ ಹೆಸರು, ಮುಚುಕುಂದ.",
    "rc10": "ಅವನು ದೇವತೆಗಳಿಗಾಗಿ, ತುಂಬಾ ದೊಡ್ಡ ಯುದ್ಧ ಮಾಡಿದ್ದ. ಅದಕ್ಕೇ ದೇವತೆಗಳು ಅವನಿಗೆ ವರ ಕೊಟ್ರು: ಮನಸಾರೆ ನಿದ್ದೆ ಮಾಡು.",
    "rc11": "ಯಾರು ನಿನ್ನನ್ನ ಎಬ್ಬಿಸ್ತಾರೋ, ನಿನ್ನ ಕಣ್ಣು ಬಿದ್ದ ತಕ್ಷಣ, ಅವರು ಸುಟ್ಟು ಬೂದಿ ಆಗ್ತಾರೆ.",
    "rc12": "ಕಾಲಯವನ ಗುಹೆಗೆ ಬಂದ. ಕತ್ತಲಲ್ಲಿ ಮಲಗಿದ್ದವನನ್ನ ನೋಡಿ ಅಂದ್ಕೊಂಡ: ಇವನೇ ಕೃಷ್ಣ! ನಿದ್ದೆ ಮಾಡೋ ನಾಟಕ ಆಡ್ತಿದ್ದಾನೆ.",
    "rc13": "ಅವನು ಪೂರ್ತಿ ಶಕ್ತಿ ಹಾಕಿ, ಮಲಗಿದ್ದ ರಾಜನಿಗೆ, ಒದ್ದ.",
    "rc14": "ರಾಜನಿಗೆ ಎಚ್ಚರ ಆಯ್ತು. ಕೋಪದಿಂದ ಕಣ್ಣು ಬಿಟ್ಟ... ಕಾಲಯವನ, ಅಲ್ಲೇ ಸುಟ್ಟು ಬೂದಿ ಆದ.",
    "rc15": "ಕೃಷ್ಣ ಹೆದರಿ ಓಡಿರಲಿಲ್ಲ. ಅವನು ಶತ್ರುವನ್ನ, ನೇರವಾಗಿ ಅವನ ಸಾವಿನ ಹತ್ರ ಕರ್ಕೊಂಡು ಹೋಗಿದ್ದ.",
    "rc15c": "ಶತ್ರು ಹೇಡಿ ಅಂತ ಕರೆದ ಅದೇ ರಣಛೋಡ್... ಒಂದೂ ಆಯುಧ ಎತ್ತದೆ, ಯುದ್ಧ ಗೆದ್ದ.",
    "rc16": "ಹಾಗಾದ್ರೆ ಕೃಷ್ಣ ಓಡಿದ್ದು: ಭಯನಾ, ಅಥವಾ ಬುದ್ಧಿನಾ? ಕಾಮೆಂಟ್ ಮಾಡಿ ಹೇಳಿ.",
}
SCRIPTS["kn"] = [dict(line, text=KN[line["id"]]) for line in SCRIPTS["hi"]]   # same ids and pauses as Hindi

_SOURCES = ["Bhagavata Purana 10.50-51", "Vishnu Purana 5.23 (H. H. Wilson translation)"]
METADATA = {
    "hi": dict(
        title="Krishna yudh chhodkar bhaag gaye the",
        caption="Socho, Bhagwan Krishna yudh chhodkar bhaag gaye the... isiliye unka ek naam hai Ranchhod 😳\n\n"
                "Bhagavat Puran: Kalayavan karodon sainik lekar aaya. Krishna bina hathiyar ke nikle, aur bhaag gaye. "
                "Kalayavan ne peechha kiya, ek andheri gufa tak... jahan saalon se ek raja so raha tha.\n\n"
                "Krishna ka bhaagna: darr tha ya dimaag? Comment mein batao 👇",
        yt_title="Krishna Yudh Chhodkar Kyun Bhaage? 😳 | Ranchhod Ki Kahani | Bhagavat Puran",
        yt_description="Krishna ka ek naam hai Ranchhod, yaani yudh chhodkar bhaagne wala. Bhagavat Puran mein "
                       "Kalayavan karodon sainikon ke saath aata hai, Krishna bina hathiyar ke bahar nikalte hain aur "
                       "bhaag jaate hain. Kalayavan unka peechha karta hai ek andheri gufa tak, jahan Raja Muchukund "
                       "saalon se so rahe the. Devtaon ka vardaan tha: jo unhe jagaayega, woh jalkar raakh ho jaayega. "
                       "Kalayavan ne soye hue raja ko Krishna samajhkar laat maari...",
        hashtags=["#krishna", "#bhagavatpuran", "#mythology", "#kahani", "#hindu"],
        pinned_comment="Krishna ka bhaagna: darr tha, ya dimaag? 👇",
        sources=_SOURCES),
    "kn": dict(
        title="Krishna yuddha bittu odihoda",
        caption="Yochisi: Krishna yuddha bittu odihogidda... adakke avanige Ranchhod anno hesaride 😳\n\n"
                "Bhagavata: Kalayavana koti sainikarannu karkondu banda. Krishna aayudha illade horage banda, odida. "
                "Kalayavana ondu kattale guheya tanaka hinde bidda... alli varshagalinda ondu raja malagidda.\n\n"
                "Krishna odiddu: bhaya na, buddhi na? Comment maadi 👇",
        yt_title="Krishna Yuddha Bittu Odihoda 😳 | Ranchhod Kathe | Bhagavata",
        yt_description="Krishnanige Ranchhod anno hesaride, andre yuddha bittu odidavanu. Bhagavatadalli Kalayavana "
                       "koti sainikarannu karkondu baruttaane, Krishna aayudha illade horage bandu odi hogtaane. "
                       "Kalayavana avanannu ondu kattale guheya tanaka hinde biltaane, alli Muchukunda raja "
                       "varshagalinda malagidda. Devategala vara: avanannu ebbisidavaru suttu boodi aagtaare. "
                       "Kalayavana malagidda rajanannu Krishna andkondu oddabittu...",
        hashtags=["#kannada", "#krishna", "#bhagavata", "#kannadastory", "#mythology"],
        pinned_comment="Krishna odiddu: bhaya na, buddhi na? 👇",
        sources=_SOURCES),
}


USED_ASSETS, CREDITS_FILES = [], []      # everything in this video is drawn in code


def _scenes(tl):
    """Hindi: shadow puppets (scenes_ranchhod); Kannada: Yakshagana stage (scenes_ranchhod_yk), so the two channels
    never share pictures."""
    import importlib
    yk = getattr(tl, "lang", "hi") == "kn"
    return importlib.import_module("scenes_ranchhod_yk" if yk else "scenes_ranchhod")


def draw(cr, t, tl):
    _scenes(tl).draw(cr, t, tl)


def sfx(tl):
    return _scenes(tl).sfx(tl)
