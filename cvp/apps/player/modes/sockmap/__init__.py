# -*- coding: utf-8 -*-

from collections import deque
from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum, auto, unique
from socket import SOCK_STREAM, socket
from threading import Event, Lock
from typing import Deque, Final, Iterable, List, Optional, Tuple

from imgui_bundle import imgui

from cvp.apps.player.modes._base import BaseMode
from cvp.assets.fonts.mdi import CLOUD_SEARCH
from cvp.context.context import Context
from cvp.imgui.begin_child import begin_child_context
from cvp.imgui.button import button
from cvp.imgui.fit_size import FIT_SIZE, FIT_WIDTH
from cvp.imgui.flags import table
from cvp.imgui.flags.child import AUTO_RESIZE_Y, BORDERS, RESIZE_X
from cvp.imgui.flags.input_text import ENTER_RETURNS_TRUE
from cvp.imgui.input_float import input_float
from cvp.imgui.input_text import input_text
from cvp.imgui.spinner import spinner
from cvp.imgui.tooltip import hovered_tooltip_text
from cvp.logging.loggers import logger
from cvp.network.address_family import get_ip_address_family, is_ip_address
from cvp.types.override import override


@unique
class SockState(StrEnum):
    reachable = auto()
    error = auto()


@dataclass
class SockResult:
    ip: str
    port: int
    begin: datetime
    end: datetime
    state: SockState
    error: Optional[BaseException] = None

    @property
    def duration(self):
        return self.end - self.begin

    @classmethod
    def from_reachable(cls, ip: str, port: int, begin: datetime):
        return cls(
            ip=ip,
            port=port,
            begin=begin,
            end=datetime.now().astimezone(),
            state=SockState.reachable,
            error=None,
        )

    @classmethod
    def from_error(cls, ip: str, port: int, begin: datetime, error: BaseException):
        return cls(
            ip=ip,
            port=port,
            begin=begin,
            end=datetime.now().astimezone(),
            state=SockState.error,
            error=error,
        )

    def __str__(self):
        return f"{self.ip}:{self.port}"


class SockmapMode(BaseMode):
    __cvp_mode_name__ = "Sockmap"
    __cvp_mode_icon__ = CLOUD_SEARCH

    _LIST_SPLIT_X: Final[int] = 150
    _LIST_CHILD_FLAGS: Final[int] = RESIZE_X | BORDERS

    _TABLE_COLUMNS: Final[int] = 5
    _TABLE_FLAGS: Final[int] = table.BORDERS | table.ROW_BG

    _buffer: Deque[Tuple[str, int]]
    _result: List[SockResult]

    def __init__(self, context: Context):
        super().__init__(context)
        self._discovery_runner = context.create_thread_runner(self.on_discovery_main)
        self._destination_count = 0
        self._cancel = Event()

        self._buffer = deque()
        self._buffer_lock = Lock()

        self._result = list()
        self._result_lock = Lock()

    @property
    def config(self):
        return self.context.config.sockmap

    @property
    def error_color(self):
        return self.context.config.appearance.error_color

    def clear_buffer(self) -> None:
        with self._buffer_lock:
            self._buffer.clear()

    def clear_result(self) -> None:
        with self._result_lock:
            self._result.clear()

    def clear(self):
        self._destination_count = 0
        self._cancel.clear()
        self.clear_buffer()
        self.clear_result()

    def update_buffer(self, infos: Iterable[Tuple[str, int]]) -> None:
        with self._buffer_lock:
            self._buffer.clear()
            self._buffer.extend(infos)

    def pop_buffer(self) -> Optional[Tuple[str, int]]:
        with self._buffer_lock:
            try:
                return self._buffer.popleft()
            except IndexError:
                return None

    def append_result(self, result: SockResult) -> None:
        with self._result_lock:
            self._result.append(result)

    def copy_buffer(self):
        with self._buffer_lock:
            return self._buffer.copy()

    def copy_result(self):
        with self._result_lock:
            return self._result.copy()

    def size_result(self):
        with self._result_lock:
            return len(self._result)

    def run_discovery(self) -> None:
        if self._discovery_runner.running:
            raise ValueError("Sockmap discovery is already running")

        try:
            addrs = self.config.as_list()
            self._cancel.clear()
            self._destination_count = len(addrs)
            self.update_buffer(addrs)
            self.clear_result()

            self._discovery_runner(self.config.timeout)
        except BaseException as e:
            logger.exception(e)
            self.context.toast(f"Discovery failed: '{e}'")

    def resume_discovery(self) -> None:
        if self._discovery_runner.running:
            raise ValueError("Sockmap discovery is already running")

        try:
            self._cancel.clear()
            self._discovery_runner(self.config.timeout)
        except BaseException as e:
            logger.exception(e)
            self.context.toast(f"Discovery failed: '{e}'")

    def on_discovery_main(self, timeout: Optional[float] = None) -> None:
        while ip_port := self.pop_buffer():
            ip, port = ip_port
            assert isinstance(ip, str)
            assert isinstance(port, int)

            begin = datetime.now().astimezone()
            try:
                family = get_ip_address_family(ip)
                sock = socket(family, SOCK_STREAM)
                sock.settimeout(timeout)
                sock.connect((ip, port))
                sock.close()
                self.append_result(SockResult.from_reachable(ip, port, begin))
            except BaseException as e:
                self.append_result(SockResult.from_error(ip, port, begin, e))

            if self._cancel.is_set():
                break

    @override
    def on_process(self) -> None:
        with self.begin_mode_context():
            running = self._discovery_runner.running
            with begin_child_context(
                "Menu",
                size=(FIT_WIDTH, 0),
                child_flags=AUTO_RESIZE_Y,
            ):
                self.do_menu_process(running=running)

            imgui.separator()

            with begin_child_context(
                label="##Buffer",
                size=(self._LIST_SPLIT_X, 0),
                child_flags=self._LIST_CHILD_FLAGS,
            ):
                self.do_buffer_process()
            imgui.same_line()
            with begin_child_context("Result"):
                self.do_result_process()

    def do_menu_process(self, running: bool) -> None:
        imgui.text("Socket Mapping Discovery")
        imgui.separator()

        if running:
            imgui.begin_disabled()
        try:
            addr_begin = input_text(
                "Address begin",
                self.config.address_begin,
                ENTER_RETURNS_TRUE,
            )
            if addr_begin.changed and is_ip_address(addr_begin.value):
                self.config.address_begin = addr_begin.value

            addr_end = input_text(
                "Address end",
                self.config.address_end,
                ENTER_RETURNS_TRUE,
            )
            if addr_end.changed and is_ip_address(addr_end.value):
                self.config.address_end = addr_end.value

            if port_result := input_text("Port range", self.config.port_range):
                self.config.port_range = port_result.value

            if timeout_result := input_float("Timeout", self.config.timeout, step=1.0):
                self.config.timeout = timeout_result.value
            hovered_tooltip_text("Discovery timeout in seconds")

            if button("Reset Default"):
                self.config.reset_defaults()
        finally:
            if running:
                imgui.end_disabled()

        if button("Discovery", disabled=running):
            self.run_discovery()

        complete_count = self.size_result()
        assert complete_count <= self._destination_count

        imgui.same_line()
        if running:
            if self._cancel.is_set():
                button("Canceling ...", disabled=True)
            else:
                if button("Cancel"):
                    self._cancel.set()
        else:
            if complete_count < self._destination_count:
                if button("Resume"):
                    self.resume_discovery()
                imgui.same_line()
                if button("Clear"):
                    self.clear()
            else:
                button("Cancel", disabled=True)

        if running:
            imgui.same_line()
            spinner("Running Spinner")

            imgui.same_line()
            imgui.text(f"{complete_count}/{self._destination_count}")

    def do_buffer_process(self) -> None:
        if imgui.begin_list_box("##List", FIT_SIZE):
            try:
                for addr in self.copy_buffer():
                    ip, port = addr
                    imgui.selectable(f"{ip}:{port}", False)
            finally:
                imgui.end_list_box()

    def do_result_process(self) -> None:
        if imgui.begin_table("##Table", self._TABLE_COLUMNS, self._TABLE_FLAGS):
            try:
                imgui.table_setup_column("IP")
                imgui.table_setup_column("Port")
                imgui.table_setup_column("State")
                imgui.table_setup_column("Duration")
                imgui.table_setup_column("Error")
                imgui.table_headers_row()

                for info in self.copy_result():
                    imgui.table_next_row()
                    self.table_result_row(info)
            finally:
                imgui.end_table()

    def table_result_row(self, info: SockResult) -> None:
        imgui.table_set_column_index(0)
        imgui.text(info.ip)

        imgui.table_set_column_index(1)
        imgui.text(str(info.port))

        imgui.table_set_column_index(2)
        imgui.text(str(info.state))

        imgui.table_set_column_index(3)
        duration = info.duration.total_seconds()
        imgui.text(f"{duration:.02f}s")

        imgui.table_set_column_index(4)
        if info.error is not None:
            imgui.text_colored(self.error_color, str(info.error))
        else:
            imgui.text("No Error")
