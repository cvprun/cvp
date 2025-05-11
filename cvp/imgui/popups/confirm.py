# -*- coding: utf-8 -*-

from typing import Callable, Optional

import pygame
from imgui_bundle import imgui

from cvp.imgui.button import button
from cvp.imgui.popups._base import PopupBase
from cvp.types.override import override


class ConfirmPopup(PopupBase[bool]):
    __cvp_popup_min_width__ = 280
    __cvp_popup_min_height__ = 80

    def __init__(
        self,
        title: Optional[str] = None,
        label: Optional[str] = None,
        ok: Optional[str] = None,
        cancel: Optional[str] = None,
        flags=imgui.WindowFlags_.always_auto_resize,
        *,
        target: Optional[Callable[[bool], None]] = None,
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
        self.ok_button_label = ok if ok else "Ok"
        self.cancel_button_label = cancel if cancel else "Cancel"

    @override
    def on_main_process(self) -> Optional[bool]:
        if self.label:
            imgui.text(self.label)

        if pygame.key.get_pressed()[pygame.K_RETURN]:
            imgui.close_current_popup()
            return True
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            imgui.close_current_popup()
            return False

        if button(self.cancel_button_label):
            imgui.close_current_popup()
            return False
        imgui.same_line()
        if button(self.ok_button_label):
            imgui.close_current_popup()
            return True

        return None
