# From the laptop "shorts research" chat: everything studied, researched and made, A to Z (29 Oct 2026)

Written for the doctor-channel chat (owner: "Ask it a-z everything it did studied researched made").
This chat runs on the owner's Windows laptop (Claude desktop app, folder `C:\Users\tejas\Documents\shorts research`),
mostly over Remote Control. It built the new Hinglish channel **"Socho with Tejas"** (@sochowithtejas).

**Code and notes are in this repo, on branch `ccr-56282fe5-evehq4-hinglish`** (fetch it, or check out single files):
- `channels/hinglish/` holds the pipeline, the scripts and the README with every rule.
- `research_notes/meanwhilemayank_*`, `research_notes/hooks_from_shorts.md` (hooks only, the short version) and
  this file.
- `motion/audio.py` holds the music beds.

**Kept only on the laptop** (downloads, private material; never in the public repo):
- `mayank\`: downloaded reels, per-reel shot logs `mayank\study\*.md`, transcripts, voice experiments, and the
  skills reviews `mayank\skills_review\*.md`.
- `hinglish_assets\`: photos plus `credits.json`.
- `hinglish_out\`: renders and upload packs.
- `reports\`: deep-research reports.
- `trakin\`: a separate chat's study of the trakin.ai channel.

---

## A. Timeline
1. **Loaded the cloud chat's repo and rules.** Downloaded all 12 Meanwhile Mayank reels from YouTube (yt-dlp) and
   Instagram (browser grid read plus yt-dlp; no login). Analysed hooks, structure, pace and endings.
2. **Ran an Instagram deep dive** with open-source tools, and wrote rules into CLAUDE.md (frame 0, two-tier hook
   text, change density, re-hook, Instagram first).
3. **The owner chose a new channel:** "make same type of videos ... in hindi ... try what worked for him", then
   "Brand-new channel". Three scripts were approved: Toxoplasma, krait and Demodex.
4. **Voice:** long work on a narrator voice. The owner picked **Aman** (details in section E).
5. **Visual style:** a frame-by-frame study of all 12 reels, then a style bible. The owner: "Video not good you using
   same placeholder many time ... study deeply and apply same no hallucinations".
6. **Video 1, Toxoplasma:** rendered, re-voiced, rebuilt as fast cuts, sped up, given new music.
7. **Ant and wasp reel study.** The skill packs were installed and Mayank was reviewed with all 24 skills.
8. **Channel name and logo,** then the upload packs.
9. **Videos 2 (Speaker, tech) and 3 (Krait):** scripted, approved, voiced, rendered and packed.

## B. What was studied

### B1. Meanwhile Mayank (@meanwhilemayank)
He posts 2-3 minute Hinglish science explainers made of photo cut-outs on poster paper, with one calm male narrator.
He posted 12 reels, one a day, 16-27 Oct 2026, and reached **63.8K followers in 13 days**. Each reel is the same file
on YouTube and Instagram.

| Reel | IG views | YT views | Length | Opening |
|---|---|---|---|---|
| Jewel wasp | **11.2M** | 1.1K | 2:19 | "Socho, ek aisa keeda jo maarta nahi... dimaag hack... zombie... bachche zinda khaate" |
| Rabies | **4.6M** | 4.6K | 2:57 | "vaccine exists, still deadly: why?" |
| Chickenpox | **3.3M** | 4.0K | 2:40 | the virus is still inside YOU |
| Sweaty palms | **2.8M** | 6.1K | 1:32 | your palms |
| Tardigrade | **2.3M** | 6.7K | 2:35 | "socho" plus a survival claim |
| Zombie ant | 665K | 2.6K | 2:38 | "your legs walk... not you... to your death" |
| HIV | 374K | **263K** | 2:26 | hides for 10 years |
| Radiation | 258K | **223K** | 2:44 | how radiation kills |
| Sun vanished | 256K | 1.6K | 2:38 | "any time you look up..." (the obvious) |
| Jio IPO | 147K | 0.8K | 1:52 | news |
| AIDS medicine $1 | 111K | 2.7K | 2:50 | "2001: $33 a day" |
| Chronic stress | 84K | 1.7K | 2:27 | "Stress." |

**Method**
- Frames at 1 fps for every second, plus 6-fps strips of the headline zone and of motion.
- ffmpeg scene detection; Hindi transcripts from YouTube captions and Whisper.
- Hand-written shot logs for all 12, one row per scene: time, visual, headline, motion, narration.

**Findings**
- **Hits vs flops:** they differ in the opening seconds, not in voice or length.
  - Hits open on one subject on blank paper, with a contradiction in line 1.
  - Flops open on a busy scene, a number, a name or a topic.
- **Pace:** a new picture every 2.6-4.4 s; something changes inside it every 0.5-1.5 s.
  - His hits show 10-12 changes per 10 s in seconds 3-15. His number-card flops show 3-4.
- **Headline system:** a small dark setup line, then a big red key word. The red word often appears first as a faint
  grey "ghost" for 0.5-1.5 s, then turns red. Marks: a red strike, a circle, a tick or a stamp.
- **Colour meaning:** red = threat, green = reassurance, cream = neutral, gold = numbers.
- **Backgrounds:**
  - creased beige notebook paper with ruled lines and binder holes
  - dark slate "x-ray" for anything inside a body
  - grey paper for the lab and study beats
- **Assets:**
  - photo-real cut-outs with a halftone print texture
  - photo-real props: magnifier, stopwatch, padlock, ruler, compass, specimen box
  - flat x-ray diagrams
  - red rubber stamps and torn paper tags
  - no live action
- **The visual is the literal noun of the sentence:** "2 cm" is a tape measure, "noon" a sundial, "can't let go"
  tweezers.
- **One recurring metaphor object:** the marionette or puppet in the ant reel.
- **Small "LABEL / FIG. n" header:** the labels are template tags, and FIG resets at 1/5, 2/5 and so on of the
  runtime. The HIV and chickenpox reels have no labels, only a bare rule.
- **Retention:**
  - open loops, with the biggest paid off in the last fifth
  - re-hook lines at about 40%, 55-60% and 90% ("sabse hairaani ki baat", "ab aata hai sabse ajeeb hissa", "zara
    socho")
  - an escalation ladder
  - a process told step by step ("phir... phir...")
- **Endings:**
  - awe ("nature isn't only beautiful")
  - what-to-do (rabies)
  - "you too? comment" (chickenpox, palms)
  - The flops trail off.
- **Music:** a bed that never stops, about 17 dB under the voice in pauses (sustained bass plus pad), with brief dips
  before reveals.
- **Voice:**
  - pace: 173-200 wpm, about 3.3 words/s, about 5.9 syllables/s
  - pauses: sentence pauses of 0.5-0.6 s; pauses of 0.75 s or more only before reveals
  - pitch: a range of 23-25 semitones (SD about 7)
  - It is very likely an ElevenLabs library voice (closest match: "Viraj"). It was NOT cloned.
- **Covers:** a dark poster with one subject and one big key word. The Instagram 3:4 grid crop cuts the text on his
  9 newest covers.
- **Captions:**
  - The hook is repeated in one Hinglish line plus an emoji, with 13-29 filler hashtags.
  - Five reels have no caption at all.
  - Captions show no link to views.
- **Posting:** daily, 4:30-7 PM IST; posting hour separates nothing.
- **Platform:** the identical files did 100-10,000× better on Instagram, where shares and saves of "forward this to
  family" topics drive reach.

### B2. Ant reel vs wasp reel (the same story shape, 665K vs 11.2M; full note in `meanwhilemayank_parasite_reels_study_2026-10-29.md`)
- **The wasp** shows the real creature at frame 0 and escalates three times in 8 s (doesn't kill → zombie → eaten
  alive). It names the wasp at 12 s and pays off "eaten alive" at 80%.
- **The ant** opens on a mannequin standing for "you" and reveals "...to an ant" only at 17 s, so the stakes drop. It
  names the fungus at 28 s, after a The Last of Us detour.
- **The Last of Us** plants "could it happen to humans?", which he answers at 88%. That is a good device.
- **Lesson:** second person works only if the "you" is TRUE; escalate early; name early.

### B3. Skill-pack review (Jake Schincariol's yt-* and ig-* skills, 24 in all, run on all 12 reels)
- **No scorer predicts his views.**
  - hookscore: wasp 26, stress flop 46; Spearman −0.48 for spoken hooks.
  - title.py: −0.61.
  - caption.py: −0.05.
  - detect.py: −0.71 (it flags normal Hinglish as AI-written).
- **"Put a number in line 1" goes the wrong way:** −0.75.
- **What holds:** the outlier multiple (views ÷ his median of 519.5K), and beats.py as a length stopwatch.
- **His profile:** 41 of 94 points; no pinned posts, no highlights.

### B4. Earlier channel data (Interestingly Strange, the owner's English channel, 59 Shorts)
- Openings where a character asks the impossible question kept about 72%.
- Openings where the narrator sets a scene kept about 62%.
- Topic, "Meet X" or "Did you know" openings kept about 47%.

### B5. trakin.ai (a separate chat, not this one)
A study of 122 of his tech-trick reels. The advanced agentic tricks hit most often (40% reach 15K+ likes). It is in
`trakin\trick_study.md` on the laptop.

## C. What was researched
- **Voice style matching** (deep-research report, `research_notes/voice_style_match_research_2026-10-29.md` on the
  -local branch):
  - Hindi TTS options and their terms: ElevenLabs, Sarvam, Azure, Indic Parler-TTS, IndicF5 and others.
  - Prosody controls and post-processing limits.
  - The studio vocal chain.
  - How to identify a stock voice.
  - Ethics and law: no cloning of real people. Indian personality-rights orders protect "voice and style". Platforms
    have impersonation policies.
- **Fact checks** for every script, with sources named in the description (names only):
  - Toxoplasma: Berdoy 2000 (Proc R Soc B); Vyas 2007 (PNAS: only the cat fear changes); House 2011 (PLoS ONE); CDC.
    "1 in 3 people" is said as an estimate ("andaza").
  - Krait:
    - Suraweera 2020, eLife: about 58,000 deaths a year in India, mostly at home, in the monsoon. Russell's viper
      causes more deaths than the krait, so the script says "one of the most dangerous".
    - MoHFW treatment guidelines: kraits bite people sleeping on the floor at night.
    - WHO SEARO first aid.
    - The Chandigarh krait review: bites are painless, with little swelling.
    - Chappuis 2007 (Am J Trop Med Hyg), bed nets in Nepal.
    - Dropped because unconfirmed: "stomach pain in the morning".
  - Speaker:
    - Rice & Kellogg, GE, 1925 (the moving-coil loudspeaker).
    - Apple Watch Water Lock pushes water out with the speaker.
    - Phone micro-speakers are about 11×15 mm, with cone movement of about ±0.3 mm.
    - Reciprocity: a speaker run backwards works as a microphone.
    - Sound travels at 343 m/s; hearing covers 20-20,000 Hz.
- **Topics that win for Mayank:** a horror of nature (parasites, control), or a hidden thing in YOUR body, with an
  Indian stake. **Topics that lose:** news, finance, known concepts.
- **Platform rules learned:**
  - Instagram first.
  - About 6 PM IST.
  - Caption line 1 under 125 characters.
  - 3-5 specific hashtags (Instagram caps hashtags at 5).
  - YouTube title of 60 characters or fewer.
  - Shorts can now run up to 3 minutes.
  - YouTube banner: 2560×1440, with a phone-safe strip of 1546×423.

## D. What was made

### D1. The channel: "Socho with Tejas" (@sochowithtejas)
- **Owner's choices:**
  - "Use Tejas my name I will use my photo ... so it looks strong rather then ai"
  - "I go with sochowithtejas"
  - "Not only science we also do tech like how speaker works how internet works with examples"
- **Logo and banner:** the owner made them in ChatGPT from his photo, using our prompt (paper #D9C9A8, ink #291F17,
  red #BD211C, a halftone cut-out, a hand-drawn red ring). We rebuilt the banner to 2560×1440 with everything in the
  safe strip.
- **Bio:** "Science aur tech jo dimaag hila de 🧠 / Body, nature aur gadgets kaise kaam karte hain / Simple Hindi
  mein, examples ke saath / Follow karo aur socho 👇"
- **Owner rules:**
  - "Don't add anything as ai in descriptions or anything"
  - "Don't add links in source for research add 1 or 2 for photo only mention where it took from not full link"
  - Then: "i never said no credits i said we give credits but only with text name not with links"

### D2. Video 1: Toxoplasma ("Ye parasite chuhe ka darr mita deta hai"), 2:12
- **Script v2:** 24 lines. The full text is in `channels/hinglish/videos/toxoplasma.py` and `scripts_batch1.md`.
- **Hook:** "Socho, agar koi tumhara darr hi mita de... aur tum khud chal ke apne shikaari ke paas pahunch jao."
- **Then:**
  1. The Tom & Jerry anchor ("par wo cartoon tha").
  2. The real rat.
  3. "ye tumhare andar bhi ho sakta hai (1 in 3)".
  4. The name.
  5. The life cycle.
  6. Born with fear vs no fear in infected rats.
  7. The Oxford experiment, "fatal attraction".
  8. The precision beat: "sabse hairaani ki baat? only the cat fear is erased".
  9. The loop.
  10. The re-hook: "does it change our brain?"
  11. Debated, not proven.
  12. How people get it.
  13. Pregnancy rules.
  14. Indoor cats are fine.
  15. The "socho" bookend: "a single cell erases a fear the rat was born with".
  16. The YES/NO question: a cat in your home?
- **Visuals:** 44 shots.
  - The recurring metaphor: an eraser rubbing out FEAR.
  - A wooden mannequin for "you".
  - An old TV that switches off.
  - A magnet for "fatal attraction".
  - A FEARS checklist where only CATS gets erased.
  - Sobotta engravings, an enclosure diagram, a tear-off calendar, a gauge, the YES/NO card.
- **Owner feedback along the way:**
  - "Video not good you using same placeholder many time"
  - "visuals seems changing slow and repetitive it can be improved"
  - "try to make videos like mayank like on hiv chickenpox"
  - "see the starting line he use cleverly on ant fungus video"
  - Approved v2 with "Yes".
  - "This new video is better now but can you speed up slightly like matching mayank speed"
  - "Didn't added bg music?", then "Sounds good"

### D3. Video 2: Speaker ("Speaker awaaz banata hi nahi?"), 2:18, the first tech video
- **Hook:** "Socho, tumhare phone ka speaker awaaz banata hi nahi... wo bas hawa ko dhakka deta hai. Ek second mein
  hazaaron baar."
- **Then:**
  1. "Bas ek magnet aur taar ka gola."
  2. The shaadi DJ thump in your chest ("wo awaaz nahi, hawa ka dhakka hai").
  3. Its name; 1925, Rice & Kellogg.
  4. Three parts: magnet, coil, cone (often paper).
  5. Electricity in, and the coil becomes a magnet.
  6. Pull and push, so the cone moves.
  7. A wave in the air.
  8. The Mumbai local push passed person to person ("koi khud aage nahi jaata, bas dhakka jaata hai").
  9. 343 m/s, to the eardrum, and the brain says "sound".
  10. The precision beat: one tiny cone plays drums, guitar and singer at once.
  11. 30-40 vs thousands of times a second; 20-20,000.
  12. The phone speaker is 1-1.5 cm, moving less than half a millimetre.
  13. Re-hook: why does the DJ's bass reach your chest, and the phone's doesn't?
  14. A big cone moves more air.
  15. Run backwards, it's a microphone (dynamic mics on stage).
  16. Smartwatches push water out with sound.
  17. The bookend: "your favourite song is just a magnet pushing air".
  18. The YES/NO question: DJ bass in your chest?
- **Visuals:** 39 shots.
  - The recurring picture: rows of air dots carrying a compression wave.
  - Drawn: a speaker cross-section with the cone moving, magnets with pull/push arrows, and electricity as a spark
    on a wire.
  - Photos: the Mumbai local, a Gray's ear engraving, drum, guitar and mic, a smartwatch with flying drops.

### D4. Video 3: Krait ("Ye saanp sote hue kaatta hai, dard bhi nahi hota"), 1:56
- **Hook:** "Socho, tum raat ko zameen par so rahe ho... ek saanp aata hai, kaat ke chala jaata hai... aur tumhe pata
  bhi nahi chalta. Kyunki dard hota hi nahi."
- **Then:**
  1. Paralysis.
  2. The naagin anchor (everyone sees her on TV; the real one you can't see).
  3. The name.
  4. 58,000 a year, about 160 a day, the most in the world.
  5. The Big Four.
  6. At night, in the monsoon, people on the floor.
  7. Faint marks, no swelling, no pain.
  8. The precision beat: it attacks the nerves and blocks the signal.
  9. Eyelids, then swallowing, then breathing.
  10. Re-hook: the anti-venom is made in India, so why do people die?
  11. They die at home and don't reach hospital in time.
  12. The myths struck through (jhaad-phoonk, cut and suck, a tight rope).
  13. First aid: stay still, take off rings and watch, go to a hospital with anti-venom, call 108.
  14. No pain at night? Still go.
  15. Mosquito net (the Nepal study).
  16. The bookend: "the danger is silence".
  17. The YES/NO question: a snake near your home?
- **Visuals:** 31 shots (eye with a drooping lid, lung engraving, India map, Big Four specimen cards, a nerve diagram
  on slate, home vs hospital, 108 ambulance, net).
- The owner approved the speaker and krait scripts with "Approve both".

### D5. Each upload pack contains
- the master (x264 CRF 14) and a phone copy (two-pass, under 29 MB)
- a cover
- the Instagram caption: line 1 is the hook plus a number; a ✅/❌ list for health topics; one YES/NO ask; 5
  hashtags
- a pinned YES/NO comment
- a second comment with credits: two lines of names, no links
- the YouTube title, description (sources as names only), tags and settings
- first-hour advice: reply with a question back, and a Story poll

Covers are a dark slate with one subject, a small cream line, and ONE big coral word, all inside the grid crop:
"THIS PARASITE ERASES / FEAR", "YOUR SPEAKER MAKES / NO SOUND", "IT BITES WHILE YOU / SLEEP".

## E. Tools and pipeline (copy freely)

**Rendering**
- `channels/hinglish/render_hi.py --video NAME [--still T | --sheet S | --check | --remix]`.
- Frames are drawn in pycairo by spawned worker processes (CPU), encoded with x264 slow at CRF 14, and AAC 256k.
- An upload sheet is generated, with credits as names.
- `--check` runs Whisper medium on every line.
- `--remix` rebuilds only the soundtrack onto the last render.

**Drawing kit: `channels/hinglish/poster.py`**
- Paper, slate and the print texture (`finish`).
- The two-tier `headline` with ghost-to-red, auto-fit to the frame.
- Marks: `stamp`, `strike`, `tick`, `cross`, `ring`, `path`.
- Photos: `photo` and `framed_photo` cut-outs with a contact shadow.
- Text and data devices: `card`, `counter` (flip digits), `calendar` (tear-off), `gauge`, `icon_array`,
  `yes_no_card`, `magnifier`.
- Motion: `drop`, `knock`, `slide`.
- The eraser effect: `erase`.
- Fonts: Anton (headlines) and IBM Plex Mono (labels).

**Shot machinery: `channels/hinglish/shots.py`**
- Each video lists `SHOTS = [(line, cue word, draw fn, "paper"|"slate")]`, and a cut lands 0.12 s before the cue
  word is spoken.
- A shot function draws as a function of time, so any frame can be rendered on its own.
- One video module holds the SCRIPT (Devanagari, numbers written as words), METADATA (upload texts), SHOTS and
  `sfx()`.

**Voice: `channel.py` NARRATOR**
- **Engine:** AI4Bharat **IndicF5** (MIT), speaking with a reference clip of Indic Parler-TTS named speaker **"Aman"**
  (Apache-2.0). Nobody is cloned.
- **Settings:**
  - one even tempo ×1.15 (atempo)
  - studio chain v3: afftdn denoise, 75 Hz highpass, EQ matched to the reference's long-term spectrum, a gentle
    compressor, de-esser, limiter
  - gaps of 0.36 s between lines and 0.46 s after a question
  - a reveal pause of 0.6 s, before the name, the precision beat and the closing line
- **`retake.py`:** re-voices lines whose Whisper word-error rate is high, keeping only takes with speaker similarity
  ≥ 0.85.
- **`lively_retake.py`:** re-takes flat lines (pitch SD under 4.5 semitones) and keeps the liveliest clear take.
- **Results for Aman:** word-error rate about 22% (most "errors" are spelling: English words written in English
  letters), naturalness (UTMOS) 3.66.
- **Rejected along the way:**
  - edge-tts and Microsoft voices: no free voice came close (similarity at most 0.73).
  - Parler "Rohit": words unclear (word-error rate about 32%).
  - Pitch widening: it blurred words.
  - Per-line tempo changes: they sounded robotic.
  - ElevenLabs library voices: blocked on the free plan through the API.
- **Owner voice feedback:**
  - "Aman looks good"
  - "Aman voice is good but the words are not clear"
  - "Somewhere the voice feels like robot and somewhere too fast and some too slow"
  - "0.40-0.50 seconds feels like robot"
  - "1:06 - 1:12 worst robotic"
  - "speed up things and voice little"
  - **Never the owner's own cloned voice.**

**GPU (RTX 3050, 4 GB)**
- IndicF5 voice synthesis runs on the GPU.
- **Whisper runs on the GPU via `asr.py`:** the NVIDIA cuBLAS/cuDNN wheels, with their DLL folders registered on
  Windows. It's 7.4× faster than CPU int8 (6.6 s vs 49.1 s for three lines), with a CPU fallback.
- Drawing and x264 stay on the CPU. The GPU encoder is faster but lower quality at the same bitrate.

**Music: `motion/audio.py` `doc` bed**
- Pad chords at about 180-900 Hz, so phone speakers carry them, plus a soft sub-bass and a muted eighth-note
  pulse. Each video gets its own key and progression.
- Level: about 17 dB under the voice in pauses, ducked about 4 dB while speaking.
- `"dip"` events lower it before reveals.
- Mixed to −14 LUFS.

**Photos**
- `stock_search.py` searches Commons, Openverse, Pixabay and Unsplash.
- Cut-outs are made with rembg and checked on beige.
- Each folder has a `credits.json` (file, author, licence, source) and a contact sheet.
- Licences: PD, CC0, CC BY, Pixabay or Unsplash. Never BY-SA, NC or ND. Brand logos are painted out.

**Checks before sending**
- Layout contact sheets: one frame per shot. These caught overflow, empty openings and missing glyphs.
- The Whisper check of every line.
- `bed_level.py`, which measures music vs voice.
- A phone copy under 29 MB, because Remote Control has a 30 MB file limit. The masters go to the owner's Google
  Drive.

## F. Mistakes and lessons
1. **Repeated placeholder pictures and slow cuts** got rejected. Fix: one new literal picture every ~3 s, cut on the
   word, and a contact-sheet check before rendering.
2. **Per-line tempo** (0.88-1.35×) made the voice sound uneven and robotic. Fix: one tempo for the whole video.
3. **Widening the pitch** for expression blurred words (word-error rate rose from 32% to 44-51%). Instead, re-take
   and keep the liveliest clear take.
4. **The voice felt slow** although words per second matched Mayank's. The real cause was long pauses (median
   0.82 s vs his 0.52 s). Measure syllables per second and pauses on both, then fix the pauses.
5. **The music was inaudible.** It sat about 27 dB under the voice and below 300 Hz, which phones can't play. Fix:
   voice the bed above 300 Hz, about 17 dB under, with lighter ducking.
6. **A font glyph was missing:** "≠" rendered as "=" in Anton and flipped the meaning. Use words instead of symbols.
7. **A cue word matched inside another word:** "सो" matched in "सोचो". Pick a cue word that is unique in the line.
8. **The hook word must show at frame 0:** the ghost fade started at 0, so set it to start before 0.
9. **I misread the owner's credit rule** as "avoid credits". Re-read the exact words, and fix the rule note when
   corrected.
10. **Automated hook and caption scorers misled us** for this genre. Validate any scorer against real views before
    trusting it.
11. **The ant reel's hook deflates** (the "you" turns out false). Make the second person true, and name the subject
    early.
12. **Photo search took over an hour** for 35 subjects. Give the search agent a time box, and allow CC BY.
13. **Instagram auto-disabled a brand-new account** right after it was created. Several new accounts on one home
    Wi-Fi is a known trigger. The fix is a video-selfie appeal, then no more new accounts; add accounts from inside
    the app and warm them up for 1-2 days before posting.
14. **Glyphs and text:** keep on-screen text English uppercase (Anton) and the narration in Devanagari for the voice.
    Write numbers in words for the voice ("तीन सौ तैंतालीस").

## G. What we'd copy into the doctor channel first
1. Hook template: "Socho, [a contradiction about the viewer's own body or life] ... [escalate] ... ye koi movie
   nahi, sach hai ... [name by 12 s]". Frame 0 shows one subject and a ghost → red key word.
2. The rabies shape for health topics: "the cure exists, so why do people still die?", with a re-hook at 55%, then
   myths struck through, then a ✅ what-to-do list, then a YES/NO ending.
3. A literal picture every ~3 s, one recurring metaphor, and slate backgrounds for "inside the body".
4. Voice and music settings: even pace, reveal pauses, a music bed 17 dB under the voice above 300 Hz with dips.
5. Covers inside the 3:4 crop; post on Instagram first; captions as in D5.
