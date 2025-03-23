# -*- coding: utf-8 -*-

from imgui_bundle import imgui

from cvp.types.shapes import Rect


def measure_window_roi(
    content_width: float,
    content_height: float,
    viewport_pos_x: float,
    viewport_pos_y: float,
    viewport_size_width: float,
    viewport_size_height: float,
    pivot_x=0.0,
    pivot_y=0.0,
    anchor_x=0.0,
    anchor_y=0.0,
    margin_x=0.0,
    margin_y=0.0,
    padding_x=0.0,
    padding_y=0.0,
) -> Rect:
    canvas_pos_x = viewport_pos_x + margin_x
    canvas_pos_y = viewport_pos_y + margin_y
    canvas_size_x = viewport_size_width - margin_x * 2
    canvas_size_y = viewport_size_height - margin_y * 2

    window_size_x = content_width + padding_x * 2
    window_size_y = content_height + padding_y * 2

    x1 = canvas_pos_x + (canvas_size_x * anchor_x) - (window_size_x * pivot_x)
    y1 = canvas_pos_y + (canvas_size_y * anchor_y) - (window_size_y * pivot_y)
    x2 = x1 + window_size_x
    y2 = y1 + window_size_y

    return x1, y1, x2, y2


def get_window_roi(
    content_width: float,
    content_height: float,
    pivot_x=0.0,
    pivot_y=0.0,
    anchor_x=0.0,
    anchor_y=0.0,
    margin_x=0.0,
    margin_y=0.0,
    padding_x=0.0,
    padding_y=0.0,
) -> Rect:
    viewport = imgui.get_main_viewport()
    work_pos = viewport.work_pos  # Use work area to avoid menu-bar/task-bar, if any
    work_size = viewport.work_size
    work_pos_x = work_pos.x
    work_pos_y = work_pos.y
    work_size_x = work_size.x
    work_size_y = work_size.y
    assert isinstance(work_pos_x, float)
    assert isinstance(work_pos_y, float)
    assert isinstance(work_size_x, float)
    assert isinstance(work_size_y, float)
    return measure_window_roi(
        content_width=content_width,
        content_height=content_height,
        viewport_pos_x=work_pos_x,
        viewport_pos_y=work_pos_y,
        viewport_size_width=work_size_x,
        viewport_size_height=work_size_y,
        pivot_x=pivot_x,
        pivot_y=pivot_y,
        anchor_x=anchor_x,
        anchor_y=anchor_y,
        margin_x=margin_x,
        margin_y=margin_y,
        padding_x=padding_x,
        padding_y=padding_y,
    )
