import random

from graph_algorithms.KEdgeConnectAlgorithm import KEdgeConnectAlgorithm
from tools.Timer import Timer
from tools.graph_generation import generate_graph

timer = Timer()


def test1(n, p, k):
    random.seed(0)
    E, g = generate_graph(n, p)

    timer.start()
    k_edge_connect_alg = KEdgeConnectAlgorithm(n, k)
    print('init time', timer.stop())

    timer.start()
    k_edge_connect_alg.add_edges(E)
    print('add time', timer.stop())

    timer.start()
    sp_forest = k_edge_connect_alg.solve(0)
    print('solve time', timer.stop())

    # print(E)
    # print(sp_forest)
    print(len(E))
    for sp in sp_forest:
        print(len(sp))


test1(200, 0.1, 10)