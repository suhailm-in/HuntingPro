#!/bin/bash

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Install Subfinder
if command_exists subfinder; then
    echo "Subfinder is already installed."
else
    echo "Installing Subfinder..."
    GO111MODULE=on go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
    
fi

# Install Assetfinder
if command_exists assetfinder; then
    echo "Assetfinder is already installed."
else
    echo "Installing Assetfinder..."
    GO111MODULE=on go install -v github.com/tomnomnom/assetfinder@latest
fi

# Install Findomain
if command_exists findomain; then
    echo "Findomain is already installed."
else
    echo "Installing Findomain..."
    curl -LO https://github.com/findomain/findomain/releases/latest/download/findomain-linux-i386.zip
    unzip findomain-linux-i386.zip
    chmod +x findomain
    sudo mv findomain /usr/local/bin/findomain
    rm findomain-linux-i386.zip
fi

# Install Amass
if command_exists amass; then
    echo "Amass is already installed."
else
    echo "Installing Amass..."
    GO111MODULE=on go install -v github.com/owasp-amass/amass/v4/...@master
fi

# Install Httpx
if command_exists httpx; then
    echo "Httpx is already installed."
else
    echo "Installing Httpx..."
    GO111MODULE=on go install github.com/projectdiscovery/httpx/cmd/httpx@latest
fi

# Install Httpx-toolkit
if command_exists httpx-toolkit; then
    echo "Httpx-toolkit is already installed."
else
    echo "Installing Httpx-toolkit..."
    sudo apt install httpx-toolkit
fi

# Install Katana
if command_exists katana; then
    echo "Katana is already installed."
else
    echo "Installing Katana..."
    GO111MODULE=on go install github.com/projectdiscovery/katana/cmd/katana@latest
fi

# Install Gau
if command_exists gau; then
    echo "Gau is already installed."
else
    echo "Installing Gau..."
    GO111MODULE=on go install -v github.com/lc/gau/v2/cmd/gau@latest
fi

# Install Waybackurls
if command_exists waybackurls; then
    echo "Waybackurls is already installed."
else
    echo "Installing Waybackurls..."
    GO111MODULE=on go install github.com/tomnomnom/waybackurls@latest
fi

echo "All tools installed successfully."

