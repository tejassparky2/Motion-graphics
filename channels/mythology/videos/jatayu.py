"""Mythology video 26 (Hindi first): who Jatayu was and why he fought Ravana for Sita (owner, 14 Nov 2026: "who was
jatayu why was he so loyal to Rama what his motivation story should be well explained and well understandable and
1st line say as you all have watched Ramayana movie"). Timed for the Ramayana film (Part 1 opened 6 Nov 2026): line 1
is the owner's opening, then the stake (the first one to fight Ravana was an old vulture, and he gave his life for a
woman who was nothing to him). The answer: a promise to his dead friend's son. The twist: Rama could not light his
own father's pyre, but he lit Jatayu's. One storyline, a mid-story question, a callback, a two-sided ending. Look:
Togalu Gombeyaata shadow puppets with short Hindi labels. Respect: no blood; the wings are cut in a flash of light and
fall as leather pieces; the pyre is a soft glow.

Facts (Valmiki Ramayana, Aranya Kanda, Desiraju Hanumanta Rao translation, valmikiramayan.net):
- 14: on the way to Panchavati the brothers meet a huge vulture and take him for a demon; he says "know me as your
  father's friend" (14.3), born of Aruna, the Sun's charioteer, brother of Sampati (14.33), and offers to guard Sita
  when Rama and Lakshmana go out (14.34).
- 50: asleep, Jatayu hears Sita's cry (50.1); "sixty thousand years since my birth" (50.20); "I am old, you are young,
  an archer with a chariot, armour and arrows" (50.21); "while I live you will not take her" (50.26).
- 51: he breaks Ravana's bow with his feet (51.10, 13), knocks down the mules, splinters the chariot (51.15-16),
  brings down the charioteer (51.18); tired with age (51.21), Ravana cuts off his wings with a sword (51.42-43).
- 68: dying, he tells Rama that Ravana took Sita south (68.10), and dies; Rama says the bird is as worthy of honour as
  King Dasharatha (68.26) and cremates him himself "as he would his own deceased relative" (68.31), then offers water
  with Lakshmana (68.35-36).
- Ayodhya Kanda 76: Dasharatha dies after Rama has left for the forest; Bharata performs the cremation.
"""
from channel import ASSETS_ROOT, MUSIC, NARRATORS, NARRATOR_LABEL, REVEAL_GAP, TAIL  # noqa: F401

G = REVEAL_GAP
SCRIPTS = {   # one short, whole sentence per line, so every sentence gets its own take and a real pause after it
    "hi": [
        dict(id="j01", text="रामायण मूवी तो आप सबने देखी होगी।"),
        dict(id="j02", text="रावण से सबसे पहले लड़ने वाला कोई राजा नहीं था।"),
        dict(id="j03", text="वो था एक बूढ़ा गिद्ध, जटायु।", gap=G),
        dict(id="j04", text="सीता जटायु की कोई रिश्तेदार नहीं थीं।"),
        dict(id="j05", text="फिर भी जटायु ने उनके लिए अपनी जान दे दी।"),
        dict(id="j06", text="पर उसने ऐसा क्यों किया?", gap=G),
        dict(id="j07", text="जटायु गिद्धों का राजा था।"),
        dict(id="j08", text="और वो बहुत बूढ़ा था, साठ हज़ार साल का!", gap=G),
        dict(id="j09", text="राम, लक्ष्मण और सीता चौदह साल के लिए जंगल में आए।"),
        dict(id="j10", text="रास्ते में एक पेड़ पर, उन्हें ये विशाल गिद्ध दिखा।"),
        dict(id="j11", text="राम को लगा, ये कोई राक्षस है।"),
        dict(id="j12", text="पर गिद्ध प्यार से बोला: बेटा, डरो मत।"),
        dict(id="j13", text="मैं तुम्हारे पिता, राजा दशरथ का दोस्त हूँ।", gap=G),
        dict(id="j14", text="जब तुम दोनों भाई बाहर जाओगे, तब मैं सीता की रखवाली करूँगा।"),
        dict(id="j15", text="अपने दोस्त के बेटे से, जटायु ने ये वादा किया था।", gap=G),
        dict(id="j16", text="फिर एक दिन, रावण सीता को उठाकर आसमान में उड़ गया।"),
        dict(id="j17", text="सीता की चीख़ सुनकर, पेड़ पर सोया जटायु जाग गया।"),
        dict(id="j18", text="उसने उड़कर रावण का रास्ता रोक लिया।"),
        dict(id="j19", text="और बोला: मैं बूढ़ा हूँ, तुम जवान हो, तुम्हारे पास रथ और धनुष है।"),
        dict(id="j20", text="फिर भी मेरे जीते जी, तुम सीता को नहीं ले जा सकते!", gap=G),
        dict(id="j21", text="क्या एक बूढ़ा गिद्ध, अकेले रावण से जीत सकता था?", gap=G),
        dict(id="j22", text="जटायु ने अपने पंजों से रावण का धनुष तोड़ दिया।"),
        dict(id="j23", text="फिर उसका रथ तोड़ा, और रथ चलाने वाले को नीचे गिरा दिया।"),
        dict(id="j24", text="पर जटायु बूढ़ा था, वो जल्दी थक गया।"),
        dict(id="j25", text="तभी रावण ने तलवार निकाली, और उसके दोनों पंख काट दिए।", gap=G),
        dict(id="j26", text="जटायु ज़मीन पर गिर पड़ा।"),
        dict(id="j27", text="फिर भी राम के आने तक, वो ज़िंदा रहा।"),
        dict(id="j28", text="उसने राम को बताया: रावण सीता को दक्षिण की तरफ़ ले गया है।"),
        dict(id="j29", text="और फिर जटायु ने दम तोड़ दिया।", gap=G),
        dict(id="j30", text="राम के जंगल आने के बाद, उनके पिता गुज़र गए थे।"),
        dict(id="j31", text="और राम अपने पिता की चिता को आग भी नहीं दे पाए थे।", gap=G),
        dict(id="j32", text="पर जटायु की चिता को, राम ने अपने हाथों से आग दी।"),
        dict(id="j33", text="बिल्कुल वैसे, जैसे एक बेटा अपने पिता को देता है।", gap=G),
        dict(id="j34", text="जो पिता का दोस्त बनकर मिला था, वो पिता बनकर विदा हुआ।", gap=G),
        dict(id="j35", text="तो बताओ, जटायु वो लड़ाई हारा था, या जीता? कमेंट में बताओ।"),
    ],
}

_SOURCES = ["Valmiki Ramayana, Aranya Kanda 14, 50, 51, 68", "Valmiki Ramayana, Ayodhya Kanda 76"]
METADATA = {
    "hi": dict(
        title="Jatayu ne Sita ke liye jaan kyun di?",
        caption="Ramayana movie toh dekh li... par Ravan se sabse pehle ladne wala ek boodha giddh tha 😳\n\n"
                "Sita uski kuch nahi lagti thi, phir bhi Jatayu ne jaan de di. Kyun? Valmiki Ramayan mein jawab hai: "
                "woh Ram ke pita Dashrath ka dost tha, aur usne Sita ki rakhwali ka vaada kiya tha. Aur Ram ne uski "
                "chita ko apne haathon se aag di, jaise beta pita ko deta hai...\n\n"
                "Jatayu woh ladaai haara tha, ya jeeta? Comment mein batao 👇",
        yt_title="Ramayana Movie Dekhi? Jatayu Ne Sita Ke Liye Jaan Kyun Di 😳 | Valmiki Ramayan",
        yt_description="Jatayu giddhon ka raja tha, saath hazaar saal ka. Jungle mein usne Ram se kaha: main tumhare "
                       "pita ka dost hoon, tum bahar jaoge toh main Sita ki rakhwali karunga. Jab Ravan Sita ko lekar "
                       "aasmaan mein uda, boodhe Jatayu ne uska dhanush toda, rath toda, saarthi ko giraya. Thakkar "
                       "gira toh Ravan ne talwar se uske pankh kaat diye. Marte hue usne Ram ko bataya ki Ravan Sita ko "
                       "dakshin le gaya. Ram apne pita ki chita ko aag nahi de paaye the, par Jatayu ki chita ko "
                       "unhone apne haathon se aag di.",
        hashtags=["#ramayan", "#jatayu", "#ramayanamovie", "#mythology", "#hindu"],
        pinned_comment="Jatayu woh ladaai haara tha, ya jeeta? 👇",
        sources=_SOURCES),
}

USED_ASSETS, CREDITS_FILES = [], []      # everything in this video is drawn in code


def draw(cr, t, tl):
    import scenes_jatayu as S
    S.draw(cr, t, tl)


def sfx(tl):
    import scenes_jatayu as S
    return S.sfx(tl)
