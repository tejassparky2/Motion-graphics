"""Mythology video 16: the unborn baby who corrected his father from the womb (Ashtavakra). Impossible hook, a curse,
a deadly debate rule, a boy's victory and the drowned coming back (owner, 11 Nov 2026: "Make next 5 shorts all on
good topics"). Look: Togalu Gombeyaata shadow puppets; the drowning is shown as figures sinking into blue light, no
suffering. Calm sound.

Facts (Mahabharata, Vana Parva 132-134, K. M. Ganguli translation):
- 132: Kahoda reads all night; the child in the womb: "O father, thou hast been reading the whole night, but (of all
  that) thy reading doth not seem to me correct"; the father, insulted before his disciples: "Because thou speakest
  thus even while in the womb, therefore thou shalt be crooked in eight parts of the body." Kahoda "was there defeated
  in a controversy by Vandin" at Janaka's court and drowned; Ashtavakra learns this "in his twelfth year".
- 133: Vandin "after defeating (in controversy) men expert in discussion, causeth them to be drowned"; the boy is
  stopped at the gate and argues that learning, not years, makes one great; admitted.
- 134: the numbers debate from one to thirteen; Vandin loses: "I am King Varuna's son"; the Brahmanas were sent to
  Varuna's sacrifice; they rise before Janaka and Kahoda speaks; "enter into this river, Samanga", and "all his
  (crooked) limbs were immediately made straight".
"""
# (earlier) Rewritten 12 Nov 2026 for kid-level clarity (owner: "the hook needs to be strong and story clear so even a kid can understand"): max 3 names, one storyline, a concrete hook.
# Rewritten 12 Nov 2026 to 5-year-old level (owner: "I want story so clear and very good explained even a 5 year old can understand"): short sentences, everyday words, hard words explained.
from channel import ASSETS_ROOT, MUSIC, NARRATORS, NARRATOR_LABEL, REVEAL_GAP, TAIL  # noqa: F401

G = REVEAL_GAP
SCRIPTS = {
    "hi": [
        dict(id="a1", text="सोचो, एक बच्चा अभी पैदा भी नहीं हुआ था... और माँ के पेट के अंदर से बोला: पिताजी, आप गलत पढ़ रहे हो!", gap=G),
        dict(id="a2", text="ये महाभारत की सच्ची कहानी है।"),
        dict(id="a3", text="उस बच्चे के पिता, एक बड़े गुरु थे। रोज़ रात, बच्चों को पूजा के मंत्र पढ़ाते थे।"),
        dict(id="a4", text="एक रात, माँ के पेट से बच्चे की आवाज़ आई: पिताजी, ये मंत्र आप गलत पढ़ रहे हो।"),
        dict(id="a5", text="सब बच्चों के सामने, पिता को बहुत शर्म आई। और बहुत ग़ुस्सा भी।", gap=G),
        dict(id="a6", text="ग़ुस्से में पिता ने श्राप दिया, यानी बद्दुआ दी: तेरा शरीर आठ जगह से टेढ़ा हो जाएगा।"),
        dict(id="a7", text="और सच में, बच्चा टेढ़ा-मेढ़ा पैदा हुआ। उसका नाम पड़ा: अष्टावक्र। मतलब, आठ जगह से टेढ़ा।", gap=G),
        dict(id="a8", text="फिर एक दिन, पिता एक राजा के महल गए। वहाँ एक घमंडी पंडित था।"),
        dict(id="a9", text="उस पंडित का खेल था: सवाल-जवाब में जो हारेगा, उसे पानी में डुबो दिया जाएगा।", gap=G),
        dict(id="a10", text="पिता हार गए... और उन्हें पानी में डुबो दिया गया।"),
        dict(id="a10q", text="तो क्या वो बच्चा, अपने पिता को कभी देख पाएगा?"),
        dict(id="a11", text="बारह साल बाद, अष्टावक्र को ये बात पता चली। और वो अपने टेढ़े शरीर के साथ, उसी महल में पहुँच गया।"),
        dict(id="a12", text="दरवाज़े पर रोका गया: बच्चे अंदर नहीं आ सकते। अष्टावक्र बोला: कोई उम्र से बड़ा नहीं होता, अक्ल से बड़ा होता है।", gap=G),
        dict(id="a13", text="और उस छोटे से बच्चे ने, उस घमंडी पंडित को, सवाल-जवाब में हरा दिया।", gap=G),
        dict(id="a14", text="तब पंडित ने राज़ खोला: मैंने किसी को मारा नहीं। सब पानी के देवता के पास, ज़िंदा हैं।"),
        dict(id="a15", text="और पानी से, उसके पिता ज़िंदा लौट आए। पिता ने उसे नदी में नहलाया, और उसका शरीर बिल्कुल सीधा हो गया।", gap=G),
        dict(id="a15c", text="जिस बच्चे को पेट में बोलने की सज़ा मिली थी... उसी के बोलने ने, पिता को वापस ला दिया।", gap=G),
        dict(id="a16", text="तो गलती किसकी थी: पेट से बोलने वाले बेटे की, या ग़ुस्से वाले पिता की? कमेंट में बताओ।"),
    ],
}
KN = {
    "a1": "ಯೋಚಿಸಿ... ಒಂದು ಮಗು ಇನ್ನೂ ಹುಟ್ಟೇ ಇರಲಿಲ್ಲ... ಅಮ್ಮನ ಹೊಟ್ಟೆಯೊಳಗಿಂದ ಹೇಳ್ತು: ಅಪ್ಪಾ, ನೀವು ತಪ್ಪಾಗಿ ಓದ್ತಿದ್ದೀರ!",
    "a2": "ಇದು ಮಹಾಭಾರತದ ನಿಜವಾದ ಕಥೆ.",
    "a3": "ಆ ಮಗುವಿನ ಅಪ್ಪ ಒಬ್ಬ ದೊಡ್ಡ ಗುರು. ಪ್ರತಿ ರಾತ್ರಿ, ಮಕ್ಕಳಿಗೆ ಪೂಜೆಯ ಮಂತ್ರ ಹೇಳಿಕೊಡ್ತಿದ್ರು.",
    "a4": "ಒಂದು ರಾತ್ರಿ, ಅಮ್ಮನ ಹೊಟ್ಟೆಯಿಂದ ಮಗುವಿನ ಧ್ವನಿ ಬಂತು: ಅಪ್ಪಾ, ಈ ಮಂತ್ರ ನೀವು ತಪ್ಪಾಗಿ ಹೇಳ್ತಿದ್ದೀರ.",
    "a5": "ಎಲ್ಲ ಮಕ್ಕಳ ಮುಂದೆ, ಅಪ್ಪನಿಗೆ ತುಂಬಾ ನಾಚಿಕೆ ಆಯ್ತು. ತುಂಬಾ ಕೋಪನೂ ಬಂತು.",
    "a6": "ಕೋಪದಲ್ಲಿ ಅಪ್ಪ ಶಾಪ ಕೊಟ್ರು: ನಿನ್ನ ದೇಹ ಎಂಟು ಕಡೆ ಸೊಟ್ಟಗಾಗುತ್ತೆ.",
    "a7": "ನಿಜವಾಗಲೂ, ಮಗು ಸೊಟ್ಟಗೆ ಹುಟ್ಟಿತು. ಅದಕ್ಕೇ ಹೆಸರು: ಅಷ್ಟಾವಕ್ರ. ಅಂದ್ರೆ, ಎಂಟು ಕಡೆ ಸೊಟ್ಟ.",
    "a8": "ಆಮೇಲೆ ಒಂದು ದಿನ, ಅಪ್ಪ ಒಬ್ಬ ರಾಜನ ಅರಮನೆಗೆ ಹೋದ್ರು. ಅಲ್ಲಿ ಒಬ್ಬ ಜಂಭದ ಪಂಡಿತ ಇದ್ದ.",
    "a9": "ಆ ಪಂಡಿತನ ಆಟ: ಪ್ರಶ್ನೆ ಉತ್ತರದಲ್ಲಿ ಯಾರು ಸೋಲ್ತಾರೋ, ಅವರನ್ನ ನೀರಲ್ಲಿ ಮುಳುಗಿಸ್ತಾರೆ.",
    "a10": "ಅಪ್ಪ ಸೋತರು... ಅವರನ್ನ ನೀರಲ್ಲಿ ಮುಳುಗಿಸಿದ್ರು.",
    "a10q": "ಹಾಗಾದ್ರೆ ಆ ಮಗು, ತನ್ನ ಅಪ್ಪನನ್ನ ಯಾವತ್ತಾದ್ರೂ ನೋಡುತ್ತಾ?",
    "a11": "ಹನ್ನೆರಡು ವರ್ಷದ ನಂತರ, ಅಷ್ಟಾವಕ್ರನಿಗೆ ಈ ವಿಷಯ ಗೊತ್ತಾಯ್ತು. ಅವನು ತನ್ನ ಸೊಟ್ಟ ದೇಹದ ಜೊತೆ, ಅದೇ ಅರಮನೆಗೆ ಹೋದ.",
    "a12": "ಬಾಗಿಲಲ್ಲಿ ತಡೆದ್ರು: ಮಕ್ಕಳನ್ನ ಒಳಗೆ ಬಿಡಲ್ಲ. ಅಷ್ಟಾವಕ್ರ ಹೇಳಿದ: ವಯಸ್ಸಿಂದ ಯಾರೂ ದೊಡ್ಡವರಾಗಲ್ಲ, ಬುದ್ಧಿಯಿಂದ ದೊಡ್ಡವರಾಗ್ತಾರೆ.",
    "a13": "ಆ ಪುಟ್ಟ ಹುಡುಗ, ಆ ಜಂಭದ ಪಂಡಿತನನ್ನ, ಪ್ರಶ್ನೆ ಉತ್ತರದಲ್ಲಿ ಸೋಲಿಸಿದ.",
    "a14": "ಆಗ ಪಂಡಿತ ರಹಸ್ಯ ಹೇಳಿದ: ನಾನು ಯಾರನ್ನೂ ಕೊಂದಿಲ್ಲ. ಎಲ್ಲರೂ ನೀರಿನ ದೇವರ ಹತ್ರ ಜೀವಂತವಾಗಿದ್ದಾರೆ.",
    "a15": "ನೀರಿಂದ, ಅವನ ಅಪ್ಪ ಜೀವಂತವಾಗಿ ವಾಪಸ್ ಬಂದ್ರು. ಅಪ್ಪ ಅವನನ್ನ ನದಿಯಲ್ಲಿ ಸ್ನಾನ ಮಾಡಿಸಿದ್ರು, ಅವನ ದೇಹ ನೇರ ಆಯ್ತು.",
    "a15c": "ಹೊಟ್ಟೆಯಲ್ಲಿ ಮಾತಾಡಿದ್ದಕ್ಕೆ ಶಿಕ್ಷೆ ಸಿಕ್ಕ ಮಗು... ಅದೇ ಮಾತಿಂದ, ಅಪ್ಪನನ್ನ ವಾಪಸ್ ಕರ್ಕೊಂಡು ಬಂತು.",
    "a16": "ಹಾಗಾದ್ರೆ ತಪ್ಪು ಯಾರದ್ದು: ಹೊಟ್ಟೆಯಿಂದ ಮಾತಾಡಿದ ಮಗನದ್ದಾ, ಅಥವಾ ಕೋಪದ ಅಪ್ಪನದ್ದಾ? ಕಾಮೆಂಟ್ ಮಾಡಿ ಹೇಳಿ.",
}
SCRIPTS["kn"] = [dict(line, text=KN[line["id"]]) for line in SCRIPTS["hi"]]   # same ids and pauses as Hindi

_SOURCES = ["Mahabharata, Vana Parva, sections 132-134 (K. M. Ganguli translation)"]
METADATA = {
    "hi": dict(
        title="Maa ke pet se pita ki galti pakdi",
        caption="Socho, ek bachche ne maa ke pet ke andar se apne pita ki galti pakad li... aur pita ne use shraap de "
                "diya 😳\n\nMahabharat, Van Parva: aath jagah se tedha paida hua Ashtavakra, 12 saal ki umar mein Raja "
                "Janak ke darbaar mein us vidvaan ko hara aaya jo haarne waalon ko paani mein dubo deta tha.\n\n"
                "Galti kiski thi: bete ki ya pita ki? Comment mein batao 👇",
        yt_title="Maa Ke Pet Se Pita Ki Galti Pakdi 😳 | Ashtavakra Ki Katha | Mahabharat",
        yt_description="Kahod raat bhar ved padha rahe the, tab pet ke andar se bachcha bola ki aapka padhna sahi nahi "
                       "hai. Pita ne shraap diya ki tera shareer aath jagah se tedha hoga. Kahod Janak ke darbaar mein "
                       "Bandi se bahas haare aur paani mein dubo diye gaye. 12 saal baad Ashtavakra ne Bandi ko hara "
                       "diya, Bandi Varun ka beta nikla, saare brahman paani se laut aaye aur Samanga nadi mein "
                       "Ashtavakra ka shareer seedha ho gaya.",
        hashtags=["#mahabharat", "#ashtavakra", "#mythology", "#kahani", "#hindu"],
        pinned_comment="Galti kiski thi: pet mein bolne wale bete ki, ya shraap dene wale pita ki? 👇",
        sources=_SOURCES),
    "kn": dict(
        title="Hotteyalle appana tappu hidida magu",
        caption="Yochisi: ondu magu ammana hotteyolagindale tanna appana tappu hiditu... appa adakke shaapa kottru 😳"
                "\n\nMahabharata, Vana Parva: entu kade sottagaagi hutthida Ashtavakra, 12 varshadalli Janakana "
                "aasthanadalli sotavarannu neeralli mulugisuva panditanannu solisida.\n\n"
                "Tappu yaaraddu: magana, appana? Comment maadi 👇",
        yt_title="Hotteyalle Appana Tappu Hidida Magu 😳 | Ashtavakrana Kathe | Mahabharata",
        yt_description="Kahoda raatriyella veda helikodtidru, aaga hotteyolagininda magu helitu nimma odu sari illa "
                       "anta. Appa shaapa kottru ninna deha entu kade sottagaagutte anta. Kahoda Janakana aasthanadalli "
                       "Bandi jote vaadadalli sotu neeralli mulugidaru. 12 varshada nantara Ashtavakra Bandiyannu "
                       "solisida, Bandi Varunana maga, ella brahmanaru vaapas bandru, Samanga nadiyalli Ashtavakrana "
                       "deha nera aaytu.",
        hashtags=["#kannada", "#mahabharata", "#ashtavakra", "#kannadastory", "#mythology"],
        pinned_comment="Tappu yaaraddu: hotteyalli maataadida magana, athava shaapa kotta appana? 👇",
        sources=_SOURCES),
}


USED_ASSETS, CREDITS_FILES = [], []      # everything in this video is drawn in code


def _scenes(tl):
    """Hindi: shadow puppets (scenes_ashtavakra); Kannada: Yakshagana stage (scenes_ashtavakra_yk), so the two channels never share
    pictures."""
    import importlib
    yk = getattr(tl, "lang", "hi") == "kn"
    return importlib.import_module("scenes_ashtavakra_yk" if yk else "scenes_ashtavakra")


def draw(cr, t, tl):
    _scenes(tl).draw(cr, t, tl)


def sfx(tl):
    return _scenes(tl).sfx(tl)
