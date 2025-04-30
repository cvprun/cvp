# -*- coding: utf-8 -*-

from collections import OrderedDict
from typing import Sequence, Union

from imgui_bundle import imgui

from cvp.apps.player.modes.interface import ModeInterface, retrieve_mode_instances
from cvp.context.context import Context
from cvp.imgui.menu_item_ex import menu_item


class ModeManager:
    _menu_modes: Sequence[ModeInterface]
    _submenu_modes: OrderedDict[str, Sequence[ModeInterface]]

    def __init__(self, context: Context):
        from cvp.apps.player.modes.canvas import CanvasMode
        from cvp.apps.player.modes.chat import ChatMode
        from cvp.apps.player.modes.crypto.hash import HashMode
        from cvp.apps.player.modes.cv.tracker import ObjectTrackerMode
        from cvp.apps.player.modes.dashboard import DashboardMode
        from cvp.apps.player.modes.encoding.binary_text import BinaryTextMode
        from cvp.apps.player.modes.files import FilesMode
        from cvp.apps.player.modes.flows.dtype import DtypeMode
        from cvp.apps.player.modes.flows.flow import FlowMode
        from cvp.apps.player.modes.flows.node import NodeMode
        from cvp.apps.player.modes.games.tetrix import TetrixMode
        from cvp.apps.player.modes.generators.faker import FakerMode
        from cvp.apps.player.modes.medias import MediasMode
        from cvp.apps.player.modes.network.downloader import DownloaderMode
        from cvp.apps.player.modes.network.sock_map import SockMapMode
        from cvp.apps.player.modes.onvif import OnvifMode
        from cvp.apps.player.modes.preference import PreferenceMode
        from cvp.apps.player.modes.system.terminal import TerminalMode
        from cvp.apps.player.modes.wsdiscovery import WsDiscoveryMode

        # ==============================================================================
        # region: Initialize Mode Instances
        # [IMPORTANT] Do not change the initialize order!

        self.binary_text_mode = BinaryTextMode(context)
        self.canvas_mode = CanvasMode(context)
        self.chat_mode = ChatMode(context)
        self.dashboard_mode = DashboardMode(context)
        self.download_mode = DownloaderMode(context)
        self.dtype_mode = DtypeMode(context)
        self.faker_mode = FakerMode(context)
        self.files_mode = FilesMode(context)
        self.flow_mode = FlowMode(context)
        self.hash_mode = HashMode(context)
        self.medias_mode = MediasMode(context)
        self.node_mode = NodeMode(context)
        self.object_tracker_mode = ObjectTrackerMode(context)
        self.onvif_mode = OnvifMode(context)
        self.preference_mode = PreferenceMode(context)
        self.sock_map = SockMapMode(context)
        self.terminal_mode = TerminalMode(context)
        self.tetrix_mode = TetrixMode(context)
        self.wsdiscovery_mode = WsDiscoveryMode(context)

        # ------------------------------------------------------------------------------
        # Retrieves and stores all ModeInterface instances assigned to `self`
        self._modes = retrieve_mode_instances(self)
        self._key2index = {m.get_mode_name(): i for i, m in enumerate(self._modes)}
        self._num2index = {m.get_mode_number(): i for i, m in enumerate(self._modes)}
        # endregion: Initialize Mode Instances
        # ==============================================================================

        self._context = context
        self._menu_modes = (
            self.dashboard_mode,
            self.chat_mode,
            self.files_mode,
            self.canvas_mode,
            self.medias_mode,
            self.onvif_mode,
            self.wsdiscovery_mode,
        )
        self._submenu_modes = OrderedDict(
            {
                "Computer Vision": (self.object_tracker_mode,),
                "Cryptography": (self.hash_mode,),
                "Encoding": (self.binary_text_mode,),
                "Flows": (self.dtype_mode, self.flow_mode, self.node_mode),
                "Games": (self.tetrix_mode,),
                "Generators": (self.faker_mode,),
                "Network": (self.download_mode, self.sock_map),
                "System": (self.terminal_mode,),
            }
        )

    @property
    def mode_key(self) -> str:
        return self._context.config.appearance.mode

    @mode_key.setter
    def mode_key(self, value: str) -> None:
        self._context.config.appearance.mode = value

    @property
    def default_mode(self):
        return self.dashboard_mode

    def get_mode_with_key(self, key: str) -> ModeInterface:
        index = self._key2index.get(key)
        if index is None:
            raise KeyError(f"Invalid mode key: {key}")
        assert 0 <= index < len(self._modes)
        return self._modes[index]

    def get_mode_with_number(self, number: int) -> ModeInterface:
        index = self._num2index.get(number)
        if index is None:
            raise KeyError(f"Invalid number key: {number}")
        assert 0 <= index < len(self._modes)
        return self._modes[index]

    def get_mode(self, key: Union[str, int]) -> ModeInterface:
        if isinstance(key, str):
            return self.get_mode_with_key(key)
        elif isinstance(key, int):
            return self.get_mode_with_number(key)
        else:
            raise TypeError(f"Unsupported key type: {type(key).__name__}")

    def set_mode_with_key(self, key: str) -> None:
        index = self._key2index.get(key)
        if index is None:
            raise KeyError(f"Invalid mode key: {key}")
        assert 0 <= index < len(self._modes)
        assert self._modes[index].get_mode_name() == key
        self.mode_key = key

    def set_mode_with_number(self, number: int) -> None:
        index = self._num2index.get(number)
        if index is None:
            raise KeyError(f"Invalid number key: {number}")
        assert 0 <= index < len(self._modes)
        self.mode_key = self._modes[index].get_mode_name()

    def set_mode(self, key: Union[str, int]) -> None:
        if isinstance(key, str):
            self.set_mode_with_key(key)
        elif isinstance(key, int):
            self.set_mode_with_number(key)
        else:
            raise TypeError(f"Unsupported key type: {type(key).__name__}")

    @property
    def current_mode(self) -> ModeInterface:
        try:
            return self.get_mode_with_key(self.mode_key)
        except:  # noqa
            return self.default_mode

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
        name = mode.get_mode_name()
        number = mode.get_mode_number()
        selected = name == self.mode_key
        shortcut = f"Alt+{number}" if 0 <= number <= 9 else str()
        enabled = not selected
        if menu_item(name, selected=selected, shortcut=shortcut, enabled=enabled):
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
