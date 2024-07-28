#!/bin/bash

# Check if Go is installed
if ! [ -x "$(command -v go)" ]; then
  echo 'Error: Go is not installed.' >&2
  sudo apt install golang-go
fi

# Function to install a tool if not already installed
install_tool() {
    if ! [ -x "$(command -v $1)" ]; then
        echo "$1 is not installed. Installing..."
        eval $2
    else
        echo "$1 is already installed."
    fi
}

# Install tools
install_tool "subfinder" "go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest"
install_tool "assetfinder" "go install -v github.com/tomnomnom/assetfinder@latest"
install_tool "findomain" "curl -LO https://github.com/findomain/findomain/releases/latest/download/findomain-linux-i386.zip && unzip findomain-linux-i386.zip && chmod +x findomain && sudo mv findomain /usr/local/bin/findomain && rm findomain-linux-i386.zip"
install_tool "amass" "go install -v github.com/owasp-amass/amass/v4/...@master || sudo apt install -y amass"
install_tool "httpx" "go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest"
install_tool "httpx-toolkit" "sudo apt install httpx-toolkit"
install_tool "katana" "go install github.com/projectdiscovery/katana/cmd/katana@latest"
install_tool "gau" "go install github.com/lc/gau/v2/cmd/gau@latest"
install_tool "waybackurls" "go install github.com/tomnomnom/waybackurls@latest"
install_tool "git" "sudo apt install -y git"
