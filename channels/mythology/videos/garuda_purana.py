"""Mythology video 14: what happens after death, according to the Garuda Purana (owner, 11 Nov 2026: "Or garada puran
what happens after dead"). Impossible-sounding hook (a thumb-sized soul; a new body built from rice-balls in ten
days), a journey with stakes (the river of blood, the boat only for cow-givers, the judgment) and an open belief
question at the end. Told as "the Garuda Purana says", never as proven fact. Look: Togalu Gombeyaata shadow puppets;
the Vaitarani is dark red water, never gore; Yama's messengers are fearsome silhouettes, not monsters. Calm sound.

Facts (Garuda Purana, Preta Kalpa / Saroddhara, Wood & Subrahmanyam translation 1911, chapters I-III):
- I.32: "The man of the size of a thumb, crying out 'oh, oh,' is dragged from the body by the servants of Yama."
- I.41: "Having seen the fearful Yama, the man, after a time, by command of Yama, swiftly comes back through the air."
- I.47-53: the son offers rice-balls for ten days; "By the rice-ball of the first day the head is formed", then the
  neck and shoulders (2), heart (3), back (4), navel (5), hips and secret parts (6), thighs (7), knees and feet (8-9),
  hunger and thirst (10).
- I.56-59: "The extent of the way of Yama measures eighty-six thousand Yojanas", 16 cities before the city of Yama.
- II.3-4: no water or food on the road; II.51: sons offer monthly rice-balls; II.82: near Yama's abode "at the end
  of the year".
- II.15-16: "the terribly horrible Vaitarani River ... Extending a hundred yojanas, a flow of pus and blood";
  II.66-67: "If you have made the gift of a cow, then the boat will come to you, otherwise not."
- III: Chitragupta reports each person's deeds; Yama judges.
"""
from channel import ASSETS_ROOT, MUSIC, NARRATORS, NARRATOR_LABEL, REVEAL_GAP, TAIL  # noqa: F401

G = REVEAL_GAP
SCRIPTS = {
    "hi": [
        dict(id="p1", text="सोचो, मरने के बाद आत्मा अंगूठे जितनी छोटी हो जाती है... और दस दिन में, चावल के पिंडों से उसका "
                           "नया शरीर बनता है।", gap=G),
        dict(id="p2", text="ये कोई फ़िल्मी कहानी नहीं है। ये गरुड़ पुराण में लिखा है।"),
        dict(id="p3", text="गरुड़ पुराण कहता है: मौत के समय, यमराज के दूत आते हैं।"),
        dict(id="p4", text="वो अंगूठे जितनी आत्मा को, शरीर से खींचकर बाहर निकालते हैं। आत्मा चिल्लाती है: हाय, हाय!"),
        dict(id="p5", text="दूत उसे यमराज के सामने ले जाते हैं। और फिर यमराज के हुक्म से, आत्मा हवा में उड़कर वापस घर "
                           "लौट आती है।", gap=G),
        dict(id="p6", text="आत्मा अपने शरीर में वापस जाना चाहती है। पर जा नहीं पाती। अब उसका कोई शरीर नहीं है।"),
        dict(id="p7", text="तब बेटा दस दिन तक, चावल के पिंड चढ़ाता है। और हर पिंड से, नए शरीर का एक हिस्सा बनता है।",
             gap=G),
        dict(id="p8", text="पहले दिन सिर। दूसरे दिन गर्दन और कंधे। तीसरे दिन दिल। चौथे दिन पीठ।"),
        dict(id="p9", text="पाँचवें दिन नाभि। फिर कमर, जांघें, घुटने, और पैर।"),
        dict(id="p10", text="और दसवें दिन... भूख और प्यास।", gap=G),
        dict(id="p11", text="फिर शुरू होता है यमराज की नगरी का सफ़र। छियासी हज़ार योजन लंबा रास्ता, सोलह नगर, और लगभग "
                            "एक साल।"),
        dict(id="p12", text="रास्ते में न पानी है, न खाना। आत्मा बस उन पिंडों के सहारे चलती है, जो घरवाले हर महीने चढ़ाते "
                            "हैं।"),
        dict(id="p13", text="और बीच रास्ते में आती है, वैतरणी नदी। सौ योजन चौड़ी, जिसमें पानी नहीं, ख़ून और पीप बहता है।",
             gap=G),
        dict(id="p14", text="उसे पार करने के लिए एक नाव आती है। पर सिर्फ़ उनके लिए, जिन्होंने ज़िंदगी में गाय दान की हो।",
             gap=G),
        dict(id="p15", text="आख़िर में, चित्रगुप्त हर एक काम का हिसाब पढ़ते हैं। और यमराज फ़ैसला सुनाते हैं।"),
        dict(id="p16", text="गरुड़ पुराण के मुताबिक, मरने के बाद यही सफ़र होता है। आप इसे मानते हो? हाँ या ना, कमेंट में "
                            "बताओ।"),
    ],
}
KN = {
    "p1": "ಯೋಚಿಸಿ... ಸತ್ತ ಮೇಲೆ ಆತ್ಮ ಹೆಬ್ಬೆರಳಿನಷ್ಟು ಚಿಕ್ಕದಾಗುತ್ತೆ... ಹತ್ತು ದಿನದಲ್ಲಿ, ಅನ್ನದ ಪಿಂಡಗಳಿಂದ ಅದಕ್ಕೆ ಹೊಸ "
          "ದೇಹ ಆಗುತ್ತೆ.",
    "p2": "ಇದು ಸಿನಿಮಾ ಕಥೆ ಅಲ್ಲ. ಗರುಡ ಪುರಾಣದಲ್ಲೇ ಇದೆ.",
    "p3": "ಗರುಡ ಪುರಾಣ ಹೇಳುತ್ತೆ: ಸಾವಿನ ಸಮಯದಲ್ಲಿ, ಯಮನ ದೂತರು ಬರ್ತಾರೆ.",
    "p4": "ಅವರು ಹೆಬ್ಬೆರಳಿನಷ್ಟು ಆತ್ಮವನ್ನ, ದೇಹದಿಂದ ಎಳೆದು ಹೊರಗೆ ತೆಗೀತಾರೆ. ಆತ್ಮ ಕೂಗುತ್ತೆ: ಅಯ್ಯೋ, ಅಯ್ಯೋ!",
    "p5": "ದೂತರು ಅದನ್ನ ಯಮನ ಮುಂದೆ ಕರ್ಕೊಂಡು ಹೋಗ್ತಾರೆ. ಆಮೇಲೆ ಯಮನ ಆಜ್ಞೆಯಿಂದ, ಆತ್ಮ ಗಾಳಿಯಲ್ಲಿ ಹಾರಿ ಮನೆಗೆ ವಾಪಸ್ "
          "ಬರುತ್ತೆ.",
    "p6": "ಆತ್ಮ ತನ್ನ ದೇಹದ ಒಳಗೆ ಮತ್ತೆ ಹೋಗೋಕೆ ನೋಡುತ್ತೆ. ಆದ್ರೆ ಆಗಲ್ಲ. ಈಗ ಅದಕ್ಕೆ ದೇಹನೇ ಇಲ್ಲ.",
    "p7": "ಆಗ ಮಗ ಹತ್ತು ದಿನ, ಅನ್ನದ ಪಿಂಡ ಇಡ್ತಾನೆ. ಪ್ರತಿ ಪಿಂಡದಿಂದ, ಹೊಸ ದೇಹದ ಒಂದು ಭಾಗ ಆಗುತ್ತೆ.",
    "p8": "ಮೊದಲ ದಿನ ತಲೆ. ಎರಡನೇ ದಿನ ಕುತ್ತಿಗೆ ಮತ್ತು ಭುಜ. ಮೂರನೇ ದಿನ ಹೃದಯ. ನಾಲ್ಕನೇ ದಿನ ಬೆನ್ನು.",
    "p9": "ಐದನೇ ದಿನ ಹೊಕ್ಕುಳು. ಆಮೇಲೆ ಸೊಂಟ, ತೊಡೆ, ಮಂಡಿ, ಮತ್ತು ಕಾಲು.",
    "p10": "ಹತ್ತನೇ ದಿನ... ಹಸಿವು ಮತ್ತು ಬಾಯಾರಿಕೆ.",
    "p11": "ಆಮೇಲೆ ಶುರುವಾಗುತ್ತೆ ಯಮಪುರಿಯ ಪ್ರಯಾಣ. ಎಂಬತ್ತಾರು ಸಾವಿರ ಯೋಜನದ ದಾರಿ, ಹದಿನಾರು ನಗರಗಳು, ಸುಮಾರು ಒಂದು ವರ್ಷ.",
    "p12": "ದಾರಿಯಲ್ಲಿ ನೀರೂ ಇಲ್ಲ, ಊಟನೂ ಇಲ್ಲ. ಮನೆಯವರು ಪ್ರತಿ ತಿಂಗಳು ಇಡೋ ಪಿಂಡಗಳ ಬಲದಿಂದಲೇ, ಆತ್ಮ ನಡೆಯುತ್ತೆ.",
    "p13": "ದಾರಿ ಮಧ್ಯದಲ್ಲಿ ಬರುತ್ತೆ, ವೈತರಣಿ ನದಿ. ನೂರು ಯೋಜನ ಅಗಲ, ಅದರಲ್ಲಿ ನೀರಲ್ಲ, ರಕ್ತ ಮತ್ತು ಕೀವು ಹರಿಯುತ್ತೆ.",
    "p14": "ಅದನ್ನ ದಾಟೋಕೆ ಒಂದು ದೋಣಿ ಬರುತ್ತೆ. ಆದ್ರೆ ಜೀವನದಲ್ಲಿ ಹಸು ದಾನ ಮಾಡಿದವರಿಗೆ ಮಾತ್ರ.",
    "p15": "ಕೊನೆಗೆ, ಚಿತ್ರಗುಪ್ತ ಪ್ರತಿ ಕೆಲಸದ ಲೆಕ್ಕ ಓದ್ತಾರೆ. ಯಮ ತೀರ್ಪು ಕೊಡ್ತಾನೆ.",
    "p16": "ಗರುಡ ಪುರಾಣದ ಪ್ರಕಾರ, ಸತ್ತ ಮೇಲೆ ಇದೇ ಪ್ರಯಾಣ ಆಗುತ್ತೆ. ನೀವು ಇದನ್ನ ನಂಬ್ತೀರಾ? ಹೌದಾ ಇಲ್ವಾ, ಕಾಮೆಂಟ್ ಮಾಡಿ ಹೇಳಿ.",
}
SCRIPTS["kn"] = [dict(line, text=KN[line["id"]]) for line in SCRIPTS["hi"]]   # same ids and pauses as Hindi

_SOURCES = ["Garuda Purana, Preta Kalpa (Saroddhara), chapters 1-3 (Wood & Subrahmanyam translation)"]
METADATA = {
    "hi": dict(
        title="Marne ke baad kya hota hai: Garuda Puran",
        caption="Socho, marne ke baad aatma angoothe jitni chhoti ho jaati hai... aur das din mein chawal ke pindon "
                "se uska naya shareer banta hai 😳\n\nGaruda Puran: pehle din sir, dasve din bhookh aur pyaas. Phir "
                "86,000 yojan ka safar, khoon ki nadi Vaitarani, aur Chitragupt ka hisaab.\n\n"
                "Aap ise maante ho? Haan ya na, comment mein batao 👇",
        yt_title="Marne Ke Baad Kya Hota Hai? 😳 | Garuda Puran Ka Safar",
        yt_description="Garuda Puran ke mutabik maut ke samay Yamraj ke doot angoothe jitni aatma ko shareer se "
                       "nikaalte hain. Das din tak bete ke chadhaaye pindon se naya shareer banta hai: pehle din sir, "
                       "dasve din bhookh aur pyaas. Phir 86,000 yojan, 16 nagar aur lagbhag ek saal ka safar, beech "
                       "mein Vaitarani nadi jise sirf gaay daan karne wale naav se paar karte hain, aur aakhir mein "
                       "Chitragupt ka hisaab.",
        hashtags=["#garudapuran", "#afterlife", "#mythology", "#kahani", "#hindu"],
        pinned_comment="Aap Garuda Puran ki ye baat maante ho? Haan ya na? 👇",
        sources=_SOURCES),
    "kn": dict(
        title="Satta mele enaagutte: Garuda Purana",
        caption="Yochisi: satta mele aatma hebberalinashtu chikkadaagutte... hattu dinadalli annada pindagalinda "
                "adakke hosa deha aagutte 😳\n\nGaruda Purana: modala dina tale, hattane dina hasivu mattu "
                "baayarike. Aamele 86,000 yojanada prayaana, rakthada nadi Vaitarani, mattu Chitraguptana lekka.\n\n"
                "Neevu idannu nambteera? Houda illva, comment maadi 👇",
        yt_title="Satta Mele Enaagutte? 😳 | Garuda Puranada Prayaana",
        yt_description="Garuda Puranada prakaara saavina samayadalli Yamana dootaru hebberalinashtu aatmavannu dehadinda "
                       "horage teegutaare. Hattu dina maga idoo pindagalinda hosa deha aagutte: modala dina tale, "
                       "hattane dina hasivu mattu baayarike. Aamele 86,000 yojana, 16 nagaragalu mattu sumaaru ondu "
                       "varshada prayaana, madhyadalli Vaitarani nadi, adannu hasu daana maadidavaru maatra doniyalli "
                       "daatutaare, koneyalli Chitraguptana lekka.",
        hashtags=["#kannada", "#garudapurana", "#afterlife", "#kannadastory", "#mythology"],
        pinned_comment="Neevu Garuda Puranada ee maatu nambteera? Houda illva? 👇",
        sources=_SOURCES),
}


USED_ASSETS, CREDITS_FILES = [], []      # everything in this video is drawn in code


def draw(cr, t, tl):
    from scenes_garuda_purana import draw as _draw
    _draw(cr, t, tl)


def sfx(tl):
    from scenes_garuda_purana import sfx as _sfx
    return _sfx(tl)
