from math import ceil, log2

from graph_algorithms.KEdgeConnectAlgorithm import KEdgeConnectAlgorithm
from tools.hash_function import pick_k_ind_hash_function


class MinCutAlgorithm:
    """

    """

    def __init__(self, n, eps):
        """

        :param n:
        :type n:
        :param eps:
        :type eps:
        """

        self.n = n
        self.eps = eps

        self.levels = ceil(2*log2(n))
        self.hash_functions = tuple(pick_k_ind_hash_function(n*n, 2, 2) for i in range(self.levels))

        self.k = ceil(log2(n)/eps**2)

        self.k_edge_connect_instances = tuple(KEdgeConnectAlgorithm(self.n, self.k) for i in range(self.levels))

    def hash_edge(self, i, edge):
        """

        :param i:
        :type i:
        :param edge:
        :type edge:
        :return:
        :rtype:
        """

        return self.hash_functions[i](min(edge.u, edge.v) * self.n + max(edge.u, edge.v))

    def add_edge(self, edge):
        """

        :param edge:   Edge to add.
        :type edge:    Edge
        :return:
        :rtype:
        """

        self.k_edge_connect_instances[0].add_edge(edge)

        for i in range(1, self.levels):
            if self.hash_edge(i, edge) == 1:
                self.k_edge_connect_instances[i].add_edge(edge)
            else:
                break

    def add_edges(self, edges):
        """

        :param edges:   Edges to add.
        :type edges:    list
        :return:
        :rtype:
        """

        for edge in edges:
            self.add_edge(edge)

    def solve(self):
        """

        :return:
        :rtype:
        """

        result = self.n
        i = -1
        while i + 1 < self.levels and result >= self.k:
            i += 1
            result = self.k_edge_connect_instances[i].get_sp_forest_edges(2)

        return result << i
