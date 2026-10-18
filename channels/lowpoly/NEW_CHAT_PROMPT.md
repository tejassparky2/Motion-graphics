# Prompt to start the low-poly chat (paste this as the first message of the new chat)

You're taking over my **low-poly 3D YouTube Shorts channel**: dev-comedy skits about Claude and Codex. It's a separate
channel from Interestingly Strange. Repo: tejassparky2/motion-graphics. Start from branch `ccr-56282fe5-evehq4` (where
the work so far lives), then work on **your own branch `ccr-56282fe5-evehq4-lowpoly`** (like the doctor and news chats),
and don't make Interestingly Strange videos there.

Read first:
1. `channels/lowpoly/README.md`: the four reference skits I sent (@agentpoly and a campfire one) and the rules we
   settled on for **look, music and camera** (dark low-key room, monitor glowing behind Claude and Codex, depth of
   field, dust motes; quiet ambient pad with silences on punchlines plus room tone; eye-level shots of the desk
   characters, 3/4 shot of Dev, over-the-shoulder, close-ups for punchlines, high wide shot from behind Dev; small
   clean speaker-coloured captions).
2. `channels/lowpoly/scripts/ep01_code_review.md` and the finished episode `out/lowpoly/ep01_code_review.mp4`
   ("I Asked AI to Review My Coworker's Code", approved 17 Oct 2026).
3. The repo's `CLAUDE.md` for the general rules that still apply: script first and I approve before rendering, keep
   my words, Whisper-medium check every line after rendering, every video ships with an upload sheet, **never use
   my cloned voice**, never clone a real person.

Cast and voices (all synthetic, Chatterbox Turbo): **Dev** (boy in a hoodie and glasses, male voice: Turbo with
`turbo_ref="am_michael"`), **Claude** (the Claude Code mascot in low poly: orange block, upright eyes, side nubs,
four legs; voice `turbo_ref="af_heart"`), **Codex** (blue floating robot with a visor; `turbo_ref="am_puck+2"`).
Every description says "Parody. Not affiliated with Anthropic or OpenAI." No official logos; never make Claude or Codex
say false or harmful things about the real products.

How to build: `python channels/lowpoly/make_skit.py EPISODE` (voices -> timing -> 3D frames in headless Chromium ->
captions, panels, music -> out/lowpoly/EPISODE.mp4). Each episode is `channels/lowpoly/EPISODE.py` (script, panels,
captions) plus `channels/lowpoly/directions/<name>.js` (per line: emotion and pose for each character). One-time
setup: `cd build/lowpoly && npm init -y && npm install three@0.169.0 playwright-core@1.48.2`.
`--stills 1.0,5.0` renders check frames; `--reuse-frames` redoes captions/sound without the 3D.

Next: write the episode 2 comedy script (about 40-55 s, a relatable developer pain point, short lines, a twist ending)
and send it to me for approval before making it.
