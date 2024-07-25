#!/bin/bash

# Install Subfinder
echo "Installing Subfinder..."
GO111MODULE=on go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest

# Install Assetfinder
echo "Installing Assetfinder..."
go get -u github.com/tomnomnom/assetfinder

# Install Findomain
echo "Installing Findomain..."
curl -LO https://github.com/findomain/findomain/releases/latest/download/findomain-linux-i386.zip
unzip findomain-linux-i386.zip
chmod +x findomain
sudo mv findomain /usr/local/bin/findomain
rm findomain-linux-i386.zip

# Install Amass
echo "Installing Amass..."
GO111MODULE=on go install -v github.com/owasp-amass/amass/v4/...@master

# Install Httpx-toolkit
echo "Installing Httpx"
GO111MODULE=on go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest

# Install Httpx-toolkit
echo "Installing Httpx-toolkit..."
sudo apt install httpx-toolkit

# Install Katana
echo "Installing Katana..."
GO111MODULE=on go install github.com/projectdiscovery/katana/cmd/katana@latest

# Install Gau
echo "Installing Gau..."
GO111MODULE=on go install -v github.com/lc/gau/v2/cmd/gau@latest

# Install Waybackurls
echo "Installing Waybackurls..."
go get -u github.com/tomnomnom/waybackurls

echo "All tools installed successfully."
