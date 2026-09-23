---
name: source-subject-map
description: >-
  Analyze an existing source clip into an auditable subject map before
  recasting, swapping, or VFX-editing footage with several subjects or objects.
  Records source hash and probe data, cuts, subjects with observable
  descriptors (screen position, clothing, action), swappable objects with
  per-cut counts, occlusions, hand/object contact windows, speakers with speech
  windows, on-screen text and logos, and open ambiguities, confirmed by a
  per-cut keyframe spot-check. Observable descriptors only; never identifies
  real people. Open ambiguities block downstream prompt writing. Analysis only;
  excludes media generation and prompt writing.
---

# Source Subject Map

Turns one source clip into `subject_map.json` plus a human-readable
`subject_map.md`. The map gives every cut, subject and swappable object a
stable ID and an observable descriptor, so a later prompt can say exactly which
person or object changes and which stays. Prompt writers for motion recast,
object swap, or VFX edits can consume the map; this skill never writes those
prompts or generates media.

## Hard rules

1. **Observable descriptors only.** A descriptor is screen position + clothing
   or visible appearance + action, for example `left, red jacket, jumps the
   rail`. Never name, identify, or guess the identity, age, ethnicity, or
   other sensitive attributes of a real person, even when asked or when a name
   is visible on screen. Visible on-screen text is recorded verbatim under
   `text_logos`, not attached to a subject as an identity.
2. **Ambiguity blocks.** If two subjects or two objects in the same cut share
   one descriptor, a count is uncertain, or a timestamp cannot be confirmed,
   record it in `ambiguities`. While any ambiguity lacks a `resolution`, the
   map status is `blocked` and downstream prompt writing must not start.
3. **Look at the frames.** The agent extracts one keyframe per cut and views
   each one before the map leaves `draft`. Model output alone never confirms a
   descriptor.
4. **Analysis only.** No Seedance, Seedream, or audio generation. The only
   provider calls are `media_upload` (when needed) and `seed_understand`.
5. **Hash-bound.** The map records the source SHA-256. A changed source file
   invalidates the map; rebuild it rather than editing IDs by hand.

## Input and output contract

Input: one source clip (local file or public HTTPS video URL) inside a project
or scratch folder, plus optional user notes on which elements may change.

Output, written beside the source clip (typically the shot folder
`projects/<project>/scenes/scene-NN/sNN_shNNN/`):

| File | Contents |
| --- | --- |
| `subject_map.json` | Machine-readable map; see [manifest format](references/manifest-format.md) |
| `subject_map.md` | Tables of cuts, subjects, objects, text/logos and ambiguities |
| `subject_map_frames/cut-NN.png` | One spot-check keyframe per cut |
| `subject_map_understand.md` | Exact `seed_understand` prompt sent and the raw answer |

Status values: `draft` (model answer parsed, frames not yet checked),
`blocked` (spot-check done, unresolved ambiguities), `ready` (spot-check done,
every ambiguity resolved or none found).

## Procedure and reference loading

Load [understand prompts](references/understand-prompts.md) for step 2 and
[manifest format](references/manifest-format.md) for steps 3–4.

### 1. Source intake and probe

Probe the local file before any provider call:

```bash
shasum -a 256 <source>
ffprobe -v error -show_entries format=duration:stream=codec_type,width,height,r_frame_rate \
  -of json <source>
```

Record `sha256`, `duration_s`, `fps` (evaluate `r_frame_rate`), `width`,
`height`, and `audio` (true when any stream has `codec_type` `audio`).

For the `seed_understand` input, prefer a public HTTPS URL the provider can
fetch as video. Otherwise call `media_upload` with `media_type: "video"`, the
file's `mime_type` (for example `video/mp4`), and an absolute `file_path`;
reuse an existing `ref_cache.json` entry for the same hash and storage scope.
If only a URL was supplied, download it locally first so it can be hashed and
probed. Page or platform links are not video inputs.

### 2. Understanding pass

Submit `seed_understand` through `ark_job_submit` (it requires background
execution) with the fixed question set as `prompt`, the clip in `videos` as
`{"kind": "url", "url": ...}`, `thinking: true`, `reasoning_effort: "high"`,
and a low `temperature`. Poll `ark_job_get` no faster than `poll_after_ms`.
Save the exact prompt and raw answer to `subject_map_understand.md`. Long
clips and uncertain timestamps follow the reference.

### 3. Assign IDs

Parse the answer into cuts `cut-01..`, subjects `subj-01..`, and objects
`obj-01..`, numbered in order of first appearance (left to right on ties). A
subject who reappears in a later cut keeps one ID only when clothing and
context make the match unambiguous; otherwise record an ambiguity.

### 4. Confirm cuts

Model timestamps are approximate. Confirm cut boundaries with ffmpeg scene
detection (see the reference) and use the ffmpeg times in the map. Record a
disagreement larger than one second, or a model cut that ffmpeg cannot find,
as an ambiguity.

### 5. Visual spot-check

Extract one keyframe from the middle of each cut:

```bash
ffmpeg -v error -ss <mid_s> -i <source> -frames:v 1 subject_map_frames/cut-01.png
```

Open and view every frame. Do not burn labels into frames: this workspace's
ffmpeg may lack the `drawtext` filter. Label in the `subject_map.md` table
instead, one row per subject per cut with its frame file. Confirm each
descriptor, object count, and visible text against the frame. Correct errors,
and add an ambiguity whenever two subjects or objects share a descriptor.

### 6. Write and hand off

Write `subject_map.json` and `subject_map.md`, set `status`, and report the
open ambiguities to the user as questions. Resolutions come from the user or
from further frame inspection, never from guessing; record each in its
`resolution` field and re-derive `status`.

## Submission boundary and failure behavior

- This skill submits only analysis calls. It never submits generation, and it
  does not decide what to change; consumers add dispositions later.
- If `seed_understand` fails or times out, reconcile the existing job with
  `ark_job_get` before resubmitting. Never retry with a shorter prompt to work
  around a client timeout.
- If the provider refuses the clip, record the refusal and stop. Do not crop,
  blur, or re-encode the source to get past a moderation decision.
- If `ffprobe` or `ffmpeg` is unavailable, the map stays `draft`; report the
  missing tool rather than marking the spot-check done.
- If the user asks who a person is, decline to identify them and continue with
  observable descriptors.
- Missing inputs stay unresolved. A parsed model answer is not approval.

## Checklist

- [ ] Source SHA-256, duration, fps, resolution and audio presence recorded
      from local `shasum` and `ffprobe`
- [ ] `seed_understand` run with the fixed question set; exact prompt and raw
      answer saved
- [ ] Cut boundaries confirmed with ffmpeg scene detection
- [ ] Every subject has an ID and an observable descriptor; no names or
      inferred identity
- [ ] Every swappable object has an ID and a per-cut count
- [ ] Occlusions, contact windows and speech windows recorded where present
- [ ] On-screen text and logos recorded verbatim with cut and position
- [ ] One keyframe per cut extracted and viewed by the agent
- [ ] Shared descriptors, uncertain counts and unconfirmed times recorded as
      ambiguities
- [ ] `status` is `blocked` while any ambiguity lacks a resolution
- [ ] `subject_map.json` and `subject_map.md` agree
