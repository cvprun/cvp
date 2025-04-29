# -*- coding: utf-8 -*-

from typing import Callable, Optional, Union

import pygame
from imgui_bundle import imgui

from cvp.imgui.button import button
from cvp.imgui.flags.window import WindowFlags
from cvp.imgui.input_text_value import input_text_value
from cvp.imgui.popups._base import PopupBase
from cvp.imgui.push_item_width import item_width
from cvp.types.override import override


class InputTextPopup(PopupBase[str]):
    __cvp_popup_min_width__ = 200
    __cvp_popup_min_height__ = 120

    def __init__(
        self,
        title: Optional[str] = None,
        label: Optional[str] = None,
        text: Optional[str] = None,
        ok: Optional[str] = None,
        cancel: Optional[str] = None,
        flags: Union[WindowFlags, int] = WindowFlags.always_auto_resize,
        *,
        validate: Optional[Callable[[str], bool]] = None,
        target: Optional[Callable[[str], None]] = None,
        oneshot: Optional[bool] = None,
        identifier: Optional[str] = None,
        min_width: Optional[int] = None,
        min_height: Optional[int] = None,
        centered=True,
    ):
        super().__init__(
            title=title,
            flags=flags,
            target=target,
            oneshot=oneshot,
            identifier=identifier,
            min_width=min_width,
            min_height=min_height,
            centered=centered,
        )

        self._label = label if label else str()
        self._text = text if text else str()
        self._ok_button_label = ok if ok else "Ok"
        self._cancel_button_label = cancel if cancel else "Cancel"
        self._validate = validate

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, value: str) -> None:
        self._text = value

    @override
    def on_process(self) -> Optional[str]:
        if self._label:
            imgui.text(self._label)

        if imgui.is_window_appearing():
            imgui.set_keyboard_focus_here()

        with item_width(-1):
            self._text = input_text_value("##Text", self._text)

        if pygame.key.get_pressed()[pygame.K_RETURN]:
            imgui.close_current_popup()
            return self._text
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            imgui.close_current_popup()
            return None

        validate = True
        if self._validate is not None:
            validate = bool(self._validate(self._text))

        if button(self._cancel_button_label):
            imgui.close_current_popup()
            return None
        imgui.same_line()
        enabled_ok_button = bool(self._text) and validate
        if button(self._ok_button_label, disabled=not enabled_ok_button):
            imgui.close_current_popup()
            return self._text

        return None
