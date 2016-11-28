import random
from math import log2, ceil

from graph_representation.GraphSketch import GraphSketch
from graph_representation.tools import Edge, WEdge
from graph_algorithms.spanning_forest.SpanningForestAlgorithm import SpanningForestAlgorithm
from tools.Timer import Timer
from tools.graph_generation import build_g, count_cc, generate_weighted_graph, generate_graph
from tools.primality_test import prime_getter
from graph_algorithms.MST.OrdinaryMSTAlgorithm import OrdinaryMSTAlgorithm
from graph_algorithms.MST.ApproximateMSTAlgorithm import ApproximateMSTAlgorithm
from graph_algorithms.MST.ExactMSTAlgorithm import ExactMSTAlgorithm

timer = Timer()


def test1_ord():
    E = []
    with open('input.txt', 'r') as f:
        lines = [line.split() for line in f.readlines()]
        n = int(lines[0][0])
        m = int(lines[0][1])

        for i in range(m):
            E.append(WEdge(int(lines[i + 1][0]) - 1, int(lines[i + 1][1]) - 1, int(lines[i + 1][2])))

    timer.start()

    mst_alg = OrdinaryMSTAlgorithm(n)
    mst_alg.add_edges(E)

    print('total build time', timer.stop())
    timer.start()

    weight = mst_alg.get_weight()

    print('weight', weight)
    print('solving time', timer.stop())


def test1_approx():
    E = []
    with open('input.txt', 'r') as f:
        lines = [line.split() for line in f.readlines()]
        n = int(lines[0][0])
        m = int(lines[0][1])

        for i in range(m):
            E.append(WEdge(int(lines[i + 1][0]) - 1, int(lines[i + 1][1]) - 1, int(lines[i + 1][2])))

    timer.start()

    mst_alg = ApproximateMSTAlgorithm(n, 1)
    mst_alg.add_edges(E)

    print('total build time', timer.stop())
    timer.start()

    weight = mst_alg.get_weight()

    print('weight', weight)
    print('solving time', timer.stop())


def test1_exact():
    E = []
    with open('input.txt', 'r') as f:
        lines = [line.split() for line in f.readlines()]
        n = int(lines[0][0])
        m = int(lines[0][1])

        for i in range(m):
            E.append(WEdge(int(lines[i + 1][0]) - 1, int(lines[i + 1][1]) - 1, int(lines[i + 1][2])))

    timer.start()

    mst_alg = ExactMSTAlgorithm(n)
    mst_alg.add_edges(E)

    print('total build time', timer.stop())
    timer.start()

    weight = mst_alg.get_weight()

    print('weight', weight)
    print('solving time', timer.stop())


def test2(p, n, eps, print_log=False):

    timer.start()

    def gen_w_f():
        return random.randint(1, 1000)

    E, g = generate_weighted_graph(n, p, gen_w_f)

    if print_log:
        print('gen time', timer.stop())

        print('edges: ', len(E))

        print()

    if print_log:
        timer.start()
    ord_mst_alg = OrdinaryMSTAlgorithm(n)
    if print_log:
        print('ordinary total build time', timer.stop())

    if print_log:
        timer.start()
    ord_mst_alg.add_edges(E)
    if print_log:
        print('ordinary edges add time', timer.stop())

        print()

    if print_log:
        timer.start()
    approx_mst_alg = ApproximateMSTAlgorithm(n, eps)
    if print_log:
        print('approximate total build time', timer.stop())

    if print_log:
        timer.start()
    approx_mst_alg.add_edges(E)

    if print_log:
        print('approximate edges add time', timer.stop())

        print()

    if print_log:
        timer.start()
    exact_mst_alg = ExactMSTAlgorithm(n)
    if print_log:
        print('exact total build time', timer.stop())

    if print_log:
        timer.start()
        exact_mst_alg.add_edges(E)

    if print_log:
        print('exact edges add time', timer.stop())

        print()

    w = ord_mst_alg.get_weight()

    if print_log:
        timer.start()
    approx_w = int(approx_mst_alg.get_weight())
    if print_log:
        print('approx solve', timer.stop())

        print()

    if print_log:
        timer.start()
    exact_w = exact_mst_alg.get_weight()
    if print_log:
        print('exact solve', timer.stop())

        print()

    if print_log:
        print('ord mst alg weight:', w)
        print('approx mst alg weight:', approx_w)
        print('exact mst alg weight:', exact_w)

        print()
    print('approx - ordinary:', approx_w - w, 'ratio:', (approx_w - w)/w)
    print('exact - ordinary:', exact_w - w)

    return (approx_w - w)/w


def test3(n):
    random.seed(0)

    T = 1
    avg = 0
    for test in range(0, T):

        timer.start()
        avg += test2(5/n, n, 0.5, True)
        print('__________________________________________________________')

    print('avg ratio:', avg/T)


def test4(n):
    random.seed(0)

    timer.start()
    sp_forest_alg = SpanningForestAlgorithm(n)
    print('init time:', timer.stop())

    p = 0.9

    E = set()
    g = build_g([], n)
    E_inv = set()
    for i in range(n):
        for j in range(i + 1, n):
            E_inv.add(Edge(i, j))

    random.seed(0)
    while True:
        if random.random() < p:
            e = random.sample(E_inv, 1)[0]

            E.add(e)
            E_inv.remove(e)
            g[e.u].add(e.v)
            g[e.v].add(e.u)
            timer.start()
            sp_forest_alg.add_edge(e)
        elif len(E) > 0:
            e = random.sample(E, 1)[0]

            E_inv.add(e)
            E.remove(e)
            g[e.u].remove(e.v)
            g[e.v].remove(e.u)

            timer.start()
            sp_forest_alg.remove_edge(e)

        if random.randint(0, 100) == 0:
            timer.start()
            cc = count_cc(g, n)
            print('naive cc count time', timer.stop())

            timer.start()
            span_size = len(sp_forest_alg.get_sp_forest_edges())
            print('build span tree time', timer.stop())

            if span_size != n - cc:
                print('Fail')
            else:
                print('Ok')
            print('edges count:', len(E))
            print('________________________________________________')


def test5(n):
    random.seed(0)

    timer.start()
    sp_forest_alg = SpanningForestAlgorithm(n)
    print('init time:', timer.stop())

    p = 0.9

    random.seed(0)
    edge_cnt = 0
    while True:
        if random.random() < p:
            u = random.randint(0, n - 1)
            v = random.randint(0, n - 1)
            while u == v:
                v = random.randint(0, n - 1)

            e = Edge(u, v)

            sp_forest_alg.add_edge(e)

            edge_cnt += 1
        else:
            e = sp_forest_alg.graph_sketches[0].sample_edge()

            if e is not None:
                sp_forest_alg.remove_edge(e)

                edge_cnt -= 1

        if random.randint(0, 100) == 0:
            timer.start()
            sp_forest_alg.get_sp_forest_edges()
            print('build span tree time', timer.stop(), 'edge count', edge_cnt)


# test1()
# test1_exact()
test3(1000)
