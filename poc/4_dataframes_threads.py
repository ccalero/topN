# -*- coding: UTF-8 -*-

"""
Execute:
__________________________

    python 4_dataframes_threads.py -i n50M.txt -n 10

Example Out:
__________________________

    [ ] Calculating...
    [ ] Execution Time: 0.89 seconds 
    [ ] Result:
    value
    10000
    10000
    10000
    10000
    10000
    10000
    10000
    10000
    10000
    10000

Conclusión:
__________________________

Not valid to large files, maybe, optimizing the calculation of the lines of the file
"""

# IMPORT
import numpy as np
import pandas as pd
import sqlite3
from sqlalchemy import create_engine
import math
import time
import argparse
import os
import threading
from functools import partial

N_THREADS = 6 # Set to 2 times number of cores, assuming hyperthreading


def printTime(start_time):
    print("[ ] Execution Time: %.2f seconds " % (time.time() - start_time))

class GetMaxNumbersThread(threading.Thread):

    def __init__(self, filename, numbers, start_line, nrows, chunksize = 300000):
        threading.Thread.__init__(self)
        self.filename = filename
        self.numbers = numbers
        self.start_line = start_line
        self.nrows = nrows
        self.chunksize = chunksize

        self.topN_df = pd.DataFrame({},columns=['value'])

    def run(self):
        for df in pd.read_csv(filename, chunksize=self.chunksize, iterator = True,
                                header=None, skiprows=self.start_line, nrows=self.nrows,
                                names = ['value'] ):
            largest_df = df.nlargest(self.numbers, 'value')
            self.topN_df = pd.concat([self.topN_df, largest_df], ignore_index=True).astype('int32')
            self.topN_df = self.topN_df.nlargest(self.numbers, 'value')

def get_max_numbers(filename, numbers, chunksize = 300000):
    start_time = time.time()
    
    df = pd.read_csv(filename, header=None)
    total_lines = len(df.index)
    nrows = math.ceil(total_lines / N_THREADS)

    list_threads = []
    for fh_idx in range(0,N_THREADS):
        start_line = fh_idx * nrows

        list_threads.append(GetMaxNumbersThread(filename, numbers, int(start_line), nrows, chunksize) )
        list_threads[fh_idx].start()

    topN_df = pd.DataFrame({},columns=['value'])
    for fh_idx in range(0,N_THREADS):
        list_threads[fh_idx].join()
        topN_df = pd.concat([topN_df, list_threads[fh_idx].topN_df], ignore_index=True).astype('int32')
        topN_df = topN_df.nlargest(numbers, 'value')

    printTime(start_time)
    return topN_df

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ifile", "-i", help="set input file", required=True)
    parser.add_argument("--nnum", "-n", help="set N numbers", required=True)
    args = parser.parse_args()

    filename = args.ifile
    n_nums = int(args.nnum)

    print("[ ] Calculating...")
    topN_df = get_max_numbers(filename, n_nums)
    print("[ ] Result:")
    print(topN_df.to_string(index=False))