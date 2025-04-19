# -*- coding: utf-8 -*-

from collections import OrderedDict
from functools import lru_cache
from typing import Final, Sequence, Type

from imgui_bundle import imgui

from cvp.apps.player.modes._base import BaseMode
from cvp.apps.player.modes.medias._base import BaseMediaTab
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
from cvp.media.config import MediaConfig
from cvp.popups.confirm import ConfirmPopup
from cvp.types.override import override

_MENU_SPLIT_X: Final[int] = 300
_MENU_CHILD_FLAGS: Final[int] = RESIZE_X | BORDERS


@lru_cache
def create_media_tab_types() -> Sequence[Type[BaseMediaTab]]:
    from cvp.apps.player.modes.medias.info import MediaInfoTab
    from cvp.apps.player.modes.medias.player import MediaPlayerTab

    return MediaInfoTab, MediaPlayerTab


def create_media_tabs(context: Context):
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
                self.medias.read_all_config_files()
            imgui.same_line()
            if imgui.button("Add"):
                self.selected = self.medias.add_config()[0]
            imgui.same_line()
            if button("Del", disabled=self.selected not in self.medias):
                self._remove_candidate = self.selected
                self._confirm_remove.show()
            imgui.same_line()
            if button("Clear", disabled=not self.medias):
                self._confirm_clear.show()

            if imgui.begin_list_box("##List", FIT_SIZE):
                try:
                    for key, media in self.medias.items():
                        label = f"{media.name}###{key}"
                        selected = key == self.selected
                        if imgui.selectable(label, selected)[1]:
                            self.selected = key
                finally:
                    imgui.end_list_box()

        imgui.same_line()

        with begin_child_context("Main"):
            if selected_media := self.medias.get(self.selected):
                self.do_media_tab_bar(selected_media)
            else:
                text_centered("Please select a item")

        self._confirm_remove.do_process()
        self._confirm_clear.do_process()

    def do_media_tab_bar(self, media: MediaConfig) -> None:
        if imgui.begin_tab_bar("Tabs"):
            try:
                for name, tab in self._tabs.items():
                    if imgui.begin_tab_item(name)[0]:
                        try:
                            tab.do_process(media)
                        finally:
                            imgui.end_tab_item()
            finally:
                imgui.end_tab_bar()
