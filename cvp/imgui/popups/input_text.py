# -*- coding: utf-8 -*-

from typing import Callable, Optional, Union

import pygame
from imgui_bundle import imgui

from cvp.imgui.button import button
from cvp.imgui.fit_size import FIT_WIDTH
from cvp.imgui.flags.window import WindowFlags
from cvp.imgui.input_text_value import input_text_value
from cvp.imgui.popups._base import PopupBase
from cvp.imgui.push_item_width import item_width_context
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

        self.label = label if label else str()
        self.text = text if text else str()
        self.ok_button_label = ok if ok else "Ok"
        self.cancel_button_label = cancel if cancel else "Cancel"
        self.validate = validate

    @override
    def on_main_process(self) -> Optional[str]:
        if self.label:
            imgui.text(self.label)

        if imgui.is_window_appearing():
            imgui.set_keyboard_focus_here()

        with item_width_context(FIT_WIDTH):
            self.text = input_text_value("##Text", self.text)

        if pygame.key.get_pressed()[pygame.K_RETURN]:
            imgui.close_current_popup()
            return self.text
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            imgui.close_current_popup()
            return None

        validate = True
        if self.validate is not None:
            validate = bool(self.validate(self.text))

        if button(self.cancel_button_label):
            imgui.close_current_popup()
            return None
        imgui.same_line()
        enabled_ok_button = bool(self.text) and validate
        if button(self.ok_button_label, disabled=not enabled_ok_button):
            imgui.close_current_popup()
            return self.text

        return None
