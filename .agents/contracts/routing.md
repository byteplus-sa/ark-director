# Tool and skill routing

| Intent | Route |
| --- | --- |
| Platform administration, catalog, pricing, billing, interactive generation | Available Ark CLI skills and current CLI help |
| In-agent durable generation | ModelArk MCP preferred; persist project-local media and request/task evidence |
| MCP unavailable before submission | Equivalent Ark CLI transport if it supports the same required contract and authorized operation |
| Timeout after possible submission | Reconcile the existing operation; changing transport is not permission to submit twice |
| User explicitly chooses Lumina | Author copy-paste prompts in chat; do not generate through MCP/CLI or create production files unless requested |
| Prompt composition only | Relevant independent prompt skill; no asset-generation or production-lock ceremony for a writing-only task |
| Multi-scene production | `film-production`; declared orchestrators route specialist work |
| Production stage review | Required persistent `showcase-html` canvas; update and freshness-check it at every stage |
| Ad-hoc media comparison | `showcase-html --quick`; `media-review` only for an explicitly requested OS player or unavailable browser |
| Mermaid system/process diagram | `design-doc-mermaid` when available; cinematic blocking requests use `tig-blocking-map` |
| Brand-ad / reference-video inspiration | Obtain watchable media first: pass a public HTTPS URL that `seed_understand` accepts, or download then `media_upload` when the link is unusable; do not substitute scripts or article text. Full reverse-engineering → `template-factory`; lighter visual/motion analysis → `modelark-mcp` (`seed_understand`) |

## Capability evidence

Resolve the actual tool schema/model binding before selecting operation, resolution, duration, reference roles/counts, or optional flags. A capability record contains model, source, verified_at, operations, parameter JSON Schemas, required_parameters, reference_roles, max_references, and supports_first_frame_with_reference_images. Recheck when the tool, binding, or operation changes; cached evidence is historical, not a live guarantee.

The workspace default remains Seedance 2.5; legacy 2.0 may be selected for a verified capability such as requested 4K or an available lower-cost variant. A face in a shot is a QA concern, not an automatic model switch. Chaining does not override unsupported mixed frame/reference inputs.

Credential names are BYTEPLUS_MODELARK_API_KEY and BYTEPLUS_SEED_AUDIO_API_KEY. A transport may document compatibility aliases. Resolve secrets, region, and base URL at runtime; never serialize credentials into requests, fixtures, snapshots, or logs.

## Directorial axes

Read [seedance-reference.md](seedance-reference.md) when composing a requested concrete camera, lens, lighting, grade, acting, pacing, blocking, or medium axis. Load only the requested axes. Keep one grade, one dominant lighting direction, and one or two camera moves per clip unless the explicitly requested choreography needs more.
