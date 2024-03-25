#!/bin/python3

import sys
import os
import subprocess
import shlex
import threading
from threading import Lock #import the Lock type
import concurrent.futures

def nuclei_scan(scope):
    with open(scope,'r') as file:
        for domain in file:
            domain = domain.strip()            
            
            # nuclei scan in progress
            nuclei_update_command = f'nuclei --update -ut -silent'
            nuclei_scan_command = f'cat {domain}/Recon/httpx.txt | nuclei -t /root/nuclei-templates/  -o {domain}/Recon/nuclei/nuclei.txt'

            # print(f"Nuclei Scan - {domain} ")
            nuclei_update_command_results = subprocess.run(nuclei_update_command, shell=False, text=True, stdout=subprocess.PIPE)
            nuclei_scan_command_results = subprocess.run(nuclei_scan_command, shell=False, text=True, stdout=subprocess.PIPE)
            print(nuclei_scan_command_results.stdout)

#taking argument
scope = sys.argv[1]

nuclei_scan(scope)
