# Hinglish mini-documentary channel: "Socho with Tejas" (@sochowithtejas)

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

**Don't trust the yt-*/ig-* skill scorers for this channel** (29 Oct 2026; tested on Mayank's 12 reels, reports in
`<shorts research>/mayank/skills_review/`).
- None of them ranks his hits above his flops: hookscore, title.py, caption.py, detect.py, or swipe's formula names.
  - hookscore rates every one of his openings WEAK. His 11.2M wasp hook scores 26, his 84K stress flop 46.
  - "Put a number in line 1" went the wrong way for him: hooks with a number or name did worse.
  - detect.py marks normal Hinglish as machine-written.
- What does hold up:
  - the outlier multiple (views ÷ the channel's own median);
  - beats.py, but only as a length stopwatch.
- Judge hooks by the study rules instead: "socho" plus an impossible claim, and a contradiction in line 1.

## How to render (owner's laptop)
- Run `python -I -X utf8 channels/hinglish/render_hi.py --video toxoplasma`, using `--still T`, `--sheet 1.5` or
  `--check` as needed.
- It uses the research venv: pycairo, Pillow, edge-tts, faster-whisper and rembg.
- Photos go in `<shorts research>/hinglish_assets/<video>/` with `credits.json`. Renders go to
  `<shorts research>/hinglish_out/`. Both live outside the repo.
- Keys come from `<shorts research>/.env`, which is git-ignored.

## Status (29 Oct 2026)
- **Scripts batch 1:** `scripts_batch1.md`. The owner approved all 3 ("Approve all 3").
- **The three videos:**
  1. Toxoplasma: the parasite that makes rats walk to cats.
  2. Krait and snakebite in India: about 58,000 deaths a year, though the anti-venom is made in India.
  3. Demodex face mites.
- **Video 1, Toxoplasma: v2 script approved** (owner, 29 Oct: "Yes").
  - Changes: a second-person hook made true ("it may be inside you"), the Tom & Jerry anchor, the "only the cat
    fear" precision beat (Vyas 2007, House 2011) and a "socho" bookend.
  - Evidence: `research_notes/meanwhilemayank_parasite_reels_study_2026-10-29.md`.
  - Visuals rebuilt as 44 shots, about 3 s each. They are photo cut-outs from `hinglish_assets/toxoplasma2/` with
    credits, and FEAR is rubbed out by an eraser as the recurring metaphor (`poster.erase`).
- **Voice: Aman.**
  - Indic Parler-TTS's named speaker "Aman" is used only as the voice prompt; AI4Bharat IndicF5 speaks every line
    in that synthetic voice.
  - Processing: one even tempo (×1.13), then the studio chain v3.
  - Every line gets a Whisper retake (`retake.py`) and a liveliness retake (`lively_retake.py`, keeping the take
    with the widest pitch movement that stays clear).
  - Nobody is cloned.
- **Topics: science AND tech** (owner, 29 Oct 2026: "Not only science we also do tech like how speaker works how
  internet works with examples").
  - Tech explainers, "how X works": a speaker, the internet, a phone. Each one is built around everyday examples.
  - They use the same format: a "socho" hook, a picture change every ~3 s, and a literal object on screen for every
    noun.
- **Sources and photo credits stay short, with no links** (owner, 29 Oct 2026: "Don't add links in source for
  research add 1 or 2 for photo only mention where it took from not full link").
  - Research sources: names only (authors, year, journal).
  - Photos: two lines. Line 1 is the sites they came from; line 2 is the CC BY photographers' names, because that
    licence requires them.
  - `render_hi.write_sheet` produces exactly this.
  - Credits themselves are fine (owner, 29 Oct 2026: "i never said no credits i said we give credits but only with
    text name not with links"). Pick the best photo whatever its licence: PD, CC0, CC BY, Pixabay or Unsplash.
    Never BY-SA, NC or ND.
- **No AI wording** in descriptions, captions or upload sheets (owner, 29 Oct 2026: "Don't add anything as ai in
  descriptions or anything"). Photo credits stay, because CC BY licences require them.
- **Channel name: "Socho with Tejas", handle @sochowithtejas** (owner, 29 Oct 2026: "I go with sochowithtejas").
  It uses the owner's own name and photo; every video opens with "Socho…", so the hook and the name are one brand.
  Logo colours match the videos: paper #D9C9A8, ink #291F17, red #BD211C.
