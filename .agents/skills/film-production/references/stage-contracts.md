# Production Stage Contracts

Use these contracts to determine the next safe stage. A later stage may begin
only when its entry evidence exists. Keep unavailable future departments as
explicit gaps rather than fabricating their outputs.

## Stage checkpoint for every stage

The project's stage ledger is `studio/stages.json`, kept only by
`uv run python .agents/scripts/studio_project.py stage <project> {show|start|complete|reopen|skip}`.
It holds the eight stages in fixed order (`brief-development`,
`scene-breakdown`, `canon-elements`, `storyboard-visual-plan`,
`audio-preparation`, `shot-generation`, `assembly-review`, `delivery`) and is
never hand-written. `studio_project.py init` creates an empty Studio project and
`sync` creates it from the shot manifests: an outline frame for each planned shot and a built frame for
each take, without deleting prior frames, variants or decisions. Exact
generation prompts stay in their immutable snapshot files, referenced from the
manifests.

Read `approval_mode` from `project.md` at start/resume and before each stage
decision. New projects write `approval_mode: approve_for_me` before the first
stage; `ask_for_approval` requires user choices. A legacy project without the
field uses the default for new decisions only. Both modes keep all eight stages
and the same checkpoint. Record the effective mode, decision actor, reason,
review outcome, current selection or stage lock, and unresolved gaps in the
relevant manifest. `status` detects only the codes listed in the production
policy (missing, modified or unmanaged assets, a changed take, a placed take that
differs from the selection, a frame and its timeline host disagreeing, a pending selection); it
checks takes and Studio assets and does not read review, decision or scene
files. Re-run prompt-review or reopen the stage when those files change. The
storyboard `approval:` line is refreshed from the manifest by `sync`.

Every stage exit additionally requires:

1. `studio_project.py stage <project> complete <stage-id>` passes. It requires
   a `project.md` with a valid `approval_mode` for `brief-development`; for `scene-breakdown` through
   `audio-preparation` a Studio project with no blocking `status` issue; for
   `shot-generation`, `assembly-review` and `delivery` also a placed take for
   every shot and a passing pinned `check`; for `assembly-review` and `delivery`
   also no pending selection and the stage locks (a `picture` lock, plus an
   `audio` lock unless audio-preparation was skipped, at `assembly-review`; a
   `final_master` lock on the delivery render at `delivery`, each recorded with
   `record-lock`); and for `delivery` the newest `render` record at a
   delivery-level quality (`standard`, `delivery` or `high`; drafts and manual
   records are ignored) still matches its file, was rendered from the Studio tree
   as it is now (`index.html`, `hyperframes.json`, `compositions/`, `assets/`),
   and its frames equal the placed takes. `storyboard-visual-plan` and
   `audio-preparation` may instead be `skip`ped with `--reason`; a skipped stage
   counts as done for later stages;
2. the stage's inputs, outputs, prompts, bindings, review evidence and
   mode-authorized decisions or pending recommendations are in the manifests;
3. the project has been opened in Studio for visual review after the latest
   material edit;
4. `handoff.md` records the completed stage, current selections, operations
   still in flight with their registry IDs, open defects, and the next action.

`handoff.md` is plain Markdown for resuming work, not an approval record. Keep
it short and overwrite it at each exit rather than appending history.

A pre-Studio canvas project with `showcase.json` keeps its canvas checkpoint instead
(`generate_showcase.py <project> --check --stage <stage-id>`). The
stage-specific required outputs below describe what the matching stage must
expose in the manifests; Studio frames exist for shot video takes only. A CLI/OS-player review does
not replace this checkpoint.

## 1. Brief and development

Entry: user intent or an existing `project.md`.

Required output: `approval_mode`, audience, format, runtime, aspect ratio,
story objective, tone, creative constraints, known rights constraints, budget
posture, and unresolved questions recorded in `project.md`. Confirmed
directorial defaults (structure, energy level, camera and light stance, lens,
grade, pacing, acting, staging, medium, audio) from
`brief-intake` persisted as a `locked` block in `project.md` frontmatter.
The brief is the `brief-development` stage source; `stage complete` checks that `project.md` is a valid record.

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
For every narrative, ad, micro-drama, music-video or showcase scene it also
requires a shot plan from `seedance-shot-design` in the scene file's
`## Shot plan` section: per shot, duration, size, angle, camera move, lens
intent and a named light source with key side, the energy level, and where each
confirmed project axis appears. The plan is `draft` until the scene's locations
are approved in Stage 3 and is revalidated before Stage 6. A scene that is exempt
(user lock, static-by-design format, an explicit per-shot camera plan from another skill, plate
for cutdown, source-preserving edit, extension continuation, or no video shot)
records its `static_reason` instead. The `scene-breakdown` stage lists
every scene/shot manifest (each shot becomes an outline frame in the Studio
storyboard), its shot plan section, and its required production-input inventory.

Exit: every planned scene has observable action, a draft shot plan or a recorded
exemption, and an inventory of required production inputs, with missing
approvals recorded as unresolved.

## 3. Canon and elements

Entry: breakdown identifies recurring characters, locations, or props.

Required output: one flat `elements/<element-id>/` folder per reusable element,
manifest, reference files, hashes, variants, and lifecycle states. Generated
sheets carry prompt snapshots; acquired brand/product/logo assets carry
provenance and `generation: none`; deterministic screens/cards/posters carry an
editable HTML entrypoint with local CSS/SVG dependencies, a render record, and
`generation: deterministic_html`
instead of a model prompt or provider task. **Before locking
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
Use a deterministic HTML entrypoint with local CSS/SVG dependencies for exact
typography, screen/UI, product lineup, price/CTA, and poster geometry. Use
Seedream for synthesized image content; a
hybrid binds the selected image as a hashed input and finishes exact copy/layout
deterministically.
Record missing required references before dependent tasks are submitted.
The `canon-elements` manifests record every variant (acquired, generated, or
deterministically rendered), its prompt or provenance/render record,
recommendation/selection state and downstream role. Studio's Assets panel shows
only the locked (selected, approved) elements, copied as
`LOCKED_<element>_<vNN>.<ext>`; candidates and rejected samples stay in
`elements/`. `studio_project.py lock-element` records the decision and does this
copy; `sync-elements` repairs it and rewrites the static candidates page
(`review/elements.html`).

Exit: every required canonical element has an approved selected variant, or the
dependent scene is explicitly marked unresolved. The element list has been
cross-checked against the Element identification checklist and no gaps remain.
An approved selected variant may be a downloaded packshot/logo, generated
sheet, or deterministic graphic — all satisfy exit when the file hash, passing
review, and mode-authorized decision are recorded. An agent decision cannot
replace an explicit user lock.

## 4. Storyboard and visual plan

Entry: scene objective, geography, continuity state, and approved relevant canon
exist before dependent panel generation. A text-only visual plan may be drafted
earlier and stays draft until its input requirements are satisfied.

Required output: beat/panel plan that follows the scene's shot plan, bound
references, prompts, generated panels or prompt package, continuity review,
provenance, and video-handoff eligibility.
Record these together in the `storyboard-visual-plan` manifests; Studio shows shot takes only.

Exit: required panels have a mode-authorized approval and all source element
hashes remain current, or the scene has a mode-authorized direct-to-video path.

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

Entry: shot objective, the scene's revalidated shot plan (or recorded exemption), selected
video mode, approved inputs, reference roles, prompt snapshot target, duration,
and any requested audio (if Stage 5 was completed) exist. Before submission the `prompt-review` gate has passed for
every prompt being submitted. Review inline by default; use a sub-agent only
when the user explicitly requests sub-agent prompt review for the project or
specific generation. The ordered `references:` array is verified 1:1
against `shot.md` (same files, same order, same `@Image N` / `@Video N` /
`@Audio N` bindings); and the Seedance 2.5 draft pass explicitly uses `resolution: "480p"`.
Record the separate delivery target and any explicit user override or verified
operation constraint under the production policy.

Required output: task registry entry, local media, exact prompt snapshot,
provider metadata, actual media properties, cost fields, SHA-256, semantic QA
including a comparison of the take against its shot plan, and `review` status. Resolution is raised only after the current pass is
approved (final-candidate gate). For multi-shot productions, review the draft
assembly and record picture/audio decisions before generating final takes.
Each final request is separately registered and reviewed against its complete
request hash; each final output needs fresh playback, audio and creative QA and
a mode-authorized selection before it replaces the draft in Studio. A 480p
output alone does not establish native Draft/promotion support.
The `shot-generation` stage records every take, exact prompt, ordered element
bindings, metadata, inspection result and selection state. When a style/grammar
reference pin (or other watchable reference video) exists, that pin and each
generated take must be playable for review: each take is viewable in its Studio
frame, and the pin is recorded in the manifest and played from its file. A pre-Studio canvas
project instead lists them in one `kind: "takes"` group using
`groups[].takes[].media` objects (`{ "type": "video", "src": "…" }`); follow
`showcase-html` production-canvas and schema.

Exit: a passing take has a hash-bound, mode-authorized selection. In
`ask_for_approval`, the recommendation remains pending until the user chooses.
If no take passes, make a bounded correction within the run budget or leave the
shot blocked.

## 7. Assembly and review

Entry: approved takes and any requested audio assets exist.

Required output: ordered edit, review render, transition and continuity review,
audio presence check, technical decode QA, and outstanding notes.
The `assembly-review` stage keeps its approved inputs and comparison renders on
the same page.

Exit: picture and audio have separate mode-authorized locks bound to the exact
artifact and passing review hashes. Audio lock is required when audio is in
scope. In `ask_for_approval`, wait for explicit user locks. Full editorial,
color, and sound-post department contracts are future work tracked in the
lifecycle specification.

## 8. Delivery

Entry: approved picture and audio plus a known delivery target.

Required output: inspected master, review proxy if needed, caption or localization
status, delivery metadata, hashes, and archive pointers.
The `delivery` stage exposes those files and final approval evidence.

Exit: inspect the actual local master, then record a mode-authorized final
master lock bound to its file and review hashes. In `ask_for_approval`, wait for
the user's explicit acceptance. Publishing, sending, or external delivery needs
separate authorization in either mode.
