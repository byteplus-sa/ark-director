# Video-to-Video Inputs

This contract covers identity references, source footage, muted submission and
post audio for Seedance video-to-video work: Motion Transfer
(`seedance-motion-recast`), Object Swap (`seedance-object-swap`), Restyle
(`seedance-restyle`) and the shot runner (`seedance-vfx-pipeline`).

- [Identity references: Virtual Portrait assets](#identity-references-virtual-portrait-assets)
- [Source footage](#source-footage)
- [Muted source master](#muted-source-master)
- [Post audio](#post-audio)
- [Provider rejections](#provider-rejections)

## Identity references: Virtual Portrait assets

Every person or character identity bound into a video-to-video request is a
Seedance Virtual Portrait asset: an Advanced Creation Rights AIGC asset,
referenced as `asset://<asset_id>`. This is the BytePlus-recommended path, and
these workflows do not use the liveness-verification flow.

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
  (`@Image 1`), never by asset ID or subject name.

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
- **Length.** Sources run 4–30 s. Edit routes (Object Swap, Restyle) are most
  stable under 20 s; split longer takes into shots.
- **Whole seconds for reference routes.** A route that sets `duration` takes
  whole seconds. Trim the source to a whole-second span first, so the saved
  audio and the output share one timeline.

## Muted source master

Submit only a muted master; never the source with its audio. Keep the audio as
a separate file for post.

```bash
ffmpeg -i <source>.mp4 -map 0:a:0 -vn -c:a pcm_s24le source/<stem>_audio.wav
ffmpeg -i <source>.mp4 -map 0:v:0 -an -c:v copy source/<stem>_muted.mp4
```

1. Skip the first command when the source has no audio stream, and record that.
2. Confirm with `ffprobe` that the muted master has no audio stream and the same
   frame count and duration as the source.
3. Record the source, muted master and audio file with SHA-256 in the shot
   manifest. Upload and bind only the muted master as `@Video 1`.
4. Submit with `generate_audio: false` and no `@Audio` bindings. The prompt's
   audio line states that the output is silent and sound is added in post.

Native audio generation is not part of these workflows. Use it only when the
user explicitly asks for it on a named take, and record that exception.

## Post audio

Pick one route per shot from the requirement and record it in the shot
manifest.

| Route | Use when | Method |
| --- | --- | --- |
| **Original** | Timing is preserved and the source sound stays | Mux the saved source audio |
| **New** | The brief asks for new music, SFX, ambience or voice | Generate with Seed Audio or use an approved library track, then mux |
| **Mixed** | Keep one layer (usually dialogue) and replace the rest | Separate the saved audio with the VOD voice/background tool, mix the kept stem with the new stem |
| **Re-voiced** | New words or a new voice over the same picture | Post voice overlay through `audio-dubbing`; lip-sync work follows the [audio-video alignment contract](audio-video-alignment.md) and is opt-in |

Mux to the picture length:

```bash
ffmpeg -i <generated>.mp4 -i <audio>.wav -map 0:v:0 -map 1:a:0 \
  -c:v copy -af apad -c:a aac -b:a 192k -shortest <final>.mp4
```

- Keep the silent generated master. The muxed file is a derivative with its own
  SHA-256 and a recorded recipe.
- Edit outputs land within about 0.3 s of the source length; reference-route
  outputs match the requested whole-second duration. Record the measured
  output duration and any padding or trim.
- Output frame rate may differ from the source. Audio aligns by time; check two
  or three sync points (hits, claps, plosives) by playback.
- When a person speaks on screen, the mouth follows the source mouth motion.
  Check plosives and open vowels. A visible drift routes to Re-voiced or to a
  new take; it is never accepted silently.
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
  only on the user's explicit decision.
