# -*- coding: utf-8 -*-

from cvp.apps.player.modes.preference._base import BasePreference
from cvp.context.context import Context
from cvp.imgui.checkbox import checkbox
from cvp.imgui.input_int import input_int
from cvp.logging.logging import logger
from cvp.types.override import override


class DeveloperPreference(BasePreference):
    __cvp_menu_name__ = "Developer"

    def __init__(self, context: Context):
        super().__init__(context)

    @property
    def config(self):
        return self.context.config.developer

    @property
    def debug(self) -> bool:
        return self.config.debug

    @debug.setter
    def debug(self, value: bool):
        self.config.debug = value

    @property
    def verbose(self) -> int:
        return self.config.verbose

    @verbose.setter
    def verbose(self, value: int):
        self.config.verbose = value

    @override
    def do_process(self) -> None:
        if debug_result := checkbox("Enable Debug Mode", self.debug):
            self.debug = debug_result.state
            if debug_result.state:
                logger.info("Enabled debug mode")
            else:
                logger.info("Disabled debug mode")

        if verbose_result := input_int("Verbose Level", self.verbose):
            self.verbose = verbose_result.value
            logger.info(f"Changed verbose level: {verbose_result.value}")
