#!/bin/bash

# Install Subfinder
echo "Installing Subfinder..."
GO111MODULE=on go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest

# Install Assetfinder
echo "Installing Assetfinder..."
go get -u github.com/tomnomnom/assetfinder

# Install Findomain
echo "Installing Findomain..."
curl -LO https://github.com/Findomain/Findomain/releases/latest/download/findomain-linux
chmod +x findomain-linux
sudo mv findomain-linux /usr/local/bin/findomain

# Install Amass
echo "Installing Amass..."
GO111MODULE=on go install -v github.com/OWASP/Amass/v3/...@master

# Install Httpx-toolkit
echo "Installing Httpx-toolkit..."
GO111MODULE=on go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest

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
