from math import log2, ceil

from graph_algorithms.spanning_forest.DSU import DSU
from graph_representation.GraphSketch import GraphSketch


class SpanningForestAlgorithm:
    """
        Spanning forest solver.

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

    def solve(self):
        """
            Returns sketch of spanning forest of some graph_representation
            presented as its t = O(log(n)) independent sketches.
    
        Time Complexity:
            O(n*log(n)**4)
    
        :return:    Edges of the spanning forest.
        :rtype:     list
        """
    
        dsu = DSU(self.n)
    
        sampled_edges = []
    
        not_sampled_any_edge_in_a_row = 0
        for r in range(self.t):
            sampled_any_edge = False
    
            for old_leader in list(dsu.leaders):
    
                leader = dsu.find_leader(old_leader)
    
                for member in dsu.members[leader]:
                    if leader != member:
                        self.graph_sketches[r].add_row(leader, member)
    
                sampled_edge = self.graph_sketches[r].sample_edge(leader)
    
                for member in dsu.members[leader]:
                    if leader != member:
                        self.graph_sketches[r].subtract_row(leader, member)
    
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
