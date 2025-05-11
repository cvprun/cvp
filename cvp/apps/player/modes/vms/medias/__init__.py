# -*- coding: utf-8 -*-

from collections import OrderedDict
from functools import lru_cache
from typing import Sequence, Type

from imgui_bundle import imgui

from cvp.apps.player.modes._base import BaseMode
from cvp.apps.player.modes.vms.medias._base import BaseMediaTab, MediaTabInterface
from cvp.context.context import Context
from cvp.imgui.begin_child import begin_child_context
from cvp.imgui.button import button
from cvp.imgui.fit_size import FIT_SIZE
from cvp.imgui.flags.child import BORDERS, RESIZE_X
from cvp.imgui.popups.confirm import ConfirmPopup
from cvp.imgui.text_centered import text_centered
from cvp.media.config import MediaConfig
from cvp.types.override import override


@lru_cache
def create_media_tab_types() -> Sequence[Type[BaseMediaTab]]:
    from cvp.apps.player.modes.vms.medias.info import MediaInfoTab
    from cvp.apps.player.modes.vms.medias.stream import MediaStreamTab

    return MediaInfoTab, MediaStreamTab


def create_media_tabs(context: Context) -> OrderedDict[str, MediaTabInterface]:
    tab_types = create_media_tab_types()
    return OrderedDict({tt.get_tab_name(): tt(context) for tt in tab_types})


class MediasMode(BaseMode):
    __cvp_mode_name__ = "Medias"

    def __init__(self, context: Context):
        super().__init__(context)
        self._tabs = create_media_tabs(context)
        self._remove_candidate = str()
        self._confirm_remove = ConfirmPopup(
            title="Remove",
            label="Are you sure you want to remove media?",
            ok="Remove",
            cancel="No",
            target=self.on_confirm_remove,
        )
        self._confirm_clear = ConfirmPopup(
            title="Clear",
            label="Are you sure you want to remove all medias?",
            ok="Clear",
            cancel="No",
            target=self.on_confirm_clear,
        )

    @property
    def medias(self):
        return self.context.medias

    def on_confirm_remove(self, value: bool) -> None:
        if not value:
            return
        assert self._remove_candidate in self.medias
        self.medias.remove(self._remove_candidate)

    def on_confirm_clear(self, value: bool) -> None:
        if not value:
            return
        self.medias.remove_all()

    @override
    def on_process(self) -> None:
        with self.begin_mode_context():
            self.do_child_process()

    def do_child_process(
        self,
        menu_split_x=300,
        menu_child_flags=RESIZE_X | BORDERS,
    ) -> None:
        with begin_child_context(
            label="Menu",
            size=(menu_split_x, 0),
            child_flags=menu_child_flags,
        ):
            if button("Reload"):
                self.medias.read_all_config_files()
            imgui.same_line()
            if imgui.button("Add"):
                self.selected_submenu = self.medias.add_media()[0]
            imgui.same_line()
            if button("Del", disabled=self.selected_submenu not in self.medias):
                self._remove_candidate = self.selected_submenu
                self._confirm_remove.show()
            imgui.same_line()
            if button("Clear", disabled=not self.medias):
                self._confirm_clear.show()

            if imgui.begin_list_box("##List", FIT_SIZE):
                try:
                    for key, media in self.medias.items():
                        label = f"{media.name}###{key}"
                        selected = key == self.selected_submenu
                        if imgui.selectable(label, selected)[1]:
                            self.selected_submenu = key
                finally:
                    imgui.end_list_box()

        imgui.same_line()

        with begin_child_context("Main"):
            if selected_media := self.medias.get(self.selected_submenu):
                self.do_media_tab_bar(selected_media)
            else:
                text_centered("Please select a item")

        self._confirm_remove.on_process()
        self._confirm_clear.on_process()

    def do_media_tab_bar(self, media: MediaConfig) -> None:
        if imgui.begin_tab_bar("Tabs"):
            try:
                for name, tab in self._tabs.items():
                    if imgui.begin_tab_item(name)[0]:
                        try:
                            tab.on_process(media)
                        finally:
                            imgui.end_tab_item()
            finally:
                imgui.end_tab_bar()
