# Api Reference

Focused reference for `seed-audio-prompt`. Read [the entrypoint](../SKILL.md) for
mode selection and caller responsibilities.

- [Quick reference card](#quick-reference-card)
- [Model identity](#model-identity)
- [Request body](#request-body)
- [Response fields](#response-fields)
- [Limits](#limits)
- [Output configuration (`audio_config`)](#output-configuration-audio_config)
- [Watermark (`watermark` object)](#watermark-watermark-object)
- [Pricing](#pricing)
- [Long-form pattern](#long-form-pattern)
- [Prompt language](#prompt-language)

## Quick reference card

### Model identity
- Model ID: `seed-audio-1.0`
- Endpoint: `POST <base>/api/v3/tts/create`, where `<base>` is resolved from env (`BYTEPLUS_SEED_AUDIO_BASE_URL`); the example below is for orientation only and must not be hard-coded.
- Auth: `X-Api-Key` header (required). Optional: `X-Api-Request-Id` (client-generated UUID for tracing).
- Output: non-streaming HTTP only.

### Request body
| Field | Description |
|---|---|
| `model` (required) | `seed-audio-1.0` |
| `text_prompt` (required) | Up to 3000 characters. In image mode, contains only text to synthesize. |
| `references[]` | Array of references. Per reference: exactly one of `speaker` (TTS 2.0 / cloned voice ID), `audio_data` (base64), `audio_url`; OR `image_data` / `image_url` for image mode. Max 3 audio OR 1 image. |
| `audio_config` | Object containing `format`, `sample_rate`, `speech_rate`, `loudness_rate`, `pitch_rate`. |
| `watermark` | Object (see below). |

### Response fields
| Field | Description |
|---|---|
| `code` / `message` | Status code and message. |
| `audio` | Base64-encoded generated audio. |
| `duration` | Post-processed audio duration (seconds). |
| `original_duration` | Pre-processed duration — **basis for billing**, capped at 120s. |
| `url` | Temporary download URL — **expires in 2 hours**. |

### Limits
| Parameter | Limit |
|---|---|
| `text_prompt` max characters | 3000 |
| Max generated audio duration | 120 seconds (2 minutes) |
| Max reference audio clips | 3 (reference-audio mode) |
| Max reference images | 1 (reference-image mode) |
| Reference clip max duration | 30 seconds each |
| Reference clip max size | 10 MB each |
| Reference clip formats | WAV, MP3, PCM, OGG_OPUS |
| Reference image formats | JPEG, PNG, WebP (≤10 MB) |

### Output configuration (`audio_config`)
| Parameter | Range / Values |
|---|---|
| `format` | wav / mp3 / pcm / ogg_opus |
| `sample_rate` | one of [8000, 16000, 24000, 32000, 44100, 48000]; default follows the provider setting |
| `speech_rate` | -50 to 100 (-50 = 0.5x, 0 = default, 100 = 2.0x) |
| `loudness_rate` | -50 to 100 (-50 = 0.5x, 0 = default, 100 = 2.0x) |
| `pitch_rate` | -12 to 12 semitones (0 = default) |

### Watermark (`watermark` object)
| Sub-field | Type | Description |
|---|---|---|
| `aigc_watermark` | bool | Explicit rhythm marker appended to end of audio. Default `false`. |
| `aigc_metadata` | object | Implicit header metadata. Sub-fields: `enable` (bool), `content_producer`, `produce_id`, `content_propagator`, `propagate_id`. Default disabled. |

Note: the MCP tool `seed_audio_generate` exposes these as `watermark.enable` and
`watermark.metadata`; the `aigc_watermark` / `aigc_metadata` names above are the
raw REST API fields.

### Pricing
- **0.15 USD per minute** of generated audio (0.0025 USD/second), billed per second based on `original_duration`.
- 60-minute free trial provided on service activation.
- Prepaid packages available (e.g. 200 min / $28.50 up to 2,000,000 min / $240,000).

### Long-form pattern
For content longer than 2 minutes, chain generations: take the output of one call, use it as a reference audio clip in the next call, and continue the scene. Voice identity carries through if you re-pass the original voice reference clips.

### Prompt language
Preserve the supplied dialogue/script language, including mixed-language lines. Control descriptions follow the user's language preference; do not translate protected dialogue merely to match them. Seed Audio 1.0 supports cross-lingual synthesis; consult the [API reference](https://docs.byteplus.com/en/docs/byteplusvoice/seedaudio-01) for the current voice and language list.
