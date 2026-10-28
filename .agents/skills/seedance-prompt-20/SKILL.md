---
name: seedance-prompt-20
description: >-
  Write and revise Seedance 2.0 video prompts, the legacy model used for 4K
  output and the Fast/Mini speed variants: asset preparation within the 2.0
  reference limits, Define subject definitions, task-type declaration,
  shot-by-shot sequencing with inline reference binding, spatial continuity for
  chase or action blocking, native audio, and inline constraints. Use for
  Seedance 2.0 prompts, shot lists, 4K or Fast/Mini requests, and corrections
  to 2.0 generations. For Seedance 2.5 prompts, use seedance-prompt-25 instead.
---

# Seedance 2.0 Prompt

This skill covers only what differs on the legacy Seedance 2.0 series. New
work defaults to Seedance 2.5 (`seedance-prompt-25`); use 2.0 when the request
needs 4K output through 2.0, the Fast or Mini variants, or a revision of an
existing 2.0 take. The 2.0 action, emotion and revision rules are below; broader
directing craft (shot plans, counts, frame-side hands, text-free frames, the
speech budget) matches `seedance-prompt-25`, which can be composed for depth.

## Source authority

The prompt structure and rules here follow the official BytePlus Seedance 2.0
prompt guide:
- [Seedance 2.0 Prompt Guide](https://docs.byteplus.com/en/docs/ModelArk/2222480)
- [Seedance 2.0 Series Tutorial](https://docs.byteplus.com/en/docs/ModelArk/2291680)
- [Lens Language Reference](https://docs.byteplus.com/en/docs/ModelArk/1631633#a395fd3b)

When the official guide is updated, prefer the live page where they conflict.

## What differs from 2.5

| Topic | Seedance 2.0 | Seedance 2.5 |
|---|---|---|
| Duration | 4-15 s | 4-30 s |
| References | 9 images, 3 videos, 3 audio; audio never alone; combined video ≤ 15 s, combined audio ≤ 15 s | 30 images, 10 videos, 10 audio (50 total) |
| Resolution | Standard 480p-4K; Fast and Mini 480p/720p | 480p-1080p (4K only on whitelisted 2.5 Premium) |
| Draft mode | None in the MCP tool: a 480p request is an ordinary paid run | `draft: true`, then promote by `draft_task_id` |
| Prompt anatomy | Fixed section order with `Define` labels and a task-type line | Flexible six-part formula |
| MCP tool | `seedance_create_task` | `seedance_2_5_create_task` |

## Recommended prompt structure

Assemble a Seedance 2.0 prompt in this order. Use short natural-language
headings; omit a section only when it does not apply.

```text
Asset preparation:
Subject definitions:
Prompt:
Shot 1:
Shot 2:
Quality and constraints:
```

### 1. Asset preparation (always first)

Label every reference `@Image 1`, `@Video 1`, `@Audio 1`, numbered from 1 per
type with a space separator, and give each a short role.

```text
Asset preparation:
@Image 1: female lead character sheet
@Image 2: dormitory room location sheet
@Video 1: medium-shot dolly camera movement reference
@Audio 1: indoor ambience
```

Input limits for 2.0:

- Images: .jpeg/.png/.webp/.bmp/.tiff/.gif (+ .heic/.heif), aspect ratio
  0.4-2.5, 300-6000 px, ≤ 30 MB each, ≤ 64 MB request body.
- Videos: 2-15 s each, MP4/MOV (H.264/H.265; AAC/MP3 audio), 24-60 fps,
  ≤ 200 MB; combined ≤ 15 s.
- Audio: 2-15 s each, WAV/MP3, ≤ 15 MB; combined ≤ 15 s.

Classify each reference as visible identity, visible environment, motion or
camera reference, or control-only. Translate a control-only image (route map,
blocking diagram) into text and omit it. If the user insists the image stays in
the bundle, label it control-only, state exactly what to extract, forbid visual
reproduction, and say leakage is still possible. Storyboard boards and panels are never
bound: their numbers and sketch medium leak into the video. If a reference
shows something that must not appear (an aura, a logo, an extra face), clean or
replace the reference rather than relying on "no aura".

**People.** Seedance 2.0 rejects direct uploads of real human faces. Use recent
Seedance/Seedream outputs, preset digital characters, or authorized `asset://`
portrait assets; compose with `seedance-virtual-portrait` for that route.

### 2. Subject definitions

Define every distinct subject with the `Define` keyword and 2-3 stable static
features (clothing, hairstyle, build, category). Labels are unique and reused in
every shot.

```text
Subject definitions:
Define the young woman with long dark hair and a white blouse in @Image 1 as Girl
Define the [features] in @Image 1 and [features] in @Image 2 as [Label]
Define the [features of A] in @Video 1 as [Label_A], and the [features of B] in @Video 1 as [Label_B]
```

- Static features only; no expression or pose.
- For simple scenes, bind inline instead: `Girl @Image 1`.
- Never use Asset IDs; the model cannot associate them with reference content.

### 3. Prompt and task type

Declare one primary task type (or a genuine combination):

```text
Prompt:
Task type: Multimodal Reference | Video Editing | Video Extension | Combined Tasks
```

- **Multimodal Reference:** `Reference <Subject> in @Image 1 to generate...`,
  `Reference the camera movement in @Video 1...`, `Reference the timbre in @Audio 1...`.
- **Video Editing:** unmentioned parts stay unchanged. Add: `<Element_Features>
  + <Timing> + <Location>`; modify: `Strictly edit @Video 1, and modify
  <Original> in it to <New>`; for a removal, say what stays.
- **Video Extension:** `Extend @Video 1 forward/backward to generate...`, or
  `@Video 1 + <transition> + followed by @Video 2`.
- **Combined Tasks:** `Reference [dimension] of @Image 1, strictly edit @Video 1, [edits]`.

For edit and extend tasks write `@Video 1` directly. "Reference @Video 1"
switches the model to multimodal reference mode.

### 4. Shots

Write `Shot 1 / Shot 2 / Shot 3` in event order, one coherent unit of action
per shot. For narrative, ad, micro-drama, music-video and showcase shots, carry
each shot's size, angle, move and light source from the scene's shot plan
(`seedance-shot-design`). For movement-heavy scenes, state start positions,
travel axis, subject order, boundary behavior, end state and forbidden
transitions first, using physical locations ("forest interior → inland tree
line → white sand"), and repeat the invariants that matter in every shot.

Per shot, in this order:

1. Camera movement or transition (one primary move), with any `@Video N`.
2. Subject action at body-part level, with the subject's `@Image N`.
3. Position or spatial change, with the environment's `@Image N`.
4. Light: the plan's source and key side ("warm dusk window light from
   frame-left").
5. Audio, with any `@Audio N`.

Repeat every applicable `@Image N`, `@Video N` and `@Audio N` inline in each
shot; the asset list does not replace shot-level binding. Never leave a bare
`@<Asset>` placeholder.

**Timing.** Set length with the API `duration` (the REST API also documents
`frames`; the MCP tool exposes only `duration`). Let the model pace ordinary
multi-shot clips; add second-level ranges such as `Shot 1 (0-4s):` only when
requested, contiguous and consistent with the duration.

**Complexity budget.** A 15 s generation holds at most about 3 major action
beats or 4 tightly related shots when continuity must be exact. A scene with
several cuts, close encounters, a location change and a precise end pose is
split into generated shots chained from an approved last frame. Camera variety
never reverses the travel direction.

**Dialogue.** Put spoken lines in `{curly braces}` (or quotes) when
`generate_audio` is true, with speaker labels for several speakers:
`{Speaker A, urgent}: Did you hear that? {Speaker B, calm}: Stay behind me.`

**Action.** Describe actions at body-part level (hands, legs, head, shoulders)
with range, speed and force, and link them ("using the turn's momentum, she
raises a hand"). Speed, amplitude, interruptions and recovery follow approved
intent and physically plausible action. There is no slow-body default or
universal burst cap. Slow motion or one burst with holds is an optional
selected pattern or a remedy for a demonstrated failure, not a quality gate.
Preserve locked actions and timing; return conflicts rather than softening
them. Actor energy, camera energy and edit rhythm are separate choices.
Speech permits kinetic coverage when required delivery and performance remain
readable at the planned framing and speed.

**Emotion.** Externalize feelings as visible physical detail, never "very sad":

| Emotion | Externalize as |
|---|---|
| Sadness | head lowering, shoulders trembling slightly, eyes reddening, fingers clutching clothing |
| Joy | mouth corners rising, brows relaxing, light quick steps |
| Nervousness | checking a watch, fingers tapping the table, eyes darting |
| Anger | fists clenched, jaw tight, chest heaving, words squeezed through teeth |
| Relief | a long exhale, shoulders dropping, a faint smile, gaze lifting |

**Revisions.** Before rewriting a take, record `Locked decisions`, `Requested
delta` (the one behavior that changes), `Acceptance criteria` and `Known
rejections`; carry the locks into the new prompt and change only one of prompt
wording, reference bundle or motion design per retry when practical.
Budget speech from measured delivery or a native-language-informed read with
pauses, onset and tail. About 2.2 words/s is an English planning estimate;
0.5-1.5 s onset and about 0.4 s tail are provisional margins, not minimums.
Verify actual delivery; preserve requested language and locked words, proposing
retiming or splitting before an authorized wording revision.

### 5. Quality and constraints

Close with a short quality, style and constraint paragraph. Seedance 2.0 has no
separate negative-prompt field, so constraints go inline. Describe the wanted
result positively and keep only the few exclusions that prevent expensive
failures.

```text
Quality and constraints:
Quality: sharp detail, natural skin texture, soft window light, natural colour.
Style: <one concrete look, e.g. cool blue-purple night tones>.
Constraints: clean frames edge to edge with no subtitles, logos, watermark or
on-screen text; stable faces and clothing.
```

Captions, titles and end cards are added in post. A contradiction between the
brief, references, shots and constraints does more damage than a missing
adjective.

## Preflight review

1. Prompt and request agree on resolution, duration, ratio, model variant and
   audio; Fast and Mini stay at 480p/720p.
2. Every reference is indexed, classified, within the 2.0 limits and bound only
   where intended; no storyboard is bound.
3. Start, travel axis, subject order, boundary behavior and end state are
   explicit for movement-heavy scenes.
4. Each shot carries its planned camera and light facts, or a recorded static
   reason.
5. No contradictions ("single continuous shot" plus cuts; "no powers" plus an
   aura in a reference).
6. The beats and dialogue fit the duration, or the scene is split.

## Full example

```text
Asset preparation:
@Image 1: female lead character sheet
@Image 2: dormitory room location sheet
@Video 1: indoor medium-shot dolly camera movement reference
@Audio 1: indoor ambience

Subject definitions:
Define the young woman with long dark hair and a white blouse in @Image 1 as Girl

Prompt:
Task type: Multimodal Reference
Use Girl @Image 1 as the main character, the dormitory in @Image 2 as the scene,
and @Video 1 as the indoor camera-language reference.

Shot 1: Match the steady medium-shot follow movement from @Video 1. Girl @Image 1
walks toward the dormitory entrance from @Image 2, pauses at the doorway, takes
one deep breath, and her right hand, frame-left, tightens on her bag strap.
Light: warm dusk sun through the hallway window from frame-left. Blend the
indoor ambience from @Audio 1 beneath her footsteps.

Shot 2: Use the restrained medium-shot dolly movement from @Video 1. Girl
@Image 1 pushes the door open and enters the dormitory from @Image 2. Two
roommates look up from the books on the desk, and one asks:
{How did the exam go?} Light: warm desk lamp at frame-right, dusk window
behind. Keep the ambience from @Audio 1 under the line.

Shot 3: Begin on a close-up, then one slow pull-back modeled on @Video 1. Girl
@Image 1 lowers her head; after one beat she looks up, the corners of her mouth
lift, and she says: {I passed.} Both roommates laugh as the frame widens to the
whole dormitory from @Image 2. Light: desk lamp at frame-right as the key.
Blend their laughter with the ambience from @Audio 1.

Quality and constraints:
Quality: natural skin texture, warm dusk tones, soft practical light.
Constraints: clean frames with no subtitles, logos, watermark or on-screen text;
stable faces and clothing.
```

## Quick reference card

### Image modes (mutually exclusive)

- **First frame (I2V):** one clean keyframe as `first_frame`.
- **First + last frame (FLF2V):** two clean keyframes that share a ratio.
- **Reference-to-video (R2V):** 0-9 images + 0-3 videos + 0-3 audio as references.

Do not combine frame roles with an R2V bundle unless the live tool confirms it.
Record the mode, ordered roles, paths, hashes, selected variants and approval
states in the shot manifest.

### Model IDs

| Variant | Model ID |
|---|---|
| Seedance 2.0 Standard | `dreamina-seedance-2-0-260128` |
| Seedance 2.0 Fast | `dreamina-seedance-2-0-fast-260128` |
| Seedance 2.0 Mini | `dreamina-seedance-2-0-mini-260615` |

IDs are version-dated; copy the live ID from the
[Model list](https://docs.byteplus.com/en/docs/ModelArk/1330310) before calling.
In the MCP tool, Standard is the default and the Fast/Mini IDs depend on the
server's model bindings.

### Tool parameters

- `seed`: documented for the REST API; the MCP tool has no seed field, so reuse
  the approved prompt and references.
- `camera_fixed`: REST-only; the MCP tool has no such field (checked
  2026-10-06), so state a locked camera in the prompt with its reason.
- `return_last_frame: true` chains multi-shot continuity.
- `watermark: false` unless the user asks for the AIGC watermark.

### Prompt limits and languages

- BytePlus recommends under 1,000 words for focus; the MCP tool accepts up to
  32,000 characters.
- Languages: English, Chinese, Japanese, Indonesian, Spanish, Portuguese.

### Cost ladder

Prototype on Mini 480p, confirm on Fast 720p, finalize on Standard at the
target resolution. Billing is per successful task; confirm on the
[Pricing page](https://docs.byteplus.com/en/docs/ModelArk/1544106).
