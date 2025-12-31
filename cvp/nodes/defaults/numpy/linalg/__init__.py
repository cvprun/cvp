# -*- coding: utf-8 -*-

from typing import List

from cvp.nodes.node import Node

from .dot_node import DotNode
from .einsum_node import EinsumNode
from .inner_node import InnerNode
from .linalg_cholesky_node import LinalgCholeskyNode
from .linalg_cond_node import LinalgCondNode
from .linalg_det_node import LinalgDetNode
from .linalg_eig_node import LinalgEigNode
from .linalg_eigh_node import LinalgEighNode
from .linalg_eighvals_node import LinalgEighvalsNode
from .linalg_eigvals_node import LinalgEigvalsNode
from .linalg_inv_node import LinalgInvNode
from .linalg_lstsq_node import LinalgLstsqNode
from .linalg_matrix_rank_node import LinalgMatrixRankNode
from .linalg_norm_node import LinalgNormNode
from .linalg_pinv_node import LinalgPinvNode
from .linalg_qr_node import LinalgQrNode
from .linalg_slogdet_node import LinalgSlogdetNode
from .linalg_solve_node import LinalgSolveNode
from .linalg_svd_node import LinalgSvdNode
from .matmul_node import MatmulNode
from .outer_node import OuterNode
from .tensordot_node import TensordotNode
from .vdot_node import VdotNode


def get_linalg_nodes() -> List[Node]:
    """Get all linalg nodes."""
    return [
        DotNode(),
        MatmulNode(),
        InnerNode(),
        OuterNode(),
        VdotNode(),
        TensordotNode(),
        EinsumNode(),
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
