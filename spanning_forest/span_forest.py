from spanning_forest.DSU import DSU


def get_spanning_forest(graph_sketches):
    """
        Returns sketch of spanning forest of some graph
        presented as its t = O(log(n)) independent sketches.

    Time Complexity:
        O(n*log(n)**4)

    Space Complexity:
        O(n*log(n)**5)

    :param graph_sketches:  List of sketches.
    :type graph_sketches:   []
    :return:                Edges of the spanning forest.
    :rtype:                 list
    """

    t = len(graph_sketches)
    n = graph_sketches[0].n

    dsu = DSU(n)

    sampled_edges = []

    not_sampled_any_edge_in_a_row = 0
    for r in range(t):
        sampled_any_edge = False

        for old_leader in list(dsu.leaders):

            leader = dsu.find_leader(old_leader)

            for member in dsu.members[leader]:
                if leader != member:
                    graph_sketches[r].add_row(leader, member)

            sampled_edge = graph_sketches[r].sample_edge(leader)

            for member in dsu.members[leader]:
                if leader != member:
                    graph_sketches[r].subtract_row(leader, member)

            if sampled_edge is not None:
                sampled_edges.append(sampled_edge)

                dsu.unite(leader, sampled_edge[0])
                dsu.unite(leader, sampled_edge[1])

                sampled_any_edge = True

        if not sampled_any_edge:
            not_sampled_any_edge_in_a_row += 1
        else:
            not_sampled_any_edge_in_a_row = 0
        if not_sampled_any_edge_in_a_row == 2:
            break

    return sampled_edges
