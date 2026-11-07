"""Mythology video 5: Ravana lost twice before Rama: to King Kartavirya Arjuna, and to Vali, who carried him under his
arm across the oceans. Made the week the Ramayana Part 1 film came out (5-6 Nov 2026, Yash as Ravana); the reel
claims nothing about the film and its Ravana is a leather puppet, never an actor's face. Script approved by the
owner (7 Nov 2026: "ok for ramayana script"). Look: Karnataka's Togalu Gombeyaata leather shadow puppets on a
lamp-lit screen, like the Jarasandha reel (owner, 7 Nov 2026: "The jarasanda video animation did good").

Facts (Valmiki Ramayana, Uttara Kanda; sarga numbers of the common Southern/Gita Press text, sections in M. N. Dutt's
1894 translation in brackets):
- Sarga 16 (XVI): at Kailasa, Ravana laughs at Nandi's monkey-like form; Nandi: "monkeys endowed with prowess, and
  possessed of my form and energy shall be born ... for compassing the destruction of thy race". (The same sarga has
  Ravana lifting Kailasa and Shiva pressing it down with his toe; not used.)
- Sargas 31-33 (XXXVII-XXXVIII): on the Narmada, King Arjuna of the Haihayas (Kartavirya, of Mahishmati), "in order to
  measure the strength of his thousand arms", obstructs the river; the stream carries away the flowers Ravana had
  gathered to worship Shiva; Arjuna captures and binds Ravana and takes him to his capital; Pulastya, Ravana's
  grandfather, comes to Mahishmati and Arjuna releases him.
- Sarga 34 (XXXIX): Vali at his twilight devotions by the southern ocean; Ravana approaches to seize him; Vali,
  "placing him under his arm-pit", rises into the sky and does his devotions at the western, northern and eastern
  oceans, "having journeyed over many thousand leagues"; back at Kishkindha he lets Ravana go and the two make
  friends before a lit fire.
- Hanuman burning Lanka (Sundara Kanda) and the vanara army reaching Lanka (Yuddha Kanda) close the curse callback.
The Uttara Kanda is the Ramayana's last book; the reel names it as the source.
"""
from channel import ASSETS_ROOT, MUSIC, NARRATORS, NARRATOR_LABEL, REVEAL_GAP, TAIL  # noqa: F401

SCRIPTS = {
    "hi": [
        dict(id="r1", text="सोचो, जिस रावण से देवता भी काँपते थे... उसे एक वानर ने बगल में दबाया, और चारों समुद्र घुमा दिए।",
             gap=REVEAL_GAP),
        dict(id="r2", text="ये कोई फ़िल्म का सीन नहीं है। ये वाल्मीकि रामायण के उत्तर कांड में लिखा है।"),
        dict(id="r3", text="और राम से पहले, रावण एक नहीं, दो बार हार चुका था।", gap=REVEAL_GAP),
        dict(id="r4", text="ब्रह्मा जी से वरदान मिलने के बाद, रावण पूरी दुनिया जीतने निकला।"),
        dict(id="r5", text="कैलाश पर उसे नंदी ने रोका। नंदी का चेहरा वानर जैसा था... और रावण ज़ोर से हँस पड़ा।"),
        dict(id="r6", text="नंदी ने श्राप दिया: मेरे जैसे वानर पैदा होंगे... और तुम्हारे कुल का नाश करेंगे।",
             gap=REVEAL_GAP),
        dict(id="r7", text="पहली हार, नर्मदा के किनारे। रावण शिवलिंग पर फूल चढ़ा रहा था।"),
        dict(id="r8", text="थोड़ा आगे, महिष्मती के राजा कार्तवीर्य अर्जुन नदी में खेल रहे थे। उनके एक हज़ार हाथ थे।"),
        dict(id="r9", text="अपनी ताक़त नापने के लिए, उन्होंने हज़ार हाथों से नर्मदा का बहाव रोक दिया।"),
        dict(id="r10", text="पानी उल्टा बहा... और रावण के सारे फूल बहा ले गया।"),
        dict(id="r11", text="ग़ुस्से में रावण लड़ने पहुँचा। पर अर्जुन ने उसे पकड़ा, बाँधा, और अपनी राजधानी ले गए।"),
        dict(id="r12", text="आख़िर में रावण के दादा, ऋषि पुलस्त्य को ख़ुद आकर उसे छुड़वाना पड़ा।", gap=REVEAL_GAP),
        dict(id="r13", text="पर असली बेइज़्ज़ती तो अभी बाकी थी।", gap=REVEAL_GAP),
        dict(id="r14", text="रावण ने सुना, किष्किंधा का वानर राजा वाली बहुत ताक़तवर है। वो सीधा उससे लड़ने चला गया।"),
        dict(id="r15", text="वाली दक्षिण समुद्र के किनारे संध्या कर रहा था। रावण चुपके से, पीछे से उसे पकड़ने बढ़ा।"),
        dict(id="r16", text="जैसे ही रावण पास आया, वाली ने उसे पकड़ा... और बगल में दबा लिया।", gap=REVEAL_GAP),
        dict(id="r17", text="फिर उड़ चला। पश्चिम समुद्र, उत्तर समुद्र, पूर्व समुद्र... हर जगह संध्या की। और रावण पूरे "
                            "रास्ते बगल में लटका रहा।"),
        dict(id="r18", text="हज़ारों योजन घुमाकर, वाली किष्किंधा लौटा और उसे छोड़ दिया। रावण ने आग के सामने उससे दोस्ती "
                            "कर ली।", gap=REVEAL_GAP),
        dict(id="r19", text="और नंदी का श्राप? जो रावण वानर के चेहरे पर हँसा था... उसकी लंका एक वानर ने जलाई, और वानर "
                            "सेना ही उसके दरवाज़े तक पहुँची।"),
        dict(id="r20", text="क्या तुम्हें पता था, राम से पहले रावण दो बार हार चुका था? यस या नो, कमेंट में बताओ।"),
    ],
    "kn": [
        dict(id="r1", text="ಯೋಚಿಸಿ... ದೇವತೆಗಳೇ ನಡುಗ್ತಿದ್ದ ರಾವಣನನ್ನ, ಒಬ್ಬ ವಾನರ ಕಂಕುಳಲ್ಲಿ ಇಟ್ಕೊಂಡು, ನಾಲ್ಕೂ ಸಮುದ್ರ "
                           "ಸುತ್ತಿಸಿಬಿಟ್ಟ.", gap=REVEAL_GAP),
        dict(id="r2", text="ಇದು ಯಾವ್ದೋ ಸಿನಿಮಾ ಕಥೆ ಅಲ್ಲ. ವಾಲ್ಮೀಕಿ ರಾಮಾಯಣದ ಉತ್ತರ ಕಾಂಡದಲ್ಲೇ ಇದೆ."),
        dict(id="r3", text="ರಾಮನಿಗಿಂತ ಮುಂಚೆ, ರಾವಣ ಒಂದಲ್ಲ, ಎರಡು ಸಲ ಸೋತಿದ್ದ.", gap=REVEAL_GAP),
        dict(id="r4", text="ಬ್ರಹ್ಮದೇವರಿಂದ ವರ ಸಿಕ್ಕ ಮೇಲೆ, ರಾವಣ ಇಡೀ ಲೋಕ ಗೆಲ್ಲೋಕೆ ಹೊರಟ."),
        dict(id="r5", text="ಕೈಲಾಸದಲ್ಲಿ ನಂದಿ ಅವನನ್ನ ತಡೆದ. ನಂದಿಯ ಮುಖ ವಾನರನ ತರ ಇತ್ತು... ರಾವಣ ಜೋರಾಗಿ ನಕ್ಕುಬಿಟ್ಟ."),
        dict(id="r6", text="ನಂದಿ ಶಾಪ ಕೊಟ್ಟ: ನನ್ನ ತರಾನೇ ವಾನರರು ಹುಟ್ತಾರೆ... ನಿನ್ನ ವಂಶವನ್ನೇ ನಾಶ ಮಾಡ್ತಾರೆ.",
             gap=REVEAL_GAP),
        dict(id="r7", text="ಮೊದಲ ಸೋಲು, ನರ್ಮದಾ ನದಿ ದಡದಲ್ಲಿ. ರಾವಣ ಶಿವಲಿಂಗಕ್ಕೆ ಹೂವು ಏರಿಸ್ತಿದ್ದ."),
        dict(id="r8", text="ಸ್ವಲ್ಪ ಮುಂದೆ, ಮಾಹಿಷ್ಮತಿಯ ರಾಜ ಕಾರ್ತವೀರ್ಯಾರ್ಜುನ ನೀರಲ್ಲಿ ಆಟ ಆಡ್ತಿದ್ದ. ಅವನಿಗೆ ಸಾವಿರ ಕೈಗಳು "
                           "ಇದ್ವು."),
        dict(id="r9", text="ತನ್ನ ಶಕ್ತಿ ಎಷ್ಟು ಅಂತ ನೋಡೋಕೆ, ಸಾವಿರ ಕೈಯಿಂದ ನರ್ಮದೆಯ ಹರಿವನ್ನೇ ತಡೆದುಬಿಟ್ಟ."),
        dict(id="r10", text="ನೀರು ಹಿಂದಕ್ಕೆ ಹರೀತು... ರಾವಣನ ಹೂವೆಲ್ಲಾ ಕೊಚ್ಕೊಂಡು ಹೋಯ್ತು."),
        dict(id="r11", text="ಕೋಪದಲ್ಲಿ ರಾವಣ ಯುದ್ಧಕ್ಕೆ ಹೋದ. ಆದ್ರೆ ಅರ್ಜುನ ಅವನನ್ನ ಹಿಡಿದು, ಕಟ್ಟಿ, ತನ್ನ ರಾಜಧಾನಿಗೆ "
                            "ಎಳ್ಕೊಂಡು ಹೋದ."),
        dict(id="r12", text="ಕೊನೆಗೆ ರಾವಣನ ಅಜ್ಜ, ಪುಲಸ್ತ್ಯ ಋಷಿಗಳೇ ಬಂದು, ಅವನನ್ನ ಬಿಡಿಸ್ಕೊಂಡು ಹೋಗಬೇಕಾಯ್ತು.",
             gap=REVEAL_GAP),
        dict(id="r13", text="ಆದ್ರೆ ನಿಜವಾದ ಅವಮಾನ ಇನ್ನೂ ಬಾಕಿ ಇತ್ತು.", gap=REVEAL_GAP),
        dict(id="r14", text="ಕಿಷ್ಕಿಂಧೆಯ ವಾನರ ರಾಜ ವಾಲಿ ತುಂಬಾ ಶಕ್ತಿಶಾಲಿ ಅಂತ ರಾವಣ ಕೇಳಿದ. ಸೀದಾ ಅವನ ಜೊತೆ ಯುದ್ಧಕ್ಕೆ "
                            "ಹೊರಟ."),
        dict(id="r15", text="ವಾಲಿ ದಕ್ಷಿಣ ಸಮುದ್ರದ ದಡದಲ್ಲಿ ಸಂಧ್ಯಾವಂದನೆ ಮಾಡ್ತಿದ್ದ. ರಾವಣ ಸದ್ದಿಲ್ಲದೆ, ಹಿಂದಿನಿಂದ ಅವನನ್ನ "
                            "ಹಿಡಿಯೋಕೆ ಹೋದ."),
        dict(id="r16", text="ರಾವಣ ಹತ್ರ ಬರ್ತಿದ್ದ ಹಾಗೆ, ವಾಲಿ ಅವನನ್ನ ಹಿಡಿದು... ಕಂಕುಳಲ್ಲಿ ಅವುಚಿಕೊಂಡ.", gap=REVEAL_GAP),
        dict(id="r17", text="ಆಮೇಲೆ ಆಕಾಶಕ್ಕೆ ಹಾರಿದ. ಪಶ್ಚಿಮ ಸಮುದ್ರ, ಉತ್ತರ ಸಮುದ್ರ, ಪೂರ್ವ ಸಮುದ್ರ... ಎಲ್ಲಾ ಕಡೆ "
                            "ಸಂಧ್ಯಾವಂದನೆ ಮುಗಿಸಿದ. ರಾವಣ ದಾರಿಯುದ್ದಕ್ಕೂ ಕಂಕುಳಲ್ಲೇ ನೇತಾಡ್ತಿದ್ದ."),
        dict(id="r18", text="ಸಾವಿರಾರು ಯೋಜನ ಸುತ್ತಿ, ವಾಲಿ ಕಿಷ್ಕಿಂಧೆಗೆ ವಾಪಸ್ ಬಂದು ಅವನನ್ನ ಬಿಟ್ಟ. ರಾವಣ ಬೆಂಕಿಯ ಮುಂದೆ "
                            "ಅವನ ಜೊತೆ ಸ್ನೇಹ ಮಾಡ್ಕೊಂಡ.", gap=REVEAL_GAP),
        dict(id="r19", text="ನಂದಿಯ ಶಾಪ? ವಾನರನ ಮುಖ ನೋಡಿ ನಕ್ಕ ರಾವಣನ ಲಂಕೆಯನ್ನ... ಒಬ್ಬ ವಾನರನೇ ಸುಟ್ಟ. ವಾನರ ಸೇನೆಯೇ "
                            "ಅವನ ಬಾಗಿಲಿಗೆ ಬಂತು."),
        dict(id="r20", text="ರಾಮನಿಗಿಂತ ಮುಂಚೆ ರಾವಣ ಎರಡು ಸಲ ಸೋತಿದ್ದ ಅಂತ ನಿಮಗೆ ಗೊತ್ತಿತ್ತಾ? ಹೌದಾ ಇಲ್ವಾ, ಕಾಮೆಂಟ್ "
                            "ಮಾಡಿ ಹೇಳಿ."),
    ],
}

_SOURCES = ["Valmiki Ramayana, Uttara Kanda (M. N. Dutt translation, 1894)"]
METADATA = {
    "hi": dict(
        title="Ram se pehle, Ravan do baar haara tha",
        caption="Socho, jis Ravan se devta bhi kaanpte the... use ek vaanar ne bagal mein dabaya aur chaaron samudra "
                "ghuma diye 😳\n\n"
                "Valmiki Ramayan, Uttar Kand: Narmada ke kinare raja Kartavirya Arjun ne apne hazaar haathon se nadi "
                "rok di, Ravan ko baandh ke le gaye. Phir Vali ne Ravan ko bagal mein daba ke paschim, uttar aur poorv "
                "samudra ghumaya. Aur Nandi ka shraap vaanaron ke haath hi poora hua.\n\n"
                "Kya tumhe ye pata tha? YES ya NO, comment mein batao 👇",
        yt_title="Ram Se Pehle, Ravan Do Baar Haara Tha 😳 | Vali Aur Ravan | Ramayan",
        yt_description="Valmiki Ramayan ke Uttar Kand mein Ravan ki do haar likhi hain. Narmada ke kinare raja Kartavirya "
                       "Arjun ne hazaar haathon se nadi ka bahaav roka, Ravan ke phool beh gaye, aur Arjun ne use baandh "
                       "kar Mahishmati le gaye; Pulastya rishi ko aakar chhudwana pada. Phir Vali ne sandhya karte hue "
                       "Ravan ko bagal mein dabaya aur samudra-samudra ghumaya. Kailash par Nandi ka shraap tha: vaanar hi "
                       "tumhare kul ka naash karenge.",
        hashtags=["#ramayan", "#ravan", "#vali", "#mythology", "#kahani"],
        pinned_comment="Kya tumhe pata tha, Ram se pehle Ravan do baar haara tha? YES ya NO? 👇",
        sources=_SOURCES),
    "kn": dict(
        title="Ramaniginta munche Ravana eradu sala sotidda",
        caption="Yochisi: devategale nadugtidda Ravanananna, obba vaanara kankulalli itkondu naalku samudra "
                "suttisibitta 😳\n\n"
                "Valmiki Ramayana, Uttara Kanda: Narmada nadi dadadalli raja Kartaviryarjuna saavira kaiyinda nadiyanne "
                "tadedu, Ravananannu kattikondu hoda. Aamele Vali Ravananannu kankulalli itkondu paschima, uttara, "
                "poorva samudra suttisida. Nandiya shaapa vaanararinda ne nijavaaytu.\n\n"
                "Nimge idu gottittaa? Houda illva, comment maadi 👇",
        yt_title="Ramaniginta Munche Ravana Eradu Sala Sotidda 😳 | Vali Mattu Ravana | Ramayana",
        yt_description="Valmiki Ramayanada Uttara Kandadalli Ravanana eradu solugalu ive. Narmada dadadalli raja "
                       "Kartaviryarjuna saavira kaiyinda nadiya harivannu tadeda, Ravanana hoovella kochkondu hoytu, "
                       "Arjuna avanannu kattikondu Mahishmatige hoda; Pulastya rishigale bandu bidisbekaaytu. Aamele Vali "
                       "sandhyavandane maadta Ravananannu kankulalli itkondu samudradinda samudrakke haarida. Kailasadalli "
                       "Nandiya shaapa: vaanararu ninna vamshavanne naasha maadtare.",
        hashtags=["#kannada", "#ramayana", "#ravana", "#kannadastory", "#mythology"],
        pinned_comment="Ramaniginta munche Ravana eradu sala sotidda anta nimge gottittaa? Houda illva? 👇",
        sources=_SOURCES),
}

USED_ASSETS, CREDITS_FILES = [], []      # everything in this video is drawn in code


def draw(cr, t, tl):
    from scenes_ravana import draw as _draw
    _draw(cr, t, tl)


def sfx(tl):
    from scenes_ravana import sfx as _sfx
    return _sfx(tl)
