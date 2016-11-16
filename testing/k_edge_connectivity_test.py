from math import log2, ceil
import random

from edge_connectivity.k_edge_connect import k_edge_connect
from tools.graph_generation import generate_graph
from tools.Timer import Timer
from graph.GraphSketch import GraphSketch


timer = Timer()


def test1(n, p, k):
    random.seed(0)
    E, g = generate_graph(n, p)

    timer.start()

    t = ceil(log2(n))
    sketches = []
    for i in range(k):
        sketches.append([])
        for j in range(t):
            sketch = GraphSketch(n)
            sketch.add_edges(E)
            sketches[i].append(sketch)

    print('init time', timer.stop())
    timer.start()

    sketch, sp_forest = k_edge_connect(sketches)

    print('solve time', timer.stop())

    # print(E)
    # print(sp_forest)
    print(len(E))
    for sp in sp_forest:
        print(len(sp))


test1(50, 0.2, 2)