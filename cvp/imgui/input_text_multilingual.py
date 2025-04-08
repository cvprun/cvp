# -*- coding: utf-8 -*-

from typing import NamedTuple, Optional, Union

from imgui_bundle import imgui

from cvp.imgui.flags.input_text import InputTextFlags


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


def input_text_multilingual(
    label: str,
    value: str,
    flags: Union[InputTextFlags, int] = 0,
    size: Optional[imgui.ImVec2Like] = None,
    hint: Optional[str] = None,
):
    if isinstance(flags, InputTextFlags):
        flags = int(flags)
    assert isinstance(flags, int)

    # active = get_ime_active()
    # composing = get_ime_composing()
    has_newline = 0 <= value.find("\n")

    if has_newline:
        raw_result = imgui.input_text_multiline(label, value, size, flags)
    elif hint:
        if size is not None:
            imgui.set_next_item_width(size[0])
        raw_result = imgui.input_text_with_hint(label, hint, value, flags)
    else:
        if size is not None:
            imgui.set_next_item_width(size[0])
        raw_result = imgui.input_text(label, value, flags)

    return InputTextMultilingualResult.from_raw(raw_result)
