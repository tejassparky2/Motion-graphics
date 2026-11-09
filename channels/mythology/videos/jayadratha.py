"""Mythology video 9: "To kill me, Krishna had to hide the sun": Jayadratha tells his own death (owner, 9 Nov 2026: "no everyone
knows it not only born type videos go for all any krishna intellegent sakuni history or any unknown events"). A
little-known clever turn, told simply, ending in a fair debate (clever or a trick?). Look: Togalu Gombeyaata shadow
puppets; the beheading is never shown in gore: an arrow, a flash, the head as a small dark silhouette in flight.
Calm sound.

Facts (Mahabharata, Drona Parva, Jayadratha-vadha, K. M. Ganguli translation):
- Abhimanyu dies inside Drona's formation after Jayadratha holds back the Pandavas at its mouth; Arjuna vows to
  slay Jayadratha before the next sunset or enter fire himself.
- Krishna: "Without vanquishing those six car-warriors ... thou wilt never be able to slay the ruler of the Sindhus
  ... I shall, therefore, resort to Yoga for shrouding the sun"; "having taken recourse to Yoga, created that
  darkness"; "Thy warriors, O king, thinking the sun to have set were filled with delight at the prospect of
  Partha's laying down his life"; Jayadratha looks up at the sun; Krishna tells Arjuna to strike.
- At Jayadratha's birth a voice foretold his beheading; his father Vriddhakshatra declared that whoever made his
  son's head fall to the ground would have his own head "crack into a hundred pieces". Krishna: "throw that head
  ... upon the lap of Vriddhakshatra himself"; the father, at his evening prayers, does not see it; "as the latter
  ... stood up after finishing his prayers it suddenly fell down on the earth" and his head cracked into a hundred
  pieces (chapter 145 in the Krishna-kosh numbering).
- "that darkness ... was withdrawn by Vasudeva ... the darkness, they had seen, had all been an illusion produced
  by Vasudeva."
"""
from channel import ASSETS_ROOT, MUSIC, NARRATORS, NARRATOR_LABEL, REVEAL_GAP, TAIL  # noqa: F401

# Owner, 9 Nov 2026 (reference reel "Raja Bali ki katha"): "Narration and hooks like this": the character tells his
# own story in the first person; a cold open on the climax's shouted line; a proud impossible claim ("to kill me,
# Krishna had to hide the sun"); short emotional sentences, ~50 s; a twist question at the end ("अब बताओ, ...?").
SCRIPTS = {
    "hi": [
        dict(id="y1", text="अर्जुन! सूरज अभी डूबा नहीं है!", gap=REVEAL_GAP),
        dict(id="y2", text="मैं जयद्रथ हूँ, सिंधु का राजा। और मुझे मारने के लिए... कृष्ण को सूरज छिपाना पड़ा।", gap=REVEAL_GAP),
        dict(id="y3", text="चक्रव्यूह के दरवाज़े पर, मैंने पांडवों को रोका था। अंदर, अभिमन्यु मारा गया।"),
        dict(id="y4", text="अर्जुन ने क़सम खाई: कल सूरज ढलने से पहले जयद्रथ मरेगा... वरना मैं आग में कूद जाऊँगा।"),
        dict(id="y5", text="पूरी कौरव सेना ने मुझे अपने बीच छिपा लिया। और शाम हो गई।"),
        dict(id="y6", text="फिर अचानक, अंधेरा छा गया। सब चिल्लाए: सूरज डूब गया!", gap=REVEAL_GAP),
        dict(id="y7", text="मैं ख़ुशी से बाहर आया, आसमान देखने।"),
        dict(id="y8", text="तभी वो आवाज़ आई: अर्जुन, सूरज अभी डूबा नहीं है!", gap=REVEAL_GAP),
        dict(id="y9", text="पर मेरी एक ढाल थी। मेरे पिता ने कहा था: जो मेरे बेटे का सिर ज़मीन पर गिराएगा, उसका अपना सिर सौ "
                           "टुकड़ों में फट जाएगा।"),
        dict(id="y10", text="कृष्ण ये जानते थे।", gap=REVEAL_GAP),
        dict(id="y11", text="अर्जुन के तीर ने मेरा सिर उड़ाया... और दूर पूजा कर रहे मेरे पिता की गोद में गिरा दिया।"),
        dict(id="y12", text="पिता उठे। सिर ज़मीन पर गिरा।", gap=REVEAL_GAP),
        dict(id="y13", text="और उनका अपना ही श्राप... उन्हीं पर गिरा।", gap=REVEAL_GAP),
        dict(id="y14", text="जो श्राप मुझे बचाने के लिए था... उसी ने मेरे पिता की जान ले ली। अब बताओ, ग़लती किसकी थी?"),
    ],
    "kn": [
        dict(id="y1", text="ಅರ್ಜುನ! ಸೂರ್ಯ ಇನ್ನೂ ಮುಳುಗಿಲ್ಲ!", gap=REVEAL_GAP),
        dict(id="y2", text="ನಾನು ಜಯದ್ರಥ, ಸಿಂಧು ದೇಶದ ರಾಜ. ನನ್ನನ್ನ ಕೊಲ್ಲೋಕೆ... ಕೃಷ್ಣ ಸೂರ್ಯನನ್ನೇ ಮುಚ್ಚಬೇಕಾಯ್ತು.",
             gap=REVEAL_GAP),
        dict(id="y3", text="ಚಕ್ರವ್ಯೂಹದ ಬಾಗಿಲಲ್ಲಿ, ನಾನು ಪಾಂಡವರನ್ನ ತಡೆದೆ. ಒಳಗೆ, ಅಭಿಮನ್ಯು ಸತ್ತುಹೋದ."),
        dict(id="y4", text="ಅರ್ಜುನ ಪ್ರತಿಜ್ಞೆ ಮಾಡಿದ: ನಾಳೆ ಸೂರ್ಯ ಮುಳುಗೋದ್ರೊಳಗೆ ಜಯದ್ರಥ ಸಾಯ್ತಾನೆ... ಇಲ್ಲಾಂದ್ರೆ ನಾನೇ ಬೆಂಕಿಗೆ "
                           "ಹಾರ್ತೀನಿ."),
        dict(id="y5", text="ಇಡೀ ಕೌರವ ಸೈನ್ಯ ನನ್ನನ್ನ ತಮ್ಮ ನಡುವೆ ಬಚ್ಚಿಟ್ಟುಕೊಂಡಿತು. ಸಂಜೆ ಆಯ್ತು."),
        dict(id="y6", text="ಇದ್ದಕ್ಕಿದ್ದಂತೆ, ಕತ್ತಲು ಆವರಿಸ್ತು. ಎಲ್ಲರೂ ಕೂಗಿದ್ರು: ಸೂರ್ಯ ಮುಳುಗಿದ!", gap=REVEAL_GAP),
        dict(id="y7", text="ನಾನು ಖುಷಿಯಿಂದ, ಆಕಾಶ ನೋಡೋಕೆ ಹೊರಗೆ ಬಂದೆ."),
        dict(id="y8", text="ಆಗಲೇ ಆ ಧ್ವನಿ ಕೇಳಿಸ್ತು: ಅರ್ಜುನ, ಸೂರ್ಯ ಇನ್ನೂ ಮುಳುಗಿಲ್ಲ!", gap=REVEAL_GAP),
        dict(id="y9", text="ಆದ್ರೆ ನನಗೊಂದು ರಕ್ಷೆ ಇತ್ತು. ನನ್ನ ತಂದೆ ಹೇಳಿದ್ರು: ಯಾರು ನನ್ನ ಮಗನ ತಲೆಯನ್ನ ನೆಲಕ್ಕೆ ಬೀಳಿಸ್ತಾರೋ, ಅವರ "
                           "ತಲೆ ನೂರು ಚೂರಾಗುತ್ತೆ."),
        dict(id="y10", text="ಇದು ಕೃಷ್ಣನಿಗೆ ಗೊತ್ತಿತ್ತು.", gap=REVEAL_GAP),
        dict(id="y11", text="ಅರ್ಜುನನ ಬಾಣ ನನ್ನ ತಲೆ ಹಾರಿಸಿತು... ದೂರದಲ್ಲಿ ಪೂಜೆ ಮಾಡ್ತಿದ್ದ ನನ್ನ ತಂದೆಯ ತೊಡೆ ಮೇಲೆ ಬೀಳಿಸಿತು."),
        dict(id="y12", text="ತಂದೆ ಎದ್ರು. ತಲೆ ನೆಲಕ್ಕೆ ಬಿತ್ತು.", gap=REVEAL_GAP),
        dict(id="y13", text="ಅವರ ಶಾಪವೇ... ಅವರ ಮೇಲೆ ಬಿತ್ತು.", gap=REVEAL_GAP),
        dict(id="y14", text="ನನ್ನನ್ನ ಕಾಪಾಡೋಕೆ ಇದ್ದ ಶಾಪವೇ, ನನ್ನ ತಂದೆಯ ಪ್ರಾಣ ತೆಗೆಯಿತು. ಈಗ ಹೇಳಿ, ತಪ್ಪು ಯಾರದ್ದು?"),
    ],
}

_SOURCES = ["Mahabharata, Drona Parva, Jayadratha-vadha (K. M. Ganguli translation)"]
METADATA = {
    "hi": dict(
        title="Mujhe maarne ke liye Krishna ko suraj chhupana pada",
        caption="Main Jayadrath hoon. Aur mujhe maarne ke liye... Krishna ko suraj chhupana pada 😳\n\n"
                "Mahabharat, Drona Parva: Arjun ki kasam thi, suraj dhalne se pehle Jayadrath ko maaroonga, warna aag "
                "mein kood jaaunga. Krishna ne suraj dhak diya, Jayadrath bahar aaya, aur Arjun ke teer ne uska sir "
                "uske pita ki god mein gira diya.\n\n"
                "Ab batao, galti kiski thi? Comment mein batao 👇",
        yt_title="Mujhe Maarne Ke Liye Krishna Ko Suraj Chhupana Pada 😳 | Jayadrath | Mahabharat",
        yt_description="Jayadrath ki zubaani: chakravyuh ke darwaze par usne Pandavon ko roka, Abhimanyu maara gaya, aur "
                       "Arjun ne kasam khaayi ki suraj dhalne se pehle use maarega. Shaam ko Krishna ne yoga-maya se suraj "
                       "dhak diya; Jayadrath bahar aaya. Uske pita ka shraap tha ki jo uske bete ka sir zameen par "
                       "giraayega, uska sir sau tukdon mein phatega; Arjun ka teer sir ko pita ki god mein le gaya.",
        hashtags=["#mahabharat", "#krishna", "#jayadrath", "#mythology", "#kahani"],
        pinned_comment="Ab batao, galti kiski thi? 👇",
        sources=_SOURCES),
    "kn": dict(
        title="Nannannu kolloke Krishna sooryananne muchchabekaaytu",
        caption="Naanu Jayadratha. Nannannu kolloke... Krishna sooryananne muchchabekaaytu 😳\n\n"
                "Mahabharata, Drona Parva: Arjuna pratijne maadidda, soorya mulugodrolage Jayadrathanannu koltini, "
                "illaandre bengige haartini. Krishna sooryanannu muchchida, Jayadratha horage banda, Arjunana baana avana "
                "taleyannu tandeya tode mele beelisitu.\n\n"
                "Eega heli, tappu yaardu? Comment maadi 👇",
        yt_title="Nannannu Kolloke Krishna Sooryananne Muchchabekaaytu 😳 | Jayadratha | Mahabharata",
        yt_description="Jayadrathana baayalli: chakravyuhada baagilalli avanu Pandavarannu tadeda, Abhimanyu satta, Arjuna "
                       "soorya mulugodrolage avanannu kolluve anta pratijne maadida. Sanje Krishna yogamaayeyinda "
                       "sooryanannu muchchida; Jayadratha horage banda. Avana tandeya shaapa: yaaru nanna magana taleyannu "
                       "nelakke beelisutaaro avara tale nooru chooraaguttade; Arjunana baana taleyannu tandeya tode mele "
                       "beelisitu.",
        hashtags=["#kannada", "#mahabharata", "#krishna", "#kannadastory", "#mythology"],
        pinned_comment="Eega heli, tappu yaardu? 👇",
        sources=_SOURCES),
}


USED_ASSETS, CREDITS_FILES = [], []      # everything in this video is drawn in code


def draw(cr, t, tl):
    from scenes_jayadratha import draw as _draw
    _draw(cr, t, tl)


def sfx(tl):
    from scenes_jayadratha import sfx as _sfx
    return _sfx(tl)
