# -*- coding: utf-8 -*-

from typing import List

from cvp.nodes.defaults.numpy._base import NumpyUnaryNode, NumpyBinaryNode
from cvp.nodes.node import Node


# Trigonometric functions
class SinNode(NumpyUnaryNode):
    """Trigonometric sine."""
    def __init__(self):
        super().__init__("sin", "x", "Input array in radians")


class CosNode(NumpyUnaryNode):
    """Trigonometric cosine."""
    def __init__(self):
        super().__init__("cos", "x", "Input array in radians")


class TanNode(NumpyUnaryNode):
    """Trigonometric tangent."""
    def __init__(self):
        super().__init__("tan", "x", "Input array in radians")


class ArcsinNode(NumpyUnaryNode):
    """Inverse sine."""
    def __init__(self):
        super().__init__("arcsin", "x", "Input array")


class ArccosNode(NumpyUnaryNode):
    """Inverse cosine."""
    def __init__(self):
        super().__init__("arccos", "x", "Input array")


class ArctanNode(NumpyUnaryNode):
    """Inverse tangent."""
    def __init__(self):
        super().__init__("arctan", "x", "Input array")


class Arctan2Node(NumpyBinaryNode):
    """Element-wise arc tangent of x1/x2."""
    def __init__(self):
        super().__init__("arctan2", "x1", "y-coordinates", "x2", "x-coordinates")


# Hyperbolic functions
class SinhNode(NumpyUnaryNode):
    """Hyperbolic sine."""
    def __init__(self):
        super().__init__("sinh", "x", "Input array")


class CoshNode(NumpyUnaryNode):
    """Hyperbolic cosine."""
    def __init__(self):
        super().__init__("cosh", "x", "Input array")


class TanhNode(NumpyUnaryNode):
    """Hyperbolic tangent."""
    def __init__(self):
        super().__init__("tanh", "x", "Input array")


class ArcsinhNode(NumpyUnaryNode):
    """Inverse hyperbolic sine."""
    def __init__(self):
        super().__init__("arcsinh", "x", "Input array")


class ArccoshNode(NumpyUnaryNode):
    """Inverse hyperbolic cosine."""
    def __init__(self):
        super().__init__("arccosh", "x", "Input array")


class ArctanhNode(NumpyUnaryNode):
    """Inverse hyperbolic tangent."""
    def __init__(self):
        super().__init__("arctanh", "x", "Input array")


# Exponential and logarithmic functions
class ExpNode(NumpyUnaryNode):
    """Calculate the exponential of all elements."""
    def __init__(self):
        super().__init__("exp", "x", "Input array")


class Exp2Node(NumpyUnaryNode):
    """Calculate 2**p for all p in the input array."""
    def __init__(self):
        super().__init__("exp2", "x", "Input array")


class LogNode(NumpyUnaryNode):
    """Natural logarithm."""
    def __init__(self):
        super().__init__("log", "x", "Input array")


class Log2Node(NumpyUnaryNode):
    """Base-2 logarithm."""
    def __init__(self):
        super().__init__("log2", "x", "Input array")


class Log10Node(NumpyUnaryNode):
    """Base-10 logarithm."""
    def __init__(self):
        super().__init__("log10", "x", "Input array")


class Log1pNode(NumpyUnaryNode):
    """Return the natural logarithm of one plus the input array."""
    def __init__(self):
        super().__init__("log1p", "x", "Input array")


class Expm1Node(NumpyUnaryNode):
    """Calculate exp(x) - 1 for all elements."""
    def __init__(self):
        super().__init__("expm1", "x", "Input array")


# Arithmetic operations
class AddNode(NumpyBinaryNode):
    """Add arguments element-wise."""
    def __init__(self):
        super().__init__("add", "x1", "First input array", "x2", "Second input array")


class SubtractNode(NumpyBinaryNode):
    """Subtract arguments element-wise."""
    def __init__(self):
        super().__init__("subtract", "x1", "First input array", "x2", "Second input array")


class MultiplyNode(NumpyBinaryNode):
    """Multiply arguments element-wise."""
    def __init__(self):
        super().__init__("multiply", "x1", "First input array", "x2", "Second input array")


class DivideNode(NumpyBinaryNode):
    """Divide arguments element-wise."""
    def __init__(self):
        super().__init__("divide", "x1", "Dividend array", "x2", "Divisor array")


class TrueDivideNode(NumpyBinaryNode):
    """True division of the inputs, element-wise."""
    def __init__(self):
        super().__init__("true_divide", "x1", "Dividend array", "x2", "Divisor array")


class FloorDivideNode(NumpyBinaryNode):
    """Return the largest integer smaller or equal to the division."""
    def __init__(self):
        super().__init__("floor_divide", "x1", "Dividend array", "x2", "Divisor array")


class PowerNode(NumpyBinaryNode):
    """First array elements raised to powers from second array."""
    def __init__(self):
        super().__init__("power", "x1", "Base array", "x2", "Exponents array")


class ModNode(NumpyBinaryNode):
    """Return element-wise remainder of division."""
    def __init__(self):
        super().__init__("mod", "x1", "Dividend array", "x2", "Divisor array")


class RemainderNode(NumpyBinaryNode):
    """Return element-wise remainder of division."""
    def __init__(self):
        super().__init__("remainder", "x1", "Dividend array", "x2", "Divisor array")


# Rounding
class RoundNode(NumpyUnaryNode):
    """Round elements to the nearest integer."""
    def __init__(self):
        super().__init__("round", "x", "Input array")


class FloorNode(NumpyUnaryNode):
    """Return the floor of the input."""
    def __init__(self):
        super().__init__("floor", "x", "Input array")


class CeilNode(NumpyUnaryNode):
    """Return the ceiling of the input."""
    def __init__(self):
        super().__init__("ceil", "x", "Input array")


class TruncNode(NumpyUnaryNode):
    """Return the truncated value of the input."""
    def __init__(self):
        super().__init__("trunc", "x", "Input array")


# Other mathematical functions
class SqrtNode(NumpyUnaryNode):
    """Return the positive square-root of an array."""
    def __init__(self):
        super().__init__("sqrt", "x", "Input array")


class SquareNode(NumpyUnaryNode):
    """Return the element-wise square of the input."""
    def __init__(self):
        super().__init__("square", "x", "Input array")


class AbsoluteNode(NumpyUnaryNode):
    """Calculate the absolute value element-wise."""
    def __init__(self):
        super().__init__("absolute", "x", "Input array")


class FabsNode(NumpyUnaryNode):
    """Compute the absolute values element-wise."""
    def __init__(self):
        super().__init__("fabs", "x", "Input array")


class SignNode(NumpyUnaryNode):
    """Returns element-wise indication of the sign of a number."""
    def __init__(self):
        super().__init__("sign", "x", "Input array")


class NegativeNode(NumpyUnaryNode):
    """Numerical negative, element-wise."""
    def __init__(self):
        super().__init__("negative", "x", "Input array")


class PositiveNode(NumpyUnaryNode):
    """Numerical positive, element-wise."""
    def __init__(self):
        super().__init__("positive", "x", "Input array")


class ReciprocalNode(NumpyUnaryNode):
    """Return the reciprocal of the argument."""
    def __init__(self):
        super().__init__("reciprocal", "x", "Input array")


class MaximumNode(NumpyBinaryNode):
    """Element-wise maximum of array elements."""
    def __init__(self):
        super().__init__("maximum", "x1", "First input array", "x2", "Second input array")


class MinimumNode(NumpyBinaryNode):
    """Element-wise minimum of array elements."""
    def __init__(self):
        super().__init__("minimum", "x1", "First input array", "x2", "Second input array")


class FmaxNode(NumpyBinaryNode):
    """Element-wise maximum, ignores NaNs."""
    def __init__(self):
        super().__init__("fmax", "x1", "First input array", "x2", "Second input array")


class FminNode(NumpyBinaryNode):
    """Element-wise minimum, ignores NaNs."""
    def __init__(self):
        super().__init__("fmin", "x1", "First input array", "x2", "Second input array")


def get_mathematical_nodes() -> List[Node]:
    """Get all mathematical nodes."""
    return [
        # Trigonometric
        SinNode(),
        CosNode(),
        TanNode(),
        ArcsinNode(),
        ArccosNode(),
        ArctanNode(),
        Arctan2Node(),

        # Hyperbolic
        SinhNode(),
        CoshNode(),
        TanhNode(),
        ArcsinhNode(),
        ArccoshNode(),
        ArctanhNode(),

        # Exponential and logarithmic
        ExpNode(),
        Exp2Node(),
        LogNode(),
        Log2Node(),
        Log10Node(),
        Log1pNode(),
        Expm1Node(),

        # Arithmetic
        AddNode(),
        SubtractNode(),
        MultiplyNode(),
        DivideNode(),
        TrueDivideNode(),
        FloorDivideNode(),
        PowerNode(),
        ModNode(),
        RemainderNode(),

        # Rounding
        RoundNode(),
        FloorNode(),
        CeilNode(),
        TruncNode(),

        # Other
        SqrtNode(),
        SquareNode(),
        AbsoluteNode(),
        FabsNode(),
        SignNode(),
        NegativeNode(),
        PositiveNode(),
        ReciprocalNode(),
        MaximumNode(),
        MinimumNode(),
        FmaxNode(),
        FminNode(),
    ]