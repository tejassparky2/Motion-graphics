"""Mythology video 25 (Hindi first): why Manthara turned Kaikeyi against Rama (owner, 14 Nov 2026: "one on manthara who
was manipulating Bharatha's mom why she did that what was her motivation ... story should be well explained and well
understandable and 1st line say as you all have watched Ramayana movie"). Timed for the Ramayana film (Part 1 opened
6 Nov 2026): line 1 is the owner's opening, then the stake (Rama sent to the forest for fourteen years because of a
maid) and the question the film leaves open (why?). The reel answers in two layers, both from Ramayanas: Valmiki's
(her fear for Kaikeyi and Bharata), then Tulsidas's hidden one (the gods begged Saraswati, who turned Manthara's mind,
so that Rama would leave the palace and reach Ravana).

Version 2 (owner, 14 Nov 2026: "the explaning not clear and there is some senteces cut in half"): one short, whole
sentence per line (each its own take, a real pause after it), the family explained first. Version 3 (owner: "You said
mahabharat in manthara video not Ramayan"): the reveal now comes from Tulsidas's Ramcharitmanas instead of the
Mahabharata's retelling (Vana Parva 274, the gandharvi Dundubhi), so the whole reel stays inside the Ramayanas.
"कैकई" is the spelling the voice says clearly (on screen: कैकेयी). Look: Togalu Gombeyaata shadow puppets with short
Hindi labels. Calm sound, no effect over a spoken word.

Facts:
- Valmiki Ramayana, Ayodhya Kanda 7 (Desiraju Hanumanta Rao translation, valmikiramayan.net): Manthara, Kaikeyi's
  maid "from her paternal home", humpbacked, sees Ayodhya decorated and learns Rama is to be anointed tomorrow; she
  runs to Kaikeyi: "Get up... great danger is upon you". Kaikeyi is delighted and gives her an ornament.
- Ayodhya Kanda 8: Manthara throws the ornament away in anger (8.1); if Rama is king, Kaikeyi will wait on Kausalya
  "as a maid-servant" (8.10); Rama will send Bharata to another country (8.27).
- Ayodhya Kanda 9: the two boons the king gave Kaikeyi after she saved his life in the war against Shambara
  (9.11-17); ask for Bharata's coronation and Rama's fourteen years in the forest (9.20-22).
- Ramcharitmanas (Tulsidas), Ayodhya Kand, doha 11: the gods beg Saraswati (Sharada): "बिपति हमारि बिलोकि बड़ि
  मातु करिअ सोइ आजु। रामु जाहिं बन राजु तजि होइ सकल सुरकाजु॥" (see our great trouble, mother; make Rama leave the
  kingdom for the forest, so all the gods' work is done). Doha 12: "नामु मंथरा मंदमति चेरी कैकइ केरि। अजस पेटारी
  ताहि करि गई गिरा मति फेरि॥" (Saraswati turned the mind of Manthara, Kaikeyi's maid, and went).
- "Ravana's end could come only at Rama's hands" and "a king in his palace would never reach Ravana" are the
  plain-words link between the exile and the gods' work (Ravana's boon: no god could kill him).
"""
from channel import ASSETS_ROOT, MUSIC, NARRATORS, NARRATOR_LABEL, REVEAL_GAP, TAIL  # noqa: F401

G = REVEAL_GAP
SCRIPTS = {   # one short, whole sentence per line, so every sentence gets its own take and a real pause after it
    "hi": [
        dict(id="m01", text="रामायण मूवी तो आप सबने देखी होगी।"),
        dict(id="m02", text="राम को चौदह साल के लिए जंगल जाना पड़ा।"),
        dict(id="m03", text="और इसकी वजह थी एक कुबड़ी दासी, मंथरा।", gap=G),
        dict(id="m04", text="पर मंथरा ने ऐसा क्यों किया?"),
        dict(id="m05", text="इसका जवाब तुलसीदास जी की रामायण में छुपा है।", gap=G),
        dict(id="m06", text="राजा दशरथ की तीन रानियाँ थीं।"),
        dict(id="m07", text="सबसे बड़ी रानी के बेटे थे राम।"),
        dict(id="m08", text="और रानी कैकई के बेटे थे भरत।"),
        dict(id="m09", text="मंथरा रानी कैकई की दासी थी।"),
        dict(id="m10", text="वो कैकई के मायके से उसके साथ आई थी।", gap=G),
        dict(id="m11", text="एक सुबह मंथरा ने देखा, पूरी अयोध्या सजी हुई है।"),
        dict(id="m12", text="पता चला, कल राम राजा बनने वाले हैं।", gap=G),
        dict(id="m13", text="मंथरा भागी भागी कैकई के पास गई।"),
        dict(id="m14", text="बोली: उठो रानी, तुम पर बड़ी मुसीबत आई है!", gap=G),
        dict(id="m15", text="पर कैकई तो खुश हो गई।"),
        dict(id="m16", text="उसे राम बहुत प्यारे थे।"),
        dict(id="m17", text="ख़ुशी में उसने मंथरा को अपना गहना दे दिया।"),
        dict(id="m18", text="मंथरा ने ग़ुस्से में वो गहना फेंक दिया।", gap=G),
        dict(id="m19", text="और बोली: राम राजा बने, तो तुम बड़ी रानी की नौकरानी बन जाओगी।"),
        dict(id="m20", text="और तुम्हारे बेटे भरत को देश से निकाल देंगे।", gap=G),
        dict(id="m21", text="ये सुनकर कैकई डर गई।"),
        dict(id="m22", text="तब मंथरा ने याद दिलाया: एक युद्ध में तुमने राजा की जान बचाई थी।"),
        dict(id="m23", text="तब राजा ने तुम्हें दो वरदान दिए थे।"),
        dict(id="m24", text="यानी, तुम जो भी माँगोगी, राजा मना नहीं कर सकते।", gap=G),
        dict(id="m25", text="पहले वरदान में, भरत के लिए राज माँगो।"),
        dict(id="m26", text="और दूसरे वरदान में, राम के लिए चौदह साल का वनवास माँगो।"),
        dict(id="m27", text="कैकई ने राजा से यही माँगा, और राम को जंगल जाना पड़ा।", gap=G),
        dict(id="m28", text="पर ये सब करके, एक दासी को क्या मिलता?", gap=G),
        dict(id="m29", text="तुलसीदास जी की रामायण में, इसका एक छुपा राज़ है।"),
        dict(id="m30", text="राम के राजा बनने की ख़बर से, स्वर्ग में देवता परेशान हो गए।"),
        dict(id="m31", text="क्योंकि रावण का अंत, सिर्फ़ राम के हाथों ही हो सकता था।"),
        dict(id="m32", text="पर राम राजा बनकर महल में रहते, तो रावण तक कभी नहीं पहुँचते।", gap=G),
        dict(id="m33", text="इसलिए देवताओं ने, विद्या की देवी सरस्वती से विनती की।"),
        dict(id="m34", text="और सरस्वती ने आकर, मंथरा की बुद्धि फेर दी।", gap=G),
        dict(id="m35", text="जिसे सब विलेन कहते हैं, उसी की वजह से राम रावण तक पहुँचे।", gap=G),
        dict(id="m36", text="तो मंथरा कौन थी? घर तोड़ने वाली दासी, या देवताओं की चाल का मोहरा? कमेंट में बताओ।"),
    ],
}

_SOURCES = ["Valmiki Ramayana, Ayodhya Kanda 7-9", "Ramcharitmanas (Tulsidas), Ayodhya Kand, doha 11-12"]
METADATA = {
    "hi": dict(
        title="Manthara ne Ram ko vanvas kyun bhijwaya?",
        caption="Ramayana movie toh dekh li... par Manthara ne Ram ko 14 saal ke liye jungle kyun bhijwaya? 😳\n\n"
                "Valmiki Ramayan mein uska darr hai: Ram raja bane toh Kaikeyi naukrani, aur Bharat desh se bahar. "
                "Par Tulsidas ji ki Ramcharitmanas ek chhupa raaz batati hai: devtaon ne Maa Saraswati se vinti ki, "
                "aur Saraswati ne Manthara ki buddhi pher di...\n\n"
                "Manthara villain thi, ya devtaon ki chaal ka mohra? Comment mein batao 👇",
        yt_title="Ramayana Movie Dekhi? Manthara Ne Aisa Kyun Kiya 😳 | Tulsi Ramayan Ka Chhupa Raaz",
        yt_description="Manthara, Bharat ki maa Kaikeyi ki daasi thi. Ayodhya saji dekhkar usne Kaikeyi ko darr dikhaya: "
                       "Ram raja bane toh tum badi rani ki naukrani banogi aur Bharat ko desh se nikaal denge. Kaikeyi "
                       "pehle khush thi, usne Manthara ko gehna diya, jo Manthara ne phenk diya. Phir usne do vardaan "
                       "yaad dilaaye: Bharat ko raaj, Ram ko 14 saal ka vanvas. Tulsidas ji ki Ramcharitmanas (Ayodhya "
                       "Kand) mein chhupa raaz hai: Ravan ka ant sirf Ram ke haathon ho sakta tha, isliye devtaon ne "
                       "Maa Saraswati se vinti ki, aur Saraswati ne Manthara ki buddhi pher di.",
        hashtags=["#ramayan", "#manthara", "#ramayanamovie", "#mythology", "#hindu"],
        pinned_comment="Manthara kya thi: ghar todne wali daasi, ya devtaon ki chaal ka mohra? 👇",
        sources=_SOURCES),
}

USED_ASSETS, CREDITS_FILES = [], []      # everything in this video is drawn in code


def draw(cr, t, tl):
    import scenes_manthara as S
    S.draw(cr, t, tl)


def sfx(tl):
    import scenes_manthara as S
    return S.sfx(tl)
