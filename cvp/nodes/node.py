# -*- coding: utf-8 -*-

from inspect import signature
from typing import Any, Callable, Iterable, List, NewType, Optional, Sequence

from cvp.nodes.interface import NodeInterface
from cvp.nodes.record import NodeRecord
from cvp.pins.pin import Pin
from cvp.pins.special import NextPin, PrevPin, ReturnPin
from cvp.types.override import override
from cvp.variables import FLOW_PATH_SEPARATOR

NodeName = NewType("NodeName", str)
NodePath = NewType("NodePath", str)


class Node(NodeInterface):
    def __init__(
        self,
        path: NodePath,
        name: Optional[NodeName] = None,
        func: Optional[Callable] = None,
        docs: Optional[str] = None,
        pins: Optional[Iterable[Pin]] = None,
        tags: Optional[Iterable[str]] = None,
    ):
        if not path:
            raise ValueError("The 'path' argument is required")

        if name:
            self.__name = name
        elif func is not None:
            self.__name = NodeName(type(func).__name__)
        elif type(self) is not Node:
            self.__name = NodeName(type(self).__name__)
        else:
            self.__name = NodeName(path)

        self.__path = path
        self.__func = func
        self.__docs = docs if docs else str()
        self.__pins = tuple(pins if pins else ())
        self.__tags = tuple(tags if tags else ())

    @classmethod
    def from_callable(
        cls,
        func: Callable,
        path: Optional[NodePath] = None,
        name: Optional[NodeName] = None,
        docs: Optional[str] = None,
        tags: Optional[Iterable[str]] = None,
    ):
        if not callable(func):
            raise TypeError(f"Only callables can be registered: {func}")

        param_name = name if name else NodeName(func.__name__)
        param_docs = docs if docs else (func.__doc__ if func.__doc__ else str())

        if path:
            param_path = path
        elif hasattr(func, "__module__"):
            param_path = NodePath(func.__module__ + FLOW_PATH_SEPARATOR + param_name)
        else:
            raise ValueError("Could not find attribute '__module__' in callable")

        if not param_name:
            raise ValueError("The 'name' attribute is required")
        if not param_path:
            raise ValueError("The 'path' attribute is required")

        param_pins: List[Pin] = list()
        param_pins.append(PrevPin())
        param_pins.append(NextPin())

        sig = signature(func)
        param_pins.append(ReturnPin.from_return_annotation(sig.return_annotation))

        for param in sig.parameters.values():
            param_pin = Pin.from_parameter(param)
            param_pins.append(param_pin)

        return cls(
            path=param_path,
            name=param_name,
            func=func,
            docs=param_docs,
            pins=param_pins,
            tags=tags,
        )

    @property
    def name(self) -> NodeName:
        return self.__name

    @property
    def path(self) -> NodePath:
        return self.__path

    @property
    def func(self) -> Optional[Callable]:
        return self.__func

    @property
    def docs(self) -> str:
        return self.__docs

    @property
    def pins(self) -> Sequence[Pin]:
        return self.__pins

    @property
    def tags(self) -> Sequence[str]:
        return self.__tags

    @property
    def execs(self) -> List[Pin]:
        return list(filter(lambda p: p.is_exec_action, self.__pins))

    @property
    def datas(self) -> List[Pin]:
        return list(filter(lambda p: p.is_data_action, self.__pins))

    @property
    def inputs(self) -> List[Pin]:
        return list(filter(lambda p: p.is_input_stream, self.__pins))

    @property
    def outputs(self) -> List[Pin]:
        return list(filter(lambda p: p.is_output_stream, self.__pins))

    @property
    def exec_inputs(self) -> List[Pin]:
        return list(filter(lambda p: p.is_exec_inputs, self.__pins))

    @property
    def exec_outputs(self) -> List[Pin]:
        return list(filter(lambda p: p.is_exec_outputs, self.__pins))

    @property
    def data_inputs(self) -> List[Pin]:
        return list(filter(lambda p: p.is_data_inputs, self.__pins))

    @property
    def data_outputs(self) -> List[Pin]:
        return list(filter(lambda p: p.is_data_outputs, self.__pins))

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

        if not isinstance(exec_inputs[0], PrevPin):
            return False
        if not isinstance(exec_outputs[0], NextPin):
            return False

        return True

    def find_pin(self, pin_name: str) -> Optional[Pin]:
        for pin in self.pins:
            if pin.name == pin_name:
                return pin
        return None

    def find_return_pin(self) -> Optional[Pin]:
        for pin in self.pins:
            if isinstance(pin, ReturnPin):
                return pin
        return None

    def __call__(self, *args, **kwargs) -> Any:
        if self.func is None:
            raise ValueError("Node function is not set")
        return self.func(*args, **kwargs)

    @override
    def run(self, record: NodeRecord) -> Optional[Pin]:
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
