"""Mythology video 7: Lakshman Rekha is not in the Valmiki Ramayana (owner, 8 Nov 2026, after two rejected scripts:
"Not good and hindi explanation not clear change story"; this script approved: "Ok"). ONE simple idea, one step per
sentence, everyday words; verse numbers only as small tags on screen. Look: the Togalu Gombeyaata shadow puppets
(owner: "The jarasanda video animation did good").

Facts:
- Valmiki Ramayana, Aranya Kanda 3.45 (valmikiramayan.net): after the cry in Rama's voice, Sita sends Lakshmana;
  Lakshmana: no one can defeat Rama, "it is not the voice of Rama ... someone mimicked that voice for chicanery"
  (3.45.16); Sita answers with harsh accusations (3.45.5-30; only called "harsh" in the reel, never repeated);
  leaving, he says "rakShantu tvAm vishAlAkShi samagrA vanadevatAH": may all the forest gods protect you
  (3.45.33-34). No line or boundary is drawn.
- Tulsidas, Ramcharitmanas (16th century): no line in the Aranya Kand abduction; Lanka Kand, under doha 35,
  Mandodari to Ravana: "रामानुज लघु रेख खचाई। सोउ नहिं नाघेहु असि मनुसाई॥" (you could not even cross the small
  line Lakshmana drew). The reel says only what these two texts say; it does not claim where later tellings or TV
  versions took the line from.
"""
from channel import ASSETS_ROOT, MUSIC, NARRATORS, NARRATOR_LABEL, REVEAL_GAP, TAIL  # noqa: F401

SCRIPTS = {
    "hi": [
        dict(id="l1", text="सोचो, जिस लक्ष्मण रेखा की मिसाल हम रोज़ देते हैं... वो वाल्मीकि रामायण में है ही नहीं।",
             gap=REVEAL_GAP),
        dict(id="l2", text="ये कोई अफ़वाह नहीं है। वाल्मीकि रामायण का अरण्य कांड, ख़ुद पढ़कर देखो।"),
        dict(id="l3", text="सीता ने एक सोने का हिरण देखा। राम उसे पकड़ने गए।"),
        dict(id="l4", text="थोड़ी देर बाद, जंगल से राम की आवाज़ में एक चीख़ आई।"),
        dict(id="l5", text="सीता डर गईं। उन्होंने लक्ष्मण से कहा: जाओ, अपने भाई को बचाओ।"),
        dict(id="l6", text="लक्ष्मण ने कहा: ये राम की आवाज़ नहीं है। ये किसी राक्षस की चाल है।"),
        dict(id="l7", text="सीता नहीं मानीं। ग़ुस्से में उन्होंने लक्ष्मण को बहुत कड़वी बातें कहीं।"),
        dict(id="l8", text="दुखी होकर लक्ष्मण चले गए। पर उन्होंने ज़मीन पर कोई रेखा नहीं खींची।", gap=REVEAL_GAP),
        dict(id="l9", text="जाते-जाते बस इतना कहा: वन के सारे देवता आपकी रक्षा करें।"),
        dict(id="l10", text="तो फिर ये लक्ष्मण रेखा आई कहाँ से?", gap=REVEAL_GAP),
        dict(id="l11", text="बहुत बाद में, सोलहवीं सदी में, तुलसीदास ने रामचरितमानस लिखी।"),
        dict(id="l12", text="उसमें भी, सीता हरण के वक़्त कोई रेखा नहीं है।"),
        dict(id="l13", text="रेखा की बात आती है बाद में, लंका कांड में। मंदोदरी रावण को ताना मारती है: तुम तो लक्ष्मण की "
                            "खींची छोटी सी रेखा भी पार नहीं कर पाए।"),
        dict(id="l14", text="और वो भी, बस एक लाइन में।", gap=REVEAL_GAP),
        dict(id="l15", text="तो तुम कौन सी कहानी मानते हो? वाल्मीकि वाली, या रेखा वाली? कमेंट में बताओ।"),
    ],
    "kn": [
        dict(id="l1", text="ಯೋಚಿಸಿ... ನಾವು ದಿನಾ ಹೇಳೋ ಲಕ್ಷ್ಮಣ ರೇಖೆ... ವಾಲ್ಮೀಕಿ ರಾಮಾಯಣದಲ್ಲಿ ಇಲ್ವೇ ಇಲ್ಲ.", gap=REVEAL_GAP),
        dict(id="l2", text="ಇದು ಯಾವ್ದೋ ಗಾಳಿಸುದ್ದಿ ಅಲ್ಲ. ವಾಲ್ಮೀಕಿ ರಾಮಾಯಣದ ಅರಣ್ಯ ಕಾಂಡ ನೀವೇ ಓದಿ ನೋಡಿ."),
        dict(id="l3", text="ಸೀತೆ ಒಂದು ಬಂಗಾರದ ಜಿಂಕೆ ನೋಡಿದ್ಲು. ರಾಮ ಅದನ್ನ ಹಿಡಿಯೋಕೆ ಹೋದ."),
        dict(id="l4", text="ಸ್ವಲ್ಪ ಹೊತ್ತಾದ ಮೇಲೆ, ಕಾಡಿಂದ ರಾಮನ ಧ್ವನಿಯಲ್ಲಿ ಒಂದು ಕೂಗು ಕೇಳಿಸ್ತು."),
        dict(id="l5", text="ಸೀತೆ ಹೆದರಿದ್ಲು. ಲಕ್ಷ್ಮಣನಿಗೆ ಹೇಳಿದ್ಲು: ಹೋಗು, ನಿನ್ನ ಅಣ್ಣನ್ನ ಕಾಪಾಡು."),
        dict(id="l6", text="ಲಕ್ಷ್ಮಣ ಹೇಳಿದ: ಇದು ರಾಮನ ಧ್ವನಿ ಅಲ್ಲ. ಇದು ಯಾವ್ದೋ ರಾಕ್ಷಸನ ಮೋಸ."),
        dict(id="l7", text="ಸೀತೆ ಒಪ್ಪಲಿಲ್ಲ. ಕೋಪದಲ್ಲಿ ಲಕ್ಷ್ಮಣನಿಗೆ ತುಂಬಾ ಕಟುವಾದ ಮಾತುಗಳನ್ನ ಆಡಿದ್ಲು."),
        dict(id="l8", text="ನೋವಿನಿಂದ ಲಕ್ಷ್ಮಣ ಹೊರಟ. ಆದ್ರೆ ನೆಲದ ಮೇಲೆ ಯಾವ ಗೆರೆಯನ್ನೂ ಎಳೀಲಿಲ್ಲ.", gap=REVEAL_GAP),
        dict(id="l9", text="ಹೋಗ್ತಾ ಬರೀ ಇಷ್ಟು ಹೇಳಿದ: ಕಾಡಿನ ಎಲ್ಲಾ ದೇವತೆಗಳು ನಿಮ್ಮನ್ನ ಕಾಪಾಡಲಿ."),
        dict(id="l10", text="ಹಾಗಾದ್ರೆ ಈ ಲಕ್ಷ್ಮಣ ರೇಖೆ ಬಂದಿದ್ದು ಎಲ್ಲಿಂದ?", gap=REVEAL_GAP),
        dict(id="l11", text="ತುಂಬಾ ವರ್ಷಗಳ ನಂತರ, ಹದಿನಾರನೇ ಶತಮಾನದಲ್ಲಿ, ತುಳಸೀದಾಸರು ರಾಮಚರಿತಮಾನಸ ಬರೆದ್ರು."),
        dict(id="l12", text="ಅದರಲ್ಲೂ, ಸೀತಾಪಹರಣದ ಸಮಯದಲ್ಲಿ ಯಾವ ರೇಖೆಯೂ ಇಲ್ಲ."),
        dict(id="l13", text="ರೇಖೆಯ ಮಾತು ಬರೋದು ಆಮೇಲೆ, ಲಂಕಾ ಕಾಂಡದಲ್ಲಿ. ಮಂಡೋದರಿ ರಾವಣನಿಗೆ ಚುಚ್ಚಿ ಹೇಳ್ತಾಳೆ: ಲಕ್ಷ್ಮಣ ಎಳೆದ "
                            "ಚಿಕ್ಕ ಗೆರೆಯನ್ನೂ ನೀನು ದಾಟಲಿಲ್ಲ."),
        dict(id="l14", text="ಅದೂ, ಬರೀ ಒಂದೇ ಸಾಲಿನಲ್ಲಿ.", gap=REVEAL_GAP),
        dict(id="l15", text="ನೀವು ಯಾವ ಕಥೆ ನಂಬ್ತೀರಾ? ವಾಲ್ಮೀಕಿಯದ್ದಾ, ಅಥವಾ ರೇಖೆ ಇರೋದಾ? ಕಾಮೆಂಟ್ ಮಾಡಿ ಹೇಳಿ."),
    ],
}

_SOURCES = ["Valmiki Ramayana, Aranya Kanda 3.45", "Tulsidas, Ramcharitmanas, Lanka Kand (doha 35)"]
METADATA = {
    "hi": dict(
        title="Lakshman Rekha Valmiki Ramayan mein hai hi nahi",
        caption="Socho, jis Lakshman Rekha ki misaal hum roz dete hain... wo Valmiki Ramayan mein hai hi nahi 😳\n\n"
                "Valmiki Ramayan, Aranya Kand: Lakshman ne koi rekha nahi kheenchi, bas kaha: van ke saare devta aapki "
                "raksha karein. Rekha ki baat aati hai Tulsidas ki Ramcharitmanas mein, Lanka Kand ki ek line mein, "
                "jab Mandodari Ravan ko taana maarti hai.\n\n"
                "Tum kaunsi kahani maante ho: Valmiki wali ya rekha wali? Comment mein batao 👇",
        yt_title="Lakshman Rekha Valmiki Ramayan Mein Hai Hi Nahi 😳 | Ramayan",
        yt_description="Valmiki Ramayan ke Aranya Kand (3.45) mein Lakshman Sita ko chhod kar jaate hain, par koi rekha "
                       "nahi kheenchte; jaate hue kehte hain: van ke saare devta aapki raksha karein. Tulsidas ki "
                       "Ramcharitmanas mein bhi Sita haran ke waqt rekha nahi hai. Rekha ka zikr Lanka Kand (doha 35) "
                       "mein aata hai, jab Mandodari Ravan se kehti hai ki tum Lakshman ki kheenchi chhoti si rekha bhi "
                       "paar nahi kar paaye.",
        hashtags=["#ramayan", "#lakshmanrekha", "#ramcharitmanas", "#mythology", "#kahani"],
        pinned_comment="Tum kaunsi kahani maante ho: Valmiki wali, ya rekha wali? 👇",
        sources=_SOURCES),
    "kn": dict(
        title="Lakshmana rekhe Valmiki Ramayanadalli ille illa",
        caption="Yochisi: naavu dina helo Lakshmana rekhe... Valmiki Ramayanadalli ille illa 😳\n\n"
                "Valmiki Ramayana, Aranya Kanda: Lakshmana yaava gereyannu elelilla, bari helida: kaadina ella "
                "devategalu nimmannu kaapadali. Rekheya maatu baroda Tulsidasara Ramacharitamanasadalli, Lanka "
                "Kandada ondu saalinalli, Mandodari Ravananige chuchchi heluvaaga.\n\n"
                "Neevu yaava kathe nambteera: Valmikiyadda, rekhe iroda? Comment maadi 👇",
        yt_title="Lakshmana Rekhe Valmiki Ramayanadalli Ille Illa 😳 | Ramayana",
        yt_description="Valmiki Ramayanada Aranya Kandadalli (3.45) Lakshmana Seetheyannu bittu hogtaane, aadre yaava "
                       "gereyannu eleyalla; hogtaa heltaane: kaadina ella devategalu nimmannu kaapadali. Tulsidasara "
                       "Ramacharitamanasadalli kooda Seethaapaharanada samayadalli rekhe illa. Rekheya maatu Lanka "
                       "Kandadalli (doha 35) baratte, Mandodari Ravananige heluvaaga.",
        hashtags=["#kannada", "#ramayana", "#lakshmanarekha", "#kannadastory", "#mythology"],
        pinned_comment="Neevu yaava kathe nambteera: Valmikiyadda, illa rekhe iroda? 👇",
        sources=_SOURCES),
}

USED_ASSETS, CREDITS_FILES = [], []      # everything in this video is drawn in code


def draw(cr, t, tl):
    from scenes_lakshman_rekha import draw as _draw
    _draw(cr, t, tl)


def sfx(tl):
    from scenes_lakshman_rekha import sfx as _sfx
    return _sfx(tl)
