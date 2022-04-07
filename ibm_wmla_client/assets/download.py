import os 
from __future__ import print_function
import argparse
import time

import sys
import os
import glob
import argparse
import dill
import json

parser = argparse.ArgumentParser(description='Downloader for WMLA')
parser.add_argument('--data_dir', type=str, default="/gfps/data_dir", metavar='N',
                    help='input data directory on the WMLA shared filesystem')
parser.add_argument('--result_dir', type=str, default="/gfps/result_dir", metavar='N',
                    help='input result directory on the WMLA shared filesystem')
args = parser.parse_args()
print(args)

DATA_DIR = os.getenv("DATA_DIR")
RESULT_DIR = os.getenv("RESULT_DIR")

if __name__ == "__main__":

    with open("./func.pickle", "rb") as f: 
            func = dill.load(f)

    with open("./params.json", "r") as f:
            kwargs = json.load( f)

    download_dir = DATA_DIR + "/" + args.data_dir 

    kwargs["download_dir"] = download_dir

    func(**kwargs)


