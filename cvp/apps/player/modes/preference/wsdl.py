# -*- coding: utf-8 -*-

from cvp.apps.player.modes.preference._base import BasePreference
from cvp.context.context import Context
from cvp.imgui.checkbox import checkbox
from cvp.logging.logging import logger
from cvp.types.override import override


class WsdlPreference(BasePreference):
    __cvp_menu_name__ = "WSDL"

    def __init__(self, context: Context):
        super().__init__(context)

    @property
    def no_cache(self) -> bool:
        return self.context.config.wsdl.no_cache

    @no_cache.setter
    def no_cache(self, value: bool) -> None:
        self.context.config.wsdl.no_cache = value

    @override
    def do_process(self) -> None:
        if no_cache_result := checkbox("No Cache File", self.no_cache):
            self.no_cache = no_cache_result.state
            if no_cache_result.state:
                logger.info("Do not save the WSDL schema as a file")
            else:
                logger.info("Save the WSDL schema as a file")
