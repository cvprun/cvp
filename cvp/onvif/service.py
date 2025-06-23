# -*- coding: utf-8 -*-

from typing import Any, Dict, Final, List, Optional, Tuple, TypedDict

from cvp.network.uri.parser import replace_netloc
from cvp.resources.formats.json import JsonFormatPath

DeviceBinding: Final[str] = "DeviceBinding"
GetServices: Final[str] = "GetServices"


class OnvifVersion(TypedDict):
    Major: int
    Minor: int


class Service(TypedDict):
    Namespace: str
    XAddr: str
    Version: OnvifVersion
    Capabilities: Any


class GetServicesResponse(List[Service]):
    pass


class OnvifServiceMapper(Dict[str, Service]):
    def __init__(
        self,
        uuid: str,
        same_host: bool,
        address: str,
        jsons: JsonFormatPath,
        *,
        binding_name=DeviceBinding,
        operation_name=GetServices,
    ):
        super().__init__()
        self._uuid = uuid
        self._same_host = same_host
        self._address = address
        self._jsons = jsons
        self._binding_name = binding_name
        self._operation_name = operation_name

    @property
    def cache_args(self) -> Tuple[str, str, str]:
        return self._uuid, self._binding_name, self._operation_name

    def has_cache(self) -> bool:
        return self._jsons.has_object(*self.cache_args)

    def read_cache(self) -> GetServicesResponse:
        return self._jsons.read_object(*self.cache_args)

    def update_with_cache(self) -> None:
        if not self.has_cache():
            return
        self.update_with_response(self.read_cache())

    def update_with_response(self, response: GetServicesResponse) -> None:
        for service in response:
            self.__setitem__(service["Namespace"], service)

    def get_address(self, namespace: str) -> Optional[str]:
        service = self.get(namespace)
        if service is None:
            return None

        if not self._same_host:
            return service["XAddr"]

        return replace_netloc(service["XAddr"], self._address)
