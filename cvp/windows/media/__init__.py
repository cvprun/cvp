# -*- coding: utf-8 -*-

import os
from typing import Mapping

from imgui_bundle import imgui

from cvp.config.sections.media import MediaManagerConfig, MediaWindowConfig
from cvp.config.sections.media import Mode as MediaSectionMode
from cvp.imgui.button import button
from cvp.popups.confirm import ConfirmPopup
from cvp.popups.input_text import InputTextPopup
from cvp.popups.open_file import OpenFilePopup
from cvp.renderer.context import RendererContext
from cvp.types.override import override
from cvp.widgets.manager_tabs import ManagerTabs
from cvp.windows.media.info import MediaInfoTab
from cvp.windows.media.media import MediaWindow


class MediaManager(ManagerTabs[MediaManagerConfig, MediaWindowConfig]):
    def __init__(self, context: RendererContext):
        super().__init__(
            context=context,
            window_config=context.config.media_manager,
            title="Media Manager",
            closable=True,
            flags=None,
        )
        self.register(MediaInfoTab(context))

        self._open_file_popup = OpenFilePopup(
            title="Open file",
            target=self.on_open_file_popup,
        )
        self._open_url_popup = InputTextPopup(
            title="Open network stream",
            label="Please enter a network URL:",
            ok="Open",
            cancel="Close",
            target=self.on_open_url_popup,
        )
        self._confirm_remove = ConfirmPopup(
            title="Remove",
            label="Are you sure you want to remove media?",
            ok="Remove",
            cancel="No",
            target=self.on_confirm_remove,
        )

        self.register_popup(self._open_file_popup)
        self.register_popup(self._open_url_popup)
        self.register_popup(self._confirm_remove)

    def add_media_window(self, config: MediaWindowConfig) -> None:
        window = MediaWindow(self.context, config)
        self.context.windows.add_window(window, window.key)

    def add_media_windows(self, *configs: MediaWindowConfig) -> None:
        for config in configs:
            self.add_media_window(config)

    @override
    def on_create(self) -> None:
        self.add_media_windows(*self.context.config.media_windows)

    @override
    def on_process_sidebar_top(self) -> None:
        if imgui.button("File"):
            self._open_file_popup.show()
        imgui.same_line()
        if imgui.button("URL"):
            self._open_url_popup.show()
        imgui.same_line()
        selected_menu = self.latest_menus.get(self.selected)
        if button("Remove", disabled=selected_menu is None):
            self._confirm_remove.show()

    @override
    def get_menus(self) -> Mapping[str, MediaWindowConfig]:
        return {mw.uuid: mw for mw in self._context.config.media_windows}

    def on_open_file_popup(self, file: str) -> None:
        config = MediaWindowConfig(
            title=os.path.basename(file),
            opened=True,
            mode=MediaSectionMode.file,
            file=file,
        )
        self.context.config.media_windows.append(config)
        self.add_media_window(config)

    def on_open_url_popup(self, url: str) -> None:
        config = MediaWindowConfig(
            title=url,
            opened=True,
            mode=MediaSectionMode.url,
            file=url,
        )
        self.context.config.media_windows.append(config)
        self.add_media_window(config)

    def on_confirm_remove(self, value: bool) -> None:
        if not value:
            return

        selected_menu = self.latest_menus.get(self.selected)
        assert selected_menu is not None

        uuid = selected_menu.uuid
        self.context.windows.set_removable(uuid)
        self.context.config.remove_media_window(uuid)
