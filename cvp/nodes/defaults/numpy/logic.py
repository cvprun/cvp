# -*- coding: utf-8 -*-

from typing import Any, List

from cvp.nodes.defaults.numpy._base import NumpyUnaryNode, NumpyBinaryNode, NumpyFunctionNode
from cvp.nodes.node import Node
from cvp.dtypes.dtype import Dtype
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import PinName
from cvp.types.override import override
import numpy as np


# Truth value testing
class AllNode(NumpyFunctionNode):
    """Test whether all array elements along a given axis evaluate to True."""

    def __init__(self):
        array_pin = DataInputPin(
            name=PinName("a"),
            dtype=Dtype.any(),
            docs="Input array",
        )
        axis_pin = DataInputPin(
            name=PinName("axis"),
            dtype=Dtype.any(),
            docs="Axis along which a logical AND reduction is performed",
            default=None,
        )
        keepdims_pin = DataInputPin(
            name=PinName("keepdims"),
            dtype=Dtype.any(),
            docs="Keep the dimensions of the result",
            default=False,
        )
        super().__init__("all", array_pin, axis_pin, keepdims_pin)

    def apply_function(self, a, axis, keepdims, **kwargs) -> Any:
        return np.all(a, axis=axis, keepdims=keepdims)


class AnyNode(NumpyFunctionNode):
    """Test whether any array element along a given axis evaluates to True."""

    def __init__(self):
        array_pin = DataInputPin(
            name=PinName("a"),
            dtype=Dtype.any(),
            docs="Input array",
        )
        axis_pin = DataInputPin(
            name=PinName("axis"),
            dtype=Dtype.any(),
            docs="Axis along which a logical OR reduction is performed",
            default=None,
        )
        keepdims_pin = DataInputPin(
            name=PinName("keepdims"),
            dtype=Dtype.any(),
            docs="Keep the dimensions of the result",
            default=False,
        )
        super().__init__("any", array_pin, axis_pin, keepdims_pin)

    def apply_function(self, a, axis, keepdims, **kwargs) -> Any:
        return np.any(a, axis=axis, keepdims=keepdims)


# Array contents
class IsfiniteNode(NumpyUnaryNode):
    """Test finiteness element-wise."""
    def __init__(self):
        super().__init__("isfinite", "x", "Input array")


class IsinfiniteNode(NumpyUnaryNode):
    """Test for positive or negative infinity."""
    def __init__(self):
        super().__init__("isinf", "x", "Input array")


class IsnanNode(NumpyUnaryNode):
    """Test for NaN element-wise."""
    def __init__(self):
        super().__init__("isnan", "x", "Input array")


class IsnatNode(NumpyUnaryNode):
    """Test for NaT (not a time) element-wise."""
    def __init__(self):
        super().__init__("isnat", "x", "Input array")


class IsneginfiniteNode(NumpyUnaryNode):
    """Test for negative infinity."""
    def __init__(self):
        super().__init__("isneginf", "x", "Input array")


class IsposinfiniteNode(NumpyUnaryNode):
    """Test for positive infinity."""
    def __init__(self):
        super().__init__("isposinf", "x", "Input array")


# Logical operations
class LogicalAndNode(NumpyBinaryNode):
    """Compute the truth value of x1 AND x2 element-wise."""
    def __init__(self):
        super().__init__("logical_and", "x1", "First input array", "x2", "Second input array")


class LogicalOrNode(NumpyBinaryNode):
    """Compute the truth value of x1 OR x2 element-wise."""
    def __init__(self):
        super().__init__("logical_or", "x1", "First input array", "x2", "Second input array")


class LogicalNotNode(NumpyUnaryNode):
    """Compute the truth value of NOT x element-wise."""
    def __init__(self):
        super().__init__("logical_not", "x", "Input array")


class LogicalXorNode(NumpyBinaryNode):
    """Compute the truth value of x1 XOR x2, element-wise."""
    def __init__(self):
        super().__init__("logical_xor", "x1", "First input array", "x2", "Second input array")


# Comparison
class GreaterNode(NumpyBinaryNode):
    """Return the truth value of (x1 > x2) element-wise."""
    def __init__(self):
        super().__init__("greater", "x1", "First input array", "x2", "Second input array")


class GreaterEqualNode(NumpyBinaryNode):
    """Return the truth value of (x1 >= x2) element-wise."""
    def __init__(self):
        super().__init__("greater_equal", "x1", "First input array", "x2", "Second input array")


class LessNode(NumpyBinaryNode):
    """Return the truth value of (x1 < x2) element-wise."""
    def __init__(self):
        super().__init__("less", "x1", "First input array", "x2", "Second input array")


class LessEqualNode(NumpyBinaryNode):
    """Return the truth value of (x1 <= x2) element-wise."""
    def __init__(self):
        super().__init__("less_equal", "x1", "First input array", "x2", "Second input array")


class EqualNode(NumpyBinaryNode):
    """Return (x1 == x2) element-wise."""
    def __init__(self):
        super().__init__("equal", "x1", "First input array", "x2", "Second input array")


class NotEqualNode(NumpyBinaryNode):
    """Return (x1 != x2) element-wise."""
    def __init__(self):
        super().__init__("not_equal", "x1", "First input array", "x2", "Second input array")


# Selection
class WhereNode(NumpyFunctionNode):
    """Return elements chosen from x or y depending on condition."""

    def __init__(self):
        condition_pin = DataInputPin(
            name=PinName("condition"),
            dtype=Dtype.any(),
            docs="Where True, yield x, otherwise yield y",
        )
        x_pin = DataInputPin(
            name=PinName("x"),
            dtype=Dtype.any(),
            docs="Values from which to choose when condition is True",
            default=None,
        )
        y_pin = DataInputPin(
            name=PinName("y"),
            dtype=Dtype.any(),
            docs="Values from which to choose when condition is False",
            default=None,
        )
        super().__init__("where", condition_pin, x_pin, y_pin)

    def apply_function(self, condition, x, y, **kwargs) -> Any:
        if x is None and y is None:
            return np.where(condition)
        return np.where(condition, x, y)


class SelectNode(NumpyFunctionNode):
    """Return an array drawn from elements in choicelist, depending on conditions."""

    def __init__(self):
        condlist_pin = DataInputPin(
            name=PinName("condlist"),
            dtype=Dtype.any(),
            docs="List of conditions which determine from which array to choose",
        )
        choicelist_pin = DataInputPin(
            name=PinName("choicelist"),
            dtype=Dtype.any(),
            docs="List of arrays from which to choose",
        )
        default_pin = DataInputPin(
            name=PinName("default"),
            dtype=Dtype.any(),
            docs="Element inserted in output when all conditions evaluate to False",
            default=0,
        )
        super().__init__("select", condlist_pin, choicelist_pin, default_pin)

    def apply_function(self, condlist, choicelist, default, **kwargs) -> Any:
        return np.select(condlist, choicelist, default=default)


class NonzeroNode(NumpyUnaryNode):
    """Return the indices of the elements that are non-zero."""
    def __init__(self):
        super().__init__("nonzero", "a", "Input array")


class FlatnonzeroNode(NumpyUnaryNode):
    """Return indices that are non-zero in the flattened version of a."""
    def __init__(self):
        super().__init__("flatnonzero", "a", "Input array")


class ArgwhereNode(NumpyUnaryNode):
    """Find the indices of array elements that are non-zero, grouped by element."""
    def __init__(self):
        super().__init__("argwhere", "a", "Input array")


# Type testing
class IscomplexNode(NumpyUnaryNode):
    """Returns a bool array, where True if input element is complex."""
    def __init__(self):
        super().__init__("iscomplex", "x", "Input array")


class IscomplexobjNode(NumpyUnaryNode):
    """Check for a complex type or an array of complex numbers."""
    def __init__(self):
        super().__init__("iscomplexobj", "x", "Input array")


class IsrealNode(NumpyUnaryNode):
    """Returns a bool array, where True if input element is real."""
    def __init__(self):
        super().__init__("isreal", "x", "Input array")


class IsrealobjNode(NumpyUnaryNode):
    """Return True if x is a not complex type or an array of complex numbers."""
    def __init__(self):
        super().__init__("isrealobj", "x", "Input array")


class IsscalarNode(NumpyFunctionNode):
    """Returns True if the type of num is a scalar type."""

    def __init__(self):
        num_pin = DataInputPin(
            name=PinName("num"),
            dtype=Dtype.any(),
            docs="Input argument",
        )
        super().__init__("isscalar", num_pin)

    def apply_function(self, num, **kwargs) -> Any:
        return np.isscalar(num)


def get_logic_nodes() -> List[Node]:
    """Get all logic nodes."""
    return [
        # Truth value testing
        AllNode(),
        AnyNode(),

        # Array contents
        IsfiniteNode(),
        IsinfiniteNode(),
        IsnanNode(),
        IsnatNode(),
        IsneginfiniteNode(),
        IsposinfiniteNode(),

        # Logical operations
        LogicalAndNode(),
        LogicalOrNode(),
        LogicalNotNode(),
        LogicalXorNode(),

        # Comparison
        GreaterNode(),
        GreaterEqualNode(),
        LessNode(),
        LessEqualNode(),
        EqualNode(),
        NotEqualNode(),

        # Selection
        WhereNode(),
        SelectNode(),
        NonzeroNode(),
        FlatnonzeroNode(),
        ArgwhereNode(),

        # Type testing
        IscomplexNode(),
        IscomplexobjNode(),
        IsrealNode(),
        IsrealobjNode(),
        IsscalarNode(),
    ]