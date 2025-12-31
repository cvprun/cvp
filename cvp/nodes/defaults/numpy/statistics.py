# -*- coding: utf-8 -*-

from typing import Any, List

import numpy as np

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.numpy._base import NumpyFunctionNode
from cvp.nodes.node import Node
from cvp.nodes.record import NodeRecord
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import Pin, PinName
from cvp.types.override import override


class MeanNode(NumpyFunctionNode):
    """Compute the arithmetic mean along the specified axis."""

    def __init__(self):
        array_pin = DataInputPin(
            name=PinName("a"),
            dtype=Dtype.any(),
            docs="Array containing numbers whose mean is desired",
        )
        axis_pin = DataInputPin(
            name=PinName("axis"),
            dtype=Dtype.any(),
            docs="Axis along which the means are computed",
            default=None,
        )
        keepdims_pin = DataInputPin(
            name=PinName("keepdims"),
            dtype=Dtype.any(),
            docs="Keep the dimensions of the result",
            default=False,
        )
        super().__init__("mean", array_pin, axis_pin, keepdims_pin)

    def apply_function(self, a, axis, keepdims, **kwargs) -> Any:
        return np.mean(a, axis=axis, keepdims=keepdims)


class MedianNode(NumpyFunctionNode):
    """Compute the median along the specified axis."""

    def __init__(self):
        array_pin = DataInputPin(
            name=PinName("a"),
            dtype=Dtype.any(),
            docs="Input array",
        )
        axis_pin = DataInputPin(
            name=PinName("axis"),
            dtype=Dtype.any(),
            docs="Axis along which the medians are computed",
            default=None,
        )
        keepdims_pin = DataInputPin(
            name=PinName("keepdims"),
            dtype=Dtype.any(),
            docs="Keep the dimensions of the result",
            default=False,
        )
        super().__init__("median", array_pin, axis_pin, keepdims_pin)

    def apply_function(self, a, axis, keepdims, **kwargs) -> Any:
        return np.median(a, axis=axis, keepdims=keepdims)


class StdNode(NumpyFunctionNode):
    """Compute the standard deviation along the specified axis."""

    def __init__(self):
        array_pin = DataInputPin(
            name=PinName("a"),
            dtype=Dtype.any(),
            docs="Array containing numbers whose standard deviation is desired",
        )
        axis_pin = DataInputPin(
            name=PinName("axis"),
            dtype=Dtype.any(),
            docs="Axis along which the standard deviation is computed",
            default=None,
        )
        ddof_pin = DataInputPin(
            name=PinName("ddof"),
            dtype=Dtype.any(),
            docs="Delta degrees of freedom",
            default=0,
        )
        keepdims_pin = DataInputPin(
            name=PinName("keepdims"),
            dtype=Dtype.any(),
            docs="Keep the dimensions of the result",
            default=False,
        )
        super().__init__("std", array_pin, axis_pin, ddof_pin, keepdims_pin)

    def apply_function(self, a, axis, ddof, keepdims, **kwargs) -> Any:
        return np.std(a, axis=axis, ddof=ddof, keepdims=keepdims)


class VarNode(NumpyFunctionNode):
    """Compute the variance along the specified axis."""

    def __init__(self):
        array_pin = DataInputPin(
            name=PinName("a"),
            dtype=Dtype.any(),
            docs="Array containing numbers whose variance is desired",
        )
        axis_pin = DataInputPin(
            name=PinName("axis"),
            dtype=Dtype.any(),
            docs="Axis along which the variance is computed",
            default=None,
        )
        ddof_pin = DataInputPin(
            name=PinName("ddof"),
            dtype=Dtype.any(),
            docs="Delta degrees of freedom",
            default=0,
        )
        keepdims_pin = DataInputPin(
            name=PinName("keepdims"),
            dtype=Dtype.any(),
            docs="Keep the dimensions of the result",
            default=False,
        )
        super().__init__("var", array_pin, axis_pin, ddof_pin, keepdims_pin)

    def apply_function(self, a, axis, ddof, keepdims, **kwargs) -> Any:
        return np.var(a, axis=axis, ddof=ddof, keepdims=keepdims)


class MinNode(NumpyFunctionNode):
    """Return the minimum of an array or minimum along an axis."""

    def __init__(self):
        array_pin = DataInputPin(
            name=PinName("a"),
            dtype=Dtype.any(),
            docs="Input array",
        )
        axis_pin = DataInputPin(
            name=PinName("axis"),
            dtype=Dtype.any(),
            docs="Axis along which to operate",
            default=None,
        )
        keepdims_pin = DataInputPin(
            name=PinName("keepdims"),
            dtype=Dtype.any(),
            docs="Keep the dimensions of the result",
            default=False,
        )
        super().__init__("min", array_pin, axis_pin, keepdims_pin)

    def apply_function(self, a, axis, keepdims, **kwargs) -> Any:
        return np.min(a, axis=axis, keepdims=keepdims)


class MaxNode(NumpyFunctionNode):
    """Return the maximum of an array or maximum along an axis."""

    def __init__(self):
        array_pin = DataInputPin(
            name=PinName("a"),
            dtype=Dtype.any(),
            docs="Input array",
        )
        axis_pin = DataInputPin(
            name=PinName("axis"),
            dtype=Dtype.any(),
            docs="Axis along which to operate",
            default=None,
        )
        keepdims_pin = DataInputPin(
            name=PinName("keepdims"),
            dtype=Dtype.any(),
            docs="Keep the dimensions of the result",
            default=False,
        )
        super().__init__("max", array_pin, axis_pin, keepdims_pin)

    def apply_function(self, a, axis, keepdims, **kwargs) -> Any:
        return np.max(a, axis=axis, keepdims=keepdims)


class PtpNode(NumpyFunctionNode):
    """Range of values (maximum - minimum) along an axis."""

    def __init__(self):
        array_pin = DataInputPin(
            name=PinName("a"),
            dtype=Dtype.any(),
            docs="Input array",
        )
        axis_pin = DataInputPin(
            name=PinName("axis"),
            dtype=Dtype.any(),
            docs="Axis along which to find the peaks",
            default=None,
        )
        keepdims_pin = DataInputPin(
            name=PinName("keepdims"),
            dtype=Dtype.any(),
            docs="Keep the dimensions of the result",
            default=False,
        )
        super().__init__("ptp", array_pin, axis_pin, keepdims_pin)

    def apply_function(self, a, axis, keepdims, **kwargs) -> Any:
        return np.ptp(a, axis=axis, keepdims=keepdims)


class PercentileNode(NumpyFunctionNode):
    """Compute the qth percentile of the data along the specified axis."""

    def __init__(self):
        array_pin = DataInputPin(
            name=PinName("a"),
            dtype=Dtype.any(),
            docs="Input array",
        )
        q_pin = DataInputPin(
            name=PinName("q"),
            dtype=Dtype.any(),
            docs="Percentile or sequence of percentiles to compute",
        )
        axis_pin = DataInputPin(
            name=PinName("axis"),
            dtype=Dtype.any(),
            docs="Axis along which the percentiles are computed",
            default=None,
        )
        keepdims_pin = DataInputPin(
            name=PinName("keepdims"),
            dtype=Dtype.any(),
            docs="Keep the dimensions of the result",
            default=False,
        )
        super().__init__("percentile", array_pin, q_pin, axis_pin, keepdims_pin)

    def apply_function(self, a, q, axis, keepdims, **kwargs) -> Any:
        return np.percentile(a, q, axis=axis, keepdims=keepdims)


class QuantileNode(NumpyFunctionNode):
    """Compute the qth quantile of the data along the specified axis."""

    def __init__(self):
        array_pin = DataInputPin(
            name=PinName("a"),
            dtype=Dtype.any(),
            docs="Input array",
        )
        q_pin = DataInputPin(
            name=PinName("q"),
            dtype=Dtype.any(),
            docs="Quantile or sequence of quantiles to compute",
        )
        axis_pin = DataInputPin(
            name=PinName("axis"),
            dtype=Dtype.any(),
            docs="Axis along which the quantiles are computed",
            default=None,
        )
        keepdims_pin = DataInputPin(
            name=PinName("keepdims"),
            dtype=Dtype.any(),
            docs="Keep the dimensions of the result",
            default=False,
        )
        super().__init__("quantile", array_pin, q_pin, axis_pin, keepdims_pin)

    def apply_function(self, a, q, axis, keepdims, **kwargs) -> Any:
        return np.quantile(a, q, axis=axis, keepdims=keepdims)


class SumNode(NumpyFunctionNode):
    """Sum of array elements over a given axis."""

    def __init__(self):
        array_pin = DataInputPin(
            name=PinName("a"),
            dtype=Dtype.any(),
            docs="Elements to sum",
        )
        axis_pin = DataInputPin(
            name=PinName("axis"),
            dtype=Dtype.any(),
            docs="Axis along which a sum is performed",
            default=None,
        )
        keepdims_pin = DataInputPin(
            name=PinName("keepdims"),
            dtype=Dtype.any(),
            docs="Keep the dimensions of the result",
            default=False,
        )
        super().__init__("sum", array_pin, axis_pin, keepdims_pin)

    def apply_function(self, a, axis, keepdims, **kwargs) -> Any:
        return np.sum(a, axis=axis, keepdims=keepdims)


class ProdNode(NumpyFunctionNode):
    """Return the product of array elements over a given axis."""

    def __init__(self):
        array_pin = DataInputPin(
            name=PinName("a"),
            dtype=Dtype.any(),
            docs="Input array",
        )
        axis_pin = DataInputPin(
            name=PinName("axis"),
            dtype=Dtype.any(),
            docs="Axis along which a product is performed",
            default=None,
        )
        keepdims_pin = DataInputPin(
            name=PinName("keepdims"),
            dtype=Dtype.any(),
            docs="Keep the dimensions of the result",
            default=False,
        )
        super().__init__("prod", array_pin, axis_pin, keepdims_pin)

    def apply_function(self, a, axis, keepdims, **kwargs) -> Any:
        return np.prod(a, axis=axis, keepdims=keepdims)


class CumsumNode(NumpyFunctionNode):
    """Return the cumulative sum of the elements along a given axis."""

    def __init__(self):
        array_pin = DataInputPin(
            name=PinName("a"),
            dtype=Dtype.any(),
            docs="Input array",
        )
        axis_pin = DataInputPin(
            name=PinName("axis"),
            dtype=Dtype.any(),
            docs="Axis along which the cumulative sum is computed",
            default=None,
        )
        super().__init__("cumsum", array_pin, axis_pin)

    def apply_function(self, a, axis, **kwargs) -> Any:
        return np.cumsum(a, axis=axis)


class CumprodNode(NumpyFunctionNode):
    """Return the cumulative product of elements along a given axis."""

    def __init__(self):
        array_pin = DataInputPin(
            name=PinName("a"),
            dtype=Dtype.any(),
            docs="Input array",
        )
        axis_pin = DataInputPin(
            name=PinName("axis"),
            dtype=Dtype.any(),
            docs="Axis along which the cumulative product is computed",
            default=None,
        )
        super().__init__("cumprod", array_pin, axis_pin)

    def apply_function(self, a, axis, **kwargs) -> Any:
        return np.cumprod(a, axis=axis)


class ArgminNode(NumpyFunctionNode):
    """Returns the indices of the minimum values along an axis."""

    def __init__(self):
        array_pin = DataInputPin(
            name=PinName("a"),
            dtype=Dtype.any(),
            docs="Input array",
        )
        axis_pin = DataInputPin(
            name=PinName("axis"),
            dtype=Dtype.any(),
            docs="Axis along which to search",
            default=None,
        )
        super().__init__("argmin", array_pin, axis_pin)

    def apply_function(self, a, axis, **kwargs) -> Any:
        return np.argmin(a, axis=axis)


class ArgmaxNode(NumpyFunctionNode):
    """Returns the indices of the maximum values along an axis."""

    def __init__(self):
        array_pin = DataInputPin(
            name=PinName("a"),
            dtype=Dtype.any(),
            docs="Input array",
        )
        axis_pin = DataInputPin(
            name=PinName("axis"),
            dtype=Dtype.any(),
            docs="Axis along which to search",
            default=None,
        )
        super().__init__("argmax", array_pin, axis_pin)

    def apply_function(self, a, axis, **kwargs) -> Any:
        return np.argmax(a, axis=axis)


class ArgsortNode(NumpyFunctionNode):
    """Returns the indices that would sort an array."""

    def __init__(self):
        array_pin = DataInputPin(
            name=PinName("a"),
            dtype=Dtype.any(),
            docs="Array to sort",
        )
        axis_pin = DataInputPin(
            name=PinName("axis"),
            dtype=Dtype.any(),
            docs="Axis along which to sort",
            default=-1,
        )
        kind_pin = DataInputPin(
            name=PinName("kind"),
            dtype=Dtype.any(),
            docs="Sorting algorithm",
            default=None,
        )
        super().__init__("argsort", array_pin, axis_pin, kind_pin)

    def apply_function(self, a, axis, kind, **kwargs) -> Any:
        return np.argsort(a, axis=axis, kind=kind)


class SortNode(NumpyFunctionNode):
    """Return a sorted copy of an array."""

    def __init__(self):
        array_pin = DataInputPin(
            name=PinName("a"),
            dtype=Dtype.any(),
            docs="Array to be sorted",
        )
        axis_pin = DataInputPin(
            name=PinName("axis"),
            dtype=Dtype.any(),
            docs="Axis along which to sort",
            default=-1,
        )
        kind_pin = DataInputPin(
            name=PinName("kind"),
            dtype=Dtype.any(),
            docs="Sorting algorithm",
            default=None,
        )
        super().__init__("sort", array_pin, axis_pin, kind_pin)

    def apply_function(self, a, axis, kind, **kwargs) -> Any:
        return np.sort(a, axis=axis, kind=kind)


class HistogramNode(NumpyFunctionNode):
    """Compute the histogram of a dataset."""

    def __init__(self):
        array_pin = DataInputPin(
            name=PinName("a"),
            dtype=Dtype.any(),
            docs="Input data",
        )
        bins_pin = DataInputPin(
            name=PinName("bins"),
            dtype=Dtype.any(),
            docs="Number of equal-width bins or bin edges",
            default=10,
        )
        range_pin = DataInputPin(
            name=PinName("range"),
            dtype=Dtype.any(),
            docs="Lower and upper range of the bins",
            default=None,
        )
        density_pin = DataInputPin(
            name=PinName("density"),
            dtype=Dtype.any(),
            docs="If True, draw a density instead of a frequency histogram",
            default=False,
        )
        super().__init__("histogram", array_pin, bins_pin, range_pin, density_pin)

    def apply_function(self, a, bins, range, density, **kwargs) -> Any:
        return np.histogram(a, bins=bins, range=range, density=density)


class BincountNode(NumpyFunctionNode):
    """Count number of occurrences of each value in array of non-negative ints."""

    def __init__(self):
        array_pin = DataInputPin(
            name=PinName("x"),
            dtype=Dtype.any(),
            docs="Input array",
        )
        weights_pin = DataInputPin(
            name=PinName("weights"),
            dtype=Dtype.any(),
            docs="Weights, array of the same shape as x",
            default=None,
        )
        minlength_pin = DataInputPin(
            name=PinName("minlength"),
            dtype=Dtype.any(),
            docs="Minimum number of bins for the output array",
            default=0,
        )
        super().__init__("bincount", array_pin, weights_pin, minlength_pin)

    def apply_function(self, x, weights, minlength, **kwargs) -> Any:
        return np.bincount(x, weights=weights, minlength=minlength)


class CorrcoefNode(NumpyFunctionNode):
    """Return Pearson product-moment correlation coefficients."""

    def __init__(self):
        array_pin = DataInputPin(
            name=PinName("x"),
            dtype=Dtype.any(),
            docs="A 1-D or 2-D array containing multiple variables and observations",
        )
        y_pin = DataInputPin(
            name=PinName("y"),
            dtype=Dtype.any(),
            docs="An additional set of variables and observations",
            default=None,
        )
        rowvar_pin = DataInputPin(
            name=PinName("rowvar"),
            dtype=Dtype.any(),
            docs="If True, then each row represents a variable",
            default=True,
        )
        super().__init__("corrcoef", array_pin, y_pin, rowvar_pin)

    def apply_function(self, x, y, rowvar, **kwargs) -> Any:
        return np.corrcoef(x, y=y, rowvar=rowvar)


class CovNode(NumpyFunctionNode):
    """Estimate a covariance matrix, given data and weights."""

    def __init__(self):
        array_pin = DataInputPin(
            name=PinName("m"),
            dtype=Dtype.any(),
            docs="A 1-D or 2-D array containing multiple variables and observations",
        )
        y_pin = DataInputPin(
            name=PinName("y"),
            dtype=Dtype.any(),
            docs="An additional set of variables and observations",
            default=None,
        )
        rowvar_pin = DataInputPin(
            name=PinName("rowvar"),
            dtype=Dtype.any(),
            docs="If True, then each row represents a variable",
            default=True,
        )
        bias_pin = DataInputPin(
            name=PinName("bias"),
            dtype=Dtype.any(),
            docs="Default normalization (False) is by (N-1)",
            default=False,
        )
        ddof_pin = DataInputPin(
            name=PinName("ddof"),
            dtype=Dtype.any(),
            docs="Delta degrees of freedom",
            default=None,
        )
        super().__init__("cov", array_pin, y_pin, rowvar_pin, bias_pin, ddof_pin)

    def apply_function(self, m, y, rowvar, bias, ddof, **kwargs) -> Any:
        return np.cov(m, y=y, rowvar=rowvar, bias=bias, ddof=ddof)


def get_statistics_nodes() -> List[Node]:
    """Get all statistics nodes."""
    return [
        # Central tendency
        MeanNode(),
        MedianNode(),

        # Dispersion
        StdNode(),
        VarNode(),
        PtpNode(),

        # Extremes
        MinNode(),
        MaxNode(),
        ArgminNode(),
        ArgmaxNode(),

        # Quantiles
        PercentileNode(),
        QuantileNode(),

        # Cumulative operations
        SumNode(),
        ProdNode(),
        CumsumNode(),
        CumprodNode(),

        # Sorting
        ArgsortNode(),
        SortNode(),

        # Histograms
        HistogramNode(),
        BincountNode(),

        # Correlation
        CorrcoefNode(),
        CovNode(),
    ]