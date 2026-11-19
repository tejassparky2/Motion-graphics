"""Mythology video 27 (Hindi only; owner, 19 Nov 2026: "make only 1 hindi short for today"): King Nahusha, a man who
became king of the gods and was turned into a python by one kick. A curse-and-boon story from the Mahabharata, after
three Ramayana reels in a row (Manthara, Jatayu, Long 3). Hook: the stake in one line (a man became king of heaven,
then one kick made him a python). The clever turn is the word "sarpa": Nahusha shouts "sarpa! sarpa!" (move on!) at
the sages carrying him, and the sage answers "then become a sarpa" (a snake). The second half: the python catches the
strongest Pandava, Bhima, who cannot move (the sage's boon takes the strength of anyone the python holds), and only
Yudhishthira's answers free both. Callback: pride in his power threw him down, understanding lifted him up. Ending:
strength or understanding? Three names only (Nahusha, Bhima, Yudhishthira); the sage (Agastya) and the king of the
gods (Indra) stay roles. Look: Togalu Gombeyaata shadow puppets, short Hindi labels.

Facts (Mahabharata, K. M. Ganguli translation):
- Udyoga Parva 11-17: with Indra in hiding (after slaying Vritra), the gods and the sages make the earthly king
  Nahusha king of heaven; he grows proud, yokes the sages to his palanquin, urges them on ("sarpa", move on, in the
  telling of the curse) and touches the sage Agastya's head with his foot (17); Agastya curses him to fall to earth as
  a serpent, to be freed when Yudhishthira answers him. Anushasana Parva 99-100 tells the kick on the head again.
- Vana Parva 178-181 (Ajagara Parva): in the Himalayan forest a huge python seizes Bhima, who cannot free himself;
  the python says that by the sage's boon whoever it seizes loses his strength, that it is Nahusha, the Pandavas'
  ancestor, and that it will eat him; Yudhishthira arrives, the python offers to free Bhima if its questions are
  answered; asked who is a Brahmana (the reel says "the highest person"), Yudhishthira answers: the one in whom truth,
  charity, forgiveness, good conduct, kindness and self-control are seen, by conduct and not by birth (180); Nahusha
  frees Bhima, takes his heavenly form again and goes to heaven (181).
"""
from channel import ASSETS_ROOT, MUSIC, NARRATORS, NARRATOR_LABEL, REVEAL_GAP, TAIL  # noqa: F401

G = REVEAL_GAP
SCRIPTS = {   # one short, whole sentence per line, so every sentence gets its own take and a real pause after it
    "hi": [
        dict(id="n01", text="एक इंसान देवताओं का राजा बना, फिर एक लात ने उसे अजगर बना दिया।"),
        dict(id="n02", text="उसका नाम था नहुष, धरती का एक महान राजा।", gap=G),
        dict(id="n03", text="एक बार, देवताओं का राजा स्वर्ग छोड़कर कहीं छिप गया।"),
        dict(id="n04", text="स्वर्ग में कोई राजा नहीं बचा।"),
        dict(id="n05", text="तब देवताओं ने धरती के राजा नहुष को स्वर्ग का राजा बना दिया।"),
        dict(id="n06", text="अब एक इंसान देवताओं पर राज कर रहा था!", gap=G),
        dict(id="n07", text="पर इतनी ताक़त मिलते ही, नहुष को घमंड हो गया।"),
        dict(id="n08", text="उसने हुक्म दिया: मेरी पालकी अब ऋषि उठाएँगे।"),
        dict(id="n09", text="बूढ़े ऋषि उसकी भारी पालकी कंधों पर उठाकर धीरे धीरे चलने लगे।"),
        dict(id="n10", text="नहुष को जल्दी थी, वो चिल्लाया: सर्प! सर्प!"),
        dict(id="n11", text="संस्कृत में सर्प का एक मतलब है, जल्दी चलो।", gap=G),
        dict(id="n12", text="फिर गुस्से में, उसने एक बूढ़े ऋषि के सिर पर लात मार दी।"),
        dict(id="n13", text="ऋषि ने उसे श्राप दिया, यानी बद्दुआ दी।"),
        dict(id="n14", text="तू सर्प सर्प चिल्लाता है ना?"),
        dict(id="n15", text="तो जा, तू खुद सर्प बन जा, यानी साँप!", gap=G),
        dict(id="n16", text="उसी पल, नहुष एक विशाल अजगर बनकर धरती पर गिर पड़ा।", gap=G),
        dict(id="n17", text="सालों तक, वो जंगल में अजगर बनकर पड़ा रहा।"),
        dict(id="n18", text="फिर एक दिन, उस जंगल में भीम आया।"),
        dict(id="n19", text="भीम पांडवों में सबसे ताक़तवर भाई था।"),
        dict(id="n20", text="अचानक, अजगर ने भीम को अपने शरीर में लपेटकर जकड़ लिया।"),
        dict(id="n21", text="भीम ने पूरा ज़ोर लगाया, पर वो हिल भी नहीं पाया!", gap=G),
        dict(id="n22", text="सबसे ताक़तवर पांडव एक अजगर से कैसे हार गया?", gap=G),
        dict(id="n23", text="अजगर बोला: ऋषि ने मुझे एक वरदान भी दिया था।"),
        dict(id="n24", text="जो मेरी पकड़ में आएगा, उसकी सारी ताक़त चली जाएगी।"),
        dict(id="n25", text="मैं नहुष हूँ, तुम्हारे ही खानदान का पुराना राजा।"),
        dict(id="n26", text="और आज, मैं तुम्हें खा जाऊँगा!", gap=G),
        dict(id="n27", text="तभी भीम को ढूँढता हुआ, उसका बड़ा भाई युधिष्ठिर वहाँ आ पहुँचा।"),
        dict(id="n28", text="अजगर बोला: मेरे सवालों के सही जवाब दो, तो मैं इसे छोड़ दूँगा।"),
        dict(id="n29", text="उसने पूछा: सबसे ऊँचा इंसान कौन है?"),
        dict(id="n30", text="युधिष्ठिर बोले: जिसमें सच, दया और माफ़ी हो।"),
        dict(id="n31", text="इंसान जन्म से नहीं, अपने कामों से ऊँचा बनता है।", gap=G),
        dict(id="n32", text="ये जवाब सुनते ही, नहुष का श्राप टूट गया।"),
        dict(id="n33", text="अजगर ने भीम को छोड़ दिया, और नहुष फिर से राजा बनकर स्वर्ग चला गया।", gap=G),
        dict(id="n34", text="जिस राजा को ताक़त के घमंड ने गिराया था, उसे समझ ने उठाया।", gap=G),
        dict(id="n35", text="तो बताओ, ताक़त बड़ी या समझ? कमेंट में बताओ।"),
    ],
}

_SOURCES = ["Mahabharata, Udyoga Parva 11-17", "Mahabharata, Vana Parva 178-181 (K. M. Ganguli translation)"]
METADATA = {
    "hi": dict(
        title="Insaan bana devtaon ka raja, phir ek laat ne ajgar bana diya",
        caption="Ek insaan devtaon ka raja bana... aur ek laat ki wajah se ajgar ban gaya 😳\n\n"
                "Raja Nahush ne rishiyon se apni palki uthwayi aur chillaya \"sarp! sarp!\" (jaldi chalo). Rishi ne "
                "kaha: toh ja, khud sarp ban ja! Saalon baad usne Bheem ko jakad liya, aur sabse taakatwar Pandav "
                "hil bhi nahi paaya. Bachaya kisne? Yudhishthir ke jawaabon ne.\n\n"
                "Taakat badi ya samajh? Comment mein batao 👇",
        yt_title="Insaan Bana Devtaon Ka Raja, Phir Ban Gaya Ajgar 😳 | Raja Nahush | Mahabharat",
        yt_description="Indra ke chhup jaane par devtaon ne dharti ke raja Nahush ko swarg ka raja bana diya. Ghamand "
                       "mein usne rishiyon se apni palki uthwayi, \"sarp! sarp!\" yaani jaldi chalo chillaya, aur ek "
                       "boodhe rishi ke sir par laat maar di. Rishi ke shraap se woh ajgar bankar dharti par gira. "
                       "Saalon baad jungle mein usne Bheem ko jakad liya: rishi ke vardaan se uski pakad mein aate hi "
                       "har kisi ki taakat chali jaati thi. Yudhishthir ne uske sawaalon ke jawaab diye: insaan janm "
                       "se nahi, apne karmon se ooncha banta hai. Shraap toota aur Nahush swarg laut gaya.",
        hashtags=["#mahabharat", "#nahush", "#bheem", "#mythology", "#hindu"],
        pinned_comment="Taakat badi ya samajh? Aap kya kehte ho? 👇",
        sources=_SOURCES),
}

USED_ASSETS, CREDITS_FILES = [], []      # everything in this video is drawn in code


def draw(cr, t, tl):
    import scenes_nahusha as S
    S.draw(cr, t, tl)


def sfx(tl):
    import scenes_nahusha as S
    return S.sfx(tl)
