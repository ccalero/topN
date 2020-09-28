# -*- coding: UTF-8 -*-

"""
Execute:
__________________________

    python 5_dataframes_pool.py -i n50M.txt -n 10

Example Out:
__________________________



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
from multiprocessing import Pool

N_THREADS = 6 # Set to 2 times number of cores, assuming hyperthreading


def printTime(start_time):
    print("[ ] Execution Time: %.2f seconds " % (time.time() - start_time))

def get_max_numbers(filename, numbers, chunksize = 6400000):
    start_time = time.time()
    
    iter_file = pd.read_csv(filename, chunksize=chunksize,
                            iterator = True, header=None,
                            names = ['value'])

    max_processors = 8
    topN_df = pd.DataFrame({},columns=['value'])

    with Pool(max_processors) as pool:
        for df in iter_file:
            df_temp = pool.apply_async(df.nlargest, [numbers, 'value'])
            topN_df = pd.concat([topN_df, df_temp.get()], ignore_index=True).astype('int32')
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