# Body Facts 5-6: little-known operations

The owner asked for operations most people have never heard of (not the familiar kidney/liver ones), in the format
of a reel he sent: organs talk during the operation, a surprising twist ("they used WHAT?"), then the doctor names
the procedure and explains it step by step (the reel: orthotopic neobladder, a new bladder made from small intestine).
Two YouTube references he sent couldn't be downloaded (YouTube's bot check); their titles were read with oEmbed.

## 5. Tooth-in-eye surgery (osteo-odonto-keratoprosthesis, OOKP) — `videos/tooth_eye.py`
- For people blinded by severe damage to the front of both eyes (Stevens-Johnson syndrome, chemical burns, severe
  autoimmune dry eye) when other reconstruction, including a normal cornea transplant, has failed or can't work.
  EyeWiki (American Academy of Ophthalmology), "Modified Osteo-Odonto-Keratoprosthesis":
  https://eyewiki.org/Modified_Osteo-Odonto-Keratoprosthesis
- A single-root tooth, usually a canine, is taken with its surrounding bone, shaped into a plate, and a clear
  polymethyl methacrylate (PMMA, a plastic) optical cylinder is fixed through it (EyeWiki; All About Vision:
  https://www.allaboutvision.com/treatments-and-surgery/vision-surgery/corneal/tooth-in-eye-surgery/).
- The tooth-lens piece is placed under the skin (cheek or below the eye) so tissue grows around it: about 1 month
  (EyeWiki) to 2-4 months (All About Vision); a graft of the cheek's inner lining (oral/buccal mucosa) covers the
  eye's surface; then the piece is put into the eye. Script: "a few months".
- Outcome: EyeWiki reports 78% reaching 20/400 or better, so the script says "see light again", not perfect sight.

## 6. Toe-to-thumb transfer — `videos/toe_thumb.py`
- The big toe or the second toe is moved to the hand to make a new thumb; bone, tendons (extensor and flexor),
  arteries, veins and nerves are joined, the vessels and nerves under a microscope. "Thumb Reconstruction with Toe
  Transfer", PMC3122704: https://pmc.ncbi.nlm.nih.gov/articles/PMC3122704/
- The thumb is "the king of the digits": losing it disables the hand most; the new thumb gives back grip and pinch.
- Donor foot: "the foot functions quite adequately without a full complement of toes"; walking largely unaffected,
  slightly less push-off after a big-toe harvest. Script: "most people still walk normally without that toe".

## Voices
Natural stock voices, no pitch shift, speed 0.95 (eye/hand `af_heart`, tooth/toe `am_michael`, scalpel `af_bella`,
Danny `am_puck`, Mike `am_fenrir`). Every organ/patient line exact on Whisper medium before rendering ("Don't worry,
eye" was heard as "Don't worry, I", so it became "Don't worry. I'm bringing you some help, my friend.").
The doctor is the owner's clone; "osteo-odonto-keratoprosthesis" is spoken in parts via `CLONE_SAY`.

## Ready for later (scripts written and voice-tested, not built yet)
High heels and the feet; how not drinking water causes constipation (from the owner's other two links).
