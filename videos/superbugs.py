"""Explainer 2: "Bacteria Are Learning to Beat Our Medicine" (explainer format, owner-approved script, 24 Oct 2026).
Script, shot list and sources: research_notes/explainer_1-3.md.
"""
from motion import paper as P
from videos import superbugs_shots as S

NARRATOR = dict(orpheus="leo", tempo_min=1.0, tempo_max=1.0)   # owner's pick "O" (25 Oct): Orpheus, natural pace
STYLE = "clean"
MUSIC = "explainer"
TAIL = 1.2

SCRIPT = [
    dict(id="b1", scene="b1", text="A tiny cut on your finger used to be able to kill you."),
    dict(id="b2", scene="b2", text="Then in [nineteen twenty-eight,|1928,] a mould was found that kills bacteria."),
    dict(id="b3", scene="b3", text="Now the bacteria are fighting back."),
    dict(id="b4", scene="b4", text="In [twenty twenty-one,|2021,] drug-resistant bacteria directly killed more than a "
                                   "million people."),
    dict(id="b5", scene="b5", text="And they played a part in nearly five million deaths."),
    dict(id="b6", scene="b6", text="These germs are called superbugs. So how does a germ beat a medicine?"),
    dict(id="b7", scene="b7", text="An infection can be billions of bacteria."),
    dict(id="b8", scene="b8", text="Their copies aren't perfect, so by chance, a few are slightly different."),
    dict(id="b9", scene="b9", text="Now the antibiotic hits."),
    dict(id="b10", scene="b10", text="It kills almost all of them. But not the different ones."),
    dict(id="b11", scene="b11", text="Those survivors multiply, and now the whole infection carries their shield."),
    dict(id="b12", scene="b12", text="Worse, bacteria can hand the shield to their neighbours, in tiny loops of DNA."),
    dict(id="b13", scene="b13", text="Even to completely different kinds of bacteria."),
    dict(id="b14", scene="b14", text="The man who found penicillin saw this coming."),
    dict(id="b15", scene="b15", text="In [nineteen forty-five,|1945,] he warned that taking too little would teach "
                                     "the microbes to resist."),
    dict(id="b16", scene="b16", text="Here's what most people get wrong. Your body doesn't become resistant. The "
                                     "bacteria do."),
    dict(id="b17", scene="b17", text="And antibiotics do nothing against a cold or the flu. Those are viruses."),
    dict(id="b18", scene="b18", text="Every dose you didn't need is free training for the bacteria."),
    dict(id="b19", scene="b19", text="So take antibiotics only when a doctor prescribes them, exactly as prescribed."),
    dict(id="b20", scene="b20", text="Never share them, and never use leftovers."),
    dict(id="b21", scene="b21", text="Experts estimate superbugs could directly kill thirty-nine million people "
                                     "between now and [twenty fifty.|2050.]"),
    dict(id="b22", scene="b22", text="Have you ever taken antibiotics for a cold? Be honest in the comments."),
]
for _b in SCRIPT[1:]:
    _b.setdefault("gap", 0.42)      # a calm breath between lines, like the reference explainers

METADATA = dict(
    title="Bacteria Are Learning to Beat Our Medicine 🦠💊",
    alt_titles=["Why Antibiotics Are Stopping Working", "Your Body Isn't Resistant. The Bacteria Are.",
                "The Superbug Problem, Explained"],
    description="""Antibiotics are losing the war, and here's how bacteria do it. 🦠

💊 1928: penicillin, a mould that kills bacteria.
☠️ 2021: drug-resistant bacteria directly killed about 1.14 million people and played a part in about 4.71 million deaths.
🧬 How: in billions of bacteria a few are different by chance; the antibiotic kills the rest; the survivors multiply, and they can pass resistance genes to other bacteria on tiny loops of DNA (plasmids).
⚠️ Your body doesn't become resistant. The bacteria do.
🤧 Antibiotics don't work on colds or flu (viruses).
✅ Take antibiotics only when a doctor prescribes them, exactly as prescribed. Never share them or use leftovers.

This video is general information, not medical advice.

Sources:
- GBD 2021 Antimicrobial Resistance Collaborators, The Lancet (2024): global burden of bacterial AMR 1990-2021, forecasts to 2050
- CDC: antibiotic resistance and antibiotic use (antibiotics don't treat viruses; bacteria, not the body, become resistant)
- Nobel Prize: Alexander Fleming, Nobel lecture 1945
- American Society for Microbiology: plasmids and the spread of antibiotic resistance genes
- WHO: antimicrobial resistance fact sheet
""",
    hashtags=["#antibiotics", "#superbugs", "#health", "#science", "#shorts"],
    tags=["antibiotic resistance", "superbugs", "antimicrobial resistance", "AMR", "penicillin", "alexander fleming",
          "antibiotics for cold", "how bacteria become resistant", "plasmid", "health facts", "medical facts",
          "science explained", "doc and the organs"],
    pinned_comment="Quick check: antibiotics kill bacteria, not viruses. So they don't help a cold or the flu. 🦠 "
                   "Did you know that before this video?",
)


def draw(cr, t, tl):
    P.frame(cr, t, tl, S.SHOTS)
