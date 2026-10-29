# Hinglish mini-documentary channel (new, name not chosen yet)

Started 29 Oct 2026 from the owner's laptop chat. Owner: "I want you to make same type of videos for my channel ...
we do in hindi same type let's try what worked for him", then "Brand-new channel". This is **not** Interestingly
Strange: different language, length, look and rules. Interestingly Strange's CLAUDE.md rules on voice and privacy
still apply here:
- never the owner's cloned voice
- never a clone of a real person (that includes Meanwhile Mayank)
- no downloaded videos or chat transcripts in this public repo

Evidence for the format: `research_notes/meanwhilemayank_deep_dive_2026-10-29.md`. His 12 reels got 63.8K Instagram
followers in 13 days. The hits were 2.3M-11.2M, the flops 84K-147K.

## Format (copied from his hits)

**Shape:**
- Hinglish narration, one calm narrator, about 190 words a minute.
- 1:30-2:30 long, 9:16, English on-screen headlines.
- Post on Instagram Reels first, then YouTube Shorts. His identical files did 100-10,000x better on Instagram.

**Topics:**
- Winners:
  - a horror of nature (parasites, mind control)
  - a hidden thing in or on *your* body
  - an Indian life-or-death stake with practical steps (his rabies reel, 4.6M)
- Losers: news and finance, and concepts everyone already knows (stress, IPO, patents).

**Frame 0:** one subject alone on creased poster paper; never a busy scene.

**Headline:** a small dark setup line plus one big red word with the contradiction, fully on screen by ~2 s. The key
word is marked as it's spoken (red strike-through, tick or circle).

**Script order:**
1. Line 1: "Socho..." or a question to *you*, with the contradiction inside it. Give the premise away; never the
   payoff.
2. A reality stamp ("ye koi movie nahi, ye sach hai").
3. The name.
4. One fact of scale, Indian where possible.
5. The mechanism, one step per sentence, with exact numbers.
6. A re-hook question at about 60%.
7. One running metaphor through the whole reel.

**Ending:**
- A myth-bust (the Indian home remedy or belief), then concrete steps.
- Or an awe line.
- Then a "you too?" question: "...comment mein bataiye".
- No subscribe ask, no part 2.

**Pace:** something changes every 1-1.5 s, densest in seconds 3-15.

**Look:**
- Real-photo cut-outs (Wikimedia Commons/CC0, or generated locally) on paper texture.
- "FIG. n" and specimen labels, flip counters, red marks.
- One muted palette per section.

## Workflow
Interestingly Strange's workflow applies: script first, owner approves, render one, then the rest, Whisper-check
every line, upload sheet. Sources go with every script, and health claims must be checked before rendering.

## Status (29 Oct 2026)
- **Scripts batch 1:** `scripts_batch1.md`, waiting for the owner's approval.
  1. Toxoplasma: the parasite that makes rats walk to cats.
  2. Krait and snakebite in India: about 58,000 deaths a year, though the anti-venom is made in India.
  3. Demodex face mites.
- **Voice: not chosen.**
  - Ten free Microsoft neural voices were tested against Mayank's narration (speaker-embedding similarity). The
    best scored 0.728 (Florian multilingual); his own clips score 0.97 with each other. So no free stock voice is
    close.
  - Whisper clarity was best for Madhur (hi-IN), Florian and Swara (hi-IN); Andrew and Brian have an English
    accent in Hindi.
  - Owner chose to test premium voices next: Sarvam Bulbul (v4-flash documentary/story personas, v3 male speakers)
    and ElevenLabs eleven_v3 premade male voices.
  - The test is `voice_premium.py`. It runs on the owner's laptop, where the reference clips are, and needs
    `SARVAM_API_KEY` / `ELEVENLABS_API_KEY` set as Windows user environment variables (never pasted in chat).
- **Still to decide:**
  - the channel name and handle
  - the voice
  - the renderer: the 2D pycairo pipeline needs a photo-cut-out/poster style kit for this look
