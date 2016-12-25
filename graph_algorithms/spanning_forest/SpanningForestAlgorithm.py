from math import log2, ceil

from graph_algorithms.tools.DSU import DSU
from graph_representation.GraphSketch import GraphSketch
from graph_representation.tools import index_to_edge
from l0_sampler.fast.L0Sampler import L0Sampler


class SpanningForestAlgorithm:
    """
        Spanning forest solver.

        Space Complexity:
            O(n*log(n)**5)
    """

    def __init__(self, n):
        """

        :param n:   Size of graph.
        :type n:    int
        """

        self.n = n
        self.t = ceil(log2(log2(n)))
        self.graph_sketches = tuple(GraphSketch(n) for i in range(self.t))

    def add_edge(self, edge):
        """

        :param edge:   Edge to add.
        :type edge:    Edge
        :return:
        :rtype:
        """

        for graph_sketch in self.graph_sketches:
            graph_sketch.add_edge(edge)

    def add_edges(self, edges):
        """

        :param edges:   Edges to add.
        :type edges:    list
        :return:
        :rtype:
        """

        for edge in edges:
            self.add_edge(edge)

    def remove_edge(self, edge):
        """

        :param edge:   Edges to remove.
        :type edge:    list
        :return:
        :rtype:
        """

        for graph_sketch in self.graph_sketches:
            graph_sketch.remove_edge(edge)

    def remove_edges(self, edges):
        """

        :param edges:   Edge to remove.
        :type edges:    list
        :return:
        :rtype:
        """

        for edge in edges:
            self.remove_edge(edge)

    def get_sp_forest_edges(self):
        """
            Returns edges of spanning forest of the graph.

        Time Complexity:
            O(n*log(n)**4)

        :return:    Edges of the spanning forest.
        :rtype:     list
        """

        dsu = DSU(self.n)

        sampled_edges = []

        not_sampled_any_edge_in_a_row = 0
        for r in range(self.t):

            if len(dsu.leaders) == 1:
                break

            sampled_any_edge = False

            for old_leader in list(dsu.leaders):

                leader = dsu.find_leader(old_leader)

                summing_row = L0Sampler(self.n*(self.n - 1) >> 1, self.graph_sketches[r].a[0].delta,
                                        self.graph_sketches[r].a[0].init_seed)

                for member in dsu.members[leader]:
                    summing_row.add(self.graph_sketches[r].a[member])

                sample = summing_row.get_sample()
                if sample is not None:
                    sampled_edge = index_to_edge(sample[0], self.n)
                    if 0 <= sampled_edge.u < self.n and \
                       0 <= sampled_edge.v < self.n:
                        sampled_edges.append(sampled_edge)

                        dsu.unite(leader, sampled_edge.u)
                        dsu.unite(leader, sampled_edge.v)

                        sampled_any_edge = True

            if sampled_any_edge:
                not_sampled_any_edge_in_a_row = 0
            else:
                not_sampled_any_edge_in_a_row += 1
                if not_sampled_any_edge_in_a_row == 2:
                    break

        return sampled_edges

    def count_cc(self):
        """
            Returns number of connected components
            in the graph.

        Time Complexity:
            O(n*log(n)**4)

        :return:    Number of connected components.
        :rtype:     int
        """

        dsu = DSU(self.n)

        result = self.n

        not_sampled_any_edge_in_a_row = 0
        for r in range(self.t):

            if len(dsu.leaders) == 1:
                # print('done. in', r, 'out of', self.t)
                break

            sampled_any_edge = False

            for old_leader in list(dsu.leaders):

                leader = dsu.find_leader(old_leader)

                summing_row = L0Sampler(self.n * (self.n - 1) >> 1, self.graph_sketches[r].a[0].delta,
                                        self.graph_sketches[r].a[0].init_seed)

                for member in dsu.members[leader]:
                    summing_row.add(self.graph_sketches[r].a[member])

                sample = summing_row.get_sample()
                if sample is not None:
                    sampled_edge = index_to_edge(sample[0], self.n)
                    if 0 <= sampled_edge.u < self.n and \
                       0 <= sampled_edge.v < self.n:
                        result -= 1

                        dsu.unite(leader, sampled_edge.u)
                        dsu.unite(leader, sampled_edge.v)

                        sampled_any_edge = True

            if sampled_any_edge:
                not_sampled_any_edge_in_a_row = 0
            else:
                not_sampled_any_edge_in_a_row += 1
                if not_sampled_any_edge_in_a_row == 2:
                    # print('done in', r, 'out of', self.t)
                    break

        return result
