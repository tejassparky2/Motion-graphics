"""Mythology video 23: a sage kicked Vishnu in the chest, and Vishnu pressed the sage's feet (the owner's "Continue"
after videos 15-19, 12 Nov 2026). Sages versus gods: the test of the three gods, two failed tempers, one shocking kick
and a calm answer; debate: was the sage's test right or wrong? (not "which god is greatest", to stay respectful).
Look: Hindi = Togalu Gombeyaata shadow puppets, Kannada = Yakshagana stage. The kick is a silhouette with a soft flash,
never slapstick; the trident is only raised. Calm sound.

Facts (Bhagavata Purana 10.89.1-19, vedabase):
- 1-2: sages at a sacrifice on the Sarasvati argue which of the three chief gods is greatest; they send Bhrigu, son of
  Brahma, to find out.
- 3-4: at his father Brahma's court Bhrigu neither bows nor offers praise; Brahma flares up but controls his anger
  (his own son).
- 5-7: at Kailasa, Shiva rises gladly to embrace his brother; Bhrigu refuses, calling him a deviant; Shiva raises his
  trident to kill him; the Goddess falls at Shiva's feet and calms him.
- 8-11: in Vaikuntha, Vishnu lies with his head in Lakshmi's lap; Bhrigu kicks him on the chest; Vishnu rises with
  Lakshmi, bows his head to the ground, welcomes him, asks forgiveness for not noticing his arrival, says the sage's
  feet are very tender, presses them with his own hands, and asks to be purified by the water that washed them.
- 12-14: Bhrigu, overwhelmed, falls silent with tears in his eyes; he reports to the sages, who conclude Vishnu is
  the greatest.
"""
from channel import ASSETS_ROOT, MUSIC, NARRATORS, NARRATOR_LABEL, REVEAL_GAP, TAIL  # noqa: F401

G = REVEAL_GAP
SCRIPTS = {
    "hi": [
        dict(id="bg1", text="सोचो, एक ऋषि ने, भगवान विष्णु की छाती पर लात मार दी... और भगवान ने उल्टा, उनके पैर दबाए!", gap=G),
        dict(id="bg2", text="ये भागवत पुराण की सच्ची कहानी है।"),
        dict(id="bg3", text="एक बार, ऋषियों में बहस हो गई: ब्रह्मा, विष्णु और शिव में, सबसे बड़ा कौन है?"),
        dict(id="bg4", text="परखने का काम मिला, भृगु ऋषि को। उन्होंने सोचा: जो ग़ुस्सा न करे, वही सबसे बड़ा।", gap=G),
        dict(id="bg5", text="पहले वो गए ब्रह्मा जी के पास, जो उनके अपने पिता थे। ना प्रणाम किया, ना कुछ बोले।"),
        dict(id="bg6", text="ब्रह्मा जी को ग़ुस्सा आया... पर बेटा समझकर, उन्होंने ग़ुस्सा पी लिया।", gap=G),
        dict(id="bg7", text="फिर वो गए शिव जी के पास। शिव जी ख़ुश होकर, उन्हें गले लगाने आगे आए।"),
        dict(id="bg8", text="पर ऋषि पीछे हट गए, और उन्हें बुरा भला कहने लगे।"),
        dict(id="bg9", text="शिव जी ने ग़ुस्से में, त्रिशूल उठा लिया! तब पार्वती माँ ने, उनके पैर पकड़कर, उन्हें शांत किया।", gap=G),
        dict(id="bg9q", text="अब बचे थे, भगवान विष्णु। वहाँ क्या होगा?"),
        dict(id="bg10", text="विष्णु जी, लक्ष्मी माँ की गोद में सिर रखकर, आराम से लेटे थे।"),
        dict(id="bg11", text="ऋषि गए, और सीधे उनकी छाती पर, ज़ोर से लात मार दी!", gap=G),
        dict(id="bg12", text="विष्णु जी उठे... पर ग़ुस्सा नहीं हुए। उन्होंने झुककर, ऋषि को प्रणाम किया।"),
        dict(id="bg13", text="और बोले: माफ़ कीजिए, मैंने आपको आते नहीं देखा। आपके पैर तो बहुत नाज़ुक हैं, चोट तो नहीं लगी?"),
        dict(id="bg14", text="और प्यार से, ऋषि के पैर दबाने लगे।", gap=G),
        dict(id="bg15", text="ऋषि की आँखों में आँसू आ गए। लौटकर उन्होंने सबसे कहा: सबसे बड़े, विष्णु हैं।"),
        dict(id="bg15c", text="जिनकी छाती पर लात पड़ी... उन्होंने बदले में, पैर दबाए।", gap=G),
        dict(id="bg16", text="तो क्या ऋषि का ये इम्तिहान सही था? या ग़लत? कमेंट में बताओ।"),
    ],
}
KN = {
    "bg1": "ಯೋಚಿಸಿ... ಒಬ್ಬ ಋಷಿ, ವಿಷ್ಣುವಿನ ಎದೆಗೆ ಒದ್ದ... ಆದ್ರೆ ವಿಷ್ಣು, ಬದಲಿಗೆ ಅವನ ಕಾಲು ಒತ್ತಿದ!",
    "bg2": "ಇದು ಭಾಗವತದ ನಿಜವಾದ ಕಥೆ.",
    "bg3": "ಒಂದು ಸಲ, ಋಷಿಗಳ ಮಧ್ಯೆ ವಾದ ಶುರುವಾಯ್ತು: ಬ್ರಹ್ಮ, ವಿಷ್ಣು, ಶಿವ, ಇವರಲ್ಲಿ ಯಾರು ದೊಡ್ಡವರು?",
    "bg4": "ಪರೀಕ್ಷೆ ಮಾಡೋ ಕೆಲಸ, ಭೃಗು ಋಷಿಗೆ ಸಿಕ್ತು. ಅವನು ಅಂದ್ಕೊಂಡ: ಯಾರು ಕೋಪ ಮಾಡ್ಕೊಳ್ಳಲ್ವೋ, ಅವರೇ ದೊಡ್ಡವರು.",
    "bg5": "ಮೊದಲು ಅವನು ಬ್ರಹ್ಮನ ಹತ್ರ ಹೋದ, ಬ್ರಹ್ಮ ಅವನ ಸ್ವಂತ ಅಪ್ಪ. ನಮಸ್ಕಾರನೂ ಮಾಡಲಿಲ್ಲ, ಏನೂ ಮಾತಾಡಲಿಲ್ಲ.",
    "bg6": "ಬ್ರಹ್ಮನಿಗೆ ಕೋಪ ಬಂತು... ಆದ್ರೆ ಮಗ ಅಂತ, ಕೋಪ ನುಂಗಿಕೊಂಡ.",
    "bg7": "ಆಮೇಲೆ ಅವನು ಶಿವನ ಹತ್ರ ಹೋದ. ಶಿವ ಖುಷಿಯಿಂದ, ಅವನನ್ನ ತಬ್ಬಿಕೊಳ್ಳೋಕೆ ಮುಂದೆ ಬಂದ.",
    "bg8": "ಆದ್ರೆ ಋಷಿ ಹಿಂದೆ ಸರಿದು, ಶಿವನಿಗೆ ಬಾಯಿಗೆ ಬಂದ ಹಾಗೆ ಬೈಯೋಕೆ ಶುರು ಮಾಡಿದ.",
    "bg9": "ಶಿವ ಕೋಪದಲ್ಲಿ, ತ್ರಿಶೂಲ ಎತ್ತಿದ! ಆಗ ಪಾರ್ವತಿ, ಅವನ ಕಾಲು ಹಿಡಿದು, ಸಮಾಧಾನ ಮಾಡಿದ್ಲು.",
    "bg9q": "ಈಗ ಉಳಿದಿದ್ದು, ವಿಷ್ಣು ಒಬ್ಬನೇ. ಅಲ್ಲಿ ಏನಾಗುತ್ತೆ?",
    "bg10": "ವಿಷ್ಣು, ಲಕ್ಷ್ಮಿಯ ತೊಡೆ ಮೇಲೆ ತಲೆ ಇಟ್ಟು, ಆರಾಮಾಗಿ ಮಲಗಿದ್ದ.",
    "bg11": "ಋಷಿ ಹೋಗಿ, ನೇರವಾಗಿ ಅವನ ಎದೆಗೆ, ಜೋರಾಗಿ ಒದ್ದ!",
    "bg12": "ವಿಷ್ಣು ಎದ್ದ... ಆದ್ರೆ ಕೋಪ ಮಾಡ್ಕೊಳ್ಳಲಿಲ್ಲ. ತಲೆ ಬಾಗಿಸಿ, ಋಷಿಗೆ ನಮಸ್ಕಾರ ಮಾಡಿದ.",
    "bg13": "ಹೇಳಿದ: ಕ್ಷಮಿಸಿ, ನೀವು ಬಂದಿದ್ದು ನಾನು ನೋಡಲಿಲ್ಲ. ನಿಮ್ಮ ಕಾಲು ತುಂಬಾ ಮೃದು, ನೋವಾಯ್ತಾ?",
    "bg14": "ಆಮೇಲೆ ಪ್ರೀತಿಯಿಂದ, ಋಷಿಯ ಕಾಲು ಒತ್ತೋಕೆ ಶುರು ಮಾಡಿದ.",
    "bg15": "ಋಷಿಯ ಕಣ್ಣಲ್ಲಿ ನೀರು ಬಂತು. ವಾಪಸ್ ಬಂದು ಎಲ್ಲರಿಗೂ ಹೇಳಿದ: ಎಲ್ಲರಿಗಿಂತ ದೊಡ್ಡವರು, ವಿಷ್ಣು.",
    "bg15c": "ಯಾರ ಎದೆಗೆ ಒದೆ ಬಿತ್ತೋ... ಅವರೇ ಬದಲಿಗೆ, ಕಾಲು ಒತ್ತಿದ್ರು.",
    "bg16": "ಹಾಗಾದ್ರೆ ಋಷಿಯ ಈ ಪರೀಕ್ಷೆ, ಸರಿನಾ, ತಪ್ಪಾ? ಕಾಮೆಂಟ್ ಮಾಡಿ ಹೇಳಿ.",
}
SCRIPTS["kn"] = [dict(line, text=KN[line["id"]]) for line in SCRIPTS["hi"]]   # same ids and pauses as Hindi

_SOURCES = ["Bhagavata Purana 10.89.1-19"]
METADATA = {
    "hi": dict(
        title="Rishi ne Vishnu ji ki chhaati par laat maari",
        caption="Socho, ek rishi ne Bhagwan Vishnu ki chhaati par laat maar di... aur Bhagwan ne ulta unke pair "
                "dabaaye 😳\n\nBhagavat Puran: rishiyon mein bahas thi, Brahma, Vishnu aur Shiv mein sabse bada "
                "kaun? Bhrigu rishi ne teenon ki pariksha li. Brahma ji ne gussa pee liya, Shiv ji ne trishool utha "
                "liya... aur Vishnu ji ne?\n\nRishi ka yeh imtihaan sahi tha ya galat? Comment mein batao 👇",
        yt_title="Rishi Ne Bhagwan Vishnu Ki Chhaati Par Laat Maari 😳 | Bhrigu Ki Pariksha | Bhagavat Puran",
        yt_description="Bhagavat Puran (10.89): Saraswati ke kinare rishiyon mein bahas hui ki Brahma, Vishnu aur "
                       "Shiv mein sabse bada kaun hai. Bhrigu rishi pariksha lene gaye. Apne pita Brahma ji ko pranaam "
                       "nahi kiya, Shiv ji ko bura bhala kaha, aur Vishnu ji ki chhaati par laat maari. Vishnu ji ne "
                       "gussa nahi kiya: jhukkar pranaam kiya, maafi maangi aur rishi ke pair dabaaye.",
        hashtags=["#vishnu", "#bhagavatpuran", "#mythology", "#kahani", "#hindu"],
        pinned_comment="Rishi ka yeh imtihaan sahi tha, ya galat? 👇",
        sources=_SOURCES),
    "kn": dict(
        title="Rishi Vishnuvina edege odda",
        caption="Yochisi: obba rishi Vishnuvina edege odda... aadre Vishnu badalige avana kaalu ottida 😳\n\n"
                "Bhagavata: rishigala madhye vaada, Brahma, Vishnu, Shiva, yaaru doddavaru? Bhrigu rishi mooru "
                "jananna pareekshe maadida. Brahma kopa nungikonda, Shiva trishoola ettida... Vishnu?\n\n"
                "Rishiya ee pareekshe sari na, tappa? Comment maadi 👇",
        yt_title="Rishi Vishnuvina Edege Odda 😳 | Bhriguvina Pareekshe | Bhagavata",
        yt_description="Bhagavata (10.89): Saraswati dadadalli rishigala madhye vaada aaytu, Brahma, Vishnu, Shiva "
                       "ivaralli yaaru doddavaru anta. Bhrigu rishi pareekshe maadoke hoda. Tanna appa Brahmanige "
                       "namaskaara maadalilla, Shivanige baida, Vishnuvina edege odda. Vishnu kopa maadkollalilla: "
                       "tale baagisi namaskaara maadi, kshame kelida, rishiya kaalu ottida.",
        hashtags=["#kannada", "#vishnu", "#bhagavata", "#kannadastory", "#mythology"],
        pinned_comment="Rishiya ee pareekshe sari na, tappa? 👇",
        sources=_SOURCES),
}


USED_ASSETS, CREDITS_FILES = [], []      # everything in this video is drawn in code


def _scenes(tl):
    """Hindi: shadow puppets (scenes_bhrigu); Kannada: Yakshagana stage (scenes_bhrigu_yk), so the two channels never
    share pictures."""
    import importlib
    yk = getattr(tl, "lang", "hi") == "kn"
    return importlib.import_module("scenes_bhrigu_yk" if yk else "scenes_bhrigu")


def draw(cr, t, tl):
    _scenes(tl).draw(cr, t, tl)


def sfx(tl):
    return _scenes(tl).sfx(tl)
