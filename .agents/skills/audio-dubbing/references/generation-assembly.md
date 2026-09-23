# Generation, recovery, and assembly

## Submission and recovery

Resolve the current Seed Audio tool schema and supported limits before submission. The example fields are illustrative; use the live tool schema for the actual request.

```text
text_prompt: the exact reviewed prompt string
audio_references: [{kind: "url", url: "...", mime_type: "audio/mpeg"}]
output: {format: "wav", sample_rate: 44100}
persist: true
```

Before calling the generation tool, save the exact prompt snapshot beside its planned output and record prompt hash, reference paths/hashes/order, parameters, transport, and local operation ID. Record that operation in the existing project task registry; do not create a second registry. The caller completes the workspace prompt-review gate before spending credits.

Save every returned request/task/artifact ID immediately. A timeout with a known provider ID resumes polling that ID. A timeout or broken response without an ID is `submission_unknown`: reconcile provider state from the operation evidence; never automatically submit again or change transports. MCP-to-CLI fallback is permitted before submission, or after a verified terminal failure with a separately authorized new operation. A completed generation whose download failed needs another download, not another generation.

## Local download and checks

Persist every output under the relevant local scene/shot directory. A durable artifact ID and an expiring URL supplement the local file; they do not replace it. Save bytes, SHA-256, measured duration, provider IDs, and the exact submitted prompt snapshot. Keep generated outputs in `review` until a mode-authorized decision selects a passing result.

Prefer a provider-supported download or a returned media URL. Download to an owned temporary file, require a successful HTTP response, and probe/decode before moving it to the intended asset path. If only artifact retrieval is available, use its documented data field; never recursively guess which large JSON string contains base64. Never pass a truncated tool response to a decoder. Refresh an expired URL using its durable artifact/object identifier.

Before assembly, compare every generated segment to the approved script. Missing lines and unwanted speech require creative review; padding cannot repair omitted dialogue. Do not trim spoken words merely to pass a duration check.

## Offset mixing

Generated segments use timestamps relative to their source segment. Assemble using the recorded absolute source offsets in milliseconds:

```bash
scripts/mix_segments.sh 68.074671 final.wav \
  'seg1.wav:0' 'seg2.wav:20000' 'seg3.wav:36000' 'seg4.wav:47500'
```

The helper accepts literal filenames, including spaces, quotes, colons, and shell metacharacters. Quote each whole `file:offset_ms` argument in the invoking shell; the final colon separates the offset. Durations must be positive finite decimal seconds. Offsets must be nonnegative finite decimal milliseconds before the target end. Scientific notation and filter expressions are rejected.

It uses explicit process arguments, `adelay` on every input channel, and `amix normalize=0:dropout_transition=0`. This preserves input levels through overlap rather than changing gain as inputs end. Overlapping speech can still double, phase, or clip: listen to each seam and choose nonduplicated dialogue boundaries or an intentional crossfade when needed. The helper is a timing assembly tool, not a semantic seam repairer.

Output is stereo PCM WAV at 44.1kHz, padded or trimmed to the target duration. The helper probes and decodes its owned temporary output and requires duration accuracy within one output sample before replacing the destination. Existing output remains untouched if rendering or validation fails. Concurrent calls use separate scratch directories; choose distinct final output paths for independent takes.

## Verified video overlay

```bash
scripts/verify_and_mux.sh source_audio.wav dubbed_audio.wav \
  source_video.mp4 video_dubbed.mp4
```

The **first source video stream defines target duration**. The source-audio argument is retained for compatibility and input-duration reporting; it does not silently shorten the video. Generated audio is padded or trimmed to that video duration in an owned temporary WAV. The helper copies the first video stream and encodes one AAC audio stream at 192kbps. It never uses `-shortest` to conceal a mismatch.

Before publishing the output file, the helper requires exactly one video and one audio stream, unchanged video codec, AAC audio, successful decoding of both streams, and container/audio/video durations within **100ms** of the source video duration. That tolerance allows codec priming/padding and container timestamp rounding; it is not proof of lip synchronization. Missing reliable stream timing fails explicitly. Temporary files are unique and cleaned after failure or success; unrelated similarly named audio files are untouched.

The copied video frames retain their original mouth movements. Check dialogue timing perceptually at scene transitions and near the start/middle/end. Re-rendering lips is a separate requested video-edit operation.

## Failure handling

| Failure | Next action |
| --- | --- |
| Missing executable or invalid numeric argument | Correct the local dependency or input; no media command is submitted for invalid numbers |
| Missing audio/video stream | Supply media with the required stream; keep prior output |
| Encoded reference exceeds duration/byte cap | Reduce segment duration/overlap, choose an eligible format, or revise dialogue boundaries |
| Generated speech is missing or longer than its window | Review the script/prompt and request a new take within existing authorization |
| Output decode or duration validation fails | Retain evidence and prior output; investigate source timing/codecs |
| Provider outcome is unknown | Reconcile the existing operation; do not submit a duplicate |

These helpers validate technical media properties. User review is still needed for voice identity, pronunciation, complete dialogue, and acceptable seams.
