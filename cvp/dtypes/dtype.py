# -*- coding: utf-8 -*-

from copy import copy, deepcopy
from enum import StrEnum, auto, unique
from typing import Any, Dict, NewType, Optional, Tuple, Union

from type_serialize import Serializable, deserialize, serialize

from cvp.dtypes.icons import DTYPE_ICON_MAPPING
from cvp.fonts.types import IconCode
from cvp.modules.class_path import ClassPath, TypePath
from cvp.types.colors import RGBA, WHITE_RGBA
from cvp.types.override import override
from cvp.variables import FLOW_PATH_SEPARATOR

DtypeName = NewType("DtypeName", str)


def default_dtype_name_with_type(base: type) -> DtypeName:
    return DtypeName(base.__name__)


def default_dtype_path_with_type(base: type, name: Optional[str] = None) -> TypePath:
    path = base.__module__ + FLOW_PATH_SEPARATOR + (name if name else base.__name__)
    return TypePath(path)


def default_dtype_docs_with_type(base: type) -> str:
    return base.__doc__ if base.__doc__ else str()


def default_dtype_icon_with_type(base: type, name: Optional[str] = None) -> IconCode:
    return DTYPE_ICON_MAPPING[(name if name else base.__name__)[0]]


class Dtype(Serializable):

    @unique
    class _Keys(StrEnum):
        base = auto()
        name_ = "name"
        path = auto()
        docs = auto()
        icon = auto()
        color = auto()
        hidden = auto()

    def __init__(
        self,
        base: Union[type, ClassPath],
        name: Optional[DtypeName] = None,
        path: Optional[TypePath] = None,
        docs: Optional[str] = None,
        icon: Optional[IconCode] = None,
        color: Optional[RGBA] = None,
        *,
        hidden=False,
    ):
        if isinstance(base, ClassPath):
            self.base = base
        elif isinstance(base, type):
            self.base = ClassPath(base)  # type: ignore[var-annotated]
        else:
            raise TypeError(f"Only types can be registered: {base}")

        self.name = name if name else default_dtype_name_with_type(base)
        self.path = path if path else default_dtype_path_with_type(base, self.name)
        self.docs = docs if docs else default_dtype_docs_with_type(base)
        self.icon = icon if icon else default_dtype_icon_with_type(base, self.name)
        self.color = color if color else WHITE_RGBA
        self.hidden = hidden

        if not self.name:
            raise ValueError("The 'name' attribute is required")
        if not self.path:
            raise ValueError("The 'path' attribute is required")

    def __str__(self) -> str:
        return self.name

    def __hash__(self) -> int:
        return hash(
            (
                self.__class__,
                self.base,
                self.name,
                self.path,
                self.docs,
                self.icon,
                self.color,
                self.hidden,
            )
        )

    def __eq__(self, other) -> bool:
        if not isinstance(other, type(self)):
            return False
        return (
            self.base == other.base
            and self.name == other.name
            and self.path == other.path
            and self.docs == other.docs
            and self.icon == other.icon
            and self.color == other.color
            and self.hidden == other.hidden
        )

    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result.base = copy(self.base)
        result.name = copy(self.name)
        result.path = copy(self.path)
        result.docs = copy(self.docs)
        result.icon = copy(self.icon)
        result.color = copy(self.color)
        result.hidden = copy(self.hidden)
        return result

    def __deepcopy__(self, memo: Optional[Dict[int, Any]] = None):
        if memo is None:
            memo = dict()
        cls = self.__class__
        result = cls.__new__(cls)
        result.base = deepcopy(self.base, memo)
        result.name = deepcopy(self.name, memo)
        result.path = deepcopy(self.path, memo)
        result.docs = deepcopy(self.docs, memo)
        result.icon = deepcopy(self.icon, memo)
        result.color = deepcopy(self.color, memo)
        result.hidden = deepcopy(self.hidden, memo)
        memo[id(self)] = result
        return result

    @override
    def __serialize__(self) -> Any:
        return {
            str(self._Keys.base): serialize(self.base),
            str(self._Keys.name_): str(self.name),
            str(self._Keys.path): str(self.path),
            str(self._Keys.docs): str(self.docs),
            str(self._Keys.icon): str(self.icon),
            str(self._Keys.color): list(self.color),
            str(self._Keys.hidden): bool(self.hidden),
        }

    @override
    def __deserialize__(self, data: Any) -> None:
        if not isinstance(data, dict):
            raise TypeError(f"Unexpected data type: {type(data).__name__}")

        base = data.get(self._Keys.base)
        if not base:
            raise ValueError("Undefined base value")

        self.base = deserialize(base, ClassPath)
        self.name = DtypeName(data.get(self._Keys.name_, str()))
        self.path = TypePath(data.get(self._Keys.path, str()))
        self.docs = str(data.get(self._Keys.docs, str()))
        self.icon = IconCode(data.get(self._Keys.icon, str()))
        self.color = tuple(data.get(self._Keys.color, WHITE_RGBA))
        self.hidden = bool(data.get(self._Keys.hidden, False))

        assert isinstance(self.base, ClassPath)
        assert isinstance(self.name, str)  # DtypeName is str
        assert isinstance(self.path, str)  # TypePath is str
        assert isinstance(self.docs, str)
        assert isinstance(self.icon, str)  # IconCode is str
        assert isinstance(self.color, tuple)
        assert len(self.color) == 4
        assert all(isinstance(c, float) for c in self.color)
        assert isinstance(self.hidden, bool)

    @property
    def type(self) -> type:
        return self.base.type

    @property
    def type_path(self) -> TypePath:
        return self.base.path

    def split(self) -> Tuple[str, str]:
        return self.base.split()

    @property
    def module_path(self) -> str:
        return self.base.module_path

    @property
    def class_name(self) -> str:
        return self.base.class_name

    def __call__(self, *args, **kwargs):
        return self.base.__call__(*args, **kwargs)
