"""Mythology video 16, remade (Hindi only): Ashtavakra, rebuilt on the lessons from the owner's reference reel
(owner, 12 Nov 2026: our video 16 "was unclear and hook was week and less engaging", then "Just make that one video
like the previous reference one let me see no other"). Lessons: myth_out/LESSONS_FROM_REFERENCE_ASHTAVAKRA.md.

What changed against videos/ashtavakra.py:
- Line 1 is the stake, not a curiosity: the boy's body bent in eight places, and his own father did it. Frame 1
  shows it happening (a flash-forward the story reaches again at the curse); no "सोचो" warm-up, no "true story" line.
- Every step says why: the baby heard the mantras every night (so he could hear the mistake), the father went to the
  king for money because the baby was due, the drowned came back because the pandit was the water god's son who sent
  them to his father's ritual.
- The true order of the Mahabharata: the father is defeated and drowned before the boy is born; for twelve years
  nobody tells him; then his mother does.
- Direct speech for the curse and the comeback; a mid-story question; the callback; a two-sided question.
- Short Hindi labels on screen instead of English headlines, a colour for each place, closer framing
  (scenes_ashtavakra2).

Facts (Mahabharata, Vana Parva 132-134, K. M. Ganguli translation): 132: the child in the
womb says the father's reading is not correct; cursed "crooked in eight parts of the body"; in the tenth month Sujata,
in want of wealth, sends Kahoda to king Janaka for wealth; defeated in controversy by Vandin and drowned; the news is
kept from Ashtavakra until his twelfth year, when he learns it and asks his mother. 133: stopped at the gate, he argues
that learning, not years, makes one great. 134: Vandin loses, says he is King Varuna's son and sent the Brahmanas to
Varuna's sacrifice; they come back; Kahoda has his son enter the river Samanga and his limbs become straight.
"""
from channel import ASSETS_ROOT, MUSIC, NARRATORS, NARRATOR_LABEL, REVEAL_GAP, TAIL  # noqa: F401

G = REVEAL_GAP
SCRIPTS = {
    "hi": [
        dict(id="a1", text="इस बच्चे का शरीर, आठ जगह से टेढ़ा है... और ये श्राप, उसके अपने पिता ने दिया था।", gap=G),
        dict(id="a3", text="पिता कहोड़, हर रात बच्चों को मंत्र पढ़ाते थे... और माँ के पेट में, बच्चा भी सुनता था।"),
        dict(id="a4", text="एक रात, पेट से आवाज़ आई: पिताजी, आप ये मंत्र गलत पढ़ रहे हो!", gap=G),
        dict(id="a6", text="सबके सामने अपमान! ग़ुस्से में पिता बोले: जा, तेरा शरीर आठ जगह से टेढ़ा होगा!", gap=G),
        dict(id="a8", text="घर में पैसे नहीं थे, तो पिता धन माँगने राजा के महल गए।"),
        dict(id="a9", text="वहाँ एक घमंडी पंडित का नियम था: बहस में हारे, तो पानी में डुबो दो।", gap=G),
        dict(id="a10", text="पिता हार गए... और उन्हें पानी में डुबो दिया गया।", gap=G),
        dict(id="a7", text="फिर बच्चा पैदा हुआ, सच में टेढ़ा। नाम पड़ा, अष्टावक्र।"),
        dict(id="a11", text="बारह साल बाद, माँ ने उसे सच बता दिया।"),
        dict(id="a12", text="महल के दरवाज़े पर उसे रोका गया: बच्चे अंदर नहीं आ सकते! वो बोला: बड़ा, उम्र से नहीं... "
                            "अक्ल से होता है।", gap=G),
        dict(id="a10q", text="सामने वही पंडित था, जिसने पिता को डुबोया था। क्या ये बच्चा उसे हरा पाएगा?", gap=G),
        dict(id="a13", text="बहस हुई... और उस छोटे से बच्चे ने, घमंडी पंडित को हरा दिया!", gap=G),
        dict(id="a14", text="तब पंडित ने राज़ खोला: मैं पानी के देवता का बेटा हूँ। हारने वाले मरे नहीं... मेरे पिता की "
                            "पूजा में गए हैं।"),
        dict(id="a15", text="पूजा पूरी हुई, और पिता ज़िंदा लौट आए! उन्होंने बेटे को नदी में उतारा... और उसका शरीर "
                            "बिल्कुल सीधा हो गया!", gap=G),
        dict(id="a15c", text="जिस बच्चे को पेट में बोलने की सज़ा मिली थी... उसी के बोलने ने, पिता को वापस ला दिया।",
             gap=G),
        dict(id="a16", text="तो गलत कौन था: सच बोलने वाला बेटा, या ग़ुस्से वाला पिता?"),
    ],
}

_SOURCES = ["Mahabharata, Vana Parva, sections 132-134 (K. M. Ganguli translation)"]
METADATA = {
    "hi": dict(
        title="Apne hi pita ke shraap se tedha paida hua",
        caption="Is bachche ka shareer aath jagah se tedha hai... aur ye shraap uske apne pita ne diya tha 😳\n\n"
                "Mahabharat, Van Parva: pet ke andar se pita ki galti pakadne wala Ashtavakra, 12 saal ki umar mein "
                "usi pandit ko hara aaya jisne uske pita ko paani mein dubo diya tha.\n\n"
                "Galat kaun tha: sach bolne wala beta, ya gusse wala pita? Comment mein batao 👇",
        yt_title="Apne Hi Pita Ke Shraap Se Tedha Paida Hua 😳 | Ashtavakra | Mahabharat",
        yt_description="Kahod har raat mantra padhate the aur pet mein bachcha sab sunta tha. Ek raat pet se awaaz "
                       "aayi ki mantra galat padh rahe ho. Gusse mein pita ne shraap diya: tera shareer aath jagah se "
                       "tedha hoga. Paise ke liye Kahod Raja Janak ke mahal gaye, Bandi se bahas haare aur paani mein "
                       "dubo diye gaye. 12 saal baad Ashtavakra ne Bandi ko hara diya; Bandi Varun ka beta nikla, saare "
                       "brahman paani se laut aaye, aur Samanga nadi mein Ashtavakra ka shareer seedha ho gaya.",
        hashtags=["#mahabharat", "#ashtavakra", "#mythology", "#kahani", "#hindu"],
        pinned_comment="Galat kaun tha: sach bolne wala beta, ya gusse wala pita? 👇",
        sources=_SOURCES),
}

USED_ASSETS, CREDITS_FILES = [], []      # everything in this video is drawn in code


def draw(cr, t, tl):
    import scenes_ashtavakra2 as S
    S.draw(cr, t, tl)


def sfx(tl):
    import scenes_ashtavakra2 as S
    return S.sfx(tl)
