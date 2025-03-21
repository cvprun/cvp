# -*- coding: utf-8 -*-

from threading import Thread
from typing import Any, Callable, Iterable, Mapping, Optional

import pygame
from imgui_bundle import imgui

from cvp.imgui.button import button
from cvp.renderer.popup.base import PopupBase
from cvp.types.override import override


class ProgressPopup(PopupBase[None]):
    def __init__(
        self,
        target: Callable,
        args: Iterable[Any] = (),
        kwargs: Optional[Mapping[str, Any]] = None,
        title: Optional[str] = None,
        label: Optional[str] = None,
        cancel: Optional[str] = None,
        close: Optional[str] = None,
        centered=True,
        flags=0,
    ):
        super().__init__(title, centered, flags)
        self.label = label if label else str()
        self.cancel_button_label = cancel if cancel else "Cancel"
        self.close_button_label = close if close else "Close"
        self.progress = 0.0

        self._thread = Thread(
            group=None,
            target=target,
            name=None,
            args=args,
            kwargs=kwargs,
            daemon=None,
        )

    @property
    def completed(self) -> bool:
        return self.progress >= 1.0

    def start(self) -> None:
        self._thread.start()

    def is_alive(self) -> bool:
        return self._thread.is_alive()

    def join(self, timeout: Optional[float] = None) -> None:
        self._thread.join(timeout)

    @property
    def identifier(self):
        return self._thread.ident

    @property
    def native_id(self):
        return self._thread.native_id

    @override
    def on_process(self) -> Optional[None]:
        if self.label:
            imgui.text(self.label)

        imgui.progress_bar(self.progress, (-1, 0), "Overlay text")

        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            imgui.close_current_popup()
            return None

        if button(self.cancel_button_label, disabled=self.completed):
            imgui.close_current_popup()
            return None

        imgui.same_line()

        if button(self.close_button_label, disabled=not self.completed):
            imgui.close_current_popup()
            return None

        return None
