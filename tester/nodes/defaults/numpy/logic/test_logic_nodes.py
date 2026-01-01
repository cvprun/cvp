# -*- coding: utf-8 -*-

from unittest import TestCase

import numpy as np

from cvp.nodes.defaults.numpy.logic.all_node import AllNode
from cvp.nodes.defaults.numpy.logic.any_node import AnyNode
from cvp.nodes.defaults.numpy.logic.argwhere_node import ArgwhereNode
from cvp.nodes.defaults.numpy.logic.equal_node import EqualNode
from cvp.nodes.defaults.numpy.logic.flatnonzero_node import FlatnonzeroNode
from cvp.nodes.defaults.numpy.logic.greater_equal_node import GreaterEqualNode
from cvp.nodes.defaults.numpy.logic.greater_node import GreaterNode
from cvp.nodes.defaults.numpy.logic.iscomplex_node import IscomplexNode
from cvp.nodes.defaults.numpy.logic.iscomplexobj_node import IscomplexobjNode
from cvp.nodes.defaults.numpy.logic.isfinite_node import IsfiniteNode
from cvp.nodes.defaults.numpy.logic.isinfinite_node import IsinfiniteNode
from cvp.nodes.defaults.numpy.logic.isnan_node import IsnanNode
from cvp.nodes.defaults.numpy.logic.isnat_node import IsnatNode
from cvp.nodes.defaults.numpy.logic.isneginfinite_node import IsneginfiniteNode
from cvp.nodes.defaults.numpy.logic.isposinfinite_node import IsposinfiniteNode
from cvp.nodes.defaults.numpy.logic.isreal_node import IsrealNode
from cvp.nodes.defaults.numpy.logic.isrealobj_node import IsrealobjNode
from cvp.nodes.defaults.numpy.logic.isscalar_node import IsscalarNode
from cvp.nodes.defaults.numpy.logic.less_equal_node import LessEqualNode
from cvp.nodes.defaults.numpy.logic.less_node import LessNode
from cvp.nodes.defaults.numpy.logic.logical_and_node import LogicalAndNode
from cvp.nodes.defaults.numpy.logic.logical_not_node import LogicalNotNode
from cvp.nodes.defaults.numpy.logic.logical_or_node import LogicalOrNode
from cvp.nodes.defaults.numpy.logic.logical_xor_node import LogicalXorNode
from cvp.nodes.defaults.numpy.logic.nonzero_node import NonzeroNode
from cvp.nodes.defaults.numpy.logic.not_equal_node import NotEqualNode
from cvp.nodes.defaults.numpy.logic.select_node import SelectNode
from cvp.nodes.defaults.numpy.logic.where_node import WhereNode
from cvp.nodes.record import NodeRecord


class TestLogicNodes(TestCase):

    def setUp(self):
        self.record = NodeRecord.empty()

    def test_comparison_operations(self):
        """Test comparison operation nodes."""
        arr1 = np.array([1, 2, 3, 4, 5])
        arr2 = np.array([1, 3, 2, 4, 6])

        # Test equal
        equal_node = EqualNode()
        self.record.set(equal_node._input_pins[0], arr1)
        self.record.set(equal_node._input_pins[1], arr2)
        equal_node.run(self.record)
        result = self.record.get(equal_node._output)
        expected = np.equal(arr1, arr2)
        np.testing.assert_array_equal(result, expected)

        # Test not equal
        self.record = NodeRecord.empty()
        not_equal_node = NotEqualNode()
        self.record.set(not_equal_node._input_pins[0], arr1)
        self.record.set(not_equal_node._input_pins[1], arr2)
        not_equal_node.run(self.record)
        result = self.record.get(not_equal_node._output)
        expected = np.not_equal(arr1, arr2)
        np.testing.assert_array_equal(result, expected)

        # Test greater
        self.record = NodeRecord.empty()
        greater_node = GreaterNode()
        self.record.set(greater_node._input_pins[0], arr1)
        self.record.set(greater_node._input_pins[1], arr2)
        greater_node.run(self.record)
        result = self.record.get(greater_node._output)
        expected = np.greater(arr1, arr2)
        np.testing.assert_array_equal(result, expected)

        # Test greater equal
        self.record = NodeRecord.empty()
        greater_equal_node = GreaterEqualNode()
        self.record.set(greater_equal_node._input_pins[0], arr1)
        self.record.set(greater_equal_node._input_pins[1], arr2)
        greater_equal_node.run(self.record)
        result = self.record.get(greater_equal_node._output)
        expected = np.greater_equal(arr1, arr2)
        np.testing.assert_array_equal(result, expected)

        # Test less
        self.record = NodeRecord.empty()
        less_node = LessNode()
        self.record.set(less_node._input_pins[0], arr1)
        self.record.set(less_node._input_pins[1], arr2)
        less_node.run(self.record)
        result = self.record.get(less_node._output)
        expected = np.less(arr1, arr2)
        np.testing.assert_array_equal(result, expected)

        # Test less equal
        self.record = NodeRecord.empty()
        less_equal_node = LessEqualNode()
        self.record.set(less_equal_node._input_pins[0], arr1)
        self.record.set(less_equal_node._input_pins[1], arr2)
        less_equal_node.run(self.record)
        result = self.record.get(less_equal_node._output)
        expected = np.less_equal(arr1, arr2)
        np.testing.assert_array_equal(result, expected)

    def test_logical_operations(self):
        """Test logical operation nodes."""
        arr1 = np.array([True, False, True, False])
        arr2 = np.array([True, True, False, False])

        # Test logical and
        logical_and_node = LogicalAndNode()
        self.record.set(logical_and_node._input_pins[0], arr1)
        self.record.set(logical_and_node._input_pins[1], arr2)
        logical_and_node.run(self.record)
        result = self.record.get(logical_and_node._output)
        expected = np.logical_and(arr1, arr2)
        np.testing.assert_array_equal(result, expected)

        # Test logical or
        self.record = NodeRecord.empty()
        logical_or_node = LogicalOrNode()
        self.record.set(logical_or_node._input_pins[0], arr1)
        self.record.set(logical_or_node._input_pins[1], arr2)
        logical_or_node.run(self.record)
        result = self.record.get(logical_or_node._output)
        expected = np.logical_or(arr1, arr2)
        np.testing.assert_array_equal(result, expected)

        # Test logical xor
        self.record = NodeRecord.empty()
        logical_xor_node = LogicalXorNode()
        self.record.set(logical_xor_node._input_pins[0], arr1)
        self.record.set(logical_xor_node._input_pins[1], arr2)
        logical_xor_node.run(self.record)
        result = self.record.get(logical_xor_node._output)
        expected = np.logical_xor(arr1, arr2)
        np.testing.assert_array_equal(result, expected)

        # Test logical not
        self.record = NodeRecord.empty()
        logical_not_node = LogicalNotNode()
        self.record.set(logical_not_node._input_pins[0], arr1)
        logical_not_node.run(self.record)
        result = self.record.get(logical_not_node._output)
        expected = np.logical_not(arr1)
        np.testing.assert_array_equal(result, expected)

    def test_truth_value_testing(self):
        """Test truth value testing nodes."""
        test_array = np.array([0, 1, 2, 0, 3])

        # Test all
        all_node = AllNode()
        self.record.set(all_node._input_pins[0], test_array)
        all_node.run(self.record)
        result = self.record.get(all_node._output)
        expected = np.all(test_array)
        np.testing.assert_equal(result, expected)

        # Test any
        self.record = NodeRecord.empty()
        any_node = AnyNode()
        self.record.set(any_node._input_pins[0], test_array)
        any_node.run(self.record)
        result = self.record.get(any_node._output)
        expected = np.any(test_array)
        np.testing.assert_equal(result, expected)

        # Test all with all zeros (should be False)
        self.record = NodeRecord.empty()
        zeros_array = np.array([0, 0, 0])
        self.record.set(all_node._input_pins[0], zeros_array)
        all_node.run(self.record)
        result = self.record.get(all_node._output)
        self.assertFalse(result)

        # Test any with all zeros (should be False)
        self.record = NodeRecord.empty()
        self.record.set(any_node._input_pins[0], zeros_array)
        any_node.run(self.record)
        result = self.record.get(any_node._output)
        self.assertFalse(result)

    def test_array_contents_testing(self):
        """Test array contents testing nodes."""
        # Test isfinite
        test_array = np.array([1, 2, np.inf, -np.inf, np.nan])
        isfinite_node = IsfiniteNode()
        self.record.set(isfinite_node._input_pins[0], test_array)
        isfinite_node.run(self.record)
        result = self.record.get(isfinite_node._output)
        expected = np.isfinite(test_array)
        np.testing.assert_array_equal(result, expected)

        # Test isinfinite
        self.record = NodeRecord.empty()
        isinfinite_node = IsinfiniteNode()
        self.record.set(isinfinite_node._input_pins[0], test_array)
        isinfinite_node.run(self.record)
        result = self.record.get(isinfinite_node._output)
        expected = np.isinf(test_array)
        np.testing.assert_array_equal(result, expected)

        # Test isnan
        self.record = NodeRecord.empty()
        isnan_node = IsnanNode()
        self.record.set(isnan_node._input_pins[0], test_array)
        isnan_node.run(self.record)
        result = self.record.get(isnan_node._output)
        expected = np.isnan(test_array)
        np.testing.assert_array_equal(result, expected)

        # Test isposinfinite
        self.record = NodeRecord.empty()
        isposinf_node = IsposinfiniteNode()
        self.record.set(isposinf_node._input_pins[0], test_array)
        isposinf_node.run(self.record)
        result = self.record.get(isposinf_node._output)
        expected = np.isposinf(test_array)
        np.testing.assert_array_equal(result, expected)

        # Test isneginfinite
        self.record = NodeRecord.empty()
        isneginf_node = IsneginfiniteNode()
        self.record.set(isneginf_node._input_pins[0], test_array)
        isneginf_node.run(self.record)
        result = self.record.get(isneginf_node._output)
        expected = np.isneginf(test_array)
        np.testing.assert_array_equal(result, expected)

    def test_type_testing(self):
        """Test type testing nodes."""
        # Test isreal
        complex_array = np.array([1+0j, 2+3j, 4+0j])
        isreal_node = IsrealNode()
        self.record.set(isreal_node._input_pins[0], complex_array)
        isreal_node.run(self.record)
        result = self.record.get(isreal_node._output)
        expected = np.isreal(complex_array)
        np.testing.assert_array_equal(result, expected)

        # Test iscomplex
        self.record = NodeRecord.empty()
        iscomplex_node = IscomplexNode()
        self.record.set(iscomplex_node._input_pins[0], complex_array)
        iscomplex_node.run(self.record)
        result = self.record.get(iscomplex_node._output)
        expected = np.iscomplex(complex_array)
        np.testing.assert_array_equal(result, expected)

        # Test isrealobj
        self.record = NodeRecord.empty()
        real_array = np.array([1, 2, 3])
        isrealobj_node = IsrealobjNode()
        self.record.set(isrealobj_node._input_pins[0], real_array)
        isrealobj_node.run(self.record)
        result = self.record.get(isrealobj_node._output)
        expected = np.isrealobj(real_array)
        np.testing.assert_equal(result, expected)

        # Test iscomplexobj
        self.record = NodeRecord.empty()
        iscomplexobj_node = IscomplexobjNode()
        self.record.set(iscomplexobj_node._input_pins[0], complex_array)
        iscomplexobj_node.run(self.record)
        result = self.record.get(iscomplexobj_node._output)
        expected = np.iscomplexobj(complex_array)
        np.testing.assert_equal(result, expected)

        # Test isscalar
        self.record = NodeRecord.empty()
        isscalar_node = IsscalarNode()
        self.record.set(isscalar_node._input_pins[0], 5)
        isscalar_node.run(self.record)
        result = self.record.get(isscalar_node._output)
        expected = np.isscalar(5)
        np.testing.assert_equal(result, expected)

    def test_array_location_functions(self):
        """Test array location function nodes."""
        test_array = np.array([0, 1, 0, 3, 0, 5])

        # Test nonzero
        nonzero_node = NonzeroNode()
        self.record.set(nonzero_node._input_pins[0], test_array)
        nonzero_node.run(self.record)
        result = self.record.get(nonzero_node._output)
        expected = np.nonzero(test_array)

        # nonzero returns a tuple of arrays
        self.assertEqual(len(result), len(expected))
        for r, e in zip(result, expected):
            np.testing.assert_array_equal(r, e)

        # Test flatnonzero
        self.record = NodeRecord.empty()
        flatnonzero_node = FlatnonzeroNode()
        self.record.set(flatnonzero_node._input_pins[0], test_array)
        flatnonzero_node.run(self.record)
        result = self.record.get(flatnonzero_node._output)
        expected = np.flatnonzero(test_array)
        np.testing.assert_array_equal(result, expected)

        # Test argwhere
        self.record = NodeRecord.empty()
        argwhere_node = ArgwhereNode()
        test_2d = np.array([[0, 1, 0], [3, 0, 5]])
        self.record.set(argwhere_node._input_pins[0], test_2d)
        argwhere_node.run(self.record)
        result = self.record.get(argwhere_node._output)
        expected = np.argwhere(test_2d)
        np.testing.assert_array_equal(result, expected)

    def test_conditional_functions(self):
        """Test conditional function nodes."""
        # Test where
        where_node = WhereNode()
        condition = np.array([True, False, True, False])
        x = np.array([1, 2, 3, 4])
        y = np.array([10, 20, 30, 40])

        self.record.set(where_node._input_pins[0], condition)
        self.record.set(where_node._input_pins[1], x)
        self.record.set(where_node._input_pins[2], y)
        where_node.run(self.record)
        result = self.record.get(where_node._output)
        expected = np.where(condition, x, y)
        np.testing.assert_array_equal(result, expected)

        # Test select
        self.record = NodeRecord.empty()
        select_node = SelectNode()
        condlist = [
            np.array([True, False, False]),
            np.array([False, True, False]),
            np.array([False, False, True])
        ]
        choicelist = [
            np.array([1, 1, 1]),
            np.array([2, 2, 2]),
            np.array([3, 3, 3])
        ]

        self.record.set(select_node._input_pins[0], condlist)
        self.record.set(select_node._input_pins[1], choicelist)
        select_node.run(self.record)
        result = self.record.get(select_node._output)
        expected = np.select(condlist, choicelist)
        np.testing.assert_array_equal(result, expected)

    def test_datetime_testing(self):
        """Test datetime testing functions."""
        # Test isnat (is not-a-time)
        isnat_node = IsnatNode()

        # Create datetime array with NaT values
        dt_array = np.array(['2023-01-01', 'NaT', '2023-12-31'], dtype='datetime64')
        self.record.set(isnat_node._input_pins[0], dt_array)
        isnat_node.run(self.record)
        result = self.record.get(isnat_node._output)
        expected = np.isnat(dt_array)
        np.testing.assert_array_equal(result, expected)

    def test_edge_cases(self):
        """Test edge cases for logic operations."""
        # Test with empty arrays
        empty_array = np.array([])

        # All should return True for empty arrays
        all_node = AllNode()
        self.record.set(all_node._input_pins[0], empty_array)
        all_node.run(self.record)
        result = self.record.get(all_node._output)
        self.assertTrue(result)

        # Any should return False for empty arrays
        self.record = NodeRecord.empty()
        any_node = AnyNode()
        self.record.set(any_node._input_pins[0], empty_array)
        any_node.run(self.record)
        result = self.record.get(any_node._output)
        self.assertFalse(result)

        # Test with single element arrays
        single_true = np.array([True])
        single_false = np.array([False])

        self.record = NodeRecord.empty()
        self.record.set(all_node._input_pins[0], single_true)
        all_node.run(self.record)
        result = self.record.get(all_node._output)
        self.assertTrue(result)

        self.record = NodeRecord.empty()
        self.record.set(all_node._input_pins[0], single_false)
        all_node.run(self.record)
        result = self.record.get(all_node._output)
        self.assertFalse(result)