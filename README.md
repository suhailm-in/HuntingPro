# Hunting Pro

Hunting Pro is a comprehensive subdomain enumeration and URL extraction tool designed to identify subdomains, check for alive subdomains, and extract URLs for further analysis. It uses various subdomain enumeration tools and integrates URL extraction methods to provide a detailed report of the target domain.

## Features

- Subdomain enumeration using multiple tools (Subfinder, Assetfinder, Findomain, CRT.sh, Amass)
- Check for alive subdomains using httpx-toolkit
- Extract URLs using Katana, gau, and Waybackurls
- Merge and deduplicate URLs
- Extract sensitive files and JavaScript files from URLs
- Generate a detailed report

## Requirements

- Python 3.x
- Go 1.16+ (for some tools)

## Installation

### Step 1: Clone the repository

```bash
git clone https://github.com/yourusername/hunting-pro.git
cd hunting-pro
```

### Step 2: Install Python packages

```bash
pip3 install -r requirements.txt
```

### Step 3: Install external tools

```
chmod +x install_tools.sh
./install_tools.sh
```

## Usage
### Basic Usage

To enumerate subdomains for a single domain:
```
python3 huntingPro.py -d example.com
```

To enumerate subdomains for multiple domains from a file:
```
python3 hunterpro.py -t url.txt
```

Enumerate subdomains for a single domain with a custom timeout:
```
python3 hunterpro.py -d example.com -s 180
```

### Options

- -d, --domain: The target domain for active enumeration
- -t, --target-file: File containing a list of target domains for passive enumeration
- -s, --seconds: Timeout in seconds for each tool (default: 120 seconds)

## Output

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
This project is licensed under the MIT License - see the LICENSE file for details.


## Acknowledgements

Subfinder
Assetfinder
Findomain
Amass
httpx-toolkit
Katana
gau
Waybackurls

## Developed by
SUHAIL M
Ethical Hacker, Penetration Tester, and AI Researcher in Cybersecurity














