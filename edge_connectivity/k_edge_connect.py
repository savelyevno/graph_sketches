from spanning_forest.span_forest import get_spanning_forest
from graph.GraphSketch import GraphSketch


def k_edge_connect(graph_sketches):
    """
        Given k instantiations of the spanning forest algorithm
        returns a sketch of the subgraph H of the given graph G
        such that H is k-edge-connected iff G is at least
        k-edge-connected.

    Time Complexity
        O(k*n*log(n)**4), assuming t = O(log(n))

    Space Complexity
        O(k*n*log(n)**5), assuming t = O(log(n))

    :param graph_sketches:  Matrix of independent graph sketches
                            with k rows and t columns. Every row
                            is required for independent run of
                            spanning forest algorithm.
    :type graph_sketches:   list
    :return:                Resulting graph sketch of H.
    :rtype:                 GraphSketch
    """

    k = len(graph_sketches)
    t = len(graph_sketches[0])

    n = graph_sketches[0][0].n
    result = GraphSketch(n)

    spanning_forest = []
    for i in range(k):
        spanning_forest.append(get_spanning_forest(graph_sketches[i]))

        for j in range(i + 1, k):
            for l in range(t):
                graph_sketches[j][l].remove_edges(spanning_forest[i])

        result.add_edges(spanning_forest[i])

        for j in range(0, i):
            for l in range(t):
                graph_sketches[i][l].add_edges(spanning_forest[j])

    return result, spanning_forest
