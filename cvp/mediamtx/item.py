# -*- coding: utf-8 -*-

from copy import copy, deepcopy
from enum import StrEnum, auto, unique
from typing import Any, Dict, List, NewType, Optional, Sequence, Tuple
from uuid import uuid4

from httpx import Response, Timeout
from type_serialize import Serializable

from cvp.mediamtx.client import Error, GlobalConf, MediamtxApi, Path, PathList
from cvp.types.override import override
from cvp.variables import TIMEOUT_INFINITE

MediamtxKey = NewType("MediamtxKey", str)


class MediamtxItem(Serializable):
    @unique
    class _Keys(StrEnum):
        uuid = auto()
        name_ = "name"
        url = auto()
        headers = auto()
        follow_redirects = auto()
        verify = auto()
        timeout = auto()
        config = auto()
        paths = auto()

    def __init__(
        self,
        uuid: Optional[str] = None,
        name: Optional[str] = None,
        url: Optional[str] = None,
        headers: Optional[Sequence[Tuple[str, str]]] = None,
        follow_redirects=True,
        verify=True,
        timeout=TIMEOUT_INFINITE,
        config: Optional[GlobalConf] = None,
        paths: Optional[PathList] = None,
    ):
        self.uuid = uuid if uuid else str(uuid4())
        self.name = name if name else str()
        self.url = url if url else str()
        self.headers = list(headers if headers else ())
        self.follow_redirects = follow_redirects
        self.verify = verify
        self.timeout = timeout
        self._config = config
        self._paths = paths

    def headers_as_dict(self) -> Dict[str, str]:
        return {str(k): str(v) for k, v in self.headers}

    def __eq__(self, other) -> bool:
        if not isinstance(other, type(self)):
            return False
        return (
            self.uuid == other.uuid
            and self.name == other.name
            and self.url == other.url
            and self.headers == other.headers
            and self.follow_redirects == other.follow_redirects
            and self.verify == other.verify
            and self.timeout == other.timeout
            and self._config == other._config
            and self._paths == other._paths
        )

    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result.uuid = copy(self.uuid)
        result.name = copy(self.name)
        result.url = copy(self.url)
        result.headers = copy(self.headers)
        result.follow_redirects = copy(self.follow_redirects)
        result.verify = copy(self.verify)
        result.timeout = copy(self.timeout)
        result._config = copy(self._config)
        result._paths = copy(self._paths)
        return result

    def __deepcopy__(self, memo: Optional[Dict[int, Any]] = None):
        if memo is None:
            memo = dict()
        cls = self.__class__
        result = cls.__new__(cls)
        result.uuid = deepcopy(self.uuid, memo)
        result.name = deepcopy(self.name, memo)
        result.url = deepcopy(self.url, memo)
        result.headers = deepcopy(self.headers, memo)
        result.follow_redirects = deepcopy(self.follow_redirects, memo)
        result.verify = deepcopy(self.verify, memo)
        result.timeout = deepcopy(self.timeout, memo)
        result._config = deepcopy(self._config, memo)
        result._paths = deepcopy(self._paths, memo)
        memo[id(self)] = result
        return result

    @override
    def __serialize__(self) -> Any:
        config_obj = self._config.model_dump(by_alias=True) if self._config else None
        paths_obj = self._paths.model_dump(by_alias=True) if self._paths else None
        return {
            str(self._Keys.uuid): self.uuid,
            str(self._Keys.name_): self.name,
            str(self._Keys.url): self.url,
            str(self._Keys.headers): self.headers_as_dict(),
            str(self._Keys.follow_redirects): self.follow_redirects,
            str(self._Keys.verify): self.verify,
            str(self._Keys.timeout): self.timeout,
            str(self._Keys.config): config_obj,
            str(self._Keys.paths): paths_obj,
        }

    @override
    def __deserialize__(self, data: Any) -> None:
        if not isinstance(data, dict):
            raise TypeError(f"Unexpected data type: {type(data).__name__}")

        self.uuid = str(data.get(self._Keys.uuid, str()))
        self.name = str(data.get(self._Keys.name_, str()))
        self.url = str(data.get(self._Keys.url, str()))

        headers = data.get(self._Keys.headers, dict())
        self.headers = list((str(k), str(v)) for k, v in headers.items())

        self.follow_redirects = bool(data.get(self._Keys.follow_redirects, True))
        self.verify = bool(data.get(self._Keys.verify, True))
        self.timeout = float(data.get(self._Keys.timeout, TIMEOUT_INFINITE))

        config = data.get(self._Keys.config)
        if config is not None:
            self._config = GlobalConf.model_validate(config)
        else:
            self._config = None

        paths = data.get(self._Keys.paths)
        if paths is not None:
            self._paths = PathList.model_validate(paths)
        else:
            self._paths = None

    @property
    def key(self):
        return MediamtxKey(self.uuid)

    @key.setter
    def key(self, value: MediamtxKey) -> None:
        self.uuid = str(value)

    @property
    def config(self):
        return self._config

    @property
    def paths(self):
        return self._paths

    @property
    def path_names(self) -> List[str]:
        if not self._paths:
            return list()
        return list(path.name for path in self._paths.items)

    @property
    def client(self):
        return MediamtxApi(
            base_url=self.url,
            headers=self.headers_as_dict(),
            verify=self.verify,
            timeout=Timeout(self.timeout) if 0 < self.timeout else None,
            follow_redirects=self.follow_redirects,
        )

    def update_global_config(self) -> None:
        self._config = None
        response = self.client.configGlobalGet()
        if isinstance(response, GlobalConf):
            self._config = response
        elif isinstance(response, Error):
            raise ValueError(response.error)
        elif isinstance(response, Response):
            raise ValueError(str(response.status_code))
        else:
            assert False, "Inaccessible section"

    def update_paths(self, page=0, items_per_page=100) -> None:
        self._paths = None
        response = self.client.pathsList(page, items_per_page)
        if isinstance(response, PathList):
            self._paths = response
        elif isinstance(response, Error):
            raise ValueError(response.error)
        elif isinstance(response, Response):
            raise ValueError(str(response.status_code))
        else:
            assert False, "Inaccessible section"

    def get_path(self, name: str) -> Optional[Path]:
        if not self._paths:
            return None
        for item in self._paths.items:
            if item.name == name:
                return item
        return None
