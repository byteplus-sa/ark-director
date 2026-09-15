from __future__ import annotations

import importlib
import json
import sys
from typing import Any


def render_engine_identifiers(bpy_module: Any) -> list[str]:
    properties = bpy_module.types.RenderSettings.bl_rna.properties
    engine_property = properties.get("engine")
    if engine_property is None:
        return []
    items = getattr(engine_property, "enum_items_static", None)
    if items is None:
        items = getattr(engine_property, "enum_items", [])
    return [
        item.identifier
        for item in items
        if isinstance(getattr(item, "identifier", None), str)
    ]


def choose_eevee_engine(available_engines: list[str]) -> str | None:
    for candidate in ("BLENDER_EEVEE_NEXT", "BLENDER_EEVEE"):
        if candidate in available_engines:
            return candidate
    return None


def collect_runtime(bpy_module: Any, *, python_version: str) -> dict[str, Any]:
    scene = bpy_module.context.scene
    render = scene.render
    engines = render_engine_identifiers(bpy_module)
    effective_fps = render.fps / render.fps_base
    return {
        "blender_version": list(bpy_module.app.version),
        "blender_version_string": bpy_module.app.version_string,
        "python_version": python_version,
        "scene_name": scene.name,
        "current_render_engine": render.engine,
        "available_render_engines": engines,
        "recommended_eevee_engine": choose_eevee_engine(engines),
        "resolution": [
            render.resolution_x,
            render.resolution_y,
            render.resolution_percentage,
        ],
        "fps": render.fps,
        "fps_base": render.fps_base,
        "effective_fps": effective_fps,
        "frame_range": [scene.frame_start, scene.frame_end],
    }


def main() -> int:
    bpy = importlib.import_module("bpy")

    print(
        json.dumps(
            collect_runtime(bpy, python_version=sys.version.split()[0]),
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
