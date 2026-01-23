# -*- coding: utf-8 -*-

from collections import OrderedDict
from typing import Sequence

from imgui_bundle import imgui

from cvp.apps.player.modes.interface import ModeInterface, retrieve_mode_instances
from cvp.assets.fonts import mdi
from cvp.context.context import Context
from cvp.imgui.menu_item import menu_item


class ModeManager:
    _menu_modes: Sequence[ModeInterface]
    _submenu_modes: OrderedDict[str, Sequence[ModeInterface]]

    def __init__(self, context: Context):
        from cvp.apps.player.modes.binary import BinaryMode
        from cvp.apps.player.modes.calibration import CalibrationMode
        from cvp.apps.player.modes.canvas import CanvasMode
        from cvp.apps.player.modes.case import CaseMode
        from cvp.apps.player.modes.chat import ChatMode
        from cvp.apps.player.modes.datasets import DatasetsMode
        from cvp.apps.player.modes.downloader import DownloaderMode
        from cvp.apps.player.modes.faker import FakerMode
        from cvp.apps.player.modes.files import FilesMode
        from cvp.apps.player.modes.flow import FlowMode
        from cvp.apps.player.modes.font import FontMode
        from cvp.apps.player.modes.games.minidun import MinidunMode
        from cvp.apps.player.modes.games.tetrix import TetrixMode
        from cvp.apps.player.modes.hash import HashMode
        from cvp.apps.player.modes.hub import HubMode
        from cvp.apps.player.modes.image import ImageMode
        from cvp.apps.player.modes.logging import LoggingMode
        from cvp.apps.player.modes.main.layout import MainLayout
        from cvp.apps.player.modes.map import MapMode
        from cvp.apps.player.modes.mediamtx import MediaMTXMode
        from cvp.apps.player.modes.medias import MediasMode
        from cvp.apps.player.modes.modbus import ModbusMode
        from cvp.apps.player.modes.onvif import OnvifMode
        from cvp.apps.player.modes.preference import PreferenceMode
        from cvp.apps.player.modes.processes import ProcessesMode
        from cvp.apps.player.modes.qrcode import QrCodeMode
        from cvp.apps.player.modes.scheduler import SchedulerMode
        from cvp.apps.player.modes.services import ServicesMode
        from cvp.apps.player.modes.sockmap import SockmapMode
        from cvp.apps.player.modes.swagger import SwaggerMode
        from cvp.apps.player.modes.system import SystemMode
        from cvp.apps.player.modes.tail import TailMode
        from cvp.apps.player.modes.terminal import TerminalMode
        from cvp.apps.player.modes.text import TextMode
        from cvp.apps.player.modes.timezone import TimeZoneMode
        from cvp.apps.player.modes.tracker import ObjectTrackerMode
        from cvp.apps.player.modes.video import VideoMode
        from cvp.apps.player.modes.watchdog import WatchdogMode
        from cvp.apps.player.modes.wsdiscovery import WsDiscoveryMode

        self._main_layout = MainLayout(context)

        # ==============================================================================
        # region: Initialize Mode Instances
        # [IMPORTANT] Do not change the initialize order!

        self.binary_mode = BinaryMode(context)
        self.calibration_mode = CalibrationMode(context)
        self.canvas_mode = CanvasMode(self._main_layout)
        self.case_mode = CaseMode(context)
        self.chat_mode = ChatMode(context)
        self.datasets_mode = DatasetsMode(context)
        self.download_mode = DownloaderMode(context)
        self.faker_mode = FakerMode(context)
        self.files_mode = FilesMode(context)
        self.flow_mode = FlowMode(self._main_layout)
        self.font_mode = FontMode(context)
        self.hash_mode = HashMode(context)
        self.hub_mode = HubMode(context)
        self.image_mode = ImageMode(context)
        self.logging_mode = LoggingMode(context)
        self.map_mode = MapMode(context)
        self.mediamtx_mode = MediaMTXMode(context)
        self.medias_mode = MediasMode(context)
        self.minidun_mode = MinidunMode(context)
        self.modbus_mode = ModbusMode(context)
        self.object_tracker_mode = ObjectTrackerMode(context)
        self.onvif_mode = OnvifMode(context)
        self.preference_mode = PreferenceMode(context)
        self.processes_mode = ProcessesMode(context)
        self.qrcode_mode = QrCodeMode(context)
        self.scheduler_mode = SchedulerMode(context)
        self.services_mode = ServicesMode(context)
        self.sockmap_mode = SockmapMode(context)
        self.swagger_mode = SwaggerMode(context)
        self.system_mode = SystemMode(context)
        self.tail_mode = TailMode(context)
        self.terminal_mode = TerminalMode(context)
        self.tetrix_mode = TetrixMode(context)
        self.text_mode = TextMode(context)
        self.timezone_mode = TimeZoneMode(context)
        self.video_mode = VideoMode(context)
        self.watchdog_mode = WatchdogMode(context)
        self.wsdiscovery_mode = WsDiscoveryMode(context)

        # ------------------------------------------------------------------------------
        # Retrieves and stores all ModeInterface instances assigned to `self`
        self._modes = retrieve_mode_instances(self)
        self._name2index = {m.get_mode_name(): i for i, m in enumerate(self._modes)}
        # endregion: Initialize Mode Instances
        # ==============================================================================

        self._context = context
        self._menu_modes = (
            self.binary_mode,
            self.calibration_mode,
            self.canvas_mode,
            self.case_mode,
            self.chat_mode,
            self.download_mode,
            self.faker_mode,
            self.files_mode,
            self.flow_mode,
            self.font_mode,
            self.hash_mode,
            self.hub_mode,
            self.image_mode,
            self.logging_mode,
            self.video_mode,
            self.map_mode,
            self.mediamtx_mode,
            self.medias_mode,
            self.modbus_mode,
            self.object_tracker_mode,
            self.onvif_mode,
            self.processes_mode,
            self.qrcode_mode,
            self.scheduler_mode,
            self.services_mode,
            self.sockmap_mode,
            self.swagger_mode,
            self.system_mode,
            self.tail_mode,
            self.terminal_mode,
            self.text_mode,
            self.timezone_mode,
            self.watchdog_mode,
            self.wsdiscovery_mode,
        )
        self._submenu_modes = OrderedDict(
            {
                f"{mdi.NINTENDO_GAME_BOY} Games": (self.tetrix_mode, self.minidun_mode),
            }
        )

    def __iter__(self):
        return self._modes.__iter__()

    def __len__(self):
        return self._modes.__len__()

    @property
    def mode_key(self) -> str:
        return self._context.config.navigation.mode

    @mode_key.setter
    def mode_key(self, value: str) -> None:
        self._context.config.navigation.mode = value

    def find_mode_index(self, key: str) -> int:
        index = self._name2index.get(key)
        if index is None:
            raise KeyError(f"Invalid mode key: {key}")
        assert 0 <= index < len(self._modes)
        return index

    def find_mode(self, key: str) -> ModeInterface:
        return self._modes[self.find_mode_index(key)]

    @property
    def current_mode(self) -> ModeInterface:
        try:
            return self.find_mode(self.mode_key)
        except:  # noqa
            return self.flow_mode

    @property
    def min_index(self) -> int:
        assert 1 <= len(self._modes)
        return 0

    @property
    def max_index(self) -> int:
        assert 1 <= len(self._modes)
        return len(self._modes) - 1

    def calc_index(self, offset=1) -> int:
        index = self.find_mode_index(self.mode_key) + offset
        if index < self.min_index:
            return self.min_index
        elif self.max_index < index:
            return self.max_index
        else:
            assert 0 <= index < len(self._modes)
            return index

    def select_prev_mode(self, offset=1) -> None:
        self.set_mode_with_index(self.calc_index(offset * -1))

    def select_next_mode(self, offset=1) -> None:
        self.set_mode_with_index(self.calc_index(offset))

    def set_mode_with_index(self, index: int) -> None:
        if not (0 <= index < len(self._modes)):
            raise IndexError(f"Invalid mode index: {index}")
        self.mode_key = self._modes[index].get_mode_name()

    def prev_mode(self, *, raise_errors=False) -> None:
        prev_index = self.find_mode_index(self.mode_key) - 1
        try:
            self.set_mode_with_index(prev_index)
        except IndexError:
            if raise_errors:
                raise

    def next_mode(self, *, raise_errors=False) -> None:
        next_index = self.find_mode_index(self.mode_key) + 1
        try:
            self.set_mode_with_index(next_index)
        except IndexError:
            if raise_errors:
                raise

    @property
    def layout_preference_menu(self):
        return self.preference_mode.layout_menu

    @property
    def layout_filenames(self):
        return self.preference_mode.layout_menu.filenames

    def save_new_layout(self, *, select=False, reload=False) -> None:
        self.preference_mode.layout_menu.save_new_layout(select=select, reload=reload)

    def load_layout(self, filename: str) -> None:
        self.preference_mode.layout_menu.load_layout(filename)

    def _mode_menu_item(self, mode: ModeInterface) -> None:
        show = mode.get_mode_show()
        icon = mode.get_mode_icon()
        name = mode.get_mode_name()

        if not show:
            return

        label = f"{icon} {name}"
        number = -1  # mode.get_mode_number()
        selected = name == self.mode_key
        shortcut = f"Alt+{number}" if 0 <= number <= 9 else None
        enabled = not selected
        if menu_item(label, selected=selected, shortcut=shortcut, enabled=enabled):
            self.mode_key = name

    def do_menu_process(self) -> None:
        for menu_mode in self._menu_modes:
            self._mode_menu_item(menu_mode)

        for submenu, menu_modes in self._submenu_modes.items():
            if imgui.begin_menu(submenu):
                try:
                    for menu_mode in menu_modes:
                        self._mode_menu_item(menu_mode)
                finally:
                    imgui.end_menu()

        imgui.separator()
        self._mode_menu_item(self.preference_mode)
