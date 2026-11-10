"""Mythology video 11: Ruru gives half his life to bring his dead bride back (owner, 10 Nov 2026: "i dont want you to
focus on only one type of story i want you to ecplore all intresting ones", then "first make 1 short then we will go
for long one auto approved"). A love story after three Krishna-trick reels; a twist (the vow against snakes, the
harmless old snake who was a cursed sage) and a personal-stake question at the end.
Look: Togalu Gombeyaata shadow puppets; the snakebite is never shown in detail (a strike, a flash, she falls softly).
Calm sound.

Facts (Mahabharata, Adi Parva, Pauloma sub-book, K. M. Ganguli translation, sections 8-12):
- 8: Pramadvara, betrothed to Ruru (son of the sage Pramati), "trod upon a serpent which she did not perceive as it
  lay in coil" and died before the wedding; "Ruru, mortified beyond measure, retired" into the forest.
- 9: a messenger of the gods: one "whose days have run out can never come back to life"; but "Resign half of thy own
  life to thy bride." Ruru: "I most willingly offer a moiety of my own life in favour of my bride." Dharma (Yama):
  "let Pramadvara ... rise up endued with a moiety of Ruru's life"; she rose "as from her slumber"; they married.
  Ruru vowed to destroy serpents and killed every one he saw.
- 9-11: an old Dundubha: "I have done thee no harm"; Dundubhas are "serpents only in name" (no venom). He was a Rishi
  who, as a joke, frightened his friend Khagama with a snake made of grass and was cursed: "thou shalt be turned
  even into a venomless serpent", to be freed on meeting Ruru. Restored, he teaches: "the highest virtue of man is
  sparing the life of others."
"""
from channel import ASSETS_ROOT, MUSIC, NARRATORS, NARRATOR_LABEL, REVEAL_GAP, TAIL  # noqa: F401

SCRIPTS = {
    "hi": [
        dict(id="r1", text="सोचो, एक लड़के ने अपनी आधी उम्र देकर... अपनी मरी हुई दुल्हन को ज़िंदा कर लिया।", gap=REVEAL_GAP),
        dict(id="r2", text="ये कोई फ़िल्मी कहानी नहीं है। ये महाभारत के आदि पर्व में लिखा है।"),
        dict(id="r3", text="रुरु एक ऋषि का बेटा था। उसकी शादी, प्रमद्वरा नाम की लड़की से तय हुई थी।"),
        dict(id="r4", text="पर शादी से कुछ दिन पहले, उसका पैर घास में छिपे एक साँप पर पड़ गया।"),
        dict(id="r5", text="साँप ने डस लिया... और प्रमद्वरा वहीं मर गई।", gap=REVEAL_GAP),
        dict(id="r6", text="रुरु जंगल में जाकर रोया। बोला: अगर मैंने कभी कोई पुण्य किया है, तो वो वापस आ जाए।"),
        dict(id="r7", text="तभी देवताओं का एक दूत आया। बोला: जिसकी उम्र ख़त्म हो गई, वो वापस नहीं आता।"),
        dict(id="r8", text="पर एक रास्ता है। अपनी आधी उम्र, उसे दे दो।", gap=REVEAL_GAP),
        dict(id="r9", text="रुरु ने एक पल भी नहीं सोचा। बोला: मेरी आधी उम्र, उसकी।", gap=REVEAL_GAP),
        dict(id="r10", text="यमराज ने हाँ कहा। और प्रमद्वरा ऐसे उठी, जैसे नींद से जागी हो।", gap=REVEAL_GAP),
        dict(id="r11", text="दोनों की शादी हुई। पर रुरु की अपनी ज़िंदगी, आधी रह गई।"),
        dict(id="r12", text="फिर रुरु ने क़सम खाई: जो भी साँप दिखेगा, उसे मार दूँगा।"),
        dict(id="r13", text="एक दिन उसने एक बूढ़े साँप पर डंडा उठाया। साँप बोला: मैंने तुम्हारा क्या बिगाड़ा? मुझमें तो ज़हर भी "
                            "नहीं।", gap=REVEAL_GAP),
        dict(id="r14", text="वो साँप असल में एक ऋषि था। मज़ाक में उसने दोस्त को घास का नकली साँप दिखाकर डराया था, तो दोस्त ने "
                            "श्राप दिया: जा, तू ख़ुद बिना ज़हर का साँप बन जा।"),
        dict(id="r15", text="रुरु से मिलते ही वो फिर ऋषि बन गया, और बोला: किसी की जान न लेना, सबसे बड़ा धर्म है।",
             gap=REVEAL_GAP),
        dict(id="r16", text="क्या तुम किसी के लिए अपनी आधी उम्र दे सकते हो? हाँ या ना, कमेंट में बताओ।"),
    ],
    "kn": [
        dict(id="r1", text="ಯೋಚಿಸಿ... ಒಬ್ಬ ಹುಡುಗ ತನ್ನ ಅರ್ಧ ಆಯಸ್ಸು ಕೊಟ್ಟು... ಸತ್ತುಹೋದ ತನ್ನ ಮದುಮಗಳನ್ನ ಬದುಕಿಸಿದ.",
             gap=REVEAL_GAP),
        dict(id="r2", text="ಇದು ಸಿನಿಮಾ ಕಥೆ ಅಲ್ಲ. ಮಹಾಭಾರತದ ಆದಿ ಪರ್ವದಲ್ಲೇ ಇದೆ."),
        dict(id="r3", text="ರುರು ಒಬ್ಬ ಋಷಿಯ ಮಗ. ಅವನ ಮದುವೆ, ಪ್ರಮದ್ವರಾ ಅನ್ನೋ ಹುಡುಗಿ ಜೊತೆ ನಿಶ್ಚಯ ಆಗಿತ್ತು."),
        dict(id="r4", text="ಆದ್ರೆ ಮದುವೆಗೆ ಕೆಲವು ದಿನ ಮುಂಚೆ, ಅವಳ ಕಾಲು ಹುಲ್ಲಲ್ಲಿ ಅಡಗಿದ್ದ ಒಂದು ಹಾವಿನ ಮೇಲೆ ಬಿತ್ತು."),
        dict(id="r5", text="ಹಾವು ಕಚ್ಚಿತು... ಪ್ರಮದ್ವರಾ ಅಲ್ಲೇ ಸತ್ತುಹೋದಳು.", gap=REVEAL_GAP),
        dict(id="r6", text="ರುರು ಕಾಡಿಗೆ ಹೋಗಿ ಅತ್ತ. ಹೇಳಿದ: ನಾನು ಯಾವತ್ತಾದ್ರೂ ಪುಣ್ಯ ಮಾಡಿದ್ರೆ, ಅವಳು ವಾಪಸ್ ಬರಲಿ."),
        dict(id="r7", text="ಆಗ ದೇವತೆಗಳ ಒಬ್ಬ ದೂತ ಬಂದ. ಹೇಳಿದ: ಆಯಸ್ಸು ಮುಗಿದವರು ವಾಪಸ್ ಬರೋದಿಲ್ಲ."),
        dict(id="r8", text="ಆದ್ರೆ ಒಂದು ದಾರಿ ಇದೆ. ನಿನ್ನ ಅರ್ಧ ಆಯಸ್ಸನ್ನ ಅವಳಿಗೆ ಕೊಡು.", gap=REVEAL_GAP),
        dict(id="r9", text="ರುರು ಒಂದು ಕ್ಷಣನೂ ಯೋಚಿಸಲಿಲ್ಲ. ಹೇಳಿದ: ನನ್ನ ಅರ್ಧ ಆಯಸ್ಸು, ಅವಳದ್ದು.", gap=REVEAL_GAP),
        dict(id="r10", text="ಯಮಧರ್ಮ ಒಪ್ಪಿದ. ಪ್ರಮದ್ವರಾ, ನಿದ್ದೆಯಿಂದ ಎದ್ದ ಹಾಗೆ ಎದ್ದಳು.", gap=REVEAL_GAP),
        dict(id="r11", text="ಇಬ್ಬರ ಮದುವೆ ಆಯ್ತು. ಆದ್ರೆ ರುರುವಿನ ಸ್ವಂತ ಆಯಸ್ಸು, ಅರ್ಧ ಆಯ್ತು."),
        dict(id="r12", text="ಆಮೇಲೆ ರುರು ಪ್ರತಿಜ್ಞೆ ಮಾಡಿದ: ಕಂಡ ಕಂಡ ಹಾವನ್ನೆಲ್ಲ ಕೊಲ್ತೀನಿ."),
        dict(id="r13", text="ಒಂದು ದಿನ ಒಂದು ಮುದಿ ಹಾವಿನ ಮೇಲೆ ಕೋಲು ಎತ್ತಿದ. ಹಾವು ಹೇಳ್ತು: ನಾನೇನು ಮಾಡಿದೆ? ನನ್ನಲ್ಲಿ ವಿಷನೂ ಇಲ್ಲ.",
             gap=REVEAL_GAP),
        dict(id="r14", text="ಆ ಹಾವು ನಿಜವಾಗಿ ಒಬ್ಬ ಋಷಿ. ತಮಾಷೆಗೆ ಹುಲ್ಲಿನ ನಕಲಿ ಹಾವು ತೋರಿಸಿ ಸ್ನೇಹಿತನನ್ನ ಹೆದರಿಸಿದ್ದ. ಸ್ನೇಹಿತ "
                            "ಶಾಪ ಕೊಟ್ಟ: ಹೋಗು, ನೀನೇ ವಿಷ ಇಲ್ಲದ ಹಾವಾಗು."),
        dict(id="r15", text="ರುರುವನ್ನ ಭೇಟಿಯಾದ ತಕ್ಷಣ, ಅವನು ಮತ್ತೆ ಋಷಿ ಆದ. ಹೇಳಿದ: ಯಾರ ಜೀವನೂ ತೆಗೀಬಾರದು, ಅದೇ ದೊಡ್ಡ ಧರ್ಮ.",
             gap=REVEAL_GAP),
        dict(id="r16", text="ನೀವು ಯಾರಿಗಾದ್ರೂ ನಿಮ್ಮ ಅರ್ಧ ಆಯಸ್ಸು ಕೊಡ್ತೀರಾ? ಹೌದಾ ಇಲ್ವಾ, ಕಾಮೆಂಟ್ ಮಾಡಿ ಹೇಳಿ."),
    ],
}

_SOURCES = ["Mahabharata, Adi Parva, sections 8-12 (K. M. Ganguli translation)"]
METADATA = {
    "hi": dict(
        title="Aadhi umar dekar dulhan ko zinda kiya",
        caption="Socho, ek ladke ne apni aadhi umar dekar apni mari hui dulhan ko zinda kar liya 😳\n\n"
                "Mahabharat, Adi Parva: shaadi se pehle Pramadvara ko saanp ne das liya. Devataon ke doot ne kaha, "
                "ek hi raasta hai: apni aadhi umar use de do. Ruru ne ek pal bhi nahi socha. Phir aaya ek budha saanp "
                "jisme zeher hi nahi tha...\n\n"
                "Kya tum kisi ke liye apni aadhi umar de sakte ho? Haan ya na, comment mein batao 👇",
        yt_title="Apni Aadhi Umar Dekar Dulhan Ko Zinda Kiya 😳 | Ruru Aur Pramadvara | Mahabharat",
        yt_description="Rishi ka beta Ruru, Pramadvara se shaadi karne wala tha. Shaadi se kuch din pehle ghaas mein "
                       "chhupe saanp ne use das liya. Devataon ke doot ne kaha, jiski umar khatam ho gayi woh wapas "
                       "nahi aata, par ek raasta hai: apni aadhi umar use de do. Ruru ne de di, Yamraj ne haan kaha, "
                       "aur Pramadvara jaise neend se jaagi. Phir Ruru ne har saanp ko maarne ki kasam khaayi, jab tak "
                       "ek budhe, bina zeher ke saanp ne use sabse bada dharm nahi sikhaya.",
        hashtags=["#mahabharat", "#lovestory", "#mythology", "#kahani", "#hindu"],
        pinned_comment="Kya tum kisi ke liye apni aadhi umar de sakte ho? Haan ya na? 👇",
        sources=_SOURCES),
    "kn": dict(
        title="Ardha aayassu kottu madumagalannu badukisida",
        caption="Yochisi: obba huduga tanna ardha aayassu kottu, sattuhoda madumagalannu badukisida 😳\n\n"
                "Mahabharata, Adi Parva: maduvege munche Pramadvarage haavu kachchitu. Devategala doota helida, onde "
                "daari ide: ninna ardha aayassu avalige kodu. Ruru ondu kshananu yochisalilla. Aamele banthu ondu mudi "
                "haavu, adralli vishane irlilla...\n\n"
                "Neevu yaarigaadru nimma ardha aayassu kodteera? Houda illva, comment maadi 👇",
        yt_title="Ardha Aayassu Kottu Madumagalannu Badukisida 😳 | Ruru Pramadvara | Mahabharata",
        yt_description="Rishiya maga Ruru, Pramadvara jote maduve nishchaya aagittu. Maduvege kelavu dina munche "
                       "hullalli adagidda haavu avalige kachchitu. Devategala doota helida: aayassu mugidavaru vaapas "
                       "barolla, aadre ondu daari ide, ninna ardha aayassu avalige kodu. Ruru kotta, Yamadharma oppida, "
                       "Pramadvara nidde inda eddahaage eddalu. Aamele Ruru kanda haavannella kolteeni anda, ondu mudi, "
                       "vishavilladha haavu avanige doddha dharma kalisovaregu.",
        hashtags=["#kannada", "#mahabharata", "#lovestory", "#kannadastory", "#mythology"],
        pinned_comment="Neevu yaarigaadru nimma ardha aayassu kodteera? Houda illva? 👇",
        sources=_SOURCES),
}


USED_ASSETS, CREDITS_FILES = [], []      # everything in this video is drawn in code


def draw(cr, t, tl):
    from scenes_ruru import draw as _draw
    _draw(cr, t, tl)


def sfx(tl):
    from scenes_ruru import sfx as _sfx
    return _sfx(tl)
