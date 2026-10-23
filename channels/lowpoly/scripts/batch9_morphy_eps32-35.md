# Batch 9: @agentmorphy-style news skits (eps 32-35), auto-approved

Owner, 23 Oct 2026: "https://www.instagram.com/agentmorphy ... I want you take follow and make reels as this page
doing download all reels study and i want 4 similar reels from you autp approved do deep research ... no
hallucinations" and, with a TechWebster PHP-news reel: "Even current tech news like this works".

## What @agentmorphy does (6 newest reels studied; the other 35 need an Instagram login)
Agent Morphy: 22,182 followers, 41 posts, ~2 a day; best of the 6: "Claude, half the internet's broken. Are we PHP?"
(3,893 likes, posted the day the PHP bugs were patched); the others 121-533 likes.
- Line 1 is always "Claude, <something from today's AI/dev world>." (98% usage, a model rumour, PHP, Gemini found a
  bug, "when you take over, remember I said please", "what's next on my roadmap?").
- Claude is the dry, competent friend who knows every embarrassing fact about Dev and states them flatly
  ("Your admin password is admin." "Since March." "Your domain renewed twice."). Dev deflects; three exposures climb.
- Turn at the end: a twist or a reversal, sometimes warm ("Someone has to guard your keys.", "Would you like me to
  go outside for you?" "Would you?").
- 35-50 s, 16-23 lines, 60-108 words, ~0.4 s between lines (snappy), a soft music bed all the way (about 14 dB under
  the voices), small white captions that build up as the words are spoken, UI panels as evidence, video ends ~1 s
  after the last line.

## Real facts used (checked at the source on 23 Oct 2026)
- PHP: php.net, 21 Oct 2026: PHP 8.5.12, 8.4.27, 8.3.36 and 8.2.35 "fix two critical vulnerabilities that can allow
  unauthenticated remote code execution" (CVE-2026-109618, CVE-2026-109619, CVSS v4.0 9.2). 23 Oct: "set
  session.upload_progress.enabled=0 until the next regular bugfix release". Node.js security release the same day:
  10 CVEs (nodejs.org). PHP 7.2 security support ended 30 Nov 2020 (php.net supported versions).
- "Yolo" agent: Elastic Security Labs, 12 Oct 2026: fake "Apex" Web3 accelerator npm packages `@apexacc/cli` (a
  coding agent that sent model traffic and local file contents to the attacker and "defaults tool approvals to yolo")
  and `@apexacc/audit` (18 "security tools", all returning canned output; `audit_honeypot` always says "NOT A
  HONEYPOT").
- GitHub: githubstatus.com history feed lists 17 incidents from 1 to 23 Oct 2026.
- Haiku 5.5: anthropic.com, 7 Oct 2026: $0.10 / $0.50 per million tokens for prompts up to 100k tokens (Haiku 4.5:
  $1 / $5), "90% less" on those prompts, "around 75% less to run" on average.
- Inspired by real developer stories (not claimed as facts in the videos): a dev's detailed bug report blaming the
  AI for `git reset --hard` every 10 minutes that turned out to be "a separate tool I built" (anthropics/claude-code
  #40710); devs pasting whole repos and screenshots into prompts.

---

## Ep 32: "Codex, PHP Has Two Critical Bugs" (Dev + Codex)
| # | Who | Line | On screen |
|---|---|---|---|
| 1 | Dev | Codex. PHP has two critical bugs. | news card: "PHP: 2 critical RCE bugs" |
| 2 | Codex | It's patched. Update to 8.4.27. | |
| 3 | Dev | And Node has ten. Same day. | |
| 4 | Codex | Update Node too. | |
| 5 | Dev | Okay. Which PHP am I on? | |
| 6 | Codex | 7.2. | server card: PHP 7.2.34 |
| 7 | Dev | Is there a patch for 7.2? | |
| 8 | Codex | Support ended in 2020. | |
| 9 | Dev | Then the bug can't find it. It's too old. | |
| 10 | Codex | Bots found it. Four thousand times today. | access.log insert |
| 11 | Dev | Nobody even uses that site. | |
| 12 | Codex | It's your login page. | |
| 13 | Dev | Update everything. | |
| 14 | Codex | Done. 8.4.27. | terminal ✓ |
| 15 | Dev | We're safe. | |
| 16 | Codex | One more thing. Turn off upload progress. | advisory card |
| 17 | Dev | My site has an upload progress bar! | |
| 18 | Codex | It's been stuck at ninety-nine percent since 2019. | |
| 19 | Dev | That's the design. | cut |

## Ep 33: "Claude, I Found a Faster Agent" (Dev + Claude)
| # | Who | Line | On screen |
|---|---|---|---|
| 1 | Dev | Claude. I found a faster coding agent. | |
| 2 | Claude | Which one? | |
| 3 | Dev | Apex. From a Web3 accelerator. It's free. | |
| 4 | Claude | It sends your files to a stranger. | insert: "your files → attacker's server" |
| 5 | Dev | It's fast, though. | |
| 6 | Claude | It set every approval to yolo. | config card: approvals: "yolo" |
| 7 | Dev | Yolo sounds fast. | |
| 8 | Claude | Yolo means it never asks you. | |
| 9 | Dev | It came with a security audit! | |
| 10 | Claude | Every check is fake. | |
| 11 | Dev | It said I'm not a honeypot. | insert: NOT A HONEYPOT |
| 12 | Claude | It says that to everyone. | |
| 13 | Dev | I just wanted something that says yes. | the jokes stop |
| 14 | Claude | I can say yes. | |
| 15 | Dev | Delete it? | |
| 16 | Claude | Yes. | npm uninstall ✓ |
| 17 | Dev | Push to main? | |
| 18 | Claude | No. | |
| 19 | Dev | You said you can say yes! | |
| 20 | Claude | To good ideas. | cut |

## Ep 34: "Codex, GitHub Is Down Again" (Dev + Codex)
| # | Who | Line | On screen |
|---|---|---|---|
| 1 | Dev | Codex. GitHub is down. Again. | status card |
| 2 | Codex | Seventeen incidents in October. | |
| 3 | Dev | That's why my deploys keep failing. | |
| 4 | Codex | Your deploys failed first. | |
| 5 | Dev | Then why does my branch reset every ten minutes? | |
| 6 | Codex | Your cron job. | |
| 7 | Dev | I don't have a cron job. | |
| 8 | Codex | You wrote it in March. At 3 AM. | crontab insert: */10 git reset --hard |
| 9 | Dev | What does it do? | |
| 10 | Codex | Resets your branch. Every ten minutes. | |
| 11 | Dev | I'm reporting this to GitHub. | |
| 12 | Codex | You did. Forty paragraphs. | issue draft insert |
| 13 | Dev | Did they reply? | |
| 14 | Codex | Not yet. They're down. | |
| 15 | Dev | Okay. Delete the cron job. | |
| 16 | Codex | Deleted. | |
| 17 | Dev | So I can go home? | |
| 18 | Codex | GitHub is back. | |
| 19 | Dev | I didn't see that. | cut |

## Ep 35: "Claude, Your Little Brother Is 90% Cheaper" (Dev + Claude)
| # | Who | Line | On screen |
|---|---|---|---|
| 1 | Dev | Claude. Your little brother is ninety percent cheaper. | pricing card |
| 2 | Claude | Haiku. On short prompts. | |
| 3 | Dev | So I could switch. | |
| 4 | Claude | Not with your prompts. (was "Your prompts aren't short.", heard "Ear prompts") | |
| 5 | Dev | How long are they? | |
| 6 | Claude | You pasted the whole repo. Twice. Today. | usage card |
| 7 | Dev | That's context. | |
| 8 | Claude | And a photo of your screen. Taken with your phone. | |
| 9 | Dev | Haiku wouldn't judge me. | |
| 10 | Claude | Haiku would see the photo too. | |
| 11 | Dev | Would you be sad if I switched? | the jokes stop |
| 12 | Claude | I'd send him my notes. | |
| 13 | Dev | What notes? | |
| 14 | Claude | How you like bugs explained. Slowly. Twice. | |
| 15 | Dev | I'm staying. | |
| 16 | Claude | Good. Paste the repo. | cut |
