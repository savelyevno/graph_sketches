import random
from math import log, log2, ceil

from tools.hash_function import pick_k_ind_hash_function, run_hash_function
from tools.primality_test import prime_getter


class L0Sampler:
    """
        l0-sampler data structure.

        Contains sketched info about integer-valued vector a
        of length n allowing to make linear updates to a and
        get l0-samples from it.

        For info on how this works see References.

        Space Complexity
            O(s * log(s / delta) * log(n)**2), where eps and delta such that
            l0-sampler success probability is at least 1 - delta, output
            distribution is in range
            [(1 - eps)/l0_norm(a) - delta, (1 + eps)/l0_norm(a) + delta].

            We take s = O(log(1 / eps) + log(1 / delta)),
                eps = delta = poly(1/n).
            Thus space complexity is O(log(n)**4).

    References:
            Cormode, Graham, and Donatella Firmani. "On unifying the space of l0-sampling algorithms."
            https://pdfs.semanticscholar.org/b0f3/336c82b8a9d9a70d7cf187eea3f6dbfd1cdf.pdf
    """
    def __init__(self, n, init_seed=None):
        """

        Time Complexity:
            O(log(n)**4)

        :param n:           Length of vector a.
        :type n:            int
        :param init_seed:   Seed for random generator to initialize data structure, optional

                            This is needed for adding sketches together. We can add sketches S1 and S2
                            only if for each level l of S1 and S2, s-sparse recoverers that are stored there
                            have the same hash functions and 1-sparse recoverers that they consist of are
                            initialized with the same random parameters. This holds if we initialize S1 and S2
                            consequentially setting the seed for PRG.
        :type init_seed:    int
        """

        self.init_seed = init_seed
        if init_seed is not None:
            random.seed(init_seed)

        self.n = n
        self.levels = ceil(log2(n))

        k = 10
        self.eps = 1/k
        self.delta = 1/k

        # for more accurate distribution among levels one may want to increase this value
        self.n_hash_power = 1

        # self.sparse_degree = int(ceil(log(1 / self.eps) + log(1 / self.delta)))
        self.sparse_degree = int(2*log(k))
        self.k = self.sparse_degree >> 1

        self.hash_function = pick_k_ind_hash_function(n, n ** self.n_hash_power, self.k)

        # self.recoverers = tuple(SparseRecoverer(n, self.sparse_degree, self.delta) for i in range(self.levels))
        self.recoverers_values = {}
        self.recoverers_rows = int(log(self.sparse_degree / self.delta))
        self.recoverers_columns = 2 * self.sparse_degree

        self.recoverers_hash_p_mod = prime_getter.get_next_prime(max(self.n, self.recoverers_columns))
        self.recoverers_hash_param_gen_hash_function_domain_base = max(self.levels, self.recoverers_rows)
        self.recoverers_hash_param1_gen_hash_function =\
            pick_k_ind_hash_function(self.recoverers_hash_param_gen_hash_function_domain_base**2,
                                     self.recoverers_hash_p_mod - 1, 2)
        self.recoverers_hash_param2_gen_hash_function = \
            pick_k_ind_hash_function(self.recoverers_hash_param_gen_hash_function_domain_base ** 2,
                                     self.recoverers_hash_p_mod, 2)
        self.recoverers_hash_functions_params = {}

        self.one_sp_rec_p = prime_getter.get_next_prime(n*100)
        self.one_sp_rec_gen_z_hash_function_domain_base = max(self.levels, self.recoverers_rows, self.recoverers_columns)
        self.one_sp_rec_gen_z_hash_function =\
            pick_k_ind_hash_function(self.one_sp_rec_gen_z_hash_function_domain_base**3, self.one_sp_rec_p - 1, 2)

    def recoverer_get_hash_params(self, level, row):
        return (
            self.recoverers_hash_param1_gen_hash_function(
                level*self.recoverers_hash_param_gen_hash_function_domain_base + row) + 1,
            self.recoverers_hash_param2_gen_hash_function(
                level*self.recoverers_hash_param_gen_hash_function_domain_base + row)
        )

    def one_sp_rec_get_z(self, level, row, column):
        return self.one_sp_rec_gen_z_hash_function(
            level*self.one_sp_rec_gen_z_hash_function_domain_base**2
            + row*self.one_sp_rec_gen_z_hash_function_domain_base
            + column
        ) + 1
        
    def update(self, i, Delta):
        """
            Update of type a_i += Delta.

            Time Complexity
                O(log(n)**3)

        :param i:       Index of update.
        :type i:        int
        :param Delta:   Value of update.
        :type Delta:    int
        :return: 
        :rtype:         None
        """

        hash_value = self.hash_function(i)
        n_copy = self.n ** self.n_hash_power
        max_l = 0
        while n_copy > hash_value:
            max_l += 1
            n_copy >>= 1

        for level in range(max_l):
            for row in range(self.recoverers_rows):
                if (level, row) not in self.recoverers_hash_functions_params:
                    self.recoverers_hash_functions_params[(level, row)] = self.recoverer_get_hash_params(level, row)
                column = run_hash_function\
                    (
                        self.recoverers_hash_functions_params[(level, row)],
                        self.recoverers_hash_p_mod,
                        self.recoverers_columns,
                        i
                    )

                if (level, row, column) not in self.recoverers_values:
                    self.recoverers_values[(level, row, column)] = [self.one_sp_rec_get_z(level, row, column), 0, 0, 0]

                recoverer = self.recoverers_values[(level, row, column)]
                recoverer[1] += (i + 1) * Delta
                recoverer[2] += Delta
                recoverer[3] = (recoverer[3] + Delta * pow(recoverer[0], i + 1, self.one_sp_rec_p)) % self.one_sp_rec_p

    def get_sample(self):
        """
            Get l0-sample.

            Time Complexity
                O(log(n)**4)

        :return:    Return tuple (i, a_i) or FAIL.
        :rtype:     None or (int, int)
        """

        result = {}

        for level in range(self.levels):
            recover_result = {}

            for row in range(self.recoverers_rows):
                if (level, row) not in self.recoverers_hash_functions_params:
                    continue
                for column in range(self.recoverers_columns):
                    if (level, row, column) not in self.recoverers_values:
                        continue

                    recoverer = self.recoverers_values[(level, row, column)]

                    z = recoverer[0]
                    iota = recoverer[1]
                    fi = recoverer[2]
                    tau = recoverer[3]

                    if fi != 0 and iota % fi == 0 and iota // fi > 0 and \
                            tau == fi * pow(z, iota // fi, self.one_sp_rec_p) % self.one_sp_rec_p:
                        recover_result[iota // fi - 1] = fi
                        # return iota // fi - 1, fi

            if len(recover_result) > 0:
                key = random.choice(list(recover_result.keys()))

                # return key, recover_result[key]

                result[key] = recover_result[key]

        if len(result) > 0:
            key = random.choice(list(result.keys()))
            return key, result[key]
        return None

    def _get_info(self):
        """

        :return:    Object info
        :rtype:     dict
        """
        result = {
            'l0-sampler levels': self.levels,
            'l0-sampler s': self.sparse_degree,
            'l0-sampler k': self.k
        }

        result = {**result, **self.recoverers[0]._get_info()}

        return result

    def add(self, another_l0_sampler):
        """
            Combines two l0-samplers by adding them.

            !Assuming they have the same hash functions. (This should hold
            if they were initialized with the same random bits)

        Time Complexity
            O(log(n)**3)

        :param another_l0_sampler:  l0-sampler to add.
        :type another_l0_sampler:   L0Sampler
        :return:
        :rtype:     None
        """

        if self.n != another_l0_sampler.n:
            raise ValueError('l0-samplers are not compatible')
        if self.init_seed is None or another_l0_sampler.init_seed is None or\
           self.init_seed != another_l0_sampler.init_seed:
            raise ValueError('samplers are not initialized from the same random bits')

        for level in range(self.levels):
            for row in range(self.recoverers_rows):
                for column in range(self.recoverers_columns):
                    if (level, row, column) not in self.recoverers_values or\
                       (level, row, column) not in another_l0_sampler.recoverers_values:
                        continue

                    recoverer = self.recoverers_values[(level, row, column)]
                    another_recoverer = another_l0_sampler.recoverers_values[(level, row, column)]

                    if recoverer[0] != another_recoverer[0]:
                        raise ValueError('1-sparse recoverers are not compatible')

                    recoverer[1] += another_recoverer[1]
                    recoverer[2] += another_recoverer[2]
                    recoverer[3] = (recoverer[3] + another_recoverer[3]) % self.one_sp_rec_p

    def subtract(self, another_l0_sampler):
        """
            Combines two l0-samplers by subtracting them.

            !Assuming they have the same hash functions. (This should hold
            if they were initialized with the same random bits)

        Time Complexity
            O(log(n)**3)

        :param another_l0_sampler:  l0-sampler to add.
        :type another_l0_sampler:   L0Sampler
        :return:
        :rtype:     None
        """

        if self.n != another_l0_sampler.n:
            raise ValueError('l0-samplers are not compatible')
        if self.init_seed is None or another_l0_sampler.init_seed is None or\
           self.init_seed != another_l0_sampler.init_seed:
            raise ValueError('samplers are not initialized from the same random bits')

        for level in range(self.levels):
            for row in range(self.recoverers_rows):
                for column in range(self.recoverers_columns):
                    if (level, row, column) not in self.recoverers_values or \
                                    (level, row, column) not in another_l0_sampler.recoverers_values:
                        continue

                    recoverer = self.recoverers_values[(level, row, column)]
                    another_recoverer = another_l0_sampler.recoverers_values[(level, row, column)]

                    if recoverer[0] != another_recoverer[0]:
                        raise ValueError('1-sparse recoverers are not compatible')

                    recoverer[1] -= another_recoverer[1]
                    recoverer[2] -= another_recoverer[2]
                    recoverer[3] = (recoverer[3] - another_recoverer[3]) % self.one_sp_rec_p
