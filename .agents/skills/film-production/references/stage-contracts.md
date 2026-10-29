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

Read independent `approval_mode` and `review_mode` from `project.md` at
start/resume and before new actions; the production policy defines their values.
Default review mode uses inline preflight and short actual candidate/final
sanity records, not mandatory full checklist reports. Strict retains detailed
reviews. Explicit required rules and any supplied report remain binding.
Record the effective approval mode,
decision actor, reason, review outcome, current selection or stage lock, and
unresolved gaps in the relevant manifest. `status` checks takes and Studio
assets only; it does not read review, decision or scene files, so re-run
mode-appropriate preflight or reopen the stage when those files change.

Every stage exit additionally requires:

1. `studio_project.py stage <project> complete <stage-id>` passes. Its
   per-stage requirements (valid `project.md`, clean `status`, placed takes and
   a passing `check` at delivery in default mode or all three frame stages in
   strict mode, no pending selection, `picture`/`audio`/`final_master`
   locks, a current delivery-level `render`) are the stage-exit table in the
   production policy. An unrun check records `check_ran: false` and
   `check_ok: false`; lightweight gates remain in both modes. Only
   `storyboard-visual-plan` and `audio-preparation` may
   be skipped with `--reason`;
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

Required output: `approval_mode`, `review_mode`, audience, format, runtime, aspect ratio,
delivery resolution, story objective, tone, creative constraints, known rights
constraints, run budget, and unresolved questions recorded in `project.md`.
Confirmed directorial defaults (structure, energy level, camera and light
stance, lens, grade, pacing, acting, staging, medium, audio) from
`brief-intake` persisted as a `locked` block in `project.md` frontmatter. The
brief also records:

- the **audio route**: native dialogue, picture only with score, ambience and
  SFX built in post, opt-in separate lip-sync audio, or silent;
- the **look intent**: ungraded original model colours unless a grade or a
  capture-format look is requested, in which case it is a post treatment;
- the **on-screen copy** (titles, captions, CTA, end card) that post will add,
  and any label the user or platform requires;
- the **compact premise**: intended audience response, what carries attention,
  and why the ending matters; alternatives only when direction is unresolved
  or requested, with no mandatory arc;
- **early sound and editorial intent**: what picture and sound reveal, withhold
  or emphasize, including intentional silence, before generation;
- **project-specific artistic criteria**: a small relevant set with critical
  evidence identified for actual take and final-edit playback/listening.
  Coverage and duration serve these criteria; no contrast, hold, turn, wow or
  fixed cadence quota applies.

The brief is the `brief-development` stage source; `stage complete` checks that
`project.md` is a valid record.

Exit: the production objective, constraints, and directorial defaults are clear
enough to break down. When the brief cites brand ads or other footage for
visual or motion inspiration, record the reference URL or local path and treat
local media acquisition and native video/image inspection as unresolved until
decodable media and a capable reviewer are available. Prefer native/local
inspection; use available MCP understanding tools when needed, under privacy
and cost constraints. No upload or cloud call is required when native
inspection suffices. Scripts and
article text alone do not satisfy that gap.

## 2. Scene and production breakdown

Entry: an accepted brief and available story or script material. Draft scene
and shot breakdown may precede canonical asset generation; it identifies which
assets are required and does not make a prompt ready for production submission.
If the brief borrows grammar from cited reference footage, that media must
already be locally decodable and inspected through native video/image tools
or a capable permitted understanding tool,
with timestamped frames and local timing measurements, before treating
visual/motion claims as breakdown evidence. Missing perception stays unresolved;
reference audio needs native/local audio perception, an available
audio-understanding tool, or human listening. MCP or local ASR/separation may
assist; local-only tools are not required.

Required output: scene list, cast, locations, props, dialogue, sound needs,
continuity states, delivery assumptions, and scene-level acceptance criteria.
For character-performance scenes, require `## Performance plan` from
`acting-direction` with source evidence, intentions and a
trigger/registration/response ledger under
[Performance direction](../../../contracts/performance-direction.md).
For staged fights, include the `seedance-fight-choreography` state and exchange
ledger. Reconcile their readability needs with shot design.
For every narrative, ad, micro-drama, music-video or showcase scene it also
requires a shot plan from `seedance-shot-design` in the scene file's
`## Shot plan` section: per shot, duration, size, angle, camera move, lens
intent and a named light source with key side, the energy level, and where each
confirmed project axis appears. Derive coverage and lengths from intended
perception, preserving equal timing, repetition and sustained holds when useful.
Short multi-shot sequences are optional. About 0.8 s per shot is a provisional
caution, not a provider limit or guaranteed merge threshold. Preserve requested timing;
offer assembly for precision or demonstrated failure, returning conflicts with
locked workflows rather than silently replacing them. A long action with
people that would need extension is planned as short single passes held by a
blocking map unless `asset://` Virtual Portrait identities are available. The plan is `draft` until the scene's locations
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
the element list**, walk every beat of every scene/shot against the tracked
element-identification contract — verify that visible characters, settings,
props, screen/UI surfaces, brand/title cards, and recurring audio have been
identified and assigned the appropriate treatment. Recurring/identity-critical on-camera characters
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
Generic containers, jars, cases, labels and generated screens tend to grow
invented lettering: give a story prop a reference sheet, and describe recurring
non-sheet props positively as plain ("plain white ceramic jug, smooth solid
surface") or leave them out.
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
element references, prompts, generated panels or prompt package, continuity
review, and provenance. Boards are planning and review artifacts: their staging
is translated into shot prompt text and they are never bound as Seedance
references.
A scene board adds `scenes/scene-NN/board.md` (the level, L1, L2 or L3 with L2 as
the default, and its reason; one record per panel), the annotated sheet pages, an
optional overview and animatic, and a scene decision. Failed panels are repaired by
Seedream image editing on those panels only, never by regenerating the whole board.
Record these together in the `storyboard-visual-plan` manifests; Studio shows shot takes only.

Exit: required panels have a mode-authorized approval and all source element
hashes remain current, or the stage is skipped because the shot plan already
carries the staging. A scene board also needs `scene_board.py check` to pass and
no stale sheet page or animatic segment.

## 5. Audio preparation (optional — requested lip-sync audio or beat-led music)

Entry: exact dialogue and planned scene duration exist and the user has
explicitly requested lip-synced dialogue audio, or a music track exists that the
cut must follow.

Required output: exact audio prompt, local audio file, duration, transcript or
dialogue timing, media inspection, SHA-256, and manifest linkage.
Expose the audio player, prompt and timing evidence in `audio-preparation`.

Exit: audio duration fits the planned video and dialogue mappings are verified.

When the user has not requested lip-synced audio, skip this stage and proceed
directly to shot generation. Seedance's native audio handles dialogue by
default. A music track that the cut must follow (music video, beat-led spot)
may be prepared here so shot durations can be planned to it. Score and ambience
for a picture-only project are otherwise built after picture lock, at
assembly, to the cut's measured length. This does not postpone sound or editorial
intent: carry the brief's picture-and-sound relationships through the breakdown.
Final assets need not exist early; final cues require measured timing and listening.

## 6. Shot generation

Applicable new or revised character performances need the current performance
plan and its `seedance-acting-console` encoding, with `acting.plan_bound` and
applicable `fight.readable_exchange` checks. Missing material evidence leaves
review incomplete. Preservation-only edits retain source acting.

Entry: shot objective, the scene's revalidated shot plan (or recorded exemption), selected
video mode, approved inputs, reference roles, prompt snapshot target, duration,
and any requested audio (if Stage 5 was completed) exist. Before submission,
minimal inline preflight passes in default mode; strict mode requires the
`prompt-review` gate for every prompt. Review inline; use a sub-agent only
when the user explicitly requests sub-agent prompt review for the project or
specific generation. The ordered `references:` array is verified 1:1
against `shot.md` (same files, same order, same `@Image N` / `@Video N` /
`@Audio N` bindings); the request's `generate_audio` matches the brief's audio
route; no storyboard image is bound; and every new Seedance 2.5 request uses
`resolution: "480p"` and boolean `draft: true` in every review mode, including
edits, extensions, probes and variants. Resolve capability or transport
conflicts before submission; never fall back to plain 480p.
Initialize Studio at the delivery target, not the draft resolution. New Seedance
2.5 generations have no skip-draft override. Other models without native Draft
use ordinary 480p tests.

Required output in either mode: task registry entry, local media, exact prompt snapshot,
provider metadata, actual media properties, cost fields, SHA-256, semantic QA
including actual output sanity against the brief and shot plan, and `review`
status. Strict detailed QA additionally records frame samples with
top-left corner crops for leaked text, a speech-to-text diff for every locked
line. When using drafts, resolution is raised only after the current pass is
approved (final-candidate gate); a native Draft is promoted by its
`draft_task_id` without changing its inputs. For multi-shot productions, review the draft
assembly and record picture/audio decisions before generating final takes.
Each final request is separately registered and preflighted against its complete
request hash, with a report when strict or explicitly required; each final output
needs fresh playback, audio and creative QA and
a mode-authorized selection before it replaces the draft in Studio. A plain
480p output requested without `draft: true` cannot be promoted.
The `shot-generation` stage records every take, exact prompt, ordered element
bindings, metadata, inspection result and selection state. When a style/grammar
reference pin (or other watchable reference video) exists, that pin and each
generated take must be playable for review: each take is viewable in its Studio
frame, and the pin is recorded in the manifest and played from its file. A pre-Studio canvas
project instead lists them in one `kind: "takes"` group using
`groups[].takes[].media` objects (`{ "type": "video", "src": "…" }`); follow
`showcase-html` production-canvas and schema.

Exit: a passing take has a hash-bound, mode-authorized selection. Playback and
listening must demonstrate its declared critical performance beats, listener
responses and applicable fight continuity. Record beat IDs and timestamps;
unavailable inspection remains unresolved. In
`ask_for_approval`, the recommendation remains pending until the user chooses.
If no take passes, make a bounded correction within the run budget or leave the
shot blocked.

## 7. Assembly and review

Entry: approved takes and any requested audio assets exist.

Inspect the actual edit against accepted performance beats. Trims must retain
critical registration, response, exact dialogue and continuity; an accepted
raw take does not establish acceptance of the cut.
Review what the edit reveals, withholds and emphasizes against the brief's
project-specific artistic criteria. Use full-speed playback and actual
listening with artifact hashes and timestamps, not only technical checks or
transcripts. Missing perception and failed critical criteria remain blocking.

Required output: ordered edit, review render, transition and continuity review,
audio presence check, technical decode QA, and outstanding notes. Assembly
includes the creative pass plus conform, trim, crop, overlays, end card and mix with no grade, from
exact-length intermediates encoded once; post beds for picture-only projects
are built here to the measured cut. Audio defects are fixed word by word, and
re-voicing keeps the source soundtrack (see
[production defaults](production-defaults.md)). The `assembly-review` stage
keeps its approved inputs and comparison renders together.

Exit: picture and audio have separate mode-authorized locks bound to the exact
artifact and passing review hashes. Audio lock is required when audio is in
scope. In `ask_for_approval`, wait for explicit user locks. Full editorial,
color, and sound-post department contracts are future work tracked in the
lifecycle specification.

## 8. Delivery

Entry: approved picture and audio plus a known delivery target.

Required output: inspected master, review proxy if needed, caption or localization
status, delivery metadata, hashes, and archive pointers. On-screen text comes
only from post overlays; add no AI or fictional label unless the user, platform
or brief requires one.
The `delivery` stage exposes those files and final approval evidence.

Exit: inspect the actual local master, then record a mode-authorized final
master lock bound to its file and review hashes. In `ask_for_approval`, wait for
the user's explicit acceptance. Publishing, sending, or external delivery needs
separate authorization in either mode.
