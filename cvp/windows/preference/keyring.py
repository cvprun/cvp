# -*- coding: utf-8 -*-

import imgui

from cvp.keyring.keyring import list_keyring_names, load_keyring, set_keyring
from cvp.logging.logging import logger
from cvp.renderer.context import RendererContext
from cvp.types.override import override
from cvp.windows.preference._base import PreferenceWidget


class KeyringPreference(PreferenceWidget):
    def __init__(self, context: RendererContext, label="Keyring"):
        self._config = context.config.keyring
        self._label = label
        self._backends = list_keyring_names()

    @property
    @override
    def label(self) -> str:
        return self._label

    @property
    def backend(self) -> str:
        return self._config.backend

    @backend.setter
    def backend(self, value: str):
        self._config.backend = value

    @property
    def backend_index(self) -> int:
        try:
            return self._backends.index(self._config.backend)
        except ValueError:
            return -1

    @override
    def on_process(self) -> None:
        imgui.text("Backend:")
        backend_result = imgui.combo("##Backend", self.backend_index, self._backends)

        backend_changed = backend_result[0]
        backend_index = backend_result[1]
        assert isinstance(backend_index, int)

        if backend_changed and 0 <= backend_index < len(self._backends):
            backend_value = self._backends[backend_index]
            try:
                set_keyring(load_keyring(backend_value))
            except BaseException as e:
                logger.error(f"Changed backend error: {e}")
            else:
                logger.info(f"Changed backend: '{backend_value}'")
                self.backend = backend_value
