# -*- coding: utf-8 -*-

from collections import OrderedDict
from functools import lru_cache
from typing import Final, Sequence, Type

from imgui_bundle import imgui

from cvp.apps.player.modes._base import BaseMode
from cvp.apps.player.modes.onvif._base import BaseOnvifTab
from cvp.context.context import Context
from cvp.imgui.begin_child import begin_child_context
from cvp.imgui.button import button
from cvp.imgui.fit_size import FIT_SIZE
from cvp.imgui.flags.child import BORDERS, RESIZE_X
from cvp.imgui.text_centered import text_centered
from cvp.onvif.config import OnvifConfig
from cvp.popups.confirm import ConfirmPopup
from cvp.types.override import override

_MENU_SPLIT_X: Final[int] = 300
_MENU_CHILD_FLAGS: Final[int] = RESIZE_X | BORDERS


@lru_cache
def create_onvif_tab_types() -> Sequence[Type[BaseOnvifTab]]:
    from cvp.apps.player.modes.onvif.apis import OnvifApisTab
    from cvp.apps.player.modes.onvif.auth import OnvifAuthTab
    from cvp.apps.player.modes.onvif.client import OnvifClientTab
    from cvp.apps.player.modes.onvif.info import OnvifInfoTab

    return OnvifInfoTab, OnvifAuthTab, OnvifClientTab, OnvifApisTab


def create_onvif_tabs(context: Context):
    tab_types = create_onvif_tab_types()
    return OrderedDict({tt.get_tab_name(): tt(context) for tt in tab_types})


class OnvifMode(BaseMode):
    __cvp_mode_name__ = "Onvif"

    def __init__(self, context: Context):
        super().__init__(context)
        self._tabs = create_onvif_tabs(context)
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
        return self.context.config.onvif

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
        with self.begin_mode_context():
            self.do_child_process()

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
                self.selected = self.onvifs.add_config()[0]
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
                self.do_onvif_tab_bar(selected_onvif)
            else:
                text_centered("Please select a item")

        self._confirm_remove.do_process()
        self._confirm_clear.do_process()

    def do_onvif_tab_bar(self, onvif: OnvifConfig) -> None:
        if imgui.begin_tab_bar("Tabs"):
            try:
                for name, tab in self._tabs.items():
                    if imgui.begin_tab_item(name)[0]:
                        try:
                            tab.do_process(onvif)
                        finally:
                            imgui.end_tab_item()
            finally:
                imgui.end_tab_bar()
