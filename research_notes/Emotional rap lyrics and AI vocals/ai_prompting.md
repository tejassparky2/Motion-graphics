# Prompting AI music generators (Gemini/Lyria, Suno, Udio) for emotional, clearly delivered vocals

Research date: 24 Oct 2026. Labels: **[OFFICIAL]** is Google / Suno / Udio's own documentation. **[COMMUNITY]** is a third-party guide, blog or forum post, so treat it as practitioner folk wisdom, not a spec. **[UNCERTAIN]** means the item is unverified or the sources conflict.
Access limits: Reddit (r/SunoAI, r/udiomusic), Medium and GitHub search were blocked from this environment, so the Reddit-sourced tips below are second-hand: they come from blogs that cite Reddit, not from threads I read. The official Udio help center article and Suno's Notion metatag page could not be loaded.

## Q1. What does Google officially document for Lyria / Gemini music generation (2026)?

### Takeaway
Google documents a simple formula: genre/era, mood, instruments, tempo, vocal description, then lyrics. Put the word "Lyrics:" before your own lines, keep lyrics short for short tracks, use [Verse]/[Chorus]/[Bridge] tags or timestamps, and write "instrumental" only when you want no vocals. Google documents nothing on negative prompts, pronunciation or phonetic spelling, pause control, or editing a single section. Generation is single-turn and non-deterministic, so in practice you get a better take by re-rolling the generation, not by editing it.

### Cited Findings
**Timeline and availability [OFFICIAL]**
- Lyria 3 launched in the Gemini app on **18 Feb 2026** with 30-second tracks, auto-generated lyrics ("No need to provide your own lyrics!"), and "more creative control over style, vocals, and tempo". It is for users 18+, in English, German, Spanish, French, Hindi, Japanese, Korean and Portuguese, and Google AI Plus/Pro/Ultra subscribers get higher limits. — [Google blog, 18 Feb 2026](https://blog.google/innovation-and-ai/products/gemini-app/lyria-3/)
- SynthID: every track carries "SynthID, our imperceptible watermark for identifying Google AI-generated content". — [Google blog, 18 Feb 2026](https://blog.google/innovation-and-ai/products/gemini-app/lyria-3/). Users can upload an audio file and ask Gemini whether Google AI made it. — [9to5Google, 18 Feb 2026](https://9to5google.com/2026/02/18/gemini-app-music-lyria-3/)
- Artist names: the model is "designed for original expression, not for mimicking existing artists"; a named artist is used only as broad inspiration for a similar style or mood. — [Google blog](https://blog.google/innovation-and-ai/products/gemini-app/lyria-3/); [9to5Google](https://9to5google.com/2026/02/18/gemini-app-music-lyria-3/). Requests for specific artist voices or copyrighted lyrics are blocked by safety filters. — [Gemini API music generation docs](https://ai.google.dev/gemini-api/docs/music-generation.md.txt)
- **Lyria 3 Pro reached the Gemini app in March 2026** (25 Mar, paid tiers) and was **expanded on 9 Apr 2026** (rollout from 8 Apr) to more tiers, including consumer Google AI Plus. It makes tracks "up to three minutes long" and responds to requests for "intros, verses, choruses, and bridges". — [Workspace Updates, 9 Apr 2026](https://workspaceupdates.googleblog.com/2026/04/expanding-access-to-longer-musical-tracks-in-the-Gemini-app.html)
- Gemini Help Center (current): open Upload & tools → Create music. "For a full track, switch the model to 'Pro'". There are dropdowns for **length (short ≈1 min / full ≈2–3 min)**, **whether the track has vocals**, and genre. Output is MP4 (with cover art) or MP3. Requirements are 18+, signed in, and Keep Activity on. Lyria has track-creation limits that refresh. The page does not say whether you can supply your own lyrics. Its prompt tips: start with a verb (write/compose/create), name the genre, optionally name instruments, and describe the subject, what it's doing, and the setting. — [Gemini Apps Help](https://support.google.com/gemini/answer/16901237)

**Prompt craft in the Gemini app [OFFICIAL]**
- Six tips (23 Feb 2026): begin with text; upload an image or video; define genre and era (blending allowed); add instruments, song dynamics (e.g. a quiet build into a loud chorus) and vocals (sex, range, texture, layering); if you name no instruments, Lyria picks them from the genre; write your own lyrics by putting **"Lyrics:" before your lines and keeping them short**, with **background singers in parentheses**, or give a theme and let Lyria write them. The post assumes the original 30-second limit ("keep them brief"). — [Google blog, 6 tips](https://blog.google/products-and-platforms/products/gemini/tips-prompting-lyria-3/)

**Prompt craft in the API / Vertex (Lyria 3 / 3 Pro / 3.5) [OFFICIAL]**
- Google Cloud's "Ultimate prompting guide for Lyria 3 models" (7 Apr 2026) gives the framework **[Genre and style] + [Mood] + [Instrumentation] + [Tempo and rhythm] + [Vocal style & language] + [Lyrics]**, and says to "provide your exact lyrics in quotes for the model to perform". — [Google Cloud blog](https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-lyria-3-pro)
  - Own lyrics: "write the "Lyrics:" before the lines you want the model to sing."
  - Vocals: specify male or female and the range ("commanding baritone vocals", "clear and high soprano range"), the texture ("gravelly", "soulful", "breathy"), the delivery ("e.g. rapping"), and dynamic change ("calmer and quieter as the track progresses"). For backing vocals, "mention where you want the backing vocals in the prompt".
  - Mood: "Describe the emotional intent, for example, 'tense and suspenseful'"; "Use adjectives to create a clear description."
  - Tempo: "a fast, energetic pace with a driving beat" / "A slow, swaying tempo". The guide uses descriptive words, not a BPM parameter.
  - Timestamps workflow: `[00:00] ... [00:15] ... [00:30] A male lead vocalist begins rapping a confident verse...` for timed genre shifts or video scoring.
  - Instrumental: "write in the prompt 'instrumental'" (the only exclusion mechanism mentioned).
  - Lyria 3 makes 30 s clips; Lyria 3 Pro "supports compositions up to three minutes long". Vocals are supported in 8 languages; specify the language, e.g. "singing in Japanese".
- The Gemini API Music Generation guide (fetched 24 Oct 2026) now lists **Lyria 3 Clip** (`lyria-3-clip-preview`, always 30 s, MP3) and **Lyria 3.5** (`lyria-3.5`, "a couple of minutes", with verses, choruses and bridges; duration steered by the prompt or by timestamps; MP3 by default, WAV optional; 44.1 kHz stereo; up to 10 images as input). — [Gemini API docs](https://ai.google.dev/gemini-api/docs/music-generation.md.txt)
  - Tips from that page: "Mention instruments, BPM, key, mood, and structure for the best output"; use `[Verse]`, `[Chorus]`, `[Bridge]` tags; **"Separate lyrics from instructions."** Timed sections use the form `[0:00 - 0:10] Intro: ...`.
  - Language: "To generate a song with French lyrics, write your prompt in French"; the model adapts vocal style and pronunciation to the language.
  - Instrumental: "Instrumental only, no vocals."
  - The response returns the generated lyrics and song structure as text, along with the audio.
  - Limits: **"Iterative editing across multiple prompts isn't supported"** (single-turn); outputs vary even with identical prompts; Lyria 3.5 duration is influenced, not fixed. The guide recommends iterating with the Clip model before a full song.
  - All audio carries a SynthID watermark, "imperceptible to the human ear".
  - The page documents no negative-prompt field and no BPM or key parameter; BPM and key go into the prompt text.
- **Lyria RealTime is instrumental only** ("The model generates instrumental music only"). It has weighted prompts, guidance (0–6), BPM (60–200), density, brightness, scale, mute_bass/mute_drums, and a `VOCALIZATION` mode that treats vocalisations "as another instrument" (no lyrics). Output "is always watermarked". — [Lyria RealTime docs](https://ai.google.dev/gemini-api/docs/realtime-music-generation)

### Inferences
- **Instrumental-only results in Gemini** most likely come from (a) the Vocals dropdown in the app set to no vocals, (b) the word "instrumental" or a beat/lo-fi wording in the style text, (c) lyrics not marked with "Lyrics:", so the model reads them as description, or (d) a Lyria RealTime-based tool (always instrumental). The fix is to set Vocals on, put "Lyrics:" right before the lines, and state the singer explicitly ("a male rapper with a raw, emotional delivery"). This is inferred from the official docs above, not documented as the cause.
- **Words like "cry" sung as "lie"**: Google offers no pronunciation control. The documented levers are writing the prompt in the target language, separating lyrics from instructions, short lyrics, and re-rolling, since output is non-deterministic and nothing can be edited in place. The Suno-community tricks in Q2 (respelling, giving a word its own phrase) are untested on Lyria **[UNCERTAIN]**.
- With a 30-second or ~1-minute short track, a full verse plus chorus is likely too many words, so the model rushes; Google's own advice is "keep them short".
- Pick the Pro model / full length when the lyrics need room to breathe.

### Gaps
- No official Google guidance on punctuation for pauses, syllable counts, phonetic spelling, emotion tags inside lyrics (e.g. [Whispered]), or negative prompts in the Gemini app.
- The Gemini Help page does not say whether the app sings user-supplied lyrics verbatim; the blog tips imply it does ("Lyrics:"), but how faithfully is not documented.
- The Lyria 3.5 model pages appeared in search, but I did not find an announcement date for Lyria 3.5 or confirm whether the Gemini app uses 3 Pro or 3.5 now **[UNCERTAIN]**.
- Exact usage limits per tier are unpublished.

## Q2. Suno and Udio prompt craft: tags, styles, exclusions, pronunciation, pauses, takes

### Takeaway
Suno's official docs are thin: the Exclude field is documented, and tags are described as guidance rather than commands. Most technique is community lore. The most repeated advice: keep the style prompt short with one emotional direction; describe the voice's texture, not just its gender; use short lines for intimacy; use section-level tags like [Whispered] and [Spoken Word]; respell only the words that fail; spell out numbers and acronyms; add commas or line breaks where words get rushed; fix single sections with Replace Section; and generate many takes, then pick one.

### Cited Findings
**Suno: official**
- Exclude: in Custom Mode, open Advanced Options; the Exclude field is first: "Enter any information (instruments, etc) that you do not want in your track." Thumbs up/down feedback is encouraged. No date is shown. — [Suno Help Center](https://help.suno.com/en/articles/3161921)
- Each generation returns **two versions**; Custom mode takes lyrics (your own or generated), style, persona (beta at the time) and title; Extend expands an uploaded clip you own the rights to. Learn Prompting (Feb 2025, may be dated) found lyrics written with an external LLM matched the theme better than Suno's generator. — [Learn Prompting, 7 Feb 2025](https://learnprompting.org/blog/guide-suno)
- I could not open Suno's own Notion "Using Metatags" page (it rendered empty). A search snippet says it describes metatags as guiding prompts that are not themselves sung, and its list as "far from exhaustive" **[UNCERTAIN: snippet only]**. — [Suno Notion](https://suno-ai.notion.site/Using-Metatags-34944efe09ec41d693e314f13af44695)

**Suno: community meta-tag lists [COMMUNITY]**
- Structural tags: [Intro], [Verse], [Chorus], [Bridge], [Outro]. Vocal tags: [Male singer], [Female singer], [Whispers], [Echoing vocals], [Harmonized chorus], [Announcer]. Sound-effect tags: [Applause], [Silence], [Static], [Censored]. Prompt template: "A [mood] [genre] song with [instrumentation]. Features a [vocal style] with [specific elements]." — [Learn Prompting](https://learnprompting.org/blog/guide-suno)
- AceTagGen "Vocal Trick Sheet" (11 Apr 2026; the author's own tests, "results may vary"):
  - **[whispered]** is "One of the most reliable tags in SUNO" and works best section-level, paired with short lines.
  - **[spoken word]** switches to speech while "SUNO maintains the backing music".
  - Use **one tone descriptor per prompt**; two can blend, three or more "dilute the signal".
  - "Short lines give the AI less syllabic material per phrase, naturally producing a more restrained, intimate delivery."
  - Ellipses / broken sentences make the AI "pause and hesitate naturally".
  - Hyphens inside a word ("lo-o-ove" style) stretch the vowel into melisma; keep stutters to 2–3 repetitions.
  - Duets are unreliable; adding "male and female vocals" to Style helps.
  - [acetaggen.com](https://acetaggen.com/blog/vocal-trick-sheet-make-suno-sing-like-you-imagine)
- Tags are influences, not guaranteed commands, and over-complex tags can get sung as lyrics. — [Jack Righteous meta tags guide](https://jackrighteous.com/de-gb/pages/suno-ai-meta-tags-guide) (search-result summary; page not opened in full **[UNCERTAIN]**)

**Suno: pronunciation, pauses and rushed words [COMMUNITY]** — all from the Jack Righteous pronunciation guide (first published 24 Sep 2025, updated 15 Aug 2026), [jackrighteous.com](https://jackrighteous.com/de-gb/blogs/guides-using-suno-ai-music-creation/suno-v5-multilingual-english-pronunciation-guide):
- "Do not rewrite a word before it actually fails". Respell only the failing word and keep that spelling identical everywhere. Change one thing per test.
- Acronyms: `A-I`, not `AI`. Numbers: write "twenty twenty-six", not "2026". Syllable spelling for misgrouped words: "Care-uh-BEE-un".
- If a word is rushed into its neighbour, "add a comma or line break" or give the word its own short phrase. If a correct word is rushed, "Shorten the surrounding lyric." Capitals, hyphens and extra vowels "can influence a performance, but results vary". Avoid formatting so extreme that it "becomes part of the performance".
- Fix one bad word with Edit Lyrics / Replace Section on that region only; "changing displayed lyrics alone does not rewrite existing audio".
- Multilingual: one language per section, labels like `[Verse – Spanish]` as an experiment, native script first, and check with a fluent speaker. A reader comment says switching language mid-verse is "not always consistant".
- Suno itself publishes no phonetic syntax, so respelling is experimentation, not a documented feature (same source).

**Suno: style prompt length, emotion, Exclude [COMMUNITY, second-hand Reddit]**
- An r/SunoAI roundup says the most-repeated tip was to keep the style prompt under ~100 words and lyrics around 100–120 words, because past that Suno treats parts as optional. It also advises limiting voice switches to ~4–6 per song and not stacking 3–4 metatags on one line. "Male vocals" alone is not enough; stack 2–3 texture words instead. — reported via search summary of [Medium r/SunoAI roundup](https://medium.com/@aitooldiscovery/suno-reddit-tips-and-prompts-what-r-sunoai-users-actually-do-65b59d51bcad) (page returned 403 when opened, so these are **[UNCERTAIN]**, not verified)
- Exclude is "guidance, not a surgical mute button": keep the list short, pair it with a positive replacement in Style, and don't use minus signs (updated Jul 2026). — [Jack Righteous negative prompting guide](https://jackrighteous.com/es/blogs/guides-using-suno-ai-music-creation/negative-prompting-suno-v5-guide) (search summary **[UNCERTAIN]**)
- Suno's current toolset (reported as V6) includes Extend, Cover, Replace Section, crop/fade/rearrange in a Song Editor, and Personas for a consistent voice across songs. — [Jack Righteous Replace Section guide](https://jackrighteous.com/en-gb/blogs/guides-using-suno-ai-music-creation/suno-replace-section-guide) (search summary; version naming **[UNCERTAIN]**)

**Udio [COMMUNITY]**
- By default Udio rewrites prompts. **Manual mode** passes your prompt through unchanged but accepts tags only (no free-form text), so pair it with custom lyrics or the lyrics come out generic. Structure tags such as [Verse], [Chorus], [Hook], [Drop]; parentheses for backing vocals; special descriptors "not always reliable". Udio makes two versions per input, and more iterations are usually needed. — search summaries of [allthings.how](https://allthings.how/how-to-create-realistic-songs-with-udio-ai/) and [Pulse Pixels Substack](https://pulsepixels.substack.com/p/guide-to-udio-music-creation) **[UNCERTAIN: not opened]**
- One r/udiomusic user reported that manual-mode generations "sucked" for lyrics, and that turning manual off and just giving the lyrics got the result on the first try (July 2024; a single anecdote, mirror page 503'd, seen in a search snippet only). — [r/udiomusic thread](https://www.reddit.com/r/udiomusic/comments/1dwudzb/lyrics_and_udio/) **[UNCERTAIN]**
- Udio's official "Prompt Like a Master" help article exists per an aggregator, but I could not open it. — [skillsetcourse listing](https://skillsetcourse.com/class/udio-prompt-like-a-master)

### Inferences
- Across all three tools, the practitioner consensus maps onto the creator's problems:
  1. **Misheard words**: put a rhyme-critical word like "cry" at the end of a line, on its own, followed by a comma or full stop. Avoid near-homophones in the same rhyme slot ("cry" next to "lie" or "my" invites a swap). If one word fails, respell only that word and re-roll.
  2. **Rushed pauses**: fewer syllables per line, line breaks where the breath should go, commas or ellipses, and short punchy lines for emotional peaks.
  3. **Generic delivery**: one clear emotion word plus 2–3 voice-texture words ("raspy, breathy, strained"), dynamic direction ("quiet, almost spoken verse; chorus breaks open"), and a section tag such as [Spoken Word] / [Whispered] where Suno is used.
- Suno has section-level repair (Replace Section); Gemini/Lyria is documented as single-turn. So when lyric precision matters, Suno/Udio give more control, and with Gemini the only remedy is more takes.

### Gaps
- No primary Reddit threads could be read (blocked), so "community consensus" here is mediated by blogs that may be commercial.
- No official Suno documentation of the meta-tag vocabulary, punctuation effects, or syllable guidance was reachable.
- No controlled tests of syllables-per-line versus intelligibility were found for any tool.
- No GitHub prompt-guide repos could be verified (GitHub search API blocked in this session).

## Q3. Why AI vocals sound generic or less emotional than human reference songs, and the fixes people report

### Takeaway
Reviewers and mix engineers say AI vocals come out loud and even, dry and detached, artifact-prone, and pulled toward the "average" of a requested emotion. Reported fixes are on both sides: at the prompt (fewer words, a single strong emotion, explicit dynamics) and after generation (WAV export, stems, light cleanup, moderate compression, shared reverb, or replacing the AI vocal with a real singer). There is no controlled study isolating the cause, so the causes are plausible explanations, not established findings.

### Cited Findings
- A Dubspot mixing guide (12 Jun 2026) on why AI vocals sound flat:
  - Generated and separated stems carry "digital residue": hiss, metallic ringing, watery high end, exaggerated sibilance.
  - AI vocals "often sound loud and even, with the life squeezed out of them" and "often sound dry and detached".
  - Fixes: export WAV, not MP3; light de-noise and notches ("aggressive cleanup can hollow out a stem"); high-pass and cut 200–400 Hz boxiness; tame 2–5 kHz harshness; de-ess at 5–8 kHz; compress only moderately (2:1–4:1, 2–4 dB of gain reduction, since heavy compression on an already flat vocal makes it lifeless); add reverb/delay for shared space.
  - [Dubspot](https://blog.dubspot.com/mixing-ai-generated-stems-2026)
- Suno stems: Pro/Premier plans can split a song into up to 12 stems; free users get only the stereo mix and must use a separate separation tool. Set a manual BPM before extracting so stems line up in a DAW. — search summaries of [RoEx guide](https://www.roexaudio.com/blog/how-to-mix-and-master-suno-stems) and [Dubspot export guide](https://blog.dubspot.com/export-ai-stems-to-your-daw-2026) **[UNCERTAIN: not opened]**
- Critic views (search summaries, pages not opened **[UNCERTAIN]**):
  - One review calls Suno vocals "technically brilliant but soulless": consistently polished, with reverb and harmonies even when told otherwise. — [digitrendz](https://digitrendz.blog/newswire/artificial-intelligence/51784/sunos-ai-music-generator-technically-brilliant-but-soulless/) (403 when opened)
  - A Medium guide says Suno responds better to concrete instructions (tempo, key, vocal style, imagery) than to vague mood words. — [Medium](https://medium.com/@adnanhaiderarwriter/suno-ai-is-not-working-the-way-you-expected-heres-why-and-how-to-fix-it-ade7e1281d69)
  - A Gearspace commenter argues the model samples statistically, so emotional impact is incidental. — [Gearspace](https://gearspace.com/threads/introducing-suno-studio.1455850/)
- Prompt-side fixes:
  - Short lines produce restrained, intimate delivery (AceTagGen).
  - One tone word, because competing emotions cancel into flat (AceTagGen).
  - Write explicit vocal dynamics such as "start out confident but get calmer and quieter" ([Google Cloud](https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-lyria-3-pro)), or a quiet build into a loud chorus ([Google 6 tips](https://blog.google/products-and-platforms/products/gemini/tips-prompting-lyria-3/)).
  - Shorten crowded lines ([Jack Righteous](https://jackrighteous.com/de-gb/blogs/guides-using-suno-ai-music-creation/suno-v5-multilingual-english-pronunciation-guide)).
- Lyria docs encourage putting BPM and key in the prompt ([Gemini API docs](https://ai.google.dev/gemini-api/docs/music-generation.md.txt)), and Lyria RealTime has a hard BPM control (60–200) ([RealTime docs](https://ai.google.dev/gemini-api/docs/realtime-music-generation)). Writing lyrics to a known BPM therefore lets you count syllables per bar.

### Inferences
- Dense lyrics are probably the single biggest cause of rushed, generic rap delivery. A model squeezing too many syllables into a bar has no room for pauses, emphasis or breath. Reference human rappers leave rests, stretch key words and vary their dynamics, and the reference songs the creator likes almost certainly do this.
- A practical syllable budget: at ~90 BPM, one 4/4 bar lasts ~2.7 s. Comfortable emotional rap is roughly 8–12 syllables per bar, and fast double-time 16+. (My calculation and rule of thumb, not a sourced figure **[UNCERTAIN]**.)
- The mix-side causes (over-even loudness, dry sound, artifacts) are partly fixable with stems and a light mix. The "averaging toward the middle of the emotional range" is a model property, and the reliable workaround reported is using a real singer or rapper over the AI instrumental, or replacing the vocal.

### Gaps
- No peer-reviewed listening study specifically on emotional expressiveness of Suno, Udio or Lyria vocals was found.
- No official statement from Google, Suno or Udio on why vocals default to polished or even.

## Q4. Concrete good vs bad prompt examples

### Takeaway
Official Google examples show the shape of a good prompt: genre plus era, a mood, named instruments, a tempo description, a specific voice (sex, range, texture), a dynamic arc, and then "Lyrics:" or a theme. Thin prompts ("a relaxing beach melody") are the documented "bad" end. Few sources show side-by-side tested results.

### Cited Findings
- Official good examples:
  - Jazz ballad: "A smooth, moody jazz ballad featuring piano and upright bass. The vocals should be a female singer with a breathy, soulful soprano range. The vocal pattern should start out confident but get calmer and quieter as the track progresses..."
  - Timestamped hip-hop/gospel: "[00:30] A male lead vocalist begins rapping a confident verse about overcoming life's challenges..."
  - Instrumental lofi ending in "**Instrumental**."
  - [Google Cloud prompting guide, 7 Apr 2026](https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-lyria-3-pro)
- Gemini app examples: a '90s skate punk track about asking a roommate to do the dishes ("high energy, fast drums"); an Afrobeats family-meal song with a West African singer. — [Google 6 tips](https://blog.google/products-and-platforms/products/gemini/tips-prompting-lyria-3/) (via search snippet; tips confirmed on the page). The Help Center gives "Compose a lo-fi hip-hop beat with a chill, melancholic vibe and a simple piano melody." — [Gemini Help](https://support.google.com/gemini/answer/16901237)
- Thin versus structured: Learn Prompting contrasts "a relaxing beach melody" with a prompt covering genre, mood, instrumentation/production and vocal preferences. — [Learn Prompting](https://learnprompting.org/blog/guide-suno)
- The Udio anecdote (manual tags only gave bad lyric results, while plain lyrics without manual mode worked first try) is the closest user-reported A/B found. — [r/udiomusic](https://www.reddit.com/r/udiomusic/comments/1dwudzb/lyrics_and_udio/) **[UNCERTAIN]**

### Inferences
Below is a template for an emotional rap prompt in Gemini/Lyria, synthesised from the official framework. It is not a tested example.

> Emotional, melancholic hip-hop ballad, 2010s style, around 80 BPM, minor key. Sparse piano, soft 808s, light rain ambience. A male rapper with a raw, slightly raspy, breathy voice. Verses are close-mic, half-spoken and unhurried, with clear pauses between lines. The chorus is sung softly, then opens up with backing vocals on the last line. Singing in English.
> Lyrics:
> [Verse] … (short lines, one breath each; the key word ends the line)
> [Chorus] … (identical every time it repeats)

- Bad pattern, by inference: long run-on lines; several moods at once ("happy, sad, angry, epic"); lyrics pasted with no "Lyrics:" marker; a full 3-minute lyric sheet in a 30-second or 1-minute short track; artist names expected to clone a voice (Google treats them only as loose inspiration).
- Workflow: make 4–10 takes per prompt and pick the best (all three tools are non-deterministic). Check intelligibility by ear or with speech-to-text, since that is what catches "cry"→"lie". When one word fails, change only that word or line on the next take.

### Gaps
- No verified, user-documented before/after pairs for Lyria lyric intelligibility were found; most good-versus-bad material is Suno-specific and comes from commercial blogs.
