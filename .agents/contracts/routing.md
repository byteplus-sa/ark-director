# Tool and skill routing

| Intent | Route |
| --- | --- |
| Platform administration, catalog, pricing, billing, interactive generation | Available Ark CLI skills and current CLI help |
| In-agent durable generation | `ark-mcp` preferred; persist project-local media and request/task evidence |
| MCP unavailable before submission | Equivalent Ark CLI transport if it supports the same required contract and authorized operation |
| User explicitly requests direct HTTP/curl generation | Use the documented endpoint and exact API contract; resolve credentials from runtime configuration, record `curl` as the transport, and preserve the same review, registry, persistence and reconciliation gates |
| Timeout after possible submission | Reconcile the existing operation; changing transport is not permission to submit twice |
| Prompt composition only | Relevant independent prompt skill; no asset-generation or production-lock ceremony for a writing-only task |
| Multi-scene production | `film-production`; declared orchestrators route specialist work |
| Exact static copy, poster, UI, title/end card, product grid, logo/price/CTA layout, or transparent overlay | `html-graphic-render`; keep source and inputs local, render exact-size PNG, and preserve provenance |
| Invented photographic or illustrative still | Appropriate Seedream skill; hybrid work finishes exact copy/layout through `html-graphic-render` after the image is selected |
| Animated exact graphic or timed overlay | HyperFrames for animation; HyperFrames or FFmpeg for final video composition |
| Media sourcing or generation: images, icons, voiceover, music, SFX, captions | Generate through `ark-mcp` (Seedream, Seed Audio, `speech_to_text`); acquire authorized real assets per [Element identification](element-identification.md); finish, including grades and LUTs, with FFmpeg or HyperFrames. The upstream `media-use` skill is not installed; ignore its pointers inside vendored HyperFrames skills |
| Production stage review | HyperFrames Studio project through `studio_project.py` (`sync`, `stage complete` with its `status` and `check`) at every stage; pre-Studio canvas projects with `showcase.json` keep the `showcase-html` canvas |
| Interactive editing, assembly and final render of a production | HyperFrames Studio; `studio_project.py render` is the only authority for final files and writes the hash-bound render record; post work made elsewhere is placed in Studio and rendered. Skills stay local; no `hyperframes skills` installs; `publish`, `cloud`, `lambda`, `cloudrun` and other account commands only on explicit request |
| Ad-hoc media comparison, also an optional look at a Studio project's elements, audio or candidate takes (never a gate) | `showcase-html --quick`; `media-review` only for an explicitly requested OS player or unavailable browser |
| Mermaid system/process diagram | `design-doc-mermaid` when available; cinematic blocking requests use `tig-blocking-map` |
| Brand-ad / reference-video inspiration | Obtain watchable media first: pass a public HTTPS URL that `seed_understand` accepts, or download then `media_upload` when the link is unusable; do not substitute scripts or article text. Full reverse-engineering → `template-factory`; lighter visual/motion analysis → `ark-mcp` (`seed_understand`) |

Deterministic HTML/CSS/SVG is a production route, not a provider fallback. In
this workspace, that shorthand means one HTML entrypoint with project-local CSS
and SVG dependencies; standalone CSS or SVG is not a renderer entrypoint.
Choose it when exact copy, alignment, repeated brand assets, safe areas, or
transparent geometry are the primary fidelity risk. It does not create a model
prompt or provider operation. A hybrid retains normal generation evidence for
its synthesized image layer and a separate deterministic render record for its
exact graphic layer.

## Capability evidence

Resolve the actual tool schema/model binding before selecting operation, resolution, duration, reference roles/counts, or optional flags. A capability record contains model, source, verified_at, operations, parameter JSON Schemas, required_parameters, reference_roles, max_references, and supports_first_frame_with_reference_images. Recheck when the tool, binding, or operation changes; cached evidence is historical, not a live guarantee.

The workspace default remains Seedance 2.5; legacy 2.0 may be selected for a verified capability such as an available lower-cost variant. Requested 4K needs 2.0 or, when the operator has enabled it, the whitelist-only 2.5 Premium model (the 2.5 feature set plus 4K); standard 2.5 tops out at 1080p. Skills defer to this paragraph for 4K routing. A face in a shot is a QA concern, not an automatic model switch. Chaining does not override unsupported mixed frame/reference inputs.

Credential names are BYTEPLUS_MODELARK_API_KEY and BYTEPLUS_SEED_AUDIO_API_KEY. A transport may document compatibility aliases. Resolve secrets, region, and base URL at runtime; never serialize credentials into requests, fixtures, snapshots, or logs.

## Operation names

New requests set `operation` to the short verb, not the provider tool name: `generate` (the dominant value in existing registries), `edit`, `extend`, `generate_variations`, `text_video_to_audio`, `enhance`, or the legacy hyphenated `erase-subtitles`. `validate_request.py` checks `operation` against the `operations` list in the capability evidence, so a value must appear there. The provider tool is identified by `model` and `transport`. Submit long-running work through `ark_job_submit`. Existing records that carry a tool name such as `seedance_2_5_create_task` are read as-is; constrain the schema to an enum only after the legacy-registry migration preview.

## Directorial axes

Read [seedance-reference.md](seedance-reference.md) when composing a generation-bound shot. Plan the shots first with `seedance-shot-design` (per-shot camera, lens intent and light, with a recorded reason for any static camera or constant light), then load only the preset skills the plan or the user's request needs for camera, lens, lighting, grade, acting, pacing, blocking or medium. Keep one grade per clip, one dominant lighting direction per shot and one or two camera moves per shot unless the explicitly requested choreography needs more.
