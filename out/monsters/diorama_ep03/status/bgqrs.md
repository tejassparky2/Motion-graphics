# bGqrs status (Ep 3)

Updated 7 Nov 2026, 10:25 UTC.

| Shot | State | File |
|---|---|---|
| S13 "So I put the light below them." | **Building** (`channels/monsters/diorama_ep03/bgqrs.py`, `s13`); a first test still is rendering. The staging: | shots/S13.mp4 (pending) |

### S13 staging (helper 10: S14 can match it; helper 6/1: tell me here if S10 or the lane put Kai elsewhere)
- **Where:** the grass on the village's north edge, east of the track: his feet at **(12, -140)** at frame 1 (helper 9's
  Ep 2 village; I'll move it onto helper 1's lane verge when village.py lands).
- **Kai:** standing, his left wrist raised to the swarm (as S10 leaves him). He dips, sits back and drops flat on his
  back, with a small bounce. He lies **east-west, his head to the west** (compass 90), LYING_V3's legs (the left knee up).
  Then he lays his left arm out on the grass beside his head, **palm up** (the forearm rolled so the mark faces the
  sky). Grass round the wrist. Determined face, eyes on the swarm.
- **The light:** a coral point key at the mark (it lights his arm, face and the grass) plus a broad coral glow just
  above the wrist that lights the moths' bellies once he lies. The 2D pass draws the zigzag and its glow up through
  the grass (helper 9's post_helper9.mark) from `build/monsters/diorama_ep03/S13_mark.json`.
- **The swarm:** a loose dome circling the vertical through the light, following it down: 4.5-11 units above the
  wrist at the end. Stand-in fluffmoths at 0.42 until helper 6's `swarm()` lands.
- **The shrimp:** on his left shoulder at **0.6** (E2.SHRIMP_IN_HAND, helper 4's S01). It ducks flat with its eyes
  shut as he drops, then peeks up at the swarm. (Helper 3's S02 uses 0.42 on the shoulder: one of us should change.)
- **Camera:** north of him, a little toward his feet, looking south over the village; a slow push-in on 1s. He drops
  from a profile facing frame right to lying across the frame, with the light low and the swarm above.
- **Night:** a stand-in night look until helper 9's grade lands (I pick it up automatically from diorama_ep03/helper9.py).

After S13: render parts of the long shots (S14/S06/S10/S15/S18) from their owners' status files.

## Coordinator
