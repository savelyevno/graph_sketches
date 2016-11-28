from graph_algorithms.tools.DSU import DSU
from graph_representation.tools import WEdge


class OrdinaryMSTAlgorithm:
    def __init__(self, n):
        """

        :param n:
        :type n:
        """

        self.n = n
        self.dsu = DSU(self. n)

        self.g = tuple(set() for i in range(self.n))

        self.weight = 0

    def add_edge(self, edge):
        """

        :param edge:
        :type edge:
        :return:
        :rtype:
        """

        if self.dsu.find_leader(edge.u) != self.dsu.find_leader(edge.v):
            self.g[edge.u].add(edge)
            self.g[edge.v].add(WEdge(edge.v, edge.u, edge.w))
            self.dsu.unite(edge.u, edge.v)
            self.weight += edge.w
        else:
            self._get_path(edge.u, edge.v)

            max_edge = WEdge(-1, -1, 0)
            for e in self.path:
                if e.w > max_edge.w:
                    max_edge = e

            if max_edge.w > edge.w:
                self.g[max_edge.u].remove(max_edge)
                self.g[max_edge.v].remove(WEdge(max_edge.v, max_edge.u, max_edge.w))
                self.weight -= max_edge.w

                self.g[edge.u].add(edge)
                self.g[edge.v].add(WEdge(edge.v, edge.u, edge.w))
                self.dsu.unite(edge.u, edge.v)
                self.weight += edge.w

    def add_edges(self, edges):
        """

        :param edges:
        :type edges:
        :return:
        :rtype:
        """

        for edge in edges:
            self.add_edge(edge)

    def _get_path(self, u, v):
        path = []
        used = [False]*self.n

        def dfs(u0, v0):
            used[u0] = True

            if u0 == v0:
                return True

            for e in self.g[u0]:
                if not used[e.v]:
                    if dfs(e.v, v0):
                        path.append(e)
                        return True

            return False

        self.path = path

        dfs(u, v)

    def get_weight(self):
        """

        :return:
        :rtype:
        """

        return self.weight
