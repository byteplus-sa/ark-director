# Delivery And Manifest

Focused reference for `seedance-vfx-pipeline`. Read [the entrypoint](../SKILL.md) for
mode selection and caller responsibilities.

- [Step 5 — Download and save the asset](#step-5--download-and-save-the-asset)
- [Step 6 — Write the shot.md manifest](#step-6--write-the-shotmd-manifest)
- [Step 7 — Verify the prepared standalone prompt file](#step-7--verify-the-prepared-standalone-prompt-file)
- [Step 8 — Report results](#step-8--report-results)

## Step 5 — Download and save the asset

On `succeeded`, the MCP response includes `artifacts` with the generated video
(and optionally the last frame image). The MCP server's artifact store
(`persist_output: true`) has already persisted the asset.

Save the video in its shot directory:

```
projects/<project>/scenes/scene-NN/sNN_shNNN/sNN_shNNN_t01_v01.mp4
```

File naming follows the workspace convention:
- `<scene>_sh<NNN>_t<NN>_v<NN>.mp4` — e.g. `s01_sh010_t01_v01.mp4`
- If approved as final: `<scene>_sh<NNN>_final_v<NN>.mp4`

If `return_last_frame=true`, save the last frame image alongside the video for
chaining:

```
projects/<project>/scenes/scene-NN/sNN_shNNN/sNN_shNNN_t01_v01_lastframe.png
```

> **Delivery transcode (HEVC → H.264).** Seedance 2.5 edit outputs are usually
> HEVC (`video_codec: hevc`). Lark/doc previews and many players need H.264. Keep
> the HEVC master as the archival take and produce a browser-safe derivative:
>
> `ffmpeg -i <take>.mp4 -c:v libx264 -pix_fmt yuv420p -profile:v high -crf 20 -c:a aac -b:a 128k -movflags +faststart <take>_lark_h264.mp4`

## Step 6 — Write the shot.md manifest

Write the `shot.md` file in the shot directory with full YAML frontmatter for
reproducibility:

```
projects/<project>/scenes/scene-NN/sNN_shNNN/shot.md
```

**Manifest template:**

```yaml
---
project: <project>
scene: <scene>
shot: <shot>
model: <resolved model from the prepared request>
mode: V2V
vfx_level: <1 | 2 | 3>
references:
  - <source video path or URL>
  - elements/<character-id>/<character-sheet>.png
  - elements/<location-id>/<location-sheet>.png
prompt_file: scenes/scene-NN/sNN_shNNN/prompt_sNN_shNNN_t01_v01.md
prompt_sha256: <sha256 of exact submitted prompt>
seed: null
params:
  resolution: <submitted supported resolution>
  omni_reference_task_type: edit
  audio: true
  watermark: false
  return_last_frame: true
  submission_mode: single
take: t01
version: v01
status: review
cost_usd: <from MCP response>
billing_tokens_total: <from MCP response>
artifacts:
  - take: t01
    id: <artifact_id from MCP>
    uri: <seed-media:// URI from MCP>
    task_id: <task_id from MCP>
    media_type: video
    mime_type: video/mp4
    bytes: <file size>
    sha256: <hash>
    width: <probed width>
    height: <probed height>
    duration: <actual duration>
    audio_channels: 2
    audio_sample_rate: <from MCP>
    completion_tokens: <from MCP>
    cost_usd: <per-take cost>
    created_at: <ISO timestamp>
safety_identifier: <project>-<scene>-<shot>
---

# <shot> — VFX edit (<vfx_level>, <actual resolution>, <actual audio>)

<Description of the VFX edit performed on the source clip.>

## Source clip

- **Source**: `<source video path or URL>`
- **VFX level**: <1 — World Swap | 2 — Element Change | 3 — Handheld Showcase>

## Element references

- **@Image 1**: `<sheet>` — <element description>
- **@Video 1**: `<source>` — source clip for VFX edit

## Generation parameters

- **Model**: <resolved submitted model>
- **Resolution**: <probed width and height>
- **Ratio**: <probed aspect ratio>
- **Duration**: <N>s
- **generate_audio**: `true` (native diegetic audio); `false` for Object Swap,
  Motion Transfer and Restyle
- **Muted master** (Object Swap, Motion Transfer, Restyle): `<path>` — SHA-256 `<hash>`
- **Saved source audio**: `<path or none>` — SHA-256 `<hash>`
- **Post-audio route**: `<original | new | mixed | re-voiced>` — final mux `<path>`, SHA-256 `<hash>`
- **watermark**: `false`
- **return_last_frame**: `true` (for shot chaining)
- **safety_identifier**: `<project>-<scene>-<shot>`

## Cost

- <N> take × $<cost>/take = **$<total> total**
- <N> × <tokens> completion tokens = <total> total tokens

## Prompt

Full prompt text saved at:
- `scenes/scene-NN/sNN_shNNN/prompt_sNN_shNNN_t01_v01.md`

## Reproduction

To re-create this take from this manifest alone:

1. Resolve the prepared request and its exact prompt/reference hashes.
2. Validate the currently supported transport, model, operation, and ordered
   inputs; do not copy stale parameters or presigned URLs blindly.
3. A reproduction is a new authorized operation, not a retry of the original.
   Persist the new prepared request and complete its review before submission.
4. Poll the new task to terminal, then download and inspect the actual media.
5. Record actual streams, dimensions, duration, usage, and confirmed cost.

```

## Step 7 — Verify the prepared standalone prompt file

Verify the immutable prompt snapshot saved before submission, alongside the asset:

```
projects/<project>/scenes/scene-NN/sNN_shNNN/prompt_sNN_shNNN_t01_v01.md
```

The file is plain Markdown containing the full VFX prompt text (from
the selected model's complete edit grammar), human-readable and
shareable without parsing YAML frontmatter.

## Step 8 — Report results

After completion, report to the user:

| Field | Source |
|---|---|
| **Status** | `succeeded` / `failed` |
| **Local file path** | `projects/<project>/scenes/scene-NN/sNN_shNNN/<file>.mp4` |
| **Artifact URI** | `seed-media://artifacts/<id>` (MCP artifact store) |
| **Task ID** | From MCP response |
| **Cost** | `cost_usd` from MCP response |
| **Tokens** | `completion_tokens` from MCP response |
| **Resolution** | Probed output width and height |
| **Duration** | Actual output duration |
| **Last frame** | Path to saved last-frame PNG (if `return_last_frame=true`) |
| **Latency** | Wall-clock time from submit to succeeded |
| **Manifest** | `projects/<project>/scenes/scene-NN/sNN_shNNN/shot.md` |

If the task failed, report:
- The `error` field from the MCP response
- The `task_id` for support reference
- Suggested retry action (fix prompt, change reference, resubmit)
