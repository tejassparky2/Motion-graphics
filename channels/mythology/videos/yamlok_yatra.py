"""Mythology long video 2 (Hindi only): the soul's one-year walk to Yama's city, as the Garuda Purana tells it, as ONE
continuous story (owner, 12 Nov 2026: "Make 1 long video on what happens after we die on Garuda Purana not like
previous one set of story I want continuity story with strong hook good pacing engaging ammsuing so user stays only
in hindi not in kannada"). Landscape 16:9, about 9 minutes, shadow puppets.

Device: two travellers who die the same night, the stingy rich Seth Dhaniram and the poor water-seller Bhola. The
narrator says plainly they are our own example characters; everything that HAPPENS to them is from the text. Open loop
from the intro (one of them will be frightened by Yama, the other will have his feet washed by Yama); Bhola is kept
off-screen through the journey (re-hook c9) and arrives at the end by the eastern gate. The humour is Dhaniram's: his
bribe with no pocket, the messengers' "commission" quarter of every rice-ball, "how much for the boat?", his munim.
No gore: the Vaitarani is dark red water, the messengers are fierce but not monstrous, the hells are not shown.

Facts (Garuda Purana, Preta Kalpa / Saroddhara, Ernest Wood and S. V. Subrahmanyam translation, 1911):
- I.26: at the last moment "a divine vision arises, all the worlds appear as one, and he does not attempt to say
  anything". I.30-31: two messengers of Yama "bearing nooses and rods ... as black as crows, with hair erect".
- I.32-35: "The man of the size of a thumb, crying out 'oh, oh,' is dragged from the body ... looking the while at his
  own body"; noose about the neck; "Hurry up, you wicked man."
- I.40-42: brought to Yama "in a short time", shown, then "by command of Yama, swiftly comes back through the air";
  "desiring the body but held back with a noose".
- I.47-53: ten days of rice-balls, each in four portions: two nourish the body, "the third goes to the messengers of
  Yama; he lives upon the fourth"; head (1), neck and shoulders (2), heart (3), back (4), navel (5), hips (6), thighs
  (7), knees and feet (8-9), hunger and thirst (10). I.50: a body "the size of a hand". I.55: "On the thirteenth day the
  departed, bound by the servants of Yama, walks alone along the road like a captured monkey."
- I.56-59: the way is 86,000 yojanas; 247 yojanas a day, by day and night (a yojana is 8-9 miles in the translators'
  note); sixteen cities.
- II.3-11: no shade, no food, no water, "twelve suns blaze", thorns, hot sand, a forest of sword-like leaves.
- II.43-51: seventeen days alone, the city of Saumya on the 18th day (river Pushpabhadra, a fig tree); he weeps for
  wealth, wife and son; "Where is your wealth now? Where are your children and wife now? ... You only suffer the result
  of your own karma"; "provisions are the strength of a traveller ... that way, where there is neither buying nor
  selling ... familiar even to children"; monthly rice-balls eaten on the way. II.35: "I made no gifts".
- II.52: Sauripura, king Jangama "who has the appearance of Death"; II.58: Shailagama in the 4th month, "stones rain
  down"; II.74-78: Nanakranda (people crying), Sutaptabhavana, Payovarshana (clouds).
- II.63-69: Chitrabhavana, king Vichitra, "the younger brother of Yama"; fishermen with a boat for the Vaitarani:
  "Vitarana is a gift, and this is called Vaitarani because it is crossed over by that. If you have made the gift of a
  cow, then the boat will come to you, otherwise not"; "Oh heavens"; the river seethes; the messengers carry him across
  through the air "like a fish upon a hook". II.15-18: a hundred yojanas wide, a flow of blood, crocodiles, birds;
  "seethes ... like butter in the frying-pan".
- II.79-83: Shitadhya, "cold a hundred times greater than that of the Himalaya"; "Does there remain any relative who
  will remove my misery?"; "What sort of merit have you?"; at Bahubhiti he casts off the hand-sized body; the
  thumb-sized spirit goes on. II.85 and XIV.50: four gateways; the southern way for sinners, the other three for the
  good. III.3: the city is 44 yojanas beyond Bahubhiti.
- III.5-6: the doorkeeper Dharmadhwaja reports to Chitragupta. III.9-11: the Shravanas, sons of Brahma, wander in
  heaven, earth and the nether regions, "hear and understand at a distance, and see a long way off", report all that is
  "said and done, openly and secretly". III.16: sun, moon, fire, wind, sky, earth, water, the heart, day and night know
  a man's actions. XIV.10-15: Chitragupta "is never mistaken".
- III.18-21: to the sinful, Yama shows a terrible form: huge, rod in hand, seated on a buffalo, roaring like a cloud at
  the pralaya. III.29: "Yama deals equally with the fool and the learned, the beggar and the wealthy, the strong and
  the weak." III.37 and 45: "Oh, forgive my faults"; "Forgiveness of faults is done by the Lord Hari. We only punish
  miscreants, as we are ordered."
- XIV.51-55: the eastern way, paved with jewels, shaded by Parijata trees, chariots and swans, for those who comfort the
  distressed, are devoted to father and mother, give cows, and so on. XIV.74-76: "Yama, seeing them come, rising and
  coming forward, repeatedly bids them welcome. He offers them the throne, and bows to them; washes their feet".
- I.46: "Karma not experienced does not die away".
"""
from channel import ASSETS_ROOT, MUSIC, NARRATORS, NARRATOR_LABEL, REVEAL_GAP, TAIL  # noqa: F401

FORMAT = "landscape"      # 1920x1080 (render_all sets MYTH_FORMAT for it)
G = REVEAL_GAP

SCRIPTS = {
    "hi": [
        # intro: the hook, the source, the two travellers, the open loop
        dict(id="i1", text="मरने के बाद, असल में क्या होता है? सुनो... मरने के ठीक तेरह दिन बाद, एक सफ़र शुरू होता है। पूरे "
                           "एक साल का, पैदल।", gap=G),
        dict(id="i2", text="न खाना, न पानी, न छाँव। और साथ में चलेंगे, यमराज के दो दूत।"),
        dict(id="i3", text="ये कोई डरावनी फ़िल्म नहीं है। गरुड़ पुराण में, भगवान विष्णु ने ख़ुद गरुड़ को, ये सफ़र दिन-ब-दिन "
                           "बताया है।", gap=G),
        dict(id="i4", text="आज ये सफ़र, हम दो लोगों के साथ करेंगे।"),
        dict(id="i5", text="पहला: सेठ धनीराम। शहर का सबसे अमीर आदमी... और सबसे बड़ा कंजूस।"),
        dict(id="i6", text="दूसरा: भोला। उसी गली का, एक ग़रीब पानी वाला।", gap=G),
        dict(id="i7", text="धनीराम और भोला, कहानी के लिए हमारे दो मुसाफ़िर हैं। पर उनके साथ जो होगा, वो सब गरुड़ पुराण में "
                           "लिखा है।"),
        dict(id="i8", text="और आख़िर तक देखना... क्योंकि इन दोनों में से एक को, यमराज डराएँगे... और दूसरे के पैर, ख़ुद "
                           "यमराज धोएँगे।", gap=G),
        # the two lives, the night of death, the first trip and the return
        dict(id="d1", text="धनीराम की दुकान पर, गर्मी में कोई प्यासा पानी माँगता, तो वो कहता: पानी मुफ़्त नहीं आता भाई, आगे "
                           "बढ़ो।"),
        dict(id="d2", text="उसकी तिजोरी सोने से भरी थी। पर उसने ज़िंदगी में, किसी को एक रोटी भी मुफ़्त नहीं दी।"),
        dict(id="d3", text="और भोला? वो दिन भर पानी बेचता था... पर जो प्यासा पैसे न दे पाता, उसे मुफ़्त में पिला देता।"),
        dict(id="d4", text="हर सुबह, अपनी रोटी में से आधी, गली की गाय को खिलाता। और शाम को, अपनी बूढ़ी माँ के पैर दबाता।",
             gap=G),
        dict(id="d5", text="फिर एक ही रात, दोनों की ज़िंदगी पूरी हो गई।"),
        dict(id="d6", text="गरुड़ पुराण कहता है: आख़िरी पल में, इंसान को सारी दुनिया एक साथ दिखती है। और वो कुछ बोल नहीं "
                           "पाता।"),
        dict(id="d7", text="तभी धनीराम के कमरे में, दो दूत आए। कौवे जैसे काले, खड़े बाल, हाथ में फंदा और डंडा।", gap=G),
        dict(id="d8", text="उन्होंने धनीराम के शरीर से, उसकी आत्मा खींचकर बाहर निकाली। अंगूठे जितनी छोटी।"),
        dict(id="d9", text="छोटा सा धनीराम चिल्लाया: हाय, हाय! और अपने ही शरीर को, देखता रह गया।"),
        dict(id="d10", text="दूतों ने उसके गले में फंदा डाला, और बोले: चल, जल्दी चल!"),
        dict(id="d11", text="धनीराम ने झट से जेब टटोली: भाई साहब, कुछ ले-देकर बात कर लें? पर अब तो, उसकी जेब ही नहीं थी।",
             gap=G),
        dict(id="d12", text="दूत उसे थोड़ी ही देर में, यमराज के सामने ले गए। और फिर यमराज के हुक्म से, हवा में उड़ाकर, वापस "
                            "घर ले आए।"),
        dict(id="d13", text="घर में सब रो रहे थे। धनीराम अपने शरीर में वापस घुसना चाहता था... पर फंदा, उसे पीछे खींचे रखता।",
             gap=G),
        # ten days, ten rice-balls: the new body
        dict(id="p1", text="अब धनीराम के पास, शरीर ही नहीं था। तो आगे का सफ़र, वो करेगा कैसे?"),
        dict(id="p2", text="गरुड़ पुराण कहता है: दस दिन तक, बेटा चावल के पिंड चढ़ाता है। और हर पिंड से, नए शरीर का एक "
                           "हिस्सा बनता है।", gap=G),
        dict(id="p3", text="पहले दिन, सिर बना। दूसरे दिन, गर्दन और कंधे। तीसरे दिन, दिल।"),
        dict(id="p4", text="चौथे दिन पीठ, पाँचवें दिन नाभि। फिर कमर, जांघें, घुटने, और पैर।"),
        dict(id="p5", text="और दसवें दिन? भूख... और प्यास।", gap=G),
        dict(id="p6", text="पर एक मज़ेदार बात: हर पिंड के चार हिस्से होते हैं। दो से शरीर बनता है, एक धनीराम खाता है... और "
                           "एक? यमदूतों का हिस्सा!", gap=G),
        dict(id="p7", text="धनीराम बोला: यहाँ भी कमीशन?"),
        dict(id="p8", text="ये नया शरीर, बस एक हाथ जितना था। और तेरहवें दिन, दूत उसे, पकड़े हुए बंदर की तरह बाँधकर, सफ़र पर "
                           "ले चले।", gap=G),
        # the road
        dict(id="w1", text="यमराज के नगर का रास्ता: छियासी हज़ार योजन लंबा।"),
        dict(id="w2", text="और रोज़ चलना है, दो सौ सैंतालीस योजन। दिन भी, रात भी।", gap=G),
        dict(id="w3", text="धनीराम ने उँगलियों पर हिसाब लगाया... और उसके होश उड़ गए। ये तो रोज़, हज़ारों किलोमीटर है!"),
        dict(id="w4", text="रास्ते में न पेड़ की छाँव, न खाना, न पानी। और आसमान में, बारह सूरज जल रहे थे।"),
        dict(id="w5", text="कहीं काँटे, कहीं गरम रेत, कहीं तलवार जैसे पत्तों वाला जंगल।", gap=G),
        dict(id="w6", text="धनीराम गिरता, उठता, फिर गिरता। और दूत पीछे से कहते: चलता रह!"),
        dict(id="w7", text="पूरे सत्रह दिन चलने के बाद, अठारहवें दिन, पहला नगर आया: सौम्य नगर।", gap=G),
        # the cities
        dict(id="c1", text="वहाँ एक सुंदर नदी थी, और एक बरगद का पेड़। धनीराम पेड़ के नीचे बैठकर रोने लगा: मेरी तिजोरी! मेरा "
                           "घर! मेरा बेटा!"),
        dict(id="c2", text="तब वहाँ के लोग और दूत बोले: कहाँ है अब तेरा धन? कहाँ हैं तेरे बेटे? यहाँ तो बस, तेरे कर्म चलते "
                           "हैं।", gap=G),
        dict(id="c3", text="सफ़र में खाना साथ लेकर चलते हैं, ये तो बच्चे भी जानते हैं। और इस रास्ते पर, न कुछ ख़रीदा जाता है, "
                           "न बेचा जाता है।"),
        dict(id="c4", text="धनीराम ने पहली बार सोचा: काश, मैंने ज़िंदगी में कुछ दान किया होता।", gap=G),
        dict(id="c5", text="आगे का रास्ता, वो बस उन पिंडों के सहारे चला, जो घर पर हर महीने चढ़ाए जाते।"),
        dict(id="c6", text="अगले नगर में, मौत जैसा दिखने वाला एक राजा मिला। उसे देखते ही, धनीराम ने हिम्मत छोड़ दी।"),
        dict(id="c7", text="चौथे महीने, एक नगर में, आसमान से पत्थर बरसे।", gap=G),
        dict(id="c8", text="महीने बीतते गए, नगर आते गए। एक नगर में चारों तरफ़ रोने की आवाज़ें, एक में तपती गर्मी, एक में "
                           "बादल ही बादल।"),
        dict(id="c9", text="और भोला? वो कहाँ था? इस पूरे रास्ते पर, उसका कहीं नामो-निशान नहीं था।", gap=G),
        # the Vaitarani
        dict(id="v1", text="छठे महीने, धनीराम पहुँचा एक अजीब नगर में। वहाँ का राजा, विचित्र, ख़ुद यमराज का छोटा भाई था।"),
        dict(id="v2", text="और उस नगर के आगे बहती थी: वैतरणी नदी।", gap=G),
        dict(id="v3", text="सौ योजन चौड़ी। पानी की जगह, ख़ून बहता था। अंदर मगरमच्छ, और ऊपर गिद्ध।"),
        dict(id="v4", text="किनारे पर कुछ मछुआरे, एक नाव लेकर खड़े थे। बोले: नदी पार करनी है?"),
        dict(id="v5", text="धनीराम ख़ुश हो गया: हाँ, हाँ! कितने पैसे?", gap=G),
        dict(id="v6", text="मछुआरे बोले: यहाँ पैसे नहीं चलते। ज़िंदगी में गाय दान की थी? तो नाव आएगी। वरना नहीं।"),
        dict(id="v7", text="वैतरणी का मतलब ही यही है। वितरण, यानी दान। जो दान से पार हो, वो वैतरणी।", gap=G),
        dict(id="v8", text="धनीराम ने ज़िंदगी में, एक बछड़ा तक दान नहीं किया था। वो बोला: हाय राम!"),
        dict(id="v9", text="उसे देखते ही, नदी उबलने लगी। जैसे कढ़ाई में घी।"),
        dict(id="v10", text="और फिर दूत उसे, काँटे में फँसी मछली की तरह लटकाकर, हवा में उड़ते हुए, नदी के पार ले गए।", gap=G),
        # the cold city, the last body
        dict(id="s1", text="साल के आख़िर में, आया शीत नगर। वहाँ की ठंड, हिमालय से सौ गुना ज़्यादा।"),
        dict(id="s2", text="काँपता हुआ धनीराम, दसों दिशाओं में देखने लगा: कोई अपना है, जो मुझे बचा ले?"),
        dict(id="s3", text="दूतों ने पूछा: तेरे पास कौन सा पुण्य है? और धनीराम के पास, कोई जवाब नहीं था।", gap=G),
        dict(id="s4", text="आख़िरी नगर में, उसका वो हाथ भर का शरीर भी छूट गया। और अंगूठे जितनी आत्मा, आगे बढ़ी।"),
        dict(id="s5", text="और एक साल बाद, आख़िरकार... सामने था, यमराज का नगर।", gap=G),
        # Yama's court
        dict(id="y1", text="यमराज के नगर के, चार दरवाज़े हैं। और धनीराम जैसों के लिए: दक्षिण का दरवाज़ा।"),
        dict(id="y2", text="पहरेदार ने ख़बर दी चित्रगुप्त को। चित्रगुप्त, यानी यमराज के मुनीम, जो हर इंसान के कर्मों का हिसाब "
                           "रखते हैं।"),
        dict(id="y3", text="पर चित्रगुप्त को, ये सारा हिसाब मिलता कैसे है?", gap=G),
        dict(id="y4", text="गरुड़ पुराण कहता है: ब्रह्मा जी के कुछ बेटे हैं, श्रवण। जो धरती, आकाश, पाताल, हर जगह घूमते हैं। "
                           "दूर से सुनते हैं, दूर तक देखते हैं।"),
        dict(id="y5", text="हर इंसान ने, छुपकर या खुलेआम, जो कहा और जो किया, वो सब, ये चित्रगुप्त को बता देते हैं।", gap=G),
        dict(id="y6", text="और गवाह? सूरज, चाँद, आग, हवा, धरती, पानी, दिन, रात... और ख़ुद इंसान का दिल।", gap=G),
        dict(id="y7", text="धनीराम ने सोचा: मेरा मुनीम तो, हिसाब में थोड़ी गड़बड़ कर देता था। यहाँ भी कुछ जुगाड़ हो जाएगा।"),
        dict(id="y8", text="पर चित्रगुप्त, कभी ग़लती नहीं करते।"),
        dict(id="y9", text="फिर धनीराम को दिखा, यमराज का रूप। भैंसे पर सवार, पहाड़ जितने बड़े, हाथ में दंड, और प्रलय के बादल "
                           "जैसी गरज।", gap=G),
        dict(id="y10", text="धनीराम थर-थर काँपने लगा।"),
        dict(id="y11", text="चित्रगुप्त बोले: यमराज के लिए, मूर्ख और विद्वान, भिखारी और अमीर, कमज़ोर और ताक़तवर, सब बराबर हैं।",
             gap=G),
        dict(id="y12", text="धनीराम हाथ जोड़कर बोला: माफ़ कर दो! दूत बोले: माफ़ करना, भगवान विष्णु का काम है। हम तो बस, "
                            "हुक्म मानते हैं।", gap=G),
        # the twist: Bhola at the eastern gate
        dict(id="t1", text="तभी, पूरब के दरवाज़े पर, एक रथ आकर रुका।"),
        dict(id="t2", text="पूरब का रास्ता: हीरों से जड़ा, पारिजात के पेड़ों की छाँव, और किनारे तैरते हंस।"),
        dict(id="t3", text="और उस रथ से उतरा... भोला।", gap=G),
        dict(id="t4", text="वही भोला, जो प्यासों को मुफ़्त पानी पिलाता था, गाय को रोटी खिलाता था, और माँ की सेवा करता था।"),
        dict(id="t5", text="और फिर जो हुआ, उसे देखकर, धनीराम की आँखें फटी की फटी रह गईं।", gap=G),
        dict(id="t6", text="वही यमराज, जिनसे धनीराम काँप रहा था... अपने सिंहासन से उठ खड़े हुए।"),
        dict(id="t7", text="आगे बढ़कर, बार-बार भोला का स्वागत किया। उसे अपना सिंहासन दिया... और झुककर, उसके पैर धोए।",
             gap=G),
        dict(id="t8", text="गरुड़ पुराण कहता है: बुरे कर्म वालों को, यमराज डरावने दिखते हैं। और अच्छे कर्म वालों का, वही "
                           "यमराज, उठकर स्वागत करते हैं।", gap=G),
        # outro: the callback and the question
        dict(id="o1", text="धनीराम की तिजोरी, घर पर ही रह गई। और भोला का पानी का घड़ा?"),
        dict(id="o2", text="उसका पुण्य बनकर, पूरे रास्ते, उसके साथ चला।"),
        dict(id="o3", text="धनीराम को अब, अपने कर्मों का हिसाब चुकाना था। क्योंकि गरुड़ पुराण कहता है: कर्म का फल भोगे बिना, "
                           "कोई कर्म मिटता नहीं।", gap=G),
        dict(id="o4c", text="याद है, वो एक साल का सफ़र? उस रास्ते पर, न कुछ ख़रीदा जाता है, न बेचा जाता है। जो साथ ले जाना "
                            "है, वो यहीं कमाना पड़ता है।", gap=G),
        dict(id="o5", text="तो अगर कल आपका सफ़र शुरू हो, तो आप किस दरवाज़े से जाओगे: धनीराम वाले, या भोला वाले? ईमानदारी से, "
                           "कमेंट में बताओ।"),
    ],
}

# YouTube chapters: first line id of each part -> chapter title (finish.py writes them with the real timestamps)
CHAPTERS = {
    "hi": [
        ("i1", "Marne ke baad asal mein kya hota hai?"),
        ("d1", "Dhaniram aur Bhola: aakhri raat"),
        ("p1", "10 din, 10 pind: naya shareer"),
        ("w1", "86,000 yojan ka raasta"),
        ("c1", "Solah nagar"),
        ("v1", "Vaitarani nadi aur naav"),
        ("s1", "Sheet nagar"),
        ("y1", "Yamraj ka darbar aur Chitragupt"),
        ("t1", "Poorab ka darwaza"),
        ("o1", "Aap kis darwaze se jaoge?"),
    ],
}

_SOURCES = ["Garuda Purana, Preta Kalpa (Saroddhara), chapters I-III and XIV, Ernest Wood and S. V. Subrahmanyam "
            "translation"]
METADATA = {
    "hi": dict(
        title="Marne ke baad asal mein kya hota hai?",
        caption="Marne ke baad asal mein kya hota hai? Marne ke theek 13 din baad ek safar shuru hota hai: poore ek "
                "saal ka, paidal. Na khaana, na paani, na chhaanv 😳\n\nGarud Puran mein Bhagwan Vishnu ne Garud ko yeh safar din-ba-din bataya hai: "
                "10 pindon se bana naya shareer, 86,000 yojan ka raasta, solah nagar, Vaitarani nadi, Chitragupt ka "
                "hisaab... aur Yamraj ke do roop.\n\nAap kis darwaze se jaoge: Dhaniram wale ya Bhola wale? "
                "Comment mein batao 👇",
        yt_title="Marne Ke Baad Asal Mein Kya Hota Hai? 😳 Garud Puran Ka Poora Safar",
        yt_description="Garud Puran (Preta Kalpa) ke mutabik marne ke baad aatma ka poora safar, ek kahani mein: do "
                       "musafir, kanjoos Seth Dhaniram aur gareeb paani wala Bhola, ek hi raat duniya chhodte hain. "
                       "Yamdoot, angoothe jitni aatma, 10 din ke pind se bana naya shareer, 86,000 yojan ka raasta aur "
                       "solah nagar, Vaitarani nadi aur gaay daan ki naav, Shravan aur Chitragupt ka hisaab, aur "
                       "Yamraj ke do roop. Dhaniram aur Bhola kahani ke liye hain; unke saath jo hota hai, woh Garud "
                       "Puran mein likha hai.",
        hashtags=["#garudpuran", "#yamraj", "#mythology", "#kahani", "#hindu"],
        pinned_comment="Aap kis darwaze se jaoge: Dhaniram wale, ya Bhola wale? Imaandari se batao 👇",
        sources=_SOURCES),
}


USED_ASSETS, CREDITS_FILES = [], []      # everything in this video is drawn in code


def draw(cr, t, tl):
    from scenes_yamlok_yatra import draw as _draw
    _draw(cr, t, tl)


def sfx(tl):
    from scenes_yamlok_yatra import sfx as _sfx
    return _sfx(tl)
