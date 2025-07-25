# -*- coding: utf-8 -*-

from typing import Callable, Iterable, Optional

from imgui_bundle import imgui

from cvp.imgui.button import button
from cvp.imgui.popups._base import PopupBase
from cvp.types.override import override


class ConfirmButtonsPopup(PopupBase[int]):
    __cvp_popup_min_width__ = 280
    __cvp_popup_min_height__ = 80

    def __init__(
        self,
        title: Optional[str] = None,
        label: Optional[str] = None,
        button_labels: Optional[Iterable[str]] = None,
        flags=imgui.WindowFlags_.always_auto_resize,
        *,
        target: Optional[Callable[[int], None]] = None,
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
        self.button_labels = list(button_labels if button_labels else ("Ok", "Cancel"))

    @override
    def on_main_process(self) -> Optional[int]:
        if self.label:
            imgui.text(self.label)

        if not self.button_labels:
            return None

        assert 1 <= len(self.button_labels)
        first_button_label = self.button_labels[0]
        if button(first_button_label):
            imgui.close_current_popup()
            return 0

        remain_button_labels = self.button_labels[1:]
        if not remain_button_labels:
            return None

        assert 1 <= len(remain_button_labels)
        for i, button_label in enumerate(remain_button_labels, start=1):
            imgui.same_line()
            if button(button_label):
                imgui.close_current_popup()
                return i

        return None
