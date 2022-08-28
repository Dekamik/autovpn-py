"""
AutoVPN

Automatically provisions and de-provisions single-use VPN servers for one-shot VPN sessions.

Usage: autovpn.py up [ -k API_KEY | --key API_KEY ] [ -t SLUG | --type SLUG ] PROVIDER REGION
       autovpn.py regions PROVIDER
       autovpn.py providers
       autovpn.py (-h | --help)
       autovpn.py --version

Commands:
  up PROVIDER REGION  create and connect to VPN endpoint at PROVIDER on REGION
  regions PROVIDER    list available regions for PROVIDER
  providers           list available providers

Arguments:
  PROVIDER  VPS provider to use
  REGION    VPS provider region on which to create VPN endpoint

Options:
  -k --key API_KEY  specify API key
  -t --type SLUG    specify instance type slug to use as server
  -h --help         show help
  --version         show version
"""
import sys

from docopt import docopt
import yaml

from providers.exceptions import ProviderError
from providers.linode import Linode
from providers.base import Provider
from provisioning.agent import Agent


def is_provider_defined(provider, config) -> bool:
    return provider in config["providers"]


def get_provider(provider_arg, api_key) -> Provider:
    if provider_arg == "linode":
        return Linode(api_key)
    raise ValueError(f"{provider_arg} is not a supported provider")


def get_key(args, config):
    key = args["--key"]
    if key:
        return key

    provider_arg = args["PROVIDER"]
    if not is_provider_defined(provider_arg, config):
        print(f"{provider_arg} is not a supported provider")
        sys.exit(1)

    key = config["providers"][provider_arg]["key"]
    if not key:
        print("API key must be defined in command or in config file")
        sys.exit(1)

    return key


def up(args, config):
    key = get_key(args, config)
    provider_arg = args["PROVIDER"]
    authorized_keys = config["authorized_keys"]

    try:
        region = args["REGION"]
        type_slug = args["--type"] or config["providers"][provider_arg]["type_slug"]
        provider = get_provider(provider_arg, key)

        print("Creating server...")
        instance = provider.create_server(region, type_slug, authorized_keys)

        try:
            agent = Agent()

            print("Installing OpenVPN server...")
            agent.install_vpn_server()

            print("Connecting to OpenVPN server...")
            agent.vpn_connect()

        finally:
            print("Destroying server...")
            provider.destroy_server(instance)

    except (ProviderError, ValueError) as ex:
        print(ex)
        sys.exit(1)


def show_regions(args, config):
    key = get_key(args, config)
    provider_arg = args["PROVIDER"]

    if not is_provider_defined(provider_arg, config):
        print(f"{provider_arg} is not a supported provider")
        sys.exit(1)

    print("Downloading regions...")
    provider = get_provider(provider_arg, key)
    regions = provider.get_regions(True)
    print(*regions, sep="\n")


def show_providers(config):
    print(*config["providers"].keys(), sep="\n")


def main():
    with open("./config.yml", "r") as stream:
        config = yaml.safe_load(stream)

    args = docopt(__doc__)

    if args["up"]:
        up(args, config)

    elif args["regions"]:
        show_regions(args, config)

    elif args["providers"]:
        show_providers(config)

    sys.exit(0)


if __name__ == '__main__':
    main()
