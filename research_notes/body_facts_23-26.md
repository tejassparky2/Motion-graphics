# Body Facts 23-26: hidden body processes, reference style (scripts approved by the owner, 15 Oct 2026)

Drawn like the owner's reference videos: real anatomy cut-aways with googly-eyed parts and white labels, then the
masked doctor with Step 1/2/3 cards. Voices: doctor Kokoro `am_adam`, Mike `am_fenrir`, Danny `am_puck`; parts in
stock Kokoro voices at 0.95.

## 23. Sun sneeze (photic sneeze reflex) — `videos/sun_sneeze.py`
- Sneezing on sudden exposure to bright light. Estimates vary (about 18-35%); the 23andMe genome-wide study
  (Eriksson et al., PLoS Genetics 2010, https://journals.plos.org/plosgenetics/article?id=10.1371/journal.pgen.1000993)
  found about a quarter of participants reported it, so "about one in four". Runs in families (autosomal dominant).
- Mechanism unproven; the leading idea is crosstalk between the optic nerve and the trigeminal nerve, so the
  doctor says "Scientists think". Cleveland Clinic: https://my.clevelandclinic.org/health/symptoms/photic-sneeze-reflex
- Safety line: never stare at the sun. "photic" added to `motion/voice.py` PRONOUNCE.

## 24. Wrinkly fingers in water — `videos/wrinkly_fingers.py`
- Water-immersion wrinkling is driven by sympathetic nerves: the fingertip vessels constrict, the pulp loses
  volume, the skin folds (Wilder-Smith & Chow, 2003). Denervated fingers don't wrinkle (O'Riain, BMJ 1973), used as
  a bedside nerve test.
- Grip benefit (Kareklas et al., Biology Letters 2013) didn't replicate (Haseleu et al., PLoS ONE 2014): "studies
  disagree".

## 25. The heart's own electricity — `videos/heart_spark.py`
- SA node in the right atrium fires spontaneously, the impulse spreads across the atria, pauses at the AV node,
  then runs down the bundle of His and Purkinje fibres to the ventricles. Resting rate 60-100 beats a minute.
  Cleveland Clinic: https://my.clevelandclinic.org/health/body/21648-heart-conduction-system
- A transplanted (denervated) heart keeps beating from its own SA node; the autonomic nerves only adjust the rate.
- The "0.1 s pause" sign: the AV-node delay is about 0.1 s (normal PR interval 0.12-0.20 s).

## 26. Contagious yawning — `videos/yawn.py`
- Roughly 40-60% of adults yawn contagiously in studies ("about half").
- Brown et al., "A neural basis for contagious yawning", Current Biology 2017 (University of Nottingham): the urge
  tracked primary motor cortex excitability; told to resist, people still yawned (stifled), and the urge went up.
- Stronger between kin and friends (Norscia & Palagi, PLoS ONE 2011); dogs catch human yawns (Joly-Mascheroni et
  al., Biology Letters 2008). The empathy explanation is debated, so it isn't claimed.
