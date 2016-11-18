from graph_representation.GraphSketch import GraphSketch
from graph_algorithms.spanning_forest.SpanningForestAlgorithm import SpanningForestAlgorithm


class KEdgeConnectAlgorithm:
    """
        k-edge-connect solver.

    Space Complexity
        O(k*n*log(n)**5), assuming t = O(log(n))
    """

    def __init__(self, n, k):
        """

        :param n:
        :type n:
        :param k:
        :type k:
        """

        self.n = n
        self.k = k

        self.span_forest_instances = tuple(SpanningForestAlgorithm(self.n) for i in range(k))

    def add_edge(self, edge):
        """

        :param edge:   Edge to add.
        :type edge:    Edge
        :return:
        :rtype:
        """

        for span_forest in self.span_forest_instances:
            span_forest.add_edge(edge)

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

        for span_forest in self.span_forest_instances:
            span_forest.remove_edge(edge)

    def solve(self, return_type=0):
        """
            Returns the subgraph H of the given graph G
            such that H is k-edge-connected iff G is at least
            k-edge-connected.

        Time Complexity
            O(k*n*log(n)**4), assuming t = O(log(n))

        :param return_type:     if 0, returns edges of the spanning forest,
                                   1, returns graph sketch, containing found
                                      spanning forest,
                                   2, returns number of full spanning trees
                                      (which is equal to min-cut)
        :type return_type:      int
        :return:                list of spanning forests or
                                graph sketch of spanning forest or
                                number of full spanning trees

        :rtype:                 list or GraphSketch or int
        """

        spanning_forest_array = []

        for i in range(self.k):
            spanning_forest_array.append(self.span_forest_instances[i].solve())

            for j in range(i + 1, self.k):
                self.span_forest_instances[j].remove_edges(spanning_forest_array[i])

            for j in range(0, i):
                self.span_forest_instances[i].add_edges(spanning_forest_array[j])

        if return_type == 0:
            return spanning_forest_array
        elif return_type == 1:
            result_sketch = GraphSketch(self.n)

            for spanning_forest in spanning_forest_array:
                result_sketch.add_edges(spanning_forest)

            return result_sketch
        else:
            count = 0

            for i in range(self.k):
                if len(spanning_forest_array[i]) == self.n - 1:
                    count += 1
                else:
                    break

            return count
