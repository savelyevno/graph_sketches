import random
from math import log2, ceil

from graph_representation.GraphSketch import GraphSketch
from graph_representation.tools import Edge
from graph_algorithms.spanning_forest.SpanningForestAlgorithm import SpanningForestAlgorithm
from tools.Timer import Timer
from tools.graph_generation import build_g, count_cc, generate_graph, read_from_file
from tools.primality_test import prime_getter

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

    span_for = sp_forest_alg.get_sp_forest_edges()

    g = build_g(E, n)
    cc = count_cc(g, n)

    print(cc)
    print(len(span_for) == n - cc)
    print('solving time', timer.stop())


def test2(p, n, print_log=False):

    timer.start()

    E, g = generate_graph(n, p)

    if print_log:
        print('gen time', timer.stop())

        print('edges: ', len(E))

    if print_log:
        timer.start()
    sp_forest_alg = SpanningForestAlgorithm(n)
    if print_log:
        print('total build time', timer.stop())

    if print_log:
        timer.start()
    sp_forest_alg.add_edges(E)
    if print_log:
        print('edges add time', timer.stop())

    if print_log:
        timer.start()
    cc = count_cc(g, n)
    if print_log:
        print('naive solve time:', timer.stop())

    if print_log:
        timer.start()
    cc_est = sp_forest_alg.count_cc()

    if print_log:
        print('solving time', timer.stop())

    return cc_est == cc, cc


def test2_file(filename, print_log=False):

    timer.start()

    E, g = read_from_file(filename)
    n = len(g)

    if print_log:
        print('gen time', timer.stop())

        print('edges: ', len(E))

    if print_log:
        timer.start()
    sp_forest_alg = SpanningForestAlgorithm(n)
    if print_log:
        print('total build time', timer.stop())

    if print_log:
        timer.start()
    sp_forest_alg.add_edges(E)
    if print_log:
        print('edges add time', timer.stop())

    if print_log:
        timer.start()
    cc = count_cc(g, n)
    if print_log:
        print('naive solve time:', timer.stop())

    if print_log:
        timer.start()
    cc_est = sp_forest_alg.count_cc()

    if print_log:
        print('solving time', timer.stop())

    return cc_est == cc, cc


def test3(n):
    random.seed(0)

    T = 1
    p = n**(-0.7)
    for test in range(0, T):

        timer.start()
        result, cc = test2_file('graphs/rmat1.txt', True)
        # result, cc = test2(p, n, True)
        if not result:
            print(test, 'Fail', timer.stop())
        else:
            print(test, 'Ok', timer.stop())
        print(cc)
        print('__________________________________________________________')


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
            g[e.u].add_another_sketch(e.v)
            g[e.v].add_another_sketch(e.u)
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
test3(1000)
