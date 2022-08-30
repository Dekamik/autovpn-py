# AutoVPN

# Setup

## 1: Install Python

Python is required to run this script.

You should be able to find it here: https://www.python.org/downloads/
or install it through a package manager on Linux.

## 2: Install OpenVPN

OpenVPN is required to connect to the VPN server.

**Note:** This script doesn't support "OpenVPN Connect", you need to install 
the "OpenVPN" CLI tool.
If you're on Windows, you should find installers etc. here: 
https://openvpn.net/community-downloads/

## 3: Install script dependencies

Open a terminal inside the project folder (where `requirements.txt` is)
and run `pip install -r requirements.txt`.

AutoVPN is now installed.

# Usage

# Development

## Add provider
In order to implement a new provider you need to perform these steps:
1. Implement the provider as a class that extends the Provider class (preferably inside the providers package)
2. Implement inherited functions
3. Add lowercase provider name to global providers variable in autovpn.py
4. Add case for this provider in autovpn.get_provider()
