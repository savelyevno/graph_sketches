from random import randint

from l0_sampler.L0Sampler import L0Sampler
from tools.validation import check_type, check_in_range
from graph.tools import Edge, edge_to_index, index_to_edge


class GraphSketch:
    """
        Graph sketch.
        Stores table a of n rows of l0-samplers for vectors
        of length n * (n - 1) / 2. Each column corresponds to
        edge (j, k).

        a_i,(j, k) = 1, if i = j and edge (j, k) present,
        a_i,(j, k) = -1, if i = k and edge (j, k) present,
        a_i,(j, k) = 0, otherwise.

        Space Complexity:
            O(n*log(n)**4)

        References
            https://people.cs.umass.edu/~mcgregor/papers/12-dynamic.pdf
    """

    def __init__(self, n):
        """
            Initializes l0-sampler for every vertex with the same
            random parameters to be able to combine them.

        Time Complexity
            O(n*log(n)**7)

        :param n:   Maximal size of a graph.
        :type n:    int
        """

        self.n = n

        self.init_seed = randint(0, 2147483647)
        self.a = tuple(L0Sampler(n*(n - 1) >> 1, self.init_seed) for i in range(n))

    def add_edge(self, e):
        """
               Adds edge.

        Time Complexity
            O(log(n)**3)

        :param e:   Edge to add.
        :type e:    Edge
        :return:
        :rtype:
        """

        if e.u < e.v:
            self.a[e.u].update(edge_to_index(e, self.n), 1)
            self.a[e.v].update(edge_to_index(e, self.n), -1)
        else:
            self.a[e.u].update(edge_to_index(e, self.n), -1)
            self.a[e.v].update(edge_to_index(e, self.n), 1)

    def add_edges(self, edges):
        """
            Adds edges.

        Time Complexity
            O(log(n)**3) for every edge

        :param edges:    Edge or list of edges to add.
        :type edges:     list
        :return:
        :rtype:
        """

        for e in edges:
            self.add_edge(e)

    def remove_edge(self, e):
        """
            Removes edge.

        Time Complexity
            O(log(n)**3)

        :param e:    Edge to remove
        :type e:     Edge
        :return:
        :rtype:
        """

        if e.u < e.v:
            self.a[e.u].update(edge_to_index(e, self.n), -1)
            self.a[e.v].update(edge_to_index(e, self.n), 1)
        else:
            self.a[e.u].update(edge_to_index(e, self.n), 1)
            self.a[e.v].update(edge_to_index(e, self.n), -1)

    def remove_edges(self, edges):
        """
            Removes edges.

        Time Complexity
            O(log(n)**3) for every removed edge.

        :param edges:    List of edges to remove.
        :type edges:     list
        :return:
        :rtype:
        """

        for e in edges:
            self.remove_edge(e)

    def sample_edge(self, u):
        """
            Samples random neighbour of vertex u.

        Time Complexity
            O(log(n)**4)

        :param u:   Vertex which neighbour we need to sample.
        :type u:    int
        :return:    Index of neighbour or None
        :rtype:     Edge or None
        """

        check_type(u, int)
        check_in_range(0, self.n - 1, u)

        sample = self.a[u].get_sample()
        if sample is None:
            return None
        return index_to_edge(sample[0], self.n)

    def add(self, another_graph_sketch):
        """
            Adds two sketches together.

        Time Complexity
            O(n*log(n)**3)

        :param another_graph_sketch:    Sketch of another graph.
        :type another_graph_sketch:     GraphSketch
        :return:
        :rtype:
        """

        if self.n != another_graph_sketch.n or\
           self.init_seed != another_graph_sketch.init_seed:
            raise ValueError('graph sketches are not compatible')

        for i in range(self.n):
            self.a[i].add(another_graph_sketch.a[i])

    def add_row(self, i, j):
        """
            Adds two graph sketch rows together.

        Time Complexity
            O(log(n)**3)

        :param i:
        :type i:
        :param j:
        :type j:
        :return:
        :rtype:
        """

        if self.a[i].n != self.a[j].n or\
           self.a[i].init_seed != self.a[j].init_seed:
            raise ValueError('graph sketch rows are not compatible')

        self.a[i].add(self.a[j])

    def subtract_row(self, i, j):
        """
            Subtracts one row from another.

        Time Complexity
            O(log(n)**3)

        :param i:
        :type i:
        :param j:
        :type j:
        :return:
        :rtype:
        """

        if self.a[i].n != self.a[j].n or\
           self.a[i].init_seed != self.a[j].init_seed:
            raise ValueError('graph sketch rows are not compatible')

        self.a[i].subtract(self.a[j])
