# Blockout manifest contract

The Blender scene remains the editable source, while the blockout manifest is
the machine-readable handoff to prompt composition, request preflight, and QA.
Do not maintain a separate hand-written dummy map when a current manifest is
available.

Use [blockout-manifest.schema.json](blockout-manifest.schema.json) as the format
authority and validate it before rendering or submitting:

```bash
uv run python .agents/skills/blender-to-seedance/scripts/validate_blockout_manifest.py projects/<project>/scenes/<scene>/<shot>/blockout_manifest.json
```

## Blender metadata

Give each visible proxy a stable semantic identity. Store these values as
custom properties or derive them deterministically from a maintained scene
registry:

| Property | Purpose |
|---|---|
| `ad_subject_id` | Stable lowercase ID used by motion checks and prompt bindings |
| `ad_proxy_role` | Character, vehicle, product, prop, environment, support, effect, or camera target |
| `ad_final_subject` | Plain-language identity used in the dummy mapping |
| `ad_proxy_color` | Unique six-digit color used only to distinguish proxies |
| `ad_appearance_reference` | Optional ordered `@Image N` binding |

Object names are Blender implementation identifiers. Subject IDs are the
production contract. Renaming an object must not silently change the subject
ID or its reference binding.

## Required manifest sections

- `source`: project-relative `.blend` path and SHA-256.
- `timeline`: FPS, FPS base, inclusive frame range, and measured duration.
- `render`: project-relative previz path, SHA-256, resolution, percentage,
  container, and codec.
- `cameras` and `cuts`: stable camera IDs and the first frame where each camera
  becomes active. The first camera assignment starts at `frame_start`.
- `subjects`: every visible proxy, including support surfaces or fixed targets
  used by motion checks.
- `motion_checks`: observable rules with a frame window and measurable
  expectation.
- `conditioning`: `control_only: true` until explicit selection is recorded.

The timeline uses an inclusive frame count:

```text
duration_seconds = (frame_end - frame_start + 1) / (fps / fps_base)
```

## Motion checks

Use the smallest check set that proves the intended action:

| Type | Required expectation | Typical use |
|---|---|---|
| `distance_trend` | Target and increasing, decreasing, or stable trend | Hand reaching toward a wrench |
| `world_displacement` | Axis, positive/negative direction, and minimum delta | Car or astronaut advances through the scene |
| `ground_contact` | Support target and maximum gap | Tires remain on the countertop |
| `rotation_from_travel` | Parent target and minimum revolutions | Wheel roll follows vehicle travel |
| `screen_occupancy` | Minimum and maximum frame fraction | Product remains readable |
| `end_state` | Observable terminal relationship | Open hand stops short of the wrench |

Motion checks are acceptance criteria, not proof that the animation satisfies
them. Record observations through the temporal QA procedure after rendering.

## Conditioning state

An analysis-only blockout contains:

```json
{
  "conditioning": {
    "control_only": true
  }
}
```

When the user explicitly selects that exact previz for generation, record the
selection manifest, field, key, and selected previz SHA-256 and set
`control_only: false`. The validator requires the selected hash to equal the
current render hash. A flag change without the selection evidence is invalid.

## Change handling

Recompute the `.blend` and previz hashes after any material scene or render
change. Changes to subject identity, camera cuts, timing, or motion invalidate
the previous prompt package, request review, and temporal QA. Surface-only
changes to the eventual Seedance dressing do not change the Blender motion
manifest unless they alter reference bindings.
