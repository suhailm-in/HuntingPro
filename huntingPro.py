import subprocess
import requests
import json
import argparse
import os
import signal
import time
from datetime import datetime


def run_command(command, timeout=None, tool_name=None):
    try:
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if timeout:
            try:
                stdout, stderr = process.communicate(timeout=timeout)
                if process.returncode == 0:
                    return stdout.splitlines()
                else:
                    print(f"[!] {tool_name} failed with return code {process.returncode}")
                    print(stderr)
                    return []
            except subprocess.TimeoutExpired:
                print(f"[!] {tool_name} timed out after {timeout} seconds")
                os.kill(process.pid, signal.SIGINT)  # Send SIGINT signal
                time.sleep(1)  # Wait for 1 second
                os.kill(process.pid, signal.SIGTERM)  # Send SIGTERM signal
                return []
        else:
            stdout, stderr = process.communicate()
            if process.returncode == 0:
                return stdout.splitlines()
            else:
                print(f"[!] {tool_name} failed with return code {process.returncode}")
                print(stderr)
                return []
    except Exception as e:
        print(f"Error executing command: {e}")
        return []


def subfinder_enum(domain=None, target_file=None):
    if target_file:
        command = f"subfinder -dL {target_file} -all -recursive"
    elif domain:
        command = f"subfinder -d {domain} -silent -all -recursive"
    else:
        return []
    return run_command(command, timeout, "Subfinder")


def assetfinder_enum(domain):
    command = f"assetfinder --subs-only {domain}"
    return run_command(command, timeout, "Assetfinder")


def findomain_enum(domain):
    command = f"findomain -t {domain} -q"
    return run_command(command, timeout, "Findomain")


def crtsh_enum(domain):
    crtsh_url = f"https://crt.sh/?q=%25.{domain}&output=json"
    response = requests.get(crtsh_url)
    subdomains = set()
    if response.status_code == 200:
        data = json.loads(response.text)
        for entry in data:
            if 'name_value' in entry:
                subdomains.update(entry['name_value'].split('\n'))
    return list(subdomains)


def amass_enum(domain):
    command = f"amass enum -passive -d {domain}"
    return run_command(command, timeout, "Amass")


def merge_subdomains(output_file, folder):
    all_files = [
        os.path.join(folder, 'subfinder.txt'),
        os.path.join(folder, 'assetfinder.txt'),
        os.path.join(folder, 'findomain.txt'),
        os.path.join(folder, 'crtsh.txt'),
        os.path.join(folder, 'amass.txt')
    ]
    subdomains = set()

    for file in all_files:
        if os.path.exists(file):
            with open(file, 'r') as f:
                subdomains.update([line.strip() for line in f.readlines()])

    with open(output_file, 'w') as f:
        for subdomain in sorted(subdomains):
            f.write(f"{subdomain}\n")


def create_result_folder():
    result_folder = "Result"
    if not os.path.exists(result_folder):
        os.makedirs(result_folder)
    return result_folder


def create_output_folder(domain):
    date_str = datetime.now().strftime('%Y%m%d')
    base_folder_name = f"{domain}_{date_str}"
    counter = 1

    result_folder = create_result_folder()
    while os.path.exists(os.path.join(result_folder, f"{base_folder_name}_{counter}")):
        counter += 1

    folder_name = f"{base_folder_name}_{counter}"
    os.makedirs(os.path.join(result_folder, folder_name), exist_ok=True)
    return os.path.join(result_folder, folder_name)


def enumerate_domain(domain, folder_name):
    subdomains = set()

    print(f"[*] Starting Subfinder Enumeration for {domain}...")
    subfinder_output = subfinder_enum(domain=domain)
    subfinder_file = os.path.join(folder_name, 'subfinder.txt')
    with open(subfinder_file, 'a') as f:
        f.write('\n'.join(subfinder_output) + '\n')
    subdomains.update(subfinder_output)
    print(f"[*] Subfinder results saved to subfinder.txt")

    print("[*] Starting Assetfinder Enumeration...")
    assetfinder_output = assetfinder_enum(domain)
    assetfinder_file = os.path.join(folder_name, 'assetfinder.txt')
    with open(assetfinder_file, 'a') as f:
        f.write('\n'.join(assetfinder_output) + '\n')
    subdomains.update(assetfinder_output)
    print(f"[*] Assetfinder results saved to assetfinder.txt")

    print("[*] Starting Findomain Enumeration...")
    findomain_output = findomain_enum(domain)
    findomain_file = os.path.join(folder_name, 'findomain.txt')
    with open(findomain_file, 'a') as f:
        f.write('\n'.join(findomain_output) + '\n')
    subdomains.update(findomain_output)
    print(f"[*] Findomain results saved to findomain.txt")

    print("[*] Fetching Subdomains from CRT.sh...")
    crtsh_output = crtsh_enum(domain)
    crtsh_file = os.path.join(folder_name, 'crtsh.txt')
    with open(crtsh_file, 'a') as f:
        f.write('\n'.join(crtsh_output) + '\n')
    subdomains.update(crtsh_output)
    print(f"[*] CRT.sh results saved to crtsh.txt")

    print("[*] Starting Amass Enumeration...")
    amass_output = amass_enum(domain)
    amass_file = os.path.join(folder_name, 'amass.txt')
    with open(amass_file, 'a') as f:
        f.write('\n'.join(amass_output) + '\n')
    subdomains.update(amass_output)
    print(f"[*] Amass results saved to amass.txt")

    return subdomains


def check_alive_subdomains(input_file, output_file):
    command = f"cat {input_file} | httpx-toolkit -ports 80,443,8080,8000,8888 -threads 200 > {output_file}"
    run_command(command)
    print(f"[*] Alive subdomains saved to subdomains_alive.txt")


def extract_urls_with_katana(input_file, output_file):
    command = f"katana -u {input_file} -d 5 -ps -pss waybackarchive,commoncrawl,alienvault -kf -jc -fx -ef woff,css,png,svg,jpg,woff2,jpeg,gif,svg -o {output_file}"
    run_command(command)
    print(f"[*] Katana URLs saved to katana_urls.txt")


def extract_urls_with_gau(input_file, output_file):
    command = f"cat {input_file} | gau --threads 20 --subs --o {output_file}"
    run_command(command, tool_name="gau")
    print(f"[*] gau URLs saved to gau_urls.txt")


def extract_urls_with_waybackurls(domain, output_file):
    command = f"waybackurls {domain} >> {output_file}"
    run_command(command)
    print(f"[*] Wayback URLs saved to waybackurls.txt")


def merge_and_deduplicate_urls(output_file, *input_files):
    command = f"cat {' '.join(input_files)} | sort -u > {output_file}"
    run_command(command)
    print(f"[*] Merged and deduplicated URLs saved to all_urls.txt")


def extract_sensitive_files(input_file, output_file):
    command = f"cat {input_file} | grep -E '\\.txt|\\.log|\\.cache|\\.secret|\\.db|\\.backup|\\.yml|\\.json|\\.gz|\\.rar|\\.zip|\\.config' > {output_file}"
    run_command(command)
    print(f"[*] Sensitive files saved to sensitive_files.txt")


def extract_js_files(input_file, output_file):
    command = f"cat {input_file} | grep -E '\\.js$' > {output_file}"
    run_command(command)
    print(f"[*] JavaScript files saved to js_files.txt")


def count_lines(file_path):
    try:
        with open(file_path, 'r') as f:
            return sum(1 for _ in f)
    except FileNotFoundError:
        return 0


def generate_report(folder_name):
    subdomains_count = count_lines(os.path.join(folder_name, 'subdomains.txt'))
    alive_subdomains_count = count_lines(os.path.join(folder_name, 'subdomains_alive.txt'))
    katana_urls_count = count_lines(os.path.join(folder_name, 'katana_urls.txt'))
    gau_urls_count = count_lines(os.path.join(folder_name, 'gau_urls.txt'))
    waybackurls_count = count_lines(os.path.join(folder_name, 'waybackurls.txt'))
    all_urls_count = count_lines(os.path.join(folder_name, 'all_urls.txt'))
    sensitive_files_count = count_lines(os.path.join(folder_name, 'sensitive_files.txt'))
    js_files_count = count_lines(os.path.join(folder_name, 'js_files.txt'))

    report_file = os.path.join(folder_name, 'report.txt')
    current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    with open(report_file, 'w') as f:
        f.write(print_title() + "\n")
        f.write("Report :\n")
        f.write(f"Report Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("===============================================================\n\n")
        f.write(f"Subdomains ({subdomains_count}): subdomains.txt\n")
        f.write(f"Alive Subdomains ({alive_subdomains_count}): subdomains_alive.txt\n")
        f.write(f"Katana URLs ({katana_urls_count}): katana_urls.txt\n")
        f.write(f"GAU URLs ({gau_urls_count}): gau_urls.txt\n")
        f.write(f"Wayback URLs ({waybackurls_count}): waybackurls.txt\n")
        f.write(f"All URLs (merged and deduplicated) ({all_urls_count}): all_urls.txt\n")
        f.write(f"Sensitive Files ({sensitive_files_count}): sensitive_files.txt\n")
        f.write(f"JavaScript Files ({js_files_count}): js_files.txt\n")
        f.write(f"\nResults saved in folder: {folder_name}\n")

    print(f"[*] Report generated: report.txt")


def print_title():
    title = """               
 _   _             _   _               ____
| | | |_   _ _ __ | |_(_)_ __   __ _  |  _ \ _ __ ___
| |_| | | | | '_ \| __| | '_ \ / _` | | |_) | '__/ _ \ 
|  _  | |_| | | | | |_| | | | | (_| | |  __/| | | (_) |
|_| |_|\__,_|_| |_|\__|_|_| |_|\__, | |_|   |_|  \___/
                               |___/

                Tool name : Hunting Pro
                Version   : 3.7
                Developed by @ SUHAIL M

    """
    return (title)


def main():
    # Print the title
    print(print_title())

def update_tool():
    try:
        # Change this to your tool's repository URL
        repo_url = "https://github.com/suhailm-in/HuntingPro.git"
        # Check if the script is running from a git repository
        if os.path.exists(".git"):
            print("[*] Updating Hunting Pro...")
            command = f"git pull {repo_url}"
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate()
            if process.returncode == 0:
                print("[*] Hunting Pro has been updated successfully.")
            else:
                print(f"[!] Update failed with return code {process.returncode}")
                print(stderr)
        else:
            print("[-] This script is not running from a git repository. Update manually from the GitHub repository.")
    except Exception as e:
        print(f"Error updating tool: {e}")

def main():
    # Print the title
    print(print_title())
    parser = argparse.ArgumentParser(description='Hunting Pro - Subdomain Enumeration Tool')
    parser.add_argument('-d', '--domain', help='The target domain for active enumeration')
    parser.add_argument('-t', '--target-file', help='File containing a list of target domains for passive enumeration')
    parser.add_argument('-s', '--seconds', type=int, default=120, help='Timeout in seconds for each tool (default: 120 seconds)')
    parser.add_argument('-u', '--update', action='store_true', help='Update Hunting Pro to the latest version')
    args = parser.parse_args()

    global timeout
    timeout = args.seconds

    domain = args.domain
    target_file = args.target_file

    if not domain and not target_file:
        print("[-] Please specify either a domain or a target file.")
        return

    if domain:
        folder_name = create_output_folder(domain)
        subdomains = enumerate_domain(domain, folder_name)
    elif target_file:
        folder_name = create_output_folder("targets")
        with open(target_file, 'r') as f:
            domains = [line.strip() for line in f.readlines()]
        subdomains = set()
        for domain in domains:
            subdomains.update(enumerate_domain(domain, folder_name))

    # Merge subdomains from different sources and deduplicate
    final_output_file = os.path.join(folder_name, 'subdomains.txt')
    print("[*] Merging and Deduplicating Subdomains...")
    merge_subdomains(final_output_file, folder_name)
    print(f"[*] Merged subdomains saved to subdomains.txt")

    # Check alive subdomains
    alive_subdomains_file = os.path.join(folder_name, 'subdomains_alive.txt')
    print("[*] Checking alive subdomains...")
    check_alive_subdomains(final_output_file, alive_subdomains_file)

    # Extract URLs with katana
    katana_output_file = os.path.join(folder_name, 'katana_urls.txt')
    print("[*] Extracting URLs with Katana...")
    extract_urls_with_katana(alive_subdomains_file, katana_output_file)

    # Extract URLs with gau
    gau_output_file = os.path.join(folder_name, 'gau_urls.txt')
    print("[*] Extracting URLs with gau...")
    extract_urls_with_gau(alive_subdomains_file, gau_output_file)

    # Extract URLs with waybackurls
    waybackurls_output_file = os.path.join(folder_name, 'waybackurls.txt')
    print("[*] Extracting historical URLs with Waybackurls...")
    extract_urls_with_waybackurls(domain, waybackurls_output_file)

    # Merge and deduplicate URLs
    all_urls_output_file = os.path.join(folder_name, 'all_urls.txt')
    print("[*] Merging and Deduplicating URLs...")
    merge_and_deduplicate_urls(all_urls_output_file, katana_output_file, gau_output_file, waybackurls_output_file)

    # Extract sensitive files
    sensitive_files_output_file = os.path.join(folder_name, 'sensitive_files.txt')
    print("[*] Extracting sensitive files...")
    extract_sensitive_files(all_urls_output_file, sensitive_files_output_file)

    # Extract JavaScript files
    js_files_output_file = os.path.join(folder_name, 'js_files.txt')
    print("[*] Extracting JavaScript files...")
    extract_js_files(all_urls_output_file, js_files_output_file)

    print(f"[*] Subdomain enumeration completed. Results saved to {folder_name}")

    # Generate the report
    generate_report(folder_name)


if __name__ == "__main__":
    main()
