# -*- coding: utf-8 -*-

from typing import Any, Callable, Optional, Union

import pygame
from imgui_bundle import imgui

from cvp.dtypes.defaults.typing import get_typing_any
from cvp.dtypes.dtype import Dtype
from cvp.flow.variable import FlowVariable
from cvp.imgui.button import button
from cvp.imgui.flags.window import WindowFlags
from cvp.imgui.input_text_value import input_text_value
from cvp.imgui.popups.base import PopupBase
from cvp.imgui.push_item_width import item_width
from cvp.types.override import override
from cvp.variables import MIN_POPUP_VARIABLE_HEIGHT, MIN_POPUP_VARIABLE_WIDTH


class InputVariablePopup(PopupBase[FlowVariable]):
    def __init__(
        self,
        title: Optional[str] = None,
        label: Optional[str] = None,
        ok: Optional[str] = None,
        cancel: Optional[str] = None,
        centered=True,
        flags: Union[WindowFlags, int] = WindowFlags.always_auto_resize,
        *,
        min_width=MIN_POPUP_VARIABLE_WIDTH,
        min_height=MIN_POPUP_VARIABLE_HEIGHT,
        target: Optional[Callable[[FlowVariable], None]] = None,
        oneshot: Optional[bool] = None,
    ):
        super().__init__(
            title,
            centered,
            flags,
            min_width=min_width,
            min_height=min_height,
            target=target,
            oneshot=oneshot,
        )

        self._label = label if label else str()
        self._ok_button_label = ok if ok else "Ok"
        self._cancel_button_label = cancel if cancel else "Cancel"

        self._name = str()
        self._dtype = get_typing_any()
        self._docs = str()
        self._value: Any = None
        self._initial: Any = None
        self._persistent = False
        self._use_copy = False
        self._use_deepcopy = False

    @property
    def name(self):
        return self._name

    def create_variable(self):
        return FlowVariable(self._name, self._dtype.path)

    @override
    def on_process(self) -> Optional[FlowVariable]:
        if self._label:
            imgui.text(self._label)

        if imgui.is_window_appearing():
            imgui.set_keyboard_focus_here()

        with item_width(-1):
            self._name = input_text_value("Name", self._name)

        if pygame.key.get_pressed()[pygame.K_RETURN]:
            imgui.close_current_popup()
            return self.create_variable()
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            imgui.close_current_popup()
            return None

        if button(self._cancel_button_label):
            imgui.close_current_popup()
            return None
        imgui.same_line()
        if button(self._ok_button_label, disabled=not self._name):
            imgui.close_current_popup()
            return self.create_variable()

        return None

    def show_with_dtype(
        self,
        dtype: Dtype,
        title: Optional[str] = None,
        target: Optional[Callable[[FlowVariable], None]] = None,
        oneshot: Optional[bool] = None,
    ) -> None:
        self._dtype = dtype
        super().show(title, target, oneshot)
