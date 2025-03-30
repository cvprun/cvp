# -*- coding: utf-8 -*-

from typing import NamedTuple, Union

from imgui_bundle import imgui

from cvp.imgui.flags.input_text import CALLBACK_EDIT, InputTextFlags
from cvp.logging.logging import logger


class InputTextMultilingualResult(NamedTuple):
    changed: bool
    value: str

    @classmethod
    def from_raw(cls, result):
        assert isinstance(result, tuple)
        assert len(result) == 2
        changed = result[0]
        value = result[1]
        assert isinstance(changed, bool)
        assert isinstance(value, str)
        return cls(changed, value)

    def __bool__(self):
        return self.changed


def input_text_ko(
    label: str,
    value: str,
    flags: Union[InputTextFlags, int] = 0,
):
    if isinstance(flags, InputTextFlags):
        flags = int(flags)
    assert isinstance(flags, int)
    flags |= CALLBACK_EDIT

    # active = get_ime_active()
    # composing = get_ime_composing()

    raw_result = imgui.input_text(label, value, flags)
    result = InputTextMultilingualResult.from_raw(raw_result)

    # if imgui.is_item_active():
    #     if not get_ime_active():
    #         start_text_input()
    # else:
    #     if get_ime_active():
    #         stop_text_input()

    return result
