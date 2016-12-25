import random
import numpy as np
import matplotlib.pyplot as plt

from l0_sampler.plain_v2.SparseRecoverer import SparseRecoverer
from tools.Timer import timer


MAX_VAL = int(1e6)


def test_sample_size(N, s, delta):
    n = 1 << 31
    indexes = random.sample(range(0, n - 1), N)

    recoverer = SparseRecoverer(n, s, delta)
    for j in range(N):
        # recoverer.update(indexes[j], random.randint(1, MAX_VAL))
        recoverer.update(indexes[j], 2*random.randint(0, 1) - 1)

    samples = recoverer.recover()

    if samples is not None:
        return len(samples)
    else:
        return 0


def plot_size_on_N():
    colors = ['r', 'g', 'b', 'm', 'orange']
    plt.grid()

    delta = 1e-3
    Ns = [1e1, 1e2, 1e3, 1e4]
    Ns_names = ['1', '2', '3', '4', '5']
    ss = np.linspace(1, 1e3, 1 << 6)

    i = 0
    for N in Ns:
        timer.start()
        sizes = [test_sample_size(int(N), int(s), delta) for s in ss]
        print(N, timer.stop())

        plt.plot(ss, sizes, c=colors[i], label='$N = 10^' + Ns_names[i] + '$')

        i += 1

    plt.xlabel('$s$', fontsize=16)
    plt.ylabel('$|R_{s, \delta}|$', rotation='horizontal', fontsize=16)
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0, fontsize=16)
    plt.subplots_adjust(left=0.1, right=0.75)

    plt.show()


def plot_size_on_delta(a, b, s, N):
    random.seed(0)

    deltas = list(np.linspace(a, b, 64))
    sample_sizes = []

    for delta in deltas:
        timer.start()

        sample_sizes.append(test_sample_size(1 << 31, N, s, 1/delta))

        print('delta:', delta, 'run time:', timer.stop())

    plt.grid()
    plt.plot(deltas, sample_sizes, '-o')

    plt.show()


def plot_size_on_s(a, b, delta, N):
    random.seed(0)

    ss = list(np.linspace(a, b, 64))
    sample_sizes = []

    for s in ss:
        timer.start()

        sample_sizes.append(test_sample_size(1 << 31, N, int(s), 1/delta))

        print('s:', s, 'run time:', timer.stop())

    plt.grid()
    plt.plot(ss, sample_sizes)

    plt.show()


def plot_size_on_s_and_delta(N):
    random.seed(0)

    deltas = np.logspace(1, 5, num=5, base=10)

    data = []

    for delta in deltas:
        ss = list(np.linspace(1, N//2, 32))
        sample_sizes = []

        timer.start()

        for s in ss:

            sample_sizes.append(test_sample_size(1 << 31, N, int(s), 1/delta))

        print('delta:', delta, 'run time:', timer.stop())

        data.append(ss)
        data.append(sample_sizes)
        plt.plot(ss, sample_sizes, '-', c=np.random.rand(3, 1))

    with open("io/data3.txt", 'w') as f:
        lines = []
        for a in data:
            s = ''
            for it in a:
                s += str(it) + ' '
            s += '\n'
            f.writelines(s)

    plt.grid()
    plt.show()


def plot_from_file():
    colors = ['r', 'g', 'b', 'm', 'orange']

    # f, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
    #
    # ax1.grid()
    # with open('io/data3.txt', 'r') as f:
    #     lines = f.readlines()
    #     for i in range(0, len(lines), 2):
    #         x = [float(it) for it in lines[i].split()]
    #         y = [float(it) for it in lines[i + 1].split()]
    #
    #         ax1.plot(x, y, c=colors[4 - i])
    #
    # ax2.grid()
    # with open('io/data3_1.txt', 'r') as f:
    #     lines = f.readlines()
    #     for i in range(0, len(lines), 2):
    #         x = [float(it) for it in lines[i].split()]
    #         y = [float(it) for it in lines[i + 1].split()]
    #
    #         ax2.plot(x, y, c=colors[4 - i], label='delta = 1e-' + str((i + 2)//2))
    #
    # ax2.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0, fontsize=12)
    #
    # plt.subplots_adjust(left=0.08, right=0.8)

    plt.grid()
    with open('io/data4.txt', 'r') as f:
        lines = f.readlines()
        for i in range(0, len(lines), 2):
            x = [float(it) for it in lines[i].split()]
            y = [float(it) for it in lines[i + 1].split()]

            plt.plot(x, y, c=colors[4 - i], label='delta = 1e-' + str((i + 2)//2))
    # plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0, fontsize=12)
    # plt.subplots_adjust(right=0.7)

    plt.show()


# test_sample_size(1 << 31, int(5e4), int(5e4), 1e-2)
# plot_size_on_delta(1, 100000, int(1e2), int(1e3))
# plot_size_on_s(1, int(1e3), int(1e3), int(1e3))
# plot_size_on_s_and_delta(int(1e4))
# plot_from_file()
plot_size_on_N()