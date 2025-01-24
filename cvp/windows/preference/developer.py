# -*- coding: utf-8 -*-

import imgui

from cvp.logging.logging import logger
from cvp.renderer.context import RendererContext
from cvp.types.override import override
from cvp.windows.preference._base import PreferenceWidget


class DeveloperPreference(PreferenceWidget):
    def __init__(self, context: RendererContext, label="Developer"):
        self._config = context.config.developer
        self._label = label

    @property
    @override
    def label(self) -> str:
        return self._label

    @property
    def debug(self) -> bool:
        return self._config.debug

    @debug.setter
    def debug(self, value: bool):
        self._config.debug = value

    @property
    def verbose(self) -> int:
        return self._config.verbose

    @verbose.setter
    def verbose(self, value: int):
        self._config.verbose = value

    @override
    def on_process(self) -> None:
        debug_result = imgui.checkbox("Enable Debug Mode", self.debug)

        debug_changed = debug_result[0]
        debug_value = debug_result[1]
        assert isinstance(debug_value, bool)

        if debug_changed:
            self.debug = debug_value
            if debug_value:
                logger.info("Enabled debug mode")
            else:
                logger.info("Disabled debug mode")

        imgui.text("Verbose level:")
        verbose_result = imgui.input_int("##VerboseLevel", self.verbose)

        verbose_changed = verbose_result[0]
        verbose_value = verbose_result[1]
        assert isinstance(verbose_value, int)

        if verbose_changed:
            self.verbose = verbose_value
            logger.info(f"Changed verbose level: {verbose_value}")
