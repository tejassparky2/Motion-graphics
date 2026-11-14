"""Mythology long video 3 (Hindi only first): what happened after the Ramayana, as ONE continuous story (owner, 14 Nov
2026, picking option 1 of three: "Go with 1"; topic "रामायण के बाद क्या हुआ?", posted on a Sunday at noon). Rides the
Ramayana film (Part 1 opened 6 Nov 2026): the film ends at the war; Valmiki's last book, the Uttara Kanda, goes on.
Landscape 16:9, about 7 minutes, shadow puppets, the fast camera (camera_beats), one short whole sentence per line.

Respect: Rama, Sita and Lakshmana with dignity; the question is left to the viewer (a king's duty or his family?).
One honest line says the Ramcharitmanas does not have this part. Sita's return to the earth is a throne of light and
the Earth goddess; Lakshmana's end is meditation by the river; no death is shown.

Facts (Valmiki Ramayana, Uttara Kanda, Hari Prasad Shastri translation, wisdomlib.org; Bala Kanda for Sita's birth):
- 42: Sita, expecting a child, wishes to visit the hermitages on the Ganga; Rama: tomorrow you shall go.
- 43: Rama asks his friends what the people say; Bhadra: they praise you, but "What pleasure can his heart experience
  in possessing Sita, whom Ravana formerly held in his lap ... has taken his spouse into his house again"; and "we too
  shall have to put up with such conduct in our wives, for subjects follow the king". Rama is stricken with grief.
- 45: Rama calls his brothers: his inner self knows Sita is pure, but the people's censure is unbearable to a king;
  Lakshmana is to take her across the Ganga and leave her near Valmiki's hermitage.
- 47-48: across the river Lakshmana weeps and tells her; she falls to the ground; she would end her life in the Ganga
  "lest I bring the royal line to an end" ("I am far advanced in pregnancy"); "I am not distressed on mine own
  account". 49: Valmiki, told by the hermit boys, takes her to his hermitage.
- 66: the twins Kusha and Lava are born in Valmiki's hermitage. 93-94: Valmiki has taught them his poem; at Rama's
  great sacrifice (91-92: in the Naimisha forest; a golden image of Sita sits beside Rama) they sing it before him;
  people say they look like Rama; they refuse the gold. 95: Rama learns they are Sita's sons and asks that Sita take
  an oath before the assembly. 96: Valmiki swears to her purity.
- 97: Sita: if she has never thought of anyone but Rama, may the Earth goddess (Madhavi) receive her; a celestial throne
  rises from the earth, the goddess takes her in her arms, and she enters the earth. Bala Kanda 66: Janaka found her
  in a ploughed field. 98: Rama, in grief and anger, demands Sita back from the Earth. 99: Rama takes no other wife; a
  golden Sita at every sacrifice.
- 103-104: Death (Kala), in the form of an ascetic, comes with Brahma's message that Rama's work on earth is done;
  "whoever shall overhear us should be put to death by you"; Lakshmana stands at the door. 105: Durvasa demands to
  see Rama at once and threatens to curse the kingdom, the city, Rama, Bharata and the whole House; Lakshmana: "It were
  better that I should perish than all others be destroyed!" 106: Lakshmana: keep your vow; Vasishtha: a broken
  promise destroys righteousness; Rama banishes him ("a sentence of banishment or death is the same to men of
  honour"); Lakshmana sits by the Sarayu, restrains his breath, flowers rain, Indra (Shakra) carries him to heaven.
- 107-108: Kusha gets Kushavati, Lava Shravasti; to Hanuman: "As long as my story is told in the world ... so long
  mayest you be happy" (Uttara 40: Hanuman's boon to live as long as Rama's story is told). 110: Rama walks to the
  Sarayu with the people of Ayodhya; Brahma and the gods appear; Rama enters the river and his Vishnu form; those who
  followed reach heaven.
"""
from channel import ASSETS_ROOT, MUSIC, NARRATORS, NARRATOR_LABEL, REVEAL_GAP, TAIL  # noqa: F401

FORMAT = "landscape"      # 1920x1080
G = REVEAL_GAP
_LINES = [
    # hook
    ("u001", "रामायण मूवी में रावण मारा जाता है, और कहानी ख़त्म हो जाती है।"),
    ("u002", "पर वाल्मीकि रामायण वहाँ ख़त्म नहीं होती।"),
    ("u003", "उसके बाद राम को, अपनी पत्नी सीता को जंगल भेजना पड़ा।"),
    ("u004", "अपने ही बेटों को, वो सालों तक पहचान नहीं पाए।"),
    ("u005", "और अपने सबसे प्यारे भाई लक्ष्मण को, उन्होंने ख़ुद त्याग दिया।", G),
    ("u006", "ये है रामायण का आख़िरी हिस्सा, उत्तर कांड।"),
    ("u007", "तुलसीदास जी की रामचरितमानस में ये हिस्सा नहीं है, पर वाल्मीकि रामायण में है।"),
    ("u008", "तो चलो, सुनते हैं रामायण के बाद की कहानी।", G),
    # the happy years
    ("u009", "रावण को हराकर, राम सीता और लक्ष्मण के साथ अयोध्या लौटे।"),
    ("u010", "राम राजा बने, और अयोध्या में ख़ुशियाँ ही ख़ुशियाँ थीं।"),
    ("u011", "कुछ समय बाद, सीता माँ बनने वाली थीं।"),
    ("u012", "राम ने ख़ुशी से पूछा: तुम्हें क्या चाहिए?"),
    ("u013", "सीता बोलीं: मैं गंगा किनारे के ऋषियों के आश्रम देखना चाहती हूँ।"),
    ("u014", "राम ने कहा: ठीक है, कल ही चली जाना।", G),
    # the rumour
    ("u015", "उसी रात, राम ने अपने दोस्तों से पूछा: लोग मेरे बारे में क्या कहते हैं?"),
    ("u016", "एक दोस्त पहले तो चुप रहा।"),
    ("u017", "फिर डरते डरते बोला: लोग आपकी तारीफ़ करते हैं, पर एक बात भी कहते हैं।"),
    ("u018", "सीता महीनों तक रावण की लंका में रहीं।"),
    ("u019", "फिर भी राजा उन्हें वापस घर ले आए।"),
    ("u020", "अब हमें भी अपनी पत्नियों की ऐसी बातें सहनी पड़ेंगी।"),
    ("u021", "ये सुनकर, राम का दिल टूट गया।", G),
    ("u022", "राम जानते थे कि सीता पूरी तरह पवित्र हैं।"),
    ("u023", "पर वो राजा थे, और राजा को अपनी प्रजा की बात सुननी पड़ती है।"),
    ("u024", "उन्होंने अपने भाइयों को बुलाया।"),
    ("u025", "और लक्ष्मण से कहा: कल सुबह, सीता को गंगा पार जंगल में छोड़ आओ।", G),
    ("u026", "तो क्या राम ने सही किया: एक राजा की तरह, या एक पति की तरह?", G),
    # Sita in the forest
    ("u027", "अगली सुबह, सीता ख़ुशी ख़ुशी रथ में बैठीं।"),
    ("u028", "उन्हें लगा, वो आश्रम घूमने जा रही हैं।"),
    ("u029", "गंगा पार करके, लक्ष्मण फूट फूटकर रोने लगे।"),
    ("u030", "फिर उन्होंने सीता को सच बता दिया: राम ने आपको त्याग दिया है।"),
    ("u031", "सीता वहीं ज़मीन पर गिर पड़ीं।", G),
    ("u032", "फिर उन्होंने कहा: मैं गंगा में कूदकर जान दे देती।"),
    ("u033", "पर मेरे पेट में राजा का वंश है।"),
    ("u034", "राम से कहना, मैं अपने लिए दुखी नहीं हूँ।"),
    ("u035", "लक्ष्मण रोते रोते अयोध्या लौट गए।", G),
    ("u036", "जंगल में अकेली रोती सीता के पास, एक ऋषि आए।"),
    ("u037", "वो ऋषि थे, वाल्मीकि।"),
    ("u038", "वही वाल्मीकि, जिन्होंने रामायण लिखी।"),
    ("u039", "वाल्मीकि सीता को बेटी की तरह अपने आश्रम ले गए।", G),
    # Lava and Kusha
    ("u040", "कुछ दिनों बाद, आश्रम में सीता ने जुड़वाँ बेटों को जन्म दिया।"),
    ("u041", "उनके नाम रखे गए: लव और कुश।"),
    ("u042", "वाल्मीकि ने दोनों को पढ़ाया, और एक लंबा गीत सिखाया।"),
    ("u043", "वो गीत था, पूरी रामायण।"),
    ("u044", "यानी, उनके अपने पिता की कहानी।"),
    ("u045", "पर लव और कुश को, ये बात पता नहीं थी।", G),
    ("u046", "सालों बाद, राम ने एक बहुत बड़ा यज्ञ किया।"),
    ("u047", "राम ने दूसरी शादी नहीं की थी।"),
    ("u048", "यज्ञ में उनके पास, सीता की सोने की मूर्ति बैठी थी।", G),
    ("u049", "वाल्मीकि लव और कुश को लेकर वहाँ पहुँचे।"),
    ("u050", "दोनों बच्चों ने, राम के सामने रामायण गाई।"),
    ("u051", "राम अपनी ही कहानी, दो बच्चों के मुँह से सुन रहे थे।"),
    ("u052", "लोग हैरान थे: ये बच्चे तो बिल्कुल राम जैसे दिखते हैं!"),
    ("u053", "राम ने उन्हें सोना देना चाहा, पर बच्चों ने मना कर दिया।"),
    ("u054", "बोले: हम आश्रम में रहते हैं, हमें सोने का क्या करना?"),
    ("u055", "फिर राम को पता चला, ये सीता के बेटे हैं, यानी उनके अपने बेटे।", G),
    # Sita returns to the Earth
    ("u056", "राम ने सीता को बुलवाया।"),
    ("u057", "पर एक शर्त रखी: सीता सबके सामने क़सम खाएँ कि वो पवित्र हैं।"),
    ("u058", "अगले दिन भरी सभा में, वाल्मीकि सीता को लेकर आए।"),
    ("u059", "वाल्मीकि बोले: मैं क़सम खाता हूँ, सीता पूरी तरह पवित्र हैं।"),
    ("u060", "फिर सीता ने हाथ जोड़कर धरती माँ से विनती की।"),
    ("u061", "अगर मैंने राम के सिवा कभी किसी के बारे में नहीं सोचा, तो धरती माँ मुझे अपनी गोद में ले लो।", G),
    ("u062", "तभी धरती फटी, और एक चमकता हुआ सिंहासन ऊपर आया।"),
    ("u063", "धरती माँ ने सीता को अपनी गोद में बिठाया।"),
    ("u064", "और सीता, सबके सामने धरती में समा गईं।", G),
    ("u065", "सीता धरती से ही पैदा हुई थीं।"),
    ("u066", "राजा जनक को वो खेत जोतते हुए, धरती में मिली थीं।"),
    ("u067", "और आख़िर में, वो धरती में ही लौट गईं।", G),
    ("u068", "राम दुख और ग़ुस्से में, धरती से सीता को वापस माँगने लगे।"),
    ("u069", "पर सीता कभी वापस नहीं आईं।", G),
    # Death at the door
    ("u070", "बहुत साल बीत गए।"),
    ("u071", "एक दिन, एक तपस्वी राम से मिलने आया।"),
    ("u072", "पर वो कोई आम तपस्वी नहीं था।"),
    ("u073", "वो ख़ुद काल था, यानी मौत का रूप।", G),
    ("u074", "काल बोला: हमारी बात अकेले में होगी।"),
    ("u075", "और जो भी हमारी बात सुनेगा या देखेगा, उसे मौत की सज़ा देनी होगी।"),
    ("u076", "राम ने वादा किया, और लक्ष्मण को दरवाज़े पर खड़ा कर दिया।"),
    ("u077", "अंदर काल ने कहा: धरती पर आपका काम पूरा हो गया है।", G),
    ("u078", "तभी बाहर, ऋषि दुर्वासा आ गए।"),
    ("u079", "दुर्वासा, जिनका ग़ुस्सा सबसे ज़्यादा मशहूर था।"),
    ("u080", "बोले: मुझे अभी इसी वक़्त राम से मिलना है।"),
    ("u081", "लक्ष्मण ने विनती की: बस थोड़ी देर रुक जाइए।"),
    ("u082", "दुर्वासा भड़क गए: अभी नहीं जाने दिया, तो पूरे राज्य को श्राप दे दूँगा!", G),
    ("u083", "लक्ष्मण ने सोचा: सबके मरने से अच्छा है, अकेला मैं मरूँ।"),
    ("u084", "और वो अंदर चले गए।", G),
    ("u085", "राम ने अपने सबसे प्यारे भाई को देखा, और सब समझ गए।"),
    ("u086", "अब राम क्या करते? वादा तोड़ते, या भाई को खोते?", G),
    ("u087", "लक्ष्मण बोले: भैया, दुखी मत होइए, अपना वादा निभाइए।"),
    ("u088", "गुरु वशिष्ठ ने भी कहा: वादा टूटा, तो धर्म टूट जाएगा।"),
    ("u089", "तब राम ने भारी मन से कहा: लक्ष्मण, मैं तुम्हें त्यागता हूँ।"),
    ("u090", "क्योंकि इज़्ज़तदार इंसान के लिए, त्याग और मौत एक बराबर हैं।", G),
    ("u091", "लक्ष्मण चुपचाप सरयू नदी के किनारे गए।"),
    ("u092", "उन्होंने ध्यान लगाया, और अपनी साँस रोक ली।"),
    ("u093", "देवताओं ने फूल बरसाए, और उन्हें स्वर्ग ले गए।", G),
    ("u094", "जो लक्ष्मण चौदह साल राम के साथ जंगल में रहे, उनका अंत राम के ही एक वादे से हुआ।", G),
    # Rama's end
    ("u095", "लक्ष्मण के बिना, राम भी अब धरती पर रहना नहीं चाहते थे।"),
    ("u096", "उन्होंने अपना राज्य अपने बेटों में बाँट दिया।"),
    ("u097", "कुश को कुशावती मिली, और लव को श्रावस्ती।"),
    ("u098", "फिर राम ने हनुमान से कहा: तुम धरती पर ही रहना।"),
    ("u099", "जब तक दुनिया में मेरी कहानी सुनाई जाएगी, तब तक तुम ज़िंदा रहोगे।"),
    ("u100", "कहते हैं, इसीलिए हनुमान जी आज भी धरती पर हैं।", G),
    ("u101", "फिर एक सुबह, राम सरयू नदी की तरफ़ चल पड़े।"),
    ("u102", "उनके पीछे पीछे, अयोध्या के लोग भी चल पड़े।"),
    ("u103", "कोई भी अपने राम के बिना रहना नहीं चाहता था।"),
    ("u104", "आसमान में ब्रह्मा जी और सारे देवता आ गए।"),
    ("u105", "राम सरयू के पानी में उतरे।"),
    ("u106", "और अपने असली रूप, भगवान विष्णु में लौट गए।"),
    ("u107", "उनके पीछे आए सब लोग भी, स्वर्ग पहुँच गए।", G),
    # the end
    ("u108", "तो ये थी, रामायण के बाद की कहानी।"),
    ("u109", "जिस राम ने रावण जैसे राक्षस को हराया, उन्हें अपने ही फ़र्ज़ के लिए अपना परिवार खोना पड़ा।"),
    ("u110", "पहले सीता चली गईं, फिर लक्ष्मण भी चले गए।", G),
    ("u111", "तो तुम बताओ: राजा का धर्म बड़ा होता है, या परिवार का? कमेंट में बताओ।"),
]
SCRIPTS = {"hi": [dict(id=x[0], text=x[1], **({"gap": x[2]} if len(x) > 2 else {})) for x in _LINES]}

CHAPTERS = {"hi": [
    ("u001", "Ramayan ke baad kya hua?"),
    ("u009", "Ayodhya ke khushi ke din"),
    ("u015", "Ek afwaah"),
    ("u027", "Sita jungle mein"),
    ("u040", "Lav aur Kush"),
    ("u056", "Sita dharti mein"),
    ("u070", "Kaal darwaze par"),
    ("u095", "Ram ka ant"),
    ("u108", "Raja ka dharm, ya parivaar?"),
]}

_SOURCES = ["Valmiki Ramayana, Uttara Kanda 42-110 and Bala Kanda 66 (Hari Prasad Shastri translation)"]
METADATA = {
    "hi": dict(
        title="Ramayan ke baad kya hua?",
        caption="Ramayana movie Ravan ki maut par khatam hoti hai... par Valmiki Ramayan wahan khatam nahi hoti 😳\n\n"
                "Uttar Kand: Sita ka jungle jaana, Lav-Kush ka Ram ke saamne Ramayan gaana, Sita ka dharti mein samaana, "
                "aur Kaal ke ek vaade ki wajah se Lakshman ka tyaag.\n\n"
                "Raja ka dharm bada, ya parivaar? Comment mein batao 👇",
        yt_title="Ramayan Ke Baad Kya Hua? 😳 | Sita, Lav-Kush Aur Lakshman Ka Ant | Uttar Kand",
        yt_description="Ramayana movie Ravan ki maut par khatam hoti hai, par Valmiki Ramayan ka aakhri hissa, Uttar Kand, "
                       "aage ki kahani batata hai. Ek afwaah ki wajah se Ram ne garbhvati Sita ko jungle bheja. "
                       "Valmiki ke aashram mein Lav aur Kush paida hue, aur saalon baad unhone Ram ke saamne hi Ramayan "
                       "gaayi. Sita ne sabha mein dharti maa se vinti ki aur dharti mein samaa gayi. Phir Kaal, yaani "
                       "maut, Ram se milne aaya, aur Durvasa rishi ke gusse ki wajah se Ram ko apne bhai Lakshman ka "
                       "tyaag karna pada. Aakhir mein Ram Saryu nadi mein utarkar Vishnu roop mein laut gaye. "
                       "Tulsidas ji ki Ramcharitmanas mein yeh hissa nahi hai; yeh Valmiki Ramayan ke Uttar Kand se hai.",
        hashtags=["#ramayan", "#uttarkand", "#ramayanamovie", "#mythology", "#hindu"],
        pinned_comment="Raja ka dharm bada hota hai, ya parivaar ka? Aap kya kehte ho? 👇",
        sources=_SOURCES),
}

USED_ASSETS, CREDITS_FILES = [], []      # everything in this video is drawn in code


def draw(cr, t, tl):
    import scenes_uttar_kand as S
    S.draw(cr, t, tl)


def sfx(tl):
    import scenes_uttar_kand as S
    return S.sfx(tl)
