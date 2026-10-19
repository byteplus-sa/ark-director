# Reference audio analysis

Analyze the soundtrack as evidence tied to the original pin. Produce
`audio-analysis.json` under the run's template directory and validate it against
`audio-analysis-schema.json`. The artifact is separate from `VideoBreakdown` so
older visual breakdowns remain valid.

## Measure and listen

1. Use `ffprobe` to check whether the pin has an audio stream and record its
   duration, channel count, and sample rate. Record `absent` only after a
   successful probe shows no audio stream. Use `unavailable` when the pin cannot
   be decoded or the audio cannot be accessed.
2. When audio exists, extract a lossless copy without changing the pin. Use
   verified native audio input or a capable local audio model first. If those
   cannot inspect audio, use an available audio-understanding tool such as
   `ark-mcp` `seed_audio_understand`, or documented human listening.
   A terminal agent cannot hear sound by
   running FFmpeg or opening a player. Cover the full soundtrack, then inspect
   short windows around cuts, prominent action, speech, effects and the ending.
   Record the reviewer/runtime, actual audio input capability, audio hash,
   inspected ranges, exact analysis instructions and observations in a review note;
   link it from `auditory_review.evidence_ref`. A waveform can locate transients
   but cannot name their source.
3. Measure silence and loudness with FFmpeg, recording the command, thresholds,
   and output in `audio-analysis.md`. Use `silencedetect` for gaps and `ebur128`
   for loudness; neither identifies speech, instruments, music, or sound effects.
   Keep picture and audio durations separate because an audio tail may extend
   beyond the final frame.
4. If speech matters, use available MCP or local ASR on the extracted audio and check
   important words and timestamps against the auditory review. If overlapping voice, music,
   and effects prevent reliable listening, use an available MCP or local separator,
   retain its tool/model version, arguments and artifact hashes, and pass the stems
   through a verified audio-capable reviewer. Separation is an optional
   analysis aid, not proof of exact source
   identity. Local ASR and separation are not prerequisites. Follow the selected
   tool's authentication, upload, cost, authorization and task-persistence
   contracts; honor explicit offline constraints. Missing local tools alone do
   not block an available permitted MCP route.
5. Build a timestamped event map with music entrances, changes and accents;
   voice entries; identifiable effects; ambience changes; deliberate silence;
   and audio tails. Link each event only to visual beats it overlaps. Describe
   confidence and evidence for each event. Preserve uncertainty. Do not infer
   BPM, key, instrument, speaker, or exact sound source from loudness peaks.
6. Separate reusable grammar from replaceable content: dynamic arc, transition
   accent pattern, silence, and audio-to-picture synchronization may become
   template rules. Music recording, melody, lyrics, voices, brand slogans, and
   distinctive effects remain run-specific inputs unless independently
   authorized. In de-identify mode, remove source brands, spoken taglines, and
   lyrics from the reusable recipe.

## Auditory review route

Use `auditory_review.method: native_agent_audio` only when the current host
actually receives and understands audio, or `local_audio_model` for a verified
on-device audio-capable model. A local CLI that proxies to a remote model is
not an on-device model. Use `ark_mcp_seed_audio_understand` for that MCP tool,
`audio_understanding_tool` for another verified audio-capable tool (identify
the tool/model in the evidence note), and `human_review` for a person who listened.
ASR or separation alone is not an auditory review method.
New records use `schema_version: "1.1"` and completed native/local/tool reviews
include `capability_evidence` (the actual audio interface/runtime),
`audio_sha256` (the extracted audio bytes), and `coverage` (contiguous
`start_s`/`end_s` ranges in extracted-audio time covering the full soundtrack).
Set `evidence_ref` to the saved listening note. The validator checks coverage
and required provenance, not whether the reviewer truly heard the clip; inspect
the note and current audio hash before accepting it.

Apply these instructions to the actual audio:

```text
Listen to the entire supplied audio. Map audible music, speech, effects,
ambience and silence with timestamps in seconds relative to this audio clip.
Describe changes, accents, uncertainty and undecodable passages. Report only
what is audible; do not infer sound from the picture.
```

If the input exceeds native context limits, split it into contiguous labeled
windows, review all windows and retain each window's offset and notes. Do not
leave gaps. Translate clip-relative event timestamps to picture time
using the measured audio and video stream start times, then compare against
cuts and visible action. Recheck uncertain claims with shorter audio windows,
ASR, or separated stems where useful. Do not infer that a visible event made a
sound merely because its timing overlaps an audio accent.

Use an available audio-understanding tool when native audio perception is
insufficient and the user's constraints permit it; no additional preference
for local ASR is imposed. Record the capability gap, input hashes, tool/model,
request instructions, saved response and any actual task ID. Do not fabricate
provider IDs for synchronous tools. Retain full-soundtrack coverage and check
uncertain claims; provider output is evidence, not automatic approval. Historical
`ark_mcp_seed_audio_understand` evidence remains valid under schema v1.0;
preserve it without fabricating new native provenance or repeating the job.

A human may listen (to the audio file, to a take in its Studio frame, or in the pre-Studio project canvas) and supply timestamped notes; link
those notes as `auditory_review.evidence_ref`. Opening a player for the user
does not count as agent listening. If the audio tool or source is unavailable
and no reviewer can hear the clip, set `auditory_review.status: unavailable`.
Keep music, speech, effects and ambience unknown, and leave reusable audio
grammar empty. FFmpeg may still establish stream properties and
threshold-defined silence. Keep `audio_stream.status: present` when the stream
is decodable but the runtime cannot listen. Do not represent this as a completed
sound map. Continue visual work; source-matching audio remains unresolved.

## Example measurement commands

```bash
ffprobe -v error -show_entries stream=index,codec_type,start_time,duration,channels,sample_rate -of json pin.mp4
ffmpeg -v error -i pin.mp4 -map 0:a:0 -vn -c:a flac reference-audio.flac
ffmpeg -hide_banner -i reference-audio.flac -af 'silencedetect=noise=-40dB:d=0.1' -f null -
ffmpeg -hide_banner -i reference-audio.flac -af 'ebur128=peak=true' -f null -
```

Keep those outputs as measurement evidence, not as a substitute for listening.
Use the original pin hash from intake and the exact frozen breakdown hash in
`audio-analysis.json`. Run:

```bash
uv run python .agents/skills/template-factory/scripts/validate_breakdown.py \
  analysis.vNN.json --source-duration-s <picture-seconds> \
  --audio-analysis audio-analysis.json --source-pin-sha256 <pin-sha256>
```

For `absent` or `unavailable` audio, leave `events` empty, set unknown stream
properties to `null`, and state the condition in `soundscape.dynamic_arc`. Set
`auditory_review.status` to `not_needed` for an absent stream and `unavailable`
when audio cannot be decoded. Mark
the audio-preparation stage skipped (`stage skip audio-preparation --reason`) only when the intended output is
silent or audio production is outside the current scope. A sound map by itself
does not authorize generation or use of a source soundtrack.
