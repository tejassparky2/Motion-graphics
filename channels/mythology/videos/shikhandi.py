"""Mythology video 18: Amba, reborn to kill Bhishma, swaps bodies with a Yaksha (owner, 11 Nov 2026: "Make next 5
shorts all on good topics"). Body-impossible hook, revenge across two lives, a Yaksha's curse, and Bhishma himself
telling his enemies how to defeat him. Debate: who brought Bhishma down? Look: Togalu Gombeyaata shadow puppets;
the fire is a glow, the body swap a crossing of two lights; Bhishma falls on a bed of arrows as a silhouette.
Calm sound.

Facts (Mahabharata, Udyoga Parva 173-195 and Bhishma Parva 108, K. M. Ganguli translation):
- Bhishma carried off the Kasi princesses for Vichitravirya; Amba loved Salva, who refused her when she was let go.
- 189: years of austerities against Bhishma. 190: Rudra: "Thou shalt slay Bhishma, and even obtain manhood"; she
  "entered that blazing fire ... with a heart burning with wrath".
- 192-194: born to Drupada as a daughter, raised as a son and married to the daughter of the Dasarna king; the
  bride discovers it; her father prepares war; Sikhandini goes to a forest to end her life and meets the Yaksha
  Sthunakarna, who agrees to exchange sexes for a time.
- 195: Kuvera: "from this day, thou shalt remain a woman and she shall remain a man!"; "After Sikhandin's death ...
  this one will regain his own form!"
- Bhishma Parva 108: Bhishma tells the Pandavas Sikhandin "was a female before but subsequently obtained manhood";
  "let Arjuna, keeping Sikhandin before him, attack me with his sharp shafts"; he will never strike him.
"""
# (earlier) Rewritten 12 Nov 2026 for kid-level clarity (owner: "the hook needs to be strong and story clear so even a kid can understand"): max 3 names, one storyline, a concrete hook.
# Rewritten 12 Nov 2026 to 5-year-old level (owner: "I want story so clear and very good explained even a 5 year old can understand"): short sentences, everyday words, hard words explained.
from channel import ASSETS_ROOT, MUSIC, NARRATORS, NARRATOR_LABEL, REVEAL_GAP, TAIL  # noqa: F401

G = REVEAL_GAP
SCRIPTS = {
    "hi": [
        dict(id="b1", text="सोचो, भीष्म जैसे सबसे ताक़तवर योद्धा को, एक ऐसे योद्धा ने हराया... जो पिछले जन्म में एक लड़की थी।", gap=G),
        dict(id="b2", text="ये महाभारत की सच्ची कहानी है।"),
        dict(id="b3", text="भीष्म, एक बहुत ताक़तवर योद्धा थे। उन्हें कोई हरा नहीं सकता था।"),
        dict(id="b4", text="एक दिन भीष्म, अंबा नाम की एक राजकुमारी को ज़बरदस्ती उठा लाए, अपने छोटे भाई की शादी के लिए।"),
        dict(id="b5", text="पर अंबा किसी और राजा से प्यार करती थी। वो उसके पास गई, तो उस राजा ने भी कहा: अब मैं तुमसे शादी नहीं करूँगा।", gap=G),
        dict(id="b6", text="अंबा अकेली रह गई। उसे लगा, ये सब भीष्म की वजह से हुआ।"),
        dict(id="b7", text="उसने क़सम खाई: मैं भीष्म को हराकर रहूँगी।"),
        dict(id="b8", text="उसने सालों तक भगवान शिव की पूजा की। तब शिव जी आए, और बोले: अगले जन्म में, तुम भीष्म को हराओगी।", gap=G),
        dict(id="b9", text="अंबा ने आग में कूदकर, ये जन्म छोड़ दिया।"),
        dict(id="b10", text="अगले जन्म में वो एक राजा के घर, बेटी बनकर पैदा हुई। नाम था: शिखंडी।"),
        dict(id="b11", text="बड़ी होकर, जंगल के एक जादुई यक्ष ने, उसे अपना लड़के वाला शरीर दे दिया। अब शिखंडी, एक लड़का योद्धा बन गया।", gap=G),
        dict(id="b12", text="फिर बहुत बड़ा युद्ध हुआ। दस दिन तक, भीष्म को कोई नहीं हरा पाया।"),
        dict(id="b12q", text="तो भीष्म को हराया कैसे गया?"),
        dict(id="b13", text="भीष्म का एक नियम था: जो कभी लड़की रहा हो, उससे मैं नहीं लड़ूँगा।"),
        dict(id="b14", text="तो अर्जुन ने शिखंडी को, अपने रथ में सबसे आगे खड़ा कर दिया।", gap=G),
        dict(id="b15", text="भीष्म ने हथियार नीचे रख दिए। और अर्जुन के तीरों से, भीष्म गिर पड़े। अंबा का बदला पूरा हुआ।", gap=G),
        dict(id="b15c", text="जो लड़की भीष्म की वजह से रोई थी... वही अगले जन्म में, भीष्म की हार बनी।", gap=G),
        dict(id="b16", text="तो भीष्म को किसने हराया: अर्जुन ने, या अंबा ने? कमेंट में बताओ।"),
    ],
}
KN = {
    "b1": "ಯೋಚಿಸಿ... ಭೀಷ್ಮನಂಥ ಅತಿ ಶಕ್ತಿಶಾಲಿ ಯೋಧನನ್ನ ಒಬ್ಬ ಯೋಧ ಸೋಲಿಸಿದ... ಆ ಯೋಧ, ಹಿಂದಿನ ಜನ್ಮದಲ್ಲಿ ಒಬ್ಬ ಹುಡುಗಿ.",
    "b2": "ಇದು ಮಹಾಭಾರತದ ನಿಜವಾದ ಕಥೆ.",
    "b3": "ಭೀಷ್ಮ, ತುಂಬಾ ಶಕ್ತಿಶಾಲಿ ಯೋಧ. ಅವನನ್ನ ಯಾರೂ ಸೋಲಿಸೋಕಾಗ್ತಿರಲಿಲ್ಲ.",
    "b4": "ಒಂದು ದಿನ ಭೀಷ್ಮ, ಅಂಬೆ ಅನ್ನೋ ರಾಜಕುಮಾರಿಯನ್ನ ಬಲವಂತವಾಗಿ ಕರ್ಕೊಂಡು ಬಂದ, ತನ್ನ ತಮ್ಮನ ಮದುವೆಗೆ.",
    "b5": "ಆದ್ರೆ ಅಂಬೆ ಬೇರೆ ರಾಜನನ್ನ ಪ್ರೀತಿಸ್ತಿದ್ಳು. ಅವನ ಹತ್ರ ಹೋದಾಗ, ಆ ರಾಜನೂ ಹೇಳಿದ: ಈಗ ನಾನು ನಿನ್ನನ್ನ ಮದುವೆ ಆಗಲ್ಲ.",
    "b6": "ಅಂಬೆ ಒಂಟಿಯಾದ್ಳು. ಇದೆಲ್ಲ ಭೀಷ್ಮನಿಂದಾನೇ ಆಯ್ತು ಅಂತ ಅವಳಿಗೆ ಅನ್ನಿಸ್ತು.",
    "b7": "ಅವಳು ಶಪಥ ಮಾಡಿದ್ಳು: ನಾನು ಭೀಷ್ಮನನ್ನ ಸೋಲಿಸೇ ಸೋಲಿಸ್ತೀನಿ.",
    "b8": "ವರ್ಷಗಟ್ಟಲೆ ಶಿವನ ಪೂಜೆ ಮಾಡಿದ್ಳು. ಆಗ ಶಿವ ಬಂದು ಹೇಳಿದ: ಮುಂದಿನ ಜನ್ಮದಲ್ಲಿ, ನೀನು ಭೀಷ್ಮನನ್ನ ಸೋಲಿಸ್ತೀಯ.",
    "b9": "ಅಂಬೆ ಬೆಂಕಿಗೆ ಹಾರಿ, ಈ ಜನ್ಮ ಬಿಟ್ಟಳು.",
    "b10": "ಮುಂದಿನ ಜನ್ಮದಲ್ಲಿ ಅವಳು ಒಬ್ಬ ರಾಜನ ಮನೆಯಲ್ಲಿ, ಮಗಳಾಗಿ ಹುಟ್ಟಿದ್ಳು. ಹೆಸರು: ಶಿಖಂಡಿ.",
    "b11": "ದೊಡ್ಡವಳಾದ ಮೇಲೆ, ಕಾಡಿನ ಒಬ್ಬ ಮಾಯಾವಿ ಯಕ್ಷ, ತನ್ನ ಗಂಡಸಿನ ದೇಹವನ್ನ ಅವಳಿಗೆ ಕೊಟ್ಟ. ಈಗ ಶಿಖಂಡಿ, ಒಬ್ಬ ಗಂಡು ಯೋಧ.",
    "b12": "ಆಮೇಲೆ ದೊಡ್ಡ ಯುದ್ಧ ಬಂತು. ಹತ್ತು ದಿನ, ಯಾರಿಗೂ ಭೀಷ್ಮನನ್ನ ಸೋಲಿಸೋಕಾಗಲಿಲ್ಲ.",
    "b12q": "ಹಾಗಾದ್ರೆ ಭೀಷ್ಮನನ್ನ ಹೇಗೆ ಸೋಲಿಸಿದ್ರು?",
    "b13": "ಭೀಷ್ಮನಿಗೆ ಒಂದು ನಿಯಮ ಇತ್ತು: ಒಮ್ಮೆ ಹುಡುಗಿಯಾಗಿದ್ದವರ ಜೊತೆ, ನಾನು ಯುದ್ಧ ಮಾಡಲ್ಲ.",
    "b14": "ಅದಕ್ಕೆ ಅರ್ಜುನ, ಶಿಖಂಡಿಯನ್ನ ತನ್ನ ರಥದಲ್ಲಿ ಎಲ್ಲರಿಗಿಂತ ಮುಂದೆ ನಿಲ್ಲಿಸಿದ.",
    "b15": "ಭೀಷ್ಮ ಆಯುಧ ಕೆಳಗಿಟ್ಟ. ಅರ್ಜುನನ ಬಾಣಗಳಿಂದ, ಭೀಷ್ಮ ಬಿದ್ದ. ಅಂಬೆಯ ಸೇಡು ಪೂರ್ತಿ ಆಯ್ತು.",
    "b15c": "ಭೀಷ್ಮನಿಂದ ಅತ್ತ ಆ ಹುಡುಗಿನೇ... ಮುಂದಿನ ಜನ್ಮದಲ್ಲಿ, ಭೀಷ್ಮನ ಸೋಲಾದಳು.",
    "b16": "ಹಾಗಾದ್ರೆ ಭೀಷ್ಮನನ್ನ ಸೋಲಿಸಿದ್ದು ಯಾರು: ಅರ್ಜುನನಾ, ಅಥವಾ ಅಂಬೆನಾ? ಕಾಮೆಂಟ್ ಮಾಡಿ ಹೇಳಿ.",
}
SCRIPTS["kn"] = [dict(line, text=KN[line["id"]]) for line in SCRIPTS["hi"]]   # same ids and pauses as Hindi

_SOURCES = ["Mahabharata, Udyoga Parva, sections 173-195 (K. M. Ganguli translation)",
            "Mahabharata, Bhishma Parva, section 108"]
METADATA = {
    "hi": dict(
        title="Bhishma ko maarne ke liye ladki ladka bani",
        caption="Socho, ek ladki ne Bhishma ko maarne ke liye doosra janm liya... aur phir ek yaksh se apna shareer hi "
                "badal liya 😳\n\nMahabharat, Udyog Parv: Amba, Shikhandini, yaksh Sthunakarna aur Kuber ka shraap. "
                "Aur Bhishma ne khud Pandavon ko bataya ki unhe kaise giraaya jaaye.\n\n"
                "Bhishma ko kisne giraaya: Arjun ya Amba? Comment mein batao 👇",
        yt_title="Bhishma Ko Maarne Ke Liye Ladki Ladka Bani 😳 | Amba Aur Shikhandi | Mahabharat",
        yt_description="Bhishma ki wajah se Amba ki zindagi barbaad hui. Shiv ji ne vardaan diya ki woh Bhishma ko "
                       "maaregi aur purush banegi. Agle janm mein Drupad ki beti Shikhandini, bete ki tarah paali gayi, "
                       "aur jungle mein yaksh Sthunakarna se shareer badalkar Shikhandi bani. Kuber ne yaksh ko shraap "
                       "diya. Yuddh mein Bhishma ne khud bataya ki Shikhandi pehle stree tha, aur Arjun ne Shikhandi ko "
                       "aage rakhkar baan chalaaye.",
        hashtags=["#mahabharat", "#bhishma", "#mythology", "#kahani", "#hindu"],
        pinned_comment="Bhishma ko kisne giraaya: Arjun ne, ya Amba ne? 👇",
        sources=_SOURCES),
    "kn": dict(
        title="Bheeshmanannu kolloke hudugi gandasaadalu",
        caption="Yochisi: obba hudugi Bheeshmanannu kolloke innondu janma tagondlu... aamele obba yakshana jote tanna "
                "dehane badalaayisikondlu 😳\n\nMahabharata, Udyoga Parva: Ambe, Shikhandini, yaksha Sthunakarna "
                "mattu Kuberana shaapa. Bheeshma taane Pandavarige helida avanannu hege beelisabeku anta.\n\n"
                "Bheeshmanannu beelisiddu yaaru: Arjuna na, Ambe na? Comment maadi 👇",
        yt_title="Bheeshmanannu Kolloke Hudugi Gandasaadalu 😳 | Ambe Mattu Shikhandi | Mahabharata",
        yt_description="Bheeshmanindaagi Ambeya jeevana haalaaytu. Shiva vara kotta, avalu Bheeshmanannu koltaale, "
                       "gandasu aagtaale anta. Mundina janmadalli Drupadana magalu Shikhandini, maganante belesalpattalu, "
                       "kaadinalli yaksha Sthunakarnana jote deha badalaayisi Shikhandi aadalu. Kubera yakshanige "
                       "shaapa kotta. Yuddhadalli Bheeshma taane helida Shikhandi modalu hennaagidda anta, Arjuna "
                       "Shikhandiyannu munde nillisi baana bitta.",
        hashtags=["#kannada", "#mahabharata", "#bhishma", "#kannadastory", "#mythology"],
        pinned_comment="Bheeshmanannu beelisiddu yaaru: Arjuna na, athava Ambe na? 👇",
        sources=_SOURCES),
}


USED_ASSETS, CREDITS_FILES = [], []      # everything in this video is drawn in code


def _scenes(tl):
    """Hindi: shadow puppets (scenes_shikhandi); Kannada: Yakshagana stage (scenes_shikhandi_yk), so the two channels never share
    pictures."""
    import importlib
    yk = getattr(tl, "lang", "hi") == "kn"
    return importlib.import_module("scenes_shikhandi_yk" if yk else "scenes_shikhandi")


def draw(cr, t, tl):
    _scenes(tl).draw(cr, t, tl)


def sfx(tl):
    return _scenes(tl).sfx(tl)
