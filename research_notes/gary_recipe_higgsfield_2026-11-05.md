# "I kill my AI character in every reel": the @everyonemeetgary recipe (owner link, 5 Nov 2026)

Source: a public blog post by @alberteinsteinjr on higgsfield.ai (published 29 Oct 2026). Summary for our use; the
post's full prompts are on the page.

**Results claimed:** 1.2M views, 12K followers, 12 reels in 14 days (Instagram).

## The format
- Gary, a silent 3D intern, tries something adults do (shots, energy drinks, seawater on a raft) in an absurd amount.
- A calm, deadpan narrator explains what happens inside his body, like explaining to a five-year-old.
- He dies at the end (wordless, no gore). The next episode has a new Gary with a higher badge number: "This is Gary.
  Intern number 54. Don't ask about the other 53." The comments ask about the other 53.
- Three ideas: the contrast is the joke (adult, slightly dangerous topic; explanation for a kid); he never talks (one
  silent character, one calm voice); the format writes the next episode (the badge number).

## The six steps
1. **Character in GPT Image:** full-body 3D character on a plain grey studio background, one signature colour (his
   lime-green tie). Style words: muted European 3D animation, matte clay-like materials, soft key light, gentle floor
   shadow, no glossy shine.
2. **Turnaround sheet in Nano Banana:** front, side and back views, so the video model doesn't invent what it can't
   see (his hair went spiky when he turned until every take got this sheet).
3. **Script (Higgsfield "Supercomputer"):** hook in 3 s ("What if [NAME] [absurd amount]?" plus a paradox line that
   names the danger without spoiling it: "The shots won't kill him. The nap afterwards will."); tagline; a dose ladder
   of 4 rungs with a visible counter (each rung: what he feels, one real fact, one literal cartoon picture, one dry
   joke); a re-hook every 10-15 s; a twist (the real danger isn't the obvious one); his death, wordless; one honest
   safety tip; a callback to the opening. Lines of 4-12 words, an emotion tag on each, a shot note next to each.
   Facts checked; the science is what people screenshot.
4. **Narrator in ElevenLabs v4:** one preset voice, stability ~0.2 so it acts, an emotion tag before every line
   ([deadpan], [matter-of-fact], [warmly], [gently]...).
5. **One video take per line in Seedance 2.5 (Higgsfield):** every prompt has the same parts: ACTIVE REFERENCES (what
   each image defines, what is NOT inherited), STYLE (high-end 3D feature film, 12 principles, one continuous N-second
   shot at real speed), LOCATION, LIGHTING, CAMERA (exact framing; chest-up or wider), PHYSICS, numbered RULES (one
   character, two hands, keeps size, hair stays flat, no text anywhere, no cuts, no gore), ACTION TIMING second by
   second with an END STATE for each segment, and HOLD FOR THE FULL TIMELINE.
   Tips: generate each take at the real length of its line; never stretch with slow motion; give the action a 1-2 s
   run-up (the model starts late); keep the camera chest-up or wider (face close-ups get flagged); put all text in
   the edit (generated text comes out as gibberish). Falls work in a side view "pivoting on his heels".
6. **Edit on the voice:** narration first, one take under each line, picture changes on the word; a climbing counter
   sticker ("SHOTS 15 · BAC 0.30"); a big number slam on every fact; music ~12 dB under the voice. Cover = the most
   extreme frame (text-only covers were his weakest).

## What he learned
- His four most-shared episodes are about something Gary puts in his body (1.2-1.6 shares per 1,000 views vs 0.5-1.0).
- Make the number arguable: the top comments argue about the dose.
- "What if" plus a paradox hooks; the most extreme frame as the cover; the lore builds itself; one real safety tip
  gives people a reason to send it to a friend.
- He runs it through Claude with the Higgsfield MCP: a writers' room of agents, four agents generating takes in
  parallel, two auditors checking the cut at 4 fps; topic to first cut in 3-4 hours.

## For us
- We can do steps 3, 4 and 6 here (script with checked facts, Turbo or ElevenLabs narrator with tags, the edit with
  counters and number slams) and write the step-5 prompts in his structure.
- Steps 1, 2 and 5 need image and video models we don't have in this container: the owner generates them (ChatGPT /
  Gemini for images, Higgsfield for Seedance takes), or connects a Higgsfield connector on claude.ai so a session can
  generate takes itself (costs Higgsfield credits).
- Topic care for YouTube's harmful-content rules: prefer "absurd but legal and everyday" (energy drinks, no sleep,
  seawater, too much water, holding breath, cold showers, lightning) over alcohol or drugs; always a real safety tip.
