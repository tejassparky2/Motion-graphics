"""Mythology video 9: 100 sons from one lump of flesh: Gandhari and the 101 pots (owner, 9 Nov 2026: "Next video",
after asking for stories "interesting mind blowing shocking like jarasanda one"; the previous script was "Auto
approved"). One clear story, one step per sentence. Look: the Togalu Gombeyaata shadow puppets of the Jarasandha
reel; the womb blow is shown as a flash, never as violence in detail. Calm sound (render_myth.calm_sfx).

Facts (Mahabharata, Adi Parva, Sambhava Parva, sections CXV-CXVI, K. M. Ganguli translation, Project Gutenberg
#7864): Vyasa grants Gandhari "a century of sons"; she "bore the burden in her womb for two long years without being
delivered"; she hears that Kunti "had brought forth a son"; "deprived of reason by grief, she struck her womb with
great violence"; out comes "a hard mass of flesh like unto an iron ball"; "When she was about to throw it away,
Dwaipayana ... came there"; "Let a hundred pots full of clarified butter be brought instantly ... let cool water be
sprinkled over this ball of flesh"; it divided "into a hundred and one parts, each about the size of the thumb";
the pots were to be opened "after full two years"; Duryodhana is born first and "began to cry and bray like an ass",
and "asses, vultures, jackals and crows uttered their respective cries"; Vidura and the Brahmanas: "he shall be the
exterminator of thy race ... abandon him"; Dhritarashtra "out of affection for his son had not the heart to follow
that advice"; "within a month, were born a full hundred sons ... and a daughter also" (CXV); the extra part became
the daughter Duhsala (CXVI).
"""
from channel import ASSETS_ROOT, MUSIC, NARRATORS, NARRATOR_LABEL, REVEAL_GAP, TAIL  # noqa: F401

SCRIPTS = {
    "hi": [
        dict(id="g1", text="सोचो, एक माँ ने बच्चे की जगह... मांस का एक सख़्त गोला जन्म दिया। और उसी गोले से, सौ बेटे पैदा हुए।",
             gap=REVEAL_GAP),
        dict(id="g2", text="ये किसी की गढ़ी हुई कहानी नहीं है। ये महाभारत के आदि पर्व में लिखा है।"),
        dict(id="g3", text="गांधारी को व्यास ऋषि से वरदान मिला था: तुम्हारे सौ बेटे होंगे।"),
        dict(id="g4", text="गांधारी गर्भवती हुईं। पर दो साल बीत गए... और बच्चा पैदा ही नहीं हुआ।"),
        dict(id="g5", text="तभी ख़बर आई: कुंती के बेटा हुआ है।"),
        dict(id="g6", text="दुख में, गांधारी ने अपने ही पेट पर ज़ोर से वार किया।", gap=REVEAL_GAP),
        dict(id="g7", text="और बाहर आया... बच्चा नहीं, बल्कि लोहे जैसा सख़्त, मांस का एक गोला।", gap=REVEAL_GAP),
        dict(id="g8", text="गांधारी उसे फेंकने ही वाली थीं, कि व्यास ऋषि आ गए।"),
        dict(id="g9", text="उन्होंने कहा: घी से भरे सौ घड़े लाओ, और इस गोले पर ठंडा पानी छिड़को।"),
        dict(id="g10", text="पानी पड़ते ही, गोला एक सौ एक टुकड़ों में बँट गया। हर टुकड़ा, अंगूठे जितना।", gap=REVEAL_GAP),
        dict(id="g11", text="हर टुकड़ा, घी के एक घड़े में रखा गया। और घड़े, दो साल तक बंद रहे।"),
        dict(id="g12", text="दो साल बाद, घड़ों में से सबसे पहले निकला... दुर्योधन।", gap=REVEAL_GAP),
        dict(id="g13", text="जन्म लेते ही वो गधे की तरह रेंका। और चारों तरफ़, गीदड़, गिद्ध और कौवे चीख़ने लगे।"),
        dict(id="g14", text="विदुर ने कहा: ये बच्चा पूरे कुल का नाश करेगा। इसे त्याग दो।"),
        dict(id="g15", text="पर धृतराष्ट्र ने बेटे के मोह में, ये बात नहीं मानी।", gap=REVEAL_GAP),
        dict(id="g16", text="एक महीने में सौ बेटे पैदा हुए... और एक सौ एकवें टुकड़े से, एक बेटी: दुःशला।"),
        dict(id="g17", text="अगर धृतराष्ट्र ने विदुर की बात मान ली होती, तो क्या महाभारत का युद्ध होता? यस या नो, कमेंट में "
                            "बताओ।"),
    ],
    "kn": [
        dict(id="g1", text="ಯೋಚಿಸಿ... ಒಬ್ಬ ತಾಯಿ ಮಗುವಿನ ಬದಲು... ಮಾಂಸದ ಒಂದು ಗಟ್ಟಿ ಉಂಡೆಗೆ ಜನ್ಮ ಕೊಟ್ಟಳು. ಅದೇ ಉಂಡೆಯಿಂದ, "
                           "ನೂರು ಮಕ್ಕಳು ಹುಟ್ಟಿದ್ರು.", gap=REVEAL_GAP),
        dict(id="g2", text="ಇದು ಯಾರೋ ಕಟ್ಟಿದ ಕಥೆ ಅಲ್ಲ. ಮಹಾಭಾರತದ ಆದಿ ಪರ್ವದಲ್ಲೇ ಇದೆ."),
        dict(id="g3", text="ಗಾಂಧಾರಿಗೆ ವ್ಯಾಸ ಋಷಿಗಳು ವರ ಕೊಟ್ಟಿದ್ರು: ನಿನಗೆ ನೂರು ಮಕ್ಕಳು ಆಗ್ತಾರೆ."),
        dict(id="g4", text="ಗಾಂಧಾರಿ ಗರ್ಭಿಣಿ ಆದ್ಲು. ಆದ್ರೆ ಎರಡು ವರ್ಷ ಕಳೆದ್ರೂ... ಮಗು ಹುಟ್ಟಲೇ ಇಲ್ಲ."),
        dict(id="g5", text="ಆಗ ಸುದ್ದಿ ಬಂತು: ಕುಂತಿಗೆ ಮಗ ಹುಟ್ಟಿದ."),
        dict(id="g6", text="ದುಃಖದಲ್ಲಿ, ಗಾಂಧಾರಿ ತನ್ನ ಹೊಟ್ಟೆಗೇ ಜೋರಾಗಿ ಹೊಡ್ಕೊಂಡ್ಲು.", gap=REVEAL_GAP),
        dict(id="g7", text="ಹೊರಗೆ ಬಂದಿದ್ದು... ಮಗು ಅಲ್ಲ. ಕಬ್ಬಿಣದ ತರ ಗಟ್ಟಿಯಾದ, ಮಾಂಸದ ಒಂದು ಉಂಡೆ.", gap=REVEAL_GAP),
        dict(id="g8", text="ಗಾಂಧಾರಿ ಅದನ್ನ ಎಸೆಯೋಕೆ ಹೊರಟಾಗ, ವ್ಯಾಸರು ಬಂದ್ರು."),
        dict(id="g9", text="ಅವರು ಹೇಳಿದ್ರು: ತುಪ್ಪ ತುಂಬಿದ ನೂರು ಮಡಿಕೆ ತನ್ನಿ. ಈ ಉಂಡೆ ಮೇಲೆ ತಣ್ಣೀರು ಚಿಮುಕಿಸಿ."),
        dict(id="g10", text="ನೀರು ಬಿದ್ದ ತಕ್ಷಣ, ಉಂಡೆ ನೂರಾ ಒಂದು ತುಂಡುಗಳಾಯ್ತು. ಒಂದೊಂದೂ, ಹೆಬ್ಬೆರಳಿನಷ್ಟು.", gap=REVEAL_GAP),
        dict(id="g11", text="ಒಂದೊಂದು ತುಂಡನ್ನೂ ತುಪ್ಪದ ಒಂದೊಂದು ಮಡಿಕೆಯಲ್ಲಿ ಇಟ್ರು. ಮಡಿಕೆಗಳು ಎರಡು ವರ್ಷ ಮುಚ್ಚಿದ್ವು."),
        dict(id="g12", text="ಎರಡು ವರ್ಷದ ನಂತರ, ಮಡಿಕೆಗಳಿಂದ ಮೊದಲು ಬಂದವನು... ದುರ್ಯೋಧನ.", gap=REVEAL_GAP),
        dict(id="g13", text="ಹುಟ್ಟಿದ ತಕ್ಷಣ ಅವನು ಕತ್ತೆ ತರ ಕಿರುಚಿದ. ಸುತ್ತಲೂ ನರಿಗಳು, ರಣಹದ್ದುಗಳು, ಕಾಗೆಗಳು ಕೂಗೋಕೆ ಶುರು "
                            "ಮಾಡಿದ್ವು."),
        dict(id="g14", text="ವಿದುರ ಹೇಳಿದ: ಈ ಮಗು ಇಡೀ ವಂಶವನ್ನೇ ನಾಶ ಮಾಡುತ್ತೆ. ಇವನನ್ನ ಬಿಟ್ಟುಬಿಡಿ."),
        dict(id="g15", text="ಆದ್ರೆ ಮಗನ ಮೇಲಿನ ಪ್ರೀತಿಯಿಂದ, ಧೃತರಾಷ್ಟ್ರ ಆ ಮಾತು ಕೇಳಲಿಲ್ಲ.", gap=REVEAL_GAP),
        dict(id="g16", text="ಒಂದು ತಿಂಗಳಲ್ಲಿ ನೂರು ಮಕ್ಕಳು ಹುಟ್ಟಿದ್ರು... ನೂರಾ ಒಂದನೇ ತುಂಡಿನಿಂದ, ಒಬ್ಬ ಮಗಳು: ದುಶ್ಶಲೆ."),
        dict(id="g17", text="ಧೃತರಾಷ್ಟ್ರ ವಿದುರನ ಮಾತು ಕೇಳಿದ್ರೆ, ಮಹಾಭಾರತ ಯುದ್ಧ ನಡೀತಿತ್ತಾ? ಹೌದಾ ಇಲ್ವಾ, ಕಾಮೆಂಟ್ ಮಾಡಿ ಹೇಳಿ."),
    ],
}

_SOURCES = ["Mahabharata, Adi Parva, Sambhava Parva CXV-CXVI (K. M. Ganguli translation)"]
METADATA = {
    "hi": dict(
        title="Maans ke ek gole se paida hue 100 bete",
        caption="Socho, ek maa ne bachche ki jagah maans ka ek sakht gola janma diya... aur usi gole se 100 bete paida "
                "hue 😳\n\n"
                "Mahabharat, Adi Parva: do saal ki garbhavastha ke baad Gandhari ne apne pet par vaar kiya. Vyas rishi ne "
                "us gole ke 101 tukde karke ghee ke ghadon mein rakhe. Do saal baad sabse pehle nikla Duryodhan.\n\n"
                "Agar Dhritarashtra ne Vidur ki baat maan li hoti, toh kya Mahabharat ka yuddh hota? YES ya NO, comment "
                "mein batao 👇",
        yt_title="Maans Ke Ek Gole Se Paida Hue 100 Bete 😳 | Gandhari Aur Duryodhan | Mahabharat",
        yt_description="Gandhari do saal tak garbhvati rahi. Kunti ke bete ki khabar sunkar usne apne pet par vaar kiya, "
                       "aur lohe jaisa sakht maans ka gola bahar aaya. Vyas rishi ne thanda paani chhidakwaya, gola 101 "
                       "tukdon mein banta, har tukda ghee ke ghade mein do saal rakha gaya. Pehle nikla Duryodhan, jo "
                       "gadhe ki tarah renka; Vidur ne use tyaagne ko kaha, par Dhritarashtra nahi maane.",
        hashtags=["#mahabharat", "#gandhari", "#duryodhan", "#mythology", "#kahani"],
        pinned_comment="Agar Dhritarashtra ne Vidur ki baat maan li hoti, toh kya Mahabharat ka yuddh hota? 👇",
        sources=_SOURCES),
    "kn": dict(
        title="Maamsada ondu undeyinda huttida 100 makkalu",
        caption="Yochisi: obba taayi maguvina badalu maamsada ondu gatti undege janma kottalu... ade undeyinda nooru "
                "makkalu huttidru 😳\n\n"
                "Mahabharata, Adi Parva: eradu varsha garbhini aagidda Gandhari tanna hottege hodkondlu. Vyasaru aa "
                "undeyannu 101 tundu maadi tuppada madikegalalli ittru. Eradu varshada nantara modalu banda Duryodhana.\n\n"
                "Dhritarashtra Vidurana maatu kelidre, Mahabharata yuddha nadeetitta? Houda illva, comment maadi 👇",
        yt_title="Maamsada Ondu Undeyinda Huttida 100 Makkalu 😳 | Gandhari Mattu Duryodhana | Mahabharata",
        yt_description="Gandhari eradu varsha garbhini aagiddlu. Kuntige maga huttida suddi kelida mele tanna hottege "
                       "hodkondlu, kabbinada tara gatti maamsada unde horage bantu. Vyasaru tanniru chimukisidaaga unde "
                       "101 tundaaytu, ondondu tuppada madikeyalli eradu varsha ittru. Modalu banda Duryodhana katte tara "
                       "kiruchida; Vidura avanannu bittubidi anda, aadre Dhritarashtra kelalilla.",
        hashtags=["#kannada", "#mahabharata", "#gandhari", "#kannadastory", "#mythology"],
        pinned_comment="Dhritarashtra Vidurana maatu kelidre, Mahabharata yuddha nadeetitta? Houda illva? 👇",
        sources=_SOURCES),
}

USED_ASSETS, CREDITS_FILES = [], []      # everything in this video is drawn in code


def draw(cr, t, tl):
    from scenes_gandhari import draw as _draw
    _draw(cr, t, tl)


def sfx(tl):
    from scenes_gandhari import sfx as _sfx
    return _sfx(tl)
