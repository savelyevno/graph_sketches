from math import log, ceil


from graph_algorithms.spanning_forest.SpanningForestAlgorithm import SpanningForestAlgorithm
from graph_representation.tools import Edge, WEdge


class ApproximateMSTAlgorithm:
    def __init__(self, n, eps, W=1000):
        """

        :param n:
        :type n:
        :param eps:
        :type eps:
        :param W:
        :type W:
        """

        self.n = n
        self.eps = eps
        self.W = W

        self.r = ceil(log(W, 1 + eps)) + 1

        self.w = tuple((1 + self.eps)**i for i in range(self.r))
        self.lam = tuple((1 + self.eps)**(i + 1) - (1 + self.eps)**i for i in range(self.r))

        self.span_forest_instances = tuple(SpanningForestAlgorithm(n) for i in range(self.r))

    def add_edge(self, edge):
        """

        :param edge:   Edge to add.
        :type edge:    WEdge
        :return:
        :rtype:
        """

        for i in range(self.r):
            if edge.w > self.w[i]:
                continue

            self.span_forest_instances[i].add_edge(Edge(edge.u, edge.v))

    def add_edges(self, edges):
        """

        :param edges:   Edges to add.
        :type edges:    Edge
        :return:
        :rtype:
        """

        for edge in edges:
            self.add_edge(edge)

    def remove_edge(self, edge):
        """

        :param edge:   Edge to remove.
        :type edge:    Edge
        :return:
        :rtype:
        """

        for i in range(self.r):
            if edge.w > self.w[i]:
                break

            self.span_forest_instances[i].remove_edge(Edge(edge.u, edge.v))

    def get_weight(self):
        """

        :return:
        :rtype:
        """

        # cc = [self.span_forest_instances[i].count_cc() for i in range(self.r)]
        #
        # result = self.n - cc[0]
        #
        # for i in range(1, self.r):
        #     result += self.w[i]*(cc[i - 1] - cc[i])

        result = self.n

        for i in range(self.r - 1):
            result += self.span_forest_instances[i].count_cc()*self.lam[i]

        result -= self.span_forest_instances[-1].count_cc()*self.w[-1]

        return result
