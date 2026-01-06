# -*- coding: utf-8 -*-

from unittest import TestCase

import numpy as np

from cvp.nodes.defaults.numpy.fft.fft2_node import Fft2Node
from cvp.nodes.defaults.numpy.fft.fft_node import FftNode
from cvp.nodes.defaults.numpy.fft.fftfreq_node import FftfreqNode
from cvp.nodes.defaults.numpy.fft.fftn_node import FftnNode
from cvp.nodes.defaults.numpy.fft.fftshift_node import FftshiftNode
from cvp.nodes.defaults.numpy.fft.ifft2_node import Ifft2Node
from cvp.nodes.defaults.numpy.fft.ifft_node import IfftNode
from cvp.nodes.defaults.numpy.fft.ifftn_node import IfftnNode
from cvp.nodes.defaults.numpy.fft.ifftshift_node import IfftshiftNode
from cvp.nodes.defaults.numpy.fft.irfft2_node import Irfft2Node
from cvp.nodes.defaults.numpy.fft.irfft_node import IrfftNode
from cvp.nodes.defaults.numpy.fft.irfftn_node import IrfftnNode
from cvp.nodes.defaults.numpy.fft.rfft2_node import Rfft2Node
from cvp.nodes.defaults.numpy.fft.rfft_node import RfftNode
from cvp.nodes.defaults.numpy.fft.rfftfreq_node import RfftfreqNode
from cvp.nodes.defaults.numpy.fft.rfftn_node import RfftnNode
from cvp.nodes.record import NodeRecord


class TestFftNodes(TestCase):

    def setUp(self):
        self.record = NodeRecord.empty()
        # Create test signals
        self.real_signal_1d = np.array([1, 2, 3, 4, 3, 2, 1, 0])
        self.complex_signal_1d = np.array([1 + 1j, 2 + 0j, 3 - 1j, 4 + 2j])
        self.real_signal_2d = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]])
        self.complex_signal_2d = np.array([[1 + 1j, 2 + 0j], [3 - 1j, 4 + 2j]])

    def test_basic_fft_operations(self):
        """Test basic 1D FFT operations."""
        # Test FFT
        fft_node = FftNode()
        self.record.set(fft_node._input_pins[0], self.real_signal_1d)
        fft_node.run(self.record)
        fft_result = self.record.get(fft_node._output)
        expected_fft = np.fft.fft(self.real_signal_1d)
        np.testing.assert_array_almost_equal(fft_result, expected_fft)

        # Test IFFT (inverse)
        self.record = NodeRecord.empty()
        ifft_node = IfftNode()
        self.record.set(ifft_node._input_pins[0], fft_result)
        ifft_node.run(self.record)
        ifft_result = self.record.get(ifft_node._output)
        # IFFT should recover original signal
        np.testing.assert_array_almost_equal(ifft_result, self.real_signal_1d)

    def test_real_fft_operations(self):
        """Test real FFT operations (more efficient for real inputs)."""
        # Test RFFT
        rfft_node = RfftNode()
        self.record.set(rfft_node._input_pins[0], self.real_signal_1d)
        rfft_node.run(self.record)
        rfft_result = self.record.get(rfft_node._output)
        expected_rfft = np.fft.rfft(self.real_signal_1d)
        np.testing.assert_array_almost_equal(rfft_result, expected_rfft)

        # Test IRFFT (inverse real FFT)
        self.record = NodeRecord.empty()
        irfft_node = IrfftNode()
        self.record.set(irfft_node._input_pins[0], rfft_result)
        irfft_node.run(self.record)
        irfft_result = self.record.get(irfft_node._output)
        # Should recover original signal
        np.testing.assert_array_almost_equal(irfft_result, self.real_signal_1d)

    def test_2d_fft_operations(self):
        """Test 2D FFT operations."""
        # Test FFT2
        fft2_node = Fft2Node()
        self.record.set(fft2_node._input_pins[0], self.real_signal_2d)
        fft2_node.run(self.record)
        fft2_result = self.record.get(fft2_node._output)
        expected_fft2 = np.fft.fft2(self.real_signal_2d)
        np.testing.assert_array_almost_equal(fft2_result, expected_fft2)

        # Test IFFT2 (inverse)
        self.record = NodeRecord.empty()
        ifft2_node = Ifft2Node()
        self.record.set(ifft2_node._input_pins[0], fft2_result)
        ifft2_node.run(self.record)
        ifft2_result = self.record.get(ifft2_node._output)
        # Should recover original signal
        np.testing.assert_array_almost_equal(ifft2_result, self.real_signal_2d)

        # Test RFFT2 (real 2D FFT)
        self.record = NodeRecord.empty()
        rfft2_node = Rfft2Node()
        self.record.set(rfft2_node._input_pins[0], self.real_signal_2d)
        rfft2_node.run(self.record)
        rfft2_result = self.record.get(rfft2_node._output)
        expected_rfft2 = np.fft.rfft2(self.real_signal_2d)
        np.testing.assert_array_almost_equal(rfft2_result, expected_rfft2)

        # Test IRFFT2 (inverse real 2D FFT)
        self.record = NodeRecord.empty()
        irfft2_node = Irfft2Node()
        self.record.set(irfft2_node._input_pins[0], rfft2_result)
        irfft2_node.run(self.record)
        irfft2_result = self.record.get(irfft2_node._output)
        # Should recover original signal
        np.testing.assert_array_almost_equal(irfft2_result, self.real_signal_2d)

    def test_nd_fft_operations(self):
        """Test N-dimensional FFT operations."""
        # Create 3D test data
        signal_3d = np.random.random((4, 4, 4))

        # Test FFTN
        fftn_node = FftnNode()
        self.record.set(fftn_node._input_pins[0], signal_3d)
        fftn_node.run(self.record)
        fftn_result = self.record.get(fftn_node._output)
        expected_fftn = np.fft.fftn(signal_3d)
        np.testing.assert_array_almost_equal(fftn_result, expected_fftn)

        # Test IFFTN (inverse)
        self.record = NodeRecord.empty()
        ifftn_node = IfftnNode()
        self.record.set(ifftn_node._input_pins[0], fftn_result)
        ifftn_node.run(self.record)
        ifftn_result = self.record.get(ifftn_node._output)
        # Should recover original signal
        np.testing.assert_array_almost_equal(ifftn_result, signal_3d)

        # Test RFFTN (real N-D FFT)
        self.record = NodeRecord.empty()
        rfftn_node = RfftnNode()
        self.record.set(rfftn_node._input_pins[0], signal_3d)
        rfftn_node.run(self.record)
        rfftn_result = self.record.get(rfftn_node._output)
        expected_rfftn = np.fft.rfftn(signal_3d)
        np.testing.assert_array_almost_equal(rfftn_result, expected_rfftn)

        # Test IRFFTN (inverse real N-D FFT)
        self.record = NodeRecord.empty()
        irfftn_node = IrfftnNode()
        self.record.set(irfftn_node._input_pins[0], rfftn_result)
        irfftn_node.run(self.record)
        irfftn_result = self.record.get(irfftn_node._output)
        # Should recover original signal
        np.testing.assert_array_almost_equal(irfftn_result, signal_3d)

    def test_fft_shifting(self):
        """Test FFT shifting operations."""
        # Test fftshift
        fftshift_node = FftshiftNode()
        self.record.set(fftshift_node._input_pins[0], self.real_signal_1d)
        fftshift_node.run(self.record)
        fftshift_result = self.record.get(fftshift_node._output)
        expected_fftshift = np.fft.fftshift(self.real_signal_1d)
        np.testing.assert_array_almost_equal(fftshift_result, expected_fftshift)

        # Test ifftshift (inverse)
        self.record = NodeRecord.empty()
        ifftshift_node = IfftshiftNode()
        self.record.set(ifftshift_node._input_pins[0], fftshift_result)
        ifftshift_node.run(self.record)
        ifftshift_result = self.record.get(ifftshift_node._output)
        # Should recover original signal
        np.testing.assert_array_almost_equal(ifftshift_result, self.real_signal_1d)

        # Test fftshift on 2D array
        self.record = NodeRecord.empty()
        self.record.set(fftshift_node._input_pins[0], self.real_signal_2d)
        fftshift_node.run(self.record)
        fftshift_2d_result = self.record.get(fftshift_node._output)
        expected_fftshift_2d = np.fft.fftshift(self.real_signal_2d)
        np.testing.assert_array_almost_equal(fftshift_2d_result, expected_fftshift_2d)

    def test_frequency_arrays(self):
        """Test frequency array generation."""
        n = 8
        d = 1.0  # sample spacing

        # Test fftfreq
        fftfreq_node = FftfreqNode()
        self.record.set(fftfreq_node._input_pins[0], n)
        self.record.set(fftfreq_node._input_pins[1], d)
        fftfreq_node.run(self.record)
        fftfreq_result = self.record.get(fftfreq_node._output)
        expected_fftfreq = np.fft.fftfreq(n, d)
        np.testing.assert_array_almost_equal(fftfreq_result, expected_fftfreq)

        # Test rfftfreq
        self.record = NodeRecord.empty()
        rfftfreq_node = RfftfreqNode()
        self.record.set(rfftfreq_node._input_pins[0], n)
        self.record.set(rfftfreq_node._input_pins[1], d)
        rfftfreq_node.run(self.record)
        rfftfreq_result = self.record.get(rfftfreq_node._output)
        expected_rfftfreq = np.fft.rfftfreq(n, d)
        np.testing.assert_array_almost_equal(rfftfreq_result, expected_rfftfreq)

        # Check that rfftfreq gives positive frequencies only
        self.assertTrue(np.all(rfftfreq_result >= 0))

    def test_complex_inputs(self):
        """Test FFT operations with complex inputs."""
        # Test FFT with complex input
        fft_node = FftNode()
        self.record.set(fft_node._input_pins[0], self.complex_signal_1d)
        fft_node.run(self.record)
        fft_result = self.record.get(fft_node._output)
        expected_fft = np.fft.fft(self.complex_signal_1d)
        np.testing.assert_array_almost_equal(fft_result, expected_fft)

        # Test 2D FFT with complex input
        self.record = NodeRecord.empty()
        fft2_node = Fft2Node()
        self.record.set(fft2_node._input_pins[0], self.complex_signal_2d)
        fft2_node.run(self.record)
        fft2_result = self.record.get(fft2_node._output)
        expected_fft2 = np.fft.fft2(self.complex_signal_2d)
        np.testing.assert_array_almost_equal(fft2_result, expected_fft2)

    def test_fft_properties(self):
        """Test mathematical properties of FFT."""
        # Test Parseval's theorem: energy conservation
        fft_node = FftNode()
        self.record.set(fft_node._input_pins[0], self.real_signal_1d)
        fft_node.run(self.record)
        fft_result = self.record.get(fft_node._output)

        # Energy in time domain
        energy_time = np.sum(np.abs(self.real_signal_1d) ** 2)
        # Energy in frequency domain (scaled by length)
        energy_freq = np.sum(np.abs(fft_result) ** 2) / len(self.real_signal_1d)

        np.testing.assert_almost_equal(energy_time, energy_freq, decimal=10)

    def test_fft_linearity(self):
        """Test linearity property of FFT."""
        signal1 = np.array([1, 2, 3, 4])
        signal2 = np.array([4, 3, 2, 1])
        a, b = 2, 3

        fft_node = FftNode()

        # FFT of linear combination
        combined_signal = a * signal1 + b * signal2
        self.record.set(fft_node._input_pins[0], combined_signal)
        fft_node.run(self.record)
        fft_combined = self.record.get(fft_node._output)

        # Linear combination of FFTs
        self.record = NodeRecord.empty()
        self.record.set(fft_node._input_pins[0], signal1)
        fft_node.run(self.record)
        fft1 = self.record.get(fft_node._output)

        self.record = NodeRecord.empty()
        self.record.set(fft_node._input_pins[0], signal2)
        fft_node.run(self.record)
        fft2 = self.record.get(fft_node._output)

        combined_fft = a * fft1 + b * fft2

        # Should be equal due to linearity
        np.testing.assert_array_almost_equal(fft_combined, combined_fft)

    def test_dc_component(self):
        """Test DC component handling in FFT."""
        # Signal with DC offset
        dc_signal = np.ones(8) * 5  # DC signal

        fft_node = FftNode()
        self.record.set(fft_node._input_pins[0], dc_signal)
        fft_node.run(self.record)
        fft_result = self.record.get(fft_node._output)

        # DC component should be at index 0
        dc_component = fft_result[0]
        # DC component should equal sum of signal
        np.testing.assert_almost_equal(dc_component, np.sum(dc_signal))

        # All other components should be (nearly) zero
        ac_components = fft_result[1:]
        np.testing.assert_array_almost_equal(ac_components, 0, decimal=10)

    def test_nyquist_frequency(self):
        """Test Nyquist frequency handling."""
        # For even-length signals, check Nyquist component
        even_signal = np.array([1, 2, 3, 4, 5, 6, 7, 8])

        fft_node = FftNode()
        self.record.set(fft_node._input_pins[0], even_signal)
        fft_node.run(self.record)
        fft_result = self.record.get(fft_node._output)

        # For real signals, Nyquist frequency component should be real
        nyquist_index = len(even_signal) // 2
        nyquist_component = fft_result[nyquist_index]
        # Check that imaginary part is (nearly) zero
        np.testing.assert_almost_equal(np.imag(nyquist_component), 0, decimal=10)

    def test_edge_cases(self):
        """Test edge cases for FFT operations."""
        # Test with single element
        single_element = np.array([5])
        fft_node = FftNode()
        self.record.set(fft_node._input_pins[0], single_element)
        fft_node.run(self.record)
        fft_result = self.record.get(fft_node._output)
        np.testing.assert_array_equal(fft_result, single_element)

        # Test with two elements
        self.record = NodeRecord.empty()
        two_elements = np.array([1, 2])
        self.record.set(fft_node._input_pins[0], two_elements)
        fft_node.run(self.record)
        fft_result = self.record.get(fft_node._output)
        expected = np.fft.fft(two_elements)
        np.testing.assert_array_almost_equal(fft_result, expected)

    def test_zero_padding_effect(self):
        """Test effect of zero padding on FFT."""
        # Original signal
        original = np.array([1, 2, 3, 4])
        # Zero-padded version
        padded = np.concatenate([original, np.zeros(4)])

        fft_node = FftNode()

        # FFT of original
        self.record.set(fft_node._input_pins[0], original)
        fft_node.run(self.record)
        fft_original = self.record.get(fft_node._output)

        # FFT of padded
        self.record = NodeRecord.empty()
        self.record.set(fft_node._input_pins[0], padded)
        fft_node.run(self.record)
        fft_padded = self.record.get(fft_node._output)

        # Zero padding should interpolate the frequency spectrum
        # Check that the padded FFT has twice the length
        self.assertEqual(len(fft_padded), 2 * len(fft_original))

        # Every other sample of the padded FFT should approximate the original
        # (this is an approximation due to interpolation effects)
        downsampled = fft_padded[::2]
        # Allow for small numerical differences
        np.testing.assert_array_almost_equal(downsampled, fft_original, decimal=10)
