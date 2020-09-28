# -*- coding: UTF-8 -*-

import os
import threading
from shutil import copyfile
import random
import argparse

def create_file(filename, size_gb):
    lines = int(size_gb) * 10_000_000

    with open(filename, 'w') as f:
        for i in range(lines):
            # Range from 1_000_000_000 to 9_999_999_999
            # each line will be 10 bytes
            f.write('%s\n' % random.randint(1_000_000_000, 9_999_999_999))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--size", "-s", help="set size file in GB", required=True)
    parser.add_argument("--ofile", "-o", help="set output file", required=True)

    # Read arguments from the command line
    args = parser.parse_args()
    size = args.size
    ofile = args.ofile

    print("[ ] Generating...")
    create_file(ofile, size)
    print("[ ] Generated")
