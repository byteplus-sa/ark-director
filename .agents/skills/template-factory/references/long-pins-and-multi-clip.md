# Long pins, multi-clip takes, and multi-pin batches

Read this when a pin is longer than about 20 s or has more than about 25 beats,
when its video exceeds one reliable clip, or when one run handles several pins.

## Windowed analysis for long pins

A single `seed_understand` call over a long, dense pin can time out on the
provider or come back too long to use. A 33.6 s, 42-beat montage timed out four
times at full length, including at half length. Plan windows from the start
rather than after a failure:

1. Measure picture duration and hard cuts first (step 2).
2. Split the pin into 3–6 windows of about 5–8 s. Each window must start and
   end on a measured hard cut, so no beat straddles a boundary.
3. Run the same analysis prompt once per window on the same uploaded object,
   in parallel. Tell each call its window span and that its beat times are
   pin-absolute.
4. Merge the windows in order, renumber the beats, and reconcile any element
   names that differ between windows.
5. Record every window's job ID and span in `raw_seed_understand_windows_vNN.json`.
   Then validate the merged breakdown as usual.

A timeout with `ambiguous_completion` still needs reconciliation before retry.
The windowed calls are new operations with a different scope, not a duplicate
of the full-length call.

## Splitting video into clips

Seedance 2.5 bills per output second, so several shorter clips cost about the
same as one long clip covering the same duration. Prefer the split that keeps
each clip reliable:

| Budget per clip | Guidance |
| --- | --- |
| Hard cuts | At most about 6–7 shots per clip, and no shot shorter than about 0.8 s. Denser grammar merges or drops cuts. |
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

Continuity across clips:

- Give each clip a one-line state ledger at the top of its prompt. Say what the
  subject looks like at the clip's start, for example "raw: pepper strips and
  onions already on top; no shrimp or scallops yet". For food builds, state raw
  versus baked explicitly.
- Generated clips can still show later-stage items early. Check this in QA. A
  re-order of whole shots in the edit is often cheaper than a retake. Record the
  edit list and the reason on the scene manifest.

## Continuous audio across clips

Native audio generated per clip does not share tempo or key across seams. For
a multi-clip spot, either:

- generate one separate music bed after the picture is locked, or
- build the bed from the clips' native audio. Measure each clip's tempo. Loop
  exact whole-bar segments from clips that share a tempo, and switch sources
  only on section changes (drop, reveal, lead entry). Crossfade seams by
  30–120 ms, then confirm with a listening pass that names each seam.

Long generated music beds are more exposed to provider output audits. If a bed
is rejected, diagnose before revising and prefer the native-audio edit over
repeated submissions.

## Multi-pin batches

When one run handles several pins:

- Give each pin its own analysis sub-agent. It owns only
  `templates/<pin-id>/` and never edits `showcase.json`, `index.html`,
  `project.md`, or `ref_cache.json`.
- Every registry write, by any agent, goes through the lock in
  `.agents/scripts/operation_store.py`: `registry_lock`, `read_registry`,
  `replace_registry`, or `prepare_operation`.
  `.agents/scripts/prepare_request.py --register` does this for you.
- Upload each shared element reference once, and record the object keys in
  `ref_cache.json` from the main agent.
- A pin that is fully deterministic, such as a flat motion graphic rebuilt from
  official cutouts, can go straight to a HyperFrames build from the breakdown's
  measured timing table. Only its music and effects enter prompt review.
