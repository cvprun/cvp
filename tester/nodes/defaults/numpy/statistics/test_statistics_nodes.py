# -*- coding: utf-8 -*-

from unittest import TestCase

import numpy as np

from cvp.nodes.defaults.numpy.statistics.argmax_node import ArgmaxNode
from cvp.nodes.defaults.numpy.statistics.argmin_node import ArgminNode
from cvp.nodes.defaults.numpy.statistics.argsort_node import ArgsortNode
from cvp.nodes.defaults.numpy.statistics.bincount_node import BincountNode
from cvp.nodes.defaults.numpy.statistics.corrcoef_node import CorrcoefNode
from cvp.nodes.defaults.numpy.statistics.cov_node import CovNode
from cvp.nodes.defaults.numpy.statistics.cumprod_node import CumprodNode
from cvp.nodes.defaults.numpy.statistics.cumsum_node import CumsumNode
from cvp.nodes.defaults.numpy.statistics.histogram_node import HistogramNode
from cvp.nodes.defaults.numpy.statistics.max_node import MaxNode
from cvp.nodes.defaults.numpy.statistics.mean_node import MeanNode
from cvp.nodes.defaults.numpy.statistics.median_node import MedianNode
from cvp.nodes.defaults.numpy.statistics.min_node import MinNode
from cvp.nodes.defaults.numpy.statistics.percentile_node import PercentileNode
from cvp.nodes.defaults.numpy.statistics.prod_node import ProdNode
from cvp.nodes.defaults.numpy.statistics.ptp_node import PtpNode
from cvp.nodes.defaults.numpy.statistics.quantile_node import QuantileNode
from cvp.nodes.defaults.numpy.statistics.sort_node import SortNode
from cvp.nodes.defaults.numpy.statistics.std_node import StdNode
from cvp.nodes.defaults.numpy.statistics.sum_node import SumNode
from cvp.nodes.defaults.numpy.statistics.var_node import VarNode
from cvp.nodes.record import NodeRecord


class TestStatisticsNodes(TestCase):

    def setUp(self):
        self.record = NodeRecord.empty()
        self.test_array = np.array([3, 1, 4, 1, 5, 9, 2, 6])
        self.test_2d_array = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

    def test_basic_statistics(self):
        """Test basic statistics nodes."""
        # Test mean
        mean_node = MeanNode()
        self.record.set(mean_node._input_pins[0], self.test_array)
        mean_node.run(self.record)
        result = self.record.get(mean_node._output)
        expected = np.mean(self.test_array)
        np.testing.assert_almost_equal(result, expected)

        # Test median
        self.record = NodeRecord.empty()
        median_node = MedianNode()
        self.record.set(median_node._input_pins[0], self.test_array)
        median_node.run(self.record)
        result = self.record.get(median_node._output)
        expected = np.median(self.test_array)
        np.testing.assert_almost_equal(result, expected)

        # Test std
        self.record = NodeRecord.empty()
        std_node = StdNode()
        self.record.set(std_node._input_pins[0], self.test_array)
        std_node.run(self.record)
        result = self.record.get(std_node._output)
        expected = np.std(self.test_array)
        np.testing.assert_almost_equal(result, expected)

        # Test var
        self.record = NodeRecord.empty()
        var_node = VarNode()
        self.record.set(var_node._input_pins[0], self.test_array)
        var_node.run(self.record)
        result = self.record.get(var_node._output)
        expected = np.var(self.test_array)
        np.testing.assert_almost_equal(result, expected)

    def test_min_max_functions(self):
        """Test min/max function nodes."""
        # Test min
        min_node = MinNode()
        self.record.set(min_node._input_pins[0], self.test_array)
        min_node.run(self.record)
        result = self.record.get(min_node._output)
        expected = np.min(self.test_array)
        np.testing.assert_equal(result, expected)

        # Test max
        self.record = NodeRecord.empty()
        max_node = MaxNode()
        self.record.set(max_node._input_pins[0], self.test_array)
        max_node.run(self.record)
        result = self.record.get(max_node._output)
        expected = np.max(self.test_array)
        np.testing.assert_equal(result, expected)

        # Test ptp (peak-to-peak)
        self.record = NodeRecord.empty()
        ptp_node = PtpNode()
        self.record.set(ptp_node._input_pins[0], self.test_array)
        ptp_node.run(self.record)
        result = self.record.get(ptp_node._output)
        expected = np.ptp(self.test_array)
        np.testing.assert_equal(result, expected)

    def test_arg_functions(self):
        """Test argmin/argmax function nodes."""
        # Test argmin
        argmin_node = ArgminNode()
        self.record.set(argmin_node._input_pins[0], self.test_array)
        argmin_node.run(self.record)
        result = self.record.get(argmin_node._output)
        expected = np.argmin(self.test_array)
        np.testing.assert_equal(result, expected)

        # Test argmax
        self.record = NodeRecord.empty()
        argmax_node = ArgmaxNode()
        self.record.set(argmax_node._input_pins[0], self.test_array)
        argmax_node.run(self.record)
        result = self.record.get(argmax_node._output)
        expected = np.argmax(self.test_array)
        np.testing.assert_equal(result, expected)

    def test_sorting_functions(self):
        """Test sorting function nodes."""
        # Test sort
        sort_node = SortNode()
        self.record.set(sort_node._input_pins[0], self.test_array)
        sort_node.run(self.record)
        result = self.record.get(sort_node._output)
        expected = np.sort(self.test_array)
        np.testing.assert_array_equal(result, expected)

        # Test argsort
        self.record = NodeRecord.empty()
        argsort_node = ArgsortNode()
        self.record.set(argsort_node._input_pins[0], self.test_array)
        argsort_node.run(self.record)
        result = self.record.get(argsort_node._output)
        expected = np.argsort(self.test_array)
        np.testing.assert_array_equal(result, expected)

    def test_sum_prod_functions(self):
        """Test sum and product function nodes."""
        # Test sum
        sum_node = SumNode()
        self.record.set(sum_node._input_pins[0], self.test_array)
        sum_node.run(self.record)
        result = self.record.get(sum_node._output)
        expected = np.sum(self.test_array)
        np.testing.assert_equal(result, expected)

        # Test prod
        self.record = NodeRecord.empty()
        prod_node = ProdNode()
        test_small_array = np.array([1, 2, 3, 4])
        self.record.set(prod_node._input_pins[0], test_small_array)
        prod_node.run(self.record)
        result = self.record.get(prod_node._output)
        expected = np.prod(test_small_array)
        np.testing.assert_equal(result, expected)

    def test_cumulative_functions(self):
        """Test cumulative function nodes."""
        # Test cumsum
        cumsum_node = CumsumNode()
        test_array = np.array([1, 2, 3, 4])
        self.record.set(cumsum_node._input_pins[0], test_array)
        cumsum_node.run(self.record)
        result = self.record.get(cumsum_node._output)
        expected = np.cumsum(test_array)
        np.testing.assert_array_equal(result, expected)

        # Test cumprod
        self.record = NodeRecord.empty()
        cumprod_node = CumprodNode()
        test_array = np.array([1, 2, 3, 2])
        self.record.set(cumprod_node._input_pins[0], test_array)
        cumprod_node.run(self.record)
        result = self.record.get(cumprod_node._output)
        expected = np.cumprod(test_array)
        np.testing.assert_array_equal(result, expected)

    def test_percentile_quantile_functions(self):
        """Test percentile and quantile function nodes."""
        # Test percentile
        percentile_node = PercentileNode()
        self.record.set(percentile_node._input_pins[0], self.test_array)
        self.record.set(percentile_node._input_pins[1], 50)  # 50th percentile (median)
        percentile_node.run(self.record)
        result = self.record.get(percentile_node._output)
        expected = np.percentile(self.test_array, 50)
        np.testing.assert_almost_equal(result, expected)

        # Test quantile
        self.record = NodeRecord.empty()
        quantile_node = QuantileNode()
        self.record.set(quantile_node._input_pins[0], self.test_array)
        self.record.set(quantile_node._input_pins[1], 0.5)  # 50th quantile (median)
        quantile_node.run(self.record)
        result = self.record.get(quantile_node._output)
        expected = np.quantile(self.test_array, 0.5)
        np.testing.assert_almost_equal(result, expected)

    def test_correlation_covariance_functions(self):
        """Test correlation and covariance function nodes."""
        # Test covariance
        cov_node = CovNode()
        test_data = np.array([[1, 2, 3], [4, 5, 6]])
        self.record.set(cov_node._input_pins[0], test_data)
        cov_node.run(self.record)
        result = self.record.get(cov_node._output)
        expected = np.cov(test_data)
        np.testing.assert_array_almost_equal(result, expected)

        # Test correlation coefficient
        self.record = NodeRecord.empty()
        corrcoef_node = CorrcoefNode()
        self.record.set(corrcoef_node._input_pins[0], test_data)
        corrcoef_node.run(self.record)
        result = self.record.get(corrcoef_node._output)
        expected = np.corrcoef(test_data)
        np.testing.assert_array_almost_equal(result, expected)

    def test_histogram_functions(self):
        """Test histogram function nodes."""
        # Test histogram
        histogram_node = HistogramNode()
        test_data = np.array([1, 2, 1, 3, 2, 1, 4, 3, 2])
        bins = 4
        self.record.set(histogram_node._input_pins[0], test_data)
        self.record.set(histogram_node._input_pins[1], bins)
        histogram_node.run(self.record)
        result = self.record.get(histogram_node._output)
        expected_hist, expected_bins = np.histogram(test_data, bins)

        # Result should be a tuple (hist, bin_edges)
        result_hist, result_bins = result
        np.testing.assert_array_equal(result_hist, expected_hist)
        np.testing.assert_array_almost_equal(result_bins, expected_bins)

    def test_bincount_function(self):
        """Test bincount function node."""
        bincount_node = BincountNode()
        test_data = np.array([0, 1, 1, 3, 2, 1, 7])
        self.record.set(bincount_node._input_pins[0], test_data)
        bincount_node.run(self.record)
        result = self.record.get(bincount_node._output)
        expected = np.bincount(test_data)
        np.testing.assert_array_equal(result, expected)

    def test_axis_parameter(self):
        """Test statistics functions with axis parameter."""
        # Test mean with axis
        mean_node = MeanNode()
        self.record.set(mean_node._input_pins[0], self.test_2d_array)
        if len(mean_node._input_pins) > 1:  # If axis parameter exists
            self.record.set(mean_node._input_pins[1], 0)  # axis=0
        mean_node.run(self.record)
        result = self.record.get(mean_node._output)

        if len(mean_node._input_pins) > 1:
            expected = np.mean(self.test_2d_array, axis=0)
            np.testing.assert_array_almost_equal(result, expected)
        else:
            expected = np.mean(self.test_2d_array)
            np.testing.assert_almost_equal(result, expected)

    def test_2d_array_statistics(self):
        """Test statistics on 2D arrays."""
        # Test sum on 2D array
        sum_node = SumNode()
        self.record.set(sum_node._input_pins[0], self.test_2d_array)
        sum_node.run(self.record)
        result = self.record.get(sum_node._output)
        expected = np.sum(self.test_2d_array)
        np.testing.assert_equal(result, expected)