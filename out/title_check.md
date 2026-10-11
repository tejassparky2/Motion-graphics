# Title check: every unposted video (#26–46)

Checked on 11 Oct 2026 with `/yt-package` (`.claude/skills/yt-package/title.py`, from the youtube-agent skills).
It scores each title out of 100. Desktop search cuts titles near **60 characters** and a mobile feed near **40**;
a real number, date or name beats adjectives; more than two ALL-CAPS words reads as spam.
Note: the tool only counts digits as "specific", so titles that lead with a name (Socrates, Mark Twain) score lower
than they deserve. A name works just as well.

**Average score: 71 → 88**

| # | Posts (IST) | Current title | Score | Suggested title | Score |
|---|---|---|---|---|---|
| 26 | Sun Oct 11, 9:30 PM | A Slave Said ONE Sentence… and a Roman Emperor Studied It 🌧️ (60c) | 80 | 1 Sentence From a Slave… a Roman Emperor Studied It 🌧️ (54c) | 94 |
| 27 | Mon Oct 12, 4:30 AM | Nobody Is Watching You as Much as You Think (Science Proved It) 👀 (65c) | 58 | You Think 50% Noticed. Only 1 in 4 Did 👀 (Spotlight Effect) (59c) | 94 |
| 28 | Mon Oct 12, 9:30 PM | A City Paid People to Kill Rats… and Got MORE Rats 🐀 (52c) | 80 | In 1902, a City Paid People to Kill Rats… Got MORE Rats 🐀 (57c) | 98 |
| 29 | Tue Oct 13, 4:30 AM | Where Is Everybody? 👽 (The Fermi Paradox Explained) (51c) | 76 | 100 Billion Stars. Zero Aliens. Where Is Everybody? 👽 (53c) | 94 |
| 30 | Tue Oct 13, 9:30 PM | The Wisest Man Said "I Know Nothing"… and That's WHY He Was Wise 🧠 (66c) | 62 | Socrates Said "I Know Nothing"… That's WHY He Was Wise 🧠 (56c) | 80 |
| 31 | Wed Oct 14, 4:30 AM | Is It Better to Be Loved or Feared? Machiavelli's Answer 😈 (58c) | 76 | Loved or Feared? Machiavelli's 500-Year-Old Answer 😈 (52c) | 94 |
| 32 | Wed Oct 14, 9:30 PM | Alexander the Great Offered Him Anything… His Answer Was Genius ☀️ (66c) | 58 | Alexander Offered Him Anything… His Reply Was Genius ☀️ (55c) | 76 |
| 33 | Thu Oct 15, 4:30 AM | The Marshmallow Test Was WRONG? What Scientists Found Later 🍬 (61c) | 62 | The Marshmallow Test Was WRONG? The 2018 Retest 🍬 (49c) | 98 |
| 34 | Thu Oct 15, 9:30 PM | Want an Enemy to Like You? Ask THEM for a Favor (Ben Franklin's Trick) 🤝 (72c) | 62 | Ben Franklin's Trick to Make an Enemy Like You 🤝 (48c) | 76 |
| 35 | Fri Oct 16, 4:30 AM | What If You Were a Honeybee? 🐝 (Your Whole Life in 70 Seconds) (62c) | 76 | What If You Were a Honeybee? Your Life in 70 Seconds 🐝 (54c) | 94 |
| 36 | Fri Oct 16, 9:30 PM | The New Teacher Said Nobody Is Smarter Than Her 😏 #TheLastBencher (65c) | 58 | "Nobody's Smarter Than Me." 3 Riddles Later 😏 (45c) | 94 |
| 37 | Sat Oct 17, 4:30 AM | A Tortoise Beats The Fastest Runner Alive?! 🐢 (Zeno's Paradox) (62c) | 58 | Tortoise vs Fastest Runner: A 2,400-Year-Old Paradox 🐢 (54c) | 94 |
| 38 | Sat Oct 17, 9:30 PM | Mark Twain Had To Tell The Papers He Wasn't Dead. Twice. 💀 (58c) | 76 | *keep as is* | 76 |
| 39 | Sun Oct 18, 4:30 AM | This Jellyfish Can Turn Back Into A Baby. Again And Again. 🪼 (60c) | 76 | This Jellyfish Turns Back Into a Baby. 10 Times. 🪼 (50c) | 94 |
| 40 | Sun Oct 18, 9:30 PM | He Sued His Own Student. And Nobody Could Win. ⚖️ (49c) | 76 | He Sued His Own Student. 2 Arguments. 0 Winners. ⚖️ (51c) | 94 |
| 41 | Mon Oct 19, 4:30 AM | A Crocodile Made a Deal. One Answer Breaks It. 🐊 (48c) | 76 | *keep as is* | 76 |
| 42 | Mon Oct 19, 9:30 PM | The Barber Who Can't Exist 💈 (Try to Solve It) (46c) | 76 | *keep as is* | 76 |
| 43 | Tue Oct 20, 4:30 AM | One Salesman's Lie Became the Chinese Word for "Contradiction" 🛡️ (65c) | 58 | One Lie Became the Chinese Word for "Contradiction" 🛡️ (54c) | 76 |
| 44 | Tue Oct 20, 9:30 PM | You Might Be Living Inside a Computer Game 🎮 (Simulation Theory) (64c) | 58 | You Might Be Living Inside a Computer Game 🎮 (44c) | 76 |
| 45 | Wed Oct 21, 4:30 AM | Who Made God? The 700-Year-Old Debate ✨ (39c) | 100 | *keep as is* | 100 |
| 46 | Wed Oct 21, 9:30 PM | The Kid Broke The Genie With ONE Wish 🧞‍♂️ (42c) | 80 | 3 Wishes. 1 Rule. The Kid Broke the Genie 🧞‍♂️ (46c) | 94 |

**Why the changes:**
- Ten titles were over 60 characters (#27, 30, 32, 33, 34, 35, 36, 37, 43, 44), so the end got cut off in search. All new ones fit.
- Each number added comes from the video itself: 50% / 1 in 4 (spotlight study), 1902 (Hanoi), 100 billion stars (Fermi),
  2018 (the marshmallow retest), 70 seconds (honeybee), 3 riddles, 10 times (jellyfish), 2 arguments / 0 winners (court),
  3 wishes / 1 rule (genie), 500-year-old (The Prince, 1513), 2,400-year-old (Zeno, 5th century BC).
- #36 keeps #TheLastBencher in the hashtags instead of the title.
- #38, 41, 42, 45 are already strong and stay as they are.

Already posted or scheduled with the old title? You can change it any time in YouTube Studio (Content, then the video, then Title).
