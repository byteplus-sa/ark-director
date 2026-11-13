import ast
import re
import runpy
import sys
import tempfile
import types
import unittest
from contextlib import contextmanager
from pathlib import Path
from unittest.mock import patch

from ruamel.yaml import YAML

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / ".agents/skills"
PHYSICS = SKILLS / "blender-physics-simulation"
COMPOSITOR = SKILLS / "blender-compositing-nodes"
SCRIPTING = SKILLS / "blender-python-scripting"
AVATAR = SKILLS / "seedance-ai-avatar"


def python_blocks(path):
    return re.findall(r"```python\n(.*?)\n```", path.read_text(), re.DOTALL)


def load_recipe(path, function_name, bpy=None):
    for source in python_blocks(path):
        module = ast.parse(source)
        if any(
            isinstance(node, ast.FunctionDef) and node.name == function_name
            for node in module.body
        ):
            if any(
                not isinstance(node, (ast.Import, ast.ImportFrom, ast.FunctionDef))
                for node in module.body
            ):
                raise AssertionError("Helper block contains unexpected top-level actions")
            with (
                tempfile.TemporaryDirectory(prefix="batch-d-snippet-") as directory,
                patch.dict(sys.modules, {"bpy": bpy} if bpy else {}),
            ):
                script = Path(directory) / "recipe.py"
                script.write_text(source)
                namespace = runpy.run_path(str(script))
            return namespace[function_name]
    raise AssertionError(f"Missing executable recipe: {function_name} in {path}")


def run_section(path, heading, bpy, namespace=None):
    text = path.read_text().split(heading + "\n", 1)[1]
    source = re.findall(r"```python\n(.*?)\n```", text, re.DOTALL)[0]
    with (
        tempfile.TemporaryDirectory(prefix="batch-d-snippet-") as directory,
        patch.dict(sys.modules, {"bpy": bpy}),
    ):
        script = Path(directory) / "recipe.py"
        script.write_text(source)
        runpy.run_path(str(script), init_globals=namespace)


class FakeObject:
    def __init__(self, name, modifiers=(), selected=False):
        self.name = name
        self.type = "MESH"
        self.mode = "OBJECT"
        self.library = None
        self.override_library = None
        self.is_editable = True
        self.data = types.SimpleNamespace(
            library=None, override_library=None, is_editable=True, users=1
        )
        self.modifiers = list(modifiers)
        self.particle_systems = []
        self.soft_body = None
        self.selected = selected

    def select_set(self, selected):
        self.selected = selected


class FakeObjects(list):
    active = None

    def get(self, name):
        return next((obj for obj in self if obj.name == name), None)


class FakeContext:
    def __init__(self, scene, objects=()):
        self.scene = scene
        self.view_layer = types.SimpleNamespace(objects=FakeObjects(objects))
        self.mode = "OBJECT"
        self.overrides = {}

    @property
    def selected_objects(self):
        return [obj for obj in self.view_layer.objects if obj.selected]

    @property
    def active_object(self):
        return self.view_layer.objects.active

    @contextmanager
    def temp_override(self, **kwargs):
        previous = self.overrides
        self.overrides = {**previous, **kwargs}
        try:
            yield self
        finally:
            self.overrides = previous


class FakeOperator:
    def __init__(self, callback):
        self.callback = callback
        self.available = True

    def poll(self):
        return self.available

    def __call__(self, **kwargs):
        return self.callback(**kwargs)


class FakeSocket:
    def __init__(self, node, name):
        self.node = node
        self.name = name
        self.default_value = 1.0


class FakeSockets(dict):
    def __getitem__(self, name):
        if isinstance(name, int):
            name = "Image"
        if name not in self:
            self[name] = FakeSocket(self.node, name)
        return super().__getitem__(name)


class FakeNode(dict):
    def __init__(self, node_type):
        super().__init__()
        self.bl_idname = node_type
        self.select = False
        self.inputs = FakeSockets()
        self.outputs = FakeSockets()
        self.inputs.node = self.outputs.node = self

    def __eq__(self, other):
        if isinstance(other, FakeNode):
            return self is other
        return NotImplemented

    def __ne__(self, other):
        equal = self.__eq__(other)
        return NotImplemented if equal is NotImplemented else not equal


class FakeLinks(list):
    fail_after = None

    def new(self, output, input_socket):
        if self.fail_after is not None and len(self) >= self.fail_after:
            raise RuntimeError("Synthetic link failure")
        self[:] = [link for link in self if link.to_socket is not input_socket]
        link = types.SimpleNamespace(
            from_node=output.node,
            to_node=input_socket.node,
            from_socket=output,
            to_socket=input_socket,
        )
        self.append(link)
        return link


class FakeNodes(list):
    active = None

    def new(self, type):
        node = FakeNode(type)
        self.append(node)
        self.active = node
        node.select = True
        return node

    def remove(self, node):
        self[:] = [item for item in self if item is not node]
        self.links[:] = [
            link for link in self.links
            if link.from_node is not node and link.to_node is not node
        ]


class FreshRnaWrapper:
    def __init__(self, value):
        object.__setattr__(self, "value", value)

    def __getattr__(self, name):
        value = getattr(self.value, name)
        if isinstance(value, (FakeNode, FakeSocket, FakeSockets)):
            return FreshRnaWrapper(value)
        return value

    def __setattr__(self, name, value):
        setattr(self.value, name, unwrap_rna(value))

    def __getitem__(self, name):
        value = self.value[name]
        return FreshRnaWrapper(value) if isinstance(value, FakeSocket) else value

    def __setitem__(self, name, value):
        self.value[name] = value

    def __eq__(self, other):
        return self.value is unwrap_rna(other)

    def __ne__(self, other):
        return not self.__eq__(other)


def unwrap_rna(value):
    return value.value if isinstance(value, FreshRnaWrapper) else value


class FreshRnaCollection:
    def __init__(self, collection):
        self.collection = collection

    def __iter__(self):
        return (FreshRnaWrapper(value) for value in self.collection)

    def __len__(self):
        return len(self.collection)

    def __getitem__(self, index):
        return FreshRnaWrapper(self.collection[index])

    @property
    def active(self):
        active = self.collection.active
        return FreshRnaWrapper(active) if active is not None else None

    @active.setter
    def active(self, value):
        self.collection.active = unwrap_rna(value)

    def new(self, *args, **kwargs):
        return FreshRnaWrapper(
            self.collection.new(*(unwrap_rna(value) for value in args), **kwargs)
        )

    def remove(self, value):
        self.collection.remove(unwrap_rna(value))


def compositor_fixture():
    links = FakeLinks()
    nodes = FakeNodes()
    nodes.links = links
    tree = types.SimpleNamespace(
        nodes=nodes, links=links, library=None, is_editable=True
    )
    source = nodes.new("CompositorNodeRLayers")
    output = nodes.new("CompositorNodeComposite")
    source.select = True
    links.new(source.outputs["Image"], output.inputs["Image"])
    scene = types.SimpleNamespace(
        use_nodes=True, node_tree=tree, library=None, is_editable=True
    )
    bpy = types.SimpleNamespace(context=FakeContext(scene))
    return bpy, tree, source, output


class BatchDCacheTests(unittest.TestCase):
    def setUp(self):
        self.cache = types.SimpleNamespace(
            frame_start=1, frame_end=250, is_baked=True
        )
        self.other_cache = types.SimpleNamespace(
            frame_start=10, frame_end=80, is_baked=True
        )
        self.scene = types.SimpleNamespace(
            library=None,
            override_library=None,
            is_editable=True,
            rigidbody_world=types.SimpleNamespace(point_cache=self.cache),
        )
        self.context = FakeContext(self.scene)
        self.calls = []
        self.result = {"FINISHED"}

        def free():
            cache = self.context.overrides["point_cache"]
            self.calls.append(("free", cache))
            cache.is_baked = False
            return self.result

        def bake(bake):
            self.assertIs(bake, True)
            cache = self.context.overrides["point_cache"]
            self.calls.append(("bake", cache))
            if self.result == {"FINISHED"}:
                cache.is_baked = True
            return self.result

        self.bpy = types.SimpleNamespace(
            context=self.context,
            ops=types.SimpleNamespace(
                ptcache=types.SimpleNamespace(
                    free_bake=FakeOperator(free), bake=FakeOperator(bake)
                )
            ),
        )
        self.recipe = load_recipe(
            PHYSICS / "references/python_api.md",
            "bake_owned_point_cache",
            self.bpy,
        )

    def bake(self, **kwargs):
        return self.recipe(
            self.scene, self.cache, (self.cache,), 1, 250, **kwargs
        )

    def test_replacement_and_repeat_runs_touch_only_authorized_cache(self):
        for _ in range(2):
            self.bake(replace_cache=True)
        self.assertEqual([call[0] for call in self.calls], ["free", "bake"] * 2)
        self.assertTrue(all(cache is self.cache for _, cache in self.calls))
        self.assertTrue(self.other_cache.is_baked)
        self.assertEqual(self.context.overrides, {})

    def test_existing_bake_requires_explicit_replacement(self):
        with self.assertRaises(ValueError):
            self.bake()
        self.assertEqual(self.calls, [])
        self.assertTrue(self.cache.is_baked)

    def test_unbaked_cache_does_not_call_free(self):
        self.cache.is_baked = False
        self.bake()
        self.assertEqual([call[0] for call in self.calls], ["bake"])

    def test_empty_or_wrong_cache_allowlist_fails_before_mutation(self):
        for allowlist in ((), (self.other_cache,), None):
            with self.subTest(allowlist=allowlist), self.assertRaises(ValueError):
                self.recipe(self.scene, self.cache, allowlist, 1, 250)
        self.assertEqual(self.calls, [])

    def test_wrong_owner_missing_world_and_linked_scene_fail_closed(self):
        for change in (
            {"rigidbody_world": None},
            {"rigidbody_world": types.SimpleNamespace(point_cache=self.other_cache)},
            {"library": object()},
            {"override_library": object()},
            {"is_editable": False},
        ):
            with self.subTest(change=change):
                owner = types.SimpleNamespace(**{**vars(self.scene), **change})
                with self.assertRaises(ValueError):
                    self.recipe(owner, self.cache, (self.cache,), 1, 250)
        self.assertEqual(self.calls, [])

    def test_invalid_frame_ranges_fail_before_free(self):
        for start, end in ((0, 1), (3, 2), (True, 250), (1, None), (1, 2.5)):
            with self.subTest(start=start, end=end), self.assertRaises(ValueError):
                self.recipe(self.scene, self.cache, (self.cache,), start, end)
        self.assertEqual(self.calls, [])

    def test_operator_failure_restores_override_and_does_not_bake(self):
        self.result = {"CANCELLED"}
        with self.assertRaises(RuntimeError):
            self.bake(replace_cache=True)
        self.assertEqual([call[0] for call in self.calls], ["free"])
        self.assertEqual(self.context.overrides, {})
        self.assertTrue(self.other_cache.is_baked)

    def test_poll_failure_leaves_existing_cache_intact(self):
        self.bpy.ops.ptcache.free_bake.available = False
        with self.assertRaises(RuntimeError):
            self.bake(replace_cache=True)
        self.assertEqual(self.calls, [])
        self.assertTrue(self.cache.is_baked)

    def test_object_cache_preserves_selection_and_active_object(self):
        modifier = types.SimpleNamespace(point_cache=self.cache)
        obj = FakeObject("OwnedCloth", [modifier])
        other = FakeObject("UnrelatedMesh", selected=True)
        self.context.view_layer.objects.extend([obj, other])
        self.context.view_layer.objects.active = other
        self.recipe(obj, self.cache, (self.cache,), 1, 250, replace_cache=True)
        self.assertEqual(self.context.selected_objects, [other])
        self.assertIs(self.context.active_object, other)
        self.assertEqual(self.context.overrides, {})

    def test_rigid_body_cache_accepts_fresh_equivalent_rna_wrappers(self):
        for separate_allowlist_wrapper in (False, True):
            with self.subTest(separate_allowlist_wrapper=separate_allowlist_wrapper):
                self.cache.is_baked = False
                supplied = FreshRnaWrapper(self.cache)
                approved = FreshRnaWrapper(self.cache) if separate_allowlist_wrapper else supplied
                self.recipe(self.scene, supplied, (approved,), 1, 40)
                self.assertTrue(self.cache.is_baked)
                self.assertEqual((self.cache.frame_start, self.cache.frame_end), (1, 40))
                self.assertEqual(self.calls[-1], ("bake", supplied))
                self.assertTrue(self.other_cache.is_baked)
                self.assertEqual(self.context.overrides, {})

    def test_object_cache_accepts_equivalent_wrappers_without_accepting_other_data(self):
        modifier = types.SimpleNamespace(point_cache=self.cache)
        owner = FakeObject("OwnedCloth", [modifier])
        self.context.view_layer.objects.append(owner)
        self.cache.is_baked = False
        self.recipe(
            owner, FreshRnaWrapper(self.cache), (FreshRnaWrapper(self.cache),), 1, 40
        )
        self.assertTrue(self.cache.is_baked)
        unrelated = types.SimpleNamespace(**vars(self.cache))
        with self.assertRaises(ValueError):
            self.recipe(
                owner, FreshRnaWrapper(unrelated), (FreshRnaWrapper(self.cache),), 1, 40
            )
        with self.assertRaises(ValueError):
            self.recipe(
                owner, FreshRnaWrapper(unrelated), (FreshRnaWrapper(unrelated),), 1, 40
            )
        self.assertEqual(len(self.calls), 1)
        self.assertEqual(self.context.overrides, {})

    def test_rigid_body_entrypoint_preserves_unrelated_bakes(self):
        self.cache.is_baked = False

        def free_all():
            self.other_cache.is_baked = False
            return {"FINISHED"}

        self.bpy.ops.ptcache.free_bake_all = free_all
        self.bpy.ops.ptcache.bake_all = lambda **kwargs: {"FINISHED"}
        run_section(
            PHYSICS / "SKILL.md", "### Rigid Body Bake", self.bpy,
            {
                "bpy": self.bpy,
                "bake_owned_point_cache": self.recipe,
                "authorized_caches": (self.cache,),
            },
        )
        self.assertTrue(self.other_cache.is_baked)


class BatchDFluidTests(unittest.TestCase):
    def setUp(self):
        self.modifier = types.SimpleNamespace(
            type="FLUID", fluid_type="DOMAIN", domain_settings=types.SimpleNamespace()
        )
        self.domain = FakeObject("OwnedDomain", [self.modifier])
        self.other = FakeObject("UnrelatedDomain", selected=True)
        self.context = FakeContext(types.SimpleNamespace(), [self.domain, self.other])
        self.context.view_layer.objects.active = self.other
        self.calls = []
        self.result = {"FINISHED"}

        def operate():
            self.calls.append(self.context.overrides["object"])
            return self.result

        self.operator = FakeOperator(operate)
        self.bpy = types.SimpleNamespace(
            context=self.context,
            ops=types.SimpleNamespace(
                fluid=types.SimpleNamespace(
                    bake_data=self.operator, free_data=self.operator
                )
            ),
        )
        self.recipe = load_recipe(
            PHYSICS / "references/python_api.md",
            "operate_owned_fluid_cache", self.bpy,
        )

    def operate(self, operation="bake_data", **kwargs):
        return self.recipe(
            self.domain, self.modifier, (self.domain,), operation, **kwargs
        )

    def test_bake_targets_only_owned_domain_and_preserves_context(self):
        self.operate()
        self.assertEqual(self.calls, [self.domain])
        self.assertEqual(self.context.selected_objects, [self.other])
        self.assertIs(self.context.active_object, self.other)
        self.assertEqual(self.context.overrides, {})

    def test_fluid_modifier_accepts_fresh_wrapper_but_rejects_identical_other_data(self):
        self.recipe(
            self.domain, FreshRnaWrapper(self.modifier), (self.domain,), "bake_data"
        )
        unrelated = types.SimpleNamespace(**vars(self.modifier))
        with self.assertRaises(ValueError):
            self.recipe(
                self.domain, FreshRnaWrapper(unrelated), (self.domain,), "bake_data"
            )
        self.assertEqual(self.calls, [self.domain])
        self.assertEqual(self.context.selected_objects, [self.other])
        self.assertIs(self.context.active_object, self.other)
        self.assertEqual(self.context.overrides, {})

    def test_free_requires_explicit_replacement_authorization(self):
        with self.assertRaises(ValueError):
            self.operate("free_data")
        self.assertEqual(self.calls, [])
        self.operate("free_data", replace_cache=True)
        self.assertEqual(self.calls, [self.domain])

    def test_unknown_domain_modifier_and_operation_fail_before_mutation(self):
        for domain, modifier, allowlist, operation in (
            (None, self.modifier, (), "bake_data"),
            (self.domain, self.modifier, (), "bake_data"),
            (self.domain, self.modifier, (self.other,), "bake_data"),
            (self.domain, None, (self.domain,), "bake_data"),
            (self.domain, self.modifier, (self.domain,), "free_all"),
        ):
            with (
                self.subTest(operation=operation, allowlist=allowlist),
                self.assertRaises(ValueError),
            ):
                self.recipe(domain, modifier, allowlist, operation)
        self.assertEqual(self.calls, [])

    def test_linked_and_non_domain_targets_fail_closed(self):
        self.domain.library = object()
        with self.assertRaises(ValueError):
            self.operate()
        self.domain.library = None
        self.modifier.fluid_type = "FLOW"
        with self.assertRaises(ValueError):
            self.operate()
        self.assertEqual(self.calls, [])

    def test_cancelled_operator_restores_context_and_reports_failure(self):
        self.result = {"CANCELLED"}
        with self.assertRaisesRegex(RuntimeError, "bake_data"):
            self.operate()
        self.assertEqual(self.context.overrides, {})
        self.assertEqual(self.context.selected_objects, [self.other])
        self.assertIs(self.context.active_object, self.other)


class BatchDCompositorTests(unittest.TestCase):
    def setUp(self):
        self.bpy, self.tree, self.source, self.output = compositor_fixture()
        self.recipe = load_recipe(
            COMPOSITOR / "references/python_api.md",
            "build_owned_color_grade",
            self.bpy,
        )

    def test_owned_branch_preserves_unrelated_graph_and_repeat_run(self):
        original_link = self.tree.links[0]
        original_active = self.tree.nodes.active
        first = self.recipe(self.tree, "approved-branch")
        second = self.recipe(self.tree, "approved-branch")
        self.assertIs(first, second)
        self.assertEqual(len(self.tree.nodes), 6)
        self.assertEqual(len(self.tree.links), 6)
        self.assertIs(self.tree.links[0], original_link)
        self.assertIs(self.tree.nodes.active, original_active)
        self.assertTrue(self.source.select)
        self.assertTrue(self.output.select)
        self.assertFalse(first.select)

    def test_empty_owner_and_linked_tree_fail_before_changes(self):
        for owner in ("", " ", None):
            with self.subTest(owner=owner), self.assertRaises(ValueError):
                self.recipe(self.tree, owner)
        self.tree.library = object()
        with self.assertRaises(ValueError):
            self.recipe(self.tree, "approved-branch")
        self.assertEqual(len(self.tree.nodes), 2)

    def test_failure_removes_only_new_owned_nodes_and_links(self):
        original_link = self.tree.links[0]
        self.tree.links.fail_after = 2
        with self.assertRaises(RuntimeError):
            self.recipe(self.tree, "approved-branch")
        self.assertEqual(len(self.tree.nodes), 2)
        self.assertEqual(self.tree.links, [original_link])
        self.assertIs(self.tree.nodes.active, self.output)

    def test_foreign_link_to_owned_branch_is_not_rewired(self):
        self.recipe(self.tree, "approved-branch")
        denoise = next(
            node for node in self.tree.nodes
            if node.bl_idname == "CompositorNodeDenoise"
        )
        foreign_link = self.tree.links.new(
            self.source.outputs["Image"], denoise.inputs["Image"]
        )
        before = list(self.tree.links)
        with self.assertRaises(ValueError):
            self.recipe(self.tree, "approved-branch")
        self.assertEqual(self.tree.links, before)
        self.assertTrue(any(link is foreign_link for link in self.tree.links))

    def test_duplicate_owned_roles_fail_before_any_changes(self):
        self.recipe(self.tree, "approved-branch")
        duplicate = self.tree.nodes.new("CompositorNodeDenoise")
        duplicate["local_overlay_owner"] = "approved-branch"
        duplicate["local_overlay_role"] = "denoise"
        before = list(self.tree.links)
        with self.assertRaises(ValueError):
            self.recipe(self.tree, "approved-branch")
        self.assertEqual(self.tree.links, before)
        self.assertEqual(len(self.tree.nodes), 7)

    def test_full_pipeline_does_not_delete_or_replace_existing_output(self):
        original_link = self.tree.links[0]
        run_section(
            COMPOSITOR / "references/python_api.md",
            "### Full Denoise + Color Grade Pipeline", self.bpy,
            {
                "build_owned_color_grade": self.recipe,
                "approved_branch_key": "approved-branch",
            },
        )
        self.assertTrue(any(node is self.source for node in self.tree.nodes))
        self.assertTrue(any(node is self.output for node in self.tree.nodes))
        self.assertTrue(any(link is original_link for link in self.tree.links))


class BatchDFreshRnaCompositorTests(unittest.TestCase):
    def setUp(self):
        self.bpy, self.tree, self.source, self.output = compositor_fixture()
        self.tree.nodes = FreshRnaCollection(self.tree.nodes)
        self.tree.links = FreshRnaCollection(self.tree.links)
        self.recipe = load_recipe(
            COMPOSITOR / "references/python_api.md",
            "build_owned_color_grade", self.bpy,
        )

    def node(self, role):
        return next(
            node for node in self.tree.nodes
            if node.get("local_overlay_role") == role
        )

    def test_fixture_models_fresh_wrappers_with_shared_native_identity(self):
        first = self.tree.nodes[0]
        second = self.tree.nodes[0]
        self.assertIsNot(first, second)
        self.assertEqual(first, second)
        self.assertNotEqual(first, self.tree.nodes[1])
        self.assertIsNot(first.outputs["Image"], second.outputs["Image"])
        self.assertEqual(first.outputs["Image"], second.outputs["Image"])
        self.assertEqual(self.tree.links[0].from_node, first)
        self.assertIsNot(self.tree.links[0].from_node, first)

    def test_rerun_preserves_existing_links_selection_and_active_node(self):
        first = self.recipe(self.tree, "approved-branch")
        before = list(self.tree.links)
        second = self.recipe(self.tree, "approved-branch")
        self.assertEqual(first, second)
        self.assertEqual(list(self.tree.links), before)
        self.assertEqual(len(self.tree.nodes), 6)
        self.assertEqual(len(self.tree.links), 6)
        self.assertTrue(self.source.select)
        self.assertTrue(self.output.select)
        self.assertFalse(first.select)
        self.assertEqual(self.tree.nodes.active, self.output)

    def test_foreign_incoming_link_is_rejected_without_replacement(self):
        self.recipe(self.tree, "approved-branch")
        foreign = self.tree.links.new(
            FreshRnaWrapper(self.source).outputs["Image"],
            self.node("denoise").inputs["Image"],
        )
        before = list(self.tree.links)
        with self.assertRaises(ValueError):
            self.recipe(self.tree, "approved-branch")
        self.assertEqual(list(self.tree.links), before)
        self.assertIn(foreign, self.tree.links)
        self.assertEqual(self.tree.nodes.active, self.output)

    def test_foreign_outgoing_link_is_rejected_without_routing_changes(self):
        self.recipe(self.tree, "approved-branch")
        self.tree.links.new(
            self.node("saturation").outputs["Image"],
            FreshRnaWrapper(self.output).inputs["Image"],
        )
        before = list(self.tree.links)
        with self.assertRaises(ValueError):
            self.recipe(self.tree, "approved-branch")
        self.assertEqual(list(self.tree.links), before)

    def test_conflicting_owned_input_is_rejected_without_replacement(self):
        self.recipe(self.tree, "approved-branch")
        self.tree.links.new(
            self.node("saturation").outputs["Image"],
            self.node("denoise").inputs["Image"],
        )
        before = list(self.tree.links)
        with self.assertRaises(ValueError):
            self.recipe(self.tree, "approved-branch")
        self.assertEqual(list(self.tree.links), before)


class BatchDModifierTests(unittest.TestCase):
    def setUp(self):
        self.first = types.SimpleNamespace(name="ApprovedBevel")
        self.second = types.SimpleNamespace(name="ApprovedSubdivision")
        self.keep = types.SimpleNamespace(name="UnapprovedCloth")
        self.owned = FakeObject("OwnedMesh", [self.first, self.second, self.keep])
        self.other = FakeObject(
            "UnrelatedMesh", [types.SimpleNamespace(name="KeepBevel")], True
        )
        self.context = FakeContext(types.SimpleNamespace(), [self.owned, self.other])
        self.context.view_layer.objects.active = self.other
        self.calls = []
        self.fail_on = None

        def apply(modifier):
            obj = self.context.overrides["object"]
            self.calls.append((obj.name, modifier))
            if modifier == self.fail_on:
                return {"CANCELLED"}
            obj.modifiers[:] = [
                item for item in obj.modifiers if item.name != modifier
            ]
            return {"FINISHED"}

        self.bpy = types.SimpleNamespace(
            context=self.context,
            ops=types.SimpleNamespace(
                object=types.SimpleNamespace(modifier_apply=FakeOperator(apply))
            ),
        )
        self.recipe = load_recipe(
            SCRIPTING / "SKILL.md", "apply_owned_modifiers", self.bpy
        )

    def run_batch(self):
        return self.recipe(
            [(self.owned, ("ApprovedBevel", "ApprovedSubdivision"))]
        )

    def test_applies_exact_modifier_allowlist_without_iteration_skips(self):
        self.run_batch()
        self.assertEqual(
            self.calls,
            [("OwnedMesh", "ApprovedBevel"), ("OwnedMesh", "ApprovedSubdivision")],
        )
        self.assertEqual(self.owned.modifiers, [self.keep])
        self.assertEqual(len(self.other.modifiers), 1)
        self.assertEqual(self.context.selected_objects, [self.other])
        self.assertIs(self.context.active_object, self.other)
        self.assertEqual(self.context.overrides, {})

    def test_repeat_run_with_stale_modifier_names_fails_without_more_mutation(self):
        self.run_batch()
        with self.assertRaises(ValueError):
            self.run_batch()
        self.assertEqual(len(self.calls), 2)

    def test_empty_missing_or_unknown_targets_fail_before_mutation(self):
        for targets in (
            None, [], [(None, ("Bevel",))], [(self.owned, ())],
            [(self.owned, ("MissingModifier",))],
            [(FakeObject("MissingObject"), ("Bevel",))],
        ):
            with self.subTest(targets=targets), self.assertRaises(ValueError):
                self.recipe(targets)
        self.assertEqual(self.calls, [])

    def test_linked_overridden_shared_and_non_mesh_data_fail_closed(self):
        for target, field, value in (
            (self.owned, "library", object()),
            (self.owned, "override_library", object()),
            (self.owned.data, "library", object()),
            (self.owned.data, "users", 2),
            (self.owned, "type", "CURVE"),
            (self.owned, "mode", "EDIT"),
        ):
            with self.subTest(field=field):
                previous = getattr(target, field)
                setattr(target, field, value)
                with self.assertRaises(ValueError):
                    self.run_batch()
                setattr(target, field, previous)
        self.assertEqual(self.calls, [])

    def test_invalid_later_target_prevents_partial_batch(self):
        self.other.library = object()
        with self.assertRaises(ValueError):
            self.recipe([
                (self.owned, ("ApprovedBevel",)),
                (self.other, ("KeepBevel",)),
            ])
        self.assertEqual(self.calls, [])

    def test_cancelled_operator_reports_partial_work_and_restores_state(self):
        self.fail_on = "ApprovedSubdivision"
        with self.assertRaisesRegex(RuntimeError, "ApprovedSubdivision"):
            self.run_batch()
        self.assertEqual(self.owned.modifiers, [self.second, self.keep])
        self.assertEqual(self.context.selected_objects, [self.other])
        self.assertIs(self.context.active_object, self.other)
        self.assertEqual(self.context.overrides, {})

    def test_raised_operator_reports_completed_modifiers_and_restores_override(self):
        original = self.bpy.ops.object.modifier_apply.callback

        def raise_on_second(modifier):
            if modifier == "ApprovedSubdivision":
                raise RuntimeError("Synthetic operator exception")
            return original(modifier)

        self.bpy.ops.object.modifier_apply.callback = raise_on_second
        with self.assertRaisesRegex(RuntimeError, "ApprovedBevel"):
            self.run_batch()
        self.assertEqual(self.context.overrides, {})
        self.assertEqual(self.owned.modifiers, [self.second, self.keep])

    def test_unavailable_operator_leaves_batch_untouched(self):
        self.bpy.ops.object.modifier_apply.available = False
        with self.assertRaises(RuntimeError):
            self.run_batch()
        self.assertEqual(self.calls, [])


class BatchDAvatarTests(unittest.TestCase):
    def setUp(self):
        self.recipe = load_recipe(
            AVATAR / "references/likeness-and-inputs.md", "avatar_reference_binding"
        )
        self.consent = {"identity": "fictional-presenter", "face": True, "voice": True}
        self.asset = {
            "identity": "fictional-presenter",
            "kind": "real-person",
            "status": "Active",
            "uri": "asset://fixture-face",
            "account_operation_verified": True,
        }
        self.provider = {"face": self.asset, "voice": {**self.asset, "uri": "asset://fixture-voice"}}

    def bind(self, **kwargs):
        return self.recipe(
            "fictional-presenter", self.consent, self.provider, **kwargs
        )

    def test_verified_face_and_voice_assets_produce_only_asset_bindings(self):
        self.assertEqual(
            self.bind(require_voice=True),
            {"face": "asset://fixture-face", "voice": "asset://fixture-voice"},
        )
        self.assertEqual(self.bind(), {"face": "asset://fixture-face"})

    def test_consent_and_policy_approval_do_not_replace_provider_authorization(self):
        for consent in (None, self.consent):
            for provider in (None, {}, {"face": None}):
                with (
                    self.subTest(consent=consent, provider=provider),
                    self.assertRaises(ValueError),
                ):
                    self.recipe(
                        "fictional-presenter", consent, provider,
                        policy_approved=True,
                    )

    def test_provider_asset_does_not_replace_consent_or_required_policy(self):
        for consent in (None, {}, {**self.consent, "face": False}):
            with self.subTest(consent=consent), self.assertRaises(ValueError):
                self.recipe("fictional-presenter", consent, self.provider)
        with self.assertRaises(ValueError):
            self.bind(policy_required=True)
        self.assertEqual(
            self.bind(policy_required=True, policy_approved=True),
            {"face": "asset://fixture-face"},
        )

    def test_inactive_wrong_identity_raw_url_and_unknown_scope_are_rejected(self):
        for change in (
            {"status": "Pending"}, {"status": "Disabled"}, {"status": None},
            {"identity": "different-person"}, {"kind": "virtual-portrait"},
            {"uri": "https://example.invalid/sheet.png"}, {"uri": "asset://"},
            {"account_operation_verified": False},
        ):
            with self.subTest(change=change), self.assertRaises(ValueError):
                self.recipe(
                    "fictional-presenter", self.consent,
                    {"face": {**self.asset, **change}},
                )

    def test_voice_requires_its_own_consent_and_active_provider_asset(self):
        for consent, provider in (
            ({**self.consent, "voice": False}, self.provider),
            (self.consent, {"face": self.asset}),
            (self.consent, {**self.provider, "voice": {**self.asset, "status": "Pending"}}),
        ):
            with (
                self.subTest(consent=consent, provider=provider),
                self.assertRaises(ValueError),
            ):
                self.recipe(
                    "fictional-presenter", consent, provider, require_voice=True
                )

    def test_non_boolean_gate_flags_are_rejected(self):
        for kwargs in (
            {"require_voice": "false"}, {"policy_required": "false"},
            {"policy_approved": 1},
        ):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                self.bind(**kwargs)


class BatchDInstructionTests(unittest.TestCase):
    def test_metadata_and_canonical_aliases_remain_valid(self):
        for skill in (PHYSICS, COMPOSITOR, SCRIPTING, AVATAR):
            with self.subTest(skill=skill):
                frontmatter = (skill / "SKILL.md").read_text().split("---", 2)[1]
                metadata = YAML(typ="safe").load(frontmatter)
                self.assertEqual(metadata["name"], skill.name)
                self.assertIsInstance(metadata["description"], str)
                alias = ROOT / ".claude/skills" / skill.name
                self.assertTrue(alias.is_symlink())
                self.assertEqual(alias.resolve(), skill.resolve())

    def test_owned_markdown_file_links_resolve(self):
        paths = (
            PHYSICS / "SKILL.md", PHYSICS / "references/python_api.md",
            COMPOSITOR / "SKILL.md", COMPOSITOR / "references/python_api.md",
            SCRIPTING / "SKILL.md", AVATAR / "SKILL.md",
            AVATAR / "references/likeness-and-inputs.md",
            AVATAR / "references/seedance-talking-head.md",
        )
        for path in paths:
            for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", path.read_text()):
                if "://" in target or target.startswith("#"):
                    continue
                with self.subTest(path=path, target=target):
                    self.assertTrue((path.parent / target.split("#", 1)[0]).is_file())

    def test_no_scene_wide_point_cache_calls_or_compositor_clear_remain(self):
        for path in (PHYSICS / "SKILL.md", PHYSICS / "references/python_api.md"):
            with self.subTest(path=path):
                self.assertNotRegex(
                    path.read_text(), r"bpy\.ops\.ptcache\.(?:free_bake_all|bake_all)\("
                )
        self.assertNotIn(
            "nodes.clear()", (COMPOSITOR / "references/python_api.md").read_text()
        )

    def test_local_overlay_notes_preserve_vendored_provenance(self):
        for path in (
            COMPOSITOR / "SKILL.md", COMPOSITOR / "references/python_api.md",
            PHYSICS / "SKILL.md", PHYSICS / "references/python_api.md",
            SCRIPTING / "SKILL.md",
        ):
            with self.subTest(path=path):
                self.assertIn("Local safety overlay", path.read_text())

    def test_all_avatar_instructions_remove_policy_or_sheet_bypass(self):
        forbidden = re.compile(
            r"route or a named policy|route or a policy"
            r"|or the character sheet as `reference_image`"
            r"|often rejected.*?prefer the `asset://`",
            re.DOTALL,
        )
        for path in (
            AVATAR / "SKILL.md", AVATAR / "references/likeness-and-inputs.md",
            AVATAR / "references/seedance-talking-head.md",
        ):
            with self.subTest(path=path):
                self.assertIsNone(forbidden.search(path.read_text()))

    def test_all_owned_python_snippets_compile_without_execution(self):
        for path in (
            PHYSICS / "SKILL.md", PHYSICS / "references/python_api.md",
            COMPOSITOR / "SKILL.md", COMPOSITOR / "references/python_api.md",
            SCRIPTING / "SKILL.md", AVATAR / "references/likeness-and-inputs.md",
        ):
            for source in python_blocks(path):
                with self.subTest(path=path, source=source[:80]):
                    compile(source, str(path), "exec")


if __name__ == "__main__":
    unittest.main()
