from tools.primality_test import prime_getter
import random


def pick_k_ind_hash_function(n, w, k):
    """
        Picks random hash function h:{0, ..., n - 1}-->{0, ..., w - 1}
        from a family of k-independent hash functions.

    :param n:   Defines domain of resulting hash function.
    :type n:    int
    :param w:   Defines image of resulting hash function.
    :type w:    int
    :param k:   Degree of independence of hash function.
    :type k:    int
    :return:    Generated hash function.
    :rtype:     function

    Notes
        Firstly, finds smallest prime p >= n. Then constructs array of
        coefficients a from Z_p, where a[0] != 0. Let
        h(x) = a[0] + ... + a[k - 2] * x^(k - 2) + a[k - 1] * x^(k - 1) mod p mod w.

    Time complexity
        Constructed hash function's complexity is O(k * log(x)).

    References
        https://en.wikipedia.org/wiki/K-independent_hashing

    """

    p = prime_getter.get_next_prime(max(n, w))

    a = tuple(random.randint(i == k - 1, p - 1) for i in range(k))

    def h(x):
        res = 0
        pow_x = 1
        for i in range(k):
            res = (res + pow_x * a[i]) % p
            pow_x = (pow_x * x) % p
        return res % w

    return h


def run_hash_function(a, p, w, arg):
    """

    :param a:
    :type a:
    :param p:
    :type p:
    :param w:
    :type w:
    :param arg:
    :type arg:
    :return:
    :rtype:
    """

    res = 0
    pow_x = 1
    for i in range(len(a)):
        res = (res + pow_x * a[i]) % p
        pow_x = (pow_x * arg) % p
    return res % w


def hash_int(arg, arg_range, image_range, rnd_seed=-1, p=-1):
    if rnd_seed != -1:
        random.seed(rnd_seed)

    if p == -1:
        p = prime_getter.get_next_prime(max(arg_range, image_range))

    return (arg*random.randint(1, p - 1) + random.randint(0, p - 1)) % image_range


def hash_tuple(arg, arg_ranges, image_range, rnd_seed=-1):
    if rnd_seed != -1:
        random.seed(rnd_seed)

    p = prime_getter.get_next_prime(max(max(arg_ranges), image_range))
    P = prime_getter.get_next_prime(p)

    hash_int_rnd_seeds = [random.getrandbits(32) for i in range(len(arg))]

    res = 0
    for i in range(len(arg)):
        res = (((res
                 + hash_int(arg[i],
                            arg_ranges[i],
                            prime_getter.get_next_prime(arg_ranges[i]),
                            hash_int_rnd_seeds[i]
                            )
                 ) % P) * p) % P

    return res % image_range
