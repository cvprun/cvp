# -*- coding: utf-8 -*-

from typing import List

from cvp.nodes.node import Node

from .random_beta_node import RandomBetaNode
from .random_binomial_node import RandomBinomialNode
from .random_chisquare_node import RandomChisquareNode
from .random_choice_node import RandomChoiceNode
from .random_exponential_node import RandomExponentialNode
from .random_gamma_node import RandomGammaNode
from .random_multivariate_normal_node import RandomMultivariateNormalNode
from .random_normal_node import RandomNormalNode
from .random_permutation_node import RandomPermutationNode
from .random_poisson_node import RandomPoissonNode
from .random_rand_node import RandomRandNode
from .random_randint_node import RandomRandintNode
from .random_randn_node import RandomRandnNode
from .random_random_node import RandomRandomNode
from .random_seed_node import RandomSeedNode
from .random_shuffle_node import RandomShuffleNode
from .random_uniform_node import RandomUniformNode


def get_random_nodes() -> List[Node]:
    """Get all random nodes."""
    return [
        RandomRandNode(),
        RandomRandnNode(),
        RandomRandintNode(),
        RandomRandomNode(),
        RandomChoiceNode(),
        RandomShuffleNode(),
        RandomPermutationNode(),
        RandomSeedNode(),
        RandomNormalNode(),
        RandomUniformNode(),
        RandomBinomialNode(),
        RandomPoissonNode(),
        RandomExponentialNode(),
        RandomGammaNode(),
        RandomBetaNode(),
        RandomChisquareNode(),
        RandomMultivariateNormalNode(),
    ]
