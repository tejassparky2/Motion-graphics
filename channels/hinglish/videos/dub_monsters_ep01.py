"""Voice only, no video: the Hinglish dub of the owner's anime Short "Cute Things Kill Here" Ep 1, asked for by the
anime chat on the owner's request (1 Nov 2026: "make the same in hindi now just change voice to hindi hinglish the
voice is already created in shorts chat take from it"; captions stay English). Voiced with this channel's narrator
(Aman ref, IndicF5, tempo x1.15, studio v3, Whisper and liveliness retakes); export_dub.py writes one 48 kHz WAV per
line to out/monsters_hi/ep01_takes/. TARGET is each line's slot in seconds in the English cut (there is no l18)."""
# the narrator settings are channel-wide
from channel import NARRATOR, VOICE_REF  # noqa: F401

SCRIPT = [dict(id=i, text=s) for i, s in (
    ("l01", "हिलना मत। इसका पंजा पानी उबाल देता है।"),
    ("l02", "दस मिनट पहले, मैं ज़िंदा था।"),
    ("l03", "मरीन लैब में नाइट शिफ्ट। बस मैं, और पिस्टल श्रिम्प।"),
    ("l04", "पंजा इतना तेज़, कि पानी उबल जाए।"),
    ("l05", "क़रीब सूरज की सतह जितना गरम। पर सिर्फ पानी में।"),   # "लगभग" came out "lagbhabh" in 7 takes
    ("l06", "फिर तूफ़ान आया।"),
    ("l07", "श्रिम्प घबरा गया। उसके स्नैप से टैंक टूट गया।"),
    ("l08", "पानी डेस्क से गिरा, सीधा पावर केबल्स में।"),
    ("l09", "और मैं उसी में खड़ा था।"),
    ("l10", "ऐसे मैं मरा।"),
    ("l11", "फिर मैं जागा। एक दूसरी दुनिया में।"),
    ("l12", "यहाँ सब कुछ छोटा था। और क्यूट।"),
    ("l13", "और हर एक में कुछ गड़बड़ थी।"),
    ("l14", "मुझे बहुत प्यास लगी थी।"),
    ("l15", "कोई और पहले से पी रहा था।"),
    ("l16", "एक श्रिम्प। ज़मीन पर। नामुमकिन।"),
    ("l17", "फिर उसने सीधा मुझे देखा।"),
    ("l19", "बस एक इंच से बचा।"),
    ("l20", "आँख खुली, तो वो मेरी छाती पर बैठा था।"),
    ("l21", "फिर मैंने बूँदें देखीं।"),
    ("l22", "पंजा सिर्फ गीले में चलता है।"),
    ("l23", "तो मैं हिला नहीं। धूप ने उसे सुखा दिया।"),
    ("l24", "फिर भी, उसने वार किया।"),
    ("l25", "फिर गुस्से में, वापस पानी की तरफ़।"),
    ("l26", "तभी मैंने काँटों वाला पेड़ देखा।"),
    ("l27", "बुचर बर्ड अपना खाना काँटों पर टाँग देती है।"),
    ("l28", "और वो श्रिम्प को देख रही थी।"),
    ("l29", "श्रिम्प को कुछ पता नहीं था।"),
    ("l30", "ऑप्शन ए: उस श्रिम्प को बचाऊँ, जिसने मुझे मारना चाहा। ऑप्शन बी: भाग जाऊँ, जब तक मौका है। "
            "कमेंट करो, ए या बी।"),
)]
NOTES = dict(
    l05="respelled: 'लगभग' -> 'क़रीब' (same meaning); 'लगभग' came out 'lagbhabh' in 7 of 7 takes",
    l10="the flattest of the takes heard as 'ऐसे मैं मरा' (a quiet beat, as asked)",
    l20="Whisper writes 'आख' (no nasal mark); the earlier take was heard as 'आग', this one is not",
    l30="Whisper hears 'ऑप्शन बी' as 'option भी' in every take (it guesses the common word); this take is the one "
        "where it heard 'A या B' at the end. The English captions show A / B.",
)
TARGET = dict(l01=2.2, l02=1.5, l03=2.9, l04=2.1, l05=3.6, l06=1.0, l07=2.7, l08=3.1, l09=1.5, l10=1.0, l11=2.1,
              l12=2.4, l13=1.7, l14=1.2, l15=1.7, l16=2.5, l17=1.4, l19=1.4, l20=2.3, l21=1.2, l22=1.7, l23=2.4,
              l24=1.5, l25=1.8, l26=1.7, l27=2.5, l28=1.6, l29=1.6, l30=6.3)
