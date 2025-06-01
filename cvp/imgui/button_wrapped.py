# -*- coding: utf-8 -*-

from typing import Optional, Sequence

from imgui_bundle import imgui

from cvp.imgui.calc_button_size import calc_button_size
from cvp.types.colors import GREEN_RGBA, RED_RGBA, YELLOW_RGBA


def button_wrapped(
    labels: Sequence[str],
    outer_width: Optional[float] = None,
    *,
    show_debugging=False,
) -> Optional[int]:
    if not labels:
        return None

    if outer_width is None:
        outer_width = imgui.get_content_region_avail().x
    assert isinstance(outer_width, float)

    item_spacing = imgui.get_style().item_spacing

    clicked_index: Optional[int] = None

    next_color = imgui.color_convert_float4_to_u32(RED_RGBA)
    error_color = imgui.color_convert_float4_to_u32(YELLOW_RGBA)
    outer_color = imgui.color_convert_float4_to_u32(GREEN_RGBA)

    draw_list = imgui.get_window_draw_list()
    cursor_pos = imgui.get_cursor_screen_pos()
    cx = cursor_pos.x
    cy = cursor_pos.y

    max_right_x = cx + outer_width
    p1 = cx, cy
    p2 = max_right_x, cy

    if show_debugging:
        draw_list.add_line(p1, p2, outer_color)

    label = labels[0]
    button_size = calc_button_size(label)

    if show_debugging:
        p1 = cx, cy
        p2 = p1[0] + button_size.x, p1[1] + button_size.y
        draw_list.add_rect(p1, p2, next_color)

    if imgui.button(label):
        clicked_index = 0

    line_max_height = button_size.y
    cursor_x = calc_button_size(label).x + item_spacing.x
    cursor_y = 0.0

    for i, label in enumerate(labels[1:], 1):
        button_size = calc_button_size(label)
        line_max_height = max(line_max_height, button_size.y)

        p1 = cx + cursor_x, cy + cursor_y
        p2 = p1[0] + button_size.x, p1[1] + button_size.y
        use_same_line = p2[0] <= max_right_x

        if use_same_line:
            imgui.same_line()

            if show_debugging:
                draw_list.add_rect(p1, p2, next_color)
        else:
            if show_debugging:
                draw_list.add_rect(p1, p2, error_color)

            cursor_x = 0.0
            cursor_y += line_max_height + item_spacing.y

            if show_debugging:
                p1 = cx + cursor_x, cy + cursor_y
                p2 = p1[0] + button_size.x, p1[1] + button_size.y
                draw_list.add_rect(p1, p2, next_color)

        if imgui.button(label):
            clicked_index = i

        cursor_x += button_size.x + item_spacing.x

    return clicked_index
