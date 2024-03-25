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

#Recon structure for all main domains
def recon_structure(scope):
    with open(scope, 'r') as file:
        for domain in file:
            # Remove leading / trailing whitespaces
            domain = domain.strip()
            
            # Create the root folder for the domain
            domain_path = os.path.join(".", domain)
            os.makedirs(domain_path, exist_ok=True)
            
            # Create subfolders within the root folder
            for folder_name in folder_names:
                folder_path = os.path.join(domain_path, folder_name)
                os.makedirs(folder_path, exist_ok=True)
                # print(f"{domain} - {folder_name} has been created")

def dns_resolvers():
    
    dns_resolver_command = f'dnsvalidator -tL https://public-dns.info/nameservers.txt -threads 100 -o /tmp/tmp-resolvers.txt'
    results = os.system(dns_resolver_command)

    dns_resolver_command_filter =  f'cat /tmp/tmp-resolvers.txt | head -n 700 > /tmp/recon-resolvers.txt'
    results = os.system(dns_resolver_command_filter)

#dns enumeration chaos
def passive_dns_enumeration_chaos(scope):
    with open(scope,'r') as file:
        for domain in file:
            domain = domain.strip()

            command = [
                'sh', '-c', f'chaos -d {domain} -o {domain}/sources/chaos.txt -silent'
            ]

            print(f"chaos -d {domain} - In Progress ")

            results = subprocess.run(command, text=True, stdout=subprocess.PIPE)
            print(results.stdout)

def passive_dns_enumeration_subfinder(scope):
    with open(scope,'r') as file:
        for domain in file:
            domain = domain.strip()

            command = [
                'sh', '-c', f'subfinder -d {domain} -o {domain}/sources/subfinder.txt -silent'
            ]
            
            print(f"subfinder -d {domain} - In Progress ")
            results = subprocess.run(command, text=True, stdout=subprocess.PIPE)
            
            print(results.stdout)

def passive_dns_enumeration_assetfinder(scope):
    with open(scope,'r') as file:
        for domain in file:
            domain = domain.strip()

            command = [
                'sh', '-c', f'assetfinder -subs-only {domain} | anew {domain}/sources/assetfinder.txt -silent'
            ]

            print(f"assetfinder -subs-only {domain} - In Progress ")
            
            results = subprocess.run(command, text=True, stdout=subprocess.PIPE)    
            print(results.stdout)

def passive_dns_enumeration_crobat(scope):
    with open(scope,'r') as file:
        for domain in file:
            domain = domain.strip() 

            command = [
                'sh', '-c', f'crobat -s {domain} | anew {domain}/sources/crobat.txt'
            ]

            print(f"crobat -s {domain} - In Progress ")
            results = subprocess.run(command, text=True, stdout=subprocess.PIPE)    
            
            print(results.stdout)

def passive_dns_enumeration_amass(scope):
    with open(scope,'r') as file:
        for domain in file:
            domain = domain.strip()

            command = [
                'sh', '-c', f'amass enum -passive -d {domain} -silent'
            ]

            print(f"amass enum -passive -d {domain} - In Progress ")
            results = subprocess.run(command, text=True, stdout=subprocess.PIPE)        
            print(results.stdout)
             
def passive_dns_enumeration_github(scope):
    with open(scope,'r') as file:
        for domain in file:
            domain = domain.strip()

            command = [
                'sh', '-c', f'github-subdomains -d {domain} -t {github_token} -o {domain}/sources/github-subdomains.txt'
            ]

            print(f"github-subdomains -d {domain} - In Progress ")
            
            results = subprocess.run(command, text=True, stdout=subprocess.PIPE)    
            print(results.stdout)

def passive_dns_enumeration_collection(scope):
    with open(scope,'r') as file:
        for domain in file:
            domain = domain.strip()            
            
            oam_subs_command = [
                'oam_subs', '-d', domain, '--names', '-o', f'{domain}/sources/amass-passive.txt'
                ]

            print(f"oam_subs -d {domain} --names")
            results = subprocess.run(oam_subs_command, text=True, stdout=subprocess.PIPE)

            # Collecting all domains from all sources
            cat_command = f'cat {domain}/sources/*.txt | anew {domain}/sources/all.txt'

            print(f"Collecting all passive subdomains in all.txt ")
            results = subprocess.run(cat_command, shell=False, text=True, stdout=subprocess.PIPE)

def resolve_domains(scope):
    with open(scope, 'r') as file:
        for domain in file:
            domain = domain.strip() 

            resolve_dns_command = f'cat {domain}/sources/*.txt | dnsx -silent | anew {domain}/domains.txt'
            print(f"valid dns in progress - {domain}")
            results = os.system(resolve_dns_command)
            # print(results)

def active_dns_enumeration_amass(scope):
    with open(scope, 'r') as file:
        for domain in file:
            domain = domain.strip()

            amass_active_command = f'amass enum -active -d {domain} -timeout 60 -nf {domain}/domains.txt'
            
            print(f"Active subdomains enumeration - Amass -d {domain} ")
            results = os.system(amass_active_command)

def active_dns_enumeration_dnscan(scope):
    with open(scope, 'r') as file:
        for domain in file:
            domain = domain.strip()

            #dnscan running in active mode
            dns_command = f"python3 /root/tools/dnscan/dnscan.py -w {dns_wordlist} -t 30 -v -D -o {domain}/sources/dnscan/dnscan.txt -r -d {domain}"
        
            print(f" dnscan -d {domain} ")
            results = os.system(dns_command)
        
            #collecting dnscan domains
            dnscan_command = f'cat {domain}/sources/dnscan/dnscan.txt | grep "{domain}" | awk "{{print $1}}" | grep -v "*" | anew {domain}/sources/dnscan.txt | dnsx -silent | anew {domain}/domains.txt '
                        
            print(f"Collecting dnscan results for {domain} ")
            results = os.system(dnscan_command)

def active_dns_enumeration_OneForAll(scope):
    with open(scope,'r') as file:
        for domain in file:
            domain = domain.strip()            
            
            # Collecting all domains from all sources
            OneForAll_command = f'python3 /root/tools/OneForAll/oneforall.py --target {domain} run'

            # print(f"OneForAll subdomains - {domain} ")
            results = subprocess.run(OneForAll_command, shell=False, text=True, stdout=subprocess.PIPE)
            print(results.stderr)

            # Construct the command as a string
            cat_OneForAll_command = f'cat /root/tools/OneForAll/results/temp/collected_subdomains_{domain}_*.txt | unfurl format %d | anew {domain}/sources/oneforall.txt | dnsx -silent | anew {domain}/domains.txt | anew {domain}/new.txt'

            # Use subprocess.PIPE to capture the output
            results_oneforall = subprocess.run(cat_OneForAll_command, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            # Print the output
            print(f"OneForAll subdomains finished - {domain}\n")

def dns_bruteforce_gotator():
    with open(scope, 'r') as file:
        for domain in file:
            domain = domain.strip()

            gotator_command_domains = f'gotator -sub {domain}/domains.txt -mindup -silent -perm {perm_wordlist} -depth 1 | head -c 1G | anew {domain}/Recon/gotator/gotator.txt'
            gotator_command_domains_resolve = f'cat {domain}/Recon/gotator/gotator.txt | puredns resolve -q -r /root/resolvers.txt| anew {domain}/domains.txt | anew {domain}/new.txt | anew {domain}/Recon/gotator/new.txt'
            
            print(f"httpx - {domain}")
            results_gotator_domains = os.system(gotator_command_domains)
            results_gotator_domains_resolve = os.system(gotator_command_domains_resolve)

            # print(results)

def http_probe():
    with open(scope, 'r') as file:
        for domain in file:
            domain = domain.strip()

            http_probe_command = f'cat {domain}/domains.txt | dnsx -silent | httpx -silent | anew {domain}/Recon/httpx.txt | anew {domain}/Recon/new.txt'

            print(f"httpx - {domain}")
            results = os.system(http_probe_command)       
            # print(results)

def execute_task(task):
    try:
        result = task.result()
        # Process the result if needed
    except Exception as e:
        print(f'Error in task: {e}')

def passive_concurrent_request(scope):
    with concurrent.futures.ThreadPoolExecutor() as executor:

        passive_tasks = [executor.submit(passive_dns_enumeration_chaos, domain) for domain in scope.split()] + [executor.submit(passive_dns_enumeration_subfinder, domain) for domain in scope.split()] + [executor.submit(passive_dns_enumeration_assetfinder, domain) for domain in scope.split()] + [executor.submit(passive_dns_enumeration_crobat, domain) for domain in scope.split()] + [executor.submit(passive_dns_enumeration_github, domain) for domain in scope.split()] + [executor.submit(passive_dns_enumeration_amass, domain) for domain in scope.split()] + [executor.submit(active_dns_enumeration_dnscan, domain) for domain in scope.split()] + [executor.submit(active_dns_enumeration_amass, domain) for domain in scope.split()]
        
        #[executor.submit(dns_resolvers)] +        
        for completed_task in concurrent.futures.as_completed(passive_tasks):
            execute_task(completed_task)

def active_concurrent_request(scope):
    with concurrent.futures.ThreadPoolExecutor() as executor:

        active_tasks = [executor.submit(active_dns_enumeration_dnscan, domain) for domain in scope.split()] + [executor.submit(active_dns_enumeration_amass, domain) for domain in scope.split()] + [executor.submit(active_dns_enumeration_OneForAll, domain) for domain in scope.split()]
          
        for completed_task in concurrent.futures.as_completed(active_tasks):
            execute_task(completed_task)

#taking argument
scope = sys.argv[1]

#Main function to execute all other functions.
def main():
        #Calling Functions
        recon_structure(scope)  
        passive_concurrent_request(scope)
        resolve_domains(scope)
        
        dns_bruteforce_gotator()
        active_concurrent_request(scope)
        resolve_domains(scope)
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
    print(f'Script execution time: ' + total_time )

