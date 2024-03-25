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
                "Recon/crawler",
                "Recon/crawler/gospider",
                "Recon/crawler/hakrawler",
                "Recon/crawler/katana",
                "Recon/fuzz",
                "Recon/wordpress",
                "Recon/javascript",
                "Recon/dnsgen",
                "Recon/files",
                "Recon/cloudenum"]

#Recon structure for all main domains
def recon_structure():
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

#Gospider crawler function
def crawler_go_spider(scope):
    with open(scope,'r') as file:
        for domain in file:
            domain = domain.strip()

            #Gospider command to crawl
            print("Gospider in Progress !!")
            go_spider_command = f'gospider -S {domain}/Recon/httpx.txt -o {domain}/Recon/crawler/gospider/output -c 10 -d 10 --other-source --include-subs'

            #Execute Gospider
            go_spider_results = subprocess.run(go_spider_command, shell=False, text=True, stdout=subprocess.PIPE)
            print(go_spider_results.stdout)

#Hakrawler crawler function
def crawler_hakrawler(scope):
    with open(scope,'r') as file:
        for domain in file:
            domain = domain.strip()

            #Hakrawler command to crawl
            print("Hakrawler in Progress !!")
            hakrawler_command = f'cat {domain}/Recon/httpx.txt | hakrawler -subs -d 10 -json | anew {domain}/Recon/crawler/hakrawler/hakrawler.txt'

            #Execute Hakrawler
            hakrawler_command_results = subprocess.run(hakrawler_command, shell=False, text=True, stdout=subprocess.PIPE)
            print(hakrawler_command_results.stdout)

            hakrawler_command_output = f'cat {domain}/Recon/crawler/hakrawler/hakrawler.txt | jq -r ".URL" | sort -fiu | anew {domain}/Recon/crawler/hakrawler/urls.txt' 
            hakrawler_command_output_results = subprocess.run(hakrawler_command_output, shell=False, text=True, stdout=subprocess.PIPE)
            print(hakrawler_command_output_results.stdout)

#Katana crawler function
def crawler_katana(scope):
    with open(scope,'r') as file:
        for domain in file:
            domain = domain.strip()

            #Katana command to crawl
            print("Katana in Progress !!")
            katana_command = f'katana -list {domain}/Recon/httpx.txt -d 10 -ef png,css,jpeg,jpg,woff,woff2,ico,ttf,ttf2,svg -jc -kf -aff -o {domain}/Recon/crawler/katana/katana_results.txt -silent'

            #Execute Katana
            katana_command_results = subprocess.run(katana_command, shell=False, text=True, stdout=subprocess.PIPE)
            print(katana_command_results.stdout)

            katana_command_output = f'mv katana_field {domain}/Recon/crawler/katana/' 
            katana_command_output_results = subprocess.run(katana_command_output, shell=False, text=True, stdout=subprocess.PIPE)

#nuclei for crawler results
def crawler_nuclei_scanner():
    with open(scope,'r') as file:
        for domain in file:
            domain = domain.strip()

            #nuclei crawler command
            print(f'Nuclei is running on Katana Results - {domain} !!')
            crawler_nuclei_command = f'cat {domain}/Recon/crawler/katana/katana_results.txt | httpx -silent | nuclei -t /root/nuclei-templates/ -o {domain}/Recon/nuclei/nuclei-crawler.txt -silent | notify -silent'

            #Execute nuclei crawler command
            crawler_nuclei_command_results = subprocess.run(crawler_nuclei_command, shell=False, text=True, stdout=subprocess.PIPE)
            print(crawler_nuclei_command_results.stdout)

def execute_task(task):
    try:
        result = task.result()
        # Process the result if needed
    except Exception as e:
        print(f'Error in task: {e}')

#Concurrent request for Crawlers [Katana, Hakrawler, Gospider]
def crawler_concurrent_request(scope):
    with concurrent.futures.ThreadPoolExecutor() as executor:

        passive_tasks = [executor.submit(crawler_katana, domain) for domain in scope.split()] + [executor.submit(crawler_go_spider, domain) for domain in scope.split()] + [executor.submit(crawler_hakrawler, domain) for domain in scope.split()] 
        
        #[executor.submit(dns_resolvers)] +        
        for completed_task in concurrent.futures.as_completed(passive_tasks):
            execute_task(completed_task)

#default function to execute
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python recon.py scope.txt")
        sys.exit(1)

    #taking argument
    scope = sys.argv[1]

    recon_structure()
    crawler_concurrent_request(scope)
    crawler_nuclei_scanner()
    
    if not os.path.isfile(scope):
        print(f'Error: File {scope} not found')
        sys.exit(1)
        
