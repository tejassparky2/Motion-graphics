# Game-theory and behavioral-economics building blocks for original death games

Scope: classic strategic structures as raw material for ORIGINAL games. For each one: the setup, the trap, how real people behave, and how fiction has used it. Each fact carries a source. Anything I could not verify in this session is marked **[unverified]** or listed under Gaps. Rule paragraphs written for viewers and the "why it's brutal" notes are my own design commentary, marked *(inference)*.

---

## Q1. For each structure: the cleanest one-minute rule set, and what makes it psychologically brutal (with fiction uses)

### Takeaway
About 27 structures fall into five families: **trust/defection** (PD, public goods, commons, trust, ultimatum/dictator, volunteer, stag hunt), **out-guessing the crowd** (beauty contest, minority/El Farol, unique-bid), **escalation** (dollar/all-pay auction, chicken, sunk cost), **knowledge and logic** (blue-eyed islanders, two generals, hats, 100 prisoners, Monty Hall, Newcomb, pirate game), and **moral or social pressure** (trolley, bystander, hidden roles, cheap talk). Death-game fiction (Liar Game, Kaiji, Alice in Borderland, Squid Game, The Genius, Tomodachi Game) has already used several of them almost directly, so original games should **combine or re-skin** them rather than copy any one.

### Cited Findings

#### A. Trust and defection family

**1. Prisoner's dilemma (one-shot) and Split or Steal**
- Real-money version from the TV show Golden Balls: if both choose split they share the jackpot; if one steals and the other splits, the stealer takes everything; if both steal, both get nothing. ([van den Assem, van Dolder & Thaler 2012, *Management Science* 58(1)](https://repub.eur.nl/pub/31292/SplitorSteal_2012.pdf))
- The Golden Balls version is a "weak" PD: stealing never does worse than splitting, but steal/steal pays the same as being robbed (zero). This is why "I will steal, then share with you afterwards" threats are possible (the Chicken article cites a televised Golden Balls final where one contestant's stated intent to steal ended with both choosing split). ([Wikipedia: Chicken (game)](https://en.wikipedia.org/wiki/Chicken_(game)))
- Fiction: Liar Game's whole tournament uses this "lie or be lied to" logic, and Akiyama's cooperative counter-plans are covered under Q3. ([Wikipedia: Liar Game](https://en.wikipedia.org/wiki/Liar_Game))
- *Why brutal (inference):* the decision is simultaneous and final. The worst outcome is not losing but being the honest one who got robbed in public.

**2. Iterated PD, tit-for-tat and Axelrod's tournaments**
- Axelrod ran computer tournaments. In the first round, 14 entries played a round robin, and the simplest program, TIT FOR TAT (cooperate first, then copy the opponent's last move), submitted by Anatol Rapoport, won. 8 of the 14 programs were "nice" (never defect first), and every nice rule outperformed the 6 not-nice ones. ([Axelrod library: overview of past tournaments](https://axelrod.readthedocs.io/en/latest/discussion/overview_of_past_tournaments.html); [Axelrod quote, *The Evolution of Cooperation*](https://www.goodreads.com/quotes/7062124-in-fact-the-fourteen-programs-submitted-in-the-first-round); [Axelrod 1980, *J. Conflict Resolution* 24(3)](https://ideas.repec.org/a/sae/jocore/v24y1980i3p379-403.html))
- The second round drew 62 entries from six countries, whose authors knew the first-round results, and TIT FOR TAT won again. One arXiv paper gives 64 entries; Axelrod's own count is 62. ([Axelrod library](https://axelrod.readthedocs.io/en/latest/discussion/overview_of_past_tournaments.html))
- *Design lever (inference):* a known last round makes cooperation unravel (backward induction). An unknown number of rounds ("the game ends when the bell rings") keeps the shadow of the future and makes tit-for-tat viable. Revealing the last round mid-game is a cruel twist.

**3. Public goods game (with and without punishment)**
- Rules: each of n players gets an endowment M and secretly puts g into a pot. The pot is multiplied by a factor greater than 1 but smaller than n and shared equally. Contributing 0 is the individually best move (Nash), while everyone contributing everything is the group optimum. ([Wikipedia: Public goods game](https://en.wikipedia.org/wiki/Public_goods_game))
- Fehr & Gächter added a stage where players can pay to fine others. Their study of costly punishment in humans is *Nature* 2002 ("Altruistic punishment in humans"). ([IDEAS listing, *Nature* 415:137](https://ideas.repec.org/a/nat/nature/v415y2002i6868d10.1038_415137a.html))
- Antisocial punishment: across 16 subject pools in 15 countries (1,120 participants), some groups punished *high* contributors about as much as free riders, enough to cancel punishment's benefit. Weak civic norms and weak rule of law predicted it. ([Herrmann, Thöni & Gächter 2008, *Science* 319](https://www.umass.edu/preferen/You%20Must%20Read%20This/herrmann-thoni-gachter.pdf))
- *Why brutal (inference):* the "sucker" is visible after each round, and the punishment option turns the room into a court in which do-gooders can also be punished.

**4. Tragedy of the commons (common-pool resource)**
- Ostrom, Walker & Gardner (1992) tested in the lab whether resource users can make credible commitments without an outside enforcer: communication alone, sanctioning alone, and both together ("covenants with and without a sword"). Their thesis is that self-governance is possible. ([Ostrom, Walker & Gardner 1992, *APSR* 86(2)](https://econpapers.repec.org/article/cupapsrev/v_3a86_3ay_3a1992_3ai_3a02_3ap_3a404-417_5f08.htm))
- Pointer: Hardin, "The Tragedy of the Commons," *Science* 162:1243 (1968) ([DOI](https://doi.org/10.1126/science.162.3859.1243)); not re-read in this session.
- *Game skin (inference):* a shared oxygen tank, a refilling water tank, a bank of "lives" that regrows only if total withdrawals stay under a threshold.

**5. Trust (investment) game, Berg, Dickhaut & McCabe 1995**
- Rules: the trustor sends any part of a $10 endowment, the amount is tripled, and the trustee decides how much to send back. The subgame-perfect prediction is "no trust" (send 0), but experiments rarely end there. ([Wikipedia: Trust game](https://en.wikipedia.org/wiki/Trust_game); [Berg et al. 1995, *Games and Economic Behavior*, doi:10.1006/game.1995.1027](https://en.wikipedia.org/wiki/Trust_game))
- *Why brutal (inference):* the decision isn't symmetric. One person makes themselves vulnerable first, and the other then sees exactly how much power they were given.

**6. Ultimatum and dictator games**
- Ultimatum: a proposer offers a split; the responder accepts (split happens) or rejects (both get nothing). First described by Harsanyi (1961); the classic experiment is Güth, Schmittberger & Schwarze (1982). ([Wikipedia: Ultimatum game](https://en.wikipedia.org/wiki/Ultimatum_game))
- Dictator: the same, but the responder cannot reject. Over 100 dictator experiments were published in 25 years and are summarized by Engel's meta-study. ([Engel 2011, *Experimental Economics*](https://www.cambridge.org/core/journals/experimental-economics/article/abs/dictator-games-a-meta-study/8597E66280017C3A83863C12A7F8F687))
- *Death-game skin (inference):* "You choose how many of the 10 antidote doses your partner gets. If they refuse, nobody gets any." Rejection becomes spite at the cost of one's own life, which is the brutal part.

**7. Volunteer's dilemma**
- Rules: if at least one player volunteers (pays a cost), everyone benefits; if nobody does, everyone gets the worst outcome. The volunteer gets no extra benefit, so each player hopes someone else will do it. With two players it resembles chicken. In the mixed equilibrium, adding players lowers the chance that anyone volunteers. ([Wikipedia: Volunteer's dilemma](https://en.wikipedia.org/wiki/Volunteer%27s_dilemma))
- Theory origin: Diekmann (1985). Under that Nash analysis, the probability of no volunteer rises with group size. ([Kopányi-Peuker 2018, Tinbergen DP](https://papers.tinbergen.nl/18072.pdf))
- Fiction: the Squid Game glass bridge is a sequential volunteer's dilemma. Players pick their order numbers *before* they know the game, and whoever goes first reveals safe tiles (by dying) for those behind. ([arXiv 2409.05263](https://arxiv.org/pdf/2409.05263); [Chalkdust](https://chalkdustmagazine.com/features/surviving-the-bridge-in-squid-game/))

**8. Stag hunt / weakest-link coordination**
- Van Huyck, Battalio & Beil (1990), "Tacit Coordination Games, Strategic Uncertainty, and Coordination Failure," *AER* 80. In the minimum-effort game, payoff depends on your own effort and the group's *minimum* effort. Any common effort level is an equilibrium, and higher is better for all. The lab groups converged quickly to the most inefficient equilibrium. ([Crawford lecture notes, UCSD](https://econweb.ucsd.edu/~vcrawfor/LearnLockTalkNotes.pdf); [CERGE-EI WP 302](https://ei.cerge-ei.cz/pdf/wp/Wp302.pdf))
- *Why brutal (inference):* no one needs to be greedy for it to fail. Fear that *one* person is afraid is enough, so the weakest link sets everyone's fate.

#### B. Out-guess-the-crowd family

**9. Keynesian beauty contest / guess p × average**
- Rules: everyone picks a number from 0 to 100 at the same time, and the winner is closest to p times the average (p = 2/3 is the classic). The unique equilibrium is 0, reached by iterated elimination. About 21 levels of reasoning are needed to reach 0, and most people reason at levels 0 to 3. ([Wikipedia: Guess 2/3 of the average](https://en.wikipedia.org/wiki/Guess_2/3_of_the_average))
- Origin: Keynes, *General Theory* (1936), ch. 12, where judges try to pick the faces that average opinion expects average opinion to pick. ([Wikipedia: Keynesian beauty contest](https://en.wikipedia.org/wiki/Keynesian_beauty_contest))
- Fiction (near-direct use): Alice in Borderland's **King of Diamonds** game. Pick 0 to 100; the average × 0.8 is the target; closest wins; each lost point adds acid to a scale above the player's head, and at −10 the scale tips and the acid kills them. The manga calls it "Beauty Contest," Netflix "Balance Scale," and the character Asuma names the Keynesian beauty contest on screen. ([AiB wiki: Diamonds](https://aliceinborderland.fandom.com/wiki/Diamonds); [GIPE analysis](https://gipe.ac.in/the-king-of-diamonds-a-dissected-gameplay-of-balance-scales/))
- → **Do not reuse a plain p-beauty contest; it is the most recognisable death-game borrowing.**

**10. Minority game and the El Farol bar problem**
- El Farol (Arthur 1994): each week a population decides whether to go to a bar. Below 60% attendance, those who go have more fun than those who stay home; above 60%, they have less. If everyone uses the same deterministic rule, it always fails: predict "quiet" and everyone goes; predict "crowded" and no one does. ([Wikipedia: El Farol Bar problem](https://en.wikipedia.org/wiki/El_Farol_Bar_problem); [Arthur 1994, *AER P&P* 84:406](https://spf.pt/magazines/GFIS/65/article/352/pdf))
- Minority game (Challet & Zhang 1997, *Physica A* 246:407): the side chosen by the minority wins, so both choices are symmetric. ([SPF article](https://spf.pt/magazines/GFIS/65/article/352/pdf); [Challet, Marsili & Zhang, *Minority Games*](https://arxiv.org/pdf/0811.1479))
- Fiction: Liar Game Round 2, "Minority Rule": yes/no questions, the largest group loses, and the smallest group goes on. ([Wikipedia: Liar Game](https://en.wikipedia.org/wiki/Liar_Game); [Substack analysis](https://eseoghene.substack.com/p/analysing-minority-rule)). A LessWrong comment links it to a theorem on when a coalition can guarantee a win, depending on whether its size is a multiple of the minority size. ([LessWrong](https://www.lesswrong.com/lw/oj4/a_majority_coalition_can_lose_a_symmetric_zerosum/dlwc))

**11. Unique-bid auctions (lowest/highest unique bid, LUPI)**
- Rules: the lowest (or highest) bid that *nobody else made* wins. Bidders can often place several bids, and bid counts are secret. LUPI (Lowest Unique Positive Integer) drops payment: pick the lowest number nobody else picks. Sweden's Svenska Spel ran it as "Limbo" (Jan–Mar 2007, about 50,000 players a day). ([Wikipedia: Unique bid auction](https://en.wikipedia.org/wiki/Unique_bid_auction); Östling et al. 2011, *AEJ: Micro*)
- *Why brutal (inference):* the "safe" choice (1, the lowest) is exactly the one everyone thinks of, so a tie means death. The best number is one that is obvious to you and invisible to everyone else.

#### C. Escalation family

**12. Dollar auction / all-pay auctions (Shubik 1971)**
- Rules: a $1 bill is auctioned; the highest bidder wins it, but the **second-highest bidder also pays** their bid and gets nothing. Bids go past $1 because each bidder is trying not to be second. ([Shubik 1971, *J. Conflict Resolution* 15(1):109–111 via Wikipedia: Dollar auction](https://en.wikipedia.org/wiki/Dollar_auction))
- Related: the war of attrition is an all-pay second-price auction (both pay the lower bid), the standard model for contests settled by endurance. ([Wikipedia: Chicken](https://en.wikipedia.org/wiki/Chicken_(game)))
- Classic book: Teger, *Too Much Invested to Quit* (Pergamon, 1980). ([MPRA paper 72608](https://mpra.ub.uni-muenchen.de/72608/1/MPRA_paper_72608.pdf))

**13. Chicken / brinkmanship / hawk–dove**
- Payoffs: if both swerve, both get 0; if one swerves, the swerver gets −1 and the other +1; if both go straight, both get −1000. Russell (1959) compared nuclear brinkmanship to it: "the moment will come when neither side can face the derisive cry of 'Chicken!'" ([Wikipedia: Chicken](https://en.wikipedia.org/wiki/Chicken_(game)); Russell, *Common Sense and Nuclear Warfare*, p. 30)
- Commitment trick: if one driver ostentatiously disables their steering wheel, the other must swerve (Kahn 1965, cited in Rapoport & Chammah 1966). Brinkmanship adds risk nobody controls, so catastrophe can happen even when everyone acts rationally (Dixit & Nalebuff 1991). ([Wikipedia: Chicken](https://en.wikipedia.org/wiki/Chicken_(game)))
- Iterated chicken can lead to turn-taking. ([Wikipedia: Chicken](https://en.wikipedia.org/wiki/Chicken_(game)))
- Fiction listed there: *Rebel Without a Cause* (the "chickie run"), *Footloose*, *Dr. Strangelove* (a doomsday deterrent announced too late to deter). ([Wikipedia: Chicken](https://en.wikipedia.org/wiki/Chicken_(game)))

**14. Sunk cost and escalation of commitment**
- Arkes & Blumer (1985) ski-trip study: subjects had paid $100 for a Michigan trip and then $50 for a Wisconsin trip on the same weekend that they were told they'd enjoy more; the tickets were non-refundable. Only 46% chose Wisconsin, so the majority went on the trip they would enjoy less because it cost more. ([Arkes & Blumer 1985](https://cognition.aau.at/bg/BA/Arkes%20%26%20Blumer%201985.pdf))
- Pointer: Staw (1976), "Knee-deep in the big muddy" [unverified in this session].

#### D. Knowledge, logic and prediction family

**15. Blue-eyed islanders (common knowledge)**
- Tao's version: 1,000 islanders, 100 blue-eyed, none allowed to learn their own eye colour; anyone who works it out must die at noon the next day. A visitor says publicly that it's unusual to see another blue-eyed person. One argument says this adds nothing, since everyone already sees blue eyes. The other argument, by induction, says all 100 blue-eyed islanders die on day 100. Tao leaves the resolution to the comments. ([Tao 2008 blog](https://terrytao.wordpress.com/2008/02/05/the-blue-eyed-islanders-puzzle/))
- Standard resolution (not confirmed on Tao's main page): the announcement turns mutual knowledge into *common* knowledge (everyone knows that everyone knows ...), which starts the induction clock. **[resolution text unverified in this session]**
- *Why brutal (inference):* one innocent public sentence kills, so the survival rule becomes "never say what everybody already knows."

**16. Two generals (coordination over an unreliable channel)**
- Two armies must attack together, and messengers may be captured. Any protocol that guarantees agreement still guarantees it with its last message deleted; repeat the deletion and you're left with zero messages, so no protocol can guarantee agreement. It was the first computer-communication problem proven unsolvable. It first appeared in Akkoyunlu, Ekanadham & Huber (1975) in a gangster framing; Gray (1978) named it. ([Wikipedia: Two Generals' Problem](https://en.wikipedia.org/wiki/Two_Generals%27_Problem); [Yale PineWiki](https://cs.yale.edu/homes/aspnes/pinewiki/TwoGenerals.html))
- *Death-game use (inference):* the "all survive" path requires one side to **act without the final confirmation**, which is a trust leap rather than a logic proof.

**17. Hat puzzles**
- Ten-prisoner line, guessing from the back: the back prisoner calls the parity of red hats, and **9 of 10 are guaranteed** to survive (the back one has a 50% chance). ([Wikipedia: Hat puzzle](https://en.wikipedia.org/wiki/Hat_puzzle))
- Ebert's three-player version (1998 thesis): guesses are simultaneous, and players may pass. If you see two different colours, pass; if you see two the same, guess the opposite. The team wins **75%** of the time instead of 50%, and Hamming codes extend this to 7/8 for 7 players. ([Wikipedia: Hat puzzle](https://en.wikipedia.org/wiki/Hat_puzzle); [Georgia Tech handout](https://barry.ece.gatech.edu/6602/handouts/hatcolor.pdf))
- Simultaneous guessing with no hearing: 5 of 10 guaranteed, by splitting into groups that assume opposite parities. ([Wikipedia: Hat puzzle](https://en.wikipedia.org/wiki/Hat_puzzle), uncited section)
- Fiction: Alice in Borderland **Jack of Hearts, "Solitary Confinement"**. Explosive collars show a suit only *others* can see; each round every player declares their own suit in a cell, and a wrong answer means death; a hidden "Jack" among them is trying to deceive the 19 real players. It combines a hat puzzle with a hidden-role game. ([AiB wiki: Jack of Hearts](https://aliceinborderland.fandom.com/wiki/Jack_of_Hearts))

**18. 100 prisoners (boxes) problem**
- 100 numbered prisoners, 100 boxes with shuffled numbers, and each may open 50. Everyone must find their own number or all die. Random search gives about (1/2)^100. The cycle-following strategy (open the box with your own number, then the box named inside, and so on) succeeds whenever no cycle is longer than 50: **about 31.18%** for 100 prisoners, tending to 1 − ln 2 ≈ 30.69%. It is optimal (Curtin & Warshauer 2006). Proposed by Gál & Miltersen (2003). ([Wikipedia: 100 prisoners problem](https://en.wikipedia.org/wiki/100_prisoners_problem))
- *Why it's ideal for this story (inference):* a hidden *coordination* strategy turns near-certain death into roughly a one-in-three group survival, and one prisoner who goes off-plan to "save time" breaks it for all.

**19. Monty Hall**
- Pick 1 of 3 doors; the host, who knows where the prize is, opens a losing door you didn't pick and offers a switch. Switching wins 2/3. (Standard result; see Granberg below for behaviour.)

**20. Newcomb's problem**
- A reliable predictor puts $1M in an opaque box only if it predicted you would take that box alone; a clear box holds $1,000. Take one box or both? ([Wikipedia: Newcomb's problem](https://en.wikipedia.org/wiki/Newcomb%27s_problem))
- *Death-game skin (inference):* "The Warden already sealed the poison based on what he predicted you'd do."

**21. Pirate game (Stewart 1999)**
- Five pirates ranked by seniority split 100 coins. The most senior proposes a split; if it fails the vote, the proposer is thrown overboard. Pirates are rational, want to survive first and gain coins second, and prefer throwing someone overboard when all else is equal. Backward induction gives **98, 0, 1, 0, 1**: the senior pirate buys the two cheapest votes. ([Wikipedia: Pirate game](https://en.wikipedia.org/wiki/Pirate_game); Stewart, "A Puzzle for Pirates," *Scientific American* 280(5):98–99, May 1999)
- The game changes character once there are more than twice as many pirates as coins. ([Wikipedia: Pirate game](https://en.wikipedia.org/wiki/Pirate_game))
- *Why brutal (inference):* the "fair" 20-20-20-20-20 split loses the vote. Pure logic produces a grotesquely unequal outcome, and the lowest-ranked players are bought for one coin.

#### E. Moral and social-pressure family

**22. Trolley problems and sacrifice dilemmas**
- Three variants, Switch, Loop and Footbridge, were tested on 70,000 people in 42 countries. ([Awad et al. 2020, *PNAS*](https://www.pnas.org/doi/10.1073/pnas.1911517117); [Daily Nous summary](https://dailynous.com/2020/01/22/learned-70000-responses-trolley-scenarios/))
- Fiction: the Squid Game glass bridge forces players to decide whether to push others forward (see #7).

**23. Bystander effect and diffusion of responsibility**
- Darley & Latané (1968) seizure study over an intercom. ([Themantic Education](https://www.themantic-education.com/ibpsych/?p=837))
- Caution: the Kitty Genovese story ("38 witnesses") was later found unfounded; using it as a simple parable has been criticised. ([Manning, Levine & Collins 2007, *Am. Psychologist*, via Wikipedia: Volunteer's dilemma](https://en.wikipedia.org/wiki/Volunteer%27s_dilemma))

**24. Cheap talk and credible commitment**
- In Golden Balls, the talk before the decision is free. About half (53%) of contestants made an explicit promise to split. ([van den Assem et al. 2012](https://repub.eur.nl/pub/31292/SplitorSteal_2012.pdf))
- Credible commitment: the burned steering wheel (#13). Self-binding cuts your own options to change what the other side does. ([Wikipedia: Chicken](https://en.wikipedia.org/wiki/Chicken_(game)))
- Fiction: Death Note's "Lind L. Tailor" broadcast. L airs a decoy claiming to be L, in the Kanto region only, and dares Kira to kill him. Kira's reaction reveals his location and his ability to kill without being present, which makes it a screening move. ([Death Note wiki: "The Game Begins"](https://deathnote.fandom.com/wiki/The_Game_Begins); [MAL: Lind L. Tailor](https://myanimelist.net/character/30944))

**25. Hidden-role / social deduction (Mafia, Werewolf)**
- Braverman, Etesami & Mossel (2008, *Annals of Applied Probability* 18(3):825–846): with optimal randomised play and no detective, mafia and civilians have comparable winning chances when the mafia number is about the **square root** of the number of players. A small hidden minority is enough. ([arXiv 0804.0071](https://arxiv.org/abs/0804.0071)). A follow-up by Erlin Yao argues the main theorem needed correcting but reaches the same √n conclusion; I saw this only in a search summary, not the paper **[unverified]**. Migdal reached the same √n result independently, also seen only in a search summary.
- Fiction: AiB Jack of Hearts (#17); Tomodachi Game, where one friend may be the traitor whose debt dragged the group in. ([ANN This Week in Anime](https://www.animenewsnetwork.com/this-week-in-anime/2022-05-05/.185340); [MyAnimeList](https://myanimelist.net/anime/50273))

#### F. Fiction cross-reference (what each series already used)
- **Liar Game** (Shinobu Kaitani, *Weekly Young Jump* 2005–2015; sequel *The Last Game* 2026; anime April 2026): Round 1 is a 30-day money-stealing game (keep what you steal, repay what's stolen); Round 2 Minority Rule; the Downsizing revival with ticket-trading votes; Round 3 Contraband (smugglers carry briefcases of cash, inspectors guess the amounts); revival games including 24-chamber Russian roulette betting, "Seventeen Poker," and "Stationary Roulette" (bluffing about which of four pockets holds the ball). ([Wikipedia: Liar Game](https://en.wikipedia.org/wiki/Liar_Game))
- **Kaiji**: *Restricted Rock Paper Scissors* (each player has 12 cards, 4 of each gesture, and 3 stars as currency; a market grows around cards and stars, and Kaiji tries to corner a card type) ([Kaiji wiki](https://kaiji.fandom.com/wiki/Restricted_Rock_Paper_Scissors?oldid=7305)); *E-Card* (Emperor beats Citizen, Citizen beats Slave, Slave beats Emperor; the Slave side is paid 5x) ([Kaiji wiki: E-Card](https://kaiji.fandom.com/wiki/E-Card?oldid=5026)); the *Brave Men Road* electrified steel-beam crossing. ([TV Tropes](https://www.tvtropes.org/pmwiki/pmwiki.php/NightmareFuel/Kaiji)). An arXiv paper on online card games names RRPS and E-Card as inspirations for its "semi-restricted" variants. ([arXiv 2106.11866](https://arxiv.org/pdf/2106.11866))
- **The Genius** (tvN, 4 seasons, 2013–2015): each episode has a Main Match and a Death Match. The Main Match winner gets garnets and a "token of life" (immunity), and the Main Match loser picks a Death Match opponent who holds no token. Example games: "1, 2, 3 Game" (compared to Kaiji's RRPS) and "Big Dinner" (predicting others' choices). ([Wikipedia: The Genius](https://en.wikipedia.org/wiki/The_Genius_(TV_series)); [TV Tropes](https://tvtropes.org/pmwiki/pmwiki.php/Series/TheGenius))
- **Squid Game**: S1 E2 consent-form clause 3, by which the games end if a majority votes to stop. The players vote to stop and go home, and most come back. S2 adds a vote after every game, with those who stop leaving with a share of the prize so far. ([Ready Steady Cut recap](https://readysteadycut.com/2021/09/17/squid-game-season-1-episode-2-recap-hell/); [Dexerto](https://www.dexerto.com/tv-movies/squid-game-season-2-voting-change-3015885))
- **Tomodachi Game**: the opening "Kokkuri-san" game asks the group true/false questions, and debt can be paid off, increased, or **offloaded onto a friend**. It tests whether friends trust each other more than they fear owing money. ([ANN](https://www.animenewsnetwork.com/this-week-in-anime/2022-05-05/.185340); [MyAnimeList](https://myanimelist.net/anime/50273))

### Inferences
- Combinations make original games: e.g., hat puzzle + hidden role (AiB already did this), beauty contest + all-pay cost, volunteer's dilemma + sequential reveal (the glass bridge). Fresh pairings still open: **100-prisoners cycle strategy + one traitor who can swap two box contents**; **pirate-game voting + public-goods pot**; **LUPI + cheap-talk alliances**; **two-generals signalling + chicken deadline**.
- What makes each brutal comes down to three dials: **visibility** (does the room see who betrayed?), **reversibility** (one-shot vs iterated), and **asymmetry** (who moves first or is more exposed: trustor, proposer, first on the bridge).
- The most "fiction-worn" structures (avoid as-is): p-beauty contest (AiB King of Diamonds), minority game (Liar Game), split/steal (Golden Balls), restricted RPS (Kaiji), glass bridge (Squid Game).

### Gaps
- No full per-game list for The Genius seasons; the fandom wiki for Liar Game was paywalled (HTTP 402).
- Exact Squid Game clause wording comes from recaps, not a transcript.
- I did not find a reliable source tying Death Note to formal game theory; only the Lind L. Tailor screening logic is sourced (fan wikis).

---

## Q2. What experiments say about how real people behave

### Takeaway
Real people cooperate far more than Nash predicts in one-shot dilemmas (around 50%), reason only 1–2 steps deep in guessing games, overbid badly in escalation auctions, reject "insulting" offers at their own cost, and lean heavily on promises. They keep cooperating if they can punish cheats, but punishment can turn antisocial. These deviations are the engine of believable characters.

### Cited Findings

**Prisoner's dilemma / Split or Steal (real stakes)**
- Golden Balls (UK, 2007–2009), 574 finalists across 287 episodes: **52.8%** chose split; both split in **31%** of shows, one split and one stole in **44%**, both stole in **25%**. The jackpot was paid out in 75% of shows. Mean prize £4,851, median only £39, because **47% of finalists left with nothing**. ([van den Assem, van Dolder & Thaler 2012](https://repub.eur.nl/pub/31292/SplitorSteal_2012.pdf))
- The "big peanuts" effect: for jackpots up to £500, **73.4%** split; the rate falls to about **45%** at larger stakes and stays flat above about £1,500. ([same](https://repub.eur.nl/pub/31292/SplitorSteal_2012.pdf))
- The largest jackpot (£100,150, March 2008) was stolen entirely by one contestant from the other. ([same](https://repub.eur.nl/pub/31292/SplitorSteal_2012.pdf))
- The 53% cooperation rate is "remarkably similar" to earlier lab evidence (Sally 1995 meta-analysis, experiments 1958–1992). ([same](https://repub.eur.nl/pub/31292/SplitorSteal_2012.pdf); [Sally 1995, *Rationality and Society*](https://ideas.repec.org/a/sae/ratsoc/v7y1995i1p58-92.html))
- Lying is common before the final: 41% of finalists lied about their hidden balls in round 1 and 36% in round 2; in round 1, 24% overstated a cash ball and 21% hid a "killer" ball. ([same](https://repub.eur.nl/pub/31292/SplitorSteal_2012.pdf))

**Iterated PD**
- TIT FOR TAT won both Axelrod tournaments (14 and 62 entries); "nice" strategies outperformed "not nice" ones in round one. ([Axelrod library](https://axelrod.readthedocs.io/en/latest/discussion/overview_of_past_tournaments.html))

**Communication / cheap talk**
- A meta-analysis of 45 effect sizes found that communication strongly increases cooperation in social dilemmas (**d = 1.01**). Face-to-face (d = 1.21) works better than written (d = 0.46), the effect is larger in bigger groups, and timing doesn't matter. ([Balliet 2010, *J. Conflict Resolution* 54(1)](https://ideas.repec.org/a/sae/jocore/v54y2010i1p39-57.html))
- In Golden Balls, contestants who made an explicit promise to split were **about 31 percentage points more likely** to split, and a promise was the single most reliable predictor. **But** players whose *opponent* promised were not more likely to split; the effect was even marginally negative. Promises predict the promiser, but listeners don't use them. ([van den Assem et al. 2012](https://repub.eur.nl/pub/31292/SplitorSteal_2012.pdf))
- Revenge is real: a contestant's likelihood of splitting "plummets by approximately 21 percentage points if this opponent has voted against her earlier in the game" (p = 0.0195). ([same](https://repub.eur.nl/pub/31292/SplitorSteal_2012.pdf))

**Public goods and punishment**
- Without punishment, contributions decay to low levels, with **53–75% of subjects free riding completely** in the final period. With punishment, average contributions are held at **50–95%** of the endowment. In one treatment, 82.5% contributed everything in the final period. ([Fehr & Gächter, CESifo WP 183](https://www.cesifo.org/DocDL/ces_wp183.pdf); AER 2000 version)
- Multiplier matters: with 40 players, a factor of 1.03 led to almost no contributions after a few rounds, while 1.3 produced about 50% of the endowment. ([Wikipedia: Public goods game](https://en.wikipedia.org/wiki/Public_goods_game))
- Antisocial punishment cancels punishment's benefit in some societies. ([Herrmann, Thöni & Gächter 2008](https://www.umass.edu/preferen/You%20Must%20Read%20This/herrmann-thoni-gachter.pdf))
- Commonly quoted figure that first-round contributions start at 40–60% of the endowment: **[unverified in this session]**.

**Trust game**
- Berg et al. 1995: **30 of 32** trustors sent money; average sent **$5.16** of $10. ([Futility Closet](https://www.futilitycloset.com/2021/11/11/the-trust-game/); [GSU EconPort](https://econport.gsu.edu/content/handbook/trustreciprocity/experiments/TRSHistory.html))
- Returns: the GSU handbook (via search snippet) gives average payback as $4.56, i.e. **slightly less than was sent**, so trusting lost money on average. A UCSD lecture slide says about 90% of trustees returned something and "player 1 loses money on average." The 90% figure has no primary confirmation here. ([UCSD slides](https://econweb.ucsd.edu/~jandreon/182/TrustLect1ug.pdf)) **[exact return figure conflicts across secondary sources: $4.56 vs. the often-quoted $4.66]**
- Meta-analysis of 84 replications in 29 countries: about 40% of the variance in trust and 30% in trustworthiness is explained by protocol differences. ([Johnson & Mislin 2011, *J. Econ. Psych.* 32(5)](https://ideas.repec.org:443/a/eee/joepsy/v32y2011i5p865-889.html))

**Ultimatum and dictator**
- Meta-analysis of 37 papers: proposers offer about **40%** on average, and about **16%** of offers are rejected. Rejection falls as the pie grows and as the offered share rises. ([Oosterbeek, Sloof & van de Kuilen 2004](https://econwpa.ub.uni-muenchen.de/econ-wp/exp/papers/0401/0401003.pdf))
- Offers under about 20% are rejected about half the time; proposers typically offer 40–45%. ([JEPS article](https://jeps.efpsa.org/articles/17)). The equal split is often the modal and median offer. ([Bonn BGSE DP 22/2004, citing Camerer 2003](https://www.wiwi.uni-bonn.de/bgsepapers/old%20series/bonedp/bgse22_2004.pdf))
- High stakes: in a US$100 game in Indonesia, $30 offers (about two weeks' wages) were still rejected. With stakes up to 40 weeks' wages in India, "as stakes increase, rejection rates approach zero" (Andersen et al. 2011). ([Wikipedia: Ultimatum game](https://en.wikipedia.org/wiki/Ultimatum_game))
- Anonymity: Nash-consistent outcomes rose from 30% to 46% with more anonymity, and to nearly 100% when the responder could not punish (Bolton & Zwick 1995). ([Wikipedia: Ultimatum game](https://en.wikipedia.org/wiki/Ultimatum_game))
- Across 15 small-scale societies (Henrich et al. 2005), norms differ: in gift-giving cultures, *high* offers were rejected more often. ([Wikipedia: Ultimatum game](https://en.wikipedia.org/wiki/Ultimatum_game))
- Dictator average giving (often quoted as about 28% from Engel 2011): **[unverified; abstract does not state it]** ([Engel 2011](https://www.cambridge.org/core/journals/experimental-economics/article/abs/dictator-games-a-meta-study/8597E66280017C3A83863C12A7F8F687))

**Beauty contest / levels of reasoning**
- Nagel 1995 design: 15–18 subjects per session, 4 rounds, p = 1/2, 2/3 or 4/3, winner paid 20 DM per round, prize split among ties. ([Nagel 1995, *AER* 85(5):1313–1326](https://extranet.parisschoolofeconomics.eu/docs/guesnerie-roger/nagel95.pdf))
- First-round means: **36.73** (p = 2/3), **27.05** (median 17, p = 1/2), **60.12** (median 66, p = 4/3). In the p = 2/3 sessions the winning number was about 25, sitting at "iteration step 2" with about 25% of choices; almost 50% of choices were near step 1 or step 2, and only **6–10%** were at step 3 or above. Almost no one chose 0 in round 1; only 6% chose below 10. ([Nagel 1995](https://extranet.parisschoolofeconomics.eu/docs/guesnerie-roger/nagel95.pdf); my reading of a scanned PDF, so some panel labels are OCR-garbled)
- Learning: choices fall each round. In the p = 1/2 sessions more than half the choices were below 1 by round 4, yet only 3 of 48 chose exactly 0. With p = 4/3, 100 was chosen by 16%, 59% and 68% of subjects in rounds 2, 3 and 4. ([Nagel 1995](https://extranet.parisschoolofeconomics.eu/docs/guesnerie-roger/nagel95.pdf))
- Danish newspaper *Politiken* (2005): 19,196 entrants, average guess 33. ([Wikipedia](https://en.wikipedia.org/wiki/Guess_2/3_of_the_average)). Thaler's 1997 *Financial Times* contest: **[unverified in this session]**.
- A class mean of 23.5 compared with 36.7 in Nagel's sample shows populations differ. ([Mark Dean lecture slides, Columbia](https://www.columbia.edu/~md3405/Behave_Bounded_5_17.pdf))
- NPR *Planet Money* (2011): asked to pick the cutest animal video, 50% chose the kitten; asked what *most people* would choose, 76% chose the kitten. Second-guessing converges on focal points. ([Wikipedia: Keynesian beauty contest](https://en.wikipedia.org/wiki/Keynesian_beauty_contest))

**Unique-bid / LUPI**
- In Swedish Limbo, players quickly stopped choosing high numbers that hadn't won, and an early excess of very low numbers faded, but choices never spread as high as Nash predicts. A level-k mixture model fit well. Players chose birth years and avoided even or round numbers in favour of odd or prime ones. With N = 100, the Nash cutoff means no one should pick above 31. ([Wikipedia: Unique bid auction](https://en.wikipedia.org/wiki/Unique_bid_auction), citing Östling et al. 2011)
- Real auctions of about 200 players matched the Nash distribution "strikingly"; in auctions of over 2,000 players, some mid-range bids won more than 10x as often as Nash predicts, so crowds leave exploitable holes. ([same](https://en.wikipedia.org/wiki/Unique_bid_auction), citing Pigolotti et al. 2012)

**Dollar auction / escalation**
- Bazerman's $20-bill auctions to MBA students reportedly reached a **record winning bid of $204**. Sources are secondary (Patch, Inomics, forum). ([Patch](https://patch.com/illinois/highlandpark/bp--20-and-a-havard-mba); [Inomics](https://inomics.com/fr/blog/can-you-sell-a-20-bill-for-200-52378))
- Murnighan (2002), as cited by Morone et al.: a class where the winner paid $54 for a $20 bill, and more extreme classes where it went to $2,000. Groups bid closer to Nash than individuals, and experience reduces escalation. ([Morone, Nuzzo & Caferra, MPRA 72608](https://mpra.ub.uni-muenchen.de/72608/1/MPRA_paper_72608.pdf))
- An informal claim that "these games routinely end with the winning bid being 50 percent higher than the value." ([Freakonomics 2008](https://freakonomics.com/2008/12/16/an-all-pay-auction/))
- Field data: in penny auctions for straight cash prizes, average revenue was **204% of face value**. ([Augenblick 2015, *Review of Economic Studies*](https://kylewoodward.com/blog-data/pdfs/references/augenblick-the-review-of-economic-studies-2015A.pdf))
- Hafenbrädl: people with direct prior experience of competitive escalation did better in the dollar auction. ([IESE Insight](https://www.iese.edu/insight/articles/not-lose-head-bidding-war))

**Coordination / stag hunt**
- Minimum-effort groups converged quickly to the *worst* equilibrium (Van Huyck et al. 1990). Smaller groups, entry fees and money-back guarantees were later tested as fixes. ([Crawford notes](https://econweb.ucsd.edu/~vcrawfor/LearnLockTalkNotes.pdf); [CERGE-EI WP 302](https://ei.cerge-ei.cz/pdf/wp/Wp302.pdf))

**Volunteer's dilemma / bystander**
- Darley & Latané 1968: **85%** of those who believed they were the only listener helped within 2 minutes (100% by 6 minutes), against **31%** by 2 minutes (62% by 6) when they believed four others heard. With one other bystander, figures are 62–64% depending on the source. ([Themantic Education](https://www.themantic-education.com/ibpsych/?p=837); [Save My Exams](https://savemyexams.com/dp/psychology/ib/17/hl/revision-notes/human-relationships/social-responsibility-bystanderism-and-prosocial-behaviour/two-key-studies-of-bystanderism))
- Counter-evidence from CCTV of **219 real public conflicts** (UK, Netherlands, South Africa): at least one bystander intervened in about **9 of 10** (press release: 91%), and more bystanders made intervention *more* likely. ([Philpot et al. 2020, *Am. Psychologist*, Lancaster release](https://lancaster.ac.uk/news/bystanders-will-intervene-to-help-victims-of-aggressive-public-disputes); [PDF](https://gwern.net/doc/crime/2020-philpot.pdf))
- One-shot volunteer's-dilemma lab (203 subjects): volunteering did **not** fall steadily as group size grew. ([Kopányi-Peuker 2018](https://papers.tinbergen.nl/18072.pdf)). Field experiment with more than 2,000 remote workers: willingness to volunteer didn't change with team size. ([Southampton](https://eprints.soton.ac.uk/505956/1/willingness-to-volunteer-among-remote-workers-is-insensitive-to-the-team-size.pdf))

**Monty Hall**
- On first encounter only **12%** switch; over repeated trials switching rises to 55%. ([Granberg & Brown 1995, *Personality and Social Psychology Bulletin*](https://journals.sagepub.com/doi/10.1177/0146167295217006); abstract only)

**Newcomb**
- 2020 PhilPapers survey: 39.0% of professional philosophers two-box and 31.2% one-box. Among 48 decision theorists, 73% two-box and 21% one-box. ([Wikipedia: Newcomb's problem](https://en.wikipedia.org/wiki/Newcomb%27s_problem); [LessWrong write-up](https://www.lesswrong.com/posts/JTekFwz3rWjsirBbr/2020-philpapers-survey-results))

**Trolley**
- 70,000 participants, 42 countries: country-level average approval of sacrifice was **81% Switch, 72% Loop, 51% Footbridge**. The ordering held in every country. ([Daily Nous on Awad et al. 2020](https://dailynous.com/2020/01/22/learned-70000-responses-trolley-scenarios/))
- Moral Sense Test (Hauser): 89% said hitting the switch was acceptable and 11% said pushing the man was. ([Berkeley *California* magazine](https://alumni.berkeley.edu/california-magazine/online/trolleyology/))

**Sunk cost**
- 54% chose the less enjoyable $100 trip over the more enjoyable $50 trip (99% CI for the Wisconsin share: 30–62%). ([Arkes & Blumer 1985](https://cognition.aau.at/bg/BA/Arkes%20%26%20Blumer%201985.pdf))

**Hidden roles**
- A mafia of about the square root of the player count is enough for even odds against an uninformed majority. ([Braverman, Etesami & Mossel 2008](https://arxiv.org/abs/0804.0071))

### Inferences
- **Believable cast ratios** from the data: in any group of about 10, expect about 5 cooperators on a one-shot betrayal choice (Golden Balls / Sally), 1–2 deep reasoners (Nagel step 3+ is 6–10%), about 1 in 6 who reject an unfair deal at their own cost (16% rejection), and a near-certain escalation once two people have sunk money into an all-pay contest.
- **Stakes flip behaviour:** cooperation is high for "peanuts" and falls to about 45% when it matters (Golden Balls). Stories should raise the stakes mid-game to make former allies defect.
- **Promises:** characters who promise usually keep them (+31 pp), but listeners don't trust promises. That gap drives dramatic irony: the audience knows she meant it, and he stole anyway.
- **Punishment cuts both ways:** let players fine each other and cooperation can soar (50–95%), but expect someone to punish the *generous* player out of spite (antisocial punishment).

### Gaps
- Exact original numbers for Güth et al. 1982, Teger 1980 and Shubik's own classroom dollar auctions, Engel's average dictator share, Johnson & Mislin's mean sent and returned, Thaler's FT contest, and Fehr & Gächter 2002's figures: not retrieved (paywalls or scanned PDFs).
- The PNAS trolley paper itself returned HTTP 403; the percentages come from a reputable summary (Daily Nous) quoting it.
- No experimental data found on the pirate game, blue-eyed islanders, or two generals with human players.

---

## Q3. Which structures hide an "everyone survives" solution that trust or coordination unlocks (and greed, fear or betrayal breaks)?

### Takeaway
Most social dilemmas contain a group-optimal outcome that is **not** an individual equilibrium. Universal cooperation in the PD, full contribution in public goods, a sustainable harvest in the commons, the stag in the stag hunt, and rotation in El Farol are natural "all survive" paths that one defector can break. Logic puzzles (hats, 100 prisoners) hide a pre-agreed **coordination protocol** that raises group survival dramatically and fails if one person goes off-script. Fiction already models this: Liar Game's protagonists repeatedly find a "nobody loses" plan, and the main threat to it is distrust.

### Cited Findings
- **PD / Split or Steal:** both-split is the all-win outcome; in real play it happened in only **31%** of finals, and in 25% both stole and both got nothing. ([van den Assem et al. 2012](https://repub.eur.nl/pub/31292/SplitorSteal_2012.pdf))
- **Public goods:** the social optimum is everyone contributing everything when the multiplier × n > 1, while the Nash prediction is 0, "the core free-rider problem." ([Wikipedia: Public goods game](https://en.wikipedia.org/wiki/Public_goods_game)). Cooperation survives only when cheats can be punished (50–95% contributions) and collapses without it. ([Fehr & Gächter WP](https://www.cesifo.org/DocDL/ces_wp183.pdf))
- **Commons:** lab resource users can self-govern through communication and internal sanctions without an outside enforcer. ([Ostrom, Walker & Gardner 1992](https://econpapers.repec.org/article/cupapsrev/v_3a86_3ay_3a1992_3ai_3a02_3ap_3a404-417_5f08.htm))
- **Stag hunt / minimum effort:** the high-effort equilibrium is best for everyone, yet groups slid to the worst one. ([Crawford notes](https://econweb.ucsd.edu/~vcrawfor/LearnLockTalkNotes.pdf))
- **Chicken:** iterated chicken can settle into turn-taking. ([Wikipedia: Chicken](https://en.wikipedia.org/wiki/Chicken_(game)))
- **Hat puzzles:** with a pre-agreed parity code, 9 of 10 in a line are guaranteed; with optional passing, a 3-person team wins 75% instead of 50%; in the cooperative version where everyone sees all other hats, everyone is right except when all hats match. ([Wikipedia: Hat puzzle](https://en.wikipedia.org/wiki/Hat_puzzle))
- **100 prisoners:** the cycle protocol raises all-survive odds from about (1/2)^100 to about **31%**. ([Wikipedia: 100 prisoners problem](https://en.wikipedia.org/wiki/100_prisoners_problem))
- **Liar Game, Minority Rule:** Nao and Akiyama form an 8-person bloc that splits its votes evenly between Yes and No, so the bloc always contains the minority. They narrow it down to one bloc member who wins and pays the others' debts. ([Wikipedia: Liar Game](https://en.wikipedia.org/wiki/Liar_Game))
- **Liar Game, Contraband:** Nao proposes that everyone carry **empty briefcases**, so nobody can lose money through confiscation or compensation. This is the cleanest fictional "hidden all-survive" solution; it depends on every smuggler trusting the others not to smuggle. ([Wikipedia: Liar Game](https://en.wikipedia.org/wiki/Liar_Game))
- **Liar Game, Salvation revival:** players agree to let one player win each round so the organisers earn nothing from debts. Nao then pays another player's debt and returns her winnings to the other seven. ([Wikipedia: Liar Game](https://en.wikipedia.org/wiki/Liar_Game))
- **Squid Game:** consent clause 3 (games end if a majority votes to stop) is a real exit; the players use it, and most return because life outside is worse. ([Ready Steady Cut](https://readysteadycut.com/2021/09/17/squid-game-season-1-episode-2-recap-hell/))
- **Writer community view:** a death-game writer on r/GAMETHEORY wants games with "an indisputable optimal solution" the audience can deduce. Their example is a checkers death game whose win condition ("reach the other side and become a King") never requires capturing the opponent, so both can survive by clearing a path, with a "players may speak at any time" rule as a clue. A commenter says the best rounds are those where a both-survive solution exists "but there's always that one selfish character" with extra incentives. ([r/GAMETHEORY thread, July 2026](https://www.reddit.com/r/GAMETHEORY/comments/1v1st24/requesting_ideas_for_a_death_game_story/))

### Inferences
Each structure, with its natural all-survive path and what breaks it:
| Structure | Hidden all-survive path | What breaks it |
|---|---|---|
| PD / split-steal | all split | greed (steal + "I'll share later"), fear of being the sucker |
| Iterated PD | tit-for-tat until the end | revealing the last round (backward induction) |
| Public goods / commons | everyone contributes / harvests under threshold | one free rider; spiteful antisocial punisher |
| Trust game | send all, return half | trustee keeps it; first mover's fear |
| Ultimatum | equal split | proposer greed, or responder pride rejecting a "fair enough" offer |
| Volunteer's dilemma | rotation or lottery of who volunteers, agreed in advance | diffusion of responsibility; each waits |
| Stag hunt | everyone picks stag | fear that one person is afraid |
| Chicken | both swerve; or alternate who "wins" | ego, audience ("derisive cry of Chicken!") |
| Beauty contest | everyone picks the same number, so all tie (if ties survive) | one person undercuts to win outright |
| Minority / El Farol | bloc splits votes evenly; rotation | bloc member defects to sit in the smaller group |
| Unique bid (LUPI) | pre-assigned distinct numbers | someone copies another's number |
| Dollar / all-pay auction | nobody bids, or one bid and then everyone stops; split the dollar | the second bidder's loss aversion |
| Pirate game | none by pure logic; a pre-game pact to vote down any unequal split | the senior pirate's bribery |
| Blue-eyed islanders | never make it common knowledge (silence) | one well-meaning public statement |
| Two generals | one side commits without final confirmation | demanding certainty |
| Hats / 100 prisoners | pre-agreed code / cycle protocol | one person doesn't trust or follow the protocol |
| Monty Hall | (individual) switch | anchoring on the first choice |
| Newcomb | one-box, if the predictor is reliable | greed for the extra small prize |
| Trolley / sacrifice | rule loophole only (e.g. "save five" needn't mean "kill one") | utilitarian panic |
| Hidden role | the innocent majority shares information and votes carefully | paranoia, framing, the hidden minority |
| Bystander | assign one named responder | "someone else will" |
| Sunk cost | quit early | "too much invested to quit" |

- The strongest story engines combine a **coordination protocol** (hats, 100 prisoners, minority bloc) with a **trust leap** (PD-like temptation at the end). Example: the protocol saves everyone only if each person also refrains from a private bonus option.
- Empirically, fragility is high: even with communication, real groups reach full cooperation only part of the time (31% both-split; collapse without punishment). So it's realistic that "people break it."

### Gaps
- No source quantifies how often real groups find a hidden coordination protocol (like the 100-prisoners strategy) unaided. I found no experiments on this.
- I found no published analysis of hidden all-survive solutions in Alice in Borderland or Kaiji games specifically.

---

## Q4. How rule wording creates a fair loophole (exact words, definitions of "player", "spent", "tie", timing)

### Takeaway
Fair loopholes come from rules that are **literally precise but socially misread**: an unstated tie rule, a win condition that never says the opponent must lose, an optional "pass," a definition of who counts as a player, or a clause that lets the majority end the game. Real games show how small wording changes swing outcomes (a pass option takes hats from 50% to 75%; changing p or the tie rule in a beauty contest changes everything). Fiction plants such clauses early (Squid Game's consent clause 3).

### Cited Findings
- **Tie rules decide everything.** Nagel's guessing game split the prize among ties ([Nagel 1995](https://extranet.parisschoolofeconomics.eu/docs/guesnerie-roger/nagel95.pdf)). With integers only from 0 to 100, every choice except 0 and 1 is eliminated, and whether to pick 0 or 1 depends on how many others pick 0 ([Wikipedia](https://en.wikipedia.org/wiki/Guess_2/3_of_the_average), "citation needed").
- **Domain wording:** the first public contest (*Jeux & Stratégie*, 1981) used integers from 1 to 1,000,000,000 and was limited to readers who had earned points in earlier puzzles, so "who is a player" was itself a rule. ([Wikipedia](https://en.wikipedia.org/wiki/Guess_2/3_of_the_average))
- **An optional "pass":** allowing a pass is what lets Ebert's team reach 75%; release requires at least one correct guess and no wrong ones. ([Wikipedia: Hat puzzle](https://en.wikipedia.org/wiki/Hat_puzzle))
- **"Who pays":** in the dollar auction, the second-highest bidder also pays. That clause alone creates escalation. ([Wikipedia: Dollar auction](https://en.wikipedia.org/wiki/Dollar_auction))
- **Multiple entries / "unique":** unique-bid auctions usually allow several bids per person, and bid counts are secret. ([Wikipedia: Unique bid auction](https://en.wikipedia.org/wiki/Unique_bid_auction))
- **Majority exit clause:** Squid Game's clause 3 (games end by majority vote) was there from the consent form, and a character pointed it out. ([Ready Steady Cut](https://readysteadycut.com/2021/09/17/squid-game-season-1-episode-2-recap-hell/))
- **Order chosen before the game is known:** on the glass bridge, players pick their order numbers before learning the game. ([arXiv 2409.05263](https://arxiv.org/pdf/2409.05263))
- **Win condition that doesn't require the opponent's death:** the r/GAMETHEORY checkers example ("survive by reaching the other side and becoming King"), plus nothing forbidding rearranging the board, plus a time limit that lets a trapped player threaten mutual death. ([Reddit](https://www.reddit.com/r/GAMETHEORY/comments/1v1st24/requesting_ideas_for_a_death_game_story/))
- **Minority-rule wording:** "the smallest group wins" says nothing against coalitions, so the Liar Game bloc strategy is legal. ([Wikipedia: Liar Game](https://en.wikipedia.org/wiki/Liar_Game); [LessWrong](https://www.lesswrong.com/lw/oj4/a_majority_coalition_can_lose_a_symmetric_zerosum/dlwc))
- **Contraband:** nothing required carrying money, so empty briefcases were legal. ([Wikipedia: Liar Game](https://en.wikipedia.org/wiki/Liar_Game))
- **Pirate-game assumptions:** the result (98-0-1-0-1) depends on stated preferences (survival first, then coins, then a preference for throwing others overboard) and on the vote threshold. Change those and the answer changes. ([Wikipedia: Pirate game](https://en.wikipedia.org/wiki/Pirate_game))
- **Two generals:** demanding *certainty* makes it unsolvable; a rule that only asks for "attack together" without guaranteed confirmation leaves room for a trust solution. ([Wikipedia: Two Generals' Problem](https://en.wikipedia.org/wiki/Two_Generals%27_Problem))
- **Commitment wording:** a player who visibly removes their own options (the burned steering wheel) forces the other side's hand. ([Wikipedia: Chicken](https://en.wikipedia.org/wiki/Chicken_(game)))
- **Restricting a forbidden action:** AiB Jack of Hearts bans reflective items and physical violence, closing the obvious "see your own collar" loophole and forcing the information to come from other people (trust). ([AiB wiki: Jack of Hearts](https://aliceinborderland.fandom.com/wiki/Jack_of_Hearts))

### Inferences
Wording levers for original games, each a fair loophole if stated on screen early:
- **"Player":** does the host count? A dead player's vote? A proxy? "Each player must submit a number." Does a pair submitting one number count?
- **"Spent" / "paid" / "bid":** "the highest *bid* wins" vs "the highest *payment*." "Chips spent" vs "chips wagered." Can chips be lent, gifted, or pooled before being "spent"?
- **"Tie":** "the closest number wins" with ties undefined, vs "all tied players win." The all-tie rule makes "everyone picks the same number" an all-survive solution; "ties both lose" makes it a trap.
- **"Win" vs "survive":** separate them. "The winner gets the prize" while "anyone above 0 points survives." Most characters assume they're the same.
- **Timing words:** "by the end of the round" vs "at the bell"; "before the door closes" vs "while the door is open." An unknown round count preserves iterated-PD cooperation; a revealed last round breaks it.
- **"At least one" / "exactly one" / "each":** volunteer's dilemmas hinge on "if at least one person presses the button." A rule saying "the button can be pressed by anyone" can allow the host, or a machine, to press it.
- **What's not forbidden:** speaking, trading, rearranging, abstaining, passing, submitting jointly. The Reddit checkers rule "players may speak at any time" works because it's a plain-sight hint.
- **Information rules:** "you may not *tell* anyone their colour" doesn't forbid *standing in a coded position* (hat puzzles via signalling). A cheap-talk ban that covers words but not actions invites signalling.
- **Exit clauses:** majority-vote termination, or "the game ends if all players agree," lets the hidden all-survive solution literally be written in the rules, and its failure becomes purely social.
- **Fairness test:** follow the Reddit writer's standard. The audience must be able to deduce the solution from rules shown on screen, and the clue should be an oddly specific word or an unnecessary-seeming clause.

### Gaps
- I found no academic source on "fair loophole" design in death-game fiction specifically; the guidance above is drawn from the cited mechanics and one writer community thread.
- Some fictional rule details (Squid Game clause wording, AiB extra rules added as King of Diamonds players are eliminated) come from recaps and fan wikis and should be checked against the episodes before being quoted.
