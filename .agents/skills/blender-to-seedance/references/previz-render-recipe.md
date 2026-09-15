# Previz render recipe (Blender → Seedance master)

Build a flat-gray, viewport-like previz and render it to a 24fps MPEG-4 clip
that Seedance 2.5 will treat as the motion master.

Blender 5.x removed `bpy.ops.render.opengl`; render with a lightweight **EEVEE**
setup and flat materials instead.

## Target contract

| Property | Value |
|---|---|
| Resolution | 1920 x 1080 |
| FPS | 24 |
| Frame range | `1 .. int(24 * duration)` |
| Format | FFMPEG / MPEG4, codec H264 |
| Look | Flat untextured identity colors, neutral world, AO + one soft light |

## Render snippet

```python
import bpy

scene = bpy.context.scene
engine_property = bpy.types.RenderSettings.bl_rna.properties.get('engine')
engine_items = getattr(engine_property, 'enum_items_static', None)
if engine_items is None:
    engine_items = getattr(engine_property, 'enum_items', [])
available_engines = {item.identifier for item in engine_items}
eevee_engine = next(
    (candidate for candidate in ('BLENDER_EEVEE_NEXT', 'BLENDER_EEVEE') if candidate in available_engines),
    None,
)
if eevee_engine is None:
    raise RuntimeError('No supported EEVEE render engine is available')

scene.render.engine = eevee_engine
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.resolution_percentage = 100
scene.render.fps = 24
scene.render.fps_base = 1.0
scene.render.frame_step = 1
scene.render.frame_start = 1
scene.render.frame_end = scene.render.frame_start + round(scene.render.fps * DURATION) - 1
scene.render.image_settings.file_format = 'FFMPEG'
scene.render.image_settings.color_mode = 'RGB'
scene.render.ffmpeg.format = 'MPEG4'
scene.render.ffmpeg.codec = 'H264'
scene.render.ffmpeg.constant_rate_factor = 'HIGH'
scene.render.ffmpeg.audio_codec = 'NONE'
scene.render.filepath = '//previz_<shot>_v01.mp4'

for mat in bpy.data.materials:
    bsdf = mat.node_tree.nodes.get('Principled BSDF') if mat.node_tree else None
    if bsdf:
        bsdf.inputs['Roughness'].default_value = 1.0

if bpy.context.scene.world:
    bpy.context.scene.world.color = (0.5, 0.5, 0.5)

bpy.ops.render.render(animation=True)
```

## Blockout conventions

- **Primitives = subjects.** Cube = person; monolith = hero; cylinder = can;
  spheres = fruit; boxes = props; checkerboard plane = "to replace".
- **Color = identity.** Distinct flat color per subject. Never rely on texture.
- **Monolith facing.** Paint a character proxy's faces: RED = the direction it
  faces, BLACK = its back, GREEN = sides/top. The prompt then reads facing
  direction as text.
- **Camera on splines.** Camera targets a null; cuts change only on frame
  boundaries. Handheld = slow sway + micro-tremor, never fast jitter.
- **Black gaps.** Leave empty frames where a later effect (liquid sim, etc.)
  will be generated separately.

## Minimal scene example (one hero, orbit camera)

```python
import bpy, math

def box(name, loc, scale, color):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    ob = bpy.context.active_object
    ob.name = name
    ob.scale = scale
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes['Principled BSDF']
    bsdf.inputs['Base Color'].default_value = (*color, 1.0)
    ob.data.materials.append(mat)
    return ob

bpy.ops.mesh.primitive_plane_add(size=40, location=(0, 0, 0))
box('hero', (0, 0, 1), (0.6, 0.6, 1.8), (0.8, 0.1, 0.1))

# Camera + target on an orbit
bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 1))
target = bpy.context.active_object
bpy.ops.object.camera_add(location=(6, 0, 2))
cam = bpy.context.active_object
cam.constraints.new('TRACK_TO').target = target

scene = bpy.context.scene
scene.camera = cam
scene.frame_start, scene.frame_end = 1, 120

cam.rotation_euler = (0, 0, 0)
for f in range(scene.frame_start, scene.frame_end + 1):
    a = (f - 1) / 24 * 2 * math.pi / 5
    cam.location = (6 * math.cos(a), 6 * math.sin(a), 2)
    cam.keyframe_insert('location', frame=f)
```

## Notes

- Verify the render in the viewport before the full pass (one test frame).
- Run `scripts/probe_blender_runtime.py` before relying on an engine identifier
  or version-specific property. The live enum is authoritative.
- Preserve flat identity colors. Do not overwrite all proxy materials with the
  same gray, because that destroys the subject mapping.
- Keep the `.blend` as the editable source; the MP4 is the submission master.
- After rendering, verify the actual stream with `ffprobe`, decode the complete
  file, update the manifest hashes, and run the temporal QA procedure.
