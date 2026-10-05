"""Clever words from history: the Spartans' one-word reply, "If."

Plutarch, On Talkativeness (Moralia 511A): Philip of Macedon wrote to the Spartans, "If I invade Laconia, I will drive
you out", and they wrote back "If." Philip was the father of Alexander the Great; after Chaeronea (338 BC) his army
was the strongest in Greece. He did later march into Laconia and give some of its border land to Sparta's neighbours,
but he never attacked or took the city of Sparta. "Laconic" (brief, saying much in few words) comes from Laconia,
Sparta's region, because Spartans were famous for short replies.
"""
from motion.captions import captions
from motion.characters import CAST, bubble, person
from motion.engine import INK, RED, WHITE, at, blob, cue, ease_out, hexc, lerp, line, pop, rrect_pts, seg, shape, \
    sharp_shape, write
from motion.kit import hl, stamp, whip
from motion.story import CLOSE, GREEN, bg, card, head_c, helmet, scroll, tag, talk

NARRATOR = dict()
TAIL = 0.8

SCRIPT = [
    dict(id="i1", scene="hook", text="A king sent Sparta a scary threat. Sparta answered with one word."),
    dict(id="i2", scene="king", text="The king was Philip of Macedon, the father of Alexander the Great. His army was "
                                     "the strongest in Greece."),
    dict(id="i3", scene="letter", text="He wrote to Sparta: If I invade your land, I will drive you out.",
         speaker="philip", speaker_from="if"),
    dict(id="i4", scene="reply", text="The Spartans wrote back just one word: If.", pace=0.9),
    dict(id="i5", scene="why", text="Why is that so clever? Look at his letter again."),
    dict(id="i6", scene="why", text="Everything hangs on the first word. If. First, he has to get in. And then, he "
                                    "has to win."),
    dict(id="i7", scene="why", text="In one word, the Spartans were telling him: That's a big if."),
    dict(id="i8", scene="bully", text="It's like a bully who says: If I catch you, you're done. And you just answer: "
                                      "If."),
    dict(id="i9", scene="later", text="Years later, Philip did march into their land. But he never took the city of "
                                      "Sparta."),
    dict(id="i10", scene="laconic", text="Their land was called Laconia. That's where the word laconic comes from. "
                                         "Saying a lot, with very few words."),
    dict(id="i11", scene="end", text="So what do you think? What's the best one word reply you've ever heard?",
         pace=0.95),
]

METADATA = dict(
    title="A King Threatened Sparta… They Replied With ONE Word 😳",
    alt_titles=["The Best One-Word Reply in History ⚔️", "Sparta's 1-Word Answer to a King's Threat 🛡️"],
    description="""A king sent Sparta a scary threat. Sparta answered with one word. ⚔️

Philip of Macedon, father of Alexander the Great, had the strongest army in Greece. He wrote to Sparta: "If I invade your land, I will drive you out."

The Spartans wrote back: "If."

Why is that so clever? His whole threat hangs on its first word. First he has to get in, and then he has to win. In one word, the Spartans told him: that's a big if. Years later Philip did march into their land, but he never took the city of Sparta.

Their land was called Laconia, and that's where the word "laconic" comes from: saying a lot with very few words.

Source: Plutarch, On Talkativeness (Moralia 511A).

💬 So what do you think? What's the best one-word reply you've ever heard? 👇

🔔 Interestingly Strange: weird animals, bizarre history, mind-bending paradoxes and strange stories, hand-drawn in under a minute.""",
    hashtags=["#Sparta", "#History", "#Spartans"],
    tags=["sparta", "spartans", "laconic", "spartan reply if", "philip of macedon", "ancient greece",
          "history facts", "clever replies", "one word reply", "interestingly strange"],
    pinned_comment="Best one-word reply you've ever heard? Go 👇⚔️",
)

SKY, GROUND = hexc("#f6e3c0"), hexc("#d6b98a")
GOLD, GOLD_D = hexc("#f2c14e"), hexc("#b9862a")
SPARTA_RED = hexc("#b8322c")
MACE_BLUE = hexc("#2f5fa8")
STONE, STONE_D = hexc("#d9cdb4"), hexc("#b5a68a")
PHILIP, SPARTAN = "philip", "spartan"
CAST.setdefault(PHILIP, dict(skin=hexc("#e8b48a"), shirt=hexc("#8e2f5a"), pants=hexc("#8e2f5a"), bw=100, bh=112,
                             head=41, kind="robe", hair="messy", hair_col=hexc("#3a2a22"),
                             beard=hexc("#3a2a22"), seed=241))
CAST.setdefault(SPARTAN, dict(skin=hexc("#e0a97f"), shirt=SPARTA_RED, pants=hexc("#8e2620"), bw=100, bh=106, head=40,
                              kind="robe", hair="messy", hair_col=hexc("#2b1c14"), beard=hexc("#2b1c14"),
                              seed=247))
CAST.setdefault("soldier_m", dict(skin=hexc("#f0c29c"), shirt=MACE_BLUE, pants=hexc("#24487f"), bw=88, bh=98,
                                  head=36, kind="robe", hair="messy", hair_col=hexc("#3a2a22"), seed=251))


def crown(cr, x, y, s=1.0):
    hx, hy = head_c(PHILIP, x, y, s)
    with at(cr, hx, hy - 40 * s, s):
        sharp_shape(cr, [(-34, 6), (-34, -24), (-17, -6), (0, -30), (17, -6), (34, -24), (34, 6)], GOLD, seed=10,
                    amp=0.3, lw=3.5)


def philip(cr, t, tl, x, y=960, s=1.1, **kw):
    kw.setdefault("arms", ("hip", "hip"))
    kw.setdefault("eyes", "sly")
    person(cr, PHILIP, x, y, t, facing=kw.pop("facing", 1), scale=s, mouth=talk(tl, PHILIP, t, kw.pop("mouth", "smirk")),
           **kw)
    crown(cr, x, y, s)


def spartan(cr, t, x, y=960, s=1.05, facing=-1, **kw):
    kw.setdefault("arms", ("hold", "down"))
    person(cr, SPARTAN, x, y, t, facing=facing, scale=s, **kw)
    helmet(cr, SPARTAN, x, y, s, crest=SPARTA_RED, facing=facing)


def note(cr, x, y, s, text, size=60, w=160, h=120, rot=0.06):
    with at(cr, x, y, s, rot=rot):
        shape(cr, rrect_pts(-w / 2, -h / 2, w, h, 10, 12), hexc("#f4e4bc"), seed=20, amp=0.5, lw=4)
        write(cr, [(text, INK)], 0, size * 0.35, size, align="center", bold=True)


def big_scroll(cr, x, y, s=1.0):
    with at(cr, x, y, s, rot=-0.08):
        shape(cr, rrect_pts(-80, -110, 160, 220, 10, 12), hexc("#f4e4bc"), seed=21, amp=0.5, lw=4)
        for k in range(7):
            line(cr, [(-56, -76 + k * 26), (56 - (k % 3) * 14, -76 + k * 26)], 4, hexc("#8a7a5a"), seed=22 + k,
                 amp=0.4)


def scene_hook(cr, t, tl):
    A = tl.at
    keys = [(0, (1.5, 360, 810)), (A("i1", "sparta", nth=2), (1.65, 470, 820)), (A("i1", "word."), (1.75, 500, 820))]
    bg(cr, t, keys, SKY, GROUND)
    philip(cr, t, tl, 200, arms=("give", "hip"), eyes="sly")
    big_scroll(cr, 300, 800, 0.8)
    spartan(cr, t, 520, arms=("give", "down") if t >= A("i1", "one") else ("hold", "down"), eyes="sly", mouth="smirk")
    if t >= A("i1", "one"):
        note(cr, 430, 790, max(0.6, pop(t, A("i1", "one"), 0.3)) * 0.7, "IF.")
    hl(cr, t, [("a scary ", INK), ("THREAT", RED)], 215, 70, 0.0, end=A("i1", "sparta", nth=2) - 0.05, bold=True,
       sound=False)
    hl(cr, t, [("the reply: ", INK), ("ONE", RED), (" word", INK)], 215, 66, A("i1", "sparta", nth=2), bold=True)
    cue("hit", t, A("i1", "word."))


def scene_king(cr, t, tl):
    A = tl.at
    keys = [(A("i2") - 0.2, (1.5, 330, 810)), (A("i2", "army"), (1.3, 360, 790))]
    bg(cr, t, keys, SKY, GROUND)
    if t >= A("i2", "army"):   # rows of his soldiers behind him
        for row, (yy, sc) in enumerate(((900, 0.62), (935, 0.7))):
            for k in range(6):
                x = 60 + k * 125 + row * 60
                if abs(x - 330) < 90:
                    continue
                st = A("i2", "army") + 0.05 * (k + row * 6)
                if t >= st:
                    person(cr, "soldier_m", x, yy, t, facing=1, arms=("hold", "down"), eyes="dot", mouth="flat",
                           scale=sc)
                    helmet(cr, "soldier_m", x, yy, sc, crest=MACE_BLUE)
    philip(cr, t, tl, 330, arms=("hip", "hip") if t < A("i2", "army") else ("point", "hip"), eyes="sly")
    tag(cr, t, A("i2", "philip"), 330, 560, "PHILIP OF MACEDON", GOLD, s=0.65)
    if A("i2", "father") <= t < A("i2", "army"):
        tag(cr, t, A("i2", "father"), 330, 640, "ALEXANDER'S DAD", hexc("#ffb3c7"), s=0.55, seed=61)
    hl(cr, t, [("the ", INK), ("STRONGEST", RED), (" army", INK)], 215, 66, A("i2", "army"), bold=True)


def scene_letter(cr, t, tl):
    A = tl.at
    keys = [(A("i3") - 0.2, (1.0, 360, 640)), (A("i3", "drive"), (1.06, 360, 640))]
    bg(cr, t, keys, SKY)
    lines = [([("\"If I ", INK), ("invade", RED), (" your land,", INK)], A("i3", "if")),
             ([("I will ", INK), ("drive you out.\"", RED)], A("i3", "drive"))]
    scroll(cr, t, lines, 360, 450, 1.0, size=54, gap=84, w=670)
    philip(cr, t, tl, 360, y=880, s=0.85, arms=("point", "hip"), eyes="sly")
    tag(cr, t, A("i3"), 360, 300, "PHILIP TO SPARTA", GOLD, s=0.6)
    cue("hit", t, A("i3", "out."))


def scene_reply(cr, t, tl):
    A = tl.at
    keys = [(A("i4") - 0.2, (1.5, 400, 810)), (A("i4", "if."), (1.7, 420, 820))]
    bg(cr, t, keys, SKY, GROUND)
    spartan(cr, t, 300, facing=1, arms=("give", "down") if t >= A("i4", "if.") else ("hold", "down"), eyes="sly",
            mouth="smirk")
    spartan(cr, t, 520, facing=-1, arms=("hip", "hip"), eyes="happy", mouth="grin", s=1.0)
    if t >= A("i4", "one"):
        note(cr, 410, 690, max(0.6, pop(t, A("i4", "if."), 0.3)) * (0.9 if t >= A("i4", "if.") else 0.7),
             "IF." if t >= A("i4", "if.") else "", size=80, w=200, h=150)
    hl(cr, t, [("just ", INK), ("ONE", RED), (" word", INK)], 215, 70, A("i4", "just"), bold=True)
    cue("hit", t, A("i4", "if."))


def scene_why(cr, t, tl):
    A = tl.at
    keys = [(A("i5") - 0.2, (1.0, 360, 640))]
    bg(cr, t, keys, SKY)
    focus = t >= A("i6", "if.")
    rest = hexc("#8a8a8a") if focus else INK
    lines = [([("\"", rest), ("If", RED), (" I invade your land,", rest)], A("i5", "look")),
             ([("I will drive you out.\"", rest)], A("i5", "look") + 0.3)]
    scroll(cr, t, lines, 360, 430, 1.0, size=52, gap=82, w=670)
    if focus:   # the word everything hangs on, big
        with at(cr, 360, 630, max(0.6, pop(t, A("i6", "if."), 0.3)), rot=-0.05):
            write(cr, [("IF", RED)], 0, 50, 150, align="center", bold=True)
    if t >= A("i6", "get"):
        card(cr, t, A("i6", "get"), 210, 790, 0.62, "STEP 1", "GET IN", seed=70, w=380)
    if t >= A("i6", "win."):
        card(cr, t, A("i6", "win."), 510, 790, 0.62, "STEP 2", "WIN", seed=71, w=380)
    hl(cr, t, [("why so ", INK), ("CLEVER", GREEN), ("?", INK)], 215, 70, A("i5"), end=A("i6") - 0.05, bold=True)
    hl(cr, t, [("the ", INK), ("FIRST", RED), (" word", INK)], 215, 70, A("i6"), end=A("i7") - 0.05, bold=True)
    hl(cr, t, [("\"That's a ", INK), ("BIG", RED), (" if.\"", INK)], 215, 70, A("i7", "that's"), bold=True)
    if t >= A("i7", "big"):
        stamp(cr, t, A("i7", "big"), "BIG IF!", dur=0.8, y=330)
    cue("hit", t, A("i6", "if."))


def scene_bully(cr, t, tl):
    A = tl.at
    keys = [(A("i8") - 0.2, (1.5, 360, 810))]
    bg(cr, t, keys, hexc("#cfe8f5"), hexc("#9ccc7a"))
    bully_talk = A("i8", "if") <= t < A("i8", "and")
    person(cr, "kid_b", 230, 960, t, facing=1, arms=("point", "hip"), eyes="sly" if t < A("i8", "answer:") else "wide",
           mouth=("o" if int(t * 12) % 2 else "smirk") if bully_talk else ("o" if t >= A("i8", "if.") else "smirk"),
           scale=1.3)
    person(cr, "chotu", 510, 960, t, facing=-1, arms=("hip", "hip") if t >= A("i8", "answer:") else ("down", "down"),
           eyes="sly" if t >= A("i8", "answer:") else "wide", mouth="smirk" if t >= A("i8", "answer:") else "o",
           scale=1.0)
    if t >= A("i8", "if"):
        bubble(cr, 300, 640, 340, 130, (250, 740), [("If I catch you, ", INK), ("you're done!", RED)],
               s=max(0.6, pop(t, A("i8", "if"), 0.25)) * (0.8 if t >= A("i8", "if.") else 1.0), size=40,
               lines=[[("If I catch you,", INK)], [("you're done!", RED)]])
    if t >= A("i8", "if."):
        bubble(cr, 525, 700, 150, 100, (515, 790), [("If.", INK)], s=max(0.6, pop(t, A("i8", "if."), 0.25)),
               size=60)
    hl(cr, t, [("like a ", INK), ("BULLY", RED)], 215, 70, A("i8"), end=A("i8", "answer:") - 0.05, bold=True)
    hl(cr, t, [("you just say: ", INK), ("\"IF.\"", GREEN)], 215, 66, A("i8", "answer:"), bold=True)
    cue("hit", t, A("i8", "if."))


def wall(cr, x0, x1, y, h):
    shape(cr, rrect_pts(x0, y - h, x1 - x0, h, 4, 14), STONE, seed=80, amp=0.5, lw=4)
    for k in range(int((x1 - x0) / 60)):
        shape(cr, rrect_pts(x0 + 8 + k * 60, y - h - 34, 36, 36, 3, 10), STONE, seed=81 + k, amp=0.4, lw=4)
    for r in range(1, int(h / 50)):
        line(cr, [(x0 + 6, y - r * 50), (x1 - 6, y - r * 50)], 3, STONE_D, seed=90 + r, amp=0.5)


def scene_later(cr, t, tl):
    A = tl.at
    keys = [(A("i9") - 0.2, (1.1, 370, 760))]
    bg(cr, t, keys, SKY, GROUND)
    wall(cr, 440, 700, 960, 220)
    write(cr, [("SPARTA", INK)], 570, 860, 40, align="center", bold=True)
    for k, x in enumerate((500, 610)):
        spartan(cr, t, x, y=740, s=0.7, facing=-1, arms=("hip", "hip"), eyes="sly", mouth="smirk")
    u = ease_out(seg(t, A("i9", "march"), A("i9", "march") + 1.2))
    for k in range(3):
        x = lerp(-60, 190, u) - k * 80
        person(cr, "soldier_m", x, 960, t, facing=1, walk=t * 1.4 if 0 < u < 1 else None, arms=("hold", "down"),
               eyes="dot", mouth="flat", scale=0.75)
        helmet(cr, "soldier_m", x, 960, 0.75, crest=MACE_BLUE)
    philip(cr, t, tl, lerp(40, 300, u), arms=("point", "hip"), eyes="sad" if t >= A("i9", "never") else "sly",
           s=0.95, walk=t * 1.4 if 0 < u < 1 else None)
    tag(cr, t, A("i9", "years"), 360, 500, "YEARS LATER", hexc("#ffe6a0"), s=0.6)
    hl(cr, t, [("he ", INK), ("marched in", RED), ("...", INK)], 215, 66, A("i9", "march"), end=A("i9", "never") - 0.05,
       bold=True)
    hl(cr, t, [("but ", INK), ("NEVER", GREEN), (" took Sparta", INK)], 215, 62, A("i9", "never"), bold=True)
    cue("hit", t, A("i9", "never"))


def scene_laconic(cr, t, tl):
    A = tl.at
    keys = [(A("i10") - 0.2, (1.0, 360, 640)), (A("i10", "saying"), (1.04, 360, 640))]
    bg(cr, t, keys, SKY)
    if t >= A("i10", "laconia."):
        card(cr, t, A("i10", "laconia."), 360, 350, 1.0, "THEIR LAND:", "LACONIA", seed=72, top_col=INK,
             bottom_col=SPARTA_RED)
    if t >= A("i10", "laconic"):
        with at(cr, 360, 465, max(0.6, pop(t, A("i10", "laconic"), 0.25))):
            line(cr, [(0, -20), (0, 30)], 8, INK, seed=73, amp=0.2)
            sharp_shape(cr, [(-20, 20), (20, 20), (0, 46)], INK, seed=74, amp=0.2, lw=0)
        card(cr, t, A("i10", "laconic"), 360, 590, 1.0, "THE WORD:", "LACONIC", seed=75, top_col=INK,
             bottom_col=GREEN)
    if t >= A("i10", "saying"):
        lines = [([("saying a ", INK), ("LOT", RED)], A("i10", "saying")),
                 ([("with very ", INK), ("FEW", GREEN), (" words", INK)], A("i10", "few"))]
        scroll(cr, t, lines, 360, 795, 0.95, size=48, gap=70, w=560, h=190)
    hl(cr, t, [("the word ", INK), ("LACONIC", GREEN)], 215, 66, A("i10"), bold=True)


def scene_end(cr, t, tl):
    A = tl.at
    keys = [(A("i11") - 0.2, (1.5, 360, 810)), (A("i11", "best"), (1.65, 400, 815))]
    bg(cr, t, keys, SKY, GROUND)
    philip(cr, t, tl, 210, arms=("hip", "hip"), eyes="wide", mouth="o")
    spartan(cr, t, 520, arms=("give", "down"), eyes="sly", mouth="smirk")
    note(cr, 430, 790, 0.7, "IF.")
    hl(cr, t, [("best ", INK), ("ONE-WORD", RED), (" reply?", INK)], 215, 64, A("i11", "what's"), bold=True,
       underline=True)
    stamp(cr, t, A("i11", "heard?", end=True), "COMMENT BELOW!", dur=0.8, y=330)


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    {"hook": scene_hook, "king": scene_king, "letter": scene_letter, "reply": scene_reply, "why": scene_why,
     "bully": scene_bully, "later": scene_later, "laconic": scene_laconic, "end": scene_end}[name](cr, t, tl)
    cr.restore()
    captions(cr, t, tl)
