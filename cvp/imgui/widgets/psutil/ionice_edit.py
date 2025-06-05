# -*- coding: utf-8 -*-

from typing import NamedTuple, Optional

import psutil
from imgui_bundle import imgui

from cvp.assets.fonts import mdi
from cvp.imgui.begin_child import begin_child_context
from cvp.imgui.button import button
from cvp.imgui.flags.child import AUTO_RESIZE_Y, BORDERS
from cvp.imgui.radio_button import radio_button
from cvp.imgui.slider_int import slider_int
from cvp.values.temp import TempValue


class IoniceEditResult(NamedTuple):
    changed: bool
    ioclass: int
    level: Optional[int]

    @classmethod
    def from_raw(cls, result):
        assert isinstance(result, tuple)
        assert len(result) == 3
        changed = result[0]
        ioclass = result[1]
        level = result[2]
        assert isinstance(changed, bool)
        assert isinstance(ioclass, int)
        assert isinstance(level, (type(None), int))
        return cls(changed, ioclass, level)

    def __bool__(self):
        return self.changed


def ionice_edit(
    label: str,
    ionice_class: TempValue[int],
    ionice_level: TempValue[int],
    width: Optional[float] = None,
    *,
    top_title: Optional[str] = None,
    right_title: Optional[str] = None,
    border=False,
    no_commit=False,
) -> IoniceEditResult:
    if width is None:
        width = imgui.calc_item_width()
    assert isinstance(width, float)

    with begin_child_context(
        label=label,
        size=(width, 0),
        child_flags=AUTO_RESIZE_Y | (BORDERS if border else 0),
    ):
        if top_title:
            imgui.text(top_title)
            imgui.separator()

        if psutil.WINDOWS:
            if radio_button("High", ionice_class.temp == psutil.IOPRIO_HIGH):
                ionice_class.temp = psutil.IOPRIO_HIGH
                ionice_level.temp = 0
            if radio_button("Normal", ionice_class.temp == psutil.IOPRIO_NORMAL):
                ionice_class.temp = psutil.IOPRIO_NORMAL
                ionice_level.temp = 0
            if radio_button("Low", ionice_class.temp == psutil.IOPRIO_LOW):
                ionice_class.temp = psutil.IOPRIO_LOW
                ionice_level.temp = 0
            if radio_button("VeryLow", ionice_class.temp == psutil.IOPRIO_VERYLOW):
                ionice_class.temp = psutil.IOPRIO_VERYLOW
                ionice_level.temp = 0

        elif psutil.LINUX:
            if radio_button("RT", ionice_class.temp == psutil.IOPRIO_CLASS_RT):
                ionice_class.temp = psutil.IOPRIO_CLASS_RT
            if ionice_class.temp == psutil.IOPRIO_CLASS_RT:
                imgui.same_line()
                if level := slider_int("##Level", ionice_level.temp, 0, 7):
                    ionice_level.temp = level.value
                imgui.same_line()
                imgui.text("Additional priority level. 0 (highest) to 7 (lowest)")

            if radio_button("BE", ionice_class.temp == psutil.IOPRIO_CLASS_BE):
                ionice_class.temp = psutil.IOPRIO_CLASS_BE
            if ionice_class.temp == psutil.IOPRIO_CLASS_BE:
                imgui.same_line()
                if level := slider_int("##Level", ionice_level.temp, 0, 7):
                    ionice_level.temp = level.value
                imgui.same_line()
                imgui.text("Additional priority level. 0 (highest) to 7 (lowest)")

            if radio_button("IDLE", ionice_class.temp == psutil.IOPRIO_CLASS_IDLE):
                ionice_class.temp = psutil.IOPRIO_CLASS_IDLE
                ionice_level.temp = 0
            if radio_button("NONE", ionice_class.temp == psutil.IOPRIO_CLASS_NONE):
                ionice_class.temp = psutil.IOPRIO_CLASS_NONE
                ionice_level.temp = 0

        disabled_commit = not ionice_class.changed and not ionice_level.changed
        if button(f"{mdi.CLOSE} Cancel", disabled=disabled_commit):
            ionice_class.reset()
            ionice_level.reset()

        imgui.same_line()
        if button(f"{mdi.CHECK} Commit", disabled=disabled_commit):
            if not no_commit:
                ionice_class.commit()
                ionice_level.commit()

            class_result = ionice_class.value
            level_result = ionice_level.value

            if psutil.LINUX:
                if class_result in (psutil.IOPRIO_CLASS_RT, psutil.IOPRIO_CLASS_BE):
                    return IoniceEditResult(True, class_result, level_result)

            return IoniceEditResult(True, class_result, None)

    if right_title:
        imgui.same_line(spacing=imgui.get_style().item_inner_spacing.x)
        imgui.text(right_title)

    return IoniceEditResult(False, ionice_class.value, ionice_level.value)
