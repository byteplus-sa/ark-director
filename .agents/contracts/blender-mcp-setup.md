# Blender MCP Setup

Reference for the eight `blender-*` skills vendored from
`ra100/blender-claude-plugin` (see `skills-lock.json`). The skills were written
against the upstream "Blender Lab" MCP server whose tools are unprefixed
(`execute_blender_code`, `get_objects_summary`, `search_api_docs`, …). This
workspace connects to a different Blender MCP surface whose tools carry a
`blender_` prefix. Treat this mapping as adapter guidance; resolve actual callable names from the connected tool inventory before use.

## Tool-name mapping

| Vendored (upstream) tool | Connected (`blender_`) tool |
|---|---|
| `execute_blender_code` | `blender_execute_blender_code` |
| `get_objects_summary` | `blender_get_scene_info` |
| `get_object_detail_summary` | `blender_get_object_info` |
| `get_screenshot_of_window_as_image` / `get_screenshot_of_area_as_image` | `blender_get_viewport_screenshot` |
| `render_thumbnail_to_path` / `render_viewport_to_path` | `blender_get_viewport_screenshot` |
| `get_blendfile_summary_*`, `jump_to_*`, `search_api_docs`, `get_python_api_docs`, `search_manual_docs` | No connected equivalent — use `blender_execute_blender_code` to inspect data, and confirm API/doc details via a docs lookup tool such as Context7. |

## Detection

The connected Blender MCP server is available when tools prefixed `blender_`
are present (e.g. `blender_execute_blender_code`, `blender_get_scene_info`,
`blender_get_object_info`, `blender_get_viewport_screenshot`). When those tools
are absent, fall back to emitting self-contained `bpy` scripts.

Core connection, add-on compatibility, and optional generators are separate
capabilities. When exposed, use add-on and generator status tools to verify
protocol compatibility and whether Hyper3D or Hunyuan3D integration is enabled.
Do not infer optional generation support from a working `bpy` execution tool.
The Blender add-on's Hyper3D integration and the separate ModelArk MCP Seed 3D
tool registration are independent surfaces; check the surface actually selected
for the operation.

## Runtime capability probe

Before using a version-gated API, run
[probe_blender_runtime.py](../skills/blender-to-seedance/scripts/probe_blender_runtime.py)
inside the connected Blender process. Retain its Blender and Python versions,
available render-engine identifiers, current engine, resolution, FPS base,
effective FPS, and frame range with the operation evidence.

The live RNA enum is authoritative for engine identifiers. Prefer the available
EEVEE identifier selected by the probe rather than hard-coding
`BLENDER_EEVEE` or `BLENDER_EEVEE_NEXT` from a different Blender minor.

## Workflow

1. Inspect core, add-on, optional-generator, and runtime capabilities.
2. Inspect the scene with `blender_get_scene_info` / `blender_get_object_info`.
3. Mutate via small, idempotent `blender_execute_blender_code` calls.
4. Verify data state and viewport appearance.
5. For animation or video work, verify the rendered media temporally; a
   screenshot does not prove motion or timing.

## Notes

- These skills support Blender modeling, generated-3D normalization, previz,
  and post work. The `blender-to-seedance` orchestrator owns the project-local
  3D blockout-to-video handoff; the vendored leaf skills remain independently
  usable. Cross-project installation is a separate explicit task.
- The skills document Blender 5.0/5.1 API; the local install may be a newer
  minor (e.g. 5.2). Verify version-gated API claims against the installed
  `bpy` before relying on them.
