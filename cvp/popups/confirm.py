# -*- coding: utf-8 -*-

from typing import Callable, Optional

import pygame
from imgui_bundle import imgui

from cvp.imgui.button import button
from cvp.renderer.popup.base import PopupBase
from cvp.types.override import override
from cvp.variables import MIN_POPUP_CONFIRM_HEIGHT, MIN_POPUP_CONFIRM_WIDTH


class ConfirmPopup(PopupBase[bool]):
    def __init__(
        self,
        title: Optional[str] = None,
        label: Optional[str] = None,
        ok: Optional[str] = None,
        cancel: Optional[str] = None,
        centered=True,
        flags=imgui.WindowFlags_.always_auto_resize,
        *,
        min_width=MIN_POPUP_CONFIRM_WIDTH,
        min_height=MIN_POPUP_CONFIRM_HEIGHT,
        target: Optional[Callable[[bool], None]] = None,
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

    @override
    def on_process(self) -> Optional[bool]:
        if self._label:
            imgui.text(self._label)

        if pygame.key.get_pressed()[pygame.K_RETURN]:
            imgui.close_current_popup()
            return True
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            imgui.close_current_popup()
            return False

        if button(self._cancel_button_label):
            imgui.close_current_popup()
            return False
        imgui.same_line()
        if button(self._ok_button_label):
            imgui.close_current_popup()
            return True

        return None
