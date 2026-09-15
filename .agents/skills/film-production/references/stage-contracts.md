# Production Stage Contracts

Use these contracts to determine the next safe stage. A later stage may begin
only when its entry evidence exists. Keep unavailable future departments as
explicit gaps rather than fabricating their outputs.

## Canvas checkpoint for every stage

Create the project's `showcase.json` and generated `index.html` during Stage 1.
Keep all eight stage records in the manifest from initialization onward. Each
stage adds its sources and stage-tagged sections without deleting prior variants
or decisions. Exact generation prompts use `promptFile` so their immutable
snapshot is embedded into the portable page.

Every stage exit additionally requires:

1. the canvas current stage and status match the stage being completed;
2. the stage shows its inputs, outputs, prompts, bindings and review evidence;
3. `index.html` has been regenerated and opened after the latest material edit;
4. `generate_showcase.py <project> --check --stage <stage-id>` passes.

The stage-specific required outputs below describe what the matching canvas
section must expose. A CLI/OS-player review does not replace this checkpoint.

## 1. Brief and development

Entry: user intent or an existing `project.md`.

Required output: audience, format, runtime, aspect ratio, story objective, tone,
creative constraints, known rights constraints, budget posture, and unresolved
questions recorded in `project.md`. Confirmed directorial defaults (structure,
camera, lens, lighting, grade, pacing, acting, staging, medium, audio) from
`brief-intake` persisted as a `locked` block in `project.md` frontmatter.
The canvas embeds or links this brief as the `brief-development` stage source.

Exit: the production objective, constraints, and directorial defaults are clear
enough to break down. When the brief cites brand ads or other footage for
visual or motion inspiration, record the reference URL or local path and treat
watchable-media acquisition (direct `seed_understand`-usable HTTPS URL, or
download plus upload when unusable) as unresolved until obtained — scripts and
article text alone do not satisfy that gap.

## 2. Scene and production breakdown

Entry: an accepted brief and available story or script material. Draft scene
and shot breakdown may precede canonical asset generation; it identifies which
assets are required and does not make a prompt ready for production submission.
If the brief borrows grammar from cited reference footage, that media must
already be watchable (URL accepted by `seed_understand`, or a local pin after
upload) before treating visual/motion claims from the ad as breakdown evidence.

Required output: scene list, cast, locations, props, dialogue, sound needs,
continuity states, delivery assumptions, and scene-level acceptance criteria.
The `scene-breakdown` canvas stage lists every scene/shot manifest and its
required production-input inventory.

Exit: every planned scene has observable action and an inventory of required
production inputs, with missing approvals recorded as unresolved.

## 3. Canon and elements

Entry: breakdown identifies recurring characters, locations, or props.

Required output: one flat `elements/<element-id>/` folder per reusable element,
manifest, reference files, hashes, variants, and lifecycle states. Generated
sheets also carry prompt snapshots; acquired brand/product/logo assets carry
provenance and `generation: none` instead of a Seedream prompt. **Before locking
the element list**, walk every beat of every scene/shot against the Element
identification checklist in AGENTS.md — verify that visible characters, settings,
props, screen/UI surfaces, brand/title cards, and recurring audio have been
identified and assigned the appropriate treatment under the tracked
element-identification contract. Recurring/identity-critical on-camera characters
and recurring/geography-critical spaces need canonical references; incidental
people/settings may use descriptors or scene direction. Screen-only callers use
a locked UI with text-directed movement/dialogue, not character sheets as static
screen content. Apply the prop threshold rather than turning every visible object
into a generation requirement. For authorized real brands, logos, and labeled
products, prefer official or authorized web/user downloads over Seedream; generate
only when no usable real asset exists or a stylized substitute is requested.
Record missing required references before dependent tasks are submitted.
The `canon-elements` canvas section shows every variant (acquired or generated),
its prompt or provenance, manifest, recommendation/selection state and downstream
role.

Exit: every required canonical element has an approved selected variant, or the
dependent scene is explicitly marked unresolved. The element list has been
cross-checked against the Element identification checklist and no gaps remain.
An approved selected variant may be a downloaded packshot/logo or a generated
sheet — both satisfy exit when hashes and user selection are recorded.

## 4. Storyboard and visual plan

Entry: scene objective, geography, continuity state, and approved relevant canon
exist before dependent panel generation. A text-only visual plan may be drafted
earlier and stays draft until its input requirements are satisfied.

Required output: beat/panel plan, bound references, prompts, generated panels or
prompt package, continuity review, provenance, and video-handoff eligibility.
Expose these together in the `storyboard-visual-plan` canvas stage.

Exit: required panels are approved and all source element hashes remain current,
or the scene has an explicitly approved direct-to-video path.

## 5. Audio preparation (optional — when user requests lip-synced dialogue)

Entry: exact dialogue and planned scene duration exist, and the user has
explicitly requested lip-synced dialogue audio.

Required output: exact audio prompt, local audio file, duration, transcript or
dialogue timing, media inspection, SHA-256, and manifest linkage.
Expose the audio player, prompt and timing evidence in `audio-preparation`.

Exit: audio duration fits the planned video and dialogue mappings are verified.

When the user has not requested lip-synced audio, skip this stage and proceed
directly to shot generation. Seedance's native audio handles dialogue by
default.

## 6. Shot generation

Entry: shot objective, selected video mode, approved inputs, reference roles,
prompt snapshot target, duration, and any requested audio (if Stage 5 was
completed) exist. Before submission the `prompt-review` gate has passed for
every prompt being submitted; the ordered `references:` array is verified 1:1
against `shot.md` (same files, same order, same `@Image N` / `@Video N` /
`@Audio N` bindings); and the pass uses the lowest suitable resolution for the
current prototype.

Required output: task registry entry, local media, exact prompt snapshot,
provider metadata, actual media properties, cost fields, SHA-256, semantic QA,
and `review` status. Resolution is raised only after the current pass is
approved (final-candidate gate).
The `shot-generation` stage shows every take, exact prompt, ordered element
bindings, metadata, inspection result and selection state. When a style/grammar
reference pin (or other watchable reference video) exists, that pin and each
generated take must appear as playable players on this stage in the same
`kind: "takes"` group using `groups[].takes[].media` objects
(`{ "type": "video", "src": "…" }`). Flat `cards` or string `media` paths do
not render players — follow `showcase-html` production-canvas and schema.

Exit: the user approves a take or requests a bounded revision.

## 7. Assembly and review

Entry: approved takes and any requested audio assets exist.

Required output: ordered edit, review render, transition and continuity review,
audio presence check, technical decode QA, and outstanding notes.
The `assembly-review` stage keeps its approved inputs and comparison renders on
the same page.

Exit: explicit picture and audio approval. Full editorial, color, and sound-post
department contracts are future work tracked in the lifecycle specification.

## 8. Delivery

Entry: approved picture and audio plus a known delivery target.

Required output: inspected master, review proxy if needed, caption or localization
status, delivery metadata, hashes, and archive pointers.
The `delivery` stage exposes those files and final approval evidence.

Exit: explicit user approval of the final deliverable.
