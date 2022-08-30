# AutoVPN

# Setup

Before running AutoVPN you must have python3, pip and OpenVPN installed.
After installation copy `example.config.yml` into `config.yml` and set up 
your API keys for each provider you wish to use.

Next, open a terminal in the project folder (where `requirements.txt` is)
and run `pip install -r requirements.txt`.

Now you're ready to use AutoVPN.

# Usage

# Development

## Add provider
In order to implement a new provider you need to perform these steps:
1. Implement the provider as a class that extends the Provider class (preferably inside the providers package)
2. Implement inherited functions
3. Add lowercase provider name to global providers variable in autovpn.py
4. Add case for this provider in autovpn.get_provider()
