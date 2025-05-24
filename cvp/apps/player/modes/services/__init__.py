# -*- coding: utf-8 -*-

import os
from pathlib import Path
from typing import Final, Union

from imgui_bundle import imgui

from cvp.apps.player.modes._base import BaseMode
from cvp.assets.fonts.mdi import APPLICATION_COG
from cvp.context.context import Context
from cvp.imgui.begin_child import begin_child_context
from cvp.imgui.button import button
from cvp.imgui.combo_enum import combo_enum
from cvp.imgui.fit_size import FIT_SIZE
from cvp.imgui.flags.child import BORDERS, RESIZE_X
from cvp.imgui.input_float import input_float
from cvp.imgui.input_int import input_int
from cvp.imgui.input_text import input_text
from cvp.imgui.input_text_disabled import input_text_disabled
from cvp.imgui.input_text_multiline import (
    calc_input_text_multiline_with_line_count,
    input_text_multiline,
)
from cvp.imgui.popups.confirm import ConfirmPopup
from cvp.imgui.popups.containers import PopupList
from cvp.imgui.popups.open_file import OpenFilePopup
from cvp.imgui.tab_container import TabList
from cvp.imgui.text_centered import text_centered
from cvp.imgui.tooltip import hovered_tooltip_text_wrapped
from cvp.service.item import ServiceKey
from cvp.types.dataclass.field_default import get_field_default
from cvp.types.dataclass.field_name import get_field_name
from cvp.types.override import override
from cvp.variables import COMMA


class ServicesMode(BaseMode):
    __cvp_mode_name__ = "Services"
    __cvp_mode_icon__ = APPLICATION_COG

    _MENU_SPLIT_X: Final[int] = 300
    _MENU_CHILD_FLAGS: Final[int] = RESIZE_X | BORDERS

    _ARGS_LINE_COUNT: Final[int] = 5

    def __init__(self, context: Context):
        super().__init__(context)

        self._tabs = TabList(
            ("Config", self.do_config_process),
            ("Status", self.do_status_process),
        )

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
        self._executable_browser = OpenFilePopup(
            "Select executable file",
            target=self.on_executable_selected,
            open_mode=OpenFilePopup.OpenMode.select_file,
        )
        self._cwd_browser = OpenFilePopup(
            "Select working directory",
            target=self.on_cwd_selected,
            open_mode=OpenFilePopup.OpenMode.select_directory,
        )
        self._pid_file_browser = OpenFilePopup(
            "Select PID file",
            target=self.on_pid_selected,
            open_mode=OpenFilePopup.OpenMode.input_filename,
        )
        self._popups = PopupList(
            self._confirm_remove,
            self._confirm_clear,
            self._executable_browser,
        )

    @property
    def success_color(self):
        return self.context.config.appearance.success_color

    @property
    def warning_color(self):
        return self.context.config.appearance.warning_color

    @property
    def error_color(self):
        return self.context.config.appearance.error_color

    def text_success(self, text: str) -> None:
        imgui.text_colored(self.success_color, text)

    def text_error(self, text: str) -> None:
        imgui.text_colored(self.error_color, text)

    def hovered_tooltip(self, message: Union[str, BaseException]) -> bool:
        if isinstance(message, BaseException):
            return hovered_tooltip_text_wrapped(str(message), self.error_color)
        else:
            assert isinstance(message, str)
            return hovered_tooltip_text_wrapped(message)

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

    def on_confirm_clear(self, value: bool) -> None:
        if not value:
            return
        self.services.remove_all()

    def on_executable_selected(self, file: str) -> None:
        if not file:
            return

        if not os.path.exists(file):
            self.context.toast_error(f"'{file}' does not exist")
            return

        if not os.path.isfile(file):
            self.context.toast_error(f"'{file}' is not a file")
            return

        if not os.access(file, os.X_OK):
            self.context.toast_error(f"'{file}' is not executable")
            return

        selected_service = self.selected_service
        assert selected_service is not None
        selected_service.executable = file

    def on_cwd_selected(self, file: str) -> None:
        if not file:
            return

        if not os.path.exists(file):
            self.context.toast_error(f"'{file}' does not exist")
            return

        if not os.path.isdir(file):
            self.context.toast_error(f"'{file}' is not a directory")
            return

        selected_service = self.selected_service
        assert selected_service is not None
        selected_service.cwd = file

    def on_pid_selected(self, file: str) -> None:
        if not file:
            return

        selected_service = self.selected_service
        assert selected_service is not None
        selected_service.pid_file = file

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
                if self.selected_submenu in self.services:
                    self._tabs.do_process("Service Tabs")
                else:
                    text_centered("Please select a item")

        self._popups.do_process()

    def do_config_process(self) -> None:
        service = self.selected_service
        assert service is not None

        imgui.text("Service Config")
        imgui.separator()

        input_text_disabled("UUID", service.uuid)

        if name := input_text("Name", service.name):
            service.name = name.value

        if executable := input_text("Executable", service.executable):
            service.executable = executable.value

        if service.executable:
            self.hovered_tooltip(service.normalize_executable())

        if button("Browse Executable"):
            self._executable_browser.set_location(service.normalize_executable())
            self._executable_browser.show()

        imgui.same_line()
        if not service.executable:
            self.text_error("No executable path provided")
        elif not os.path.exists(service.executable):
            self.text_error("Executable does not exist")
        elif not os.path.isfile(service.executable):
            self.text_error("Executable is not a file")
        elif not os.access(service.executable, os.X_OK):
            self.text_error("Executable is not executable")
        else:
            self.text_success("Executable is valid and ready")

        cmds_height = calc_input_text_multiline_with_line_count(self._ARGS_LINE_COUNT)
        if cmds := input_text_multiline("Arguments", service.args, (0, cmds_height)):
            service.args = cmds.value

        try:
            if multiline_arguments := service.multiline_normalize_arguments():
                self.hovered_tooltip(multiline_arguments)
        except BaseException as e:
            self.hovered_tooltip(e)

        if buffer_size := input_int("Buffer Size", service.buffer_size):
            service.buffer_size = buffer_size.value

        if button("Default"):
            buffer_size_key = get_field_name(service).buffer_size
            buffer_size_default = get_field_default(service, buffer_size_key)
            service.buffer_size = buffer_size_default
        imgui.same_line()
        if button("Unbuffered"):
            service.set_unbuffered()
        imgui.same_line()
        if button("Line Buffered"):
            service.set_line_buffered()
        imgui.same_line()
        if button("System Default Buffer"):
            service.set_system_default_buffer()
        imgui.same_line()
        if button("Obtain Default Buffer Size"):
            service.set_default_buffer_size()

        if cwd := input_text("Working Directory", service.cwd):
            service.cwd = cwd.value
        if button("Browse Directory"):
            self._cwd_browser.set_location(service.cwd)
            self._cwd_browser.show()
        imgui.same_line()
        if button("Home Directory"):
            service.cwd = str(Path.home())

        if service.cwd:
            if not os.path.exists(service.cwd):
                imgui.same_line()
                imgui.text_colored(self.error_color, "Not exist")
            elif not os.path.isdir(service.cwd):
                imgui.same_line()
                imgui.text_colored(self.error_color, "Not a directory")

        if creation_flags := input_int("Creation flags", service.creation_flags):
            service.creation_flags = creation_flags.value

        if user := input_text("User", service.user):
            service.user = user.value
        if button("Current User Name"):
            service.set_user_name()
        imgui.same_line()
        if button("Current User ID"):
            service.set_user_id()

        if group := input_text("Group", service.group):
            service.group = group.value
        if button("Current Group Name"):
            service.set_group_name()
        imgui.same_line()
        if button("Current Group ID"):
            service.set_group_id()

        if restart_policy := combo_enum("Restart policy", service.restart_policy):
            service.restart_policy = restart_policy.item

        if restart_delay := input_float("Restart delay", service.restart_delay):
            service.restart_delay = restart_delay.item

        if restart_max_attempts := input_int(
            "Restart max attempts",
            service.restart_max_attempts,
        ):
            service.restart_max_attempts = restart_max_attempts.item

        success_exit_codes = input_text(
            "Success exit codes",
            service.join_success_exit_codes(),
        )

        try:
            if success_exit_codes:
                codes = service.split_success_exit_codes(success_exit_codes.value)
                service.success_exit_codes = codes
            self.hovered_tooltip(f"Separate multiple exit codes with commas ({COMMA})")
        except BaseException as e:
            self.hovered_tooltip(e)

        if pid_file := input_text("PID File", service.pid_file):
            service.pid_file = pid_file.value
        if button("Browse PID File"):
            self._pid_file_browser.set_location(service.pid_file)
            self._pid_file_browser.show()

    def do_status_process(self) -> None:
        service = self.selected_service
        assert service is not None

        imgui.text("Service Status")
        imgui.separator()

        input_text_disabled("UUID", service.uuid)
        input_text_disabled("Name", service.name)
