# Long pins, multi-clip takes, and multi-pin batches

Read this when a pin is longer than about 20 s or has more than about 25 beats,
when its video exceeds one reliable clip, or when one run handles several pins.

## Windowed analysis for long pins

A long, dense pin can exceed the host's visual context. Plan bounded local
inspection windows before analysis:

1. Measure picture duration and hard cuts first (step 2).
2. Prefer windows of about 5-8 s aligned to confirmed hard cuts. Use as many
   as the duration requires. If a long continuous shot has no cut, use
   overlapping context around window edges and assign each beat to one owner;
   do not invent a cut at a context boundary.
3. Inspect every window with the same checklist, preferring native/local
   perception and using available understanding tools when needed. With host sub-agent
   support, delegate independent windows to native agents with unique output
   files, read-only media, explicit pin-absolute offsets and image/video input
   requirements. Otherwise work sequentially with saved checkpoints.
4. Merge the windows in order, renumber the beats, and reconcile any element
   names that differ between windows.
5. Record window spans, inspected frame paths, reviewer/runtime, uncertainty
   and completion in `analysis-windows.vNN.json`. The main agent checks gap-free
   coverage and overlap consistency, reconciles boundary action and element IDs,
   and validates the merged breakdown before freezing it.

Resume completed windows from saved evidence after interruption. Native
analysis needs no provider tasks or IDs. For optional provider tools, retain
actual task IDs/results under their contracts and reconcile ambiguous
submissions before retrying. Do not resubmit completed windows.

## Splitting video into clips

Seedance 2.5 bills per output second, so several shorter clips cost about the
same as one long clip covering the same duration. Prefer the split that keeps
each clip reliable:

| Budget per clip | Guidance |
| --- | --- |
| Hard cuts | At most about 6–7 shots per clip, and no shot shorter than about 0.8 s. Denser grammar merges or drops cuts; build the pin's blink cuts, flashes and intercuts in the edit. |
| Duration | Choose natural integer durations from the pin spans, rounded up, with at least 0.3 s of hold after the last action. |
| Split points | Split only on measured hard cuts. Do not split inside a whip, match cut, or continuous camera move. |

Timing rules at clip boundaries:

- Write every stage timestamp in clip-local time, and list the trim point the
  edit will use.
- A whip, fade, or other transition that must survive the edit must peak or
  finish before the trim point. A whip that crosses into the next clip needs
  both halves: the outgoing clip ends in blur and the incoming clip opens in
  blur that resolves within about 0.3 s.
- Put the final fade to black in post (FFmpeg), not in the prompt, so the trim
  cannot cut it.
- Do not plan native extension to join clips that contain people: extension and
  video inputs with generated or real people are rejected unless the
  identities are `asset://` Virtual Portrait assets. Join independent clips at
  hard cuts, matching first frames and a shared state ledger instead.

Continuity across clips:

- Give each clip a one-line state ledger at the top of its prompt. Say what the
  subject looks like at the clip's start, for example "base layer only; no
  toppings yet". For build or assembly sequences, state each stage explicitly.
- Generated clips can still show later-stage items early. Check this in QA. A
  re-order of whole shots in the edit is often cheaper than a retake. Record the
  edit list and the reason on the scene manifest.

## Continuous audio across clips

Native audio generated per clip does not share tempo or key across seams, and a
"no music" or "ambience only" line does not reliably hold. For a multi-clip spot
whose sound is score-led or ambient, generate picture with
`generate_audio: false` and either:

- generate one separate music bed after the picture is locked, or
- build the bed from the clips' native audio. Measure each clip's tempo. Loop
  exact whole-bar segments from clips that share a tempo, and switch sources
  only on section changes (drop, reveal, lead entry). Crossfade seams by
  30–120 ms, then confirm with a listening pass that names each seam.

Long generated music beds are more exposed to provider output audits. If a bed
is rejected, diagnose before revising and prefer the native-audio edit over
repeated submissions. Budget spare samples, and measure the delivered bed's
tempo and section timing; pad or splice in assembly rather than trusting the
prompt's timing.

## Assembling the clips

- Render each trimmed clip to an exact-length lossless intermediate in whole
  frames, pad or trim its audio to the same length, join with the concat
  demuxer, and encode once. The concat filter needs `setsar=1`.
- Read video-stream durations, not container durations.
- Keep the takes' original colours. Decode 10-bit HEVC finals as limited-range
  BT.709 and tag the output BT.709; apply a look only when the recipe locks one.

## Multi-pin batches

When one run handles several pins:

- When the host supports sub-agents, give each pin its own native analysis
  sub-agent with explicit media inputs and perception capabilities. Otherwise
  process pins sequentially. Each analysis worker owns only
  `templates/<pin-id>/` and never edits the Studio project (or pre-Studio
  canvas `showcase.json`, `index.html`),
  `project.md`, or `ref_cache.json`.
- Native analysis does not write the provider registry. The main agent owns
  optional tool submissions, uploads and task records to prevent duplicates.
  Every generation registry
  write, by any agent, goes through the lock in
  `.agents/scripts/operation_store.py`: `registry_lock`, `read_registry`,
  `replace_registry`, or `prepare_operation`.
  `.agents/scripts/prepare_request.py --register` does this for you.
- Upload each shared element reference once, and record the object keys in
  `ref_cache.json` from the main agent.
- A pin that is fully deterministic, such as a flat motion graphic rebuilt from
  official cutouts, can go straight to a HyperFrames build from the breakdown's
  measured timing table. Only its music and effects enter prompt review.
