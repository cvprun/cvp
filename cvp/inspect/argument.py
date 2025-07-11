# -*- coding: utf-8 -*-

from collections import OrderedDict
from datetime import date, time
from inspect import Parameter, Signature, signature
from typing import (
    Annotated,
    Any,
    Callable,
    Dict,
    Mapping,
    Optional,
    Sequence,
    TypeVar,
    get_args,
    get_origin,
)

from cvp.chrono.constants import MIDNIGHT_TIME, UNIX_EPOCH_START_DATE
from cvp.types.annotations import AnnotatedAlias

_ValueT = TypeVar("_ValueT")


class Argument:
    def __init__(
        self,
        param: Parameter,
        value: Any = Parameter.empty,
        doc: Optional[str] = None,
    ):
        self.param = param
        self.value = value
        self.doc = doc

    @classmethod
    def from_details(
        cls,
        name: str,
        kind=Parameter.POSITIONAL_OR_KEYWORD,
        default=Parameter.empty,
        annotation=Parameter.empty,
        value=Parameter.empty,
        doc: Optional[str] = None,
    ):
        parameter = Parameter(name, kind, default=default, annotation=annotation)
        return cls(parameter, value, doc)

    @property
    def name(self):
        return self.param.name

    @property
    def default(self):
        return self.param.default

    @property
    def annotation(self):
        return self.param.annotation

    @property
    def kind(self):
        return self.param.kind

    def get_value(self, default: _ValueT) -> _ValueT:
        if self.value == Parameter.empty:
            if self.param.default == Parameter.empty:
                return default
            else:
                return self.param.default
        else:
            return self.value

    def get_bool(self, default=False) -> bool:
        return self.get_value(default)

    def get_int(self, default=0) -> int:
        return self.get_value(default)

    def get_float(self, default=0.0) -> float:
        return self.get_value(default)

    def get_str(self, default="") -> str:
        return self.get_value(default)

    def get_date(self, default=UNIX_EPOCH_START_DATE) -> date:
        return self.get_value(default)

    def get_time(self, default=MIDNIGHT_TIME) -> time:
        return self.get_value(default)

    @property
    def is_empty_value(self):
        return self.value == Parameter.empty

    @property
    def is_empty_default(self):
        return self.param.default == Parameter.empty

    @property
    def is_empty_annotation(self):
        return self.param.annotation == Parameter.empty

    @property
    def is_annotated(self):
        return (
            hasattr(self.param.annotation, "__metadata__")
            and isinstance(self.param.annotation, AnnotatedAlias)
            and get_origin(self.param.annotation) == Annotated
        )

    @property
    def annotated_args(self) -> Sequence[Any]:
        if not self.is_annotated:
            if isinstance(self.param.annotation, type):
                annotation_name = self.param.annotation.__name__
            else:
                annotation_name = type(self.param.annotation).__name__
            raise TypeError(f"Parameter is not of type Annotated: {annotation_name}")

        return get_args(self.param.annotation)

    def type_deduction(self) -> type:
        if not self.is_empty_annotation:
            if self.is_annotated:
                return self.annotated_args[0]
            else:
                origin = get_origin(self.param.annotation)
                if origin is not None:
                    return origin
                else:
                    return self.param.annotation
        elif self.param.default != Parameter.empty:
            return type(self.param.default)
        else:
            return object


class ArgumentMapper(OrderedDict[str, Argument]):
    @classmethod
    def from_parameters(cls, parameters: Mapping[str, Parameter]):
        return cls(**{key: Argument(param) for key, param in parameters.items()})

    @classmethod
    def from_signature(cls, sig: Signature):
        return cls.from_parameters(sig.parameters)

    @classmethod
    def from_callable(cls, func: Callable):
        return cls.from_signature(signature(func))

    @property
    def requestable(self) -> bool:
        """Ready to Callable?"""
        if not bool(self):
            return True

        return all(not a.is_empty_value for a in self.values())

    def as_dict(self) -> Dict[str, Any]:
        return {k: v.value for k, v in self.items()}
