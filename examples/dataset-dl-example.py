"""
Utility script to be run in a training job to download files from COS into the WMLA storage.
Your code folder (submitted as .zip file to WMLA) must contain both this script, and a JSON file
cos_credentials.json containing an access key, secret key, bucket name,
and the correct public endpoint to connect to this bucket.
"""
import os
import argparse
import boto3
import json
from pprint import pformat
import subprocess

import subprocess
subprocess.call('pip install --upgrade tqdm', shell=True)

from tqdm import tqdm
from tqdm.contrib.concurrent import thread_map

# STEP 0 - IDENTIFY WHERE THE DATA WILL BE STORED IN WML-A
DATA_DIR = os.environ['DATA_DIR']
RESULT_DIR = os.environ["RESULT_DIR"]
print(f"Data will be stored in $DATA_DIR {DATA_DIR}")
print("Current content of this folder is:")
print(os.listdir(DATA_DIR))

# STEP 1 - READ USER ARGUMENTS
parser = argparse.ArgumentParser('WMLA COS data loader')
parser.add_argument('--nthreads', dest='nthreads', type=int,
                    help='Number of threads to read data in parallel (default: 10)', default=10)
parser.add_argument('--prefix', dest='prefix', type=str,
                    help='Used to filter the files to download from the COS bucket (default: empty)', default='')
parser.add_argument('--target_subdirectory', dest='target_subdirectory', type=str,
                    help='Data will be stored in $DATA_DIR/target_subdirectory (default: empty)', default='')
parser.add_argument('--limit', dest='limit', type=int,
                    help='For debugging purposes, limit the number of files downloaded', default=None)

args = parser.parse_args()
print(f'\nRemote data will be downloaded using {args.nthreads} threads')
print(f'Remote data will be filtered using prefix: {args.prefix}')
print(f'Remote data will be downloaded into local directory: {os.path.join(DATA_DIR, args.target_subdirectory)}')
if args.limit:
    print(f'Remote data limited to {args.limit} files')
else:
    print('No limit on remote data files, downloading all files matching prefix.')

# STEP 2 - LOAD THE COS CREDENTIALS AND CREATE A COS CLIENT
with open('cos_credentials.json', 'r') as f:
    credentials = json.load(f)
print("\nCOS credentials loaded successfully. Keys: ", list(credentials.keys()))

s3 = boto3.resource('s3',
                    aws_access_key_id=credentials['access_key'],
                    aws_secret_access_key=credentials['secret_key'],
                    endpoint_url=credentials['url'])
bucket = s3.Bucket(credentials['bucket'])
print(f"Connected to bucket {credentials['bucket']}")

# STEP 3 - IDENTIFY REMOTE KEYS TO BE DOWNLOADED
keys = [file.key for file in bucket.objects.filter(Prefix=args.prefix).limit(args.limit)]
print(f"Will download {len(keys)} remote files. First 10 keys are: {pformat(keys[:min(10, len(keys))])}")

# STEP 4 - DOWNLOAD THE DATA FROM COS IN PARALLEL
def download(key):
    local_path = os.path.join(DATA_DIR, args.target_subdirectory, key)
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    if os.path.exists(local_path):
        # if we already downloaded the file in a previous run...
        # ...or if the key is a subfolder not a file, ignore
        return
    bucket.download_file(key, local_path)
thread_map(download, keys, max_workers=args.nthreads, tqdm_class=tqdm)
    
# STEP 5 - LET WMLA KNOW WE SUCCEEDED BY SAVING IN THE /model FOLDER
os.makedirs(os.path.join(RESULT_DIR, 'model'), exist_ok=True)
with open(os.path.join(RESULT_DIR, 'model', 'done.txt'), 'w') as f:
    f.write('Done.')