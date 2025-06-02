# -*- coding: utf-8 -*-

import os
import sys
from pathlib import Path
from typing import Optional, Union

from imgui_bundle import imgui

from cvp.assets.fonts.mdi import LOCK, LOCK_OPEN_VARIANT
from cvp.context.context import Context
from cvp.imgui.begin_child import begin_child_context
from cvp.imgui.button import button
from cvp.imgui.checkbox import checkbox
from cvp.imgui.combo_enum import combo_enum
from cvp.imgui.flags.child import AUTO_RESIZE_Y, BORDERS
from cvp.imgui.input_float import input_float
from cvp.imgui.input_int import input_int
from cvp.imgui.input_text import input_text
from cvp.imgui.input_text_multiline import (
    calc_input_text_multiline_with_line_count,
    input_text_multiline,
)
from cvp.imgui.popups.containers import PopupList
from cvp.imgui.popups.open_file import OpenFilePopup
from cvp.imgui.radio_button import radio_button
from cvp.imgui.tooltip import hovered_tooltip_text_wrapped
from cvp.imgui.widgets.table_mutable_mapping import table_mutable_mapping
from cvp.service.item import RestartPolicy, ServiceItem, StreamInfo
from cvp.system.shell import get_default_shell_path
from cvp.variables import COMMA


class ServicesConfigTab:
    _stream_candidate: Optional[StreamInfo]
    _selected_service: Optional[ServiceItem]

    def __init__(self, context: Context, *, args_lines=5):
        self._context = context
        self._args_lines = args_lines

        self._stream_candidate = None
        self._selected_service = None

        self._executable_browser = OpenFilePopup(
            "Select executable file",
            target=self.on_executable_selected,
            mode=OpenFilePopup.Mode.select_file,
        )
        self._cwd_browser = OpenFilePopup(
            "Select working directory",
            target=self.on_cwd_selected,
            mode=OpenFilePopup.Mode.select_directory,
        )
        self._pid_file_browser = OpenFilePopup(
            "Select PID file",
            target=self.on_pid_selected,
            mode=OpenFilePopup.Mode.input_filename,
        )
        self._stdio_file_browser = OpenFilePopup(
            "Select stdio file",
            target=self.on_stdio_selected,
            mode=OpenFilePopup.Mode.input_filename,
        )

        self._popups = PopupList(
            self._executable_browser,
            self._cwd_browser,
            self._pid_file_browser,
            self._stdio_file_browser,
        )

    @property
    def context(self):
        return self._context

    @property
    def popups(self):
        return self._popups

    @property
    def services(self):
        return self.context.services

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

    def text_warning(self, text: str) -> None:
        imgui.text_colored(self.warning_color, text)

    def text_error(self, text: str) -> None:
        imgui.text_colored(self.error_color, text)

    def hovered_tooltip(self, message: Union[str, BaseException]) -> bool:
        if isinstance(message, BaseException):
            return hovered_tooltip_text_wrapped(str(message), self.error_color)
        else:
            assert isinstance(message, str)
            return hovered_tooltip_text_wrapped(message)

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

        assert self._selected_service is not None
        self._selected_service.executable = file
        self._selected_service = None

    def on_cwd_selected(self, file: str) -> None:
        if not file:
            return

        if not os.path.exists(file):
            self.context.toast_error(f"'{file}' does not exist")
            return

        if not os.path.isdir(file):
            self.context.toast_error(f"'{file}' is not a directory")
            return

        assert self._selected_service is not None
        self._selected_service.cwd = file
        self._selected_service = None

    def on_pid_selected(self, file: str) -> None:
        if not file:
            return

        assert self._selected_service is not None
        self._selected_service.pid_file = file
        self._selected_service = None

    def on_stdio_selected(self, file: str) -> None:
        if not file:
            return

        assert self._stream_candidate is not None
        self._stream_candidate.set_none_handle()
        self._stream_candidate.set_file(file)
        self._stream_candidate = None

    def __call__(self, service: ServiceItem) -> None:
        active_service = not self.services.spawnable(service.key)

        if service.managed:
            self.text_warning("Managed services cannot be modified")
        elif active_service:
            self.text_warning("Activated services cannot be modified")
        else:
            freeze_icon = LOCK if service.freeze else LOCK_OPEN_VARIANT
            if freeze := checkbox(freeze_icon, service.freeze):
                service.freeze = freeze.state

            imgui.same_line()
            if service.freeze:
                self.text_success("The service can be controlled")
            else:
                self.text_error("The service cannot be controlled unless it is locked")

        readonly = service.freeze or service.managed or active_service
        imgui.begin_disabled(disabled=readonly)
        try:
            self.do_config_process(service)
        finally:
            imgui.end_disabled()

    def do_config_process(self, service: ServiceItem) -> None:
        if enabled := checkbox("Start Automatically", service.enabled):
            service.enabled = enabled.state
        hovered_tooltip_text_wrapped(
            "When activated, the program will automatically launch at startup",
        )

        if name := input_text("Name", service.name):
            service.name = name.value

        if executable := input_text("Executable", service.executable):
            service.executable = executable.value

        if service.executable:
            self.hovered_tooltip(service.normalize_executable())

        if button("Python Executable"):
            service.executable = sys.executable

        imgui.same_line()
        if button("Default SHELL"):
            service.executable = get_default_shell_path()

        imgui.same_line()
        if button("Browse Executable"):
            self._selected_service = service
            self._executable_browser.set_location(service.normalize_executable())
            self._executable_browser.show()

        imgui.same_line()
        if not service.executable:
            self.text_error("No executable path provided")
        else:
            normalize_executable = service.normalize_executable()
            if not os.path.exists(normalize_executable):
                self.text_error("Executable does not exist")
            elif not os.path.isfile(normalize_executable):
                self.text_error("Executable is not a file")
            elif not os.access(normalize_executable, os.X_OK):
                self.text_error("Executable is not executable")
            else:
                self.text_success("Executable is valid and ready")

        cmds_height = calc_input_text_multiline_with_line_count(self._args_lines)
        if cmds := input_text_multiline("Arguments", service.args, (0, cmds_height)):
            service.args = cmds.value

        try:
            if multiline_arguments := service.multiline_normalize_arguments():
                self.hovered_tooltip(multiline_arguments)
        except BaseException as e:
            self.hovered_tooltip(e)

        if buffer_size := input_int("Buffer Size", service.buffer_size):
            service.buffer_size = buffer_size.value

        if button("Unbuffered"):
            service.set_unbuffered()
        imgui.same_line()
        if button("Line Buffered"):
            service.set_line_buffered()
        imgui.same_line()
        if button("Use System Default"):
            service.set_system_default_buffer()
        imgui.same_line()
        if button("Obtain System Default"):
            service.set_default_buffer_size()

        if self.context.debug:
            self.do_stream_process("Standard input", service, service.stdin)
            self.text_warning("Standard input does not support direct control")

        self.do_stream_process("Standard output", service, service.stdout)
        self.do_stream_process("Standard error", service, service.stderr)

        if cwd := input_text("Working Directory", service.cwd):
            service.cwd = cwd.value

        if button("Home Directory"):
            service.cwd = str(Path.home())
        imgui.same_line()
        if button("CWD"):
            service.cwd = str(Path.cwd())
        self.hovered_tooltip("Current Working Directory")
        imgui.same_line()
        if button("Browse Directory"):
            self._selected_service = service
            self._cwd_browser.set_location(service.cwd)
            self._cwd_browser.show()

        if service.cwd:
            if not os.path.exists(service.cwd):
                imgui.same_line()
                self.text_error("Not exist")
            elif not os.path.isdir(service.cwd):
                imgui.same_line()
                self.text_error("Not a directory")

        with begin_child_context(
            label="EnvChild",
            size=(imgui.calc_item_width(), 0),
            child_flags=AUTO_RESIZE_Y | BORDERS,
        ):
            table_mutable_mapping(
                label="EnvTable",
                container=service.env,
                addable_factory=lambda k, v: (k, v),
                removable=True,
                show_key=True,
                show_value=True,
            )
        imgui.same_line(spacing=imgui.get_style().item_inner_spacing.x)
        imgui.text("Environment variables")

        if self.context.debug:
            if creation_flags := input_int("Creation flags", service.creation_flags):
                service.creation_flags = creation_flags.value
            self.hovered_tooltip("Modifying this value is generally not recommended")

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

        imgui.begin_disabled(service.restart_policy == RestartPolicy.none)
        try:
            if restart_delay := input_float("Restart delay", service.restart_delay):
                service.restart_delay = restart_delay.item
            if restart_max_attempts := input_int(
                "Restart max attempts",
                service.restart_max_attempts,
            ):
                service.restart_max_attempts = restart_max_attempts.item
        finally:
            imgui.end_disabled()

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

        if button("No PID File"):
            service.pid_file = str()
        imgui.same_line()
        if button("Default PID File"):
            pid_file_path = self.services.get_pid_file_path(service.key)
            service.pid_file = str(pid_file_path)
        imgui.same_line()
        if button("Browse PID File"):
            self._selected_service = service
            self._pid_file_browser.set_location(service.pid_file)
            self._pid_file_browser.show()

    def do_stream_process(
        self,
        label: str,
        service: ServiceItem,
        stream: StreamInfo,
    ) -> None:
        with begin_child_context(
            label=f"##StdioChild.{stream.type}",
            size=(imgui.calc_item_width(), 0),
            child_flags=AUTO_RESIZE_Y,
        ):
            if radio_button("DEVNULL", stream.is_devnull):
                stream.set_devnull()

            imgui.same_line()
            imgui.begin_disabled(not stream.is_stderr)
            try:
                if radio_button("Same STDOUT", stream.is_same_standard_output):
                    stream.set_same_standard_output()
            finally:
                imgui.end_disabled()

            imgui.begin_disabled(not self.context.debug)
            try:
                imgui.same_line()
                if radio_button("PIPE", stream.is_pipe):
                    stream.set_pipe()
                self.hovered_tooltip(
                    "PIPE is only supported for programmable subprocesses.\n"
                    "(i.e., managed subprocesses)"
                )
            finally:
                imgui.end_disabled()

            imgui.same_line()
            padded_label = stream.name.upper() + (" " if stream.is_stdin else "")
            if radio_button(padded_label, stream.is_same_type):
                stream.set_default()

            imgui.same_line()
            if radio_button("File", stream.is_file):
                stream.set_none_handle()

            imgui.begin_disabled(not stream.is_file)
            try:
                imgui.same_line()
                if file := input_text(f"##StreamFile.{stream.type}", stream.file):
                    stream.file = file.value
                self.hovered_tooltip(stream.file)
            finally:
                imgui.end_disabled()

            imgui.same_line()
            if button("Generate Log File"):
                log_path = self.services.generate_stream_log_path(service.key, stream)
                stream.set_none_handle()
                stream.set_file(str(log_path))

            imgui.same_line()
            if button("Browse Log File"):
                self._stream_candidate = stream
                if stream.file:
                    self._stdio_file_browser.set_location(stream.file)
                self._stdio_file_browser.show()

        imgui.same_line(spacing=imgui.get_style().item_inner_spacing.x)
        imgui.text(label)
