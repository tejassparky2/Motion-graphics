# Chatterbox Turbo voice tags: what works (tested 14 Oct 2026)

**Source of the tag list:** Turbo's own tokenizer (`added_tokens.json` in ResembleAI/chatterbox-turbo) has 19 tags.
The model card documents only a few sound tags ([cough], [laugh], [chuckle]); its example puts the tag inline exactly
where the sound happens ("calling you back [chuckle], have you got one minute..."). Third-party guides (fal.ai) say to
put tags at natural boundaries and use them sparingly, because overuse sounds theatrical.

| Kind | Tags | What our test showed |
|---|---|---|
| Sound | [laugh] [chuckle] [sigh] [gasp] [sniff] [groan] [cough] [clear throat] [shush] | Real sound, but **only on some takes** (e.g. [gasp], [sniff], [chuckle] before a line: 1 of 2 seeds; [chuckle] after a line: 2 of 2, ~1.1 s). Whisper sometimes writes the laugh as "Heh". |
| Mood | [angry] [fear] [surprised] [whispering] [dramatic] [narration] [crying] [happy] [sarcastic] [advertisement] | **Undocumented and weak.** No real whisper (breathiness unchanged); [angry]/[dramatic] read ~25% slower and more emphatic; the others change little. Use lightly, never rely on them. |

Test: 17 variants x 2 seeds on lines from the crocodile video, measured with Whisper medium (words), pYIN (pitch),
RMS and spectral flatness. Tags are never read out as words.

**Characters:** Turbo can take the timbre of a short reference clip. We use a ~9 s clip of a synthetic Kokoro voice
(am_onyx for a deep crocodile, af_heart for the mother): words stayed clear (Whisper medium, 6/6) and the pitch range
was 16-33 semitones against 5-9 for the stock narrator, i.e. far more expressive. Nobody real is cloned.

## How to use them in a script
- Markup: write the tag on its own, e.g. `"[sniff] You will not give my child back!"`. It is voiced with the next
  word (or the last word at the end of a line), never shown in captions, and dropped by Kokoro/the owner clone.
- Put a sound where a person telling the story would make it: before a line for a reaction ([sniff], [gasp], [sigh]),
  after a line for a reaction to what was just said ([laugh], [chuckle]). One tag per line at most; 4-6 per video.
- Keep logic/explanation lines plain (clarity first).
- The render re-makes a tagged take (up to 5 tries) until Whisper medium hears the words right AND the sound is
  there (`voice._sound_ok`); it warns if a sound never came.
- Render: `NARRATOR_ENGINE=clone CLONE_MODEL=turbo python render.py --video NAME`; characters need
  `turbo_ref="<kokoro voice>"` in `voice.SPEAKERS`.

Sources: https://huggingface.co/ResembleAI/chatterbox-turbo , https://blog.fal.ai/chatterbox-turbo-is-now-available-on-fal/

## Update 15 Oct 2026: tags with character reference voices (Milo series)
Tested 3 takes each with the Kokoro-reference voices (Milo am_puck+3, "her" af_nicole, Lily af_sky+5, boy am_puck+6):
- A sound tag **after** the line works far better: "Of me. Sleeping. [sniff]" 2/3, "...breathing. [chuckle]" 2/3.
- **Before** the line it mostly fails: "[gasp] ..." 0/6 for Milo, "[sniff] Are they gone?" 0/3 for the boy;
  "[sigh] ..." 1/3.
- So: put the reaction sound at the end of the line it reacts to; the render retries (up to 5) until the sound is there.
