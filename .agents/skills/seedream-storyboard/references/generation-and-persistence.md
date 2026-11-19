# Generation And Persistence

Focused reference for `seedream-storyboard`. Read [the entrypoint](../SKILL.md) for
mode selection and caller responsibilities.

- [10. Generate variants when requested or authorized](#10-generate-variants-when-requested-or-authorized)
- [11. Persist every generated result locally](#11-persist-every-generated-result-locally)
- [Downloading artifacts](#downloading-artifacts)
- [Manifest and metadata](#manifest-and-metadata)

### 10. Generate variants when requested or authorized

For authorized image creation, the caller submits `seedream_generate_image`
through `ark_job_submit` after selected-model and tool verification:

- use one image for a single panel or a whole grid;
- use `variations` for independent samples (separate calls, not native batch);
- use `max_images` above one only for verified native sequential output.
  Seedream 5.5 and Pro do not support native batches; do not downgrade models
  to obtain them or combine native batches with `variations` above one;
- for corrections, put the source first in `images` and use structured `point`
  or `bbox` integer coordinates in 0-999, without raw tags in the prompt;
- set `persist: true`;
- use the lowest suitable draft size;
- set `watermark: false` unless the user requires a visible watermark;
- use `prompt_optimization` only when supported; 5.5 accepts `standard`, not
  `fast`. Latency preference does not establish capability.
- Pass Element files as HTTPS URLs or schema-supported base64, never local filepaths;
  keep their `@Image N` indices identical in the prompt, request, and manifest.

Default review uses one sample per panel or whole grid; strict uses three
stochastic samples where applicable. Explicit requested count or creative
alternatives wins. Comparison samples keep prompt, references and effective
parameters identical except supported seed variation. Creative alternatives
change only requested axes with their own provenance. Samples are candidates,
not extra story beats. Prompt-only work authorizes no calls.

### 11. Persist every generated result locally

Never rely only on a provider URL. Use durable artifact persistence and save the
actual file under:

```text
projects/<project>/scenes/scene-NN/
```

For individual panels (one-panel board, separate-images mode, or a standalone
panel regenerated from a grid):

```text
<scene>_sh<NNN>_p<NNN>_t<NN>_v<NN>.<ext>
```

Example:

```text
s01_sh010_p020_t01_v01.png
prompt_s01_sh010_p020_t01_v01.md
```

For a single-image grid (the whole board in one file):

```text
<scene>_sh<NNN>_board_t<NN>_v<NN>.<ext>
```

Example:

```text
s01_sh010_board_t01_v01.png
prompt_s01_sh010_board_t01_v01.md
```

The `board` token indicates the composite grid image containing all panels;
individual panel prompts are recorded in the same prompt snapshot under their
panel numbers.

### Downloading artifacts

The durable artifact is always kept. Through `ark_job_submit`, never pass
`output_path` or `output_dir`; inspect terminal state and any `persistence_error`
with `ark_job_get`, then copy the persisted artifact with
`seed_media_export_artifact` and verify its bytes and hash. A direct call with
MCP task augmentation may set `output_path` (an absolute path inside an allowed
output root) instead. Alternatively, pass `response_format: "url"` and download the
presigned URL promptly. Do not hand-decode Base64 from tool output: large
artifacts are truncated. Recover persistence/export failures without regenerating;
reconcile uncertain submission before retrying.

### Manifest and metadata

The prompt snapshot must contain the exact submitted prompt and parameters, with
its SHA-256 in the manifest. A video keyframe is never this panel file or a crop
of it. When a shot needs one, the caller authors a new full-colour, text-free
keyframe prompt from the element references and the panel's staging text, and
saves it under the project keyframe naming convention:

```text
s01_kf01_v01.png
```

Do not overwrite the storyboard source panel.

Record:

- model and model ID;
- ordered reference list and role of each image;
- prompt file and hash;
- size, format, watermark, seed, optimization mode, and batch count;
- output path, byte size, and hash;
- provider artifact ID when available;
- generated variants;
- requested delta and acceptance criteria;
- status;
- `source_assets` with each path, role, selected variant, approval state, and
  SHA-256;
- `video_handoff` with eligibility, the staging text to carry into the shot
  prompt, the element references to bind (paths and hashes from
  `source_assets`), `bind_board: false`, and any invalidation reason.

Set a newly generated output to `review`, not `approved`.
Set `video_handoff.eligible: true` only after a mode-authorized panel approval
and after verifying that all recorded source-asset variants and hashes still
match. Eligibility means the staging is approved for translation into prompt
text; the board file itself is never a video input. A changed character,
location, or prop returns the dependent panel to `review`; do not silently
carry stale staging into motion generation.

Use this minimum `source_assets` record for every visible canonical Element:

```yaml
source_assets:
  - element_id: mara
    element_type: character
    role: character_identity
    path: elements/mara/ref_01_front.png
    selected_variant: ref_01_front.png
    status: approved
    sha256: "..."
    prompt_token: "@Image 1"
```
