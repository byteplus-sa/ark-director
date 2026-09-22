# Voice reference

Seedance 2.5 accepts up to 10 audio refs, ≤30s combined. A single clean 8–15s
clip of the presenter is enough to carry timbre, accent and pacing.

## Isolate the voice

1. `media_upload` the reference video (`media_type: video`, TTL ≥ 3600s; VOD
   fetches asynchronously).
2. `ark_job_submit` → `vod_separate_audio` with `video_url`, `scene: "Audio"`,
   `output_format: "wav"`.
3. Poll with `vod_get_audio_separation` (`persist_output: true`) and download
   the `voice` track to `references/ref_03_voice_isolated.wav`. Check that the
   SHA-256 matches the persisted artifact.

## Cut the clip

Find natural pauses:

```bash
ffmpeg -i references/ref_03_voice_isolated.wav -af silencedetect=n=-40dB:d=0.25 -f null - 2>&1 | grep silence_
```

Cut at a pause, mono 48 kHz, normalised, short fade:

```bash
ffmpeg -i references/ref_03_voice_isolated.wav -ss 0 -to 8.86 -ac 1 -ar 48000 \
  -af "loudnorm=I=-16:TP=-1.5:LRA=11,afade=t=out:st=8.66:d=0.2" \
  elements/<id>/voice_<id>_timbre_v01.wav
```

Also keep a ~15s alternate (`voice_<id>_timbre-long_v01.wav`) for a retake if
resemblance is weak. Upload the clip with `media_upload` (`media_type: audio`,
7-day TTL) and put its URL in `options/BRIEF.md`.

## Binding

```
@Audio 1 defines <Name>'s voice timbre, accent and pacing only; do not reuse any words from @Audio 1.
```

Put the full new script in the `{}` dialogue block and state the language
("Dialogue language: American English").

## QA

- Run `speech_to_text` on the generated take and diff it against the script.
  No words from the reference clip may appear.
- Compare median pitch as a rough check (e.g. with a `librosa`/`parselmouth`
  one-off). A human listen is still required, so say so in NOTES.
