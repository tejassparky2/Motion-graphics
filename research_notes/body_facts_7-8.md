# Body Facts 7-8: more weird operations

The owner asked for "more weird operations" after videos 5-6. Same format: organs argue during the procedure, the
masked doctor (the owner's cloned voice) names it and explains it in three plain steps, then a joke.

## 7. Rotationplasty — `videos/rotationplasty.py`
- Done mostly for children and teenagers with a bone tumour (usually osteosarcoma) around the knee, sometimes for
  birth defects of the thigh bone (Children's Hospital Colorado; Johns Hopkins Medicine; OncoLink).
- The diseased section (lower thigh bone, knee, top of the shin) is removed; the lower leg is turned 180 degrees and
  joined to the thigh, so the foot points backwards and the ankle works as a knee. The main blood vessels and the
  sciatic nerve are kept so the foot stays alive and can feel and move (OncoLink; Wikipedia, "Rotationplasty":
  https://en.wikipedia.org/wiki/Rotationplasty).
- A prosthetic leg fits over the backwards foot; bending the ankle bends the prosthesis like a knee. Function is
  generally better than an above-knee amputation and many patients run and play sports (Children's Colorado;
  Johns Hopkins). Script stays general: "Many patients can run and play sports again."
- Left out: exact survival numbers (they depend on the cancer, not the operation).

## 8. Fecal microbiota transplant (FMT) — `videos/fecal_transplant.py`
- Used for Clostridioides difficile (C. diff) infection that keeps coming back. C. diff often takes over after
  antibiotics wipe out the normal gut bacteria; it causes diarrhoea that can last weeks (American College of
  Gastroenterology guideline; American Gastroenterological Association; Wikipedia, "Fecal microbiota transplant":
  https://en.wikipedia.org/wiki/Fecal_microbiota_transplant).
- Stool from a screened, tested healthy donor is processed and its bacteria placed in the patient's gut by
  colonoscopy, enema or capsules. The healthy bacteria crowd out C. diff and rebuild a normal gut community.
- Most patients get better: reported cure rates run from roughly 60% after a single treatment to around 90% overall
  (varies by study, route and number of treatments). Script: "most patients get better", no number.
- The US FDA approved the first microbiota products for recurrent C. diff in 2022 (Rebyota, given rectally) and 2023
  (Vowst, capsules). Not in the script; useful for the pinned comment if viewers ask "is this real?".
- Left out: FMT for other diseases (still experimental or disputed).

## Voices
Natural stock voices at speed 0.95, no pitch shift. Rotationplasty: knee `af_heart`, foot `am_michael`, scalpel
`af_bella`, Danny `am_puck`. FMT: colon `af_heart`, germ `am_onyx`, good bacteria `af_nova`, Mike `am_fenrir`, Danny
`am_puck`. Doctor = owner's clone. Whisper medium writes "rotationplasty" as "rotation plasti" (spelling only; the
word is spoken correctly).
