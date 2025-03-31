# -*- coding: utf-8 -*-

from imgui_bundle import imgui

from cvp.apps.player.modes.preference._base import BasePreference
from cvp.containers.immutable_list import ImmutableList
from cvp.keyring.details import list_keyring_names, load_keyring, set_keyring
from cvp.logging.logging import logger
from cvp.renderer.context import Context
from cvp.types.override import override
from cvp.variables import NOT_FOUND_INDEX


class Keyring(BasePreference):
    def __init__(self, context: Context):
        super().__init__(context)
        self._keyring_names = ImmutableList(list_keyring_names())

    @property
    def keyring_backend(self) -> str:
        return self.context.config.keyring.backend

    @keyring_backend.setter
    def keyring_backend(self, value: str) -> None:
        self.context.config.keyring.backend = value

    @property
    def keyring_backend_index(self) -> int:
        try:
            return self._keyring_names.index(self.keyring_backend)
        except ValueError:
            return NOT_FOUND_INDEX

    @override
    def do_process(self) -> None:
        backend_index = self.keyring_backend_index
        backend_result = imgui.combo("Backend", backend_index, self._keyring_names)
        backend_changed, backend_index = backend_result
        assert isinstance(backend_changed, bool)
        assert isinstance(backend_index, int)

        if backend_changed and 0 <= backend_index < len(self._keyring_names):
            try:
                backend_name = self._keyring_names[backend_index]
                set_keyring(load_keyring(backend_name))
            except BaseException as e:
                logger.error(f"Changed backend error: {e}")
            else:
                logger.info(f"Changed backend: '{backend_name}'")
                self.keyring_backend = backend_name
