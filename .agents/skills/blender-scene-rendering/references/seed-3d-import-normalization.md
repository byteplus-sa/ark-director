# Seed 3D import normalization

Use this contract when a generated Hyper3D or Hitem3d package becomes a Blender
asset. Generation success proves only that the provider produced a package;
Blender readiness requires a separate import and inspection pass.

## Preserve provenance

Before extraction or import, record:

- provider family and model ID;
- request and reference hashes;
- MCP task ID and provider task ID as separate values;
- artifact ID, package byte size, and SHA-256;
- requested format, material mode, topology settings, and texture options;
- provider status and source URL expiry when available.

Keep the downloaded package immutable. Extract into a new bounded directory,
reject absolute paths and parent traversal, and never overwrite the provider
archive with Blender exports.

## Format choice

Prefer GLB for the first Blender handoff because it packages mesh, materials,
textures, hierarchy, and transforms in one file. Use FBX when an armature or a
downstream DCC requires it. Use OBJ for simple static geometry when external
texture files are acceptable. STL contains geometry only and is unsuitable
when appearance matters. USDZ is primarily a delivery format rather than the
default Blender working format.

## Quarantine import

1. Save the current `.blend` before import.
2. Import into a dedicated collection named for the asset and take.
3. Do not merge the imported hierarchy into production collections yet.
4. Record imported object, mesh, material, image, and armature counts.
5. Capture a neutral viewport screenshot before cleanup.

## Normalize a working copy

- Set the scene unit system and record the source-to-scene scale conversion.
- Inspect world-space dimensions before applying transforms.
- Move the working copy to the intended origin and ground plane while
  preserving the untouched imported collection.
- Resolve forward/up-axis orientation explicitly; do not rotate by eye without
  recording the correction.
- Apply transforms only after scale and axis decisions are approved for the
  working copy.
- Recalculate normals when evidence shows they are incorrect. Do not use this
  as a blanket repair for missing or inverted geometry.

## Geometry and appearance QA

Record bounding-box dimensions, object and face counts, non-manifold findings,
loose geometry, degenerate faces, normal orientation, UV-layer count, material
slots, missing images, and texture resolution. Confirm that transparent areas,
PBR channels, and material assignments match the requested generation mode.

For animation use, inspect whether the package contains an armature, skin
weights, shape keys, and a neutral pose. A humanoid-looking mesh is not
automatically rig-ready. Keep topology cleanup and rigging as explicit later
stages rather than silently changing the generated asset during import.

## Handoff to Blender-to-Seedance

The generated 3D asset supplies appearance and structure. It does not become
the motion authority merely because it is imported into the blockout. The
animated Blender previz remains the motion, camera, cut, and timing master.
Bind the normalized asset to the corresponding stable subject ID and retain
the generated package hash in the asset manifest.

Complete the handoff only after the normalized working copy has a saved
`.blend`, recorded measurements, a viewport screenshot, and an explicit
`review` state. Provider success or successful import does not imply creative
approval.
