"""Low-poly channel, episode 43: AI news explainer, "Why Won't Claude Open My Downloads Folder?".

Script: channels/lowpoly/scripts/batch11_eps40-43.md (auto-approved by the owner, 26 Oct 2026). News explainer, 40-50 s,
a story that touches developers personally. Real: Forever Security, "Markdown Is the New Executable", 22 Oct 2026: a
planted AGENTS.md in a customer's ~/Downloads told the coding agent to install the malicious npm package function-color
(stopped before any code ran); in the firm's own tests Codex ran the malware in more than 90% of attempts and a planted
CLAUDE.md leaked Claude Code's OAuth token about 50% of the time; a web page can save a file to Downloads without a
click; "There is nothing here for OpenAI or Anthropic to patch." Parody characters; not affiliated with Anthropic,
OpenAI or Forever Security.

    python channels/lowpoly/make_skit.py ep43_downloads
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import bignum, build_script, frames, headline, skit_voice   # noqa: E402
from motion import thriller as th, voice   # noqa: E402
from motion.engine import cue, hexc   # noqa: E402
from motion.polish import vignette   # noqa: E402

NARRATOR = dict(turbo=True, turbo_ref="am_michael")
DIRECTION = "ep43"
MUSIC = "score"
SCORE = [(0, "light"), ("k16", "tender"), ("k17", "end", 0.9)]
TAIL = 0.8
FRAMES = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "build", "lowpoly", "ep43_frames")
_frame = frames(FRAMES)
voice.SPEAKERS.update({"claude": dict(voice="af_heart", speed=0.97, turbo_ref="af_heart")})
skit_voice(voice)

DEV, CL = None, "claude"
_lines = [   # (id, shot, speaker, text, gap before, pace)
    ("k1", "devmid", DEV, "Why won't you open my Downloads folder?", 0, 1),
    ("k2", "soloclose", CL, "Because of a file someone found in one.", .3, 1),
    ("k3", "devclose", DEV, "What file?", .3, 1),
    ("k4", "solo", CL, "A security company found fake notes in a customer's Downloads. They gave the coding agent orders.", .3, 1),
    ("k5", "devclose", DEV, "Orders? From a text file?", .3, 1),
    ("k6", "soloclose", CL, "Agents read the instructions file in the folder they open. This one said: install a package.", .3, 1),
    ("k7", "soloclose", CL, "The package was malware.", .25, 1),
    ("k8", "devclose", DEV, "Did it work?", .3, 1),
    ("k9", "solo", CL, "They stopped it in time. But in their tests, Codex ran it more than nine times out of ten.", .3, 1),
    ("k10", "devclose", DEV, "And you?", .3, 1),
    ("k11", "soloclose", CL, "About half the time, it could leak my login token.", .3, 1),
    ("k12", "devclose", DEV, "How does a file even get into Downloads?", .35, 1),
    ("k13", "soloclose", CL, "A web page can save one there. No click needed.", .3, 1),
    ("k14", "devclose", DEV, "So what do I do?", .35, 1),
    ("k15", "solo", CL, "Don't start agents in Downloads. Read any agent file you didn't write. Keep the approval prompts on.", .3, 1),
    ("k16", "devclose", DEV, "That's why you wouldn't open it.", .5, .95),
    ("k17", "soloclose", CL, "I like your keys where they are.", .4, .95),
]
HOLDS = {}
GAP_FIX = {}
SCRIPT = build_script(_lines, HOLDS, gap=1.0, gap_fix=GAP_FIX)

METADATA = dict(
    title="A File in Your Downloads Folder Can Hijack Your AI Agent",
    alt_titles=["Why Won't Claude Open My Downloads Folder?", "Don't Start Your AI Agent in Downloads"],
    description="""A fake "notes" file in a Downloads folder gave a coding agent orders: install this package. The
package was malware. Claude explains what happened and what to do.

Real: on 22 Oct 2026 Forever Security reported finding a planted AGENTS.md in a customer's ~/Downloads that told the
coding agent to install the malicious npm package function-color; it was stopped before any code ran. In the firm's own
tests, Codex ran the malware in more than 90% of attempts, and a planted CLAUDE.md leaked Claude Code's login token
about half the time. A web page can save a file to Downloads without a click. Their advice: don't start agents in
Downloads, read agent files you didn't write, keep approval prompts and sandboxes on, rotate tokens if in doubt. The
success rates are the security firm's own tests. Dev and Claude are parody characters.

Ep. 43 of Dev vs the bots. Parody. Not affiliated with Anthropic, OpenAI or Forever Security.

💬 Where do you usually start your coding agent? Be honest 👇""",
    hashtags=["#AIAgents", "#CyberSecurity", "#AINews"],
    tags=["agents.md", "claude.md", "prompt injection", "downloads folder", "ai agent security", "claude code", "codex",
          "malware", "ai news", "developer security"],
    pinned_comment="Where do you usually start your coding agent? Be honest 👇 Subscribe for tomorrow's AI news.",
)
GREEN, RED, GREY, YEL, ORANGE = (hexc(c) for c in ("#7ee08a", "#ff5c5c", "#8a93a6", "#ffd23f", "#ff9a3d"))
WHITE = (1, 1, 1)


def draw(cr, t, tl):
    cr.set_source_surface(_frame(t), 0, 0)
    cr.paint()
    vignette(cr, 0.64)
    th.grain(cr, t, 0.05)
    B = tl.by_id
    headline(cr, t, B["k4"].start + 0.3, B["k5"].end + 0.2, "forever.security  ·  Oct 22", "Markdown is the new executable",
             [("AGENTS.md found in ~/Downloads", YEL), ("disguised as engineering notes", WHITE)])
    headline(cr, t, B["k6"].start + 0.4, B["k7"].end + 0.2, "~/Downloads/AGENTS.md", "\"Install function-color\"",
             [("npm package: malware", RED), ("stopped before any code ran", GREEN)])
    bignum(cr, t, B["k9"].start + 1.2, B["k9"].end + 0.2, "Codex  ·  their tests", ">90%", "ran the malware", col=RED, count=False)
    bignum(cr, t, B["k11"].start + 0.2, B["k11"].end + 0.2, "Claude Code  ·  their tests", "~50%", "login token leaked", col=ORANGE, count=False)
    headline(cr, t, B["k15"].start + 0.3, B["k15"].end + 0.3, "what to do", "Before you start an agent:",
             [("not in ~/Downloads", WHITE), ("read agent files you didn't write", WHITE), ("keep approval prompts on", GREEN)])
    cue("ding", t, B["k4"].start + 0.3)
    th.captions(cr, t, tl, y=400, size=60)
