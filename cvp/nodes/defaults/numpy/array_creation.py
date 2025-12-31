# -*- coding: utf-8 -*-

from typing import Any, List, Optional

import numpy as np

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.numpy._base import NumpyFunctionNode
from cvp.nodes.node import Node
from cvp.nodes.record import NodeRecord
from cvp.pins.datas import DataInputPin, DataOutputPin
from cvp.pins.pin import Pin, PinName
from cvp.types.override import override


class ArrayNode(NumpyFunctionNode):
    """Create an array from a list or tuple."""

    def __init__(self):
        input_pin = DataInputPin(
            name=PinName("object"),
            dtype=Dtype.any(),
            docs="Array-like object to convert to array",
        )
        dtype_pin = DataInputPin(
            name=PinName("dtype"),
            dtype=Dtype.any(),
            docs="Data type of the array",
            default=None,
        )
        super().__init__("array", input_pin, dtype_pin)

    def apply_function(self, obj, dtype, **kwargs) -> Any:
        if dtype is None:
            return np.array(obj)
        return np.array(obj, dtype=dtype)


class ZerosNode(NumpyFunctionNode):
    """Create array filled with zeros."""

    def __init__(self):
        shape_pin = DataInputPin(
            name=PinName("shape"),
            dtype=Dtype.any(),
            docs="Shape of the array",
        )
        dtype_pin = DataInputPin(
            name=PinName("dtype"),
            dtype=Dtype.any(),
            docs="Data type of the array",
            default=float,
        )
        super().__init__("zeros", shape_pin, dtype_pin)

    def apply_function(self, shape, dtype, **kwargs) -> Any:
        return np.zeros(shape, dtype=dtype)


class OnesNode(NumpyFunctionNode):
    """Create array filled with ones."""

    def __init__(self):
        shape_pin = DataInputPin(
            name=PinName("shape"),
            dtype=Dtype.any(),
            docs="Shape of the array",
        )
        dtype_pin = DataInputPin(
            name=PinName("dtype"),
            dtype=Dtype.any(),
            docs="Data type of the array",
            default=float,
        )
        super().__init__("ones", shape_pin, dtype_pin)

    def apply_function(self, shape, dtype, **kwargs) -> Any:
        return np.ones(shape, dtype=dtype)


class EmptyNode(NumpyFunctionNode):
    """Create uninitialized array."""

    def __init__(self):
        shape_pin = DataInputPin(
            name=PinName("shape"),
            dtype=Dtype.any(),
            docs="Shape of the array",
        )
        dtype_pin = DataInputPin(
            name=PinName("dtype"),
            dtype=Dtype.any(),
            docs="Data type of the array",
            default=float,
        )
        super().__init__("empty", shape_pin, dtype_pin)

    def apply_function(self, shape, dtype, **kwargs) -> Any:
        return np.empty(shape, dtype=dtype)


class EyeNode(NumpyFunctionNode):
    """Create 2-D array with ones on diagonal and zeros elsewhere."""

    def __init__(self):
        n_pin = DataInputPin(
            name=PinName("N"),
            dtype=Dtype.any(),
            docs="Number of rows (and columns)",
        )
        m_pin = DataInputPin(
            name=PinName("M"),
            dtype=Dtype.any(),
            docs="Number of columns (optional)",
            default=None,
        )
        k_pin = DataInputPin(
            name=PinName("k"),
            dtype=Dtype.any(),
            docs="Index of the diagonal",
            default=0,
        )
        dtype_pin = DataInputPin(
            name=PinName("dtype"),
            dtype=Dtype.any(),
            docs="Data type of the array",
            default=float,
        )
        super().__init__("eye", n_pin, m_pin, k_pin, dtype_pin)

    def apply_function(self, n, m, k, dtype, **kwargs) -> Any:
        return np.eye(n, M=m, k=k, dtype=dtype)


class IdentityNode(NumpyFunctionNode):
    """Create identity matrix."""

    def __init__(self):
        n_pin = DataInputPin(
            name=PinName("n"),
            dtype=Dtype.any(),
            docs="Number of rows (and columns)",
        )
        dtype_pin = DataInputPin(
            name=PinName("dtype"),
            dtype=Dtype.any(),
            docs="Data type of the array",
            default=float,
        )
        super().__init__("identity", n_pin, dtype_pin)

    def apply_function(self, n, dtype, **kwargs) -> Any:
        return np.identity(n, dtype=dtype)


class ArangeNode(NumpyFunctionNode):
    """Create evenly spaced values within a given interval."""

    def __init__(self):
        start_pin = DataInputPin(
            name=PinName("start"),
            dtype=Dtype.any(),
            docs="Start of interval",
            default=0,
        )
        stop_pin = DataInputPin(
            name=PinName("stop"),
            dtype=Dtype.any(),
            docs="End of interval (not included)",
        )
        step_pin = DataInputPin(
            name=PinName("step"),
            dtype=Dtype.any(),
            docs="Spacing between values",
            default=1,
        )
        dtype_pin = DataInputPin(
            name=PinName("dtype"),
            dtype=Dtype.any(),
            docs="Data type of the array",
            default=None,
        )
        super().__init__("arange", start_pin, stop_pin, step_pin, dtype_pin)

    def apply_function(self, start, stop, step, dtype, **kwargs) -> Any:
        if dtype is None:
            return np.arange(start, stop, step)
        return np.arange(start, stop, step, dtype=dtype)


class LinspaceNode(NumpyFunctionNode):
    """Create evenly spaced numbers over a specified interval."""

    def __init__(self):
        start_pin = DataInputPin(
            name=PinName("start"),
            dtype=Dtype.any(),
            docs="Start of sequence",
        )
        stop_pin = DataInputPin(
            name=PinName("stop"),
            dtype=Dtype.any(),
            docs="End of sequence",
        )
        num_pin = DataInputPin(
            name=PinName("num"),
            dtype=Dtype.any(),
            docs="Number of samples",
            default=50,
        )
        endpoint_pin = DataInputPin(
            name=PinName("endpoint"),
            dtype=Dtype.any(),
            docs="Include endpoint",
            default=True,
        )
        dtype_pin = DataInputPin(
            name=PinName("dtype"),
            dtype=Dtype.any(),
            docs="Data type of the array",
            default=None,
        )
        super().__init__("linspace", start_pin, stop_pin, num_pin, endpoint_pin, dtype_pin)

    def apply_function(self, start, stop, num, endpoint, dtype, **kwargs) -> Any:
        return np.linspace(start, stop, num=num, endpoint=endpoint, dtype=dtype)


class LogspaceNode(NumpyFunctionNode):
    """Create numbers spaced evenly on a log scale."""

    def __init__(self):
        start_pin = DataInputPin(
            name=PinName("start"),
            dtype=Dtype.any(),
            docs="Start exponent",
        )
        stop_pin = DataInputPin(
            name=PinName("stop"),
            dtype=Dtype.any(),
            docs="End exponent",
        )
        num_pin = DataInputPin(
            name=PinName("num"),
            dtype=Dtype.any(),
            docs="Number of samples",
            default=50,
        )
        base_pin = DataInputPin(
            name=PinName("base"),
            dtype=Dtype.any(),
            docs="Base of the log scale",
            default=10.0,
        )
        dtype_pin = DataInputPin(
            name=PinName("dtype"),
            dtype=Dtype.any(),
            docs="Data type of the array",
            default=None,
        )
        super().__init__("logspace", start_pin, stop_pin, num_pin, base_pin, dtype_pin)

    def apply_function(self, start, stop, num, base, dtype, **kwargs) -> Any:
        return np.logspace(start, stop, num=num, base=base, dtype=dtype)


class FullNode(NumpyFunctionNode):
    """Create array filled with fill_value."""

    def __init__(self):
        shape_pin = DataInputPin(
            name=PinName("shape"),
            dtype=Dtype.any(),
            docs="Shape of the array",
        )
        fill_value_pin = DataInputPin(
            name=PinName("fill_value"),
            dtype=Dtype.any(),
            docs="Fill value",
        )
        dtype_pin = DataInputPin(
            name=PinName("dtype"),
            dtype=Dtype.any(),
            docs="Data type of the array",
            default=None,
        )
        super().__init__("full", shape_pin, fill_value_pin, dtype_pin)

    def apply_function(self, shape, fill_value, dtype, **kwargs) -> Any:
        return np.full(shape, fill_value, dtype=dtype)


def get_array_creation_nodes() -> List[Node]:
    """Get all array creation nodes."""
    return [
        ArrayNode(),
        ZerosNode(),
        OnesNode(),
        EmptyNode(),
        EyeNode(),
        IdentityNode(),
        ArangeNode(),
        LinspaceNode(),
        LogspaceNode(),
        FullNode(),
    ]