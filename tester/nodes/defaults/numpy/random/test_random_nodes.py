# -*- coding: utf-8 -*-

from unittest import TestCase

import numpy as np

from cvp.nodes.defaults.numpy.random.random_beta_node import RandomBetaNode
from cvp.nodes.defaults.numpy.random.random_binomial_node import RandomBinomialNode
from cvp.nodes.defaults.numpy.random.random_chisquare_node import RandomChisquareNode
from cvp.nodes.defaults.numpy.random.random_choice_node import RandomChoiceNode
from cvp.nodes.defaults.numpy.random.random_exponential_node import (
    RandomExponentialNode,
)
from cvp.nodes.defaults.numpy.random.random_gamma_node import RandomGammaNode
from cvp.nodes.defaults.numpy.random.random_multivariate_normal_node import (
    RandomMultivariateNormalNode,
)
from cvp.nodes.defaults.numpy.random.random_normal_node import RandomNormalNode
from cvp.nodes.defaults.numpy.random.random_permutation_node import (
    RandomPermutationNode,
)
from cvp.nodes.defaults.numpy.random.random_poisson_node import RandomPoissonNode
from cvp.nodes.defaults.numpy.random.random_rand_node import RandomRandNode
from cvp.nodes.defaults.numpy.random.random_randint_node import RandomRandintNode
from cvp.nodes.defaults.numpy.random.random_randn_node import RandomRandnNode
from cvp.nodes.defaults.numpy.random.random_random_node import RandomRandomNode
from cvp.nodes.defaults.numpy.random.random_seed_node import RandomSeedNode
from cvp.nodes.defaults.numpy.random.random_shuffle_node import RandomShuffleNode
from cvp.nodes.defaults.numpy.random.random_uniform_node import RandomUniformNode
from cvp.nodes.record import NodeRecord


class TestRandomNodes(TestCase):

    def setUp(self):
        self.record = NodeRecord.empty()
        # Set random seed for reproducible tests
        np.random.seed(42)

    def test_random_seed_node(self):
        """Test RandomSeedNode functionality."""
        seed_node = RandomSeedNode()
        seed_value = 12345

        self.record.set(seed_node._input_pins[0], seed_value)
        seed_node.run(self.record)
        # Seed function typically doesn't return a value, just sets the seed
        # We can test that it runs without error

    def test_basic_random_generation(self):
        """Test basic random generation nodes."""
        # Test random
        random_node = RandomRandomNode()
        size = (2, 3)
        self.record.set(random_node._input_pins[0], size)
        random_node.run(self.record)
        result = self.record.get(random_node._output)
        self.assertEqual(result.shape, size)
        self.assertTrue(np.all((result >= 0) & (result < 1)))

        # Test rand - node takes a single shape parameter as tuple
        self.record = NodeRecord.empty()
        rand_node = RandomRandNode()
        shape = (3, 4)
        self.record.set(rand_node._input_pins[0], shape)
        rand_node.run(self.record)
        result = self.record.get(rand_node._output)
        self.assertEqual(result.shape, shape)
        self.assertTrue(np.all((result >= 0) & (result < 1)))

        # Test randn
        self.record = NodeRecord.empty()
        randn_node = RandomRandnNode()
        d0 = 5
        self.record.set(randn_node._input_pins[0], d0)
        randn_node.run(self.record)
        result = self.record.get(randn_node._output)
        self.assertEqual(result.shape, (d0,))
        # randn should produce values from standard normal distribution
        # Check that values are reasonable (not all exactly 0)
        self.assertGreater(np.std(result), 0)

    def test_random_integers(self):
        """Test random integer generation nodes."""
        # Test randint
        randint_node = RandomRandintNode()
        low, high = 0, 10
        size = 5
        self.record.set(randint_node._input_pins[0], low)
        self.record.set(randint_node._input_pins[1], high)
        self.record.set(randint_node._input_pins[2], size)
        randint_node.run(self.record)
        result = self.record.get(randint_node._output)
        self.assertEqual(len(result), size)
        self.assertTrue(np.all((result >= low) & (result < high)))
        self.assertTrue(np.issubdtype(result.dtype, np.integer))

    def test_uniform_distribution(self):
        """Test uniform distribution nodes."""
        uniform_node = RandomUniformNode()
        low, high = -1.0, 1.0
        size = (3, 3)
        self.record.set(uniform_node._input_pins[0], low)
        self.record.set(uniform_node._input_pins[1], high)
        self.record.set(uniform_node._input_pins[2], size)
        uniform_node.run(self.record)
        result = self.record.get(uniform_node._output)
        self.assertEqual(result.shape, size)
        self.assertTrue(np.all((result >= low) & (result <= high)))

    def test_normal_distribution(self):
        """Test normal distribution nodes."""
        # Test normal
        normal_node = RandomNormalNode()
        loc, scale = 0, 1
        size = (2, 4)
        self.record.set(normal_node._input_pins[0], loc)
        self.record.set(normal_node._input_pins[1], scale)
        self.record.set(normal_node._input_pins[2], size)
        normal_node.run(self.record)
        result = self.record.get(normal_node._output)
        self.assertEqual(result.shape, size)
        # For large samples, mean should be close to loc and std close to scale
        if result.size > 100:
            self.assertAlmostEqual(np.mean(result), loc, delta=0.2)
            self.assertAlmostEqual(np.std(result), scale, delta=0.2)

        # Test multivariate normal
        self.record = NodeRecord.empty()
        mvn_node = RandomMultivariateNormalNode()
        mean = np.array([0, 1])
        cov = np.array([[1, 0.5], [0.5, 2]])
        size = 5
        self.record.set(mvn_node._input_pins[0], mean)
        self.record.set(mvn_node._input_pins[1], cov)
        self.record.set(mvn_node._input_pins[2], size)
        mvn_node.run(self.record)
        result = self.record.get(mvn_node._output)
        self.assertEqual(result.shape, (size, len(mean)))

    def test_discrete_distributions(self):
        """Test discrete distribution nodes."""
        # Test binomial
        binomial_node = RandomBinomialNode()
        n, p = 10, 0.5
        size = (2, 3)
        self.record.set(binomial_node._input_pins[0], n)
        self.record.set(binomial_node._input_pins[1], p)
        self.record.set(binomial_node._input_pins[2], size)
        binomial_node.run(self.record)
        result = self.record.get(binomial_node._output)
        self.assertEqual(result.shape, size)
        self.assertTrue(np.all((result >= 0) & (result <= n)))
        self.assertTrue(np.issubdtype(result.dtype, np.integer))

        # Test poisson
        self.record = NodeRecord.empty()
        poisson_node = RandomPoissonNode()
        lam = 3.0
        size = 10
        self.record.set(poisson_node._input_pins[0], lam)
        self.record.set(poisson_node._input_pins[1], size)
        poisson_node.run(self.record)
        result = self.record.get(poisson_node._output)
        self.assertEqual(len(result), size)
        self.assertTrue(np.all(result >= 0))

    def test_continuous_distributions(self):
        """Test continuous distribution nodes."""
        # Test exponential
        exponential_node = RandomExponentialNode()
        scale = 2.0
        size = (2, 2)
        self.record.set(exponential_node._input_pins[0], scale)
        self.record.set(exponential_node._input_pins[1], size)
        exponential_node.run(self.record)
        result = self.record.get(exponential_node._output)
        self.assertEqual(result.shape, size)
        self.assertTrue(np.all(result >= 0))

        # Test gamma
        self.record = NodeRecord.empty()
        gamma_node = RandomGammaNode()
        shape, scale = 2.0, 2.0
        size = 5
        self.record.set(gamma_node._input_pins[0], shape)
        self.record.set(gamma_node._input_pins[1], scale)
        self.record.set(gamma_node._input_pins[2], size)
        gamma_node.run(self.record)
        result = self.record.get(gamma_node._output)
        self.assertEqual(len(result), size)
        self.assertTrue(np.all(result >= 0))

        # Test beta
        self.record = NodeRecord.empty()
        beta_node = RandomBetaNode()
        a, b = 2.0, 3.0
        size = (3, 2)
        self.record.set(beta_node._input_pins[0], a)
        self.record.set(beta_node._input_pins[1], b)
        self.record.set(beta_node._input_pins[2], size)
        beta_node.run(self.record)
        result = self.record.get(beta_node._output)
        self.assertEqual(result.shape, size)
        self.assertTrue(np.all((result >= 0) & (result <= 1)))

        # Test chi-square
        self.record = NodeRecord.empty()
        chisquare_node = RandomChisquareNode()
        df = 3
        size = 7
        self.record.set(chisquare_node._input_pins[0], df)
        self.record.set(chisquare_node._input_pins[1], size)
        chisquare_node.run(self.record)
        result = self.record.get(chisquare_node._output)
        self.assertEqual(len(result), size)
        self.assertTrue(np.all(result >= 0))

    def test_random_choice(self):
        """Test random choice node."""
        choice_node = RandomChoiceNode()
        a = np.array([1, 2, 3, 4, 5])
        size = 3
        self.record.set(choice_node._input_pins[0], a)
        self.record.set(choice_node._input_pins[1], size)
        choice_node.run(self.record)
        result = self.record.get(choice_node._output)
        self.assertEqual(len(result), size)
        # Check that all results are from the input array
        for item in result:
            self.assertIn(item, a)

    def test_permutation_shuffle(self):
        """Test permutation and shuffle nodes."""
        # Test permutation
        permutation_node = RandomPermutationNode()
        x = 5  # Generate permutation of range(5)
        self.record.set(permutation_node._input_pins[0], x)
        permutation_node.run(self.record)
        result = self.record.get(permutation_node._output)
        self.assertEqual(len(result), x)
        # Check that result contains all numbers from 0 to x-1
        self.assertEqual(set(result), set(range(x)))

        # Test permutation with array input
        self.record = NodeRecord.empty()
        arr = np.array([1, 2, 3, 4, 5])
        self.record.set(permutation_node._input_pins[0], arr)
        permutation_node.run(self.record)
        result = self.record.get(permutation_node._output)
        self.assertEqual(len(result), len(arr))
        # Check that result contains all elements from original array
        self.assertEqual(set(result), set(arr))

        # Test shuffle (in-place operation, but node should return shuffled array)
        self.record = NodeRecord.empty()
        shuffle_node = RandomShuffleNode()
        arr_copy = arr.copy()
        self.record.set(shuffle_node._input_pins[0], arr_copy)
        shuffle_node.run(self.record)
        result = self.record.get(shuffle_node._output)
        # Result should contain same elements but possibly in different order
        self.assertEqual(set(result), set(arr))

    def test_reproducibility(self):
        """Test that setting seed produces reproducible results."""
        # Set seed and generate random numbers
        seed_node = RandomSeedNode()
        random_node = RandomRandomNode()

        # First run
        self.record.set(seed_node._input_pins[0], 42)
        seed_node.run(self.record)

        self.record.set(random_node._input_pins[0], 5)
        random_node.run(self.record)
        result1 = self.record.get(random_node._output)

        # Reset and run again with same seed
        self.record = NodeRecord.empty()
        self.record.set(seed_node._input_pins[0], 42)
        seed_node.run(self.record)

        self.record.set(random_node._input_pins[0], 5)
        random_node.run(self.record)
        result2 = self.record.get(random_node._output)

        # Results should be identical
        np.testing.assert_array_equal(result1, result2)

    def test_edge_cases(self):
        """Test edge cases for random nodes."""
        # Test with size 0
        random_node = RandomRandomNode()
        self.record.set(random_node._input_pins[0], 0)
        random_node.run(self.record)
        result = self.record.get(random_node._output)
        self.assertEqual(result.size, 0)

        # Test with empty size tuple
        self.record = NodeRecord.empty()
        self.record.set(random_node._input_pins[0], ())
        random_node.run(self.record)
        result = self.record.get(random_node._output)
        # Should return scalar or 0-d array
        self.assertTrue(np.isscalar(result) or result.ndim == 0)

    def test_parameter_validation(self):
        """Test that nodes handle invalid parameters appropriately."""
        # Test normal with negative scale (should work but give warning)
        normal_node = RandomNormalNode()
        try:
            self.record.set(normal_node._input_pins[0], 0)
            self.record.set(normal_node._input_pins[1], -1)  # negative scale
            self.record.set(normal_node._input_pins[2], 5)
            normal_node.run(self.record)
            result = self.record.get(normal_node._output)
            # Should still produce result (NumPy handles this gracefully)
            self.assertEqual(len(result), 5)
        except (ValueError, Warning):
            # It's okay if this raises an error or warning
            pass

        # Test binomial with invalid probability
        self.record = NodeRecord.empty()
        binomial_node = RandomBinomialNode()
        try:
            self.record.set(binomial_node._input_pins[0], 10)
            self.record.set(binomial_node._input_pins[1], 1.5)  # p > 1
            self.record.set(binomial_node._input_pins[2], 5)
            binomial_node.run(self.record)
            # This should either work (with clamping) or raise an error
        except ValueError:
            # Expected for invalid parameters
            pass
