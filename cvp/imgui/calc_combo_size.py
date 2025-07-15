# -*- coding: utf-8 -*-

from typing import Sequence, Union

from imgui_bundle import imgui

from cvp.imgui.flags.combo import NO_ARROW_BUTTON, NO_PREVIEW, ComboFlags


def get_arrow_size(flags: Union[ComboFlags, int] = 0) -> float:
    return 0.0 if flags & NO_ARROW_BUTTON else imgui.get_frame_height()


def calc_max_combo_size(
    label: str,
    items: Sequence[str],
    flags: Union[ComboFlags, int] = 0,
) -> imgui.ImVec2:
    label_size = imgui.calc_text_size(label, None, True)
    items_max_width = max((imgui.calc_text_size(i, None, True).x for i in items))
    arrow_size = get_arrow_size(flags)

    frame_padding = imgui.get_style().frame_padding
    padding_x = 0.0 if flags & NO_PREVIEW else frame_padding.x * 2
    padding_y = frame_padding.y * 2

    width = arrow_size + items_max_width + padding_x
    height = label_size.y + padding_y

    return imgui.ImVec2(width, height)
