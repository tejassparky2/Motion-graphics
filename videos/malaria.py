"""Explainer 3: "This Parasite Hides in Your Liver Before It Attacks" (explainer format, owner-approved script,
24 Oct 2026). Script, shot list and sources: research_notes/explainer_1-3.md.
"""
from motion import paper as P
from videos import malaria_shots as S

NARRATOR = dict(chatterbox=True, tempo_min=1.0, tempo_max=1.0)   # owner: "change to clear and best voice" (27 Oct)
STYLE = "clean"
MUSIC = "explainer"
TAIL = 1.2

SCRIPT = [
    dict(id="m1", scene="m1", text="One mosquito bite. And something moves into your liver."),
    dict(id="m2", scene="m2", text="For days, you feel completely fine."),
    dict(id="m3", scene="m3", text="Later, it breaks out into your blood, again and again."),
    dict(id="m4", scene="m4", text="It's malaria. In [twenty twenty-four,|2024,] it made about two hundred and eighty "
                                   "million people sick."),
    dict(id="m5", scene="m5", text="And it killed about six hundred thousand. Most of them young children in Africa."),
    dict(id="m6", scene="m6", text="And it isn't a virus or a bacterium. It's a parasite. So let's follow its "
                                   "journey."),
    dict(id="m7", scene="m7", text="Only female mosquitoes drink blood. They need that blood to make their eggs."),
    dict(id="m8", scene="m8", text="When an infected one bites, tiny parasites slip into your blood."),
    dict(id="m9", scene="m9", text="Within hours, they reach your liver, and hide inside liver cells."),
    dict(id="m10", scene="m10", text="There, quietly, each one multiplies into thousands."),
    dict(id="m11", scene="m11", text="Then the liver cells burst, and the parasites flood your blood."),
    dict(id="m12", scene="m12", text="Each one breaks into a red blood cell, multiplies again, and bursts it open."),
    dict(id="m13", scene="m13", text="That's when you get sick, usually ten to fifteen days after the bite. Fever, "
                                     "chills, headache."),
    dict(id="m14", scene="m14", text="And one type, called vivax, can leave sleeping parasites in the liver. They can "
                                     "wake up weeks or even years later."),
    dict(id="m15", scene="m15", text="We know mosquitoes spread it because of a discovery in India."),
    dict(id="m16", scene="m16", text="In [eighteen ninety-seven,|1897,] in Secunderabad, a doctor named Ronald Ross "
                                     "found the parasite inside a mosquito. It won him a Nobel Prize."),
    dict(id="m17", scene="m17", text="Malaria doesn't spread from person to person. It needs the mosquito."),
    dict(id="m18", scene="m18", text="And it can be treated. If you get a fever in a malaria area, see a doctor. A "
                                     "simple blood test can find it."),
    dict(id="m19", scene="m19", text="Bed nets and repellent stop the very first step."),
    dict(id="m20", scene="m20", text="Have you or someone you know had malaria? Tell me in the comments."),
]
for _b in SCRIPT[1:]:
    _b.setdefault("gap", 0.42)      # a calm breath between lines, like the reference explainers

METADATA = dict(
    title="This Parasite Hides in Your Liver Before It Attacks 🦟",
    alt_titles=["What a Mosquito Really Puts Inside You", "The Parasite That Sleeps in Your Liver",
                "How Malaria Actually Works"],
    description="""One mosquito bite, and a parasite moves into your liver. 🦟

📊 2024: about 282 million malaria cases and about 610,000 deaths, most of them young children in Africa (WHO).
🦟 Only female mosquitoes drink blood; they need it to make eggs.
🧬 The journey: parasites reach the liver and hide in its cells, multiply into thousands, burst out into the blood, then invade and burst red blood cells. That's when fever, chills and headache start, usually 10-15 days after the bite.
😴 P. vivax can leave sleeping parasites in the liver that wake up weeks or even years later.
🇮🇳 In 1897, in Secunderabad, Ronald Ross found the parasite inside a mosquito, and won the 1902 Nobel Prize.
✅ Malaria doesn't spread from person to person. If you get a fever in a malaria area, see a doctor: a simple blood test can find it, and it can be treated. Bed nets and repellent stop the first step.

This video is general information, not medical advice.

Sources:
- WHO, Malaria fact sheet (World Malaria Report 2025 figures for 2024)
- CDC DPDx, Malaria life cycle
- CDC, Anopheles mosquito life cycle
- Prudêncio, Rodriguez & Mota, "The silent path to thousands of merozoites", Nature Reviews Microbiology (2006)
- LSHTM / nobelprize.org: Ronald Ross, 1897 discovery and 1902 Nobel Prize
""",
    hashtags=["#malaria", "#mosquito", "#health", "#science", "#shorts"],
    tags=["malaria", "how malaria works", "malaria parasite", "plasmodium", "mosquito", "anopheles", "liver",
          "vivax", "ronald ross", "secunderabad", "malaria symptoms", "health facts", "medical facts",
          "science explained", "doc and the organs"],
    pinned_comment="Fun fact: the mosquito-malaria link was proven in Secunderabad, India, in 1897. 🇮🇳🦟 "
                   "Did you know that?",
)


def draw(cr, t, tl):
    P.frame(cr, t, tl, S.SHOTS)
