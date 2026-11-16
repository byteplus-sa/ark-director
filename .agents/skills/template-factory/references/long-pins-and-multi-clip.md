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
| Hard cuts | About 6–7 shots per clip and about 0.8 s per shot are provisional cautions, not provider limits or guaranteed failure thresholds. Preserve requested timing; offer assembly for precision or demonstrated failure and return conflicts with locked workflows instead of imposing a shot ceiling. |
| Duration | Preserve measured fractional source spans and locked final timing. Choose supported generation headroom separately; integer generation duration or an extra hold does not authorize source retiming or a longer final edit. Unknown feasibility remains unresolved. |
| Split points | Split only on measured hard cuts. Do not split inside a whip, match cut, or continuous camera move. |

Timing rules at clip boundaries:

- Write every stage timestamp in clip-local time, retaining its source offset,
  and list the approved picture range the edit will use. Extra generated
  headroom stays outside that range.
- A whip, fade, or other transition that must survive the edit must peak or
  finish before the trim point. A whip that crosses into the next clip needs
  both halves: the outgoing clip ends in blur and the incoming clip opens in
  blur that resolves within about 0.3 s.
- Put a requested final fade to black in post (FFmpeg), within its approved
  span; do not add a fade or move locked final timing by default.
- Do not plan native extension to join clips that contain people: extension and
  video inputs with generated or real people are rejected unless the
  identities are `asset://` Virtual Portrait assets. Join independent clips at
  hard cuts, matching first frames and a shared state ledger instead.

Continuity across clips:

- Give each clip a one-line state ledger at the top of its prompt. Say what the
  subject looks like at the clip's start, for example "base layer only; no
  toppings yet". For build or assembly sequences, state each stage explicitly.
- Generated clips can still show later-stage items early. Check this in QA.
  Propose a re-order only within edit-scope authorization; keep locked source
  order otherwise. Record an approved edit list and reason on the scene manifest.

## Continuous audio across clips

Native audio generated per clip does not share tempo or key across seams, and a
"no music" or "ambience only" line does not reliably hold. Route by explicit
sound ownership, not speech presence, score-led genre or ambience:

| Owner | Multi-clip handling |
| --- | --- |
| native | Preserve supported requested native sound, including wordless room tone and synchronized clicks. Inspect cues and audible continuity at every seam; unwanted music is a QA finding, not permission to mute requested effects |
| post | Use supported `generate_audio: false` for explicitly selected picture-only work. Use only approved post assets or separately authorized generation |
| exact-master | Preserve supplied master bytes, independent sound span and offsets; place the unchanged selected master across clips without per-clip sound conform |
| mixed | Record each native, retained-master and post layer separately, with source hashes, spans and offsets. Preserve native cues and master locks; mix only authorized layers |
| silent | Purposeful silence adds no bed or replacement effects. Verify supported silent controls and actual silence |
| unresolved | Ask for missing ownership or current capability evidence; no automatic muting, replacement bed or generation |

Separate sound is opt-in. A new continuous bed or an edit of native audio is an
alternative only when selected and authorized. Within that scope, measure tempo
and section timing before proposing whole-bar loops, source changes or
30-120 ms crossfades; listen to each actual seam. Diagnose a rejected bed before
revising, never retry automatically or change ownership by inference.

## Assembling the clips

- Carry independent picture and sound spans, offsets, the final word and audio
  tails through the edit. Sound may be longer or shorter than picture; neither
  span is inferred from the other or from the container duration.
- Render approved picture ranges to whole-frame lossless intermediates, join
  compatible picture-only clips with the concat demuxer, and encode once. The
  concat filter needs `setsar=1`. Whole-frame representation is not whole-second
  retiming; preserve decoded timestamps, frame count, FPS and the approved
  fractional timeline. Record any representational mismatch as unresolved.
- Place sound layers independently using their recorded offsets and full
  approved ranges, including tails beyond picture. Do not pad or trim sound to
  picture length, use `-shortest` to hide mismatches, or extend picture silently.
- A trim, pad, hold, retime, loop or crossfade affecting a lock requires current
  requirement evidence and explicit derivative adaptation approval for that
  exact change; creative selection and `approve_for_me` do not supply it.
  Preserve originals and record source SHA-256, derivative SHA-256, exact window,
  command, timing delta and audio consequences. Denied or missing approval
  leaves the source unchanged and feasibility unresolved.
- Read video and audio stream durations and start timestamps independently.
  Inspect opening, seams, final words and tails by playback and listening before
  accepting the assembly or a promoted final.
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
