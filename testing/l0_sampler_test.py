import random
import matplotlib.pyplot as plt
from numpy import std, mean

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


def test_sample_size(n, N, param):
    indexes = random.sample(range(0, n - 1), N)

    l0_sampler = L0Sampler(n, param)

    for j in range(N):
        l0_sampler.update(indexes[j], random.randint(1, MAX_VAL))

    samples = l0_sampler.get_samples()

    return len(samples)


def test_run_time(n, N, param):
    indexes = random.sample(range(0, n - 1), N)

    timer.start()
    l0_sampler = L0Sampler(n, param)

    for j in range(N):
        l0_sampler.update(indexes[j], random.randint(1, MAX_VAL))

    return timer.stop().seconds


def plot_size(a, b, d=-1):
    if d == -1:
        d = (b - a) >> 4
    random.seed(0)

    params = []
    sample_sizes = []

    for param in range(a, b, d):
        params.append(param)

        timer.start()

        sample_sizes.append(test_sample_size(1 << 31, int(1e5), param))

        print('param:', param, 'run time:', timer.stop())

    plt.grid()
    plt.plot(params, sample_sizes, '-o')

    plt.show()


def plot_time(a, b, d=-1):
    if d == -1:
        d = (b - a) >> 2
    random.seed(0)

    params = []
    times = []

    for param in range(a, b, d):
        params.append(param)

        timer.start()

        times.append(test_run_time(1 << 31, int(1e5), param))

        print('param:', param, 'run time:', timer.stop())

    plt.grid()
    plt.plot(params, times, '-o')

    plt.show()


# plot_size(int(1e1), int(1e5))
plot_time(int(1e1), int(1e4))
