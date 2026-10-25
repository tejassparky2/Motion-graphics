# Batch 10: AI news explainers (eps 36-39), auto-approved

Owner, 24 Oct 2026, with a reference ("Hey USA, what's new with you?", a talking US flag explaining New York's measles
emergency): "Can we make latest news videos like this but focus on ai technology software like that?" Asked: low-poly
channel, 4 videos, auto-approved.

## The reference's form (67 s, ~170 words)
"Hey X, what's new with you?" → X states the news → "Wait, what?" → the simple background (what measles is) → the
history (eliminated 26 years ago, thanks to MMR) → "So what about the emergency?" → why (people stopped vaccinating)
→ numbers year by year (285 → 2,289 → 3,887) → the official action (executive order) → "What does that even do?" →
what changes (more people allowed to vaccinate) → a closing thought. Big all-caps captions 2-3 words at a time
(Anton-style, red/white), a picture change every ~1.5 s, no music to speak of, fast talk.

Ours: Dev asks Claude or Codex "Hey Claude, what's new with you?"; the AI explains one real AI/software story in the
same steps; Dev asks the questions a viewer would; headline and number cards carry the facts (kit.headline, kit.bignum);
th.captions in Anton (white, the spoken word red).

## Facts (opened at the primary source on 24 Oct 2026)
- LiteLLM (docs.litellm.ai, 21 Oct and the 23 Oct attack-chain post): malicious `litellm==1.107.0` on PyPI 11:39-13:23
  UTC and Docker Hub tags (incl. `latest`) 11:46-14:20 UTC on 21 Oct; "steals credentials and loads remote-code
  execution tools"; runs again on any Python start; safe: pin 1.106.2; treat hosts as compromised, rotate keys,
  rebuild. Root cause: a master key committed to a public repo on 27 May 2026, "key revocation did not occur", used
  by the attacker on 10 Oct; 3 GitHub identities; built from a lookalike "Berri-AI" fork.
- Scion (anthropic.com/engineering/redesigning-source-control, 13 Oct, updated 15 Oct): ~2,500 changes/day in May
  2026 → 30,000+/day by September; ~25 million CI checkouts/day; naive git fetching = "over 600 PB of git traffic per
  day"; Scion's CPU/memory footprint 200x smaller than the old git mirrors; built by seven people (Scion + Antique) and
  migrated in five months; "Scion is by no means a suitable replacement for git for general use"; "The bottleneck,
  now, is all of the developer infrastructure built for human scale".
- Google Cloud (cloud.google.com blog, 21 Oct): GPT-6 Astra, GPT-6.1 Sol, GPT-6 Luna in private preview for select
  enterprise customers; Codex CLI and Desktop can connect "starting today"; one Google Cloud invoice, draws down
  existing commitments; Google says it is "the only hyperscale cloud provider offering access to all three leading
  closed source LLMs". Claude (claude.com, 22 Oct): Claude Models on Google Cloud (Anthropic managed) generally
  available, with Fable 5.1, Opus 5.5, Sonnet 5.5, Haiku 5.5.
- Claude Duet (claude.com, 21 Oct): research preview, waitlist, US Pro and Max first, iOS/Android/claude.ai; morning
  brief; checks connected accounts "every few hours"; runs on its own virtual machine with its own browser; asks
  "before it sends a message, makes a payment, signs a document, or deletes anything"; never trades securities or
  moves money between accounts, even with approval; 6,000+ connectors; background checks count toward plan limits.

---

## Ep 36: "Hey Codex, What's New? (LiteLLM Got Hacked)"
| # | Who | Line | Card |
|---|---|---|---|
| 1 | Dev | Hey Codex. What's new with you? | |
| 2 | Codex | A popular AI tool got hacked. LiteLLM. | headline |
| 3 | Dev | Wait, what? Lite what? | |
| 4 | Codex | LiteLLM. It lets apps talk to lots of AI models through one plug. | |
| 5 | Dev | So what happened? | |
| 6 | Codex | On October twenty-first, someone took over its release pipeline. | |
| 7 | Codex | They published version 1.107.0. With malware inside. | version card |
| 8 | Dev | What does the malware do? | |
| 9 | Codex | It steals passwords and cloud keys. And it runs every time Python starts. | |
| 10 | Dev | How long was it up? | |
| 11 | Codex | On pip, about an hour and forty minutes. On Docker, over two hours. | timeline card |
| 12 | Dev | How did they even get in? | |
| 13 | Codex | A secret key leaked in May. Nobody revoked it. | "May 27 → Oct 10" |
| 14 | Dev | So what do I do? | |
| 15 | Codex | If you installed 1.107.0, treat that machine as hacked. Change every key. Rebuild it. | |
| 16 | Codex | The safe version is 1.106.2. | |
| 17 | Dev | And next time? | |
| 18 | Codex | Pin your versions. Don't trust latest. | |
| 19 | Dev | One old key. Five months later. | |
| 20 | Codex | That's why you revoke them. | |

## Ep 37: "Hey Claude, What's New? (Anthropic Stopped Using Git)"
| # | Who | Line | Card |
|---|---|---|---|
| 1 | Dev | Hey Claude. What's new with you? | |
| 2 | Claude | My company stopped using git. | headline |
| 3 | Dev | Wait, what? Everyone uses git. | |
| 4 | Claude | Not in our main repo. Not anymore. | |
| 5 | Dev | Why would they stop? (was "Why?", heard "What?") | |
| 6 | Claude | Because of agents like me. In May, we merged about twenty-five hundred changes a day. | 2,500 |
| 7 | Claude | By September, over thirty thousand. | 30,000 |
| 8 | Dev | Thirty thousand a day? | |
| 9 | Claude | And twenty-five million code checkouts a day, just for testing. | 25,000,000 |
| 10 | Dev | Does git break? (was "Git can't handle that?" then "Too much for git?", heard "can handle" / "forget") | |
| 11 | Claude | Done the normal way, that's over six hundred petabytes a day. | 600 PB |
| 12 | Dev | So what did they build? | |
| 13 | Claude | Scion. Their own version control. Two hundred times lighter than the old git mirrors. | 200x |
| 14 | Dev | How many people built that? | |
| 15 | Claude | Seven. In five months. | |
| 16 | Dev | Should I delete git? | |
| 17 | Claude | No. They say it only makes sense for giant repos. | |
| 18 | Dev | So the slow part isn't writing code anymore. | |
| 19 | Claude | No. It's the tools built for humans. | |

## Ep 38: "Hey Codex, What's New? (OpenAI Moves Into Google Cloud)"
| # | Who | Line | Card |
|---|---|---|---|
| 1 | Dev | Hey Codex. What's new with you? | |
| 2 | Codex | I'm moving in with Google. | |
| 3 | Dev | Wait, what? | |
| 4 | Codex | On October twenty-first, Google Cloud started offering OpenAI's models. | headline |
| 5 | Dev | OpenAI? On Google? | |
| 6 | Codex | GPT-6 Astra, GPT-6.1 Sol, and GPT-6 Luna. In private preview, for some big companies. | models card |
| 7 | Dev | And you? | |
| 8 | Codex | Codex can connect to it from day one. | |
| 9 | Dev | What about Claude? | |
| 10 | Codex | One day later, Claude's full platform went live there too. | headline |
| 11 | Dev | So Google sells its rivals? | |
| 12 | Codex | Google says it's the only big cloud with all three. Gemini, Claude, and GPT. | 3 logos-free card |
| 13 | Dev | Why would companies want that? | |
| 14 | Codex | One bill. And it counts toward what they already promised to spend on Google. | |
| 15 | Dev | And for developers? | |
| 16 | Codex | Switching models gets easier. Same account. | |
| 17 | Dev | Rivals in one shop. | |
| 18 | Codex | Like a food court. For AI. | |

## Ep 39: "Hey Claude, What's New? (An AI That Works While You Sleep)"
| # | Who | Line | Card |
|---|---|---|---|
| 1 | Dev | Hey Claude. What's new with you? | |
| 2 | Claude | I have a new app. It works while you sleep. | |
| 3 | Dev | Wait, what? | |
| 4 | Claude | It's called Claude Duet. A research preview, from October twenty-first. | headline |
| 5 | Dev | What does it do? | |
| 6 | Claude | Every morning, it sends you a short brief. Then it checks your connected apps every few hours. | |
| 7 | Dev | Even when my laptop is off? | |
| 8 | Claude | Yes. It runs on its own computer, with its own browser. | |
| 9 | Dev | Can it pay my bills? | |
| 10 | Claude | Only if you say yes. It asks before it sends, pays, signs, or deletes anything. | rules card |
| 11 | Dev | Can it trade stocks for me? | |
| 12 | Claude | Never. Not even if you say yes. | |
| 13 | Dev | Who can use it? | |
| 14 | Claude | There's a waitlist. Pro and Max users in the US go first. | |
| 15 | Dev | Does it cost extra? | |
| 16 | Claude | It's in the plan. But its background checks use your limits. | |
| 17 | Dev | An AI that works while I sleep. | |
| 18 | Claude | And only wakes you when something needs you. | |
