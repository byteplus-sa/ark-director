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
2. When audio exists, extract a lossless copy without changing the pin. Send
   that audio to `seed_audio_understand`, or obtain a documented human listening
   review. A terminal agent cannot hear sound by running FFmpeg or opening a
   player. Cover the full soundtrack, then inspect short windows around cuts,
   prominent action, speech, effects, and the ending. Record the Ark job ID,
   completion ID, model, audio hash, exact prompt, and response in a review note;
   link it from `auditory_review.evidence_ref`. A waveform can locate transients
   but cannot name their source.
3. Measure silence and loudness with FFmpeg, recording the command, thresholds,
   and output in `audio-analysis.md`. Use `silencedetect` for gaps and `ebur128`
   for loudness; neither identifies speech, instruments, music, or sound effects.
   Keep picture and audio durations separate because an audio tail may extend
   beyond the final frame.
4. If speech matters, use `speech_to_text` on the extracted audio and check
   important words and timestamps against the auditory review. If overlapping voice, music,
   and effects prevent reliable listening, use `vod_separate_audio` with a
   suitable scene, retain its task and artifact provenance, and send the stems
   through a verified audio-capable reviewer. Separation is an optional
   analysis aid, not proof of exact source
   identity. Do not submit a paid separation task for a pin with no need for it.
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

Use Ark MCP's `seed_audio_understand` on the extracted soundtrack. Check
`ark_job_capabilities` for `seed_audio_understand` and `media_upload`; both
require background jobs. Submit `media_upload` with `media_type: "audio"`,
`mime_type: "audio/flac"`, and the absolute `file_path`, then poll its Ark job
with `ark_job_get`. Submit the understanding job with the returned presigned
HTTPS URL and poll it to completion:

```json
{
  "input": {
    "tool_name": "seed_audio_understand",
    "arguments": {
      "input": {
        "prompt": "Listen to the entire supplied audio. Map audible music, speech, effects, ambience, and silence with timestamps in seconds relative to this audio clip. Describe changes and accents, uncertainty, and undecodable passages. Report only what is audible; do not infer sound from the picture.",
        "audios": [{ "kind": "url", "url": "<presigned audio URL>" }],
        "reasoning_effort": "medium"
      }
    }
  }
}
```

The JSON object is the complete argument to `ark_job_submit`. Keep presigned URLs out of
durable notes. Record the submitted prompt and the returned job, completion,
and model IDs alongside the original pin and extracted audio hashes. Set
`auditory_review.method: ark_mcp_seed_audio_understand` only after a completed
response covers the supplied audio. If a clip exceeds the upload or model
limit, split it into contiguous, labeled windows, review all windows, and
retain each window's start offset and response. Do not leave gaps. The model
receives audio only: translate its clip-relative timestamps to picture time
using the measured audio and video stream start times, then compare against
cuts and visible action. Recheck uncertain claims with shorter audio windows,
ASR, or separated stems where useful. Do not infer that a visible event made a
sound merely because its timing overlaps an audio accent.

A human may listen in the project canvas and supply timestamped notes; link
those notes as `auditory_review.evidence_ref`. Opening a player for the user
does not count as agent listening. If the audio tool or source is unavailable
and no reviewer can hear the clip, set `auditory_review.status: unavailable`.
Keep music, speech, effects and ambience unknown, and leave reusable audio
grammar empty. FFmpeg may still establish stream properties and
threshold-defined silence. Do not represent this as a completed sound map.

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
the audio-preparation canvas stage `skipped` only when the intended output is
silent or audio production is outside the current scope. A sound map by itself
does not authorize generation or use of a source soundtrack.
