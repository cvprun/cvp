# -*- coding: utf-8 -*-

from copy import copy, deepcopy
from enum import StrEnum, auto, unique
from typing import Any, Dict, List, Optional, Sequence, Tuple
from uuid import uuid4

from httpx import Timeout
from ollama import Client
from type_serialize import Serializable

from cvp.ollama.details import ModelDetails
from cvp.types.override import override
from cvp.variables import TIMEOUT_INFINITE


class Ollama(Serializable):
    model_names: List[str]

    @unique
    class _Keys(StrEnum):
        uuid = auto()
        name_ = "name"
        url = auto()
        headers = auto()
        follow_redirects = auto()
        timeout = auto()
        model_names = auto()
        details = auto()

    def __init__(
        self,
        uuid: Optional[str] = None,
        name: Optional[str] = None,
        url: Optional[str] = None,
        headers: Optional[Sequence[Tuple[str, str]]] = None,
        follow_redirects=True,
        timeout=TIMEOUT_INFINITE,
        model_names: Optional[Sequence[str]] = None,
        *,
        error: Optional[BaseException] = None,
        details: Optional[Dict[str, ModelDetails]] = None,
    ):
        self.uuid = uuid if uuid else str(uuid4())
        self.name = name if name else str()
        self.url = url if url else str()
        self.headers = list(headers if headers else ())
        self.follow_redirects = follow_redirects
        self.timeout = timeout
        self.model_names = list(model_names if model_names else ())
        self._details = dict(details if details else {})
        self._error = error

    @property
    def details(self):
        return self._details

    def header_as_dict(self) -> Dict[str, str]:
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
            and self.timeout == other.timeout
            and self.model_names == other.model_names
            and self._details == other._details
            and self._error == other._error
        )

    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result.uuid = copy(self.uuid)
        result.name = copy(self.name)
        result.url = copy(self.url)
        result.headers = copy(self.headers)
        result.follow_redirects = copy(self.follow_redirects)
        result.timeout = copy(self.timeout)
        result.model_names = copy(self.model_names)
        result._details = copy(self._details)
        result._error = copy(self._error)
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
        result.timeout = deepcopy(self.timeout, memo)
        result.model_names = deepcopy(self.model_names, memo)
        result._details = deepcopy(self._details, memo)
        result._error = deepcopy(self._error, memo)
        memo[id(self)] = result
        return result

    @override
    def __serialize__(self) -> Any:
        return {
            str(self._Keys.uuid): self.uuid,
            str(self._Keys.name_): self.name,
            str(self._Keys.url): self.url,
            str(self._Keys.headers): self.header_as_dict(),
            str(self._Keys.follow_redirects): self.follow_redirects,
            str(self._Keys.timeout): self.timeout,
            str(self._Keys.model_names): self.model_names,
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
        self.timeout = float(data.get(self._Keys.timeout, TIMEOUT_INFINITE))
        self.model_names = data.get(self._Keys.model_names, list())

        self._details = dict()
        self._error = None

    @property
    def has_error(self) -> bool:
        return self._error is not None

    @property
    def error(self):
        return self._error

    @property
    def client(self):
        return Client(
            host=self.url,
            # auth: AuthTypes | None = None,
            # params: QueryParamTypes | None = None,
            headers=self.header_as_dict(),
            # cookies: CookieTypes | None = None,
            # verify: ssl.SSLContext | str | bool = True,
            # cert: CertTypes | None = None,
            # trust_env: bool = True,
            # http1: bool = True,
            # http2: bool = False,
            # proxy: ProxyTypes | None = None,
            # mounts: None | (typing.Mapping[str, BaseTransport | None]) = None,
            timeout=Timeout(self.timeout) if 0 < self.timeout else None,
            follow_redirects=self.follow_redirects,
            # limits: Limits = DEFAULT_LIMITS,
            # max_redirects: int = DEFAULT_MAX_REDIRECTS,
            # event_hooks: None | (typing.Mapping[str, list[EventHook]]) = None,
            # base_url: URL | str = "",
            # transport: BaseTransport | None = None,
            # default_encoding: str | typing.Callable[[bytes], str] = "utf-8",
        )

    def update_model_names(self):
        self.model_names = list(m.model for m in self.client.list().models if m.model)
        return self.model_names.copy()

    def show_model(self, model_name: str) -> ModelDetails:
        response = self.client.show(model_name)
        detail = self._details.get(model_name, ModelDetails())
        try:
            modified_at = response.modified_at
            template = response.template
            model_file = response.modelfile
            license_ = response.license
            model_info = response.modelinfo
            parameters = response.parameters

            detail.modified_at = modified_at
            detail.template = template if template else str()
            detail.model_file = model_file if model_file else str()
            detail.license = license_ if license_ else str()
            detail.model_info = {str(k): str(v) for k, v in model_info.items()}
            detail.parameters = parameters if parameters else str()

            if response.details is not None:
                parent_model = response.details.parent_model
                format_ = response.details.format
                family = response.details.family
                families = response.details.families
                parameter_size = response.details.parameter_size
                q_level = response.details.quantization_level

                detail.parent_model = parent_model if parent_model else str()
                detail.format = format_ if format_ else str()
                detail.family = family if family else str()
                detail.families = list(families if families else ())
                detail.parameter_size = parameter_size if parameter_size else str()
                detail.quantization_level = q_level if q_level else str()
            return detail
        finally:
            self._details[model_name] = detail
