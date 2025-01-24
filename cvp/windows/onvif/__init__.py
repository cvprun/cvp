# -*- coding: utf-8 -*-

from typing import Mapping

import imgui

from cvp.config.sections.onvif import OnvifConfig, OnvifManagerConfig
from cvp.imgui.button import button
from cvp.popups.confirm import ConfirmPopup
from cvp.popups.input_text import InputTextPopup
from cvp.renderer.context import RendererContext
from cvp.types.override import override
from cvp.widgets.manager_tabs import ManagerTabs
from cvp.windows.onvif.apis import OnvifApisTab
from cvp.windows.onvif.auth import OnvifAuthTab
from cvp.windows.onvif.info import OnvifInfoTab
from cvp.windows.onvif.service import OnvifServiceTab


class OnvifManager(ManagerTabs[OnvifManagerConfig, OnvifConfig]):
    def __init__(self, context: RendererContext):
        super().__init__(
            context=context,
            window_config=context.config.onvif_manager,
            title="Onvif Manager",
            closable=True,
            flags=None,
        )
        self.register(OnvifInfoTab(context))
        self.register(OnvifAuthTab(context))
        self.register(OnvifServiceTab(context))
        self.register(OnvifApisTab(context))

        self._open_url_popup = InputTextPopup(
            title="Open network address",
            label="Please enter a network URL:",
            ok="Open",
            cancel="Close",
            target=self.on_open_url_popup,
        )
        self._confirm_remove = ConfirmPopup(
            title="Remove",
            label="Are you sure you want to remove device?",
            ok="Remove",
            cancel="No",
            target=self.on_confirm_remove,
        )

        self.register_popup(self._open_url_popup)
        self.register_popup(self._confirm_remove)

    @override
    def get_menus(self) -> Mapping[str, OnvifConfig]:
        return {onvif.uuid: onvif for onvif in self.context.config.onvifs}

    @override
    def on_process_sidebar_top(self) -> None:
        if imgui.button("New"):
            self._open_url_popup.show()
        imgui.same_line()
        selected_menu = self.latest_menus.get(self.selected)
        if button("Remove", disabled=selected_menu is None):
            self._confirm_remove.show()

    def on_open_url_popup(self, url: str) -> None:
        config = OnvifConfig(address=url, name=url)
        self.context.config.onvifs.append(config)

    def on_confirm_remove(self, value: bool) -> None:
        if not value:
            return

        selected_menu = self.latest_menus.get(self.selected)
        assert selected_menu is not None

        uuid = selected_menu.uuid
        self.context.config.remove_onvif(uuid)
