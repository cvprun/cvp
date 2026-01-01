# -*- coding: utf-8 -*-

from unittest import TestCase

import numpy as np

from cvp.nodes.defaults.numpy.mathematical.absolute_node import AbsoluteNode
from cvp.nodes.defaults.numpy.mathematical.add_node import AddNode
from cvp.nodes.defaults.numpy.mathematical.arccos_node import ArccosNode
from cvp.nodes.defaults.numpy.mathematical.arccosh_node import ArccoshNode
from cvp.nodes.defaults.numpy.mathematical.arcsin_node import ArcsinNode
from cvp.nodes.defaults.numpy.mathematical.arcsinh_node import ArcsinhNode
from cvp.nodes.defaults.numpy.mathematical.arctan2_node import Arctan2Node
from cvp.nodes.defaults.numpy.mathematical.arctan_node import ArctanNode
from cvp.nodes.defaults.numpy.mathematical.arctanh_node import ArctanhNode
from cvp.nodes.defaults.numpy.mathematical.ceil_node import CeilNode
from cvp.nodes.defaults.numpy.mathematical.cos_node import CosNode
from cvp.nodes.defaults.numpy.mathematical.cosh_node import CoshNode
from cvp.nodes.defaults.numpy.mathematical.divide_node import DivideNode
from cvp.nodes.defaults.numpy.mathematical.exp2_node import Exp2Node
from cvp.nodes.defaults.numpy.mathematical.exp_node import ExpNode
from cvp.nodes.defaults.numpy.mathematical.expm1_node import Expm1Node
from cvp.nodes.defaults.numpy.mathematical.fabs_node import FabsNode
from cvp.nodes.defaults.numpy.mathematical.floor_divide_node import FloorDivideNode
from cvp.nodes.defaults.numpy.mathematical.floor_node import FloorNode
from cvp.nodes.defaults.numpy.mathematical.fmax_node import FmaxNode
from cvp.nodes.defaults.numpy.mathematical.fmin_node import FminNode
from cvp.nodes.defaults.numpy.mathematical.log10_node import Log10Node
from cvp.nodes.defaults.numpy.mathematical.log1p_node import Log1pNode
from cvp.nodes.defaults.numpy.mathematical.log2_node import Log2Node
from cvp.nodes.defaults.numpy.mathematical.log_node import LogNode
from cvp.nodes.defaults.numpy.mathematical.maximum_node import MaximumNode
from cvp.nodes.defaults.numpy.mathematical.minimum_node import MinimumNode
from cvp.nodes.defaults.numpy.mathematical.mod_node import ModNode
from cvp.nodes.defaults.numpy.mathematical.multiply_node import MultiplyNode
from cvp.nodes.defaults.numpy.mathematical.negative_node import NegativeNode
from cvp.nodes.defaults.numpy.mathematical.positive_node import PositiveNode
from cvp.nodes.defaults.numpy.mathematical.power_node import PowerNode
from cvp.nodes.defaults.numpy.mathematical.reciprocal_node import ReciprocalNode
from cvp.nodes.defaults.numpy.mathematical.remainder_node import RemainderNode
from cvp.nodes.defaults.numpy.mathematical.round_node import RoundNode
from cvp.nodes.defaults.numpy.mathematical.sign_node import SignNode
from cvp.nodes.defaults.numpy.mathematical.sin_node import SinNode
from cvp.nodes.defaults.numpy.mathematical.sinh_node import SinhNode
from cvp.nodes.defaults.numpy.mathematical.sqrt_node import SqrtNode
from cvp.nodes.defaults.numpy.mathematical.square_node import SquareNode
from cvp.nodes.defaults.numpy.mathematical.subtract_node import SubtractNode
from cvp.nodes.defaults.numpy.mathematical.tan_node import TanNode
from cvp.nodes.defaults.numpy.mathematical.tanh_node import TanhNode
from cvp.nodes.defaults.numpy.mathematical.true_divide_node import TrueDivideNode
from cvp.nodes.defaults.numpy.mathematical.trunc_node import TruncNode
from cvp.nodes.record import NodeRecord


class TestMathematicalNodes(TestCase):

    def setUp(self):
        self.record = NodeRecord.empty()

    def test_trigonometric_functions(self):
        """Test trigonometric function nodes."""
        # Test sin
        sin_node = SinNode()
        self.record.set(sin_node._input_pins[0], np.pi / 2)
        sin_node.run(self.record)
        result = self.record.get(sin_node._output)
        np.testing.assert_almost_equal(result, 1.0, decimal=5)

        # Test cos
        self.record = NodeRecord.empty()
        cos_node = CosNode()
        self.record.set(cos_node._input_pins[0], 0)
        cos_node.run(self.record)
        result = self.record.get(cos_node._output)
        np.testing.assert_almost_equal(result, 1.0, decimal=5)

        # Test tan
        self.record = NodeRecord.empty()
        tan_node = TanNode()
        self.record.set(tan_node._input_pins[0], np.pi / 4)
        tan_node.run(self.record)
        result = self.record.get(tan_node._output)
        np.testing.assert_almost_equal(result, 1.0, decimal=5)

    def test_inverse_trigonometric_functions(self):
        """Test inverse trigonometric function nodes."""
        # Test arcsin
        arcsin_node = ArcsinNode()
        self.record.set(arcsin_node._input_pins[0], 1.0)
        arcsin_node.run(self.record)
        result = self.record.get(arcsin_node._output)
        np.testing.assert_almost_equal(result, np.pi / 2, decimal=5)

        # Test arccos
        self.record = NodeRecord.empty()
        arccos_node = ArccosNode()
        self.record.set(arccos_node._input_pins[0], 1.0)
        arccos_node.run(self.record)
        result = self.record.get(arccos_node._output)
        np.testing.assert_almost_equal(result, 0.0, decimal=5)

        # Test arctan
        self.record = NodeRecord.empty()
        arctan_node = ArctanNode()
        self.record.set(arctan_node._input_pins[0], 1.0)
        arctan_node.run(self.record)
        result = self.record.get(arctan_node._output)
        np.testing.assert_almost_equal(result, np.pi / 4, decimal=5)

    def test_hyperbolic_functions(self):
        """Test hyperbolic function nodes."""
        # Test sinh
        sinh_node = SinhNode()
        self.record.set(sinh_node._input_pins[0], 0)
        sinh_node.run(self.record)
        result = self.record.get(sinh_node._output)
        np.testing.assert_almost_equal(result, 0.0, decimal=5)

        # Test cosh
        self.record = NodeRecord.empty()
        cosh_node = CoshNode()
        self.record.set(cosh_node._input_pins[0], 0)
        cosh_node.run(self.record)
        result = self.record.get(cosh_node._output)
        np.testing.assert_almost_equal(result, 1.0, decimal=5)

        # Test tanh
        self.record = NodeRecord.empty()
        tanh_node = TanhNode()
        self.record.set(tanh_node._input_pins[0], 0)
        tanh_node.run(self.record)
        result = self.record.get(tanh_node._output)
        np.testing.assert_almost_equal(result, 0.0, decimal=5)

    def test_arithmetic_operations(self):
        """Test arithmetic operation nodes."""
        # Test add
        add_node = AddNode()
        self.record.set(add_node._input_pins[0], np.array([1, 2, 3]))
        self.record.set(add_node._input_pins[1], np.array([4, 5, 6]))
        add_node.run(self.record)
        result = self.record.get(add_node._output)
        expected = np.array([5, 7, 9])
        np.testing.assert_array_equal(result, expected)

        # Test subtract
        self.record = NodeRecord.empty()
        subtract_node = SubtractNode()
        self.record.set(subtract_node._input_pins[0], np.array([5, 7, 9]))
        self.record.set(subtract_node._input_pins[1], np.array([1, 2, 3]))
        subtract_node.run(self.record)
        result = self.record.get(subtract_node._output)
        expected = np.array([4, 5, 6])
        np.testing.assert_array_equal(result, expected)

        # Test multiply
        self.record = NodeRecord.empty()
        multiply_node = MultiplyNode()
        self.record.set(multiply_node._input_pins[0], np.array([2, 3, 4]))
        self.record.set(multiply_node._input_pins[1], np.array([5, 6, 7]))
        multiply_node.run(self.record)
        result = self.record.get(multiply_node._output)
        expected = np.array([10, 18, 28])
        np.testing.assert_array_equal(result, expected)

        # Test divide
        self.record = NodeRecord.empty()
        divide_node = DivideNode()
        self.record.set(divide_node._input_pins[0], np.array([10, 18, 28]))
        self.record.set(divide_node._input_pins[1], np.array([2, 3, 4]))
        divide_node.run(self.record)
        result = self.record.get(divide_node._output)
        expected = np.array([5, 6, 7])
        np.testing.assert_array_equal(result, expected)

    def test_exponential_logarithmic_functions(self):
        """Test exponential and logarithmic function nodes."""
        # Test exp
        exp_node = ExpNode()
        self.record.set(exp_node._input_pins[0], 1)
        exp_node.run(self.record)
        result = self.record.get(exp_node._output)
        np.testing.assert_almost_equal(result, np.e, decimal=5)

        # Test log
        self.record = NodeRecord.empty()
        log_node = LogNode()
        self.record.set(log_node._input_pins[0], np.e)
        log_node.run(self.record)
        result = self.record.get(log_node._output)
        np.testing.assert_almost_equal(result, 1.0, decimal=5)

        # Test log10
        self.record = NodeRecord.empty()
        log10_node = Log10Node()
        self.record.set(log10_node._input_pins[0], 100)
        log10_node.run(self.record)
        result = self.record.get(log10_node._output)
        np.testing.assert_almost_equal(result, 2.0, decimal=5)

        # Test log2
        self.record = NodeRecord.empty()
        log2_node = Log2Node()
        self.record.set(log2_node._input_pins[0], 8)
        log2_node.run(self.record)
        result = self.record.get(log2_node._output)
        np.testing.assert_almost_equal(result, 3.0, decimal=5)

    def test_power_root_functions(self):
        """Test power and root function nodes."""
        # Test power
        power_node = PowerNode()
        self.record.set(power_node._input_pins[0], 2)
        self.record.set(power_node._input_pins[1], 3)
        power_node.run(self.record)
        result = self.record.get(power_node._output)
        np.testing.assert_almost_equal(result, 8.0, decimal=5)

        # Test sqrt
        self.record = NodeRecord.empty()
        sqrt_node = SqrtNode()
        self.record.set(sqrt_node._input_pins[0], 16)
        sqrt_node.run(self.record)
        result = self.record.get(sqrt_node._output)
        np.testing.assert_almost_equal(result, 4.0, decimal=5)

        # Test square
        self.record = NodeRecord.empty()
        square_node = SquareNode()
        self.record.set(square_node._input_pins[0], 5)
        square_node.run(self.record)
        result = self.record.get(square_node._output)
        np.testing.assert_almost_equal(result, 25.0, decimal=5)

    def test_rounding_functions(self):
        """Test rounding function nodes."""
        test_val = 3.7

        # Test ceil
        ceil_node = CeilNode()
        self.record.set(ceil_node._input_pins[0], test_val)
        ceil_node.run(self.record)
        result = self.record.get(ceil_node._output)
        np.testing.assert_equal(result, 4.0)

        # Test floor
        self.record = NodeRecord.empty()
        floor_node = FloorNode()
        self.record.set(floor_node._input_pins[0], test_val)
        floor_node.run(self.record)
        result = self.record.get(floor_node._output)
        np.testing.assert_equal(result, 3.0)

        # Test round
        self.record = NodeRecord.empty()
        round_node = RoundNode()
        self.record.set(round_node._input_pins[0], test_val)
        round_node.run(self.record)
        result = self.record.get(round_node._output)
        np.testing.assert_equal(result, 4.0)

        # Test trunc
        self.record = NodeRecord.empty()
        trunc_node = TruncNode()
        self.record.set(trunc_node._input_pins[0], test_val)
        trunc_node.run(self.record)
        result = self.record.get(trunc_node._output)
        np.testing.assert_equal(result, 3.0)

    def test_sign_absolute_functions(self):
        """Test sign and absolute value function nodes."""
        # Test sign
        sign_node = SignNode()
        self.record.set(sign_node._input_pins[0], -5)
        sign_node.run(self.record)
        result = self.record.get(sign_node._output)
        np.testing.assert_equal(result, -1)

        # Test absolute
        self.record = NodeRecord.empty()
        abs_node = AbsoluteNode()
        self.record.set(abs_node._input_pins[0], -5)
        abs_node.run(self.record)
        result = self.record.get(abs_node._output)
        np.testing.assert_equal(result, 5)

        # Test fabs
        self.record = NodeRecord.empty()
        fabs_node = FabsNode()
        self.record.set(fabs_node._input_pins[0], -5.5)
        fabs_node.run(self.record)
        result = self.record.get(fabs_node._output)
        np.testing.assert_almost_equal(result, 5.5, decimal=5)

    def test_unary_operations(self):
        """Test unary operation nodes."""
        # Test negative
        negative_node = NegativeNode()
        self.record.set(negative_node._input_pins[0], 5)
        negative_node.run(self.record)
        result = self.record.get(negative_node._output)
        np.testing.assert_equal(result, -5)

        # Test positive
        self.record = NodeRecord.empty()
        positive_node = PositiveNode()
        self.record.set(positive_node._input_pins[0], -5)
        positive_node.run(self.record)
        result = self.record.get(positive_node._output)
        np.testing.assert_equal(result, -5)

        # Test reciprocal
        self.record = NodeRecord.empty()
        reciprocal_node = ReciprocalNode()
        self.record.set(reciprocal_node._input_pins[0], 4)
        reciprocal_node.run(self.record)
        result = self.record.get(reciprocal_node._output)
        np.testing.assert_almost_equal(result, 0.25, decimal=5)

    def test_min_max_functions(self):
        """Test minimum and maximum function nodes."""
        # Test minimum
        minimum_node = MinimumNode()
        self.record.set(minimum_node._input_pins[0], np.array([1, 5, 3]))
        self.record.set(minimum_node._input_pins[1], np.array([4, 2, 6]))
        minimum_node.run(self.record)
        result = self.record.get(minimum_node._output)
        expected = np.array([1, 2, 3])
        np.testing.assert_array_equal(result, expected)

        # Test maximum
        self.record = NodeRecord.empty()
        maximum_node = MaximumNode()
        self.record.set(maximum_node._input_pins[0], np.array([1, 5, 3]))
        self.record.set(maximum_node._input_pins[1], np.array([4, 2, 6]))
        maximum_node.run(self.record)
        result = self.record.get(maximum_node._output)
        expected = np.array([4, 5, 6])
        np.testing.assert_array_equal(result, expected)

        # Test fmin
        self.record = NodeRecord.empty()
        fmin_node = FminNode()
        self.record.set(fmin_node._input_pins[0], np.array([1, np.nan, 3]))
        self.record.set(fmin_node._input_pins[1], np.array([4, 2, np.nan]))
        fmin_node.run(self.record)
        result = self.record.get(fmin_node._output)
        # fmin ignores NaN values
        expected = np.array([1, 2, 3])
        np.testing.assert_array_equal(result, expected)

        # Test fmax
        self.record = NodeRecord.empty()
        fmax_node = FmaxNode()
        self.record.set(fmax_node._input_pins[0], np.array([1, np.nan, 3]))
        self.record.set(fmax_node._input_pins[1], np.array([4, 2, np.nan]))
        fmax_node.run(self.record)
        result = self.record.get(fmax_node._output)
        # fmax ignores NaN values
        expected = np.array([4, 2, 3])
        np.testing.assert_array_equal(result, expected)

    def test_division_modulo_functions(self):
        """Test division and modulo function nodes."""
        # Test true_divide
        true_divide_node = TrueDivideNode()
        self.record.set(true_divide_node._input_pins[0], 7)
        self.record.set(true_divide_node._input_pins[1], 2)
        true_divide_node.run(self.record)
        result = self.record.get(true_divide_node._output)
        np.testing.assert_almost_equal(result, 3.5, decimal=5)

        # Test floor_divide
        self.record = NodeRecord.empty()
        floor_divide_node = FloorDivideNode()
        self.record.set(floor_divide_node._input_pins[0], 7)
        self.record.set(floor_divide_node._input_pins[1], 2)
        floor_divide_node.run(self.record)
        result = self.record.get(floor_divide_node._output)
        np.testing.assert_equal(result, 3)

        # Test mod
        self.record = NodeRecord.empty()
        mod_node = ModNode()
        self.record.set(mod_node._input_pins[0], 7)
        self.record.set(mod_node._input_pins[1], 3)
        mod_node.run(self.record)
        result = self.record.get(mod_node._output)
        np.testing.assert_equal(result, 1)

        # Test remainder
        self.record = NodeRecord.empty()
        remainder_node = RemainderNode()
        self.record.set(remainder_node._input_pins[0], 7)
        self.record.set(remainder_node._input_pins[1], 3)
        remainder_node.run(self.record)
        result = self.record.get(remainder_node._output)
        np.testing.assert_equal(result, 1)

    def test_special_exponential_functions(self):
        """Test special exponential function nodes."""
        # Test exp2
        exp2_node = Exp2Node()
        self.record.set(exp2_node._input_pins[0], 3)
        exp2_node.run(self.record)
        result = self.record.get(exp2_node._output)
        np.testing.assert_almost_equal(result, 8.0, decimal=5)

        # Test expm1 (exp(x) - 1)
        self.record = NodeRecord.empty()
        expm1_node = Expm1Node()
        self.record.set(expm1_node._input_pins[0], 0)
        expm1_node.run(self.record)
        result = self.record.get(expm1_node._output)
        np.testing.assert_almost_equal(result, 0.0, decimal=5)

        # Test log1p (log(1 + x))
        self.record = NodeRecord.empty()
        log1p_node = Log1pNode()
        self.record.set(log1p_node._input_pins[0], 0)
        log1p_node.run(self.record)
        result = self.record.get(log1p_node._output)
        np.testing.assert_almost_equal(result, 0.0, decimal=5)

    def test_inverse_hyperbolic_functions(self):
        """Test inverse hyperbolic function nodes."""
        # Test arcsinh
        arcsinh_node = ArcsinhNode()
        self.record.set(arcsinh_node._input_pins[0], 0)
        arcsinh_node.run(self.record)
        result = self.record.get(arcsinh_node._output)
        np.testing.assert_almost_equal(result, 0.0, decimal=5)

        # Test arccosh
        self.record = NodeRecord.empty()
        arccosh_node = ArccoshNode()
        self.record.set(arccosh_node._input_pins[0], 1)
        arccosh_node.run(self.record)
        result = self.record.get(arccosh_node._output)
        np.testing.assert_almost_equal(result, 0.0, decimal=5)

        # Test arctanh
        self.record = NodeRecord.empty()
        arctanh_node = ArctanhNode()
        self.record.set(arctanh_node._input_pins[0], 0)
        arctanh_node.run(self.record)
        result = self.record.get(arctanh_node._output)
        np.testing.assert_almost_equal(result, 0.0, decimal=5)

    def test_two_argument_functions(self):
        """Test two-argument function nodes."""
        # Test arctan2
        arctan2_node = Arctan2Node()
        self.record.set(arctan2_node._input_pins[0], 1)  # y
        self.record.set(arctan2_node._input_pins[1], 1)  # x
        arctan2_node.run(self.record)
        result = self.record.get(arctan2_node._output)
        np.testing.assert_almost_equal(result, np.pi / 4, decimal=5)