#!/bin/bash

# Script to install ChromeDriver for browser automation

echo "Installing ChromeDriver..."

# Check if Chrome is installed
if ! command -v google-chrome &> /dev/null; then
    echo "Chrome is not installed. Please install Chrome first:"
    echo "sudo apt update && sudo apt install google-chrome-stable"
    exit 1
fi

# Get Chrome version
CHROME_VERSION=$(google-chrome --version | awk '{print $3}' | awk -F'.' '{print $1}')
echo "Chrome version: $CHROME_VERSION"

# Download ChromeDriver
CHROMEDRIVER_VERSION=$(curl -s "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_VERSION")
echo "ChromeDriver version: $CHROMEDRIVER_VERSION"

# Download and install ChromeDriver
wget -O /tmp/chromedriver.zip "https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip"
unzip /tmp/chromedriver.zip -d /tmp/
sudo mv /tmp/chromedriver /usr/local/bin/
sudo chmod +x /usr/local/bin/chromedriver

echo "ChromeDriver installed successfully!"
echo "You can now use the --browser option to create problems from your browser tabs." 