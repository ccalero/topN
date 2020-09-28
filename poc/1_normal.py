# -*- coding: UTF-8 -*-
"""
Execute:
__________________________

    python 1_normal.py -i n50M.txt -n 10

Example Out:
__________________________


    [ ] Calculating...
    [ ] Execution Time: 7.68 seconds 
    [ ] Result:
    [10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000]

"""
import os
import threading

import random
import time
from collections import deque

import sys, getopt

import argparse

top_number = [0]

def printTime(start_time):
    print("[ ] Execution Time: %.2f seconds " % (time.time() - start_time))

def get_max_numbers(filename, numbers):
    start_time = time.time()
    with open(filename) as f:
        for line in f.read().splitlines():
            number = int(line)
            min_number = min(top_number)
            if number > min_number:
                if len(top_number) >= numbers:
                    top_number.remove(min_number)
                top_number.append(number)

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
    top_number.sort(reverse=True)
    print(top_number)
    print("\n")