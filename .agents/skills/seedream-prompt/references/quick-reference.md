# Quick Reference

Focused reference for `seedream-prompt`. Read [the entrypoint](../SKILL.md) for
mode selection and caller responsibilities.

- [Quick reference card](#quick-reference-card)

## Quick reference card

### Model selection

Preserve the selected model. If none is selected, resolve the configured exact
binding and verify the requested operation with the current provider and tool
schema. Missing evidence is unresolved; do not switch models or transports
without authorization. These dated IDs are reference data, not a default.

| Model | Model ID |
|---|---|
| Seedream 5.5 | `dola-seedream-5-5-261028` |
| Seedream 5.0 Pro | `dola-seedream-5-0-pro-260628` |
| Seedream 5.0 Lite | `seedream-5-0-260128` (alias: `seedream-5-0-lite-260128`; override via `SEEDREAM_MODEL_BINDINGS`) |

### Pricing (Seedream 5.0 Pro)
| Tier | Price |
|---|---|
| Output ≤ ~2.36M pixels (1K tier) | $0.045 / image |
| Output > ~2.36M pixels (2K tier) | $0.09 / image |
| First reference image | Free |
| Each additional reference image | $0.003 |

Historical Pro pricing snapshot, not a verified current account price or a
Seedream-wide billing rule. Verify pricing separately when requested.

### Generation size (documented Pro and 5.5)
For generation, `size` accepts `1K`, `1.5K`, `2K`, or explicit `widthxheight`
within the documented pixel and aspect ranges. Verify the selected operation
and transport; decomposition has different size rules. Do not invent 3K/4K tiers.
- Pixel range: [921600, 4624220] (~0.92M–4.6M)
- Aspect-ratio range: [1/16, 16]
- 1K examples: 1024×1024, 1424×800 (16:9)
- 2K examples: 2048×2048, 2816×1584 (16:9, 2K tier)

Input per image: ≤ 36,000,000 pixels, ≤ 30 MB (per API reference).

### Prompt optimization (model-scoped)
`optimize_prompt_options.mode`:
- `standard`: documented for Pro and 5.5.
- `fast`: documented for Pro, not supported by 5.5. Use only when the selected
  model and tool expose it; latency preference alone does not enable it.

### Output parameters
- `response_format`: `url` or `b64_json`, selecting response representation.
- `output_format`: `png` or `jpeg`, selecting image encoding where supported.
  Documented defaults are PNG for 5.5 and JPEG for Pro, not family-wide defaults.
- `watermark`: boolean where the selected tool exposes it.

### Layer decomposition (separate operation)

Use `layer_decomposition: true` with exactly one input image. A creative request
to separate layers is not a substitute for verified executable controls.
The documented Pro ceiling is one base plus up to 16 layers; 5.5 supports one
base plus up to 99 layers. A ceiling is not a promised output count.

5.5 `layer_decomposition_options.max_images` is an integer from 2 to 100,
default 30, including the base. `text_recognition` is optional and yields OCR
only for recognized regular-text layers. These options are not supported by Pro.
Use documented size presets or `auto`, not explicit dimensions, and do not
send `background` during decomposition. Layers are PNG; any layer failure
fails the request. Preserve separate base/layer roles and inspect every output.

OCR output boxes use 0-1000 normalized coordinates in the base-image system.
Do not reuse the edit-input 0-999 normalization for OCR. Approximate font/style
data does not establish exact design fidelity or font-license permission.
Current provider support does not establish that a connected wrapper exposes
these controls; missing tool support requires a truthful handoff.

### Supported prompt languages (Seedream 5.0 Pro)
Native support for 14 languages: Arabic, Filipino, French, German, Indonesian, Japanese, Korean, Malay, Portuguese, Russian, Spanish, Thai, Turkish, Vietnamese. English is the base language. Other languages also work but with weaker in-image text rendering and cultural understanding.

### Throughput and streaming
- Rate limit: 500 images/minute.
- Streaming, native sequential output, and web search: unsupported by documented
  Pro and 5.5 generation. Verify any older or future selected model separately.
- A single-image grid, separate panel calls, stochastic variants, native
  sequential output, and decomposition layers are distinct operations.

### Regions
Supported in `ap-southeast-1` and `eu-west-1`.

### Trust ecosystem with Seedance
The following is a historical Pro/Lite snapshot, not evidence of current
account eligibility, trust, likeness consent, or future-model compatibility.
- Images from Seedream 5.0 Pro and Lite are trusted inputs across all Seedance models (2.5 `dreamina-seedance-2-5-260628`, 2.0 `dreamina-seedance-2-0-260128`, Fast/Mini via `SEEDANCE_MODEL_BINDINGS`).
- Text-to-Image outputs are trusted automatically for all customers.
- Image-to-Image outputs become trusted after the account passes KYC verification.
- Trust exempts input moderation only, not output moderation.

Provider source: [image API](https://ai.byteplus.com/ark/region:ap-southeast-1/docs/image-generation-api.md),
[5.5 tutorial](https://docs.byteplus.com/docs/en/modelark/seedream-5-5.md),
and [Pro tutorial](https://docs.byteplus.com/docs/en/modelark/seedream-5-0-pro.md).
Verified public documentation on 2026-11-13; account and connected-tool
availability still require current evidence.
