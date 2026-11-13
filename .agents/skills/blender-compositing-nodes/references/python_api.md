# Blender Compositor Nodes - Python API Reference

**Local safety overlay (SD-001):** Keep the upstream reference organization and
review this overlay before re-vendoring. Examples that add individual nodes are
API illustrations, not authorization to mutate existing graphs. Use stable
caller-approved ownership/role keys for a rerunnable branch. Never clear an
existing tree or silently redirect Composite, Viewer or File Output sockets.

## Setting Up the Compositor

```python
import bpy

scene = bpy.context.scene
if scene.library is not None or not scene.is_editable:
    raise ValueError("Compositor scene must be local and editable")

scene.use_nodes = True
tree = scene.node_tree
if tree is None:
    raise RuntimeError("Resolve the compositor tree API for this Blender runtime")
nodes = tree.nodes
links = tree.links
```

Enabling compositor use can create defaults; preserve those too. The following
helper builds a separate owned branch and returns its endpoint without an output
takeover. Reject duplicate ownership roles, type collisions or foreign boundary
links before writing. Names alone never establish ownership. A node already
connected to someone else's branch requires separate integration approval.

```python
def build_owned_color_grade(tree, owner_key):
    if not isinstance(owner_key, str) or not owner_key.strip():
        raise ValueError("A caller-approved ownership key is required")
    if tree.library is not None or not tree.is_editable:
        raise ValueError("Compositor tree must be local and editable")
    plan = (
        ("render", "CompositorNodeRLayers"),
        ("denoise", "CompositorNodeDenoise"),
        ("balance", "CompositorNodeColorBalance"),
        ("saturation", "CompositorNodeHueSat"),
    )
    branch = {}
    for role, node_type in plan:
        matches = [
            node for node in tree.nodes
            if node.get("local_overlay_owner") == owner_key
            and node.get("local_overlay_role") == role
        ]
        if len(matches) > 1 or (matches and matches[0].bl_idname != node_type):
            raise ValueError(f"Owned node role collision: {role}")
        if matches:
            branch[role] = matches[0]
    for link in tree.links:
        source_owned = any(link.from_node is node for node in branch.values())
        target_owned = any(link.to_node is node for node in branch.values())
        if source_owned != target_owned:
            raise ValueError("Owned branch has a foreign link; resolve routing approval")
    edges = (
        ("render", "Image", "denoise", "Image"),
        ("render", "Denoising Normal", "denoise", "Normal"),
        ("render", "Denoising Albedo", "denoise", "Albedo"),
        ("denoise", "Image", "balance", "Image"),
        ("balance", "Image", "saturation", "Image"),
    )
    for source_role, output_name, target_role, input_name in edges:
        if target_role not in branch:
            continue
        target_socket = branch[target_role].inputs[input_name]
        for link in tree.links:
            if link.to_socket is target_socket and (
                source_role not in branch
                or link.from_socket is not branch[source_role].outputs[output_name]
            ):
                raise ValueError("Existing owned input has a conflicting link")
    selection = [(node, node.select) for node in tree.nodes]
    active = tree.nodes.active
    created_nodes = []
    created_links = []
    try:
        for index, (role, node_type) in enumerate(plan):
            if role in branch:
                continue
            node = tree.nodes.new(type=node_type)
            created_nodes.append(node)
            branch[role] = node
            node["local_overlay_owner"] = owner_key
            node["local_overlay_role"] = role
            node.location = (-600 + index * 300, -400)
            if role == "saturation":
                node.inputs["Saturation"].default_value = 1.1
        for source_role, output_name, target_role, input_name in edges:
            output = branch[source_role].outputs[output_name]
            input_socket = branch[target_role].inputs[input_name]
            if not any(
                link.from_socket is output and link.to_socket is input_socket
                for link in tree.links
            ):
                created_links.append(tree.links.new(output, input_socket))
        return branch["saturation"]
    except Exception:
        for link in reversed(created_links):
            tree.links.remove(link)
        for node in reversed(created_nodes):
            tree.nodes.remove(node)
        raise
    finally:
        for node in created_nodes:
            if any(node is current for current in tree.nodes):
                node.select = False
        for node, selected in selection:
            node.select = selected
        tree.nodes.active = active
```

Snapshot the graph before separately authorized whole-tree replacement. That
operation is intentionally absent from this default recipe. After building,
check required pass/socket support on the authorized view layer and obtain
explicit approval for the exact output destination before connecting it.

## Adding Nodes

All compositor nodes use `nodes.new(type=<type_string>)`.

### Input Nodes

```python
# Render Layers (primary input)
render_layers = nodes.new(type='CompositorNodeRLayers')

# Image input
image_node = nodes.new(type='CompositorNodeImage')
image_node.image = bpy.data.images.load("/path/to/image.exr")

# Movie Clip
clip_node = nodes.new(type='CompositorNodeMovieClip')
clip_node.clip = bpy.data.movieclips.load("/path/to/video.mp4")

# Mask
mask_node = nodes.new(type='CompositorNodeMask')
# mask_node.mask = bpy.data.masks["MyMask"]

# Constants
color_node = nodes.new(type='CompositorNodeRGB')
color_node.outputs[0].default_value = (1.0, 0.5, 0.0, 1.0)

value_node = nodes.new(type='CompositorNodeValue')
value_node.outputs[0].default_value = 0.5

# Bokeh Image
bokeh = nodes.new(type='CompositorNodeBokehImage')
bokeh.flaps = 6  # Number of aperture blades

# Scene Time
scene_time = nodes.new(type='CompositorNodeSceneTime')
```

### Output Nodes

```python
# Final composite output
composite = nodes.new(type='CompositorNodeComposite')

# Viewer (backdrop preview)
viewer = nodes.new(type='CompositorNodeViewer')

# Split viewer (comparison)
split = nodes.new(type='CompositorNodeSplitViewer')
split.axis = 'X'  # 'X' or 'Y'
split.factor = 50  # Split position (percentage)

# File Output (save to disk)
file_out = nodes.new(type='CompositorNodeOutputFile')
file_out.base_path = "/path/to/output/"
file_out.format.file_format = 'OPEN_EXR_MULTILAYER'  # or 'PNG', 'JPEG', 'OPEN_EXR', etc.
```

### Color Nodes

```python
# Mix RGB
mix = nodes.new(type='CompositorNodeMixRGB')
mix.blend_type = 'MIX'  # MIX, ADD, MULTIPLY, SCREEN, OVERLAY, DARKEN, LIGHTEN, etc.
mix.use_alpha = False
mix.inputs['Fac'].default_value = 1.0

# Alpha Over
alpha_over = nodes.new(type='CompositorNodeAlphaOver')
alpha_over.premul = 0.0  # Premultiply factor

# Color Balance
color_balance = nodes.new(type='CompositorNodeColorBalance')
color_balance.correction_method = 'LIFT_GAMMA_GAIN'  # or 'OFFSET_POWER_SLOPE'
color_balance.lift = (1.0, 1.0, 1.0)
color_balance.gamma = (1.0, 1.0, 1.0)
color_balance.gain = (1.0, 1.0, 1.0)

# Bright/Contrast
bright_contrast = nodes.new(type='CompositorNodeBrightContrast')
bright_contrast.inputs['Bright'].default_value = 0.0
bright_contrast.inputs['Contrast'].default_value = 0.0

# Hue/Saturation/Value
hue_sat = nodes.new(type='CompositorNodeHueSat')
hue_sat.inputs['Hue'].default_value = 0.5
hue_sat.inputs['Saturation'].default_value = 1.0
hue_sat.inputs['Value'].default_value = 1.0

# Color Correction
color_correct = nodes.new(type='CompositorNodeColorCorrection')
# Properties: master_saturation, master_gain, master_gamma, master_lift
# Per-range: highlights_saturation, midtones_saturation, shadows_saturation, etc.

# RGB Curves
curves = nodes.new(type='CompositorNodeCurveRGB')
# Access curve: curves.mapping.curves[0] = Combined, [1]=R, [2]=G, [3]=B

# Gamma
gamma = nodes.new(type='CompositorNodeGamma')
gamma.inputs['Gamma'].default_value = 1.0

# Invert
invert = nodes.new(type='CompositorNodeInvert')
invert.invert_rgb = True
invert.invert_alpha = False

# Tonemap
tonemap = nodes.new(type='CompositorNodeTonemap')
tonemap.tonemap_type = 'RH_SIMPLE'  # 'RH_SIMPLE' or 'RD_PHOTORECEPTOR'

# Set Alpha
set_alpha = nodes.new(type='CompositorNodeSetAlpha')
set_alpha.mode = 'APPLY'  # 'APPLY' or 'REPLACE_ALPHA'

# Color Ramp
color_ramp = nodes.new(type='CompositorNodeValToRGB')
ramp = color_ramp.color_ramp
ramp.elements[0].position = 0.0
ramp.elements[0].color = (0, 0, 0, 1)
ramp.elements[1].position = 1.0
ramp.elements[1].color = (1, 1, 1, 1)

# Combine / Separate Color
combine = nodes.new(type='CompositorNodeCombineColor')
combine.mode = 'RGB'  # 'RGB', 'HSV', 'HSL', 'YCC', 'YUV'
separate = nodes.new(type='CompositorNodeSeparateColor')
separate.mode = 'RGB'
```

### Filter Nodes

```python
# Blur
blur = nodes.new(type='CompositorNodeBlur')
blur.filter_type = 'GAUSS'  # FLAT, TENT, QUAD, CUBIC, GAUSS, FAST_GAUSS, CATROM, MITCH
blur.size_x = 10
blur.size_y = 10
blur.use_relative = False

# Bilateral Blur
bilateral = nodes.new(type='CompositorNodeBilateralblur')
bilateral.iterations = 1
bilateral.sigma_color = 0.3
bilateral.sigma_space = 5.0

# Directional Blur
dir_blur = nodes.new(type='CompositorNodeDBlur')
dir_blur.iterations = 1
dir_blur.angle = 0.0
dir_blur.zoom = 0.0
dir_blur.spin = 0.0

# Vector Blur
vec_blur = nodes.new(type='CompositorNodeVecBlur')
vec_blur.samples = 32
vec_blur.factor = 1.0

# Defocus (DOF)
defocus = nodes.new(type='CompositorNodeDefocus')
defocus.use_zbuffer = True
defocus.f_stop = 2.8
defocus.blur_max = 16
defocus.threshold = 1.0

# Denoise (OpenImageDenoise)
denoise = nodes.new(type='CompositorNodeDenoise')
denoise.use_hdr = True

# Glare
glare = nodes.new(type='CompositorNodeGlare')
glare.glare_type = 'BLOOM'  # BLOOM, STREAKS, FOG_GLOW, GHOSTS
glare.quality = 'HIGH'  # LOW, MEDIUM, HIGH
glare.threshold = 1.0
glare.mix = 0.0  # -1 = original only, 0 = original + glare, 1 = glare only
# Streaks-specific:
glare.streaks = 4
glare.angle_offset = 0.0

# Dilate/Erode
dilate = nodes.new(type='CompositorNodeDilateErode')
dilate.mode = 'STEP'  # STEP, THRESHOLD, DISTANCE, FEATHER
dilate.distance = 1  # Positive = dilate, negative = erode

# Filter (convolution)
filter_node = nodes.new(type='CompositorNodeFilter')
filter_node.filter_type = 'SHARPEN'  # SOFTEN, SHARPEN, LAPLACE, SOBEL, PREWITT, KIRSCH, SHADOW

# Sun Beams
sunbeams = nodes.new(type='CompositorNodeSunBeams')
sunbeams.source = (0.5, 0.5)  # Source position (0-1 normalized)
sunbeams.ray_length = 0.2

# Anti-Aliasing
aa = nodes.new(type='CompositorNodeAntiAliasing')
aa.threshold = 1.0
aa.contrast_limit = 0.9
```

### Matte Nodes

```python
# Keying (full-featured chroma key)
keying = nodes.new(type='CompositorNodeKeying')
keying.inputs['Key Color'].default_value = (0.0, 1.0, 0.0, 1.0)  # Green
keying.clip_black = 0.0
keying.clip_white = 1.0
keying.despill_factor = 1.0
keying.despill_balance = 0.5
keying.blur_pre = 0
keying.blur_post = 0

# Keying Screen
keying_screen = nodes.new(type='CompositorNodeKeyingScreen')
# keying_screen.clip = bpy.data.movieclips["MyClip"]

# Channel Key
channel_key = nodes.new(type='CompositorNodeChannelMatte')
channel_key.color_space = 'YCC'  # RGB, HSV, YUV, YCC
channel_key.matte_channel = 'G'  # R, G, B

# Chroma Key
chroma_key = nodes.new(type='CompositorNodeChromaMatte')
chroma_key.tolerance = 30.0
chroma_key.threshold = 10.0
chroma_key.gain = 1.0

# Luminance Key
luma_key = nodes.new(type='CompositorNodeLumaMatte')
luma_key.limit_max = 1.0
luma_key.limit_min = 0.0

# Box Mask
box_mask = nodes.new(type='CompositorNodeBoxMask')
box_mask.x = 0.5
box_mask.y = 0.5
box_mask.width = 0.5
box_mask.height = 0.5

# Ellipse Mask
ellipse_mask = nodes.new(type='CompositorNodeEllipseMask')
ellipse_mask.x = 0.5
ellipse_mask.y = 0.5
ellipse_mask.width = 0.5
ellipse_mask.height = 0.5

# Cryptomatte
cryptomatte = nodes.new(type='CompositorNodeCryptomatteV2')
cryptomatte.source = 'RENDER'  # 'RENDER' or 'IMAGE'
# cryptomatte.matte_id = "ObjectName"
```

### Converter Nodes

```python
# Math
math = nodes.new(type='CompositorNodeMath')
math.operation = 'ADD'  # ADD, SUBTRACT, MULTIPLY, DIVIDE, POWER, GREATER_THAN, LESS_THAN, etc.

# Map Range
map_range = nodes.new(type='CompositorNodeMapRange')
map_range.inputs['From Min'].default_value = 0.0
map_range.inputs['From Max'].default_value = 1.0
map_range.inputs['To Min'].default_value = 0.0
map_range.inputs['To Max'].default_value = 1.0

# Map Value
map_value = nodes.new(type='CompositorNodeMapValue')
map_value.offset = [0.0]
map_value.size = [1.0]
map_value.use_min = False
map_value.use_max = False

# RGB to BW
rgb_to_bw = nodes.new(type='CompositorNodeRGBToBW')

# Alpha Convert
alpha_convert = nodes.new(type='CompositorNodePremulKey')
alpha_convert.mapping = 'PREMUL_TO_STRAIGHT'  # or 'STRAIGHT_TO_PREMUL'

# ID Mask
id_mask = nodes.new(type='CompositorNodeIDMask')
id_mask.index = 1  # Object/Material index to isolate
id_mask.use_antialiasing = True
```

### Distort Nodes

```python
# Lens Distortion
lens_dist = nodes.new(type='CompositorNodeLensdist')
lens_dist.inputs['Distort'].default_value = 0.0
lens_dist.inputs['Dispersion'].default_value = 0.0
lens_dist.use_fit = True

# Transform
transform = nodes.new(type='CompositorNodeTransform')
transform.filter_type = 'BILINEAR'  # NEAREST, BILINEAR, BICUBIC

# Scale
scale = nodes.new(type='CompositorNodeScale')
scale.space = 'RELATIVE'  # RELATIVE, ABSOLUTE, SCENE_SIZE, RENDER_SIZE

# Translate
translate = nodes.new(type='CompositorNodeTranslate')
translate.use_relative = False

# Rotate
rotate = nodes.new(type='CompositorNodeRotate')
rotate.filter_type = 'BILINEAR'

# Flip
flip = nodes.new(type='CompositorNodeFlip')
flip.axis = 'X'  # 'X', 'Y', 'XY'

# Crop
crop = nodes.new(type='CompositorNodeCrop')
crop.use_crop_size = True
crop.min_x = 0
crop.min_y = 0
crop.max_x = 1920
crop.max_y = 1080

# Displace
displace = nodes.new(type='CompositorNodeDisplace')
```

## Linking Nodes

```python
# By socket name
links.new(render_layers.outputs['Image'], denoise.inputs['Image'])
links.new(render_layers.outputs['Denoising Normal'], denoise.inputs['Normal'])
links.new(render_layers.outputs['Denoising Albedo'], denoise.inputs['Albedo'])
links.new(denoise.outputs['Image'], composite.inputs['Image'])

# By index
links.new(render_layers.outputs[0], composite.inputs[0])
```

## Node Positioning

```python
render_layers.location = (-600, 0)
denoise.location = (-300, 0)
color_balance.location = (0, 0)
composite.location = (300, 0)
viewer.location = (300, -200)
```

## Enabling Render Passes

```python
view_layer = bpy.context.view_layer

# Data passes
view_layer.use_pass_z = True                    # Depth
view_layer.use_pass_normal = True               # Normals
view_layer.use_pass_mist = True                 # Mist
view_layer.use_pass_position = True             # World Position
view_layer.use_pass_vector = True               # Motion Vectors (Speed)
view_layer.use_pass_uv = True                   # UV coordinates
view_layer.use_pass_object_index = True         # Object Index
view_layer.use_pass_material_index = True       # Material Index

# Denoising data
view_layer.use_pass_denoising_normal = True     # For Denoise node
view_layer.use_pass_denoising_albedo = True     # For Denoise node

# Light passes (Cycles)
view_layer.use_pass_diffuse_direct = True
view_layer.use_pass_diffuse_indirect = True
view_layer.use_pass_diffuse_color = True
view_layer.use_pass_glossy_direct = True
view_layer.use_pass_glossy_indirect = True
view_layer.use_pass_glossy_color = True
view_layer.use_pass_transmission_direct = True
view_layer.use_pass_transmission_indirect = True
view_layer.use_pass_transmission_color = True
view_layer.use_pass_volume_direct = True
view_layer.use_pass_volume_indirect = True
view_layer.use_pass_emit = True
view_layer.use_pass_environment = True
view_layer.use_pass_shadow = True
view_layer.use_pass_ambient_occlusion = True

# Cryptomatte
view_layer.use_pass_cryptomatte_object = True
view_layer.use_pass_cryptomatte_material = True
view_layer.use_pass_cryptomatte_asset = True
view_layer.use_pass_cryptomatte_accurate = True
```

## File Output Configuration

### Multi-Layer EXR

```python
file_out = nodes.new(type='CompositorNodeOutputFile')
file_out.base_path = "/path/to/output/"
file_out.format.file_format = 'OPEN_EXR_MULTILAYER'
file_out.format.color_depth = '32'  # '16' or '32'
file_out.format.exr_codec = 'ZIP'  # NONE, PXR24, ZIP, PIZ, RLE, ZIPS, B44, B44A, DWAA, DWAB

# Remove default input
file_out.file_slots.clear()

# Add inputs for each pass
file_out.file_slots.new("beauty")
file_out.file_slots.new("diffuse_color")
file_out.file_slots.new("glossy_direct")
file_out.file_slots.new("normal")
file_out.file_slots.new("depth")

# Connect
links.new(render_layers.outputs['Image'], file_out.inputs['beauty'])
links.new(render_layers.outputs['DiffCol'], file_out.inputs['diffuse_color'])
links.new(render_layers.outputs['GlossDir'], file_out.inputs['glossy_direct'])
links.new(render_layers.outputs['Normal'], file_out.inputs['normal'])
links.new(render_layers.outputs['Depth'], file_out.inputs['depth'])
```

### Separate Image Files

```python
file_out = nodes.new(type='CompositorNodeOutputFile')
file_out.base_path = "/path/to/output/"
file_out.format.file_format = 'PNG'

# Each slot can have its own path (relative to base_path)
file_out.file_slots.clear()
slot = file_out.file_slots.new("beauty_")
slot = file_out.file_slots.new("normal_")
slot = file_out.file_slots.new("depth_")

# Connect
links.new(render_layers.outputs['Image'], file_out.inputs['beauty_'])
links.new(render_layers.outputs['Normal'], file_out.inputs['normal_'])
links.new(render_layers.outputs['Depth'], file_out.inputs['depth_'])
```

## Common Compositing Pipelines

### Full Denoise + Color Grade Pipeline

Load the setup and `build_owned_color_grade` helper above. Supply
`approved_branch_key` from the caller's inspected ownership scope. This recipe
does not enable render passes or change output routing by inference.

```python
import bpy

scene = bpy.context.scene
if scene.library is not None or not scene.is_editable:
    raise ValueError("Compositor scene must be local and editable")
scene.use_nodes = True
tree = scene.node_tree
if tree is None:
    raise RuntimeError("Resolve the compositor tree API for this Blender runtime")
endpoint = build_owned_color_grade(tree, approved_branch_key)
```

## Frame Nodes for Organization

```python
frame = nodes.new(type='NodeFrame')
frame.label = "Denoise Stage"
frame.use_custom_color = True
frame.color = (0.2, 0.3, 0.4)

denoise.parent = frame
```
