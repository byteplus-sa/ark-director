# Generation And Persistence

Focused reference for `seedream-storyboard`. Read [the entrypoint](../SKILL.md) for
mode selection and caller responsibilities.

- [10. Generate variants when requested or authorized](#10-generate-variants-when-requested-or-authorized)
- [11. Persist every generated result locally](#11-persist-every-generated-result-locally)
- [Downloading artifacts](#downloading-artifacts)
- [Manifest and metadata](#manifest-and-metadata)

### 10. Generate variants when requested or authorized

For actual image creation:

- use `seedream_generate_image` for a single panel, a single-image grid, or a
  sequence-capable batch of separate images;
- use `seedream_generate_image_variations` for independent alternatives;
- use `seedream_edit_image` for point- or bounding-box-guided corrections;
- set `persist: true`;
- use the lowest suitable draft size;
- set `watermark: false` unless the user requires a visible watermark;
- use `prompt_optimization: standard` for final candidates and `fast` only when
  latency matters more than fidelity.
- Upload and pass the resolved local Element files as ordered reference inputs;
  keep their `@Image N` indices identical in the prompt, request, and manifest.

For a one-panel board, generate three alternatives of that same panel by
default: `p010 v01`, `p010 v02`, and `p010 v03`. They share the same decisive
moment and continuity contract but explore useful composition, lens, staging,
or lighting differences. They are candidates, not a narrative sequence.

For a multi-panel single-image grid board, generate three variants of the whole
grid by default: `board v01`, `board v02`, and `board v03`. They share the same
panel plan and continuity contract but may differ in composition within each
cell, grid layout balance, or rendering.

For a multi-panel separate-images board, generate three variants by default for
keyframes and high-risk panels. For ordinary continuity panels, first generate
one low-cost draft sequence; add alternatives only where composition or
continuity is unresolved.

### 11. Persist every generated result locally

Never rely only on a provider URL. Use durable artifact persistence and save the
actual file under:

```text
projects/<project>/scenes/scene-NN/
```

For individual panels (one-panel board, separate-images mode, or a panel
promoted from a grid):

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

Set `output_path` on the generation call (an absolute file path, or a directory
ending in `/`, inside an allowed output root) so the file is written locally and
reported in the artifact's `local_path`. The durable artifact is always kept. If
the call did not set it, copy the persisted artifact with
`seed_media_export_artifact`, or pass `response_format: "url"` and download the
presigned URL promptly. Do not hand-decode Base64 from tool output: large
artifacts are truncated.

### Manifest and metadata

The prompt snapshot must contain the exact submitted prompt and parameters, with
its SHA-256 in the manifest. When an approved panel is explicitly promoted to a
video keyframe, use the project keyframe naming convention separately:

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
- `video_handoff` with eligibility, promoted keyframe path, recommended image
  mode, target Seedance version (2.5 or 2.0), reference budget, and any
  invalidation reason.

Set a newly generated output to `review`, not `approved`.
Set `video_handoff.eligible: true` only after explicit panel approval and after
verifying that all recorded source-asset variants and hashes still match. A
changed character, location, or prop returns the dependent panel to `review`;
do not silently carry a stale panel into motion generation.

Use this minimum `source_assets` record for every visible canonical Element:

```yaml
source_assets:
  - element_id: lola-maria
    element_type: character
    role: character_identity
    path: elements/lola-maria/ref_01_front.png
    selected_variant: ref_01_front.png
    status: approved
    sha256: "..."
    prompt_token: "@Image 1"
```
