#!/bin/python3

import time
import sys
import os
import subprocess
import shlex
from threading import Lock #import the Lock type
import concurrent.futures


#Record start time of the script
start_time = time.perf_counter()

github_token = "your_github_token"
dns_wordlist = "dns_wordlist.txt"
perm_wordlist = "perm_wordlist.txt"

folder_names = ["temp",
                "Recon",
                "sources",
                "Recon/oneforall",
                "sources/dnscan",
                "Recon/gotator",
                "Recon/nuclei",
                "Recon/gf",
                "Recon/wordlist",
                "Recon/nmap",
                "Recon/gospider",
                "Recon/fuzz",
                "Recon/wordpress",
                "Recon/javascript",
                "Recon/dnsgen",
                "Recon/files"]


def http_probe():
    with open(scope, 'r') as file:
        for domain in file:
            domain = domain.strip()

            http_probe_command = f'cat {domain}/domains.txt | dnsx -silent | httpx -silent -sr -srd {domain}/Recon/output -follow-host-redirects | anew {domain}/Recon/httpx.txt | anew {domain}/Recon/new.txt | notify -silent'

            print(f"httpx - {domain}")
            results = os.system(http_probe_command)       
            # print(results)

def execute_task(task):
    try:
        result = task.result()
        # Process the result if needed
    except Exception as e:
        print(f'Error in task: {e}')

def active_concurrent_request(scope):
    with concurrent.futures.ThreadPoolExecutor() as executor:

        active_tasks = [executor.submit(http_probe, domain) for domain in scope.split()] 
          
        for completed_task in concurrent.futures.as_completed(active_tasks):
            execute_task(completed_task)

#taking argument
scope = sys.argv[1]

#Main function to execute all other functions.
def main():
        #Calling Functions
        http_probe()

#default function to execute
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python recon.py scope.txt")
        sys.exit(1)

    #taking argument
    scope = sys.argv[1]

    if not os.path.isfile(scope):
        print(f'Error: File {scope} not found')
        sys.exit(1)

    #Calling Functions
    main()
    end_time = time.perf_counter()
    total_time =  start_time - end_time
    print(f'Script execution time: ' + str(total_time) )
