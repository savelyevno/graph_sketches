from math import log2, ceil

from graph_algorithms.tools.DSU import DSU
from graph_representation.GraphSketch import GraphSketch
from graph_representation.tools import WEdge


class ExactMSTAlgorithm:
    """
        Exact Minimum Spanning Tree solver.

        Space Complexity:
            O(n*log(n)**5)
    """

    def __init__(self, n):
        """

        :param n:   Size of graph.
        :type n:    int
        """

        self.n = n
        self.t = ceil(log2(n))
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

    def get_weight(self):
        """
            Returns weight of minimum spanning forest.

        Time Complexity:
            O(n*log(n)**4)

        :return:    Weight of minimum spanning forest.
        :rtype:     int
        """

        dsu = DSU(self.n)

        result = 0

        for r in range(self.t):
            if len(dsu.leaders) == 1:
                break

            edges_to_add = []
            used_leaders = set()

            for leader in list(dsu.leaders):

                if leader in used_leaders:
                    continue

                for member in dsu.members[leader]:
                    if leader != member:
                        self.graph_sketches[r].add_row(leader, member)

                sampled_edges = self.graph_sketches[r].sample_neighbouring_weighted_edges(leader)

                for member in dsu.members[leader]:
                    if leader != member:
                        self.graph_sketches[r].subtract_row(leader, member)

                min_edge = WEdge(-1, -1, 1e9)
                for edge in sampled_edges:
                    if 0 <= edge.u < self.n and \
                       0 <= edge.v < self.n and \
                       abs(edge.w) < min_edge.w:
                        min_edge = WEdge(edge.u, edge.v, abs(edge.w))

                if min_edge.u != -1:
                    edges_to_add.append(min_edge)
                    used_leaders.add(max(dsu.find_leader(min_edge.u), dsu.find_leader(min_edge.v)))

            for edge in edges_to_add:
                dsu.unite(edge.u, edge.v)
                result += edge.w

        return result
