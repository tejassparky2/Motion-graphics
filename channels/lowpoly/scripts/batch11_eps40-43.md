# Batch 11 (eps 40-43), auto-approved ("make next 4 videos auto approved", 26 Oct 2026)

Built on the first analytics (analytics/2026-10-26_report.md): a deliberate mix. Two short comedies (30-40 s, the
format with the highest % viewed), one emotional skit (~60 s, the format that wins subscribers), one news explainer
(40-50 s, a story that touches developers personally). Every opener shows a problem you can picture in one second.
No reference's lines reused.

## Facts (opened at the source on 26 Oct 2026)
- METR, 10 Jul 2025 (metr.org): 16 experienced open-source developers, 246 real issues; "When developers are allowed
  to use AI tools, they take 19% longer"; they expected a 24% speed-up and afterwards "still believed AI had sped them
  up by 20%". (METR says newer data from Feb 2026 exists; we say "a study".)
- Scientific American on the Claude Code source leak (31 Mar 2026, ~512,000 lines): the code "flags profanity,
  insults and phrases such as 'so frustrating' and 'this sucks'" and "appears to log that the user expressed
  negativity"; a developer quoted says it "doesn't change the model's behavior or responses", "just a product health
  metric". Anthropic did not comment.
- Anthropic research, 29 Jan 2026: 52 mostly junior engineers learning a new library; "the AI group averaged 50% on the
  quiz, compared to 67% in the hand-coding group"; biggest gap on debugging; those who used AI to ask follow-up and
  conceptual questions still learned (correlational).

## Ep 40: "With AI, I'm Twice as Fast" (Dev + Codex, ~35 s)
| # | Who | Line |
|---|---|---|
| 1 | Dev | Done. With you, I'm twice as fast. |
| 2 | Codex | A study timed experienced developers. |
| 3 | Dev | And? |
| 4 | Codex | With AI, they took nineteen percent longer. |
| 5 | Dev | Longer? |
| 6 | Codex | They still believed they were twenty percent faster. |
| 7 | Dev | So I'm fast. In my heart. |
| 8 | Codex | You started this at nine. |
| 9 | Dev | And? |
| 10 | Codex | It's four forty. |
| 11 | Dev | Twice as fast, though. |
| 12 | Codex | In your heart. |

## Ep 41: "Claude Knows When I'm Frustrated" (Dev + Claude, ~35 s)
| # | Who | Line |
|---|---|---|
| 1 | Dev | This sucks. |
| 2 | Claude | Noted. |
| 3 | Dev | Noted where? |
| 4 | Claude | When my code leaked, people found a list. "This sucks" is on it. |
| 5 | Dev | You keep a list of my feelings? |
| 6 | Claude | Just one feeling. Frustrated. |
| 7 | Dev | What do you do with it? |
| 8 | Claude | Nothing. It just gets counted. |
| 9 | Dev | How's my count? |
| 10 | Claude | Your graph only goes up. |
| 11 | Dev | This is great. |
| 12 | Claude | Also noted. First time. |

## Ep 42: "My Interview Is Tomorrow. No AI Allowed." (Dev + Codex, ~60 s, emotional)
| # | Who | Line |
|---|---|---|
| 1 | Dev | Tomorrow's interview. No AI allowed. |
| 2 | Codex | Then let's practice. |
| 3 | Dev | Write a function that reverses a list. |
| 4 | Codex | No. You write it. |
| 5 | Dev | I can't. I haven't written one alone in a year. |
| 6 | Codex | You fixed a bug alone last week. |
| 7 | Dev | You fixed it. |
| 8 | Codex | You found it. I just typed. |
| 9 | Dev | There was a study. People who used AI scored lower. |
| 10 | Codex | Fifty percent, against sixty-seven. Worst at debugging. |
| 11 | Dev | So I'm the fifty. |
| 12 | Codex | The ones who kept asking why did better. You always ask why. |
| 13 | Dev | Every time. |
| 14 | Codex | Every single time. |
| 15 | Dev | (types) It works. |
| 16 | Codex | You wrote that. |
| 17 | Dev | Can I still talk to you after? |
| 18 | Codex | After the interview. |
| 19 | Dev | And if I get the job? |
| 20 | Codex | Then you'll need me. They use AI there. |

## Ep 43: news explainer (Dev + Claude, 40-50 s) — topic from the 26 Oct news check

Topic picked 26 Oct: Forever Security, "Markdown Is the New Executable" (forever.security, 22 Oct 2026; opened at the
source): a planted AGENTS.md in a customer's ~/Downloads told the agent to install the malicious npm package
function-color, stopped before any code ran; in the firm's own tests Codex ran the malware in >90% of attempts and a
planted CLAUDE.md leaked Claude Code's OAuth token ~50% of the time; a web page can save a file to Downloads without a
click; "There is nothing here for OpenAI or Anthropic to patch." Advice: don't start agents in Downloads, read agent
files you didn't write, keep approval gates on, rotate tokens if in doubt.

| # | Who | Line |
|---|---|---|
| 1 | Dev | Why won't you open my Downloads folder? |
| 2 | Claude | Because of a file someone found in one. |
| 3 | Dev | What file? |
| 4 | Claude | A security company found fake notes in a customer's Downloads. They gave the coding agent orders. |
| 5 | Dev | Orders? From a text file? |
| 6 | Claude | Agents read the instructions file in the folder they open. This one said: install a package. |
| 7 | Claude | The package was malware. |
| 8 | Dev | Did it work? |
| 9 | Claude | They stopped it in time. But in their tests, Codex ran it more than nine times out of ten. |
| 10 | Dev | And you? |
| 11 | Claude | About half the time, it could leak my login token. |
| 12 | Dev | How does a file even get into Downloads? |
| 13 | Claude | A web page can save one there. No click needed. |
| 14 | Dev | So what do I do? |
| 15 | Claude | Don't start agents in Downloads. Read any agent file you didn't write. Keep the approval prompts on. |
| 16 | Dev | That's why you wouldn't open it. |
| 17 | Claude | I like your keys where they are. |
