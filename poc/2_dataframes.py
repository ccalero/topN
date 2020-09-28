# -*- coding: UTF-8 -*-

"""
Execute:
__________________________

    python 2_dataframes.py -i n50M.txt -n 10

Example Out:
__________________________


    [ ] Calculating...
    [ ] Execution Time: 4.77 seconds
    [ ] Result:
    [0, [[10000], [10000], [10000], [10000]]]

Conclusión:
__________________________

Not valid to large files
"""

# IMPORT
import numpy as np
import pandas as pd
import sqlite3
from sqlalchemy import create_engine

import time
import argparse

top_number = []

def printTime(start_time):
    print("[ ] Execution Time: %.2f seconds " % (time.time() - start_time))

def get_max_numbers(filename, numbers):
    start_time = time.time()

    df = pd.read_csv(filename, header=None, names = ['value'])
    top_number.append(
        df.nlargest(numbers, 'value')
    )

    printTime(start_time)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ifile", "-i", help="set input file", required=True)
    parser.add_argument("--nnum", "-n", help="set N numbers", required=True)

    # Read arguments from the command line
    args = parser.parse_args()
    filename = args.ifile
    n_nums = int(args.nnum)

    print("[ ] Calculating...")
    get_max_numbers(filename, n_nums)
    print("[ ] Result:")
    print(top_number)
    print("\n")