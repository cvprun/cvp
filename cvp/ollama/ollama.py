# -*- coding: utf-8 -*-

from copy import copy, deepcopy
from enum import StrEnum, auto, unique
from typing import Any, Dict, List, Optional, Sequence, Tuple

from httpx import Timeout
from ollama import Client
from type_serialize import Serializable, deserialize, serialize

from cvp.ollama.details import ModelDetails
from cvp.types.override import override
from cvp.variables import DEFAULT_OLLAMA_TIMEOUT


class Ollama(Serializable):
    model_names: List[str]

    @unique
    class _Keys(StrEnum):
        name_ = "name"
        url = auto()
        headers = auto()
        follow_redirects = auto()
        timeout = auto()
        model_names = auto()
        details = auto()

    def __init__(
        self,
        name: Optional[str] = None,
        url: Optional[str] = None,
        headers: Optional[Sequence[Tuple[str, str]]] = None,
        follow_redirects=True,
        timeout=DEFAULT_OLLAMA_TIMEOUT,
        model_names: Optional[Sequence[str]] = None,
        *,
        error: Optional[BaseException] = None,
        details: Optional[Dict[str, ModelDetails]] = None,
    ):
        self.name = name if name else str()
        self.url = url if url else str()
        self.headers = list(headers if headers else ())
        self.follow_redirects = follow_redirects
        self.timeout = timeout
        self.model_names = list(model_names if model_names else ())
        self.details = dict(details if details else {})
        self._error = error

    def header_as_dict(self) -> Dict[str, str]:
        return {str(k): str(v) for k, v in self.headers}

    def __eq__(self, other) -> bool:
        if not isinstance(other, type(self)):
            return False
        return (
            self.name == other.name
            and self.url == other.url
            and self.headers == other.headers
            and self.follow_redirects == other.follow_redirects
            and self.timeout == other.timeout
            and self.model_names == other.model_names
            and self.details == other.details
            and self._error == other._error
        )

    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result.name = copy(self.name)
        result.url = copy(self.url)
        result.headers = copy(self.headers)
        result.follow_redirects = copy(self.follow_redirects)
        result.timeout = copy(self.timeout)
        result.model_names = copy(self.model_names)
        result.details = copy(self.details)
        result._error = copy(self._error)
        return result

    def __deepcopy__(self, memo: Optional[Dict[int, Any]] = None):
        if memo is None:
            memo = dict()
        cls = self.__class__
        result = cls.__new__(cls)
        result.name = deepcopy(self.name, memo)
        result.url = deepcopy(self.url, memo)
        result.headers = deepcopy(self.headers, memo)
        result.follow_redirects = deepcopy(self.follow_redirects, memo)
        result.timeout = deepcopy(self.timeout, memo)
        result.model_names = deepcopy(self.model_names, memo)
        result.details = deepcopy(self.details, memo)
        result._error = deepcopy(self._error, memo)
        memo[id(self)] = result
        return result

    @override
    def __serialize__(self) -> Any:
        return {
            str(self._Keys.name_): self.name,
            str(self._Keys.url): self.url,
            str(self._Keys.headers): self.header_as_dict(),
            str(self._Keys.follow_redirects): self.follow_redirects,
            str(self._Keys.timeout): self.timeout,
            str(self._Keys.model_names): self.model_names,
            str(self._Keys.details): {k: serialize(v) for k, v in self.details.items()},
        }

    @override
    def __deserialize__(self, data: Any) -> None:
        if not isinstance(data, dict):
            raise TypeError(f"Unexpected data type: {type(data).__name__}")

        self.name = str(data.get(self._Keys.name_, str()))
        self.url = str(data.get(self._Keys.url, str()))

        headers = data.get(self._Keys.headers, dict())
        self.headers = list((str(k), str(v)) for k, v in headers.items())

        self.follow_redirects = bool(data.get(self._Keys.follow_redirects, True))
        self.timeout = float(data.get(self._Keys.timeout, DEFAULT_OLLAMA_TIMEOUT))
        self.model_names = data.get(self._Keys.model_names, list())

        details = data.get(self._Keys.details, dict())
        self.details = {k: deserialize(v, ModelDetails) for k, v in details.items()}

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
            timeout=Timeout(self.timeout),
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
        # model_name = model_name.split(":")[0]
        response = self.client.show(model_name)
        detail = self.details.get(model_name, ModelDetails())
        try:
            detail.modified_at = response.modified_at
            detail.template = response.template
            detail.model_file = response.modelfile
            detail.license = response.license

            detail.model_info = {str(k): str(v) for k, v in response.modelinfo.items()}

            detail.parameters = response.parameters
            detail.parameters = response.parameters
            if response.details is not None:
                detail.parent_model = response.details.parent_model
                detail.format = response.details.format
                detail.family = response.details.family
                detail.families = response.details.families
                detail.parameter_size = response.details.parameter_size
                detail.quantization_level = response.details.quantization_level
            return detail
        finally:
            self.details[model_name] = detail
