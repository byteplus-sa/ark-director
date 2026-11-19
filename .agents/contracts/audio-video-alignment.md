# Audio-video alignment

Preserve generated or supplied audio unchanged. Native generated audio is
sufficient when it meets the brief. Finalization alone does not authorize audio modification.
Do not normalize, EQ, compress, duck, carve, fade, splice, pad, trim, time-stretch,
replace or re-voice audio unless the user explicitly requests or approves that
change. Do not suppress native audio to create a post-production workflow.
This applies to single clips, episodes, compilations and showreels.

Explicitly requested silence, exact supplied masters and scoped audio edits
remain valid. Preserve source files and independent picture/sound spans, offsets,
final words and audio tails. Use compatible stream-copy transport when assembly
requires muxing; disclose required transcoding or timing changes and obtain
specific approval before performing them. Never use `-shortest` to hide a mismatch.

Separate Seed Audio dialogue is opt-in when the user requests lip-synced dialogue audio. Otherwise use native video audio when supported. Generate each scene at its natural duration, using the selected model/tool's current supported limits.

1. Preserve exact dialogue in both audio and video prompts; bind the chosen audio reference in each applicable shot.
2. Inspect the actual audio duration and line timing before video submission. Report incompatible timing and resolve the intended spans; neither padding nor trimming is a default repair.
3. Persist the audio path, SHA-256, verified duration, and dialogue-to-shot alignment in the owning manifest. The generation request contains the same ordered audio reference.
4. Use second-level prompt timing when explicitly requested or necessary for the requested synchronization/editing operation. Ordinary prompt composition does not add per-shot seconds by default.
5. Replacing audio invalidates dependent review hashes. Preserve old snapshots/takes; obtain a new review for the changed request.
6. Provider success places output in `review`. Inspect lip sync, dialogue placement, audio streams and decode integrity. Record a hash-bound audio/video review; a mode-authorized agent decision or explicit user decision may approve only a passing take.

Read-only diagnostics remain available: probe stream timing, inspect decode
integrity and measure loudness without rewriting the media. Validate intended
duration, streams and audible continuity through actual playback/listening.
Missing inspection capability or a defect remains unresolved; report it and ask
for a scoped decision rather than silently repairing it. Loudness readings do
not replace listening and do not impose a delivery target.

Studio rendering, review, locks and provenance remain separate requirements.
They do not require an audio processing pass or authorize one.
