import random
import matplotlib.pyplot as plt
from numpy import std, mean
import numpy as np
from math import log, ceil, log2

# from tools import memory_limit
from l0_sampler.fast.L0Sampler import L0Sampler
from tools.Timer import timer, ticker


MAX_VAL = int(1e6)


def test1():
    random.seed(0)

    n = 1 << 31
    N = int(1e5)

    indexes = random.sample(range(0, n - 1), N)
    values = [random.randint(1, MAX_VAL) for i in range(N)]

    l0_sampler = L0Sampler(n)

    timer.start()

    ticker_id = ticker.start_track(5, lambda: print('tick j:', j))
    for j in range(N):
        l0_sampler.update(indexes[j], values[j])
    ticker.stop_track(ticker_id)

    # for i in sorted(ideal_l0_sampler.items.keys()):
    #     l0_sampler.update(i, ideal_l0_sampler.items[i])

    print('l0_sampler build time:', timer.stop())

    # ideal_counter = {}
    # counter = {}
    #
    # for i in ideal_l0_sampler.items.keys():
    #     ideal_counter[i] = 0
    #     counter[i] = 0
    #
    # S = 10*N
    #
    # ticker_id = ticker.start_track(5, lambda: print(r))
    #
    # for r in range(S):
    #     ideal_sample = ideal_l0_sampler.get_sample()
    #
    #     sample = l0_sampler.get_sample()
    #
    #     ideal_counter[ideal_sample[0]] += 1
    #
    #     counter[sample[0]] += 1
    #
    # ticker.stop_track(ticker_id)

    samples = l0_sampler.get_samples()

    print('sample len:', len(samples))
    print('levels count:', l0_sampler.levels_count)
    print('sample std:\t\t', int(std(list(samples.keys()))))
    print('theoretical std:', int(((n**2 - 1)/12)**0.5))

    print('sample mean:\t ', int(mean(list(samples.keys()))))
    print('theoretical mean:', int((n - 1)/2))

    # plt.figure(1)
    #
    # plt.subplot(211)
    # plt.bar(ideal_counter.keys(), ideal_counter.values(), width=2)
    #
    # plt.subplot(212)
    # plt.bar(counter.keys(), counter.values(), width=2)
    #
    # plt.show()


def test_sample_size(N, n=1 << 31, delta=1.0/100, param=2.0):
    indexes = random.sample(range(0, n - 1), N)

    l0_sampler = L0Sampler(n, delta=delta, param=param)

    for j in range(N):
        l0_sampler.update(indexes[j], random.randint(1, MAX_VAL))

    samples = l0_sampler.get_samples()
    # print(l0_sampler.levels_count)

    return len(samples)


def test_levels_distr(n, N, param):
    indexes = random.sample(range(0, n - 1), N)

    l0_sampler = L0Sampler(n, param)

    for j in range(N):
        l0_sampler.update(indexes[j], random.randint(1, MAX_VAL))

    return l0_sampler.levels_count


def test_run_time(n, N, param):
    indexes = random.sample(range(0, n - 1), N)

    timer.start()
    l0_sampler = L0Sampler(n, param)

    for j in range(N):
        l0_sampler.update(indexes[j], random.randint(1, MAX_VAL))

    return timer.stop().microseconds/1000


def plot_size_on_param():
    N = int(1e3)

    random.seed(0)

    params = np.linspace(10, 1e3, 1 << 4)
    sample_sizes = []

    for param in params:
        timer.start()

        sample_sizes.append(test_sample_size(N, delta=float(1/param)))

        print('param:', param, 'run time:', timer.stop())

    plt.grid()
    plt.plot(params, sample_sizes, '-')

    plt.show()


def plot_size_on_N():
    delta = 1e-1

    random.seed(0)

    Ns = np.linspace(10, 1e5, 1 << 4)
    sample_sizes = []

    for N in Ns:
        timer.start()

        sample_sizes.append(test_sample_size(int(N), delta=delta))

        print('param:', N, 'run time:', timer.stop())

    plt.grid()
    plt.plot(Ns, sample_sizes, '-')

    plt.show()


def plot_size_on_delta_r():
    random.seed(0)
    N = 1e4

    deltas = np.logspace(1, 3, 16)
    sample_sizes = []

    for delta in deltas:
        timer.start()

        sample_sizes.append(test_sample_size(1 << 31, int(N), delta_r=1/delta, delta=1e-3))

        print('delta:', delta, 'run time:', timer.stop())

    plt.grid()
    plt.plot(deltas, sample_sizes)

    plt.show()


def plot_time(b, N, d=-1):
    if d == -1:
        d = 32
    random.seed(0)

    params = np.logspace(1, 5, d)
    # params = np.linspace(10, b, d)
    times = []

    for param in params:
        timer.start()

        avg = 0
        rep = int(10)
        for i in range(rep):
            avg += test_run_time(1 << 31, N, param)
        avg /= rep
        times.append(avg)

        print('param:', param, 'run time:', timer.stop())

    plt.grid()
    plt.plot(params, times)

    plt.show()


def plot_levels_distr_hist(N, param):
    data = None

    rep = 100
    for i in range(rep):
        levels_count = test_levels_distr(1 << 31, N, param)

        if data is None:
            data = [it for it in levels_count]
        else:
            data = [data[i] + levels_count[i] for i in range(len(data))]

    data = [it/rep for it in data]

    print(data)

    plt.bar(np.arange(len(data)), data)

    plt.show()


def plot_param():
    random.seed(0)

    Ns = [1e4, 1e5, 1e6]
    Nss = ['1e4', '1e5', '1e6']
    colors = ['r', 'g', 'b', 'm', 'orange']

    file = open('io2/param.txt', 'w')

    deltas = np.linspace(10, 1e3, 1 << 4)
    params = np.linspace(1, 1 << 5, (1 << 7) - 1)

    # arg_s = ''
    # for delta in deltas:
    #     arg_s += str(delta) + ' '
    # file.write(arg_s + '\n')

    ress = []
    with open('io2/param_rsv.txt', 'r') as f:
        lines = f.readlines()

        for i in range(3):
            ress.append([float(x) for x in lines[i + 1].split()])

    for j in range(len(Ns)):
        N = Ns[j]

        # res = []
        # last = 0
        # for delta in deltas:
        #     timer.start()
        #
        #     i = last
        #     while i < len(params) and test_sample_size(int(N), param=float(params[i]), delta=float(1 / delta)) < min(N, delta):
        #         i += 1
        #     last = i
        #
        #     print(delta, timer.stop(), params[i])
        #
        #     res.append(params[i])
        #
        #     res.append(test_sample_size(int(N), delta=float(1/delta)))
        #     print(delta, timer.stop())
        #
        # val_s = ''
        # for param in res:
        #     val_s += str(param) + ' '
        #
        # file.write(val_s + '\n')

        # res = ress[j]

        res = []

        for delta in deltas:
            res.append(test_sample_size(int(N), delta=1/delta))

        plt.plot(deltas, res, c=colors[j], label='N='+Nss[j])

    plt.xlabel('1/delta')
    plt.ylabel('')
    plt.grid()
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0, fontsize=12)
    plt.subplots_adjust(left=0.08, right=0.8)

    plt.show()


def plot_k():
    N = 1e4
    delta = 1e-4

    ks = np.arange(2, ceil(2*log(1/delta)))

    res = []
    for k in ks:
        timer.start()
        res.append(test_sample_size(1 << 31, int(N), delta=delta, k=int(k)))
        print(k, timer.stop())

    plt.grid()
    plt.plot(ks, res)

    plt.show()


def test():
    random.seed(0)

    N = 50
    n = 1 << 31
    delta = 1e-1

    indexes = random.sample(range(0, n - 1), N)
    values = [random.randint(1, MAX_VAL) for i in range(N)]

    ind_to_order = {}
    for i in indexes:
        ind_to_order[i] = len(ind_to_order)

    count = [0]*N

    T = int(1e5)
    ticker_id = ticker.start_track(5, lambda: print(it))
    timer.start()

    for it in range(T):
        l0_sampler = L0Sampler(n, delta=delta)

        for i in range(N):
            l0_sampler.update(indexes[i], values[i])

        count[ind_to_order[l0_sampler.get_sample()[0]]] += 1

    ticker.stop_track(ticker_id)
    print('done', timer.stop())

    count = [it/T for it in count]

    entropy = 0

    for c in count:
        entropy -= c*log2(c + int(c==0))

    mn = min(count)
    mx = max(count)

    plt.bar(list(range(N)), count, color='g')
    print('min:', mn, 'max:', mx)

    print('entropy:', entropy, 'ideal:', -log2(1/N), 'ratio:', -entropy/log2(1/N))

    plt.show()


# plot_size_on_N()
# plot_size_on_param()
# plot_size_on_delta_r()
# plot_time(int(1e5), int(1e3))
# plot_levels_distr_hist(int(1e3), 1e5)
# plot_param()
# plot_k()
test()
