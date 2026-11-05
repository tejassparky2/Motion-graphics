# Task for the laptop chat: make Vex 3D clips with the owner's Google AI Pro account (Option 2, owner, 5 Nov 2026)

The owner chose to spend the 1,000 monthly Flow credits instead of paying for the Gemini API. The cloud chat writes
the prompts and edits the episode; the laptop chat runs Google's websites in the owner's Chrome with the Claude in
Chrome extension (owner logged in to his Google account), downloads the results, and pushes them to git.

Setup: `git fetch origin ccr-56282fe5-evehq4` and read `out/vex3d/ep01_energy_drinks.md` from that branch (plan,
prompts, script). Work on your branch `ccr-56282fe5-evehq4-local`; put files under `assets/vex3d/` and push; the
cloud chat fetches them. These are our own generated images and clips, so committing them is fine. Never remove
Google's SynthID watermark, and don't add text to the images or clips.

## Step 1: 3D Vex (do this now; no Flow credits)
1. Open gemini.google.com in Chrome (the owner's account).
2. Attach `assets/mascot/vex/vex_flat_front.png` (on the cloud branch) and paste prompt **A** from
   `out/vex3d/ep01_energy_drinks.md`. Download the result as `assets/vex3d/vex3d_front.png`.
3. New message: attach that 3D image and paste prompt **B** (the turnaround sheet). Save as
   `assets/vex3d/vex3d_turnaround.png`.
4. Check: same face, red eyes, fangs, hair with one curl, cape, bat bow tie in all three views, and no text. If not,
   regenerate (say "match the attached character exactly").
5. Commit and push both images, then tell the owner they're done.

## Step 2: the clips (only after the owner approves the episode script)
The cloud chat will add `out/vex3d/ep01_veo_prompts.md` with one prompt per shot. For each shot:
1. Open labs.google/flow, new project, **Veo 3.1 Fast** (about 20 credits per clip; check the cost Flow shows),
   aspect **9:16**, 8 seconds, **Ingredients to video** with the two Vex images.
2. Paste the shot's prompt, generate, and download the best take as `assets/vex3d/ep01/shotNN.mp4` (NN = 01, 02...).
   If his face or design changes, a hand looks wrong, or text appears, generate that shot once more. At most 2 tries
   per shot.
3. Keep a log in `assets/vex3d/ep01/credits.md`: shot, tries, credits shown by Flow.
4. Stop if the account's credits drop below 100 and tell the owner.
5. Commit and push the clips as they finish.
