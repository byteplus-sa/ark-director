# Seedance video creation

Load this when you build a Seedance 2.0, 2.5, or 2.5 Premium create request:
choosing the model and tool, setting parameters, using Draft mode, picking an
`omni_reference_task_type`, or diagnosing an input rejection. Polling,
persistence, and QA after submission live in
[Seedance tasks](seedance-tasks.md).

Requires `BYTEPLUS_MODELARK_API_KEY`. Auth scopes: `seedance:create`,
`seedance:read`, `seedance:delete`. Every create tool requires background
execution; submit it through `ark_job_submit` as described in `SKILL.md`.

## Choose the model and tool

| Capability | Seedance 2.0 (`seedance_create_task`) | Seedance 2.5 (`seedance_2_5_create_task`) | 2.5 Premium (`seedance_2_5_premium_create_task`) |
|---|---|---|---|
| Default model | `dreamina-seedance-2-0-260128` | `dreamina-seedance-2-5-260628` | `dreamina-seedance-2-5-premium-260915` |
| Max duration | 15 s | 30 s | 30 s |
| Images / videos / audios | 9 / 3 / 3 | 30 / 10 / 10 | 30 / 10 / 10 |
| Resolution | 480p, 720p, 1080p, 4k | 480p, 720p, 1080p | 480p, 720p, 1080p, 4k |
| Fast / Mini variants | Yes (bind via `SEEDANCE_MODEL_BINDINGS`; 480p/720p only) | No | No |
| Structured editing, native extension, keyframe sequences | Limited: `edit_video` (output caps near 5 s) and `extend_video`; otherwise chain with `return_last_frame` | Yes | Yes |
| Audio as the only media input | No (needs an image or video) | Yes | Yes |
| Draft mode (`draft`, `draft_task_id`) | Not in the tool schema | Yes (final 1080p) | Yes (final 4k) |
| Availability | ModelArk key | ModelArk key | Whitelist-only; needs `BYTEPLUS_MODELARK_SEEDANCE_2_5_PREMIUM_ENABLED=true` |

- **Seedance 2.5 is the default.** Choose it for 30 s single passes, rich
  multimodal references, structured editing, native extension, and Draft mode.
- **Choose 2.0** only for 4k without Premium access, Fast/Mini speed variants,
  or lower cost per task.
- **Choose Premium** when 4k is required together with 2.5 capabilities and the
  account is whitelisted. Premium model IDs are rejected by the 2.0 and 2.5
  tools; inputs are otherwise identical to 2.5.
- `*_variations` tools take the same inputs plus `variations` (1–5) and optional
  `variation_prompts`; each variation is a separate provider task.

## Create parameters (Seedance 2.5)

| Parameter | Type | Notes |
|---|---|---|
| `prompt` | `str` | 1–32,000 characters; optional when media inputs are present. BytePlus recommends under ~1,000 words for focus. |
| `images` | list | Up to 30; `role` is `first_frame`, `last_frame`, or `reference_image`. A plain URL string or `{"url": ...}` is coerced to `reference_image`. |
| `videos` | list | Up to 10; role `reference_video`; URL only (HTTPS or `asset://`). |
| `audios` | list | Up to 10; role `reference_audio`. |
| `model` | `str` | Omit to use the default binding. |
| `resolution` | `480p` \| `720p` \| `1080p` | Premium also accepts `4k`. See Draft mode constraints below. |
| `ratio` | `str` | e.g. `16:9`, `9:16`, `21:9`. Set the ratio here, never as a sentence in the prompt. Omit for edit/extend and first/last-frame tasks (see below). |
| `duration` | `int` | -1 (auto) to 30. Ignored for edits (derived from the input video within ~0.3 s). |
| `omni_reference_task_type` | `str` | Free-form pass-through; see Task types. |
| `generate_audio` | `bool` | Native audio track. |
| `watermark` | `bool` | Defaults to `false` in the tool; pass `false` explicitly in records. |
| `return_last_frame` | `bool` | Last frame as a separate image output, for chaining. |
| `draft` / `draft_task_id` | `bool` / `str` | Draft mode; mutually exclusive. |
| `execution_expires_after` | `int` | 3600–259200 s. |
| `priority` | `int` | 0–9; higher may cost more. |
| `safety_identifier` | `str` | Max 64 characters. |

The 2.0 tool has the same fields except Draft mode, with 2.0 limits (9/3/3
references, 15 s, `4k` allowed) and audio that cannot be the sole media input.

The 2.5 and 2.0 create tools may not expose `camera_fixed` or `seed`. State a
locked camera in the prompt and record the reason; do not send those fields,
and do not expect seed-identical Seedance retakes. Re-check the live schema
(`ark_job_capabilities`) before relying on this.

Returns `task_id`, `status="queued"`, and `recommended_poll_after_ms` inside the
background result. Record the provider `task_id` immediately.

## Draft mode (2.5 and Premium)

Draft mode is a provider-native two-step flow. Verify the fields in the live
schema before use; the tool descriptions list them.

1. **Draft:** submit the full request with `draft: true` and an explicit
   `resolution: "480p"` (the provider also accepts it omitted; record it
   explicitly). It is billed as a normal 480p video.
2. **Review** the draft (playback, motion, continuity, audio) and record a
   selection before promoting.
3. **Promote:** submit a new request with `draft_task_id` set to the succeeded
   Draft task (created by the same tool, at most 7 days old). Send only
   `draft_task_id`, `resolution` (omit, or the family's final resolution:
   `1080p` for 2.5, `4k` for Premium), and `watermark`. Optional:
   `return_last_frame`, `execution_expires_after`, `priority`,
   `safety_identifier`.

Rules for the promotion call:

- The provider reuses the Draft's model, prompt, media, duration, ratio, seed,
  `generate_audio`, and `omni_reference_task_type`. Sending any of `prompt`,
  `images`, `videos`, `audios`, `duration`, `ratio`, `generate_audio`, or
  `omni_reference_task_type` is invalid. **Edit inputs only before the draft.**
- Omitted output settings use model defaults, not the Draft's values, so
  re-send `watermark: false` and `return_last_frame` if you need them.
- The final is billed independently at the final resolution, which costs
  substantially more than the draft; estimate it from the pricing page.
- **Re-check audio on the final render.** The final soundtrack is not
  byte-identical to the draft's; speech timing and words can differ.
- A plain `resolution: "480p"` request without `draft: true` is not a Draft
  task and cannot be promoted; the final is then a new paid request that can
  change picture, timing, or audio.

```json
{"tool_name": "seedance_2_5_create_task",
 "arguments": {"input": {"draft_task_id": "<succeeded-draft-task-id>",
                         "resolution": "1080p", "watermark": false}}}
```

## Task types (`omni_reference_task_type`)

The server passes the value through unvalidated. Values accepted by Seedance 2.5:
`auto`, `reference`, `edit`, `extend`.

| Value | Use | Locks |
|---|---|---|
| omitted / `auto` | Default. Provider infers the task from prompt and media. Use for text-to-video and reference-to-video. | Ratio and duration free (`-1` = auto). |
| `reference` | Forces reference-to-video. Behaviour beyond auto-detection is undocumented; prefer omitting it. | Free. |
| `edit` | Structured edits of a source video (subject, outfit, background, audio replacement). | Ratio and duration derived from the input video. |
| `extend` | Forward/backward continuation of a source video (beta). | Ratio locked to the source; omit `ratio`. Duration free. |

- `edit_video` and `extend_video` are Seedance 2.0 values. A 2.5 request with
  `edit_video` is rejected with `InvalidParameter.TaskTypeConstraint`. 2.0
  `edit_video` output caps at about 5 s in practice.
- The server strips an explicit `ratio` for `extend_video` (logged as
  `seedance_ratio_stripped_for_extension`). Do not rely on stripping for
  `extend`; omit `ratio` yourself.
- First/last-frame generation locks ratio to the first image.

## Input rejections

These are provider input checks, distinct from output moderation (an accepted
task whose clip is blocked). Diagnose before resubmitting; never blur, crop,
re-encode, or restyle an input to slip past a check.

- **Video inputs that contain people** (extension and video-to-video of clips
  with generated or real people) are rejected with
  `InputVideoSensitiveContentDetected.PrivacyInformation` unless the people
  are bound as `asset://` Virtual Portrait or authorized assets. For swap,
  restyle, or recast, bind identities as assets and submit a muted source
  (`generate_audio: false`); add original or new audio in post. See
  [Assets and rights](assets-and-rights.md).
- **Real-person reference photos** are rejected as raw image inputs; use the
  person's authorized `asset://` reference or an invented Virtual Portrait.
- **`reference_image` crops** of a face or body can be rejected.
- **A `last_frame` without a `first_frame`** is rejected. Supply both, or use
  `reference_image`.
- Output audits (`decision_in_reject_list`, code `55001310`) are terminal
  content rejections; see [Background-job output](background-job-output.md).

## Examples

Draft-first 2.5 text-to-video (`arguments.input`):

```json
{
  "prompt": "A cinematic 30-second scene...",
  "draft": true,
  "resolution": "480p",
  "ratio": "16:9",
  "duration": 30,
  "generate_audio": true,
  "watermark": false
}
```

First and last frame, as a promotable Draft:

```json
{
  "prompt": "The camera dollies forward as the door swings open",
  "images": [
    {"role": "first_frame", "kind": "url", "url": "https://cdn.example.com/start.png"},
    {"role": "last_frame", "kind": "url", "url": "https://cdn.example.com/end.png"}
  ],
  "draft": true,
  "resolution": "480p",
  "duration": 5
}
```

Premium 4k (whitelisted accounts only): draft first, then promote to 4k.

```json
{"prompt": "A 4K aerial shot over a coastline at golden hour",
 "draft": true, "resolution": "480p", "ratio": "16:9", "duration": 15}
```

```json
{"draft_task_id": "<succeeded-draft-task-id>", "resolution": "4k",
 "watermark": false}
```

Video references are URL-only. Upload a local or Base64 video with
`media_upload` first and pass the presigned URL; see
[Object storage](object-storage.md).
