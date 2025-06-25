# -*- coding: utf-8 -*-

from typing import Final

from imgui_bundle import imgui

from cvp.apps.player.modes._base import BaseMode
from cvp.apps.player.modes.mediamtx.config import MediamtxConfigTab
from cvp.apps.player.modes.mediamtx.mtx_config import MediamtxGlobalConfTab
from cvp.apps.player.modes.mediamtx.path import MediamtxPathTab
from cvp.assets.fonts.mdi import SIGNAL_VARIANT
from cvp.context.context import Context
from cvp.imgui.begin_child import begin_child_context
from cvp.imgui.button import button
from cvp.imgui.fit_size import FIT_SIZE
from cvp.imgui.flags.child import BORDERS, RESIZE_X
from cvp.imgui.popups.confirm import ConfirmPopup
from cvp.imgui.popups.containers import PopupList
from cvp.imgui.tab_container import TabList
from cvp.imgui.text_centered import text_centered
from cvp.mediamtx.item import MediamtxKey
from cvp.types.override import override


class MediaMTXMode(BaseMode):
    __cvp_mode_name__ = "MediaMTX"
    __cvp_mode_icon__ = SIGNAL_VARIANT

    _MENU_SPLIT_X: Final[int] = 150
    _MENU_CHILD_FLAGS: Final[int] = RESIZE_X | BORDERS

    def __init__(self, context: Context):
        super().__init__(context)

        self._tabs = TabList(
            ("Config", MediamtxConfigTab(context)),
            ("GlobalConf", MediamtxGlobalConfTab(context)),
            ("Path", MediamtxPathTab(context)),
        )

        self._remove_candidate = str()
        self._confirm_remove = ConfirmPopup(
            title="Remove",
            label="Are you sure you want to remove mediamtx?",
            ok="Remove",
            cancel="No",
            target=self.on_confirm_remove,
        )
        self._confirm_clear = ConfirmPopup(
            title="Clear",
            label="Are you sure you want to remove all mediamtx?",
            ok="Clear",
            cancel="No",
            target=self.on_confirm_clear,
        )

        self._popups = PopupList(self._confirm_remove, self._confirm_clear)

    @property
    def config(self):
        return self.context.config.mediamtx

    @property
    def mediamtxs(self):
        return self.context.mediamtxs

    @property
    def selected_mediamtx(self):
        return self.mediamtxs.get(MediamtxKey(self.selected_submenu))

    def on_confirm_remove(self, value: bool) -> None:
        if not value:
            return

        assert self._remove_candidate in self.mediamtxs
        self.mediamtxs.remove(self._remove_candidate)
        self._remove_candidate = str()

    def on_confirm_clear(self, value: bool) -> None:
        if not value:
            return
        self.mediamtxs.remove_all()

    @override
    def on_process(self) -> None:
        with self.begin_mode_context():
            self.do_child_process()

    def do_child_process(self) -> None:
        with begin_child_context(
            label="Menu",
            size=(self._MENU_SPLIT_X, 0),
            child_flags=self._MENU_CHILD_FLAGS,
        ):
            if imgui.button("Reload"):
                self.mediamtxs.read_all_config_files()
            imgui.same_line()
            if imgui.button("Add"):
                self.selected_submenu = self.mediamtxs.add_new()[0]
            imgui.same_line()
            disabled_delete = self.selected_submenu not in self.mediamtxs
            if button("Del", disabled=disabled_delete):
                self._remove_candidate = self.selected_submenu
                self._confirm_remove.show()
            imgui.same_line()
            if button("Clear", disabled=not self.mediamtxs):
                self._confirm_clear.show()

            if imgui.begin_list_box("##List", FIT_SIZE):
                try:
                    for filename, mediamtx in self.mediamtxs.items():
                        label = f"{mediamtx.name}###{filename}"
                        selected = filename == self.selected_submenu
                        if imgui.selectable(label, selected)[1]:
                            self.selected_submenu = filename
                finally:
                    imgui.end_list_box()

        imgui.same_line()

        with begin_child_context("Main"):
            if mediamtx := self.mediamtxs.get(self.selected_submenu):
                self._tabs.do_process("MediamtxTabs", mediamtx)
            else:
                text_centered("Please select a item")
