# -*- coding: utf-8 -*-

from copy import deepcopy
from typing import Optional, ParamSpec, Sequence, TypeVar

from requests import Session
from requests.auth import HTTPBasicAuth, HTTPDigestAuth
from zeep import Transport

from cvp.logging.logging import onvif_logger as logger
from cvp.onvif.declarations import (
    ONVIF_ANALYTICS,
    ONVIF_DEVICEIO,
    ONVIF_DEVICEMGMT,
    ONVIF_EVENTS,
    ONVIF_IMAGING,
    ONVIF_MEDIA,
    ONVIF_NOTIFICATION,
    ONVIF_PTZ,
    ONVIF_PULLPOINT,
    ONVIF_RECEIVER,
    ONVIF_RECODING,
    ONVIF_REPLAY,
    ONVIF_SEARCH,
    ONVIF_SUBSCRIPTION,
    WsdlDeclaration,
)
from cvp.onvif.onvif import OnvifConfig
from cvp.onvif.service import OnvifServiceMapper
from cvp.resources.formats.json import JsonFormatPath
from cvp.resources.subdirs.wsdl import WsdlPath
from cvp.wsdl.cache import ZeepFileCache
from cvp.wsdl.client import WsdlClient
from cvp.wsdl.wsse import create_username_token

WsdlRequestParam = ParamSpec("WsdlRequestParam")
WsdlResponseT = TypeVar("WsdlResponseT")
WsdlServiceT = TypeVar("WsdlServiceT", bound=WsdlClient)


class OnvifClient:
    def __init__(
        self,
        config: OnvifConfig,
        root_dir: JsonFormatPath,
        wsdl_cache_dir: Optional[WsdlPath] = None,
        password: Optional[str] = None,
    ):
        self._config = deepcopy(config)
        self._root_dir = root_dir

        if config.use_wsse:
            with_http_basic = config.is_http_basic
            with_http_digest = config.is_http_digest
            username = config.username
            password = password  # keyring.onvif.get(config.uuid)
            use_digest = config.encode_digest
        else:
            with_http_basic = False
            with_http_digest = False
            username = None
            password = None
            use_digest = False

        cache_dir = str(wsdl_cache_dir) if wsdl_cache_dir else None
        no_cache = self._config.no_file_cache or not cache_dir

        self._session = Session()
        self._session.verify = not config.no_verify
        self._cache = None if no_cache else ZeepFileCache(cache_dir)
        self._wsse = create_username_token(username, password, use_digest)
        self._transport = Transport(cache=self._cache, session=self._session)

        if self._wsse is not None:
            assert username is not None
            assert password is not None
            if with_http_basic and with_http_digest:
                raise ValueError(
                    "The 'with_http_basic' and 'with_http_digest' flags cannot coexist"
                )
            if with_http_basic:
                assert not with_http_digest
                self._session.auth = HTTPBasicAuth(username, password)
            if with_http_digest:
                assert not with_http_basic
                if not use_digest:
                    logger.warning("<UsernameToken> should be encoded as a digest.")
                self._session.auth = HTTPDigestAuth(username, password)

        self._services = OnvifServiceMapper(
            uuid=self._config.uuid,
            same_host=self._config.same_host,
            address=self._config.address,
            jsons=self._root_dir,
        )
        self._services.update_with_cache()

        self.devicemgmt = self.create_wsdl(ONVIF_DEVICEMGMT, self._config.address)
        self.analytics = self.create_wsdl(ONVIF_ANALYTICS)
        self.deviceio = self.create_wsdl(ONVIF_DEVICEIO)
        self.events = self.create_wsdl(ONVIF_EVENTS)
        self.imaging = self.create_wsdl(ONVIF_IMAGING)
        self.media = self.create_wsdl(ONVIF_MEDIA)
        self.notification = self.create_wsdl(ONVIF_NOTIFICATION)
        self.ptz = self.create_wsdl(ONVIF_PTZ)
        self.pullpoint = self.create_wsdl(ONVIF_PULLPOINT)
        self.receiver = self.create_wsdl(ONVIF_RECEIVER)
        self.recording = self.create_wsdl(ONVIF_RECODING)
        self.replay = self.create_wsdl(ONVIF_REPLAY)
        self.search = self.create_wsdl(ONVIF_SEARCH)
        self.subscription = self.create_wsdl(ONVIF_SUBSCRIPTION)

    @property
    def wsdls(self) -> Sequence[WsdlClient]:
        return (
            self.devicemgmt,
            self.analytics,
            self.deviceio,
            self.events,
            self.imaging,
            self.media,
            self.notification,
            self.ptz,
            self.pullpoint,
            self.receiver,
            self.recording,
            self.replay,
            self.search,
            self.subscription,
        )

    @property
    def uuid(self):
        return self._config.uuid

    def create_wsdl(
        self,
        declaration: WsdlDeclaration,
        address: Optional[str] = None,
        *,
        update_onvif_ns_prefixes=False
    ):
        if address is None and self._services:
            address = self._services.get_address(declaration.namespace)

        result = WsdlClient(
            jsons=self._root_dir,
            uuid=self._config.uuid,
            declaration=declaration,
            wsse=self._wsse,
            transport=self._transport,
            address=address,
        )

        if update_onvif_ns_prefixes:
            client = result.client
            client.set_ns_prefix("tds", "http://www.onvif.org/ver10/device/wsdl")
            client.set_ns_prefix("tev", "http://www.onvif.org/ver10/events/wsdl")
            client.set_ns_prefix("timg", "http://www.onvif.org/ver20/imaging/wsdl")
            client.set_ns_prefix("tmd", "http://www.onvif.org/ver10/deviceIO/wsdl")
            client.set_ns_prefix("tptz", "http://www.onvif.org/ver20/ptz/wsdl")
            client.set_ns_prefix("ttr", "http://www.onvif.org/ver10/media/wsdl")
            client.set_ns_prefix("ter", "http://www.onvif.org/ver10/error")

        return result

    @property
    def config(self):
        return self._config

    @property
    def services(self):
        return self._services

    def update_services(self) -> None:
        response = self.devicemgmt.GetServices(IncludeCapability=False)
        self._services.update_with_response(response)

    def update_wsdl_addresses(self) -> None:
        for wsdl in self.wsdls:
            address = self._services.get_address(wsdl.namespace)
            if address is None:
                continue
            wsdl.address = address
