# -*- coding: utf-8 -*-

from abc import abstractmethod
from typing import Any, Optional

import numpy as np

from cvp.dtypes.dtype import Dtype
from cvp.nodes.node import Node
from cvp.nodes.record import NodeRecord
from cvp.pins.datas import DataInputPin, DataOutputPin
from cvp.pins.pin import Pin, PinName


class NumpyFunctionNode(Node):
    """Base class for numpy function nodes."""

    def __init__(self, function_name: str, *input_pins: DataInputPin):
        self._function_name = function_name
        self._input_pins = input_pins
        self._output = DataOutputPin(
            name=PinName("result"),
            dtype=Dtype.any(),
            docs=f"Result of numpy.{function_name}",
        )
        super().__init__(*self._input_pins, self._output)

    def run(self, record: NodeRecord) -> Pin:
        # Get input values
        inputs = [record.get(pin) for pin in self._input_pins]

        # Apply numpy function
        result = self.apply_function(*inputs)

        # Set output
        record.set(self._output, result)
        return self.nonext()

    @abstractmethod
    def apply_function(self, *args, **kwargs) -> Any:
        """Apply the numpy function with given arguments."""
        raise NotImplementedError


class SimpleNumpyFunctionNode(NumpyFunctionNode):
    """Node for simple numpy functions that directly call np.function_name."""

    def __init__(self, function_name: str, *input_pins: DataInputPin):
        super().__init__(function_name, *input_pins)
        self._numpy_func = getattr(np, function_name)

    def apply_function(self, *args, **kwargs) -> Any:
        return self._numpy_func(*args, **kwargs)


class NumpyUnaryNode(SimpleNumpyFunctionNode):
    """Node for numpy unary functions (single input)."""

    def __init__(
        self,
        function_name: str,
        input_name: str = "x",
        input_docs: Optional[str] = None,
    ):
        input_pin = DataInputPin(
            name=PinName(input_name),
            dtype=Dtype.any(),
            docs=input_docs or f"Input for numpy.{function_name}",
        )
        super().__init__(function_name, input_pin)


class NumpyBinaryNode(SimpleNumpyFunctionNode):
    """Node for numpy binary functions (two inputs)."""

    def __init__(
        self,
        function_name: str,
        first_name: str = "x1",
        first_docs: Optional[str] = None,
        second_name: str = "x2",
        second_docs: Optional[str] = None,
    ):
        first_pin = DataInputPin(
            name=PinName(first_name),
            dtype=Dtype.any(),
            docs=first_docs or f"First input for numpy.{function_name}",
        )
        second_pin = DataInputPin(
            name=PinName(second_name),
            dtype=Dtype.any(),
            docs=second_docs or f"Second input for numpy.{function_name}",
        )
        super().__init__(function_name, first_pin, second_pin)
