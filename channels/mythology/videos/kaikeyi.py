"""Mythology video 6: Was Kaikeyi really the villain? A debate reel (owner, 8 Nov 2026: "any interest mind blowing one a
questionable one from ramayana"; script approved: "Ok"). Both sides from the text; the viewer decides. Look: the
Togalu Gombeyaata leather shadow puppets of the Jarasandha reel (owner: "The jarasanda video animation did good"),
with a leather balance scale that tips with each point.

Facts (Valmiki Ramayana, Ayodhya Kanda, verse numbers of the common Southern text, valmikiramayan.net):
- 2.107.3, Rama to Bharata: "puraa bhraataH pitaa naH sa maataram te samudvahan / maataamahe samaashrauShiid
  raajyashulkam anuttamam": when our father married your mother, he promised your maternal grandfather the
  kingdom as the bride-price. 2.107.4: the two boons were a separate promise, made in a war of devas and asuras.
- 2.1.1: Bharata (with Shatrughna) was away at his maternal uncle's home in Kekaya.
- 2.1.46: in his hurry Dasharatha did not invite the Kekaya king or Janaka, thinking they would hear the good news
  later.
- 2.4.25: "viproShitash cha bharato yaavad eva puraad itaH / taavad evaabhiShekas te praaptakaalo mato mama": as
  long as Bharata is away from the city, now is the right time for your coronation.
- Kaikeyi asks for the kingdom for Bharata and 14 years of exile for Rama (sarga 11); Dasharatha dies of grief
  (sarga 64); Bharata rebukes his mother and refuses the throne (sargas 73-74); Rama tells Bharata of the old
  promise but stays in the forest to keep his father's word (sargas 107-111); Bharata rules from Nandigrama with
  Rama's sandals on the throne (sargas 112-115).
"""
from channel import ASSETS_ROOT, MUSIC, NARRATORS, NARRATOR_LABEL, REVEAL_GAP, TAIL  # noqa: F401

SCRIPTS = {
    "hi": [
        dict(id="k1", text="सोचो, जिस कैकेयी को हज़ारों साल से खलनायिका कहा गया... अयोध्या का राज, असल में उसी के बेटे का था।",
             gap=REVEAL_GAP),
        dict(id="k2", text="और ये बात किसी और ने नहीं, ख़ुद राम ने भरत से कही थी। वाल्मीकि रामायण, अयोध्या कांड।"),
        dict(id="k3", text="जब दशरथ ने कैकेयी से शादी की, तो उसके पिता, केकय के राजा से एक वादा किया।"),
        dict(id="k4", text="शादी के बदले, राज्य। यानी कैकेयी का बेटा ही अयोध्या का राजा बनेगा।", gap=REVEAL_GAP),
        dict(id="k5", text="सालों बाद, दशरथ ने राम का राज्याभिषेक तय किया। पर उस वक़्त भरत कहाँ था?"),
        dict(id="k6", text="अपने मामा के घर, केकय में। और दशरथ ने ख़ुद कहा: भरत जब तक नगर से बाहर है, यही सही समय है।"),
        dict(id="k7", text="और जल्दी में, न केकय के राजा को बुलाया, न जनक को। सोचा, बाद में सुन लेंगे।"),
        dict(id="k8", text="तो क्या कैकेयी बस अपना हक़ माँग रही थी?", gap=REVEAL_GAP),
        dict(id="k9", text="रुको। दूसरी तरफ़ भी सुनो।"),
        dict(id="k10", text="कैकेयी ने भरत के लिए राज माँगा... पर साथ में राम के लिए चौदह साल का वनवास भी। वो उस शादी वाले "
                            "वादे में नहीं था।"),
        dict(id="k11", text="बेटे के ग़म में, राजा दशरथ चल बसे।", gap=REVEAL_GAP),
        dict(id="k12", text="और भरत लौटा, तो उसने अपनी माँ को ही धिक्कारा... और राज लेने से मना कर दिया।"),
        dict(id="k13", text="तब राम ने वही पुराना वादा याद दिलाया: राज तुम्हारा ही है। पर पिता का वचन निभाने के लिए, वो ख़ुद "
                            "वन में ही रहेंगे।"),
        dict(id="k14", text="भरत ने राम की खड़ाऊँ सिंहासन पर रखीं, और चौदह साल, राम के नाम पर राज चलाया।", gap=REVEAL_GAP),
        dict(id="k15", text="तो ग़लत कौन था? कैकेयी, या दशरथ, जिन्होंने पुराना वादा भुला दिया? कमेंट में बताओ।"),
    ],
    "kn": [
        dict(id="k1", text="ಯೋಚಿಸಿ... ಸಾವಿರಾರು ವರ್ಷಗಳಿಂದ ಕೈಕೇಯಿಯನ್ನ ಖಳನಾಯಕಿ ಅಂತೀವಿ. ಆದ್ರೆ ಅಯೋಧ್ಯೆಯ ರಾಜ್ಯ, "
                           "ನಿಜವಾಗ್ಲೂ ಅವಳ ಮಗನಿಗೇ ಸೇರಬೇಕಿತ್ತು.", gap=REVEAL_GAP),
        dict(id="k2", text="ಈ ಮಾತನ್ನ ಬೇರೆ ಯಾರೂ ಅಲ್ಲ, ಸ್ವತಃ ರಾಮನೇ ಭರತನಿಗೆ ಹೇಳಿದ್ದ. ವಾಲ್ಮೀಕಿ ರಾಮಾಯಣ, ಅಯೋಧ್ಯಾ ಕಾಂಡ."),
        dict(id="k3", text="ದಶರಥ ಕೈಕೇಯಿಯನ್ನ ಮದುವೆ ಆದಾಗ, ಅವಳ ತಂದೆ, ಕೇಕಯ ರಾಜನಿಗೆ ಒಂದು ಮಾತು ಕೊಟ್ಟಿದ್ದ."),
        dict(id="k4", text="ಮದುವೆಗೆ ಬದಲಾಗಿ, ರಾಜ್ಯ. ಅಂದ್ರೆ, ಕೈಕೇಯಿಯ ಮಗನೇ ಅಯೋಧ್ಯೆಯ ರಾಜ ಆಗ್ತಾನೆ.", gap=REVEAL_GAP),
        dict(id="k5", text="ವರ್ಷಗಳ ನಂತರ, ದಶರಥ ರಾಮನ ಪಟ್ಟಾಭಿಷೇಕ ತೀರ್ಮಾನ ಮಾಡಿದ. ಆದ್ರೆ ಆಗ ಭರತ ಎಲ್ಲಿದ್ದ?"),
        dict(id="k6", text="ತನ್ನ ಸೋದರಮಾವನ ಮನೆಯಲ್ಲಿ, ಕೇಕಯದಲ್ಲಿ. ದಶರಥನೇ ಹೇಳಿದ: ಭರತ ಊರಲ್ಲಿ ಇಲ್ಲದಿರುವಾಗಲೇ, ಇದೇ ಸರಿಯಾದ "
                           "ಸಮಯ."),
        dict(id="k7", text="ಅವಸರದಲ್ಲಿ, ಕೇಕಯ ರಾಜನನ್ನೂ ಕರೀಲಿಲ್ಲ, ಜನಕನನ್ನೂ ಕರೀಲಿಲ್ಲ. ಆಮೇಲೆ ಕೇಳ್ಕೊಳ್ತಾರೆ ಅಂದ್ಕೊಂಡ."),
        dict(id="k8", text="ಹಾಗಾದ್ರೆ, ಕೈಕೇಯಿ ತನ್ನ ಹಕ್ಕನ್ನ ಮಾತ್ರ ಕೇಳ್ತಿದ್ಲಾ?", gap=REVEAL_GAP),
        dict(id="k9", text="ತಡೀರಿ. ಇನ್ನೊಂದು ಕಡೆನೂ ಕೇಳಿ."),
        dict(id="k10", text="ಕೈಕೇಯಿ ಭರತನಿಗೆ ರಾಜ್ಯ ಕೇಳಿದ್ಲು... ಜೊತೆಗೆ ರಾಮನಿಗೆ ಹದಿನಾಲ್ಕು ವರ್ಷ ವನವಾಸ ಕೂಡ. ಅದು ಆ "
                            "ಮದುವೆಯ ಮಾತಲ್ಲಿ ಇರಲಿಲ್ಲ."),
        dict(id="k11", text="ಮಗನ ದುಃಖದಲ್ಲಿ, ದಶರಥ ಪ್ರಾಣ ಬಿಟ್ಟ.", gap=REVEAL_GAP),
        dict(id="k12", text="ಭರತ ವಾಪಸ್ ಬಂದಾಗ, ತನ್ನ ಅಮ್ಮನನ್ನೇ ಬೈದ... ರಾಜ್ಯ ಬೇಡ ಅಂದ."),
        dict(id="k13", text="ಆಗ ರಾಮನೇ ಆ ಹಳೇ ಮಾತು ನೆನಪಿಸಿದ: ರಾಜ್ಯ ನಿನ್ನದೇ. ಆದ್ರೆ ತಂದೆಯ ಮಾತು ಉಳಿಸೋಕೆ, ತಾನು ಕಾಡಲ್ಲೇ "
                            "ಇರ್ತೀನಿ ಅಂದ."),
        dict(id="k14", text="ಭರತ ರಾಮನ ಪಾದುಕೆಗಳನ್ನ ಸಿಂಹಾಸನದ ಮೇಲಿಟ್ಟು, ಹದಿನಾಲ್ಕು ವರ್ಷ ರಾಮನ ಹೆಸರಲ್ಲೇ ರಾಜ್ಯ ನಡೆಸಿದ.",
             gap=REVEAL_GAP),
        dict(id="k15", text="ಹಾಗಾದ್ರೆ ತಪ್ಪು ಯಾರದ್ದು? ಕೈಕೇಯಿದಾ, ಅಥವಾ ಹಳೇ ಮಾತು ಮರೆತ ದಶರಥನದ್ದಾ? ಕಾಮೆಂಟ್ ಮಾಡಿ ಹೇಳಿ."),
    ],
}

_SOURCES = ["Valmiki Ramayana, Ayodhya Kanda 2.1.1, 2.1.46, 2.4.25, 2.107.3"]
METADATA = {
    "hi": dict(
        title="Kya Kaikeyi sach mein villain thi?",
        caption="Socho, jis Kaikeyi ko hazaaron saal se villain kaha gaya... Ayodhya ka raj asal mein usi ke bete ka "
                "tha 😳\n\n"
                "Valmiki Ramayan, Ayodhya Kand: khud Ram ne Bharat ko bataya ki Dashrath ne Kaikeyi se shaadi ke waqt "
                "unke pita ko rajya ka vaada kiya tha. Rajyabhishek tab tay hua jab Bharat Kekay mein the. Par "
                "Kaikeyi ne Ram ke liye 14 saal ka vanvaas bhi maanga.\n\n"
                "Galat kaun tha: Kaikeyi ya Dashrath? Comment mein batao 👇",
        yt_title="Kya Kaikeyi Sach Mein Villain Thi? 😳 | Ram Ne Khud Bataya | Ramayan",
        yt_description="Valmiki Ramayan (Ayodhya Kand 2.107.3) mein Ram Bharat se kehte hain: jab pita ji ne tumhari maa "
                       "se vivah kiya, tab tumhare nana ko rajya shulk ka vaada kiya tha. Dashrath ne Ram ka "
                       "rajyabhishek tab tay kiya jab Bharat mama ke ghar Kekay mein the (2.4.25), aur Kekay ke raja "
                       "ko bulaya tak nahi (2.1.46). Doosri taraf, Kaikeyi ne Ram ke liye 14 saal ka vanvaas bhi "
                       "maanga, Dashrath gham mein chal base, aur Bharat ne raj lene se mana kar diya.",
        hashtags=["#ramayan", "#kaikeyi", "#bharat", "#mythology", "#kahani"],
        pinned_comment="Galat kaun tha: Kaikeyi, ya Dashrath jinhone purana vaada bhula diya? 👇",
        sources=_SOURCES),
    "kn": dict(
        title="Kaikeyi nijavaaglu villain aa?",
        caption="Yochisi: saaviraaru varshagalinda Kaikeyiyanna khalanaayaki antivi... aadre Ayodhyeya raajya "
                "nijavaaglu avala maganige serabekittu 😳\n\n"
                "Valmiki Ramayana, Ayodhya Kanda: Ramane Bharatanige helida: Dasharatha Kaikeyiyanna maduve aadaaga "
                "avala tandege raajyada maatu kottidda. Pattabhisheka nirdhaara aadaaga Bharata Kekayadalli idda. "
                "Aadre Kaikeyi Ramanige 14 varsha vanavaasa kooda kelidlu.\n\n"
                "Tappu yaardu: Kaikeyida, Dasharathanda? Comment maadi 👇",
        yt_title="Kaikeyi Nijavaaglu Villain Aa? 😳 | Ramane Helida Satya | Ramayana",
        yt_description="Valmiki Ramayana (Ayodhya Kanda 2.107.3): Rama Bharatanige heltaane, appa ninna ammanannu "
                       "maduve aadaaga ninna ajjanige raajyada maatu kottidda. Bharata sodaramaavana mane Kekayadalli "
                       "iddaaga Ramana pattabhisheka nirdhaara aaytu (2.4.25), Kekaya rajanannu karelilla (2.1.46). "
                       "Innondu kade, Kaikeyi Ramanige 14 varsha vanavaasa kelidlu, Dasharatha dukhadalli praana "
                       "bitta, Bharata raajya beda anda.",
        hashtags=["#kannada", "#ramayana", "#kaikeyi", "#kannadastory", "#mythology"],
        pinned_comment="Tappu yaardu: Kaikeyida, illa hale maatu marata Dasharathanda? 👇",
        sources=_SOURCES),
}

USED_ASSETS, CREDITS_FILES = [], []      # everything in this video is drawn in code


def draw(cr, t, tl):
    from scenes_kaikeyi import draw as _draw
    _draw(cr, t, tl)


def sfx(tl):
    from scenes_kaikeyi import sfx as _sfx
    return _sfx(tl)
