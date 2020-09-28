import os
import argparse
import matplotlib.pyplot as plt

from memory_profiler import memory_usage

from topN import getTopN

if __name__ == '__main__':

    files = [
        'data/n1G.txt', 'data/n2G.txt', 'data/n5G.txt',
        'data/n10G.txt', 'data/n25G.txt', 'data/n50G.txt'
    ]

    x_size = []
    y_memory = []

    numbers = [1_000, 10_000, 100_000, 1_000_000]
    cont = 0
    for n_nums in numbers:
        for f in files:
            print("File: %s, numbers %d" % (f, n_nums))
            # save space file
            x_size.append(os.path.getsize(f) / (1024*1024*1024) )

            # Execute algorithm
            mem_usage = memory_usage( (getTopN, (f,), {'numbers' : n_nums}), interval=.2)

            # Save maximum RAM used
            y_memory.append( max(mem_usage) )
            print('Maximum memory usage: %s' % max(mem_usage))
            print('--------------\n')
        cont += 1
        plt.figure(cont)
        plt.plot(x_size, y_memory)
        plt.title('Space Complexity, Find %d longest numbers' % n_nums)
        plt.xlabel('Size')
        plt.ylabel('Memory used')
        plt.savefig('space_complexity_%d' % n_nums)