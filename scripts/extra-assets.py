#!/bin/python3

import time
import sys
import os
import subprocess
from threading import Lock #import the Lock type

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
                "Recon/screens",
                "Recon/assets",
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

def extra_assets():
    with open(scope,'r') as file:
        for domain in file:
            domain = domain.strip()

            extra_assets_command = [
                'sh', '-c', f'gf urls {domain}/ | unfurl format %d | grep "{domain}" | sort -fiu | dnsx -silent | anew {domain}/domains.txt | anew {domain}/Recon/assets/dns-new.txt | httpx -silent | anew {domain}/Recon/httpx.txt | anew {domain}/Recon/assets/httpx-new.txt'
            ]

            print(f"Looking for extra assets in response / JS File - {domain} ")
            
            extra_assets_command_results = subprocess.run(extra_assets_command, text=True, stdout=subprocess.PIPE)    
            print(extra_assets_command_results.stdout)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python recon.py scope.txt")
        sys.exit(1)

    #taking argument
    scope = sys.argv[1]
    recon_structure()
    extra_assets()

    if not os.path.isfile(scope):
        print(f'Error: File {scope} not found')
        sys.exit(1)
