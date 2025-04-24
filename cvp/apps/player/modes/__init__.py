# -*- coding: utf-8 -*-

from typing import List, Union

from imgui_bundle import imgui

from cvp.apps.player.modes.interface import ModeInterface
from cvp.context.context import Context
from cvp.imgui.menu_item_ex import menu_item


class ModeManager:
    def __init__(self, context: Context):
        from cvp.apps.player.modes.chat import ChatMode
        from cvp.apps.player.modes.dashboard import DashboardMode
        from cvp.apps.player.modes.download import DownloadMode
        from cvp.apps.player.modes.flow import FlowMode
        from cvp.apps.player.modes.games.tetrix import TetrixMode
        from cvp.apps.player.modes.medias import MediasMode
        from cvp.apps.player.modes.onvif import OnvifMode
        from cvp.apps.player.modes.preference import PreferenceMode
        from cvp.apps.player.modes.wsdiscovery import WsDiscoveryMode

        self.chat_mode = ChatMode(context)
        self.dashboard_mode = DashboardMode(context)
        self.download_mode = DownloadMode(context)
        self.flow_mode = FlowMode(context)
        self.medias_mode = MediasMode(context)
        self.onvif_mode = OnvifMode(context)
        self.preference_mode = PreferenceMode(context)
        self.tetrix_mode = TetrixMode(context)
        self.wsdiscovery_mode = WsDiscoveryMode(context)

        self._context = context
        self._modes: List[ModeInterface] = [
            self.chat_mode,
            self.dashboard_mode,
            self.download_mode,
            self.flow_mode,
            self.medias_mode,
            self.onvif_mode,
            self.preference_mode,
            self.tetrix_mode,
            self.wsdiscovery_mode,
        ]
        self._key2index = {m.get_mode_name(): i for i, m in enumerate(self._modes)}
        self._num2index = {m.get_mode_number(): i for i, m in enumerate(self._modes)}

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
        self._mode_menu_item(self.dashboard_mode)
        self._mode_menu_item(self.chat_mode)
        self._mode_menu_item(self.flow_mode)
        self._mode_menu_item(self.medias_mode)
        self._mode_menu_item(self.onvif_mode)
        self._mode_menu_item(self.wsdiscovery_mode)

        if imgui.begin_menu("Utils"):
            try:
                self._mode_menu_item(self.download_mode)
            finally:
                imgui.end_menu()

        if imgui.begin_menu("Games"):
            try:
                self._mode_menu_item(self.tetrix_mode)
            finally:
                imgui.end_menu()

        imgui.separator()

        self._mode_menu_item(self.preference_mode)
