import numpy as np


class DSU:
    """
        Disjoint set union data structure.
    """
    def __init__(self, n):
        """

        :param n:   Number of elements.
        :type n:    int
        """

        self.n = n

        self.parent = [i for i in range(n)]
        self.members = [[i] for i in range(n)]
        self.leaders = {i for i in range(n)}

    def find_leader(self, u):
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
            self.parent[u] = self.find_leader(self.parent[u])

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

        u = self.find_leader(u)
        v = self.find_leader(v)

        if u != v:
            if len(self.members[u]) < len(self.members[v]):
                u, v = v, u

            while len(self.members[v]) > 0:
                w = self.members[v].pop()

                self.parent[w] = u
                self.members[u].append(w)

            self.leaders.remove(v)
