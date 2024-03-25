# Recon.py
This is my personal multi-threaded reconnaissance script written in Python for bug hunting.

## Usage

### Using recon.py
The `recon.py` script in this repository can be used for performing reconnaissance on a specified scope using the following command:

```bash
python3 recon.py scope.txt
```

## Summary
The `recon.py` script in this repository performs the following tasks:

1. **Active/Passive Subdomain Enumeration:**
   - Utilizes various tools for discovering subdomains within a specified scope.

2. **Finding Valid Subdomains:**
   - Searches for valid subdomains.

3. **Filtering Web Applications:**
   - Filters out web applications running on default ports 80/443 using httpx.

4. **Finding Vulnerabilities:**
   - Uses nuclei to find low-hanging fruits and vulnerabilities, then sends output notifications to Discord, Slack, or email via notify.

5. **Port Scanning and Filtering:**
   - Performs port scans on discovered domains using rustscan and filters out web servers running on non-default ports. 

6. **Asset Discovery in Cloud Environments:**
   - Discovers assets in cloud environments using cloudenum and sends output notifications to Discord, Slack, or email via notify.

7. **Crawling Valid Assets:**
   - Utilizes tools like katana, hakrawler, and gospider to crawl valid discovered assets for endpoints, JavaScript files, and new subdomains.

Feel free to explore and customize these scripts and tools based on your specific needs. Contributions and feedback are welcome!

**Note:** I personally use this script on my Digital Ocean VPS and have not tested it on my local network.

## DigitalOcean Referral

If you're interested in trying out DigitalOcean for hosting your projects, you can sign up using [this referral link](https://m.do.co/c/6b4b1bf0f63e). By using this link, you'll get some free credits to start with.

[Sign up on DigitalOcean](https://m.do.co/c/6b4b1bf0f63e)

# Reconnaissance Toolbox

This repository contains a collection of tools for reconnaissance and information gathering during security assessments.

## Tools List

Each tool in this repository serves a specific purpose in reconnaissance and information gathering. Refer to the respective GitHub repositories for installation instructions, usage examples, and additional details about each tool.

1. [dnsvalidator](https://github.com/vortexau/dnsvalidator): A tool for validating and verifying DNS records.

2. [chaos](https://github.com/projectdiscovery/chaos-client): A subdomain discovery tool that uses multiple DNS sources to discover subdomains.

3. [subfinder](https://github.com/projectdiscovery/subfinder): A tool designed to find subdomains using passive methods.

4. [assetfinder](https://github.com/tomnomnom/assetfinder): A tool for finding domains and subdomains related to a given domain.

5. [crobat](https://github.com/Cgboal/SonarSearch): A tool that leverages Sonar data to find subdomains.

6. [amass](https://github.com/OWASP/Amass): An open-source intelligence tool for discovering subdomains.

7. [github-subdomains](https://github.com/gwen001/github-subdomains): A tool to discover subdomains from GitHub repositories.

8. [oam_subs](https://github.com/Artem117/oam_subs): A tool for enumerating Oracle Access Manager endpoints.

9. [dnsx](https://github.com/projectdiscovery/dnsx): A fast DNS enumeration and resolution tool.

10. [dnscan](https://github.com/rbsec/dnscan): A tool to gather information about a domain including subdomains and open ports.

11. [oneforall](https://github.com/shmilylty/OneForAll): A tool for subdomain enumeration that integrates multiple techniques.

12. [Gotator](https://github.com/Josue87/gotator): A DNS subdomain scanner with multi-threading support.

13. [httpx](https://github.com/projectdiscovery/httpx): A fast and multi-purpose HTTP toolkit.

14. [nuclei](https://github.com/projectdiscovery/nuclei): A fast and customizable vulnerability scanner based on templates.

15. [rustscan](https://github.com/RustScan/RustScan): A fast port scanner written in Rust.

16. [notify](https://github.com/projectdiscovery/notify): A simple tool for sending notifications via different mediums.

17. [cloudenum](https://github.com/initstring/cloud_enum): A tool for finding out information about cloud environments.

18. [Gospider](https://github.com/jaeles-project/gospider): A tool for web crawling and fingerprinting.

19. [Hakrawler](https://github.com/hakluke/hakrawler): A simple, fast web crawler designed for easy, quick discovery of endpoints and assets within a web application.

20. [Katana](https://github.com/projectdiscovery/katana): A next-generation crawling and spidering framework.

21. [anew](https://github.com/tomnomnom/anew): A tool for comparing two lists of lines in a file and outputting the differences.


## Social Profiles

- [YouTube](https://www.youtube.com/musabkhan)
- [LinkedIn](https://www.linkedin.com/in/musab1995/)
- [Twitter](https://twitter.com/Musab1995)
- [Facebook](https://facebook.com/imusabkhan)
- [HackerOne](https://hackerone.com/musabkhan)

## Disclaimer

Usage of these tools for unauthorized access or any malicious activity is strictly prohibited. Use them responsibly and with proper authorization.



