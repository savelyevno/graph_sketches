from random import randint

from l0_sampler.L0Sampler import L0Sampler


class GraphSketch:
    """

    """

    def __init__(self, n):
        """

        :param n:
        :type n:
        """

        self.n = n

        init_seed = randint(0, (1 << 31) - 1)
        self.a = [L0Sampler(n*(n - 1)/2, init_seed) for i in range(n)]

