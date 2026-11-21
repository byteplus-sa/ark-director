# Linking & Appending

### Append (Copy into Current File)

```python
import bpy

blend_path = "/path/to/library.blend"

# Append a single object
with bpy.data.libraries.load(blend_path) as (data_from, data_to):
    data_to.objects = ["ObjectName"]

# Link appended objects to active collection
for obj in data_to.objects:
    if obj is not None:
        bpy.context.collection.objects.link(obj)

# Append specific data types
with bpy.data.libraries.load(blend_path) as (data_from, data_to):
    data_to.materials = ["MaterialName"]
    data_to.node_groups = ["NodeGroupName"]
    data_to.collections = ["CollectionName"]
    data_to.worlds = ["WorldName"]
```

### Link (Reference, Stay Connected)

```python
import bpy

blend_path = "/path/to/library.blend"

with bpy.data.libraries.load(blend_path, link=True) as (data_from, data_to):
    data_to.collections = ["CollectionName"]

# Link collection instance to scene
for coll in data_to.collections:
    if coll is not None:
        bpy.context.collection.children.link(coll)

# Make library override (editable linked data)
# Select linked object first
bpy.ops.object.make_override_library()
```

### Reload / Relocate Libraries

```python
import bpy

for lib in bpy.data.libraries:
    lib.reload()  # Reload from disk

# Relocate a library to a new path
# lib.filepath = "/new/path/to/library.blend"
# lib.reload()
```
