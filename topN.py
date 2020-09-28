# -*- coding: UTF-8 -*-

"""
Execute:
__________________________

    python topN.py -i numbers.txt -n 10

Example Out:
__________________________

    [ ] Calculating...
    [ ] Execution Time: 17.79 seconds 
    [ ] Result:
        value
    99999999
    99999998
    99999997
    99999996
    99999995
    99999994
    99999993
    99999992
    99999991
    99999990

"""

# IMPORT
import numpy as np
import pandas as pd

import time
import argparse

def printTime(start_time):
    print("[ ] Execution Time: %.2f seconds " % (time.time() - start_time))

def getTopN(filename, numbers, chunksize = 600_000):
    topN_df = pd.DataFrame({},columns=['value'])
    start_time = time.time()

    for df in pd.read_csv(filename, chunksize=chunksize,
                            iterator = True, header=None,
                            names = ['value']):
        largest_df = df.nlargest(numbers, 'value')
        topN_df = pd.concat([topN_df, largest_df], ignore_index=True).astype('int64')
        topN_df = topN_df.nlargest(numbers, 'value')

    printTime(start_time)
    return topN_df

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ifile", "-i", help="set input file", required=True)
    parser.add_argument("--nnum", "-n", help="set N numbers", required=True)

    # Read arguments from the command line
    args = parser.parse_args()
    filename = args.ifile
    n_nums = int(args.nnum)

    print("[ ] Calculating...")
    topN_df = getTopN(filename, n_nums)
    print("[ ] Result:")
    print(topN_df.to_string(index=False))