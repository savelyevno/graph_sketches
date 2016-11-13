import numpy as np

from graph.GraphSketch import Edge
from tools.validation import check_type


class DSU:
    def __init__(self, n):
        """
            Disjoint set union data structure.

        :param n:   Number of elements.
        :type n:    int
        """

        self.n = n

        self.parent = np.arange(n)
        self.members = [[i] for i in range(n)]
        self.leaders = {i for i in range(n)}

    def find(self, u):
        """
            Finds leader of the set in which u is present.

        Time Complexity
            O(log(n))

        :param u:   Element
        :type u:    int
        :return:    Leader
        :rtype:     int
        """

        if u != self.parent[u]:
            self.parent[u] = self.find(self.parent[u])

        return self.parent[u]

    def unite(self, u, v):
        """
            Unites two sets.

        Time Complexity
            O(log(n))

        :param u:   Element of first set.
        :type u:    int
        :param v:   Element of second set.
        :type v:    int
        :return:
        :rtype:
        """

        u = self.find(u)
        v = self.find(v)

        if u != v:
            if len(self.members[u]) < len(self.members[v]):
                u, v = v, u

            while len(self.members[v]) > 0:
                w = self.members[v][len(self.members[v]) - 1]
                self.members[v].pop()

                self.parent[w] = u
                self.members[u].append(w)

            self.leaders.remove(v)
