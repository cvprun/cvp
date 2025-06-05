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
        from cvp.apps.player.modes.games.tetrix import TetrixMode
        from cvp.apps.player.modes.hash import HashMode
        from cvp.apps.player.modes.image import ImageMode
        from cvp.apps.player.modes.main.layout import MainLayout
        from cvp.apps.player.modes.mediamtx import MediaMTXMode
        from cvp.apps.player.modes.medias import MediasMode
        from cvp.apps.player.modes.onvif import OnvifMode
        from cvp.apps.player.modes.preference import PreferenceMode
        from cvp.apps.player.modes.qrcode import QrCodeMode
        from cvp.apps.player.modes.services import ServicesMode
        from cvp.apps.player.modes.sockmap import SockmapMode
        from cvp.apps.player.modes.swagger import SwaggerMode
        from cvp.apps.player.modes.system import SystemMode
        from cvp.apps.player.modes.terminal import TerminalMode
        from cvp.apps.player.modes.threading import ThreadingMode
        from cvp.apps.player.modes.tracker import ObjectTrackerMode
        from cvp.apps.player.modes.video import VideoPlayerMode
        from cvp.apps.player.modes.watchdog import WatchdogMode
        from cvp.apps.player.modes.wsdiscovery import WsDiscoveryMode

        self._main_layout = MainLayout(context)

        # ==============================================================================
        # region: Initialize Mode Instances
        # [IMPORTANT] Do not change the initialize order!

        self.binary_text_mode = BinaryMode(context)
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
        self.image_mode = ImageMode(context)
        self.media_player_mode = VideoPlayerMode(context)
        self.mediamtx_mode = MediaMTXMode(context)
        self.medias_mode = MediasMode(context)
        self.object_tracker_mode = ObjectTrackerMode(context)
        self.onvif_mode = OnvifMode(context)
        self.preference_mode = PreferenceMode(context)
        self.qrcode_mode = QrCodeMode(context)
        self.services_mode = ServicesMode(context)
        self.sockmap_mode = SockmapMode(context)
        self.swagger_mode = SwaggerMode(context)
        self.system_mode = SystemMode(context)
        self.terminal_mode = TerminalMode(context)
        self.tetrix_mode = TetrixMode(context)
        self.threading_mode = ThreadingMode(context)
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
            self.binary_text_mode,
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
            self.image_mode,
            self.media_player_mode,
            self.mediamtx_mode,
            self.medias_mode,
            self.object_tracker_mode,
            self.onvif_mode,
            self.qrcode_mode,
            self.services_mode,
            self.sockmap_mode,
            self.swagger_mode,
            self.system_mode,
            self.terminal_mode,
            self.threading_mode,
            self.watchdog_mode,
            self.wsdiscovery_mode,
        )
        self._submenu_modes = OrderedDict(
            {
                f"{mdi.NINTENDO_GAME_BOY} Games": (self.tetrix_mode,),
            }
        )

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
        icon = mode.get_mode_icon()
        name = mode.get_mode_name()
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
