import random
from math import log2, ceil

from graph_representation.GraphSketch import GraphSketch
from graph_representation.tools import Edge
from graph_algorithms.spanning_forest.SpanningForestAlgorithm import SpanningForestAlgorithm
from tools.Timer import Timer
from tools.graph_generation import build_g, count_cc, generate_graph

timer = Timer()


def test1():
    E = []
    with open('input.txt', 'r') as f:
        lines = [line.split() for line in f.readlines()]
        n = int(lines[0][0])
        m = int(lines[0][1])

        for i in range(m):
            E.append(Edge(int(lines[i + 1][0]), int(lines[i + 1][1])))

    timer.start()

    sp_forest_alg = SpanningForestAlgorithm(n)
    sp_forest_alg.add_edges(E)

    print('total build time', timer.stop())
    timer.start()

    span_for = sp_forest_alg.solve()

    g = build_g(E, n)
    cc = count_cc(g, n)

    print(cc)
    print(len(span_for) == n - cc)
    print('solving time', timer.stop())


def test2(p, n, print_log=False):

    timer.start()

    E, g = generate_graph(n, p)

    # print('gen time', timer.stop())

    # print('edges: ', len(E), E)

    timer.start()
    sp_forest_alg = SpanningForestAlgorithm(n)
    # print('total build time', timer.stop())

    timer.start()
    sp_forest_alg.add_edges(E)
    # print('edges add time', timer.stop())

    timer.start()
    span_size = len(sp_forest_alg.solve())

    cc = count_cc(g, n)

    if print_log:
        # print(cc)
        # print(span_size)
        print(span_size == n - cc)
    # print('solving time', timer.stop())

    return span_size == n - cc


def test3(n):
    random.seed(0)

    T = 1000
    for test in range(0, T):

        timer.start()
        result = test2(0.5, n, False)
        if not result:
            print(test, 'Fail', timer.stop())
        else:
            print(test, 'Ok', timer.stop())
        print('__________________________________________________________')


def test4(n):
    random.seed(0)

    t = int(ceil(log2(n)))

    timer.start()
    sp_forest_alg = SpanningForestAlgorithm(n)
    print('init time:', timer.stop())

    p = 0.9

    E = set()
    g = build_g([], n)

    random.seed(0)
    while True:
        changed = False
        if random.random() < p:
            i = random.randint(0, n - 1)
            j = random.randint(0, n - 1)
            while j == i:
                j = random.randint(0, n - 1)
            e = Edge(min(i, j), max(i, j))

            if e not in E:
                changed = True
                E.add(e)
                g[e.u].add(e.v)
                g[e.v].add(e.u)

                timer.start()
                for i in range(t):
                    sp_forest_alg.add_edge(e)
                # print('add edge time', timer.stop())

                # print('added edge', e)
        elif len(E) > 0:
            changed = True
            e = random.sample(E, 1)[0]

            E.remove(e)
            g[e.u].remove(e.v)
            g[e.v].remove(e.u)

            timer.start()
            for i in range(t):
                sp_forest_alg.remove_edge(e)
            # print('rem edge time', timer.stop())

            # print('removed edge', e)

        if changed and random.randint(0, 20) == 0:
            timer.start()
            cc = count_cc(g, n)
            # print('naive cc count time', timer.stop())

            timer.start()
            span_size = len(sp_forest_alg.solve())
            print('build span tree time', timer.stop())

            if span_size != n - cc:
                print('Fail')
            else:
                print('Ok')
            print('edges count:', len(E))
            print('________________________________________________')


def test5(n):

    timer.start()

    sketch = GraphSketch(n)

    print(timer.stop())

    timer.start()
    sketch.sample_edge(0)
    print(timer.stop())


# test1()
test3(50)
