# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from inspect import signature
from sys import exc_info
from typing import Any, Callable, List, Optional, Sequence

from cvp.dtypes.registry.globals import global_dtype_registry
from cvp.dtypes.registry.registry import DtypeRegistry
from cvp.nodes.icons import NODE_ICON_MAPPING
from cvp.nodes.record import NodeRecord
from cvp.pins.pin import Pin
from cvp.pins.special import NextPin, PrevPin, ReturnPin
from cvp.types.colors import RGBA, WHITE_RGBA
from cvp.types.override import override
from cvp.variables import FLOW_PATH_SEPARATOR


class NodeInterface(ABC):
    @abstractmethod
    def run(self, pin: Pin, record: NodeRecord) -> Optional[Pin]:
        raise NotImplementedError


class Node(NodeInterface):
    def __init__(
        self,
        name: str,
        path: str,
        func: Optional[Callable] = None,
        docs: Optional[str] = None,
        icon: Optional[str] = None,
        color: Optional[RGBA] = None,
        pins: Optional[Sequence[Pin]] = None,
        tags: Optional[Sequence[str]] = None,
    ):
        self.name = name
        self.path = path
        self.func = func
        self.docs = docs if docs else str()
        self.icon = icon if icon else str()
        self.color = color if color else WHITE_RGBA
        self.pins = list(pins if pins else [])
        self.tags = list(tags if tags else [])

    @classmethod
    def auto_parse(
        cls,
        func: Callable,
        name: Optional[str] = None,
        path: Optional[str] = None,
        docs: Optional[str] = None,
        icon: Optional[str] = None,
        color: Optional[RGBA] = None,
        flow_inputs: Optional[Sequence[Pin]] = None,
        flow_outputs: Optional[Sequence[Pin]] = None,
        data_inputs: Optional[Sequence[Pin]] = None,
        data_outputs: Optional[Sequence[Pin]] = None,
        tags: Optional[Sequence[str]] = None,
        *,
        dtype_registry: Optional[DtypeRegistry] = None,
    ):
        if not callable(func):
            raise TypeError(f"Only callables can be registered: {func}")

        base_name = name if name else func.__name__
        base_docs = docs if docs else func.__doc__
        base_icon = icon if icon else NODE_ICON_MAPPING[base_name[0]]
        base_color = color if color else WHITE_RGBA
        base_tags = list(tags if tags else list())

        if path:
            base_path = path
        elif hasattr(func, "__module__"):
            base_path = func.__module__ + FLOW_PATH_SEPARATOR + base_name
        else:
            raise ValueError("Could not find attribute '__module__' in callable")

        if not base_name:
            raise ValueError("The 'name' attribute is required")
        if not base_path:
            raise ValueError("The 'path' attribute is required")

        base_pins = list()

        if flow_inputs:
            for pin in flow_inputs:
                if not pin.is_flow_inputs:
                    raise ValueError("Pin must be flow inputs")
                base_pins.append(pin)
        else:
            base_pins.append(PrevPin())

        if flow_outputs:
            for pin in flow_outputs:
                if not pin.is_flow_outputs:
                    raise ValueError("Pin must be flow outputs")
                base_pins.append(pin)
        else:
            base_pins.append(NextPin())

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
                param_pin = Pin.from_parameter(param, dtype_registry=dtype_registry)
                base_pins.append(param_pin)

        if data_outputs:
            for pin in data_outputs:
                if not pin.is_data_outputs:
                    raise ValueError("Pin must be data outputs")
                base_pins.append(pin)
        else:
            return_pin = ReturnPin.from_return_annotation(
                sig.return_annotation,
                dtype_registry=dtype_registry,
            )
            base_pins.append(return_pin)

        return cls(
            name=base_name,
            path=base_path,
            func=func,
            docs=base_docs,
            icon=base_icon,
            color=base_color,
            pins=base_pins,
            tags=base_tags,
        )

    @property
    def flow_inputs(self) -> List[Pin]:
        return list(filter(lambda p: p.is_flow_inputs, self.pins))

    @property
    def flow_outputs(self) -> List[Pin]:
        return list(filter(lambda p: p.is_flow_outputs, self.pins))

    @property
    def data_inputs(self) -> List[Pin]:
        return list(filter(lambda p: p.is_data_inputs, self.pins))

    @property
    def data_outputs(self) -> List[Pin]:
        return list(filter(lambda p: p.is_data_outputs, self.pins))

    @property
    def is_bypass_flow(self) -> bool:
        if len(self.pins) != 2:
            return False

        flow_inputs = self.flow_inputs
        if len(flow_inputs) != 1:
            return False

        flow_outputs = self.flow_outputs
        if len(flow_outputs) != 1:
            return False

        if not isinstance(flow_inputs[0], PrevPin):
            return False
        if not isinstance(flow_outputs[0], NextPin):
            return False

        assert 0 == len(self.data_inputs)
        assert 0 == len(self.data_outputs)
        return True

    def __call__(self, *args, **kwargs) -> Any:
        if self.func is None:
            raise ValueError("Node function is not set")
        return self.func(*args, **kwargs)

    @override
    def run(self, pin: Pin, record: NodeRecord) -> Optional[Pin]:
        try:
            record.set_result(self.__call__(*record.args, **record.kwargs))
        except:  # noqa
            record.set_exception(exc_info())

        if self.is_bypass_flow:
            return self.flow_outputs[0]
        else:
            return None
