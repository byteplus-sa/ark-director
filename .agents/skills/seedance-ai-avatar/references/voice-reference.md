# Voice reference

Raw voice isolation is consent-scoped local onboarding/QA material, not a
Seedance request fallback. Consent, internal policy approval and provider face
and voice authorization are independent. Before each request, verify the
matching `Active` face asset and voice asset when voice is used, including
current account, model, operation and transport support.

## Isolate the voice

1. `media_upload` the reference video (`media_type: video`, TTL ≥ 3600s; VOD
   fetches asynchronously).
2. `ark_job_submit` → `vod_separate_audio` with `video_url`, `scene: "Audio"`,
   `output_format: "wav"`.
3. Poll by submitting `vod_get_audio_separation` through `ark_job_submit`
   (`persist_output: true` needs background execution), then read it with
   `ark_job_get`. Download the `voice` track to
   `references/ref_voice-isolated.wav` and check that its SHA-256 matches
   the persisted artifact.

## Cut the clip

Find natural pauses:

```bash
ffmpeg -i references/ref_voice-isolated.wav -af silencedetect=n=-40dB:d=0.25 -f null - 2>&1 | grep silence_
```

Choose `START_S` and `DURATION_S` from the inspected recording's pause
boundaries. Set `FADE_START_S` to the excerpt duration minus the chosen
`FADE_DURATION_S`, without fading a spoken word. These are measured inputs,
not fixed timestamps from another recording. Set a new `OUTPUT_AUDIO` path.
Cut at a pause, mono 48 kHz, normalised:

```bash
ffmpeg -n -i references/ref_voice-isolated.wav -ss "${START_S:?}" -t "${DURATION_S:?}" -ac 1 -ar 48000 \
  -af "loudnorm=I=-16:TP=-1.5:LRA=11,afade=t=out:st=${FADE_START_S:?}:d=${FADE_DURATION_S:?}" \
  "${OUTPUT_AUDIO:?}"
```

An alternate consented excerpt may support local onboarding/QA when needed.
Do not upload or bind the raw excerpt as a generation fallback. Missing,
expired, mismatched, failed or unsupported provider assets stop the request;
resolve the authorized asset route without disguising the input.

## Binding

Bind only the verified `asset://` face and voice references using the currently
supported asset roles. An approved character sheet does not authorize voice,
and raw clips do not replace provider assets. Do not invent role syntax.

Put the full new script in the `{}` dialogue block and state the language
("Dialogue language: <requested language and accent>").

## QA

- Run `speech_to_text` on the generated take and diff it against the script.
  No words from the reference clip may appear.
- Compare median pitch as a rough check (e.g. with a `librosa`/`parselmouth`
  one-off). A human listen is still required, so say so in the take report.
