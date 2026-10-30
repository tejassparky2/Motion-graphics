"""Explainer 5: "Rabies: The Vaccine Works. So Why Do Thousands Still Die?" Made 30 Oct 2026 under the owner's
standing approval ("make new video auto approved from next"; "Next video"), in the Toxoplasma video's photo style
and the rabies-reel shape (the cure exists, so why do people still die?). Script and sources:
research_notes/explainer_5_rabies.md."""
import math
import os

from poster import (CORAL, CREAM, GOLD, GREEN, INK, MARGIN, RED, W, _along, _round, calendar, card, clamp, counter,
                    cross, draw_text, footnote, gauge, headline, icon_array, magnifier, path, photo, photo_width, prog,
                    ring, stamp, strike, text_size, tick, yes_no_card)

# the narrator, music and pauses are channel-wide; render_doc reads them from this module
from channel import ASSETS_ROOT, GAP, MUSIC, NARRATOR, REVEAL_GAP, TAIL  # noqa: F401
from shots import T, checklist, draw_frame, pic, starts

SCRIPT = [
    dict(id="b1", text="Imagine you're very thirsty. But the moment you see water, your throat locks up in fear."),
    dict(id="b2", text="And it all started with a small scratch from a puppy. Weeks ago. You'd already forgotten it."),
    dict(id="b3", text="And by now, it's too late."),
    dict(id="b4", text="This isn't a zombie movie. It's real."),
    dict(id="b5", text="It's called rabies.", gap=REVEAL_GAP),
    dict(id="b6", text="In India, there are about nine million animal bites every year. Three out of four are from "
                       "dogs."),
    dict(id="b7", text="And an estimated five thousand seven hundred people die of rabies. Every year."),
    dict(id="b8", text="So how does a tiny scratch reach your brain?"),
    dict(id="b9", text="The virus lives in the saliva of an infected animal. A bite, a scratch, or a lick on broken "
                       "skin can let it in."),
    dict(id="b10", text="Then it climbs your nerves. Slowly. All the way up to your brain."),
    dict(id="b11", text="That's why it can hide for weeks, or even months, while you feel completely fine."),
    dict(id="b12", text="A bite on the face reaches the brain faster."),
    dict(id="b13", text="When it gets there, the signs begin. Fever. A strange tingling where you were bitten."),
    dict(id="b14", text="Then swallowing hurts so much that the throat goes into spasms. Even the sight of water can "
                        "set them off."),
    dict(id="b15", text="Once these signs start, rabies is almost always fatal."),
    dict(id="b16", text="But here's the strange part. There's a vaccine. And it works, even after the bite.",
         gap=REVEAL_GAP),
    dict(id="b17", text="So why do thousands still die?"),
    dict(id="b18", text="Because many people never get it. In one big study, more than one in five people bitten by a "
                        "dog got no vaccine at all."),
    dict(id="b19", text="And about half of those who started the shots never finished them."),
    dict(id="b20", text="Some put turmeric or chilli on the wound. Some go to a healer instead. Some think it was "
                        "just a puppy."),
    dict(id="b21", text="And no, it's not fourteen injections in the stomach anymore. Today, it's a few shots in the "
                        "arm."),
    dict(id="b22", text="So, if an animal bites or scratches you, wash the wound with soap and running water, for "
                        "fifteen minutes."),
    dict(id="b23", text="Then go to a hospital the same day. Even for a small scratch. Even if it was a puppy."),
    dict(id="b24", text="And finish every single dose."),
    dict(id="b25", text="Rabies kills almost everyone it reaches. But the vaccine can stop it, if you don't wait.",
         gap=REVEAL_GAP),
    dict(id="b26", text="Has a dog ever bitten or scratched you? Yes or no, tell me in the comments."),
]
for _b in SCRIPT:
    _b.setdefault("scene", _b["id"])
for _b in SCRIPT[1:]:
    _b.setdefault("gap", GAP)


METADATA = dict(
    title="Rabies: The Vaccine Works. So Why Do Thousands Still Die?",
    alt_titles=["A Puppy Scratch Can Kill You Months Later", "Why Rabies Makes You Afraid of Water",
                "The Disease That Climbs Your Nerves to Your Brain"],
    caption="Thirsty, but terrified of water 😳 That's rabies, and it still kills an estimated 5,700 people in India "
            "every year.\n\n"
            "If an animal bites or scratches you:\n✅ Wash the wound with soap and running water for 15 minutes\n"
            "✅ Go to a hospital the same day, even for a small scratch, even if it was a puppy\n"
            "✅ Finish every dose of the vaccine\n"
            "❌ No turmeric, chilli or anything else on the wound\n"
            "❌ It's not 14 injections in the stomach anymore: today it's a few shots in the arm\n\n"
            "Once the signs start, rabies is almost always fatal. The vaccine works, if you don't wait.\n\n"
            "Has a dog ever bitten or scratched you? Comment YES or NO 👇",
    yt_title="Why Rabies Makes You Afraid of Water 😳",
    yt_description="Rabies climbs your nerves to your brain, and once the signs start it's almost always fatal. "
                   "In India there are about 9 million animal bites a year, three in four from dogs, and an estimated "
                   "5,700 rabies deaths. The vaccine works even after the bite, so why do people still die?\n\n"
                   "If an animal bites or scratches you:\n✅ Wash the wound with soap and running water for 15 minutes\n"
                   "✅ Go to a hospital the same day, even for a small scratch\n"
                   "✅ Finish every dose of the vaccine\n"
                   "❌ No turmeric, chilli or anything else on the wound\n\n"
                   "General information, not medical advice.",
    hashtags=["#rabies", "#dogbite", "#healthawareness", "#india", "#sciencefacts"],
    tags=["rabies", "dog bite", "rabies vaccine", "hydrophobia", "fear of water", "anti rabies vaccine", "india",
          "stray dogs", "health facts", "science explained"],
    pinned_comment="Has a dog ever bitten or scratched you? 🐕 YES or NO? 👇",
    sources=["WHO, Rabies fact sheet",
             "CDC, Rabies: how it spreads, symptoms",
             "ICMR-National Institute of Epidemiology, The Lancet Infectious Diseases, 2025, burden of human rabies "
             "deaths and animal bites in India 2022-23",
             "Ministry of Health and Family Welfare, National Action Plan for Dog Mediated Rabies Elimination"],
)


def draw(cr, t, tl):
    pass
