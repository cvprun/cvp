# -*- coding: utf-8 -*-

from typing import NamedTuple, Optional
from uuid import uuid4

from cvp.context.mixins._base import BaseContextMixin
from cvp.onvif.client import OnvifClient
from cvp.onvif.declarations import ONVIF_DECLARATIONS
from cvp.onvif.onvif import OnvifConfig
from cvp.strings.is_uuid import is_uuid4
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

    def create_onvif_client(self, config: OnvifConfig, *, append=False):
        assert self._home is not None
        assert self._keyring is not None

        client = OnvifClient(
            config=config,
            root_dir=self._home.onvifs.get_client_root_dir(config.uuid),
            wsdl_cache_dir=self._home.wsdl,
            password=self._keyring.onvif.get(config.uuid),
        )
        if append:
            self._onvifs.add_client(config.uuid, client)
        return client

    def get_onvif_client(self, config: OnvifConfig) -> OnvifClient:
        client = self._onvifs.get_client(config.uuid)
        if client is not None:
            if client.config == config:
                return client
            self._onvifs.pop_client(config.uuid)
        return self.create_onvif_client(config, append=True)

    def initialize_onvif_clients(self) -> None:
        assert self._home is not None
        assert self._keyring is not None

        for config in self._onvifs.values():
            self.create_onvif_client(config, append=True)
