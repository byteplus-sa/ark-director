# Production policy

## Stage evidence and authorization

Draft brief and scene breakdown can identify assets before canon exists. Before dependent production generation, require the appropriate approved recurring/critical elements and declared reference roles. Canon may be created by static sheet generation **or** by acquiring and approving real brand/product/logo assets; prompt-only authoring may deliver a draft without generating or downloading assets. When the brief borrows visual or motion grammar from a cited brand ad or other footage, obtain watchable media first (a `seed_understand`-usable public HTTPS URL, or a local download plus upload when that link is unusable); do not treat scripts or article text as the reference.

The normal flow is brief → draft breakdown → required canon → optional storyboard → optional requested lip-sync audio → shot generation → review → assembly → delivery. Entry and exit evidence live in film-production's stage/handoff contracts. Stage completion cannot be inferred from filenames.

## Persistent production canvas

Initialize every production project with one `showcase.json` and its generated
`index.html`. Treat the JSON as the editable source of truth and the HTML as the
portable production canvas. Keep the canvas cumulative: retain earlier briefs,
elements, prompts, variants, decisions, rejected outputs and provenance while
adding the active stage's current sources and results.

Update the canvas after every material change to a brief, breakdown, manifest,
prompt, element, storyboard, audio asset, video take, selection, assembly,
review record or deliverable. Each section declares its production stage. The
canvas must display all eight lifecycle stages, the current status, the exact
prompt snapshot used for each generated artifact, the referenced elements, and
the available review/selection state.

Before exiting a stage, regenerate `index.html`, open it for visual review, and
run `generate_showcase.py <project> --check --stage <stage-id>`. The check must
match the declared stage and verify that the embedded manifest/source hashes are
current. A missing, invalid or stale page leaves the stage incomplete.
`media-review` may provide temporary OS-native viewing only when the HTML surface
is unavailable or explicitly requested. Record the gap and restore the canvas;
the fallback never replaces the stage checkpoint.

Defaults are proposed until the user accepts the displayed set. Store each axis with value, source (proposed/defaulted/user_confirmed), and approval evidence when available. Approval persists across turns within its stated scope. A generation request does not approve its result.

Only explicit user choice sets selected_variant or approved. Automated advice uses recommended_variant. A technical success is review. Choosing one take does not implicitly reject every other take. Preserve earlier selections and user-written metadata when updating a bounded field.

## Directing guidance

Identify assets using [element-identification.md](element-identification.md). Copy locked identity descriptors faithfully into prompts where needed. Use positive, observable direction. Necessary technical exclusions may define a limited edit scope; negative-only prompt lists are discouraged rather than universally forbidden.

Narrative shots need events, intent, blocking and observable end states. Static character/prop sheets need clear composition and visible design; music/SFX/ambience need a sound arc appropriate to the requested artifact. Do not force story tactics into a static-image or sound-bed prompt.

Screens and typography use approved layout references before production video. Inspect the actual output; reference images do not guarantee pixel-perfect text. Use deterministic finishing when exact copy is required. Never ask the model to render overlay text such as captions, taglines, CTAs or end cards; generate text-free footage and add on-screen text in post with FFmpeg or HyperFrames.

Single-person references should preserve the intended identity and avoid cloning. Clean a sheet only for the requested reference policy or observed duplicate-face defect. Preserve approved visual descriptors and the face anchor; do not infer gender identity from appearance. Visual inspection and model-assisted inspection are evidence, not substitutes for user selection. Unavailable verification remains unresolved.

An explicitly selected supported conditioning input is a promoted composition or motion reference, not a control-only asset. Record the selected manifest, current hash, reference_image/reference_video role, and control_only false. Changing the flag alone does not grant approval.

## Request preflight and review

Before submitting a **generation-bound** request, freeze the exact prompt beside its intended asset, compute hashes, verify ordered bindings/roles, check reference approval and current hashes, and resolve current model/mode capabilities. Run prompt-review for generation-bound prompts; CRITICAL/MAJOR findings must be resolved. Editing a manifest or documentation alone does not trigger generation review. A changed worked example is reviewed offline without buying media.

Acquired brand, logo, packshot, or other `generation: none` elements do not run prompt-review or the default three-sample image set. They still require local persistence, content SHA-256, canvas listing, and explicit `selected_variant` / `approved` before dependent production use. See [element-identification.md](element-identification.md).

Use explicit prompt_type, model, operation, language, requested axes, may_change and must_preserve to route review. A completed review is bound to the request hash and lists applicable rule outcomes and evidence. Missing/empty reviewer output is incomplete. Static image, audio, editing and narrative checks are applied to their relevant artifact types.

The request hash covers exact prompt bytes, model/operation/effective parameters and ordered reference hashes/roles/bindings. Credentials, expiring URLs and timestamps are excluded. Changed request content requires a new review.

## Durable operations

Use one project task_ids.json registry. New records follow schemas/generation-request.schema.json; the registry follows schemas/task-registry.schema.json. Preserve legacy records and report required migration rather than inventing missing facts.

Persist prepared request and immutable prompt snapshot before calling the provider. Save an acknowledged provider ID immediately. Separate submission_status, provider_status and review_status. On a no-ID timeout use submission_unknown and reconcile. On a poll timeout retain the ID and resume the same task. When acceptance cannot be determined, hold for an explicit retry decision explaining possible duplicate cost. A provider terminal failure is evidence to review, not automatic approval of a replacement operation.

On success save each modality locally: Elements under elements/, shot outputs beside the shot, scene outputs in the scene folder, reusable non-shot media in library/. A durable provider URI supplements rather than replaces the local copy. Record artifact/task IDs, actual streams, bytes and SHA-256; download failure can retry the existing artifact without regenerating.

Reference cache identity includes content SHA-256 and storage namespace/account scope. Re-presign expired URLs, reauthenticate unavailable credentials, and re-upload only when content changed or the recorded remote object is missing. Never store secrets or signed URLs as durable identity.

Provider moderation errors remain moderation_rejected with original error evidence. Do not label them false positives solely from the error. Legitimate creative revisions or provider escalation stay within authorization and record the exact delta. Cancel/delete/cleanup of provider tasks requires explicit scope; completion alone does not authorize deletion.

## Generation and review defaults

Generate scenes at natural duration, then chain supported frame modes or assemble approved takes. Continuous single-take/native extension is exceptional; verify every seam. Separate lip-sync audio remains opt-in; follow [audio-video-alignment.md](audio-video-alignment.md).

Use the lowest suitable cost/resolution within the requested behavior. For **Seedream (or other generative) image** selection sets, default to three samples. Sampling variations keep prompt, references, model and effective parameters identical except supported stochastic seed differences. Creative alternatives change only explicitly requested variables with distinct provenance. Explicit requested count wins. Watermark false is the default only for tools that support that parameter. Acquired web/user brand assets are not sampling variants; promote one download as the selected file unless the user asks to compare multiple acquired sources.

Record estimated cost separately from confirmed billing and provider usage. Do not infer billed cost or creative correctness from successful task status. Verify decode, actual streams/duration, opening/transitions/ending, and audible sound arc. Contact sheets support but do not replace playback and listening. Preserve high-quality masters and separately named review proxies.

## Selection state

The manifest is authoritative; selection.json is derived and selection.log is an audit. HTTP and CLI selections use one validated writer with variant membership, project containment, expected revision, writer lock and recoverable batch changes. A validation error cannot modify state. A partially committed batch must recover or report its exact state, not claim success.

## Local preflight tooling

Run validate_request.py with --project, --request, --capabilities, --review and applicable --required-rule values. It is read-only and never submits a provider task. Capability evidence uses capability-evidence.schema.json and self-contained parameter schemas; external schema URLs are rejected.

The operation_store.py helper exposes prepare_operation(root, request, capabilities, review, required_rule_ids) and transition_operation(root, operation_id, expected_status, new_status, provider_task_id, provider_status). Prepare only after the immutable snapshot exists. Validation occurs before registry writes. A file lock, unique operation/asset identities, expected state and atomic replace prevent duplicate local preparation and stale transitions. This does not promise provider idempotency. Legacy or invalid registries are preserved and require a migration preview.
