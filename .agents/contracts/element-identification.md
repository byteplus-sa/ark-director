# Element identification

Identify visible elements during draft breakdown; approve required references before dependent production generation. Static asset prompts create canon and therefore do not require that same asset to be approved already.

| Category | Treatment |
| --- | --- |
| Characters | Canonical sheet for recurring or identity-critical on-camera characters; approved descriptors for incidental people |
| Screen-only people | Lock the visible call UI; describe moving callers and dialogue in text rather than attaching their character sheets as static screen content |
| Locations | Canonical location for recurring or geography-critical spaces; scene-level direction/keyframes for incidental settings |
| Held or operated props | Identify every object, then apply the threshold below; holding an object alone does not require generating a sheet |
| Screens and text | Use deterministic HTML-entrypoint graphics for exact copy/layout; use Seedream only for synthesized screen imagery, then finish exact UI/text deterministically |
| Brand/title cards | Deterministic card for exact typography, logo, product, price, or CTA geometry; preserve source logo rights and visual design |
| Audio | Separate reusable music/SFX/ambience when the requested workflow needs them; native video audio does not require a redundant audio generation |
| Wearables | Always-worn outfit items belong in character design; scene-variant wearables are separate assets when consistency is needed |

## Prop threshold

A branded, recurring (two or more shots), or story-critical object needs a
**locked reference**. Generic one-off cups, pens, food, or background furniture
can be directed in text. A scene-level keyframe is sufficient for a one-off
composition that needs visual review. Do not invent a new generation requirement
merely because an object is visible.

A locked reference is an approved local asset with a content hash — not
automatically a Seedream generation. Prefer acquisition over generation for
real brands and products (see below).

Held/operated canonical props remain separate from the character sheet. Reference only assets actually used by the shot; preserve exact canonical identity descriptors where applicable. Record unresolved required assets and defer their dependent generation.

## Brand, logo, and product acquisition

When the brief authorizes a real brand, logo, packshot, or labeled product:

1. **Reuse** an existing project asset if its content hash still matches the
   needed identity.
2. **Acquire** an official or authorized web/pack shot/logo when no usable local
   file exists — download into `elements/<element-id>/`, keep source copies under
   `refs/` when useful, and record provenance (source URL, download time,
   SHA-256) in the element manifest and/or `PROVENANCE.md`.
3. **Promote** the acquired file to the canonical asset name
   (`prop_…`, `screen_…`, `card_…`), set `source: web_download` or
   `user_supplied`, `generation: none`, and obtain explicit
   `selected_variant` / `approved` from the user.
4. **Generate with Seedream only** when no usable real asset exists, the user
   requests a stylized or fictional substitute, or acquisition is blocked.

Do not invent a fake packshot or logo with Seedream when a downloadable official
or authorized reference is available. Trademark and rights remain with the brand
owner; keep acquired assets local to the production unless publishing is
explicitly authorized. Unknown or unauthorized brands stay de-identified in
analysis and may use placeholder descriptors until the user supplies or
authorizes real identity.

Acquired brand/product assets skip `prompt-review` and the default three-sample
Seedream set because there is no generation-bound prompt. They still require
local persistence, hashes, canvas listing, and explicit user selection or
approval before dependent video use.

## Deterministic and hybrid static graphics

Use `html-graphic-render` when exact words, typography, logo placement, UI,
price/CTA treatment, safe areas, product order, or repeatable poster geometry
carry the design. Store the editable HTML entrypoint and its local CSS/SVG
dependencies beside the versioned PNG and
record `source: deterministic_render`, `generation: deterministic_html`, local
input and font hashes, canvas dimensions, background/alpha mode, renderer
version, and output hash. Validate the record against the
[render-record schema](../skills/html-graphic-render/references/render-record.schema.json).

Use Seedream for synthesized photography, characters, locations, illustration,
materials, or expressive textures. For a hybrid, approve the generated or
acquired text-free image first, bind its current hash as an input, and add all
exact copy and graphic geometry deterministically. The upstream generated layer
keeps its prompt/review/task evidence; the deterministic output keeps its render
record.

Deterministic graphics skip prompt-review, provider registration, and the
three-sample image default. They still require exact-copy, font, overflow,
dimension, alpha, thumbnail-legibility, canvas, provenance, and explicit
selection checks. If both a white-background model reference and transparent
delivery cutout are needed, create and label separate files. Never globally
remove white from a product image when that would erase labels, highlights, or
internal white details.

## Reference footage and brand-ad inspiration

When the brief cites a real brand video ad or other footage for visual or motion
inspiration (as distinct from locking a logo/packshot still):

1. **Prefer a direct public HTTPS URL** that `seed_understand` can consume as a
   video input without downloading.
2. **Download then upload** only when the cited link is a page/platform URL
   (for example YouTube, TikTok, Instagram), auth-gated, expired, or otherwise
   rejected as a video input — persist under the project's pin/reference path,
   then `media_upload` / `media_presign` for analysis.
3. **Do not treat transcripts, scripts, or marketing write-ups as the
   reference.** They may supplement dialogue or claims after the video is
   inspected, but they do not establish shot grammar, motion, or composition.
4. **Route** full reverse-engineering (breakdown → recipe → optional remake)
   through `template-factory`; a lighter “what is this ad doing visually?” pass
   may use `seed_understand` alone inside the active production run.

Inspiration footage is analysis/reference media, not automatic canon. Brand
still acquisition above still governs logos and packshots used as locked
elements.

## Reference eligibility

Elements define persistent identity/design. Approved derivative panels define composition and continuity, with recorded source hashes. Changed source hashes invalidate a panel's previous eligibility. Analysis sketches, blocking maps, and rough control boards remain analysis-only by default; translate their movement into text. An explicitly requested supported grid-conditioning mode needs a separately selected composition reference and documented role, never inferred approval of a control image.
