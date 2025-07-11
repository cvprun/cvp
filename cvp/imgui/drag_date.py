# -*- coding: utf-8 -*-

from datetime import date
from typing import NamedTuple, Union

from imgui_bundle import imgui

from cvp.imgui.drag_int import drag_int
from cvp.imgui.flags.slider import SliderFlags
from cvp.variables import IMGUI_INPUT_DATE_SEPARATOR


class InputDateResult(NamedTuple):
    changed: bool
    value: date

    @classmethod
    def from_raw(cls, result):
        assert isinstance(result, tuple)
        assert len(result) == 2
        changed = result[0]
        value = result[1]
        assert isinstance(changed, bool)
        assert isinstance(value, date)
        return cls(changed, value)

    def __bool__(self):
        return self.changed


def calc_input_date_field_width(separator=IMGUI_INPUT_DATE_SEPARATOR):
    item_width = imgui.calc_item_width()
    field_count = 3  # year, month, day

    inner_spacing = max(0.0, imgui.get_style().item_inner_spacing.x)
    separator_width = imgui.calc_text_size(separator).x + inner_spacing
    separator_count = 2
    separator_total_width = separator_width * separator_count

    return (item_width - separator_total_width) / field_count


def drag_date(
    label: str,
    value: date,
    flags: Union[SliderFlags, int] = 0,
    separator=IMGUI_INPUT_DATE_SEPARATOR,
    year_format="%04d",
    month_format="%02d",
    day_format="%02d",
    small_input_width=False,
    raise_errors=False,
):
    if isinstance(flags, SliderFlags):
        flags = int(flags)
    assert isinstance(flags, int)

    inner_spacing = max(0.0, imgui.get_style().item_inner_spacing.x)
    half_inner_spacing = inner_spacing * 0.5
    double_inner_spacing = inner_spacing * 2.0

    if small_input_width:
        year_text_width = imgui.calc_text_size("0000").x + double_inner_spacing
        month_text_width = imgui.calc_text_size("00").x + double_inner_spacing
        day_text_width = imgui.calc_text_size("00").x + double_inner_spacing
    else:
        field_width = calc_input_date_field_width(separator)
        year_text_width = field_width
        month_text_width = field_width
        day_text_width = field_width
        del field_width

    imgui.push_id(label)
    try:
        imgui.set_next_item_width(year_text_width)
        year = drag_int(
            label="##Date.Year",
            value=value.year,
            min_value=1,
            max_value=9999,
            fmt=year_format,
            flags=flags,
        )

        imgui.same_line(spacing=half_inner_spacing)
        imgui.text(separator)
        imgui.same_line(spacing=half_inner_spacing)

        imgui.set_next_item_width(month_text_width)
        month = drag_int(
            label="##Date.Month",
            value=value.month,
            min_value=1,
            max_value=12,
            fmt=month_format,
            flags=flags,
        )

        imgui.same_line(spacing=half_inner_spacing)
        imgui.text(separator)
        imgui.same_line(spacing=half_inner_spacing)

        imgui.set_next_item_width(day_text_width)
        day = drag_int(
            label="##Date.Day",
            value=value.day,
            min_value=1,
            max_value=31,
            fmt=day_format,
            flags=flags,
        )

        if display_text := label.split("##", maxsplit=1)[0]:
            imgui.same_line(spacing=inner_spacing)
            imgui.text(display_text)
    finally:
        imgui.pop_id()

    changed = any((year[0], month[0], day[0]))
    if changed:
        try:
            assert 1 <= year[1] <= 9999
            assert 1 <= month[1] <= 12
            assert 1 <= day[1] <= 31
            value = date(year[1], month[1], day[1])
        except ValueError:
            if raise_errors:
                raise

    return InputDateResult.from_raw((changed, value))
