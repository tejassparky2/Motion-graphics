"""Low-poly channel, episode 36: AI news explainer, "Why Is Codex Changing My Keys? (LiteLLM Got Hacked)".

Script: channels/lowpoly/scripts/batch10_ai_news_eps36-39.md (auto-approved by the owner, 24 Oct 2026). Form of the
owner's reference (a news explainer; its own opener is not reused): Dev asks, the AI explains one real story step by step, Dev asks
what a viewer would, headline and number cards, Anton captions 1-3 words at a time. Real: docs.litellm.ai, 21 Oct 2026
incident post and 23 Oct attack-chain post. Parody characters; not affiliated with OpenAI or LiteLLM.

    python channels/lowpoly/make_skit.py ep36_litellm
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import bignum, build_script, frames, headline, skit_voice   # noqa: E402
from motion import thriller as th, voice   # noqa: E402
from motion.engine import cue, hexc   # noqa: E402
from motion.polish import vignette   # noqa: E402

NARRATOR = dict(turbo=True, turbo_ref="am_michael")
DIRECTION = "ep36"
MUSIC = "score"
SCORE = [(0, "light"), ("n17", "tender"), ("n20", "end", 0.9)]
TAIL = 0.8
FRAMES = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "build", "lowpoly", "ep36_frames")
_frame = frames(FRAMES)
voice.SPEAKERS.update({"codex": dict(voice="am_puck", speed=1.05, turbo_ref="am_puck+2")})
skit_voice(voice)

DEV, CX = None, "codex"
V7 = "[one point one oh seven point oh|1.107.0]"
_lines = [   # (id, shot, speaker, text, gap before, pace)
    ("n1", "devmid", DEV, "Why are you changing my keys?", 0, 1),
    ("n2", "cxclose", CX, "A popular AI tool got hacked. [Lite L L M.|LiteLLM.]", .3, 1),
    ("n3", "devclose", DEV, "Wait, what? Lite what?", .3, 1),
    ("n4", "cx", CX, "[Lite L L M.|LiteLLM.] It lets apps talk to lots of AI models through one plug.", .3, 1),
    ("n5", "devclose", DEV, "So what happened?", .3, 1),
    ("n6", "cxclose", CX, "On [October twenty-first,|Oct 21,] someone took over its release pipeline.", .3, 1),
    ("n7", "cxclose", CX, f"They published version {V7}. With malware inside.", .25, 1),
    ("n8", "devclose", DEV, "What does the malware do?", .3, 1),
    ("n9", "cx", CX, "It steals passwords and cloud keys. And it runs every time Python starts.", .3, 1),
    ("n10", "devclose", DEV, "How long was it up?", .3, 1),
    ("n11", "cxclose", CX, "On pip, about an hour and forty minutes. On Docker, over two hours.", .3, 1),
    ("n12", "devmid", DEV, "How did they even get in?", .3, 1),
    ("n13", "cxclose", CX, "A secret key leaked in May. Nobody revoked it.", .3, 1),
    ("n14", "devclose", DEV, "So what do I do?", .35, 1),
    ("n15", "cx", CX, f"If you installed {V7}, treat that machine as hacked. Change every key. Rebuild it.", .3, 1),
    ("n16", "cxclose", CX, "The safe version is [one point one oh six point two.|1.106.2.]", .25, 1),
    ("n17", "devclose", DEV, "And next time?", .35, 1),
    ("n18", "cxclose", CX, "Pin your versions. Don't trust latest.", .3, 1),
    ("n19", "devclose", DEV, "One old key. Five months later.", .5, .95),
    ("n20", "cxclose", CX, "That's why you revoke them.", .4, 1),
]
HOLDS = {}
GAP_FIX = {}
SCRIPT = build_script(_lines, HOLDS, gap=1.0, gap_fix=GAP_FIX)

METADATA = dict(
    title="LiteLLM Got Hacked: What Happened and What to Do",
    alt_titles=["Why Is Codex Changing My Keys?", "One Leaked Key, Five Months Later"],
    description="""A popular AI library shipped a release that steals credentials. Codex explains what happened, how
the attackers got in, and what to do if you installed it.

Real (docs.litellm.ai, 21 and 23 Oct 2026): litellm 1.107.0 on PyPI (11:39-13:23 UTC, 21 Oct) and its Docker images
(until 14:20 UTC) contained malware that steals credentials. The way in: a master key committed to a public repo on
27 May 2026 that was never revoked, used by the attacker on 10 Oct. Safe: pin 1.106.2. If 1.107.0 ran anywhere, rotate
every key that machine could reach and rebuild it. Dev and Codex are parody characters.

Ep. 36 of Dev vs the bots. Parody. Not affiliated with OpenAI or LiteLLM.

💬 Do you pin your dependencies, or live on latest? 👇""",
    hashtags=["#LiteLLM", "#CyberSecurity", "#AINews"],
    tags=["litellm hack", "litellm 1.107.0", "supply chain attack", "pypi malware", "ai news", "codex",
          "python security", "devops", "programmer humor", "tech news"],
    pinned_comment="Do you pin your dependencies, or live on latest? 👇 Subscribe for tomorrow's AI news.",
)
GREEN, RED, GREY, YEL = (hexc(c) for c in ("#7ee08a", "#ff5c5c", "#8a93a6", "#ffd23f"))
WHITE = (1, 1, 1)


def draw(cr, t, tl):
    cr.set_source_surface(_frame(t), 0, 0)
    cr.paint()
    vignette(cr, 0.64)
    th.grain(cr, t, 0.05)
    B = tl.by_id
    headline(cr, t, B["n2"].start + 0.3, B["n3"].end + 0.2, "docs.litellm.ai", "Security incident: LiteLLM release pipeline compromised",
             [("Oct 21, 2026", GREY), ("version 1.107.0 steals credentials", RED)], clock="Oct 21")
    bignum(cr, t, B["n7"].start + 0.3, B["n7"].end + 0.2, "PyPI · Docker", "1.107.0", "malicious release", col=RED)
    headline(cr, t, B["n11"].start, B["n11"].end + 0.2, "timeline  ·  21 Oct (UTC)", "How long it was up",
             [("PyPI     11:39 - 13:23", WHITE), ("Docker   11:46 - 14:20", WHITE), ("incl. the 'latest' tag", YEL)])
    headline(cr, t, B["n13"].start, B["n13"].end + 0.2, "attack chain  ·  23 Oct post", "A master key leaked in a public repo",
             [("May 27   key committed", WHITE), ("never revoked", RED), ("Oct 10   attacker uses it", WHITE)])
    headline(cr, t, B["n15"].start + 0.4, B["n16"].end + 0.3, "what to do", "If 1.107.0 ever ran:",
             [("treat the machine as hacked", RED), ("rotate every key it could reach", WHITE), ("rebuild it", WHITE),
              ("safe version: 1.106.2", GREEN)])
    cue("ding", t, B["n2"].start + 0.3)
    th.captions(cr, t, tl, y=400, size=60)
