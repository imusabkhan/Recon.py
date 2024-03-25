#!/bin/python3

import time
from datetime import datetime, timedelta
import sys
import os
import subprocess
import shlex
from threading import Lock #import the Lock type
import concurrent.futures


#Record start time of the script
start_time = time.perf_counter()

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
                "Recon/files",
                "Recon/cloudenum"]

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
                print(f"{domain} - {folder_name} has been created")


def cloud_enum():
    with open(scope, 'r') as file:
        for domain in file:
            domain = domain.strip()
            
            command = f'echo {domain} | unfurl format %r'
            temp_domain = subprocess.check_output(command, shell=False, text=True)
            cloud_enum_command = f'python3 /root/tools/cloud_enum/cloud_enum.py -k {temp_domain} -l {domain}/Recon/cloudenum/cloudenum.txt'

            print(f'cloud enumeration - {temp_domain}')
            results = os.system(cloud_enum_command)       
            print(results)

            notify_command = f'cat {domain}/Recon/cloudenum/cloudenum.txt | notify -silent'
            results_cloudenum = subprocess.run(notify_command, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            print(results_cloudenum.stderr)

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


recon_structure(scope)
cloud_enum()

#end time
end_time = time.perf_counter()

#Calculating total script executing time
total_time = start_time - end_time

elapsed_timedelta = timedelta(seconds=total_time)
baseline_datetime = datetime.utcfromtimestamp(0)
elapsed_time_timedelta = baseline_datetime + elapsed_timedelta
formatted_time = elapsed_time_timedelta.strftime("%I:%M:%S %p")
print(f'Script execution time: ' + str({formatted_time}) )
