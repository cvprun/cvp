# -*- coding: utf-8 -*-

from datetime import time
from typing import NamedTuple, Union

from imgui_bundle import imgui

from cvp.imgui.drag_int import drag_int
from cvp.imgui.flags.slider import SliderFlags
from cvp.variables import IMGUI_INPUT_TIME_SEPARATOR


class InputTimeResult(NamedTuple):
    changed: bool
    value: time

    @classmethod
    def from_raw(cls, result):
        assert isinstance(result, tuple)
        assert len(result) == 2
        changed = result[0]
        value = result[1]
        assert isinstance(changed, bool)
        assert isinstance(value, time)
        return cls(changed, value)

    def __bool__(self):
        return self.changed


def calc_drag_time_field_width(separator=IMGUI_INPUT_TIME_SEPARATOR):
    item_width = imgui.calc_item_width()
    field_count = 3  # hour, minute, second

    inner_spacing = max(0.0, imgui.get_style().item_inner_spacing.x)
    separator_width = imgui.calc_text_size(separator).x + inner_spacing
    separator_count = 2
    separator_total_width = separator_width * separator_count

    return (item_width - separator_total_width) / field_count


def drag_time(
    label: str,
    value: time,
    flags: Union[SliderFlags, int] = 0,
    separator=IMGUI_INPUT_TIME_SEPARATOR,
    hour_format="%02d",
    minute_format="%02d",
    second_format="%02d",
    small_field_width=False,
    raise_errors=False,
):
    if isinstance(flags, SliderFlags):
        flags = int(flags)
    assert isinstance(flags, int)

    inner_spacing = max(0.0, imgui.get_style().item_inner_spacing.x)
    half_inner_spacing = inner_spacing * 0.5
    double_inner_spacing = inner_spacing * 2.0

    if small_field_width:
        hour_text_width = imgui.calc_text_size("00").x + double_inner_spacing
        minute_text_width = imgui.calc_text_size("00").x + double_inner_spacing
        second_text_width = imgui.calc_text_size("00").x + double_inner_spacing
    else:
        field_width = calc_drag_time_field_width(separator)
        hour_text_width = field_width
        minute_text_width = field_width
        second_text_width = field_width
        del field_width

    imgui.push_id(label)
    try:
        imgui.set_next_item_width(hour_text_width)
        hour = drag_int(
            label="##Time.Hour",
            value=value.hour,
            min_value=0,
            max_value=23,
            fmt=hour_format,
            flags=flags,
        )

        imgui.same_line(spacing=half_inner_spacing)
        imgui.text(separator)
        imgui.same_line(spacing=half_inner_spacing)

        imgui.set_next_item_width(minute_text_width)
        minute = drag_int(
            label="##Time.Minute",
            value=value.minute,
            min_value=0,
            max_value=59,
            fmt=minute_format,
            flags=flags,
        )

        imgui.same_line(spacing=half_inner_spacing)
        imgui.text(separator)
        imgui.same_line(spacing=half_inner_spacing)

        imgui.set_next_item_width(second_text_width)
        second = drag_int(
            label="##Time.Second",
            value=value.second,
            min_value=0,
            max_value=59,
            fmt=second_format,
            flags=flags,
        )

        if display_text := label.split("##", maxsplit=1)[0]:
            imgui.same_line(spacing=inner_spacing)
            imgui.text(display_text)
    finally:
        imgui.pop_id()

    changed = any((hour[0], minute[0], second[0]))
    if changed:
        try:
            assert 0 <= hour[1] <= 23
            assert 0 <= minute[1] <= 59
            assert 0 <= second[1] <= 59
            value = time(hour[1], minute[1], second[1])
        except ValueError:
            if raise_errors:
                raise

    return InputTimeResult.from_raw((changed, value))
