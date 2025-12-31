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


class RandomRandNode(NumpyFunctionNode):
    """Random values in a given shape."""

    def __init__(self):
        d_pin = DataInputPin(
            name=PinName("d0"),
            dtype=Dtype.any(),
            docs="First dimension",
            default=None,
        )
        super().__init__("rand", d_pin)

    def apply_function(self, d0, **kwargs) -> Any:
        if d0 is None:
            return np.random.rand()
        elif isinstance(d0, (list, tuple)):
            return np.random.rand(*d0)
        else:
            return np.random.rand(d0)


class RandomRandnNode(NumpyFunctionNode):
    """Return sample(s) from the "standard normal" distribution."""

    def __init__(self):
        d_pin = DataInputPin(
            name=PinName("d0"),
            dtype=Dtype.any(),
            docs="First dimension",
            default=None,
        )
        super().__init__("randn", d_pin)

    def apply_function(self, d0, **kwargs) -> Any:
        if d0 is None:
            return np.random.randn()
        elif isinstance(d0, (list, tuple)):
            return np.random.randn(*d0)
        else:
            return np.random.randn(d0)


class RandomRandintNode(NumpyFunctionNode):
    """Return random integers from low (inclusive) to high (exclusive)."""

    def __init__(self):
        low_pin = DataInputPin(
            name=PinName("low"),
            dtype=Dtype.any(),
            docs="Lowest (signed) integer to be drawn",
        )
        high_pin = DataInputPin(
            name=PinName("high"),
            dtype=Dtype.any(),
            docs="Highest (signed) integer to be drawn",
            default=None,
        )
        size_pin = DataInputPin(
            name=PinName("size"),
            dtype=Dtype.any(),
            docs="Output shape",
            default=None,
        )
        super().__init__("randint", low_pin, high_pin, size_pin)

    def apply_function(self, low, high, size, **kwargs) -> Any:
        return np.random.randint(low, high=high, size=size)


class RandomRandomNode(NumpyFunctionNode):
    """Return random floats in the half-open interval [0.0, 1.0)."""

    def __init__(self):
        size_pin = DataInputPin(
            name=PinName("size"),
            dtype=Dtype.any(),
            docs="Output shape",
            default=None,
        )
        super().__init__("random", size_pin)

    def apply_function(self, size, **kwargs) -> Any:
        return np.random.random(size=size)


class RandomChoiceNode(NumpyFunctionNode):
    """Generates a random sample from a given 1-D array."""

    def __init__(self):
        a_pin = DataInputPin(
            name=PinName("a"),
            dtype=Dtype.any(),
            docs="1-D array-like or int",
        )
        size_pin = DataInputPin(
            name=PinName("size"),
            dtype=Dtype.any(),
            docs="Output shape",
            default=None,
        )
        replace_pin = DataInputPin(
            name=PinName("replace"),
            dtype=Dtype.any(),
            docs="Whether the sample is with or without replacement",
            default=True,
        )
        p_pin = DataInputPin(
            name=PinName("p"),
            dtype=Dtype.any(),
            docs="Probabilities associated with each entry",
            default=None,
        )
        super().__init__("choice", a_pin, size_pin, replace_pin, p_pin)

    def apply_function(self, a, size, replace, p, **kwargs) -> Any:
        return np.random.choice(a, size=size, replace=replace, p=p)


class RandomShuffleNode(NumpyFunctionNode):
    """Modify a sequence in-place by shuffling its contents."""

    def __init__(self):
        x_pin = DataInputPin(
            name=PinName("x"),
            dtype=Dtype.any(),
            docs="The array or list to be shuffled",
        )
        super().__init__("shuffle", x_pin)

    def apply_function(self, x, **kwargs) -> Any:
        x_copy = x.copy() if hasattr(x, 'copy') else list(x)
        np.random.shuffle(x_copy)
        return x_copy


class RandomPermutationNode(NumpyFunctionNode):
    """Randomly permute a sequence, or return a permuted range."""

    def __init__(self):
        x_pin = DataInputPin(
            name=PinName("x"),
            dtype=Dtype.any(),
            docs="Array-like or int",
        )
        super().__init__("permutation", x_pin)

    def apply_function(self, x, **kwargs) -> Any:
        return np.random.permutation(x)


class RandomSeedNode(NumpyFunctionNode):
    """Seed the generator."""

    def __init__(self):
        seed_pin = DataInputPin(
            name=PinName("seed"),
            dtype=Dtype.any(),
            docs="Seed for random number generator",
            default=None,
        )
        super().__init__("seed", seed_pin)

    def apply_function(self, seed, **kwargs) -> Any:
        np.random.seed(seed)
        return None


class RandomNormalNode(NumpyFunctionNode):
    """Draw random samples from a normal (Gaussian) distribution."""

    def __init__(self):
        loc_pin = DataInputPin(
            name=PinName("loc"),
            dtype=Dtype.any(),
            docs="Mean of the distribution",
            default=0.0,
        )
        scale_pin = DataInputPin(
            name=PinName("scale"),
            dtype=Dtype.any(),
            docs="Standard deviation of the distribution",
            default=1.0,
        )
        size_pin = DataInputPin(
            name=PinName("size"),
            dtype=Dtype.any(),
            docs="Output shape",
            default=None,
        )
        super().__init__("normal", loc_pin, scale_pin, size_pin)

    def apply_function(self, loc, scale, size, **kwargs) -> Any:
        return np.random.normal(loc=loc, scale=scale, size=size)


class RandomUniformNode(NumpyFunctionNode):
    """Draw samples from a uniform distribution."""

    def __init__(self):
        low_pin = DataInputPin(
            name=PinName("low"),
            dtype=Dtype.any(),
            docs="Lower boundary of the output interval",
            default=0.0,
        )
        high_pin = DataInputPin(
            name=PinName("high"),
            dtype=Dtype.any(),
            docs="Upper boundary of the output interval",
            default=1.0,
        )
        size_pin = DataInputPin(
            name=PinName("size"),
            dtype=Dtype.any(),
            docs="Output shape",
            default=None,
        )
        super().__init__("uniform", low_pin, high_pin, size_pin)

    def apply_function(self, low, high, size, **kwargs) -> Any:
        return np.random.uniform(low=low, high=high, size=size)


class RandomBinomialNode(NumpyFunctionNode):
    """Draw samples from a binomial distribution."""

    def __init__(self):
        n_pin = DataInputPin(
            name=PinName("n"),
            dtype=Dtype.any(),
            docs="Number of trials",
        )
        p_pin = DataInputPin(
            name=PinName("p"),
            dtype=Dtype.any(),
            docs="Probability of success",
        )
        size_pin = DataInputPin(
            name=PinName("size"),
            dtype=Dtype.any(),
            docs="Output shape",
            default=None,
        )
        super().__init__("binomial", n_pin, p_pin, size_pin)

    def apply_function(self, n, p, size, **kwargs) -> Any:
        return np.random.binomial(n=n, p=p, size=size)


class RandomPoissonNode(NumpyFunctionNode):
    """Draw samples from a Poisson distribution."""

    def __init__(self):
        lam_pin = DataInputPin(
            name=PinName("lam"),
            dtype=Dtype.any(),
            docs="Expected number of events occurring in a fixed-time interval",
            default=1.0,
        )
        size_pin = DataInputPin(
            name=PinName("size"),
            dtype=Dtype.any(),
            docs="Output shape",
            default=None,
        )
        super().__init__("poisson", lam_pin, size_pin)

    def apply_function(self, lam, size, **kwargs) -> Any:
        return np.random.poisson(lam=lam, size=size)


class RandomExponentialNode(NumpyFunctionNode):
    """Draw samples from an exponential distribution."""

    def __init__(self):
        scale_pin = DataInputPin(
            name=PinName("scale"),
            dtype=Dtype.any(),
            docs="Scale parameter (inverse of the rate parameter lambda)",
            default=1.0,
        )
        size_pin = DataInputPin(
            name=PinName("size"),
            dtype=Dtype.any(),
            docs="Output shape",
            default=None,
        )
        super().__init__("exponential", scale_pin, size_pin)

    def apply_function(self, scale, size, **kwargs) -> Any:
        return np.random.exponential(scale=scale, size=size)


class RandomGammaNode(NumpyFunctionNode):
    """Draw samples from a Gamma distribution."""

    def __init__(self):
        shape_pin = DataInputPin(
            name=PinName("shape"),
            dtype=Dtype.any(),
            docs="Parameter of the distribution",
        )
        scale_pin = DataInputPin(
            name=PinName("scale"),
            dtype=Dtype.any(),
            docs="Scale parameter of the distribution",
            default=1.0,
        )
        size_pin = DataInputPin(
            name=PinName("size"),
            dtype=Dtype.any(),
            docs="Output shape",
            default=None,
        )
        super().__init__("gamma", shape_pin, scale_pin, size_pin)

    def apply_function(self, shape, scale, size, **kwargs) -> Any:
        return np.random.gamma(shape=shape, scale=scale, size=size)


class RandomBetaNode(NumpyFunctionNode):
    """Draw samples from a Beta distribution."""

    def __init__(self):
        a_pin = DataInputPin(
            name=PinName("a"),
            dtype=Dtype.any(),
            docs="Alpha parameter",
        )
        b_pin = DataInputPin(
            name=PinName("b"),
            dtype=Dtype.any(),
            docs="Beta parameter",
        )
        size_pin = DataInputPin(
            name=PinName("size"),
            dtype=Dtype.any(),
            docs="Output shape",
            default=None,
        )
        super().__init__("beta", a_pin, b_pin, size_pin)

    def apply_function(self, a, b, size, **kwargs) -> Any:
        return np.random.beta(a=a, b=b, size=size)


class RandomChisquareNode(NumpyFunctionNode):
    """Draw samples from a chi-square distribution."""

    def __init__(self):
        df_pin = DataInputPin(
            name=PinName("df"),
            dtype=Dtype.any(),
            docs="Number of degrees of freedom",
        )
        size_pin = DataInputPin(
            name=PinName("size"),
            dtype=Dtype.any(),
            docs="Output shape",
            default=None,
        )
        super().__init__("chisquare", df_pin, size_pin)

    def apply_function(self, df, size, **kwargs) -> Any:
        return np.random.chisquare(df=df, size=size)


class RandomMultivariateNormalNode(NumpyFunctionNode):
    """Draw random samples from a multivariate normal distribution."""

    def __init__(self):
        mean_pin = DataInputPin(
            name=PinName("mean"),
            dtype=Dtype.any(),
            docs="Mean of the N-dimensional distribution",
        )
        cov_pin = DataInputPin(
            name=PinName("cov"),
            dtype=Dtype.any(),
            docs="Covariance matrix of the distribution",
        )
        size_pin = DataInputPin(
            name=PinName("size"),
            dtype=Dtype.any(),
            docs="Given shape",
            default=None,
        )
        super().__init__("multivariate_normal", mean_pin, cov_pin, size_pin)

    def apply_function(self, mean, cov, size, **kwargs) -> Any:
        return np.random.multivariate_normal(mean=mean, cov=cov, size=size)


def get_random_nodes() -> List[Node]:
    """Get all random nodes."""
    return [
        # Basic random functions
        RandomRandNode(),
        RandomRandnNode(),
        RandomRandintNode(),
        RandomRandomNode(),

        # Choice and permutation
        RandomChoiceNode(),
        RandomShuffleNode(),
        RandomPermutationNode(),
        RandomSeedNode(),

        # Continuous distributions
        RandomNormalNode(),
        RandomUniformNode(),
        RandomExponentialNode(),
        RandomGammaNode(),
        RandomBetaNode(),
        RandomChisquareNode(),
        RandomMultivariateNormalNode(),

        # Discrete distributions
        RandomBinomialNode(),
        RandomPoissonNode(),
    ]