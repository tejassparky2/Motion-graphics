# Emotional acting, camera, sound and music for short procedural 3D animation

Scope: what makes viewers feel happy or sad in 30-120 s low-poly three.js skits (developer boy, Claude block, Codex robot),
translated into parameters a code pipeline can set. Researched 21 Oct 2026. Sources found were often blogs or
summaries; the quality of each is noted inline. Where a source gives frame counts with no frame rate, the ms values
below assume 24 fps (one frame is about 42 ms), and that conversion is mine.

## 1. Animation acting for emotion: what animators and teachers say, and which small behaviours read as feeling

### Takeaway
The sources agree that emotion reads from **visible thinking before action**: the eyes move first, a blink marks every
change of thought, a held pose keeps moving slightly ("moving hold"), and restraint often lands harder than a big
reaction. The face carries most of the emotion, and the timing and direction of eye darts carry the most of all.

### Cited Findings
- John Lasseter (Pixar), SIGGRAPH '94 notes: "All the movements and actions of a character are the result of its thought process." — [Lasseter, "Tricks to Animating Characters with a Computer"](https://education.siggraph.hosting.acm.org/static/HyperGraph/animation/character_animation/principles/lasseter_s94.htm)
- Lasseter: "If the character has eyes, the eyes should move first, locking the focus of its action a few frames before the head." For a quick reaction, "the anticipation of the eyes leading the action should be just a couple of frames"; bigger decisions get more lead time (paraphrase). — [Lasseter SIGGRAPH '94](https://education.siggraph.hosting.acm.org/static/HyperGraph/animation/character_animation/principles/lasseter_s94.htm)
- Lasseter on holds: "in 3-D computer animation, as soon as you go into a held pose, the action dies immediately." "To combat this, use a 'moving hold.'" "Instead of having every part of the character stop, have some part continue to move slightly in the same direction". — [Lasseter SIGGRAPH '94](https://education.siggraph.hosting.acm.org/static/HyperGraph/animation/character_animation/principles/lasseter_s94.htm)
- AnimSchool (instructor Scott McWhinnie) breaks moving holds into four things: momentum carried from the previous move, breathing (chest/shoulder shifts), eye darts, and the head following the body's direction. — [AnimSchool, "Animating Nothing: Create Moving Holds"](https://blog.animschool.edu/?p=858) (seen through a search summary; McWhinnie is not stated to be a Pixar animator)
- Shawn Kelly (Animation Mentor co-founder), "Blinks Revisited", June 2007: "We blink when we shift our thought process"; "A shift from scared to hopeful? Blink."; "Those blinks will SELL the changes in thought process more than anything else other than possibly overall posture changes."; "We blink to show or hide emotion". — [Animation Mentor newsletter](https://newsletters.animationmentor.com/newsletter/0607/feature_geek.html)
- Shawn Kelly: "The timing and direction of your eye darts will communicate more than almost any other thing in your scene." and "70-80% of the emotion of your character is going to be sold in the face". He also says "wide, unblinking freaked out eyes" sell fear. — [Animation Mentor newsletter](https://newsletters.animationmentor.com/newsletter/0607/feature_geek.html)
- Bloop Animation blink timings (frame counts, no fps stated): regular blink is 2 frames closing, 1 closed, 3 opening; fast blink is 2 closing and 3 opening; long blink is 3 closing, 2 closed, 4 opening; an eye "bat" closes about 3/4 in 1 frame and opens in 2. Eye darts "usually take 3 frames" (start, one in-between, end); a change of point of interest takes 3-4 frames. — [Bloop Animation, blinking tutorial](https://www.bloopanimation.com/blinking-animation/) (no named author)
- Bloop, when to blink: "A head turn (or any fast head movement) would almost always get us to blink"; when "a character realizes something or thinks of a solution to a problem"; and "After a long lingering look a blink can help keep things alive." — [Bloop Animation](https://www.bloopanimation.com/blinking-animation/)
- UAL student course notes repeat the rule that eyelids should travel with the eyeball during darts. — [UAL student blog (search summary)](https://25016249.myblog.arts.ac.uk/?p=229) (low-authority source)
- Ed Hooks, *Acting for Animators* (4th ed.), has a principle titled "Thinking Tends to Lead to Conclusions, and Emotion Tends to Lead to Action". — [Ed Hooks book listing / ToC via search](https://www.abebooks.com/Acting-Animators-Hooks-Routledge/31510906554/bd) (seen only in a search summary of the ToC; not checked in the book)
- A summary page of Hooks' ideas (thinkinganimation.com, not Hooks' own words) gives: "Emotion and movement come from thought."; "We connect to emotion, not information."; "Stifled emotion can hit harder than full display."; "Small, honest 'tells' often beat big reactions."; "Make yelling a late option; control is often quieter."; "Use the moment before your shot to anchor the performance."; "Play an action until something happens that makes you play a different action." — [Thinking Animation: Acting for Animators](https://thinkinganimation.com/acting-for-animators) (secondary paraphrase; treat as unverified wording from Hooks)

### Inferences
Rules for our rig. Values marked "starting point" are my own choices, not from any source.
- **Thought beat before an emotional line**: in this order, (1) eyes dart away 3 frames (~125 ms), (2) a blink on the
  thought change (regular blink 2/1/3 frames, ~250 ms), (3) the head follows the eyes 2-4 frames later, (4) then the
  line starts. That costs about 0.4-0.7 s per beat. Use it only on the 2-3 lines per episode that carry feeling, not
  on every line.
- **Blink scheduler**: drop random blinks. Blink at (a) every head turn larger than ~20° (my threshold), (b) every
  emotion change in the script, (c) after a stare longer than ~2-3 s (starting point). For sad or tired beats, use the
  long blink (3/2/4 frames, ~375 ms) or a lid that falls slowly and only half reopens.
- **Moving holds everywhere**: no channel is ever frozen. On every hold: breathing (chest/shoulder scale, about
  0.25 Hz, i.e. 4 s per breath, is a starting point), a slow drift of 1-2° in the direction of the last move, and a
  micro eye dart every 1-2 s (starting point). The robot gets a hover bob; the block gets a squash "breath".
- **Eyes lead, always**: on any look change, rotate the eyes first, then the head 2-4 frames later, then the torso.
- **Restraint**: on sad beats, a small tell (eyes down, a slow blink, a slight shoulder drop) beats a big gesture.
  Save the large "result" pose for the payoff.
- **Looking away before admitting something**: this matches "we blink to show or hide emotion" and gaze-aversion
  practice, but I found no source that states "look away before admitting" as a rule. See Gaps.

### Gaps
- No primary Keith Lango text on "thinking holds" was found; his old blog/videos did not come up in search.
- No source gave frame-exact timings for a "thought beat before speaking", a head-down/head-up beat, or "eyes
  glistening". The ~0.4-0.7 s beat above is built from the blink and dart timings, not quoted from anyone.
- Richard Williams' *Animator's Survival Kit* and Disney's 12 principles (holds and anticipation) were not fetched
  directly; there are no quotes from them here.
- The Ed Hooks wording is from a ToC listing and a third-party summary, not the book itself.

## 2. Simple-character emotion: how minimal designs show sadness and joy with few controls

### Takeaway
With few controls, emotion is carried by **timing/speed, head angle, and posture**: happy is faster and more upright,
sad is slower with the head down and longer pauses between moves (Pixar's Luxo Jr.). Mouthless designs such as WALL-E
and BB-8 lean on head and eye tilt and on motor timing.

### Cited Findings
- Lasseter on Luxo Jr.: "When a character is happy, the timing of his movements will be faster."; "When he is chasing the ball, he is very excited and happy with all his thoughts on the ball."; then after the ball pops, "As he hops off, his head is down, the timing of each hop is slower, with much more time on the ground between hops." — [Lasseter SIGGRAPH '94](https://education.siggraph.hosting.acm.org/static/HyperGraph/animation/character_animation/principles/lasseter_s94.htm)
- Lasseter: "the timing of the movement of an object defines the weight of that object." — [Lasseter SIGGRAPH '94](https://education.siggraph.hosting.acm.org/static/HyperGraph/animation/character_animation/principles/lasseter_s94.htm)
- WALL-E's binocular eyes: Andrew Stanton got the idea when a seatmate at a baseball game handed him binoculars; NPR's commentary says the big eyes cue viewers to care about the character. — [NPR, "Pixar's Andrew Stanton: Animating From Life"](https://www.npr.org/2008/07/10/92400669/pixars-andrew-stanton-animating-from-life); [Wikipedia: WALL-E (character)](https://en.wikipedia.org/wiki/WALL-E_(character)) (accounts differ on who handed him the binoculars)
- A Pixar designer quoted by Creative Bloq says "a pair of swivelling, zoomable lenses became the 'face' of the character." — [Creative Bloq, "WALL-E: this year's model"](https://www.creativebloq.com/computer-arts/walle-year-s-model-11089200) (search summary)
- A WALL-E essay says that when he felt sad his binocular lenses had to tilt, and that without a smiling mouth for joy they relied on "the timing of his motor functions." — [Deep Focus Review, The Definitives: WALL-E](https://deepfocusreview.com/definitives/walle) (critic's essay, seen through a search summary)
- BB-8: puppeteer Brian Herring says many reactions were built around his own timing, and that head movement is how viewers read the droid's mood; builders used a rod-and-lever puppet for emotional beats because it was "incredibly expressive". — [The AU Review, Supanova interview with Brian Herring](https://www.theaureview.com/watch/supanova-interview-star-wars-puppeteer-brian-herring-talks-bringing-bb-8-to-life-the-han-solo-film/); [Ingenia, "Engineering personality into robots"](https://ingenia.org.uk/articles/engineering-personality-into-robots/) (both seen through a search summary)

### Inferences
Mood presets for each character (my mapping of the Luxo rule onto our controls):
- **Happy**: about 1.2-1.4x faster tween speed (starting point), head up 5-10°, faster idle bob, eyes wide, more
  overshoot/bounce on settles.
- **Sad**: about 0.6-0.7x speed, head pitched down 10-20°, longer holds between moves ("more time on the ground"),
  lids lowered 20-40%, brows' inner corners raised. The Codex robot hovers lower with a slower, smaller bob; the Claude
  block squashes slightly and slows its hops.
- **Codex screen face**: treat the screen eyes like WALL-E's lenses. Tilt the eye shapes (inner ends up for sad),
  make them slightly smaller, and tilt the whole body/head 5-15°. Mouthless joy is shown by a faster, springier
  motion curve, not only by a drawn smile.
- **Transition between moods**: a deliberate slow-down. The Luxo "ball pops" moment is a hold, then the head drops,
  then slower movement. That gives a sad-turn template: hold 0.5-1 s, head drops over ~0.5 s, idle slows.

### Gaps
- I found no primary sources on Baymax, Among Us beans or Kurzgesagt birds; nothing citable was gathered on them.
- The BB-8 material is about puppetry, not keyframe animation, and gives no numeric timings.

## 3. Cinematography for emotion: distance, push-ins, holds, reaction cuts, wide shots, lighting

### Takeaway
Close and extreme close shots raise emotion; a slow push-in shows a character's inner state or a realisation; a
wide shot with empty space reads as loneliness. Warm vs cool light is a rough but widely used mood convention. None
of the cited sources gives push-in speeds or durations.

### Cited Findings
- StudioBinder: push-ins "emphasize or exaggerate the emotions of a scene or character"; "By moving toward a character, a camera push-in shot can reveal the character's state of mind"; on two characters "can emphasize the closeness in their relationship"; pushing toward an object makes the audience "realize it's important"; the push-in "can help indicate growing tension." The page gives no speed, duration or lens numbers. — [StudioBinder, Push-In Shot](https://www.studiobinder.com/camera-shots/camera-movements/push-in-shot/)
- A glossary (not StudioBinder) says a slow push builds intimacy, tension or deepening attention, while a fast push creates urgency or shock. — [Morphic glossary: Push In](https://morphic.com/ai-glossary/push-in) (low-authority)
- StudioBinder on wide shots: "With all of that empty space around the character, we are lead to feel a bit of loneliness and isolation. They feel small because they are shown small." — [StudioBinder, Wide Shot](https://www.studiobinder.com/blog/wide-shot/) (search summary)
- StudioBinder on Spike Jonze: an extreme close-up "can make us feel overwhelming emotion," while an extreme wide shot "conveys isolation". — [StudioBinder, How Spike Jonze shoots movies about loneliness](https://www.studiobinder.com/blog/how-spike-jonze-shoots-movies-about-loneliness) (search summary)
- No Film School: a wide shot "uses scale, distance, and proportions to depict the emotional state of a character"; framed against a vast backdrop "He is at his most vulnerable and isolated"; in *Her*, isolation comes from "off-center framing and wide shots"; "the framing itself becomes an emotion"; "Let it breathe with the character in frame". — [No Film School, "How Wide Shots Create Isolation"](https://nofilmschool.com/when-wide-shots-mean-isolation)
- Adobe suggests starting with wide shots that "gradually transition to close-ups as a character becomes more emotionally vulnerable," and says an extreme close-up on eyes or lips "frequently reveals feelings and emotions that dialogue alone cannot always convey." — [Adobe, Camera shots and angles](https://www.adobe.com/au/creativecloud/video/production/cinematography/camera-shots-and-angles.html) (search summary)
- StudioBinder on colour temperature: it lets you "affect the overall mood of your shot," but the warm/cool split is "rather rudimentary" and "there is always room for interpretation." — [StudioBinder, What is color temperature](https://www.studiobinder.com/blog/what-is-color-temperature/)
- Other guides tie warm light (about 3000K and below) to intimacy, nostalgia and comfort, and cool light (about 6000K and above) to tension, isolation or sterile places; they suggest mixing cool key light with warm practicals. — [Videomaker, Mixed color temperatures](https://www.videomaker.com/article/c03/18939-get-more-dynamic-lighting-with-mixed-color-temperatures); [Atmosfera mag, Warm and cool lights](https://atmosferamag.it/?p=34982) (secondary; conventions, not rules)
- Re-recording mixer Jon Taylor on *Unbroken*: the screen cuts to black, the sound drops out, then a quiet line of dialogue lands, and he said the change in dynamics gave the viewer a pause in the story. — [Variety, Oscar sound editing nominees use silence](https://variety.com/2015/artisans/awards/oscar-sound-editing-nominees-unbroken-american-sniper-use-silence-1201421611) (search summary)

### Inferences
Camera parameters. All speeds are my starting points; no source gave numbers.
- **Shot ladder by emotional intensity**: wide (loneliness/setup), then medium (dialogue), then close-up (feeling),
  then extreme close-up on the eyes (the peak, used once). Follow Adobe's wide-to-close progression across the episode
  so the camera gets closer as the emotion rises.
- **Realisation push-in**: a slow dolly of about 10-20% of the subject distance over 2-4 s with ease-in-out, starting
  just before the thought beat (Section 1) and ending on the blink. Keep fast pushes (under 0.5 s) for shock or comedy.
- **Loneliness shot**: character at a third of the frame or less, off-centre, lots of negative space (an empty desk,
  a dark office), held 2-3 s with no cut; a slightly wider FOV or a pull-back.
- **Reaction cuts**: on the emotional line, cut to the *listener's* close-up and let the speaker's line play over it,
  so the viewer sees the feeling land. (This is standard editing practice; I found no source fetched for it here. Gap.)
- **Lighting cue**: sad/lonely beats get a cooler key (blue monitor light, dim room), and warm beats get a warm practical
  (desk lamp ~2700-3200K look, as the warm/cool guides suggest). A slow shift in key colour over 2-3 s at the emotional
  turn marks the mood change. Rain on a window can serve as both the cool light and the ambience bed (Section 6).
- **Depth of field**: shallow focus on close-ups isolates the face. This is common practice, but no source was fetched
  for it; flagged as unsourced.

### Gaps
- No Pixar camera talk (e.g. Pixar in a Box) or DP interview giving push-in speeds, focal lengths or hold durations was
  found.
- No source on "cutting to the listener's reaction instead of the speaker" was fetched.

## 4. Music: building emotion in 60-90 s, motifs, drop-outs, tempo, mode, instruments

### Takeaway
The research is consistent: **slow tempo + minor mode = sad, fast tempo + major mode = happy**, the effect is
strongest when both cues agree, and tempo outweighs mode when they conflict. Mixed cues give "bittersweet". Pixar's
*Up* montage shows the pattern: one simple, music-box-like theme introduced early, carried by changing
instrumentation, returned in a sadder form, with almost no dialogue. Dropping into silence before the key line is a
recognised contrast device. Mickey-mousing is seen as overused outside comedy.

### Cited Findings
- Hunter, Schellenberg & Schimmack (2010): happiness ratings were higher for fast-tempo and major-key music, sadness
  ratings were higher for slow-tempo and minor-key music, and "mixed emotional responses were elevated for music with
  mixed cues." — [Hunter et al. 2010 (PDF)](https://sites.utm.utoronto.ca/sites/sites.utm.utoronto.ca.glenn_website/files/download/HunterEtAl2010.pdf) (search summary)
- Gagnon & Peretz (2003), as cited in a later review: effects were stronger when mode and tempo agreed; when they
  disagreed, listeners relied more on tempo than on mode. The review lists Juslin (1997) among studies finding tempo
  and mode the most important cues, "with a subtle predominance of tempo". — [Frontiers in Psychology 2013 review](https://frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2013.00417/full) (secondary; the original papers were not read)
- Juslin & Laukka's review (104 vocal-expression studies, 41 music-performance studies) is summarised as finding shared
  sadness cues in speech and music: slow tempo, low sound level, dark/dull timbre, low pitch, small pitch and loudness
  variation, slow tone attacks, legato. — [Buffalo LPC lab, Emotion and Music (PDF)](https://ubwp.buffalo.edu/lpclab/wp-content/uploads/sites/188/2025/04/Emotion-and-Music-REVISED-FINAL.pdf); [iMotions, Emotional prosody](https://imotions.com/blog/insights/research-insights/understanding-emotional-prosody-unveiling-human-emotion-in-speech) (secondary summaries)
- *Up*, "Married Life": it was Giacchino's first piece for the film; he said "We knew that was going to be one of the most difficult scenes in the film." Pete Docter asked for a melody that sounded like it came from a grandmother's music box. The sequence is "almost completely silent" apart from the music, and the themes return through the film with changed timbre. Docter said that if viewers don't love the characters they're "not along for the ride." — [Wikipedia, Up opening sequence](https://en.wikipedia.org/wiki/Up_opening_sequence)
- The *Up* theme is introduced "slow and spare" on "We're in the Club Now", fleshed out in "Married Life", and a sadder version after Ellie's death became the track "Stuff We Did"; reviewers note alternating muted brass and lilting strings representing Carl and Ellie. — [Wikipedia, Up (soundtrack)](https://en.wikipedia.org/wiki/Up_(soundtrack)); [The Playlist review](https://theplaylist.net/?p=7326) (search summaries; fan/critic analysis)
- Silence before a beat: one analysis says *Oppenheimer* uses silence or near-silence "to create contrast and amplify moments of emotional weight"; SoundGirls says silence makes the audience hyper-aware, "especially effective after a film that has been heavily underscored." — [Spettacolo Film](https://spettacolofilm.com/post/the-film-score-doing-half-the-emotional-work-you-never-notice); [SoundGirls, Silence as Sound](https://soundgirls.org/silence-as-sound/) (blogs; search summaries)
- Mickey-mousing is music that tracks on-screen movement beat for beat; it is "somewhat out of favor" in serious films because of overuse, criticised as feeling mechanical or condescending, and still accepted for comedy. — [StudioBinder, Mickey Mousing](https://www.studiobinder.com/blog/mickey-mousing/); [Wikipedia, Mickey Mousing](https://www.Wikipedia.com/wiki/Mickey_Mousing) (search summaries)

### Inferences
Procedural music parameters:
- **Mood presets**: happy is major (Ionian/Lydian), about 100-120 BPM, brighter timbre and faster attacks. Sad/tender
  is minor or modal, about 60-80 BPM, low register, soft attacks, legato, little dynamic change. **Sad-hopeful
  (bittersweet)** is mixed cues on purpose: slow tempo in a major key, or a minor progression resolving to a major
  chord (Hunter et al.'s "mixed cues"). The BPM ranges are a common convention and my starting points; the studies
  cited give direction, not exact BPM.
- **Motif system**: write one 4-8-note motif per episode, or per character for a series. State it plainly and sparsely
  (single notes, music-box or felt-piano timbre) in the first 5-10 s, keep it in the background mid-episode, and
  return it at the payoff in a fuller or changed form (sadder: slower, minor, lower; happier: with a pad/strings
  swell). This follows the *Up* pattern of one theme with changing timbre.
- **Drop-out before the key line**: duck the music to silence (or room tone only) 0.5-1.5 s before the most important
  line, deliver the line dry, then bring the motif back on the reaction shot. Fade out over about 0.5-1 s rather than
  a hard cut, unless a hard cut is the joke.
- **Avoid mickey-mousing** on emotional beats; keep beat-synced stings for comedy only.
- **Instrument palette** for our synth: "music box" (sine plus a high partial with fast decay), "felt piano" (soft
  attack, low-pass, short release), warm pad (detuned saws, heavily low-passed). The music-box choice comes from
  Docter's request; "felt piano/lo-fi = nostalgic" is a convention I found no study for.

### Gaps
- No Berklee or composer source with BPM ranges for "sad/tender" was found; the 60-80 BPM figure is a convention, not
  sourced.
- No sources were fetched on key changes (e.g. a lift at the payoff), "warm" or "nostalgic" timbre perception, or
  felt piano / lo-fi.
- The Juslin/Gagnon/Hunter findings are from secondary summaries; the original papers were not read.

## 5. Voice performance: human vs synthetic, and directing TTS for emotion

### Takeaway
Sad speech is slower, quieter, lower and flatter in pitch, with dull timbre; the pattern is broadly shared with
music. For TTS, punctuation (especially ellipses) controls pauses, tags go immediately before or after the words they
change, and tags work unreliably, so they must be checked. Our own Chatterbox Turbo tests found sound tags appear only
on some takes and mood tags are weak.

### Cited Findings
- Sad vocal expression: "low f0/pitch level and little f0/pitch variability", slow tempo, low sound level. — [iMotions, Emotional prosody](https://imotions.com/blog/insights/research-insights/understanding-emotional-prosody-unveiling-human-emotion-in-speech); [Buffalo LPC lab PDF](https://ubwp.buffalo.edu/lpclab/wp-content/uploads/sites/188/2025/04/Emotion-and-Music-REVISED-FINAL.pdf) (secondary summaries of Juslin & Laukka 2003)
- Caveat: one cross-language study found sadness had the lowest F0 in German and Arabic, but in English and Hindi F0 was *higher* for sadness than for neutral speech, so "low pitch" is not universal. — [JBE Platform chapter (search summary)](https://www.jbe-platform.com/content/books/9789027270740-pbns.241.14kot)
- ElevenLabs v3 prompting guide: "Ellipses (...) add pauses and weight." "Punctuation significantly affects delivery". Tags go "typically immediately before the dialogue segment they modify or immediately after." The listed tags include `[laughs]`, `[laughs harder]`, `[starts laughing]`, `[wheezing]`, `[sighs]`, `[exhales]`, `[whispers]`. Warnings: "Some experimental tags may be less consistent across different voices"; tags "land more readily when the delivery is already in the voice's training data"; a tag "can occasionally be interpreted as a request for a sound effect"; "A serious, professional voice may not respond well to playful tags". v3 does not support SSML break tags. — [ElevenLabs, Eleven v3 prompting best practices](https://elevenlabs.io/docs/best-practices/prompting/eleven-v3)
- Chatterbox Turbo: third-party pages describe inline paralinguistic tags such as [laugh], [cough], [chuckle], placed in the text where the sound happens. — [tts.ai, Chatterbox Turbo](https://tts.ai/voices/chatterbox-turbo/?lang=it) (aggregator, not Resemble's docs)
- Our own test (repo file `out/turbo_tags_research.md`, 14-15 Oct 2026, which cites the model card at https://huggingface.co/ResembleAI/chatterbox-turbo and a fal.ai guide): Turbo's tokenizer has 19 tags. Sound tags ([laugh] [chuckle] [sigh] [gasp] [sniff] [groan] [cough] [clear throat] [shush]) give a real sound "only on some takes". Mood tags ([angry] [fear] [surprised] [whispering] [dramatic] [crying] [happy] [sarcastic]...) are "undocumented and weak"; [angry]/[dramatic] read about 25% slower. A tag *after* a line worked better than before it (e.g. 2/3 vs 0/6). With Kokoro-reference character voices, [chuckle] was sometimes spoken as the word "Chuckle". The rule adopted: one tag per line at most, 4-6 per video, verify with Whisper, and use breath SFX from `motion/audio.py` ("sniff", "gasp_in", "sigh") where tags fail. — local file `/home/user/Motion-graphics/out/turbo_tags_research.md` (internal test results)

### Inferences
- **Emotional line delivery parameters** (our pipeline): for sad lines, slow the take about 10-20% (time-stretch
  without a pitch change, or slow toward the existing 5.5 syl/s target), lower gain about 2-4 dB, add a pre-line breath
  SFX, and add a longer pause before the line (the thought beat). Happy lines: normal or slightly faster, a [chuckle]
  *after* the line. These percentages are my starting points.
- **Hesitation by text**: write ellipses and short fragments ("I... I don't know.") and false starts; per ElevenLabs,
  punctuation is the main pause control when SSML breaks are unavailable. (Whether Turbo honours ellipses as strongly
  is untested.)
- **Non-verbal placement**: put reactions where a person would make them; for Turbo, put them after the line they
  react to; layer real breath/sniff SFX under the take rather than relying on tags; at most one per line.
- **Trailing off / voice crack**: no tag is documented for these; fake them in post (fade the last word's gain, a
  small pitch dip, a breath after).
- Since this channel's audience is partly Indian (Hindi speakers), the cross-language F0 caveat suggests not forcing a
  pitch drop on sad lines. Speed and volume are safer cues.

### Gaps
- Official Resemble AI documentation for the Turbo tag list and placement was not fetched in this session (the repo
  notes cite the HF model card).
- No source was found on "um"/filler words or laughing through a line in TTS.

## 6. Sound design for emotion: room tone, ambience, small foley, silence as a beat

### Takeaway
Walter Murch calls silence "the ultimate metaphoric sound": if sound is withdrawn where it is expected, the audience
fills it with their own feelings. He also says *near*-silence with tiny sounds often works better than true silence.
For us, that means a constant room-tone/foley bed that can be pulled down to a few small sounds at the emotional
moment.

### Cited Findings
- Murch: "The ultimate metaphoric sound is silence." "If you can get the film to a place with no sound where there should be sound, the audience will crowd that silence" "with sounds and feelings of their own making, and they will, individually, answer the question of, 'Why is it quiet?'" "If the slope to silence is at the right angle, you will get the audience to a strange and wonderful place" — [Designing Sound, "Silence"](https://designingsound.org/2011/11/29/silence/) (Murch passage quoted by the blog)
- A commenter on the same post warns that silence is hard to get right and a very short film may be too short to hold a silent stretch. — [Designing Sound, "Silence"](https://designingsound.org/2011/11/29/silence/) (anecdotal comment)
- On *Jarhead*, Murch said suggesting silence often works better when the audience hears the tiniest sounds; he replaced a long silence with small falling-debris sounds. — [NPR transcript](https://www.npr.org/transcripts/4994411) (search summary)
- Murch's approach is described as a total sonic design of music, effects and "expressive silences." — [16:9 interview with Walter Murch](https://16-9.dk/2018/09/interview-with-walter-murch/) (search summary)
- *Unbroken*: a cut to black with the sound dropped out, then a quiet line; the change in dynamics gave "a pause in the story". — [Variety 2015](https://variety.com/2015/artisans/awards/oscar-sound-editing-nominees-unbroken-american-sniper-use-silence-1201421611) (search summary)

### Inferences
- **Always-on bed**: room tone (low-passed noise at about -40 to -50 dBFS, my starting point), plus scene ambience: an
  office HVAC hum, rain on a window for sad/reflective scenes, a soft late-night street for loneliness.
- **Small foley tied to acting**: keyboard clacks while typing, a chair creak on posture changes (it pairs with the
  sad slump), a phone buzz as a story turn, a mug set down as the "decision" beat. Foley marks a thought change the way
  a blink does.
- **The silence beat (Murch's "slope")**: for the key emotional line, (1) about 2 s before it, fade the music out over
  ~1 s, (2) drop ambience down to room tone plus one tiny sound (a clock tick, rain), (3) hold 0.5-1.5 s on the
  listener's face, (4) deliver the line dry, (5) bring the motif back. Use it once per episode; since 30-120 s is short,
  keep the silent stretch under ~2 s (my judgment, following the commenter's warning about short films).
- **Never true digital silence** in a Short: keep room tone or one tiny sound under it (Murch on *Jarhead*).

### Gaps
- No Designing Sound article was found with level numbers (dB) for room tone or ambience in emotional scenes; the
  levels above are my starting points.
- No source specific to rain ambience or emotional foley in animation was found.
