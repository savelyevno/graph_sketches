import random

from tools.graph_generation import generate_graph
from graph_algorithms.MinCutAlgorithm import MinCutAlgorithm
from tools.Timer import Timer

timer = Timer()


def test(n, p, eps):
    random.seed(0)

    E, g = generate_graph(n, p)

    timer.start()
    min_cut_alg = MinCutAlgorithm(n, eps)
    print('init time', timer.stop())

    timer.start()
    min_cut_alg.add_edges(E)
    print('add time', timer.stop())

    timer.start()
    min_cut_value = min_cut_alg.solve()
    print('solve time', timer.stop())

    print('min cut:', min_cut_value)


test(50, 0.5, 1)
