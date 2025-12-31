# -*- coding: utf-8 -*-

from typing import Any, List

import numpy as np

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.numpy._base import NumpyFunctionNode, NumpyUnaryNode
from cvp.nodes.node import Node
from cvp.nodes.record import NodeRecord
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import Pin, PinName
from cvp.types.override import override


class ReshapeNode(NumpyFunctionNode):
    """Give a new shape to an array without changing its data."""

    def __init__(self):
        array_pin = DataInputPin(
            name=PinName("a"),
            dtype=Dtype.any(),
            docs="Array to be reshaped",
        )
        newshape_pin = DataInputPin(
            name=PinName("newshape"),
            dtype=Dtype.any(),
            docs="The new shape should be compatible with the original shape",
        )
        super().__init__("reshape", array_pin, newshape_pin)

    def apply_function(self, a, newshape, **kwargs) -> Any:
        return np.reshape(a, newshape)


class TransposeNode(NumpyUnaryNode):
    """Reverse or permute the axes of an array."""
    def __init__(self):
        super().__init__("transpose", "a", "Input array")


class SwapaxesNode(NumpyFunctionNode):
    """Interchange two axes of an array."""

    def __init__(self):
        array_pin = DataInputPin(
            name=PinName("a"),
            dtype=Dtype.any(),
            docs="Input array",
        )
        axis1_pin = DataInputPin(
            name=PinName("axis1"),
            dtype=Dtype.any(),
            docs="First axis",
        )
        axis2_pin = DataInputPin(
            name=PinName("axis2"),
            dtype=Dtype.any(),
            docs="Second axis",
        )
        super().__init__("swapaxes", array_pin, axis1_pin, axis2_pin)

    def apply_function(self, a, axis1, axis2, **kwargs) -> Any:
        return np.swapaxes(a, axis1, axis2)


class MoveaxisNode(NumpyFunctionNode):
    """Move axes of an array to new positions."""

    def __init__(self):
        array_pin = DataInputPin(
            name=PinName("a"),
            dtype=Dtype.any(),
            docs="Input array",
        )
        source_pin = DataInputPin(
            name=PinName("source"),
            dtype=Dtype.any(),
            docs="Original positions of the axes to move",
        )
        destination_pin = DataInputPin(
            name=PinName("destination"),
            dtype=Dtype.any(),
            docs="Destination positions for each of the original axes",
        )
        super().__init__("moveaxis", array_pin, source_pin, destination_pin)

    def apply_function(self, a, source, destination, **kwargs) -> Any:
        return np.moveaxis(a, source, destination)


class FlipNode(NumpyFunctionNode):
    """Reverse the order of elements in an array along the given axis."""

    def __init__(self):
        array_pin = DataInputPin(
            name=PinName("m"),
            dtype=Dtype.any(),
            docs="Input array",
        )
        axis_pin = DataInputPin(
            name=PinName("axis"),
            dtype=Dtype.any(),
            docs="Axis or axes along which to flip over",
            default=None,
        )
        super().__init__("flip", array_pin, axis_pin)

    def apply_function(self, m, axis, **kwargs) -> Any:
        return np.flip(m, axis=axis)


class FliplrNode(NumpyUnaryNode):
    """Flip array in the left/right direction."""
    def __init__(self):
        super().__init__("fliplr", "m", "Input array")


class FlipudNode(NumpyUnaryNode):
    """Flip array in the up/down direction."""
    def __init__(self):
        super().__init__("flipud", "m", "Input array")


class SqueezeNode(NumpyFunctionNode):
    """Remove single-dimensional entries from the shape of an array."""

    def __init__(self):
        array_pin = DataInputPin(
            name=PinName("a"),
            dtype=Dtype.any(),
            docs="Input array",
        )
        axis_pin = DataInputPin(
            name=PinName("axis"),
            dtype=Dtype.any(),
            docs="Selects a subset of the single-dimensional entries",
            default=None,
        )
        super().__init__("squeeze", array_pin, axis_pin)

    def apply_function(self, a, axis, **kwargs) -> Any:
        return np.squeeze(a, axis=axis)


class ExpandDimsNode(NumpyFunctionNode):
    """Expand the shape of an array."""

    def __init__(self):
        array_pin = DataInputPin(
            name=PinName("a"),
            dtype=Dtype.any(),
            docs="Input array",
        )
        axis_pin = DataInputPin(
            name=PinName("axis"),
            dtype=Dtype.any(),
            docs="Position in the expanded axes where the new axis is placed",
        )
        super().__init__("expand_dims", array_pin, axis_pin)

    def apply_function(self, a, axis, **kwargs) -> Any:
        return np.expand_dims(a, axis=axis)


class ConcatenateNode(NumpyFunctionNode):
    """Join a sequence of arrays along an existing axis."""

    def __init__(self):
        arrays_pin = DataInputPin(
            name=PinName("arrays"),
            dtype=Dtype.any(),
            docs="Sequence of arrays",
        )
        axis_pin = DataInputPin(
            name=PinName("axis"),
            dtype=Dtype.any(),
            docs="Axis along which the arrays will be joined",
            default=0,
        )
        super().__init__("concatenate", arrays_pin, axis_pin)

    def apply_function(self, arrays, axis, **kwargs) -> Any:
        return np.concatenate(arrays, axis=axis)


class StackNode(NumpyFunctionNode):
    """Join a sequence of arrays along a new axis."""

    def __init__(self):
        arrays_pin = DataInputPin(
            name=PinName("arrays"),
            dtype=Dtype.any(),
            docs="Sequence of arrays",
        )
        axis_pin = DataInputPin(
            name=PinName("axis"),
            dtype=Dtype.any(),
            docs="Axis in the result array along which the input arrays are stacked",
            default=0,
        )
        super().__init__("stack", arrays_pin, axis_pin)

    def apply_function(self, arrays, axis, **kwargs) -> Any:
        return np.stack(arrays, axis=axis)


class HstackNode(NumpyFunctionNode):
    """Stack arrays in sequence horizontally (column wise)."""

    def __init__(self):
        arrays_pin = DataInputPin(
            name=PinName("tup"),
            dtype=Dtype.any(),
            docs="Sequence of arrays",
        )
        super().__init__("hstack", arrays_pin)

    def apply_function(self, tup, **kwargs) -> Any:
        return np.hstack(tup)


class VstackNode(NumpyFunctionNode):
    """Stack arrays in sequence vertically (row wise)."""

    def __init__(self):
        arrays_pin = DataInputPin(
            name=PinName("tup"),
            dtype=Dtype.any(),
            docs="Sequence of arrays",
        )
        super().__init__("vstack", arrays_pin)

    def apply_function(self, tup, **kwargs) -> Any:
        return np.vstack(tup)


class DstackNode(NumpyFunctionNode):
    """Stack arrays in sequence depth wise (along third axis)."""

    def __init__(self):
        arrays_pin = DataInputPin(
            name=PinName("tup"),
            dtype=Dtype.any(),
            docs="Sequence of arrays",
        )
        super().__init__("dstack", arrays_pin)

    def apply_function(self, tup, **kwargs) -> Any:
        return np.dstack(tup)


class SplitNode(NumpyFunctionNode):
    """Split an array into multiple sub-arrays as views into array."""

    def __init__(self):
        array_pin = DataInputPin(
            name=PinName("ary"),
            dtype=Dtype.any(),
            docs="Array to be divided into sub-arrays",
        )
        indices_pin = DataInputPin(
            name=PinName("indices_or_sections"),
            dtype=Dtype.any(),
            docs="If integer, number of equal sections",
        )
        axis_pin = DataInputPin(
            name=PinName("axis"),
            dtype=Dtype.any(),
            docs="Axis along which to split",
            default=0,
        )
        super().__init__("split", array_pin, indices_pin, axis_pin)

    def apply_function(self, ary, indices_or_sections, axis, **kwargs) -> Any:
        return np.split(ary, indices_or_sections, axis=axis)


class HsplitNode(NumpyFunctionNode):
    """Split an array into multiple sub-arrays horizontally (column-wise)."""

    def __init__(self):
        array_pin = DataInputPin(
            name=PinName("ary"),
            dtype=Dtype.any(),
            docs="Array to be divided into sub-arrays",
        )
        indices_pin = DataInputPin(
            name=PinName("indices_or_sections"),
            dtype=Dtype.any(),
            docs="If integer, number of equal sections",
        )
        super().__init__("hsplit", array_pin, indices_pin)

    def apply_function(self, ary, indices_or_sections, **kwargs) -> Any:
        return np.hsplit(ary, indices_or_sections)


class VsplitNode(NumpyFunctionNode):
    """Split an array into multiple sub-arrays vertically (row-wise)."""

    def __init__(self):
        array_pin = DataInputPin(
            name=PinName("ary"),
            dtype=Dtype.any(),
            docs="Array to be divided into sub-arrays",
        )
        indices_pin = DataInputPin(
            name=PinName("indices_or_sections"),
            dtype=Dtype.any(),
            docs="If integer, number of equal sections",
        )
        super().__init__("vsplit", array_pin, indices_pin)

    def apply_function(self, ary, indices_or_sections, **kwargs) -> Any:
        return np.vsplit(ary, indices_or_sections)


class DsplitNode(NumpyFunctionNode):
    """Split array along the 3rd axis (depth)."""

    def __init__(self):
        array_pin = DataInputPin(
            name=PinName("ary"),
            dtype=Dtype.any(),
            docs="Array to be divided into sub-arrays",
        )
        indices_pin = DataInputPin(
            name=PinName("indices_or_sections"),
            dtype=Dtype.any(),
            docs="If integer, number of equal sections",
        )
        super().__init__("dsplit", array_pin, indices_pin)

    def apply_function(self, ary, indices_or_sections, **kwargs) -> Any:
        return np.dsplit(ary, indices_or_sections)


class TileNode(NumpyFunctionNode):
    """Construct an array by repeating A the number of times given by reps."""

    def __init__(self):
        array_pin = DataInputPin(
            name=PinName("A"),
            dtype=Dtype.any(),
            docs="Input array",
        )
        reps_pin = DataInputPin(
            name=PinName("reps"),
            dtype=Dtype.any(),
            docs="Number of repetitions along each axis",
        )
        super().__init__("tile", array_pin, reps_pin)

    def apply_function(self, A, reps, **kwargs) -> Any:
        return np.tile(A, reps)


class RepeatNode(NumpyFunctionNode):
    """Repeat elements of an array."""

    def __init__(self):
        array_pin = DataInputPin(
            name=PinName("a"),
            dtype=Dtype.any(),
            docs="Input array",
        )
        repeats_pin = DataInputPin(
            name=PinName("repeats"),
            dtype=Dtype.any(),
            docs="Number of repetitions for each element",
        )
        axis_pin = DataInputPin(
            name=PinName("axis"),
            dtype=Dtype.any(),
            docs="Axis along which to repeat values",
            default=None,
        )
        super().__init__("repeat", array_pin, repeats_pin, axis_pin)

    def apply_function(self, a, repeats, axis, **kwargs) -> Any:
        return np.repeat(a, repeats, axis=axis)


class FlattenNode(NumpyFunctionNode):
    """Return a copy of the array collapsed into one dimension."""

    def __init__(self):
        array_pin = DataInputPin(
            name=PinName("a"),
            dtype=Dtype.any(),
            docs="Input array",
        )
        super().__init__("flatten", array_pin)

    def apply_function(self, a, **kwargs) -> Any:
        return a.flatten()


class RavelNode(NumpyFunctionNode):
    """Return a contiguous flattened array."""

    def __init__(self):
        array_pin = DataInputPin(
            name=PinName("a"),
            dtype=Dtype.any(),
            docs="Input array",
        )
        super().__init__("ravel", array_pin)

    def apply_function(self, a, **kwargs) -> Any:
        return np.ravel(a)


def get_array_manipulation_nodes() -> List[Node]:
    """Get all array manipulation nodes."""
    return [
        ReshapeNode(),
        TransposeNode(),
        SwapaxesNode(),
        MoveaxisNode(),
        FlipNode(),
        FliplrNode(),
        FlipudNode(),
        SqueezeNode(),
        ExpandDimsNode(),
        ConcatenateNode(),
        StackNode(),
        HstackNode(),
        VstackNode(),
        DstackNode(),
        SplitNode(),
        HsplitNode(),
        VsplitNode(),
        DsplitNode(),
        TileNode(),
        RepeatNode(),
        FlattenNode(),
        RavelNode(),
    ]