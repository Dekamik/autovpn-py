# AutoVPN

A tool for cheaper VPN connections.

This tool provisions single-session VPN servers at chosen VPS providers. Then it 
automatically connects to the VPN server and destroys the VPN server when you
disconnect from the session.

## Table of contents
- [1. Setup](#setup)
	- [1.1 Install Python](#1-install-python)
	- [1.2 Install OpenVPN](#2-install-openvpn)
	- [1.3 Install script dependencies](#3-install-script-dependencies)
- [2. Usage](#usage)
- [3. Development](#development)
	- [3.1 Add provider](#add-provider)
- [4. FAQ](#faq)
	- [4.1 Why should I use AutoVPN?](#why-should-i-use-autovpn)
	- [4.2 Why should I NOT use AutoVPN?](#why-should-i-not-use-autovpn)
	- [4.3 I want to watch Netflix/Disney+ in another country, will this tool help me?](#i-want-to-watch-netflixdisney-in-another-country-will-this-tool-help-me)
	- [4.4 Will this tool hide me from hackers?](#will-this-tool-hide-me-from-hackers)
	- [4.5 Will this tool hide me from the government?](#will-this-tool-hide-me-from-the-government)

# Setup

## 1: Install Python

Python is required to run this script.

You should be able to find it here: https://www.python.org/downloads/ or install 
it through a package manager.

## 2: Install OpenVPN

OpenVPN is required to connect to the VPN server.

**Note:** This script doesn't support "OpenVPN Connect", you need to install 
the "OpenVPN" CLI tool.
If you're on Windows, you should find installers etc. here: 
https://openvpn.net/community-downloads/

## 3: Install script dependencies

Open a terminal/command prompt inside the project folder (where 
`requirements.txt` is) and run `pip install -r requirements.txt`.

# Usage

OpenVPN must be run as a privileged user/root and handles escalation differently
depending on platform:

* **Linux/OSX**: If not already run as root, the script will prompt for your 
                 password and pipe it to the sudo command's stdin.
* **Windows**: The script asks for administrator privileges through UAC, and then
               opens the VPN tunnel in a separate Powershell window.

```
Usage: autovpn.py <provider> <region>  Provision a VPN server at <provider> on <region> and connects to it
       autovpn.py <provider> regions   Lists all regions at <provider>
       autovpn.py providers            Lists all available providers
       autovpn.py (-h | --help)        Shows further help and options
```

# Development

## Add provider
To implement a new provider you must do these steps:
1. Implement the provider as a class that extends the Provider class (preferrably 
   inside the providers package)
2. Implement inherited functions
3. Add lowercase provider name to global providers variable in autovpn.py
4. Add case for this provider in autovpn.get_provider()

# FAQ

## Why should I use AutoVPN?

### It's cheaper

Instead of paying over $10 per month, you only pay for what you use. Meaning 
you will only spend tens of cents per month for a slightly better service.

### No logs

The installation sets OpenVPN to not log anything on the server. If that's not
enough, the whole VPN server is automatically destroyed after you disconnect,
so it will leave little trace of your activities.

### Better privacy (if you know what you're doing)

You have better control over your VPN servers and better oversight over the tech 
stacks behind them. You can choose VPS providers that use secure and updated 
virtualization technology for maximum protection against hackers.

As of 2022-09-01, Linode is the recommended default, since they use KVM for
hardware virtualization, which is up-to-date and has fewer security 
vulnerabilities compared to other vendors.

That said: other vendors should be fine for single-sessions, despite 
vulnerabilities.

## Why should I NOT use AutoVPN?

### Fewer countries to choose from

Most VPN providers have a lot of countries to connect to, almost all of them 
in-fact. With AutoVPN, the countries and regions you can choose from is limited
by the locations of the provider's data centers, so the specific country you want
to connect to may not be available.

### Doesn't protect from government actors

If you want to hide your activity from agencies like the NSA or the FSB, this alone 
won't hide your activity from government actors.

### May not be able to connect to the VPS provider from some countries

Some countries may block the VPS resources needed and thus this may not work in
these countries.

## I want to watch Netflix/Disney+ in another country, will this tool help me?

Yes! This tool will let you connect to datacenters across the world and spoof 
your IP address in the process. Those websites won't know you're browsing from a 
different country.

## Will this tool hide me from hackers?

Partially yes. For most people this will be enough to hide your activity on public 
Wi-Fi at e.g. cafés, airports, etc. If you're browsing from your home Wi-Fi, it 
won't make a difference.

**Remember**: this won't help against other attack vectors, like rubber duckys,
phishing emails, password leaks etc. To mitigate that you must revise your 
overall operational security (OpSec).

## Will this tool hide me from the government?

No. If they want to find you, they *will* find you. If this is your concern, you must 
revise your threat model.

Even if the server gets destroyed and even if they're not somehow tapping into your
traffic (which we can assume), they could probably access your billing information,
the ip addresses and the timestamps for the servers you create for your sessions.
