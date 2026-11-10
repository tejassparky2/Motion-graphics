"""Mythology long video 1 (Hindi only first; Kannada only if the owner likes it): six true, mind-blowing stories of six
different kinds (owner, 9-10 Nov 2026: "make 1 long video on interesting mind blowing engaging one first make long
only in hindi", "i dont want you to focus on only one type of story i want you to ecplore all intresting ones",
"first make 1 short then we will go for long one auto approved"). Landscape 16:9, about 9 minutes, shadow puppets.
Thread: Devayani from story 1 returns in story 6 (open loop set in the intro).

Facts (K. M. Ganguli's Mahabharata unless noted):
1 Kacha (Adi Parva 76-77): gods send Brihaspati's son Kacha to learn Sanjivani from Shukra; Danavas kill him three
  times (pieces fed to wolves; pounded and mixed in sea water; burnt, ashes mixed in Shukra's wine); he answers from
  inside Shukra's stomach; Shukra teaches him the science inside; Kacha tears out and revives his guru; Shukra rules
  that a Brahmana who drinks wine has sinned; Kacha calls Devayani his sister (born again from her father's body);
  mutual curses: no Rishi's son will marry her.
2 Ani-Mandavya (Adi Parva 107-108): silent sage, thieves hide loot in his hermitage, impaled by order, survives,
  freed; Dharma: "a little insect was once pierced by thee on a blade of grass"; rule: no sin "below the age of
  fourteen"; curse: Dharma born "among men even in the Sudra order" = Vidura.
3 Agastya (Vana Parva 101-109): Kalakeyas hide in the ocean by day and kill ascetics by night; the gods ask Agastya
  to drink the ocean; he does; the gods slay them; asked to give the water back he says it is digested; Brahma: it
  will be filled after a long time through Bhagiratha; Ganga brought down by Bhagiratha fills the ocean.
4 Rishyashringa (Vana Parva 110-113; Valmiki Bala Kanda 9-11, 14-15): born of a doe, a horn on his head, never saw
  anyone but his father; drought in Anga; women sent to the forest, he takes them for strange ascetics; brought on
  a boat-hermitage; rain falls; marries Shanta; later performs Dasharatha's sacrifice, after which Rama is born.
5 Nachiketa (Katha Upanishad 1.1-1.2): father gives away old, dry cows; "to whom will you give me?" thrice; "to
  Death"; three nights unfed at Yama's door; three boons; the third: what happens after death; Yama offers sons,
  cattle, elephants, gold, horses, land, long life, women with chariots and music; "keep your horses, dance and
  song"; "the knowing Self is not born, it does not die" (1.2.18), close to Gita 2.19-20.
6 Yayati (Adi Parva 78-85): Sharmishtha pushes Devayani into a well; King Yayati pulls her out by the hand and
  marries her (Kacha's curse: a king, not a Rishi's son); he secretly has sons by Sharmishtha; Shukra curses him
  with old age, which can pass to one who takes it; four sons refuse, the youngest, Puru, accepts; a thousand years
  later: desire is never quenched by enjoyment, it grows like fire fed with ghee; Puru made king (the Kuru line of
  the Pandavas and Kauravas); Yadu, who refused, is the ancestor of the Yadavas, Krishna's clan.
"""
from channel import ASSETS_ROOT, MUSIC, NARRATORS, NARRATOR_LABEL, REVEAL_GAP, TAIL  # noqa: F401

FORMAT = "landscape"      # 1920x1080 (render_all sets MYTH_FORMAT for it)
G = REVEAL_GAP

SCRIPTS = {
    "hi": [
        # intro: six claims, then the open loop
        dict(id="i1", text="सोचो... एक शिष्य, जो अपने गुरु के पेट के अंदर से बोला।"),
        dict(id="i2", text="एक ऋषि, जिसने ख़ुद यमराज को सज़ा दे दी।"),
        dict(id="i3", text="एक ऋषि, जो पूरा समुद्र पी गया।"),
        dict(id="i4", text="एक लड़का, जिसने कभी कोई औरत देखी ही नहीं थी।"),
        dict(id="i5", text="एक बच्चा, जो यमराज के घर जाकर, मौत का राज़ पूछ आया।"),
        dict(id="i6", text="और एक पिता, जिसने अपने ही बेटे की जवानी ले ली।", gap=G),
        dict(id="i7", text="ये छह कहानियाँ, हमारे ग्रंथों में सच में लिखी हैं: महाभारत में, रामायण में, और उपनिषद में।"),
        dict(id="i8", text="आख़िर तक देखना। पहली कहानी की एक लड़की, आख़िरी कहानी में फिर आएगी।", gap=G),
        # 1 Kacha
        dict(id="k1", text="पहली कहानी। देवताओं और असुरों की लड़ाई चल रही थी।"),
        dict(id="k2", text="असुरों के गुरु शुक्राचार्य के पास एक विद्या थी: संजीवनी। इससे वो मरे हुए असुरों को, फिर ज़िंदा कर "
                           "देते थे।"),
        dict(id="k3", text="देवताओं के पास ये विद्या नहीं थी। तो उन्होंने अपने गुरु बृहस्पति के बेटे कच को, शुक्राचार्य के पास "
                           "भेजा।"),
        dict(id="k4", text="कच शुक्राचार्य का शिष्य बना। गुरु की सेवा की, और गुरु की बेटी देवयानी उसे पसंद करने लगी।"),
        dict(id="k5", text="असुर समझ गए कि कच विद्या सीखने आया है। उन्होंने कच को मार डाला, और उसके टुकड़े भेड़ियों को खिला दिए।"),
        dict(id="k6", text="देवयानी रोने लगी। शुक्राचार्य ने संजीवनी से कच को पुकारा, और कच भेड़ियों के पेट से ज़िंदा बाहर आ "
                           "गया।"),
        dict(id="k7", text="असुरों ने फिर मारा। इस बार उसे पीसकर, समुद्र के पानी में मिला दिया। गुरु ने फिर ज़िंदा कर दिया।"),
        dict(id="k8", text="तीसरी बार असुरों ने चाल चली। कच को जलाया, उसकी राख शराब में मिलाई, और वो शराब, ख़ुद शुक्राचार्य को "
                           "पिला दी।", gap=G),
        dict(id="k9", text="अब कच, गुरु के पेट के अंदर था।", gap=G),
        dict(id="k10", text="देवयानी फिर रोई। शुक्राचार्य ने कच को पुकारा, और अंदर से आवाज़ आई: गुरुजी, मैं आपके पेट में हूँ।",
             gap=G),
        dict(id="k11", text="अब मुश्किल ये थी: कच बाहर आएगा, तो गुरु का पेट फटेगा, और गुरु मर जाएँगे।"),
        dict(id="k12", text="तो शुक्राचार्य ने पेट के अंदर ही, कच को संजीवनी विद्या सिखा दी।"),
        dict(id="k13", text="कच पेट चीरकर बाहर आया। गुरु गिर पड़े। और कच ने उसी विद्या से, गुरु को फिर ज़िंदा कर दिया।",
             gap=G),
        dict(id="k14", text="उस दिन शुक्राचार्य ने नियम बनाया: आज से जो ब्राह्मण शराब पिएगा, वो पापी माना जाएगा।"),
        dict(id="k15", text="और देवयानी? उसने कच से शादी करनी चाही। पर कच बोला: मैं तुम्हारे पिता के शरीर से दोबारा जन्मा हूँ। "
                            "तुम मेरी बहन हो।"),
        dict(id="k16", text="ग़ुस्से में दोनों ने एक-दूसरे को श्राप दिया। कच का श्राप था: कोई ऋषि का बेटा, तुमसे शादी नहीं "
                            "करेगा।"),
        dict(id="k17", text="याद रखना, ये श्राप आख़िरी कहानी में काम आएगा।", gap=G),
        # 2 Mandavya
        dict(id="m1", text="दूसरी कहानी। एक ऋषि थे, मांडव्य। उन्होंने मौन व्रत लिया था, यानी वो किसी से बात नहीं करते थे।"),
        dict(id="m2", text="एक दिन कुछ चोर, राजा के सिपाहियों से भागते हुए, उनके आश्रम में चोरी का माल छिपा गए।"),
        dict(id="m3", text="सिपाहियों ने ऋषि से पूछा: चोर कहाँ गए? पर ऋषि मौन थे। कुछ नहीं बोले।"),
        dict(id="m4", text="सिपाहियों को माल आश्रम में ही मिल गया। उन्हें लगा, ऋषि ही चोरों के सरदार हैं।"),
        dict(id="m5", text="राजा ने सज़ा सुना दी: इसे शूली पर चढ़ा दो।", gap=G),
        dict(id="m6", text="पर ऋषि मरे नहीं। अपने तप की ताक़त से, वो शूली पर भी ज़िंदा रहे।"),
        dict(id="m7", text="राजा को सच पता चला, तो उसने पैर पकड़कर माफ़ी माँगी, और ऋषि को उतरवा लिया।"),
        dict(id="m8", text="अब ऋषि सीधे यमराज के पास गए। यमराज, यानी धर्मराज, जो सबके पाप और पुण्य का हिसाब रखते हैं।"),
        dict(id="m9", text="ऋषि ने पूछा: मैंने ऐसा कौन सा पाप किया था, जिसकी मुझे ये सज़ा मिली?"),
        dict(id="m10", text="यमराज बोले: बचपन में तुमने, एक छोटे से कीड़े को, घास के तिनके से चुभोया था।", gap=G),
        dict(id="m11", text="ऋषि बोले: एक बच्चे की नादानी की, इतनी बड़ी सज़ा? ये अन्याय है।"),
        dict(id="m12", text="और उसी दिन ऋषि ने नियम बना दिया: चौदह साल से छोटा बच्चा जो करेगा, वो पाप नहीं गिना जाएगा।", gap=G),
        dict(id="m13", text="फिर उन्होंने यमराज को श्राप दिया: तुम्हें इंसान बनकर, धरती पर जन्म लेना होगा।"),
        dict(id="m14", text="और यमराज ने जन्म लिया... महाभारत के सबसे समझदार इंसान, विदुर बनकर।", gap=G),
        # 3 Agastya
        dict(id="g1", text="तीसरी कहानी। कालकेय नाम के असुर, दिन में समुद्र के अंदर छिप जाते थे।"),
        dict(id="g2", text="और रात को बाहर निकलकर, जंगलों में ऋषियों को मार डालते थे।"),
        dict(id="g3", text="देवता उन्हें ढूँढ ही नहीं पाते थे। समुद्र बहुत बड़ा था, और बहुत गहरा।"),
        dict(id="g4", text="तब देवता ऋषि अगस्त्य के पास गए। बोले: आप ही कुछ कर सकते हैं। ये समुद्र पी जाइए।"),
        dict(id="g5", text="अगस्त्य समुद्र के किनारे गए... और पूरा समुद्र पी गए। एक बूँद नहीं छोड़ी।", gap=G),
        dict(id="g6", text="समुद्र सूखा, तो असुर दिख गए। देवताओं ने उन्हें हरा दिया, और बचे हुए असुर पाताल भाग गए।"),
        dict(id="g7", text="अब देवता बोले: ऋषिवर, अब समुद्र वापस भर दीजिए।"),
        dict(id="g8", text="अगस्त्य मुस्कुराए: वो पानी तो मैं पचा चुका हूँ।", gap=G),
        dict(id="g9", text="समुद्र ख़ाली रह गया। देवता ब्रह्मा जी के पास गए।"),
        dict(id="g10", text="ब्रह्मा जी बोले: बहुत समय बाद, राजा भगीरथ, इस समुद्र को फिर भरेंगे।"),
        dict(id="g11", text="और सच में, भगीरथ की तपस्या से गंगा धरती पर आईं... और उनके पानी से, वही ख़ाली समुद्र फिर भरा।",
             gap=G),
        # 4 Rishyashringa
        dict(id="s1", text="चौथी कहानी। जंगल में एक ऋषि, अपने बेटे ऋष्यशृंग के साथ रहते थे।"),
        dict(id="s2", text="बेटे के सिर पर एक छोटा सा सींग था। और महाभारत कहता है, उसकी माँ एक हिरनी थी।", gap=G),
        dict(id="s3", text="उसने अपने पिता के अलावा, कभी कोई इंसान नहीं देखा था। कोई औरत तो कभी नहीं।"),
        dict(id="s4", text="उधर, अंग देश में कई सालों से बारिश नहीं हुई थी। खेत सूख गए, लोग भूखे थे।"),
        dict(id="s5", text="ब्राह्मणों ने राजा से कहा: अगर वो जंगल वाला लड़का यहाँ आ जाए, तो बारिश होगी।"),
        dict(id="s6", text="पर वो जंगल से बाहर कैसे आए? तो राजा ने कुछ औरतों को, जंगल भेजा।"),
        dict(id="s7", text="लड़के ने उन्हें देखा, तो सोचा: ये तो कोई अजीब से ऋषि हैं! इनके कपड़े अलग, बातें अलग, और इनके फल "
                           "तो बहुत मीठे हैं।", gap=G),
        dict(id="s8", text="वो फल असल में मिठाइयाँ थीं। लड़के ने ज़िंदगी में पहली बार, मिठाई खाई थी।"),
        dict(id="s9", text="अगली बार, वो औरतें उसे एक नाव में बिठाकर, अंग देश ले गईं।"),
        dict(id="s10", text="और जैसे ही उसने अंग देश में पैर रखा... बारिश शुरू हो गई।", gap=G),
        dict(id="s11", text="राजा ने अपनी बेटी शांता की शादी, उससे कर दी।"),
        dict(id="s12", text="और रामायण में यही ऋषि, राजा दशरथ के लिए वो यज्ञ करते हैं... जिसके बाद राम का जन्म हुआ।", gap=G),
        dict(id="s13", text="सोचो, अगर ये लड़का जंगल से बाहर न आता, तो शायद रामायण ही न होती।", gap=G),
        # 5 Nachiketa
        dict(id="n1", text="पाँचवीं कहानी, कठ उपनिषद से। एक पिता बड़ा दान कर रहे थे। पर दान में दे रहे थे, बूढ़ी, कमज़ोर गायें।"),
        dict(id="n2", text="उनके बेटे नचिकेता को ये ग़लत लगा। उसने पूछा: पिताजी, आप मुझे किसे दान करोगे?"),
        dict(id="n3", text="पिता चुप रहे। बेटे ने दूसरी बार पूछा। फिर तीसरी बार।"),
        dict(id="n4", text="पिता ग़ुस्से में बोले: जा, तुझे मैं यमराज को देता हूँ।", gap=G),
        dict(id="n5", text="और नचिकेता सच में, यमराज के घर चला गया।"),
        dict(id="n6", text="यमराज घर पर नहीं थे। नचिकेता तीन दिन, बिना खाए पिए, उनके दरवाज़े पर बैठा रहा।"),
        dict(id="n7", text="यमराज लौटे, तो शर्मिंदा हुए। मेहमान तीन दिन भूखा रहा! बोले: तीन दिन के बदले, तीन वरदान माँगो।"),
        dict(id="n8", text="पहला वर: मेरे पिता का ग़ुस्सा शांत हो जाए। दूसरा: स्वर्ग दिलाने वाली अग्नि का ज्ञान।"),
        dict(id="n9", text="और तीसरा: बताइए, मरने के बाद इंसान का क्या होता है?", gap=G),
        dict(id="n10", text="यमराज ने टालना चाहा। बोले: ये मत पूछो। इसके बदले सोना ले लो, घोड़े, हाथी, ज़मीन, सौ साल की उम्र।"),
        dict(id="n11", text="नचिकेता बोला: ये सब तो एक दिन ख़त्म हो जाएगा। अपने घोड़े और नाच-गाने, आप ही रखिए। मुझे बस जवाब "
                            "चाहिए।", gap=G),
        dict(id="n12", text="यमराज ख़ुश हुए, और बोले: आत्मा न जन्म लेती है, न मरती है। शरीर मरता है, आत्मा नहीं।"),
        dict(id="n13", text="ये बात सुनी सुनी लगी? सदियों बाद, कृष्ण ने गीता में अर्जुन को, लगभग यही शब्द कहे।", gap=G),
        # 6 Yayati
        dict(id="y1", text="छठी और आख़िरी कहानी। याद है देवयानी? जिसे कच ने श्राप दिया था, कि कोई ऋषि का बेटा उससे शादी नहीं "
                           "करेगा?"),
        dict(id="y2", text="एक दिन देवयानी, असुर राजकुमारी शर्मिष्ठा से लड़ पड़ी। ग़ुस्से में शर्मिष्ठा ने उसे कुएँ में धकेल दिया।",
             gap=G),
        dict(id="y3", text="तभी वहाँ से राजा ययाति गुज़रे। उन्होंने देवयानी का हाथ पकड़कर, उसे बाहर निकाला।"),
        dict(id="y4", text="देवयानी बोली: आपने मेरा हाथ पकड़ा है, अब मुझसे शादी कीजिए। ययाति राजा थे, ऋषि के बेटे नहीं। "
                           "श्राप सच हो गया।", gap=G),
        dict(id="y5", text="पर ययाति ने चुपके से, शर्मिष्ठा से भी शादी कर ली, और उसके भी बेटे हुए।"),
        dict(id="y6", text="देवयानी को पता चला, तो वो रोती हुई अपने पिता शुक्राचार्य के पास गई।"),
        dict(id="y7", text="शुक्राचार्य ने ययाति को श्राप दिया: तू अभी, इसी पल बूढ़ा हो जा!", gap=G),
        dict(id="y8", text="पर एक रास्ता भी दिया: अगर कोई अपनी जवानी तुझे दे दे, तो तेरा बुढ़ापा वो ले लेगा।"),
        dict(id="y9", text="ययाति ने अपने बेटों से कहा: मुझे अपनी जवानी दे दो। चार बेटों ने साफ़ मना कर दिया।"),
        dict(id="y10", text="सबसे छोटा बेटा पुरु बोला: पिताजी, मेरी जवानी ले लीजिए।", gap=G),
        dict(id="y11", text="फिर हज़ार साल तक, पिता जवान रहे, और बेटा बूढ़ा।"),
        dict(id="y12", text="हज़ार साल बाद ययाति बोले: इच्छा कभी पूरी नहीं होती। जैसे आग में घी डालो, तो आग और भड़कती है।",
             gap=G),
        dict(id="y13", text="उन्होंने पुरु को उसकी जवानी लौटा दी, और उसे राजा बना दिया।"),
        dict(id="y14", text="और अब सबसे बड़ा ट्विस्ट: पुरु के ख़ानदान में आगे चलकर, पांडव और कौरव पैदा हुए।"),
        dict(id="y15", text="और जिस बेटे यदु ने मना किया था, उसके ख़ानदान में... ख़ुद कृष्ण पैदा हुए।", gap=G),
        # outro
        dict(id="o1", text="तो ये थीं छह कहानियाँ: पेट से बोलने वाला शिष्य, यमराज को सज़ा देने वाला ऋषि, समुद्र पीने वाले "
                           "अगस्त्य, जंगल का लड़का, नचिकेता, और ययाति।"),
        dict(id="o2", text="इनमें से सबसे शॉकिंग कौन सी थी? एक से छह तक, नंबर कमेंट करो।"),
    ],
}

# YouTube chapters: first line id of each part -> chapter title (finish.py writes them with the real timestamps)
CHAPTERS = [
    ("i1", "6 kahaniyan"),
    ("k1", "1. Guru ke pet se bola shishya (Kacha)"),
    ("m1", "2. Rishi ne Yamraj ko saza di (Mandavya)"),
    ("g1", "3. Jo poora samudra pee gaye (Agastya)"),
    ("s1", "4. Jisne kabhi aurat nahi dekhi (Rishyashringa)"),
    ("n1", "5. Yamraj se maut ka raaz (Nachiketa)"),
    ("y1", "6. Bete ki jawani le li (Yayati)"),
    ("o1", "Sabse shocking kaun si?"),
]

_SOURCES = ["Mahabharata, Adi Parva 76-85 and 107-108 (K. M. Ganguli translation)",
            "Mahabharata, Vana Parva 101-113 (K. M. Ganguli translation)",
            "Valmiki Ramayana, Bala Kanda 9-11 and 14-15",
            "Katha Upanishad 1.1-1.2"]
METADATA = {
    "hi": dict(
        title="6 kahaniyan jo dimaag hila dengi",
        caption="Ek shishya jo guru ke pet se bola. Ek rishi jisne Yamraj ko saza di. Ek rishi jo samudra pee gaya. "
                "Ek ladka jisne kabhi aurat nahi dekhi. Ek bachcha jo Yamraj se maut ka raaz pooch aaya. Aur ek pita "
                "jisne apne bete ki jawani le li 😳\n\nSabse shocking kaun si? 1 se 6, number comment karo 👇",
        yt_title="6 Kahaniyan Jo Dimaag Hila Dengi 😳 | Mahabharat, Ramayan, Upanishad",
        yt_description="Hamare granthon ki chhe sachchi kahaniyan, har ek alag tarah ki: Kacha jo Shukracharya ke pet "
                       "se bola, Mandavya jinhone Yamraj ko saza di aur Vidura ka janm hua, Agastya jo poora samudra "
                       "pee gaye, Rishyashringa jinke bina shayad Ramayan hi na hoti, Nachiketa jo Yamraj se maut ka "
                       "raaz pooch aaya, aur Yayati jinhone apne bete ki jawani le li. Pehli kahani ki Devayani, "
                       "aakhri kahani mein phir aati hai.",
        hashtags=["#mahabharat", "#ramayan", "#mythology", "#kahani", "#hindu"],
        pinned_comment="Sabse shocking kaun si thi? 1 se 6, number comment karo 👇",
        sources=_SOURCES),
}


USED_ASSETS, CREDITS_FILES = [], []      # everything in this video is drawn in code


def draw(cr, t, tl):
    from scenes_six_stories import draw as _draw
    _draw(cr, t, tl)


def sfx(tl):
    from scenes_six_stories import sfx as _sfx
    return _sfx(tl)
