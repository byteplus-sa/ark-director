# Audio-video alignment

Separate Seed Audio dialogue is opt-in when the user requests lip-synced dialogue audio. Otherwise use native video audio. Generate each scene at its natural duration, using the selected model/tool's current supported limits.

1. Preserve exact dialogue in both audio and video prompts; bind the chosen audio reference in each applicable shot.
2. Inspect the actual audio duration and line timing before video submission. Audio must fit the planned video duration. Revise or trim the intended audio within authorization rather than padding the video to a model maximum.
3. Persist the audio path, SHA-256, verified duration, and dialogue-to-shot alignment in the owning manifest. The generation request contains the same ordered audio reference.
4. Use second-level prompt timing when explicitly requested or necessary for the requested synchronization/editing operation. Ordinary prompt composition does not add per-shot seconds by default.
5. Replacing audio invalidates dependent review hashes. Preserve old snapshots/takes; obtain a new review for the changed request.
6. Provider success places output in `review`. Inspect lip sync, dialogue placement, audio streams and decode integrity. Record a hash-bound audio/video review; a mode-authorized agent decision or explicit user decision may approve only a passing take.

For assembly, probe audio and video stream durations and pad short audio to the intended video timeline before crossfades. Validate final duration within the declared codec tolerance, streams, full decode, and audible continuity. Loudness readings do not replace listening.

Normalize every delivered master to one declared integrated loudness target and peak ceiling, recorded in the delivery manifest with the measured values. Unless the brief sets another target, use -16 LUFS integrated with peaks at or below -1.5 dBFS for mobile delivery. Masters combined into a compilation or showreel are gain-matched to the same target.
