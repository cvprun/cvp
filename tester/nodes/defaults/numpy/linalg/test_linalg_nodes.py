# -*- coding: utf-8 -*-

from unittest import TestCase

import numpy as np

from cvp.nodes.defaults.numpy.linalg.dot_node import DotNode
from cvp.nodes.defaults.numpy.linalg.einsum_node import EinsumNode
from cvp.nodes.defaults.numpy.linalg.inner_node import InnerNode
from cvp.nodes.defaults.numpy.linalg.linalg_cholesky_node import LinalgCholeskyNode
from cvp.nodes.defaults.numpy.linalg.linalg_cond_node import LinalgCondNode
from cvp.nodes.defaults.numpy.linalg.linalg_det_node import LinalgDetNode
from cvp.nodes.defaults.numpy.linalg.linalg_eig_node import LinalgEigNode
from cvp.nodes.defaults.numpy.linalg.linalg_eigh_node import LinalgEighNode
from cvp.nodes.defaults.numpy.linalg.linalg_eigvals_node import LinalgEigvalsNode
from cvp.nodes.defaults.numpy.linalg.linalg_eighvals_node import LinalgEighvalsNode
from cvp.nodes.defaults.numpy.linalg.linalg_inv_node import LinalgInvNode
from cvp.nodes.defaults.numpy.linalg.linalg_lstsq_node import LinalgLstsqNode
from cvp.nodes.defaults.numpy.linalg.linalg_matrix_rank_node import LinalgMatrixRankNode
from cvp.nodes.defaults.numpy.linalg.linalg_norm_node import LinalgNormNode
from cvp.nodes.defaults.numpy.linalg.linalg_pinv_node import LinalgPinvNode
from cvp.nodes.defaults.numpy.linalg.linalg_qr_node import LinalgQrNode
from cvp.nodes.defaults.numpy.linalg.linalg_slogdet_node import LinalgSlogdetNode
from cvp.nodes.defaults.numpy.linalg.linalg_solve_node import LinalgSolveNode
from cvp.nodes.defaults.numpy.linalg.linalg_svd_node import LinalgSvdNode
from cvp.nodes.defaults.numpy.linalg.matmul_node import MatmulNode
from cvp.nodes.defaults.numpy.linalg.outer_node import OuterNode
from cvp.nodes.defaults.numpy.linalg.tensordot_node import TensordotNode
from cvp.nodes.defaults.numpy.linalg.vdot_node import VdotNode
from cvp.nodes.record import NodeRecord


class TestLinalgNodes(TestCase):

    def setUp(self):
        self.record = NodeRecord.empty()
        # Test matrices
        self.test_matrix_2x2 = np.array([[1, 2], [3, 4]])
        self.test_matrix_3x3 = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 10]])
        self.test_vector = np.array([1, 2, 3])
        self.identity_3x3 = np.eye(3)

    def test_basic_operations(self):
        """Test basic linear algebra operations."""
        # Test dot product
        dot_node = DotNode()
        vec1 = np.array([1, 2, 3])
        vec2 = np.array([4, 5, 6])
        self.record.set(dot_node._input_pins[0], vec1)
        self.record.set(dot_node._input_pins[1], vec2)
        dot_node.run(self.record)
        result = self.record.get(dot_node._output)
        expected = np.dot(vec1, vec2)
        np.testing.assert_almost_equal(result, expected)

        # Test matrix multiplication
        self.record = NodeRecord.empty()
        matmul_node = MatmulNode()
        self.record.set(matmul_node._input_pins[0], self.test_matrix_2x2)
        self.record.set(matmul_node._input_pins[1], self.test_matrix_2x2)
        matmul_node.run(self.record)
        result = self.record.get(matmul_node._output)
        expected = np.matmul(self.test_matrix_2x2, self.test_matrix_2x2)
        np.testing.assert_array_almost_equal(result, expected)

    def test_vector_products(self):
        """Test vector product operations."""
        # Test inner product
        inner_node = InnerNode()
        vec1 = np.array([1, 2, 3])
        vec2 = np.array([4, 5, 6])
        self.record.set(inner_node._input_pins[0], vec1)
        self.record.set(inner_node._input_pins[1], vec2)
        inner_node.run(self.record)
        result = self.record.get(inner_node._output)
        expected = np.inner(vec1, vec2)
        np.testing.assert_almost_equal(result, expected)

        # Test outer product
        self.record = NodeRecord.empty()
        outer_node = OuterNode()
        self.record.set(outer_node._input_pins[0], vec1)
        self.record.set(outer_node._input_pins[1], vec2)
        outer_node.run(self.record)
        result = self.record.get(outer_node._output)
        expected = np.outer(vec1, vec2)
        np.testing.assert_array_almost_equal(result, expected)

        # Test vdot
        self.record = NodeRecord.empty()
        vdot_node = VdotNode()
        self.record.set(vdot_node._input_pins[0], vec1)
        self.record.set(vdot_node._input_pins[1], vec2)
        vdot_node.run(self.record)
        result = self.record.get(vdot_node._output)
        expected = np.vdot(vec1, vec2)
        np.testing.assert_almost_equal(result, expected)

    def test_matrix_properties(self):
        """Test matrix property computations."""
        # Test determinant
        det_node = LinalgDetNode()
        self.record.set(det_node._input_pins[0], self.test_matrix_2x2)
        det_node.run(self.record)
        result = self.record.get(det_node._output)
        expected = np.linalg.det(self.test_matrix_2x2)
        np.testing.assert_almost_equal(result, expected, decimal=5)

        # Test matrix rank
        self.record = NodeRecord.empty()
        rank_node = LinalgMatrixRankNode()
        self.record.set(rank_node._input_pins[0], self.test_matrix_3x3)
        rank_node.run(self.record)
        result = self.record.get(rank_node._output)
        expected = np.linalg.matrix_rank(self.test_matrix_3x3)
        np.testing.assert_equal(result, expected)

        # Test condition number
        self.record = NodeRecord.empty()
        cond_node = LinalgCondNode()
        self.record.set(cond_node._input_pins[0], self.test_matrix_3x3)
        cond_node.run(self.record)
        result = self.record.get(cond_node._output)
        expected = np.linalg.cond(self.test_matrix_3x3)
        np.testing.assert_almost_equal(result, expected, decimal=5)

    def test_matrix_norms(self):
        """Test matrix norm computations."""
        norm_node = LinalgNormNode()
        self.record.set(norm_node._input_pins[0], self.test_vector)
        norm_node.run(self.record)
        result = self.record.get(norm_node._output)
        expected = np.linalg.norm(self.test_vector)
        np.testing.assert_almost_equal(result, expected, decimal=5)

        # Test matrix norm
        self.record = NodeRecord.empty()
        self.record.set(norm_node._input_pins[0], self.test_matrix_2x2)
        norm_node.run(self.record)
        result = self.record.get(norm_node._output)
        expected = np.linalg.norm(self.test_matrix_2x2)
        np.testing.assert_almost_equal(result, expected, decimal=5)

    def test_matrix_inverse(self):
        """Test matrix inverse operations."""
        # Create a well-conditioned invertible matrix
        invertible_matrix = np.array([[2, 1], [1, 2]], dtype=float)

        # Test inverse
        inv_node = LinalgInvNode()
        self.record.set(inv_node._input_pins[0], invertible_matrix)
        inv_node.run(self.record)
        result = self.record.get(inv_node._output)
        expected = np.linalg.inv(invertible_matrix)
        np.testing.assert_array_almost_equal(result, expected, decimal=5)

        # Test pseudo-inverse
        self.record = NodeRecord.empty()
        pinv_node = LinalgPinvNode()
        self.record.set(pinv_node._input_pins[0], self.test_matrix_3x3)
        pinv_node.run(self.record)
        result = self.record.get(pinv_node._output)
        expected = np.linalg.pinv(self.test_matrix_3x3)
        np.testing.assert_array_almost_equal(result, expected, decimal=5)

    def test_eigenvalue_decomposition(self):
        """Test eigenvalue and eigenvector computations."""
        # Use symmetric matrix for stable eigenvalue computation
        symmetric_matrix = np.array([[2, 1], [1, 2]], dtype=float)

        # Test eigenvalues and eigenvectors
        eig_node = LinalgEigNode()
        self.record.set(eig_node._input_pins[0], symmetric_matrix)
        eig_node.run(self.record)
        result = self.record.get(eig_node._output)
        expected_vals, expected_vecs = np.linalg.eig(symmetric_matrix)

        # Result should be a tuple (eigenvalues, eigenvectors)
        result_vals, result_vecs = result
        # Sort both results by eigenvalues for comparison
        sort_idx_result = np.argsort(result_vals)
        sort_idx_expected = np.argsort(expected_vals)

        np.testing.assert_array_almost_equal(
            result_vals[sort_idx_result],
            expected_vals[sort_idx_expected],
            decimal=5
        )

        # Test eigenvalues only
        self.record = NodeRecord.empty()
        eigvals_node = LinalgEigvalsNode()
        self.record.set(eigvals_node._input_pins[0], symmetric_matrix)
        eigvals_node.run(self.record)
        result = self.record.get(eigvals_node._output)
        expected = np.linalg.eigvals(symmetric_matrix)
        result_sorted = np.sort(result)
        expected_sorted = np.sort(expected)
        np.testing.assert_array_almost_equal(result_sorted, expected_sorted, decimal=5)

        # Test hermitian eigenvalue decomposition
        self.record = NodeRecord.empty()
        eigh_node = LinalgEighNode()
        self.record.set(eigh_node._input_pins[0], symmetric_matrix)
        eigh_node.run(self.record)
        result = self.record.get(eigh_node._output)
        expected_vals, expected_vecs = np.linalg.eigh(symmetric_matrix)

        result_vals, result_vecs = result
        np.testing.assert_array_almost_equal(result_vals, expected_vals, decimal=5)

        # Test hermitian eigenvalues only
        self.record = NodeRecord.empty()
        eighvals_node = LinalgEighvalsNode()
        self.record.set(eighvals_node._input_pins[0], symmetric_matrix)
        eighvals_node.run(self.record)
        result = self.record.get(eighvals_node._output)
        expected = np.linalg.eighvals(symmetric_matrix)
        np.testing.assert_array_almost_equal(result, expected, decimal=5)

    def test_matrix_decompositions(self):
        """Test matrix decomposition operations."""
        # Test QR decomposition
        qr_node = LinalgQrNode()
        self.record.set(qr_node._input_pins[0], self.test_matrix_3x3)
        qr_node.run(self.record)
        result = self.record.get(qr_node._output)
        expected_q, expected_r = np.linalg.qr(self.test_matrix_3x3)

        result_q, result_r = result
        # Check that Q*R equals original matrix
        reconstructed = np.matmul(result_q, result_r)
        np.testing.assert_array_almost_equal(reconstructed, self.test_matrix_3x3, decimal=5)

        # Test SVD decomposition
        self.record = NodeRecord.empty()
        svd_node = LinalgSvdNode()
        self.record.set(svd_node._input_pins[0], self.test_matrix_3x3)
        svd_node.run(self.record)
        result = self.record.get(svd_node._output)
        expected_u, expected_s, expected_vh = np.linalg.svd(self.test_matrix_3x3)

        result_u, result_s, result_vh = result
        # Check singular values
        np.testing.assert_array_almost_equal(result_s, expected_s, decimal=5)

        # Test Cholesky decomposition with positive definite matrix
        self.record = NodeRecord.empty()
        pos_def_matrix = np.array([[2, 1], [1, 2]], dtype=float)
        chol_node = LinalgCholeskyNode()
        self.record.set(chol_node._input_pins[0], pos_def_matrix)
        chol_node.run(self.record)
        result = self.record.get(chol_node._output)
        expected = np.linalg.cholesky(pos_def_matrix)
        np.testing.assert_array_almost_equal(result, expected, decimal=5)

    def test_linear_systems(self):
        """Test linear system solving."""
        # Test solve
        solve_node = LinalgSolveNode()
        A = np.array([[2, 1], [1, 2]], dtype=float)
        b = np.array([3, 4], dtype=float)
        self.record.set(solve_node._input_pins[0], A)
        self.record.set(solve_node._input_pins[1], b)
        solve_node.run(self.record)
        result = self.record.get(solve_node._output)
        expected = np.linalg.solve(A, b)
        np.testing.assert_array_almost_equal(result, expected, decimal=5)

        # Test least squares
        self.record = NodeRecord.empty()
        lstsq_node = LinalgLstsqNode()
        A_over = np.array([[1, 1], [1, 2], [1, 3]], dtype=float)  # Overdetermined system
        b_over = np.array([6, 8, 10], dtype=float)
        self.record.set(lstsq_node._input_pins[0], A_over)
        self.record.set(lstsq_node._input_pins[1], b_over)
        lstsq_node.run(self.record)
        result = self.record.get(lstsq_node._output)
        expected = np.linalg.lstsq(A_over, b_over, rcond=None)

        # Result should be a tuple (solution, residuals, rank, singular_values)
        result_x = result[0]
        expected_x = expected[0]
        np.testing.assert_array_almost_equal(result_x, expected_x, decimal=5)

    def test_advanced_operations(self):
        """Test advanced linear algebra operations."""
        # Test signed log determinant
        slogdet_node = LinalgSlogdetNode()
        self.record.set(slogdet_node._input_pins[0], self.test_matrix_2x2)
        slogdet_node.run(self.record)
        result = self.record.get(slogdet_node._output)
        expected = np.linalg.slogdet(self.test_matrix_2x2)

        result_sign, result_logdet = result
        expected_sign, expected_logdet = expected
        np.testing.assert_almost_equal(result_sign, expected_sign, decimal=5)
        np.testing.assert_almost_equal(result_logdet, expected_logdet, decimal=5)

    def test_tensor_operations(self):
        """Test tensor operation nodes."""
        # Test tensordot
        tensordot_node = TensordotNode()
        arr1 = np.array([[1, 2], [3, 4]])
        arr2 = np.array([[5, 6], [7, 8]])
        axes = 1  # Sum over last axis of arr1 and first axis of arr2

        self.record.set(tensordot_node._input_pins[0], arr1)
        self.record.set(tensordot_node._input_pins[1], arr2)
        self.record.set(tensordot_node._input_pins[2], axes)
        tensordot_node.run(self.record)
        result = self.record.get(tensordot_node._output)
        expected = np.tensordot(arr1, arr2, axes)
        np.testing.assert_array_almost_equal(result, expected, decimal=5)

    def test_einsum_operations(self):
        """Test Einstein summation operations."""
        einsum_node = EinsumNode()

        # Test matrix multiplication using einsum
        subscripts = "ij,jk->ik"
        arr1 = np.array([[1, 2], [3, 4]])
        arr2 = np.array([[5, 6], [7, 8]])

        self.record.set(einsum_node._input_pins[0], subscripts)
        self.record.set(einsum_node._input_pins[1], [arr1, arr2])
        einsum_node.run(self.record)
        result = self.record.get(einsum_node._output)
        expected = np.einsum(subscripts, arr1, arr2)
        np.testing.assert_array_almost_equal(result, expected, decimal=5)