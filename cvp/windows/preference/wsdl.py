# -*- coding: utf-8 -*-

from imgui_bundle import imgui

from cvp.logging.logging import logger
from cvp.renderer.context import RendererContext
from cvp.types.override import override
from cvp.windows.preference._base import PreferenceWidget


class WsdlPreference(PreferenceWidget):
    def __init__(self, context: RendererContext, label="WSDL"):
        self._config = context.config.wsdl
        self._label = label

    @property
    @override
    def label(self) -> str:
        return self._label

    @override
    def on_process(self) -> None:
        no_cache_result = imgui.checkbox("No Cache File", self._config.no_cache)
        no_cache_changed = no_cache_result[0]
        no_cache_value = no_cache_result[1]
        assert isinstance(no_cache_changed, bool)
        assert isinstance(no_cache_value, bool)
        if no_cache_changed:
            self._config.no_cache = no_cache_value
            if no_cache_value:
                logger.info("Do not save the WSDL schema as a file")
            else:
                logger.info("Save the WSDL schema as a file")
