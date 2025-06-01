# -*- coding: utf-8 -*-

from typing import Final

from imgui_bundle import imgui

from cvp.apps.player.modes._base import BaseMode
from cvp.apps.player.modes.services.config import ServicesConfigTab
from cvp.apps.player.modes.services.control import ServicesControl
from cvp.apps.player.modes.services.logging import ServicesLoggingTab
from cvp.apps.player.modes.services.status import ServicesStatusTab
from cvp.assets.fonts.mdi import APPLICATION_COG
from cvp.context.context import Context
from cvp.imgui.begin_child import begin_child_context
from cvp.imgui.button import button
from cvp.imgui.fit_size import FIT_SIZE
from cvp.imgui.flags.child import BORDERS, RESIZE_X
from cvp.imgui.popups.confirm import ConfirmPopup
from cvp.imgui.popups.containers import PopupList
from cvp.imgui.tab_container import TabList
from cvp.imgui.text_centered import text_centered
from cvp.service.item import ServiceKey
from cvp.types.override import override
from cvp.variables import STDERR_FILE_HANDLE, STDOUT_FILE_HANDLE


class ServicesMode(BaseMode):
    __cvp_mode_name__ = "Services"
    __cvp_mode_icon__ = APPLICATION_COG

    _MENU_SPLIT_X: Final[int] = 300
    _MENU_CHILD_FLAGS: Final[int] = RESIZE_X | BORDERS

    _ARGS_LINE_COUNT: Final[int] = 5

    def __init__(self, context: Context):
        super().__init__(context)

        config_tab = ServicesConfigTab(context)
        status_tab = ServicesStatusTab(context)
        stdout_tab = ServicesLoggingTab(context, STDOUT_FILE_HANDLE)
        stderr_tab = ServicesLoggingTab(context, STDERR_FILE_HANDLE)
        self._tabs = TabList(
            ("Config", config_tab),
            ("Status", status_tab),
            ("Stdout", stdout_tab),
            ("Stderr", stderr_tab),
        )
        self._controller = ServicesControl(context)

        self._remove_candidate = str()
        self._confirm_remove = ConfirmPopup(
            title="Remove",
            label="Are you sure you want to remove service?",
            ok="Remove",
            cancel="No",
            target=self.on_confirm_remove,
        )
        self._confirm_clear = ConfirmPopup(
            title="Clear",
            label="Are you sure you want to remove all service?",
            ok="Clear",
            cancel="No",
            target=self.on_confirm_clear,
        )

        self._popups = PopupList(
            self._confirm_remove,
            self._confirm_clear,
            *config_tab.popups,
        )

    @property
    def services(self):
        return self.context.services

    @property
    def selected_service(self):
        return self.services.get(ServiceKey(self.selected_submenu))

    def on_confirm_remove(self, value: bool) -> None:
        if not value:
            return

        assert self._remove_candidate in self.services
        self.services.remove(self._remove_candidate)
        self._remove_candidate = str()

    def on_confirm_clear(self, value: bool) -> None:
        if not value:
            return
        self.services.remove_all()

    @override
    def on_process(self) -> None:
        with self.begin_mode_context():
            with begin_child_context(
                label="Menu",
                size=(self._MENU_SPLIT_X, 0),
                child_flags=self._MENU_CHILD_FLAGS,
            ):
                if button("Reload"):
                    self.services.read_all_config_files()
                imgui.same_line()
                if button("Add"):
                    self.services.add_service()
                imgui.same_line()
                if button("Del", disabled=self.selected_submenu not in self.services):
                    self._remove_candidate = self.selected_submenu
                    self._confirm_remove.show()
                imgui.same_line()
                if button("Clear", disabled=not self.services):
                    self._confirm_clear.show()

                if imgui.begin_list_box("##List", FIT_SIZE):
                    try:
                        for key, service in self.services.items():
                            label = f"{service.name}###{key}" if service.name else key
                            selected = key == self.selected_submenu
                            if imgui.selectable(label, selected)[1]:
                                self.selected_submenu = key
                    finally:
                        imgui.end_list_box()

            imgui.same_line()

            with begin_child_context("Main"):
                if item := self.services.get(ServiceKey(self.selected_submenu)):
                    self._controller(item)
                    self._tabs.do_process("Service Tabs", item)
                else:
                    text_centered("Please select a item")

        self._popups.do_process()
