import os
import time
import argparse

import matplotlib.pyplot as plt

from topN import getTopN

if __name__ == '__main__':

    files = [
        'data/n1G.txt', 'data/n2G.txt', 'data/n5G.txt',
        'data/n10G.txt', 'data/n25G.txt', 'data/n50G.txt'
    ]

    x_size = []
    y_time = []

    numbers = [1_000, 10_000, 100_000, 1_000_000]
    cont = 0
    for n_nums in numbers:
        for f in files:
            print("File: %s, numbers %d" % (f, n_nums))
            # save space file
            x_size.append( os.path.getsize(f) / (1024*1024*1024) )
            # save start time
            start_time = time.time()

            # Execute algorithm
            getTopN(f, n_nums)

            # Save execution time
            y_time.append(time.time() - start_time)
            print('--------------\n')

        cont += 1
        plt.figure(cont)
        plt.plot(x_size, y_time)
        plt.title('Time Complexity, Find %d longest numbers' % n_nums)
        plt.xlabel('Size')
        plt.ylabel('Time')
        plt.savefig('time_complexity_%d' % n_nums)
