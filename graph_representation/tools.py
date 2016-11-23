from collections import namedtuple
from functools import lru_cache

Edge = namedtuple('Edge', ['u', 'v'])


def edge_to_index(e, n):
    """
        Gets index of edge (u, v) in edge array.

    Time complexity:
        O(1)

    :param e:   Edge
    :type e:    Edge
    :param n:   Number of vertices in a graph.
    :type n:    int
    :return:    Index of edge e.
    :rtype:     int
    """

    if e.u > e.v:
        e = Edge(e.v, e.u)

    return e.u * (n - 1) - (e.u * (e.u + 1)) // 2 + e.v - 1


# @lru_cache()
def index_to_edge(i, n):
    """
        Gets edge (u, v) from index of its position in edge array.

    Time Complexity
        O(log(n))

    :param i:   Index of edge e.
    :type i:    int
    :param n:   Number of vertices in a graph.
    :type n:    int
    :return:    Edge
    :rtype:     Edge
    """

    if i + 1 < n:
        return Edge(0, i + 1)

    def f(u):
        return i // (n * u - ((u * (u + 1)) >> 1)) < 1

    u = binary_search(1, n, f)
    return Edge(u, i - (n * u - ((u * (u + 1)) >> 1) - u - 1))


def binary_search(l, r, f):
    while l < r:
        m = (l + r) >> 1

        if f(m):
            r = m
        else:
            l = m + 1

    if l == r:
        return l - 1
    else:
        return l
