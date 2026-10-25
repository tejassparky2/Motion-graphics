"""Explainer 1: "The Cure for a Snakebite Is Made Inside a Horse" (new explainer format, owner-approved script,
24 Oct 2026). One narrator (Chatterbox Turbo stock voice + tags), aged paper, FIG headers, two-line headlines, no
subtitles. Script, shot list and sources: research_notes/explainer_1-3.md.
"""
from motion import paper as P
from videos import snakebite_shots as S

NARRATOR = dict(turbo=True, turbo_ref="am_echo", rate=4.7, tempo_min=0.88)   # owner's pick, voice D
STYLE = "clean"
MUSIC = "explainer"
TAIL = 1.2

SCRIPT = [
    dict(id="s1", scene="s1", text="[dramatic] If a cobra bites you tonight, the medicine that saves you was made "
                                   "inside a horse."),
    dict(id="s2", scene="s2", text="Not a lab. Not a factory. A horse."),
    dict(id="s3", scene="s3", text="A huge study found that snakebites killed about fifty-eight thousand Indians a "
                                   "year, for twenty years."),
    dict(id="s4", scene="s4", text="That's close to half of all snakebite deaths in the world."),
    dict(id="s5", scene="s5", text="So how does a horse fix a snakebite? First, let's see what venom does."),
    dict(id="s6", scene="s6", text="Your body runs on messages."),
    dict(id="s7", scene="s7", text="Your nerves tell your muscles when to move, and when to breathe."),
    dict(id="s8", scene="s8", text="The venom of a cobra or a [kryte|krait] jams that signal."),
    dict(id="s9", scene="s9", text="The eyelids droop first. Then the breathing muscles can stop."),
    dict(id="s10", scene="s10", text="Viper venom does something else. It stops your blood from clotting."),
    dict(id="s11", scene="s11", text="Now, the horse."),
    dict(id="s12", scene="s12", text="Scientists collect venom from the four snakes behind most deaths in India."),
    dict(id="s13", scene="s13", text="They give a horse tiny doses. Too small to hurt it."),
    dict(id="s14", scene="s14", text="The horse's immune army learns the enemy, and builds antibodies."),
    dict(id="s15", scene="s15", text="Doctors take some of its blood, and purify those antibodies."),
    dict(id="s16", scene="s16", text="That's antivenom. Borrowed bodyguards that grab the venom before it does more "
                                     "damage."),
    dict(id="s17", scene="s17", text="But many people don't die from the snake. They die from the delay."),
    dict(id="s18", scene="s18", text="A [kryte|krait] often bites at night, while people sleep on the floor."),
    dict(id="s19", scene="s19", text="The bite can be almost painless, so people go back to sleep."),
    dict(id="s20", scene="s20", text="Others lose hours on cutting, sucking, tight ropes or herbs."),
    dict(id="s21", scene="s21", text="None of these remove the venom."),
    dict(id="s22", scene="s22", text="Doctors say: stay calm, keep the bitten arm or leg still, and get to a "
                                     "hospital fast."),
    dict(id="s23", scene="s23", text="Did you know your life could depend on a horse? Tell me in the comments."),
]
for _b in SCRIPT[1:]:
    _b.setdefault("gap", 0.42)      # a calm breath between lines, like the reference explainers

METADATA = dict(
    title="The Cure for a Snakebite Is Made Inside a Horse 🐍🐴",
    alt_titles=["Why Snakebite Medicine Comes From Horses", "India's Deadliest Animal Isn't a Tiger 🐍",
                "How Antivenom Is Made (It Starts With a Horse)"],
    description="""If a cobra bites you, the medicine that saves you was made inside a horse. 🐴

🐍 About 58,000 people a year died from snakebite in India between 2000 and 2019 (Million Death Study), close to half of the world's snakebite deaths.
🧪 Cobra and krait venom jams the signal from nerves to muscles; viper venom stops blood from clotting.
🐴 Antivenom: horses get tiny, safe doses of venom from the "Big Four" (cobra, common krait, Russell's viper, saw-scaled viper), make antibodies, and those antibodies are purified from their blood.
⏱️ Many deaths come from delay: krait bites at night can be almost painless; cutting, sucking, tight ropes and herbs don't remove venom.
✅ What doctors say: stay calm, keep the limb still, get to a hospital fast. Antivenom works best early.

This video is general information, not medical advice. In an emergency, go to the nearest hospital.

Sources:
- Suraweera et al., "Trends in snakebite deaths in India from 2000 to 2019", eLife 2020 (Million Death Study)
- WHO, Snakebite envenoming fact sheet
- India's snakebite first aid ("Do it R.I.G.H.T.": Reassure, Immobilise, Get to Hospital, Tell the doctor)
- NIH Fogarty International Center, "Antivenom: a brief history"
""",
    hashtags=["#snakebite", "#antivenom", "#health", "#science", "#india", "#shorts"],
    tags=["snakebite", "antivenom", "how antivenom is made", "antivenom horse", "snake bite india", "cobra",
          "krait", "russell's viper", "saw scaled viper", "big four snakes", "snakebite first aid",
          "venom", "health facts", "medical facts", "science explained", "doc and the organs"],
    pinned_comment="Antivenom is made from horses that are given tiny, safe doses of venom. 🐴 Did you know that? "
                   "And what's the scariest snake where you live?",
)


def draw(cr, t, tl):
    P.frame(cr, t, tl, S.SHOTS)
