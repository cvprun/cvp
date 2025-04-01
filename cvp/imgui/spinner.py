# -*- coding: utf-8 -*-

from typing import Optional

from imgui_bundle import imgui, imspinner


def spinner(
    label: str,
    radius: Optional[float] = None,
    thickness=2.0,
    color: Optional[imgui.ImColor] = None,
    speed=2.8,
    arcs=2,
    mode=0,
) -> None:
    imspinner.spinner_arc_rotation(
        label=label,
        radius=radius if radius is not None else imgui.get_font_size() / 2.0,
        thickness=thickness,
        color=color,
        speed=speed,
        arcs=arcs,
        mode=mode,
    )
