# -*- coding: utf-8 -*-

from typing import Final

from imgui_bundle import imgui

from cvp.apps.player.modes._base import BaseMode
from cvp.context.context import Context
from cvp.imgui.begin import begin_context
from cvp.imgui.begin_child import begin_child_context
from cvp.imgui.button import button
from cvp.imgui.fit_size import FIT_SIZE
from cvp.imgui.flags.child import BORDERS, RESIZE_X
from cvp.imgui.flags.style_var import StyleVar
from cvp.imgui.flags.window import ROOT_STATIC_VIEWPORT_FLAGS
from cvp.imgui.set_next_window_as_viewport import set_next_window_as_viewport
from cvp.imgui.text_centered import text_centered
from cvp.onvif.onvif import OnvifConfig
from cvp.popups.confirm import ConfirmPopup
from cvp.types.override import override

_MENU_SPLIT_X: Final[int] = 300
_MENU_CHILD_FLAGS: Final[int] = RESIZE_X | BORDERS


class OnvifMode(BaseMode):
    __cvp_mode_name__ = "Onvif"

    def __init__(self, context: Context):
        super().__init__(context)
        self._remove_candidate = str()
        self._confirm_remove = ConfirmPopup(
            title="Remove",
            label="Are you sure you want to remove device?",
            ok="Remove",
            cancel="No",
            target=self.on_confirm_remove,
        )
        self._confirm_clear = ConfirmPopup(
            title="Clear",
            label="Are you sure you want to remove all devices?",
            ok="Clear",
            cancel="No",
            target=self.on_confirm_clear,
        )

    @property
    def onvifs(self):
        return self.context.onvifs

    @property
    def config(self):
        return self.context.config.onvif_manager

    @property
    def selected(self) -> str:
        return self.config.selected

    @selected.setter
    def selected(self, value: str) -> None:
        self.config.selected = value

    def on_confirm_remove(self, value: bool) -> None:
        if not value:
            return
        assert self._remove_candidate in self.onvifs
        self.onvifs.remove(self._remove_candidate)

    def on_confirm_clear(self, value: bool) -> None:
        if not value:
            return
        self.onvifs.remove_all()

    @override
    def do_process(self) -> None:
        imgui.push_style_var(StyleVar.window_border_size, 0)
        try:
            set_next_window_as_viewport()
            with begin_context(type(self).__name__, flags=ROOT_STATIC_VIEWPORT_FLAGS):
                self.do_child_process()
        finally:
            imgui.pop_style_var()

    def do_child_process(
        self,
        menu_split_x=_MENU_SPLIT_X,
        menu_child_flags=_MENU_CHILD_FLAGS,
    ) -> None:
        with begin_child_context("Menu", menu_split_x, child_flags=menu_child_flags):
            if button("Reload"):
                self.onvifs.read_all_config_files()
            imgui.same_line()
            if imgui.button("Add"):
                self.selected = self.onvifs.add_new()[0]
            imgui.same_line()
            if button("Del", disabled=self.selected not in self.onvifs):
                self._remove_candidate = self.selected
                self._confirm_remove.show()
            imgui.same_line()
            if button("Clear", disabled=not self.onvifs):
                self._confirm_clear.show()

            if imgui.begin_list_box("##List", FIT_SIZE):
                try:
                    for key, onvif in self.onvifs.items():
                        label = f"{onvif.name}###{key}"
                        selected = key == self.selected
                        if imgui.selectable(label, selected)[1]:
                            self.selected = key
                finally:
                    imgui.end_list_box()

        imgui.same_line()

        with begin_child_context("Main"):
            if selected_onvif := self.onvifs.get(self.selected):
                self.do_onvif_process(selected_onvif)
            else:
                text_centered("Please select a item")

        self._confirm_remove.do_process()
        self._confirm_clear.do_process()

    def do_onvif_process(self, onvif: OnvifConfig) -> None:
        pass
