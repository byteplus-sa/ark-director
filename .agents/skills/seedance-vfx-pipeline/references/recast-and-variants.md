# Recast And Variants

Focused reference for `seedance-vfx-pipeline`. Read [the entrypoint](../SKILL.md) for
mode selection and caller responsibilities. Read [Submission](submission.md)
before any provider call and [Delivery And Manifest](delivery-and-manifest.md)
after acceptance; this file adds route selection, the shared subject map, and
batch variant orchestration on top of them.

- [Route selection](#route-selection)
- [Subject map step](#subject-map-step)
- [Batch variant mode](#batch-variant-mode)
- [Parallel execution](#parallel-execution)
- [Cost preview](#cost-preview)
- [Real-person gates](#real-person-gates)
- [Recast and variant QA](#recast-and-variant-qa)

## Route selection

Choose one route per variant row before writing a prompt. The boundary is what
survives from the source: an edit preserves source pixels outside the changed
region; a recast rebuilds everything except motion.

| Route | Use when | Prompt source | Operation |
| --- | --- | --- | --- |
| VFX edit | Add, remove or restyle an effect, environment or element while the source cast and camera stay | `seedance-vfx-prompt` (2.5 edit grammar) | `omni_reference_task_type: edit` |
| Object Swap | Replace one named character, outfit, product, prop, object or the location and preserve everything else | `seedance-object-swap` | `omni_reference_task_type: edit` |
| Motion Transfer | Keep the source motion, camera path, timing and cuts; rebuild cast, wardrobe, product, location and style from locked references | `seedance-motion-recast` | R2V (below; verified on one case); fallback full-frame edit |
| Restyle | Redraw the whole clip in a new visual medium; keep the performance, motion, camera and cuts; the background changes when the prompt states a location change | `seedance-restyle` | Full-frame edit with a Location Change block; reference route as the alternative |

Decision rules:

- One replaced element with everything else preserved is Object Swap, even when
  the element is a person. Two or more replaced subjects, or any location
  replacement combined with a cast change, is Motion Transfer.
- A preset look (period, claymation, noir, market localization) over the whole
  frame with a new cast is Motion Transfer. A new medium over the original cast
  and place is Restyle. A grade or effect over the original look is a VFX edit.
- When a row changes only the product, prefer Object Swap over Motion Transfer;
  it keeps more of the approved source and needs fewer references.

### Submission parameter differences

Every route submits through `seedance_2_5_create_task` on Seedance 2.5.
Object Swap, Motion Transfer and Restyle bind the muted source master as `@Video 1` (`videos[].role = "reference_video"`),
element sheets and Virtual Portrait `asset://` views as
`images[].role = "reference_image"`, `generate_audio: false` and no `@Audio`
bindings, per the
[video-to-video inputs contract](../../../contracts/video-to-video-inputs.md).
Sound returns in post through the row's recorded post-audio route; this
overrides the `generate_audio: true` example in [Submission](submission.md)
and the manifest template in [Delivery And Manifest](delivery-and-manifest.md).
Apply every other rule in [Submission](submission.md); only these fields
differ.

| Field | VFX edit / Object Swap | Motion Transfer (R2V) | Motion Transfer fallback | Restyle Route A (edit) | Restyle Route B (reference) |
| --- | --- | --- | --- | --- | --- |
| `omni_reference_task_type` | `edit` | `auto`, or the type the route probe verified | `edit` | `edit` | `auto`, or the type the route probe verified |
| `@Video 1` meaning | Editing master; pixels outside the change persist | Motion authority only: motion, poses, screen positions, camera, cuts, timing | Editing master with full-frame replace-all-subjects-and-environment scope | Editing master; every surface redrawn in the style | Authority for composition, poses, camera, cuts and timing |
| `ratio` | Omit; locks to the source | Set explicitly to the source ratio | Omit; locks to the source | Omit; locks to the source | Set explicitly to the source ratio |
| `duration` | Omit; output is approximately the source length, verify the actual duration | Set explicitly (4–30 s) to the source or beat length | Omit; approximately the source length | Omit; approximately the source length | Set to the whole-second source length |
| `images` | Optional; Object Swap uses 1–5 target references | 1–8 subject references plus location; warn above | 1–5 references; split the shot above that | 1–5 style images and anchors | Style images and anchors |
| `resolution` | 480p probe, then the lowest suitable final (720p or 1080p) | Same | Same | Same | Same |

The Motion Transfer default route rebuilt appearance in a 480p probe on one
case (a single person, a Virtual Portrait character, a text-described
location; see `seedance-motion-recast`). It stays provisional for other cases:
until the project records a probe for its own case (multiple subjects, a
location image, a moving camera) confirming that R2V with `@Video 1` as a
motion reference rebuilds appearance rather than retaining source pixels:

1. Run the route probe on the first variant row only, on the critical path,
   before the other rows spend credits on the same route.
2. Inspect the probe for appearance rebuild: new faces, wardrobe and location
   present in every frame, and no retained source pixels.
3. Record the outcome once as a hash-bound project decision (route, operation
   type, probe task ID, evidence). Every row reuses that decision; rows never
   rediscover the route independently.
4. If the probe retains source appearance, switch all Motion Transfer rows to
   the full-frame edit fallback. The prompt changes route, so it returns to
   `seedance-motion-recast` for the fallback wording and to `prompt-review`
   before any further submission.

## Subject map step

Run `source-subject-map` once per approved source clip, before any prompt for
any row. It writes `subject_map.json` (and a readable table) beside the source
clip, bound to the original source SHA-256; the muted master and any trim are
recorded as derivatives of that hash. All variant rows share that one map.

- Every row's prompt cites subject, object and cut IDs from the shared map, so
  mappings stay comparable across variants.
- Any `ambiguities` entry with `resolution: null` blocks prompt writing for
  every row that uses the source. Resolve each ambiguity against extracted frames, re-run or amend
  the map, and record the change before any prompt is authored.
- A changed source hash (a new trim, a different approved take) invalidates the
  map and every prompt and review derived from it.
- The key-beat probe uses a trimmed derivative of the source. Record the trim
  window, its SHA-256 and its `ref_cache.json` entry; the probe prompt cites
  only cuts and subjects inside that window.
- VFX edits that touch no subject may skip the map when the user does not
  request batch variants; Object Swap and Motion Transfer always use it.

## Batch variant mode

Batch mode turns one approved source take into N variants. The source must be
`approved` under the project's `approval_mode` before any row starts.

### Variant table

Record the table in `scenes/scene-NN/variants.md` beside the source scene. The
main agent owns this file; rows change only by an explicit user decision.

| Column | Content |
| --- | --- |
| `variant_id` | Lowercase kebab-case, stable, for example `ph-maria-cola` |
| `market` | Market or locale; drives location, signage language and cast brief |
| `talent` | Element ID of the replacement cast member(s), or `keep` |
| `product` | Element ID of the replacement product, or `keep` |
| `location` | Element ID of the replacement location, or `keep` |
| `preset` | Named look from `seedance-motion-recast` or style from `seedance-restyle`, or `none` |
| `audio` | Post-audio route: `original`, `new`, `mixed` or `re-voiced` |
| `resolution` | Final resolution for this row; lowest suitable |
| `route` | Derived from [Route selection](#route-selection) |
| `shot` | Assigned shot ID for the row's folder |

A row whose only change is `product` routes to Object Swap; any row that
changes `talent` for more than one subject, or `talent` plus `location`, routes
to Motion Transfer.

### Folder and ID naming

Follow the workspace asset-naming contract
([asset naming](../../../contracts/asset-naming.md)):

- Each variant row is its own shot folder in the source scene, numbered after
  the source in gaps of ten: source `s01_sh010`, rows `s01_sh020`,
  `s01_sh030`, and so on. Very large batches may use one scene per market.
- The 480p key-beat probe is take `t01`, the full-duration 480p check is
  `t02`, and the final-resolution take is `t03`. A retry after a legitimate prompt revision is a new take with a
  new prompt snapshot. Record `take_role: probe | full | final` in `shot.md`.
- Each take has an immutable `prompt_<scene>_sh<NNN>_t<NN>_v<NN>.md` beside it.
- The comparison render sits in the row folder, for example
  `s01_sh020_compare_v01.mp4`.
- The row's `shot.md` records `variant_id`, `route`, source shot, source
  SHA-256, `subject_map.json` SHA-256 and the element hashes it used.

### Per-row sequence

Each row runs the same gated sequence. A row may start once its inputs are
stable; it does not wait for unrelated rows.

1. **Elements.** Lock the row's talent, product and location references per
   the element-identification contract: Seedream sheets for invented identity,
   registered as Virtual Portrait assets, and an authorized download for real
   brands and products. Separate images per
   view; no collages. Reuse an element another row already approved instead of
   regenerating it.
2. **Prompt.** Write it with the route's skill: `seedance-vfx-prompt` for VFX
   edit, `seedance-object-swap` for Object Swap, `seedance-motion-recast` for
   Motion Transfer and `seedance-restyle` for Restyle. Every
   source subject gets a mapping or an explicit disposition from the shared
   subject map. No overlay text in the prompt.
3. **Prompt review.** Run `prompt-review` on the exact prepared request for the
   probe and for the final. The probe and final differ in reference video,
   duration or resolution, so each request hash needs a complete review.
   Resolve CRITICAL and MAJOR findings.
4. **Probe.** Submit the 480p key-beat probe (4–5 s). Inspect it for the route
   evidence and the QA list below. A failed probe blocks the final; revise the
   prompt or elements and re-review.
5. **Full duration, then final.** Submit the full duration at 480p after the
   probe passes, then the final resolution after that take passes QA and the
   cost preview is confirmed. Each rung is a separately reviewed request.
6. **Side-by-side.** Render the final against the source with
   `ffmpeg-side-by-side-comparison`: a simultaneous `hstack` for visual
   changes, the staggered split when the rows differ mainly in audio.
7. **Canvas entry.** Add the source, prompt, probe, final, comparison, QA and
   task provenance to the `shot-generation` section, regenerate the canvas and
   pass `--check --stage shot-generation`. Set `review`; approval follows the
   project's `approval_mode` after QA passes.

## Parallel execution

Apply the parallel production rules in AGENTS.md.

- **One agent per variant row.** It owns exactly that row's shot folder, its
  elements when no other row shares them, its prompts and its provider
  operations. Assign a shared element to one owner; other rows wait for its
  approval.
- **Critical path first.** The subject map and, for Motion Transfer, the route
  probe run before the fan-out. Element work for all rows may start in parallel
  with them.
- **Serialize shared state.** The main agent, or a single designated writer,
  applies every change to `task_ids.json`, `showcase.json`, `ref_cache.json`,
  `variants.md` and selection manifests. Row agents hand prepared operations,
  acknowledged task IDs and canvas entries to that writer; they never write
  those files concurrently.
- **Never submit the same request twice.** Each prepared operation has one
  owner and one transport. A row agent never resubmits another row's request,
  and no request goes through a second agent or transport.
- **Reconcile ambiguous timeouts.** A no-ID timeout becomes
  `submission_unknown`; reconcile with the provider task list before any retry.
  A poll timeout resumes the recorded task ID.
- **Upstream changes revalidate.** A changed source take, subject map or shared
  element invalidates dependent prompts, reviews and probes in every row.
  Speculative row work never changes an approved input or user selection.
- **Concurrency limits.** Respect transport and account concurrency; queue rows
  rather than exceed them. The main agent integrates rows, runs final canvas
  verification and reports to the user.

## Cost preview

Before the first paid submission, present a cost preview and obtain user
confirmation for the batch unless the user has already authorized that exact
scope and budget. A change in row count, duration or resolution beyond the
confirmed scope needs a new confirmation.

| Row | Route | Probe (s × res) | Final (s × res) | Estimated probe | Estimated final |
| --- | --- | --- | --- | --- | --- |
| `ph-maria-cola` | Object Swap | 5 × 480p | 12 × 720p | from rate | from rate |
| ... | | | | | |
| **Total** | | Σ probe seconds | Σ final seconds | Σ | Σ |

- Estimate each line as seconds × per-second rate at that resolution, from
  current pricing evidence (`arkcli-pricing`) or the usage of a comparable
  confirmed task. State the source of the rate.
- Batch total = variants × (probe + final). Include the Motion Transfer route
  probe and a stated allowance for revision takes.
- Use the lowest suitable resolution: 480p for probes, 720p for finals unless
  the delivery needs 1080p.
- Keep the estimated cost separate from confirmed billing. Record the confirmed
  cost per task in `task_ids.json` and the row's `shot.md` when available, and
  report actual totals against the preview.

## Real-person gates

Apply the [video-to-video inputs contract](../../../contracts/video-to-video-inputs.md),
the element-identification contract
([element identification](../../../contracts/element-identification.md)) and
the production policy ([production policy](../../../contracts/production-policy.md)).

- **Source footage.** A recorded user rights decision covers the footage and the
  people visible in it, with its scope. The subject map describes people by
  observable descriptors only; never name or infer who they are.
- **Person in the source video.** A muted master that shows a person is bound
  as an `asset://` video registered in the private asset library; image assets
  of the person do not clear the provider's video check.
- **Replacement talent.** Every new character is a Virtual Portrait asset
  registered from an approved invented design. Liveness verification is not
  used. A real, identifiable person as the target is out of scope.
- **Voice.** Reusing or cloning a real person's voice needs recorded voice
  consent, separate from footage rights.
- **Rights are not selection.** Neither `approve_for_me` nor a creative choice
  supplies a rights decision. A missing record blocks that row.
- **Privacy rejections.** A `PrivacyInformation` or other sensitive-content
  rejection is evidence to diagnose. Record the code, task and inputs, stop the
  affected row and report. Follow the contract's rejection rule; do not blur,
  crop, swap or re-encode inputs, or reword the prompt, to get past it. When the
  rejection concerns the shared source, pause every row that uses it.

## Recast and variant QA

Inspect the actual probe and final by playback, not only a contact sheet.
Record each check as pass, fail or not applicable in the row's `shot.md` and
canvas entry.

- [ ] **Residual originals.** The replaced product, wardrobe, prop, person or
      location does not appear in any frame, including reflections, edges,
      entries and exits.
- [ ] **Subject count.** Each cut shows the subject map's people and
      swappable objects minus those with a `remove` disposition, with no
      extra or missing subjects.
- [ ] **Accessory bleed.** New characters wear only what their references
      show; no glasses, jewelry, hats or logos carried over from the source.
- [ ] **Identity per appearance.** Each mapped identity holds on every
      appearance, after occlusions, turns and cuts, including profile views.
- [ ] **Contact points.** Hands, grips and object contacts land where the
      subject map records them; no floating or merged objects.
- [ ] **Motion fidelity.** Poses, screen positions, camera path, cut timing and
      duration match the source within the route's expectations.
- [ ] **Post audio.** The muxed route matches the row's `audio` column, the
      final length equals the picture, and speaking subjects stay in sync.
- [ ] **No baked text.** No captions, taglines, CTAs or new signage copy in the
      footage; add on-screen text in post.
- [ ] **Logo and label fidelity.** Real product labels match the approved
      element; inspect the product on every appearance.
- [ ] **Technical.** Decode, streams, resolution, duration and audio probed;
      the HEVC master is kept and a review-safe H.264 derivative produced.
