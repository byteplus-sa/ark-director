# Voice reference

Seedance 2.5 accepts up to 10 audio refs, ≤30s combined. A single clean 8–15s
clip of the presenter is enough to carry timbre, accent and pacing.

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

Also keep a ~15s alternate (`refs/ref_voice-timbre-long.wav`) for a retake if
resemblance is weak. Upload the clip with `media_upload` (`media_type: audio`,
7-day TTL) and keep its URL only in the request, never in a file.

## Binding

```
@Audio 1 defines <Name>'s voice timbre, accent and pacing only; do not reuse any words from @Audio 1.
```

Put the full new script in the `{}` dialogue block and state the language
("Dialogue language: <requested language and accent>").

## QA

- Run `speech_to_text` on the generated take and diff it against the script.
  No words from the reference clip may appear.
- Compare median pitch as a rough check (e.g. with a `librosa`/`parselmouth`
  one-off). A human listen is still required, so say so in the take report.
