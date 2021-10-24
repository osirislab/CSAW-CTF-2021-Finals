#!/usr/bin/env python3
"""
generate.py

    Pulls a list of all available npm packages, and installs
    5000 random ones in the current directory to populate
    `node_modules/` and the `package-lock.json`.
"""
import os
import sys
import json
import random
import subprocess

import requests
from tqdm import tqdm

FEED = "https://replicate.npmjs.com/_all_docs"
FINALIZED_FEED = "finalized.json"

def download_all_packages():
    response = requests.get(FEED, stream=True)
    total_size_in_bytes= int(response.headers.get('content-length', 0))
    block_size = 1024

    progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
    with open(FINALIZED_FEED, 'wb') as file:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)
    
    progress_bar.close()
    if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
        print("ERROR, something went wrong")

def main():
    skip_download = False
    if len(sys.argv) == 2:
        if sys.argv[1] == "--skip-download":
            skip_download = True

    if not skip_download and not os.path.exists(FINALIZED_FEED):
        print("Downloading huge package feed...")
        download_all_packages()

    with open(FINALIZED_FEED) as fd:
        pkgs = fd.readlines()

    print("Sampling random packages for `package-lock.json`...")
    final_pkgs = []
    for i in range(0, 5001):
        line = random.choice(pkgs).strip()
        line = line[:-1]
        pkg = json.loads(line)
        name = pkg["key"]
        final_pkgs += [name]

    print("Installing all packages locally...")
    for pkg in final_pkgs:
        print(f"Installing {pkg}")
        subprocess.run(["npm", "install", "--save", pkg])
    
    print("Done!")

if __name__ == "__main__":
    main()
