from graph.GraphSketch import GraphSketch
from spanning_forest.DSU import DSU


def get_spanning_forest(n, graph_sketches):
    """
        Returns sketch of spanning forest of some graph
        presented as its t = O(log(n)) independent sketches.

    Time Complexity:
        O(n*log(n)**4)

    :param n:               Size of graph.
    :type n:                int
    :param graph_sketches:  List of sketches.
    :type graph_sketches:   []
    :return:                Sketch of resulting graph.
    :rtype:                 GraphSketch
    """

    t = len(graph_sketches)

    dsu = DSU(n)

    sampled_edges = []

    for r in range(t):
        for leader in dsu.leaders:
            for member in dsu.members[leader]:
                graph_sketches[r].add_row(leader, member)

            sampled_edge = graph_sketches[r].sample_edge(leader)
            if sampled_edge is not None:
                sampled_edges.append(sampled_edge)
                neighbour = graph_sketches[r].sample_edge(leader)
                dsu.unite(leader, neighbour)

    result = GraphSketch(n)
    for edge in sampled_edges:
        result.add_edge(edge)

    return result