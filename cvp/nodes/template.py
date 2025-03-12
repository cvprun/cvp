# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from inspect import signature
from typing import Any, Callable, Iterable, List, NewType, Optional

from cvp.dtypes.registry.globals import global_dtype_registry
from cvp.dtypes.registry.registry import DtypeRegistry
from cvp.fonts.types import IconCode
from cvp.nodes.icons import NODE_ICON_MAPPING
from cvp.nodes.record import NodeRecord
from cvp.pins.special import NextPinTemplate, PrevPinTemplate, ReturnPinTemplate
from cvp.pins.template import PinTemplate
from cvp.types.colors import RGBA, WHITE_RGBA
from cvp.types.override import override
from cvp.variables import FLOW_PATH_SEPARATOR

NodeName = NewType("NodeName", str)
NodePath = NewType("NodePath", str)


class NodeInterface(ABC):
    @abstractmethod
    def run(self, record: NodeRecord) -> Any:
        raise NotImplementedError

    @abstractmethod
    def on_render(self, record: NodeRecord) -> None:
        raise NotImplementedError


class NodeTemplate(NodeInterface):
    def __init__(
        self,
        path: NodePath,
        name: Optional[NodeName] = None,
        func: Optional[Callable] = None,
        docs: Optional[str] = None,
        icon: Optional[IconCode] = None,
        color: Optional[RGBA] = None,
        pins: Optional[Iterable[PinTemplate]] = None,
        tags: Optional[Iterable[str]] = None,
        hidden=False,
    ):
        if not path:
            raise ValueError("The 'path' argument is required")

        if name:
            self.name = name
        elif func is not None:
            self.name = NodeName(type(func).__name__)
        elif type(self) is NodeTemplate:
            self.name = NodeName(type(self).__name__)
        else:
            self.name = NodeName(path)

        self.path = path
        self.func = func
        self.docs = docs if docs else str()
        self.icon = icon if icon else IconCode(str())
        self.color = color if color else WHITE_RGBA
        self.pins = list(pins if pins else ())
        self.tags = list(tags if tags else ())
        self.hidden = hidden

    @classmethod
    def from_callable(
        cls,
        func: Callable,
        path: Optional[NodePath] = None,
        name: Optional[NodeName] = None,
        docs: Optional[str] = None,
        icon: Optional[IconCode] = None,
        color: Optional[RGBA] = None,
        exec_inputs: Optional[Iterable[PinTemplate]] = None,
        exec_outputs: Optional[Iterable[PinTemplate]] = None,
        data_inputs: Optional[Iterable[PinTemplate]] = None,
        data_outputs: Optional[Iterable[PinTemplate]] = None,
        tags: Optional[Iterable[str]] = None,
        hidden=False,
        *,
        dtype_registry: Optional[DtypeRegistry] = None,
    ):
        if not callable(func):
            raise TypeError(f"Only callables can be registered: {func}")

        base_name = name if name else NodeName(func.__name__)
        base_docs = docs if docs else func.__doc__
        base_icon = icon if icon else NODE_ICON_MAPPING[base_name[0]]
        base_color = color if color else WHITE_RGBA
        base_tags = list(tags if tags else list())
        base_hidden = hidden

        if path:
            base_path = path
        elif hasattr(func, "__module__"):
            base_path = NodePath(func.__module__ + FLOW_PATH_SEPARATOR + base_name)
        else:
            raise ValueError("Could not find attribute '__module__' in callable")

        if not base_name:
            raise ValueError("The 'name' attribute is required")
        if not base_path:
            raise ValueError("The 'path' attribute is required")

        base_pins = list()

        if exec_inputs:
            for pin in exec_inputs:
                if not pin.is_exec_inputs:
                    raise ValueError("Pin must be exec inputs")
                base_pins.append(pin)
        else:
            base_pins.append(PrevPinTemplate())

        if exec_outputs:
            for pin in exec_outputs:
                if not pin.is_exec_outputs:
                    raise ValueError("Pin must be exec outputs")
                base_pins.append(pin)
        else:
            base_pins.append(NextPinTemplate())

        if dtype_registry is None:
            dtype_registry = global_dtype_registry()

        assert dtype_registry is not None
        sig = signature(func)

        if data_inputs:
            for pin in data_inputs:
                if not pin.is_data_inputs:
                    raise ValueError("Pin must be data inputs")
                base_pins.append(pin)
        else:
            for param in sig.parameters.values():
                param_pin = PinTemplate.from_parameter(
                    parameter=param,
                    dtype_registry=dtype_registry,
                )
                base_pins.append(param_pin)

        if data_outputs:
            for pin in data_outputs:
                if not pin.is_data_outputs:
                    raise ValueError("Pin must be data outputs")
                base_pins.append(pin)
        else:
            return_pin = ReturnPinTemplate.from_return_annotation(
                sig.return_annotation,
                dtype_registry=dtype_registry,
            )
            base_pins.append(return_pin)

        return cls(
            path=base_path,
            name=base_name,
            func=func,
            docs=base_docs,
            icon=base_icon,
            color=base_color,
            pins=base_pins,
            tags=base_tags,
            hidden=base_hidden,
        )

    @property
    def execs(self) -> List[PinTemplate]:
        return list(filter(lambda p: p.is_exec_action, self.pins))

    @property
    def datas(self) -> List[PinTemplate]:
        return list(filter(lambda p: p.is_data_action, self.pins))

    @property
    def inputs(self) -> List[PinTemplate]:
        return list(filter(lambda p: p.is_input_stream, self.pins))

    @property
    def outputs(self) -> List[PinTemplate]:
        return list(filter(lambda p: p.is_output_stream, self.pins))

    @property
    def exec_inputs(self) -> List[PinTemplate]:
        return list(filter(lambda p: p.is_exec_inputs, self.pins))

    @property
    def exec_outputs(self) -> List[PinTemplate]:
        return list(filter(lambda p: p.is_exec_outputs, self.pins))

    @property
    def data_inputs(self) -> List[PinTemplate]:
        return list(filter(lambda p: p.is_data_inputs, self.pins))

    @property
    def data_outputs(self) -> List[PinTemplate]:
        return list(filter(lambda p: p.is_data_outputs, self.pins))

    @property
    def has_exec_input(self) -> bool:
        return bool(self.exec_inputs)

    @property
    def has_exec_output(self) -> bool:
        return bool(self.exec_outputs)

    @property
    def any_exec(self) -> bool:
        return self.has_exec_input or self.has_exec_output

    @property
    def has_data_input(self) -> bool:
        return bool(self.data_inputs)

    @property
    def has_data_output(self) -> bool:
        return bool(self.data_outputs)

    @property
    def any_data(self) -> bool:
        return self.has_data_input or self.has_data_output

    @property
    def is_exec_only(self) -> bool:
        return self.any_exec and not self.any_data

    @property
    def is_data_only(self) -> bool:
        return not self.any_exec and self.any_data

    @property
    def is_begin(self) -> bool:
        return not self.has_exec_input and self.has_exec_output

    @property
    def is_middle(self) -> bool:
        return self.has_exec_input and self.has_exec_output

    @property
    def is_end(self) -> bool:
        return self.has_exec_input and not self.has_exec_output

    @property
    def is_bypass_exec(self) -> bool:
        if len(self.execs) != 2:
            return False

        exec_inputs = self.exec_inputs
        if len(exec_inputs) != 1:
            return False

        exec_outputs = self.exec_outputs
        if len(exec_outputs) != 1:
            return False

        if not isinstance(exec_inputs[0], PrevPinTemplate):
            return False
        if not isinstance(exec_outputs[0], NextPinTemplate):
            return False

        return True

    def find_pin(self, pin_name: str) -> Optional[PinTemplate]:
        for pin in self.pins:
            if pin.name == pin_name:
                return pin
        return None

    def find_return_pin(self) -> Optional[PinTemplate]:
        for pin in self.pins:
            if isinstance(pin, ReturnPinTemplate):
                return pin
        return None

    def __call__(self, *args, **kwargs) -> Any:
        if self.func is None:
            raise ValueError("Node function is not set")
        return self.func(*args, **kwargs)

    @override
    def run(self, record: NodeRecord) -> Optional[PinTemplate]:
        result = self.__call__(*record.args, **record.kwargs)
        if return_pin := self.find_return_pin():
            record.set(return_pin, result)

        if self.is_bypass_exec:
            return self.exec_outputs[0]
        else:
            return None

    @override
    def on_render(self, record: NodeRecord) -> None:
        pass
