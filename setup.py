from setuptools import setup, find_packages
import subprocess

def install_requirements():
    subprocess.check_call(['pip', 'install', '-r', 'requirements.txt'])

def install_tools():
    tools = {
        "subfinder": "go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest",
        "assetfinder": "go install -v github.com/tomnomnom/assetfinder@latest",
        "findomain": (
            "curl -LO https://github.com/findomain/findomain/releases/latest/download/findomain-linux-i386.zip && "
            "unzip findomain-linux-i386.zip && "
            "chmod +x findomain && "
            "sudo mv findomain /usr/local/bin/findomain && "
            "rm findomain-linux-i386.zip"
        ),
        "amass": "go install -v github.com/owasp-amass/amass/v4/...@master || sudo apt install -y amass",
        "httpx": "go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest",
        "httpx-toolkit": "sudo apt install httpx-toolkit",
        "katana": "go install github.com/projectdiscovery/katana/cmd/katana@latest",
        "gau": "go install github.com/lc/gau/v2/cmd/gau@latest",
        "waybackurls": "go install github.com/tomnomnom/waybackurls@latest",
        "git": "sudo apt install -y git"
    }

    for tool, command in tools.items():
        try:
            subprocess.check_call(['which', tool])
            print(f"{tool} is already installed.")
        except subprocess.CalledProcessError:
            print(f"{tool} is not installed. Installing...")
            subprocess.check_call(command, shell=True)

def main():
    install_requirements()
    install_tools()

setup(
    name="HuntingPRO",
    version="3.7",
    packages=find_packages(),
    install_requires=[
        'requests',
        'argparse'
    ],
    entry_points={
        'console_scripts': [
            'huntingpro=huntingpro:main',
        ],
    },
    cmdclass={
        'install': main,
    }
)

if __name__ == "__main__":
    main()
