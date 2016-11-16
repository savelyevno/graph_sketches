from math import log2, ceil
import random

from graph.GraphSketch import GraphSketch
from graph.tools import Edge
from spanning_forest.span_forest import get_spanning_forest
from tools.Timer import Timer
from tools.graph_generation import build_g, count_cc


timer = Timer()


def test1():
    E = []
    with open('input.txt', 'r') as f:
        lines = [line.split() for line in f.readlines()]
        n = int(lines[0][0])
        m = int(lines[0][1])

        for i in range(m):
            E.append(Edge(int(lines[i + 1][0]), int(lines[i + 1][1])))

    t = int(ceil(log2(n)))
    sketches = []

    timer.start()

    random.seed(0)
    for i in range(t):
        graph_sketch = GraphSketch(n)

        graph_sketch.add_edges(E)

        sketches.append(graph_sketch)

    print('total build time', timer.stop())
    timer.start()

    span_for = get_spanning_forest(sketches)

    g = build_g(E, n)
    cc = count_cc(g, n)

    print(cc)
    print(len(span_for) == n - cc)
    print('solving time', timer.stop())


def test2(p, a, b, print_log=False):
    n = random.randint(a, b)

    timer.start()

    E = []
    for i in range(n):
        for j in range(i + 1, n):
            if random.random() < p:
                E.append(Edge(i, j))

    g = build_g(E, n)

    print('gen time', timer.stop())

    if print_log:
        print('n', n)
        print(E)

    timer.start()

    t = int(ceil(log2(n)))
    sketches = []
    for i in range(t):
        graph_sketch = GraphSketch(n)

        graph_sketch.add_edges(E)

        sketches.append(graph_sketch)

    print('total build time', timer.stop())
    timer.start()

    span_size = len(get_spanning_forest(sketches))

    cc = count_cc(g, n)

    if print_log:
        # print(cc)
        # print(span_size)
        print(span_size == n - cc)
    print('solving time', timer.stop())

    return span_size == n - cc


def test3(n):
    random.seed(0)

    T = 1
    for test in range(0, T):

        timer.start()
        if not test2(0.5, n, n, False):
            print(test, 'Fail', timer.stop())
        else:
            print(test, 'Ok', timer.stop())
        print('__________________________________________________________')


def test4(n):
    random.seed(0)

    t = int(ceil(log2(n)))

    sketches = []
    timer.start()
    for i in range(t):
        graph_sketch = GraphSketch(n)
        print('built', i + 1, 'sketches')
        sketches.append(graph_sketch)
    print('init time', timer.stop())

    p = 0.75

    E = set()
    g = build_g([], n)
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
                    sketches[i].add_edge(e)
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
                sketches[i].remove_edge(e)
            # print('rem edge time', timer.stop())

            # print('removed edge', e)

        if changed:
            timer.start()
            cc = count_cc(g, n)
            # print('naive cc count time', timer.stop())

            timer.start()
            span_size = get_spanning_forest(n, sketches)
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


test3(100)
