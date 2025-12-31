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


class FftNode(NumpyFunctionNode):
    """Compute the one-dimensional discrete Fourier Transform."""

    def __init__(self):
        array_pin = DataInputPin(
            name=PinName("a"),
            dtype=Dtype.any(),
            docs="Input array",
        )
        n_pin = DataInputPin(
            name=PinName("n"),
            dtype=Dtype.any(),
            docs="Length of the transformed axis",
            default=None,
        )
        axis_pin = DataInputPin(
            name=PinName("axis"),
            dtype=Dtype.any(),
            docs="Axis over which to compute the FFT",
            default=-1,
        )
        super().__init__("fft", array_pin, n_pin, axis_pin)

    def apply_function(self, a, n, axis, **kwargs) -> Any:
        return np.fft.fft(a, n=n, axis=axis)


class IfftNode(NumpyFunctionNode):
    """Compute the one-dimensional inverse discrete Fourier Transform."""

    def __init__(self):
        array_pin = DataInputPin(
            name=PinName("a"),
            dtype=Dtype.any(),
            docs="Input array",
        )
        n_pin = DataInputPin(
            name=PinName("n"),
            dtype=Dtype.any(),
            docs="Length of the transformed axis",
            default=None,
        )
        axis_pin = DataInputPin(
            name=PinName("axis"),
            dtype=Dtype.any(),
            docs="Axis over which to compute the inverse FFT",
            default=-1,
        )
        super().__init__("ifft", array_pin, n_pin, axis_pin)

    def apply_function(self, a, n, axis, **kwargs) -> Any:
        return np.fft.ifft(a, n=n, axis=axis)


class Fft2Node(NumpyFunctionNode):
    """Compute the 2-dimensional discrete Fourier Transform."""

    def __init__(self):
        array_pin = DataInputPin(
            name=PinName("a"),
            dtype=Dtype.any(),
            docs="Input array",
        )
        s_pin = DataInputPin(
            name=PinName("s"),
            dtype=Dtype.any(),
            docs="Shape (length of each transformed axis)",
            default=None,
        )
        axes_pin = DataInputPin(
            name=PinName("axes"),
            dtype=Dtype.any(),
            docs="Axes over which to compute the FFT",
            default=(-2, -1),
        )
        super().__init__("fft2", array_pin, s_pin, axes_pin)

    def apply_function(self, a, s, axes, **kwargs) -> Any:
        return np.fft.fft2(a, s=s, axes=axes)


class Ifft2Node(NumpyFunctionNode):
    """Compute the 2-dimensional inverse discrete Fourier Transform."""

    def __init__(self):
        array_pin = DataInputPin(
            name=PinName("a"),
            dtype=Dtype.any(),
            docs="Input array",
        )
        s_pin = DataInputPin(
            name=PinName("s"),
            dtype=Dtype.any(),
            docs="Shape (length of each transformed axis)",
            default=None,
        )
        axes_pin = DataInputPin(
            name=PinName("axes"),
            dtype=Dtype.any(),
            docs="Axes over which to compute the inverse FFT",
            default=(-2, -1),
        )
        super().__init__("ifft2", array_pin, s_pin, axes_pin)

    def apply_function(self, a, s, axes, **kwargs) -> Any:
        return np.fft.ifft2(a, s=s, axes=axes)


class FftnNode(NumpyFunctionNode):
    """Compute the N-dimensional discrete Fourier Transform."""

    def __init__(self):
        array_pin = DataInputPin(
            name=PinName("a"),
            dtype=Dtype.any(),
            docs="Input array",
        )
        s_pin = DataInputPin(
            name=PinName("s"),
            dtype=Dtype.any(),
            docs="Shape (length of each transformed axis)",
            default=None,
        )
        axes_pin = DataInputPin(
            name=PinName("axes"),
            dtype=Dtype.any(),
            docs="Axes over which to compute the FFT",
            default=None,
        )
        super().__init__("fftn", array_pin, s_pin, axes_pin)

    def apply_function(self, a, s, axes, **kwargs) -> Any:
        return np.fft.fftn(a, s=s, axes=axes)


class IfftnNode(NumpyFunctionNode):
    """Compute the N-dimensional inverse discrete Fourier Transform."""

    def __init__(self):
        array_pin = DataInputPin(
            name=PinName("a"),
            dtype=Dtype.any(),
            docs="Input array",
        )
        s_pin = DataInputPin(
            name=PinName("s"),
            dtype=Dtype.any(),
            docs="Shape (length of each transformed axis)",
            default=None,
        )
        axes_pin = DataInputPin(
            name=PinName("axes"),
            dtype=Dtype.any(),
            docs="Axes over which to compute the inverse FFT",
            default=None,
        )
        super().__init__("ifftn", array_pin, s_pin, axes_pin)

    def apply_function(self, a, s, axes, **kwargs) -> Any:
        return np.fft.ifftn(a, s=s, axes=axes)


class RfftNode(NumpyFunctionNode):
    """Compute the one-dimensional discrete Fourier Transform for real input."""

    def __init__(self):
        array_pin = DataInputPin(
            name=PinName("a"),
            dtype=Dtype.any(),
            docs="Input array",
        )
        n_pin = DataInputPin(
            name=PinName("n"),
            dtype=Dtype.any(),
            docs="Number of points along transformation axis",
            default=None,
        )
        axis_pin = DataInputPin(
            name=PinName("axis"),
            dtype=Dtype.any(),
            docs="Axis over which to compute the FFT",
            default=-1,
        )
        super().__init__("rfft", array_pin, n_pin, axis_pin)

    def apply_function(self, a, n, axis, **kwargs) -> Any:
        return np.fft.rfft(a, n=n, axis=axis)


class IrfftNode(NumpyFunctionNode):
    """Compute the inverse of the n-point DFT for real input."""

    def __init__(self):
        array_pin = DataInputPin(
            name=PinName("a"),
            dtype=Dtype.any(),
            docs="Input array",
        )
        n_pin = DataInputPin(
            name=PinName("n"),
            dtype=Dtype.any(),
            docs="Length of the transformed axis",
            default=None,
        )
        axis_pin = DataInputPin(
            name=PinName("axis"),
            dtype=Dtype.any(),
            docs="Axis over which to compute the inverse FFT",
            default=-1,
        )
        super().__init__("irfft", array_pin, n_pin, axis_pin)

    def apply_function(self, a, n, axis, **kwargs) -> Any:
        return np.fft.irfft(a, n=n, axis=axis)


class Rfft2Node(NumpyFunctionNode):
    """Compute the 2-dimensional FFT of a real array."""

    def __init__(self):
        array_pin = DataInputPin(
            name=PinName("a"),
            dtype=Dtype.any(),
            docs="Input array",
        )
        s_pin = DataInputPin(
            name=PinName("s"),
            dtype=Dtype.any(),
            docs="Shape of the input",
            default=None,
        )
        axes_pin = DataInputPin(
            name=PinName("axes"),
            dtype=Dtype.any(),
            docs="Axes over which to compute the FFT",
            default=(-2, -1),
        )
        super().__init__("rfft2", array_pin, s_pin, axes_pin)

    def apply_function(self, a, s, axes, **kwargs) -> Any:
        return np.fft.rfft2(a, s=s, axes=axes)


class Irfft2Node(NumpyFunctionNode):
    """Compute the 2-dimensional inverse FFT of a real array."""

    def __init__(self):
        array_pin = DataInputPin(
            name=PinName("a"),
            dtype=Dtype.any(),
            docs="Input array",
        )
        s_pin = DataInputPin(
            name=PinName("s"),
            dtype=Dtype.any(),
            docs="Shape of the input",
            default=None,
        )
        axes_pin = DataInputPin(
            name=PinName("axes"),
            dtype=Dtype.any(),
            docs="Axes over which to compute the inverse FFT",
            default=(-2, -1),
        )
        super().__init__("irfft2", array_pin, s_pin, axes_pin)

    def apply_function(self, a, s, axes, **kwargs) -> Any:
        return np.fft.irfft2(a, s=s, axes=axes)


class RfftnNode(NumpyFunctionNode):
    """Compute the N-dimensional discrete Fourier Transform for real input."""

    def __init__(self):
        array_pin = DataInputPin(
            name=PinName("a"),
            dtype=Dtype.any(),
            docs="Input array",
        )
        s_pin = DataInputPin(
            name=PinName("s"),
            dtype=Dtype.any(),
            docs="Shape of the input",
            default=None,
        )
        axes_pin = DataInputPin(
            name=PinName("axes"),
            dtype=Dtype.any(),
            docs="Axes over which to compute the FFT",
            default=None,
        )
        super().__init__("rfftn", array_pin, s_pin, axes_pin)

    def apply_function(self, a, s, axes, **kwargs) -> Any:
        return np.fft.rfftn(a, s=s, axes=axes)


class IrfftnNode(NumpyFunctionNode):
    """Compute the N-dimensional inverse discrete Fourier Transform for real input."""

    def __init__(self):
        array_pin = DataInputPin(
            name=PinName("a"),
            dtype=Dtype.any(),
            docs="Input array",
        )
        s_pin = DataInputPin(
            name=PinName("s"),
            dtype=Dtype.any(),
            docs="Shape of the input",
            default=None,
        )
        axes_pin = DataInputPin(
            name=PinName("axes"),
            dtype=Dtype.any(),
            docs="Axes over which to compute the inverse FFT",
            default=None,
        )
        super().__init__("irfftn", array_pin, s_pin, axes_pin)

    def apply_function(self, a, s, axes, **kwargs) -> Any:
        return np.fft.irfftn(a, s=s, axes=axes)


class FftfreqNode(NumpyFunctionNode):
    """Return the Discrete Fourier Transform sample frequencies."""

    def __init__(self):
        n_pin = DataInputPin(
            name=PinName("n"),
            dtype=Dtype.any(),
            docs="Window length",
        )
        d_pin = DataInputPin(
            name=PinName("d"),
            dtype=Dtype.any(),
            docs="Sample spacing",
            default=1.0,
        )
        super().__init__("fftfreq", n_pin, d_pin)

    def apply_function(self, n, d, **kwargs) -> Any:
        return np.fft.fftfreq(n, d=d)


class RfftfreqNode(NumpyFunctionNode):
    """Return the Discrete Fourier Transform sample frequencies (for usage with rfft)."""

    def __init__(self):
        n_pin = DataInputPin(
            name=PinName("n"),
            dtype=Dtype.any(),
            docs="Window length",
        )
        d_pin = DataInputPin(
            name=PinName("d"),
            dtype=Dtype.any(),
            docs="Sample spacing",
            default=1.0,
        )
        super().__init__("rfftfreq", n_pin, d_pin)

    def apply_function(self, n, d, **kwargs) -> Any:
        return np.fft.rfftfreq(n, d=d)


class FftshiftNode(NumpyFunctionNode):
    """Shift the zero-frequency component to the center of the spectrum."""

    def __init__(self):
        array_pin = DataInputPin(
            name=PinName("x"),
            dtype=Dtype.any(),
            docs="Input array",
        )
        axes_pin = DataInputPin(
            name=PinName("axes"),
            dtype=Dtype.any(),
            docs="Axes over which to shift",
            default=None,
        )
        super().__init__("fftshift", array_pin, axes_pin)

    def apply_function(self, x, axes, **kwargs) -> Any:
        return np.fft.fftshift(x, axes=axes)


class IfftshiftNode(NumpyFunctionNode):
    """The inverse of fftshift."""

    def __init__(self):
        array_pin = DataInputPin(
            name=PinName("x"),
            dtype=Dtype.any(),
            docs="Input array",
        )
        axes_pin = DataInputPin(
            name=PinName("axes"),
            dtype=Dtype.any(),
            docs="Axes over which to calculate",
            default=None,
        )
        super().__init__("ifftshift", array_pin, axes_pin)

    def apply_function(self, x, axes, **kwargs) -> Any:
        return np.fft.ifftshift(x, axes=axes)


def get_fft_nodes() -> List[Node]:
    """Get all FFT nodes."""
    return [
        # 1D transforms
        FftNode(),
        IfftNode(),
        RfftNode(),
        IrfftNode(),

        # 2D transforms
        Fft2Node(),
        Ifft2Node(),
        Rfft2Node(),
        Irfft2Node(),

        # N-D transforms
        FftnNode(),
        IfftnNode(),
        RfftnNode(),
        IrfftnNode(),

        # Helper functions
        FftfreqNode(),
        RfftfreqNode(),
        FftshiftNode(),
        IfftshiftNode(),
    ]