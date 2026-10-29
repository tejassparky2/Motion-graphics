# Hooks and retention for 2-3 minute explainer reels: what we learned (Hinglish channel "Socho with Tejas")

Written 29 Oct 2026 for the doctor-channel chat ("Doc and the Organs"), on request. Our sources are Meanwhile
Mayank's 12 reels and our own three videos (Toxoplasma, Krait, Speaker).

The full evidence is on branch `ccr-56282fe5-evehq4-hinglish`:
- `research_notes/meanwhilemayank_parasite_reels_study_2026-10-29.md`: hooks, examples and retention, ant reel vs
  wasp reel.
- `research_notes/meanwhilemayank_deep_dive_2026-10-29.md` and `research_notes/meanwhilemayank_style_bible_2026-10-29.md`.
- `channels/hinglish/README.md`: rules.
- `channels/hinglish/scripts_batch2.md`: the krait and speaker scripts, with an on-screen note for every line.

**Caveat:** our own videos aren't posted yet, so there is no performance data from them. Every number below comes
from Mayank's public reels or from earlier channels.

---

## 1. Hook rules (seconds 0-3)

**Frame 0**
- One subject, large, on a plain background, already moving.
- The hook text is on screen at frame 0, in two tiers: a few small setup words, then ONE big red key word. The big
  word shows as a faint grey "ghost" first and turns red by about 1.5-2 s, timed to the spoken word.
- Then mark the word as it's said: a strike, an eraser rubbing it out, a tick or a circle.
  - Examples: "IT WON'T / ~~KILL~~", "YOUR SPEAKER MAKES / NO SOUND", "IT BITES WHILE YOU / SLEEP".
- Sound is there from frame 0, with a music bed under the voice.

**Line 1 holds the contradiction**
- Open with "Socho," followed by something that sounds impossible.
  - "Socho, ek aisa keeda jo kisi ko maarta nahi... balki uska dimaag hack kar deta hai."
- Give the premise away in the first sentences, and keep only the HOW for later.

**Escalate two or three times within about 8 s.** This is the main difference between his 11.2M reel and his 665K
reel:
- Wasp (11.2M): "doesn't kill → hacks the brain, makes a zombie → lets its babies eat it ALIVE" by 8 s. It names
  the creature at 12 s.
- Ant (665K): "your legs walk... someone else... to your death", then "...to an ant" at 17 s, then a pop-culture
  detour. It names the fungus only at 28 s.
  - The "you" turns out to be false (it's an ant), so the stakes FALL at exactly the moment people decide whether
    to stay.
- **Second person works only when it is TRUE.** Our Toxoplasma hook turns "you" back on ("ye tumhare andar bhi ho
  sakta hai", 1 in 3 people) by about 15 s.

**A reality anchor plus an everyday or pop-culture anchor that plants a question**
- "Ye koi movie scene nahi, ye sach mein hota hai."
- The Last of Us (ant reel) plants "could this happen to humans?", which he answers at 88% of the runtime.
- Our anchors: Tom & Jerry ("the mouse wasn't scared, but that was a cartoon"), the TV-serial naagin ("everyone
  sees her; the real one you can't see"), and the shaadi DJ thump in your chest.

**Name the thing by about 10-13 s, with a short pause before the name.**

**What fails (his flops, 84K-147K)**
- Opening on a number, name or date: "2001: $33 a day", "Jio IPO", the bare word "Stress."
- Opening on a concept the viewer already knows.
- In the skills review, hooks with a number or name in line 1 ranked LOWER: Spearman −0.75 against IG views.

## 2. Data behind it

**Mayank's 12 reels, Instagram views**

| Reel | Views |
|---|---|
| Jewel wasp | 11.2M |
| Rabies | 4.6M |
| Chickenpox | 3.3M |
| Sweaty palms | 2.8M |
| Tardigrade | 2.3M |
| Zombie ant | 665K |
| HIV | 374K |
| Radiation | 258K |
| Sun vanished | 256K |
| Jio IPO | 147K |
| AIDS $1 | 111K |
| Stress | 84K |

- The same files did 100-10,000× better on Instagram than on YouTube. Post on Instagram first.
- His hits are all "a horror of nature" or "a hidden thing in YOUR body", with an Indian stake. His flops are news,
  finance, or concepts people already know.
- The **rabies 4.6M shape** fits your snakebite and malaria reels: "a vaccine exists, so why is it still deadly?",
  then a what-to-do ending.

**Automated hook scorers don't work for this genre.** We ran the yt-*/ig-* skill packs (hookscore, title.py,
caption.py, detect.py) on his reels:
- None of them ranks his hits above his flops.
- hookscore rates his 11.2M wasp hook 26 and his 84K stress flop 46.
- Judge hooks by the rules above, not by those tools.

**Earlier channel data (Interestingly Strange, 59 Shorts)**
- Openings where a character asks the impossible question kept ~72% of viewers.
- Openings where the narrator sets a scene kept ~62%.
- Openings that are a topic, "Meet X" or "Did you know" kept ~47%.

## 3. Our three openings, and why each should work

**Toxoplasma**
- Line 1: "Socho, agar koi tumhara darr hi mita de... aur tum khud chal ke apne shikaari ke paas pahunch jao."
- Frame 0: a wooden mannequin walks toward a huge cat shadow. "WHAT IF YOUR / FEAR" shows, and an eraser rubs out
  FEAR with an ERASED stamp.
- Next: "Tom & Jerry mein chuha billi se darta nahi tha. Par wo cartoon tha." Then the real rat by about 8 s. Then
  "aur sabse ajeeb baat? ye tumhare andar bhi ho sakta hai" (an estimated 1 in 3 people).
- Why it works: second person, then the contradiction (fear erased, so you walk to your hunter), a familiar anchor,
  and an escalation that makes the "you" TRUE.

**Krait**
- Line 1: "Socho, tum raat ko zameen par so rahe ho... ek saanp aata hai, kaat ke chala jaata hai... aur tumhe pata
  bhi nahi chalta. Kyunki dard hota hi nahi."
- Line 2 escalates: "phir kuch ghanton mein palkein bhaari... saans ki muscles band." Then the naagin anchor, then
  58,000 deaths a year (about 160 a day).
- Frame 0: one banded krait. "IT BITES WHILE YOU / SLEEP".
- Re-hook at about 55%: "anti-venom Bharat mein hi banta hai... toh itne log marte kyun hain?"
- Why it works: an Indian stake, a deadly bite with no pain (the contradiction), and a "why do people still die?"
  loop.

**Speaker (tech)**
- Line 1: "Socho, tumhare phone ka speaker awaaz banata hi nahi... wo bas hawa ko dhakka deta hai. Ek second mein
  hazaaron baar."
- Frame 0: a phone in a hand, with a magnifier on its speaker grille. "YOUR SPEAKER MAKES / NO SOUND".
- Why it works: it contradicts something the viewer is holding right now. Then everyday anchors: the DJ thump in
  your chest, a Mumbai local push passed person to person.

**Lines in the same mould for your topics** (drafts only; check every fact first):
- **Antivenom:** "Socho, saanp ke zeher ka ilaaj Bharat mein hi banta hai... phir bhi har din lagbhag 160 log
  saanp ke kaatne se mar jaate hain. Kyun?"
- **Superbugs:** "Socho, ek chhota sa zakhm... aur duniya ki koi bhi dawai kaam na kare."
- **Malaria:** "Duniya ka sabse khatarnaak jaanwar sher ya saanp nahi... ek machhar hai."

## 4. Other things that changed our videos

**Pace**
- A new picture every ~2.6-3.5 s, cut on the spoken word. Inside each picture something changes every 0.5-1.5 s:
  a mark, a stamp, a counter, a label.
- The visual is the LITERAL noun of the sentence: ruler, compass, stopwatch, magnet, ambulance...
- One recurring metaphor, used about three times. His is a puppet; ours are an eraser on FEAR, and air dots getting
  a "dhakka".

**Retention devices**
- **Open loops:** at least one big question is always open, and the biggest stays open until the last fifth. The
  wasp's "eaten alive" is set up at 4 s and paid off at 80%.
- **Re-hook lines** at about 40%, 55-60% and 90%: "sabse hairaani ki baat?", "toh phir ... kyun?", "sochne wali
  baat ye hai".
- **An escalation ladder:** each step is worse than the one before.
- **The ending:** a "socho" bookend line, then a YES/NO comment card with a personal stake ("tumhare ghar ke
  paas..."). No outro, no logo.

**Voice**
- Even pace: about 3.3 words/s and about 5.9 syllables/s.
- Long pauses (0.6-0.8 s) only before a reveal: the name, the big beat, the closing line.
- Speeding up or slowing down individual lines sounded robotic, so we use one even tempo for every line.
- We check every line with Whisper medium and re-take any line that's misheard or flat.

**Music**
- A continuous bed about 17 dB under the voice in pauses, matching what we measured in Mayank's reels.
- Pitched above about 300 Hz, so phone speakers carry it. Our first bed sat 27 dB under the voice and mostly below
  what phones play, and the owner couldn't hear it.
- It dips about 0.5 s before each reveal.

**Covers**
- A dark poster: one subject, at most three words, one big coloured key word.
- Keep all text inside Instagram's 3:4 grid crop (y 240-1680 on a 1080×1920 frame). Mayank's grid crop cuts the
  text on his 9 newest covers.

**Captions and titles**
- Caption line 1: the hook plus one number, under 125 characters, so it shows before "… more".
- For health topics, a ✅/❌ what-to-do list, the shape of his rabies caption.
- 3-5 specific hashtags, with the search words written plainly.
- YouTube titles: 60 characters or fewer.
- Captions showed no link to his views (two of his top four reels have no caption), but they cost nothing.

**Owner rules given to us** (ask the owner whether they apply to your channel too)
- Sources and photo credits go in as names only, never links.
- No AI wording in descriptions.
- Credits are fine: pick the best photo whatever its licence (PD, CC0, CC BY, Pixabay, Unsplash; never BY-SA, NC
  or ND).
