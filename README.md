# Hunting Pro

Hunting Pro is a powerful subdomain enumeration and URL extraction tool designed for security professionals. It performs comprehensive subdomain discovery using multiple sources, checks for active subdomains, extracts URLs with various tools, and identifies sensitive files and JavaScript files. The tool consolidates findings into detailed reports, streamlining the reconnaissance process for effective security assessments and vulnerability detection.

## Features

- Subdomain Enumeration: Utilizes multiple tools including Subfinder, Assetfinder, Findomain, CRT.sh, and Amass to discover subdomains.
- Alive Subdomain Checking: Uses httpx-toolkit to check which discovered subdomains are actively responding.
- URL Extraction: Extracts URLs from live subdomains using Katana, gau, and Waybackurls to gather potential attack surfaces.
- Merging and Deduplication: Consolidates and removes duplicate URLs for a cleaner dataset.
- Sensitive File Discovery: Identifies potentially sensitive files such as configuration files, backups, logs and more
- JavaScript File Extraction: Extracts JavaScript files from the collected URLs to analyze potential security issues in client-side code.
- Detailed Reporting: Generates a comprehensive report summarizing all findings and results.

# Resources
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)

## Requirements

- [Python 3.x](https://www.python.org/downloads/)
- [Go 1.16+](https://go.dev/doc/install) (for some tools)

# Installation

### Step 1: Clone the repository
```bash
git clone https://github.com/suhailm-in/HuntingPro.git
```
```bash
cd HuntingPro
```

### Step 2: Install Python packages
```bash
pip3 install -r requirements.txt
```

### Step 3: Install external tools
```
chmod +x install_tools.sh
```
```
./install_tools.sh
```

## Usage
- To enumerate subdomains for a single domain:
```
python3 huntingPro.py -d example.com
```
- To enumerate subdomains for multiple domains from a file:
```
python3 hunterpro.py -t url.txt
```
- Enumerate subdomains for a single domain with a custom timeout:
```
python3 hunterpro.py -d example.com -s 180
```

### Options

- -d, --domain: The target domain for active enumeration
- -t, --target-file: File containing a list of target domains for passive enumeration
- -s, --seconds: Timeout in seconds for each tool (default: 120 seconds)

### Output

The tool generates a folder named Result containing the results. Inside this folder, you will find:

- subdomains.txt: List of subdomains
- subdomains_alive.txt: List of alive subdomains
- katana_urls.txt: URLs extracted using Katana
- gau_urls.txt: URLs extracted using gau
- waybackurls.txt: Historical URLs extracted using Waybackurls
- all_urls.txt: Merged and deduplicated URLs
- sensitive_files.txt: Extracted sensitive files
- js_files.txt: Extracted JavaScript files
- report.txt: Detailed report

## License
This project is Licensed under the GNU GPLv3 - see the [LICENSE](LICENSE) for more information.


## Acknowledgements

- [Subfinder](https://github.com/projectdiscovery/subfinder)
- [Assetfinder](https://github.com/tomnomnom/assetfinder)
- [Findomain](https://github.com/Findomain/Findomain)
- [Amass](https://github.com/owasp-amass/amass)
- [httpx-toolkit](https://github.com/projectdiscovery/httpx)
- [Katana](https://github.com/projectdiscovery/katana)
- [gau](https://github.com/lc/gau)
- [Waybackurls](https://github.com/tomnomnom/waybackurls)

## Developed by
### Suhail M 
Ethical Hacker, Penetration Tester, and AI Researcher in Cybersecurity
<h3 align="left">Connect with me:</h3>
<p align="left">
<a href="https://twitter.com/suhailm_in" target="blank"><img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/twitter.svg" alt="suhailm_online" height="30" width="40" /></a>
<a href="https://linkedin.com/in/suhailm-in" target="blank"><img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/linked-in-alt.svg" alt="suhailm-online" height="30" width="40" /></a></p>


























