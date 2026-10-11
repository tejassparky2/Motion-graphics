# Body Facts 19-22: polished batch with step-by-step explanations (scripts approved by the owner)

Owner: "Make next batch with upgraded animation and upgraded explanation". New style: motion.polish / pkit / toons
(see POLISHED_STYLE.md) through `motion/pbody.py` (glossy organs, numbered step cards, tip cards, polished clinic
with the toons doctor and two patients). Every explanation is three numbered steps, then a tip and a warning.
Voices: doctor Kokoro `am_adam`, Mike `am_fenrir`, Danny `am_puck`; organs natural Kokoro voices at 0.95.

## 19. Brain freeze — `videos/brain_freeze.py`
- Cold stimulus headache (sphenopalatine ganglioneuralgia): cold on the palate; vessels constrict then dilate; the
  trigeminal nerve signals it and the pain is referred to the forehead. Harmless, usually gone within a minute.
- Serrador et al., "Cerebral vascular blood flow changes during 'brain freeze'", FASEB J 2012 (abstract;
  https://faseb.onlinelibrary.wiley.com/doi/abs/10.1096/fasebj.26.1_supplement.685.4): only a trend (p = 0.078) for
  anterior cerebral artery flow, so the script says "Scientists still study the exact details".
- Medical News Today: https://www.medicalnewstoday.com/articles/244458 . Tip: eat cold things slowly. The
  tongue-on-palate trick is left out (no evidence found).

## 20. Hiccups — `videos/hiccups.py`
- Reflex arc via the vagus and phrenic nerves and the brainstem: sudden diaphragm contraction, inrush of air, glottis
  closes ("hic"). Triggers: eating fast, fizzy drinks, swallowed air. Most stop in minutes; persistent = more than
  48 hours, intractable = more than a month. Steger et al., PMC5072913:
  https://pmc.ncbi.nlm.nih.gov/articles/PMC5072913/ ; Penn State Health:
  https://pennstatehealthnews.org/2019/01/the-medical-minute-causes-and-cures-of-hiccups-remain-elusive/
- "Scaring someone" cure: unproven (said in the script).

## 21. Foot falling asleep (pins and needles) — `videos/foot_asleep.py`
- Pressure on a nerve and its small vessels blocks conduction (numbness); when pressure is released the nerve
  restarts with disorganised firing (transient paresthesia). Harmless, fades within minutes; frequent symptoms
  without pressure: see a doctor. Cleveland Clinic: https://health.clevelandclinic.org/worry-pins-needles ;
  UPMC: https://share.upmc.com/2017/12/why-does-foot-fall-asleep/

## 22. Ears clean themselves — `videos/earwax.py`
- Cerumen = gland secretions of the outer ear canal + shed skin; it traps dust/germs and protects the canal. The
  canal skin migrates outward, helped by jaw movement; wax usually falls out by itself. Don't use cotton swabs or
  small objects; see a doctor if blocked or hearing drops. AAO-HNSF Clinical Practice Guideline: Earwax (Cerumen
  Impaction), 2017: https://aao-hnsfjournals.onlinelibrary.wiley.com/doi/10.1177/0194599816671491 ; patient sheet:
  https://www.entnet.org/wp-content/uploads/2021/04/earwax_dos-donts_current.pdf
