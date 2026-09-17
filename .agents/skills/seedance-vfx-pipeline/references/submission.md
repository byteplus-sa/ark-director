# Submission

Focused reference for `seedance-vfx-pipeline`. Read [the entrypoint](../SKILL.md) for
mode selection and caller responsibilities.

- [Step 3 — Submit via MCP](#step-3--submit-via-mcp)
- [Step 4 — Poll for completion](#step-4--poll-for-completion)

## Step 3 — Submit via MCP

Persist the exact prompt snapshot and prepared operation in `task_ids.json`
before submission. Bind the completed review to its request hash, model, edit
mode, and change contract. Submit through the selected tool only after preflight.
The sample below is for the supported legacy `seedance_create_task` branch;
use the 2.5 branch parameters below for the default model.

**MCP request structure:**

```json
{
  "server_name": "ark-mcp",
  "tool_name": "seedance_create_task",
  "args": {
    "input": {
      "prompt": "<full VFX prompt text from Step 1>",
      "videos": [
        {
          "kind": "url",
          "url": "<presigned source video URL>",
          "role": "reference_video"
        }
      ],
      "images": [
        {
          "kind": "base64",
          "data": "<base64-encoded character/location sheet>",
          "mime_type": "image/png",
          "role": "reference_image"
        }
      ],
      "model": "dreamina-seedance-2-0-260128",
      "omni_reference_task_type": "edit_video",
      "resolution": "1080p",
      "ratio": "16:9",
      "duration": 5,
      "generate_audio": true,
      "watermark": false,
      "return_last_frame": true,
      "execution_expires_after": 3600,
      "priority": 0,
      "safety_identifier": "<project>-<scene>-<shot>"
    }
  }
}
```

Key parameters for VFX:

**Seedance 2.5 (default for full-duration edits):** use `seedance_2_5_create_task`
instead, with `"omni_reference_task_type": "edit"` (2.5 accepts
`auto|reference|edit|extend`; `edit_video` is 2.0-only and will be rejected).
Omit `ratio` and `duration` — they auto-lock to the source. 2.5 caps at 1080p.
2.0 (`edit_video`) caps output at ~5s, so use 2.5 for any edit longer than ~5s.
- **`videos[].role = "reference_video"`** — the source clip to edit. This is
  what makes it a video-to-video (VFX) task rather than text-to-video.
- **`images[].role = "reference_image"`** — element references (character
  sheets, location sheets, prop sheets) for identity consistency.
- **Resolution** — use a value supported by the selected model and operation.
  Evaluate face/detail fidelity in output QA; resolution is not a guarantee.
- **`generate_audio = true`** — Seedance 2.0 native audio. The prompt's
  `Audio:` section guides the audio generation.
- **`return_last_frame = true`** — returns the last frame image, enabling
  shot chaining for multi-shot VFX sequences.
- **`safety_identifier`** — set to `<project>-<scene>-<shot>` for
  traceability.

The tool returns a `task_id` and `polling_interval`. Immediately store the task,
shot, take, version, model, status, intended asset path, and submission time in
`projects/<project>/task_ids.json` before polling. A local timeout never
authorizes a duplicate submission; resume the recorded task until terminal.

## Step 4 — Poll for completion

Call `seedance_get_task` repeatedly, respecting the `polling_interval` from
creation:

```json
{
  "server_name": "ark-mcp",
  "tool_name": "seedance_get_task",
  "args": {
    "task_id": "<task_id from Step 3>",
    "persist_output": true
  }
}
```

Task states transition through: `queued` → `running` → `succeeded` / `failed`
/ `cancelled` / `expired`.

Poll until the status is terminal:
- **`succeeded`** — proceed to Step 5. The response includes `artifacts` (the
  generated video, and optionally the last frame image if
  `return_last_frame=true`), `usage` (token counts, cost), and `settings`.
- **`failed`** — check the `error` field. Common causes: content safety
  rejection, invalid reference format, prompt too long. Report the error and
  retry guidance to the user.
- **`cancelled`** — the task was cancelled (manually or by timeout). Report
  and ask the user whether to resubmit.
- **`expired`** — the provider confirms terminal expiration. Record the evidence;
  an authorized new take requires a new prepared operation and reviewed request.
