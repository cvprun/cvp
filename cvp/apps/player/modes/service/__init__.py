# -*- coding: utf-8 -*-

from typing import Final

from imgui_bundle import imgui

from cvp.apps.player.modes._base import BaseMode
from cvp.assets.fonts.mdi import APPLICATION_COG
from cvp.context.context import Context
from cvp.imgui.begin_child import begin_child_context
from cvp.imgui.begin_tab_item import begin_tab_item, end_tab_item
from cvp.imgui.button import button
from cvp.imgui.fit_size import FIT_SIZE
from cvp.imgui.flags.child import BORDERS, RESIZE_X
from cvp.imgui.input_int import input_int
from cvp.imgui.input_text import input_text
from cvp.imgui.input_text_disabled import input_text_disabled
from cvp.imgui.popups.confirm import ConfirmPopup
from cvp.imgui.table_mutable_sequence import table_mutable_sequence
from cvp.imgui.text_centered import text_centered
from cvp.service.item import ServiceItem
from cvp.types.dataclass.field_default import get_field_default
from cvp.types.dataclass.field_name import get_field_name
from cvp.types.override import override


class ServiceManagerMode(BaseMode):
    __cvp_mode_name__ = "Service Manager"
    __cvp_mode_icon__ = APPLICATION_COG

    _MENU_SPLIT_X: Final[int] = 300
    _MENU_CHILD_FLAGS: Final[int] = RESIZE_X | BORDERS

    def __init__(self, context: Context):
        super().__init__(context)
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

    @property
    def services(self):
        return self.context.services

    def on_confirm_remove(self, value: bool) -> None:
        if not value:
            return
        assert self._remove_candidate in self.services
        self.services.remove(self._remove_candidate)

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
                if selected_service := self.services.get(self.selected_submenu):
                    self.do_main_process(selected_service)
                else:
                    text_centered("Please select a item")

        self._confirm_remove.on_process()
        self._confirm_clear.on_process()

    def do_main_process(self, service: ServiceItem) -> None:
        if imgui.begin_tab_bar("Service Tabs"):
            try:
                if begin_tab_item("Config"):
                    try:
                        self.do_config_process(service)
                    finally:
                        end_tab_item()

                if begin_tab_item("Status"):
                    try:
                        self.do_status_process(service)
                    finally:
                        end_tab_item()
            finally:
                imgui.end_tab_bar()

    @staticmethod
    def do_config_process(service: ServiceItem) -> None:
        imgui.text("Service Config")
        imgui.separator()

        input_text_disabled("UUID", service.uuid)

        if name := input_text("Name", service.name):
            service.name = name.value

        imgui.text("Arguments")
        table_mutable_sequence(
            "Arguments",
            service.args,
            swappable=True,
            removable=True,
            insertable_callback=lambda i: str(),
        )

        if buffer_size := input_int("Buffer Size", service.buffer_size):
            service.buffer_size = buffer_size.value

        if button("Default Buffer Size"):
            buffer_size_key = get_field_name(service).buffer_size
            buffer_size_default = get_field_default(service, buffer_size_key)
            service.buffer_size = buffer_size_default

    @staticmethod
    def do_status_process(service: ServiceItem) -> None:
        imgui.text("Service Status")
        imgui.separator()

        input_text_disabled("UUID", service.uuid)
        input_text_disabled("Name", service.name)
