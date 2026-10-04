# Body Facts 9-10: two more weird operations

Owner: "Make 2 more weird operation videos". Same format as 5-8; these are the first videos with the owner's
Doc and the Organs logo in the corner.

## 9. Hemispherectomy (half the brain removed) — `videos/half_brain.py`
- For children whose seizures start in one half of the brain and can't be controlled with medicine (Rasmussen
  encephalitis, a stroke around birth, malformation of one hemisphere). That half is removed or disconnected;
  the space fills with cerebrospinal fluid. In young children the other half takes over many of its jobs.
- Johns Hopkins, 111 children, 1975-2001 (Kossoff et al., Neurology 2003; PubMed 14557554:
  https://pubmed.ncbi.nlm.nih.gov/14557554): 65% seizure-free, 21% occasional non-handicapping seizures,
  14% troublesome seizures; 89% walk without assistance; 70% satisfactory spoken language.
  Script: "Most walk and talk afterwards, though one hand stays weaker." "And many never have another seizure."
- The weaker hand (hemiparesis on the other side) is stated so the video doesn't oversell it.
- Framing: Mike sees his brain scan as an adult; he had the operation as a small child (the age it's usually done).

## 10. Paramedian forehead flap (forehead skin rebuilds the nose) — `videos/forehead_nose.py`
- Used for moderate to large nasal defects, most often after skin cancer is cut out. A strip of forehead skin is cut
  and swung down onto the nose but left attached at the brow (the pedicle); its own artery keeps it alive.
- Two (or three) stages: the pedicle is divided after about 3 weeks (sources: 2-4 weeks), once new blood vessels
  have grown into the flap from the nose. Good colour and texture match; the forehead scar usually heals well.
  StatPearls, "Paramedian Forehead Flaps": https://www.ncbi.nlm.nih.gov/books/NBK499932/ ;
  review, Plastic and Aesthetic Research 2025: https://www.oaepublish.com/articles/2347-9264.2025.53
- Script: "about three weeks"; "the nose grows new blood vessels. Then we cut the strip."

## Voices
Natural stock voices at speed 0.95. Half brain: healthy half `af_heart`, sick half `am_michael`, scalpel `af_bella`,
Mike `am_fenrir`, Danny `am_puck`. Forehead flap: nose `am_michael`, forehead `af_heart`, scalpel `af_bella`, Mike,
Danny. Doctor = owner's clone; "hemispherectomy" is spoken as "hemisphere-ectomy" (`CLONE_SAY`).
Reworded after the clone check: "So we removed that half." (heard "remove") -> "So we took that half out.";
"...so we used skin from his forehead to rebuild it." (heard "use") -> "His forehead gave the skin to fix it."
