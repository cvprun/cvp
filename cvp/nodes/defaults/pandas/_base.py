# -*- coding: utf-8 -*-

from abc import abstractmethod
from typing import Any, Optional

import pandas as pd

from cvp.dtypes.dtype import Dtype
from cvp.nodes.node import Node
from cvp.nodes.record import NodeRecord
from cvp.pins.datas import DataInputPin, DataOutputPin
from cvp.pins.pin import Pin, PinName


class PandasFunctionNode(Node):
    """Base class for pandas function nodes."""

    def __init__(self, function_name: str, *input_pins: DataInputPin):
        self._function_name = function_name
        self._input_pins = input_pins
        self._output = DataOutputPin(
            name=PinName("result"),
            dtype=Dtype.any(),
            docs=f"Result of pandas.{function_name}",
        )
        super().__init__(*self._input_pins, self._output)

    def run(self, record: NodeRecord) -> Pin:
        # Get input values, handling optional pins
        inputs = []
        for pin in self._input_pins:
            try:
                value = record.get(pin)
                inputs.append(value)
            except KeyError:
                inputs.append(None)

        # Apply pandas function
        result = self.apply_function(*inputs)

        # Set output
        record.set(self._output, result)
        return self.nonext()

    @abstractmethod
    def apply_function(self, *args, **kwargs) -> Any:
        """Apply the pandas function with given arguments."""
        raise NotImplementedError


class SimplePandasFunctionNode(PandasFunctionNode):
    """Node for simple pandas functions that directly call pd.function_name."""

    def __init__(self, function_name: str, *input_pins: DataInputPin):
        super().__init__(function_name, *input_pins)
        self._pandas_func = getattr(pd, function_name)

    def apply_function(self, *args, **kwargs) -> Any:
        return self._pandas_func(*args, **kwargs)


class PandasUnaryNode(SimplePandasFunctionNode):
    """Node for pandas unary functions (single input)."""

    def __init__(
        self,
        function_name: str,
        input_name: str = "data",
        input_docs: Optional[str] = None,
    ):
        input_pin = DataInputPin(
            name=PinName(input_name),
            dtype=Dtype.any(),
            docs=input_docs or f"Input for pandas.{function_name}",
        )
        super().__init__(function_name, input_pin)


class PandasBinaryNode(SimplePandasFunctionNode):
    """Node for pandas binary functions (two inputs)."""

    def __init__(
        self,
        function_name: str,
        first_name: str = "left",
        first_docs: Optional[str] = None,
        second_name: str = "right",
        second_docs: Optional[str] = None,
    ):
        first_pin = DataInputPin(
            name=PinName(first_name),
            dtype=Dtype.any(),
            docs=first_docs or f"First input for pandas.{function_name}",
        )
        second_pin = DataInputPin(
            name=PinName(second_name),
            dtype=Dtype.any(),
            docs=second_docs or f"Second input for pandas.{function_name}",
        )
        super().__init__(function_name, first_pin, second_pin)


class DataFrameMethodNode(Node):
    """Base class for DataFrame method nodes."""

    def __init__(self, method_name: str, *additional_pins: DataInputPin):
        self._method_name = method_name
        self._dataframe_pin = DataInputPin(
            name=PinName("dataframe"),
            dtype=Dtype.any(),
            docs="Input DataFrame",
        )
        self._additional_pins = additional_pins
        self._output = DataOutputPin(
            name=PinName("result"),
            dtype=Dtype.any(),
            docs=f"Result of DataFrame.{method_name}",
        )
        super().__init__(self._dataframe_pin, *self._additional_pins, self._output)

    def run(self, record: NodeRecord) -> Pin:
        # Get DataFrame
        df = record.get(self._dataframe_pin)

        # Get additional inputs, handling optional pins
        additional_inputs = []
        for pin in self._additional_pins:
            try:
                value = record.get(pin)
                additional_inputs.append(value)
            except KeyError:
                additional_inputs.append(None)

        # Apply method
        result = self.apply_method(df, *additional_inputs)

        # Set output
        record.set(self._output, result)
        return self.nonext()

    @abstractmethod
    def apply_method(self, df: pd.DataFrame, *args, **kwargs) -> Any:
        """Apply the DataFrame method with given arguments."""
        raise NotImplementedError


class SimpleDataFrameMethodNode(DataFrameMethodNode):
    """Node for simple DataFrame methods."""

    def apply_method(self, df: pd.DataFrame, *args, **kwargs) -> Any:
        method = getattr(df, self._method_name)
        return method(*args, **kwargs)
