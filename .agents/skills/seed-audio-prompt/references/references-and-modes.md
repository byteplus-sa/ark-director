# References And Modes

Focused reference for `seed-audio-prompt`. Read [the entrypoint](../SKILL.md) for
mode selection and caller responsibilities.

- [Input references](#input-references)
- [Generation mode](#generation-mode)

### Input references

The API contract is the request's `references[]` array. For each supplied audio reference, add one `references[]` entry and identify its intended role. When the prompting guidance's inline conventions are useful, map those entries sequentially to `@Audio1`, `@Audio2`, and `@Audio3` (no space or underscore) and describe each role for the model and human reader.

```text
Input references
@Audio1: Female protagonist voice timbre — Lira
@Audio2: Male antagonist voice timbre — Voss
@Audio3: Male heroic voice timbre — Brann
```

Rules for references:
- Up to 3 reference audio clips per request (reference-audio mode), OR exactly 1 reference image (reference-image mode). Audio and image references are mutually exclusive.
- Per-clip duration: up to 30 seconds.
- Per-clip size: up to 10 MB.
- Audio formats: WAV, MP3, PCM, OGG_OPUS.
- Image format: 1 image, ≤10 MB, JPEG/PNG/WebP. In image mode, `text_prompt` contains ONLY the text to be synthesized (no scene/voice description).
- Each clip serves exactly one purpose: voice timbre cloning, emotion reference, or SFX reference.
- Per reference, provide exactly one of: `speaker` (a TTS 2.0 or cloned voice ID), `audio_data` (base64), or `audio_url`. For image mode, provide exactly one of: `image_data` (base64) or `image_url`.
- `@AudioN` labels and `<<TGT_SPKN>>` speaker tags are prompting-guide conventions, not fields or tokens defined by the public API. The source-backed reference contract is `references[]`.
- When using the prompting-guide convention for voice cloning, map `<<TGT_SPK1>>`, `<<TGT_SPK2>>`, and `<<TGT_SPK3>>` to the corresponding first, second, and third audio entries in `references[]`, labeled `@Audio1`, `@Audio2`, and `@Audio3` in the prompt.
- When no references are provided (text-only / T2A mode), omit the input references section.

### Generation mode

Determine which generation mode applies so the request is constructed correctly. Do not add a task-type heading to `text_prompt` unless the user asks for one.

**T2A — Text-only generation**: Pure text prompt describing everything — environment, music, SFX, character voices, and dialogue. No reference audio clips. Best for one-off scenes, ambience beds, and standalone content where voice cloning is not needed.

**TA2A — Reference-audio generation**: Uses up to 3 reference audio clips for voice cloning and emotion reference. Reference clips are tagged in the prompt with `<<TGT_SPK1>>`, `<<TGT_SPK2>>`, `<<TGT_SPK3>>`. Best for multi-character dialogue, audiobooks, and scenes requiring consistent character voices across multiple generations. (Speaker ID mode is also supported: pass a `speaker` voice ID instead of a clip.)

**Reference-image generation**: Exactly 1 image (≤10 MB, JPEG/PNG/WebP). The model describes the scene in the image and generates appropriate sound. `text_prompt` contains ONLY the text to be synthesized. Image and audio references are mutually exclusive — cannot mix `image_data`/`image_url` with `audio_data`/`audio_url`/`speaker`.
