# -*- coding: utf-8 -*-

from typing import Any, List

import numpy as np

from cvp.dtypes.dtype import Dtype
from cvp.nodes.defaults.numpy._base import NumpyFunctionNode, NumpyUnaryNode, NumpyBinaryNode
from cvp.nodes.node import Node
from cvp.nodes.record import NodeRecord
from cvp.pins.datas import DataInputPin
from cvp.pins.pin import Pin, PinName
from cvp.types.override import override


class DotNode(NumpyBinaryNode):
    """Dot product of two arrays."""
    def __init__(self):
        super().__init__("dot", "a", "First input array", "b", "Second input array")


class MatmulNode(NumpyBinaryNode):
    """Matrix product of two arrays."""
    def __init__(self):
        super().__init__("matmul", "x1", "First input array", "x2", "Second input array")


class InnerNode(NumpyBinaryNode):
    """Inner product of two arrays."""
    def __init__(self):
        super().__init__("inner", "a", "First input array", "b", "Second input array")


class OuterNode(NumpyBinaryNode):
    """Compute the outer product of two vectors."""
    def __init__(self):
        super().__init__("outer", "a", "First input vector", "b", "Second input vector")


class VdotNode(NumpyBinaryNode):
    """Return the dot product of two vectors."""
    def __init__(self):
        super().__init__("vdot", "a", "First input array", "b", "Second input array")


class TensordotNode(NumpyFunctionNode):
    """Compute tensor dot product along specified axes."""

    def __init__(self):
        a_pin = DataInputPin(
            name=PinName("a"),
            dtype=Dtype.any(),
            docs="First input array",
        )
        b_pin = DataInputPin(
            name=PinName("b"),
            dtype=Dtype.any(),
            docs="Second input array",
        )
        axes_pin = DataInputPin(
            name=PinName("axes"),
            dtype=Dtype.any(),
            docs="Axes to be summed over",
            default=2,
        )
        super().__init__("tensordot", a_pin, b_pin, axes_pin)

    def apply_function(self, a, b, axes, **kwargs) -> Any:
        return np.tensordot(a, b, axes=axes)


class EinsumNode(NumpyFunctionNode):
    """Evaluates the Einstein summation convention on the operands."""

    def __init__(self):
        subscripts_pin = DataInputPin(
            name=PinName("subscripts"),
            dtype=Dtype.any(),
            docs="Specifies the subscripts for summation",
        )
        operands_pin = DataInputPin(
            name=PinName("operands"),
            dtype=Dtype.any(),
            docs="Arrays for the operation",
        )
        super().__init__("einsum", subscripts_pin, operands_pin)

    def apply_function(self, subscripts, operands, **kwargs) -> Any:
        if isinstance(operands, (list, tuple)):
            return np.einsum(subscripts, *operands)
        else:
            return np.einsum(subscripts, operands)


# Linear algebra functions from np.linalg
class LinalgDetNode(NumpyFunctionNode):
    """Compute the determinant of an array."""

    def __init__(self):
        array_pin = DataInputPin(
            name=PinName("a"),
            dtype=Dtype.any(),
            docs="Input array",
        )
        super().__init__("det", array_pin)

    def apply_function(self, a, **kwargs) -> Any:
        return np.linalg.det(a)


class LinalgInvNode(NumpyFunctionNode):
    """Compute the (multiplicative) inverse of a matrix."""

    def __init__(self):
        array_pin = DataInputPin(
            name=PinName("a"),
            dtype=Dtype.any(),
            docs="Matrix to be inverted",
        )
        super().__init__("inv", array_pin)

    def apply_function(self, a, **kwargs) -> Any:
        return np.linalg.inv(a)


class LinalgPinvNode(NumpyFunctionNode):
    """Compute the (Moore-Penrose) pseudo-inverse of a matrix."""

    def __init__(self):
        array_pin = DataInputPin(
            name=PinName("a"),
            dtype=Dtype.any(),
            docs="Matrix to be pseudo-inverted",
        )
        rcond_pin = DataInputPin(
            name=PinName("rcond"),
            dtype=Dtype.any(),
            docs="Cutoff for small singular values",
            default=1e-15,
        )
        super().__init__("pinv", array_pin, rcond_pin)

    def apply_function(self, a, rcond, **kwargs) -> Any:
        return np.linalg.pinv(a, rcond=rcond)


class LinalgEigNode(NumpyFunctionNode):
    """Compute the eigenvalues and right eigenvectors of a square array."""

    def __init__(self):
        array_pin = DataInputPin(
            name=PinName("a"),
            dtype=Dtype.any(),
            docs="Square matrix to compute eigenvalues/vectors",
        )
        super().__init__("eig", array_pin)

    def apply_function(self, a, **kwargs) -> Any:
        return np.linalg.eig(a)


class LinalgEigvalsNode(NumpyFunctionNode):
    """Compute the eigenvalues of a general matrix."""

    def __init__(self):
        array_pin = DataInputPin(
            name=PinName("a"),
            dtype=Dtype.any(),
            docs="Square matrix to compute eigenvalues",
        )
        super().__init__("eigvals", array_pin)

    def apply_function(self, a, **kwargs) -> Any:
        return np.linalg.eigvals(a)


class LinalgEighNode(NumpyFunctionNode):
    """Return eigenvalues and eigenvectors of a complex Hermitian matrix."""

    def __init__(self):
        array_pin = DataInputPin(
            name=PinName("a"),
            dtype=Dtype.any(),
            docs="Complex Hermitian matrix",
        )
        uplo_pin = DataInputPin(
            name=PinName("UPLO"),
            dtype=Dtype.any(),
            docs="Whether to use lower ('L') or upper ('U') triangular part",
            default='L',
        )
        super().__init__("eigh", array_pin, uplo_pin)

    def apply_function(self, a, uplo, **kwargs) -> Any:
        return np.linalg.eigh(a, UPLO=uplo)


class LinalgEighvalsNode(NumpyFunctionNode):
    """Return eigenvalues of a complex Hermitian matrix."""

    def __init__(self):
        array_pin = DataInputPin(
            name=PinName("a"),
            dtype=Dtype.any(),
            docs="Complex Hermitian matrix",
        )
        uplo_pin = DataInputPin(
            name=PinName("UPLO"),
            dtype=Dtype.any(),
            docs="Whether to use lower ('L') or upper ('U') triangular part",
            default='L',
        )
        super().__init__("eigvalsh", array_pin, uplo_pin)

    def apply_function(self, a, uplo, **kwargs) -> Any:
        return np.linalg.eigvalsh(a, UPLO=uplo)


class LinalgSvdNode(NumpyFunctionNode):
    """Singular Value Decomposition."""

    def __init__(self):
        array_pin = DataInputPin(
            name=PinName("a"),
            dtype=Dtype.any(),
            docs="Array to decompose",
        )
        full_matrices_pin = DataInputPin(
            name=PinName("full_matrices"),
            dtype=Dtype.any(),
            docs="If True, U and Vh are of shape (M, M) and (N, N)",
            default=True,
        )
        compute_uv_pin = DataInputPin(
            name=PinName("compute_uv"),
            dtype=Dtype.any(),
            docs="Whether to compute U and Vh in addition to s",
            default=True,
        )
        super().__init__("svd", array_pin, full_matrices_pin, compute_uv_pin)

    def apply_function(self, a, full_matrices, compute_uv, **kwargs) -> Any:
        return np.linalg.svd(a, full_matrices=full_matrices, compute_uv=compute_uv)


class LinalgQrNode(NumpyFunctionNode):
    """Compute the qr factorization of a matrix."""

    def __init__(self):
        array_pin = DataInputPin(
            name=PinName("a"),
            dtype=Dtype.any(),
            docs="Matrix to be factored",
        )
        mode_pin = DataInputPin(
            name=PinName("mode"),
            dtype=Dtype.any(),
            docs="Decomposition mode ('reduced', 'complete', 'r', 'raw')",
            default='reduced',
        )
        super().__init__("qr", array_pin, mode_pin)

    def apply_function(self, a, mode, **kwargs) -> Any:
        return np.linalg.qr(a, mode=mode)


class LinalgCholeskyNode(NumpyFunctionNode):
    """Compute the Cholesky decomposition of a matrix."""

    def __init__(self):
        array_pin = DataInputPin(
            name=PinName("a"),
            dtype=Dtype.any(),
            docs="Hermitian positive-definite matrix",
        )
        super().__init__("cholesky", array_pin)

    def apply_function(self, a, **kwargs) -> Any:
        return np.linalg.cholesky(a)


class LinalgNormNode(NumpyFunctionNode):
    """Matrix or vector norm."""

    def __init__(self):
        array_pin = DataInputPin(
            name=PinName("x"),
            dtype=Dtype.any(),
            docs="Input array",
        )
        ord_pin = DataInputPin(
            name=PinName("ord"),
            dtype=Dtype.any(),
            docs="Order of the norm",
            default=None,
        )
        axis_pin = DataInputPin(
            name=PinName("axis"),
            dtype=Dtype.any(),
            docs="Axis along which to compute the norm",
            default=None,
        )
        keepdims_pin = DataInputPin(
            name=PinName("keepdims"),
            dtype=Dtype.any(),
            docs="Keep dimensions",
            default=False,
        )
        super().__init__("norm", array_pin, ord_pin, axis_pin, keepdims_pin)

    def apply_function(self, x, ord, axis, keepdims, **kwargs) -> Any:
        return np.linalg.norm(x, ord=ord, axis=axis, keepdims=keepdims)


class LinalgCondNode(NumpyFunctionNode):
    """Compute the condition number of a matrix."""

    def __init__(self):
        array_pin = DataInputPin(
            name=PinName("x"),
            dtype=Dtype.any(),
            docs="Matrix whose condition number is sought",
        )
        p_pin = DataInputPin(
            name=PinName("p"),
            dtype=Dtype.any(),
            docs="Order of the norm used in the condition number computation",
            default=None,
        )
        super().__init__("cond", array_pin, p_pin)

    def apply_function(self, x, p, **kwargs) -> Any:
        return np.linalg.cond(x, p=p)


class LinalgMatrixRankNode(NumpyFunctionNode):
    """Return matrix rank using SVD method."""

    def __init__(self):
        array_pin = DataInputPin(
            name=PinName("M"),
            dtype=Dtype.any(),
            docs="Input matrix",
        )
        tol_pin = DataInputPin(
            name=PinName("tol"),
            dtype=Dtype.any(),
            docs="Threshold below which SVD values are considered zero",
            default=None,
        )
        super().__init__("matrix_rank", array_pin, tol_pin)

    def apply_function(self, M, tol, **kwargs) -> Any:
        return np.linalg.matrix_rank(M, tol=tol)


class LinalgSlogdetNode(NumpyFunctionNode):
    """Compute the sign and (natural) logarithm of the determinant."""

    def __init__(self):
        array_pin = DataInputPin(
            name=PinName("a"),
            dtype=Dtype.any(),
            docs="Input array",
        )
        super().__init__("slogdet", array_pin)

    def apply_function(self, a, **kwargs) -> Any:
        return np.linalg.slogdet(a)


class LinalgSolveNode(NumpyFunctionNode):
    """Solve a linear matrix equation, or system of linear scalar equations."""

    def __init__(self):
        a_pin = DataInputPin(
            name=PinName("a"),
            dtype=Dtype.any(),
            docs="Coefficient matrix",
        )
        b_pin = DataInputPin(
            name=PinName("b"),
            dtype=Dtype.any(),
            docs="Ordinate or dependent variable values",
        )
        super().__init__("solve", a_pin, b_pin)

    def apply_function(self, a, b, **kwargs) -> Any:
        return np.linalg.solve(a, b)


class LinalgLstsqNode(NumpyFunctionNode):
    """Return the least-squares solution to a linear matrix equation."""

    def __init__(self):
        a_pin = DataInputPin(
            name=PinName("a"),
            dtype=Dtype.any(),
            docs="Coefficient matrix",
        )
        b_pin = DataInputPin(
            name=PinName("b"),
            dtype=Dtype.any(),
            docs="Ordinate or dependent variable values",
        )
        rcond_pin = DataInputPin(
            name=PinName("rcond"),
            dtype=Dtype.any(),
            docs="Cut-off ratio for small singular values",
            default=None,
        )
        super().__init__("lstsq", a_pin, b_pin, rcond_pin)

    def apply_function(self, a, b, rcond, **kwargs) -> Any:
        return np.linalg.lstsq(a, b, rcond=rcond)


def get_linalg_nodes() -> List[Node]:
    """Get all linear algebra nodes."""
    return [
        # Basic operations
        DotNode(),
        MatmulNode(),
        InnerNode(),
        OuterNode(),
        VdotNode(),
        TensordotNode(),
        EinsumNode(),

        # Matrix operations
        LinalgDetNode(),
        LinalgInvNode(),
        LinalgPinvNode(),
        LinalgEigNode(),
        LinalgEigvalsNode(),
        LinalgEighNode(),
        LinalgEighvalsNode(),
        LinalgSvdNode(),
        LinalgQrNode(),
        LinalgCholeskyNode(),
        LinalgNormNode(),
        LinalgCondNode(),
        LinalgMatrixRankNode(),
        LinalgSlogdetNode(),
        LinalgSolveNode(),
        LinalgLstsqNode(),
    ]