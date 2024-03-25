#!/bin/python3

import sys
import os
import subprocess

def rustports(scope):
    with open(scope,'r') as file:
        for domain in file:
            domain = domain.strip()            
            

            print("target: " + str(domain))
            # # Rust scan in progress
            # rustports_command = f'rustscan -a {domain}/domains.txt --range 1-65535 --ulimit 5000 | grep "Open" | tee {domain}/temp/ports.txt'

            # print(f"Rust Scan in Progress - {domain} ")
            # rust_results_one = subprocess.run(rustports_command, shell=False, text=True, stdout=subprocess.PIPE)
            # print(rust_results_one.stdout)

            rustports_command_results = f"cat {domain}/temp/ports.txt | awk '{{print $2}}' | httpx -silent -o {domain}/temp/httpx-ports.txt | anew {domain}/Recon/httpx.txt | notify -silent" 
            # | anew {domain}/Recon/httpx.txt | notify -silent"
            print(f"Running httpx on ports - {domain}")

            # Use subprocess.run to execute the command
            rustports_results = subprocess.run(rustports_command_results, shell=False)

            # Print the output and errors
            print("Command output:", rustports_results)

#taking argument
scope = sys.argv[1]
rustports(scope)
