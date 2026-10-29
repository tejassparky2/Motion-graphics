# Meanwhile Mayank: deep dive on all 12 reels (29 Oct 2026, laptop session)

Sources: all 12 YouTube Shorts and 11 of the 12 Instagram reels, downloaded on the owner's laptop with yt-dlp (no login;
the HIV reel needs a login on Instagram, its YouTube copy was used). Instagram view counts were read from the public
profile grid on 29 Oct ~10:30 IST; likes, comments and post times come from yt-dlp. Scripts come from YouTube's
Hindi auto-captions (a few words misheard). Frame strips, cut counts and change rates come from ffmpeg. The videos
and frame strips stay on the laptop (`shorts research\mayank\`), never in this repo.

## Correction to meanwhilemayank_2026-10-29.md
The owner's screenshot showed only the 6 newest reels. The full account is **12 reels, one a day, 16-27 Oct 2026**,
and **63.8K followers in 13 days**. Animal topics are not his flops: **his biggest reel is the jewel wasp (11.2M)**.
Every reel is the same edit on both platforms (same length, same cuts); only the platform differs.

## The 12 reels, ranked by Instagram views

| # | Posted | Topic | IG views | IG likes | IG comments | YT views | Length | Ending |
|---|---|---|---|---|---|---|---|---|
| 1 | 18 Oct | Jewel wasp turns a cockroach into a zombie | **11.2M** | 643K | 4,727 | 1.1K | 2:19 | awe line |
| 2 | 21 Oct | Rabies: vaccine exists, still kills | **4.6M** | 276K | 2,390 | 4.6K | 2:57 | what to do after a dog bite |
| 3 | 22 Oct | Chickenpox virus still inside you | **3.3M** | 140K | 848 | 4.0K | 2:40 | "did you get the vaccine? comment" |
| 4 | 26 Oct | Palms sweat for no reason | **2.8M** | 88K | 2,489 | 6.1K | 1:32 | "your palms too? comment" + comments card |
| 5 | 20 Oct | Tardigrade survives open space | **2.3M** | 88K | 205 | 6.7K | 2:35 | closes its own question |
| 6 | 19 Oct | Zombie-ant fungus | 665K | 43K | 180 | 2.6K | 2:38 | one-line punch |
| 7 | 24 Oct | HIV hides for 10 years | 374K | n/a | n/a | **263K** | 2:26 | India statistic |
| 8 | 27 Oct | How radiation kills (2 days old) | 258K | hidden | 95 | **223K** | 2:44 | myth-bust + comment question |
| 9 | 25 Oct | If the Sun vanished | 256K | hidden | 78 | 1.6K | 2:38 | awe line |
| 10 | 17 Oct | Jio IPO | 147K | hidden | 25 | 0.8K | 1:52 | price card, fade to black |
| 11 | 16 Oct | Indian who made AIDS medicine $1 a day | 111K | hidden | 40 | 2.7K | 2:50 | trails off |
| 12 | 23 Oct | Chronic stress | 84K | hidden | 51 | 1.7K | 2:27 | "what's your stress reason?" |

Posted daily between about 4:30 and 7 PM IST (two at ~10:30 AM). Captions repeat the hook in one Hinglish line
plus an emoji. All Hinglish, one calm male narrator, 173-200 words a minute; speech rate does not separate hits
from flops.

## 1. The first 3 seconds decide it

| Reel | Frame 0 | On-screen words (time) | Spoken line 1 (paraphrase) |
|---|---|---|---|
| Wasp 11.2M | one wasp photo flies onto blank creased paper | "AN INSECT" (0.0) → "IT WON'T **KILL**" (1.75), KILL struck through in red (2.25) | "Imagine an insect that doesn't kill: it hacks the brain and makes a zombie" |
| Rabies 4.6M | blank paper, a vaccine vial drops in (0.25) | "RABIES HAS A **VACCINE**" + red tick (1.5-1.75) | "Why is rabies deadly when a vaccine exists?" |
| Chickenpox 3.3M | a forearm; spots pop on one by one (0.25-1.25) | "HAD **CHICKENPOX?**" (0.75), a red circle drawn round one spot (2.0) | "Did you ever have chickenpox? Then the virus is still in your body" |
| Palms 2.8M | a hand, which turns into a sweat-pore diagram | "EVER WONDERED / **WHY SOME PALMS**" (1.25) → "FOR NO REASON" + wet palm (2.75) | "Ever wondered why some people's palms sweat for no reason?" |
| Tardigrade 2.3M | the creature floats in over Earth | none until "OPEN SPACE" (2.0) | "Imagine an animal that survives the vacuum of space" |
| Zombie ant 665K | a wooden puppet walking | "YOUR LEGS ARE **WALKING**" (2.0) → "NOT YOU." (2.75) | "Imagine your legs walking, but someone else is moving them" |
| Stress 84K | a busy street: clock tower, autos, bus, billboards, HONK/PEEP bursts | "**STRESS**" (0.25) | "Stress. You've all heard this word" |
| AIDS $1 111K | pharmacy shelves full of boxes | "2001" stamp, then "$33 A DAY" | "Year 2001. AIDS treatment cost $33 a day" |
| Jio 147K | a dim sepia phone filling with notifications | small "JIO / is everywhere right now" | "What's so special about the Jio IPO that it's trending?" |
| Sun 256K | a busy city sky, sun between buildings | "LOOK UP, ANY DAY" → "THE **SUN**" (2.75) | 2.4 s of "whenever you look up you see the sun" before the what-if |

**What separates them:**
- **The hits show one subject, isolated on empty paper, from frame 0.** It is a real-photo cut-out of an insect,
  vial, arm, hand or creature. Three of the four flops open on a busy scene (street, shelves, city).
- **In the hits, line 1 is a contradiction about that subject:**
  - "doesn't kill / turns it into a zombie"
  - "vaccine exists / still deadly"
  - "you had it / it's still inside you"
  - "your legs walk / not you"
  
  The flops' line 1 names a topic ("Stress."), a year ("2001"), a news item ("Jio IPO") or something obvious ("you see
  the sun").
- **The headline has two tiers:** a small dark setup word, then a big red word, with the contradiction on screen by
  about 1.5-2.5 s. A red strike-through, tick or circle marks the key word.
- **All six top reels open on "Socho…" (imagine) or a "you" question.** The wasp, tardigrade and ant open on
  "Socho"; chickenpox, palms and rabies on a question to "you".
- **A strong image can carry it alone:** the tardigrade (2.3M) shows no text for 2 s.

## 2. Script structure (hits)
Every reel is a 2-3 minute mini-documentary of about 470-580 words. The hits share this skeleton:
1. **0-10 s: the whole shocking premise in one breath.** The wasp even gives away the ending ("…then its babies eat
   it alive"). Then a reality stamp: "this is no horror movie / movie scene, it really happens". The viewer stays
   for *how*, not *what*.
2. **10-30 s: the name, plus one fact of scale.** It is often Indian:
   - 9 in 10 Indians carry the chickenpox virus by 30.
   - 56 lakh dog bites and about 5,700 rabies deaths a year in India; 2 of the world's 3 WHO-approved vaccines
     are made in India.
   - A tardigrade species was named after APJ Abdul Kalam.
3. **Mechanism, one step per sentence, with exact numbers.** The precision is the awe: two stings; 2-3 minutes;
   25 cm up, on the north side, at noon; a few cm a day along a nerve.
4. **A re-hook at 40-85% of the runtime:**
   - wasp at 76 s: "now the strangest part"
   - chickenpox at 92 s: "so why didn't chickenpox die out?"
   - rabies at 135 s: "why are patients afraid of water?"
   - tardigrade at 53 s: "how can something so tiny survive all that?"
5. **One running metaphor:**
   - a tenant who never leaves the house
   - a nerve as a transport line the virus hijacks
   - a puppet
   - life on pause
6. **Health reels: an Indian myth-bust, then what to do.** The myths are chili and turmeric on the wound, "14
   injections in the stomach", "mata aayi hai", and cow dung blocking radiation. The advice is concrete (soap and
   running water for 15 minutes, a vaccine the same day; no aspirin for children). That makes them reels people
   save and forward.

The flops do something else:
- They explain a concept everyone knows, textbook-style ("first, what is stress?").
- Or they recite finance and news numbers with no stakes for the viewer (IPO price band, patent law).
- The Sun reel has a good what-if but no "you are affected" stake, and it spends its first 2.4 s on the obvious.

## 3. Cut pace
Hard cuts are rare in this style, because pictures build up inside a held poster. So the useful measure is a
visible change: anything appearing, moving or swapping, sampled 5 times a second.

| Reel | Visible changes per 10 s (whole) | 3-15 s | Hard cuts per 10 s |
|---|---|---|---|
| Wasp 11.2M | 5.8 | 10.8 | 1.4 |
| Rabies 4.6M | 7.8 | 10.0 | 1.5 |
| Chickenpox 3.3M | 8.6 | 12.5 | 2.4 |
| Palms 2.8M | 9.5 | 10.8 | 2.4 |
| Tardigrade 2.3M | 7.0 | 5.0 | 1.7 |
| Jio 147K | **3.7** | 3.3 | **0.2** |
| AIDS $1 111K | **3.8** | 3.3 | 1.2 |
| Stress 84K | 10.1 | 9.2 | 2.8 |

- **Hits change something every 1.0-1.7 s**, and most densely just after the hook (10-12.5 per 10 s in seconds
  3-15).
- **The two money flops change half as often (every ~2.7 s).** They are type-only cards; Jio has 2 hard cuts in
  112 s.
- **Stress was the fastest and still the worst.** Pace is necessary, not sufficient: the subject and line 1 decide.

## 4. Endings
- **No spoken subscribe or follow ask, and no "part 2".** Most reels end within a second or two of the last line.
- **Three ending types:**
  - Awe: "Nature isn't only beautiful."; "think how strange nature is"; rogue planets wandering in the dark.
  - Practical advice: the rabies steps.
  - A personal-experience question for the comments: "Did you get the vaccine?"; "Do your palms sweat too?"
- **The comment question multiplies comments only on a reel that already hooks.** Palms drew 0.89 comments per 1K
  views; the wasp, which has no question, drew 0.42. Stress asked one too and got 51 comments.
- **The wasp's last 6 s replay the whole story as one diagram** (a framed specimen box, then the egg → larva →
  cocoon → wasp loop).
- **The flops trail off** (Jio: a price card and fade to black; AIDS $1: "the next expensive drug is already here").

## 5. Why Instagram and not YouTube
The files are identical, yet the wasp did 11.2M on Instagram and 1.1K on YouTube. YouTube's two outliers (HIV 263K,
radiation 223K) are mid-table on Instagram. So the difference is distribution, not the edit.

Instagram likes run 4-6% of views on the top reels (wasp 5.7%, rabies 6.0%, chickenpox 4.2%). These are the
"forward this to your family" topics Instagram pushes through DMs and saves (inference: Instagram doesn't publish
shares or saves). His YouTube channel has 2,160 subscribers.

## 6. What to take
**Doctor channel** (its direct model):
- Copy the skeleton in §2.
- One isolated subject on paper at frame 0.
- A contradiction in line 1, on screen as small setup word + big red word by ~2 s.
- An Indian stake in the first 30 s.
- A re-hook at about 60%.
- End on a myth-bust plus what to do, or a "you too?" question.
- Post on Instagram first.

**Interestingly Strange:**
- **Keep line 1 = a character asking the impossible question.** It is the same mechanism as his line-1
  contradiction.
- **Add his frame-0 discipline:**
  - one subject, clean background, no busy establishing scene
  - a small setup word plus one big red key word, landing by ~2 s
  - the key word marked (strike, tick, circle) as it is spoken
- **Give away the premise, never the payoff.** He states the whole shocking arc in 10 s and people still stay for
  the how.
- **One mid-video re-hook question** in anything over 40 s.
- **The debate ending already matches his "you too?" ending.** A personal stake in the question ("would *you*…")
  should raise comments.
- **Post every Short as an Instagram Reel too.** This is the strongest evidence yet: the identical file did
  100-10,000× better there.
- **Don't copy his 2-3 minute length on YouTube.** Our 40-50 s rule comes from our own YouTube data, and his long
  reels win on Instagram.

**Topics that win for him:** a horror of nature (parasites, zombie control) or a hidden thing in *your* body, with
an Indian stake. **Topics that lose:** news and finance, and concepts the viewer already knows.

## Limits
- Only 12 reels.
- The newest are 2-4 days old: radiation, palms and Sun may still grow.
- No retention data for his reels; all comparisons are view counts.
- Comment counts include his own replies.
