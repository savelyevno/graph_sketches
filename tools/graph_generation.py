import random

from graph.tools import Edge


def build_g(E, n):
    g = [set() for i in range(n)]
    for e in E:
        g[e.u].add(e.v)
        g[e.v].add(e.u)
    return g


def count_cc(g, n):
    used = [False] * n
    res = 0

    def dfs(u):
        used[u] = True

        for v in g[u]:
            if not used[v]:
                dfs(v)

    for i in range(n):
        if not used[i]:
            res += 1
            dfs(i)

    return res


def generate_graph(n, p):
    E = []
    for i in range(n):
        for j in range(i + 1, n):
            if random.random() < p:
                E.append(Edge(i, j))

    g = build_g(E, n)

    return E, g