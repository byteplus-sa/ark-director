# Video-to-Video Inputs

This contract covers identity references, source footage and audio preservation
for Seedance video-to-video work: Motion Transfer
(`seedance-motion-recast`), Object Swap (`seedance-object-swap`), Restyle
(`seedance-restyle`) and the shot runner (`seedance-vfx-pipeline`).

- [Identity references: Virtual Portrait assets](#identity-references-virtual-portrait-assets)
- [Source footage](#source-footage)
- [Audio preservation](#audio-preservation)
- [Requested audio changes](#requested-audio-changes)
- [Provider rejections](#provider-rejections)

## Identity references: Virtual Portrait assets

Every person or character identity bound into a video-to-video request is a
Seedance Virtual Portrait asset: an Advanced Creation Rights AIGC asset,
referenced as `asset://<asset_id>`. This is the BytePlus-recommended path.

- **What qualifies.** An approved invented character element, either a
  Seedream sheet view or a user-supplied invented design. A Virtual Portrait
  must not resemble a real, identifiable person. A brief that needs a specific
  real person as the target is outside these workflows; offer a Virtual
  Portrait character instead.
- **One subject per group.** Register with
  `ark_asset_create(subject="<exact element name>", sources=[...])`. Never mix
  two characters in one group. A medium-specific design, such as a clay or
  anime version of a character, is its own subject (`"Mara (claymation)"`).
- **Sources.** One image per view, never a collage or turnaround strip. The
  best set is a front-facing close-up plus a full-body view in portrait
  orientation. Sources are public HTTPS URLs or `media_upload` object keys.
- **Activation.** Wait for `all_active`, or `ark_asset_get` status `Active`,
  before binding. Assets work only with endpoints in the same `project_name`.
- **Order of work.** Seedream rejects `asset://` inputs, so design and approve
  the sheet first, then register the approved views.
- **Record.** In the element manifest, store the subject name, `group_id`, each
  view's `asset_id`, the source file path and SHA-256, the status and the
  registration time. Approval binds to the source hash. When the approved
  source changes, register a new asset and invalidate dependent reviews.
- **Prompt wording.** Refer to each asset by its binding position
  (`@Image 1`), never by asset ID. A short production label tied to that
  binding (`Mara: @Image 1 and @Image 2`) may name the character in later
  lines.

Non-identity references (products, props, locations, style frames) upload
normally through `media_upload`. Choose views without people. When a garment or
product exists only on a model, use a flat-lay, mannequin or packshot view, or
register that model as a Virtual Portrait when the model is an invented
character.

## Source footage

- **Rights.** The user records a rights decision that covers the footage and the
  people visible in it, with its scope (for example, private test or client
  delivery). Unknown rights stop the work. Creative approval mode never
  supplies this decision.
- **Inspection.** Record duration, frame rate, aspect ratio, resolution, audio
  streams, cut times and SHA-256 before writing a prompt.
- **Length.** Check the selected model and route's current documented input
  limits. Preserve the source timeline; propose splitting only when current
  limits or inspected content warrant it, with user approval of the spans.
- **Trim by route.** Keep the original unchanged. Verify current duration
  increments and frame-count constraints before preprocessing either route.
  Never impose an empirical 8n+1 pattern, whole-second rounding or a prior
  run's duration tolerance. If a verified requirement needs trimming, padding
  or retiming, explain alternatives and timing/audio consequences, then obtain
  user approval for that specific adaptation before proceeding.
  - *Reference routes* use currently supported duration settings without
    silently rounding the source.
  - *Edit routes* preserve the selected source timeline; frame-count patterns
    do not guarantee exact output timing.
  - An approved trim is a separate, frame-exact derivative. Record its source
    span, command and hashes; keep picture and sound tied to their approved
    spans. With no approved trim, use the full source.

  Example only for an approved trim:
  ```bash
  ffmpeg -ss <approved-start> -i <source>.mp4 -t <approved-duration> -map 0:v:0 -map 0:a:0? \
    -c:v libx264 -crf 16 -preset slow -c:a pcm_s24le source/<stem>_trim.mov
  ```

- **Source videos that show a person are asset:// videos.** The provider
  rejects any realistic person in a video input, including an invented person in
  a text-generated clip, with `InputVideoSensitiveContentDetected.PrivacyInformation`
  (HTTP 400, before a task is created). Registering image assets of that person
  does not clear it. Register the selected source as a video asset in the private
  asset library (Advanced Creation Rights) and bind `@Video 1` as its
  `asset://` URI. When no `ark_asset_*` tool is available, the user registers
  the clip in the console and supplies the asset ID. Record the asset ID beside
  the selected source and its hash. A source with no people can still be uploaded
  and bound by presigned URL.
- **Derivatives.** The original source hash stays the identity of the take: a
  subject map and the rights decision bind to it. Any approved picture or audio
  derivatives are recorded against that hash, with
  their own SHA-256 and the command that produced them.

## Audio preservation

Preserve the source with its audio; no muted-input, extraction or mux step is
required. Native generated audio is sufficient unchanged when it meets the
brief. Use current capability evidence for the exact model, operation and
transport to select supported source-audio handling and `generate_audio`;
an output-audio flag does not establish source-input requirements or guarantee
sample-exact preservation.

Do not assume native support when it is unknown. An unsupported source or
requested sound route stays unresolved; explain alternatives and obtain
explicit approval before preparing an adaptation. Do not silently mute the
source, disable native sound or create a post bed.

An exact supplied master or explicitly preserved source soundtrack stays
unchanged. Verify actual output against that requirement. If transport muxing
is needed, prefer compatible stream-copy and preserve independent tails and
offsets. A codec mismatch needs a disclosed, approved transcode, not automatic
normalization, padding or truncation.

## Requested audio changes

Use these routes only when the user requests or approves the sound change.
Finalization and a visual edit alone do not select them.

| Route | Use when | Method |
| --- | --- | --- |
| **Original** | Exact source sound is explicitly required | Preserve it directly where supported; use compatible stream-copy muxing only if needed |
| **New** | The brief asks for new music, SFX, ambience or voice | Generate with Seed Audio or use an approved library track within the selected scope |
| **Mixed** | Keep one layer (usually dialogue) and replace the rest | Separate the saved audio with the VOD voice/background tool, mix the kept stem with the new stem |
| **Re-voiced** | New words or a new voice over the same picture | Post voice overlay through `audio-dubbing`; lip-sync work follows the [audio-video alignment contract](audio-video-alignment.md) and is opt-in |

Measure picture and audio timing before an authorized mux. Do not use padding
or `-shortest` to hide a mismatch. For compatible streams, this optional
transport recipe copies both streams without an audio filter:

```bash
ffmpeg -i <generated>.mp4 -i <audio>.m4a -map 0:v:0 -map 1:a:0 \
  -c copy <derivative>.mp4
```

- Keep the generated master. Any muxed file is a derivative with its own
  SHA-256 and a recorded recipe.
- Measure decoded frame timestamps, duration, playback speed and cut boundaries
  against the approved source span for both routes. Report mismatches; no
  frame-count recipe or blanket tolerance establishes a pass. Obtain user
  approval before any corrective trim, padding or retiming, and record the
  derivative and its audio consequences.
- Output frame rate may differ from the source. Audio aligns by time; check two
  or three sync points (hits, claps, plosives) by playback.
- When a person speaks on screen, the mouth follows the source mouth motion.
  Check plosives and open vowels. Report visible drift and obtain a scoped
  repair or retake decision; it is never accepted or repaired silently.
- Voice reuse or timbre cloning of a real person needs that person's recorded
  voice consent, separate from footage rights.

## Provider rejections

A `PrivacyInformation` or other sensitive-content rejection is evidence to
diagnose. Report the request ID and the flagged input, and follow the
moderation rule in the [production policy](production-policy.md).

- When the flagged input is an invented character bound as a raw image,
  registering that character as a Virtual Portrait is the provider's authorized
  route; resubmit as a new reviewed request.
- When the flagged input is source footage or shows a real person, stop. Never
  blur, crop, stylize, re-encode or swap inputs to pass the check. Offer
  owned or generated source footage, or a Virtual Portrait cast, and resubmit
  only on the user's explicit decision. A real person who has consented can be
  routed through an authorized real-person asset; see
  `seedance-virtual-portrait` for the route, consent record and ledger.
