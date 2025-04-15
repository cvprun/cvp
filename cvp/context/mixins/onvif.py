# -*- coding: utf-8 -*-

from typing import NamedTuple, Optional

from cvp.context.mixins._base import BaseContextMixin
from cvp.onvif.declarations import ONVIF_DECLARATIONS
from cvp.wsdl.loader import load_wsdl_declarations


class OnvifMixin(BaseContextMixin):
    @property
    def _preload_onvif_declarations_runner(self):
        return self.get_thread_runner(self.__on_preload_onvif_declarations)

    @staticmethod
    def __on_preload_onvif_declarations() -> int:
        return load_wsdl_declarations(*ONVIF_DECLARATIONS)

    class _PreloadOnvifDeclarationsStatus(NamedTuple):
        has_error: bool
        error_message: str
        running: bool
        preload_count: Optional[int]

    def get_preload_onvif_declarations_status(self):
        return self._PreloadOnvifDeclarationsStatus(
            has_error=bool(self._preload_onvif_declarations_runner.error),
            error_message=str(self._preload_onvif_declarations_runner.error),
            running=self._preload_onvif_declarations_runner.running,
            preload_count=self._preload_onvif_declarations_runner.result,
        )

    @property
    def preload_onvif_declarations(self):
        return self.get_thread_runner(self.__on_preload_onvif_declarations)

    @property
    def is_onvif_declaration_ready(self) -> bool:
        preload_count = self._preload_onvif_declarations_runner.result
        if preload_count is None:
            return False
        assert isinstance(preload_count, int)
        return preload_count == len(ONVIF_DECLARATIONS)
