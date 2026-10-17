# Seed Audio generation

Load this when you generate speech, music, SFX, or ambience with
`seed_audio_generate` or `seed_audio_generate_variations`. For transcription
and audio analysis, use [Understanding and speech-to-text](understanding-and-stt.md).

Requires `BYTEPLUS_SEED_SPEECH_API_KEY`. Auth scope: `seed:audio:generate`.
Both tools require background execution through `ark_job_submit`. Provider
audio URLs expire after **2 hours**.

## `seed_audio_generate`

Full-scene audio from a text prompt, with optional voice cloning, image
context, subtitles, and watermarking. `audio_references` and
`image_reference` are mutually exclusive.

| Parameter | Type | Notes |
|---|---|---|
| `text_prompt` | `str` | 1–3000 characters; required |
| `audio_references` | list | Up to 3 (speaker ID, URL, or Base64). Base64 WAV is preflight-checked against the 30 s limit. |
| `image_reference` | `MediaSource` | Image for context-aware audio |
| `output` | object | `format` (`wav`/`mp3`/`pcm`/`ogg`), `sample_rate`, `speech_rate`, `loudness_rate`, `pitch_rate`, `subtitle`, `subtitle_type` |
| `watermark` | object | Enable watermark and optional metadata |
| `persist` | `bool` | Default `true` |
| `output_path`, `overwrite` | | stdio with confirmed native tasks only |

Returns `artifact`, `duration_seconds`, `billing_duration_seconds`, optional
`subtitle`, `request_id`, `provider_log_id`, optional `source_url`.

```json
{"tool_name": "seed_audio_generate",
 "arguments": {"input": {
   "text_prompt": "A gentle rain falling on a tin roof, with distant thunder rumbling every few seconds",
   "output": {"format": "wav", "sample_rate": 44100},
   "persist": true}}}
```

Voice from a preset speaker, with word subtitles:

```json
{"text_prompt": "Hello, welcome to our presentation. Today we will discuss the quarterly results.",
 "audio_references": [{"kind": "speaker", "speaker_id": "<speaker-id>"}],
 "output": {"format": "mp3", "subtitle": true, "subtitle_type": "word"},
 "persist": true}
```

## `seed_audio_generate_variations`

1–5 independent generations in parallel. Audio has **no seed**, so every
variation differs.

| Parameter | Type | Notes |
|---|---|---|
| `text_prompt` | `str` | Base prompt |
| `variations` | `int` | 1–5 |
| `variation_prompts` | `list[str]` | Optional, one per variation |
| other audio params | | Same as `seed_audio_generate`; `output_dir` instead of `output_path` |

Returns a `VariationSummary` with partial-failure capture.

## Persistence in background jobs

- Do not pass `output_path` / `output_dir` through `ark_job_submit`; the
  worker may have no session ("session is not available").
- Keep `persist: true` so the durable artifact is created server-side, then
  export it with `seed_media_export_artifact`.
- If the result carries `persistence_error`, recover with
  `seed_media_persist_url` before the 2 h URL expires, or decode
  `fallback_data` for an `inline-fallback` reference.

## Provider behaviour worth budgeting for

- Output audits reject a share of music runs; generate spare samples rather
  than assuming every submission returns audio.
- Tempo and arc timing in the prompt are only roughly obeyed; measure the
  result and pad or splice in assembly.
- Short lines can truncate unless the prompt states the clip length and the
  trailing silence wanted.
- Verify words with `speech_to_text`, not with `seed_audio_understand`.
